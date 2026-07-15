(function () {
  "use strict";

  function readPlanAi() {
    var el = document.getElementById("bs-plan-ai");
    if (!el || !el.textContent) return null;
    try {
      return JSON.parse(el.textContent);
    } catch {
      return null;
    }
  }

  function applyAiButtons(plan) {
    if (!plan || !plan.limited) return;
    var buttons = document.querySelectorAll("[data-ai-check-btn]");
    buttons.forEach(function (btn) {
      var wrap = btn.closest("[data-ai-check-wrap]") || btn.parentElement;
      var existing = wrap && wrap.querySelector(".plan-ai-counter");
      if (existing) existing.remove();

      var counter = document.createElement("span");
      counter.className = "plan-ai-counter" + (plan.at_limit ? " plan-ai-counter--limit" : "");
      counter.textContent = plan.at_limit ? plan.limit_message : plan.label;
      if (wrap) {
        wrap.insertBefore(counter, btn);
      }

      if (plan.at_limit) {
        btn.disabled = true;
        btn.classList.add("is-ai-limit");
        if (btn.tagName === "BUTTON") {
          btn.textContent = plan.limit_message;
        }
      }
    });
  }

  function bindDecrement(plan) {
    if (!plan || !plan.limited) return;
    document.addEventListener(
      "bs:ai-check-used",
      function () {
        if (plan.remaining > 0) {
          plan.remaining -= 1;
          plan.used += 1;
          plan.at_limit = plan.remaining <= 0;
          plan.label = plan.remaining + " of " + plan.limit + " checks left today";
          applyAiButtons(plan);
        }
      },
      false
    );
  }

  window.BSPlanNotifyAiUsed = function () {
    document.dispatchEvent(new CustomEvent("bs:ai-check-used"));
  };

  window.BSPlanReapplyAiButtons = function () {
    applyAiButtons(readPlanAi());
  };

  var plan = readPlanAi();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      applyAiButtons(plan);
      bindDecrement(plan);
    });
  } else {
    applyAiButtons(plan);
    bindDecrement(plan);
  }
})();
