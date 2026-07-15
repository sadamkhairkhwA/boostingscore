/**
 * Reading journey — four-stage course navigation + question types sub-course.
 */
(function () {
  "use strict";

  function qs(root, sel) {
    return (root || document).querySelector(sel);
  }
  function qsa(root, sel) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  var STAGE_ORDER = ["strategies", "question-types", "skills", "time"];
  var currentStage = "strategies";

  function parseJsonScript(id) {
    var el = qs(document, id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  function initJourney() {
    var journey = qs(document, "#rs-reading-journey");
    if (!journey) return;

    var pills = qsa(journey, ".rs-journey-pill");
    var stages = qsa(document, ".rs-journey-stage");
    var fillEl = qs(journey, "#rs-journey-progress-fill");
    var labelEl = qs(journey, "#rs-journey-stage-label");

    function stageIndex(id) {
      return STAGE_ORDER.indexOf(id);
    }

    function goToStage(id, scroll) {
      if (STAGE_ORDER.indexOf(id) < 0) return;
      currentStage = id;
      var idx = stageIndex(id);

      pills.forEach(function (pill) {
        var on = pill.getAttribute("data-rs-stage") === id;
        var done = stageIndex(pill.getAttribute("data-rs-stage")) < idx;
        pill.classList.toggle("is-active", on);
        pill.classList.toggle("is-done", done && !on);
        if (on) pill.setAttribute("aria-current", "step");
        else pill.removeAttribute("aria-current");
      });

      stages.forEach(function (stage) {
        var on = stage.getAttribute("data-rs-stage") === id;
        stage.classList.toggle("is-active", on);
        stage.hidden = !on;
      });

      if (fillEl) {
        fillEl.style.width = ((idx + 1) / STAGE_ORDER.length) * 100 + "%";
      }

      if (labelEl) {
        var activePill = pills.find(function (p) {
          return p.getAttribute("data-rs-stage") === id;
        });
        labelEl.textContent = activePill
          ? "Stage " + (idx + 1) + " of " + STAGE_ORDER.length + " — " + activePill.textContent.trim()
          : "";
      }

      if (scroll !== false) {
        journey.scrollIntoView({ block: "start", behavior: "smooth" });
      }

      document.dispatchEvent(
        new CustomEvent("rs-journey-stage", { detail: { stage: id } })
      );
    }

    pills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        goToStage(pill.getAttribute("data-rs-stage"));
      });
    });

    qsa(document, "[data-rs-goto-stage]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        goToStage(btn.getAttribute("data-rs-goto-stage"));
      });
    });

    window.ReadingJourney = { goToStage: goToStage };
    goToStage("strategies", false);
  }

  function initSubCourse(config) {
    var course = qs(document, config.containerId);
    if (!course || !window.ReadingPractice) return null;

    var data = parseJsonScript(config.dataScriptId);
    if (!data) return null;

    var lessonCount = parseInt(course.getAttribute("data-rs-lesson-count") || "0", 10);
    var units = qsa(course, config.unitSelector || ".rs-course-unit");
    var pills = qsa(course, config.pillSelector);
    var backBtn = qs(course, config.backBtnId);
    var nextBtn = qs(course, config.nextBtnId);
    var fillEl = qs(course, config.fillId);
    var phaseBadge = qs(course, config.phaseBadgeId);
    var progressLabel = qs(course, config.progressLabelId);

    var lessonIdx = 0;
    var phase = "learn";
    var hasReview = !!config.reviewKey;
    var totalSteps = lessonCount * 2 + (hasReview ? 1 : 0);

    window.ReadingPractice.mountPracticeHosts(course, data, function (id) {
      if (id === config.reviewKey) {
        return {
          instructions: null,
          passage: null,
          questions: (data.mixedReview && data.mixedReview.questions) || [],
        };
      }
      var i;
      for (i = 0; i < (data.lessons || []).length; i++) {
        if (data.lessons[i].id === id) return data.lessons[i].practice;
      }
      return null;
    });

    function stepIndex() {
      if (phase === "review") return lessonCount * 2;
      return lessonIdx * 2 + (phase === "practice" ? 1 : 0);
    }

    function activeUnit() {
      if (phase === "review") {
        return qs(course, '.rs-course-unit[data-rs-lesson="review"]');
      }
      return units[lessonIdx];
    }

    function updateMeta() {
      var step = stepIndex();
      if (fillEl) fillEl.style.width = ((step + 1) / totalSteps) * 100 + "%";

      pills.forEach(function (pill) {
        var key = pill.getAttribute("data-rs-lesson");
        var isReview = phase === "review";
        var pillLesson = key === "review" ? "review" : parseInt(key, 10);
        var on =
          (isReview && pillLesson === "review") ||
          (!isReview && pillLesson === lessonIdx);
        var done =
          !isReview &&
          typeof pillLesson === "number" &&
          (pillLesson < lessonIdx ||
            (pillLesson === lessonIdx && phase === "practice"));

        pill.classList.toggle("is-active", on);
        pill.classList.toggle("is-done", done && !on);
        if (on) pill.setAttribute("aria-current", "step");
        else pill.removeAttribute("aria-current");
      });

      if (phaseBadge) {
        if (phase === "learn") phaseBadge.textContent = "Learn";
        else if (phase === "practice") phaseBadge.textContent = "Practice";
        else phaseBadge.textContent = "Review";
      }

      if (progressLabel) {
        if (phase === "review") {
          progressLabel.textContent = config.reviewLabel || "Mixed review";
        } else {
          progressLabel.textContent =
            (config.lessonLabel || "Lesson") +
            " " +
            (lessonIdx + 1) +
            " of " +
            lessonCount;
        }
      }
    }

    function render() {
      units.forEach(function (unit, i) {
        var isReviewUnit = unit.getAttribute("data-rs-lesson") === "review";
        var show =
          (phase === "review" && isReviewUnit) ||
          (phase !== "review" && i === lessonIdx);
        unit.classList.toggle("is-active", show);
        unit.hidden = !show;

        if (!isReviewUnit) {
          var learn = qs(unit, '[data-rs-phase="learn"]');
          var practice = qs(unit, '[data-rs-phase="practice"]');
          if (learn) {
            var learnOn = show && phase === "learn";
            learn.classList.toggle("is-active", learnOn);
            learn.hidden = !learnOn;
          }
          if (practice) {
            var practiceOn = show && phase === "practice";
            practice.classList.toggle("is-active", practiceOn);
            practice.hidden = !practiceOn;
          }
        }
      });

      if (backBtn) {
        backBtn.disabled = lessonIdx === 0 && phase === "learn";
      }

      var arrow =
        '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M9 18l6-6-6-6"/></svg>';

      if (nextBtn) {
        if (phase === "learn") {
          nextBtn.innerHTML = "Start practice " + arrow;
          nextBtn.disabled = false;
          nextBtn.hidden = false;
        } else if (phase === "practice") {
          var unit = activeUnit();
          var complete = window.ReadingPractice.allAnsweredIn(unit);
          if (lessonIdx < lessonCount - 1) {
            nextBtn.innerHTML = "Next lesson " + arrow;
            nextBtn.disabled = !complete;
          } else if (hasReview) {
            nextBtn.innerHTML = "Mixed review " + arrow;
            nextBtn.disabled = !complete;
          } else if (config.completeLabel) {
            nextBtn.innerHTML = config.completeLabel + " " + arrow;
            nextBtn.disabled = !complete;
          } else {
            nextBtn.innerHTML = "Next " + arrow;
            nextBtn.disabled = !complete;
          }
          nextBtn.hidden = false;
        } else {
          var reviewUnit = activeUnit();
          var reviewDone = window.ReadingPractice.allAnsweredIn(reviewUnit);
          if (config.completeLabel && reviewDone) {
            nextBtn.innerHTML = config.completeLabel + " " + arrow;
            nextBtn.disabled = false;
          } else {
            nextBtn.innerHTML = reviewDone
              ? '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg> Complete'
              : "Answer all questions";
            nextBtn.disabled = !reviewDone;
          }
          nextBtn.hidden = false;
        }
      }

      updateMeta();
    }

    function goToLesson(idx, targetPhase) {
      if (idx < 0 || idx >= lessonCount) return;
      lessonIdx = idx;
      phase = targetPhase || "learn";
      render();
    }

    pills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        var key = pill.getAttribute("data-rs-lesson");
        if (key === "review") {
          phase = "review";
          render();
        } else {
          var idx = parseInt(key, 10);
          if (!isNaN(idx)) goToLesson(idx, "learn");
        }
      });
    });

    if (backBtn) {
      backBtn.addEventListener("click", function () {
        if (phase === "review") {
          goToLesson(lessonCount - 1, "practice");
        } else if (phase === "practice") {
          phase = "learn";
          render();
        } else if (lessonIdx > 0) {
          goToLesson(lessonIdx - 1, "practice");
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        if (nextBtn.disabled) return;
        if (phase === "learn") {
          phase = "practice";
          render();
        } else if (phase === "practice") {
          if (lessonIdx < lessonCount - 1) {
            goToLesson(lessonIdx + 1, "learn");
          } else if (hasReview) {
            phase = "review";
            render();
          } else if (config.onComplete) {
            config.onComplete();
          }
        } else if (phase === "review" && config.onComplete) {
          config.onComplete();
        }
      });
    }

    document.addEventListener("rs-practice-answered", function () {
      render();
    });

    render();
    return { render: render };
  }

  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  onReady(function () {
    initJourney();

    initSubCourse({
      containerId: "#rs-core-course",
      dataScriptId: "#rs-core-course-data",
      pillSelector: "#rs-course-lessons .rs-core-step-pill",
      backBtnId: "#rs-course-back",
      nextBtnId: "#rs-course-next",
      fillId: "#rs-course-progress-fill",
      phaseBadgeId: "#rs-course-phase-badge",
      progressLabelId: "#rs-course-progress-label",
      reviewKey: "mixed-review",
      reviewLabel: "Mixed review",
      lessonLabel: "Lesson",
      completeLabel: "Continue to question types",
      onComplete: function () {
        if (window.ReadingJourney) window.ReadingJourney.goToStage("question-types");
      },
    });

    initSubCourse({
      containerId: "#rs-qtypes-course",
      dataScriptId: "#rs-qtypes-course-data",
      pillSelector: "#rs-qtypes-lessons .rs-core-step-pill",
      backBtnId: "#rs-qtypes-back",
      nextBtnId: "#rs-qtypes-next",
      fillId: "#rs-qtypes-progress-fill",
      phaseBadgeId: "#rs-qtypes-phase-badge",
      progressLabelId: "#rs-qtypes-progress-label",
      lessonLabel: "Type",
      completeLabel: "Continue to skills lab",
      onComplete: function () {
        if (window.ReadingJourney) window.ReadingJourney.goToStage("skills");
      },
    });
  });
})();
