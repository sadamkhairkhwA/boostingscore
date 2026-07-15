(() => {
  const root = document.getElementById("wl-lesson-flow");
  if (!root) return;

  const checkUrl = root.dataset.checkUrl;
  const csrfToken = root.dataset.csrf;
  const minWords = 5;

  const panels = {
    learn: document.getElementById("wl-panel-learn"),
    practice: document.getElementById("wl-panel-practice"),
    feedback: document.getElementById("wl-panel-feedback"),
  };
  const stepEls = root.querySelectorAll("[data-wl-step]");
  const textarea = document.getElementById("wl-response");
  const wordCountEl = document.getElementById("wl-wordcount");
  const checkBtn = document.getElementById("wl-check-btn");
  const tryBtn = document.getElementById("wl-try-btn");
  const tryAgainBtn = document.getElementById("wl-try-again-btn");
  const errorEl = document.getElementById("wl-error");
  const prevBlock = document.getElementById("wl-prev-attempt");
  const prevText = document.getElementById("wl-prev-text");
  const successEl = document.getElementById("wl-success");
  const feedbackWell = document.getElementById("wl-fb-well");
  const feedbackMistakes = document.getElementById("wl-fb-mistakes");
  const feedbackImprove = document.getElementById("wl-fb-improve");
  const modelAnswer = document.getElementById("wl-model-answer");
  const backLearnBtn = document.getElementById("wl-back-learn-btn");

  const historyList = document.getElementById("wl-history-list");
  const historyWrap = document.getElementById("wl-history-wrap");
  const aiLoadingEl = document.getElementById("wl-ai-loading");
  let currentStep = "learn";
  let lastAttemptText = "";
  let activeLoading = null;

  function wordCount(text) {
    return (text || "").trim().split(/\s+/).filter(Boolean).length;
  }

  function setStep(step) {
    currentStep = step;
    Object.entries(panels).forEach(([key, el]) => {
      if (el) el.classList.toggle("is-visible", key === step);
    });
    stepEls.forEach((el) => {
      const s = el.dataset.wlStep;
      el.classList.toggle("is-active", s === step);
      const order = { learn: 0, practice: 1, feedback: 2 };
      el.classList.toggle("is-done", order[s] < order[step]);
    });
    window.scrollTo({ top: root.offsetTop - 12, behavior: "smooth" });
  }

  function updateWordCount() {
    const n = wordCount(textarea.value);
    wordCountEl.textContent = `${n} word${n === 1 ? "" : "s"}`;
    wordCountEl.classList.toggle("is-low", n > 0 && n < minWords);
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.remove("wl-hidden");
  }

  function clearError() {
    errorEl.textContent = "";
    errorEl.classList.add("wl-hidden");
  }

  function renderFeedback(fb, ready) {
    feedbackWell.innerHTML = "";
    (fb.what_you_did_well || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      feedbackWell.appendChild(li);
    });

    feedbackMistakes.innerHTML = "";
    const mistakes = fb.mistakes_and_fixes || [];
    if (!mistakes.length) {
      const p = document.createElement("p");
      p.textContent = "No significant mistakes for this skill.";
      p.style.color = "#6b7280";
      p.style.fontSize = "14px";
      feedbackMistakes.appendChild(p);
    } else {
      mistakes.forEach((m) => {
        const div = document.createElement("div");
        div.className = "wl-mistake";
        div.innerHTML = `
          <div class="wl-mistake__quote">"${escapeHtml(m.problem || "")}"</div>
          <div>${escapeHtml(m.why || "")}</div>
          <div class="wl-mistake__fix">→ ${escapeHtml(m.corrected || "")}</div>
        `;
        feedbackMistakes.appendChild(div);
      });
    }

    feedbackImprove.innerHTML = "";
    (fb.how_to_improve || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      feedbackImprove.appendChild(li);
    });

    modelAnswer.textContent = fb.model_answer || "";

    if (ready) {
      successEl.classList.remove("wl-hidden");
    } else {
      successEl.classList.add("wl-hidden");
    }
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function addHistoryItem(attemptNumber, wc, ready) {
    if (historyWrap) historyWrap.classList.remove("wl-hidden");
    const li = document.createElement("div");
    li.className = "wl-history-item";
    const badge = ready
      ? '<span class="wl-badge wl-badge--ready">Ready</span>'
      : '<span class="wl-badge wl-badge--retry">Keep practising</span>';
    li.innerHTML = `<span>Attempt ${attemptNumber} · ${wc} words</span>${badge}`;
    historyList.prepend(li);
  }

  backLearnBtn?.addEventListener("click", () => {
    if (activeLoading) {
      activeLoading.destroy();
      activeLoading = null;
    }
    clearError();
    setStep("learn");
  });

  tryBtn?.addEventListener("click", () => {
    if (activeLoading) {
      activeLoading.destroy();
      activeLoading = null;
    }
    clearError();
    setStep("practice");
    textarea.focus();
  });

  tryAgainBtn?.addEventListener("click", () => {
    if (activeLoading) {
      activeLoading.destroy();
      activeLoading = null;
    }
    clearError();
    if (lastAttemptText) {
      prevText.textContent = lastAttemptText;
      prevBlock.classList.remove("wl-hidden");
    }
    textarea.value = "";
    updateWordCount();
    setStep("practice");
    textarea.focus();
  });

  textarea?.addEventListener("input", updateWordCount);

  checkBtn?.addEventListener("click", async () => {
    clearError();
    const text = textarea.value.trim();
    const wc = wordCount(text);
    if (wc < minWords) {
      showError(`Write at least ${minWords} words before checking.`);
      return;
    }

    if (activeLoading) activeLoading.destroy();
    activeLoading = window.WritingAILoading?.begin({
      button: checkBtn,
      container: aiLoadingEl,
      mode: "lesson",
      buttonLabelChecking: "Checking your writing…",
    });

    const ctrl = new AbortController();
    const timeout = setTimeout(() => ctrl.abort(), 120000);

    try {
      const res = await fetch(checkUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ response_text: text }),
        signal: ctrl.signal,
      });
      clearTimeout(timeout);
      const data = await res.json();
      if (!data.ok) {
        const errMsg = data.error === "ai_limit" ? (data.message || "Daily limit reached — resets tomorrow.") : (data.error || "Couldn't check your answer. Try again.");
        activeLoading?.fail(errMsg);
        activeLoading = null;
        showError(errMsg);
        return;
      }
      if (window.BSPlanNotifyAiUsed) window.BSPlanNotifyAiUsed();
      activeLoading?.finish();
      activeLoading?.destroy();
      activeLoading = null;
      lastAttemptText = text;
      renderFeedback(data.feedback, data.ready);
      addHistoryItem(data.attempt_number, data.word_count, data.ready);
      if (data.completed) {
        const sub = root.querySelector(".wt1-sub");
        if (sub && !sub.textContent.includes("Complete")) {
          sub.insertAdjacentHTML(
            "beforeend",
            ' · <span style="color:#3B6D11;font-weight:700">Complete</span>'
          );
        }
      }
      setStep("feedback");
    } catch {
      clearTimeout(timeout);
      activeLoading?.fail("Couldn't check your answer. Try again.");
      activeLoading = null;
      showError("Couldn't check your answer. Try again.");
    }
  });

  updateWordCount();
})();
