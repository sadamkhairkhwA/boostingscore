/**
 * IELTS Academic Reading Test 1 — client-side navigation, timer, marking.
 */
(function () {
  "use strict";

  var app = document.getElementById("art-app");
  var dataEl = document.getElementById("art-data");
  if (!app || !dataEl) return;

  var DATA = JSON.parse(dataEl.textContent);
  var SUBMIT_URL = app.getAttribute("data-submit-url") || "";
  var TESTS_URL = app.getAttribute("data-tests-url") || "/reading/tests/";
  var INDEX_URL = app.getAttribute("data-index-url") || TESTS_URL;
  var isDrill = !!(DATA.singlePart);

  var currentPart = isDrill ? DATA.part || 1 : 1;
  var answers = {};
  var submitted = false;
  var timeLeft = DATA.timeLimitSeconds || 3600;
  var timerId = null;
  var startTs = Date.now();

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function iconTile(slug, variant, size) {
    return typeof BSIcons !== "undefined" ? BSIcons.tile(slug, variant, size || "sm") : "";
  }
  function iconInline(slug, kind) {
    return typeof BSIcons !== "undefined" ? BSIcons.inline(slug, kind || "ok") : "";
  }
  function iconWarn() {
    return typeof BSIcons !== "undefined" ? BSIcons.warn() : "";
  }

  function getCsrfToken() {
    var inp = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return inp ? inp.value : "";
  }

  function normGap(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/£/g, "");
  }

  function answerMatches(q, raw) {
    var t = q.type;
    if (t === "match" || t === "tfng" || t === "ynng" || t === "para_match") {
      return String(raw || "").trim().toLowerCase() === String(q.correct || "").trim().toLowerCase();
    }
    if (t === "mc") {
      var letter = String(raw || "").trim().toUpperCase().charAt(0);
      return letter === String(q.correct || "").trim().toUpperCase();
    }
    var opts = (q.accepted && q.accepted.length ? q.accepted : [q.correct]).map(normGap);
    return opts.indexOf(normGap(raw)) >= 0;
  }

  function formatTime(secs) {
    var m = Math.floor(secs / 60);
    var s = secs % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function setTimerDisplay() {
    var el = document.getElementById("art-timer");
    var box = document.getElementById("art-timer-box");
    if (!el || !box) return;
    el.textContent = formatTime(Math.max(0, timeLeft));
    if (timeLeft <= 300 && timeLeft > 0) {
      box.classList.add("art-topbar__timer-box--warn");
    } else {
      box.classList.remove("art-topbar__timer-box--warn");
    }
  }

  function startTimer() {
    if (timerId) clearInterval(timerId);
    setTimerDisplay();
    timerId = setInterval(function () {
      if (submitted) return;
      timeLeft -= 1;
      if (timeLeft <= 0) {
        timeLeft = 0;
        setTimerDisplay();
        clearInterval(timerId);
        timerId = null;
        submitTest(true);
        return;
      }
      setTimerDisplay();
    }, 1000);
  }

  function isAnswered(q) {
    var v = answers[q.id];
    return v != null && String(v).trim() !== "";
  }

  function updateNavStates() {
    for (var i = 1; i <= 40; i++) {
      var btn = document.querySelector('.art-qnav-btn[data-q="' + i + '"]');
      if (!btn) continue;
      btn.classList.remove("art-qnav-btn--answered", "art-qnav-btn--correct", "art-qnav-btn--wrong", "art-qnav-btn--active");
      var q = DATA.questions.filter(function (x) {
        return x.id === i;
      })[0];
      if (!q) continue;
      if (submitted) {
        var ok = answerMatches(q, answers[i]);
        if (ok) btn.classList.add("art-qnav-btn--correct");
        else btn.classList.add("art-qnav-btn--wrong");
      } else if (isAnswered(q)) {
        btn.classList.add("art-qnav-btn--answered");
      }
    }
  }

  function setActiveNav(qid) {
    document.querySelectorAll(".art-qnav-btn").forEach(function (b) {
      b.classList.toggle("art-qnav-btn--active", parseInt(b.getAttribute("data-q"), 10) === qid);
    });
  }

  function scrollToQuestion(qid) {
    var q = DATA.questions.filter(function (x) {
      return x.id === qid;
    })[0];
    if (!q) return;
    if (q.part !== currentPart) {
      switchPart(q.part);
    }
    setActiveNav(qid);
    var el = document.getElementById("art-q-" + qid);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function switchPart(part) {
    currentPart = part;
    document.querySelectorAll(".art-tab").forEach(function (tab) {
      var p = parseInt(tab.getAttribute("data-part"), 10);
      var on = p === part;
      tab.classList.toggle("art-tab--active", on);
      tab.setAttribute("aria-selected", on ? "true" : "false");
    });
    var inst = document.getElementById("art-instruction");
    if (inst) inst.textContent = DATA.instructions[String(part)] || "";
    var pass = document.getElementById("art-passage");
    if (pass) pass.innerHTML = DATA.passages[String(part)] || "";
    renderQuestions(part);
    updateNavStates();
  }

  function pillTypes(q) {
    return q.type === "match" || q.type === "tfng" || q.type === "ynng" || q.type === "para_match";
  }

  function renderPills(q) {
    var opts = q.options || [];
    var cur = answers[q.id];
    var html =
      '<div class="art-pills" data-qid="' +
      q.id +
      '">' +
      opts
        .map(function (opt) {
          var sel = cur === opt;
          var cls = "art-pill";
          if (submitted) {
            if (answerMatches(q, opt) && cur === opt) cls += " art-pill--correct";
            else if (cur === opt) cls += " art-pill--wrong";
            else if (answerMatches(q, opt)) cls += " art-pill--correct";
          } else if (sel) cls += " art-pill--selected";
          return (
            '<button type="button" class="' +
            cls +
            '" data-value="' +
            escapeHtml(opt) +
            '">' +
            escapeHtml(opt) +
            "</button>"
          );
        })
        .join("") +
      "</div>";
    return html;
  }

  function renderMc(q) {
    var opts = q.options || [];
    var cur = answers[q.id];
    var html = '<div class="art-mc" data-qid="' + q.id + '">';
    opts.forEach(function (line, idx) {
      var letter = String.fromCharCode(65 + idx);
      var sel = cur === letter;
      var rowCls = "art-mc-row";
      if (submitted) {
        if (answerMatches(q, letter) && sel) rowCls += " art-mc-row--correct";
        else if (sel) rowCls += " art-mc-row--wrong";
        else if (answerMatches(q, letter)) rowCls += " art-mc-row--correct";
      } else if (sel) rowCls += " art-mc-row--selected";
      html +=
        '<div class="' +
        rowCls +
        '" data-letter="' +
        letter +
        '" role="button" tabindex="0">' +
        '<span class="art-mc-letter">' +
        letter +
        "</span>" +
        '<span class="art-mc-text">' +
        escapeHtml(line.replace(/^[A-D]\.\s*/, "")) +
        "</span></div>";
    });
    html += "</div>";
    return html;
  }

  function renderGap(q) {
    var v = answers[q.id] || "";
    var ok = submitted && answerMatches(q, v);
    var inpCls = "art-gap-input";
    if (submitted) {
      inpCls += ok ? " art-gap-input--correct" : " art-gap-input--wrong";
    }
    var html =
      '<div class="art-gap-row" data-qid="' +
      q.id +
      '">' +
      '<input type="text" class="' +
      inpCls +
      '" data-gap="' +
      q.id +
      '" name="art-q-' +
      q.id +
      '" autocomplete="off" autocapitalize="off" spellcheck="false" value="' +
      escapeHtml(v) +
      '" ' +
      (submitted ? "disabled" : "") +
      " />";
    html += "</div>";
    if (submitted) {
      html += explainHtml(q, ok, v);
    }
    return html;
  }

  function explainHtml(q, ok, userVal) {
    var cls = ok ? "art-explain art-explain--ok" : "art-explain art-explain--bad";
    var msg = q.explanation || "";
    if (!ok && q.correct != null) {
      msg += (msg ? " " : "") + "Correct answer: <strong>" + escapeHtml(String(q.correct)) + "</strong>.";
    }
    return '<div class="' + cls + '">' + msg + "</div>";
  }

  function renderSummaryRow(q) {
    var v = answers[q.id] || "";
    var ok = submitted && answerMatches(q, v);
    var inpCls = "art-gap-input";
    if (submitted) {
      inpCls += ok ? " art-gap-input--correct" : " art-gap-input--wrong";
    }
    var html =
      '<div class="art-q-block art-sum-row" id="art-q-' +
      q.id +
      '" data-q="' +
      q.id +
      '">' +
      '<div class="art-q-prompt"><span class="art-q-num">' +
      q.id +
      ".</span> Summary gap (max one word from the passage)</div>" +
      '<div class="art-gap-row">' +
      '<input type="text" class="' +
      inpCls +
      '" data-summary="' +
      q.id +
      '" name="art-sum-' +
      q.id +
      '" autocomplete="off" autocapitalize="off" spellcheck="false" value="' +
      escapeHtml(v) +
      '" ' +
      (submitted ? "disabled" : "") +
      " />";
    html += "</div>";
    if (submitted) {
      html += explainHtml(q, ok, v);
    }
    html += "</div>";
    return html;
  }

  function renderQuestions(part) {
    var host = document.getElementById("art-questions");
    if (!host) return;
    var qs = DATA.questions.filter(function (q) {
      return q.part === part;
    });
    var html = "";
    var lastHeading = null;
    var summaryBlockDone = false;

    qs.forEach(function (q) {
      if (q.section_heading !== lastHeading) {
        if (lastHeading !== null) html += "</div>";
        html += '<div class="art-q-section">';
        html += '<div class="art-q-section-title">' + escapeHtml(q.section_heading) + "</div>";
        if (q.section_subtype) {
          html += '<div class="art-q-section-sub">' + escapeHtml(q.section_subtype) + "</div>";
        }
        html += '<div class="art-q-instruction">' + escapeHtml(q.instruction) + "</div>";
        lastHeading = q.section_heading;
      }

      if (q.type === "summary" && !summaryBlockDone && part === 3) {
        html += '<div class="art-sum-wrap">' + (DATA.summaryIntroHtml || "") + "</div>";
        summaryBlockDone = true;
      }

      if (q.type === "summary") {
        html += renderSummaryRow(q);
      } else {
        html +=
          '<div class="art-q-block" id="art-q-' +
          q.id +
          '" data-q="' +
          q.id +
          '">' +
          '<div class="art-q-prompt"><span class="art-q-num">' +
          q.id +
          ".</span> " +
          escapeHtml(q.prompt) +
          "</div>";
        if (pillTypes(q)) {
          html += renderPills(q);
        } else if (q.type === "mc") {
          html += renderMc(q);
        } else if (q.type === "gap") {
          html += renderGap(q);
        }
        if (submitted && pillTypes(q)) {
          var ok = answerMatches(q, answers[q.id]);
          html += explainHtml(q, ok, answers[q.id]);
        }
        if (submitted && q.type === "mc") {
          html += explainHtml(q, answerMatches(q, answers[q.id]), answers[q.id]);
        }
        html += "</div>";
      }
    });
    if (lastHeading !== null) html += "</div>";
    host.innerHTML = html;
    bindQuestionHandlers(part);
    if (part === 3) {
      [37, 38, 39, 40].forEach(function (id) {
        syncSummarySlot(id, answers[id] || "");
      });
    }
  }

  function bindQuestionHandlers(part) {
    document.querySelectorAll(".art-pills").forEach(function (wrap) {
      var qid = parseInt(wrap.getAttribute("data-qid"), 10);
      wrap.querySelectorAll(".art-pill").forEach(function (btn) {
        btn.addEventListener("click", function () {
          if (submitted) return;
          var val = btn.getAttribute("data-value");
          answers[qid] = val;
          switchPart(part);
          updateNavStates();
        });
      });
    });
    document.querySelectorAll(".art-mc").forEach(function (wrap) {
      var qid = parseInt(wrap.getAttribute("data-qid"), 10);
      wrap.querySelectorAll(".art-mc-row").forEach(function (row) {
        function pick() {
          if (submitted) return;
          answers[qid] = row.getAttribute("data-letter");
          switchPart(part);
          updateNavStates();
        }
        row.addEventListener("click", pick);
        row.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            pick();
          }
        });
      });
    });
    document.querySelectorAll("input[data-gap]").forEach(function (inp) {
      inp.addEventListener("input", function () {
        var qid = parseInt(inp.getAttribute("data-gap"), 10);
        answers[qid] = inp.value;
        updateNavStates();
      });
    });
    document.querySelectorAll("input[data-summary]").forEach(function (inp) {
      inp.addEventListener("input", function () {
        var qid = parseInt(inp.getAttribute("data-summary"), 10);
        answers[qid] = inp.value;
        syncSummarySlot(qid, inp.value);
        updateNavStates();
      });
    });
  }

  function syncSummarySlot(qid, val) {
    var span = document.querySelector('.art-sum-slot[data-q="' + qid + '"]');
    if (!span) return;
    span.textContent = (val || "").trim() || String(qid);
  }

  function buildQnav() {
    var nav = document.getElementById("art-qnav");
    if (!nav) return;
    var groups = [
      { label: "Part 1", from: 1, to: 14 },
      { label: "Part 2", from: 15, to: 27 },
      { label: "Part 3", from: 28, to: 40 },
    ];
    nav.innerHTML = groups
      .map(function (g) {
        var btns = "";
        for (var n = g.from; n <= g.to; n++) {
          btns += '<button type="button" class="art-qnav-btn" data-q="' + n + '">' + n + "</button>";
        }
        return (
          '<div class="art-qnav-group"><span class="art-qnav-label">' +
          g.label +
          "</span>" +
          btns +
          "</div>"
        );
      })
      .join("");
    nav.querySelectorAll(".art-qnav-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var qid = parseInt(btn.getAttribute("data-q"), 10);
        scrollToQuestion(qid);
      });
    });
  }

  function bandFromScore(score) {
    if (score >= 39) return "9.0";
    if (score >= 37) return "8.5";
    if (score >= 35) return "8.0";
    if (score >= 33) return "7.5";
    if (score >= 30) return "7.0";
    if (score >= 27) return "6.5";
    if (score >= 23) return "6.0";
    if (score >= 19) return "5.5";
    if (score >= 15) return "5.0";
    return "Below 5.0";
  }

  function barClass(pct) {
    if (pct >= 70) return "art-results-bar__fill art-results-bar__fill--hi";
    if (pct >= 50) return "art-results-bar__fill art-results-bar__fill--mid";
    return "art-results-bar__fill art-results-bar__fill--lo";
  }

  var arReviewFilter = "wrong";
  var artResultsClickBound = false;

  function resultTriState(q) {
    if (!isAnswered(q)) return "skipped";
    if (answerMatches(q, answers[q.id])) return "correct";
    return "wrong";
  }

  function mistakeBucket(q) {
    var t = q.type;
    if (t === "match" || t === "para_match") return "Matching";
    if (t === "tfng") return "T/F/NG";
    if (t === "ynng") return "Y/N/NG";
    if (t === "mc") return "MC";
    if (t === "gap") return "Gap-fill";
    if (t === "summary") return "Summary";
    return "Other";
  }

  var MISTAKE_TIP = {
    Matching: "Scan all texts before choosing",
    "T/F/NG": "Watch for negatives and qualifiers",
    "Y/N/NG": "Don't confuse facts with opinions",
    MC: "Eliminate obviously wrong options first",
    "Gap-fill": "Copy exact words from the passage",
    Summary: "Use only words that appear in the passage",
  };

  var MISTAKE_ORDER = ["Matching", "T/F/NG", "Y/N/NG", "MC", "Gap-fill", "Summary"];

  function typePillLabel(q) {
    var b = mistakeBucket(q);
    if (b === "Matching" && q.type === "para_match") return "Para match";
    if (b === "T/F/NG") return "T/F/NG";
    if (b === "Y/N/NG") return "Y/N/NG";
    return b;
  }

  function formatAnswerDisplay(q, raw) {
    if (raw == null || String(raw).trim() === "") return "—";
    var t = q.type;
    if (t === "mc") return String(raw).trim().toUpperCase().charAt(0);
    return String(raw).trim();
  }

  function nextBandGoal(curScore) {
    var tiers = [
      { need: 15, band: "5.0" },
      { need: 19, band: "5.5" },
      { need: 23, band: "6.0" },
      { need: 27, band: "6.5" },
      { need: 30, band: "7.0" },
      { need: 33, band: "7.5" },
      { need: 35, band: "8.0" },
      { need: 37, band: "8.5" },
      { need: 39, band: "9.0" },
    ];
    for (var i = 0; i < tiers.length; i++) {
      if (curScore < tiers[i].need) return tiers[i];
    }
    return null;
  }

  function pickWeakestPart(p1, m1, p2, m2, p3, m3, meta) {
    var parts = [
      { n: 1, pct: p1 / m1, label: meta.part1Title || "Part 1 — Notices & accommodation" },
      { n: 2, pct: p2 / m2, label: meta.part2Title || "Part 2 — Flexible working" },
      { n: 3, pct: p3 / m3, label: meta.part3Title || "Part 3 — Bilingualism" },
    ];
    parts.sort(function (a, b) {
      if (a.pct !== b.pct) return a.pct - b.pct;
      return a.n - b.n;
    });
    return parts[0];
  }

  function partAdviceForWeakest(n) {
    if (n === 1) {
      return "those items reward careful scanning—underline numbers, prices, and age limits in each notice before you choose.";
    }
    if (n === 2) {
      return "Yes/No/Not Given often turns on one qualifying phrase about what the writer actually claims.";
    }
    return "paragraph matching is easier when you jot a 3–5 word gist label for each paragraph before you match statements.";
  }

  function buildBandTipCard(score, p1, m1, p2, m2, p3, m3, meta) {
    var goal = nextBandGoal(score);
    var w = pickWeakestPart(p1, m1, p2, m2, p3, m3, meta);
    if (!goal) {
      return (
        '<div class="art-results-tip">' +
        '<span class="art-results-tip__ic" aria-hidden="true">' + iconTile("lightbulb", "amber", "sm") + '</span>' +
        '<div class="art-results-tip__txt"><strong>Strong performance.</strong> You are already at or above the top target on this scale—keep balancing speed and accuracy across all three parts.</div></div>'
      );
    }
    var need = goal.need;
    var more = Math.max(0, need - score);
    var inner =
      "To reach Band " +
      goal.band +
      " you need " +
      need +
      " correct answers. You got " +
      score +
      " this attempt — you need " +
      more +
      " more. Your easiest gains are in " +
      w.label +
      " — " +
      partAdviceForWeakest(w.n);
    return (
      '<div class="art-results-tip">' +
      '<span class="art-results-tip__ic" aria-hidden="true">' + iconTile("lightbulb", "amber", "sm") + '</span>' +
      '<div class="art-results-tip__txt">' +
      escapeHtml(inner) +
      "</div></div>"
    );
  }

  function aggregateSkills(questions) {
    var m = {};
    questions.forEach(function (q) {
      var sk = q.skill || "";
      if (!m[sk]) m[sk] = { ok: 0, tot: 0 };
      m[sk].tot++;
      if (resultTriState(q) === "correct") m[sk].ok++;
    });
    return m;
  }

  function pickWeakestStrongestSkill(skillMap) {
    var keys = Object.keys(skillMap);
    var best = null;
    var worst = null;
    keys.forEach(function (k) {
      var o = skillMap[k];
      if (!o.tot) return;
      var pct = o.ok / o.tot;
      if (!worst || pct < worst.pct) worst = { key: k, pct: pct, ok: o.ok, tot: o.tot };
      if (!best || pct > best.pct) best = { key: k, pct: pct, ok: o.ok, tot: o.tot };
    });
    return { worst: worst, best: best };
  }

  function buildSkillsSection(questions) {
    var sm = aggregateSkills(questions);
    var order = [
      "Scanning for detail",
      "Identifying T/F/NG",
      "Identifying writer's view",
      "Recognising paraphrase",
      "Reading for gist (MC)",
    ];
    var rows = order
      .map(function (label) {
        var o = sm[label] || { ok: 0, tot: 0 };
        var pct = o.tot ? Math.round((100 * o.ok) / o.tot) : 0;
        return (
          '<div class="art-sk-row">' +
          '<div class="art-sk-row__label">' +
          escapeHtml(label) +
          "</div>" +
          '<div class="art-sk-row__bar"><div class="' +
          barClass(pct) +
          '" style="width:' +
          pct +
          '%"></div></div>' +
          '<div class="art-sk-row__num">' +
          o.ok +
          "/" +
          o.tot +
          "</div></div>"
        );
      })
      .join("");
    var ws = pickWeakestStrongestSkill(sm);
    var pills = "";
    if (ws.worst && ws.best) {
      pills =
        '<div class="art-sk-pills">' +
        '<span class="art-sk-pill art-sk-pill--bad">Weakest skill — ' +
        escapeHtml(ws.worst.key) +
        " — " +
        ws.worst.ok +
        "/" +
        ws.worst.tot +
        "</span>" +
        '<span class="art-sk-pill art-sk-pill--good">Strongest skill — ' +
        escapeHtml(ws.best.key) +
        " — " +
        ws.best.ok +
        "/" +
        ws.best.tot +
        "</span></div>";
    }
    return (
      '<section class="art-sk-card" aria-labelledby="art-sk-h">' +
      '<h2 class="art-sec-kicker" id="art-sk-h">Your reading skills this attempt</h2>' +
      rows +
      pills +
      "</section>"
    );
  }

  function aggregateMistakes(questions) {
    var m = {};
    MISTAKE_ORDER.forEach(function (k) {
      m[k] = { wrong: 0, tot: 0 };
    });
    questions.forEach(function (q) {
      var b = mistakeBucket(q);
      if (!m[b]) m[b] = { wrong: 0, tot: 0 };
      m[b].tot++;
      if (resultTriState(q) !== "correct") m[b].wrong++;
    });
    return m;
  }

  function buildMistakesSection(questions) {
    var mm = aggregateMistakes(questions);
    var rows = MISTAKE_ORDER.map(function (key) {
      var o = mm[key] || { wrong: 0, tot: 0 };
      var pctWrong = o.tot ? Math.round((100 * o.wrong) / o.tot) : 0;
      var tip = MISTAKE_TIP[key] || "";
      return (
        '<div class="art-mp-row">' +
        '<div class="art-mp-row__label">' +
        escapeHtml(key) +
        "</div>" +
        '<div class="art-mp-row__mid"><div class="art-mp-bar"><div class="art-mp-bar__fill" style="width:' +
        pctWrong +
        '%"></div></div>' +
        "<div>" +
        o.wrong +
        "/" +
        o.tot +
        " wrong</div></div>" +
        '<div class="art-mp-row__tip">' +
        escapeHtml(tip) +
        "</div></div>"
      );
    }).join("");
    return (
      '<section class="art-mp-card" aria-labelledby="art-mp-h">' +
      '<h2 class="art-sec-kicker" id="art-mp-h">Mistake patterns</h2>' +
      rows +
      "</section>"
    );
  }

  function tallyReviewCounts(questions) {
    var c = 0,
      w = 0,
      s = 0;
    questions.forEach(function (q) {
      var st = resultTriState(q);
      if (st === "correct") c++;
      else if (st === "skipped") s++;
      else w++;
    });
    return { correct: c, wrong: w, skipped: s };
  }

  function questionMatchesFilter(q, filt) {
    var st = resultTriState(q);
    if (filt === "wrong") return st === "wrong";
    if (filt === "correct") return st === "correct";
    return true;
  }

  function questionTitleLine(q) {
    if (q.type === "summary") {
      return "Summary completion — gap Q" + q.id + " (one word from the passage).";
    }
    return q.prompt || "";
  }

  function buildWrongReviewCard(q) {
    var ua = formatAnswerDisplay(q, answers[q.id]);
    var ca = formatAnswerDisplay(q, q.correct);
    var cm = (q.common_mistake || "").trim();
    var expl = (q.explanation || "").trim();
    var pref = (q.passage_ref || "").trim();
    var why = (q.why_wrong || "").trim();
    var skill = (q.skill || "").trim();
    return (
      '<div class="art-ar-card art-ar-card--wrong">' +
      '<div class="art-ar-card__head">' +
      '<span class="art-ar-card__x" aria-hidden="true">' + (typeof BSIcons !== "undefined" ? BSIcons.cross() : "") + '</span>' +
      '<div class="art-ar-card__qmain"><strong>Q' +
      q.id +
      "</strong> " +
      escapeHtml(questionTitleLine(q)) +
      "</div>" +
      '<span class="art-ar-type">' +
      escapeHtml(typePillLabel(q)) +
      "</span></div>" +
      '<div class="art-ar-row art-ar-row--answer">' +
      '<span class="art-ar-muted">Your answer</span> ' +
      '<span class="art-ar-pill art-ar-pill--bad">' +
      escapeHtml(ua) +
      "</span>" +
      ' <span class="art-ar-muted">→</span> ' +
      '<span class="art-ar-muted">Correct</span> ' +
      '<span class="art-ar-pill art-ar-pill--ok">' +
      escapeHtml(ca) +
      "</span>" +
      '<span class="art-ar-skill">' +
      escapeHtml(skill) +
      "</span></div>" +
      '<div class="art-ar-row art-ar-row--why"><span aria-hidden="true">' + iconInline("pin", "ok") + '</span> ' +
      '<span class="art-ar-why-pill">' +
      escapeHtml(why) +
      "</span></div>" +
      (expl
        ? '<div class="art-ar-row art-ar-row--explain"><span aria-hidden="true">' + iconInline("lightbulb", "warn") + '</span> ' + escapeHtml(expl) + "</div>"
        : "") +
      (pref
        ? '<div class="art-ar-row art-ar-row--quote"><span aria-hidden="true">' + iconInline("pin", "ok") + '</span> <span class="art-ar-muted">Find it in the passage:</span> “' +
          escapeHtml(pref) +
          '”</div>'
        : "") +
      (cm
        ? '<div class="art-ar-row art-ar-row--cm"><span aria-hidden="true">' + iconWarn() + '</span> <strong>Common mistake —</strong> ' +
          escapeHtml(cm) +
          "</div>"
        : "") +
      "</div>"
    );
  }

  function buildCorrectReviewCard(q) {
    var ua = formatAnswerDisplay(q, answers[q.id]);
    var skill = (q.skill || "").trim();
    var expl = (q.explanation || "").trim();
    var pref = (q.passage_ref || "").trim();
    var more =
      expl || pref
        ? '<details class="art-ar-more">' +
          '<summary class="art-ar-more__sum">Show explanation</summary>' +
          (expl
            ? '<div class="art-ar-row art-ar-row--explain art-ar-row--inmore"><span aria-hidden="true">' + iconInline("lightbulb", "warn") + '</span> ' +
              escapeHtml(expl) +
              "</div>"
            : "") +
          (pref
            ? '<div class="art-ar-row art-ar-row--quote art-ar-row--inmore"><span aria-hidden="true">' + iconInline("pin", "ok") + '</span> <span class="art-ar-muted">Find it in the passage:</span> “' +
              escapeHtml(pref) +
              '”</div>'
            : "") +
          "</details>"
        : "";
    return (
      '<div class="art-ar-card art-ar-card--correct">' +
      '<div class="art-ar-card__head">' +
      '<span class="art-ar-card__ok" aria-hidden="true">' + (typeof BSIcons !== "undefined" ? BSIcons.check() : "") + '</span>' +
      '<div class="art-ar-card__qmain"><strong>Q' +
      q.id +
      "</strong> " +
      escapeHtml(questionTitleLine(q)) +
      "</div>" +
      '<span class="art-ar-type">' +
      escapeHtml(typePillLabel(q)) +
      "</span>" +
      '<span class="art-ar-skill art-ar-skill--head">' +
      escapeHtml(skill) +
      "</span></div>" +
      '<div class="art-ar-row art-ar-row--answer">' +
      '<span class="art-ar-muted">Your answer</span> ' +
      '<span class="art-ar-pill art-ar-pill--ok">' +
      escapeHtml(ua) +
      "</span> " + (typeof BSIcons !== "undefined" ? BSIcons.check() : "") + " Correct</div>" +
      more +
      "</div>"
    );
  }

  function buildAnswerReviewInner(questions, filt) {
    var tc = tallyReviewCounts(questions);
    var pills =
      '<div class="art-ar-stats">' +
      '<span class="art-ar-stat art-ar-stat--ok">' + (typeof BSIcons !== "undefined" ? BSIcons.check() : "") + " " +
      tc.correct +
      " correct</span>" +
      '<span class="art-ar-stat art-ar-stat--bad">' + (typeof BSIcons !== "undefined" ? BSIcons.cross() : "") + " " +
      tc.wrong +
      " wrong</span>" +
      '<span class="art-ar-stat art-ar-stat--skip">— ' +
      tc.skipped +
      " skipped</span></div>";
    var filters =
      '<div class="art-ar-filters" role="tablist" aria-label="Filter answers">' +
      '<button type="button" role="tab" class="art-ar-filter' +
      (filt === "wrong" ? " art-ar-filter--on" : "") +
      '" data-ar-filter="wrong">Wrong only (' +
      tc.wrong +
      ")</button>" +
      '<button type="button" role="tab" class="art-ar-filter' +
      (filt === "all" ? " art-ar-filter--on" : "") +
      '" data-ar-filter="all">All 40</button>' +
      '<button type="button" role="tab" class="art-ar-filter' +
      (filt === "correct" ? " art-ar-filter--on" : "") +
      '" data-ar-filter="correct">Correct only (' +
      tc.correct +
      ")</button></div>";
    var partsHtml = [1, 2, 3]
      .map(function (part) {
        var pq = questions.filter(function (q) {
          return q.part === part;
        });
        pq.sort(function (a, b) {
          return a.id - b.id;
        });
        var shown = pq.filter(function (q) {
          return questionMatchesFilter(q, filt);
        });
        if (!shown.length && filt !== "all") return "";
        var meta = DATA.partMeta || {};
        var pm = meta[String(part)] || {};
        var label = (pm.label || "Part " + part) + " — " + (pm.subtitle || "");
        var rFrom = pm.q_start || pq[0].id;
        var rTo = pm.q_end || pq[pq.length - 1].id;
        var ok = 0;
        pq.forEach(function (q) {
          if (resultTriState(q) === "correct") ok++;
        });
        var inner = pq
          .filter(function (q) {
            return questionMatchesFilter(q, filt);
          })
          .map(function (q) {
            return resultTriState(q) === "correct" ? buildCorrectReviewCard(q) : buildWrongReviewCard(q);
          })
          .join("");
        if (!inner && filt !== "all") return "";
        var body =
          inner ||
          '<p class="art-ar-empty">No questions in this section for this filter.</p>';
        return (
          '<details class="art-ar-part" open>' +
          '<summary class="art-ar-part__sum">' +
          '<span class="art-ar-part__title">' +
          escapeHtml(label) +
          " Q" +
          rFrom +
          "–" +
          rTo +
          "</span>" +
          '<span class="art-ar-part__score">' +
          ok +
          "/" +
          pq.length +
          '</span><span class="art-ar-part__chev" aria-hidden="true"></span></summary>' +
          '<div class="art-ar-part__body">' +
          body +
          "</div></details>"
        );
      })
      .join("");
    if (!partsHtml.trim()) {
      partsHtml = '<p class="art-ar-empty">No answers match this filter.</p>';
    }
    return pills + filters + '<div class="art-ar-parts">' + partsHtml + "</div>";
  }

  function refreshAnswerReview() {
    var host = document.getElementById("art-ar-host");
    if (!host) return;
    host.innerHTML = buildAnswerReviewInner(DATA.questions, arReviewFilter);
  }

  function onArtResultsClick(e) {
    var btn = e.target.closest("[data-ar-filter]");
    if (!btn || !document.getElementById("art-results").contains(btn)) return;
    e.preventDefault();
    arReviewFilter = btn.getAttribute("data-ar-filter") || "wrong";
    refreshAnswerReview();
  }

  function showResults(server) {
    if (timerId) {
      clearInterval(timerId);
      timerId = null;
    }
    arReviewFilter = "wrong";
    var score = server.score;
    var band = server.band;
    var totalQ = server.total || 40;
    if (isDrill) {
      var elapsed = Math.max(0, (DATA.timeLimitSeconds || 1200) - timeLeft);
      var em = Math.floor(elapsed / 60);
      var es = elapsed % 60;
      var autoNote = server.auto_submit
        ? '<p class="art-results-hero__meta">Time expired — answers submitted automatically.</p>'
        : "";
      var htmlDrill =
        '<div class="art-results-inner">' +
        '<div class="art-results-hero">' +
        '<div class="art-results-hero__label">Timed drill complete</div>' +
        '<div class="art-results-hero__score">' +
        score +
        " / " +
        totalQ +
        "</div>" +
        '<div class="art-results-hero__band">Estimated band: ' +
        escapeHtml(band) +
        "</div>" +
        '<div class="art-results-hero__meta">Time used: ' +
        em +
        " min " +
        (es < 10 ? "0" : "") +
        es +
        " sec</div>" +
        autoNote +
        "</div>" +
        '<div class="art-results-actions art-results-actions--row">' +
        '<button type="button" class="art-results-btn art-results-btn--outline" id="art-retry">Try again</button>' +
        '<a class="art-results-btn art-results-btn--solid" href="' +
        escapeHtml(INDEX_URL) +
        '">Back to drills</a>' +
        "</div></div>";
      var shellDrill = document.getElementById("art-results");
      if (shellDrill) {
        shellDrill.innerHTML = htmlDrill;
        shellDrill.classList.remove("art-results--hidden");
      }
      app.classList.add("art-app--hidden");
      var retryDrill = document.getElementById("art-retry");
      if (retryDrill) {
        retryDrill.addEventListener("click", function () {
          window.location.reload();
        });
      }
      return;
    }
    var p1 = server.part1_score;
    var p2 = server.part2_score;
    var p3 = server.part3_score;
    var m1 = server.part1_max || 14;
    var m2 = server.part2_max || 13;
    var m3 = server.part3_max || 13;
    var pct1 = Math.round((100 * p1) / m1);
    var pct2 = Math.round((100 * p2) / m2);
    var pct3 = Math.round((100 * p3) / m3);
    var elapsed = Math.max(0, (DATA.timeLimitSeconds || 3600) - timeLeft);
    var em = Math.floor(elapsed / 60);
    var es = elapsed % 60;
    var meta = DATA.resultsMeta || {};
    var questions = DATA.questions;

    function partCard(title, got, mx, pct) {
      return (
        '<div class="art-results-part">' +
        '<div class="art-results-part__title">' +
        escapeHtml(title) +
        " · " +
        got +
        "/" +
        mx +
        "</div>" +
        '<div class="art-results-bar"><div class="' +
        barClass(pct) +
        '" style="width:' +
        pct +
        '%"></div></div>' +
        "<div>" +
        pct +
        "% correct</div></div>"
      );
    }

    var histUrl = escapeHtml((TESTS_URL || "/reading/tests/").replace(/\/?$/, "") + "#art-history-heading");
    var testsUrl = escapeHtml(TESTS_URL);

    var html =
      '<div class="art-results-inner">' +
      '<div class="art-results-hero">' +
      '<div class="art-results-hero__label">Test complete</div>' +
      '<div class="art-results-hero__score">' +
      score +
      " / 40</div>" +
      '<div class="art-results-hero__band">Estimated band: ' +
      escapeHtml(band) +
      "</div>" +
      '<div class="art-results-hero__meta">Accuracy: ' +
      Math.round((100 * score) / 40) +
      "% · Time: " +
      em +
      " min " +
      (es < 10 ? "0" : "") +
      es +
      " sec</div></div>" +
      buildBandTipCard(score, p1, m1, p2, m2, p3, m3, meta) +
      '<div class="art-results-parts-block">' +
      '<h2 class="art-sec-kicker">Part breakdown</h2>' +
      '<div class="art-results-parts">' +
      partCard(meta.part1Title || "Part 1", p1, m1, pct1) +
      partCard(meta.part2Title || "Part 2", p2, m2, pct2) +
      partCard(meta.part3Title || "Part 3", p3, m3, pct3) +
      "</div></div>" +
      buildSkillsSection(questions) +
      buildMistakesSection(questions) +
      '<section class="art-ar-wrap" aria-labelledby="art-ar-h">' +
      '<h2 class="art-ar-h" id="art-ar-h">Answer review</h2>' +
      '<div id="art-ar-host">' +
      buildAnswerReviewInner(questions, arReviewFilter) +
      "</div></section>" +
      '<div class="art-results-actions art-results-actions--row">' +
      '<button type="button" class="art-results-btn art-results-btn--outline" id="art-retry">Take again</button>' +
      '<a class="art-results-btn art-results-btn--outline" href="' +
      histUrl +
      '">History</a>' +
      '<a class="art-results-btn art-results-btn--solid" href="' +
      testsUrl +
      '">Back to tests</a>' +
      "</div></div>";

    var shell = document.getElementById("art-results");
    if (shell) {
      shell.innerHTML = html;
      shell.classList.remove("art-results--hidden");
      if (!artResultsClickBound) {
        shell.addEventListener("click", onArtResultsClick);
        artResultsClickBound = true;
      }
    }
    app.classList.add("art-app--hidden");

    var retry = document.getElementById("art-retry");
    if (retry) {
      retry.addEventListener("click", function () {
        window.location.reload();
      });
    }
  }

  var submitInFlight = false;

  function submitTest(auto) {
    if (submitted || submitInFlight) return;
    if (!auto) {
      if (!window.confirm("Submit your test? You cannot change answers after submitting.")) return;
    }
    DATA.questions.forEach(function (q) {
      if (q.type === "gap") {
        var inp = document.querySelector('input[data-gap="' + q.id + '"]');
        if (inp) answers[q.id] = inp.value;
      }
      if (q.type === "summary") {
        var inp2 = document.querySelector('input[data-summary="' + q.id + '"]');
        if (inp2) {
          answers[q.id] = inp2.value;
          syncSummarySlot(q.id, inp2.value);
        }
      }
    });
    var elapsed = Math.max(0, (DATA.timeLimitSeconds || 3600) - timeLeft);
    submitInFlight = true;

    fetch(SUBMIT_URL, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify({
        answers: answers,
        time_taken_seconds: elapsed,
        auto_submit: !!auto,
      }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        submitInFlight = false;
        if (!data.ok) return;
        submitted = true;
        switchPart(currentPart);
        DATA.questions.forEach(function (q) {
          if (q.type === "summary") {
            var ok = answerMatches(q, answers[q.id]);
            var sp = document.querySelector('.art-sum-slot[data-q="' + q.id + '"]');
            if (sp) {
              sp.classList.remove("art-sum-slot--correct", "art-sum-slot--wrong");
              sp.classList.add(ok ? "art-sum-slot--correct" : "art-sum-slot--wrong");
            }
          }
        });
        updateNavStates();
        showResults(data);
      })
      .catch(function () {
        submitInFlight = false;
        if (!auto) alert("Could not save your result. Check your connection and try again.");
      });
  }

  /* Help + passage toggle */
  document.getElementById("art-help").addEventListener("click", function () {
    document.getElementById("art-help-bar").classList.toggle("art-help-bar--hidden");
  });
  document.getElementById("art-help-close").addEventListener("click", function () {
    document.getElementById("art-help-bar").classList.add("art-help-bar--hidden");
  });
  document.getElementById("art-toggle-passage").addEventListener("click", function () {
    app.classList.toggle("art-app--hide-passage");
    var on = app.classList.contains("art-app--hide-passage");
    this.textContent = on ? "Show passage" : "Hide passage";
  });
  document.getElementById("art-submit").addEventListener("click", function () {
    submitTest(false);
  });

  document.querySelectorAll(".art-tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      var p = parseInt(tab.getAttribute("data-part"), 10);
      switchPart(p);
    });
  });

  buildQnav();
  if (DATA.testTitleBar) {
    var titleEl = document.querySelector(".art-topbar__title");
    if (titleEl) titleEl.textContent = DATA.testTitleBar;
    if (document.title.indexOf("IELTS Academic Reading") === 0 || document.title.indexOf("ELTS") !== -1) {
      document.title = DATA.testTitleBar + " — Boosting Score";
    }
  }
  if (isDrill) {
    var tabsEl = document.querySelector(".art-tabs");
    if (tabsEl) tabsEl.hidden = true;
    switchPart(currentPart);
  } else {
    switchPart(1);
  }
  startTimer();
})();
