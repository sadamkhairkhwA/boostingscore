/**
 * Client-side flashcard session: queue, 3D flip, spaced repetition ratings, APIs, gestures, keyboard.
 */
(function () {
  "use strict";

  var cfg = window.FC_SESSION || {};
  var deckEl = document.getElementById("fc-deck-data");
  var masteryEl = document.getElementById("fc-mastery-data");
  if (deckEl) {
    try {
      cfg.deck = JSON.parse(deckEl.textContent);
    } catch (e) {
      return;
    }
  }
  if (masteryEl) {
    try {
      cfg.masteryLabels = JSON.parse(masteryEl.textContent);
    } catch (e) {
      cfg.masteryLabels = {};
    }
  }
  if (!cfg.deck || !cfg.deck.length) return;

  var shell = document.getElementById("fc-shell");
  var cardEl = document.getElementById("fcard");
  var flipBtn = document.getElementById("fc-flip-btn");
  var expandBtn = document.getElementById("fc-expand");
  var shuffleBtn = document.getElementById("fc-shuffle");
  var saveBtn = document.getElementById("fc-save");
  var barFill = document.getElementById("fc-bar-fill");
  var metaN = document.getElementById("fc-meta-n");
  var metaPct = document.getElementById("fc-meta-pct");
  var celebration = document.getElementById("fc-celebration");
  var confettiCanvas = document.getElementById("fc-confetti-canvas");
  var celeAcc = document.getElementById("fc-cele-acc");
  var celeList = document.getElementById("fc-cele-review-list");
  var studyAgain = document.getElementById("fc-study-again");

  var statEasy = document.getElementById("stat-easy");
  var statGood = document.getElementById("stat-good");
  var statHard = document.getElementById("stat-hard");
  var statRev = document.getElementById("stat-reviewed");

  var RATE_URL = cfg.rateUrl;
  var SAVE_PENDING_URL = cfg.savePendingUrl;
  var STAT_KEY = cfg.statKey;
  var MASTERY_LABELS = cfg.masteryLabels || {
    1: "New",
    2: "Recognizing",
    3: "Learning",
    4: "Confident",
    5: "Mastered",
  };
  var LS_KEY = "fc_sess_v5_" + STAT_KEY;

  var deck = cfg.deck.slice();
  var initialTotal = deck.length;
  var queue = [];
  var pendingHard = [];
  var easyCount = 0;
  var goodCount = 0;
  var hardPressCount = 0;
  var wordsMarkedHard = {};

  function getCsrf() {
    var el = document.querySelector("[name=csrfmiddlewaretoken]");
    return el ? el.value : "";
  }

  function savedLabel(ok) {
    var ic = typeof BSIcons !== "undefined" ? BSIcons.check() : "";
    return ok ? ic + " Saved" : "Save failed — retry";
  }
  function saveProgressLabel() {
    return (typeof BSIcons !== "undefined" ? BSIcons.check() : "") + " Save progress";
  }

  function cardKey(c) {
    if (c.id) return "w" + c.id;
    if (c.card_id) return "c" + c.card_id;
    return "h" + (c.word || "").slice(0, 40);
  }

  function saveState() {
    try {
      localStorage.setItem(
        LS_KEY,
        JSON.stringify({
          v: 5,
          statKey: STAT_KEY,
          initialTotal: initialTotal,
          queue: queue,
          pendingHard: pendingHard,
          easyCount: easyCount,
          goodCount: goodCount,
          hardPressCount: hardPressCount,
          wordsMarkedHard: wordsMarkedHard,
        })
      );
    } catch (e) {}
  }

  function loadState() {
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (!raw) return false;
      var s = JSON.parse(raw);
      if (s.statKey !== STAT_KEY || s.initialTotal !== initialTotal) return false;
      if (!Array.isArray(s.queue) || s.queue.length === 0) return false;
      var validKeys = {};
      deck.forEach(function (c) {
        validKeys[cardKey(c)] = true;
      });
      var ok = s.queue.every(function (c) {
        return validKeys[cardKey(c)];
      });
      if (!ok) return false;
      queue = s.queue;
      pendingHard = s.pendingHard || [];
      easyCount = s.easyCount || 0;
      goodCount = s.goodCount || 0;
      hardPressCount = s.hardPressCount || 0;
      wordsMarkedHard = s.wordsMarkedHard || {};
      return true;
    } catch (e) {
      return false;
    }
  }

  function initQueue() {
    if (loadState()) return;
    queue = deck.slice();
    if (cfg.initialShuffle) {
      shuffleArray(queue);
    }
    pendingHard = [];
    easyCount = 0;
    goodCount = 0;
    hardPressCount = 0;
    wordsMarkedHard = {};
    saveState();
  }

  function shuffleArray(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i];
      arr[i] = arr[j];
      arr[j] = t;
    }
  }

  function currentCard() {
    return queue[0];
  }

  function setShellFlipped(on) {
    if (shell) shell.classList.toggle("bs-fc-session--flipped", !!on);
  }

  function flip() {
    if (!cardEl) return;
    cardEl.classList.toggle("is-flipped");
    setShellFlipped(cardEl.classList.contains("is-flipped"));
  }

  function renderCard() {
    var c = currentCard();
    if (!c) return;

    var wEl = document.getElementById("fc-word");
    var phonEl = document.getElementById("fc-phon");
    var defEl = document.getElementById("fc-def");
    var exEl = document.getElementById("fc-ex");
    var posEl = document.getElementById("fc-tag-pos");
    var lvlEl = document.getElementById("fc-tag-lvl");
    var topEl = document.getElementById("fc-tag-topic");
    var stageEl = document.getElementById("fc-stage");
    var dots = document.querySelectorAll("#fcard .bs-fc-dot");

    if (wEl) wEl.textContent = c.word || "";
    if (defEl) defEl.textContent = c.definition || "";
    if (exEl) exEl.textContent = c.example_sentence || "";
    if (phonEl) {
      var ph = (c.phonetic || "").trim();
      phonEl.textContent = ph || "Add phonetic in word bank";
      phonEl.style.opacity = ph ? "1" : "0.45";
    }
    if (posEl) posEl.textContent = c.part_of_speech || "word";
    if (lvlEl) lvlEl.textContent = "Level " + c.level + " · " + (c.level_label || "");
    if (topEl) topEl.textContent = c.topic_label || c.topic || "";
    var ml = parseInt(c.mastery_level, 10) || 1;
    if (stageEl) {
      stageEl.textContent =
        "Level " + ml + " — " + (MASTERY_LABELS[ml] || MASTERY_LABELS[String(ml)] || "Learning");
    }
    for (var i = 0; i < dots.length; i++) {
      dots[i].classList.toggle("on", i < ml);
    }

    if (cardEl) {
      cardEl.classList.remove("is-flipped");
      setShellFlipped(false);
    }
  }

  function updateProgressUI() {
    var doneCount = easyCount + goodCount;
    var pct = initialTotal ? Math.round((doneCount / initialTotal) * 100) : 0;
    if (barFill) {
      barFill.style.width = pct + "%";
    }
    if (metaN) {
      metaN.textContent =
        "Progress " + doneCount + " / " + initialTotal + " · " + queue.length + " left";
    }
    if (metaPct) metaPct.textContent = pct + "%";
    if (statEasy) statEasy.textContent = String(easyCount);
    if (statGood) statGood.textContent = String(goodCount);
    if (statHard) statHard.textContent = String(hardPressCount);
    if (statRev) statRev.textContent = String(doneCount + hardPressCount);
  }

  function postRating(rating, c, done) {
    var body = {
      rating: rating,
      word_id: c.id || null,
      card_id: c.card_id || null,
    };
    fetch(RATE_URL, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrf(),
      },
      body: JSON.stringify(body),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (done) done(!!data.ok);
      })
      .catch(function () {
        if (done) done(false);
      });
  }

  function postPendingHard(done) {
    if (!pendingHard.length) {
      if (done) done(true);
      return;
    }
    fetch(SAVE_PENDING_URL, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrf(),
      },
      body: JSON.stringify({ items: pendingHard.slice() }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.ok) pendingHard = [];
        saveState();
        if (done) done(!!data.ok);
      })
      .catch(function () {
        if (done) done(false);
      });
  }

  function queuePendingHard(c) {
    pendingHard.push({
      word_id: c.id || null,
      card_id: c.card_id || null,
    });
  }

  function trackHardCard(c) {
    var k = cardKey(c);
    wordsMarkedHard[k] = (c.word || k).toString();
  }

  function markHard() {
    var c = currentCard();
    if (!c || !cardEl.classList.contains("is-flipped")) return;
    queue.shift();
    queue.push(c);
    trackHardCard(c);
    hardPressCount++;
    saveState();
    updateProgressUI();
    renderCard();
    postRating("hard", c, function (ok) {
      if (ok) return;
      queuePendingHard(c);
      saveState();
    });
  }

  function markEasy() {
    var c = currentCard();
    if (!c || !cardEl.classList.contains("is-flipped")) return;
    queue.shift();
    easyCount++;
    postRating("easy", c, function (ok) {
      if (!ok) {
        queue.unshift(c);
        easyCount--;
        saveState();
        updateProgressUI();
        renderCard();
        return;
      }
      saveState();
      updateProgressUI();
      if (queue.length) renderCard();
      else finishSession();
    });
  }

  function markGood() {
    var c = currentCard();
    if (!c || !cardEl.classList.contains("is-flipped")) return;
    queue.shift();
    goodCount++;
    postRating("good", c, function (ok) {
      if (!ok) {
        queue.unshift(c);
        goodCount--;
        saveState();
        updateProgressUI();
        renderCard();
        return;
      }
      saveState();
      updateProgressUI();
      if (queue.length) renderCard();
      else finishSession();
    });
  }

  function skipNext() {
    var c = currentCard();
    if (!c) return;
    queue.shift();
    queue.push(c);
    saveState();
    updateProgressUI();
    setShellFlipped(false);
    if (cardEl) cardEl.classList.remove("is-flipped");
    renderCard();
  }

  function finishSession() {
    saveState();
    updateProgressUI();
    if (celeAcc) {
      var doneCount = easyCount + goodCount;
      var tot = doneCount + hardPressCount;
      celeAcc.textContent =
        "Completed " +
        doneCount +
        " of " +
        initialTotal +
        " · " +
        easyCount +
        " easy · " +
        goodCount +
        " good · " +
        hardPressCount +
        " hard";
    }
    if (celeList) {
      celeList.innerHTML = "";
      var words = [];
      for (var k in wordsMarkedHard) {
        if (wordsMarkedHard.hasOwnProperty(k)) words.push(wordsMarkedHard[k]);
      }
      words.sort();
      words.forEach(function (w) {
        var li = document.createElement("li");
        li.textContent = w;
        celeList.appendChild(li);
      });
      if (!words.length) {
        var li0 = document.createElement("li");
        li0.className = "bs-fc-cele-review-none";
        li0.textContent = "No words added to Hard words — perfect run.";
        celeList.appendChild(li0);
      }
    }
    if (celebration) {
      celebration.hidden = false;
      document.body.classList.add("bs-fc-celebration-on");
      runConfetti();
    }
  }

  function runConfetti() {
    if (!confettiCanvas) return;
    var ctx = confettiCanvas.getContext("2d");
    var W = window.innerWidth;
    var H = window.innerHeight;
    var dpr = window.devicePixelRatio || 1;
    confettiCanvas.width = W * dpr;
    confettiCanvas.height = H * dpr;
    confettiCanvas.style.width = W + "px";
    confettiCanvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var pieces = [];
    var colors = ["#3B6D11", "#1E3A5F", "#C94C4C", "#F59E0B", "#8B5CF6", "#EC4899"];
    for (var i = 0; i < 120; i++) {
      pieces.push({
        x: Math.random() * W,
        y: Math.random() * -H,
        r: 4 + Math.random() * 6,
        vy: 2 + Math.random() * 4,
        vx: -2 + Math.random() * 4,
        rot: Math.random() * Math.PI,
        vr: -0.1 + Math.random() * 0.2,
        c: colors[Math.floor(Math.random() * colors.length)],
      });
    }
    var t0 = Date.now();
    function frame() {
      var elapsed = Date.now() - t0;
      ctx.clearRect(0, 0, W, H);
      pieces.forEach(function (p) {
        p.y += p.vy;
        p.x += p.vx;
        p.rot += p.vr;
        p.vy += 0.05;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.c;
        ctx.fillRect(-p.r, -p.r, p.r * 2, p.r * 2);
        ctx.restore();
      });
      if (elapsed < 4500) requestAnimationFrame(frame);
    }
    frame();
  }

  function onShuffle() {
    if (!queue.length) return;
    shuffleArray(queue);
    if (cardEl) cardEl.classList.remove("is-flipped");
    setShellFlipped(false);
    saveState();
    renderCard();
    updateProgressUI();
  }

  function onSaveProgress(ev) {
    if (ev) ev.preventDefault();
    postPendingHard(function (ok) {
      if (saveBtn) {
        saveBtn.innerHTML = savedLabel(ok);
        window.setTimeout(function () {
          saveBtn.innerHTML = saveProgressLabel();
        }, 2000);
      }
    });
  }

  var touchStartX = null;
  function onTouchStart(e) {
    if (e.touches.length !== 1) return;
    touchStartX = e.touches[0].clientX;
  }
  function onTouchEnd(e) {
    if (touchStartX === null || !e.changedTouches.length) return;
    var dx = e.changedTouches[0].clientX - touchStartX;
    touchStartX = null;
    if (Math.abs(dx) < 70) return;
    if (!cardEl.classList.contains("is-flipped")) return;
    if (dx < 0) markHard();
    else markEasy();
  }

  function onKeyDown(e) {
    var tag = (e.target && e.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
    if (e.code === "Space") {
      e.preventDefault();
      flip();
      return;
    }
    if (e.key === "Enter") {
      e.preventDefault();
      skipNext();
      return;
    }
    if (e.code === "ArrowLeft") {
      e.preventDefault();
      if (cardEl.classList.contains("is-flipped")) markHard();
      return;
    }
    if (e.code === "ArrowDown") {
      e.preventDefault();
      if (cardEl.classList.contains("is-flipped")) markGood();
      return;
    }
    if (e.code === "ArrowRight") {
      e.preventDefault();
      if (cardEl.classList.contains("is-flipped")) markEasy();
      return;
    }
  }

  initQueue();
  renderCard();
  updateProgressUI();

  if (cardEl) {
    cardEl.addEventListener("click", function (e) {
      if (e.target.closest("button")) return;
      flip();
    });
  }
  if (flipBtn)
    flipBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      flip();
    });
  if (expandBtn)
    expandBtn.addEventListener("click", function () {
      if (shell) shell.classList.toggle("bs-fc-expanded");
    });
  if (shuffleBtn)
    shuffleBtn.addEventListener("click", function (e) {
      e.preventDefault();
      onShuffle();
    });
  if (saveBtn) saveBtn.addEventListener("click", onSaveProgress);

  document.getElementById("fc-btn-hard").addEventListener("click", function (e) {
    e.preventDefault();
    markHard();
  });
  document.getElementById("fc-btn-good").addEventListener("click", function (e) {
    e.preventDefault();
    markGood();
  });
  document.getElementById("fc-btn-easy").addEventListener("click", function (e) {
    e.preventDefault();
    markEasy();
  });

  document.addEventListener("keydown", onKeyDown);

  if (shell) {
    shell.addEventListener("touchstart", onTouchStart, { passive: true });
    shell.addEventListener("touchend", onTouchEnd, { passive: true });
  }

  if (studyAgain) {
    studyAgain.addEventListener("click", function () {
      try {
        localStorage.removeItem(LS_KEY);
      } catch (e) {}
    });
  }
})();
