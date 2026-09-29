/* =========================================================================
   Licter — use cases (home). The visitor picks a question; each one opens
   its own visual, played differently:

     communication  a volume curve; drag the launch line, hover the peaks
     brand          a word cloud coloured by tone; filter, click a word
     audiences      a community map; open a segment, show the brief's target
     trends         a trend radar that plays over 18 months; open a topic

   Around every visual: the live badge, the count of posts read, a couple of
   real-looking posts, then the answer, then the booking button.

   MOCK: every post, handle and figure below is illustrative. Replace with
   anonymised client material before going live.
   ========================================================================= */
(function () {
  "use strict";

  var stage = document.getElementById("cases-panel");
  var topics = Array.prototype.slice.call(document.querySelectorAll(".lf__topic[data-topic]"));
  if (!stage || !topics.length) return;

  var html = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  function fr() { return html.lang === "fr"; }
  function t(en, frText) { return fr() ? frText : en; }
  function L(pair) { return fr() ? pair[1] : pair[0]; }
  function num(n) { return Math.round(n).toLocaleString(fr() ? "fr-FR" : "en-GB"); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;"); }

  var DATA = {
    communication: {
      label: ["Spring campaign, 3 weeks", "Campagne de printemps, 3 semaines"],
      themes: [
        { name: ["Shares creator videos", "Partage des vidéos de créateurs"], w: 0.46, color: "#F4A93B" },
        { name: ["Wants to buy", "Veut acheter"], w: 0.28, color: "#3CC2A6" },
        { name: ["Talks about the ad", "Parle de la pub"], w: 0.14, color: "#4292F2" },
        { name: ["Mocks it", "S'en moque"], w: 0.12, color: "#E2468D" }
      ],
      answer: ["<b>Yes, but not the way it was planned.</b> Creators carried it: 46 % of posts share their videos, the ad itself only 14 %. And 28 % say they want to buy.",
               "<b>Oui, mais pas comme prévu.</b> Les créateurs l'ont portée : 46 % des posts partagent leurs vidéos, la pub elle-même seulement 14 %. Et 28 % disent vouloir acheter."],
      posts: [
        ["TIKTOK", "@lea.cuisine", 0, 1, "Okay, the recipe @chef.maud made with the new sauce is actually insane.", "Ok, la recette que @chef.maud a faite avec la nouvelle sauce est vraiment folle."],
        ["INSTAGRAM", "@thomas.run", 1, 1, "Saw it in three stories today. Buying it this weekend.", "Vu dans trois stories aujourd'hui. Je l'achète ce week-end."],
        ["X", "@nadia_b", 2, 0, "The TV ad is fine, but nobody I know watches TV anymore.", "La pub télé est correcte, mais plus personne autour de moi ne regarde la télé."],
        ["TIKTOK", "@hugo.eats", 0, 1, "Duetting this. My version is spicier.", "Je fais un duo. Ma version est plus épicée."],
        ["X", "@pauline_v", 3, -1, "Another brand trying to become a meme. Pass.", "Encore une marque qui veut devenir un mème. Non merci."],
        ["INSTAGRAM", "@mum.of.three", 1, 1, "Where do you find it? Still not in my supermarket.", "Où est-ce qu'on le trouve ? Toujours pas dans mon supermarché."],
        ["YOUTUBE", "@foodtest", 0, 0, "Tested the three recipes from the campaign. Two out of three work.", "J'ai testé les trois recettes de la campagne. Deux sur trois fonctionnent."],
        ["FACEBOOK", "@jp.lambert", 2, -1, "Saw the ad twelve times during the match. Too much.", "Vu la pub douze fois pendant le match. Trop."],
        ["TIKTOK", "@sarah.k", 1, 1, "Added to cart, no questions asked.", "Ajouté au panier, sans réfléchir."],
        ["INSTAGRAM", "@ben.foodie", 0, 1, "Everyone on my feed is making this now.", "Tout mon fil fait cette recette en ce moment."]
      ]
    },
    brand: {
      label: ["Negative spike, week 6", "Pic négatif, semaine 6"],
      themes: [
        { name: ["Delivery", "Livraison"], w: 0.62, color: "#E2468D" },
        { name: ["Price", "Prix"], w: 0.18, color: "#4292F2" },
        { name: ["Product", "Produit"], w: 0.12, color: "#7B6CF2" },
        { name: ["Service", "Service"], w: 0.08, color: "#3CC2A6" }
      ],
      answer: ["<b>A delivery problem, not a reputation crisis.</b> 62 % of the negative posts are about late parcels. The product itself is still praised, even by the people who complain.",
               "<b>Un problème de livraison, pas une crise de réputation.</b> 62 % des posts négatifs parlent de colis en retard. Le produit reste salué, même par ceux qui se plaignent."],
      posts: [
        ["X", "@karim_d", 0, -1, "Ordered on the 3rd, still nothing. Tracking says 'in preparation' for a week.", "Commandé le 3, toujours rien. Le suivi indique « en préparation » depuis une semaine."],
        ["FACEBOOK", "@martine.g", 0, -1, "Parcel left in front of the building, in the rain. Great.", "Colis laissé devant l'immeuble, sous la pluie. Génial."],
        ["INSTAGRAM", "@lucie.m", 2, 1, "The product is still great, that's why the delivery annoys me this much.", "Le produit est toujours top, c'est pour ça que la livraison m'agace autant."],
        ["X", "@alex_r", 1, -1, "Two euros more in a year, same size. We noticed.", "Deux euros de plus en un an, même format. On a remarqué."],
        ["TIKTOK", "@ines.vlog", 0, -1, "Day 9 of waiting for my order: a series.", "Jour 9 d'attente de ma commande : une série."],
        ["LINKEDIN", "@s.dubois", 3, 1, "Customer service called me back within the hour. Rare enough to say it.", "Le service client m'a rappelé dans l'heure. Assez rare pour le dire."],
        ["X", "@yannick_p", 0, -1, "Three orders, three late deliveries. Something changed in their logistics.", "Trois commandes, trois retards. Quelque chose a changé dans leur logistique."],
        ["FACEBOOK", "@nathalie.r", 1, 0, "Still worth it, just less than before.", "Ça reste intéressant, juste moins qu'avant."],
        ["INSTAGRAM", "@marco.t", 0, -1, "Cancelled and reordered in store. Faster.", "Annulé, recommandé en magasin. Plus rapide."]
      ]
    },
    audiences: {
      label: ["Who writes about the brand", "Qui parle de la marque"],
      themes: [
        { name: ["Parents", "Parents"], w: 0.41, color: "#F4A93B" },
        { name: ["Students", "Étudiants"], w: 0.22, color: "#E2468D" },
        { name: ["Sport fans", "Sportifs"], w: 0.21, color: "#3CC2A6" },
        { name: ["Seniors", "Seniors"], w: 0.16, color: "#4292F2" }
      ],
      answer: ["<b>Not the audience in the brief.</b> Parents write 41 % of the posts; the 18-24 target barely 22 %. They talk about saving time, not about recipes.",
               "<b>Pas l'audience du brief.</b> Les parents écrivent 41 % des posts ; la cible 18-24 ans à peine 22 %. Ils parlent de temps gagné, pas de recettes."],
      posts: [
        ["FACEBOOK", "@claire.maman", 0, 1, "The only thing my kids eat without negotiating.", "La seule chose que mes enfants mangent sans négocier."],
        ["INSTAGRAM", "@papa.en.cuisine", 0, 1, "Wednesday dinner sorted in ten minutes.", "Dîner du mercredi réglé en dix minutes."],
        ["TIKTOK", "@student.budget", 1, 1, "Student budget meal of the week.", "Repas budget étudiant de la semaine."],
        ["YOUTUBE", "@runlab", 2, 0, "Checked the protein content. Fine after a run, not more.", "J'ai vérifié les protéines. Correct après une course, pas plus."],
        ["FACEBOOK", "@jacqueline.m", 3, 1, "Been buying it for twenty years. Please don't change it.", "Je l'achète depuis vingt ans. Ne le changez pas, s'il vous plaît."],
        ["INSTAGRAM", "@mum.of.three", 0, 0, "Lunchbox idea: it survives the school bag.", "Idée de lunchbox : ça survit au cartable."],
        ["TIKTOK", "@coloc.paris", 1, 1, "Flatshare staple.", "Incontournable de la coloc."],
        ["X", "@gym_theo", 2, -1, "Too much sugar for what it promises.", "Trop de sucre pour ce que ça promet."],
        ["FACEBOOK", "@parents.presses", 0, 1, "Saved my evening again.", "Ça m'a encore sauvé la soirée."]
      ]
    },
    trends: {
      label: ["Food conversation, last quarter", "Conversation food, dernier trimestre"],
      themes: [
        { name: ["High protein", "Protéiné"], w: 0.38, color: "#F4A93B" },
        { name: ["Gut health", "Santé intestinale"], w: 0.27, color: "#3CC2A6" },
        { name: ["Upcycled food", "Alimentation upcyclée"], w: 0.21, color: "#7B6CF2" },
        { name: ["Meal kits", "Box repas"], w: 0.14, color: "#E2468D" }
      ],
      answer: ["<b>Protein is the loudest, upcycled food is the one to watch.</b> It is only 21 % of the posts, but most of them are new this quarter. Meal kits are fading.",
               "<b>Le protéiné fait le plus de bruit, l'upcyclé est à surveiller.</b> Seulement 21 % des posts, mais la plupart datent de ce trimestre. Les box repas reculent."],
      posts: [
        ["TIKTOK", "@nutri.jade", 0, 1, "High-protein snack ranking, part 4.", "Classement des snacks protéinés, partie 4."],
        ["INSTAGRAM", "@happy.gut", 1, 1, "Kefir in everything this month.", "Du kéfir partout ce mois-ci."],
        ["LINKEDIN", "@m.laurent", 2, 1, "Bread made from brewers' grain: the startup raised again.", "Du pain fait avec des drêches de brasserie : la startup a encore levé des fonds."],
        ["X", "@kit.fatigue", 3, -1, "Cancelled my meal kit. Cooking again.", "J'ai résilié ma box repas. Je recuisine."],
        ["TIKTOK", "@maman.fit", 0, 1, "Protein pancakes the kids actually like.", "Des pancakes protéinés que les enfants aiment vraiment."],
        ["YOUTUBE", "@zero.gaspi", 2, 1, "Cooking with what supermarkets throw away.", "Cuisiner avec ce que les supermarchés jettent."],
        ["INSTAGRAM", "@dr.flore", 1, 0, "Probiotics: what the studies say, and what they don't.", "Probiotiques : ce que disent les études, et ce qu'elles ne disent pas."],
        ["FACEBOOK", "@sylvie.b", 3, -1, "Too expensive for what's in the box.", "Trop cher pour ce qu'il y a dans la box."]
      ]
    }
  };

  var PLATFORM_NAMES = { TIKTOK: "TikTok", INSTAGRAM: "Instagram", X: "X", YOUTUBE: "YouTube", LINKEDIN: "LinkedIn", FACEBOOK: "Facebook", TWITCH: "Twitch" };
  var READ_TOTAL = { communication: 11400, brand: 8230, audiences: 15640, trends: 42300 };

  var current = null, visible = false, timers = [], cleanup = [];
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function every(fn, ms) { var id = setInterval(fn, ms); timers.push(id); return id; }
  function stopAll() {
    timers.forEach(function (id) { clearTimeout(id); clearInterval(id); });
    timers = [];
    cleanup.forEach(function (fn) { fn(); });
    cleanup = [];
  }

  /* ============================================================ frame */
  function frame(title, hint, body) {
    return '<div class="uv">' +
        '<div class="uv__head">' +
          '<span class="uv__live"><i></i>' + t("Live", "En direct") + "</span>" +
          '<p class="uv__title">' + title + "</p>" +
          '<span class="uv__tag">' + t("Illustrative data", "Données illustratives") + "</span>" +
        "</div>" +
        '<p class="uv__hint"><span aria-hidden="true">✦</span>' + hint + "</p>" +
        '<div class="uv__body">' + body + "</div>" +
      "</div>" +
      '<aside class="lf__read">' +
        '<p class="lf__k">' + t("Posts read", "Posts lus") + "</p>" +
        '<p class="lf__count" id="uv-count">0</p>' +
        '<p class="lf__k">' + t("Latest posts", "Derniers posts") + "</p>" +
        '<div class="mps" id="uv-posts"></div>' +
        '<div class="lf__answer" id="uv-answer" aria-live="polite"><p class="lf__reading">' + t("Reading", "Lecture en cours") +
          '<span class="lf__dots"><i></i><i></i><i></i></span></p></div>' +
        '<a class="btn btn--primary lf__cta" href="#book">' + t("Book a meeting", "Prendre rendez-vous") + ' <span aria-hidden="true">→</span></a>' +
      "</aside>";
  }

  function postHTML(p) {
    return '<div class="mp">' +
      '<p class="mp__meta">' + ((window.LicterIcons || {})[p[0]] || "") + "<b>" + esc(p[1]) + "</b><span>" + PLATFORM_NAMES[p[0]] + "</span></p>" +
      '<p class="mp__text">' + esc(fr() ? p[5] : p[4]) + "</p></div>";
  }

  /* the count climbs, two posts rotate, then the answer lands */
  function runSide(key) {
    var d = DATA[key], target = READ_TOTAL[key];
    var countEl = document.getElementById("uv-count");
    var postsEl = document.getElementById("uv-posts");
    var answerEl = document.getElementById("uv-answer");
    var i = 0;
    function showPosts() {
      postsEl.innerHTML = postHTML(d.posts[i % d.posts.length]) + postHTML(d.posts[(i + 1) % d.posts.length]);
      postsEl.classList.remove("is-in"); void postsEl.offsetWidth; postsEl.classList.add("is-in");
      i += 1;
    }
    function answer() {
      answerEl.classList.add("is-in");
      answerEl.innerHTML = '<p class="lf__k">' + t("What it means", "Ce que ça veut dire") + "</p><p>" + L(d.answer) + "</p>";
    }
    showPosts();
    if (reduced.matches) { countEl.textContent = num(target); answer(); return; }
    var start = performance.now(), DUR = 3200;
    (function tick(now) {
      var k = Math.min(1, (now - start) / DUR);
      countEl.textContent = num(target * (1 - Math.pow(1 - k, 3)));
      if (k < 1 && current === key) requestAnimationFrame(tick);
    })(start);
    later(answer, DUR + 300);
    every(showPosts, 3600);
  }

  /* ================================================= 1. communication */
  function communication() {
    var D = 42, L0 = 21, V = [], CAT = [];
    for (var d = 0; d < D; d++) {
      var v = 800 + 70 * Math.sin(d * 1.3) + 40 * Math.cos(d * 0.7);
      if (d >= L0) v += 2500 * Math.exp(-Math.pow(d - 22.5, 2) / 5) + 760 * (1 - Math.exp(-(d - L0) / 5)) + 380 * Math.exp(-Math.pow(d - 34, 2) / 3);
      V.push(Math.round(v));
      CAT.push(Math.round(930 + 40 * Math.sin(d * 0.5)));
    }
    var PEAKS = [
      { d: 23, pf: "TIKTOK", h: "@chef.maud", txt: ["The recipe video that started it: 1.2M views in 48 hours.", "La vidéo recette qui a tout lancé : 1,2 M de vues en 48 heures."] },
      { d: 27, pf: "INSTAGRAM", h: "@thomas.run", txt: ["Stories reshare the recipe three days in a row.", "Les stories repartagent la recette trois jours d'affilée."] },
      { d: 34, pf: "YOUTUBE", h: "@foodtest", txt: ["A long test of the three recipes brings it back.", "Un long test des trois recettes relance la conversation."] }
    ];
    var W = 640, H = 290, P = { l: 44, r: 16, t: 22, b: 30 };
    function X(d) { return P.l + d * (W - P.l - P.r) / (D - 1); }
    function Y(v) { return P.t + (1 - v / 4000) * (H - P.t - P.b); }
    function line(a) { return a.map(function (v, i) { return (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(v).toFixed(1); }).join(" "); }
    var area = line(V) + " L" + X(D - 1) + " " + (H - P.b) + " L" + X(0) + " " + (H - P.b) + " Z";
    var grid = [0, 1000, 2000, 3000, 4000].map(function (v) {
      return '<line class="g" x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/>' +
        '<text class="ax" x="' + (P.l - 8) + '" y="' + (Y(v) + 3.5) + '" text-anchor="end">' + (v ? v / 1000 + "k" : "0") + "</text>";
    }).join("");
    var weeks = [0, 7, 14, 21, 28, 35].map(function (d, i) {
      return '<text class="ax" x="' + X(d + 3) + '" y="' + (H - 8) + '" text-anchor="middle">' + t("Week ", "Sem. ") + (i + 1) + "</text>";
    }).join("");
    var pins = PEAKS.map(function (p, i) {
      return '<g class="pin" tabindex="0" role="button" data-i="' + i + '" transform="translate(' + X(p.d).toFixed(1) + "," + Y(V[p.d]).toFixed(1) + ')" aria-label="' + esc(L(p.txt)) + '">' +
        '<circle class="pin__halo" r="13"/><circle class="pin__dot" r="5.5"/></g>';
    }).join("");
    var svg =
      '<svg class="uv-svg" id="c-svg" viewBox="0 0 ' + W + " " + H + '" role="group" aria-label="' + t("Daily volume of posts over six weeks", "Volume quotidien de posts sur six semaines") + '">' +
        '<defs><linearGradient id="c-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAA93D" stop-opacity=".38"/><stop offset="1" stop-color="#EAA93D" stop-opacity="0"/></linearGradient></defs>' +
        grid + weeks +
        '<rect class="after" id="c-after" y="' + P.t + '" height="' + (H - P.t - P.b) + '"/>' +
        '<path class="area" d="' + area + '"/>' +
        '<path class="cat" d="' + line(CAT) + '"/>' +
        '<text class="cat__t" x="' + (W - P.r) + '" y="' + (Y(CAT[D - 1]) + 16) + '" text-anchor="end">' + t("Category average", "Moyenne de la catégorie") + "</text>" +
        '<path class="brand draw" pathLength="1" d="' + line(V) + '"/>' +
        '<g id="c-launch" class="launch"><line y1="' + (P.t - 6) + '" y2="' + (H - P.b) + '"/>' +
          '<rect x="-34" y="' + (P.t - 20) + '" width="68" height="22" rx="11"/>' +
          '<text y="' + (P.t - 5) + '" text-anchor="middle">' + t("Launch", "Lancement") + "</text>" +
          '<circle class="launch__grip" cy="' + ((P.t + H - P.b) / 2) + '" r="9"/></g>' +
        pins +
      "</svg>";
    var body =
      '<div class="kchips">' +
        '<div class="kchip"><span>' + t("Before", "Avant") + '</span><b id="c-b"></b></div>' +
        '<div class="kchip"><span>' + t("After", "Après") + '</span><b id="c-a"></b></div>' +
        '<div class="kchip kchip--hi"><span>' + t("Uplift", "Gain") + '</span><b id="c-u"></b></div>' +
      "</div>" +
      '<div class="uv-chart" id="c-chart">' + svg + '<div class="uv-tip" id="c-tip" hidden></div></div>' +
      '<input class="visually-hidden" type="range" id="c-range" min="4" max="37" value="' + L0 + '" aria-label="' + t("Campaign launch day", "Jour du lancement") + '" />';
    stage.innerHTML = frame(t("Posts per day, six weeks", "Posts par jour, six semaines"),
      t("Drag the launch line. Hover the peaks.", "Déplacez la ligne de lancement. Survolez les pics."), body);

    var svgEl = document.getElementById("c-svg"), g = document.getElementById("c-launch"), after = document.getElementById("c-after");
    var range = document.getElementById("c-range"), tip = document.getElementById("c-tip"), chart = document.getElementById("c-chart");
    var launch = L0;
    function avg(a) { return a.reduce(function (s, v) { return s + v; }, 0) / (a.length || 1); }
    function update() {
      var x = (X(launch - 1) + X(launch)) / 2;
      g.setAttribute("transform", "translate(" + x.toFixed(1) + ",0)");
      after.setAttribute("x", x.toFixed(1)); after.setAttribute("width", (W - P.r - x).toFixed(1));
      var b = avg(V.slice(Math.max(0, launch - 14), launch)), a = avg(V.slice(launch, launch + 14));
      document.getElementById("c-b").textContent = num(b) + t("/day", "/jour");
      document.getElementById("c-a").textContent = num(a) + t("/day", "/jour");
      var up = (a / b - 1) * 100;
      document.getElementById("c-u").textContent = (up >= 0 ? "+" : "") + Math.round(up) + " %";
      range.value = launch;
    }
    function fromPointer(e) {
      var r = svgEl.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * W;
      launch = Math.max(4, Math.min(37, Math.round((x - P.l) / ((W - P.l - P.r) / (D - 1)) + 0.5)));
      update();
    }
    var dragging = false;
    svgEl.addEventListener("pointerdown", function (e) {
      if (e.target.closest(".pin")) return;
      dragging = true; svgEl.setPointerCapture(e.pointerId); fromPointer(e);
    });
    svgEl.addEventListener("pointermove", function (e) { if (dragging) fromPointer(e); });
    svgEl.addEventListener("pointerup", function () { dragging = false; });
    range.addEventListener("input", function () { launch = +range.value; update(); });

    function showTip(i) {
      var p = PEAKS[i];
      tip.innerHTML = '<p class="uv-tip__meta">' + ((window.LicterIcons || {})[p.pf] || "") + "<b>" + p.h + "</b> · " + PLATFORM_NAMES[p.pf] + "</p><p>" + L(p.txt) + "</p>";
      tip.style.left = (X(p.d) / W * 100) + "%";
      tip.style.top = (Y(V[p.d]) / H * 100) + "%";
      tip.hidden = false;
    }
    Array.prototype.forEach.call(chart.querySelectorAll(".pin"), function (el) {
      var i = +el.dataset.i;
      el.addEventListener("mouseenter", function () { showTip(i); });
      el.addEventListener("focus", function () { showTip(i); });
      el.addEventListener("click", function () { showTip(i); });
      el.addEventListener("mouseleave", function () { tip.hidden = true; });
      el.addEventListener("blur", function () { tip.hidden = true; });
    });
    update();
  }

  /* ======================================================== 2. brand */
  var WORDS = [
    ["delivery", "livraison", 10, -1], ["late", "retard", 8, -1], ["parcel", "colis", 7, -1], ["price", "prix", 7, -1],
    ["order", "commande", 6, 0], ["product", "produit", 6, 1], ["tracking", "suivi", 5, -1], ["great", "top", 5, 1],
    ["quality", "qualité", 5, 1], ["waiting", "attente", 5, -1], ["expensive", "cher", 4, -1], ["taste", "goût", 4, 1],
    ["customer service", "service client", 4, 1], ["pack", "format", 4, 0], ["refund", "remboursement", 3, -1],
    ["store", "magasin", 3, 0], ["love it", "j'adore", 3, 1], ["app", "appli", 3, 0], ["promo", "promo", 3, 0],
    ["quick reply", "réponse rapide", 3, 1], ["cancelled", "annulé", 3, -1], ["recipe", "recette", 2, 1], ["size", "taille", 2, 0]
  ];
  var TONE = { "-1": "neg", "0": "neu", "1": "pos" };

  function brand() {
    var on = { neg: true, neu: true, pos: true };
    var body =
      '<div class="tones" role="group" aria-label="' + t("Tone", "Tonalité") + '">' +
        [["neg", t("Negative", "Négatif")], ["neu", t("Neutral", "Neutre")], ["pos", t("Positive", "Positif")]].map(function (x) {
          return '<button class="tone tone--' + x[0] + ' is-on" type="button" data-t="' + x[0] + '" aria-pressed="true"><i></i>' + x[1] + "</button>";
        }).join("") +
      "</div>" +
      '<div class="cloud" id="b-cloud"></div>' +
      '<div class="quotes" id="b-q"><p class="quotes__hint">' + t("Click a word to read what people actually wrote.", "Cliquez un mot pour lire ce que les gens ont vraiment écrit.") + "</p></div>";
    stage.innerHTML = frame(t("What people say about the brand", "Ce que les gens disent de la marque"),
      t("Filter by tone. Click a word.", "Filtrez par ton. Cliquez un mot."), body);

    var cloud = document.getElementById("b-cloud"), q = document.getElementById("b-q");
    var font = getComputedStyle(document.body).fontFamily;
    var ctx = document.createElement("canvas").getContext("2d");

    function layout() {
      var Wc = cloud.clientWidth || 600, Hc = cloud.clientHeight || 300, cx = Wc / 2, cy = Hc / 2;
      var scale = Math.max(.72, Math.min(1, Wc / 640));
      var placed = [], out = "";
      WORDS.forEach(function (w, i) {
        var label = fr() ? w[1] : w[0], size = Math.round((12 + w[2] * 3.3) * scale);
        ctx.font = "700 " + size + "px " + font;
        var bw = ctx.measureText(label).width + 10, bh = size * 1.1;
        for (var s = 0; s < 1200; s += 1) {
          var a = s * 0.32, r = 2.2 * a;
          var x = cx + r * Math.cos(a) * 1.7 - bw / 2, y = cy + r * Math.sin(a) - bh / 2;
          if (x < 2 || y < 2 || x + bw > Wc - 2 || y + bh > Hc - 2) continue;
          var hit = placed.some(function (p) { return x < p[0] + p[2] + 4 && x + bw + 4 > p[0] && y < p[1] + p[3] + 2 && y + bh + 2 > p[1]; });
          if (hit) continue;
          placed.push([x, y, bw, bh]);
          out += '<button class="word word--' + TONE[w[3]] + '" type="button" data-i="' + i + '" style="left:' + x.toFixed(0) + "px;top:" + y.toFixed(0) +
            "px;font-size:" + size + "px;--d:" + (i * 45) + 'ms">' + esc(label) + "</button>";
          break;
        }
      });
      cloud.innerHTML = out;
      filter();
    }
    function filter() {
      Array.prototype.forEach.call(cloud.querySelectorAll(".word"), function (el) {
        var tone = TONE[WORDS[+el.dataset.i][3]];
        el.classList.toggle("is-off", !on[tone]);
        el.tabIndex = on[tone] ? 0 : -1;
      });
    }
    function quotesFor(w) {
      var posts = DATA.brand.posts, key = w[0].split(" ")[0].toLowerCase();
      var hits = posts.filter(function (p) { return p[4].toLowerCase().indexOf(key) >= 0; });
      if (hits.length < 2) hits = hits.concat(posts.filter(function (p) { return p[3] === w[3] && hits.indexOf(p) < 0; }));
      return hits.slice(0, 2);
    }
    cloud.addEventListener("click", function (e) {
      var el = e.target.closest(".word"); if (!el) return;
      Array.prototype.forEach.call(cloud.querySelectorAll(".word"), function (x) { x.classList.toggle("is-on", x === el); });
      var w = WORDS[+el.dataset.i];
      q.innerHTML = '<p class="quotes__head"><b class="word--' + TONE[w[3]] + '">' + esc(fr() ? w[1] : w[0]) + "</b> · " +
        num(w[2] * 137 + 42) + " " + t("mentions", "mentions") + "</p>" +
        quotesFor(w).map(function (p) {
          return '<blockquote class="quote"><p>' + esc(fr() ? p[5] : p[4]) + "</p><cite>" + esc(p[1]) + " · " + PLATFORM_NAMES[p[0]] + "</cite></blockquote>";
        }).join("");
    });
    stage.querySelector(".tones").addEventListener("click", function (e) {
      var b = e.target.closest(".tone"); if (!b) return;
      on[b.dataset.t] = !on[b.dataset.t];
      b.classList.toggle("is-on", on[b.dataset.t]); b.setAttribute("aria-pressed", on[b.dataset.t] ? "true" : "false");
      filter();
    });
    layout();
    var rt = null;
    function onResize() { clearTimeout(rt); rt = setTimeout(layout, 150); }
    window.addEventListener("resize", onResize);
    cleanup.push(function () { window.removeEventListener("resize", onResize); });
  }

  /* ===================================================== 3. audiences */
  var SEGMENTS = [
    { name: ["Parents", "Parents"], share: 41, age: "30–44", color: "#EAA93D", x: 190, y: 170,
      platforms: [["Instagram", 62], ["Facebook", 48], ["YouTube", 41]],
      interests: [["Batch cooking", "Batch cooking"], ["School runs", "Trajets d'école"], ["Budget", "Budget"]],
      expect: ["Time saved, not recipes.", "Du temps gagné, pas des recettes."] },
    { name: ["Students", "Étudiants"], share: 22, age: "18–24", color: "#E2468D", x: 395, y: 90, brief: true,
      platforms: [["TikTok", 78], ["Instagram", 55], ["Twitch", 31]],
      interests: [["Quick recipes", "Recettes rapides"], ["Flatshare", "Coloc"], ["Dupes", "Dupes"]],
      expect: ["Something worth filming.", "Quelque chose qui vaut une vidéo."] },
    { name: ["Sport fans", "Sportifs"], share: 21, age: "25–39", color: "#3CC2A6", x: 400, y: 245,
      platforms: [["Instagram", 51], ["YouTube", 47], ["Strava", 29]],
      interests: [["Protein", "Protéines"], ["Labels", "Étiquettes"], ["Running", "Course"]],
      expect: ["Proof, not promises.", "Des preuves, pas des promesses."] },
    { name: ["Seniors", "Seniors"], share: 16, age: "55+", color: "#4292F2", x: 75, y: 60,
      platforms: [["Facebook", 64], ["YouTube", 35], ["Pinterest", 22]],
      interests: [["Tradition", "Tradition"], ["Quality", "Qualité"], ["Price", "Prix"]],
      expect: ["Don't change the recipe.", "Ne changez pas la recette."] }
  ];
  var LINKS = [[0, 1, 3], [0, 2, 2], [1, 2, 4], [0, 3, 3], [1, 3, 1]];

  function audiences() {
    var sel = 0, brief = false;
    function R(s) { return 20 + Math.sqrt(s.share) * 6.4; }
    var W = 480, H = 310;
    var defs = SEGMENTS.map(function (s, i) {
      return '<radialGradient id="a-g' + i + '" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".85"/>' +
        '<stop offset=".55" stop-color="' + s.color + '" stop-opacity=".55"/><stop offset="1" stop-color="' + s.color + '" stop-opacity=".9"/></radialGradient>';
    }).join("");
    var links = LINKS.map(function (l) {
      var a = SEGMENTS[l[0]], b = SEGMENTS[l[1]];
      return '<line class="alink" x1="' + a.x + '" y1="' + a.y + '" x2="' + b.x + '" y2="' + b.y + '" stroke-width="' + (l[2] * 1.4) + '"/>';
    }).join("");
    var nodes = SEGMENTS.map(function (s, i) {
      var r = R(s);
      return '<g class="seg" data-i="' + i + '" tabindex="0" role="button" transform="translate(' + s.x + "," + s.y + ')" style="--c:' + s.color + '" aria-label="' + esc(L(s.name)) + ", " + s.share + '%">' +
        '<circle class="seg__ring" r="' + (r + 7) + '"/>' +
        '<circle class="seg__disc" r="' + r + '" fill="url(#a-g' + i + ')"/>' +
        '<text class="seg__n" y="5" text-anchor="middle">' + s.share + "%</text>" +
        '<text class="seg__name" y="' + (r + 20) + '" text-anchor="middle">' + esc(L(s.name)) + "</text></g>";
    }).join("");
    var b = SEGMENTS[1], br = R(b) + 18;
    var body =
      '<div class="aud">' +
        '<div class="aud__map">' +
          '<svg class="uv-svg" viewBox="0 0 ' + W + " " + H + '" role="group" aria-label="' + t("Communities talking about the brand", "Communautés qui parlent de la marque") + '">' +
            "<defs>" + defs + "</defs>" + links + nodes +
            '<g class="brief" id="a-brief" transform="translate(' + b.x + "," + b.y + ')"><circle r="' + br + '"/>' +
              '<text y="' + (-br - 8) + '" text-anchor="middle">' + t("The brief's target, 18–24", "La cible du brief, 18-24 ans") + "</text></g>" +
          "</svg>" +
          '<button class="brief-btn" type="button" id="a-btn" aria-pressed="false"><i></i>' + t("Show the brief's target", "Montrer la cible du brief") + "</button>" +
        "</div>" +
        '<div class="aud__card" id="a-card"></div>' +
      "</div>" +
      '<p class="aud__note" id="a-note" hidden>' + t("<b>The brief put 60 % of the media budget on 18–24s.</b> They write 22 % of the posts. Parents write 41 %.",
        "<b>Le brief mettait 60 % du budget média sur les 18-24 ans.</b> Ils écrivent 22 % des posts. Les parents, 41 %.") + "</p>";
    stage.innerHTML = frame(t("Who actually talks about the brand", "Qui parle vraiment de la marque"),
      t("Click a community. Compare with the brief.", "Cliquez une communauté. Comparez avec le brief."), body);

    var map = stage.querySelector(".aud__map svg");
    function draw() {
      var s = SEGMENTS[sel];
      Array.prototype.forEach.call(map.querySelectorAll(".seg"), function (g, i) {
        g.classList.toggle("is-on", i === sel);
        g.setAttribute("aria-pressed", i === sel ? "true" : "false");
      });
      document.getElementById("a-card").innerHTML =
        '<p class="acard__name" style="--c:' + s.color + '"><i></i>' + esc(L(s.name)) + "</p>" +
        '<p class="acard__meta">' + s.share + " % " + t("of the posts", "des posts") + " · " + s.age + " " + t("years", "ans") + "</p>" +
        '<p class="acard__k">' + t("Where they are", "Où ils sont") + "</p>" +
        s.platforms.map(function (p) {
          return '<div class="abar"><span>' + p[0] + '</span><span class="abar__t"><i style="width:' + p[1] + "%;background:" + s.color + '"></i></span><b>' + p[1] + "%</b></div>";
        }).join("") +
        '<p class="acard__k">' + t("What they talk about", "De quoi ils parlent") + "</p>" +
        '<p class="acard__tags">' + s.interests.map(function (x) { return "<span>" + esc(L(x)) + "</span>"; }).join("") + "</p>" +
        '<p class="acard__expect">“' + esc(L(s.expect)) + "”</p>";
    }
    function pick(e) {
      var g = e.target.closest(".seg"); if (!g) return;
      if (e.type === "keydown" && e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault(); sel = +g.dataset.i; draw();
    }
    map.addEventListener("click", pick);
    map.addEventListener("keydown", pick);
    document.getElementById("a-btn").addEventListener("click", function () {
      brief = !brief;
      this.setAttribute("aria-pressed", brief ? "true" : "false");
      this.classList.toggle("is-on", brief);
      stage.querySelector(".aud").classList.toggle("show-brief", brief);
      document.getElementById("a-note").hidden = !brief;
    });
    draw();
  }

  /* ======================================================== 4. trends */
  var TRENDS = [
    { name: ["Upcycled food", "Alimentation upcyclée"], from: [6, 8], to: [20, 92], verdict: ["Small, but growing fastest. Worth a pilot now, before it is obvious.", "Petit, mais c'est ce qui croît le plus vite. À tester maintenant, avant que ce soit évident."] },
    { name: ["High-protein snacks", "Snacks protéinés"], from: [14, 24], to: [62, 76], verdict: ["Moved from gyms to parents. Mainstream within a year.", "Passé des salles de sport aux parents. Grand public d'ici un an."] },
    { name: ["Gut health", "Santé intestinale"], from: [24, 30], to: [56, 60], verdict: ["Steady climb, driven by creators. A safe bet for messaging.", "Montée régulière, portée par les créateurs. Un pari sûr pour le discours."] },
    { name: ["Plant-based milk", "Laits végétaux"], from: [72, 44], to: [84, 2], verdict: ["Big and flat. Compete on price and taste, not novelty.", "Gros et stable. Se battre sur le prix et le goût, pas sur la nouveauté."] },
    { name: ["Zero-sugar drinks", "Boissons zéro sucre"], from: [56, 26], to: [62, 20], verdict: ["Mature. No reason to lead with it.", "Mature. Aucune raison d'en faire un argument principal."] },
    { name: ["Meal kits", "Box repas"], from: [52, 22], to: [34, -14], verdict: ["Fading since the pandemic peak. Do not build here.", "En recul depuis le pic du confinement. Ne pas investir ici."] }
  ];
  var MONTHS = 18;

  function trends() {
    var month = 0, sel = 0, timer = null;
    var body =
      '<div class="radar2">' +
        '<div class="radar2__chart" id="t-chart"></div>' +
        '<div class="radar2__card" id="t-card"></div>' +
      "</div>" +
      '<div class="play2">' +
        '<button class="play2__btn" type="button" id="t-play">▶</button>' +
        '<div class="play2__track"><input type="range" id="t-range" min="0" max="' + MONTHS + '" value="0" aria-label="' + t("Month", "Mois") + '" /></div>' +
        '<span class="play2__m" id="t-month"></span>' +
      "</div>";
    stage.innerHTML = frame(t("Food topics, volume against growth", "Sujets food, volume et croissance"),
      t("Press play, then click a topic.", "Lancez la lecture, puis cliquez un sujet."), body);
    var box = document.getElementById("t-chart"), range = document.getElementById("t-range"), btn = document.getElementById("t-play");
    var W = 460, H = 300, P = { l: 30, r: 12, t: 12, b: 26 };
    function X(v) { return P.l + v / 100 * (W - P.l - P.r); }
    function Y(g) { return P.t + (1 - (g + 20) / 120) * (H - P.t - P.b); }
    function pos(tr, m) { var k = m / MONTHS; k = k * k * (3 - 2 * k); return [tr.from[0] + (tr.to[0] - tr.from[0]) * k, tr.from[1] + (tr.to[1] - tr.from[1]) * k]; }
    function draw() {
      var mx = X(45), my = Y(40);
      var q =
        '<rect class="q q--weak" x="' + P.l + '" y="' + P.t + '" width="' + (mx - P.l) + '" height="' + (my - P.t) + '" rx="10"/>' +
        '<rect class="q q--rise" x="' + mx + '" y="' + P.t + '" width="' + (W - P.r - mx) + '" height="' + (my - P.t) + '" rx="10"/>' +
        '<rect class="q q--mat" x="' + mx + '" y="' + my + '" width="' + (W - P.r - mx) + '" height="' + (H - P.b - my) + '" rx="10"/>' +
        '<rect class="q q--fade" x="' + P.l + '" y="' + my + '" width="' + (mx - P.l) + '" height="' + (H - P.b - my) + '" rx="10"/>' +
        /* labels sit against the centre lines, away from the corners the dots end up in */
        '<text class="q__t" x="' + (mx - 10) + '" y="' + (my - 10) + '" text-anchor="end">' + t("Weak signals", "Signaux faibles") + "</text>" +
        '<text class="q__t" x="' + (mx + 10) + '" y="' + (my - 10) + '">' + t("Rising", "En essor") + "</text>" +
        '<text class="q__t" x="' + (mx + 10) + '" y="' + (my + 20) + '">' + t("Mature", "Matures") + "</text>" +
        '<text class="q__t" x="' + (mx - 10) + '" y="' + (my + 20) + '" text-anchor="end">' + t("Fading", "En recul") + "</text>" +
        '<text class="ax" x="' + (W - P.r) + '" y="' + (H - 6) + '" text-anchor="end">' + t("Volume →", "Volume →") + "</text>" +
        '<text class="ax" x="12" y="' + ((P.t + H - P.b) / 2) + '" text-anchor="middle" transform="rotate(-90 12 ' + ((P.t + H - P.b) / 2) + ')">' + t("Growth →", "Croissance →") + "</text>";
      var dots = TRENDS.map(function (tr, i) {
        var p = pos(tr, month), trail = "";
        for (var m = 0; m <= month; m += 2) { var pp = pos(tr, m); trail += (m ? "L" : "M") + X(pp[0]).toFixed(1) + " " + Y(pp[1]).toFixed(1); }
        trail += "L" + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1);
        var right = p[0] > 58;
        return '<path class="trail' + (i === sel ? " is-on" : "") + '" d="' + trail + '"/>' +
          '<g class="tdot2' + (i === sel ? " is-on" : "") + '" data-i="' + i + '" tabindex="0" role="button" transform="translate(' + X(p[0]).toFixed(1) + "," + Y(p[1]).toFixed(1) + ')" aria-label="' + esc(L(tr.name)) + '">' +
          '<circle class="tdot2__halo" r="14"/><circle class="tdot2__dot" r="' + (i === sel ? 7 : 5.5) + '"/>' +
          '<text x="' + (right ? -12 : 12) + '" y="4" text-anchor="' + (right ? "end" : "start") + '">' + esc(L(tr.name)) + "</text></g>";
      }).join("");
      box.innerHTML = '<svg class="uv-svg" viewBox="0 0 ' + W + " " + H + '" role="group" aria-label="' + t("Topics by volume and growth", "Sujets par volume et croissance") + '">' + q + dots + "</svg>";
      var tr = TRENDS[sel], p = pos(tr, month), sp = "", sw = 200, sh = 50;
      /* the curve is the topic's growth, scaled to its own range so every topic reads */
      var gs = []; for (var m = 0; m <= MONTHS; m++) gs.push(pos(tr, m)[1]);
      var lo = Math.min.apply(null, gs), hi = Math.max.apply(null, gs), span = (hi - lo) || 1;
      function SY(g) { return (sh - 6 - (g - lo) / span * (sh - 12)).toFixed(1); }
      gs.forEach(function (g, m) { sp += (m ? "L" : "M") + (m / MONTHS * sw).toFixed(1) + " " + SY(g); });
      var verdictTone = tr.to[1] > 40 ? "go" : tr.to[1] < 0 ? "stop" : "watch";
      document.getElementById("t-card").innerHTML =
        '<p class="tcard__name">' + esc(L(tr.name)) + "</p>" +
        '<div class="tcard__nums"><div><b>' + Math.round(p[0]) + "</b><span>" + t("volume index", "indice de volume") + "</span></div>" +
          "<div><b>" + (p[1] >= 0 ? "+" : "") + Math.round(p[1]) + "%</b><span>" + t("growth", "croissance") + "</span></div></div>" +
        '<svg class="tcard__spark" viewBox="0 0 ' + sw + " " + sh + '" preserveAspectRatio="none" aria-hidden="true"><path d="' + sp + '"/><circle cx="' + (month / MONTHS * sw) + '" cy="' + SY(p[1]) + '" r="3.5"/></svg>' +
        '<p class="tcard__verdict tcard__verdict--' + verdictTone + '">' + esc(L(tr.verdict)) + "</p>";
      document.getElementById("t-month").textContent = t("Month ", "Mois ") + month + " / " + MONTHS;
      range.value = month;
      range.style.setProperty("--fill", (month / MONTHS * 100) + "%");
    }
    function stopPlay() { clearInterval(timer); timer = null; btn.textContent = "▶"; btn.setAttribute("aria-label", t("Play 18 months", "Lire 18 mois")); }
    function play() {
      if (month >= MONTHS) month = 0;
      if (reduced.matches) { month = MONTHS; draw(); return; }
      btn.textContent = "❚❚"; btn.setAttribute("aria-label", t("Pause", "Pause"));
      timer = setInterval(function () { month++; draw(); if (month >= MONTHS) stopPlay(); }, 240);
    }
    btn.addEventListener("click", function () { if (timer) stopPlay(); else play(); });
    range.addEventListener("input", function () { stopPlay(); month = +range.value; draw(); });
    function pick(e) {
      var g = e.target.closest(".tdot2"); if (!g) return;
      if (e.type === "keydown" && e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault(); sel = +g.dataset.i; draw();
    }
    box.addEventListener("click", pick);
    box.addEventListener("keydown", pick);
    stopPlay(); draw();
    later(play, 700);
    cleanup.push(stopPlay);
  }

  /* ============================================================ switch */
  var RENDER = { communication: communication, brand: brand, audiences: audiences, trends: trends };

  function render() {
    stopAll();
    RENDER[current]();
    stage.classList.remove("is-in"); void stage.offsetWidth; stage.classList.add("is-in");
    if (visible) runSide(current);
  }

  function select(key) {
    current = key;
    topics.forEach(function (b) {
      var on = b.dataset.topic === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    stage.setAttribute("aria-labelledby", "tab-" + key);
    stage.classList.add("has-feed");
    render();
  }

  topics.forEach(function (b, i) {
    b.addEventListener("click", function () { select(b.dataset.topic); });
    b.addEventListener("keydown", function (e) {
      var dir = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!dir) return;
      e.preventDefault();
      var n = topics[(i + dir + topics.length) % topics.length];
      n.focus(); select(n.dataset.topic);
    });
  });

  /* the side panel only runs while the section is on screen */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      var was = visible;
      visible = e[0].isIntersecting;
      if (visible && !was && current) render();
    }, { threshold: 0.15 }).observe(stage);
  } else visible = true;

  if (window.MutationObserver) {
    new MutationObserver(function () { if (current) render(); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }
})();
