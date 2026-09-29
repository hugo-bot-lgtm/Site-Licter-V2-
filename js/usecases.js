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
      answer: ["<b>The opportunity is not in the brief.</b> Food creators' followers love the brand but barely buy it: opportunity 86 / 100. Students, the brief's target, score 31.",
               "<b>L'opportunité n'est pas dans le brief.</b> Les abonnés des créateurs food adorent la marque mais l'achètent peu : opportunité 86 / 100. Les étudiants, cible du brief, font 31."],
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

  var current = null, timers = [], cleanup = [];
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

  /* The side panel: two posts rotate; the count and the answer follow the
     visual. A visual calls progress(k) with k from 0 to 1 as it reveals
     itself; at 1 the answer lands. Visuals with nothing to reveal use
     autoProgress(). */
  var gen = 0;
  function runSide(key) {
    var d = DATA[key];
    var postsEl = document.getElementById("uv-posts");
    var i = 0;
    function showPosts() {
      postsEl.innerHTML = postHTML(d.posts[i % d.posts.length]) + postHTML(d.posts[(i + 1) % d.posts.length]);
      postsEl.classList.remove("is-in"); void postsEl.offsetWidth; postsEl.classList.add("is-in");
      i += 1;
    }
    showPosts();
    every(showPosts, 3600);
  }
  var answered = false;
  function progress(k) {
    var countEl = document.getElementById("uv-count"), answerEl = document.getElementById("uv-answer");
    if (!countEl) return;
    k = Math.max(0, Math.min(1, k));
    countEl.textContent = num(READ_TOTAL[current] * k);
    if (k >= 1 && !answered) {
      answered = true;
      answerEl.classList.add("is-in");
      answerEl.innerHTML = '<p class="lf__k">' + t("What it means", "Ce que ça veut dire") + "</p><p>" + L(DATA[current].answer) + "</p>";
    }
  }
  /* runs fn(k) from 0 to 1 over ms, frame by frame, until the topic changes */
  function tween(ms, fn, done) {
    var my = gen, start = performance.now();
    if (reduced.matches) { fn(1); if (done) done(); return; }
    (function step(now) {
      if (my !== gen) return;
      var k = Math.min(1, (now - start) / ms);
      fn(k);
      if (k < 1) requestAnimationFrame(step); else if (done) done();
    })(start);
  }
  function autoProgress() { tween(3200, function (k) { progress(1 - Math.pow(1 - k, 3)); }); }

  /* ================================================= 1. communication */
  function communication() {
    var D = 42, L0 = 21, V = [], CAT = [];
    for (var d = 0; d < D; d++) {
      var v = 800 + 70 * Math.sin(d * 1.3) + 40 * Math.cos(d * 0.7);
      if (d >= L0) v += 2500 * Math.exp(-Math.pow(d - 22.5, 2) / 5) + 760 * (1 - Math.exp(-(d - L0) / 5)) + 380 * Math.exp(-Math.pow(d - 34, 2) / 3);
      V.push(Math.round(v));
      CAT.push(Math.round(930 + 40 * Math.sin(d * 0.5)));
    }
    var CUM = [], acc = 0; V.forEach(function (v) { acc += v; CUM.push(acc); });
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
      return '<g class="pin is-hidden" tabindex="0" role="button" data-i="' + i + '" transform="translate(' + X(p.d).toFixed(1) + "," + Y(V[p.d]).toFixed(1) + ')" aria-label="' + esc(L(p.txt)) + '">' +
        '<circle class="pin__halo" r="13"/><circle class="pin__dot" r="5.5"/></g>';
    }).join("");
    var svg =
      '<svg class="uv-svg is-locked" id="c-svg" viewBox="0 0 ' + W + " " + H + '" role="group" aria-label="' + t("Daily volume of posts over six weeks", "Volume quotidien de posts sur six semaines") + '">' +
        '<defs><linearGradient id="c-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAA93D" stop-opacity=".38"/><stop offset="1" stop-color="#EAA93D" stop-opacity="0"/></linearGradient>' +
          '<clipPath id="c-clip"><rect id="c-reveal" x="0" y="0" width="' + P.l + '" height="' + H + '"/></clipPath></defs>' +
        grid + weeks +
        '<rect class="after" id="c-after" y="' + P.t + '" height="' + (H - P.t - P.b) + '"/>' +
        '<path class="cat" d="' + line(CAT) + '"/>' +
        '<text class="cat__t" x="' + (W - P.r) + '" y="' + (Y(CAT[D - 1]) + 16) + '" text-anchor="end">' + t("Category average", "Moyenne de la catégorie") + "</text>" +
        '<g clip-path="url(#c-clip)"><path class="area" d="' + area + '"/><path class="brand" d="' + line(V) + '"/></g>' +
        '<circle class="head" id="c-head" r="5"/>' +
        '<g id="c-launch" class="launch"><line y1="' + (P.t - 6) + '" y2="' + (H - P.b) + '"/>' +
          '<rect x="-34" y="' + (P.t - 20) + '" width="68" height="22" rx="11"/>' +
          '<text y="' + (P.t - 5) + '" text-anchor="middle">' + t("Launch", "Lancement") + "</text>" +
          '<circle class="launch__grip" cy="' + ((P.t + H - P.b) / 2) + '" r="9"/></g>' +
        pins +
      "</svg>";
    var body =
      '<div class="kchips">' +
        '<div class="kchip"><span>' + t("Before", "Avant") + '</span><b id="c-b">–</b></div>' +
        '<div class="kchip"><span>' + t("After", "Après") + '</span><b id="c-a">–</b></div>' +
        '<div class="kchip kchip--hi"><span>' + t("Uplift", "Gain") + '</span><b id="c-u">–</b></div>' +
        '<span class="kchip__day" id="c-day"></span>' +
      "</div>" +
      '<div class="uv-chart" id="c-chart">' + svg + '<div class="uv-tip" id="c-tip" hidden></div></div>' +
      '<input class="visually-hidden" type="range" id="c-range" min="4" max="37" value="' + L0 + '" disabled aria-label="' + t("Campaign launch day", "Jour du lancement") + '" />';
    stage.innerHTML = frame(t("Posts per day, six weeks", "Posts par jour, six semaines"),
      '<span id="c-hint">' + t("Reading the six weeks…", "Lecture des six semaines…") + "</span>", body);

    var svgEl = document.getElementById("c-svg"), g = document.getElementById("c-launch"), after = document.getElementById("c-after");
    var range = document.getElementById("c-range"), tip = document.getElementById("c-tip"), chart = document.getElementById("c-chart");
    var reveal = document.getElementById("c-reveal"), head = document.getElementById("c-head");
    var launch = L0, shown = 0, ready = false;
    function avg(a) { return a.reduce(function (s, v) { return s + v; }, 0) / (a.length || 1); }
    function update() {
      var x = (X(launch - 1) + X(launch)) / 2;
      g.setAttribute("transform", "translate(" + x.toFixed(1) + ",0)");
      after.setAttribute("x", x.toFixed(1)); after.setAttribute("width", Math.max(0, X(Math.max(launch, shown)) - x).toFixed(1));
      var b = V.slice(Math.max(0, launch - 14), Math.min(launch, shown + 1));
      var a = shown >= launch ? V.slice(launch, Math.min(launch + 14, shown + 1)) : [];
      document.getElementById("c-b").textContent = b.length ? num(avg(b)) + t("/day", "/jour") : "–";
      document.getElementById("c-a").textContent = a.length ? num(avg(a)) + t("/day", "/jour") : "–";
      document.getElementById("c-u").textContent = a.length && b.length ? ((avg(a) / avg(b) - 1) * 100 >= 0 ? "+" : "") + Math.round((avg(a) / avg(b) - 1) * 100) + " %" : "–";
      range.value = launch;
    }
    /* the curve draws itself day by day; the chips and the count follow it */
    tween(4200, function (k) {
      var f = k * (D - 1);
      shown = Math.floor(f);
      var x = X(f);
      reveal.setAttribute("width", x.toFixed(1));
      var i = Math.min(D - 2, shown), v = V[i] + (V[i + 1] - V[i]) * (f - i);
      head.setAttribute("cx", x.toFixed(1)); head.setAttribute("cy", Y(v).toFixed(1));
      Array.prototype.forEach.call(chart.querySelectorAll(".pin"), function (el) {
        if (PEAKS[+el.dataset.i].d <= f) el.classList.remove("is-hidden");
      });
      document.getElementById("c-day").textContent = t("Day ", "Jour ") + (shown + 1) + " / " + D;
      update();
      progress(CUM[shown] / CUM[D - 1]);
    }, function () {
      shown = D - 1; ready = true; update(); progress(1);
      svgEl.classList.remove("is-locked"); range.disabled = false;
      head.style.opacity = "0";
      document.getElementById("c-day").textContent = "";
      document.getElementById("c-hint").textContent = t("Now drag the launch line. Hover the peaks.", "Déplacez maintenant la ligne de lancement. Survolez les pics.");
    });

    function fromPointer(e) {
      var r = svgEl.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * W;
      launch = Math.max(4, Math.min(37, Math.round((x - P.l) / ((W - P.l - P.r) / (D - 1)) + 0.5)));
      update();
    }
    var dragging = false;
    svgEl.addEventListener("pointerdown", function (e) {
      if (!ready || e.target.closest(".pin")) return;
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
          return '<button class="tone tone--' + x[0] + ' is-on" type="button" data-t="' + x[0] + '" aria-pressed="true"><i></i>' + x[1] +
            ' <b class="tone__n" data-n="' + x[0] + '">0</b></button>';
        }).join("") +
      "</div>" +
      '<div class="cloud" id="b-cloud"></div>' +
      '<div class="quotes" id="b-q"><p class="quotes__hint">' + t("Words appear as we read. Click one to see what people actually wrote.", "Les mots apparaissent à mesure que nous lisons. Cliquez-en un pour lire ce que les gens ont vraiment écrit.") + "</p></div>";
    stage.innerHTML = frame(t("What people say about the brand", "Ce que les gens disent de la marque"),
      t("Filter by tone. Click a word.", "Filtrez par ton. Cliquez un mot."), body);

    var cloud = document.getElementById("b-cloud"), q = document.getElementById("b-q");
    var font = getComputedStyle(document.body).fontFamily;
    var ctx = document.createElement("canvas").getContext("2d");
    var order = [], revealed = 0;

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
          out += '<button class="word word--' + TONE[w[3]] + (i < revealed || revealed >= WORDS.length ? " is-shown" : "") + '" type="button" data-i="' + i +
            '" style="left:' + x.toFixed(0) + "px;top:" + y.toFixed(0) + "px;font-size:" + size + 'px">' + esc(label) + "</button>";
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
        el.tabIndex = on[tone] && el.classList.contains("is-shown") ? 0 : -1;
      });
    }
    /* the order words are read in: loud ones first, then the rest shuffled */
    var rest = WORDS.map(function (_, i) { return i; }).slice(4);
    for (var k = rest.length - 1; k > 0; k--) { var j = (k * 7 + 3) % (k + 1), tmp = rest[k]; rest[k] = rest[j]; rest[j] = tmp; }
    order = [0, 1, 3, 2].concat(rest);
    function counts() {
      var n = { neg: 0, neu: 0, pos: 0 };
      order.slice(0, revealed).forEach(function (i) { n[TONE[WORDS[i][3]]] += WORDS[i][2] * 137 + 42; });
      Array.prototype.forEach.call(stage.querySelectorAll(".tone__n"), function (b) { b.textContent = num(n[b.dataset.n]); });
    }
    layout();
    tween(4600, function (k) {
      var target = Math.round(k * WORDS.length);
      while (revealed < target) {
        var el = cloud.querySelector('.word[data-i="' + order[revealed] + '"]');
        if (el) el.classList.add("is-shown");
        revealed++;
      }
      filter(); counts();
      progress(k);
    });

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
    var rt = null;
    function onResize() { clearTimeout(rt); rt = setTimeout(layout, 150); }
    window.addEventListener("resize", onResize);
    cleanup.push(function () { window.removeEventListener("resize", onResize); });
  }

  /* ===================================================== 3. audiences
     The hero's map, with audience communities, and their scores beside it:
     affinity (how much they like the brand), penetration (share already
     buying) and opportunity (room to grow). */
  var AUDIENCES = [
    { name: ["Pragmatic parents", "Parents pragmatiques"], share: 41, aff: 78, pen: 122, opp: 52, color: "#EAA93D",
      x: 0.36, y: 0.52, r: 0.36, n: 2300, swirl: 0.55,
      note: ["Your base. Loyal, already buying: keep them, do not chase them.", "Votre socle. Fidèles, déjà clients : à garder, pas à conquérir."] },
    { name: ["Food creators' followers", "Abonnés des créateurs food"], share: 19, aff: 74, pen: 36, opp: 86, color: "#E2468D",
      x: 0.66, y: 0.26, r: 0.26, n: 1560, swirl: -0.6,
      note: ["Love the brand, barely buy it. The biggest opportunity on the map.", "Aiment la marque, l'achètent peu. La plus grosse opportunité de la carte."] },
    { name: ["Sport fans", "Sportifs"], share: 16, aff: 57, pen: 48, opp: 69, color: "#3CC2A6",
      x: 0.73, y: 0.7, r: 0.24, n: 1400, swirl: 0.5,
      note: ["Interested if the proof is there: labels, protein, tests.", "Intéressés si la preuve suit : étiquettes, protéines, tests."] },
    { name: ["Students", "Étudiants"], share: 14, aff: 36, pen: 30, opp: 31, color: "#7B6CF2",
      x: 0.5, y: 0.83, r: 0.2, n: 1120, swirl: -0.55,
      note: ["The brief's target. Low affinity: expensive to convince.", "La cible du brief. Faible affinité : chers à convaincre."] },
    { name: ["Loyal seniors", "Seniors fidèles"], share: 10, aff: 82, pen: 140, opp: 24, color: "#4292F2",
      x: 0.16, y: 0.24, r: 0.2, n: 1040, swirl: 0.6,
      note: ["Already won. Do not change the recipe.", "Déjà acquis. Ne changez pas la recette."] }
  ];
  var AUD_OUT = [{ x: 0.1, y: 0.62, r: 0.05, n: 12 }, { x: 0.9, y: 0.45, r: 0.05, n: 12 }, { x: 0.88, y: 0.1, r: 0.04, n: 10 }, { x: 0.28, y: 0.9, r: 0.05, n: 12 }];

  function ring(v, color, label) {
    var C = 2 * Math.PI * 26;
    return '<div class="gauge"><svg viewBox="0 0 64 64" aria-hidden="true"><circle class="gauge__bg" cx="32" cy="32" r="26"/>' +
      '<circle class="gauge__v" cx="32" cy="32" r="26" stroke="' + color + '" stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + C.toFixed(1) + '" data-v="' + v + '"/></svg>' +
      '<b>' + v + "</b><span>" + label + "</span></div>";
  }

  function audiences() {
    var sel = 1, map = null;
    var body =
      '<div class="aud2">' +
        '<div class="aud2__map" id="a-map" aria-hidden="true"></div>' +
        '<div class="aud2__side">' +
          '<div class="aud2__focus" id="a-focus" aria-live="polite"></div>' +
          '<ol class="aud2__rank" id="a-rank" aria-label="' + t("Communities by opportunity", "Communautés par opportunité") + '"></ol>' +
        "</div>" +
      "</div>";
    stage.innerHTML = frame(t("Audience communities and their scores", "Communautés d'audience et leurs scores"),
      t("Hover the map or pick a community.", "Survolez la carte ou choisissez une communauté."), body);
    var focusEl = document.getElementById("a-focus"), rankEl = document.getElementById("a-rank");
    var labels = AUDIENCES.map(function (a) { return L(a.name); });

    function focusCard(i) {
      var a = AUDIENCES[i];
      focusEl.style.setProperty("--c", a.color);
      focusEl.innerHTML =
        '<p class="afocus__name"><i></i>' + esc(L(a.name)) + "</p>" +
        '<p class="afocus__meta">' + a.share + " % " + t("of the conversation", "de la conversation") + "</p>" +
        '<div class="gauges">' +
          ring(a.aff, "#EAA93D", t("Affinity", "Affinité")) +
          ring(a.pen, "#4292F2", t("Penetration", "Pénétration")) +
          ring(a.opp, "#2E9E6B", t("Opportunity", "Opportunité")) +
        "</div>" +
        '<p class="afocus__note">' + esc(L(a.note)) + "</p>";
      var C = 2 * Math.PI * 26;
      requestAnimationFrame(function () {
        Array.prototype.forEach.call(focusEl.querySelectorAll(".gauge__v"), function (c) {
          c.style.strokeDashoffset = (C * (1 - (+c.dataset.v) / 100)).toFixed(1);
        });
      });
      Array.prototype.forEach.call(rankEl.children, function (li) { li.classList.toggle("is-on", +li.dataset.i === i); });
    }
    var sorted = AUDIENCES.map(function (a, i) { return i; }).sort(function (a, b) { return AUDIENCES[b].opp - AUDIENCES[a].opp; });
    rankEl.innerHTML = sorted.map(function (i) {
      var a = AUDIENCES[i];
      return '<li data-i="' + i + '" style="--c:' + a.color + '"><button type="button" class="arow" data-i="' + i + '">' +
        '<span class="arow__name"><i></i>' + esc(L(a.name)) + "</span>" +
        '<span class="arow__bars">' +
          '<span class="arow__bar" title="' + t("Affinity", "Affinité") + '"><i style="--w:' + a.aff + '%;background:#EAA93D"></i></span>' +
          '<span class="arow__bar" title="' + t("Penetration", "Pénétration") + '"><i style="--w:' + a.pen + '%;background:#4292F2"></i></span>' +
          '<span class="arow__bar" title="' + t("Opportunity", "Opportunité") + '"><i style="--w:' + a.opp + '%;background:#2E9E6B"></i></span>' +
        "</span><b>" + a.opp + "</b></button></li>";
    }).join("");
    rankEl.insertAdjacentHTML("beforebegin", '<p class="arank__head"><span>' + t("Ranked by opportunity", "Classées par opportunité") + "</span><span class=\"arank__keys\"><i style=\"background:#EAA93D\"></i>" + t("Affinity", "Affinité") +
      '<i style="background:#4292F2"></i>' + t("Penetration", "Pénétration") + '<i style="background:#2E9E6B"></i>' + t("Opportunity", "Opportunité") + "</span></p>");
    rankEl.addEventListener("click", function (e) {
      var b = e.target.closest(".arow"); if (!b) return;
      sel = +b.dataset.i; if (map) map.select(sel); focusCard(sel);
    });

    if (window.LicterMap) {
      map = window.LicterMap(document.getElementById("a-map"), {
        communities: AUDIENCES, outliers: AUD_OUT, labels: labels,
        onHover: function (i) { focusCard(i >= 0 ? i : sel); },
        onSelect: function (i) { sel = i; map.select(i); focusCard(i); }
      });
      if (map) { map.select(sel); cleanup.push(function () { map.destroy(); }); }
    }
    focusCard(sel);
    rankEl.classList.add("is-in");
    autoProgress();
  }

  /* ======================================================== 4. trends
     A race: food topics by volume of conversation, month by month over
     eighteen months. The bars reorder as topics overtake one another. */
  var RACE = [
    { name: ["High-protein snacks", "Snacks protéinés"], color: "#EAA93D", f: function (m) { return 18 + 75 / (1 + Math.exp(-(m - 8) / 2.2)); },
      lead: ["Parents, then gyms", "Les parents, puis les salles de sport"], verdict: ["go", "Mainstream within a year. Build it now.", "Grand public d'ici un an. À lancer maintenant."] },
    { name: ["Gut health", "Santé intestinale"], color: "#3CC2A6", f: function (m) { return 28 + 2.4 * m; },
      lead: ["Food creators", "Créateurs food"], verdict: ["watch", "Steady climb. A safe angle for messaging.", "Montée régulière. Un angle sûr pour le discours."] },
    { name: ["Upcycled food", "Alimentation upcyclée"], color: "#7B6CF2", f: function (m) { return m < 5 ? 2 + m * .3 : 3.5 + Math.pow(m - 5, 1.5) * 1.35; },
      lead: ["Zero-waste communities", "Communautés zéro déchet"], verdict: ["go", "Out of nowhere, fastest riser. Pilot it before it is obvious.", "Parti de rien, la plus forte hausse. À tester avant que ce soit évident."] },
    { name: ["Plant-based milk", "Laits végétaux"], color: "#C6D64A", f: function (m) { return 78 - 0.3 * m + 3 * Math.sin(m); },
      lead: ["Everyone", "Tout le monde"], verdict: ["watch", "Big and flat. Compete on price, not novelty.", "Gros et stable. Se battre sur le prix, pas la nouveauté."] },
    { name: ["Zero-sugar drinks", "Boissons zéro sucre"], color: "#4292F2", f: function (m) { return 60 - 0.45 * m + 2 * Math.cos(m * 0.8); },
      lead: ["Sport fans", "Sportifs"], verdict: ["watch", "Mature. No reason to lead with it.", "Mature. Aucune raison d'en faire un argument."] },
    { name: ["Meal kits", "Box repas"], color: "#E2468D", f: function (m) { return 74 - 2.9 * m; },
      lead: ["Busy couples", "Couples pressés"], verdict: ["stop", "Fading since the pandemic. Do not build here.", "En recul depuis le confinement. Ne pas investir ici."] },
    { name: ["Fermented drinks", "Boissons fermentées"], color: "#F2656F", f: function (m) { return 12 + 1.9 * m + 2 * Math.sin(m * 1.3); },
      lead: ["Health optimisers", "Adeptes du bien-être"], verdict: ["watch", "Rising slowly. Watch for a creator to tip it.", "Monte lentement. Guetter le créateur qui la fera basculer."] },
    { name: ["Mushroom coffee", "Café aux champignons"], color: "#D796E6", f: function (m) { return m < 9 ? 1 + m * .1 : 1.9 + (m - 9) * 3.6; },
      lead: ["Remote workers", "Télétravailleurs"], verdict: ["watch", "Brand new. Too early to bet, worth monitoring.", "Tout nouveau. Trop tôt pour parier, à surveiller."] }
  ];
  var MONTHS = 18;

  function trends() {
    var month = 0, sel = 2, timer = null, prevRank = null;
    var start = new Date(2024, 3, 1);
    function monthLabel(m) {
      var d = new Date(start.getFullYear(), start.getMonth() + m, 1);
      return d.toLocaleDateString(fr() ? "fr-FR" : "en-GB", { month: "short", year: "numeric" });
    }
    var ROW = 36;
    var body =
      '<div class="race2">' +
        '<div class="race" id="t-race" style="height:' + (RACE.length * ROW + 34) + 'px">' +
          '<p class="race__month" id="t-when" aria-hidden="true"></p>' +
          RACE.map(function (r, i) {
            return '<button class="race__row" type="button" data-i="' + i + '" style="--c:' + r.color + '">' +
              '<span class="race__bar"><i></i></span>' +
              '<span class="race__name">' + esc(L(r.name)) + "</span>" +
              '<span class="race__v"></span><span class="race__delta"></span></button>';
          }).join("") +
        "</div>" +
        '<div class="race2__card" id="t-card"></div>' +
      "</div>" +
      '<div class="play2">' +
        '<button class="play2__btn" type="button" id="t-play">▶</button>' +
        '<div class="play2__track"><input type="range" id="t-range" min="0" max="' + MONTHS + '" value="0" aria-label="' + t("Month", "Mois") + '" /></div>' +
        '<span class="play2__m" id="t-month"></span>' +
      "</div>";
    stage.innerHTML = frame(t("Food topics, share of the conversation over 18 months", "Sujets food, part de la conversation sur 18 mois"),
      t("Watch them overtake each other. Click a topic.", "Regardez-les se dépasser. Cliquez un sujet."), body);
    var race = document.getElementById("t-race"), rows = Array.prototype.slice.call(race.querySelectorAll(".race__row"));
    var range = document.getElementById("t-range"), btn = document.getElementById("t-play");

    function vals(m) { return RACE.map(function (r) { return Math.max(0, r.f(m)); }); }
    function draw() {
      var v = vals(month), max = Math.max.apply(null, v);
      var order = v.map(function (x, i) { return i; }).sort(function (a, b) { return v[b] - v[a]; });
      var rank = []; order.forEach(function (i, k) { rank[i] = k; });
      rows.forEach(function (row, i) {
        row.style.transform = "translateY(" + (34 + rank[i] * ROW) + "px)";
        row.querySelector(".race__bar i").style.width = (v[i] / max * 100).toFixed(1) + "%";
        row.querySelector(".race__v").textContent = Math.round(v[i]);
        var d = row.querySelector(".race__delta");
        if (prevRank && prevRank[i] !== rank[i]) { d.textContent = prevRank[i] > rank[i] ? "▲" : "▼"; d.className = "race__delta " + (prevRank[i] > rank[i] ? "is-up" : "is-down"); }
        row.classList.toggle("is-on", i === sel);
        row.setAttribute("aria-label", L(RACE[i].name) + ", " + (rank[i] + 1) + ", " + Math.round(v[i]));
      });
      prevRank = rank;
      document.getElementById("t-when").textContent = monthLabel(month);
      document.getElementById("t-month").textContent = t("Month ", "Mois ") + month + " / " + MONTHS;
      range.value = month; range.style.setProperty("--fill", (month / MONTHS * 100) + "%");
      card();
      progress(month / MONTHS);
    }
    function card() {
      var r = RACE[sel], s = [], lo = Infinity, hi = -Infinity;
      for (var m = 0; m <= MONTHS; m++) { var x = Math.max(0, r.f(m)); s.push(x); lo = Math.min(lo, x); hi = Math.max(hi, x); }
      var sw = 200, sh = 54, span = (hi - lo) || 1;
      function SY(x) { return (sh - 6 - (x - lo) / span * (sh - 12)).toFixed(1); }
      var path = s.map(function (x, m) { return (m ? "L" : "M") + (m / MONTHS * sw).toFixed(1) + " " + SY(x); }).join(" ");
      var now = s[month], first = s[0], ch = Math.round(now - first);
      document.getElementById("t-card").innerHTML =
        '<p class="tcard__name" style="--c:' + r.color + '"><i></i>' + esc(L(r.name)) + "</p>" +
        '<div class="tcard__nums"><div><b>' + Math.round(now) + "</b><span>" + t("share index, ", "indice de part, ") + monthLabel(month) + "</span></div>" +
          "<div><b>" + (ch >= 0 ? "+" : "") + ch + "</b><span>" + t("since ", "depuis ") + monthLabel(0) + "</span></div></div>" +
        '<svg class="tcard__spark" viewBox="0 0 ' + sw + " " + sh + '" preserveAspectRatio="none" aria-hidden="true"><path d="' + path + '" style="stroke:' + r.color + '"/><circle cx="' + (month / MONTHS * sw).toFixed(1) + '" cy="' + SY(now) + '" r="3.5"/></svg>' +
        '<p class="tcard__lead"><span>' + t("Driven by", "Porté par") + "</span> " + esc(L(r.lead)) + "</p>" +
        '<p class="tcard__verdict tcard__verdict--' + r.verdict[0] + '">' + esc(fr() ? r.verdict[2] : r.verdict[1]) + "</p>";
    }
    function stopPlay() { clearInterval(timer); timer = null; btn.textContent = "▶"; btn.setAttribute("aria-label", t("Play 18 months", "Lire 18 mois")); }
    function play() {
      if (month >= MONTHS) { month = 0; prevRank = null; }
      if (reduced.matches) { month = MONTHS; draw(); return; }
      btn.textContent = "❚❚"; btn.setAttribute("aria-label", t("Pause", "Pause"));
      timer = setInterval(function () { month++; draw(); if (month >= MONTHS) stopPlay(); }, 320);
    }
    btn.addEventListener("click", function () { if (timer) stopPlay(); else play(); });
    range.addEventListener("input", function () { stopPlay(); month = +range.value; draw(); });
    race.addEventListener("click", function (e) { var r = e.target.closest(".race__row"); if (!r) return; sel = +r.dataset.i; draw(); });
    stopPlay(); draw();
    later(play, 500);
    cleanup.push(stopPlay);
  }

  /* ============================================================ switch */
  var RENDER = { communication: communication, brand: brand, audiences: audiences, trends: trends };

  function render() {
    stopAll();
    gen += 1; answered = false;
    RENDER[current]();
    stage.classList.remove("is-in"); void stage.offsetWidth; stage.classList.add("is-in");
    runSide(current);
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

  if (window.MutationObserver) {
    new MutationObserver(function () { if (current) render(); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }
})();
