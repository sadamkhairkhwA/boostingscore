/**
 * IELTS topic vocabulary hub — checklist word selection, session slider, flashcard link.
 */
(function () {
  "use strict";

  var GREEN = "#3B6D11";
  var LEVEL_STYLE = {
    1: { iconBg: "#EAF3DE", icon: "level-easy" },
    2: { iconBg: "#e8ecf8", icon: "level-medium" },
    3: { iconBg: "#fce8e8", icon: "level-hard" },
  };

  var CHECK_OFF =
    '<svg class="vocab-check-legend__icon" viewBox="0 0 20 20" width="18" height="18" aria-hidden="true">' +
    '<rect x="1.5" y="1.5" width="17" height="17" rx="3.5" fill="none" stroke="#c8c8c4" stroke-width="1.5"/></svg>';
  var CHECK_ON =
    '<svg class="vocab-check-legend__icon" viewBox="0 0 20 20" width="18" height="18" aria-hidden="true">' +
    '<rect x="1" y="1" width="18" height="18" rx="4" fill="#3B6D11"/>' +
    '<path d="M6 10l3 3 5-6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CHECK_MASTERED =
    '<svg class="vocab-check-legend__icon" viewBox="0 0 20 20" width="18" height="18" aria-hidden="true">' +
    '<circle cx="10" cy="10" r="9" fill="#3B6D11"/>' +
    '<path d="M6 10l2.5 2.5L14 7" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function rowIcon(mastered, selected) {
    if (mastered) return CHECK_MASTERED;
    if (selected) return CHECK_ON;
    return CHECK_OFF;
  }

  var root = document.getElementById("topic-ielts-hub");
  if (!root) return;

  var topic = root.getAttribute("data-topic") || "";
  var apiUrl = root.getAttribute("data-api-url") || "";
  var flashcardBase = root.getAttribute("data-flashcard-url") || "";

  var elLoading = document.getElementById("topic-hub-loading");
  var elLoadingMsg = document.getElementById("topic-hub-loading-msg");
  var elError = document.getElementById("topic-hub-error");
  var elErrorMsg = document.getElementById("topic-hub-error-msg");
  var elLevels = document.getElementById("topic-hub-levels");
  var elOverall = document.getElementById("topic-hub-overall");
  var elOverallLabel = document.getElementById("topic-hub-overall-label");
  var elOverallFill = document.getElementById("topic-hub-overall-fill");
  var elOverallPct = document.getElementById("topic-hub-overall-pct");
  var elMeta = document.getElementById("topic-hub-meta");

  var state = {
    data: null,
    selectedWordIds: { 1: {}, 2: {}, 3: {} },
    sessionSize: { 1: 10, 2: 10, 3: 10 },
    expandedWords: { 1: false, 2: false, 3: false },
    searchQuery: { 1: "", 2: "", 3: "" },
  };

  var VISIBLE_DEFAULT = 8;

  function sliderSteps(maxN) {
    var steps = [];
    for (var n = 5; n <= maxN; n += 5) steps.push(n);
    if (maxN >= 5 && steps.indexOf(maxN) < 0) steps.push(maxN);
    if (maxN < 5 && maxN > 0) steps.push(maxN);
    if (!steps.length) steps.push(5);
    return steps;
  }

  function nearestStep(val, steps) {
    var best = steps[0];
    var diff = Math.abs(val - best);
    steps.forEach(function (s) {
      var d = Math.abs(val - s);
      if (d < diff) {
        diff = d;
        best = s;
      }
    });
    return best;
  }

  function buildFlashcardUrl(level, limit, selectedIds) {
    var q =
      "topic=" +
      encodeURIComponent(topic) +
      "&level=" +
      encodeURIComponent(String(level)) +
      "&limit=" +
      encodeURIComponent(String(limit || ""));
    if (selectedIds && selectedIds.length) {
      q += "&words=" + encodeURIComponent(selectedIds.join(","));
    }
    return flashcardBase + (flashcardBase.indexOf("?") >= 0 ? "&" : "?") + q;
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

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function posShortLabel(raw) {
    var s = String(raw || "").trim().toLowerCase().replace(/\.+$/g, "");
    var map = {
      noun: "n.",
      "noun phrase": "n.",
      n: "n.",
      verb: "v.",
      v: "v.",
      adjective: "adj.",
      adj: "adj.",
      adverb: "adv.",
      adv: "adv.",
      phrase: "phrase",
    };
    return map[s] || "";
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
      var mastered = lv.mastered_in_level || 0;
      var band = lv.band_label || "Band 5";
      var words = lv.words || [];

      if (!state.selectedWordIds[lvl] || Object.keys(state.selectedWordIds[lvl]).length === 0) {
        state.selectedWordIds[lvl] = {};
        words.forEach(function (w) {
          state.selectedWordIds[lvl][String(w.id)] = !w.mastered;
        });
      }

      var steps = sliderSteps(wc || 65);
      if (!state.sessionSize[lvl] || steps.indexOf(state.sessionSize[lvl]) < 0) {
        state.sessionSize[lvl] = nearestStep(Math.min(10, wc || 10), steps);
      }

      var card = document.createElement("section");
      card.className = "topic-hub-level";
      card.setAttribute("data-level", key);

      var head = document.createElement("div");
      head.className = "topic-hub-level__head";
      head.innerHTML =
        '<div class="topic-hub-level__icon" style="background:' +
        st.iconBg +
        '">' +
        (typeof BSIcons !== "undefined" ? BSIcons.tile(st.icon, null, "md") : "") +
        "</div>" +
        '<div class="topic-hub-level__head-text">' +
        '<h2 class="topic-hub-level__title">' +
        escapeHtml(lv.title) +
        "</h2>" +
        '<p class="topic-hub-level__meta">' +
        escapeHtml(band) +
        " vocabulary · " +
        wc +
        " words</p></div>";

      var progWrap = document.createElement("div");
      progWrap.className = "topic-hub-level__prog";
      var pct = wc ? Math.round((100 * mastered) / wc) : 0;
      progWrap.innerHTML =
        '<div class="topic-hub-level__prog-row">' +
        "<span>" +
        mastered +
        " of " +
        wc +
        " mastered</span></div>" +
        '<div class="topic-hub-level__prog-track"><div class="topic-hub-level__prog-fill" style="width:' +
        pct +
        "%;background:" +
        GREEN +
        '"></div></div>';

      var controls = document.createElement("div");
      controls.className = "vocab-check-controls";
      controls.innerHTML =
        '<input type="search" class="vocab-check-search" placeholder="Search words…" aria-label="Search words" value="' +
        escapeHtml(state.searchQuery[lvl] || "") +
        '">' +
        '<div class="vocab-check-actions">' +
        '<button type="button" class="vocab-check-btn" data-action="all">Select all</button>' +
        '<button type="button" class="vocab-check-btn" data-action="clear">Clear</button>' +
        "</div>";

      var legend = document.createElement("div");
      legend.className = "vocab-check-legend";
      legend.innerHTML =
        '<span class="vocab-check-legend__item">' +
        CHECK_ON +
        " Selected</span>" +
        '<span class="vocab-check-legend__item">' +
        CHECK_OFF +
        " Not selected</span>" +
        '<span class="vocab-check-legend__item">' +
        CHECK_MASTERED +
        " Mastered</span>";

      var gridWrap = document.createElement("div");
      var grid = document.createElement("div");
      grid.className = "vocab-check-grid";
      gridWrap.appendChild(grid);

      var expandBtn = null;
      var opened = !!state.expandedWords[lvl];
      var query = (state.searchQuery[lvl] || "").trim().toLowerCase();

      function filteredWords() {
        if (!query) return words;
        return words.filter(function (w) {
          return (w.text || "").toLowerCase().indexOf(query) >= 0;
        });
      }

      function renderGrid() {
        grid.innerHTML = "";
        var list = filteredWords();
        if (!list.length) {
          grid.innerHTML = '<p class="vocab-check-empty">No words match your search.</p>';
          if (expandBtn) expandBtn.hidden = true;
          return;
        }
        var showAll = opened || list.length <= VISIBLE_DEFAULT;
        list.forEach(function (w, idx) {
          var row = document.createElement("button");
          row.type = "button";
          var isSel = !!state.selectedWordIds[lvl][String(w.id)];
          row.className =
            "vocab-check-row" +
            (w.mastered ? " is-mastered" : "") +
            (isSel && !w.mastered ? " is-selected" : "");
          if (!showAll && idx >= VISIBLE_DEFAULT) row.classList.add("is-hidden");
          row.dataset.wordId = String(w.id);
          row.dataset.mastered = w.mastered ? "1" : "0";
          row.innerHTML =
            '<span class="vocab-check-row__icon">' +
            rowIcon(w.mastered, isSel) +
            "</span>" +
            '<span class="vocab-check-row__text">' +
            escapeHtml(w.text) +
            (w.part_of_speech
              ? '<span class="vocab-check-row__pos">' +
                escapeHtml(posShortLabel(w.part_of_speech)) +
                "</span>"
              : "") +
            "</span>";
          if (!w.mastered) {
            row.addEventListener("click", function () {
              var id = row.dataset.wordId;
              state.selectedWordIds[lvl][id] = !state.selectedWordIds[lvl][id];
              renderGrid();
              updateStart();
            });
          }
          grid.appendChild(row);
        });

        if (expandBtn) {
          if (list.length > VISIBLE_DEFAULT) {
            expandBtn.hidden = false;
            expandBtn.textContent = opened
              ? "Show fewer words"
              : "Show all " + list.length + " words";
          } else {
            expandBtn.hidden = true;
          }
        }
      }

      if (words.length > VISIBLE_DEFAULT) {
        expandBtn = document.createElement("button");
        expandBtn.type = "button";
        expandBtn.className = "vocab-check-expand";
        expandBtn.addEventListener("click", function () {
          opened = !opened;
          state.expandedWords[lvl] = opened;
          renderGrid();
        });
        gridWrap.appendChild(expandBtn);
      }

      var sessBlock = document.createElement("div");
      sessBlock.className = "vocab-sess-size";
      var sliderMax = steps[steps.length - 1];
      var sliderVal = state.sessionSize[lvl];
      sessBlock.innerHTML =
        '<p class="vocab-sess-size__label">Session size</p>' +
        '<div class="vocab-sess-size__row">' +
        '<span class="vocab-sess-size__num" id="sess-num-' +
        lvl +
        '">' +
        sliderVal +
        "</span>" +
        '<input type="range" class="vocab-sess-size__slider" id="sess-slider-' +
        lvl +
        '" min="0" max="' +
        (steps.length - 1) +
        '" step="1" value="' +
        steps.indexOf(sliderVal) +
        '" aria-label="Session size">' +
        "</div>";

      var startBtn = document.createElement("a");
      startBtn.className = "vocab-start-btn";
      startBtn.id = "sess-start-" + lvl;

      function updateStart() {
        var selectedIds = selectedIdsForLevel(lvl);
        var n = state.sessionSize[lvl];
        var sessionN = Math.min(n, selectedIds.length || n);
        startBtn.textContent = "Start session — " + sessionN + " cards →";
        startBtn.href = buildFlashcardUrl(lvl, sessionN, selectedIds);
        var disabled = selectedIds.length === 0;
        startBtn.classList.toggle("is-disabled", disabled);
        startBtn.setAttribute("aria-disabled", disabled ? "true" : "false");
        if (disabled) startBtn.removeAttribute("href");
      }

      renderGrid();
      updateStart();

      var searchInput = controls.querySelector(".vocab-check-search");
      searchInput.addEventListener("input", function () {
        state.searchQuery[lvl] = searchInput.value;
        renderGrid();
      });

      controls.addEventListener("click", function (e) {
        var btn = e.target.closest("[data-action]");
        if (!btn || !controls.contains(btn)) return;
        var action = btn.dataset.action;
        if (action === "all") {
          words.forEach(function (w) {
            if (!w.mastered) state.selectedWordIds[lvl][String(w.id)] = true;
          });
        } else if (action === "clear") {
          words.forEach(function (w) {
            if (!w.mastered) state.selectedWordIds[lvl][String(w.id)] = false;
          });
        }
        renderGrid();
        updateStart();
      });

      var slider = sessBlock.querySelector(".vocab-sess-size__slider");
      var numEl = sessBlock.querySelector(".vocab-sess-size__num");
      slider.addEventListener("input", function () {
        var idx = parseInt(slider.value, 10);
        var val = steps[idx] || steps[0];
        state.sessionSize[lvl] = val;
        numEl.textContent = String(val);
        updateStart();
      });

      card.appendChild(head);
      card.appendChild(progWrap);
      card.appendChild(controls);
      card.appendChild(legend);
      card.appendChild(gridWrap);
      card.appendChild(sessBlock);
      card.appendChild(startBtn);
      elLevels.appendChild(card);
    });
  }

  function renderOverall() {
    if (!state.data) return;
    var t = state.data.total_words || 0;
    var m = state.data.mastered_total || 0;
    var p = state.data.overall_pct || 0;
    elOverall.hidden = false;
    elOverallLabel.textContent = "Overall progress — " + m + " of " + t + " words mastered";
    elOverallFill.style.width = p + "%";
    elOverallFill.style.background = GREEN;
    elOverallPct.textContent = p + "%";
    elMeta.textContent = t + " words · 3 levels · start anywhere";
  }

  async function fetchJson(url) {
    var res = await fetch(url, { credentials: "same-origin" });
    try {
      return await res.json();
    } catch (e) {
      return { ok: false, status: "error", message: "Could not load words — tap to retry" };
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
        if (elErrorMsg) elErrorMsg.textContent = data.message || "Could not load words — tap to retry";
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
        if (elErrorMsg) elErrorMsg.textContent = data.message || "Could not load words — tap to retry";
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
