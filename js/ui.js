/* =========================================================================
   Where the use-case pages live, in the visitor's language. They are
   generated in both (tools/build-usecases.py); the rest of the site links
   to the right twin.
   ========================================================================= */
window.LicterUC = (function () {
  var h = document.documentElement, lang = "fr";
  if (h.hasAttribute("data-i18n-static")) lang = h.lang;
  else { try { lang = localStorage.getItem("licter-lang") || "fr"; } catch (e) { lang = "fr"; } }
  var P = {
    fr: { hub: "/fr/cas-usage/", communication: "/fr/cas-usage/communication/", brand: "/fr/cas-usage/sante-de-marque/",
          audiences: "/fr/cas-usage/audiences/", trends: "/fr/cas-usage/tendances-innovation/",
          "campaign-impact": "/fr/cas-usage/communication/mesurer-impact-campagne/",
          reputation: "/fr/cas-usage/sante-de-marque/e-reputation-image-de-marque/",
          segmentation: "/fr/cas-usage/audiences/segmentation-cibles/",
          "product-test": "/fr/cas-usage/tendances-innovation/tester-evaluer-produits/",
          "market-opportunities": "/fr/cas-usage/tendances-innovation/analyse-marche-opportunites/" },
    en: { hub: "/en/use-cases/", communication: "/en/use-cases/communication/", brand: "/en/use-cases/brand-health/",
          audiences: "/en/use-cases/audiences/", trends: "/en/use-cases/trends-innovation/",
          "campaign-impact": "/en/use-cases/communication/measure-campaign-impact/",
          reputation: "/en/use-cases/brand-health/brand-reputation-monitoring/",
          segmentation: "/en/use-cases/audiences/audience-segmentation/",
          "product-test": "/en/use-cases/trends-innovation/product-testing/",
          "market-opportunities": "/en/use-cases/trends-innovation/market-opportunities/" }
  };
  return function (key) { return (P[lang] || P.fr)[key || "hub"]; };
})();

/* =========================================================================
   Licter — page behaviour: logo crop, client marquee, use-case tabs, form.
   ========================================================================= */
/* =========================================================================
   The visitor's contact, once given anywhere on the site, is remembered for
   the session: the other forms prefill it, one-click offers use it, and the
   guide bar stops asking. MOCK: kept in the browser only; the CRM is the
   real record once wired.
   ========================================================================= */
(function () {
  var KEY = "licter-lead", subs = [];
  window.LicterLead = {
    get: function () { try { return sessionStorage.getItem(KEY) || ""; } catch (e) { return ""; } },
    set: function (v) {
      try { sessionStorage.setItem(KEY, v); } catch (e) { /* private mode */ }
      subs.forEach(function (fn) { fn(v); });
    },
    on: function (fn) { subs.push(fn); }
  };
})();

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
     Official marks (Wikimedia Commons / Wikipedia), cropped to their ink and
     sized to a common visual area so no brand shouts over the others. Shown in
     grey; colour returns on hover. Licter must hold each client's agreement to
     display its logo. Sources: assets/img/clients/SOURCES.md */
  var CLIENTS = [
    { name: "HP",                  src: "/assets/img/clients/hp.svg", w:  46, h: 46 },
    { name: "DECATHLON",           src: "/assets/img/clients/decathlon.svg", w: 119, h: 19 },
    { name: "UNESCO",              src: "/assets/img/clients/unesco.svg", w:  55, h: 42 },
    { name: "L'ORÉAL",             src: "/assets/img/clients/loreal.svg", w: 110, h: 21 },
    { name: "DANONE",              src: "/assets/img/clients/danone.png", w:  41, h: 46 },
    { name: "SOCIÉTÉ GÉNÉRALE",    src: "/assets/img/clients/societegenerale.svg", w:  98, h: 23 },
    { name: "GALERIES LAFAYETTE",  src: "/assets/img/clients/galerieslafayette.svg", w:  66, h: 35 },
    { name: "CELIO",               src: "/assets/img/clients/celio.svg", w:  84, h: 27 },
    { name: "LA POSTE",            src: "/assets/img/clients/laposte.svg", w: 120, h: 19 },
    { name: "SISLEY",              src: "/assets/img/clients/sisley.svg", w: 168, h: 12 },
    { name: "BOUYGUES TELECOM",    src: "/assets/img/clients/bouygues.svg", w:  85, h: 27 },
    { name: "STUDI",               src: "/assets/img/clients/studi.svg", w:  80, h: 29 },
    { name: "TV5 MONDE",           src: "/assets/img/clients/tv5monde.svg", w:  83, h: 28 },
    { name: "PMU",                 src: "/assets/img/clients/pmu.svg", w:  77, h: 30 },
    { name: "LA MARINE RECRUTE",   src: "/assets/img/clients/marine.svg", w:  31, h: 46, label: "Marine nationale" },
    { name: "BIOPARC",             src: "/assets/img/clients/bioparc.png", w:  64, h: 36, label: "Bioparc de Doué La Fontaine" }
  ];
  var GAP = 44;
  /* px per second the logo band travels. It ran at 126, which reads as a
     ticker rather than a wall of names you have time to recognise. */
  var MARQUEE_SPEED = 45;

  function markFor(c, hidden) {
    return '<img src="' + c.src + '" alt="' + (hidden ? "" : (c.label || c.name)) +
      '" width="' + c.w + '" height="' + c.h + '" loading="lazy" decoding="async" />';
  }

  function buildMarquee() {
    var track = document.getElementById("marquee-track");
    if (!track) return;

    /* same scale-up as the rest of the hero past the reference width */
    var k = Math.min(1.28, Math.max(1, window.innerWidth / 1247)) * 0.88;
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
                'px"' + (r === 0 ? "" : ' aria-hidden="true"') + ">" + markFor(c, r > 0) + "</span>";
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
      /* one height for the grid, scaled from the marquee size */
      var k = 1.15;
      return '<li><img class="wall-logo" src="' + c.src + '" alt="' + (c.label || c.name) +
             '" width="' + Math.round(c.w * k) + '" height="' + Math.round(c.h * k) + '" loading="lazy" decoding="async" /></li>';
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
    FACEBOOK: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M14.3 8.2h-1.2a1.8 1.8 0 0 0-1.8 1.8V20M9.7 12.6h4.4"/></svg>',
    TWITCH: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M5 3.5h15.5v10.5l-4.5 4.5h-4l-3 3v-3H5.5z"/><path d="M11 8v4M15.5 8v4"/></svg>'
  };

  /* ------------------------------------------------------------ use cases */

  /* Every figure in this console is illustrative — a plausible read, not a
     client result. Licter has to replace them before this goes live. */
  var CASES = {
    communication: {
      family: "COMMUNICATION",
      label: "CAMPAIGN IMPACT · SHARE OF VOICE",
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
      anchor: LicterUC("communication"),
      questions: [
        "Analyse the impact of an event or campaign",
        "Optimise your leader advocacy strategy",
        "Identify the right ambassadors"
      ]
    },
    brand: {
      family: "BRAND HEALTH",
      label: "BRAND HEALTH · NET SENTIMENT",
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
      anchor: LicterUC("brand"),
      questions: [
        "Monitor your brand image and reputation",
        "Develop your brand messaging",
        "Identify and mitigate brand risks"
      ]
    },
    audiences: {
      family: "AUDIENCES",
      label: "CORE TARGET · QUALIFIED REACH",
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
      anchor: LicterUC("audiences"),
      questions: [
        "Segment your target profiles",
        "Rejuvenate your audiences",
        "Understand expectations at every touchpoint"
      ]
    },
    trends: {
      family: "INNOVATION",
      label: "EMERGING TOPICS · VELOCITY",
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
      anchor: LicterUC("trends"),
      questions: [
        "Test and evaluate your products",
        "Analyse markets and identify opportunities",
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

  /* MOCK: example readouts, one per family. Illustrative findings, not a
     client result. They replace the old dashboard (invented KPIs on a fake
     screen) with what a client actually receives: a question, what the data
     said, and the decision it informed. Replace with approved, anonymised
     readouts before this goes live. */
  var READOUTS = {
    communication: {
      question: "Did the spring campaign move anything beyond the paid reach?",
      findings: [
        "Creators carried most of the reach. The brand's own posts, very little.",
        "The conversation spread into two communities the brief had not targeted.",
        "Paid amplification stopped adding reach after the third week."
      ],
      decision: "Move a third of the paid budget to creator partnerships for the autumn launch."
    },
    brand: {
      question: "Is the drop in sentiment a crisis, or a bad week?",
      findings: [
        "Negative posts tripled, but most of them came from a single community.",
        "Search interest in the brand did not move.",
        "The complaint was about delivery times, not the product."
      ],
      decision: "Fix the delivery message. No crisis communication needed."
    },
    audiences: {
      question: "Who is our core target, really?",
      findings: [
        "The buyers are about ten years younger than the brand's personas.",
        "They follow cooking creators, not fashion ones.",
        "They ask generative AI for a recommendation before they search."
      ],
      decision: "Rebuild the personas and move the media plan toward food creators."
    },
    trends: {
      question: "Is the high-protein trend worth a product line?",
      findings: [
        "Mentions have grown steadily for eighteen months, in three countries.",
        "The topic moved from gym communities to parents.",
        "The unmet need is taste, not protein content."
      ],
      decision: "Launch a pilot range in one market, positioned on taste."
    }
  };

  function renderViz(key) {
    if (!viz) return;
    var d = CASES[key];
    var r = READOUTS[key];

    viz.innerHTML =
      '<div class="viz__head">' +
        '<div class="viz__id"><span class="viz__dot" aria-hidden="true"></span>' +
          '<span class="viz__label">' + d.family + "</span></div>" +
        '<span class="readout__tag">Example readout</span>' +
      "</div>" +
      '<div class="readout">' +
        '<p class="readout__k">The question</p>' +
        '<p class="readout__q">' + r.question + "</p>" +
        '<p class="readout__k">What the data said</p>' +
        '<ol class="readout__list">' + r.findings.map(function (f, i) {
          return '<li style="--i:' + i + '">' + f + "</li>";
        }).join("") + "</ol>" +
        '<p class="readout__k">The decision it informed</p>' +
        '<p class="readout__d">' + r.decision + "</p>" +
      "</div>" +
      '<figcaption class="viz__foot">Illustrative example. Every readout is written by the analyst who ran the study.</figcaption>';
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
    "Analyse the impact of a campaign",
    "Monitor your brand reputation",
    "Segment your target profiles",
    "Test and evaluate your products"
  ];

  var MENUS = {
    "use-cases": {
      label: "FOUR FAMILIES OF QUESTIONS",
      items: [
        { icon: "influence", name: "Communication", href: LicterUC("communication"),
          desc: "Campaign impact, leader advocacy, the right ambassadors." },
        { icon: "brand", name: "Brand health", href: LicterUC("brand"),
          desc: "Image, messaging and the risks worth catching early." },
        { icon: "audiences", name: "Audiences", href: LicterUC("audiences"),
          desc: "Segmentation, rejuvenation, expectations at every touchpoint." },
        { icon: "trends", name: "Trends & innovation", href: LicterUC("trends"),
          desc: "Product verdicts, market opportunities, emerging topics." }
      ],
      aside: {
        label: "FLAGSHIP QUESTIONS",
        items: QUESTIONS.map(function (q, i) {
          var cases = ["campaign-impact", "reputation", "segmentation", "product-test"];
          return { icon: "question", name: q, href: LicterUC(cases[i]) };
        })
      },
      cta: { label: "Book a meeting", href: "/index.html#book" },
      link: { label: "All twelve use cases", href: LicterUC() }
    },

    expertise: {
      label: "SOCIAL INTELLIGENCE",
      items: [
        { icon: "chart", name: "Social listening", href: "/expertise-social-listening.html",
          desc: "What is said about you, your competitors and your market." },
        { icon: "audiences", name: "Audience listening", href: "/expertise-audience-listening.html",
          desc: "Who the people talking about you really are." },
        { icon: "influence", name: "Influence listening", href: "/expertise-influence-listening.html",
          desc: "The voices that actually carry in your category." },
        { icon: "ai", name: "AI listening", href: "/expertise-ai-listening.html",
          desc: "What generative AI says about your brand." },
        { icon: "bell", name: "Live listening", href: "/expertise-live-listening.html",
          desc: "The conversation in real time, an alert within 15 minutes." },
        { icon: "search", name: "Search listening", href: "/expertise-search-listening.html",
          desc: "What people search for on Google, YouTube and Amazon." }
      ],
      aside: {
        label: "IN OUR OFFERS",
        items: [
          { icon: "chart", name: "Social Insights", href: "/offer-social-insights.html" },
          { icon: "bell", name: "Vigie 360", href: "/offer-vigie-360.html" },
          { icon: "layers", name: "Social Listening as a Service", href: "/offer-slaas.html" },
          { icon: "ai", name: "Nox", href: "/offer-nox.html" }
        ]
      },
      cta: { label: "Book a meeting", href: "/index.html#book" },
      link: { label: "All our expertise", href: "/expertise.html" }
    },

    offers: {
      label: "FOUR WAYS TO WORK WITH US",
      items: [
        { icon: "chart", name: "Social Insights", href: "/offer-social-insights.html",
          desc: "Fixed fee, unlimited studies, no commitment." },
        { icon: "bell", name: "Vigie 360", href: "/offer-vigie-360.html",
          desc: "Alerts in 15 minutes, 24/7, in 20+ languages." },
        { icon: "layers", name: "Social Listening as a Service", href: "/offer-slaas.html",
          desc: "We make the platform you already own produce decisions." },
        { icon: "ai", name: "Nox", href: "/offer-nox.html",
          desc: "AI-assisted monitoring, tuned by our analysts." }
      ],
      aside: {
        label: "HOW AN ENGAGEMENT RUNS",
        items: [
          { icon: "question", name: "Framing", href: "/offers.html#method" },
          { icon: "question", name: "Collection", href: "/offers.html#method" },
          { icon: "question", name: "Analysis", href: "/offers.html#method" },
          { icon: "question", name: "Decision", href: "/offers.html#method" }
        ]
      },
      cta: { label: "Book a meeting", href: "/index.html#book" },
      link: { label: "Compare the offers", href: "/offers.html" }
    },

    tech: {
      label: "THE PLATFORMS WE RUN",
      items: [
        { letter: "T", logo: "/assets/img/tools/talkwalker.png", name: "Talkwalker", href: "/tech-talkwalker.html",
          desc: "Broad listening and analytics, across markets and languages." },
        { letter: "V", logo: "/assets/img/tools/visibrain.png", name: "Visibrain", href: "/tech-visibrain.html",
          desc: "Real-time monitoring, and the media conversation as it breaks." },
        { letter: "Y", logo: "/assets/img/tools/youscan.png", name: "YouScan", href: "/tech-youscan.html",
          desc: "Visual listening: what appears in the image, not only in the text." },
        { letter: "S", logo: "/assets/img/tools/soprism.png", name: "SoPrism", href: "/tech-soprism.html",
          desc: "Audience intelligence: who the communities are, in detail." }
      ],
      aside: {
        label: "WHERE THE DATA COMES FROM",
        items: [
          { platform: "TIKTOK", name: "TikTok", href: "/tech-tools.html#sources" },
          { platform: "INSTAGRAM", name: "Instagram", href: "/tech-tools.html#sources" },
          { platform: "X", name: "X", href: "/tech-tools.html#sources" },
          { platform: "LINKEDIN", name: "LinkedIn", href: "/tech-tools.html#sources" },
          { platform: "YOUTUBE", name: "YouTube", href: "/tech-tools.html#sources" },
          { platform: "FACEBOOK", name: "Facebook", href: "/tech-tools.html#sources" },
          { icon: "ai", name: "Generative AI", href: "/tech-tools.html#sources" }
        ]
      },
      cta: { label: "Book a meeting", href: "/index.html#book" },
      link: { label: "See the stack", href: "/tech-tools.html" }
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

      /* the item is a link to its own page: a click goes there. The menu
         opens on hover, and from the keyboard with the down arrow. */

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
  /* Off until the clips exist: an empty media slot on the first screen
     reads as a placeholder. Set to true once renderMedia returns a video. */
  var STORIES_READY = false;

  (function stories() {
    if (!STORIES_READY || reduced.matches) return;
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
  Array.prototype.forEach.call(document.querySelectorAll(".signup"), function (form, n) {
    var note = form.parentNode.querySelector(".signup__note");
    var field = form.querySelector(".signup__input");
    /* a red border alone does not say what is wrong */
    var error = document.createElement("p");
    error.className = "signup__error";
    error.id = "signup-error-" + n;
    error.setAttribute("role", "alert");
    error.hidden = true;
    error.textContent = "Enter a work email, like name@company.com.";
    form.parentNode.insertBefore(error, form.nextSibling);
    field.setAttribute("aria-describedby", error.id);
    field.addEventListener("input", function () {
      if (error.hidden) return;
      error.hidden = true;
      field.setAttribute("aria-invalid", "false");
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(field.value.trim());
      field.setAttribute("aria-invalid", ok ? "false" : "true");
      error.hidden = ok;
      if (!ok) { field.focus(); return; }
      /* wire to the real endpoint here */
      if (window.LicterLead) window.LicterLead.set(field.value.trim());
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

/* =========================================================================
   Guide bar (home)
   The guide is offered once the visitor has read something: it slides in
   when the use cases reach the screen, steps aside at the footer (which has
   its own sign-up), and stays gone for the session once closed.
   ========================================================================= */
(function () {
  var bar = document.getElementById("guide-bar");
  if (!bar || !("IntersectionObserver" in window)) return;
  var KEY = "licter-guide-bar";
  try { if (sessionStorage.getItem(KEY) === "closed") return; } catch (e) {}
  /* someone who has already left an email is not asked again */
  if (window.LicterLead && window.LicterLead.get()) return;

  /* after the first proof, not over the use cases the visitor is reading */
  var trigger = document.getElementById("case") || document.getElementById("use-cases");
  var foot = document.querySelector(".site-foot");
  var reached = false, atFoot = false, closed = false;

  function render() { bar.classList.toggle("is-shown", reached && !atFoot && !closed); }

  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.target === trigger && (e.isIntersecting || e.boundingClientRect.top < 0)) reached = true;
    });
    render();
  }, { threshold: 0 }).observe(trigger || document.body);
  /* it also steps aside where the page makes the same offer itself */
  var zones = [foot, document.getElementById("hero"), document.getElementById("guide"), document.getElementById("book"), document.getElementById("use-cases"), document.getElementById("diagnostic")].filter(Boolean);
  var inZone = {};
  if (zones.length) {
    var zio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { inZone[e.target.id || "foot"] = e.isIntersecting; });
      atFoot = Object.keys(inZone).some(function (k) { return inZone[k]; });
      render();
    });
    zones.forEach(function (z) { zio.observe(z); });
  }

  if (window.LicterLead) window.LicterLead.on(function () { closed = true; render(); });

  bar.querySelector(".banner__close").addEventListener("click", function () {
    closed = true;
    render();
    try { sessionStorage.setItem(KEY, "closed"); } catch (e) {}
  });
})();

/* =========================================================================
   Mobile menu
   Under 860px the nav folds behind one button, so the first screen of every
   page shows the page, not two rows of links.
   ========================================================================= */
(function () {
  var top = document.querySelector(".hero__top");
  var nav = document.getElementById("nav");
  if (!top || !nav) return;

  var btn = document.createElement("button");
  btn.className = "nav__toggle";
  btn.type = "button";
  btn.setAttribute("aria-controls", "nav");
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-label", "Menu");
  btn.innerHTML = '<span class="nav__bars" aria-hidden="true"><i></i><i></i></span>';
  top.insertBefore(btn, nav);

  function set(open) {
    top.classList.toggle("is-nav-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { set(!top.classList.contains("is-nav-open")); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && top.classList.contains("is-nav-open")) { set(false); btn.focus(); }
  });
  /* a link inside the page (#book, #diagnostic) closes the menu on its way */
  nav.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (a && a.getAttribute("href").indexOf("#") !== -1) set(false);
  });
})();

/* =========================================================================
   Footer on a phone: each column folds behind its title (one open at a
   time); above 720 px everything is back as it was.
   ========================================================================= */
(function () {
  var foot = document.querySelector(".site-foot");
  if (!foot || !window.matchMedia) return;
  var cols = Array.prototype.filter.call(foot.querySelectorAll(".site-foot__in > div"), function (d) {
    return d.querySelector(":scope > h3") && d.querySelector(":scope > ul");
  });
  if (!cols.length) return;
  var mq = window.matchMedia("(max-width: 720px)"), on = false;
  function fold() {
    if (on) return; on = true;
    foot.classList.add("is-folding");
    cols.forEach(function (d, i) {
      var h = d.querySelector(":scope > h3"), ul = d.querySelector(":scope > ul");
      if (!ul.id) ul.id = "foot-col-" + i;
      var b = document.createElement("button");
      b.type = "button"; b.className = "site-foot__toggle";
      b.setAttribute("aria-expanded", "false"); b.setAttribute("aria-controls", ul.id);
      while (h.firstChild) b.appendChild(h.firstChild);
      h.appendChild(b);
      ul.hidden = true;
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") !== "true";
        cols.forEach(function (o) {
          var ob = o.querySelector(".site-foot__toggle"), ou = o.querySelector(":scope > ul");
          if (ob) ob.setAttribute("aria-expanded", "false");
          ou.hidden = true;
        });
        b.setAttribute("aria-expanded", open ? "true" : "false");
        ul.hidden = !open;
      });
    });
  }
  function unfold() {
    if (!on) return; on = false;
    foot.classList.remove("is-folding");
    cols.forEach(function (d) {
      var h = d.querySelector(":scope > h3"), b = h.querySelector(".site-foot__toggle");
      if (b) { while (b.firstChild) h.insertBefore(b.firstChild, b); b.remove(); }
      d.querySelector(":scope > ul").hidden = false;
    });
  }
  function apply() { if (mq.matches) fold(); else unfold(); }
  apply();
  if (mq.addEventListener) mq.addEventListener("change", apply); else mq.addListener(apply);
})();

/* =========================================================================
   Compact bar
   Once the header has scrolled away, scrolling back up brings a slim bar
   with the logo and the one action that matters. It stays out of the way
   while reading down, and where the page already shows the booking.
   ========================================================================= */
(function () {
  var head = document.querySelector(".hero__top");
  var cta = head && head.querySelector(".nav__cta");
  if (!head || !("IntersectionObserver" in window)) return;
  /* the home has no header button (the hero carries it): book is on the page */
  var ctaHref = cta ? cta.getAttribute("href") : (document.getElementById("book") ? "#book" : "/book-a-meeting.html");

  var bar = document.createElement("div");
  bar.className = "stickybar";
  bar.setAttribute("aria-hidden", "true");
  var logo = head.querySelector(".logo");
  bar.innerHTML =
    '<div class="stickybar__in shell">' +
      '<a class="stickybar__logo" href="' + (logo ? logo.getAttribute("href") : "/index.html") + '" tabindex="-1" aria-label="Licter home">' +
        '<img src="' + (document.querySelector(".logo__img") || {}).getAttribute("src") + '" alt="" width="36" height="40" /></a>' +
      '<a class="btn btn--primary stickybar__cta" href="' + ctaHref + '" tabindex="-1">' +
        (document.body.classList.contains("home") ? "Talk to a consultant" : "Book a meeting") + ' <span aria-hidden="true">→</span></a>' +
    "</div>";
  document.body.appendChild(bar);
  /* home, phone: Antoine rides in the bar instead of floating over the text */
  if (document.body.classList.contains("home")) {
    var chat = document.createElement("button");
    chat.type = "button"; chat.className = "stickybar__chat"; chat.tabIndex = -1;
    chat.innerHTML = '<img src="/assets/img/team/founder-antoine-160.webp" alt="" width="44" height="44" /><i aria-hidden="true"></i>';
    var chatLabel = function () { chat.setAttribute("aria-label", document.documentElement.lang === "fr" ? "Discuter avec Antoine" : "Chat with Antoine"); };
    chatLabel();
    new MutationObserver(chatLabel).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    chat.addEventListener("click", function () { if (window.LicterChat) window.LicterChat.open(); });
    bar.querySelector(".stickybar__in").insertBefore(chat, bar.querySelector(".stickybar__cta"));
    /* and the magazine, once its popup was closed without sending: the cover
       sits in the bar rather than floating over the text */
    var mag = document.createElement("button");
    mag.type = "button"; mag.className = "stickybar__mag"; mag.tabIndex = -1;
    mag.innerHTML = '<img src="/assets/img/magazine/audience-first-ed2-440.webp" alt="" width="440" height="640" />';
    var magLabel = function () { mag.setAttribute("aria-label", document.documentElement.lang === "fr" ? "Audience First, le magazine gratuit" : "Audience First, the free magazine"); };
    magLabel();
    new MutationObserver(magLabel).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    mag.addEventListener("click", function () { if (window.LicterPopups) window.LicterPopups.open("mag"); });
    bar.querySelector(".stickybar__in").insertBefore(mag, chat);
  }

  var headGone = false, inBook = false, lastY = window.scrollY, up = false, ticking = false;
  /* on a phone or a tablet (< 1200 px, no room for the button in the header)
     the home pins it at the bottom, under the thumb, and keeps it there from
     the end of the hero to the booking form */
  var thumb = document.body.classList.contains("home") && window.matchMedia ? window.matchMedia("(max-width: 1199px)") : null;
  if (thumb) {
    var mode = function () { bar.classList.toggle("stickybar--bottom", thumb.matches); render(); };
    if (thumb.addEventListener) thumb.addEventListener("change", mode); else thumb.addListener(mode);
    bar.classList.toggle("stickybar--bottom", thumb.matches);
  }

  function render() {
    var on = headGone && (up || (thumb && thumb.matches)) && !inBook;
    bar.classList.toggle("is-shown", on);
    bar.setAttribute("aria-hidden", on ? "false" : "true");
    Array.prototype.forEach.call(bar.querySelectorAll("a, button"), function (a) { a.tabIndex = on ? 0 : -1; });
  }

  new IntersectionObserver(function (e) { headGone = !e[0].isIntersecting; render(); }).observe(head);
  var book = document.getElementById("book");
  if (book) new IntersectionObserver(function (e) { inBook = e[0].isIntersecting; render(); }).observe(book);

  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY;
      if (Math.abs(y - lastY) > 6) { up = y < lastY; lastY = y; render(); }
      ticking = false;
    });
  }, { passive: true });
})();

/* =========================================================================
   English home, French browser: offer the French site in a banner rather
   than redirecting (search engines are told by hreflang, not by a redirect).
   Once closed or chosen, it does not come back.
   ========================================================================= */
(function () {
  var h = document.documentElement;
  if (!h.hasAttribute("data-i18n-static") || h.lang !== "en") return;
  var alt = h.getAttribute("data-alt-fr");
  if (!alt || !/^fr\b/i.test(navigator.language || "")) return;
  var KEY = "licter-fr-offer";
  try { if (localStorage.getItem("licter-lang") === "en" || localStorage.getItem(KEY)) return; } catch (e) { return; }
  var bar = document.createElement("aside");
  bar.className = "langoffer";
  bar.setAttribute("lang", "fr");
  bar.setAttribute("aria-label", "Langue");
  bar.innerHTML = '<a class="langoffer__go" href="' + alt + '">Voir le site en français <span aria-hidden="true">→</span></a>' +
    '<button class="langoffer__x" type="button" aria-label="Fermer">×</button>';
  /* after the skip link, which has to stay the first thing on the page */
  var skip = document.querySelector(".skip-link");
  document.body.insertBefore(bar, skip ? skip.nextSibling : document.body.firstChild);
  function done() { try { localStorage.setItem(KEY, "1"); } catch (e) {} }
  bar.querySelector(".langoffer__go").addEventListener("click", function () { done(); try { localStorage.setItem("licter-lang", "fr"); } catch (e) {} });
  bar.querySelector(".langoffer__x").addEventListener("click", function () { done(); bar.remove(); });
})();

/* =========================================================================
   The navigation item of the page you are on, marked.
   ========================================================================= */
(function () {
  var path = location.pathname.replace(/index\.html$/, "");
  var map = [
    [/\/(fr\/cas-usage|en\/use-cases)\//, "use-cases"], [/\/(offers|offer-[a-z0-9-]+)\.html$/, "offers.html"], [/\/expertise(-[a-z0-9-]+)?\.html$/, "expertise.html"], [/\/why-licter\.html$/, "why-licter.html"],
    [/\/(tech-[\w-]+)\.html$/, "tech"], [/\/clients\.html$/, "clients.html"], [/\/(blog|article-[\w-]+)\.html$/, "blog.html"]
  ];
  var hit = null;
  map.forEach(function (m) { if (!hit && m[0].test(path)) hit = m[1]; });
  if (!hit) return;
  Array.prototype.forEach.call(document.querySelectorAll(".hero__top .nav__list > .nav__item > a"), function (a) {
    var h = a.getAttribute("href") || "", key = a.getAttribute("data-menu");
    if (key === hit || h.replace(/^\//, "") === hit) { a.classList.add("is-current"); a.setAttribute("aria-current", "page"); }
  });
})();

/* =========================================================================
   Tabs on the offers and tech pages (.xo__wrap, .xl__wrap): click, arrow
   keys, and links elsewhere on the page that open a given tab (data-tab).
   ========================================================================= */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('.xo__wrap [role="tablist"], .xl__wrap [role="tablist"]'), function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    function show(i, focus) {
      tabs.forEach(function (t, k) {
        var on = k === i, panel = document.getElementById(t.getAttribute("aria-controls"));
        t.classList.toggle("is-on", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        if (panel) { panel.hidden = !on; if (on) { panel.classList.remove("is-in"); void panel.offsetWidth; panel.classList.add("is-in"); } }
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(i); });
      t.addEventListener("keydown", function (e) {
        var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (!d) return;
        e.preventDefault();
        show((i + d + tabs.length) % tabs.length, true);
      });
    });
    /* "which one is for you": a situation opens its offer */
    Array.prototype.forEach.call(document.querySelectorAll("[data-tab]"), function (a) {
      a.addEventListener("click", function (e) {
        var i = +a.getAttribute("data-tab") - 1;
        if (!tabs[i]) return;
        e.preventDefault();
        show(i);
        list.closest("section").scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
      });
    });
  });
})();

/* =========================================================================
   Carousel of the four families on the use-cases hub (.ucc): the arrows
   scroll by one card, and switch off at either end.
   ========================================================================= */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll(".ucc"), function (box) {
    var track = box.querySelector(".ucc__track"), btns = box.querySelectorAll(".ucc__btn");
    if (!track) return;
    function step() {
      var card = track.querySelector(".ucc__card");
      return card ? card.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0) : track.clientWidth;
    }
    function sync() {
      var max = track.scrollWidth - track.clientWidth - 2;
      btns[0].disabled = track.scrollLeft <= 2;
      btns[1].disabled = track.scrollLeft >= max;
    }
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () { track.scrollBy({ left: step() * +b.getAttribute("data-dir") }); });
    });
    track.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });
})();

/* =========================================================================
   The three cases of a family page (.ucw): pills turn a stack of cards.
   It turns by itself every few seconds while in view, and stops for good
   as soon as the visitor clicks, types or prefers reduced motion.
   ========================================================================= */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll(".ucw"), function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    var cards = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    var n = tabs.length, cur = 0, timer = null, T = 6000, stopped = false, seen = false;
    if (!n) return;
    box.style.setProperty("--ucw-t", T / 1000 + "s");
    function show(i, focus) {
      cur = (i + n) % n;
      tabs.forEach(function (t, k) {
        var on = k === cur;
        t.classList.toggle("is-on", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        // restart the progress bar on the new pill
        var bar = t.querySelector(".ucw__bar"); if (bar && on) { bar.style.animation = "none"; void bar.offsetWidth; bar.style.animation = ""; }
      });
      cards.forEach(function (c, k) {
        var d = (k - cur + n) % n;
        c.classList.remove("is-on", "is-next", "is-prev");
        c.classList.add(d === 0 ? "is-on" : d === 1 ? "is-next" : "is-prev");
        // the cards behind stay clickable (they come forward), but out of
        // the tab order and hidden from screen readers
        if (d === 0) c.removeAttribute("aria-hidden"); else c.setAttribute("aria-hidden", "true");
        Array.prototype.forEach.call(c.querySelectorAll("a"), function (a) { a.tabIndex = d === 0 ? 0 : -1; });
      });
      if (focus) tabs[cur].focus();
    }
    function stop() { stopped = true; clearInterval(timer); timer = null; box.classList.remove("is-auto"); }
    function play() {
      if (stopped || timer || !seen) return;
      box.classList.add("is-auto"); show(cur);
      timer = setInterval(function () { show(cur + 1); }, T);
    }
    function pause() { clearInterval(timer); timer = null; box.classList.remove("is-auto"); }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { stop(); show(i); });
      t.addEventListener("keydown", function (e) {
        var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (e.key === "Home") d = -cur; if (e.key === "End") d = n - 1 - cur;
        if (d === undefined) return;
        e.preventDefault(); stop(); show(cur + d, true);
      });
    });
    // a card behind the front one comes forward when clicked
    cards.forEach(function (c, k) {
      c.addEventListener("click", function (e) { if (k !== cur) { e.preventDefault(); stop(); show(k); } });
    });
    box.addEventListener("mouseenter", pause);
    box.addEventListener("mouseleave", play);
    box.addEventListener("focusin", pause);
    show(0);
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) { stopped = true; return; }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { seen = e.isIntersecting; if (seen) play(); else pause(); });
      }, { threshold: 0.4 }).observe(box);
    }
  });
})();

/* =========================================================================
   The sales drawer (callback and chat, js/assistant.js), on every page:
   loaded from here so no page has to list it, with this file's version.
   ========================================================================= */
(function () {
  var me = document.querySelector('script[src*="js/ui.js"]');
  if (!me || document.querySelector('script[src*="js/assistant.js"]')) return;
  /* the two popups first: the chat hands its callback over to them */
  var pp = document.createElement("script");
  pp.src = me.getAttribute("src").replace(/ui\.js/, "popups.js");
  pp.async = false;
  document.body.appendChild(pp);
  var s = document.createElement("script");
  s.src = me.getAttribute("src").replace(/ui\.js/, "assistant.js");
  s.async = false;
  s.defer = true;
  document.body.appendChild(s);
  /* the events banner and the registration pages (js/events.js) */
  if (!document.querySelector('script[src*="js/events.js"]')) {
    var ev = document.createElement("script");
    ev.src = me.getAttribute("src").replace(/ui\.js/, "events.js");
    document.body.appendChild(ev);
  }
})();
