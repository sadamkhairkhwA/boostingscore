(() => {
  "use strict";

  const root = document.getElementById("wp-root");
  if (!root) return;

  const sentenceUrl = root.dataset.sentenceUrl;
  const checkUrl = root.dataset.checkUrl;
  const csrfToken = root.dataset.csrf;

  const modeBtns = root.querySelectorAll(".wp-mode-tabs [data-mode]");
  const topicPanel = document.getElementById("wp-topic-panel");
  const topicPills = root.querySelectorAll(".wp-topic-pill");
  const newBtn = document.getElementById("wp-new-sentence");
  const sourceEl = document.getElementById("wp-source");
  const paraphraseEl = document.getElementById("wp-paraphrase");
  const topicTag = document.getElementById("wp-topic-tag");
  const feedbackBtn = document.getElementById("wp-feedback-btn");
  const loadingEl = document.getElementById("wp-ai-loading");
  const errorEl = document.getElementById("wp-error");
  const feedbackEl = document.getElementById("wp-feedback");
  const prevBlock = document.getElementById("wp-prev-attempt");
  const prevText = document.getElementById("wp-prev-text");

  const TECHNIQUE_LABELS = {
    synonym_replacement: "Synonym replacement",
    word_form_change: "Word-form change",
    voice_change: "Voice change",
    clause_structure_change: "Clause/structure change",
  };

  const TECHNIQUE_ORDER = [
    "synonym_replacement",
    "word_form_change",
    "voice_change",
    "clause_structure_change",
  ];

  let mode = "bank";
  let topic = "all";
  let activeLoading = null;
  let lastAttemptText = "";

  function wordCount(text) {
    return (text || "").trim().split(/\s+/).filter(Boolean).length;
  }

  function show(el) {
    if (!el) return;
    el.hidden = false;
    el.classList.remove("wp-hidden");
  }

  function hide(el) {
    if (!el) return;
    el.hidden = true;
    el.classList.add("wp-hidden");
  }

  function showError(msg) {
    if (!errorEl) return;
    errorEl.textContent = msg;
    show(errorEl);
  }

  function clearError() {
    if (!errorEl) return;
    errorEl.textContent = "";
    hide(errorEl);
  }

  function clearPrevAttempt() {
    lastAttemptText = "";
    if (prevText) prevText.textContent = "";
    hide(prevBlock);
  }

  function clearPracticeState() {
    clearError();
    hide(feedbackEl);
    clearPrevAttempt();
    if (paraphraseEl) paraphraseEl.value = "";
  }

  function setMode(next) {
    mode = next;
    modeBtns.forEach((btn) => {
      const on = btn.dataset.mode === mode;
      btn.classList.toggle("wt1-btn--dark", on);
      btn.classList.toggle("wt1-btn--outline", !on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    if (topicPanel) {
      topicPanel.classList.toggle("wp-hidden", mode !== "bank");
      topicPanel.hidden = mode !== "bank";
    }
    if (sourceEl) {
      const editable = mode === "own";
      sourceEl.readOnly = !editable;
      sourceEl.classList.toggle("is-editable", editable);
      if (editable) {
        sourceEl.placeholder = "Type or paste a sentence you want to paraphrase…";
        if (topicTag) topicTag.textContent = "Your sentence";
      } else {
        sourceEl.placeholder = "";
        if (topicTag) topicTag.textContent = root.dataset.initialTopicLabel || topic;
      }
    }
    clearPracticeState();
  }

  function setTopic(code) {
    topic = code;
    topicPills.forEach((pill) => {
      pill.classList.toggle("is-on", pill.dataset.topic === code);
    });
  }

  async function loadSentence(exclude) {
    if (mode !== "bank") return;
    const params = new URLSearchParams({ topic });
    if (exclude) params.set("exclude", exclude);
    try {
      const res = await fetch(`${sentenceUrl}?${params}`, { credentials: "same-origin" });
      const data = await res.json();
      if (!data.ok) throw new Error("load failed");
      if (sourceEl) sourceEl.value = data.sentence || "";
      if (topicTag) topicTag.textContent = data.topic_label || "";
      root.dataset.initialTopicLabel = data.topic_label || "";
    } catch {
      showError("Couldn't load a new sentence. Try again.");
    }
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatVerdict(fb) {
    const verdict = String(fb.verdict || "").trim();
    const band = Number(fb.band_score);
    if (verdict) return verdict;
    if (Number.isFinite(band) && band > 0) {
      return `Band ${band.toFixed(1)} — reasonable attempt; keep varying structure and vocabulary.`;
    }
    return "Feedback ready — review the techniques below.";
  }

  function renderTechniquePills(techniques) {
    const tech = techniques || {};
    return TECHNIQUE_ORDER.map((key) => {
      const used = !!tech[key];
      const label = TECHNIQUE_LABELS[key] || key;
      return (
        `<span class="wp-tech-pill ${used ? "wp-tech-pill--used" : "wp-tech-pill--unused"}">` +
        `${escapeHtml(label)}</span>`
      );
    }).join("");
  }

  function renderModelParaphrases(models) {
    const items = Array.isArray(models) ? models : [];
    if (!items.length) {
      return '<p class="wp-feedback__similarity">No model paraphrases available.</p>';
    }
    return items
      .map(
        (item) =>
          '<div class="wp-model-item">' +
          `<p class="wp-model-item__label">${escapeHtml(item.label || item.technique || "Technique")}</p>` +
          `<p class="wp-model-item__text">${escapeHtml(item.text || "")}</p>` +
          "</div>"
      )
      .join("");
  }

  function renderFeedback(fb) {
    if (!feedbackEl) return;

    const verdict = formatVerdict(fb);
    const bandMatch = verdict.match(/band\s*([\d.]+)/i);
    let verdictHtml = escapeHtml(verdict);
    if (bandMatch) {
      const bandStr = bandMatch[0];
      verdictHtml = verdictHtml.replace(
        escapeHtml(bandStr),
        `<span class="wp-feedback__verdict-band">${escapeHtml(bandStr)}</span>`
      );
    }

    const similarity = String(fb.similarity || "medium").toLowerCase();
    const simTagClass =
      similarity === "high"
        ? "wp-feedback__similarity-tag wp-feedback__similarity-tag--high"
        : "wp-feedback__similarity-tag";
    const simNote = fb.similarity_note
      ? escapeHtml(fb.similarity_note)
      : similarity === "high"
        ? "Your wording is very close to the source — vary structure and vocabulary more for IELTS paraphrasing."
        : "Overlap with the source is moderate — keep pushing for more varied grammar and vocabulary.";

    const newSentenceBtn =
      mode === "bank"
        ? '<button type="button" class="wt1-btn wt1-btn--outline" id="wp-feedback-new">New sentence</button>'
        : "";

    feedbackEl.innerHTML =
      '<div class="wp-feedback__card">' +
      `<p class="wp-feedback__verdict">${verdictHtml}</p>` +
      '<div class="wp-feedback__block"><h3>Techniques you used</h3>' +
      `<div class="wp-tech-pills">${renderTechniquePills(fb.techniques)}</div></div>` +
      '<div class="wp-feedback__block"><h3>Feedback</h3>' +
      `<p>${escapeHtml(fb.feedback || "")}</p></div>` +
      '<div class="wp-feedback__block"><h3>Similarity to source</h3>' +
      `<p class="wp-feedback__similarity"><span class="${simTagClass}">${escapeHtml(similarity)} overlap</span>${simNote}</p></div>` +
      '<div class="wp-feedback__block"><h3>Model paraphrases</h3>' +
      renderModelParaphrases(fb.model_paraphrases) +
      "</div>" +
      '<div class="wp-feedback__actions">' +
      '<button type="button" class="wt1-btn wt1-btn--green" id="wp-try-again">Try again</button>' +
      newSentenceBtn +
      "</div></div>";

    document.getElementById("wp-try-again")?.addEventListener("click", onTryAgain);
    document.getElementById("wp-feedback-new")?.addEventListener("click", onNewSentence);

    show(feedbackEl);
  }

  function onTryAgain() {
    if (activeLoading) {
      activeLoading.destroy();
      activeLoading = null;
    }
    clearError();
    if (lastAttemptText && prevText && prevBlock) {
      prevText.textContent = lastAttemptText;
      show(prevBlock);
    }
    if (paraphraseEl) {
      paraphraseEl.value = "";
      paraphraseEl.focus();
    }
    hide(feedbackEl);
    paraphraseEl?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  async function onNewSentence() {
    clearPracticeState();
    await loadSentence(sourceEl?.value || "");
    sourceEl?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  modeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.dataset.mode === mode) return;
      setMode(btn.dataset.mode);
      if (mode === "bank") {
        loadSentence();
      } else if (sourceEl) {
        sourceEl.value = "";
        sourceEl.focus();
      }
    });
  });

  topicPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      if (pill.dataset.topic === topic) return;
      clearPracticeState();
      setTopic(pill.dataset.topic);
      loadSentence();
    });
  });

  newBtn?.addEventListener("click", onNewSentence);

  feedbackBtn?.addEventListener("click", async () => {
    clearError();
    hide(feedbackEl);

    const source = (sourceEl?.value || "").trim();
    const paraphrase = (paraphraseEl?.value || "").trim();

    if (!source) {
      showError(
        mode === "own"
          ? "Enter a source sentence before checking."
          : "Source sentence is missing — try New sentence."
      );
      return;
    }
    if (wordCount(paraphrase) < 3) {
      showError("Write your paraphrase before checking.");
      return;
    }

    if (activeLoading) activeLoading.destroy();
    activeLoading = window.WritingAILoading?.begin({
      button: feedbackBtn,
      container: loadingEl,
      mode: "simple",
      buttonLabelChecking: "Checking your answer…",
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
        body: JSON.stringify({
          source_text: source,
          paraphrase_text: paraphrase,
        }),
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
      lastAttemptText = paraphrase;
      hide(prevBlock);
      renderFeedback(data.feedback || {});
      feedbackEl?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch {
      clearTimeout(timeout);
      activeLoading?.fail("Couldn't check your answer. Try again.");
      activeLoading = null;
      showError("Couldn't check your answer. Try again.");
    }
  });

  setMode("bank");
  setTopic("all");
})();
