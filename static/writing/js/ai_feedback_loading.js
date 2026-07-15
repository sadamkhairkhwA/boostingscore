/**
 * Shared loading UI for Writing AI feedback (Task 1, Task 2, lesson practice).
 */
(function () {
  "use strict";

  var GREEN = "#3B6D11";
  var GREY = "#d1d5db";

  var CRITERIA_TASK1 = [
    "Task achievement",
    "Coherence and cohesion",
    "Lexical resource",
    "Grammatical range and accuracy",
  ];
  var CRITERIA_TASK2 = [
    "Task response",
    "Coherence and cohesion",
    "Lexical resource",
    "Grammatical range and accuracy",
  ];

  function spinnerSvg(size) {
    var s = size || 16;
    return (
      '<svg class="wt1-ai-spin" width="' +
      s +
      '" height="' +
      s +
      '" viewBox="0 0 16 16" aria-hidden="true">' +
      '<circle cx="8" cy="8" r="6" fill="none" stroke="' +
      GREY +
      '" stroke-width="2"/>' +
      '<path d="M8 2a6 6 0 0 1 6 6" fill="none" stroke="' +
      GREEN +
      '" stroke-width="2" stroke-linecap="round"/>' +
      "</svg>"
    );
  }

  function emptyCircleSvg() {
    return (
      '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">' +
      '<circle cx="9" cy="9" r="7" fill="none" stroke="' +
      GREY +
      '" stroke-width="1.5"/>' +
      "</svg>"
    );
  }

  function checkSvg() {
    return (
      '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">' +
      '<circle cx="9" cy="9" r="7" fill="' +
      GREEN +
      '"/>' +
      '<path d="M5.5 9.2 7.8 11.5 12.5 6.8" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>"
    );
  }

  function skeletonHtml() {
    return (
      '<div class="wt1-ai-loading__skeleton" aria-hidden="true">' +
      '<div class="wt1-ai-loading__skel-bar"></div>' +
      '<div class="wt1-ai-loading__skel-bar"></div>' +
      '<div class="wt1-ai-loading__skel-bar"></div>' +
      '<div class="wt1-ai-loading__skel-bar"></div>' +
      "</div>"
    );
  }

  function hintHtml() {
    return '<p class="wt1-ai-loading__hint">This usually takes a few seconds. Please don\'t close the page.</p>';
  }

  function criteriaListHtml(labels) {
    var items = labels
      .map(function (label, i) {
        return (
          '<li class="wt1-ai-loading__criterion" data-criterion-idx="' +
          i +
          '">' +
          '<span class="wt1-ai-loading__icon">' +
          emptyCircleSvg() +
          "</span>" +
          '<span class="wt1-ai-loading__label">' +
          label +
          "</span>" +
          "</li>"
        );
      })
      .join("");
    return '<ul class="wt1-ai-loading__criteria" aria-live="polite">' + items + "</ul>";
  }

  function setButtonLoading(btn, label) {
    if (!btn) return;
    btn.disabled = true;
    btn.classList.add("is-loading");
    btn.setAttribute("aria-busy", "true");
    btn.innerHTML = spinnerSvg(16) + '<span>' + label + "</span>";
  }

  function restoreButton(btn, originalHtml) {
    if (!btn) return;
    btn.disabled = false;
    btn.classList.remove("is-loading");
    btn.removeAttribute("aria-busy");
    btn.innerHTML = originalHtml;
  }

  function begin(opts) {
    var button = opts.button;
    var container = opts.container;
    var mode = opts.mode || "criteria";
    var task = opts.task || "task1";
    var checkingLabel = opts.buttonLabelChecking || "Checking your answer…";
    var labels = task === "task2" ? CRITERIA_TASK2 : CRITERIA_TASK1;
    var timers = [];
    var done = false;
    var originalHtml = button ? button.innerHTML : "";

    var linkedButtons = [];
    if (button && button.form) {
      var formId = button.form.id;
      if (formId) {
        document.querySelectorAll('[form="' + formId + '"]').forEach(function (el) {
          if (el !== button && el.tagName === "BUTTON") linkedButtons.push(el);
        });
      }
    }
    var linkedOriginals = linkedButtons.map(function (b) {
      return b.innerHTML;
    });
    linkedButtons.forEach(function (b) {
      b.disabled = true;
    });

    setButtonLoading(button, checkingLabel);

    if (container) {
      container.hidden = false;
      container.classList.remove("wl-hidden");
      var body =
        mode === "lesson"
          ? '<div class="wt1-ai-loading__lesson"><span class="wt1-ai-loading__lesson-spin">' +
            spinnerSvg(18) +
            '</span><span class="wt1-ai-loading__lesson-text">Checking your writing…</span></div>'
          : mode === "simple"
            ? ""
            : criteriaListHtml(labels);
      container.innerHTML =
        '<div class="wt1-ai-loading__card">' + body + skeletonHtml() + hintHtml() + "</div>";
    }

    if (mode === "criteria" && container) {
      var items = container.querySelectorAll(".wt1-ai-loading__criterion");
      var step = 0;

      function tickStep() {
        if (done || step >= items.length) return;
        for (var i = 0; i < items.length; i++) {
          var li = items[i];
          var icon = li.querySelector(".wt1-ai-loading__icon");
          li.classList.remove("is-active", "is-done");
          if (i < step) {
            li.classList.add("is-done");
            if (icon) icon.innerHTML = checkSvg();
          } else if (i === step) {
            li.classList.add("is-active");
            if (icon) icon.innerHTML = spinnerSvg(18);
          } else if (icon) {
            icon.innerHTML = emptyCircleSvg();
          }
        }
        step += 1;
        if (step <= items.length && !done) {
          timers.push(setTimeout(tickStep, 1200));
        }
      }
      timers.push(setTimeout(tickStep, 200));
    }

    function clearTimers() {
      timers.forEach(clearTimeout);
      timers = [];
    }

    function markAllDone() {
      if (mode !== "criteria" || !container) return;
      container.querySelectorAll(".wt1-ai-loading__criterion").forEach(function (li) {
        li.classList.remove("is-active");
        li.classList.add("is-done");
        var icon = li.querySelector(".wt1-ai-loading__icon");
        if (icon) icon.innerHTML = checkSvg();
      });
    }

    return {
      finish: function () {
        done = true;
        clearTimers();
        markAllDone();
      },
      fail: function (message) {
        done = true;
        clearTimers();
        restoreButton(button, originalHtml);
        linkedButtons.forEach(function (b, i) {
          b.disabled = false;
          b.innerHTML = linkedOriginals[i];
        });
        if (container) {
          container.hidden = true;
          container.classList.add("wl-hidden");
          container.innerHTML = "";
        }
        if (typeof opts.onFail === "function") {
          opts.onFail(message || "Couldn't check your answer. Try again.");
        }
      },
      destroy: function () {
        done = true;
        clearTimers();
        restoreButton(button, originalHtml);
        linkedButtons.forEach(function (b, i) {
          b.disabled = false;
          b.innerHTML = linkedOriginals[i];
        });
        if (container) {
          container.hidden = true;
          container.classList.add("wl-hidden");
          container.innerHTML = "";
        }
      },
    };
  }

  window.WritingAILoading = { begin: begin };
})();
