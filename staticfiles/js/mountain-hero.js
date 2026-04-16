(function () {
  var canvas = document.getElementById("mountain-canvas");
  if (!canvas) return;
  var ctx, W, H;

  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    W = rect.width;
    H = rect.height;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
  }

  resize();
  window.addEventListener("resize", function () {
    resize();
  });

  var t = 0;
  var CYCLE = 520;
  var confetti = [];

  function easeInOut(t0) {
    return t0 < 0.5 ? 2 * t0 * t0 : -1 + (4 - 2 * t0) * t0;
  }
  function lerp(a, b, t0) {
    return a + (b - a) * t0;
  }
  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }

  function getPct(start, end) {
    var f = t % CYCLE;
    if (f < start) return 0;
    if (f > end) return 1;
    return easeInOut((f - start) / (end - start));
  }

  function drawSky() {
    var f = t % CYCLE;
    var sunBright = getPct(280, 420);
    var sunY = lerp(H * 0.1, H * 0.08, sunBright);
    var sunAlpha = lerp(0.15, 0.42, sunBright);

    var grd = ctx.createRadialGradient(W * 0.85, sunY, 0, W * 0.85, sunY, 80);
    grd.addColorStop(0, "rgba(255,215,0," + sunAlpha + ")");
    grd.addColorStop(1, "rgba(255,215,0,0)");
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.arc(W * 0.85, sunY, 80, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "rgba(255,200,0," + sunAlpha * 0.6 + ")";
    ctx.beginPath();
    ctx.arc(W * 0.85, sunY, 18, 0, Math.PI * 2);
    ctx.fill();

    for (var i = 0; i < 6; i++) {
      var angle = (i / 6) * Math.PI * 2 + f * 0.01;
      ctx.strokeStyle = "rgba(255,215,0," + sunAlpha * 0.35 + ")";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(W * 0.85 + Math.cos(angle) * 22, sunY + Math.sin(angle) * 22);
      ctx.lineTo(W * 0.85 + Math.cos(angle) * 32, sunY + Math.sin(angle) * 32);
      ctx.stroke();
    }

    var cOff = (f * 0.08) % 40;
    ctx.fillStyle = "rgba(176,190,197,0.18)";
    ctx.beginPath();
    ctx.ellipse(W * 0.15 - cOff, H * 0.12, 30, 12, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(W * 0.23 - cOff, H * 0.1, 22, 9, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "rgba(176,190,197,0.12)";
    ctx.beginPath();
    ctx.ellipse(W * 0.5 - cOff * 0.5, H * 0.16, 25, 10, 0, 0, Math.PI * 2);
    ctx.fill();

    var rainAlpha = 1 - getPct(60, 180);
    if (rainAlpha > 0.05) {
      for (var r = 0; r < 8; r++) {
        var rx = (W * 0.05 + r * (W * 0.1) + f * 0.4) % (W * 0.6);
        var ry = (f * 2 + r * 37) % H;
        ctx.strokeStyle = "rgba(144,202,249," + 0.32 * rainAlpha + ")";
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(rx, ry);
        ctx.lineTo(rx + 2, ry + 16);
        ctx.stroke();
      }
    }
  }

  function drawMountain() {
    var sw = W,
      sh = H;
    var mx = sw * 0.62,
      my = sh * 0.18,
      ground = sh * 0.88;

    ctx.beginPath();
    ctx.rect(0, ground, sw, sh - ground + 10);
    ctx.fillStyle = "rgba(107,158,108,0.18)";
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(sw * 0.08, ground);
    ctx.lineTo(mx, my);
    ctx.lineTo(sw * 0.98, ground);
    ctx.closePath();
    ctx.fillStyle = "rgba(78,130,79,0.32)";
    ctx.fill();
    ctx.strokeStyle = "rgba(90,145,91,0.2)";
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-10, ground);
    ctx.lineTo(mx * 0.38, my * 1.3);
    ctx.lineTo(mx * 0.82, ground);
    ctx.closePath();
    ctx.fillStyle = "rgba(60,100,61,0.2)";
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(mx * 1.1, ground);
    ctx.lineTo(mx * 1.5, my * 1.22);
    ctx.lineTo(sw + 10, ground);
    ctx.closePath();
    ctx.fillStyle = "rgba(60,100,61,0.18)";
    ctx.fill();

    ctx.beginPath();
    ctx.ellipse(mx, my + 8, 18, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255,255,255,0.28)";
    ctx.fill();
  }

  function drawPerson(px, py, phase) {
    var f = t % CYCLE;
    ctx.save();
    ctx.translate(px, py);

    var col = "rgba(84,110,122,0.75)";
    if (phase === "climbing") col = "rgba(100,180,100,0.85)";
    if (phase === "summit" || phase === "flag" || phase === "celebrate") col = "rgba(255,200,0,0.92)";

    ctx.strokeStyle = col;
    ctx.fillStyle = col;
    ctx.lineWidth = 2;
    ctx.lineCap = "round";

    var bob =
      phase === "struggling" ? Math.sin(f * 0.12) * 4 : phase === "climbing" ? Math.sin(f * 0.3) * 2 : 0;

    ctx.beginPath();
    ctx.arc(0, -18 + bob * 0.3, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(0, -13 + bob * 0.3);
    ctx.lineTo(0, 2);
    ctx.stroke();

    if (phase === "struggling") {
      var sw2 = Math.sin(f * 0.1) * 12;
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(-8 + sw2 * 0.5, 4);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(8 - sw2 * 0.5, 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(-6, 14 + sw2 * 0.3);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(6, 14 - sw2 * 0.3);
      ctx.stroke();
    } else if (phase === "climbing") {
      var st = Math.sin(f * 0.3) * 8;
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(-9, 2 + st * 0.3);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(7, 3 - st * 0.3);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(-7, 14 + st * 0.4);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(5, 12 - st * 0.4);
      ctx.stroke();
    } else if (phase === "summit") {
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(-8, -2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(8, -2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(-5, 13);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(5, 13);
      ctx.stroke();
    } else if (phase === "flag") {
      var raisePct = getPct(360, 430);
      var armY = lerp(-2, -16, raisePct);

      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(10, armY);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(-7, 0);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(-5, 13);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(5, 13);
      ctx.stroke();

      ctx.strokeStyle = "#B8860B";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(10, armY);
      ctx.lineTo(10, armY - 22);
      ctx.stroke();

      var wv = Math.sin(f * 0.25) * 3;
      ctx.fillStyle = "#FFD700";
      ctx.beginPath();
      ctx.moveTo(10, armY - 22);
      ctx.quadraticCurveTo(20, armY - 25 + wv, 28, armY - 22 + wv * 0.5);
      ctx.lineTo(28, armY - 14 + wv * 0.5);
      ctx.quadraticCurveTo(20, armY - 11 + wv, 10, armY - 14);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = "rgba(255,255,255,0.25)";
      ctx.beginPath();
      ctx.moveTo(10, armY - 22);
      ctx.quadraticCurveTo(16, armY - 24 + wv, 22, armY - 22 + wv * 0.3);
      ctx.lineTo(22, armY - 18 + wv * 0.3);
      ctx.quadraticCurveTo(16, armY - 16 + wv, 10, armY - 18);
      ctx.closePath();
      ctx.fill();
    } else if (phase === "celebrate") {
      var cel = Math.sin(f * 0.3) * 10;
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(-12, -8 + cel * 0.5);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(12, -8 - cel * 0.5);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(-5, 13);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, 2);
      ctx.lineTo(5, 13);
      ctx.stroke();

      ctx.strokeStyle = "#B8860B";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(12, -8 - cel * 0.5);
      ctx.lineTo(12, -30 - cel * 0.5);
      ctx.stroke();

      var wv2 = Math.sin(f * 0.25) * 5;
      ctx.fillStyle = "#FFD700";
      ctx.beginPath();
      ctx.moveTo(12, -30 - cel * 0.5);
      ctx.quadraticCurveTo(24, -34 - cel * 0.5 + wv2, 34, -30 - cel * 0.5 + wv2 * 0.5);
      ctx.lineTo(34, -20 - cel * 0.5 + wv2 * 0.5);
      ctx.quadraticCurveTo(24, -16 - cel * 0.5 + wv2, 12, -20 - cel * 0.5);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = "rgba(255,255,255,0.25)";
      ctx.beginPath();
      ctx.moveTo(12, -30 - cel * 0.5);
      ctx.quadraticCurveTo(20, -33 - cel * 0.5 + wv2, 28, -30 - cel * 0.5 + wv2 * 0.3);
      ctx.lineTo(28, -24 - cel * 0.5 + wv2 * 0.3);
      ctx.quadraticCurveTo(20, -21 - cel * 0.5 + wv2, 12, -24 - cel * 0.5);
      ctx.closePath();
      ctx.fill();
    }

    ctx.restore();
  }

  function drawConfetti() {
    var colors = ["#FFD700", "#68D391", "#7F77DD", "#EF9F27", "#ffffff", "#F06292"];
    for (var i = 0; i < confetti.length; i++) {
      var c = confetti[i];
      c.y += c.vy;
      c.x += c.vx;
      c.rot += c.rotV;
      c.life -= 0.013;
      if (c.life <= 0) {
        confetti.splice(i, 1);
        i--;
        continue;
      }
      ctx.save();
      ctx.globalAlpha = c.life;
      ctx.translate(c.x, c.y);
      ctx.rotate(c.rot);
      ctx.fillStyle = c.col;
      ctx.fillRect(-4, -4, 8, 8);
      ctx.restore();
    }
  }

  function drawCrowd(alpha) {
    if (alpha <= 0) return;
    var cols = [
      "rgba(255,200,0,",
      "rgba(104,211,145,",
      "rgba(127,119,221,",
      "rgba(239,159,39,",
    ];
    for (var i = 0; i < 6; i++) {
      var cx = W * 0.08 + i * (W * 0.15);
      var cy = H * 0.88;
      var bob2 = Math.sin(t * 0.08 + i * 1.2) * 5 * alpha;
      ctx.fillStyle = cols[i % cols.length] + 0.35 * alpha + ")";
      ctx.beginPath();
      ctx.arc(cx, cy - bob2 - 8, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillRect(cx - 5, cy - bob2, 10, 18);
    }
  }

  var labelEl = document.getElementById("stage-label");

  function frame() {
    if (!ctx || W < 1 || H < 1) {
      requestAnimationFrame(frame);
      return;
    }
    ctx.clearRect(0, 0, W, H);
    t++;

    var f = t % CYCLE;
    var mx = W * 0.62,
      my = H * 0.18,
      ground = H * 0.88;

    drawSky();
    drawMountain();

    var climbPct = clamp(getPct(80, 300), 0, 1);
    var px = lerp(W * 0.12, mx, climbPct);
    var py = lerp(ground - 20, my + 20, climbPct);

    var phase = "struggling";
    var lbl = "Struggling at the base...";
    if (f >= 440) {
      phase = "celebrate";
      lbl = "Achievement unlocked! ★";
    } else if (f >= 360) {
      phase = "flag";
      lbl = "Raising the flag!";
    } else if (f >= 300) {
      phase = "summit";
      lbl = "Reached the summit!";
    } else if (f >= 80) {
      phase = "climbing";
      lbl = "Climbing with effort...";
    }

    if (labelEl) labelEl.textContent = lbl;

    if (phase === "summit" || phase === "flag" || phase === "celebrate") {
      var glowGrd = ctx.createRadialGradient(mx, my, 0, mx, my, 70);
      glowGrd.addColorStop(0, "rgba(255,215,0,0.28)");
      glowGrd.addColorStop(1, "rgba(255,215,0,0)");
      ctx.fillStyle = glowGrd;
      ctx.beginPath();
      ctx.arc(mx, my, 70, 0, Math.PI * 2);
      ctx.fill();
    }

    if (phase === "celebrate" || phase === "flag") {
      if (Math.random() < 0.1) {
        var cols2 = ["#FFD700", "#68D391", "#7F77DD", "#EF9F27", "#fff"];
        confetti.push({
          x: W * 0.1 + Math.random() * W * 0.8,
          y: H * 0.2 + Math.random() * H * 0.3,
          vx: (Math.random() - 0.5) * 3,
          vy: Math.random() * 2 + 1,
          rot: Math.random() * Math.PI * 2,
          rotV: (Math.random() - 0.5) * 0.2,
          col: cols2[Math.floor(Math.random() * cols2.length)],
          life: 0.8 + Math.random() * 0.4,
        });
      }
    }

    drawConfetti();
    drawPerson(px, py, phase);

    var crowdAlpha = getPct(380, 460);
    drawCrowd(crowdAlpha);

    requestAnimationFrame(frame);
  }

  frame();
})();
