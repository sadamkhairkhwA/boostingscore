/**
 * Shared practice question UI for Reading course stages.
 */
(function (global) {
  "use strict";

  var ICON_CHECK =
    '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>';
  var ICON_X =
    '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18"/></svg>';

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function buildPracticeBlock(practice) {
    var wrap = document.createElement("div");
    wrap.className = "rs-practice";

    if (practice.instructions) {
      var instr = document.createElement("p");
      instr.className = "rs-practice-instructions";
      instr.textContent = practice.instructions;
      wrap.appendChild(instr);
    }

    if (practice.passage) {
      var passBox = document.createElement("div");
      passBox.className = "rs-exbox rs-practice-passage-box";
      var passLbl = document.createElement("div");
      passLbl.className = "rs-exbox-lbl";
      passLbl.textContent = "Passage";
      var passP = document.createElement("p");
      passP.className = "rs-passage";
      passP.textContent = practice.passage;
      passBox.appendChild(passLbl);
      passBox.appendChild(passP);
      wrap.appendChild(passBox);
    }

    var qList = document.createElement("div");
    qList.className = "rs-practice-questions";

    (practice.questions || []).forEach(function (q, idx) {
      var qEl = document.createElement("div");
      qEl.className = "rs-prq";
      qEl.setAttribute("data-qid", q.id);
      qEl.setAttribute("data-answer", q.answer);

      var prompt = document.createElement("p");
      prompt.className = "rs-prq-prompt";
      var promptHtml = '<span class="rs-prq-num">' + (idx + 1) + ".</span> ";
      if (q.strategy) {
        promptHtml +=
          '<span class="rs-prq-strategy">' + escapeHtml(q.strategy) + "</span> ";
      }
      promptHtml += escapeHtml(q.prompt);
      prompt.innerHTML = promptHtml;
      qEl.appendChild(prompt);

      var opts = document.createElement("div");
      opts.className =
        "rs-prq-opts" + (q.type === "tfng" ? " rs-prq-opts--tfng" : "");

      (q.options || []).forEach(function (opt) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "rs-prq-opt";
        btn.setAttribute("data-value", opt.value);
        btn.textContent = opt.label;
        opts.appendChild(btn);
      });
      qEl.appendChild(opts);

      var fb = document.createElement("div");
      fb.className = "rs-prq-feedback";
      fb.hidden = true;
      qEl.appendChild(fb);

      qList.appendChild(qEl);
    });

    wrap.appendChild(qList);
    return wrap;
  }

  function collectQuestions(data) {
    var list = [];
    (data.lessons || []).forEach(function (lesson) {
      var practice = lesson.practice;
      if (!practice || !practice.questions) return;
      practice.questions.forEach(function (q) {
        list.push(q);
      });
    });
    if (data.mixedReview && data.mixedReview.questions) {
      data.mixedReview.questions.forEach(function (q) {
        list.push(q);
      });
    }
    return list;
  }

  function findExplanation(data, qid) {
    var all = collectQuestions(data);
    var i;
    for (i = 0; i < all.length; i++) {
      if (all[i].id === qid) return all[i].explanation;
    }
    return "";
  }

  function mountPracticeHosts(root, data, resolvePractice) {
    var hosts = root.querySelectorAll(".rs-practice-host");
    Array.prototype.forEach.call(hosts, function (host) {
      var id = host.getAttribute("data-rs-practice-lesson");
      var practice = resolvePractice(id);
      if (!practice) return;
      host.innerHTML = "";
      host.appendChild(buildPracticeBlock(practice));
    });

    var prqs = root.querySelectorAll(".rs-prq");
    Array.prototype.forEach.call(prqs, function (qEl) {
      var opts = qEl.querySelectorAll(".rs-prq-opt");
      Array.prototype.forEach.call(opts, function (btn) {
        btn.addEventListener("click", function () {
          if (qEl.classList.contains("is-answered")) return;
          var chosen = btn.getAttribute("data-value");
          var correct = qEl.getAttribute("data-answer");
          var ok = chosen === correct;
          qEl.classList.add("is-answered");
          qEl.classList.add(ok ? "is-correct" : "is-wrong");

          Array.prototype.forEach.call(opts, function (b) {
            var val = b.getAttribute("data-value");
            b.disabled = true;
            if (val === correct) b.classList.add("is-correct-opt");
            else if (val === chosen && !ok) b.classList.add("is-wrong-opt");
          });

          var fb = qEl.querySelector(".rs-prq-feedback");
          var qid = qEl.getAttribute("data-qid");
          var explanation = findExplanation(data, qid);
          if (fb) {
            fb.hidden = false;
            fb.className =
              "rs-prq-feedback " + (ok ? "rs-prq-feedback--ok" : "rs-prq-feedback--bad");
            fb.innerHTML =
              (ok ? ICON_CHECK : ICON_X) +
              " <span>" +
              escapeHtml(explanation || (ok ? "Correct." : "Not quite.")) +
              "</span>";
          }

          document.dispatchEvent(new CustomEvent("rs-practice-answered"));
        });
      });
    });
  }

  function allAnsweredIn(container) {
    var prqs = container.querySelectorAll(".rs-prq");
    if (!prqs.length) return true;
    return Array.prototype.every.call(prqs, function (el) {
      return el.classList.contains("is-answered");
    });
  }

  global.ReadingPractice = {
    buildPracticeBlock: buildPracticeBlock,
    mountPracticeHosts: mountPracticeHosts,
    allAnsweredIn: allAnsweredIn,
    findExplanation: findExplanation,
  };
})(window);
