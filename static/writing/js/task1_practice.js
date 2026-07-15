(function () {
  "use strict";

  function words(text) {
    return (text || "")
      .trim()
      .split(/\s+/)
      .filter(Boolean).length;
  }

  function bindWordCount() {
    var area = document.getElementById("wt1-response");
    if (!area) return;
    var form = document.getElementById("wt1-response-form");
    var minWords = Number((form && form.getAttribute("data-min-words")) || 150);
    var live = document.getElementById("wt1-live-count");
    var progN = document.getElementById("wt1-progress-count");
    var fill = document.getElementById("wt1-progress-fill");
    function repaint() {
      var n = words(area.value);
      if (live) live.textContent = String(n);
      if (progN) progN.textContent = String(n);
      if (fill) {
        var pct = Math.max(0, Math.min(100, (n / minWords) * 100));
        fill.style.width = pct + "%";
        fill.classList.toggle("is-good", n >= minWords);
      }
    }
    area.addEventListener("input", repaint);
    repaint();
  }

  function bindTimer() {
    var timer = document.getElementById("wt1-timer");
    if (!timer) return;
    var fixed = timer.getAttribute("data-fixed");
    if (fixed) {
      timer.textContent = fixed;
      return;
    }
    var area = document.getElementById("wt1-response");
    if (!area) {
      timer.textContent = "20:00";
      return;
    }
    var key = "wt1_timer_" + window.location.pathname;
    var form = document.getElementById("wt1-response-form");
    var durationMinutes = Number((form && form.getAttribute("data-duration-minutes")) || 20);
    var now = Date.now();
    var end = Number(localStorage.getItem(key) || 0);
    if (!end || end < now) {
      end = now + durationMinutes * 60 * 1000;
      localStorage.setItem(key, String(end));
    }

    function paint() {
      var remain = Math.max(0, end - Date.now());
      var mins = Math.floor(remain / 60000);
      var secs = Math.floor((remain % 60000) / 1000);
      timer.textContent = String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
      timer.classList.toggle("is-red", remain <= 2 * 60 * 1000);
    }

    paint();
    setInterval(paint, 1000);

    var form = document.getElementById("wt1-response-form");
    if (form) {
      form.addEventListener("submit", function () {
        var used = Math.max(0, Math.round((durationMinutes * 60 * 1000 - (end - Date.now())) / 1000));
        var hidden = document.getElementById("wt1-time-used");
        if (!hidden) return;
        hidden.value = String(used);
      });
    }
  }

  function renderAnnotated(raw) {
    var text = String(raw || "");
    function esc(s) {
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }
    var out = "";
    var idx = 0;
    var re =
      /<<GREEN>>(.*?)<(?:<)?\/GREEN>>|<<RED error="([^"]*)" reason="([^"]*)">>(.*?)<(?:<)?\/RED>>|<<AMBER better="([^"]*)" reason="([^"]*)">>(.*?)<(?:<)?\/AMBER>>/gs;
    var m;
    while ((m = re.exec(text)) !== null) {
      out += esc(text.slice(idx, m.index));
      if (m[1] !== undefined) {
        out += '<span class="ann-good">' + esc(m[1]) + "</span>";
      } else if (m[4] !== undefined) {
        out += '<span class="ann-err" title="→ ' + esc(m[2]) + '">' + esc(m[4]) + "</span>";
      } else if (m[7] !== undefined) {
        out += '<span class="ann-imp" title="Better: ' + esc(m[5]) + '">' + esc(m[7]) + "</span>";
      }
      idx = re.lastIndex;
    }
    out += esc(text.slice(idx));
    return out.replace(/\n/g, "<br>");
  }

  function extractRows(raw) {
    var text = String(raw || "");
    var red = [];
    var amber = [];
    text.replace(/<<RED error="([^"]*)" reason="([^"]*)">>(.*?)<(?:<)?\/RED>>/g, function (_, corr, reason, orig) {
      red.push({ orig: orig, corr: corr, reason: reason });
      return _;
    });
    text.replace(
      /<<AMBER better="([^"]*)" reason="([^"]*)">>(.*?)<(?:<)?\/AMBER>>/g,
      function (_, better, reason, orig) {
        amber.push({ orig: orig, better: better, reason: reason });
        return _;
      }
    );
    return { red: red, amber: amber };
  }

  function bindFeedbackPage() {
    var fbEl = document.getElementById("wt1-feedback-json");
    var criteriaEl = document.getElementById("wt1-criteria-json");
    if (!fbEl || !criteriaEl) return;
    var feedback = JSON.parse(fbEl.textContent || "{}");
    var criteria = JSON.parse(criteriaEl.textContent || "[]");
    var annHost = document.getElementById("wt1-annotated-text");
    if (annHost) annHost.innerHTML = renderAnnotated(feedback.annotated_text || "");
    var corrections = extractRows(feedback.annotated_text || "");
    var corrHost = document.getElementById("wt1-corrections");
    if (corrHost) {
      var rows = [];
      corrections.red.forEach(function (r) {
        rows.push(
          '<div class="wt1-corr-row is-red"><div class="icon">' + (typeof BSIcons !== "undefined" ? BSIcons.cross() : "") + '</div><div><strong>"' +
            r.orig +
            '"</strong> → <strong>"' +
            r.corr +
            '"</strong><p>' +
            r.reason +
            "</p></div></div>"
        );
      });
      corrections.amber.forEach(function (r) {
        rows.push(
          '<div class="wt1-corr-row is-amber"><div class="icon">↗</div><div><strong>"' +
            r.orig +
            '"</strong> → <strong>"' +
            r.better +
            '"</strong><p>' +
            r.reason +
            "</p></div></div>"
        );
      });
      corrHost.innerHTML = rows.join("");
    }

    document.querySelectorAll(".wt1-ann-text[data-excerpt]").forEach(function (el) {
      var key = el.getAttribute("data-excerpt");
      var map = {
        task_achievement: "task_excerpt",
        coherence_cohesion: "coherence_excerpt",
        lexical_resource: "lexical_excerpt",
        grammar_accuracy: "grammar_excerpt",
      };
      el.innerHTML = renderAnnotated(feedback[map[key]] || "");
    });

    var panel = document.getElementById("wt1-crit-panel");
    function paintCriterion(key) {
      var c = null;
      for (var i = 0; i < criteria.length; i++) {
        if (criteria[i].key === key) {
          c = criteria[i];
          break;
        }
      }
      if (!c || !panel) return;
      var pct = Math.max(0, Math.min(100, (Number(c.score || 0) / 9) * 100));
      panel.innerHTML =
        '<div class="wt1-crit-panel__row"><strong>' +
        c.label +
        '</strong><span>' +
        Number(c.score || 0).toFixed(1) +
        "</span></div>" +
        '<div class="wt1-scoreline"><span class="fill" style="width:' +
        pct +
        "%;background:" +
        c.color +
        '"></span></div>' +
        '<p class="wt1-sub wt1-sub--tight">' +
        (feedback.summary || "") +
        "</p>";
    }
    var first = criteria.length ? criteria[0].key : null;
    document.querySelectorAll(".wt1-crit-tab").forEach(function (btn) {
      if (btn.classList.contains("is-active")) first = btn.getAttribute("data-criterion");
      btn.addEventListener("click", function () {
        document.querySelectorAll(".wt1-crit-tab").forEach(function (b) {
          b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
        paintCriterion(btn.getAttribute("data-criterion"));
      });
    });
    if (first) paintCriterion(first);

    document.querySelectorAll(".wt1-ac-row .wt1-ac-head").forEach(function (head) {
      head.addEventListener("click", function () {
        head.parentElement.classList.toggle("is-open");
      });
    });

    document.querySelectorAll(".wt1-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        var key = tab.getAttribute("data-tab");
        document.querySelectorAll(".wt1-tab").forEach(function (t) {
          t.classList.remove("is-on");
        });
        document.querySelectorAll(".wt1-tab-panel").forEach(function (p) {
          p.classList.remove("is-on");
        });
        tab.classList.add("is-on");
        var panelEl = document.querySelector('.wt1-tab-panel[data-panel="' + key + '"]');
        if (panelEl) panelEl.classList.add("is-on");
      });
    });

    var vocabHost = document.getElementById("wt1-next-vocab");
    if (vocabHost) {
      var weakest = document.querySelector(".wt1-weak-badge");
      var parent = weakest ? weakest.closest(".wt1-ac-row") : null;
      var key = parent ? parent.getAttribute("data-key") : "lexical_resource";
      if (key === "grammar_accuracy") {
        vocabHost.innerHTML =
          "<ul><li>Subject-verb agreement</li><li>Article use (a/the)</li><li>Comparative forms</li><li>Comma after discourse markers</li><li>Tense consistency</li></ul>";
      } else if (key === "coherence_cohesion") {
        vocabHost.innerHTML =
          "<ul><li>Contrast: however, in contrast, whereas</li><li>Addition: moreover, furthermore</li><li>Result: therefore, consequently</li><li>Highlight: notably, it is clear that</li></ul>";
      } else if (key === "task_achievement") {
        vocabHost.innerHTML =
          "<ol><li>Write a clear overview sentence</li><li>Cover all key categories</li><li>Use at least 4 specific figures</li><li>Make direct comparisons</li><li>Avoid opinions</li></ol>";
      } else {
        vocabHost.innerHTML =
          '<div class="wt1-vocab-grid"><div><h4>' + (typeof BSIcons !== "undefined" ? BSIcons.inline("trend-up", "ok") : "") + ' Increases</h4><p>rose · increased · surged · climbed · edged up · doubled</p></div><div><h4>' + (typeof BSIcons !== "undefined" ? BSIcons.inline("trend-down", "bad") : "") + ' Decreases</h4><p>fell · declined · dropped · dipped · halved</p></div><div><h4>' + (typeof BSIcons !== "undefined" ? BSIcons.inline("scale", "ok") : "") + ' Stability</h4><p>remained stable · levelled off · plateaued · fluctuated</p></div><div><h4>' + (typeof BSIcons !== "undefined" ? BSIcons.inline("chart", "ok") : "") + ' Proportions</h4><p>accounted for · the majority of · a minority of · dominated</p></div></div>';
      }
    }
  }

  bindWordCount();
  bindTimer();
  bindFeedbackPage();
})();
