/**
 * Reading strategies — Skills lab interactions (sub-tabs + exercises).
 */
(function () {
  "use strict";

  function qs(root, sel) {
    return (root || document).querySelector(sel);
  }
  function qsa(root, sel) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* ——— Main vs skills sub-tabs ——— */
  function initMainTabs() {
    qsa(document, ".rs-main-tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-rs-tab");
        qsa(document, ".rs-main-tab").forEach(function (b) {
          var on = b.getAttribute("data-rs-tab") === key;
          b.classList.toggle("active", on);
          b.setAttribute("aria-selected", on ? "true" : "false");
        });
        qsa(document, ".rs-main-panel").forEach(function (p) {
          p.classList.toggle("active", p.getAttribute("data-rs-panel") === key);
        });
      });
    });
  }

  function initSkillTabs() {
    qsa(document, ".rs-skill-tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-rs-skill");
        qsa(document, ".rs-skill-tab").forEach(function (b) {
          var on = b.getAttribute("data-rs-skill") === key;
          b.classList.toggle("active", on);
          b.setAttribute("aria-selected", on ? "true" : "false");
        });
        qsa(document, ".rs-skill-panel").forEach(function (p) {
          p.classList.toggle("active", p.getAttribute("data-rs-skill-panel") === key);
        });
      });
    });
  }

  /* ——— Scanning ——— */
  function initScanning() {
    var fb = qs(document, "#rs-scan-feedback");
    qsa(document, "#rs-scan-passage .rs-scan-word").forEach(function (el) {
      el.addEventListener("click", function () {
        var ok = el.getAttribute("data-correct") === "1";
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-lab-feedback " + (ok ? "rs-lab-feedback--ok" : "rs-lab-feedback--bad");
          fb.textContent = ok
            ? "Correct — that phrase answers the question."
            : "Not the best match — look for when the rules began, not where or why.";
        }
        qsa(document, "#rs-scan-passage .rs-scan-word").forEach(function (w) {
          w.classList.remove("rs-scan-word--picked-ok", "rs-scan-word--picked-bad");
          if (w === el) w.classList.add(ok ? "rs-scan-word--picked-ok" : "rs-scan-word--picked-bad");
        });
      });
    });
  }

  /* ——— Skimming ——— */
  function initSkimming() {
    var start = qs(document, "#rs-skim-start");
    var passage = qs(document, "#rs-skim-passage");
    var bar = qs(document, "#rs-skim-countdown-bar");
    var quiz = qs(document, "#rs-skim-quiz");
    if (!start || !passage || !quiz) return;
    start.addEventListener("click", function () {
      start.disabled = true;
      passage.hidden = false;
      quiz.hidden = true;
      if (bar) {
        bar.style.transition = "none";
        bar.style.width = "100%";
        void bar.offsetWidth;
        bar.style.transition = "width 8s linear";
        bar.style.width = "0%";
      }
      window.setTimeout(function () {
        passage.hidden = true;
        quiz.hidden = false;
        start.disabled = false;
        if (bar) {
          bar.style.transition = "none";
          bar.style.width = "100%";
        }
      }, 8000);
    });
    qsa(document, ".rs-skim-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        var fb = qs(document, "#rs-skim-feedback");
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-lab-feedback " + (ok ? "rs-lab-feedback--ok" : "rs-lab-feedback--bad");
          fb.textContent = ok
            ? "Right — the passage is mainly about how the scheme affected traffic and timing."
            : "Not quite — re-read the opening: it centres on the parking scheme and its measured outcome.";
        }
      });
    });
  }

  /* ——— Paraphrase ——— */
  function initParaphrase() {
    qsa(document, ".rs-para-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        var fb = qs(document, "#rs-para-feedback");
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-lab-feedback " + (ok ? "rs-lab-feedback--ok" : "rs-lab-feedback--bad");
          fb.textContent = ok
            ? "Correct — same meaning: reduced spending / cut expenditure."
            : "Different meaning: this changes scale (slightly vs sharply) or adds ideas not in the original.";
        }
      });
    });
  }

  /* ——— T/F/NG batch ——— */
  function tfngPick(container, stmtIdx, val) {
    if (!container) return;
    var row = container.querySelector('.rs-tfng-row[data-stmt="' + stmtIdx + '"]');
    if (!row) return;
    qsa(row, ".rs-tfng-choice").forEach(function (b) {
      b.classList.toggle("rs-tfng-choice--sel", b.getAttribute("data-val") === val);
    });
    row.setAttribute("data-answer", val);
  }

  function initTfng() {
    var root = qs(document, "#rs-tfng-block");
    if (!root) return;
    qsa(root, ".rs-tfng-row").forEach(function (row) {
      var idx = row.getAttribute("data-stmt");
      qsa(row, ".rs-tfng-choice").forEach(function (btn) {
        btn.addEventListener("click", function () {
          tfngPick(root, idx, btn.getAttribute("data-val"));
        });
      });
    });
    var sub = qs(document, "#rs-tfng-submit");
    if (sub) {
      sub.addEventListener("click", function () {
        var rows = qsa(root, ".rs-tfng-row");
        var correct = 0;
        rows.forEach(function (row) {
          var pick = row.getAttribute("data-answer") || "";
          var want = row.getAttribute("data-correct") || "";
          if (pick === want) correct += 1;
        });
        var fb = qs(document, "#rs-tfng-feedback");
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-lab-feedback rs-lab-feedback--ok";
          fb.textContent =
            "Score: " +
            correct +
            " / " +
            rows.length +
            ". S1: False (passage says unclear priorities dominate, not video fatigue). S2: False (productivity stays stable). S3: True (exit surveys).";
        }
      });
    }
  }

  function initYnng() {
    var root = qs(document, "#rs-ynng-block");
    if (!root) return;
    qsa(root, ".rs-tfng-row").forEach(function (row) {
      var idx = row.getAttribute("data-stmt");
      qsa(row, ".rs-tfng-choice").forEach(function (btn) {
        btn.addEventListener("click", function () {
          tfngPick(root, idx, btn.getAttribute("data-val"));
        });
      });
    });
    var sub = qs(document, "#rs-ynng-submit");
    if (sub) {
      sub.addEventListener("click", function () {
        var rows = qsa(root, ".rs-tfng-row");
        var correct = 0;
        rows.forEach(function (row) {
          var pick = row.getAttribute("data-answer") || "";
          var want = row.getAttribute("data-correct") || "";
          if (pick === want) correct += 1;
        });
        var fb = qs(document, "#rs-ynng-feedback");
        if (fb) {
          fb.hidden = false;
          fb.className = "rs-lab-feedback rs-lab-feedback--ok";
          fb.textContent =
            "Score: " +
            correct +
            " / " +
            rows.length +
            ". S1: No (author presents both sides). S2: Not Given (no personal pledge). S3: Yes (states regulations could help).";
        }
      });
    }
  }

  /* ——— Speed reading ——— */
  function initSpeed() {
    var start = qs(document, "#rs-speed-start");
    var wrap = qs(document, "#rs-speed-reading-wrap");
    var passage = qs(document, "#rs-speed-passage");
    var bar = qs(document, "#rs-speed-bar");
    var done = qs(document, "#rs-speed-done");
    var quiz = qs(document, "#rs-speed-quiz");
    var wpmEl = qs(document, "#rs-speed-wpm");
    var startTs = 0;
    var wordCount = parseInt((passage && passage.getAttribute("data-word-count")) || "0", 10) || 1;

    if (start && wrap) {
      start.addEventListener("click", function () {
        start.hidden = true;
        wrap.hidden = false;
        startTs = Date.now();
        if (bar) {
          bar.style.transition = "none";
          bar.style.width = "100%";
          void bar.offsetWidth;
          bar.style.transition = "width 90s linear";
          bar.style.width = "0%";
        }
      });
    }
    if (done && wrap && quiz) {
      done.addEventListener("click", function () {
        var elapsedMin = (Date.now() - startTs) / 60000;
        if (elapsedMin < 0.05) elapsedMin = 0.05;
        var wpm = Math.round(wordCount / elapsedMin);
        wrap.hidden = true;
        quiz.hidden = false;
        if (wpmEl) {
          wpmEl.textContent =
            "Rough speed: about " +
            wpm +
            " wpm (≈" +
            wordCount +
            " words). Many Academic Reading sets need ~200 wpm with accuracy — use this drill to track pace.";
        }
      });
    }
    function speedFb(ok, msg) {
      var fb = qs(document, "#rs-speed-q-feedback");
      if (fb) {
        fb.hidden = false;
        fb.className = "rs-lab-feedback " + (ok ? "rs-lab-feedback--ok" : "rs-lab-feedback--bad");
        fb.textContent = msg;
      }
    }
    qsa(document, ".rs-speed-q1").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        speedFb(
          ok,
          ok
            ? "Q1 correct — the phased upgrade centres on signalling."
            : "Q1: the passage opens with signalling equipment across three lines."
        );
      });
    });
    qsa(document, ".rs-speed-q2").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ok = btn.getAttribute("data-correct") === "1";
        speedFb(
          ok,
          ok
            ? "Q2 correct — work completes in December."
            : "Q2: connections advice runs until work completes in December."
        );
      });
    });
  }

  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  onReady(function () {
    initMainTabs();
    initSkillTabs();
    initScanning();
    initSkimming();
    initParaphrase();
    initTfng();
    initYnng();
    initSpeed();
  });
})();
