(function () {
  "use strict";

  var el = document.getElementById("ti-deck-data");
  if (!el) return;

  var DATA = JSON.parse(el.textContent);
  var words = DATA.words || [];
  var bestScores = {};
  try {
    Object.keys(DATA.best_scores || {}).forEach(function (k) {
      bestScores[k] = DATA.best_scores[k];
    });
  } catch (e) {}

  var viewList = document.getElementById("ti-view-list");
  var viewStudy = document.getElementById("ti-view-study");
  var viewTest = document.getElementById("ti-view-test");
  var viewFeedback = document.getElementById("ti-view-feedback");

  var wordIndex = 0;
  var assisted = false;
  var lastFeedback = null;
  var lastWordPayload = null;

  function getCsrfToken() {
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function wordCount(s) {
    var t = (s || "").trim();
    if (!t) return 0;
    return t.split(/\s+/).filter(Boolean).length;
  }

  function starsFromScore5(n) {
    var x = Math.max(1, Math.min(5, Math.round(Number(n) || 0)));
    var out = "";
    for (var i = 1; i <= 5; i++) {
      out += i <= x
        ? (typeof BSIcons !== "undefined" ? BSIcons.inline("star", "warn") : "")
        : (typeof BSIcons !== "undefined" ? BSIcons.inline("star-outline", "warn") : "");
    }
    return out;
  }

  function starsFromTotal10(t) {
    var x = Math.max(1, Math.min(5, Math.round((Number(t) || 0) / 2)));
    return starsFromScore5(x);
  }

  function doneCount() {
    var n = 0;
    words.forEach(function (w) {
      var b = bestScores[String(w.id)] || 0;
      if (b >= 7) n++;
    });
    return n;
  }

  function renderProgress() {
    var total = words.length;
    var d = doneCount();
    var badge = document.getElementById("ti-done-badge");
    var fill = document.getElementById("ti-progress-fill");
    if (badge) badge.textContent = d + " / " + total + " done";
    if (fill) fill.style.width = total ? Math.round((100 * d) / total) + "%" : "0%";
  }

  function statusForWord(w) {
    var b = bestScores[String(w.id)] || 0;
    if (b === 0) return { kind: "new", label: "Not started", cls: "ti-row--new" };
    if (b < 7) return { kind: "retry", label: b + "/10 — retry", cls: "ti-row--retry" };
    var mark = typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "";
    return { kind: "done", label: b + "/10 " + mark, cls: "ti-row--done" };
  }

  function renderList() {
    var sub = document.getElementById("ti-deck-subtitle");
    if (sub) {
      sub.textContent =
        DATA.title + " · " + DATA.word_count + " word" + (DATA.word_count === 1 ? "" : "s");
    }
    var back = document.getElementById("ti-back-decks");
    if (back) back.href = DATA.decks_url || "/vocabulary/type-it/";

    var ul = document.getElementById("ti-word-list");
    if (!ul) return;
    ul.innerHTML = words
      .map(function (w, idx) {
        var st = statusForWord(w);
        return (
          '<li class="ti-row ' +
          st.cls +
          '" data-idx="' +
          idx +
          '" role="button" tabindex="0">' +
          '<div class="ti-row__main">' +
          '<span class="ti-row__word">' +
          escapeHtml(w.word) +
          "</span>" +
          '<span class="ti-row__meta">' +
          escapeHtml(w.topic_label) +
          " · " +
          escapeHtml(w.level_label) +
          "</span></div>" +
          '<span class="ti-row__badge">' +
          escapeHtml(st.label) +
          "</span>" +
          '<span class="ti-row__arrow" aria-hidden="true">›</span></li>'
        );
      })
      .join("");

    ul.querySelectorAll(".ti-row").forEach(function (row) {
      function go() {
        openStudy(parseInt(row.getAttribute("data-idx"), 10));
      }
      row.addEventListener("click", go);
      row.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          go();
        }
      });
    });

    renderProgress();
  }

  function showView(name) {
    [viewList, viewStudy, viewTest, viewFeedback].forEach(function (v) {
      if (!v) return;
      v.classList.add("ti-view--hidden");
    });
    var map = { list: viewList, study: viewStudy, test: viewTest, feedback: viewFeedback };
    if (map[name]) map[name].classList.remove("ti-view--hidden");
    window.scrollTo(0, 0);
  }

  function currentWord() {
    return words[wordIndex] || null;
  }

  function openStudy(idx) {
    wordIndex = typeof idx === "number" ? idx : wordIndex;
    var w = currentWord();
    if (!w) return;
    assisted = false;
    document.getElementById("ti-study-word").textContent = w.word;
    var tags = document.getElementById("ti-study-tags");
    if (tags)
      tags.innerHTML =
        '<span class="ti-tag">' +
        escapeHtml(w.topic_label) +
        '</span> <span class="ti-tag">' +
        escapeHtml(w.level_label) +
        '</span> <span class="ti-tag">' +
        escapeHtml(w.pos) +
        "</span>";
    document.getElementById("ti-study-def").textContent = w.definition;
    document.getElementById("ti-study-ex").innerHTML = "<em>" + escapeHtml(w.example) + "</em>";
    var chips = document.getElementById("ti-study-chips");
    if (chips) {
      chips.innerHTML = (w.collocations || [])
        .map(function (c) {
          return '<span class="ti-chip">' + escapeHtml(c) + "</span>";
        })
        .join("");
    }
    document.getElementById("ti-study-note").textContent = w.ielts_note || "";
    showView("study");
  }

  function openTest() {
    var w = currentWord();
    if (!w) return;
    document.getElementById("ti-test-word").textContent = w.word;
    var tt = document.getElementById("ti-test-tags");
    if (tt)
      tt.innerHTML =
        '<span class="ti-tag">' +
        escapeHtml(w.topic_label) +
        '</span> <span class="ti-tag">' +
        escapeHtml(w.level_label) +
        "</span>";
    document.getElementById("ti-def-input").value = "";
    document.getElementById("ti-sent-input").value = "";
    document.getElementById("ti-assisted-box").classList.add("ti-hidden");
    document.getElementById("ti-assisted-modal").classList.add("ti-modal--hidden");
    updateWc();
    showView("test");
  }

  function updateWc() {
    var d = document.getElementById("ti-def-input");
    var s = document.getElementById("ti-sent-input");
    var wd = document.getElementById("ti-def-wc");
    var ws = document.getElementById("ti-sent-wc");
    if (wd) wd.textContent = wordCount(d && d.value) + " words";
    if (ws) ws.textContent = wordCount(s && s.value) + " words";
  }

  function numOrNull(v) {
    if (v === null || v === undefined || v === "") return null;
    var n = parseInt(v, 10);
    return isNaN(n) ? null : n;
  }

  function renderFeedback(fb, total, w, dsArg, ssArg, modeArg) {
    lastFeedback = fb;
    lastWordPayload = w;
    var mode = modeArg || "both";
    var outOf = mode === "both" ? 10 : 5;
    document.getElementById("ti-fb-total").textContent = total + " / " + outOf;
    document.getElementById("ti-fb-stars").textContent =
      mode === "both" ? starsFromTotal10(total) : starsFromScore5(total);
    document.getElementById("ti-fb-band").textContent = fb.band_tip || "";

    var ds =
      dsArg != null && dsArg !== ""
        ? numOrNull(dsArg)
        : numOrNull(fb.definition_score);
    var ss =
      ssArg != null && ssArg !== ""
        ? numOrNull(ssArg)
        : numOrNull(fb.sentence_score);
    if (mode === "sentence") ds = null;
    if (mode === "definition") ss = null;

    function colBlockDef(title, score, good, miss, correctHtml) {
      var high = score >= 4;
      var badgeCol = high ? "ti-badge--ok" : "ti-badge--bad";
      var html =
        '<h4 class="ti-fb-col-title">' +
        title +
        '</h4><div class="ti-fb-badge ' +
        badgeCol +
        '">' +
        starsFromScore5(score) +
        " " +
        score +
        '/5</div><div class="ti-fb-h">' +
        (high ? (typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "") + " Good" : (typeof BSIcons !== "undefined" ? BSIcons.cross() : "") + " Needs work") +
        "</div>" +
        '<div class="ti-fb-box ti-fb-box--good"><strong>What was good</strong><p>' +
        escapeHtml(good || "—") +
        "</p></div>";
      if (!high && miss) {
        html +=
          '<div class="ti-fb-box ti-fb-box--bad"><strong>What was missing</strong><p>' +
          escapeHtml(miss) +
          "</p></div>";
      }
      html += correctHtml || "";
      return html;
    }

    function colBlockSent(title, score, good, miss, improve, betterSent) {
      var high = score >= 4;
      var badgeCol = high ? "ti-badge--ok" : "ti-badge--bad";
      var html =
        '<h4 class="ti-fb-col-title">' +
        title +
        '</h4><div class="ti-fb-badge ' +
        badgeCol +
        '">' +
        starsFromScore5(score) +
        " " +
        score +
        '/5</div><div class="ti-fb-h">' +
        (high ? (typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "") + " Good" : (typeof BSIcons !== "undefined" ? BSIcons.cross() : "") + " Needs work") +
        "</div>" +
        '<div class="ti-fb-box ti-fb-box--good"><strong>What was good</strong><p>' +
        escapeHtml(good || "—") +
        "</p></div>";
      if (!high && miss) {
        html +=
          '<div class="ti-fb-box ti-fb-box--bad"><strong>What was missing</strong><p>' +
          escapeHtml(miss) +
          "</p></div>";
      }
      if (!high && improve) {
        html +=
          '<div class="ti-fb-box ti-fb-box--amber"><strong>What to improve</strong><p>' +
          escapeHtml(improve) +
          "</p></div>";
      }
      html +=
        '<div class="ti-fb-box ti-fb-box--navy"><strong>A stronger sentence</strong><p class="ti-fb-italic">' +
        escapeHtml(betterSent || "") +
        "</p></div>";
      return html;
    }

    var defCol = document.getElementById("ti-fb-def-col");
    if (defCol) {
      if (ds == null) {
        defCol.innerHTML = "";
        defCol.style.display = "none";
      } else {
        defCol.style.display = "";
        defCol.innerHTML = colBlockDef(
          "Definition feedback",
          ds,
          fb.definition_good,
          fb.definition_missing,
          '<div class="ti-fb-box ti-fb-box--def-ref"><strong>Correct definition</strong><p>' +
            escapeHtml(w.definition) +
            "</p></div>"
        );
      }
    }
    var sentCol = document.getElementById("ti-fb-sent-col");
    if (sentCol) {
      if (ss == null) {
        sentCol.innerHTML = "";
        sentCol.style.display = "none";
      } else {
        sentCol.style.display = "";
        sentCol.innerHTML = colBlockSent(
          "Sentence feedback",
          ss,
          fb.sentence_good,
          "",
          fb.sentence_improve,
          fb.better_sentence
        );
      }
    }

    document.getElementById("ti-fb-correct-def").textContent = w.definition;
    document.getElementById("ti-fb-correct-ex").innerHTML = "<em>" + escapeHtml(w.example) + "</em>";

    showView("feedback");
  }

  document.getElementById("ti-study-test").addEventListener("click", function () {
    openTest();
  });
  document.getElementById("ti-study-skip").addEventListener("click", function () {
    openTest();
  });
  document.getElementById("ti-study-back").addEventListener("click", function () {
    showView("list");
    renderList();
  });

  document.getElementById("ti-def-input").addEventListener("input", updateWc);
  document.getElementById("ti-sent-input").addEventListener("input", updateWc);

  document.getElementById("ti-show-def-link").addEventListener("click", function () {
    document.getElementById("ti-assisted-modal").classList.remove("ti-modal--hidden");
  });
  document.getElementById("ti-assisted-cancel").addEventListener("click", function () {
    document.getElementById("ti-assisted-modal").classList.add("ti-modal--hidden");
  });
  document.getElementById("ti-assisted-confirm").addEventListener("click", function () {
    assisted = true;
    var w = currentWord();
    document.getElementById("ti-assisted-modal").classList.add("ti-modal--hidden");
    var box = document.getElementById("ti-assisted-box");
    var p = document.getElementById("ti-assisted-def-text");
    if (w && p) p.textContent = w.definition;
    if (box) box.classList.remove("ti-hidden");
  });

  document.getElementById("ti-test-study-again").addEventListener("click", function () {
    openStudy(wordIndex);
  });

  document.getElementById("ti-submit-feedback").addEventListener("click", function () {
    var w = currentWord();
    if (!w) return;
    var def = (document.getElementById("ti-def-input").value || "").trim();
    var sent = (document.getElementById("ti-sent-input").value || "").trim();
    if (!def && !sent) {
      alert("Write a definition, a sentence, or both — then get feedback.");
      return;
    }
    var loading = document.getElementById("ti-loading");
    if (loading) loading.classList.remove("ti-hidden");
    fetch(DATA.feedback_url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify({
        word_id: w.id,
        deck_slug: DATA.slug,
        definition_text: def,
        sentence_text: sent,
        assisted: assisted,
      }),
    })
      .then(function (r) {
        return r.text().then(function (t) {
          try {
            return JSON.parse(t);
          } catch (e) {
            return { ok: false, error: t.slice(0, 200) };
          }
        });
      })
      .then(function (data) {
        if (loading) loading.classList.add("ti-hidden");
        var ok = data.ok === true || data.success === true;
        if (!ok) {
          console.error("Type it feedback:", data);
          alert(data.message || data.error || "Something went wrong — try again.");
          return;
        }
        var total = data.total_score;
        bestScores[String(w.id)] = Math.max(bestScores[String(w.id)] || 0, total);
        renderFeedback(
          data.feedback,
          total,
          data.word,
          data.definition_score,
          data.sentence_score,
          data.mode
        );
        renderProgress();
      })
      .catch(function () {
        if (loading) loading.classList.add("ti-hidden");
        alert("Something went wrong — try again.");
      });
  });

  document.getElementById("ti-fb-study-again").addEventListener("click", function () {
    openStudy(wordIndex);
  });
  document.getElementById("ti-fb-next").addEventListener("click", function () {
    wordIndex = (wordIndex + 1) % words.length;
    openStudy(wordIndex);
  });

  document.getElementById("ti-step-to-list").addEventListener("click", function () {
    showView("list");
    renderList();
  });
  document.getElementById("ti-fb-step-list").addEventListener("click", function () {
    showView("list");
    renderList();
  });

  renderList();
  showView("list");
})();
