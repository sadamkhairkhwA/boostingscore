(function () {
  var root = document.querySelector(".home-mint");
  if (!root) return;

  function onScroll() {
    var y = window.scrollY || 0;
    var v = -Math.min(y * 0.08, 48);
    root.style.setProperty("--mint-scroll", v + "px");
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var reduce =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    root.style.setProperty("--mint-breathe-y", "0px");
    return;
  }

  var t0 = performance.now();
  function frame(now) {
    var t = (now - t0) / 1000;
    var breathe = Math.sin(t * 0.55) * 6 + Math.sin(t * 1.15) * 2.5;
    root.style.setProperty("--mint-breathe-y", breathe.toFixed(3) + "px");
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
