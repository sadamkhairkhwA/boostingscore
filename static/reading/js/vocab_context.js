/**
 * Vocabulary in context — one excerpt at a time.
 */
(function () {
  "use strict";

  var ICON_CHECK =
    '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>';
  var ICON_X =
    '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18"/></svg>';

  var host = document.getElementById("rs-vc-host");
  var dataEl = document.getElementById("rs-vocab-data");
  if (!host || !dataEl) return;

  var excerpts = JSON.parse(dataEl.textContent);
  var idx = 0;

  function wireQuestion(qEl, ex) {
    qEl.querySelectorAll(".rs-prq-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (qEl.classList.contains("is-answered")) return;
        var chosen = btn.getAttribute("data-value");
        var ok = chosen === ex.answer;
        qEl.classList.add("is-answered");
        qEl.classList.toggle("is-correct", ok);
        qEl.classList.toggle("is-wrong", !ok);
        qEl.querySelectorAll(".rs-prq-opt").forEach(function (b) {
          b.disabled = true;
          var val = b.getAttribute("data-value");
          if (val === ex.answer) b.classList.add("is-correct-opt");
          else if (val === chosen && !ok) b.classList.add("is-wrong-opt");
        });
        var fb = qEl.querySelector(".rs-prq-feedback");
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-prq-feedback " + (ok ? "rs-prq-feedback--ok" : "rs-prq-feedback--bad");
          fb.innerHTML = (ok ? ICON_CHECK : ICON_X) + " <span>" + ex.explanation + "</span>";
        }
        var next = document.getElementById("rs-vc-next");
        if (next) next.disabled = false;
      });
    });
  }

  function render() {
    var ex = excerpts[idx];
    host.innerHTML = "";
    var card = document.createElement("div");
    card.className = "rs-strat-card rs-strat-card--full";
    card.innerHTML =
      '<span class="rs-badge rs-badge--core">' +
      ex.topic +
      '</span><div class="rs-exbox" style="margin-top:10px;"><div class="rs-exbox-lbl">Passage excerpt</div>' +
      '<p class="rs-passage">' +
      ex.passage_html +
      "</p></div>";

    if (window.ReadingPractice) {
      var block = window.ReadingPractice.buildPracticeBlock({
        instructions: ex.prompt,
        questions: [
          {
            id: ex.id,
            prompt: 'What does "' + ex.target_word + '" mean here?',
            type: "choice",
            options: ex.options,
            answer: ex.answer,
          },
        ],
      });
      card.appendChild(block);
      var qEl = card.querySelector(".rs-prq");
      if (qEl) wireQuestion(qEl, ex);
    }
    host.appendChild(card);

    var prog = document.getElementById("rs-vc-progress");
    if (prog) prog.textContent = "Question " + (idx + 1) + " of " + excerpts.length;
    document.getElementById("rs-vc-back").disabled = idx === 0;
    var next = document.getElementById("rs-vc-next");
    next.textContent = idx >= excerpts.length - 1 ? "Finish" : "Next excerpt";
    next.disabled = true;
  }

  document.getElementById("rs-vc-next").addEventListener("click", function () {
    if (this.disabled) return;
    if (idx < excerpts.length - 1) {
      idx++;
      render();
    }
  });
  document.getElementById("rs-vc-back").addEventListener("click", function () {
    if (idx > 0) {
      idx--;
      render();
    }
  });

  render();
})();
