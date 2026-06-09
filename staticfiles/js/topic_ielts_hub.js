/**
 * IELTS topic vocabulary hub: load tier word lists, mastery chips, session size, flashcard link.
 */
(function () {
  "use strict";

  var root = document.getElementById("topic-ielts-hub");
  if (!root) return;

  var topic = root.getAttribute("data-topic") || "";
  var topicLabel = root.getAttribute("data-topic-label") || topic;
  var apiUrl = root.getAttribute("data-api-url") || "";
  var flashcardBase = root.getAttribute("data-flashcard-url") || "";

  var TOPIC_EMOJI = {
    environment: "🌿",
    health: "🩺",
    technology: "💻",
    education: "🎓",
    society: "🏛️",
    travel: "✈️",
    science: "🔬",
    business: "💼",
  };

  var LEVEL_STYLE = {
    1: { iconBg: "#EAF3DE", icon: "📗", bar: "#3B6D11" },
    2: { iconBg: "#e8ecf8", icon: "📘", bar: "#1e3a8a" },
    3: { iconBg: "#fce8e8", icon: "📙", bar: "#7f1d1d" },
  };

  var elLoading = document.getElementById("topic-hub-loading");
  var elLoadingMsg = document.getElementById("topic-hub-loading-msg");
  var elError = document.getElementById("topic-hub-error");
  var elErrorMsg = document.getElementById("topic-hub-error-msg");
  var elLevels = document.getElementById("topic-hub-levels");
  var elOverall = document.getElementById("topic-hub-overall");
  var elOverallLabel = document.getElementById("topic-hub-overall-label");
  var elOverallFill = document.getElementById("topic-hub-overall-fill");
  var elOverallPct = document.getElementById("topic-hub-overall-pct");
  var elEmoji = document.getElementById("topic-hub-emoji");
  var elMeta = document.getElementById("topic-hub-meta");

  if (elEmoji) elEmoji.textContent = TOPIC_EMOJI[topic] || "📚";

  var state = {
    data: null,
    selectedWordIds: { 1: {}, 2: {}, 3: {} },
    selectedPill: { 1: "10", 2: "10", 3: "10" },
    expandedWords: { 1: false, 2: false, 3: false },
  };

  function sessionLimitOptions(n) {
    var base = [5, 10, 15, 20, 25, 30];
    return base.filter(function (p) {
      return p <= n;
    });
  }

  function buildFlashcardUrl(level, selectedCount, selectedIds) {
    var q =
      "topic=" +
      encodeURIComponent(topic) +
      "&level=" +
      encodeURIComponent(String(level)) +
      "&limit=" +
      encodeURIComponent(String(selectedCount || ""));
    if (selectedIds && selectedIds.length) {
      q += "&words=" + encodeURIComponent(selectedIds.join(","));
    }
    return flashcardBase + (flashcardBase.indexOf("?") >= 0 ? "&" : "?") + q;
  }

  function unmasteredCount(levelKey) {
    var lv = state.data && state.data.levels && state.data.levels[levelKey];
    if (!lv || !lv.words) return 0;
    var c = 0;
    lv.words.forEach(function (w) {
      if (!w.mastered) c += 1;
    });
    return c;
  }

  function selectedIdsForLevel(levelNum) {
    var bucket = state.selectedWordIds[levelNum] || {};
    var ids = [];
    Object.keys(bucket).forEach(function (id) {
      if (bucket[id]) ids.push(parseInt(id, 10));
    });
    ids.sort(function (a, b) {
      return a - b;
    });
    return ids;
  }

  function pickFirstN(words, n) {
    var unmastered = words.filter(function (w) {
      return !w.mastered;
    });
    var mastered = words.filter(function (w) {
      return w.mastered;
    });
    return unmastered.concat(mastered).slice(0, n);
  }

  function renderLevels() {
    if (!state.data || !state.data.levels) return;
    elLevels.innerHTML = "";
    [1, 2, 3].forEach(function (lvl) {
      var key = String(lvl);
      var lv = state.data.levels[key];
      if (!lv) return;
      var st = LEVEL_STYLE[lvl] || LEVEL_STYLE[1];
      var wc = lv.word_count || 0;
      if (!state.selectedWordIds[lvl] || Object.keys(state.selectedWordIds[lvl]).length === 0) {
        state.selectedWordIds[lvl] = {};
        (lv.words || []).forEach(function (w) {
          state.selectedWordIds[lvl][String(w.id)] = true;
        });
        state.selectedPill[lvl] = "all";
      }
      var limOpts = sessionLimitOptions(wc);
      var mastered = lv.mastered_in_level || 0;

      var card = document.createElement("section");
      card.className = "topic-hub-level";
      card.setAttribute("data-level", key);

      var head = document.createElement("div");
      head.className = "topic-hub-level__head";
      head.innerHTML =
        '<div class="topic-hub-level__icon" style="background:' +
        st.iconBg +
        '">' +
        st.icon +
        "</div>" +
        '<div class="topic-hub-level__head-text">' +
        "<h2 class=\"topic-hub-level__title\">" +
        escapeHtml(lv.title) +
        '</h2><span class="topic-hub-level__badge">' +
        wc +
        " words</span></div>";

      var desc = document.createElement("p");
      desc.className = "topic-hub-level__desc";
      desc.textContent = lv.description || "";

      var progWrap = document.createElement("div");
      progWrap.className = "topic-hub-level__prog";
      var pct = wc ? Math.round((100 * mastered) / wc) : 0;
      progWrap.innerHTML =
        '<div class="topic-hub-level__prog-row">' +
        "<span>" +
        mastered +
        " of " +
        wc +
        " mastered</span><span>" +
        pct +
        "%</span></div>" +
        '<div class="topic-hub-level__prog-track"><div class="topic-hub-level__prog-fill" style="width:' +
        pct +
        "%;background:" +
        st.bar +
        '"></div></div>';

      var wordsLbl = document.createElement("p");
      wordsLbl.className = "topic-hub-level__words-lbl";
      wordsLbl.textContent = "WORDS — DARK = SELECTED · GREEN = MASTERED · TAP TO TOGGLE";

      var controls = document.createElement("div");
      controls.className = "topic-hub-level__controls";
      var selectedCount = selectedIdsForLevel(lvl).length;
      controls.innerHTML =
        '<div class="topic-hub-level__selected-count">' +
        selectedCount +
        ' words selected</div><div class="topic-hub-level__control-actions"><button type="button" class="topic-hub-level__control-btn" data-action="all">Select all</button><button type="button" class="topic-hub-level__control-btn" data-action="clear">Clear all</button></div>';

      var chipWrap = document.createElement("div");
      chipWrap.className = "topic-hub-level__chips";
      var chipsMore = document.createElement("div");
      chipsMore.className = "topic-hub-level__chips-inner";
      var words = lv.words || [];
      var maxFirst = 16;
      var opened = !!state.expandedWords[lvl];
      words.forEach(function (w, idx) {
        var chip = document.createElement("button");
        chip.type = "button";
        var isSel = !!state.selectedWordIds[lvl][String(w.id)];
        chip.className =
          "topic-hub-chip" +
          (w.mastered ? " is-mastered" : "") +
          (isSel ? " is-selected" : " is-inactive");
        chip.textContent = w.text;
        chip.title = w.mastered ? "Mastered (3× Easy)" : "Not mastered";
        chip.dataset.wordId = String(w.id);
        chip.dataset.level = String(lvl);
        chip.dataset.mastered = w.mastered ? "1" : "0";
        if (idx >= maxFirst) chip.hidden = !opened;
        chipsMore.appendChild(chip);
      });
      chipWrap.appendChild(chipsMore);

      var moreBtn = null;
      if (words.length > maxFirst) {
        moreBtn = document.createElement("button");
        moreBtn.type = "button";
        moreBtn.className = "topic-hub-chip topic-hub-chip--more";
        moreBtn.textContent = opened ? "Show less ▲" : "+" + (words.length - maxFirst) + " more ▼";
        moreBtn.addEventListener("click", function () {
          opened = !opened;
          state.expandedWords[lvl] = opened;
          chipsMore.querySelectorAll(".topic-hub-chip").forEach(function (c, i) {
            if (i >= maxFirst && !c.classList.contains("topic-hub-chip--more")) {
              c.hidden = !opened;
            }
          });
          moreBtn.textContent = opened
            ? "Show less ▲"
            : "+" + (words.length - maxFirst) + " more ▼";
        });
        chipWrap.appendChild(moreBtn);
      }

      var sessLbl = document.createElement("p");
      sessLbl.className = "topic-hub-level__sess-lbl";
      sessLbl.textContent = "Session size";

      var sessRow = document.createElement("div");
      sessRow.className = "topic-hub-level__sess-pills";
      limOpts.forEach(function (opt) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "topic-hub-sess-pill";
        b.textContent = String(opt);
        b.dataset.limit = String(opt);
        if (String(state.selectedPill[lvl]) === String(opt)) b.classList.add("is-active");
        sessRow.appendChild(b);
      });
      var allBtn = document.createElement("button");
      allBtn.type = "button";
      allBtn.className = "topic-hub-sess-pill";
      allBtn.textContent = "All " + wc;
      allBtn.dataset.limit = "all";
      if (String(state.selectedPill[lvl]) === "all") allBtn.classList.add("is-active");
      sessRow.appendChild(allBtn);
      var customPill = document.createElement("button");
      customPill.type = "button";
      customPill.className = "topic-hub-sess-pill";
      customPill.textContent = "Custom";
      customPill.dataset.limit = "custom";
      if (String(state.selectedPill[lvl]) === "custom") customPill.classList.add("is-active");
      sessRow.appendChild(customPill);

      function setActivePill(active) {
        sessRow.querySelectorAll(".topic-hub-sess-pill").forEach(function (p) {
          p.classList.toggle("is-active", p === active);
        });
      }

      function applyChipVisual(chipEl, isSelected) {
        var isMastered = chipEl.dataset.mastered === "1";
        chipEl.classList.toggle("is-selected", isSelected);
        chipEl.classList.toggle("is-inactive", !isSelected);
        chipEl.classList.toggle("is-mastered", isMastered);
      }

      function syncChipVisuals() {
        chipsMore.querySelectorAll(".topic-hub-chip[data-word-id]").forEach(function (chipEl) {
          var wid = chipEl.dataset.wordId;
          var isSelected = !!state.selectedWordIds[lvl][wid];
          applyChipVisual(chipEl, isSelected);
        });
      }

      function setCustomPill() {
        state.selectedPill[lvl] = "custom";
        sessRow.querySelectorAll(".topic-hub-sess-pill").forEach(function (p) {
          p.classList.toggle("is-active", p.dataset.limit === "custom");
        });
      }

      function applyPillSelection(lim) {
        var toPick = [];
        var picked = {};
        if (lim === "all") {
          toPick = words.slice();
          state.selectedPill[lvl] = "all";
        } else {
          var n = parseInt(lim, 10);
          if (!isNaN(n) && n > 0) {
            toPick = pickFirstN(words, n);
            state.selectedPill[lvl] = String(n);
          }
        }
        toPick.forEach(function (w) {
          picked[String(w.id)] = true;
        });
        state.selectedWordIds[lvl] = picked;
        syncChipVisuals();
      }

      controls.addEventListener("click", function (e) {
        var btn = e.target.closest(".topic-hub-level__control-btn");
        if (!btn || !controls.contains(btn)) return;
        var action = btn.dataset.action;
        if (action === "all") {
          var allPicked = {};
          state.selectedWordIds[lvl] = {};
          words.forEach(function (w) {
            allPicked[String(w.id)] = true;
          });
          state.selectedPill[lvl] = "all";
          state.selectedWordIds[lvl] = allPicked;
          syncChipVisuals();
          sessRow.querySelectorAll(".topic-hub-sess-pill").forEach(function (p) {
            p.classList.toggle("is-active", p.dataset.limit === "all");
          });
          updateFooter();
          return;
        }
        state.selectedWordIds[lvl] = {};
        state.selectedPill[lvl] = "custom";
        syncChipVisuals();
        sessRow.querySelectorAll(".topic-hub-sess-pill").forEach(function (p) {
          p.classList.toggle("is-active", p.dataset.limit === "custom");
        });
        updateFooter();
      });

      sessRow.addEventListener("click", function (e) {
        var t = e.target.closest(".topic-hub-sess-pill");
        if (!t || !sessRow.contains(t)) return;
        var lim = t.dataset.limit;
        if (lim === "custom") return;
        applyPillSelection(lim);
        setActivePill(t);
        updateFooter();
      });

      chipWrap.addEventListener("click", function (e) {
        var chip = e.target.closest(".topic-hub-chip");
        if (!chip || !chipWrap.contains(chip)) return;
        if (chip.classList.contains("topic-hub-chip--more")) return;
        var id = chip.dataset.wordId;
        if (!id) return;
        state.selectedWordIds[lvl][id] = !state.selectedWordIds[lvl][id];
        applyChipVisual(chip, !!state.selectedWordIds[lvl][id]);
        setCustomPill();
        updateFooter();
      });

      var foot = document.createElement("p");
      foot.className = "topic-hub-level__foot";
      var cta = document.createElement("a");
      cta.className = "topic-hub-level__cta";
      cta.textContent = "Start " + lv.title + " — ";

      function updateFooter() {
        var selectedIds = selectedIdsForLevel(lvl);
        var selectedN = selectedIds.length;
        var unmasteredTotal = words.filter(function (w) {
          return !w.mastered;
        }).length;
        var selectedCountEl = controls.querySelector(".topic-hub-level__selected-count");
        if (selectedCountEl) selectedCountEl.textContent = selectedN + " words selected";
        foot.textContent =
          "You selected " +
          selectedN +
          " cards" +
          " · " +
          unmasteredTotal +
          " words still unmastered";
        cta.textContent =
          "Start " + lv.title + " — " + selectedN + " cards →";
        cta.href = buildFlashcardUrl(lvl, selectedN, selectedIds);
        cta.classList.toggle("is-disabled", selectedN === 0);
        cta.setAttribute("aria-disabled", selectedN === 0 ? "true" : "false");
        if (selectedN === 0) {
          cta.removeAttribute("href");
        }
      }

      updateFooter();
      syncChipVisuals();

      card.appendChild(head);
      card.appendChild(desc);
      card.appendChild(progWrap);
      card.appendChild(controls);
      card.appendChild(wordsLbl);
      card.appendChild(chipWrap);
      card.appendChild(sessLbl);
      card.appendChild(sessRow);
      card.appendChild(foot);
      card.appendChild(cta);
      elLevels.appendChild(card);
    });
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function renderOverall() {
    if (!state.data) return;
    var t = state.data.total_words || 0;
    var m = state.data.mastered_total || 0;
    var p = state.data.overall_pct || 0;
    elOverall.hidden = false;
    elOverallLabel.textContent =
      "Overall progress — " + m + " of " + t + " words mastered";
    elOverallFill.style.width = p + "%";
    elOverallPct.textContent = p + "%";
    elMeta.textContent = t + " words · 3 levels · start anywhere";
  }

  async function fetchJson(url) {
    var res = await fetch(url, { credentials: "same-origin" });
    try {
      return await res.json();
    } catch (e) {
      return {
        ok: false,
        status: "error",
        message: "Could not load words — tap to retry",
      };
    }
  }

  async function loadHub(force) {
    var url = apiUrl + (force ? "?force=1" : "");
    var attempts = 0;
    while (attempts < 90) {
      var data = await fetchJson(url);
      if (data.status === "generating") {
        if (elLoadingMsg) elLoadingMsg.textContent = "Loading vocabulary…";
        await new Promise(function (r) {
          setTimeout(r, 2000);
        });
        attempts += 1;
        url = apiUrl;
        continue;
      }
      return data;
    }
    return { ok: false, status: "error", message: "Could not load words — tap to retry" };
  }

  async function init() {
    elError.hidden = true;
    elLevels.hidden = true;
    elOverall.hidden = true;
    elLoading.hidden = false;
    if (elLoadingMsg) elLoadingMsg.textContent = "Loading vocabulary…";

    try {
      var data = await loadHub(false);
      if (!data.ok || data.status === "error") {
        elLoading.hidden = true;
        elError.hidden = false;
        if (elErrorMsg)
          elErrorMsg.textContent =
            data.message || "Could not load words — tap to retry";
        return;
      }
      state.data = data;
      elLoading.hidden = true;
      elLevels.hidden = false;
      renderOverall();
      renderLevels();
    } catch (e) {
      elLoading.hidden = true;
      elError.hidden = false;
    }
  }

  elError.addEventListener("click", function () {
    elError.hidden = true;
    elLoading.hidden = false;
    loadHub(true).then(function (data) {
      if (!data.ok || data.status === "error") {
        elLoading.hidden = true;
        elError.hidden = false;
        if (elErrorMsg)
          elErrorMsg.textContent =
            data.message || "Could not load words — tap to retry";
        return;
      }
      state.data = data;
      elLoading.hidden = true;
      elLevels.hidden = false;
      renderOverall();
      renderLevels();
    });
  });

  init();
})();
