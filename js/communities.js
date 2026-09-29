/* =========================================================================
   Licter — community map (home hero frame)

   Drawn after Licter's own network maps: a dark ground, a handful of
   communities, each a bright hub with hundreds of accounts around it, tied to
   it by curved links that swirl in one direction. Where two communities
   overlap their colours mix. A few small grey groups sit on the edge.

   Cost: every community is rendered once into its own offscreen canvas.
   A frame only redraws those canvases (each swaying a little around its hub),
   the hub glows, and a few hundred signals travelling in to the hubs.
   Nothing runs while the frame is off screen or the tab is hidden.
   ========================================================================= */
(function () {
  "use strict";

  /* The renderer is a factory: the hero uses it, and so does the audiences
     use case, each with its own communities.
       opts.communities  [{x, y, r, n, color, swirl, platform?, cap?}]
       opts.outliers     grey constellations on the edge
       opts.stories      open the platform window on hover (hero)
       opts.labels       a name per community, shown beside its hub
       opts.onHover(i) / opts.onSelect(i), and .select(i) for a lasting highlight */
  function LicterMap(host, opts) {
  if (!host || !document.createElement("canvas").getContext) return null;
  opts = opts || {};
  var selected = -1, alive = true, observers = [];
  /* opts.grow: the communities form one after the other, each spreading out
     from its hub, instead of being there from the first frame */
  var bornAt = 0, GROW_STEP = 650, GROW_DUR = 1500, shownLabels = [];
  function growth(i, now) {
    if (!opts.grow || reduced.matches) return 1;
    var k = (now - bornAt - i * GROW_STEP) / GROW_DUR;
    k = Math.max(0, Math.min(1, k));
    return 1 - Math.pow(1 - k, 3);
  }

  var canvas = document.createElement("canvas");
  canvas.className = "communities";
  host.appendChild(canvas);
  var ctx = canvas.getContext("2d");

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ------------------------------------------------------------ the map
     x, y and r are fractions of the frame (r of its smaller side).
     n is the number of accounts, swirl the direction and strength of the
     curve on the links. The largest community carries the brand amber. */
  var COMMUNITIES = opts.communities || [
    { x: 0.27, y: 0.47, r: 0.34, n: 1300, color: "#F4A93B", swirl:  0.55, platform: "TIKTOK",    cap: "Reel · 14 min" },
    { x: 0.45, y: 0.17, r: 0.25, n: 800, color: "#E2468D", swirl: -0.6,  platform: "INSTAGRAM", cap: "Story · 2 h" },
    { x: 0.55, y: 0.38, r: 0.26, n: 900, color: "#D796E6", swirl:  0.5,  platform: "TWITCH",    cap: "Live · 2 h" },
    { x: 0.66, y: 0.20, r: 0.20, n: 620, color: "#3CC2A6", swirl:  0.55, platform: "YOUTUBE",   cap: "Video · 1 h" },
    { x: 0.78, y: 0.42, r: 0.25, n: 820, color: "#4292F2", swirl: -0.5,  platform: "LINKEDIN",  cap: "Post · 3 h" },
    { x: 0.43, y: 0.75, r: 0.26, n: 920, color: "#7B6CF2", swirl:  0.6,  platform: "X",         cap: "Post · 22 min" },
    { x: 0.52, y: 0.64, r: 0.12, n: 300, color: "#8D7DF5", swirl: -0.5,  platform: "FACEBOOK",  cap: "Post · 5 h" },
    { x: 0.66, y: 0.74, r: 0.24, n: 760, color: "#C6D64A", swirl:  0.5,  platform: "TIKTOK",    cap: "Reel · 1 h" },
    { x: 0.2, y: 0.26, r: 0.10, n: 380, color: "#F2656F", swirl: -0.7,  platform: "YOUTUBE",   cap: "Short · 40 min" }
  ];
  /* small groups on the edge, drawn as grey constellations */
  var OUTLIERS = opts.outliers || [
    { x: 0.14, y: 0.37, r: 0.05, n: 14 }, { x: 0.23, y: 0.12, r: 0.045, n: 12 },
    { x: 0.15, y: 0.66, r: 0.05, n: 14 }, { x: 0.22, y: 0.82, r: 0.06, n: 16 },
    { x: 0.83, y: 0.70, r: 0.05, n: 14 }, { x: 0.80, y: 0.14, r: 0.05, n: 12 },
    { x: 0.88, y: 0.83, r: 0.05, n: 12 }
  ];

  /* ------------------------------------------------------------ helpers */
  var seed = 20260929;
  function rnd() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
  function rgba(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + (n >> 16 & 255) + "," + (n >> 8 & 255) + "," + (n & 255) + "," + a + ")";
  }
  function mix(hex, t) { /* toward white */
    var n = parseInt(hex.slice(1), 16);
    var r = n >> 16 & 255, g = n >> 8 & 255, b = n & 255;
    return "#" + [r, g, b].map(function (c) {
      var v = Math.round(c + (255 - c) * t).toString(16);
      return v.length < 2 ? "0" + v : v;
    }).join("");
  }
  /* On the dark ground the map is drawn with additive light; on the cream
     ground (light theme, no frame) it is drawn like ink: normal blending,
     colours pulled a little toward navy, navy hubs instead of white ones. */
  var LIGHT = true;
  function isLight() { return document.documentElement.getAttribute("data-theme") !== "dark"; }
  function toward(hex, target, t) {
    var a = parseInt(hex.slice(1), 16), b = parseInt(target.slice(1), 16);
    return "#" + [16, 8, 0].map(function (sh) {
      var v = Math.round((a >> sh & 255) + ((b >> sh & 255) - (a >> sh & 255)) * t).toString(16);
      return v.length < 2 ? "0" + v : v;
    }).join("");
  }
  function tone(hex) { return LIGHT ? toward(hex, "#13162D", 0.18) : hex; }
  function BLEND() { return LIGHT ? "source-over" : "lighter"; }

  /* point on the quadratic curve hub -> node, bent by the community's swirl */
  function curve(hx, hy, nx, ny, swirl) {
    var mx = (hx + nx) / 2, my = (hy + ny) / 2;
    var dx = nx - hx, dy = ny - hy;
    return { cx: mx - dy * swirl * 0.9, cy: my + dx * swirl * 0.9 };
  }
  function bez(p0, c, p1, t) {
    var u = 1 - t;
    return u * u * p0 + 2 * u * t * c + t * t * p1;
  }

  /* ------------------------------------------------------------ build */
  var W = 0, H = 0, S = 0, dpr = 1;
  var labelBox = null;
  if (opts.labels) { labelBox = document.createElement("div"); labelBox.className = "map-labels"; host.appendChild(labelBox); }
  var layers = [];      /* one per community: offscreen canvas + geometry */
  var base = null;      /* outliers and the links between communities */
  var signals = [];

  function build() {
    seed = 20260929;
    LIGHT = isLight();
    W = Math.max(1, host.clientWidth);
    H = Math.max(1, host.clientHeight);
    S = Math.min(W, H);
    dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    /* smaller frames get fewer accounts, not smaller dots */
    var density = Math.max(0.45, Math.min(1, (W * H) / (640 * 480)));

    layers = COMMUNITIES.map(function (c) {
      var hx = c.x * W, hy = c.y * H, R = c.r * S * 1.25;
      var pad = R * 0.35;
      var size = Math.ceil((R + pad) * 2);
      var off = document.createElement("canvas");
      off.width = Math.round(size * dpr);
      off.height = Math.round(size * dpr);
      var o = off.getContext("2d");
      o.scale(dpr, dpr);
      o.globalCompositeOperation = BLEND();
      var col = tone(c.color);
      var ox = size / 2, oy = size / 2;       /* hub, in the layer */
      var nodes = [];
      var n = Math.round(c.n * density);

      for (var i = 0; i < n; i++) {
        /* denser near the hub, a soft ragged rim */
        var d = R * (0.08 + 0.92 * Math.pow(rnd(), 0.75)) * (0.92 + rnd() * 0.2);
        var a = rnd() * Math.PI * 2;
        var nx = ox + Math.cos(a) * d, ny = oy + Math.sin(a) * d * 0.92;
        var cv = curve(ox, oy, nx, ny, c.swirl * (0.7 + rnd() * 0.6));
        nodes.push({ x: nx, y: ny, cx: cv.cx, cy: cv.cy });

        /* the link: brighter near the hub, fading outward */
        var grad = o.createLinearGradient(ox, oy, nx, ny);
        grad.addColorStop(0, rgba(col, LIGHT ? 0.05 : 0.03));
        grad.addColorStop(0.25, rgba(col, LIGHT ? 0.22 : 0.16));
        grad.addColorStop(1, rgba(col, LIGHT ? 0.1 : 0.07));
        o.strokeStyle = grad;
        o.lineWidth = 0.45;
        o.beginPath();
        o.moveTo(ox, oy);
        o.quadraticCurveTo(cv.cx, cv.cy, nx, ny);
        o.stroke();
      }
      /* the accounts */
      for (var k = 0; k < nodes.length; k++) {
        var p = nodes[k];
        var big = rnd() < 0.04;
        o.fillStyle = rnd() < 0.2
          ? (LIGHT ? rgba(toward(c.color, "#13162D", 0.45), 0.85) : rgba(mix(c.color, 0.55), 0.9))
          : rgba(col, LIGHT ? 0.75 : 0.8);
        o.beginPath();
        o.arc(p.x, p.y, big ? 1.3 : 0.45 + rnd() * 0.5, 0, Math.PI * 2);
        o.fill();
      }
      /* the hub's own glow is animated; the soft core here is static */
      var g = o.createRadialGradient(ox, oy, 0, ox, oy, R * 0.4);
      g.addColorStop(0, rgba(col, LIGHT ? 0.08 : 0.1));
      g.addColorStop(1, rgba(col, 0));
      o.fillStyle = g;
      o.beginPath(); o.arc(ox, oy, R * 0.45, 0, Math.PI * 2); o.fill();

      return { c: c, off: off, size: size, hx: hx, hy: hy, ox: ox, oy: oy, R: R, nodes: nodes,
               phase: rnd() * Math.PI * 2, glow: 0 };
    });

    /* base layer: grey outlier constellations, and faint links between
       communities so the map reads as one network */
    base = document.createElement("canvas");
    base.width = canvas.width; base.height = canvas.height;
    var b = base.getContext("2d");
    b.scale(dpr, dpr);
    b.globalCompositeOperation = BLEND();
    OUTLIERS.forEach(function (g) {
      var cx = g.x * W, cy = g.y * H, R = g.r * S * 1.2, pts = [];
      for (var i = 0; i < g.n; i++) {
        var a = rnd() * Math.PI * 2, d = R * Math.sqrt(rnd());
        pts.push([cx + Math.cos(a) * d, cy + Math.sin(a) * d]);
      }
      b.strokeStyle = LIGHT ? "rgba(19,22,45,0.18)" : "rgba(220,224,235,0.16)";
      b.lineWidth = 0.6;
      for (var p = 0; p < pts.length; p++) {
        for (var q = p + 1; q < pts.length; q++) {
          if (rnd() < 0.3) { b.beginPath(); b.moveTo(pts[p][0], pts[p][1]); b.lineTo(pts[q][0], pts[q][1]); b.stroke(); }
        }
      }
      b.fillStyle = LIGHT ? "rgba(19,22,45,0.5)" : "rgba(230,232,240,0.7)";
      pts.forEach(function (pt) { b.beginPath(); b.arc(pt[0], pt[1], 0.9, 0, Math.PI * 2); b.fill(); });
      b.fillStyle = LIGHT ? "rgba(19,22,45,0.85)" : "rgba(255,255,255,0.9)";
      b.beginPath(); b.arc(cx, cy, 1.6, 0, Math.PI * 2); b.fill();
    });
    for (var i = 0; i < layers.length; i++) {
      for (var j = i + 1; j < layers.length; j++) {
        var A = layers[i], B = layers[j];
        var dist = Math.hypot(A.hx - B.hx, A.hy - B.hy);
        var links = Math.round(Math.max(0, 70 - dist / (S * 0.012)) * density);
        for (var k = 0; k < links; k++) {
          var na = A.nodes[(rnd() * A.nodes.length) | 0], nb = B.nodes[(rnd() * B.nodes.length) | 0];
          var ax = A.hx + na.x - A.ox, ay = A.hy + na.y - A.oy;
          var bx = B.hx + nb.x - B.ox, by = B.hy + nb.y - B.oy;
          var grad = b.createLinearGradient(ax, ay, bx, by);
          grad.addColorStop(0, rgba(tone(A.c.color), LIGHT ? 0.12 : 0.09));
          grad.addColorStop(1, rgba(tone(B.c.color), LIGHT ? 0.12 : 0.09));
          b.strokeStyle = grad; b.lineWidth = 0.5;
          var cv = curve(ax, ay, bx, by, 0.25);
          b.beginPath(); b.moveTo(ax, ay); b.quadraticCurveTo(cv.cx, cv.cy, bx, by); b.stroke();
        }
      }
    }

    /* names beside the hubs, as text so they stay crisp and translatable */
    if (labelBox) {
      labelBox.innerHTML = "";
      layers.forEach(function (L, i) {
        if (!opts.labels || !opts.labels[i]) return;
        var el = document.createElement("span");
        el.className = "map-label" + (opts.grow && !reduced.matches && !shownLabels[i] ? "" : " is-shown");
        el.style.top = (L.hy + 12) + "px";
        el.style.setProperty("--c", L.c.color);
        el.textContent = opts.labels[i];
        labelBox.appendChild(el);
        /* kept inside the frame, even for a hub near the edge */
        var half = el.offsetWidth / 2 + 6;
        el.style.left = Math.max(half, Math.min(W - half, L.hx)) + "px";
      });
    }

    /* signals: a bright point running down a link to its hub */
    signals = [];
    var count = Math.round(180 * density);
    for (var s = 0; s < count; s++) signals.push(newSignal(true));
  }

  function newSignal(anywhere) {
    var L = layers[(rnd() * layers.length) | 0];
    var node = L.nodes[(rnd() * L.nodes.length) | 0];
    return { L: L, n: node, t: anywhere ? rnd() : 0, speed: 0.18 + rnd() * 0.3 };
  }

  /* ------------------------------------------------------------ pointer
     The community under the pointer lights up; the others step back. */
  var hover = -1;

  /* the same window the old map opened on its travellers: platform, a media
     slot, a caption, and a thread back to the hub it belongs to */
  var cards = document.createElement("div");
  cards.className = "stories";
  host.appendChild(cards);
  var card = null;

  function closeCard() {
    if (!card) return;
    var old = card; card = null;
    old.classList.add("is-out");
    setTimeout(function () { old.remove(); }, 400);
  }
  function openCard(i) {
    closeCard();
    if (i < 0 || !opts.stories) return;
    var L = layers[i], c = L.c, CW = 216, CH = 190;
    var el = document.createElement("figure");
    el.className = "story";
    el.style.setProperty("--story-color", c.color);
    el.style.setProperty("--hold", "4200ms");
    el.innerHTML =
      '<span class="story__bar"><i></i></span>' +
      '<span class="story__head">' + ((window.LicterIcons || {})[c.platform] || "") + c.platform + "</span>" +
      '<span class="story__media"><span class="story__play" aria-hidden="true">▶</span></span>' +
      '<figcaption class="story__cap">' + c.cap + "</figcaption>";
    var x = L.hx + 34;
    if (x + CW + 10 > W) { x = L.hx - 34 - CW; el.classList.add("story--left"); }
    el.style.left = Math.round(Math.max(10, x)) + "px";
    el.style.top = Math.round(Math.max(10, Math.min(H - CH - 10, L.hy - CH / 2))) + "px";
    cards.appendChild(el);
    card = el;
  }
  function setHover(i) {
    if (i === hover) return;
    hover = i;
    openCard(i);
    if (labelBox) Array.prototype.forEach.call(labelBox.children, function (el, k) { el.classList.toggle("is-on", k === focusIndex()); });
    if (opts.onHover) opts.onHover(i);
  }
  /* the community in focus: under the pointer, else the selected one */
  function focusIndex() { return hover >= 0 ? hover : selected; }

  function onMove(e) {
    var r = host.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    var best = -1, bestD = Infinity;
    layers.forEach(function (L, i) {
      var d = Math.hypot(x - L.hx, y - L.hy) / L.R;
      if (d < 0.8 && d < bestD) { best = i; bestD = d; }
    });
    setHover(best);
  }
  function onLeave() { setHover(-1); }
  function onClick() { if (hover >= 0 && opts.onSelect) opts.onSelect(hover); }
  host.addEventListener("pointermove", onMove);
  host.addEventListener("pointerleave", onLeave);
  host.addEventListener("click", onClick);

  /* ------------------------------------------------------------ frame */
  var running = false, last = 0;

  function draw(now) {
    var t = now / 1000;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.clearRect(0, 0, W, H);
    var gAll = opts.grow ? growth(layers.length - 1, now) : 1;
    ctx.globalAlpha = gAll;
    ctx.drawImage(base, 0, 0, W, H);
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = BLEND();

    for (var i = 0; i < layers.length; i++) {
      var L = layers[i];
      var f = focusIndex();
      L.glow += ((f === i ? 1 : 0) - L.glow) * 0.08;
      var dim = f >= 0 && f !== i ? 0.4 : 1;
      var sway = reduced.matches ? 0 : Math.sin(t * 0.25 + L.phase) * 0.05;
      var gr = growth(i, now);
      L.gr = gr;
      if (labelBox && labelBox.children[i] && (gr > 0.55) !== !!shownLabels[i]) {
        shownLabels[i] = gr > 0.55;
        labelBox.children[i].classList.toggle("is-shown", shownLabels[i]);
      }
      if (gr <= 0) continue;
      ctx.save();
      ctx.globalAlpha = dim * gr;
      ctx.translate(L.hx, L.hy);
      ctx.rotate(sway + (1 - gr) * 0.6);
      if (gr < 1) { var sc = 0.2 + 0.8 * gr; ctx.scale(sc, sc); }
      ctx.drawImage(L.off, -L.ox, -L.oy, L.size, L.size);
      if (L.glow > 0.02) { ctx.globalAlpha = L.glow * 0.6; ctx.drawImage(L.off, -L.ox, -L.oy, L.size, L.size); }
      ctx.restore();
      L.sway = sway;

      /* the hub: a white core in a pulsing halo of its colour */
      var pulse = reduced.matches ? 1 : 1 + 0.25 * Math.sin(t * 1.4 + L.phase);
      var hr = (2 + L.R * 0.012) * (1 + L.glow * 0.3);
      var halo = hr * (4 + 1.5 * pulse);
      var g = ctx.createRadialGradient(L.hx, L.hy, 0, L.hx, L.hy, halo);
      g.addColorStop(0, rgba(tone(L.c.color), (LIGHT ? 0.45 : 0.35) * dim));
      g.addColorStop(1, rgba(tone(L.c.color), 0));
      ctx.globalAlpha = Math.min(1, gr * 1.6);
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(L.hx, L.hy, halo, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = LIGHT ? "rgba(19,22,45," + (0.9 * dim) + ")" : "rgba(255,255,255," + (0.95 * dim) + ")";
      ctx.beginPath(); ctx.arc(L.hx, L.hy, hr, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = 1;
    }

    /* signals travelling in to their hub */
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
    last = now;
    for (var s = 0; s < signals.length; s++) {
      var sg = signals[s], L2 = sg.L;
      if (L2.gr !== undefined && L2.gr < 1) continue;
      if (!reduced.matches) sg.t += dt * sg.speed;
      if (sg.t >= 1) { signals[s] = newSignal(false); continue; }
      var u = 1 - sg.t; /* 1 at the account, 0 at the hub */
      var lx = bez(L2.ox, sg.n.cx, sg.n.x, u) - L2.ox;
      var ly = bez(L2.oy, sg.n.cy, sg.n.y, u) - L2.oy;
      var cs = Math.cos(L2.sway || 0), sn = Math.sin(L2.sway || 0);
      var px = L2.hx + lx * cs - ly * sn, py = L2.hy + lx * sn + ly * cs;
      var fade = Math.sin(Math.PI * sg.t);
      var fS = focusIndex(), dimS = fS >= 0 && fS !== layers.indexOf(L2) ? 0.35 : 1;
      ctx.fillStyle = LIGHT ? rgba(toward(L2.c.color, "#13162D", 0.35), 0.9 * fade * dimS) : rgba(mix(L2.c.color, 0.55), 0.9 * fade * dimS);
      ctx.beginPath(); ctx.arc(px, py, 1.1, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalCompositeOperation = "source-over";
  }

  function loop(now) {
    if (!running || !alive) return;
    draw(now);
    requestAnimationFrame(loop);
  }
  function start() {
    if (running || reduced.matches) return;
    running = true; last = 0;
    requestAnimationFrame(loop);
  }
  function stop() { running = false; }

  function init() {
    bornAt = performance.now();
    build();
    draw(performance.now());
    if (!reduced.matches) start();
  }

  /* only while visible */
  var visible = true;
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (e) {
      visible = e[0].isIntersecting;
      if (visible && !document.hidden) start(); else stop();
    });
    io.observe(host); observers.push(io);
  }
  function onVis() { if (document.hidden) stop(); else if (visible) start(); }
  document.addEventListener("visibilitychange", onVis);

  if (window.MutationObserver) {
    var mo = new MutationObserver(function () {
      if (isLight() === LIGHT) return;
      setHover(-1); build(); draw(performance.now());
    });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    observers.push(mo);
  }

  var t0 = null;
  function rebuild() { clearTimeout(t0); t0 = setTimeout(function () { setHover(-1); build(); draw(performance.now()); }, 150); }
  if (window.ResizeObserver) { var ro = new ResizeObserver(rebuild); ro.observe(host); observers.push(ro); }
  else window.addEventListener("resize", rebuild);

  init();

  return {
    select: function (i) {
      selected = i;
      if (labelBox) Array.prototype.forEach.call(labelBox.children, function (el, k) { el.classList.toggle("is-on", k === focusIndex()); });
      if (!running) draw(performance.now());
    },
    destroy: function () {
      alive = false; stop(); clearTimeout(t0);
      observers.forEach(function (o) { o.disconnect(); });
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("resize", rebuild);
      host.removeEventListener("pointermove", onMove);
      host.removeEventListener("pointerleave", onLeave);
      host.removeEventListener("click", onClick);
      canvas.remove(); cards.remove(); if (labelBox) labelBox.remove();
    }
  };
  }

  window.LicterMap = LicterMap;

  /* the hero */
  var hero = document.getElementById("carto-frame");
  if (hero) LicterMap(hero, { stories: true });
})();
