(function () {
  function closeAll(except) {
    document.querySelectorAll("[data-avatar-menu]").forEach(function (root) {
      if (except && root === except) return;
      var panel = root.querySelector("[data-avatar-panel]");
      var btn = root.querySelector("[data-avatar-toggle]");
      if (panel) panel.hidden = true;
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-avatar-toggle]");
    if (toggle) {
      e.preventDefault();
      e.stopPropagation();
      var root = toggle.closest("[data-avatar-menu]");
      var panel = root && root.querySelector("[data-avatar-panel]");
      if (!panel) return;
      var open = panel.hidden;
      closeAll();
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      return;
    }
    if (!e.target.closest("[data-avatar-menu]")) closeAll();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll();
  });
})();
