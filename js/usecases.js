/* =========================================================================
   Licter — use cases (home): a live listening feed.

   The visitor picks a question. Posts start coming in on the left; each one
   is read, then tagged with its theme. On the right the count of posts read
   climbs, the theme bars settle, and once enough has been read the answer
   appears. Clicking a theme filters the feed; the feed can be paused.

   MOCK: every post, handle and figure below is illustrative. Replace with
   anonymised client material before going live.

   Text lives here, so each string carries its French, and the feed restarts
   in the new language when the switch is used.
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

  /* ------------------------------------------------------------ data
     posts: [platform, handle, theme index, sentiment -1/0/1, EN, FR] */
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

  var PLATFORM_NAMES = { TIKTOK: "TikTok", INSTAGRAM: "Instagram", X: "X", YOUTUBE: "YouTube", LINKEDIN: "LinkedIn", FACEBOOK: "Facebook" };
  var AVATAR = ["#C98A1E", "#C23A74", "#1F8F78", "#2F6FC0", "#5A4BD1", "#7C8A1F"];

  /* ------------------------------------------------------------ state */
  var current = null, d = null;
  var timer = null, playing = true, visible = false;
  var idx = 0, shown = 0, read = 0, filter = -1;
  var feed, bars, readEl, answerEl, playBtn;

  function stop() { clearTimeout(timer); timer = null; }

  function render() {
    stop();
    d = DATA[current];
    idx = 0; shown = 0; read = 0; filter = -1;

    stage.innerHTML =
      '<div class="lf__feed-wrap">' +
        '<div class="lf__bar">' +
          '<span class="lf__live"><i></i>' + t("Live", "En direct") + "</span>" +
          '<span class="lf__label">' + L(d.label) + "</span>" +
          '<button class="lf__play" type="button" aria-pressed="false">' + t("Pause", "Pause") + "</button>" +
        "</div>" +
        '<ol class="lf__feed" aria-live="polite" aria-relevant="additions"></ol>' +
        '<p class="lf__note">' + t("Illustrative posts", "Posts illustratifs") + "</p>" +
      "</div>" +
      '<aside class="lf__read">' +
        '<p class="lf__k">' + t("Posts read", "Posts lus") + "</p>" +
        '<p class="lf__count">0</p>' +
        '<p class="lf__k">' + t("What they talk about", "De quoi ils parlent") + ' <span class="lf__hint">' + t("click to filter", "cliquez pour filtrer") + "</span></p>" +
        '<ul class="lf__themes">' + d.themes.map(function (th, i) {
          return '<li><button class="lf__theme" type="button" data-i="' + i + '" aria-pressed="false" style="--c:' + th.color + '">' +
            '<span class="lf__theme-top"><span class="lf__theme-n">' + L(th.name) + '</span><span class="lf__theme-v">0 %</span></span>' +
            '<span class="lf__track"><i></i></span></button></li>';
        }).join("") + "</ul>" +
        '<div class="lf__answer" aria-live="polite"><p class="lf__reading">' + t("Reading", "Lecture en cours") + '<span class="lf__dots"><i></i><i></i><i></i></span></p></div>' +
        '<a class="btn btn--primary lf__cta" href="#book">' + t("Book a meeting", "Prendre rendez-vous") + ' <span aria-hidden="true">→</span></a>' +
      "</aside>";

    feed = stage.querySelector(".lf__feed");
    bars = Array.prototype.slice.call(stage.querySelectorAll(".lf__theme"));
    readEl = stage.querySelector(".lf__count");
    answerEl = stage.querySelector(".lf__answer");
    playBtn = stage.querySelector(".lf__play");

    playBtn.addEventListener("click", function () {
      playing = !playing;
      playBtn.setAttribute("aria-pressed", playing ? "false" : "true");
      playBtn.textContent = playing ? t("Pause", "Pause") : t("Resume", "Reprendre");
      stage.classList.toggle("is-paused", !playing);
      if (playing) tick(); else stop();
    });
    stage.querySelector(".lf__themes").addEventListener("click", function (e) {
      var b = e.target.closest(".lf__theme"); if (!b) return;
      var i = +b.dataset.i;
      filter = filter === i ? -1 : i;
      applyFilter();
    });

    if (reduced.matches) {
      /* no stream: the whole read at once */
      for (var k = 0; k < 5; k++) addPost(true);
      read = 11400; settle(1);
      showAnswer();
      return;
    }
    tick();
  }

  function addPost(instant) {
    var p = d.posts[idx % d.posts.length];
    idx++;
    var li = document.createElement("li");
    li.className = "post" + (instant ? " is-tagged" : "");
    li.dataset.theme = p[2];
    var th = d.themes[p[2]];
    var sentiment = p[3] > 0 ? ["pos", t("positive", "positif")] : p[3] < 0 ? ["neg", t("negative", "négatif")] : ["neu", t("neutral", "neutre")];
    li.innerHTML =
      '<span class="post__av" style="background:' + AVATAR[idx % AVATAR.length] + '" aria-hidden="true">' + p[1].charAt(1).toUpperCase() + "</span>" +
      '<div class="post__body">' +
        '<p class="post__meta"><b>' + p[1] + "</b>" +
          '<span class="post__pf">' + ((window.LicterIcons || {})[p[0]] || "") + PLATFORM_NAMES[p[0]] + "</span>" +
          '<span class="post__time"></span></p>' +
        '<p class="post__text">' + (fr() ? p[5] : p[4]) + "</p>" +
        '<p class="post__tags">' +
          '<span class="post__sent post__sent--' + sentiment[0] + '"><i></i>' + sentiment[1] + "</span>" +
          '<span class="post__theme" style="--c:' + th.color + '">' + L(th.name) + "</span>" +
          '<span class="post__reading">' + t("reading…", "lecture…") + "</span>" +
        "</p>" +
      "</div>";
    feed.insertBefore(li, feed.firstChild);
    if (filter >= 0 && filter !== p[2]) li.hidden = true;
    /* keep the column short */
    var items = feed.children;
    for (var i = items.length - 1; i >= 8; i--) feed.removeChild(items[i]);
    ages();
    if (!instant) setTimeout(function () { li.classList.add("is-tagged"); }, 700);
    shown++;
  }

  /* newest on top reads "just now", the ones below it get older */
  var AGES = [0, 1, 2, 4, 6, 9, 13, 18];
  function ages() {
    Array.prototype.forEach.call(feed.children, function (li, i) {
      var a = AGES[Math.min(i, AGES.length - 1)];
      li.querySelector(".post__time").textContent = a ? a + " min" : t("just now", "à l'instant");
    });
  }

  /* the bars settle on the real split as more is read */
  function settle(k) {
    var vals = d.themes.map(function (th) {
      return Math.max(0.02, th.w + (1 - k) * (Math.random() - 0.5) * 0.3);
    });
    var total = vals.reduce(function (s, v) { return s + v; }, 0);
    bars.forEach(function (b, i) {
      var pct = k >= 1 ? d.themes[i].w * 100 : vals[i] / total * 100;
      b.querySelector(".lf__theme-v").textContent = Math.round(pct) + " %";
      b.querySelector(".lf__track i").style.width = pct + "%";
    });
    readEl.textContent = num(read);
  }

  function showAnswer() {
    if (answerEl.classList.contains("is-in")) return;
    answerEl.classList.add("is-in");
    answerEl.innerHTML = '<p class="lf__k">' + t("What it means", "Ce que ça veut dire") + "</p><p>" + L(d.answer) + "</p>";
  }

  function tick() {
    stop();
    if (!d || !playing || !visible || document.hidden) return;
    addPost(false);
    read += 280 + Math.random() * 520;
    settle(Math.min(1, shown / 8));
    if (shown >= 8) showAnswer();
    timer = setTimeout(tick, shown < 3 ? 900 : 1800);
  }

  function applyFilter() {
    bars.forEach(function (b, i) {
      b.classList.toggle("is-on", filter === i);
      b.classList.toggle("is-dim", filter >= 0 && filter !== i);
      b.setAttribute("aria-pressed", filter === i ? "true" : "false");
    });
    Array.prototype.forEach.call(feed.children, function (li) {
      li.hidden = filter >= 0 && +li.dataset.theme !== filter;
    });
    /* a filter shows a few posts of that theme straight away */
    if (filter >= 0) {
      var have = feed.querySelectorAll('.post[data-theme="' + filter + '"]').length, guard = 0;
      while (have < 3 && guard++ < 40) {
        var p = d.posts[idx % d.posts.length];
        if (p[2] === filter) { addPost(true); have++; } else idx++;
      }
    }
  }

  /* ------------------------------------------------------------ select */
  function select(key) {
    current = key;
    topics.forEach(function (b) {
      var on = b.dataset.topic === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    stage.setAttribute("aria-labelledby", "tab-" + key);
    stage.classList.add("has-feed");
    playing = true;
    stage.classList.remove("is-paused");
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

  /* only streams while on screen and in a visible tab */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      visible = e[0].isIntersecting;
      if (visible) tick(); else stop();
    }, { threshold: 0.15 }).observe(stage);
  } else visible = true;
  document.addEventListener("visibilitychange", function () { if (!document.hidden) tick(); else stop(); });

  if (window.MutationObserver) {
    new MutationObserver(function () { if (current) render(); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }
})();
