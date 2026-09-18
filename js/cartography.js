/* =========================================================================
   Licter — animated community cartography.

   Two layers:
     - a static layer (clusters, hubs, edges, constellations, dust) rendered
       once into an offscreen canvas and blitted every frame;
     - an animated layer (travellers, hub pulse, hover ring) redrawn per frame.

   Cluster geometry lives in a 600 x 500 design space and is scaled to the
   viewport, so nothing is frozen at the 1097 px mock width.
   ========================================================================= */
(function () {
  "use strict";

  /* Thème clair : la carto est dessinée en tons sombres sur la crème.
     L'ambre pur disparaît sur ce fond, les amas ambrés descendent donc d'un
     cran ; l'ancien amas blanc devient l'amas navy. */
  var C = {
    amber:     "#C08C0E",
    amberDeep: "#9A6F08",
    cream:     "#13162D",  /* l'amas sombre */
    grey:      "#6E7A82",
    greyLight: "#96A1A8",
    greyDark:  "#46505A",
    constell:  "#5F6A72",
    dust:      "#94A0A7"
  };

  var PLATFORMS = ["TIKTOK", "INSTAGRAM", "X", "LINKEDIN", "YOUTUBE", "FACEBOOK"];

  /* Design-space clusters (600 x 500). Two passes each: wide, then dense. */
  /* Four communities instead of five, each markedly denser: a small number of
     big poles reads as a network, where many small ones read as scatter.
     Point counts are up ~45 % on what remains. */
  var CLUSTERS = [
    { key: "core",   color: C.amber,     cx: 320, cy: 200, rx: 70, ry: 62, nWide: 92, nDense: 112 },
    { key: "amber",  color: C.amberDeep, cx: 362, cy: 300, rx: 58, ry: 64, nWide: 78, nDense: 96 },
    { key: "violet", color: C.grey,      cx: 232, cy: 270, rx: 52, ry: 46, nWide: 56, nDense: 66 },
    { key: "cream",  color: C.cream,     cx: 336, cy: 110, rx: 46, ry: 40, nWide: 44, nDense: 54 }
  ];

  /* Two satellites instead of five, kept far apart and twice the size. */
  var SATELLITES = [
    { key: "sage",  color: C.greyLight, cx: 472, cy: 288, rx: 40, ry: 36, n: 66 },
    { key: "ochre", color: C.amberDeep, cx: 256, cy: 140, rx: 38, ry: 32, n: 58 }
  ];

  /* Fixed hubs, plus one per satellite (added at build time). */
  var HUBS = [
    { key: "cream",  x: 341, y:  62 },
    { key: "violet", x: 196, y: 300 },
    { key: "amber",  x: 352, y: 372 },
    { key: "core",   x: 286, y: 152 },
    { key: "amber2", x: 432, y: 286, cluster: "amber" }
  ];

  /* Which communities are bridged to which. */
  /* Fewer communities means fewer pairs, so each pair carries more links. */
  var BRIDGES = [
    ["core", "amber"], ["core", "violet"], ["core", "cream"], ["core", "sage"],
    ["core", "ochre"], ["amber", "violet"], ["amber", "sage"], ["cream", "ochre"],
    ["violet", "chain"], ["violet", "ochre"], ["amber", "chain"]
  ];

  var CHAIN = { key: "chain", color: C.amber, x1: 52, y1: 448, x2: 210, y2: 336, n: 34 };

  var TRAVELLER_COUNT = 70;
  var BG_TRAVELLER_COUNT = 46;
  var HUB_PULSE_MS    = 2600;
  var FADE_MS         = 350;
  var HOVER_RADIUS    = 17;   /* generous hit area, per brief */
  var PARALLAX        = 0.3;  /* map drifts slower than the page */
  var STATIC_OVERSCAN = 1.32; /* static layer height = viewport * this */

  /* ---------------------------------------------------------------- utils */

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rnd = mulberry32(20260915);
  function rr(a, b) { return a + rnd() * (b - a); }
  /* Sum of three uniforms ~ gaussian. Gives organic clumps, not flat discs. */
  function gauss() { return ((rnd() + rnd() + rnd()) / 3) * 2 - 1; }

  function hexToRgba(hex, alpha) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + ((n >> 16) & 255) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + alpha + ")";
  }

  /* ------------------------------------------------------------- the scene */

  var canvas = document.getElementById("carto");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");

  var still = document.createElement("canvas");
  var sctx = still.getContext("2d");

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  var view = { w: 0, h: 0, sh: 0, dpr: 1, scale: 1, ox: 0, oy: 0, density: 1 };
  var points = [];      /* cluster points, design space */
  var bgEdges = [];     /* background network, layer space (for travellers) */
  var hubs = [];        /* design space */
  var edges = [];       /* design space, for the traveller graph */
  var travellers = [];
  var dimZones = [];
  var shift = 0;        /* current parallax offset */
  var running = false;
  var startedAt = 0;

  /* --------------------------------------------------------- build helpers */

  function scatter(cluster, count, rx, ry, sizeLo, sizeHi) {
    for (var i = 0; i < count; i++) {
      points.push({
        x: cluster.cx + gauss() * rx,
        y: cluster.cy + gauss() * ry,
        r: rr(sizeLo, sizeHi),
        /* dark dots on a light ground need a higher floor than light dots on
           a dark one — below ~.5 they read as dirt rather than nodes */
        a: rr(0.5, 1),
        color: cluster.color,
        cluster: cluster.key,
        platform: PLATFORMS[(rnd() * PLATFORMS.length) | 0]
      });
    }
  }

  function buildPoints() {
    points = [];
    var d = view.density;
    var i, c;

    for (i = 0; i < CLUSTERS.length; i++) {
      c = CLUSTERS[i];
      scatter(c, Math.round(c.nWide * d), c.rx, c.ry, 0.9, 2.1);
      /* dense pass: ~60 % of the wide radii */
      scatter(c, Math.round(c.nDense * d), c.rx * 0.6, c.ry * 0.6, 0.8, 1.8);
    }
    for (i = 0; i < SATELLITES.length; i++) {
      c = SATELLITES[i];
      scatter(c, Math.round(c.n * 0.55 * d), c.rx, c.ry, 0.9, 1.9);
      scatter(c, Math.round(c.n * 0.45 * d), c.rx * 0.6, c.ry * 0.6, 0.8, 1.6);
    }

    /* detached chain, bottom left */
    var n = Math.round(CHAIN.n * d);
    for (i = 0; i < n; i++) {
      var t = i / (n - 1);
      points.push({
        x: CHAIN.x1 + (CHAIN.x2 - CHAIN.x1) * t + gauss() * 9,
        y: CHAIN.y1 + (CHAIN.y2 - CHAIN.y1) * t + gauss() * 9,
        r: rr(0.9, 1.9),
        a: rr(0.5, 1),
        color: CHAIN.color,
        cluster: CHAIN.key,
        platform: PLATFORMS[(rnd() * PLATFORMS.length) | 0]
      });
    }
  }

  function colorOf(key) {
    var i;
    for (i = 0; i < CLUSTERS.length; i++) if (CLUSTERS[i].key === key) return CLUSTERS[i].color;
    for (i = 0; i < SATELLITES.length; i++) if (SATELLITES[i].key === key) return SATELLITES[i].color;
    return CHAIN.color;
  }

  function buildHubs() {
    hubs = [];
    var i;
    for (i = 0; i < HUBS.length; i++) {
      var h = HUBS[i];
      var key = h.cluster || h.key;
      hubs.push({
        x: h.x, y: h.y, cluster: key, color: colorOf(key),
        phase: rnd() * Math.PI * 2,
        platform: PLATFORMS[i % PLATFORMS.length]
      });
    }
    for (i = 0; i < SATELLITES.length; i++) {
      var s = SATELLITES[i];
      hubs.push({
        x: s.cx, y: s.cy, cluster: s.key, color: s.color,
        phase: rnd() * Math.PI * 2,
        platform: PLATFORMS[(i + 3) % PLATFORMS.length]
      });
    }
  }

  function pointsOf(key) {
    return points.filter(function (p) { return p.cluster === key; });
  }

  function buildEdges() {
    edges = [];
    var i, j, k;

    /* 1. hub rays — hub to its ~26 closest points */
    for (i = 0; i < hubs.length; i++) {
      var h = hubs[i];
      var near = points
        .map(function (p) { var dx = p.x - h.x, dy = p.y - h.y; return { p: p, d2: dx * dx + dy * dy }; })
        .filter(function (o) { return o.d2 < 90 * 90; })
        .sort(function (a, b) { return a.d2 - b.d2; })
        .slice(0, Math.round(26 * view.density));
      for (j = 0; j < near.length; j++) {
        edges.push({ ax: h.x, ay: h.y, bx: near[j].p.x, by: near[j].p.y,
                     a: rr(0.14, 0.3), w: 0.4, color: h.color });
      }
    }

    /* 2. local mesh — same-cluster pairs closer than ~26 units */
    var keys = CLUSTERS.map(function (c) { return c.key; })
      .concat(SATELLITES.map(function (c) { return c.key; }), [CHAIN.key]);
    for (k = 0; k < keys.length; k++) {
      var ps = pointsOf(keys[k]);
      var degree = {};
      for (i = 0; i < ps.length; i++) {
        for (j = i + 1; j < ps.length; j++) {
          var dx = ps[i].x - ps[j].x, dy = ps[i].y - ps[j].y;
          if (dx * dx + dy * dy > 26 * 26) continue;
          if ((degree[i] || 0) >= 3 || (degree[j] || 0) >= 3) continue;
          if (rnd() > 0.42) continue; /* thin it out, keep ~1800 edges total */
          degree[i] = (degree[i] || 0) + 1;
          degree[j] = (degree[j] || 0) + 1;
          edges.push({ ax: ps[i].x, ay: ps[i].y, bx: ps[j].x, by: ps[j].y,
                       a: rr(0.1, 0.22), w: 0.35, color: ps[i].color });
        }
      }
    }

    /* 3. inter-community bridges — what lets travellers cross over */
    for (k = 0; k < BRIDGES.length; k++) {
      var A = pointsOf(BRIDGES[k][0]), B = pointsOf(BRIDGES[k][1]);
      if (!A.length || !B.length) continue;
      var links = 9 + ((rnd() * 4) | 0);
      for (i = 0; i < links; i++) {
        var a = A[(rnd() * A.length) | 0], b = B[(rnd() * B.length) | 0];
        edges.push({ ax: a.x, ay: a.y, bx: b.x, by: b.y,
                     a: rr(0.07, 0.15), w: 0.3, color: a.color });
      }
    }
  }

  /* Background layer: NOT a star chart. The page is about social listening,
     so the backdrop is the same object as the foreground, one scale down —
     small communities spread over the whole surface, each one meshed
     internally, and linked to the communities next to it. Hence: a mesh
     inside each group (not a two-nearest-neighbour chain, which is what
     draws constellations) and bridges to adjacent groups only (no long
     diagonals across the page, which is what draws a sky).
     Laid out on a jittered grid so no region is left empty — a free random
     draw always clumps. */
  function drawBackdrop() {
    var w = view.w, h = view.sh;
    bgEdges = [];
    /* The grid and the dust follow the actual surface: on a wide screen the
       bands either side of the column stay populated instead of going bare. */
    var area = (w * h) / (1097 * 1020);
    var cols = Math.max(4, Math.min(8, Math.round(5 * w / 1097)));
    var rows = Math.max(3, Math.min(5, Math.round(3 * h / 1020)));
    var cw = w / cols, ch = h / rows;
    var groups = [];
    var i, j, k, m;

    /* dust first, so the network sits on top of it */
    for (i = 0; i < Math.round(250 * view.density * Math.max(1, area)); i++) {
      sctx.beginPath();
      sctx.fillStyle = hexToRgba(rnd() < 0.6 ? C.dust : C.grey, rr(0.32, 0.7));
      sctx.arc(rnd() * w, rnd() * h, rr(1.6, 4) / 2, 0, Math.PI * 2);
      sctx.fill();
    }

    /* one small community per grid cell */
    for (i = 0; i < cols; i++) {
      for (j = 0; j < rows; j++) {
        var cx = cw * (i + 0.5) + rr(-cw * 0.24, cw * 0.24);
        var cy = ch * (j + 0.5) + rr(-ch * 0.24, ch * 0.24);
        var n = Math.round((18 + rnd() * 14) * Math.min(1, view.density + 0.25));
        var rad = rr(46, 88);
        var squash = rr(0.62, 1);
        var nodes = [];
        for (k = 0; k < n; k++) {
          nodes.push({
            x: cx + gauss() * rad,
            y: cy + gauss() * rad * squash,
            r: rr(1, 1.9),
            a: rr(0.4, 0.78)
          });
        }
        /* a handful of groups take the amber, so the backdrop belongs to the
           same family as the foreground communities */
        var tone = rnd();
        groups.push({
          col: i, row: j, cx: cx, cy: cy, nodes: nodes,
          color: tone < 0.14 ? C.amber : (tone < 0.55 ? C.constell : C.greyDark)
        });
      }
    }

    /* bridges between neighbouring communities — the web, not the sky */
    function nearestPair(a, b) {
      var best = null, bd = Infinity;
      for (var p = 0; p < a.nodes.length; p++) {
        for (var q = 0; q < b.nodes.length; q++) {
          var dx = a.nodes[p].x - b.nodes[q].x, dy = a.nodes[p].y - b.nodes[q].y;
          var d = dx * dx + dy * dy;
          if (d < bd) { bd = d; best = [a.nodes[p], b.nodes[q]]; }
        }
      }
      return best;
    }

    function groupAt(col, row) {
      for (var g = 0; g < groups.length; g++) {
        if (groups[g].col === col && groups[g].row === row) return groups[g];
      }
      return null;
    }

    for (m = 0; m < groups.length; m++) {
      var g = groups[m];
      var neighbours = [groupAt(g.col + 1, g.row), groupAt(g.col, g.row + 1)];
      if (rnd() < 0.35) neighbours.push(groupAt(g.col + 1, g.row + 1));
      if (rnd() < 0.25) neighbours.push(groupAt(g.col - 1, g.row + 1));

      for (k = 0; k < neighbours.length; k++) {
        if (!neighbours[k]) continue;
        var links = 1 + ((rnd() * 2) | 0);
        for (var l = 0; l < links; l++) {
          var pair = l === 0
            ? nearestPair(g, neighbours[k])
            : [g.nodes[(rnd() * g.nodes.length) | 0],
               neighbours[k].nodes[(rnd() * neighbours[k].nodes.length) | 0]];
          if (!pair) continue;
          sctx.beginPath();
          sctx.strokeStyle = hexToRgba(C.constell, rr(0.1, 0.2));
          sctx.lineWidth = 0.5;
          sctx.moveTo(pair[0].x, pair[0].y);
          sctx.lineTo(pair[1].x, pair[1].y);
          sctx.stroke();
          bgEdges.push({ ax: pair[0].x, ay: pair[0].y,
                         bx: pair[1].x, by: pair[1].y, color: g.color });
        }
      }
    }

    /* internal mesh + nodes */
    for (m = 0; m < groups.length; m++) {
      var grp = groups[m];
      var degree = {};
      var reach = 54;
      for (k = 0; k < grp.nodes.length; k++) {
        for (i = k + 1; i < grp.nodes.length; i++) {
          var ddx = grp.nodes[k].x - grp.nodes[i].x;
          var ddy = grp.nodes[k].y - grp.nodes[i].y;
          if (ddx * ddx + ddy * ddy > reach * reach) continue;
          if ((degree[k] || 0) >= 5 || (degree[i] || 0) >= 5) continue;
          if (rnd() > 0.7) continue;
          degree[k] = (degree[k] || 0) + 1;
          degree[i] = (degree[i] || 0) + 1;
          sctx.beginPath();
          sctx.strokeStyle = hexToRgba(grp.color, rr(0.2, 0.4));
          sctx.lineWidth = 0.6;
          sctx.moveTo(grp.nodes[k].x, grp.nodes[k].y);
          sctx.lineTo(grp.nodes[i].x, grp.nodes[i].y);
          sctx.stroke();
          bgEdges.push({ ax: grp.nodes[k].x, ay: grp.nodes[k].y,
                         bx: grp.nodes[i].x, by: grp.nodes[i].y, color: grp.color });
        }
      }

      /* the node closest to the centre acts as the group's small hub */
      var hub = null, hd = Infinity;
      for (k = 0; k < grp.nodes.length; k++) {
        var hx = grp.nodes[k].x - grp.cx, hy = grp.nodes[k].y - grp.cy;
        if (hx * hx + hy * hy < hd) { hd = hx * hx + hy * hy; hub = grp.nodes[k]; }
      }

      for (k = 0; k < grp.nodes.length; k++) {
        var nd = grp.nodes[k];
        sctx.beginPath();
        sctx.fillStyle = hexToRgba(grp.color, nd.a);
        sctx.arc(nd.x, nd.y, nd === hub ? nd.r * 1.9 : nd.r, 0, Math.PI * 2);
        sctx.fill();
      }
    }
  }

  function X(x) { return view.ox + x * view.scale; }
  function Y(y) { return view.oy + y * view.scale; }

  function renderStatic() {
    still.width  = Math.round(view.w * view.dpr);
    still.height = Math.round(view.sh * view.dpr);
    sctx.setTransform(view.dpr, 0, 0, view.dpr, 0, 0);
    sctx.clearRect(0, 0, view.w, view.sh);

    drawBackdrop();

    var i;
    for (i = 0; i < edges.length; i++) {
      var e = edges[i];
      sctx.beginPath();
      sctx.strokeStyle = hexToRgba(e.color, e.a);
      sctx.lineWidth = Math.max(0.35, e.w * view.scale * 0.6);
      sctx.moveTo(X(e.ax), Y(e.ay));
      sctx.lineTo(X(e.bx), Y(e.by));
      sctx.stroke();
    }

    for (i = 0; i < points.length; i++) {
      var p = points[i];
      sctx.beginPath();
      sctx.fillStyle = hexToRgba(p.color, p.a);
      sctx.arc(X(p.x), Y(p.y), Math.max(0.6, p.r * view.scale * 0.62), 0, Math.PI * 2);
      sctx.fill();
    }
  }

  /* ------------------------------------------------------- traveller graph */

  var adjacency = null;    /* main communities, design space */
  var bgAdjacency = null;  /* background network, layer space */

  function nodeKey(x, y) { return Math.round(x) + ":" + Math.round(y); }

  function graphFrom(list) {
    var map = new Map();
    function link(ax, ay, bx, by, color) {
      var ka = nodeKey(ax, ay);
      if (!map.has(ka)) map.set(ka, { x: ax, y: ay, color: color, next: [] });
      map.get(ka).next.push(nodeKey(bx, by));
    }
    for (var i = 0; i < list.length; i++) {
      var e = list[i];
      link(e.ax, e.ay, e.bx, e.by, e.color);
      link(e.bx, e.by, e.ax, e.ay, e.color);
    }
    return map;
  }

  function buildAdjacency() {
    adjacency = graphFrom(edges);
    bgAdjacency = graphFrom(bgEdges);
  }

  /* `raw` graphs are already in layer pixels; the main one is in design
     units and has to be scaled to measure a journey in pixels.
     `leftBias` favours starting points on the left half of the page, which
     is where the main communities leave the most empty room. */
  function walkableKeys(graph, raw) {
    if (graph.all) return;
    graph.all = [];
    graph.left = [];
    graph.forEach(function (node, key) {
      if (node.next.length < 2) return;   /* dead ends make for dull journeys */
      graph.all.push(key);
      var px = raw ? node.x : X(node.x);
      if (px < view.w * 0.55) graph.left.push(key);
    });
  }

  function randomWalk(graph, raw, minPx, leftBias) {
    walkableKeys(graph, raw);
    if (!graph.all.length) return null;
    var k = view.scale;

    for (var attempt = 0; attempt < 30; attempt++) {
      /* Picking from a pre-filtered left-hand list rather than rejecting
         right-hand picks: rejection wasted most of the attempts and the
         left side stayed half as busy as the right. */
      var pool = (leftBias && graph.left.length > 12 && rnd() < 0.8)
        ? graph.left : graph.all;
      var key = pool[(rnd() * pool.length) | 0];
      var node = graph.get(key);
      if (!node) continue;

      var path = [node], prev = null, cur = key, hops = 4 + ((rnd() * 3) | 0);
      for (var i = 0; i < hops; i++) {
        var opts = graph.get(cur).next.filter(function (n) { return n !== prev; });
        if (!opts.length) break;
        prev = cur;
        cur = opts[(rnd() * opts.length) | 0];
        var nx = graph.get(cur);
        if (!nx) break;
        path.push(nx);
      }
      if (path.length < 3) continue;

      var len = 0;
      for (i = 1; i < path.length; i++) {
        var dx = (path[i].x - path[i - 1].x) * (raw ? 1 : k);
        var dy = (path[i].y - path[i - 1].y) * (raw ? 1 : k);
        len += Math.sqrt(dx * dx + dy * dy);
      }
      if (len < minPx) continue; /* too short to read as a journey */
      return { path: path, length: len };
    }
    return null;
  }

  function nearestCluster(x, y) {
    var best = null, bd = Infinity;
    for (var i = 0; i < points.length; i += 7) {
      var dx = points[i].x - x, dy = points[i].y - y, d = dx * dx + dy * dy;
      if (d < bd) { bd = d; best = points[i]; }
    }
    return best;
  }

  /* `wait` is in SECONDS. `travelled` is a distance, so the wait has to be
     converted with the traveller's own speed — passing a raw distance made
     the slower background points wait ten seconds before showing up. */
  function spawnTraveller(wait) {
    var walk = randomWalk(adjacency, false, 110, false);
    if (!walk) return null;
    var seed = nearestCluster(walk.path[0].x, walk.path[0].y);
    var speed = view.w / 14;         /* ~78 px/s at the 1097 px reference */
    return {
      path: walk.path,
      length: walk.length,
      speed: speed,
      travelled: -(speed * (wait || 0)),
      color: seed ? seed.color : C.amber,
      platform: seed ? seed.platform : PLATFORMS[0],
      raw: false, r: 1.9, glow: 7, dim: 1,
      x: 0, y: 0, alpha: 0
    };
  }

  /* Same walk, on the background network: it covers the whole surface, so it
     brings the left half of the page to life where the main communities do
     not reach. Smaller, slower and fainter, to stay behind the content. */
  function spawnBgTraveller(wait) {
    var walk = randomWalk(bgAdjacency, true, 90, true);
    if (!walk) return null;
    var speed = view.w / 20;
    return {
      path: walk.path,
      length: walk.length,
      speed: speed,
      travelled: -(speed * (wait || 0)),
      color: walk.path[0].color || C.constell,
      platform: PLATFORMS[(rnd() * PLATFORMS.length) | 0],
      raw: true, r: 1.5, glow: 5.5, dim: 0.8,
      x: 0, y: 0, alpha: 0
    };
  }

  function buildTravellers() {
    travellers = [];
    if (reduced.matches) return;
    var i, t;
    var count = Math.round(TRAVELLER_COUNT * view.density);
    for (i = 0; i < count; i++) {
      t = spawnTraveller(rnd() * 3.5);
      if (t) travellers.push(t);
    }
    var bgCount = Math.round(BG_TRAVELLER_COUNT * view.density);
    for (i = 0; i < bgCount; i++) {
      t = spawnBgTraveller(rnd() * 4);
      if (t) travellers.push(t);
    }
  }

  /* Constant speed, linear interpolation per segment — easing per segment
     makes the motion stutter at every node. */
  function advance(t, dt) {
    t.travelled += t.speed * dt;
    if (t.travelled < 0) { t.alpha = 0; return; }
    if (t.travelled > t.length) {
      var fresh = t.raw ? spawnBgTraveller(rnd() * 2.5) : spawnTraveller(rnd() * 2);
      if (fresh) { t.path = fresh.path; t.length = fresh.length; t.color = fresh.color;
                   t.platform = fresh.platform; t.travelled = fresh.travelled; }
      else t.travelled = 0;
    }

    var walked = 0;
    for (var i = 1; i < t.path.length; i++) {
      var ax = t.raw ? t.path[i - 1].x : X(t.path[i - 1].x);
      var ay = t.raw ? t.path[i - 1].y : Y(t.path[i - 1].y);
      var bx = t.raw ? t.path[i].x : X(t.path[i].x);
      var by = t.raw ? t.path[i].y : Y(t.path[i].y);
      var seg = Math.hypot(bx - ax, by - ay);
      if (walked + seg >= t.travelled || i === t.path.length - 1) {
        var u = seg ? Math.min(1, (t.travelled - walked) / seg) : 0;
        t.x = ax + (bx - ax) * u;
        t.y = ay + (by - ay) * u;
        break;
      }
      walked += seg;
    }

    var fadeDist = t.speed * (FADE_MS / 1000);
    var inFade  = Math.min(1, t.travelled / fadeDist);
    var outFade = Math.min(1, (t.length - t.travelled) / fadeDist);
    t.alpha = Math.max(0, Math.min(inFade, outFade));
  }

  /* --------------------------------------------------- text legibility mask */

  function collectDimZones() {
    dimZones = [];
    var els = document.querySelectorAll("[data-dim]");
    for (var i = 0; i < els.length; i++) {
      var r = els[i].getBoundingClientRect();
      if (r.bottom < -80 || r.top > view.h + 80 || !r.width) continue;
      dimZones.push(r);
    }
  }

  /* Punches 50 % of the map out from behind the text blocks, with a soft
     falloff. Done on the composite so travellers are dimmed too. */
  function applyDim() {
    if (!dimZones.length) return;
    /* On the cream ground a dark line reads through text far more than a pale
       line did on navy: the punch-out has to take most of the map out, not
       half of it. */
    /* The sheets and the veil now carry most of the legibility work, so the
       punch-out can be lighter and let the communities read through. */
    var steps = 6, feather = 34, strength = 0.42;
    ctx.save();
    ctx.globalCompositeOperation = "destination-out";
    for (var i = 0; i < dimZones.length; i++) {
      var r = dimZones[i];
      for (var s = 0; s < steps; s++) {
        var grow = feather * (1 - s / steps);
        ctx.fillStyle = "rgba(0,0,0," + (strength / steps) + ")";
        roundRect(ctx, r.left - 14 - grow, r.top - 10 - grow,
                       r.width + 28 + grow * 2, r.height + 20 + grow * 2, 18 + grow);
        ctx.fill();
      }
    }
    ctx.restore();
  }

  function roundRect(c, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

  /* ---------------------------------------------------------------- frame */

  var last = 0;

  function frame(now) {
    if (!running) return;
    requestAnimationFrame(frame);
    /* a hidden or not-yet-laid-out tab can report a zero-size viewport */
    if (!still.width || !still.height) return;
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
    last = now;
    if (!startedAt) startedAt = now;

    var maxShift = view.sh - view.h;
    shift = Math.min(maxShift, window.scrollY * PARALLAX);

    ctx.setTransform(view.dpr, 0, 0, view.dpr, 0, 0);
    ctx.clearRect(0, 0, view.w, view.h);
    ctx.drawImage(still, 0, -shift, view.w, view.sh);

    ctx.save();
    ctx.translate(0, -shift);

    /* hubs: pulse 1 -> 1.45 -> 1, offset from one another */
    for (var i = 0; i < hubs.length; i++) {
      var h = hubs[i];
      var k = reduced.matches ? 1
        : 1 + 0.45 * (0.5 - 0.5 * Math.cos((now / HUB_PULSE_MS) * Math.PI * 2 + h.phase));
      var hx = X(h.x), hy = Y(h.y), base = Math.max(2, 2.1 * view.scale * 0.62 * 2);

      /* on the cream ground a halo reads as a soft shadow, not a glow —
         the dark cluster needs a lighter one than the amber ones */
      var haloAlpha = h.color === C.cream ? 0.12 : 0.22;
      var halo = ctx.createRadialGradient(hx, hy, 0, hx, hy, base * 4.4 * k);
      halo.addColorStop(0, hexToRgba(h.color, haloAlpha));
      halo.addColorStop(1, hexToRgba(h.color, 0));
      ctx.fillStyle = halo;
      ctx.beginPath();
      ctx.arc(hx, hy, base * 4.4 * k, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = hexToRgba(h.color, 0.95);
      ctx.beginPath();
      ctx.arc(hx, hy, base * (0.75 + 0.25 * k), 0, Math.PI * 2);
      ctx.fill();
    }

    /* travellers */
    for (i = 0; i < travellers.length; i++) {
      var t = travellers[i];
      advance(t, dt);
      if (t.alpha <= 0) continue;
      var glow = ctx.createRadialGradient(t.x, t.y, 0, t.x, t.y, t.glow);
      glow.addColorStop(0, hexToRgba(t.color, 0.3 * t.alpha * t.dim));
      glow.addColorStop(1, hexToRgba(t.color, 0));
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(t.x, t.y, t.glow, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = hexToRgba(t.color, 0.95 * t.alpha * t.dim);
      ctx.beginPath();
      ctx.arc(t.x, t.y, t.r, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
    applyDim();
  }

  /* ---------------------------------------------------------------- setup */

  function measure() {
    view.w = Math.max(1, window.innerWidth);
    view.h = Math.max(1, window.innerHeight);
    view.sh = Math.round(view.h * STATIC_OVERSCAN);
    view.dpr = Math.min(2, window.devicePixelRatio || 1);
    /* below ~900 px the map loses density rather than being scaled down */
    view.density = Math.max(0.5, Math.min(1, view.w / 1040));
    if (view.w < 820) {
      /* portrait: fit the 600 x 500 design space to the width instead of
         cropping it, otherwise the communities fall outside the screen */
      view.scale = (view.w / 600) * 1.15;
      view.oy = view.h * 0.46 - 250 * view.scale;
    } else {
      /* The map keeps growing past the reference width, but at about half
         the rate of the screen: it covers a wide display without the
         communities ballooning out of frame. */
      var refW = Math.max(1097, Math.min(1750, 1097 + (view.w - 1097) * 0.55));
      var refH = Math.min(view.h, 980);
      view.scale = Math.max(refW / 600, refH / 500) * 1.03;
      view.oy = (view.h - 500 * view.scale) / 2;
    }
    view.ox = (view.w - 600 * view.scale) / 2;

    canvas.width  = Math.round(view.w * view.dpr);
    canvas.height = Math.round(view.h * view.dpr);
    canvas.style.width = view.w + "px";
    canvas.style.height = view.h + "px";
  }

  function build() {
    rnd = mulberry32(20260915);
    measure();
    buildPoints();
    buildHubs();
    buildEdges();
    /* renderStatic draws the background network and records its edges, so the
       adjacency maps are built after it, not before */
    renderStatic();
    buildAdjacency();
    buildTravellers();
    collectDimZones();
  }

  function start() {
    if (running) return;
    running = true;
    last = 0;
    requestAnimationFrame(frame);
  }

  build();
  start();

  /* Lets the UI anchor a story card on a point that is actually moving:
     returns a live traveller in the right-hand half of the viewport, in
     viewport coordinates, or null if none is available right now. */
  window.LicterCarto = {
    pickTraveller: function (minX, maxX, minY, maxY) {
      var candidates = [];
      for (var i = 0; i < travellers.length; i++) {
        var t = travellers[i];
        if (t.alpha < 0.4) continue;
        var y = t.y - shift;
        if (t.x < minX || t.x > maxX || y < minY || y > maxY) continue;
        candidates.push({ x: Math.round(t.x), y: Math.round(y),
                          platform: t.platform, color: t.color });
      }
      if (!candidates.length) return null;
      return candidates[(Math.random() * candidates.length) | 0];
    }
  };


  var resizeTimer = null;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { build(); }, 180);
  });

  window.addEventListener("scroll", collectDimZones, { passive: true });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) { running = false; }
    else { start(); }
  });
  reduced.addEventListener("change", function () { build(); });

  /* recompute text zones when fonts land and the layout settles */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(collectDimZones);
  window.addEventListener("load", collectDimZones);
})();
