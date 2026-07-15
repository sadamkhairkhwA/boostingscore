(function () {
  "use strict";
  var dataEl = document.getElementById("ld-drills-data");
  var host = document.getElementById("ld-drills-host");
  if (!dataEl || !host) return;
  var drills = JSON.parse(dataEl.textContent);
  var idx = 0;

  function norm(s) {
    return String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[.,;:!?"']/g, "")
      .replace(/\s+/g, " ");
  }

  function isCorrect(drill, given) {
    var g = norm(given);
    var accepted = drill.accepted || [drill.answer];
    return accepted.some(function (a) {
      return norm(a) === g;
    });
  }

  function render() {
    var d = drills[idx];
    host.innerHTML =
      '<article class="ld-card">' +
      '<span class="ld-card__type">' +
      d.label +
      "</span>" +
      '<p class="ld-card__hint">' +
      (d.hint || "") +
      "</p>" +
      '<div class="ll-aud ld-aud">' +
      '<button type="button" class="ll-aud__btn ld-play" aria-label="Play">' +
      '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M8 5v14l11-7L8 5z"/></svg></button>' +
      '<div class="ll-aud__main"><div class="ll-aud__status">Tap play — clip plays once.</div></div>' +
      '<span class="ll-aud__once">Plays once</span>' +
      '<audio preload="auto" src="' +
      d.audio_url +
      '"></audio></div>' +
      '<label class="ld-input-lbl">Type what you hear</label>' +
      '<input type="text" class="ll-input ld-input" autocomplete="off">' +
      '<button type="button" class="ll-btn ll-btn--primary ld-check">Check</button>' +
      '<div class="ld-feedback" hidden></div>' +
      '<p class="ld-progress">Drill ' +
      (idx + 1) +
      " of " +
      drills.length +
      "</p></article>";

    var card = host.querySelector(".ld-card");
    var audio = card.querySelector("audio");
    var played = false;
    card.querySelector(".ld-play").addEventListener("click", function () {
      if (played) return;
      played = true;
      audio.play().catch(function () {});
      card.querySelector(".ll-aud__status").textContent = "Playing…";
      audio.addEventListener("ended", function () {
        card.querySelector(".ll-aud__status").textContent = "Clip finished — type your answer.";
      });
    });

    card.querySelector(".ld-check").addEventListener("click", function () {
      var inp = card.querySelector(".ld-input");
      var fb = card.querySelector(".ld-feedback");
      var ok = isCorrect(d, inp.value);
      fb.hidden = false;
      fb.className = "ld-feedback " + (ok ? "ld-feedback--ok" : "ld-feedback--bad");
      fb.textContent = ok
        ? "Correct — " + d.answer
        : "Not quite — correct answer: " + d.answer + ". " + (d.hint || "");
      if (ok && idx < drills.length - 1) {
        setTimeout(function () {
          idx++;
          render();
        }, 1200);
      }
    });
  }

  render();
})();
