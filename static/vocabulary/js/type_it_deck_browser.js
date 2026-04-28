(function () {
  "use strict";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  var topicsEl = document.getElementById("ti-type-it-topics-data");
  var viewTopics = document.getElementById("tidb-view-topics");
  var viewLevels = document.getElementById("tidb-view-levels");
  var levelHead = document.getElementById("tidb-level-head");
  var levelCards = document.getElementById("tidb-level-cards");
  var backBtn = document.getElementById("tidb-back-topics");

  var topicsData = [];
  if (topicsEl) {
    try {
      topicsData = JSON.parse(topicsEl.textContent) || [];
    } catch (e) {
      topicsData = [];
    }
  }

  function findTopic(key) {
    for (var i = 0; i < topicsData.length; i++) {
      if (topicsData[i].topic === key) return topicsData[i];
    }
    return null;
  }

  function renderLevelView(topicKey) {
    var t = findTopic(topicKey);
    if (!t || !levelHead || !levelCards) return;
    levelHead.innerHTML =
      '<div class="tidb-level-head-inner">' +
      '<span class="tidb-level-emoji" aria-hidden="true">' +
      escapeHtml(t.emoji || "") +
      "</span><div><h2 class=\"tidb-level-topic-name\">" +
      escapeHtml(t.name || "") +
      '</h2><p class="tidb-level-sub">Choose a difficulty level</p></div></div>';

    levelCards.innerHTML = (t.levels || [])
      .map(function (L) {
        var pct = Math.max(0, Math.min(100, Number(L.pct) || 0));
        return (
          '<div class="tidb-level-card">' +
          '<div class="tidb-level-icon" aria-hidden="true">' +
          escapeHtml(L.icon_emoji || "") +
          "</div>" +
          '<div class="tidb-level-main">' +
          '<div class="tidb-level-title-row">' +
          '<span class="tidb-level-tier">' +
          escapeHtml(L.tier_title || "") +
          "</span>" +
          '<span class="tidb-badge tidb-badge--' +
          escapeHtml(L.badge || "") +
          '">' +
          escapeHtml(L.ielts || "") +
          " · " +
          escapeHtml(String(L.count)) +
          " words</span></div>" +
          '<p class="tidb-level-desc">' +
          escapeHtml(L.desc || "") +
          "</p>" +
          '<div class="tidb-level-progress-row">' +
          '<div class="tidb-bar" role="progressbar"><div class="tidb-bar-fill" style="width:' +
          pct +
          '%"></div></div>' +
          '<span class="tidb-level-count">' +
          escapeHtml(String(L.done)) +
          " / " +
          escapeHtml(String(L.count)) +
          " done</span></div></div>" +
          '<div class="tidb-level-actions">' +
          '<a class="tidb-start-btn" href="' +
          String(L.words_url || "#").replace(/"/g, "") +
          '">Start →</a></div></div>'
        );
      })
      .join("");
  }

  function showTopics() {
    if (viewTopics) viewTopics.classList.remove("tidb-hidden");
    if (viewLevels) {
      viewLevels.classList.add("tidb-hidden");
      viewLevels.setAttribute("aria-hidden", "true");
    }
    window.scrollTo(0, 0);
  }

  function showLevels(topicKey) {
    renderLevelView(topicKey);
    if (viewTopics) viewTopics.classList.add("tidb-hidden");
    if (viewLevels) {
      viewLevels.classList.remove("tidb-hidden");
      viewLevels.setAttribute("aria-hidden", "false");
    }
    window.scrollTo(0, 0);
  }

  if (viewTopics && viewLevels) {
    viewTopics.addEventListener("click", function (e) {
      var btn = e.target.closest(".tidb-topic-card");
      if (!btn || !viewTopics.contains(btn)) return;
      var topic = btn.getAttribute("data-topic");
      if (!topic) return;
      showLevels(topic);
    });
    if (backBtn) {
      backBtn.addEventListener("click", showTopics);
    }
  }

  /* —— Create deck modal —— */
  var modal = document.getElementById("ti-create-modal");
  var openBtn = document.getElementById("ti-open-create");
  if (modal && openBtn) {
  var colours = [
    { id: "navy", hex: "#0d2140" },
    { id: "green", hex: "#3B6D11" },
    { id: "amber", hex: "#d97706" },
    { id: "purple", hex: "#6d28d9" },
    { id: "red", hex: "#b91c1c" },
    { id: "teal", hex: "#0f766e" },
  ];
  var emojis = ["📖", "🎯", "💡", "✏️", "🔑", "🧠", "⭐", "🔥"];
  var colourSel = "navy";
  var emojiSel = "📖";

  function csrfFromCookie() {
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function closeModal() {
    modal.classList.add("ti-modal--hidden");
  }
  function openModal() {
    modal.classList.remove("ti-modal--hidden");
  }

  function renderPicks() {
    var c = document.getElementById("ti-colours");
    var e = document.getElementById("ti-emojis");
    if (c) {
      c.innerHTML = colours
        .map(function (x) {
          return (
            '<button type="button" class="ti-dot ' +
            (x.id === colourSel ? "ti-dot--on" : "") +
            '" data-colour="' +
            x.id +
            '" style="background:' +
            x.hex +
            '"></button>'
          );
        })
        .join("");
      c.querySelectorAll("[data-colour]").forEach(function (b) {
        b.addEventListener("click", function () {
          colourSel = b.getAttribute("data-colour") || "navy";
          renderPicks();
        });
      });
    }
    if (e) {
      e.innerHTML = emojis
        .map(function (x) {
          return (
            '<button type="button" class="ti-emoji-btn ' +
            (x === emojiSel ? "ti-emoji-btn--on" : "") +
            '" data-emoji="' +
            x +
            '">' +
            x +
            "</button>"
          );
        })
        .join("");
      e.querySelectorAll("[data-emoji]").forEach(function (b) {
        b.addEventListener("click", function () {
          emojiSel = b.getAttribute("data-emoji") || "📖";
          renderPicks();
        });
      });
    }
  }

  openBtn.addEventListener("click", openModal);
  document.getElementById("ti-create-cancel").addEventListener("click", closeModal);
  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeModal();
  });

  document.getElementById("ti-create-save").addEventListener("click", function () {
    var err = document.getElementById("ti-create-err");
    var name = (document.getElementById("ti-create-name").value || "").trim();
    var words = (document.getElementById("ti-create-words").value || "").trim();
    if (!name || !words) {
      err.textContent = "Deck name and words are required.";
      err.classList.remove("ti-hidden");
      return;
    }
    err.classList.add("ti-hidden");
    fetch(window.TI_DECK_CREATE.createUrl, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfFromCookie(),
      },
      body: JSON.stringify({ name: name, colour: colourSel, emoji: emojiSel, words: words }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (!data.ok) {
          err.textContent = "Could not create deck.";
          err.classList.remove("ti-hidden");
          return;
        }
        window.location.href = data.words_url;
      })
      .catch(function () {
        err.textContent = "Could not create deck.";
        err.classList.remove("ti-hidden");
      });
  });

  renderPicks();
  }
})();
