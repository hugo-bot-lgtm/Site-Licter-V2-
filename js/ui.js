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

  function buildMarquee() {
    var track = document.getElementById("marquee-track");
    if (!track) return;

    /* same scale-up as the rest of the hero past the reference width */
    var k = Math.min(1.28, Math.max(1, window.innerWidth / 1247));
    var gap = Math.round(GAP * k);

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
    track.style.setProperty("--marquee-duration", (setWidth / (126 * k)).toFixed(2) + "s");
  }

  buildMarquee();
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

  var CASES = {
    communication: {
      label: "CAMPAIGN IMPACT — SHARE OF VOICE",
      metric: "+23%",
      trend: "vs. category benchmark, rolling 90 days",
      caption: "Creator-driven reach over the last 90 days, measured against the category benchmark.",
      series: [18, 22, 20, 28, 34, 31, 42, 47, 45, 58, 63, 71],
      railTitle: "WHERE THE VOICE COMES FROM",
      rail: [
        { name: "TikTok", v: 34 }, { name: "Instagram", v: 27 },
        { name: "YouTube", v: 21 }, { name: "X", v: 11 }, { name: "LinkedIn", v: 7 }
      ],
      anchor: "use-cases.html#communication",
      questions: [
        "Analyze the impact of an event or campaign",
        "Optimize your leader advocacy strategy",
        "Identify the right ambassadors"
      ]
    },
    brand: {
      label: "BRAND HEALTH — NET SENTIMENT",
      metric: "+17%",
      trend: "net positive, owned and earned conversations",
      caption: "Net positive sentiment on owned and earned conversations, panel-weighted.",
      series: [30, 34, 31, 36, 41, 39, 44, 48, 52, 50, 57, 62],
      railTitle: "WHAT DRIVES THE SENTIMENT",
      rail: [
        { name: "Product", v: 38 }, { name: "Service", v: 24 },
        { name: "Pricing", v: 18 }, { name: "Campaigns", v: 12 }, { name: "Corporate", v: 8 }
      ],
      anchor: "use-cases.html#brand-health",
      questions: [
        "Monitor your brand image and reputation",
        "Develop your brand messaging",
        "Identify and mitigate brand risks"
      ]
    },
    audiences: {
      label: "CORE TARGET — QUALIFIED REACH",
      metric: "×2.4",
      trend: "qualified reach, look-alike communities folded in",
      caption: "Qualified reach inside the core target once look-alike communities are folded in.",
      series: [12, 16, 24, 21, 33, 38, 36, 49, 55, 61, 58, 74],
      railTitle: "WHO THE COMMUNITIES ARE",
      rail: [
        { name: "Core target", v: 41 }, { name: "Look-alikes", v: 26 },
        { name: "Prescribers", v: 16 }, { name: "Detractors", v: 10 }, { name: "Undecided", v: 7 }
      ],
      anchor: "use-cases.html#audiences",
      questions: [
        "Segment your target profiles",
        "Rejuvenate your audiences",
        "Understand expectations at every touchpoint"
      ]
    },
    trends: {
      label: "EMERGING TOPICS — VELOCITY",
      metric: "+41%",
      trend: "velocity of topics breaking out of the category",
      caption: "Velocity of the topics breaking out of the category over the last four weeks.",
      series: [8, 11, 14, 13, 22, 29, 27, 38, 46, 52, 66, 79],
      railTitle: "WHAT IS BREAKING OUT",
      rail: [
        { name: "Refill formats", v: 31 }, { name: "Dupe culture", v: 25 },
        { name: "AI try-on", v: 20 }, { name: "Resale", v: 14 }, { name: "Longevity", v: 10 }
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
      '<path class="chart__line" d="' + line + '" fill="none" stroke="#C08C0E" stroke-width="2.4" ' +
        'stroke-linejoin="round" stroke-linecap="round"/>' +
      '<circle class="chart__cursor" cx="' + lastX.toFixed(1) + '" cy="' + lastY.toFixed(1) + '" r="20" fill="url(#vizDot)"/>' +
      dots + labels + "</svg>";
  }

  function railRows(rows) {
    var top = Math.max.apply(null, rows.map(function (r) { return r.v; }));
    return rows.map(function (r, i) {
      return '<li class="rail__row">' +
        '<span class="rail__name">' + r.name + "</span>" +
        '<span class="rail__value">' + r.v + "%</span>" +
        '<span class="rail__bar"><i style="--w:' + Math.round((r.v / top) * 100) +
          "%;--i:" + i + '"></i></span>' +
        "</li>";
    }).join("");
  }

  var viz = document.getElementById("viz");
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  var panel = document.getElementById("cases-panel");

  var questions = document.getElementById("questions");

  /* The three questions of the selected family, straight from the deck. */
  function renderQuestions(key) {
    if (!questions) return;
    var d = CASES[key];
    questions.innerHTML = d.questions.map(function (q, i) {
      return '<li style="--i:' + i + '"><a class="question" href="' + d.anchor + '">' + q +
             '<span class="question__arrow" aria-hidden="true">→</span></a></li>';
    }).join("");
    questions.classList.remove("is-swap");
    void questions.offsetWidth;
    questions.classList.add("is-swap");
  }

  function renderViz(key) {
    if (!viz) return;
    var d = CASES[key];
    viz.innerHTML =
      '<div class="viz__head">' +
        '<div class="viz__id"><span class="viz__dot" aria-hidden="true"></span>' +
          '<span class="viz__label">' + d.label + "</span></div>" +
        '<div class="viz__figure"><span class="viz__metric">' + d.metric + "</span>" +
          '<span class="viz__trend">' + d.trend + "</span></div>" +
      "</div>" +
      '<div class="viz__body">' +
        '<div class="rail"><p class="rail__title">' + d.railTitle + "</p>" +
          '<ul class="rail__list">' + railRows(d.rail) + "</ul></div>" +
        '<div class="viz__chart">' + chart(d.series) + "</div>" +
      "</div>" +
      '<figcaption class="viz__foot">' + d.caption + "</figcaption>";

    animateViz();
  }

  /* The panel is a data visual, so the data is what moves: the curve draws
     itself, the bars grow to their value, the headline figure counts up. */
  function animateViz() {
    if (reduced.matches) {
      viz.querySelectorAll(".rail__bar i").forEach(function (bar) {
        bar.style.width = bar.style.getPropertyValue("--w");
      });
      return;
    }

    var line = viz.querySelector(".chart__line");
    if (line && line.getTotalLength) {
      line.style.setProperty("--len", Math.ceil(line.getTotalLength()));
    }

    requestAnimationFrame(function () {
      viz.querySelectorAll(".rail__bar i").forEach(function (bar) {
        bar.classList.add("is-grown");
      });
    });

    countUp(viz.querySelector(".viz__metric"));
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
        { letter: "T", name: "Talkwalker", href: "tech-tools.html#tools",
          desc: "Broad listening and analytics, across markets and languages." },
        { letter: "V", name: "Visibrain", href: "tech-tools.html#tools",
          desc: "Real-time monitoring, and the media conversation as it breaks." },
        { letter: "Y", name: "YouScan", href: "tech-tools.html#tools",
          desc: "Visual listening: what appears in the image, not only in the text." },
        { letter: "S", name: "SoPrism", href: "tech-tools.html#tools",
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
    /* tools have no glyph we are entitled to reproduce: a monogram instead */
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
