/* =========================================================================
   Licter — page behaviour: logo crop, client marquee, use-case tabs, form.
   ========================================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ------------------------------------------------------------------ logo
     The source PNG carries a wide transparent margin; crop it at runtime so
     the mark sits at its 44 x 48 box without a hand-made asset. */
  Array.prototype.forEach.call(document.querySelectorAll(".logo"), function (wrap) {
    var img = wrap.querySelector(".logo__img");
    var out = wrap.querySelector(".logo__canvas");
    if (!img || !out) return;

    function run() {
      var src = document.createElement("canvas");
      src.width = img.naturalWidth; src.height = img.naturalHeight;
      var sc = src.getContext("2d", { willReadFrequently: true });
      sc.drawImage(img, 0, 0);
      var data;
      try { data = sc.getImageData(0, 0, src.width, src.height).data; }
      catch (e) { return; } /* file:// without --allow-file-access: keep the img */

      var minX = src.width, minY = src.height, maxX = -1, maxY = -1;
      for (var y = 0; y < src.height; y++) {
        for (var x = 0; x < src.width; x++) {
          if (data[(y * src.width + x) * 4 + 3] > 12) {
            if (x < minX) minX = x; if (x > maxX) maxX = x;
            if (y < minY) minY = y; if (y > maxY) maxY = y;
          }
        }
      }
      if (maxX < 0) return;

      var cw = maxX - minX + 1, chh = maxY - minY + 1;
      var dpr = Math.min(2, window.devicePixelRatio || 1);
      var box = wrap.getBoundingClientRect();
      var bw = Math.round(box.width) || 44;
      var bh = Math.round(box.height) || 48;
      out.width = bw * dpr; out.height = bh * dpr;
      out.style.width = bw + "px"; out.style.height = bh + "px";
      var oc = out.getContext("2d");
      oc.setTransform(dpr, 0, 0, dpr, 0, 0);
      var k = Math.min(bw / cw, bh / chh);
      oc.drawImage(img, minX, minY, cw, chh,
                   (bw - cw * k) / 2, (bh - chh * k) / 2, cw * k, chh * k);
      wrap.classList.add("is-trimmed");
    }

    if (img.complete && img.naturalWidth) run();
    else img.addEventListener("load", run);

    var t = null;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { if (img.naturalWidth) run(); }, 200);
    });
  });

  /* --------------------------------------------------------- client logos
     PLACEHOLDER MARKS. The real files were not supplied; each entry below is
     a white wordmark at the display ratio taken from the mock. Drop the
     official assets in as white silhouettes on transparent ground and keep
     the same width / height pairs. */
  var CLIENTS = [
    { name: "HP",                   w:  42, h: 42, opacity: 0.78, weight: 700, tracking: 0 },
    { name: "DECATHLON",            w:  64, h: 42, opacity: 1,    weight: 700, tracking: 0 },
    { name: "UNESCO",               w: 120, h: 25, opacity: 0.78, weight: 600, tracking: 2 },
    { name: "L'ORÉAL",              w: 120, h: 22, opacity: 1,    weight: 400, tracking: 4 },
    { name: "DANONE",               w: 114, h: 36, opacity: 1,    weight: 700, tracking: 1 },
    { name: "SOCIÉTÉ GÉNÉRALE",     w: 120, h: 24, opacity: 1,    weight: 600, tracking: 0 },
    { name: "GALERIES LAFAYETTE",   w: 132, h: 20, opacity: 1,    weight: 400, tracking: 1 },
    { name: "CELIO",                w: 120, h: 26, opacity: 1,    weight: 600, tracking: 3 },
    { name: "LA POSTE",             w:  96, h: 30, opacity: 1,    weight: 700, tracking: 0 },
    { name: "SISLEY",               w: 104, h: 22, opacity: 1,    weight: 400, tracking: 5 },
    { name: "BOUYGUES TELECOM",     w: 130, h: 22, opacity: 1,    weight: 600, tracking: 0 },
    { name: "STUDI",                w:  88, h: 28, opacity: 1,    weight: 700, tracking: 1 },
    { name: "TV5 MONDE",            w: 104, h: 28, opacity: 1,    weight: 700, tracking: 0 },
    { name: "PMU",                  w:  74, h: 30, opacity: 1,    weight: 700, tracking: 1 },
    { name: "LA MARINE RECRUTE",    w: 124, h: 24, opacity: 1,    weight: 600, tracking: 0 },
    /* nom complet en étiquette accessible, le wordmark serait illisible */
    { name: "BIOPARC", label: "Bioparc de Doué La Fontaine",
                                    w: 108, h: 26, opacity: 1,    weight: 600, tracking: 2 }
  ];
  var GAP = 44;
  /* px per second the logo band travels. It ran at 126, which reads as a
     ticker rather than a wall of names you have time to recognise. */
  var MARQUEE_SPEED = 45;

  function svgFor(c) {
      var vw = 200, vh = Math.round(200 * c.h / c.w);
      var size = Math.min(vh * 0.86, (vw * 1.35) / Math.max(4, c.name.length));
      return '<svg viewBox="0 0 ' + vw + ' ' + vh + '" role="img" aria-label="' +
        (c.label || c.name) + '">' +
        '<text x="' + (vw / 2) + '" y="' + (vh / 2) + '" fill="currentColor" ' +
        'text-anchor="middle" dominant-baseline="central" ' +
        'font-family="Josefin Sans, system-ui, sans-serif" font-weight="' + c.weight + '" ' +
        'letter-spacing="' + c.tracking + '" font-size="' + size.toFixed(1) + '">' +
        c.name + "</text></svg>";
  }

  function buildMarquee() {
    var track = document.getElementById("marquee-track");
    if (!track) return;

    /* same scale-up as the rest of the hero past the reference width */
    var k = Math.min(1.28, Math.max(1, window.innerWidth / 1247));
    var gap = Math.round(GAP * k);

    var setWidth = 0;
    CLIENTS.forEach(function (c) { setWidth += Math.round(c.w * k) + gap; });

    /* Repeat the set until the track is always at least one set longer than
       the screen — otherwise a gap shows up at the end of the cycle. */
    var repeats = Math.max(2, Math.ceil(window.innerWidth / setWidth) + 1);
    var html = "";
    for (var r = 0; r < repeats; r++) {
      CLIENTS.forEach(function (c) {
        html += '<span class="client-logo" style="width:' + Math.round(c.w * k) +
                "px;height:" + Math.round(c.h * k) +
                "px;--logo-opacity:" + c.opacity + '"' +
                (r === 0 ? "" : ' aria-hidden="true"') + ">" + svgFor(c) + "</span>";
      });
    }
    track.innerHTML = html;
    track.style.gap = gap + "px";
    track.style.paddingLeft = gap + "px";
    track.style.setProperty("--marquee-shift", -setWidth + "px");
    track.style.setProperty("--marquee-duration", (setWidth / (MARQUEE_SPEED * k)).toFixed(2) + "s");
  }

  buildMarquee();

  /* The wall on clients.html held the same sixteen names as plain text, all at
     one weight, in a boxed grid — a spreadsheet. It now takes the weight,
     tracking and opacity the marquee gives each brand, so they keep their own
     character. It does NOT reuse the marquee's SVG: those boxes are sized per
     brand, which in a grid renders HP at 10px next to DANONE at 21px. A single
     font size with the per-brand weight keeps the identity and the evenness.
     The static markup stays as the no-JS fallback. */
  (function () {
    var wall = document.getElementById("logo-wall");
    if (!wall) return;
    wall.innerHTML = CLIENTS.map(function (c) {
      return '<li><span class="wordmark" style="font-weight:' + c.weight +
             ";letter-spacing:" + (c.tracking * 0.06).toFixed(2) + "em;opacity:" + c.opacity +
             '">' + (c.label ? '<abbr title="' + c.label + '">' + c.name + "</abbr>" : c.name) +
             "</span></li>";
    }).join("");
    wall.classList.add("is-built");
  })();

  (function () {
    var t = null, w = window.innerWidth;
    window.addEventListener("resize", function () {
      if (window.innerWidth === w) return;
      w = window.innerWidth;
      clearTimeout(t);
      t = setTimeout(buildMarquee, 200);
    });
  })();

  /* ----------------------------------------------------- platform icons
     PLACEHOLDER GLYPHS, drawn monochrome white to sit on the navy card.
     Platform brand guidelines generally forbid recolouring: swap these for
     the official assets before shipping (see the note in the brief). */
  window.LicterIcons = {
    TIKTOK: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13.5 3v11.2a3.3 3.3 0 1 1-2.6-3.2"/><path d="M13.5 3c.4 2.4 2 4 4.5 4.2"/></svg>',
    INSTAGRAM: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/></svg>',
    X: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4.5 4.5l15 15M19.5 4.5l-15 15"/></svg>',
    LINKEDIN: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 10.5V17M8 7.6v.1M12 17v-3.6a2.2 2.2 0 0 1 4.4 0V17"/></svg>',
    YOUTUBE: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.2 9.4l4.6 2.6-4.6 2.6z" fill="currentColor" stroke="none"/></svg>',
    FACEBOOK: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M14.3 8.2h-1.2a1.8 1.8 0 0 0-1.8 1.8V20M9.7 12.6h4.4"/></svg>'
  };

  /* ------------------------------------------------------------ use cases */

  /* Every figure in this console is illustrative — a plausible read, not a
     client result. Licter has to replace them before this goes live. */
  var CASES = {
    communication: {
      family: "COMMUNICATION",
      label: "CAMPAIGN IMPACT — SHARE OF VOICE",
      metric: "+23%",
      trend: "vs. category benchmark, rolling 90 days",
      caption: "Creator-driven reach over the last 90 days, measured against the category benchmark.",
      series: [18, 22, 20, 28, 34, 31, 42, 47, 45, 58, 63, 71],
      seed: 7,
      kpis: [
        { label: "Share of voice", value: "23.4%", delta: "+15.5%", dir: "up", spark: [12, 15, 14, 18, 17, 21, 23] },
        { label: "Creator reach", value: "4.1M", delta: "+40.2%", dir: "up", spark: [1.8, 2.1, 2.0, 2.8, 3.2, 3.6, 4.1] },
        { label: "Paid share", value: "12.8%", delta: "-6.4%", dir: "down", spark: [21, 20, 18, 17, 15, 14, 13] }
      ],
      barsTitle: "VOLUME BY MONTH",
      barsTotal: "48.2k",
      barsNote: "posts collected, owned and earned",
      railTitle: "WHERE THE VOICE COMES FROM",
      rail: [
        { name: "TikTok", v: 34, posts: "12.4k", d: "+18%", dir: "up" },
        { name: "Instagram", v: 27, posts: "9.8k", d: "+11%", dir: "up" },
        { name: "YouTube", v: 21, posts: "3.2k", d: "+6%", dir: "up" },
        { name: "X", v: 11, posts: "5.1k", d: "-4%", dir: "down" },
        { name: "LinkedIn", v: 7, posts: "1.4k", d: "+2%", dir: "up" }
      ],
      signalsTitle: "SIGNALS TO WATCH",
      signals: [
        { name: "Short-form formats", note: "carrying the reach", state: "up", v: "62%" },
        { name: "Earned over owned", note: "share still climbing", state: "up", v: "41%" },
        { name: "Brand mentions", note: "steady, no spike", state: "flat", v: "18%" },
        { name: "Paid amplification", note: "losing ground", state: "down", v: "9%" }
      ],
      anchor: "use-cases.html#communication",
      questions: [
        "Analyze the impact of an event or campaign",
        "Optimize your leader advocacy strategy",
        "Identify the right ambassadors"
      ]
    },
    brand: {
      family: "BRAND HEALTH",
      label: "BRAND HEALTH — NET SENTIMENT",
      metric: "+17%",
      trend: "net positive, owned and earned conversations",
      caption: "Net positive sentiment on owned and earned conversations, panel-weighted.",
      series: [30, 34, 31, 36, 41, 39, 44, 48, 52, 50, 57, 62],
      seed: 23,
      kpis: [
        { label: "Net sentiment", value: "17.2", delta: "+9.4 pts", dir: "up", spark: [8, 9, 11, 10, 13, 15, 17] },
        { label: "Negative share", value: "8.6%", delta: "-3.1 pts", dir: "down", spark: [13, 12, 12, 11, 10, 9, 9] },
        { label: "Risk alerts", value: "4", delta: "-2 vs. Q3", dir: "down", spark: [9, 8, 7, 6, 6, 5, 4] }
      ],
      barsTitle: "VOLUME BY MONTH",
      barsTotal: "36.9k",
      barsNote: "conversations classified, owned and earned",
      railTitle: "WHAT DRIVES THE SENTIMENT",
      rail: [
        { name: "Product", v: 38, posts: "8.9k", d: "+12%", dir: "up" },
        { name: "Service", v: 24, posts: "6.2k", d: "+21%", dir: "up" },
        { name: "Pricing", v: 18, posts: "4.4k", d: "+9%", dir: "up" },
        { name: "Campaigns", v: 12, posts: "2.8k", d: "-5%", dir: "down" },
        { name: "Corporate", v: 8, posts: "1.1k", d: "-2%", dir: "down" }
      ],
      signalsTitle: "SIGNALS TO WATCH",
      signals: [
        { name: "Service backlog", note: "the fastest riser", state: "up", v: "21%" },
        { name: "Pricing chatter", note: "spreading past the core", state: "up", v: "14%" },
        { name: "Product quality", note: "stable quarter on quarter", state: "flat", v: "38%" },
        { name: "Corporate news", note: "fading from the feed", state: "down", v: "8%" }
      ],
      anchor: "use-cases.html#brand-health",
      questions: [
        "Monitor your brand image and reputation",
        "Develop your brand messaging",
        "Identify and mitigate brand risks"
      ]
    },
    audiences: {
      family: "AUDIENCES",
      label: "CORE TARGET — QUALIFIED REACH",
      metric: "2.4",
      metricPrefix: "\u00d7",
      trend: "qualified reach, look-alike communities folded in",
      caption: "Qualified reach inside the core target once look-alike communities are folded in.",
      series: [12, 16, 24, 21, 33, 38, 36, 49, 55, 61, 58, 74],
      seed: 41,
      kpis: [
        { label: "Core target share", value: "41%", delta: "+7 pts", dir: "up", spark: [28, 30, 31, 34, 36, 39, 41] },
        { label: "Look-alike overlap", value: "26%", delta: "+12 pts", dir: "up", spark: [12, 14, 17, 19, 21, 24, 26] },
        { label: "Out of target", value: "17%", delta: "-8 pts", dir: "down", spark: [26, 25, 23, 21, 20, 18, 17] }
      ],
      barsTitle: "PROFILES BY MONTH",
      barsTotal: "1.9M",
      barsNote: "profiles qualified, core and look-alike",
      railTitle: "WHO THE COMMUNITIES ARE",
      rail: [
        { name: "Core target", v: 41, posts: "780k", d: "+7%", dir: "up" },
        { name: "Look-alikes", v: 26, posts: "495k", d: "+31%", dir: "up" },
        { name: "Prescribers", v: 16, posts: "304k", d: "+5%", dir: "up" },
        { name: "Detractors", v: 10, posts: "190k", d: "-3%", dir: "down" },
        { name: "Undecided", v: 7, posts: "133k", d: "-1%", dir: "down" }
      ],
      signalsTitle: "SIGNALS TO WATCH",
      signals: [
        { name: "Look-alike pool", note: "the reach upside", state: "up", v: "31%" },
        { name: "Under-25 share", note: "growing on two platforms", state: "up", v: "23%" },
        { name: "Prescribers", note: "size holding", state: "flat", v: "16%" },
        { name: "Detractor cluster", note: "shrinking slowly", state: "down", v: "10%" }
      ],
      anchor: "use-cases.html#audiences",
      questions: [
        "Segment your target profiles",
        "Rejuvenate your audiences",
        "Understand expectations at every touchpoint"
      ]
    },
    trends: {
      family: "INNOVATION",
      label: "EMERGING TOPICS — VELOCITY",
      metric: "+41%",
      trend: "velocity of topics breaking out of the category",
      caption: "Velocity of the topics breaking out of the category over the last four weeks.",
      series: [8, 11, 14, 13, 22, 29, 27, 38, 46, 52, 66, 79],
      seed: 59,
      kpis: [
        { label: "Topics tracked", value: "128", delta: "+12 new", dir: "up", spark: [96, 101, 104, 112, 118, 123, 128] },
        { label: "Breakout rate", value: "9.4%", delta: "+3.2 pts", dir: "up", spark: [4, 5, 5, 7, 8, 9, 9] },
        { label: "Median lead time", value: "6", delta: "weeks ahead", dir: "up", spark: [3, 4, 4, 5, 5, 6, 6] }
      ],
      barsTitle: "MENTIONS BY MONTH",
      barsTotal: "22.7k",
      barsNote: "mentions on the tracked topics",
      railTitle: "WHAT IS BREAKING OUT",
      rail: [
        { name: "Refill formats", v: 31, posts: "7.0k", d: "+64%", dir: "up" },
        { name: "Dupe culture", v: 25, posts: "5.7k", d: "+48%", dir: "up" },
        { name: "AI try-on", v: 20, posts: "4.5k", d: "+37%", dir: "up" },
        { name: "Resale", v: 14, posts: "3.2k", d: "+9%", dir: "up" },
        { name: "Longevity", v: 10, posts: "2.3k", d: "-2%", dir: "down" }
      ],
      signalsTitle: "SIGNALS TO WATCH",
      signals: [
        { name: "Refill formats", note: "out of the niche", state: "up", v: "64%" },
        { name: "Dupe culture", note: "crossing into press", state: "up", v: "48%" },
        { name: "Resale", note: "plateau after two quarters", state: "flat", v: "14%" },
        { name: "Longevity claims", note: "cooling off", state: "down", v: "10%" }
      ],
      anchor: "use-cases.html#trends",
      questions: [
        "Test and evaluate your products",
        "Analyze markets and identify opportunities",
        "Map out your stakeholders and future trends"
      ]
    }
  };

  var MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];

  function chart(series) {
    var w = 1000, h = 300, padL = 10, padR = 44, padT = 22, padB = 36;
    var max = Math.max.apply(null, series), min = Math.min.apply(null, series);
    var span = Math.max(1, max - min);
    var pts = series.map(function (v, i) {
      return [padL + (w - padL - padR) * (i / (series.length - 1)),
              h - padB - (h - padT - padB) * ((v - min) / span)];
    });

    /* light horizontal guides */
    var guides = "";
    for (var g = 0; g <= 3; g++) {
      var gy = padT + ((h - padT - padB) / 3) * g;
      guides += '<line x1="' + padL + '" y1="' + gy.toFixed(1) + '" x2="' + (w - padR) +
                '" y2="' + gy.toFixed(1) + '" stroke="rgba(19,22,45,.07)" stroke-width="1"/>';
    }

    var line = pts.map(function (p, i) {
      return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1);
    }).join(" ");
    var area = line + " L" + (w - padR) + " " + (h - padB) + " L" + padL + " " + (h - padB) + " Z";

    var dots = pts.map(function (p, i) {
      var last = i === pts.length - 1;
      return '<circle class="chart__dot" style="--i:' + i + '" cx="' + p[0].toFixed(1) +
             '" cy="' + p[1].toFixed(1) + '" r="' + (last ? 6 : 3) +
             '" fill="' + (last ? "#C08C0E" : "#96A1A8") + '"/>';
    }).join("");

    var labels = pts.map(function (p, i) {
      return '<text x="' + p[0].toFixed(1) + '" y="' + (h - 10) + '" fill="#6F7A82" ' +
             'font-family="Josefin Sans, sans-serif" font-size="13" letter-spacing="1.5" ' +
             'text-anchor="middle">' + MONTHS[i % 12] + "</text>";
    }).join("");

    var lastX = pts[pts.length - 1][0], lastY = pts[pts.length - 1][1];

    return '<svg class="chart" viewBox="0 0 ' + w + " " + h + '" role="img" aria-hidden="true">' +
      '<defs>' +
        '<linearGradient id="vizFill" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0%" stop-color="#FDBA11" stop-opacity=".5"/>' +
          '<stop offset="100%" stop-color="#FDBA11" stop-opacity="0"/>' +
        '</linearGradient>' +
        '<radialGradient id="vizDot"><stop offset="0%" stop-color="#FDBA11" stop-opacity=".7"/>' +
          '<stop offset="100%" stop-color="#FDBA11" stop-opacity="0"/></radialGradient>' +
      "</defs>" + guides +
      '<path class="chart__area" d="' + area + '" fill="url(#vizFill)"/>' +
      '<line class="chart__cursor" x1="' + lastX.toFixed(1) + '" y1="' + padT + '" x2="' + lastX.toFixed(1) +
        '" y2="' + (h - padB) + '" stroke="rgba(154,111,8,.35)" stroke-width="1" stroke-dasharray="3 4"/>' +
      '<path class="chart__line" data-draw d="' + line + '" fill="none" stroke="#C08C0E" stroke-width="2.4" ' +
        'stroke-linejoin="round" stroke-linecap="round"/>' +
      '<circle class="chart__cursor" cx="' + lastX.toFixed(1) + '" cy="' + lastY.toFixed(1) + '" r="20" fill="url(#vizDot)"/>' +
      dots + labels + "</svg>";
  }

  /* the tiny curve in the corner of a stat cell — same draw-on as the big one */
  function spark(series) {
    var w = 104, h = 22, p = 3;
    var max = Math.max.apply(null, series), min = Math.min.apply(null, series);
    var span = Math.max(0.001, max - min);
    var d = series.map(function (v, i) {
      var x = p + (w - p * 2) * (i / (series.length - 1));
      var y = h - p - (h - p * 2) * ((v - min) / span);
      return (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1);
    }).join(" ");
    return '<svg class="spark" viewBox="0 0 ' + w + " " + h + '" aria-hidden="true">' +
      '<path class="spark__line" data-draw d="' + d + '" fill="none" stroke="currentColor" ' +
      'stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>';
  }

  /* owned / earned split, derived from the series so the two charts agree */
  function split(series, seed) {
    var s = (seed || 1) >>> 0;
    function rnd() { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }
    return series.map(function (v) {
      var owned = Math.max(3, Math.round(v * (0.3 + rnd() * 0.2)));
      return [owned, Math.max(2, v - owned)];
    });
  }

  function barsChart(pairs) {
    var w = 430, h = 168, padB = 20, padT = 8;
    var max = Math.max.apply(null, pairs.map(function (p) { return Math.max(p[0], p[1]); }));
    var slot = w / pairs.length, bw = Math.min(8, slot * 0.3), gap = 3;
    var usable = h - padB - padT;

    return '<svg class="bars" viewBox="0 0 ' + w + " " + h + '" aria-hidden="true">' +
      pairs.map(function (p, i) {
        var cx = slot * (i + 0.5);
        return p.map(function (v, k) {
          var bh = Math.max(3, usable * (v / max));
          var x = cx - bw - gap / 2 + k * (bw + gap);
          return '<rect class="bars__b bars__b--' + (k ? "earned" : "owned") + '" style="--i:' + i +
                 '" x="' + x.toFixed(1) + '" y="' + (h - padB - bh).toFixed(1) +
                 '" width="' + bw.toFixed(1) + '" height="' + bh.toFixed(1) + '" rx="2"/>';
        }).join("");
      }).join("") +
      pairs.map(function (p, i) {
        return '<text x="' + (slot * (i + 0.5)).toFixed(1) + '" y="' + (h - 6) +
               '" fill="#8C959C" font-family="Josefin Sans, sans-serif" font-size="9" ' +
               'letter-spacing="1" text-anchor="middle">' + MONTHS[i % 12] + "</text>";
      }).join("") + "</svg>";
  }

  function tableRows(rows) {
    var top = Math.max.apply(null, rows.map(function (r) { return r.v; }));
    return rows.map(function (r, i) {
      return '<tr>' +
        '<td class="tbl__name">' + r.name + "</td>" +
        '<td class="tbl__share"><b>' + r.v + "%</b>" +
          '<span class="tbl__bar"><i data-grow style="--w:' + Math.round((r.v / top) * 100) +
          "%;--i:" + i + '"></i></span></td>' +
        '<td class="tbl__num">' + r.posts + "</td>" +
        '<td class="tbl__delta is-' + r.dir + '">' + r.d + "</td>" +
        "</tr>";
    }).join("");
  }

  function signalRows(rows) {
    var arrow = { up: "↗", flat: "→", down: "↘" };
    return rows.map(function (r, i) {
      return '<li class="sig" style="--i:' + i + '">' +
        '<span class="sig__mark is-' + r.state + '" aria-hidden="true">' + arrow[r.state] + "</span>" +
        '<span class="sig__text"><b>' + r.name + "</b><em>" + r.note + "</em></span>" +
        '<span class="sig__v">' + r.v + "</span></li>";
    }).join("");
  }

  function statCells(kpis) {
    return kpis.map(function (k, i) {
      return '<div class="viz__cell stat" style="--i:' + i + '">' +
        '<p class="stat__label">' + k.label + "</p>" +
        '<p class="stat__value" data-count>' + k.value + "</p>" +
        '<p class="stat__delta is-' + k.dir + '">' + k.delta + "</p>" +
        '<span class="stat__spark is-' + k.dir + '">' + spark(k.spark) + "</span>" +
        "</div>";
    }).join("");
  }

  var viz = document.getElementById("viz");
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  var panel = document.getElementById("cases-panel");

  var questions = document.getElementById("questions");

  /* The three questions of the selected family, straight from the deck. The
     column answers the console: same head, same numbering, same foot line. */
  var asksLabel = document.getElementById("asks-label");
  var asksCount = document.getElementById("asks-count");

  function renderQuestions(key) {
    if (!questions) return;
    var d = CASES[key];

    if (asksLabel) asksLabel.textContent = d.family;
    if (asksCount) asksCount.textContent = "0" + d.questions.length + " / 12";

    questions.innerHTML = d.questions.map(function (q, i) {
      return '<li style="--i:' + i + '"><a class="question" href="' + d.anchor + '">' +
        '<span class="question__n">0' + (i + 1) + "</span>" +
        '<span class="question__text">' + q + "</span>" +
        '<span class="question__arrow" aria-hidden="true">\u2192</span></a></li>';
    }).join("");

    questions.classList.remove("is-swap");
    void questions.offsetWidth;
    questions.classList.add("is-swap");
  }

  function renderViz(key) {
    if (!viz) return;
    var d = CASES[key];
    var pairs = split(d.series, d.seed);

    viz.innerHTML =
      '<div class="viz__head">' +
        '<div class="viz__id"><span class="viz__dot" aria-hidden="true"></span>' +
          '<span class="viz__label">' + d.label + "</span></div>" +
        '<div class="viz__range" aria-hidden="true">' +
          '<span class="viz__chip is-on">90 days</span>' +
          '<span class="viz__chip">12 months</span>' +
          '<span class="viz__chip">Export</span>' +
        "</div>" +
      "</div>" +

      '<div class="viz__grid">' +
        statCells(d.kpis) +
        '<div class="viz__cell viz__cell--hero vizhero">' +
          '<p class="stat__label">' + d.label.split(" — ")[0] + "</p>" +
          '<p class="vizhero__metric" data-count>' + (d.metricPrefix || "") + d.metric + "</p>" +
          '<p class="vizhero__trend">' + d.trend + "</p>" +
        "</div>" +

        '<div class="viz__cell viz__cell--wide">' +
          '<p class="viz__cellTitle">Trend — rolling 12 months</p>' +
          '<p class="viz__cellNote">Indexed against the category benchmark.</p>' +
          '<div class="viz__chart">' + chart(d.series) + "</div>" +
        "</div>" +
        '<div class="viz__cell viz__cell--side">' +
          '<p class="viz__cellTitle">' + d.barsTitle + "</p>" +
          '<p class="viz__total" data-count>' + d.barsTotal + "</p>" +
          '<p class="viz__cellNote">' + d.barsNote + "</p>" +
          '<div class="viz__legend"><span class="key key--owned">Owned</span>' +
            '<span class="key key--earned">Earned</span></div>' +
          barsChart(pairs) +
        "</div>" +

        '<div class="viz__cell viz__cell--wide">' +
          '<p class="viz__cellTitle">' + d.railTitle + "</p>" +
          '<table class="tbl"><thead><tr><th>Source</th><th>Share</th>' +
            "<th>Posts</th><th>30 d</th></tr></thead>" +
            "<tbody>" + tableRows(d.rail) + "</tbody></table>" +
        "</div>" +
        '<div class="viz__cell viz__cell--side">' +
          '<p class="viz__cellTitle">' + d.signalsTitle + "</p>" +
          '<ul class="sigs">' + signalRows(d.signals) + "</ul>" +
        "</div>" +
      "</div>" +

      '<figcaption class="viz__foot">' + d.caption + "</figcaption>";

    animateViz();
  }

  /* The panel is a data visual, so the data is what moves: the curves draw
     themselves, the bars grow to their value, every figure counts up. */
  function animateViz() {
    if (reduced.matches) {
      viz.querySelectorAll("[data-grow]").forEach(function (bar) {
        bar.style.width = bar.style.getPropertyValue("--w");
      });
      return;
    }

    viz.querySelectorAll("[data-draw]").forEach(function (path) {
      if (path.getTotalLength) path.style.setProperty("--len", Math.ceil(path.getTotalLength()));
    });

    requestAnimationFrame(function () {
      viz.querySelectorAll("[data-grow]").forEach(function (bar) {
        bar.classList.add("is-grown");
      });
    });

    viz.querySelectorAll("[data-count]").forEach(function (el) { countUp(el); });
  }

  function countUp(el) {
    if (!el) return;
    var raw = el.textContent;
    var parts = raw.match(/^([^\d]*)([\d.]+)(.*)$/);
    if (!parts) return;
    var target = parseFloat(parts[2]);
    var decimals = (parts[2].split(".")[1] || "").length;
    var start = null, span = 820;

    function step(now) {
      if (start === null) start = now;
      var t = Math.min(1, (now - start) / span);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = parts[1] + (target * eased).toFixed(decimals) + parts[3];
      if (t < 1) requestAnimationFrame(step);
    }
    el.textContent = parts[1] + (0).toFixed(decimals) + parts[3];
    requestAnimationFrame(step);
  }

  var deck = document.getElementById("deck");

  /* Tab change = the deck deals a card: the current panel turns away, the
     stack behind it steps forward, the new panel arrives from the other side. */
  function dealTo(key) {
    if (!viz) return;
    renderQuestions(key);
    if (reduced.matches) { renderViz(key); return; }

    viz.classList.remove("is-in");
    viz.classList.add("is-out");
    if (deck) deck.classList.add("is-dealing");

    setTimeout(function () {
      renderViz(key);
      viz.classList.remove("is-out");
      viz.classList.add("is-in");
      if (deck) deck.classList.remove("is-dealing");
      /* belt and braces: animationend does the cleanup, this catches the case
         where the animation never runs (tab in the background, for instance) */
      setTimeout(function () { viz.classList.remove("is-in"); }, 700);
    }, 220);
  }

  if (viz) {
    viz.addEventListener("animationend", function (e) {
      if (e.animationName === "viz-in") viz.classList.remove("is-in");
    });
  }

  function selectTab(btn) {
    tabs.forEach(function (t) {
      var on = t === btn;
      t.classList.toggle("is-active", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    if (panel) panel.setAttribute("aria-labelledby", btn.id);
    dealTo(btn.dataset.tab);
  }

  tabs.forEach(function (btn, i) {
    btn.addEventListener("click", function () { selectTab(btn); });
    btn.addEventListener("keydown", function (e) {
      var dir = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!dir) return;
      e.preventDefault();
      var next = tabs[(i + dir + tabs.length) % tabs.length];
      next.focus();
      selectTab(next);
    });
  });

  renderQuestions("communication");
  renderViz("communication");

  /* The stack assembles itself the first time it comes into view.
     Three triggers rather than one: an observer, a rect check on scroll, and
     a hard fallback timer — a reveal that never fires leaves the console
     invisible, so it must not hang on a single mechanism. */
  (function buildDeck() {
    if (!deck) return;

    var done = false;
    function ready() {
      if (done) return;
      done = true;
      deck.classList.add("is-ready");
    }
    function build() {
      if (done) return;
      done = true;
      deck.classList.add("is-building");
      setTimeout(function () {
        deck.classList.remove("is-building");
        deck.classList.add("is-ready");
      }, 960);
    }

    if (reduced.matches) { ready(); return; }

    function inView() {
      var r = deck.getBoundingClientRect();
      return r.top < window.innerHeight * 0.85 && r.bottom > 0;
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        build();
      }, { threshold: 0.25 });
      io.observe(deck);
    }

    function onScroll() {
      if (done) { window.removeEventListener("scroll", onScroll); return; }
      if (inView()) { build(); window.removeEventListener("scroll", onScroll); }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    if (inView()) build();
    setTimeout(ready, 4000);
  })();

  /* The stack leans a few degrees towards the cursor — enough to read as an
     object in space, little enough not to fight the text next to it. */
  (function tiltDeck() {
    if (!deck || reduced.matches) return;
    if (!window.matchMedia("(hover: hover)").matches) return;

    var zone = document.querySelector(".cases__live") || deck;
    var raf = null, tx = 0, ty = 0;

    function apply() {
      raf = null;
      deck.style.setProperty("--tilt-x", tx.toFixed(2) + "deg");
      deck.style.setProperty("--tilt-y", ty.toFixed(2) + "deg");
    }

    zone.addEventListener("mousemove", function (e) {
      var r = deck.getBoundingClientRect();
      ty = ((e.clientX - (r.left + r.width / 2)) / r.width) * 7;
      tx = -((e.clientY - (r.top + r.height / 2)) / r.height) * 4.5;
      deck.classList.add("is-tracking");
      if (!raf) raf = requestAnimationFrame(apply);
    });

    zone.addEventListener("mouseleave", function () {
      tx = 0; ty = 0;
      deck.classList.remove("is-tracking");
      if (!raf) raf = requestAnimationFrame(apply);
    });
  })();

  /* ------------------------------------------------------------ nav menus
     Two entries carry a panel: the four use-case categories (same four as
     the tabs below) and the six platforms of the panel. OFFERS and WHY
     LICTER stay plain links until there is real content for them. */

  var ICONS = {
    influence: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2.6"/><circle cx="5" cy="6" r="1.8"/><circle cx="19" cy="7" r="1.8"/><circle cx="6.5" cy="18.5" r="1.8"/><circle cx="18" cy="17.5" r="1.8"/><path d="M6.4 7.2 10 10.3M17.4 8.3 14 10.5M7.7 17 10.4 13.9M16.6 16.3 13.8 13.6"/></svg>',
    brand: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5 19.5 6v6.1c0 4-3.1 7-7.5 8.4-4.4-1.4-7.5-4.4-7.5-8.4V6z"/><path d="m9.2 12 2 2 3.6-3.8"/></svg>',
    audiences: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="10.5" r="2.2"/><path d="M15.2 19a4.4 4.4 0 0 1 5.3-4.2"/></svg>',
    trends: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 16.5 9 11l3.5 3.5L20.5 6"/><path d="M15.5 6h5v5"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="6"/><path d="m15.5 15.5 4 4"/></svg>',
    ai: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5 13.6 8 18 9.6 13.6 11.2 12 15.6 10.4 11.2 6 9.6 10.4 8z"/><path d="M17.5 15.5 18.3 17.7 20.5 18.5 18.3 19.3 17.5 21.5 16.7 19.3 14.5 18.5 16.7 17.7z"/></svg>',
    question: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M5 12h12"/><path d="m13 8 4 4-4 4"/></svg>',
    chart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5h16"/><path d="M6.5 16V9.5M11 16V5.5M15.5 16v-8M20 16v-4"/></svg>',
    bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 16.5v-5a5.5 5.5 0 0 1 11 0v5l1.5 2H5z"/><path d="M10 19.8a2.2 2.2 0 0 0 4 0"/></svg>',
    layers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="m12 3.5 8 4-8 4-8-4z"/><path d="m4.5 12.2 7.5 3.8 7.5-3.8"/><path d="m4.5 16.4 7.5 3.8 7.5-3.8"/></svg>',
    panel: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="7" cy="8" r="2"/><circle cx="12" cy="15" r="2"/><circle cx="17" cy="7.5" r="2"/><path d="M8.6 9.4 10.5 13M13.9 13.7 15.7 9.3M9 8.2l6-.6"/></svg>'
  };

  /* One flagship question per family, for the nav panel. */
  var QUESTIONS = [
    "Analyze the impact of a campaign",
    "Monitor your brand reputation",
    "Segment your target profiles",
    "Test and evaluate your products"
  ];

  var MENUS = {
    "use-cases": {
      label: "FOUR FAMILIES OF QUESTIONS",
      items: [
        { icon: "influence", name: "Communication", href: "use-cases.html#communication",
          desc: "Campaign impact, leader advocacy, the right ambassadors." },
        { icon: "brand", name: "Brand health", href: "use-cases.html#brand-health",
          desc: "Image, messaging and the risks worth catching early." },
        { icon: "audiences", name: "Audiences", href: "use-cases.html#audiences",
          desc: "Segmentation, rejuvenation, expectations at every touchpoint." },
        { icon: "trends", name: "Trends & innovation", href: "use-cases.html#trends",
          desc: "Product verdicts, market opportunities, emerging topics." }
      ],
      aside: {
        label: "FLAGSHIP QUESTIONS",
        items: QUESTIONS.map(function (q, i) {
          var anchors = ["#communication", "#brand-health", "#audiences", "#trends"];
          return { icon: "question", name: q, href: "use-cases.html" + anchors[i] };
        })
      },
      cta: { label: "Book a meeting", href: "index.html#signup" },
      link: { label: "All twelve use cases", href: "use-cases.html" }
    },

    offers: {
      label: "THREE WAYS TO WORK WITH US",
      items: [
        { icon: "chart", name: "Social Insights", href: "offers.html#social-insights",
          desc: "Fixed fee, unlimited studies, no commitment." },
        { icon: "bell", name: "Vigie 360", href: "offers.html#vigie",
          desc: "Alerts in 15 minutes, 24/7, in 20+ languages." },
        { icon: "layers", name: "Social Listening as a Service", href: "offers.html#slaas",
          desc: "We make the platform you already own produce decisions." }
      ],
      aside: {
        label: "HOW AN ENGAGEMENT RUNS",
        items: [
          { icon: "question", name: "Framing", href: "offers.html#method" },
          { icon: "question", name: "Collection", href: "offers.html#method" },
          { icon: "question", name: "Analysis", href: "offers.html#method" },
          { icon: "question", name: "Decision", href: "offers.html#method" }
        ]
      },
      cta: { label: "Book a meeting", href: "index.html#signup" },
      link: { label: "Compare the offers", href: "offers.html" }
    },

    tech: {
      label: "THE PLATFORMS WE RUN",
      items: [
        { letter: "T", logo: "assets/img/tools/talkwalker.png", name: "Talkwalker", href: "tech-talkwalker.html",
          desc: "Broad listening and analytics, across markets and languages." },
        { letter: "V", logo: "assets/img/tools/visibrain.png", name: "Visibrain", href: "tech-visibrain.html",
          desc: "Real-time monitoring, and the media conversation as it breaks." },
        { letter: "Y", logo: "assets/img/tools/youscan.png", name: "YouScan", href: "tech-youscan.html",
          desc: "Visual listening: what appears in the image, not only in the text." },
        { letter: "S", logo: "assets/img/tools/soprism.png", name: "SoPrism", href: "tech-soprism.html",
          desc: "Audience intelligence: who the communities are, in detail." }
      ],
      aside: {
        label: "WHERE THE DATA COMES FROM",
        items: [
          { platform: "TIKTOK", name: "TikTok", href: "tech-tools.html#sources" },
          { platform: "INSTAGRAM", name: "Instagram", href: "tech-tools.html#sources" },
          { platform: "X", name: "X", href: "tech-tools.html#sources" },
          { platform: "LINKEDIN", name: "LinkedIn", href: "tech-tools.html#sources" },
          { platform: "YOUTUBE", name: "YouTube", href: "tech-tools.html#sources" },
          { platform: "FACEBOOK", name: "Facebook", href: "tech-tools.html#sources" },
          { icon: "ai", name: "Generative AI", href: "tech-tools.html#sources" }
        ]
      },
      cta: { label: "Book a meeting", href: "index.html#signup" },
      link: { label: "See the stack", href: "tech-tools.html" }
    }
  };

  function menuIcon(item) {
    if (item.platform) return window.LicterIcons[item.platform] || "";
    /* Third-party tool logos: dropped in assets/img/tools/. If a file is
       missing the monogram takes over, so the menu never shows a broken
       image. */
    if (item.logo) {
      return '<img class="menu__logo" src="' + item.logo + '" alt="' + item.name +
             '" loading="lazy" onerror="this.parentNode.innerHTML=&quot;' +
             '<span class=\\&quot;menu__mono\\&quot;>' + item.letter + '</span>&quot;" />';
    }
    if (item.letter) return '<span class="menu__mono">' + item.letter + "</span>";
    return ICONS[item.icon] || "";
  }

  function menuItem(item, compact, i) {
    return '<li style="--i:' + (i || 0) + '"><a class="menu__item' + (compact ? " menu__item--compact" : "") + '" href="' + item.href + '">' +
      '<span class="menu__icon" aria-hidden="true">' + menuIcon(item) + "</span>" +
      '<span class="menu__text"><span class="menu__name">' + item.name + "</span>" +
      (item.desc ? '<span class="menu__desc">' + item.desc + "</span>" : "") +
      "</span></a></li>";
  }

  function buildMenu(key, data) {
    var el = document.createElement("div");
    el.className = "menu";
    el.id = "menu-" + key;
    el.hidden = true;
    el.innerHTML =
      '<div class="menu__grid">' +
        '<div class="menu__main">' +
          '<p class="menu__label">' + data.label + "</p>" +
          '<ul class="menu__list">' +
            data.items.map(function (it, i) { return menuItem(it, false, i); }).join("") + "</ul>" +
        "</div>" +
        (data.aside ?
        '<div class="menu__aside">' +
          '<p class="menu__label">' + data.aside.label + "</p>" +
          '<ul class="menu__list menu__list--single">' +
            data.aside.items.map(function (it, i) { return menuItem(it, !it.desc, i + 2); }).join("") +
          "</ul>" +
        "</div>" : "") +
      "</div>" +
      '<div class="menu__foot">' +
        '<a class="menu__cta" href="' + data.cta.href + '">' + data.cta.label +
          ' <span aria-hidden="true">→</span></a>' +
        '<a class="menu__ghost" href="' + data.link.href + '">' + data.link.label + "</a>" +
      "</div>";
    return el;
  }

  (function navMenus() {
    var nav = document.getElementById("nav");
    if (!nav) return;

    var triggers = Array.prototype.slice.call(nav.querySelectorAll("[data-menu]"));
    var panels = {};
    var openKey = null;
    var timer = null;
    var canHover = window.matchMedia("(hover: hover)");

    triggers.forEach(function (btn) {
      var key = btn.dataset.menu;
      var panel = buildMenu(key, MENUS[key]);
      nav.appendChild(panel);
      panels[key] = panel;
    });

    function open(key) {
      if (openKey === key) return;
      close();
      var btn = triggers.filter(function (t) { return t.dataset.menu === key; })[0];
      panels[key].hidden = false;
      /* next frame, so the transition has a starting point */
      requestAnimationFrame(function () { panels[key].classList.add("is-open"); });
      btn.setAttribute("aria-expanded", "true");
      btn.classList.add("is-open");
      nav.classList.add("has-open-menu");
      openKey = key;
    }

    function close() {
      if (!openKey) return;
      var panel = panels[openKey];
      var btn = triggers.filter(function (t) { return t.dataset.menu === openKey; })[0];
      panel.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      btn.classList.remove("is-open");
      nav.classList.remove("has-open-menu");
      var closing = panel;
      setTimeout(function () { if (!closing.classList.contains("is-open")) closing.hidden = true; }, 180);
      openKey = null;
    }

    function delayedClose() {
      clearTimeout(timer);
      timer = setTimeout(close, 180);
    }

    triggers.forEach(function (btn) {
      var key = btn.dataset.menu;

      btn.addEventListener("click", function () {
        if (openKey === key) close(); else open(key);
      });

      btn.addEventListener("mouseenter", function () {
        if (!canHover.matches) return;
        clearTimeout(timer);
        timer = setTimeout(function () { open(key); }, 70);
      });
      btn.addEventListener("mouseleave", function () {
        if (!canHover.matches) return;
        clearTimeout(timer);
        delayedClose();
      });

      panels[key].addEventListener("mouseenter", function () {
        if (canHover.matches) clearTimeout(timer);
      });
      panels[key].addEventListener("mouseleave", function () {
        if (canHover.matches) delayedClose();
      });

      btn.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") {
          e.preventDefault();
          open(key);
          var first = panels[key].querySelector("a");
          if (first) first.focus();
        }
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" || !openKey) return;
      var btn = triggers.filter(function (t) { return t.dataset.menu === openKey; })[0];
      close();
      btn.focus();
    });

    /* clicking a link inside a panel, or anywhere outside the nav, closes it */
    nav.addEventListener("click", function (e) {
      if (e.target.closest(".menu")) close();
    });
    document.addEventListener("click", function (e) {
      if (openKey && !nav.contains(e.target)) close();
    });
    nav.addEventListener("focusout", function (e) {
      if (openKey && !nav.contains(e.relatedTarget)) close();
    });
    window.addEventListener("scroll", function () { if (openKey) close(); }, { passive: true });
  })();

  /* ---------------------------------------------------------- stories
     A traveller on the right-hand side of the hero occasionally opens into a
     story card: the moving point IS the story. The media slot is empty for
     now — drop a <video> in `renderMedia` when the clips are ready. */
  (function stories() {
    if (reduced.matches) return;
    var hero = document.querySelector(".hero");
    if (!hero || !window.matchMedia("(min-width: 901px)").matches) return;

    var layer = document.createElement("div");
    layer.className = "stories";
    layer.setAttribute("aria-hidden", "true");
    hero.appendChild(layer);

    var CAPTIONS = ["Story · 2 h", "Reel · 14 min", "Story · 47 min",
                    "Reel · 1 h", "Post · 3 h", "Story · 22 min"];
    var HOLD = 5200;        /* how long a card stays */
    var GAP = [3600, 7200]; /* pause between two cards */

    function renderMedia() {
      /* the slot: replace the inner span with <video …> when clips exist */
      return '<span class="story__play" aria-hidden="true">▶</span>';
    }

    function open() {
      /* Hard guard: any path that re-schedules (a visibility change, a failed
         attempt) could otherwise open a second card over the live one. */
      if (layer.children.length) return schedule();

      var r = hero.getBoundingClientRect();
      if (r.bottom < 120) return schedule();   /* hero scrolled away */

      var api = window.LicterCarto;
      /* the zone Licter marked out: right-hand side, from just under the
         navbar down to just above the clients band */
      var point = api && api.pickTraveller(
        r.left + r.width * 0.53, r.left + r.width * 0.97,
        r.top + r.height * 0.11, r.top + r.height * 0.77);
      if (!point) return schedule();

      var platform = point.platform || "INSTAGRAM";
      var card = document.createElement("figure");
      card.className = "story";
      card.style.setProperty("--hold", HOLD + "ms");
      card.style.setProperty("--story-color", point.color || "");
      card.innerHTML =
        '<span class="story__bar"><i></i></span>' +
        '<span class="story__head">' + (window.LicterIcons[platform] || "") +
          platform + "</span>" +
        '<span class="story__media">' + renderMedia() + "</span>" +
        '<figcaption class="story__cap">' +
          CAPTIONS[(Math.random() * CAPTIONS.length) | 0] + "</figcaption>";

      /* anchored beside the point, flipped when it would leave the hero */
      var W = 216, H = 190;
      var x = point.x - r.left + 34;
      var y = point.y - r.top;
      if (x + W + 12 > r.width) {
        x = point.x - r.left - 34 - W;
        card.classList.add("story--left");
      }
      card.style.left = Math.round(Math.max(12, x)) + "px";
      card.style.top = Math.round(Math.max(10, Math.min(r.height - H - 10, y - H / 2))) + "px";

      layer.appendChild(card);
      /* one card at a time: the next one is scheduled once this one is gone */
      setTimeout(function () {
        card.classList.add("is-out");
        setTimeout(function () { card.remove(); schedule(); }, 420);
      }, HOLD);
    }

    var timer = null;
    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(open, GAP[0] + Math.random() * (GAP[1] - GAP[0]));
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) clearTimeout(timer); else schedule();
    });
    setTimeout(open, 2600);
  })();

  /* ------------------------------------------------------------- veil
     The cartography is the hero's subject; below it, it is a texture behind
     text. A cream veil fades in as soon as the reading content starts, and
     pages without a hero start already veiled. */
  (function veil() {
    var hero = document.querySelector(".hero");
    var body = document.body;

    if (!hero) { body.style.setProperty("--veil", "0.28"); return; }

    var raf = null, last = -1;
    function apply() {
      raf = null;
      var h = window.innerHeight;
      var v = Math.max(0, Math.min(1, (window.scrollY - h * 0.25) / (h * 0.5))) * 0.3;
      v = Math.round(v * 100) / 100;
      if (v === last) return;
      last = v;
      body.style.setProperty("--veil", v);
    }
    window.addEventListener("scroll", function () {
      if (!raf) raf = requestAnimationFrame(apply);
    }, { passive: true });
    window.addEventListener("resize", apply);
    apply();
  })();

  /* ---------------------------------------------------------- reveals
     Hero blocks play on load, the rest as they scroll in. The hiding rule
     lives behind `html.reveal`, added here: if this script never runs, or
     motion is reduced, the page simply renders in place. */
  (function reveals() {
    if (reduced.matches) return;

    var root = document.documentElement;
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
    if (!items.length) return;
    root.classList.add("reveal");

    Array.prototype.forEach.call(document.querySelectorAll(".questions li"),
      function (li, i) { li.style.setProperty("--i", i); });

    function show(el, delay) {
      if (el.classList.contains("is-in")) return;
      el.style.setProperty("--d", (delay || 0).toFixed(2) + "s");
      el.classList.add("is-in");
    }

    var hero = [], rest = [];
    items.forEach(function (el) {
      (el.closest(".hero") ? hero : rest).push(el);
    });

    /* two frames, so the hidden state is committed before the transition */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        hero.forEach(function (el, i) { show(el, 0.06 + i * 0.09); });
      });
    });

    function reveal(el) {
      var group = rest.indexOf(el);
      show(el, Math.max(0, group % 3) * 0.06);
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          reveal(entry.target);
          io.unobserve(entry.target);
        });
      }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
      rest.forEach(function (el) { io.observe(el); });
    }

    function sweep() {
      var pending = false;
      rest.forEach(function (el) {
        if (el.classList.contains("is-in")) return;
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight * 0.9 && r.bottom > 0) reveal(el);
        else pending = true;
      });
      if (!pending) window.removeEventListener("scroll", sweep);
    }
    window.addEventListener("scroll", sweep, { passive: true });
    sweep();

    /* last resort: nothing stays hidden */
    setTimeout(function () { rest.forEach(function (el) { show(el, 0); }); }, 6000);
  })();

  /* ------------------------------------------------------------------ form */

  /* funnel forms: guide, diagnostic, meeting */
  Array.prototype.forEach.call(document.querySelectorAll(".form"), function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fields = form.querySelectorAll("input[required], textarea[required]");
      var firstBad = null;
      Array.prototype.forEach.call(fields, function (f) {
        var v = f.value.trim();
        var ok = f.type === "email"
          ? /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)
          : v.length > 1;
        f.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !firstBad) firstBad = f;
      });
      if (firstBad) { firstBad.focus(); return; }
      /* wire to the real endpoint here */
      form.classList.add("is-sent");
    });
  });

  /* every capture form on the site, hero and page footers alike */
  Array.prototype.forEach.call(document.querySelectorAll(".signup"), function (form) {
    var note = form.parentNode.querySelector(".signup__note");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var field = form.querySelector(".signup__input");
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(field.value.trim());
      field.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok) { field.focus(); return; }
      /* wire to the real endpoint here */
      if (note) note.classList.add("is-visible");
      field.value = "";
      field.blur();
    });
  });
})();

/* =========================================================================
   Cover artwork
   A cover with nothing in it reads as an image that failed to load. Each one
   gets a small community drawn in the vocabulary of the map behind the page:
   a hub, a ring of nodes at comparable radius so no two spokes cross, and a
   few anonymous points. The seed is the card's own title, so a given card
   always draws the same cluster.
   ========================================================================= */
(function () {
  var covers = document.querySelectorAll(".cover");
  if (!covers.length) return;

  function seeded(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = (h * 16777619) >>> 0;
    }
    return function () {
      h = (h * 1664525 + 1013904223) >>> 0;
      return h / 4294967296;
    };
  }

  function cluster(seed) {
    var rnd = seeded(seed);
    var cx = 50, cy = 50, r = 27;
    var n = 5 + ((rnd() * 3) | 0);
    var start = rnd() * 360;
    var pts = [], lines = [], dots = [];

    for (var i = 0; i < n; i++) {
      var a = (start + (360 / n) * i + (rnd() * 26 - 13)) * Math.PI / 180;
      var d = r * (0.84 + rnd() * 0.32);
      pts.push([cx + Math.cos(a) * d, cy + Math.sin(a) * d]);
    }
    pts.forEach(function (p) { lines.push([cx, cy, p[0], p[1]]); });
    for (var k = 0; k < n - 1; k++) {
      if (rnd() < 0.55) lines.push([pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1]]);
    }
    for (var j = 0; j < 4; j++) {
      var aa = (start + rnd() * 360) * Math.PI / 180;
      var dd = r * (0.45 + rnd() * 0.95);
      var dx = cx + Math.cos(aa) * dd, dy = cy + Math.sin(aa) * dd;
      dots.push([dx, dy]);
      lines.push([cx, cy, dx, dy]);
    }

    var f = function (v) { return Math.round(v * 10) / 10; };
    var d = lines.map(function (l) {
      return "M" + f(l[0]) + " " + f(l[1]) + "L" + f(l[2]) + " " + f(l[3]);
    }).join(" ");

    var out = '<svg class="cover__art" viewBox="0 0 100 100" aria-hidden="true" focusable="false">';
    out += '<path class="l" d="' + d + '"/>';
    out += '<circle class="h" cx="' + cx + '" cy="' + cy + '" r="2.6"/>';
    pts.forEach(function (p) {
      out += '<circle class="n" cx="' + f(p[0]) + '" cy="' + f(p[1]) + '" r="' + f(1 + rnd() * .9) + '"/>';
    });
    dots.forEach(function (p) {
      out += '<circle class="n" cx="' + f(p[0]) + '" cy="' + f(p[1]) + '" r=".8" opacity=".6"/>';
    });
    return out + "</svg>";
  }

  Array.prototype.forEach.call(covers, function (cover) {
    if (cover.querySelector(".cover__art")) return;
    var title = cover.querySelector(".cover__title");
    cover.insertAdjacentHTML("afterbegin", cluster(title ? title.textContent : cover.textContent));
  });
})();

/* =========================================================================
   Client wall — the caption wave, driven by the beam's own clock
   The beam is a CSS animation, so rather than keeping a second timer in step
   we read its currentTime straight off the Web Animations object. The wave
   then sweeps the words exactly while the beam is behind them.
   ========================================================================= */
(function () {
  var wall = document.getElementById("wall");
  var beam = document.getElementById("wall-beam");
  var wave = document.getElementById("wall-wave");
  if (!wall || !beam || !wave) return;

  /* offset-path is what carries the beam; without it there is nothing to sync */
  var rides = window.CSS && CSS.supports && CSS.supports("offset-path", "rect(0 100% 100% 0)");
  if (!rides) { wall.classList.add("no-beam"); return; }

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduced.matches) return;

  var caption = wave.parentNode;
  var anim = null, visible = false, running = false;

  function clock() {
    if (anim && anim.currentTime !== null) return anim.currentTime;
    var list = beam.getAnimations ? beam.getAnimations() : [];
    anim = list[0] || null;
    return anim && anim.currentTime !== null ? anim.currentTime : 0;
  }

  function frame() {
    if (!visible) { running = false; return; }

    var dur = (anim && anim.effect && anim.effect.getTiming().duration) || 8000;
    var offset = ((clock() % dur) / dur) * 100;          /* 0–100 of the perimeter */

    var card = wall.getBoundingClientRect();
    var text = caption.getBoundingClientRect();
    var perimeter = 2 * (card.width + card.height);
    if (!perimeter) { requestAnimationFrame(frame); return; }

    /* the caption sits on the top edge, so its span maps straight onto the
       first stretch of the perimeter */
    var start = (Math.max(0, text.left - card.left) / perimeter) * 100;
    var end = (Math.min(card.width, text.right - card.left) / perimeter) * 100;

    var pos;
    if (offset >= start && offset <= end) {
      var t = (offset - start) / (end - start || 1);
      pos = 95 - t * 90;                                  /* 95% → 5% */
    } else {
      pos = offset < start ? 0 : 100;                     /* parked, plain colour */
    }
    wave.style.backgroundPosition = pos + "% center";

    requestAnimationFrame(frame);
  }

  function start() {
    if (running || !visible) return;
    running = true;
    requestAnimationFrame(frame);
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible = e.isIntersecting; });
      start();
    }, { threshold: 0.1 }).observe(wall);
  } else {
    visible = true;
    start();
  }
})();
