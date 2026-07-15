(function () {
  "use strict";
  var el = document.getElementById("ti-words-payload");
  if (!el) return;
  var data = JSON.parse(el.textContent);
  var words = data.words || [];
  var wordBests = data.word_bests || {};
  var selected = {};
  var filter = "all";
  var searchInput = document.getElementById("ti-word-search");
  var searchQ = "";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function passes(meta) {
    return meta && meta.passed;
  }
  function status(item) {
    var b = wordBests[item.item_id] || { total: 0, out_of: 10, passed: false };
    var t = Number(b.total || 0);
    var o = Number(b.out_of || 10);
    if (!t && !b.passed) return { key: "new", label: "Not started", cls: "ti-word-row__badge--new" };
    if (passes(b)) return { key: "done", label: t + "/" + o, cls: "ti-word-row__badge--done" };
    return { key: "retry", label: t + "/" + o + " retry", cls: "ti-word-row__badge--retry" };
  }

  function includeByFilter(item) {
    var st = status(item).key;
    return filter === "all" || filter === st;
  }

  function matchesSearch(item) {
    if (!searchQ) return true;
    var blob = ((item.word || "") + " " + (item.pos || "")).toLowerCase();
    return blob.indexOf(searchQ) !== -1;
  }

  function visibleWords() {
    return words.filter(includeByFilter).filter(matchesSearch);
  }

  function selectedCount() {
    return Object.keys(selected).filter(function (k) {
      return selected[k];
    }).length;
  }

  function checkMark() {
    return typeof BSIcons !== "undefined" ? BSIcons.check() : "";
  }

  function rowClass(st, isSel) {
    var c = "ti-word-row";
    if (st.key === "done" && isSel) return c + " ti-word-row--done-sel";
    if (isSel) return c + " ti-word-row--sel";
    if (st.key === "done") return c + " ti-word-row--done-only";
    return c;
  }

  function render() {
    var host = document.getElementById("ti-word-rows");
    if (!host) return;
    var list = visibleWords();
    host.innerHTML = list
      .map(function (item) {
        var st = status(item);
        var isSel = !!selected[item.item_id];
        return (
          '<div class="' +
          rowClass(st, isSel) +
          '" data-id="' +
          escapeHtml(item.item_id) +
          '">' +
          '<span class="ti-word-row__cb ' +
          (isSel ? "ti-word-row__cb--on" : "") +
          '">' +
          (isSel ? checkMark() : "") +
          "</span>" +
          '<div class="ti-word-row__main"><span class="ti-word-row__line">' +
          '<span class="ti-word-row__word">' +
          escapeHtml(item.word || "") +
          "</span>" +
          '<span class="ti-word-row__pos">' +
          escapeHtml(item.pos || "word") +
          "</span></span></div>" +
          '<span class="ti-word-row__badge ' +
          st.cls +
          '">' +
          (st.key === "done" ? checkMark() + " " : "") +
          escapeHtml(st.label) +
          "</span>" +
          "</div>"
        );
      })
      .join("");
    host.querySelectorAll(".ti-word-row").forEach(function (row) {
      row.addEventListener("click", function () {
        var id = row.getAttribute("data-id");
        selected[id] = !selected[id];
        render();
      });
    });
    var c = selectedCount();
    var countEl = document.getElementById("ti-selected-count");
    if (countEl) {
      countEl.textContent = c === 1 ? "1 word selected" : c + " words selected";
    }
    var btn = document.getElementById("ti-start-session");
    if (btn) {
      btn.disabled = c === 0;
    }
  }

  document.getElementById("ti-select-all").addEventListener("click", function () {
    visibleWords().forEach(function (w) {
      selected[w.item_id] = true;
    });
    render();
  });
  document.getElementById("ti-clear-all").addEventListener("click", function () {
    visibleWords().forEach(function (w) {
      delete selected[w.item_id];
    });
    render();
  });

  var filterRow = document.getElementById("ti-filter-row");
  if (filterRow) {
    filterRow.addEventListener("click", function (e) {
      var btn = e.target.closest(".ti-ws-filter");
      if (!btn || !filterRow.contains(btn)) return;
      filter = btn.getAttribute("data-filter") || "all";
      filterRow.querySelectorAll(".ti-ws-filter").forEach(function (x) {
        x.classList.remove("ti-ws-filter--on");
      });
      btn.classList.add("ti-ws-filter--on");
      render();
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      searchQ = (searchInput.value || "").trim().toLowerCase();
      render();
    });
  }

  document.getElementById("ti-start-session").addEventListener("click", function () {
    var ids = Object.keys(selected).filter(function (k) {
      return selected[k];
    });
    if (!ids.length) return;
    window.location.href = data.session_url + "?words=" + encodeURIComponent(ids.join(","));
  });

  render();
})();
