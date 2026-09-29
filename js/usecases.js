/* =========================================================================
   Licter — use cases (home): the visitor picks a topic, its dashboard
   appears, and each dashboard is played differently:

     communication  drag the campaign launch, see before / after
     brand          toggle the complaint drivers, see what drives the noise
     audiences      open a segment, read its profile
     trends         play 18 months, watch the topics move, open one

   MOCK: every figure below is illustrative. Replace with anonymised client
   data before going live.

   Text lives here, not in the HTML, so each string carries its French and
   the dashboard re-renders when the language changes.
   ========================================================================= */
(function () {
  "use strict";

  var stage = document.getElementById("cases-panel");
  var topics = Array.prototype.slice.call(document.querySelectorAll(".topic[data-topic]"));
  if (!stage || !topics.length) return;

  var html = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  function fr() { return html.lang === "fr"; }
  function t(en, frText) { return fr() ? frText : en; }
  function L(pair) { return fr() ? pair[1] : pair[0]; }
  function num(n, d) {
    return n.toLocaleString(fr() ? "fr-FR" : "en-GB", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  }
  var SVGNS = "http://www.w3.org/2000/svg";

  var current = null;
  var cleanup = null;

  /* ============================================================ shell */
  function shell(title, how, body, side) {
    return '<div class="dash">' +
      '<div class="dash__head">' +
        '<p class="dash__title">' + title + "</p>" +
        '<p class="dash__how"><span class="dash__hand" aria-hidden="true">↔</span>' + how + "</p>" +
        '<span class="dash__tag">' + t("Illustrative data", "Données illustratives") + "</span>" +
      "</div>" +
      '<div class="dash__body">' + body + "</div>" +
    "</div>" +
    '<aside class="dash__side">' + side + "</aside>";
  }
  function sideBlock(questions, anchor) {
    return '<p class="dash__side-k">' + t("Questions we answer here", "Les questions traitées ici") + "</p>" +
      '<ul class="dash__qs">' + questions.map(function (q) {
        return '<li><a href="use-cases.html#' + anchor + '">' + L(q) + ' <span aria-hidden="true">→</span></a></li>';
      }).join("") + "</ul>" +
      '<a class="btn btn--primary dash__cta" href="#book">' + t("Book a meeting", "Prendre rendez-vous") + ' <span aria-hidden="true">→</span></a>';
  }

  /* ================================================= 1. communication */
  var SOV = [11.8, 12.1, 12.6, 12.2, 12.9, 13.1, 18.4, 20.2, 21.5, 19.8, 19.1, 18.6];
  var CAT = [14.2, 14.0, 14.4, 14.1, 14.3, 14.2, 14.6, 14.4, 14.5, 14.3, 14.2, 14.4];

  function communication() {
    var body =
      '<div class="kpis">' +
        '<div class="kpi"><p class="kpi__k">' + t("Before launch", "Avant le lancement") + '</p><p class="kpi__v" id="c-before"></p></div>' +
        '<div class="kpi"><p class="kpi__k">' + t("After launch", "Après le lancement") + '</p><p class="kpi__v" id="c-after"></p></div>' +
        '<div class="kpi kpi--hi"><p class="kpi__k">' + t("Uplift", "Gain") + '</p><p class="kpi__v" id="c-up"></p></div>' +
      "</div>" +
      '<div class="chart" id="c-chart"></div>' +
      '<label class="scrub"><span class="scrub__k">' + t("Campaign launch", "Lancement de la campagne") + '</span>' +
        '<input type="range" id="c-range" min="1" max="11" step="1" value="6" aria-label="' + t("Campaign launch week", "Semaine de lancement") + '" /></label>' +
      '<p class="dash__insight" id="c-insight"></p>';
    stage.innerHTML = shell(t("Share of voice, 12 weeks", "Part de voix, 12 semaines"),
      t("Drag the launch date", "Faites glisser la date de lancement"), body,
      sideBlock([["Analyze the impact of an event or campaign", "Mesurer l'impact d'un événement ou d'une campagne"],
                 ["Optimize your leader advocacy strategy", "Optimiser la prise de parole de vos dirigeants"],
                 ["Identify the right ambassadors", "Identifier les bons ambassadeurs"]], "communication"));

    var box = document.getElementById("c-chart"), range = document.getElementById("c-range");
    var Wd = 600, Hd = 220, P = { l: 34, r: 12, t: 16, b: 26 };
    var X = function (i) { return P.l + i * (Wd - P.l - P.r) / (SOV.length - 1); };
    var Y = function (v) { return P.t + (1 - (v - 8) / 16) * (Hd - P.t - P.b); };
    function path(a) { return a.map(function (v, i) { return (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(v).toFixed(1); }).join(" "); }

    function draw() {
      var k = +range.value;               /* launch sits between week k-1 and k */
      var mx = (X(k - 1) + X(k)) / 2;
      var grid = [8, 12, 16, 20, 24].map(function (v) {
        return '<line x1="' + P.l + '" x2="' + (Wd - P.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" class="g"/>' +
          '<text x="' + (P.l - 6) + '" y="' + (Y(v) + 3) + '" class="ax" text-anchor="end">' + v + "%</text>";
      }).join("");
      var labels = SOV.map(function (_, i) {
        return i % 2 ? "" : '<text x="' + X(i) + '" y="' + (Hd - 8) + '" class="ax" text-anchor="middle">' + t("W", "S") + (i + 1) + "</text>";
      }).join("");
      var area = path(SOV) + " L" + X(SOV.length - 1) + " " + (Hd - P.b) + " L" + X(0) + " " + (Hd - P.b) + " Z";
      box.innerHTML =
        '<svg viewBox="0 0 ' + Wd + " " + Hd + '" role="img" aria-label="' + t("Share of voice by week", "Part de voix par semaine") + '">' +
          '<defs><linearGradient id="c-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDBA11" stop-opacity=".32"/><stop offset="1" stop-color="#FDBA11" stop-opacity="0"/></linearGradient></defs>' +
          grid + labels +
          '<rect x="' + mx + '" y="' + P.t + '" width="' + (Wd - P.r - mx) + '" height="' + (Hd - P.t - P.b) + '" class="after"/>' +
          '<path d="' + area + '" fill="url(#c-fill)"/>' +
          '<path d="' + path(CAT) + '" class="cat"/>' +
          '<path d="' + path(SOV) + '" class="brand"/>' +
          SOV.map(function (v, i) { return '<circle cx="' + X(i) + '" cy="' + Y(v) + '" r="3" class="dot' + (i >= k ? " is-after" : "") + '"/>'; }).join("") +
          '<line x1="' + mx + '" x2="' + mx + '" y1="' + (P.t - 4) + '" y2="' + (Hd - P.b) + '" class="marker"/>' +
          '<g transform="translate(' + mx + "," + (P.t + 2) + ')"><rect x="-30" y="-2" width="60" height="18" rx="9" class="pill"/>' +
          '<text y="11" text-anchor="middle" class="pill__t">' + t("Launch", "Lancement") + "</text></g>" +
          '<text x="' + (Wd - P.r) + '" y="' + (Y(CAT[CAT.length - 1]) - 6) + '" text-anchor="end" class="cat__t">' + t("Category average", "Moyenne de la catégorie") + "</text>" +
        "</svg>";
      var before = SOV.slice(0, k), after = SOV.slice(k);
      var avg = function (a) { return a.reduce(function (s, v) { return s + v; }, 0) / a.length; };
      var b = avg(before), a = avg(after), up = a - b;
      document.getElementById("c-before").textContent = num(b, 1) + " %";
      document.getElementById("c-after").textContent = num(a, 1) + " %";
      document.getElementById("c-up").textContent = (up >= 0 ? "+" : "") + num(up, 1) + " pts";
      var ins = document.getElementById("c-insight");
      if (k === 6) ins.innerHTML = t("<b>The launch week holds up.</b> Share of voice jumps 7 points and stays above the category for six weeks: the campaign moved the conversation, not just the reach.",
                                      "<b>La semaine de lancement tient.</b> La part de voix bondit de 7 points et reste au-dessus de la catégorie pendant six semaines : la campagne a fait bouger la conversation, pas seulement la portée.");
      else if (k < 6) ins.innerHTML = t("<b>Too early.</b> Nothing moves in the weeks after this date: the lift you would credit to the campaign is diluted.",
                                        "<b>Trop tôt.</b> Rien ne bouge dans les semaines qui suivent : le gain attribué à la campagne est dilué.");
      else ins.innerHTML = t("<b>Too late.</b> The jump already happened before this date: you would miss what caused it.",
                             "<b>Trop tard.</b> Le saut a déjà eu lieu avant cette date : on passerait à côté de ce qui l'a provoqué.");
    }
    range.addEventListener("input", draw);
    /* a click on the chart moves the launch there */
    box.addEventListener("click", function (e) {
      var r = box.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * Wd;
      var i = Math.round((x - P.l) / ((Wd - P.l - P.r) / (SOV.length - 1)));
      range.value = Math.max(1, Math.min(11, i)); draw();
    });
    draw();
  }

  /* ======================================================== 2. brand */
  var DRIVERS = [
    { key: "delivery", name: ["Delivery", "Livraison"], color: "#E2468D", v: [40, 42, 38, 45, 60, 210, 180, 70, 50, 45] },
    { key: "price",    name: ["Price", "Prix"],         color: "#4292F2", v: [80, 85, 78, 82, 90, 95, 88, 84, 80, 79] },
    { key: "product",  name: ["Product", "Produit"],    color: "#7B6CF2", v: [55, 50, 58, 52, 54, 60, 57, 53, 51, 50] },
    { key: "service",  name: ["Service", "Service"],    color: "#3CC2A6", v: [30, 28, 35, 32, 30, 40, 38, 33, 31, 30] }
  ];

  function brand() {
    var on = { delivery: true, price: true, product: true, service: true };
    var body =
      '<div class="chips" role="group" aria-label="' + t("Complaint drivers", "Sujets de plainte") + '">' +
        DRIVERS.map(function (d) {
          return '<button class="chip2 is-on" type="button" aria-pressed="true" data-k="' + d.key + '" style="--c:' + d.color + '">' +
            '<span class="chip2__dot"></span>' + L(d.name) + "</button>";
        }).join("") +
      "</div>" +
      '<div class="kpis">' +
        '<div class="kpi"><p class="kpi__k">' + t("Negative mentions", "Mentions négatives") + '</p><p class="kpi__v" id="b-total"></p></div>' +
        '<div class="kpi"><p class="kpi__k">' + t("Main driver", "Premier sujet") + '</p><p class="kpi__v" id="b-main"></p></div>' +
        '<div class="kpi kpi--hi"><p class="kpi__k">' + t("Peak week", "Semaine du pic") + '</p><p class="kpi__v" id="b-peak"></p></div>' +
      "</div>" +
      '<div class="chart" id="b-chart"></div>' +
      '<p class="dash__insight" id="b-insight"></p>';
    stage.innerHTML = shell(t("Negative mentions, 10 weeks", "Mentions négatives, 10 semaines"),
      t("Turn the topics on and off", "Activez ou coupez les sujets"), body,
      sideBlock([["Monitor your brand image and reputation", "Surveiller l'image et la réputation de votre marque"],
                 ["Develop your brand messaging", "Construire votre discours de marque"],
                 ["Identify and mitigate brand risks", "Identifier et désamorcer les risques de marque"]], "brand-health"));

    var box = document.getElementById("b-chart");
    var Wd = 600, Hd = 220, P = { l: 34, r: 10, t: 12, b: 26 }, n = 10;
    function draw() {
      var act = DRIVERS.filter(function (d) { return on[d.key]; });
      var tot = []; for (var i = 0; i < n; i++) tot[i] = act.reduce(function (s, d) { return s + d.v[i]; }, 0);
      var max = 400, bw = (Wd - P.l - P.r) / n;
      var Y = function (v) { return P.t + (1 - v / max) * (Hd - P.t - P.b); };
      var bars = "";
      for (i = 0; i < n; i++) {
        var y0 = Hd - P.b;
        act.forEach(function (d) {
          var h = (Hd - P.t - P.b) * d.v[i] / max;
          bars += '<rect x="' + (P.l + i * bw + bw * 0.18).toFixed(1) + '" y="' + (y0 - h).toFixed(1) + '" width="' + (bw * 0.64).toFixed(1) + '" height="' + Math.max(0, h - 1).toFixed(1) + '" rx="2" fill="' + d.color + '" class="bar"/>';
          y0 -= h;
        });
        bars += '<text x="' + (P.l + i * bw + bw / 2) + '" y="' + (Hd - 8) + '" text-anchor="middle" class="ax">' + t("W", "S") + (i + 1) + "</text>";
      }
      var grid = [0, 100, 200, 300, 400].map(function (v) {
        return '<line x1="' + P.l + '" x2="' + (Wd - P.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" class="g"/><text x="' + (P.l - 6) + '" y="' + (Y(v) + 3) + '" text-anchor="end" class="ax">' + v + "</text>";
      }).join("");
      box.innerHTML = '<svg viewBox="0 0 ' + Wd + " " + Hd + '" role="img" aria-label="' + t("Negative mentions by week and topic", "Mentions négatives par semaine et par sujet") + '">' + grid + bars + "</svg>";

      var total = tot.reduce(function (s, v) { return s + v; }, 0);
      var main = act.slice().sort(function (a, b) { return b.v.reduce(function (s, v) { return s + v; }, 0) - a.v.reduce(function (s, v) { return s + v; }, 0); })[0];
      var peak = tot.indexOf(Math.max.apply(null, tot));
      document.getElementById("b-total").textContent = act.length ? num(total) : "0";
      document.getElementById("b-main").textContent = main ? L(main.name) : "–";
      document.getElementById("b-peak").textContent = act.length ? t("W", "S") + (peak + 1) : "–";
      var ins = document.getElementById("b-insight");
      if (!act.length) ins.innerHTML = t("Turn a topic back on.", "Réactivez un sujet.");
      else if (on.delivery && (peak === 5 || peak === 6)) ins.innerHTML = t("<b>The spike is delivery, and only delivery.</b> Price and product complaints stay flat: this is an operations problem for two weeks, not a reputation crisis.",
        "<b>Le pic, c'est la livraison, et seulement elle.</b> Les plaintes sur le prix et le produit restent stables : un problème logistique de deux semaines, pas une crise de réputation.");
      else if (!on.delivery) ins.innerHTML = t("<b>Without delivery, there is no spike at all.</b> The underlying noise is price, and it is stable week after week.",
        "<b>Sans la livraison, il n'y a plus de pic.</b> Le bruit de fond, c'est le prix, stable semaine après semaine.");
      else ins.innerHTML = t("<b>" + L(main.name) + "</b> drives most of what you kept on.", "<b>" + L(main.name) + "</b> porte l'essentiel de ce que vous avez gardé.");
    }
    stage.querySelector(".chips").addEventListener("click", function (e) {
      var b = e.target.closest(".chip2"); if (!b) return;
      on[b.dataset.k] = !on[b.dataset.k];
      b.classList.toggle("is-on", on[b.dataset.k]);
      b.setAttribute("aria-pressed", on[b.dataset.k] ? "true" : "false");
      draw();
    });
    draw();
  }

  /* ===================================================== 3. audiences */
  var SEGMENTS = [
    { name: ["Practical parents", "Parents pragmatiques"], share: 34, age: "30–44", color: "#F4A93B", x: 36, y: 44,
      platforms: [["Instagram", 62], ["Facebook", 48], ["YouTube", 41]],
      interests: [["Batch cooking", "Batch cooking"], ["School runs", "Trajets d'école"], ["Budget", "Budget"]],
      expect: ["Time saved, not recipes.", "Du temps gagné, pas des recettes."] },
    { name: ["Creators' fans", "Fans de créateurs"], share: 24, age: "18–29", color: "#E2468D", x: 70, y: 30,
      platforms: [["TikTok", 78], ["Instagram", 55], ["YouTube", 38]],
      interests: [["Quick recipes", "Recettes rapides"], ["Trends", "Tendances"], ["Dupes", "Dupes"]],
      expect: ["Something worth filming.", "Quelque chose qui vaut une vidéo."] },
    { name: ["Health optimisers", "Adeptes du bien-être"], share: 18, age: "25–39", color: "#3CC2A6", x: 68, y: 72,
      platforms: [["Instagram", 51], ["YouTube", 47], ["Reddit", 29]],
      interests: [["Protein", "Protéines"], ["Labels", "Étiquettes"], ["Sport", "Sport"]],
      expect: ["Proof, not promises.", "Des preuves, pas des promesses."] },
    { name: ["Loyal seniors", "Seniors fidèles"], share: 14, age: "55+", color: "#4292F2", x: 18, y: 76,
      platforms: [["Facebook", 64], ["YouTube", 35], ["Pinterest", 22]],
      interests: [["Tradition", "Tradition"], ["Quality", "Qualité"], ["Price", "Prix"]],
      expect: ["Don't change the recipe.", "Ne changez pas la recette."] },
    { name: ["Deal hunters", "Chasseurs de promos"], share: 10, age: "25–54", color: "#7B6CF2", x: 88, y: 54,
      platforms: [["Facebook", 52], ["TikTok", 33], ["X", 18]],
      interests: [["Promotions", "Promotions"], ["Comparisons", "Comparatifs"], ["Loyalty cards", "Cartes de fidélité"]],
      expect: ["A reason to switch.", "Une raison de changer."] }
  ];

  function audiences() {
    var sel = 0;
    var body =
      '<div class="seg">' +
        '<div class="seg__map" role="group" aria-label="' + t("Audience segments", "Segments d'audience") + '">' +
          SEGMENTS.map(function (s, i) {
            var d = 34 + Math.sqrt(s.share) * 13;
            return '<button class="bub" type="button" data-i="' + i + '" style="--c:' + s.color + ";left:" + s.x + "%;top:" + s.y + "%;width:" + d + "px;height:" + d + 'px" aria-pressed="false">' +
              '<span class="bub__n">' + s.share + '%</span><span class="visually-hidden"> ' + L(s.name) + "</span></button>";
          }).join("") +
        "</div>" +
        '<div class="seg__card" id="a-card"></div>' +
      "</div>" +
      '<p class="dash__insight" id="a-insight"></p>';
    stage.innerHTML = shell(t("Who is actually buying", "Qui achète vraiment"),
      t("Click a segment to open it", "Cliquez un segment pour l'ouvrir"), body,
      sideBlock([["Segment your target profiles", "Segmenter vos profils cibles"],
                 ["Rejuvenate your audiences", "Rajeunir vos audiences"],
                 ["Understand expectations at every touchpoint", "Comprendre les attentes à chaque point de contact"]], "audiences"));
    var bubs = Array.prototype.slice.call(stage.querySelectorAll(".bub"));
    function draw() {
      var s = SEGMENTS[sel];
      bubs.forEach(function (b, i) { b.classList.toggle("is-on", i === sel); b.setAttribute("aria-pressed", i === sel ? "true" : "false"); });
      document.getElementById("a-card").innerHTML =
        '<p class="seg__name" style="--c:' + s.color + '"><span></span>' + L(s.name) + "</p>" +
        '<p class="seg__meta">' + s.share + "% " + t("of buyers", "des acheteurs") + " · " + s.age + " " + t("years", "ans") + "</p>" +
        '<p class="seg__k">' + t("Where they are", "Où ils sont") + "</p>" +
        s.platforms.map(function (p) {
          return '<div class="pbar"><span class="pbar__n">' + p[0] + '</span><span class="pbar__t"><i style="width:' + p[1] + "%;background:" + s.color + '"></i></span><span class="pbar__v">' + p[1] + "%</span></div>";
        }).join("") +
        '<p class="seg__k">' + t("What they talk about", "De quoi ils parlent") + "</p>" +
        '<p class="seg__tags">' + s.interests.map(function (x) { return "<span>" + L(x) + "</span>"; }).join("") + "</p>";
      document.getElementById("a-insight").innerHTML = "<b>" + t("What they expect: ", "Ce qu'ils attendent : ") + "</b>" + L(s.expect);
    }
    stage.querySelector(".seg__map").addEventListener("click", function (e) {
      var b = e.target.closest(".bub"); if (!b) return;
      sel = +b.dataset.i; draw();
    });
    draw();
  }

  /* ======================================================== 4. trends */
  var TRENDS = [
    { name: ["Upcycled food", "Alimentation upcyclée"], from: [6, 8], to: [20, 92], verdict: ["Small, but growing fastest. Worth a pilot now, before it is obvious.", "Petit, mais c'est ce qui croît le plus vite. À tester maintenant, avant que ce soit évident."] },
    { name: ["High-protein snacks", "Snacks protéinés"], from: [14, 24], to: [62, 76], verdict: ["Moved from gyms to parents. Mainstream within a year.", "Passé des salles de sport aux parents. Grand public d'ici un an."] },
    { name: ["Gut health", "Santé intestinale"], from: [24, 30], to: [56, 64], verdict: ["Steady climb, driven by creators. A safe bet for messaging.", "Montée régulière, portée par les créateurs. Un pari sûr pour le discours."] },
    { name: ["Plant-based milk", "Laits végétaux"], from: [72, 44], to: [84, 2], verdict: ["Big and flat. Compete on price and taste, not novelty.", "Gros et stable. Se battre sur le prix et le goût, pas sur la nouveauté."] },
    { name: ["Zero-sugar drinks", "Boissons zéro sucre"], from: [56, 26], to: [60, 22], verdict: ["Mature. No reason to lead with it.", "Mature. Aucune raison d'en faire un argument principal."] },
    { name: ["Meal kits", "Box repas"], from: [52, 22], to: [34, -14], verdict: ["Fading since the pandemic peak. Do not build here.", "En recul depuis le pic du confinement. Ne pas investir ici."] }
  ];
  var MONTHS = 18;

  function trends() {
    var month = 0, sel = 0, timer = null;
    var body =
      '<div class="radar">' +
        '<div class="chart" id="t-chart"></div>' +
        '<div class="radar__card" id="t-card"></div>' +
      "</div>" +
      '<div class="play">' +
        '<button class="play__btn" type="button" id="t-play" aria-label="' + t("Play 18 months", "Lire 18 mois") + '">▶</button>' +
        '<input type="range" id="t-range" min="0" max="' + MONTHS + '" value="0" aria-label="' + t("Month", "Mois") + '" />' +
        '<span class="play__m" id="t-month"></span>' +
      "</div>" +
      '<p class="dash__insight" id="t-insight"></p>';
    stage.innerHTML = shell(t("Topic radar, volume against growth", "Radar des sujets, volume et croissance"),
      t("Press play, then open a topic", "Lancez la lecture, puis ouvrez un sujet"), body,
      sideBlock([["Test and evaluate your products", "Tester et évaluer vos produits"],
                 ["Analyze markets and identify opportunities", "Analyser les marchés et repérer les opportunités"],
                 ["Map out your stakeholders and future trends", "Cartographier vos parties prenantes et les tendances à venir"]], "trends"));
    var box = document.getElementById("t-chart"), range = document.getElementById("t-range"), btn = document.getElementById("t-play");
    var Wd = 420, Hd = 260, P = { l: 30, r: 10, t: 10, b: 24 };
    var X = function (v) { return P.l + v / 100 * (Wd - P.l - P.r); };
    var Y = function (g) { return P.t + (1 - (g + 20) / 120) * (Hd - P.t - P.b); };
    function pos(tr, m) {
      var k = m / MONTHS; k = k * k * (3 - 2 * k);
      return [tr.from[0] + (tr.to[0] - tr.from[0]) * k, tr.from[1] + (tr.to[1] - tr.from[1]) * k];
    }
    function draw() {
      var mx = X(40), my = Y(40);
      var q = '<rect x="' + P.l + '" y="' + P.t + '" width="' + (mx - P.l) + '" height="' + (my - P.t) + '" class="q q--weak"/>' +
        '<text x="' + (P.l + 6) + '" y="' + (my - 6) + '" class="q__t">' + t("Weak signals", "Signaux faibles") + "</text>" +
        '<text x="' + (Wd - P.r - 6) + '" y="' + (my - 6) + '" text-anchor="end" class="q__t">' + t("Rising", "En essor") + "</text>" +
        '<text x="' + (Wd - P.r - 6) + '" y="' + (my + 14) + '" text-anchor="end" class="q__t">' + t("Mature", "Matures") + "</text>" +
        '<text x="' + (P.l + 6) + '" y="' + (my + 14) + '" class="q__t">' + t("Fading", "En recul") + "</text>" +
        '<line x1="' + mx + '" x2="' + mx + '" y1="' + P.t + '" y2="' + (Hd - P.b) + '" class="g"/>' +
        '<line x1="' + P.l + '" x2="' + (Wd - P.r) + '" y1="' + my + '" y2="' + my + '" class="g"/>' +
        '<text x="' + (Wd - P.r) + '" y="' + (Hd - 6) + '" text-anchor="end" class="ax">' + t("Volume →", "Volume →") + "</text>" +
        '<text x="12" y="' + ((P.t + Hd - P.b) / 2) + '" text-anchor="middle" class="ax" transform="rotate(-90 12 ' + ((P.t + Hd - P.b) / 2) + ')">' + t("Growth →", "Croissance →") + "</text>";
      var dots = TRENDS.map(function (tr, i) {
        var p = pos(tr, month), trail = "";
        for (var m = 0; m <= month; m += 3) { var pp = pos(tr, m); trail += (m ? "L" : "M") + X(pp[0]).toFixed(1) + " " + Y(pp[1]).toFixed(1); }
        trail += "L" + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1);
        return '<path d="' + trail + '" class="trail' + (i === sel ? " is-on" : "") + '"/>' +
          '<g class="tdot' + (i === sel ? " is-on" : "") + '" data-i="' + i + '" transform="translate(' + X(p[0]).toFixed(1) + "," + Y(p[1]).toFixed(1) + ')" tabindex="0" role="button" aria-label="' + L(tr.name) + '">' +
          '<circle r="' + (i === sel ? 8 : 6) + '"/>' +
          /* labels on the right half read leftward, so they stay inside the chart */
          (p[0] > 55 ? '<text x="-11" y="4" text-anchor="end" class="tdot__t">' : '<text x="11" y="4" class="tdot__t">') + L(tr.name) + "</text></g>";
      }).join("");
      box.innerHTML = '<svg viewBox="0 0 ' + Wd + " " + Hd + '" role="img" aria-label="' + t("Topics by volume and growth", "Sujets par volume et croissance") + '">' + q + dots + "</svg>";
      var tr = TRENDS[sel], p = pos(tr, month);
      /* the selected topic's volume over the months so far */
      var spark = "", sw = 180, sh = 44;
      for (var m = 0; m <= MONTHS; m++) { var v = pos(tr, m)[0]; spark += (m ? "L" : "M") + (m / MONTHS * sw).toFixed(1) + " " + (sh - v / 100 * sh).toFixed(1); }
      document.getElementById("t-card").innerHTML =
        '<p class="radar__name">' + L(tr.name) + "</p>" +
        '<p class="radar__nums"><span><b>' + Math.round(p[0]) + "</b> " + t("volume index", "indice de volume") + "</span><span><b>" + (p[1] >= 0 ? "+" : "") + Math.round(p[1]) + "%</b> " + t("growth", "croissance") + "</span></p>" +
        '<svg class="radar__spark" viewBox="0 0 ' + sw + " " + sh + '" aria-hidden="true"><path d="' + spark + '"/><circle cx="' + (month / MONTHS * sw) + '" cy="' + (sh - p[0] / 100 * sh) + '" r="3"/></svg>' +
        '<p class="radar__verdict">' + L(tr.verdict) + "</p>";
      document.getElementById("t-month").textContent = t("Month ", "Mois ") + month + " / " + MONTHS;
      range.value = month;
      document.getElementById("t-insight").innerHTML = month < MONTHS
        ? t("<b>Press play.</b> Watch which topics climb out of the weak-signal corner.", "<b>Lancez la lecture.</b> Regardez quels sujets sortent du coin des signaux faibles.")
        : t("<b>Upcycled food and protein snacks</b> crossed into growth; meal kits fell out. That is the shortlist.", "<b>L'upcyclé et les snacks protéinés</b> sont passés en croissance ; les box repas sont sorties. Voilà la shortlist.");
    }
    function stopPlay() { clearInterval(timer); timer = null; btn.textContent = "▶"; btn.setAttribute("aria-label", t("Play 18 months", "Lire 18 mois")); }
    btn.addEventListener("click", function () {
      if (timer) { stopPlay(); return; }
      if (month >= MONTHS) month = 0;
      if (reduced.matches) { month = MONTHS; draw(); return; }
      btn.textContent = "❚❚"; btn.setAttribute("aria-label", t("Pause", "Pause"));
      timer = setInterval(function () { month++; draw(); if (month >= MONTHS) stopPlay(); }, 260);
    });
    range.addEventListener("input", function () { stopPlay(); month = +range.value; draw(); });
    function pick(e) {
      var g = e.target.closest(".tdot"); if (!g) return;
      if (e.type === "keydown" && e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault(); sel = +g.dataset.i; draw();
    }
    box.addEventListener("click", pick);
    box.addEventListener("keydown", pick);
    draw();
    cleanup = stopPlay;
  }

  /* ============================================================ switch */
  var RENDER = { communication: communication, brand: brand, audiences: audiences, trends: trends };

  function select(key, focus) {
    if (cleanup) { cleanup(); cleanup = null; }
    current = key;
    topics.forEach(function (b) {
      var on = b.dataset.topic === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    stage.setAttribute("aria-labelledby", "tab-" + key);
    stage.classList.remove("is-in"); void stage.offsetWidth;
    stage.classList.add("has-dash");
    RENDER[key]();
    stage.classList.add("is-in");
    if (focus) stage.focus({ preventScroll: true });
  }

  topics.forEach(function (b, i) {
    b.addEventListener("click", function () { select(b.dataset.topic); });
    b.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = topics[(i + d + topics.length) % topics.length];
      n.focus(); select(n.dataset.topic);
    });
  });

  /* language switch: redraw the open dashboard in the new language */
  if (window.MutationObserver) {
    new MutationObserver(function () { if (current) select(current); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }
})();
