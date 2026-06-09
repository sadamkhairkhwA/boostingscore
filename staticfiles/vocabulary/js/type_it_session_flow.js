(function () {
  "use strict";
  var el = document.getElementById("ti-session-payload");
  if (!el) return;
  var data = JSON.parse(el.textContent);
  var words = data.words || [];
  var idx = 0;
  var wordStage = "study";
  var sessionMode = "both";
  var assisted = false;
  var lastFeedback = null;
  var wordBests = JSON.parse(JSON.stringify(data.word_bests || {}));
  var sessionResult = {};

  var nav = document.getElementById("ti-session-nav");
  var stageStudy = document.getElementById("ti-stage-study");
  var stageTest = document.getElementById("ti-stage-test");
  var stageFeedback = document.getElementById("ti-stage-feedback");
  var stageSummary = document.getElementById("ti-stage-summary");
  var pillsHost = document.getElementById("ti-pills");
  var stepsBar = document.getElementById("ti-steps-bar");

  function csrfFromCookie() {
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : "";
  }
  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function wc(s) {
    var t = (s || "").trim();
    if (!t) return 0;
    return t.split(/\s+/).filter(Boolean).length;
  }
  function stars5(n) {
    var x = Math.max(1, Math.min(5, Math.round(Number(n) || 0)));
    var out = "";
    for (var i = 1; i <= 5; i++) out += i <= x ? "★" : "☆";
    return out;
  }
  function starsHero(total, outOf) {
    var x;
    if (outOf === 10) x = Math.max(1, Math.min(5, Math.round((total * 5) / 10)));
    else x = Math.max(1, Math.min(5, Math.round(Number(total) || 0)));
    var out = "";
    for (var i = 1; i <= 5; i++) out += i <= x ? "★" : "☆";
    return out;
  }
  function cur() {
    return words[idx];
  }
  function passes(mode, total) {
    var m = mode || "both";
    if (m === "both") return total >= 7;
    return total >= 4;
  }
  function mergeWordBest(itemId, mode, total) {
    var outOf = mode === "both" ? 10 : 5;
    var prev = wordBests[itemId] || { total: 0, out_of: outOf, passed: false };
    var p = passes(mode, total);
    if (p) {
      wordBests[itemId] = {
        total: Math.max(prev.total || 0, total),
        out_of: outOf,
        passed: true,
        mode: mode,
      };
    } else if (!prev.passed) {
      wordBests[itemId] = { total: total, out_of: outOf, passed: false, mode: mode };
    }
  }
  function hideStages() {
    [stageStudy, stageTest, stageFeedback, stageSummary].forEach(function (n) {
      n.classList.add("ti-hidden");
    });
  }
  function showNav(on) {
    if (!nav) return;
    if (on) nav.classList.remove("ti-hidden");
    else nav.classList.add("ti-hidden");
  }
  function paintSteps(activeKey) {
    if (!stepsBar) return;
    var keys = ["select", "study", "test", "feedback"];
    var labels = ["Select", "Study", "Test", "Feedback"];
    var ai = keys.indexOf(activeKey);
    if (ai < 0) ai = 1;
    var parts = [];
    for (var i = 0; i < keys.length; i++) {
      var k = keys[i];
      var sep = i ? '<span class="ti-s-step-sep">→</span>' : "";
      var cls = "ti-s-step";
      if (k === "select") cls += " ti-s-step--done";
      else if (i < ai) cls += " ti-s-step--done";
      else if (i === ai) cls += " ti-s-step--active";
      var txt = labels[i];
      if (k === "select") txt = "Select ✓";
      else if (i < ai) txt = labels[i] + " ✓";
      parts.push(sep + '<span class="' + cls + '" data-step="' + k + '">' + txt + "</span>");
    }
    stepsBar.innerHTML = parts.join("");
  }
  function renderPills() {
    if (!pillsHost) return;
    pillsHost.innerHTML = words
      .map(function (w, i) {
        var meta = wordBests[w.item_id] || { passed: false, total: 0 };
        var cls = "ti-pill";
        if (i === idx) cls += " ti-pill--current";
        else if (meta.passed) cls += " ti-pill--done";
        return (
          '<button type="button" class="' +
          cls +
          '" data-idx="' +
          i +
          '" role="tab">' +
          escapeHtml(String(i + 1) + " " + w.word) +
          (meta.passed ? " ✓" : "") +
          "</button>"
        );
      })
      .join("");
    pillsHost.querySelectorAll(".ti-pill").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var j = parseInt(btn.getAttribute("data-idx"), 10);
        if (isNaN(j)) return;
        idx = j;
        sessionMode = "both";
        wordStage = "study";
        hideStages();
        stageStudy.classList.remove("ti-hidden");
        renderStudy();
        paintSteps("study");
        document.getElementById("ti-word-counter").textContent = "Word " + (idx + 1) + " of " + words.length;
        renderPills();
        window.scrollTo(0, 0);
      });
    });
  }
  function showFlowStage() {
    hideStages();
    paintSteps(
      wordStage === "study" ? "study" : wordStage === "test" ? "test" : "feedback"
    );
    if (wordStage === "study") stageStudy.classList.remove("ti-hidden");
    if (wordStage === "test") stageTest.classList.remove("ti-hidden");
    if (wordStage === "feedback") stageFeedback.classList.remove("ti-hidden");
    document.getElementById("ti-word-counter").textContent = "Word " + (idx + 1) + " of " + words.length;
    renderPills();
    window.scrollTo(0, 0);
  }
  function showSummaryView() {
    hideStages();
    showNav(false);
    stageSummary.classList.remove("ti-hidden");
    var n = words.length;
    var rows = words
      .map(function (w) {
        var r = sessionResult[w.item_id];
        var rowCls = "ti-sum-row";
        var right = "";
        if (!r) {
          rowCls += " ti-sum-row--muted";
          right = "—";
        } else if (r.skipped) {
          rowCls += " ti-sum-row--skip";
          right = "Skipped";
        } else {
          var pct = (r.total / r.out_of) * 100;
          if (pct >= 70) rowCls += " ti-sum-row--ok";
          else if (pct >= 50) rowCls += " ti-sum-row--mid";
          else rowCls += " ti-sum-row--bad";
          right =
            '<span class="ti-sum-score">' +
            escapeHtml(String(r.total) + "/" + String(r.out_of)) +
            "</span> " +
            stars5(r.out_of === 10 ? Math.round((r.total * 5) / 10) : r.total);
        }
        return (
          '<div class="' +
          rowCls +
          '"><div><div class="ti-sum-word">' +
          escapeHtml(w.word) +
          '</div><div class="ti-sum-pos">' +
          escapeHtml(w.pos || "word") +
          '</div></div><div class="ti-sum-right">' +
          right +
          "</div></div>"
        );
      })
      .join("");
    stageSummary.innerHTML =
      '<div class="ti-sum-inner">' +
      '<div class="ti-sum-icon" aria-hidden="true">🎉</div>' +
      '<h2 class="ti-sum-title">Session complete</h2>' +
      '<p class="ti-sum-sub">' +
      n +
      " word" +
      (n === 1 ? "" : "s") +
      " practised this session.</p>" +
      '<div class="ti-sum-rows">' +
      rows +
      "</div>" +
      '<div class="ti-sum-actions">' +
      '<button type="button" class="ti-btn ti-btn--outline" id="ti-sum-again">Practise again</button>' +
      '<button type="button" class="ti-btn ti-btn--dark" id="ti-sum-decks">Back to decks</button>' +
      "</div></div>";
    document.getElementById("ti-sum-again").addEventListener("click", function () {
      idx = 0;
      sessionMode = "both";
      sessionResult = {};
      wordBests = JSON.parse(JSON.stringify(data.word_bests || {}));
      wordStage = "study";
      showNav(true);
      hideStages();
      stageSummary.classList.add("ti-hidden");
      stageStudy.classList.remove("ti-hidden");
      renderStudy();
      paintSteps("study");
      document.getElementById("ti-word-counter").textContent = "Word 1 of " + words.length;
      renderPills();
      window.scrollTo(0, 0);
    });
    document.getElementById("ti-sum-decks").addEventListener("click", function () {
      window.location.href = data.deck.decks_url;
    });
  }

  function renderStudy() {
    var w = cur();
    stageStudy.innerHTML =
      '<div class="ti-card ti-card--study">' +
      '<p class="ti-eyebrow">Study this word carefully</p>' +
      '<h2 class="ti-word">' +
      escapeHtml(w.word) +
      "</h2>" +
      '<div class="ti-tags"><span class="ti-tag ti-tag--topic">' +
      escapeHtml(w.topic_label) +
      '</span><span class="ti-tag ti-tag--level">' +
      escapeHtml(w.level_label) +
      '</span><span class="ti-tag">' +
      escapeHtml(w.pos || "word") +
      "</span></div>" +
      '<div class="ti-box ti-box--def-study"><div class="ti-box-lbl">Definition</div><div>' +
      escapeHtml(w.definition) +
      "</div></div>" +
      '<div class="ti-box ti-box--ex"><div class="ti-box-lbl ti-box-lbl--green">IELTS example sentence</div><div><em>' +
      escapeHtml(w.example) +
      "</em></div></div>" +
      '<div class="ti-box ti-box--colloc"><div class="ti-box-lbl">Collocations</div><div class="ti-tags">' +
      (w.collocations || [])
        .slice(0, 8)
        .map(function (x) {
          return '<span class="ti-tag ti-tag--chip">' + escapeHtml(x) + "</span>";
        })
        .join("") +
      "</div></div>" +
      '<div class="ti-box ti-box--note"><div class="ti-box-lbl ti-box-lbl--amber">IELTS usage note</div><div>' +
      escapeHtml(w.ielts_note || "") +
      "</div></div>" +
      '<button id="ti-go-test" class="ti-btn ti-btn--dark ti-btn--block" type="button">I\'ve studied this — start test →</button>' +
      '<div class="ti-study-links">' +
      '<button type="button" class="ti-link-muted" id="ti-skip-know">Skip — I already know this word</button>' +
      '<button type="button" class="ti-link-muted ti-study-links__right" id="ti-skip-next">Skip to next word →</button>' +
      "</div></div>";

    function goTest() {
      sessionMode = "both";
      assisted = false;
      wordStage = "test";
      renderTest();
      showFlowStage();
    }
    document.getElementById("ti-go-test").addEventListener("click", goTest);
    document.getElementById("ti-skip-know").addEventListener("click", goTest);
    document.getElementById("ti-skip-next").addEventListener("click", function () {
      var w0 = cur();
      sessionResult[w0.item_id] = { skipped: true, total: 0, out_of: 0 };
      if (idx < words.length - 1) {
        idx += 1;
        sessionMode = "both";
        wordStage = "study";
        renderStudy();
        showFlowStage();
      } else {
        showSummaryView();
      }
    });
  }

  function practiseLabel() {
    return "Definition + sentence";
  }

  function renderTest() {
    var w = cur();
    var m = "both";
    var tasks =
      '<p class="ti-task-hint">Submit a definition, a sentence, or both — feedback scores only what you write.</p>' +
      '<div class="ti-task" id="ti-task-def-wrap"><div class="ti-task-h"><span class="ti-task-num">1</span><div><h3 class="ti-task-title">Write the definition from memory</h3><p class="ti-task-sub">Don\'t look back. Write in your own words.</p></div></div><textarea id="ti-def" class="ti-area" placeholder="What does this word mean?..."></textarea><div class="ti-count" id="ti-def-c">0 words</div></div>' +
      '<div class="ti-task" id="ti-task-sent-wrap"><div class="ti-task-h"><span class="ti-task-num">2</span><div><h3 class="ti-task-title">Write a sentence using this word</h3><p class="ti-task-sub">One IELTS-style sentence. Use the word correctly.</p></div></div><textarea id="ti-sent" class="ti-area" placeholder="Write your sentence here..."></textarea><div class="ti-count" id="ti-sent-c">0 words</div></div>';
    stageTest.innerHTML =
      '<div class="ti-banner"><span>🧠</span><div><strong>Definition and example are now hidden</strong><div>Recall from memory. This is what makes vocabulary stick.</div></div></div>' +
      '<div class="ti-card ti-card--test-word">' +
      '<h2 class="ti-word">' +
      escapeHtml(w.word) +
      "</h2>" +
      '<div class="ti-tags"><span class="ti-tag ti-tag--topic">' +
      escapeHtml(w.topic_label) +
      '</span><span class="ti-tag ti-tag--level">' +
      escapeHtml(w.level_label) +
      "</span></div>" +
      '<div class="ti-practise-bar"><span>Practising: <strong>' +
      escapeHtml(practiseLabel()) +
      "</strong></span></div></div>" +
      tasks +
      '<button id="ti-assist-link" class="ti-link-red" type="button">I can\'t remember — show definition</button>' +
      '<div id="ti-assist-confirm" class="ti-assist-box ti-hidden"><strong>⚠ This marks your attempt as assisted</strong><div>Even a wrong attempt helps you learn more than looking it up.</div><div class="ti-actions"><button id="ti-assist-yes" class="ti-btn ti-btn--dark" type="button">Show anyway</button><button id="ti-assist-no" class="ti-btn ti-btn--outline" type="button">Cancel</button></div></div>' +
      '<div id="ti-assist-def" class="ti-assist-box ti-hidden"><span class="ti-assist-tag">Assisted</span>' +
      escapeHtml(w.definition) +
      "</div>" +
      '<button id="ti-get-feedback" class="ti-btn ti-btn--block ti-btn--green" type="button">Get AI feedback →</button>' +
      '<p id="ti-ai-loading" class="ti-ai-loading ti-hidden">AI is checking your answers…</p>' +
      '<button type="button" class="ti-link-muted ti-link-center" id="ti-back-study">← Back to study</button>';

    function upd() {
      var d = document.getElementById("ti-def");
      var s = document.getElementById("ti-sent");
      if (d && document.getElementById("ti-def-c"))
        document.getElementById("ti-def-c").textContent = wc(d.value) + " words";
      if (s && document.getElementById("ti-sent-c"))
        document.getElementById("ti-sent-c").textContent = wc(s.value) + " words";
    }
    if (document.getElementById("ti-def")) document.getElementById("ti-def").addEventListener("input", upd);
    if (document.getElementById("ti-sent")) document.getElementById("ti-sent").addEventListener("input", upd);
    upd();
    document.getElementById("ti-back-study").addEventListener("click", function () {
      wordStage = "study";
      sessionMode = "both";
      renderStudy();
      showFlowStage();
    });
    document.getElementById("ti-assist-link").addEventListener("click", function () {
      document.getElementById("ti-assist-confirm").classList.remove("ti-hidden");
    });
    document.getElementById("ti-assist-no").addEventListener("click", function () {
      document.getElementById("ti-assist-confirm").classList.add("ti-hidden");
    });
    document.getElementById("ti-assist-yes").addEventListener("click", function () {
      assisted = true;
      document.getElementById("ti-assist-confirm").classList.add("ti-hidden");
      document.getElementById("ti-assist-def").classList.remove("ti-hidden");
    });
    document.getElementById("ti-get-feedback").addEventListener("click", function () {
      var d = (document.getElementById("ti-def") && document.getElementById("ti-def").value) || "";
      d = d.trim();
      var s = (document.getElementById("ti-sent") && document.getElementById("ti-sent").value) || "";
      s = s.trim();
      if (!d && !s) {
        alert("Write a definition, a sentence, or both — then tap Get AI feedback.");
        return;
      }
      document.getElementById("ti-ai-loading").classList.remove("ti-hidden");
      fetch(data.deck.feedback_url, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfFromCookie() },
        body: JSON.stringify({
          item_id: w.item_id,
          word_id: w.word_id,
          deck_slug: data.deck.slug,
          mode: m,
          definition_text: d,
          sentence_text: s,
          assisted: assisted,
        }),
      })
        .then(function (r) {
          return r.text().then(function (t) {
            try {
              return JSON.parse(t);
            } catch (e) {
              return {
                ok: false,
                error: "invalid_response",
                message: "Something went wrong — try again.",
              };
            }
          });
        })
        .then(function (res) {
          document.getElementById("ti-ai-loading").classList.add("ti-hidden");
          var ok = res.ok === true || res.success === true;
          if (!ok) {
            var detail = res.message || res.error || "Something went wrong — try again.";
            console.error("Type it feedback:", res);
            alert(detail);
            return;
          }
          lastFeedback = res;
          mergeWordBest(w.item_id, res.mode, res.total_score);
          sessionResult[w.item_id] = {
            skipped: false,
            total: res.total_score,
            out_of: res.mode === "both" ? 10 : 5,
            assisted: assisted,
            mode: res.mode,
          };
          wordStage = "feedback";
          renderFeedback();
          showFlowStage();
        })
        .catch(function () {
          document.getElementById("ti-ai-loading").classList.add("ti-hidden");
          alert("Something went wrong — try again.");
        });
    });
  }

  function renderFeedback() {
    var w = cur();
    var res = lastFeedback;
    var fb = res.feedback || {};
    var mode = res.mode || sessionMode;
    var total = Number(res.total_score || 0);
    var outOf = mode === "both" ? 10 : 5;
    var ds = typeof res.definition_score === "number" ? res.definition_score : null;
    var ss = typeof res.sentence_score === "number" ? res.sentence_score : null;
    var correctDef = fb.correct_definition || w.definition;
    var isLast = idx >= words.length - 1;

    var hero =
      '<div class="ti-hero"><div class="ti-eyebrow" style="color:#cbd5e1">Your score</div><div class="score">' +
      total +
      " / " +
      outOf +
      '</div><div class="stars">' +
      starsHero(total, outOf) +
      "</div><div>" +
      escapeHtml(fb.band_tip || "") +
      "</div></div>";

    var colDef = "";
    var colSent = "";
    if (mode !== "sentence" && typeof ds === "number") {
      colDef =
        '<div class="ti-fcol"><h4>Definition feedback</h4><div class="ti-score-badge ' +
        (ds >= 4 ? "ti-score-badge--ok" : "ti-score-badge--bad") +
        '">' +
        stars5(ds) +
        " " +
        ds +
        '/5</div><div>' +
        (ds >= 4 ? "✓ Good" : "✗ Needs work") +
        '</div><div class="ti-fbox ti-fbox--good"><strong>What was good</strong><div>' +
        escapeHtml(fb.definition_good || "") +
        "</div></div>" +
        (ds < 4 && fb.definition_missing
          ? '<div class="ti-fbox ti-fbox--bad"><strong>What was missing</strong><div>' +
            escapeHtml(fb.definition_missing) +
            "</div></div>"
          : "") +
        '<div class="ti-fbox ti-fbox--blue"><strong>Correct definition</strong><div>' +
        escapeHtml(correctDef) +
        "</div></div></div>";
    }
    if (mode !== "definition" && typeof ss === "number") {
      colSent =
        '<div class="ti-fcol"><h4>Sentence feedback</h4><div class="ti-score-badge ' +
        (ss >= 4 ? "ti-score-badge--ok" : "ti-score-badge--bad") +
        '">' +
        stars5(ss) +
        " " +
        ss +
        '/5</div><div>' +
        (ss >= 4 ? "✓ Good" : "✗ Needs work") +
        '</div><div class="ti-fbox ti-fbox--good"><strong>What was good</strong><div>' +
        escapeHtml(fb.sentence_good || "") +
        "</div></div>" +
        (ss < 4 && fb.sentence_improve
          ? '<div class="ti-fbox ti-fbox--amber"><strong>What to improve</strong><div>' +
            escapeHtml(fb.sentence_improve) +
            "</div></div>"
          : "") +
        '<div class="ti-fbox ti-fbox--navy"><strong>A stronger sentence</strong><div><em>' +
        escapeHtml(fb.better_sentence || "") +
        "</em></div></div></div>";
    }

    var colsClass = mode === "both" ? "ti-cols" : "ti-cols ti-cols--single";
    stageFeedback.innerHTML =
      hero +
      '<div class="' +
      colsClass +
      '">' +
      colDef +
      colSent +
      "</div>" +
      '<div class="ti-correct-card"><div class="ti-box-lbl">Correct answers — compare with yours</div><div class="ti-box ti-box--def-study">' +
      escapeHtml(w.definition) +
      '</div><div class="ti-box ti-box--ex"><em>' +
      escapeHtml(w.example) +
      "</em></div></div>" +
      '<button id="ti-fb-next" class="ti-btn ti-btn--dark ti-btn--block" type="button">' +
      (isLast ? "Finish session →" : "Next word →") +
      "</button>" +
      '<button type="button" class="ti-link-muted ti-link-center" id="ti-fb-study-again">Study this word again</button>';

    document.getElementById("ti-fb-study-again").addEventListener("click", function () {
      sessionMode = "both";
      wordStage = "study";
      renderStudy();
      showFlowStage();
    });
    document.getElementById("ti-fb-next").addEventListener("click", function () {
      if (isLast) {
        showSummaryView();
        return;
      }
      idx += 1;
      sessionMode = "both";
      wordStage = "study";
      renderStudy();
      showFlowStage();
    });
  }

  renderStudy();
  paintSteps("study");
  document.getElementById("ti-word-counter").textContent = "Word 1 of " + words.length;
  renderPills();
})();
