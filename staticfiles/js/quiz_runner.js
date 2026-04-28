/**
 * Quiz runner — per-method UI (quiz_methods.css)
 */
(function () {
  var STORAGE_KEY = "quizSetupV1";

  function clearQuizSetupStorage() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
  }

  function speakEnglish(text, rate) {
    try {
      if (!window.speechSynthesis || !text) return;
      var u = new SpeechSynthesisUtterance(String(text));
      u.lang = "en-GB";
      if (typeof rate === "number") u.rate = rate;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    } catch (e) {}
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function escAttr(s) {
    return escHtml(s).replace(/"/g, "&quot;");
  }

  function shuffle(a) {
    var arr = a.slice();
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i];
      arr[i] = arr[j];
      arr[j] = t;
    }
    return arr;
  }

  var cfg = window.__QUIZ_INIT__;
  var root = document.getElementById("quiz-runner-root");
  var doneEl = document.getElementById("quiz-runner-done");
  if (!root || !cfg) return;

  var deckWords = cfg.deck || [];
  var quizMethod = cfg.quizMethod || "mc";
  if (!deckWords.length) {
    root.innerHTML = "<p>No words to quiz. <a href=\"" + escAttr(cfg.setupUrl || "/vocabulary/quiz/setup/") + "\">Back to setup</a></p>";
    return;
  }
  if (deckWords.length < 3) {
    root.innerHTML = "<p>Need at least three words. <a href=\"" + escAttr(cfg.setupUrl || "/vocabulary/quiz/setup/") + "\">Back to setup</a></p>";
    return;
  }

  var order = shuffle(
    deckWords.map(function (_, i) {
      return i;
    })
  );
  var qIndex = 0;

  function buildWordChoices(correctIdx) {
    var correct = deckWords[correctIdx];
    var pool = deckWords
      .map(function (_, i) {
        return i;
      })
      .filter(function (i) {
        return i !== correctIdx;
      });
    var picks = shuffle(pool).slice(0, 3);
    var opts = shuffle(
      picks.concat([correctIdx]).map(function (i) {
        return deckWords[i].word;
      })
    );
    return { def: correct.definition || "—", correctWord: correct.word, options: opts };
  }

  function buildDefChoices(correctIdx) {
    var correct = deckWords[correctIdx];
    var pool = deckWords
      .map(function (_, i) {
        return i;
      })
      .filter(function (i) {
        return i !== correctIdx;
      });
    var picks = shuffle(pool).slice(0, 3);
    var defs = shuffle(
      picks.concat([correctIdx]).map(function (i) {
        return deckWords[i].definition || "—";
      })
    );
    return { word: correct.word, correctDef: correct.definition || "—", options: defs };
  }

  function modeLabel(m) {
    if (m === "truefalse") return "True / false";
    if (m === "fillblank") return "Fill in the blank";
    if (m === "match") return "Match the pairs";
    if (m === "type") return "Spell it";
    if (m === "listen") return "Listen & answer";
    return "Multiple choice";
  }

  function shell(cardClass, inner, metaText) {
    return (
      '<div class="QQ-shell">' +
      '<div class="QQ-card ' +
      cardClass +
      '">' +
      inner +
      "</div>" +
      '<div class="QQ-bar">' +
      '<span class="QQ-meta">' +
      escHtml(metaText) +
      "</span>" +
      '<button type="button" class="QQ-next" id="quiz-next" disabled>Next question →</button>' +
      "</div>" +
      "</div>"
    );
  }

  function enableNext() {
    var b = document.getElementById("quiz-next");
    if (b) b.disabled = false;
  }

  function advance() {
    qIndex += 1;
    if (qIndex >= order.length) {
      showComplete();
      return;
    }
    paintQ();
  }

  function showComplete() {
    clearQuizSetupStorage();
    root.innerHTML = "";
    if (doneEl) doneEl.hidden = false;
  }

  function bindNext() {
    var b = document.getElementById("quiz-next");
    if (b)
      b.addEventListener("click", function () {
        if (b.disabled) return;
        advance();
      });
  }

  function metaLine() {
    return "Question " + (qIndex + 1) + " of " + order.length + " · " + modeLabel(quizMethod);
  }

  function pickTriple(correctIdx) {
    var pool = deckWords
      .map(function (_, i) {
        return i;
      })
      .filter(function (i) {
        return i !== correctIdx;
      });
    var need = Math.min(2, pool.length);
    var others = shuffle(pool).slice(0, need);
    return shuffle([correctIdx].concat(others));
  }

  function paintQ() {
    var idx = order[qIndex];
    var card = deckWords[idx];
    var mode = quizMethod;
    if (mode === "syn") mode = "mc";

    if (mode === "fillblank") {
      paintFillBlank(idx, card);
      return;
    }
    if (mode === "mc") {
      paintMultipleChoice(idx, card);
      return;
    }
    if (mode === "truefalse") {
      paintTrueFalse(idx, card);
      return;
    }
    if (mode === "match") {
      paintMatch(idx, card);
      return;
    }
    if (mode === "type") {
      paintSpell(idx, card);
      return;
    }
    if (mode === "listen") {
      paintListen(idx, card);
      return;
    }

    root.innerHTML =
      "<p>Unknown quiz mode. <a href=\"" + escAttr(cfg.setupUrl || "/vocabulary/quiz/setup/") + '">Back to setup</a></p>';
  }

  function paintMultipleChoice(idx, card) {
    var dc = buildDefChoices(idx);
    var word = card.word || "";
    var correctDef = String(dc.correctDef || "").trim();
    var options = dc.options;
    var optsHtml = "";
    options.forEach(function (defText) {
      var dt = String(defText || "").trim();
      optsHtml +=
        '<button type="button" class="qqmc-opt" data-def="' +
        escAttr(dt) +
        '">' +
        escHtml(dt.length > 220 ? dt.slice(0, 220) + "…" : dt) +
        "</button>";
    });
    var inner =
      '<p class="qqmc-word">' +
      escHtml(word) +
      '</p><p class="qqmc-sub">Pick the correct meaning</p><div class="qqmc-options">' +
      optsHtml +
      "</div>";
    root.innerHTML = shell("QQ-card--mc", inner, metaLine());
    bindNext();
    root.querySelectorAll(".qqmc-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var picked = String(btn.getAttribute("data-def") || "").trim();
        var ok = picked === correctDef;
        root.querySelectorAll(".qqmc-opt").forEach(function (b) {
          b.disabled = true;
          var d = String(b.getAttribute("data-def") || "").trim();
          if (d === correctDef) b.classList.add("is-reveal-correct");
          else if (b === btn) b.classList.add("is-reveal-wrong");
        });
        enableNext();
      });
    });
  }

  function paintFillBlank(idx, card) {
    var ex = ((card.example || "") + "").trim();
    var wtxt = ((card.word || "") + "").trim();
    var sentenceHtml = "";
    if (ex && wtxt && ex.toLowerCase().indexOf(wtxt.toLowerCase()) >= 0) {
      var re = new RegExp(wtxt.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
      var m = ex.match(re);
      if (m && m.index != null) {
        var before = escHtml(ex.slice(0, m.index));
        var after = escHtml(ex.slice(m.index + m[0].length));
        sentenceHtml =
          '<div class="qqfb-sentence">' + before + '<span class="qqfb-gap"></span>' + after + "</div>";
      } else {
        sentenceHtml = '<div class="qqfb-sentence">' + escHtml(ex) + "</div>";
      }
    } else {
      var def = (card.definition || "—").slice(0, 160);
      sentenceHtml = '<div class="qqfb-sentence">' + escHtml(def) + ' <span class="qqfb-gap"></span></div>';
    }
    var inner =
      sentenceHtml +
      '<div class="qqfb-row">' +
      '<input type="text" class="qqfb-input" id="qqfb-in" placeholder="Type the missing word..." autocomplete="off" />' +
      '<button type="button" class="qqfb-check" id="qqfb-check">Check</button>' +
      '</div><p class="qqfb-feedback" id="qqfb-fb"></p>';
    root.innerHTML = shell("QQ-card--fb", inner, metaLine());
    bindNext();
    var inp = document.getElementById("qqfb-in");
    var fb = document.getElementById("qqfb-fb");
    setTimeout(function () {
      if (inp) inp.focus();
    }, 50);
    document.getElementById("qqfb-check").addEventListener("click", function () {
      var ok = (inp.value || "").trim().toLowerCase() === wtxt.toLowerCase();
      fb.textContent = ok ? "✓ Correct!" : "✗ The correct answer is: " + wtxt;
      fb.className = "qqfb-feedback " + (ok ? "is-ok" : "is-bad");
      enableNext();
    });
  }

  function paintTrueFalse(idx, card) {
    var really = Math.random() < 0.5;
    var correctBtn = "true";
    var statement = "";
    if (really) {
      statement =
        "“" + escHtml(card.word || "") + "” means: " + escHtml((card.definition || "—").trim()) + ".";
      correctBtn = "true";
    } else {
      var pool = deckWords
        .map(function (_, i) {
          return i;
        })
        .filter(function (i) {
          return i !== idx;
        });
      var oi = pool[Math.floor(Math.random() * pool.length)] || 0;
      var wrongDef = deckWords[oi].definition || "—";
      statement =
        "“" + escHtml(card.word || "") + "” means: " + escHtml((wrongDef || "—").trim()) + ".";
      correctBtn = "false";
    }
    var inner =
      '<div class="qqtf-statement">' +
      statement +
      '</div><div class="qqtf-row">' +
      '<button type="button" class="qqtf-btn qqtf-btn--true" data-tf="true">✓ True</button>' +
      '<button type="button" class="qqtf-btn qqtf-btn--false" data-tf="false">✗ False</button>' +
      "</div>";
    root.innerHTML = shell("QQ-card--tf", inner, metaLine());
    bindNext();
    root.querySelectorAll(".qqtf-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-tf");
        var ok = v === correctBtn;
        root.querySelectorAll(".qqtf-btn").forEach(function (x) {
          x.disabled = true;
          if (x === b) x.classList.add("is-picked");
          else x.classList.add("is-dim");
        });
        enableNext();
      });
    });
  }

  function paintMatch(idx, card) {
    var triple = pickTriple(idx);
    var pairColors = ["c0", "c1", "c2"];
    var wordSide = shuffle(
      triple.map(function (ti) {
        return { pair: ti, text: deckWords[ti].word };
      })
    );
    var defSide = shuffle(
      triple.map(function (ti) {
        return { pair: ti, text: deckWords[ti].definition || "—" };
      })
    );
    var wHtml = "";
    wordSide.forEach(function (w) {
      wHtml +=
        '<button type="button" class="qqmp-chip" data-pair="' +
        w.pair +
        '">' +
        escHtml(w.text) +
        "</button>";
    });
    var dHtml = "";
    defSide.forEach(function (d) {
      dHtml +=
        '<button type="button" class="qqmp-chip qqmp-chip--def" data-pair="' +
        d.pair +
        '">' +
        escHtml(d.text.length > 180 ? d.text.slice(0, 180) + "…" : d.text) +
        "</button>";
    });
    var inner =
      '<div class="qqmp-grid">' +
      '<div><p class="qqmp-col-title">Words</p><div class="qqmp-stack" id="qqmp-words">' +
      wHtml +
      '</div></div><div><p class="qqmp-col-title">Definitions</p><div class="qqmp-stack" id="qqmp-defs">' +
      dHtml +
      "</div></div></div>";
    root.innerHTML = shell("QQ-card--mp", inner, metaLine());
    bindNext();

    var selWord = null;
    var matched = 0;
    var colorIdx = 0;

    function tryMatch(wordEl, defEl) {
      var pw = parseInt(wordEl.getAttribute("data-pair"), 10);
      var pd = parseInt(defEl.getAttribute("data-pair"), 10);
      if (pw !== pd) {
        wordEl.classList.add("qqmp-shake");
        defEl.classList.add("qqmp-shake");
        setTimeout(function () {
          wordEl.classList.remove("qqmp-shake", "is-sel");
          defEl.classList.remove("qqmp-shake", "is-sel-def");
          selWord = null;
        }, 350);
        return;
      }
      var c = pairColors[colorIdx % pairColors.length];
      colorIdx++;
      wordEl.classList.remove("is-sel");
      defEl.classList.remove("is-sel-def");
      wordEl.classList.add("is-matched", c);
      defEl.classList.add("is-matched", c);
      wordEl.disabled = true;
      defEl.disabled = true;
      matched++;
      selWord = null;
      if (matched >= triple.length) enableNext();
    }

    root.querySelectorAll("#qqmp-words .qqmp-chip").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.disabled) return;
        root.querySelectorAll("#qqmp-words .qqmp-chip").forEach(function (b) {
          b.classList.remove("is-sel");
        });
        btn.classList.add("is-sel");
        selWord = btn;
      });
    });
    root.querySelectorAll("#qqmp-defs .qqmp-chip").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.disabled || !selWord) return;
        tryMatch(selWord, btn);
      });
    });
  }

  function paintSpell(idx, card) {
    var answer = (card.word || "").trim();
    var chars = answer.split("");
    var defSafe = escHtml((card.definition || "—").trim());
    var boxesHtml = "";
    for (var i = 0; i < chars.length; i++) {
      boxesHtml += '<span class="qqsp-lbox" data-i="' + i + '"></span>';
    }
    var inner =
      '<p class="qqsp-def">' +
      defSafe +
      '</p><div class="qqsp-letters" id="qqsp-boxes">' +
      boxesHtml +
      '</div><input type="text" class="qqsp-input" id="qqsp-in" autocomplete="off" />' +
      '<div class="qqsp-row">' +
      '<button type="button" class="qqsp-check" id="qqsp-check">Check</button>' +
      '</div><p class="qqsp-feedback" id="qqsp-fb"></p>';
    root.innerHTML = shell("QQ-card--sp", inner, metaLine());
    bindNext();
    var inp = document.getElementById("qqsp-in");
    var fb = document.getElementById("qqsp-fb");
    var boxes = root.querySelectorAll(".qqsp-lbox");
    document.getElementById("qqsp-check").addEventListener("click", function () {
      var guess = (inp.value || "").trim();
      var okAll = guess.toLowerCase() === answer.toLowerCase();
      for (var i = 0; i < boxes.length; i++) {
        var g = (guess[i] || "").toLowerCase();
        var a = (chars[i] || "").toLowerCase();
        boxes[i].textContent = guess[i] || "";
        if (!guess.length) {
          boxes[i].classList.remove("is-ok", "is-bad");
          continue;
        }
        if (g === a) boxes[i].classList.add("is-ok");
        else boxes[i].classList.add("is-bad");
      }
      fb.textContent = okAll ? "✓ Correct!" : "✗ Answer: " + answer;
      fb.className = "qqsp-feedback " + (okAll ? "is-ok" : "is-bad");
      enableNext();
    });
  }

  function paintListen(idx, card) {
    var dc = buildDefChoices(idx);
    var correctDef = String(dc.correctDef || "").trim();
    var options = dc.options;
    var word = card.word || "";

    var inner =
      '<div class="qqln-play-wrap" id="qqln-stage">' +
      '<button type="button" class="qqln-play" id="qqln-play" aria-label="Play word">' +
      '<span class="qqln-play-icon" aria-hidden="true"></span>' +
      "</button>" +
      '<p class="qqln-hint" id="qqln-hint">Tap to hear the word</p>' +
      "</div>" +
      '<div id="qqln-after" hidden>' +
      '<p class="qqln-prompt">Pick the correct meaning</p>' +
      '<div class="qqln-grid" id="qqln-grid"></div>' +
      "</div>";
    root.innerHTML = shell("QQ-card--ln", inner, metaLine());
    bindNext();

    var hint = document.getElementById("qqln-hint");
    var playBtn = document.getElementById("qqln-play");
    var after = document.getElementById("qqln-after");
    var grid = document.getElementById("qqln-grid");

    playBtn.addEventListener("click", function () {
      hint.textContent = "Playing…";
      playBtn.disabled = true;
      try {
        if (!window.speechSynthesis || !word) {
          after.hidden = false;
          buildListenGrid();
          return;
        }
        var u = new SpeechSynthesisUtterance(String(word));
        u.lang = "en-GB";
        u.rate = 0.85;
        window.speechSynthesis.cancel();
        u.onend = function () {
          hint.textContent = "Tap to hear again";
          playBtn.disabled = false;
          after.hidden = false;
          buildListenGrid();
        };
        window.speechSynthesis.speak(u);
      } catch (e) {
        hint.textContent = "Tap to hear again";
        playBtn.disabled = false;
        after.hidden = false;
        buildListenGrid();
      }
    });

    function buildListenGrid() {
      if (grid.querySelector(".qqln-opt")) return;
      options.forEach(function (defText) {
        var dt = String(defText || "").trim();
        var b = document.createElement("button");
        b.type = "button";
        b.className = "qqln-opt";
        b.setAttribute("data-def", dt);
        b.textContent = dt.length > 120 ? dt.slice(0, 120) + "…" : dt;
        grid.appendChild(b);
      });
      grid.querySelectorAll(".qqln-opt").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var picked = String(btn.getAttribute("data-def") || "").trim();
          var ok = picked === correctDef;
          grid.querySelectorAll(".qqln-opt").forEach(function (b) {
            b.disabled = true;
            var d = String(b.getAttribute("data-def") || "").trim();
            if (d === correctDef) b.classList.add("is-reveal-correct");
            else if (b === btn) b.classList.add("is-reveal-wrong");
          });
          enableNext();
        });
      });
    }
  }

  paintQ();
})();
