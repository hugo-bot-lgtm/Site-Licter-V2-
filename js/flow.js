/* =========================================================================
   Licter — gateway flow.

   Where the cartography stops, this takes over: paths entering from both
   edges and bending into a single point at the centre of the screen, with a
   signal travelling along each one. It says the same thing the map said, with
   fewer marks — everything converges on one reading.

   Two layers, like the map: the paths are drawn once into an offscreen canvas
   and blitted every frame, and only the travelling points are redrawn. The
   source component restrokes eighty dashed beziers per frame; on a page that
   already runs a canvas in the hero that is a lot of paint for a backdrop
   nobody is meant to look at.
   ========================================================================= */
(function () {
  "use strict";

  var canvas = document.getElementById("flow");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");

  /* The source draws white on black. Here the navy carries the path and the
     deep amber carries the point: the two inks the charter already uses for
     "a signal on its way". Pure amber disappears on the cream. */
  var LINE = "19, 22, 45";
  var DOT = "192, 140, 14";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  var view = { w: 0, h: 0, dpr: 1 };
  var paths = [];
  var still = null, sctx = null;
  var running = false, raf = null;

  function measure() {
    /* clientWidth, not innerWidth: the scrollbar counts, and sizing past it
       hands the document a horizontal scroll */
    view.w = Math.max(1, document.documentElement.clientWidth || window.innerWidth);
    view.h = Math.max(1, window.innerHeight);
    view.dpr = Math.min(2, window.devicePixelRatio || 1);

    canvas.width = Math.round(view.w * view.dpr);
    canvas.height = Math.round(view.h * view.dpr);
    canvas.style.width = view.w + "px";
    canvas.style.height = view.h + "px";
    /* setTransform rather than scale: scale() multiplies the transform still
       in place, so every resize would compound it */
    ctx.setTransform(view.dpr, 0, 0, view.dpr, 0, 0);
  }

  function bezier(t, p0, p1, p2, p3) {
    var u = 1 - t, u2 = u * u, t2 = t * t;
    return {
      x: u2 * u * p0.x + 3 * u2 * t * p1.x + 3 * u * t2 * p2.x + t2 * t * p3.x,
      y: u2 * u * p0.y + 3 * u2 * t * p1.y + 3 * u * t2 * p2.y + t2 * t * p3.y
    };
  }

  function anchors(p) {
    var w = view.w, cx = w / 2, cy = view.h / 2;
    return [
      { x: p.isLeft ? 0 : w, y: p.startY },
      { x: p.isLeft ? cx * 0.5 : w - cx * 0.5, y: p.startY },
      { x: p.isLeft ? cx * 0.8 : w - cx * 0.8, y: cy },
      { x: cx, y: cy }
    ];
  }

  function build() {
    measure();

    /* Eighty paths on a black screen read as a beam. On the cream they read as
       hatching, so the count follows the width: a dozen on a phone, forty on a
       desktop. */
    var n = Math.max(12, Math.min(44, Math.round(view.w / 30)));
    paths = [];
    for (var i = 0; i < n; i++) {
      paths.push({
        isLeft: i % 2 === 0,
        startY: (i / n) * view.h * 1.4 - view.h * 0.2,
        t: i / n,
        speed: 0.0009 + (i % 7) * 0.00013
      });
    }

    renderPaths();
  }

  function renderPaths() {
    if (!still) still = document.createElement("canvas");
    still.width = canvas.width;
    still.height = canvas.height;
    sctx = still.getContext("2d");
    sctx.setTransform(view.dpr, 0, 0, view.dpr, 0, 0);
    sctx.clearRect(0, 0, view.w, view.h);
    sctx.lineWidth = 1;
    /* the source's [1, 4] at this scale reads as a grey line; opened up, the
       path stays a series of marks rather than a rule */
    sctx.setLineDash([1, 5]);

    var cx = view.w / 2, cy = view.h / 2;
    for (var i = 0; i < paths.length; i++) {
      var a = anchors(paths[i]);
      /* The paths all end on the same point. Left solid, that junction becomes
         a dark star in the middle of the page, so each one fades out before it
         arrives and the convergence is implied rather than drawn. */
      var g = sctx.createLinearGradient(a[0].x, a[0].y, cx, cy);
      g.addColorStop(0, "rgba(" + LINE + ", .24)");
      g.addColorStop(0.62, "rgba(" + LINE + ", .15)");
      g.addColorStop(1, "rgba(" + LINE + ", 0)");
      sctx.strokeStyle = g;
      sctx.beginPath();
      sctx.moveTo(a[0].x, a[0].y);
      sctx.bezierCurveTo(a[1].x, a[1].y, a[2].x, a[2].y, a[3].x, a[3].y);
      sctx.stroke();
    }
    sctx.setLineDash([]);
  }

  function frame(now) {
    raf = null;
    if (!running) return;

    ctx.clearRect(0, 0, view.w, view.h);
    ctx.drawImage(still, 0, 0, view.w, view.h);

    for (var i = 0; i < paths.length; i++) {
      var p = paths[i];
      p.t += p.speed;
      if (p.t > 1) p.t -= 1;

      var a = anchors(p);
      var pos = bezier(p.t, a[0], a[1], a[2], a[3]);
      /* in at the edge, out before the centre: the point is read and gone,
         and forty of them never pile up on the same pixel */
      var alpha = Math.min(1, p.t / 0.08) * Math.min(1, (1 - p.t) / 0.36);
      /* the point is the brightest mark on a pale page, so it carries much
         further than its size suggests: at .95 it read as sitting on top of
         the site rather than behind it */
      ctx.fillStyle = "rgba(" + DOT + ", " + (alpha * 0.38).toFixed(3) + ")";
      ctx.fillRect(pos.x - 1.5, pos.y - 1.5, 3, 3);
    }

    raf = requestAnimationFrame(frame);
  }

  function paintStill() {
    ctx.clearRect(0, 0, view.w, view.h);
    ctx.drawImage(still, 0, 0, view.w, view.h);
  }

  function start() {
    if (running) return;
    if (reduced.matches) { paintStill(); return; }
    running = true;
    if (!raf) raf = requestAnimationFrame(frame);
  }

  function stop() {
    running = false;
    if (raf) { cancelAnimationFrame(raf); raf = null; }
  }

  build();
  paintStill();

  /* The map owns the hero and this owns everything under it. js/ui.js crosses
     them on scroll and stops whichever one is out of sight, so there is never
     more than one canvas painting. */
  window.LicterFlow = {
    setActive: function (on) { if (on) start(); else stop(); }
  };

  var resizeTimer = null;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var wasRunning = running;
      stop();
      build();
      if (wasRunning) start(); else paintStill();
    }, 160);
  }, { passive: true });

  /* a scrollbar appearing narrows the page without firing a resize */
  function refit() {
    var w = document.documentElement.clientWidth || window.innerWidth;
    if (Math.abs(w - view.w) > 1) {
      var wasRunning = running;
      stop();
      build();
      if (wasRunning) start(); else paintStill();
    }
  }
  window.addEventListener("load", function () { setTimeout(refit, 60); });
  setTimeout(refit, 400);
  setTimeout(refit, 1400);

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop();
    else if (parseFloat(canvas.style.opacity || "0") > 0) start();
  });

  reduced.addEventListener("change", function () {
    stop();
    build();
    paintStill();
    if (!reduced.matches && parseFloat(canvas.style.opacity || "0") > 0) start();
  });
})();
