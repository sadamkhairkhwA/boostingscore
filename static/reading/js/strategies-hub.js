/**
 * Reading strategies hub — primary tabs, skills sub-tabs, interactive exercises.
 */
(function () {
  "use strict";

  function qs(root, sel) {
    return (root || document).querySelector(sel);
  }
  function qsa(root, sel) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* ——— Primary tabs ——— */
  function activateMain(key) {
    qsa(document, ".rs-main-tab").forEach(function (b) {
      var on = b.getAttribute("data-tab") === key;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    qsa(document, ".rs-main-panel").forEach(function (p) {
      p.classList.toggle("active", p.getAttribute("data-panel") === key);
      p.hidden = p.getAttribute("data-panel") !== key;
    });
  }

  qsa(document, ".rs-main-tab").forEach(function (btn) {
    btn.addEventListener("click", function () {
      activateMain(btn.getAttribute("data-tab"));
    });
  });

  /* ——— Skills sub-tabs ——— */
  function activateSkill(key) {
    qsa(document, ".rs-skill-tab").forEach(function (b) {
      var on = b.getAttribute("data-skill") === key;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    qsa(document, ".rs-skill-panel").forEach(function (p) {
      var on = p.getAttribute("data-skill-panel") === key;
      p.classList.toggle("active", on);
      p.hidden = !on;
    });
  }

  qsa(document, ".rs-skill-tab").forEach(function (btn) {
    btn.addEventListener("click", function () {
      activateSkill(btn.getAttribute("data-skill"));
    });
  });

  /* ——— Scanning ——— */
  var scanHost = qs(document, "[data-rs-scan]");
  if (scanHost) {
    scanHost.addEventListener("click", function (e) {
      var t = e.target.closest(".rs-scan-word");
      if (!t || !scanHost.contains(t)) return;
      qsa(scanHost, ".rs-scan-word").forEach(function (w) {
        w.classList.remove("rs-pick-good", "rs-pick-bad");
      });
      if (t.getAttribute("data-correct") === "1") {
        t.classList.add("rs-pick-good");
        qs(scanHost, ".rs-scan-feedback").textContent =
          "Correct — you scanned for the exact date, not the whole paragraph.";
      } else {
        t.classList.add("rs-pick-bad");
        qs(scanHost, ".rs-scan-feedback").textContent =
          "Not that detail — keep scanning for when the rules took effect.";
      }
    });
  }

  /* ——— Skimming ——— */
  var skim = qs(document, "[data-rs-skim]");
  if (skim) {
    var bar = qs(skim, ".rs-skim-bar-inner");
    var readEl = qs(skim, ".rs-skim-read");
    var quizEl = qs(skim, ".rs-skim-quiz");
    var passageEl = qs(skim, ".rs-skim-passage");
    var btnStart = qs(skim, ".rs-skim-start");
    var totalMs = 8000;
    var timer = null;

    function resetSkim() {
      if (timer) clearInterval(timer);
      timer = null;
      readEl.hidden = false;
      quizEl.hidden = true;
      if (bar) bar.style.width = "0%";
      qsa(skim, ".rs-skim-opt").forEach(function (o) {
        o.classList.remove("rs-pick-good", "rs-pick-bad");
        o.disabled = false;
      });
      qs(skim, ".rs-skim-feedback").textContent = "";
    }

    btnStart.addEventListener("click", function () {
      resetSkim();
      readEl.hidden = false;
      quizEl.hidden = true;
      var start = Date.now();
      timer = setInterval(function () {
        var p = Math.min(100, ((Date.now() - start) / totalMs) * 100);
        if (bar) bar.style.width = p + "%";
        if (Date.now() - start >= totalMs) {
          clearInterval(timer);
          timer = null;
          readEl.hidden = true;
          quizEl.hidden = false;
          if (passageEl) passageEl.hidden = true;
        }
      }, 50);
    });

    qsa(skim, ".rs-skim-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        qsa(skim, ".rs-skim-opt").forEach(function (o) {
          o.disabled = true;
        });
        btn.classList.add(ok ? "rs-pick-good" : "rs-pick-bad");
        qs(skim, ".rs-skim-feedback").textContent = ok
          ? "Right — the first lines + topic sentences carry the gist."
          : "Not quite — re-skim for the overall purpose, not one detail.";
      });
    });
  }

  /* ——— Paraphrase ——— */
  var par = qs(document, "[data-rs-paraphrase]");
  if (par) {
    qsa(par, ".rs-par-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        qsa(par, ".rs-par-opt").forEach(function (o) {
          o.disabled = true;
          o.classList.remove("rs-pick-good", "rs-pick-bad");
        });
        btn.classList.add(ok ? "rs-pick-good" : "rs-pick-bad");
        qs(par, ".rs-par-feedback").textContent = ok
          ? "Same meaning, different grammar — that is the skill IELTS rewards."
          : "This option shifts the meaning or is too narrow. Compare the core claim.";
      });
    });
  }

  /* ——— TFNG + YNNG shared pattern ——— */
  function wireMcq(rootSel, feedbackSel) {
    var root = qs(document, rootSel);
    if (!root) return;
    var fb = qs(document, feedbackSel);
    var keyJson = root.getAttribute("data-answer-key");
    var key = keyJson ? JSON.parse(keyJson) : [];

    qs(root, ".rs-mcq-submit").addEventListener("click", function () {
      var rows = qsa(root, ".rs-mcq-row");
      var correct = 0;
      rows.forEach(function (row, i) {
        var want = key[i];
        var picked = qs(row, "input[name=\"tfng-" + i + "\"]:checked");
        qsa(row, ".rs-mcq-pill").forEach(function (lab) {
          lab.classList.remove("rs-reveal-good", "rs-reveal-bad", "rs-reveal-miss");
        });
        qsa(row, "input").forEach(function (inp) {
          inp.disabled = true;
        });
        if (!picked) {
          qsa(row, 'label[for^="tfng-' + i + '-"]').forEach(function (lab) {
            if (lab.getAttribute("for") && lab.getAttribute("for").indexOf(want) !== -1)
              lab.classList.add("rs-reveal-miss");
          });
          return;
        }
        var val = picked.value;
        if (val === want) correct += 1;
        qsa(row, "label").forEach(function (lab) {
          var inp = document.getElementById(lab.getAttribute("for"));
          if (!inp) return;
          if (inp.value === want) lab.classList.add("rs-reveal-good");
          else if (inp === picked && val !== want) lab.classList.add("rs-reveal-bad");
        });
      });
      if (fb)
        fb.textContent =
          "Score: " + correct + " / " + rows.length + ". Green = correct answer; your wrong pick in red.";
    });
  }

  wireMcq("[data-rs-tfng]", "#rs-tfng-feedback");
  wireMcq("[data-rs-ynng]", "#rs-ynng-feedback");

  /* ——— Speed reading ——— */
  var sp = qs(document, "[data-rs-speed]");
  if (sp) {
    var spPass = qs(sp, ".rs-speed-passage");
    var spQ = qs(sp, ".rs-speed-quiz");
    var spStart = qs(sp, ".rs-speed-start");
    var spDone = qs(sp, ".rs-speed-done");
    var spBar = qs(sp, ".rs-speed-bar-inner");
    var spTimer = null;
    var spT0 = 0;
    var durationMs = 60000;
    var wordCount = parseInt(sp.getAttribute("data-word-count") || "0", 10);

    spStart.addEventListener("click", function () {
      spPass.hidden = false;
      spQ.hidden = true;
      spT0 = Date.now();
      qsa(sp, ".rs-speed-opt").forEach(function (o) {
        o.classList.remove("rs-pick-good", "rs-pick-bad");
        o.disabled = false;
      });
      qs(sp, ".rs-speed-result").textContent = "";
      if (spTimer) clearInterval(spTimer);
      spTimer = setInterval(function () {
        var elapsed = Date.now() - spT0;
        var p = Math.min(100, (elapsed / durationMs) * 100);
        if (spBar) spBar.style.width = p + "%";
      }, 200);
    });

    spDone.addEventListener("click", function () {
      if (spTimer) clearInterval(spTimer);
      spTimer = null;
      spPass.hidden = true;
      spQ.hidden = false;
      var mins = (Date.now() - spT0) / 60000;
      var wpm = mins > 0 ? Math.round(wordCount / mins) : 0;
      qs(sp, ".rs-speed-wpm").textContent = String(wpm);
    });

    qsa(sp, ".rs-speed-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        qsa(sp, ".rs-speed-opt").forEach(function (o) {
          o.disabled = true;
        });
        btn.classList.add(ok ? "rs-pick-good" : "rs-pick-bad");
        var mins = (Date.now() - spT0) / 60000;
        var wpm = mins > 0 ? Math.round(wordCount / mins) : 0;
        var tgt = 200;
        qs(sp, ".rs-speed-result").textContent =
          "About " +
          wpm +
          " wpm vs IELTS-style target ~" +
          tgt +
          " wpm. " +
          (wpm >= tgt ? "Strong pace — keep accuracy." : "Speed will grow with practice; accuracy first.");
      });
    });
  }
})();
