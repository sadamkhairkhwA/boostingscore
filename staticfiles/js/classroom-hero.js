/**
 * Classroom canvas: only inside .home-mint__hero-left. Resizes to parent getBoundingClientRect().
 * Chalkboard cycles short motivation lines with a typewriter effect.
 */
(function () {
  var canvas = document.getElementById("classroom-canvas");
  if (!canvas) return;

  var ctx;
  var W = 0;
  var H = 0;
  var dpr = 1;
  var visible = true;
  var rafId = 0;

  var reduce =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var MOTIVATIONS = [
    "You got this!",
    "Keep going.",
    "One step at a time.",
    "Small wins add up.",
    "Focus. Breathe. Improve.",
    "You've got the spark.",
    "Trust the process.",
    "Progress beats perfect.",
  ];

  function resize() {
    var parent = canvas.parentElement;
    if (!parent) return;
    var rect = parent.getBoundingClientRect();
    var rw = Math.max(1, Math.floor(rect.width));
    var rh = Math.max(1, Math.floor(rect.height));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(rw * dpr);
    canvas.height = Math.round(rh * dpr);
    canvas.style.width = rw + "px";
    canvas.style.height = rh + "px";
    W = rw;
    H = rh;
    ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function motivationBoard(phaseSec) {
    if (reduce) {
      var si = Math.floor(phaseSec / 2.8) % MOTIVATIONS.length;
      return { text: MOTIVATIONS[si], caret: false };
    }
    var period = 5.4;
    var total = MOTIVATIONS.length * period;
    var cycle = phaseSec % total;
    var idx = Math.floor(cycle / period) % MOTIVATIONS.length;
    var t = cycle % period;
    var msg = MOTIVATIONS[idx];
    var cps = 15;
    var typeDur = msg.length / cps;
    if (t < typeDur) {
      var n = Math.min(msg.length, Math.floor(t * cps));
      return { text: msg.slice(0, n), caret: true };
    }
    var blink = Math.floor(t * 2.8) % 2 === 0;
    return { text: msg, caret: blink };
  }

  function draw(phase) {
    if (!ctx || W < 2 || H < 2) return;

    ctx.clearRect(0, 0, W, H);

    var sceneShiftY = Math.round(H * 0.03);
    ctx.fillStyle = "#ebe3d4";
    ctx.fillRect(0, 0, W, sceneShiftY);
    ctx.save();
    ctx.translate(0, sceneShiftY);

    /* Keep top ~36% as plain wall only so hero text (HTML overlay) does not sit on shelf/board */
    var floorY = H * 0.8;
    var wallPlainEnd = H * 0.36;

    ctx.fillStyle = "#ebe3d4";
    ctx.fillRect(0, 0, W, floorY);

    ctx.fillStyle = "#c9a87a";
    ctx.beginPath();
    ctx.moveTo(0, floorY);
    ctx.lineTo(W, floorY);
    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = "rgba(100, 80, 55, 0.14)";
    ctx.lineWidth = 1;
    for (var g = 0; g < 14; g++) {
      var gx = (g / 14) * W * 1.2 - W * 0.05;
      ctx.beginPath();
      ctx.moveTo(gx, floorY);
      ctx.lineTo(gx + W * 0.12, H);
      ctx.stroke();
    }

    var trimY = wallPlainEnd - H * 0.015;
    ctx.strokeStyle = "rgba(110, 95, 78, 0.5)";
    ctx.lineWidth = 0.75;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(0, trimY);
    ctx.lineTo(W, trimY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, trimY + 3);
    ctx.lineTo(W, trimY + 3);
    ctx.stroke();

    var shelfX = W * 0.04;
    var shelfY = H * 0.4;
    var shelfW = W * 0.26;
    var shelfH = H * 0.3;
    ctx.fillStyle = "#8d6e63";
    ctx.fillRect(shelfX, shelfY, shelfW, shelfH);
    ctx.strokeStyle = "#5d4037";
    ctx.lineWidth = 2;
    for (var s = 0; s < 4; s++) {
      var sy = shelfY + (shelfH / 4) * (s + 1);
      ctx.beginPath();
      ctx.moveTo(shelfX, sy);
      ctx.lineTo(shelfX + shelfW, sy);
      ctx.stroke();
    }
    var bookColors = ["#e57373", "#ffb74d", "#4db6ac", "#ba68c8", "#fff176", "#90a4ae"];
    for (var b = 0; b < 15; b++) {
      var col = b % 4;
      var row = (b / 4) | 0;
      if (row > 2) break;
      var bw = shelfW / 4 - 4;
      var bh = shelfH / 4 - 14;
      ctx.fillStyle = bookColors[b % bookColors.length];
      ctx.fillRect(
        shelfX + 6 + col * (shelfW / 4),
        shelfY + 10 + row * (shelfH / 4),
        bw,
        bh
      );
    }

    var boardX = W * 0.38;
    var boardY = H * 0.42;
    var boardW = W * 0.38;
    var boardH = H * 0.26;
    ctx.fillStyle = "#5d4037";
    ctx.fillRect(boardX - 5, boardY - 5, boardW + 10, boardH + 10);
    ctx.fillStyle = "#2e4a3a";
    ctx.fillRect(boardX, boardY, boardW, boardH);

    var mb = motivationBoard(phase);
    var fontPx = Math.max(10, Math.min(W * 0.028, boardW * 0.09));
    ctx.font = "600 " + fontPx + "px Inter, system-ui, sans-serif";
    ctx.fillStyle = "rgba(255, 248, 225, 0.92)";
    var tx = boardX + boardW * 0.08;
    var ty = boardY + boardH * 0.42;
    var line = mb.text;
    if (ctx.measureText(line).width > boardW * 0.84) {
      ctx.font = "600 " + Math.max(8, fontPx * 0.85) + "px Inter, system-ui, sans-serif";
    }
    ctx.fillText(line, tx, ty);
    if (mb.caret) {
      var tw = ctx.measureText(line).width;
      ctx.fillStyle = "rgba(255, 248, 225, 0.75)";
      ctx.fillRect(tx + tw + 1, ty - fontPx * 0.85, 2, fontPx * 0.95);
    }

    ctx.font = "500 " + Math.max(8, W * 0.02) + "px Inter, system-ui, sans-serif";
    ctx.fillStyle = "rgba(255, 248, 225, 0.55)";
    ctx.fillText("— IELTS study club", boardX + boardW * 0.08, boardY + boardH * 0.72);

    var deskX = W * 0.78;
    var deskY = H * 0.73;
    var deskW = W * 0.2;
    ctx.fillStyle = "#a1887f";
    ctx.fillRect(deskX, deskY, deskW, H * 0.065);
    ctx.fillStyle = "#795548";
    ctx.fillRect(deskX + deskW * 0.15, deskY - 4, deskW * 0.7, 6);

    ctx.fillStyle = "#5c6bc0";
    ctx.fillRect(deskX + 8, deskY - 16, 10, 14);
    ctx.fillStyle = "#ef5350";
    ctx.fillRect(deskX + 22, deskY - 14, 8, 12);
    ctx.fillStyle = "#26a69a";
    ctx.fillRect(deskX + 34, deskY - 15, 9, 13);

    var globeX = deskX + deskW * 0.72;
    var globeY = deskY - 10;
    ctx.fillStyle = "#1e88e5";
    ctx.beginPath();
    ctx.arc(globeX, globeY, 9, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#0d47a1";
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.strokeStyle = "rgba(255,255,255,0.5)";
    ctx.beginPath();
    ctx.arc(globeX, globeY, 9, -0.3, 0.8);
    ctx.stroke();

    var cx = W * 0.88;
    var cy = H * 0.38;
    var cr = Math.min(W, H) * 0.055;
    ctx.fillStyle = "#faf8f5";
    ctx.beginPath();
    ctx.arc(cx, cy, cr, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#8d6e63";
    ctx.lineWidth = 2;
    ctx.stroke();
    var ang = reduce ? -Math.PI / 2 : phase * 0.35 - Math.PI / 2;
    ctx.strokeStyle = "#37474f";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(ang) * cr * 0.55, cy + Math.sin(ang) * cr * 0.55);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx, cy - cr * 0.35);
    ctx.stroke();

    ctx.restore();
  }

  var t0 = performance.now();
  function loop(now) {
    if (!visible) {
      rafId = 0;
      return;
    }
    var phase = (now - t0) / 1000;
    draw(phase);
    if (!reduce) rafId = requestAnimationFrame(loop);
  }

  function startLoop() {
    if (reduce) {
      draw(0);
      return;
    }
    if (!rafId && visible) rafId = requestAnimationFrame(loop);
  }

  function stopLoop() {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  function onVis(entries) {
    entries.forEach(function (e) {
      visible = e.isIntersecting;
      if (visible) startLoop();
      else stopLoop();
    });
  }

  resize();
  if (reduce) draw(0);
  else startLoop();

  window.addEventListener("resize", function () {
    resize();
    if (reduce) draw(0);
  });

  if (window.ResizeObserver && canvas.parentElement) {
    var ro = new ResizeObserver(function () {
      resize();
      if (reduce) draw(0);
    });
    ro.observe(canvas.parentElement);
  }

  if ("IntersectionObserver" in window && canvas.parentElement) {
    var io = new IntersectionObserver(onVis, { root: null, threshold: 0.05 });
    io.observe(canvas.parentElement);
  }
})();
