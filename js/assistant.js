/* =========================================================================
   The sales drawer: a panel that slides in from the right, with two tabs.

   - "Call me back": the callback of the home, one field, email or phone.
   - "Chat": Antoine Khaitrine, co-founder, answers questions about Licter.
     Every answer ends on a call to action. It is labelled as an automatic
     assistant: it speaks in his name, it is not him typing.

   MOCK: nothing is sent anywhere yet (the callback, like the one of the
   home, is to be wired to the CRM). The answers are matched on keywords,
   from what the site says; there is no AI behind them. To answer freely,
   plug a serverless function in reply() and keep the CTA at the end.

   Loaded by js/ui.js on every page.
   ========================================================================= */
(function () {
  "use strict";
  if (window.__licterDrawer) return;
  window.__licterDrawer = true;

  var html = document.documentElement;
  function fr() { return (html.lang || "fr").slice(0, 2) === "fr"; }
  /* French typography: a non-breaking space before ? ! : ; and inside « » */
  function typo(s) {
    return s.replace(/ ([?!:;»])/g, " $1").replace(/« /g, "« ").replace(/(\d) %/g, "$1 %");
  }
  function T(pair) { return fr() ? typo(pair[0]) : pair[1]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function session(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* ------------------------------------------------------------ the agent */
  var A = { name: "Antoine", full: "Antoine Khaitrine", img: "/assets/img/team/founder-antoine-160.webp" };

  var UC = function (fam) { return fr() ? "/fr/cas-usage/" + (fam ? fam + "/" : "") : "/en/use-cases/" + (fam ? { "sante-de-marque": "brand-health", "tendances-innovation": "trends-innovation" }[fam] || fam : "") + (fam ? "/" : ""); };

  var L = {
    launch: ["Une question ? " + A.name + " vous répond", "A question? " + A.name + " answers"],
    launchShort: ["Une question ?", "A question?"],
    open: ["Ouvrir l'échange avec " + A.name, "Open the chat with " + A.name],
    role: ["Cofondateur de Licter", "Co-founder of Licter"],
    bot: ["Assistant automatique, en son nom", "Automatic assistant, in his name"],
    close: ["Fermer", "Close"],
    tabChat: ["Discuter", "Chat"],
    tabCall: ["Être rappelé", "Call me back"],
    region: ["Échanger avec Licter", "Talk to Licter"],
    hello: ["Bonjour, je suis " + A.name + ", cofondateur de Licter. Posez-moi vos questions sur nos offres, nos méthodes, nos délais ou nos tarifs.",
            "Hello, I am " + A.name + ", co-founder of Licter. Ask me about our offers, our methods, our timings or our pricing."],
    placeholder: ["Votre question…", "Your question…"],
    send: ["Envoyer", "Send"],
    you: ["Vous", "You"],
    typing: [A.name + " écrit…", A.name + " is typing…"],
    callCta: ["Être rappelé par un consultant", "Get a call back from a consultant"],
    /* the callback: the same words as the home */
    callT: ["Trente minutes avec un consultant.", "Thirty minutes with a consultant."],
    callL: ["Laissez votre e-mail ou votre téléphone. Un consultant vous rappelle dans les 30 minutes en semaine.",
            "Leave your email or phone number. A consultant calls you back within 30 minutes on weekdays."],
    field: ["E-mail ou téléphone", "Email or phone"],
    ph: ["nom@entreprise.com ou 06 12 34 56 78", "name@company.com or 06 12 34 56 78"],
    callBtn: ["Me faire rappeler", "Call me back"],
    promise: ["Un consultant, pas un commercial. En semaine, de 9\u00a0h à 19\u00a0h.", "A consultant, not a sales team. Weekdays, 9am to 7pm."],
    consent: ["Vos coordonnées servent uniquement à vous rappeler.", "We use your contact details only to call you back."],
    privacy: ["Politique de confidentialité", "Privacy policy"],
    err: ["Indiquez un e-mail professionnel ou un numéro de téléphone.", "Enter a work email or a phone number."],
    doneMail: ["C'est noté. Un consultant vous écrit à ", "Noted. A consultant writes to you at "],
    donePhone: ["C'est noté. Un consultant vous appelle au ", "Noted. A consultant calls you on "],
    doneEnd: [" dans les 30 minutes.", " within 30 minutes."]
  };

  /* ------------------------------------------------------- what he knows
     k: keywords, without accents, lower case. a: the answer. go: a link to
     go further, shown beside the callback. */
  var KB = [
    { k: ["bonjour", "salut", "hello", "hey", "coucou", "bonsoir"],
      a: ["Bonjour ! Dites-moi ce que vous cherchez à décider : mesurer une campagne, suivre votre réputation, comprendre vos audiences, repérer une tendance ? Je vous dis comment on s'y prend.",
          "Hello! Tell me what you are trying to decide: measuring a campaign, following your reputation, understanding your audiences, spotting a trend? I will tell you how we go about it."] },
    { k: ["offre", "offres", "formule", "formules", "service", "services", "proposez", "faites", "offer", "offers", "plan", "plans", "what do you do"],
      a: ["Quatre façons de travailler avec nous : Social Insights, des études à la demande dans un forfait fixe ; Vigie 360, une veille qui vous alerte en 15 minutes, 24 h/24 ; Social Listening as a Service, pour faire servir la plateforme que vous payez déjà ; et Nox, notre outil de veille assisté par l'IA.",
          "Four ways to work with us: Social Insights, studies on demand inside a fixed fee; Vigie 360, monitoring that alerts you within 15 minutes, 24/7; Social Listening as a Service, to make the platform you already pay for useful; and Nox, our AI-assisted monitoring tool."],
      go: [["Comparer les offres", "Compare the offers"], "/offers.html"] },
    { k: ["prix", "tarif", "tarifs", "cout", "couts", "combien", "budget", "cher", "devis", "price", "pricing", "cost", "how much", "fee", "quote"],
      a: ["Un forfait mensuel fixe, sans engagement, avec des études illimitées à l'intérieur. Le montant dépend du périmètre : les marques, les marchés et les langues suivis. Le plus juste est d'en parler une demi-heure, pour vous donner un chiffre réel plutôt qu'une fourchette.",
          "A fixed monthly fee, no lock-in, with unlimited studies inside it. The amount depends on the scope: the brands, markets and languages covered. The fairest is to talk for half an hour, so you get a real figure rather than a range."] },
    { k: ["delai", "delais", "combien de temps", "rapide", "rapidement", "vite", "quand", "jours", "timing", "how long", "fast", "quick", "when", "days"],
      a: ["Une dizaine de jours pour une première lecture, du cadrage à la restitution. Pour une alerte, 15 minutes, jour et nuit, avec Vigie 360.",
          "About ten days for a first read, from framing to readout. For an alert, 15 minutes, day and night, with Vigie 360."],
      go: [["Voir Vigie 360", "See Vigie 360"], "/offer-vigie-360.html"] },
    { k: ["source", "sources", "reseau", "reseaux", "tiktok", "instagram", "linkedin", "youtube", "facebook", "twitter", "presse", "forum", "forums", "avis", "donnees", "data", "networks", "media", "medias"],
      a: ["Ce que les gens publient (TikTok, Instagram, X, LinkedIn, YouTube, Facebook, presse, forums, avis), ce qu'ils recherchent sur Google, YouTube et Amazon, et ce qu'ils demandent aux IA. Plus de vingt langues, choisies selon votre question.",
          "What people post (TikTok, Instagram, X, LinkedIn, YouTube, Facebook, news, forums, reviews), what they search on Google, YouTube and Amazon, and what they ask AI. More than twenty languages, chosen for your question."],
      go: [["Voir nos sources et outils", "See our sources and tools"], "/tech-tools.html"] },
    { k: ["langue", "langues", "language", "languages", "international", "pays", "country", "countries", "chinois", "arabe", "espagnol", "anglais"],
      a: ["Plus de vingt langues, lues par des analystes qui les parlent, dont l'anglais, l'espagnol, le chinois, l'arabe et l'hindi. Une traduction automatique ne suffit pas à lire un marché.",
          "More than twenty languages, read by analysts who speak them, including English, Spanish, Chinese, Arabic and Hindi. Machine translation is not enough to read a market."] },
    { k: ["talkwalker", "visibrain", "youscan", "soprism", "outil", "outils", "plateforme", "plateformes", "licence", "logiciel", "tool", "tools", "platform", "software", "licence", "license"],
      a: ["Nous faisons tourner Talkwalker, Visibrain, YouScan et SoPrism, et choisissons la bonne plateforme pour chaque question. Si vous en payez déjà une, nous pouvons la reprendre et la faire servir : c'est Social Listening as a Service.",
          "We run Talkwalker, Visibrain, YouScan and SoPrism, and pick the right platform for each question. If you already pay for one, we can take it over and make it useful: that is Social Listening as a Service."],
      go: [["Voir Social Listening as a Service", "See Social Listening as a Service"], "/offer-slaas.html"] },
    { k: ["ia", "intelligence artificielle", "ai", "chatgpt", "gpt", "llm", "algorithme", "humain", "humains", "human", "robot", "automatique", "automatise"],
      a: ["L'IA nous aide à collecter et à trier. Ce sont des personnes qui lisent : des analystes qui parlent la langue du marché et un consultant qui connaît votre marque, qui vous présente la recommandation. Nous écoutons aussi ce que les IA disent de vous : c'est l'AI listening.",
          "AI helps us collect and sort. People do the reading: analysts who speak the market's language and a consultant who knows your brand and presents the recommendation to you. We also listen to what AI says about you: that is AI listening."],
      go: [["Voir l'AI listening", "See AI listening"], "/expertise-ai-listening.html"] },
    { k: ["nox"],
      a: ["Nox est notre outil de veille assisté par l'IA : il regroupe la conversation par sujets, vous envoie un brief chaque matin et signale ce qui sort de l'ordinaire. Nos analystes le configurent et le vérifient avec vous.",
          "Nox is our AI-assisted monitoring tool: it groups the conversation into topics, sends you a brief every morning and flags what looks unusual. Our analysts set it up and check it with you."],
      go: [["Voir Nox", "See Nox"], "/offer-nox.html"] },
    { k: ["vigie", "crise", "crises", "alerte", "alertes", "bad buzz", "badbuzz", "crisis", "alert", "alerts", "temps reel", "real time", "veille", "monitoring", "24/7"],
      a: ["Avec Vigie 360, un analyste lit le signal avant de vous alerter, en 15 minutes, nuits et week-ends compris. Une alerte veut dire qu'il s'est passé quelque chose, pas qu'un mot-clé s'est déclenché.",
          "With Vigie 360, an analyst reads the signal before alerting you, within 15 minutes, nights and weekends included. An alert means something happened, not that a keyword fired."],
      go: [["Voir Vigie 360", "See Vigie 360"], "/offer-vigie-360.html"] },
    { k: ["audience", "audiences", "persona", "personas", "cible", "cibles", "segment", "segmentation", "jeunes", "gen z", "target", "consommateurs", "consumers"],
      a: ["Nous profilons vos communautés à partir de ce qu'elles suivent, partagent et consomment : centres d'intérêt, affinités de marque, médias. De quoi remplacer un persona déclaratif par un comportement observé.",
          "We profile your communities from what they follow, share and consume: interests, brand affinities, media. Enough to replace a declared persona with observed behaviour."],
      go: [["Voir les cas Audiences", "See the Audiences cases"], "audiences"] },
    { k: ["campagne", "campagnes", "campaign", "lancement", "launch", "evenement", "event", "roi", "impact", "mesurer", "mesure", "measure"],
      a: ["Nous mesurons ce qu'une campagne a déplacé dans la conversation : volume, tonalité, thèmes, et surtout quelles audiences ont changé de position. Souvent plus parlant qu'un taux de clic.",
          "We measure what a campaign moved in the conversation: volume, tone, themes, and above all which audiences changed their position. Often more telling than a click-through rate."],
      go: [["Voir les cas Communication", "See the Communication cases"], "communication"] },
    { k: ["influence", "influenceur", "influenceurs", "influenceuse", "createur", "createurs", "ambassadeur", "ambassadeurs", "creator", "creators", "influencer", "influencers"],
      a: ["Nous identifions les voix qui portent vraiment dans votre catégorie, pas celles qui ont le plus d'abonnés : recouvrement avec votre audience, affinité, et risques avant un partenariat.",
          "We identify the voices that actually carry in your category, not the ones with the most followers: overlap with your audience, affinity, and risks before a partnership."],
      go: [["Voir l'influence listening", "See influence listening"], "/expertise-influence-listening.html"] },
    { k: ["reputation", "e-reputation", "ereputation", "image", "marque", "brand", "notoriete"],
      a: ["Nous suivons l'image et la tonalité attachées à votre marque, sur tous vos marchés, et vous alertons sur les ruptures. Chaque mois, ce qui a bougé et pourquoi.",
          "We follow the image and tone attached to your brand, across your markets, and alert you on breaks. Every month, what moved and why."],
      go: [["Voir les cas Santé de marque", "See the Brand health cases"], "sante-de-marque"] },
    { k: ["tendance", "tendances", "innovation", "produit", "produits", "trend", "trends", "product", "products", "opportunite", "opportunites", "marche"],
      a: ["Nous lisons le verdict non filtré sur vos produits et ceux des concurrents, et repérons les besoins que personne ne couvre encore, avant qu'ils n'arrivent dans les études.",
          "We read the unfiltered verdict on your products and your competitors', and spot the needs nobody covers yet, before they reach the surveys."],
      go: [["Voir les cas Tendances", "See the Trends cases"], "tendances-innovation"] },
    { k: ["client", "clients", "reference", "references", "qui travaille", "customers", "case study", "exemple", "exemples"],
      a: ["Plus de 50 organisations et 160 projets depuis 2022, parmi lesquelles Decathlon, L'Oréal, Danone, La Poste, Bouygues Telecom, Société Générale, TV5Monde et l'UNESCO.",
          "More than 50 organisations and 160 projects since 2022, including Decathlon, L'Oréal, Danone, La Poste, Bouygues Telecom, Société Générale, TV5Monde and UNESCO."],
      go: [["Voir nos clients", "See our clients"], "/clients.html"] },
    { k: ["rgpd", "gdpr", "vie privee", "privacy", "donnees personnelles", "personal data", "conforme", "legal", "anonyme"],
      a: ["Nous travaillons sur des données publiques et des communautés agrégées, jamais sur le profil d'un individu. Vos propres données restent les vôtres.",
          "We work on public data and aggregated communities, never on an individual's profile. Your own data stays yours."],
      go: [["Lire la politique de confidentialité", "Read the privacy policy"], "/privacy.html"] },
    { k: ["diagnostic", "audit", "evaluer", "evaluation", "score", "assess", "maturite"],
      a: ["Le diagnostic gratuit fait le point sur votre écoute en six questions, trois minutes : votre score tout de suite, la lecture complète par e-mail.",
          "The free diagnostic takes stock of your listening in six questions, three minutes: your score at once, the full readout by email."],
      go: [["Faire le diagnostic", "Take the diagnostic"], "/diagnostic.html"] },
    { k: ["qui etes", "equipe", "fondateur", "fondateurs", "licter", "cabinet", "team", "founder", "founders", "about", "who are you", "histoire"],
      a: ["Licter est un cabinet de conseil en social data intelligence, fondé en 2022 par Adrien Krebs et Antoine Khaitrine. Une équipe d'analystes et de consultants qui lit pour vous ce que les gens publient, recherchent et demandent à l'IA.",
          "Licter is a social data intelligence consultancy, founded in 2022 by Adrien Krebs and Antoine Khaitrine. A team of analysts and consultants who read for you what people post, search and ask AI."],
      go: [["Pourquoi Licter", "Why Licter"], "/why-licter.html"] },
    { k: ["engagement", "resilier", "resiliation", "contrat", "arreter", "duree", "commitment", "contract", "cancel", "lock-in"],
      a: ["Sans engagement : le forfait s'arrête quand vous le décidez. Nous préférons que vous restiez parce que c'est utile.",
          "No lock-in: the fee stops when you decide. We would rather you stay because it is useful."] },
    { k: ["rendez-vous", "rdv", "appel", "appeler", "rappel", "rappeler", "contact", "contacter", "parler", "telephone", "joindre", "meeting", "call", "talk", "demo", "phone"],
      a: ["Avec plaisir. Laissez votre e-mail ou votre téléphone : un consultant vous rappelle dans les 30 minutes en semaine, pas un commercial.",
          "With pleasure. Leave your email or phone number: a consultant calls you back within 30 minutes on weekdays, not a salesperson."],
      go: [["Choisir un créneau", "Pick a slot"], "/book-a-meeting.html"] },
    { k: ["merci", "thanks", "thank you", "super", "parfait", "top", "genial", "great"],
      a: ["Avec plaisir. Si vous voulez aller plus loin sur votre cas précis, le plus efficace reste une demi-heure avec un consultant.",
          "My pleasure. To go further on your own case, the most useful is still half an hour with a consultant."] }
  ];
  var FALLBACK = {
    a: ["Bonne question, et je préfère ne pas vous y répondre à moitié. Le plus simple : un consultant vous rappelle dans les 30 minutes en semaine, et vous aurez une réponse précise.",
        "Good question, and I would rather not half-answer it. The simplest: a consultant calls you back within 30 minutes on weekdays, and you get a precise answer."],
    go: [["Prendre rendez-vous", "Book a meeting"], "/book-a-meeting.html"]
  };
  var CHIPS = [
    [["Vos offres", "Your offers"], "offres"],
    [["Vos tarifs", "Your pricing"], "prix"],
    [["En combien de temps ?", "How fast?"], "delai"],
    [["Des humains ou de l'IA ?", "People or AI?"], "humain"]
  ];

  function norm(s) {
    /* "l'IA", "qu'est-ce": the apostrophe splits the words */
    return " " + s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/['\u2019]/g, " ").replace(/[^a-z0-9/\- ]+/g, " ").replace(/\s+/g, " ") + " ";
  }
  function match(q) {
    var n = norm(q), best = null, score = 0;
    KB.forEach(function (it) {
      var s = 0;
      it.k.forEach(function (w) { if (n.indexOf(" " + w + " ") >= 0 || (w.length > 4 && n.indexOf(w) >= 0)) s += w.length > 4 ? 2 : 1; });
      if (s > score) { score = s; best = it; }
    });
    return best || FALLBACK;
  }

  /* -------------------------------------------------------------- the DOM */
  var root = document.createElement("div");
  root.className = "lx";
  root.innerHTML =
    '<button class="lx__launch" type="button" aria-expanded="false" aria-controls="lx-panel">' +
      '<span class="lx__face"><img src="' + A.img + '" alt="" width="80" height="80" loading="lazy" decoding="async" /><i aria-hidden="true"></i></span>' +
      '<span class="lx__launch-t" data-l="launch"></span>' +
    "</button>" +
    '<aside class="lx__panel" id="lx-panel" hidden>' +
      '<header class="lx__head">' +
        '<span class="lx__face"><img src="' + A.img + '" alt="" width="80" height="80" loading="lazy" decoding="async" /><i aria-hidden="true"></i></span>' +
        '<span class="lx__who"><b>' + A.full + '</b><small data-l="role"></small><small class="lx__bot" data-l="bot"></small></span>' +
        '<button class="lx__close" type="button"><span aria-hidden="true">×</span><span class="visually-hidden" data-l="close"></span></button>' +
      "</header>" +
      '<div class="lx__tabs" role="tablist">' +
        '<button class="lx__tab" type="button" role="tab" id="lx-t-call" aria-controls="lx-call" data-tab="call" data-l="tabCall"></button>' +
        '<button class="lx__tab" type="button" role="tab" id="lx-t-chat" aria-controls="lx-chat" data-tab="chat" data-l="tabChat"></button>' +
      "</div>" +
      /* the callback */
      '<div class="lx__view lx__call" id="lx-call" role="tabpanel" aria-labelledby="lx-t-call">' +
        '<h2 class="lx__title" data-l="callT"></h2>' +
        '<p class="lx__lead" data-l="callL"></p>' +
        '<form class="lx__form" novalidate>' +
          '<label class="lx__label" for="lx-contact" data-l="field"></label>' +
          '<input class="lx__input" id="lx-contact" type="text" inputmode="email" autocomplete="email" required aria-describedby="lx-err" />' +
          '<p class="lx__err" id="lx-err" data-l="err" hidden></p>' +
          '<button class="btn btn--primary lx__submit" type="submit"><span data-l="callBtn"></span> <span aria-hidden="true">→</span></button>' +
          '<p class="lx__promise"><span class="lx__dot" aria-hidden="true"></span><span data-l="promise"></span></p>' +
          '<p class="lx__consent"><span data-l="consent"></span> <a href="/privacy.html" data-l="privacy"></a>.</p>' +
        "</form>" +
        '<p class="lx__done" role="status" hidden></p>' +
      "</div>" +
      /* the chat */
      '<div class="lx__view lx__chat" id="lx-chat" role="tabpanel" aria-labelledby="lx-t-chat" hidden>' +
        '<div class="lx__log" role="log" aria-live="polite"></div>' +
        '<div class="lx__chips"></div>' +
        '<form class="lx__ask">' +
          '<label class="visually-hidden" for="lx-q" data-l="placeholder"></label>' +
          '<input class="lx__q" id="lx-q" type="text" autocomplete="off" maxlength="300" />' +
          '<button class="lx__send" type="submit"><span aria-hidden="true">↑</span><span class="visually-hidden" data-l="send"></span></button>' +
        "</form>" +
      "</div>" +
    "</aside>";
  document.body.appendChild(root);

  var launch = root.querySelector(".lx__launch"), panel = root.querySelector(".lx__panel");
  var log = root.querySelector(".lx__log"), chips = root.querySelector(".lx__chips");
  var tabs = Array.prototype.slice.call(root.querySelectorAll(".lx__tab"));
  var views = { call: root.querySelector(".lx__call"), chat: root.querySelector(".lx__chat") };
  var history = [];   /* what was said, to redraw it in the other language */

  function paint() {
    Array.prototype.forEach.call(root.querySelectorAll("[data-l]"), function (el) { el.textContent = T(L[el.getAttribute("data-l")]); });
    launch.setAttribute("aria-label", T(L.open));
    panel.setAttribute("aria-label", T(L.region));
    root.querySelector(".lx__input").setAttribute("placeholder", T(L.ph));
    root.querySelector(".lx__q").setAttribute("placeholder", T(L.placeholder));
    chips.innerHTML = CHIPS.map(function (c) { return '<button type="button" class="lx__chip" data-q="' + c[1] + '">' + esc(T(c[0])) + "</button>"; }).join("");
    redraw();
  }

  /* ------------------------------------------------------------- the chat */
  function bubble(m) {
    if (m.who === "you") return '<div class="lx__msg lx__msg--you"><span class="visually-hidden">' + esc(T(L.you)) + " : </span>" + esc(m.text) + "</div>";
    var it = m.it, go = it && it.go;
    var href = go ? (go[1].charAt(0) === "/" ? go[1] : UC(go[1])) : null;
    return '<div class="lx__msg lx__msg--him"><span class="visually-hidden">' + esc(A.name) + " : </span>" + esc(T(m.it ? m.it.a : L.hello)) +
      /* always a call to action at the end */
      '<span class="lx__cta"><button type="button" class="lx__cta-call">' + esc(T(L.callCta)) + ' <span aria-hidden="true">→</span></button>' +
      (href ? '<a class="lx__cta-go" href="' + href + '">' + esc(T(go[0])) + "</a>" : "") + "</span></div>";
  }
  function redraw() {
    log.innerHTML = history.map(bubble).join("");
    log.scrollTop = log.scrollHeight;
  }
  function ask(q) {
    q = (q || "").trim();
    if (!q) return;
    history.push({ who: "you", text: q });
    redraw();
    chips.hidden = true;
    var typing = document.createElement("div");
    typing.className = "lx__msg lx__msg--him lx__typing";
    typing.innerHTML = '<span class="lx__dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="visually-hidden">' + esc(T(L.typing)) + "</span>";
    log.appendChild(typing);
    log.scrollTop = log.scrollHeight;
    var it = match(q);
    setTimeout(function () { history.push({ who: "him", it: it }); redraw(); }, 650 + Math.min(900, it.a[0].length * 4));
  }
  root.querySelector(".lx__ask").addEventListener("submit", function (e) {
    e.preventDefault();
    var input = root.querySelector(".lx__q");
    ask(input.value); input.value = "";
  });
  chips.addEventListener("click", function (e) {
    var b = e.target.closest(".lx__chip");
    if (b) ask(b.textContent.replace(/ /g, " ") + " ");
  });
  log.addEventListener("click", function (e) {
    if (!e.target.closest(".lx__cta-call")) return;
    show("call"); root.querySelector(".lx__input").focus();
  });

  /* --------------------------------------------------------- the callback */
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var sent = null;
  function kind(v) {
    if (EMAIL.test(v)) return "email";
    return /^\+?\d{9,15}$/.test(v.replace(/[\s.()-]/g, "")) ? "phone" : null;
  }
  var form = root.querySelector(".lx__form"), input = root.querySelector(".lx__input"), err = root.querySelector(".lx__err");
  input.addEventListener("input", function () { if (!err.hidden) { err.hidden = true; input.setAttribute("aria-invalid", "false"); } });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = input.value.trim(), k = kind(v);
    input.setAttribute("aria-invalid", k ? "false" : "true");
    err.hidden = !!k;
    if (!k) { input.focus(); return; }
    /* MOCK: wire to the CRM here (v, k) */
    if (k === "email" && window.LicterLead) window.LicterLead.set(v);
    sent = { v: v, k: k };
    form.hidden = true;
    done();
    session("lx-sent", "1");
  });
  function done() {
    if (!sent) return;
    var box = root.querySelector(".lx__done");
    box.hidden = false;
    box.innerHTML = esc(T(sent.k === "phone" ? L.donePhone : L.doneMail)) + "<b>" + esc(sent.v) + "</b>" + esc(window.LicterHours ? window.LicterHours.when(fr()) + "." : T(L.doneEnd));
  }

  /* ---------------------------------------------------- open, close, tabs */
  function show(tab) {
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-tab") === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      views[t.getAttribute("data-tab")].hidden = !on;
    });
    if (tab === "chat" && !history.length) { history.push({ who: "him", it: null }); redraw(); }
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { show(t.getAttribute("data-tab")); });
    t.addEventListener("keydown", function (e) {
      var d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (!d) return;
      e.preventDefault();
      var n = tabs[(i + d + tabs.length) % tabs.length];
      show(n.getAttribute("data-tab")); n.focus();
    });
  });

  function open(tab, quiet) {
    if (window.LicterTrack) window.LicterTrack("chat_open", { tab: tab, auto: !!quiet });
    show(tab);
    panel.hidden = false;
    requestAnimationFrame(function () { root.classList.add("is-open"); html.classList.add("lx-open"); });
    launch.setAttribute("aria-expanded", "true");
    session("lx-shown", "1");
    /* the automatic opening never takes the focus away from the page; on a
       phone the focus goes to the panel, not the field: the keyboard would
       otherwise cover half the conversation before anything is read */
    if (!quiet) {
      if (phone.matches) root.querySelector(".lx__close").focus({ preventScroll: true });
      else (tab === "chat" ? root.querySelector(".lx__q") : input).focus();
    }
    fit();
  }
  /* phone: the panel is the whole screen, and follows the keyboard (the
     visual viewport) so the field always stays above it */
  var phone = window.matchMedia("(max-width: 720px)");
  var vv = window.visualViewport;
  function fit() {
    var K = ["--lx-vh", "--lx-vw", "--lx-top", "--lx-left", "--lx-bottom", "--lx-right"];
    K.forEach(function (k) { panel.style.removeProperty(k); });
    if (!phone.matches || !vv) return;
    /* the visible part of the page, even zoomed in (iOS zooms on a field and
       stays there): the panel covers exactly what is on screen */
    panel.style.setProperty("--lx-vh", Math.floor(vv.height) + "px");
    panel.style.setProperty("--lx-vw", Math.floor(vv.width) + "px");
    panel.style.setProperty("--lx-top", Math.round(vv.offsetTop) + "px");
    panel.style.setProperty("--lx-left", Math.round(vv.offsetLeft) + "px");
    panel.style.setProperty("--lx-bottom", "auto");
    panel.style.setProperty("--lx-right", "auto");
  }
  if (vv) { vv.addEventListener("resize", fit); vv.addEventListener("scroll", fit); }
  /* back to where the visitor opened it from: the launcher, or the home's bar */
  function back() {
    var bar = document.querySelector(".stickybar.is-shown .stickybar__chat");
    var seen = function (el) { return el && el.getClientRects().length > 0; };
    if (seen(launch)) launch.focus(); else if (seen(bar)) bar.focus();
  }
  function close() {
    root.classList.remove("is-open");
    html.classList.remove("lx-open");
    launch.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!root.classList.contains("is-open")) panel.hidden = true; }, 320);
  }
  launch.addEventListener("click", function () { root.classList.contains("is-open") ? close() : open("chat"); });
  root.querySelector(".lx__close").addEventListener("click", function () { close(); back(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("is-open")) { close(); back(); } });

  /* ------------------------------------------------- the automatic opening
     Once per visit, on a large screen, half-way down the page or after 35
     seconds, never over the callback of the page itself nor after a send. */
  var wide = window.matchMedia("(min-width: 900px)");
  function pageBookInView() {
    var b = document.getElementById("book");
    if (!b) return false;
    var r = b.getBoundingClientRect();
    return r.top < innerHeight && r.bottom > 0;
  }
  /* the home has its own callback at the end: the drawer never opens by
     itself there, and the launcher waits until the hero (and its client
     logos) has scrolled past */
  var isHome = document.body.classList.contains("home");
  var hero = document.getElementById("hero");
  if (isHome && hero) {
    root.classList.add("lx--wait");
    var onHero = function () {
      var past = hero.getBoundingClientRect().bottom < innerHeight * 0.4;
      root.classList.toggle("lx--wait", !past);
    };
    window.addEventListener("scroll", onHero, { passive: true });
    onHero();
  }
  /* use-case pages, large screens: once the hero is past, the launcher keeps
     only Antoine's face, so it never sits over the content */
  var ucHero = (document.body.classList.contains("ucp-page") || document.body.classList.contains("xpage")) && document.querySelector(".ucp__head, .ucr-hero, .xpage .xh");
  if (ucHero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (e) { root.classList.toggle("lx--compact", !e[0].isIntersecting); }).observe(ucHero);
  }
  function auto() {
    /* the callback now opens as a popup of its own (js/popups.js): the
       drawer is the chat, and only opens when asked */
    if (window.LicterPopups || isHome) return;
    if (session("lx-shown") || session("lx-sent") || !wide.matches || root.classList.contains("is-open") || pageBookInView()) return;
    open("call", true);
  }
  var timer = setTimeout(auto, 35000);
  function onScroll() {
    var h = document.documentElement.scrollHeight - innerHeight;
    if (h > 0 && scrollY / h > 0.5) { window.removeEventListener("scroll", onScroll); clearTimeout(timer); auto(); }
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* the home's bottom bar on a phone carries Antoine's face: it opens the chat */
  window.LicterChat = { open: function () { open("chat"); }, close: close };

  paint();
  show("chat");
  new MutationObserver(function () { paint(); done(); }).observe(html, { attributes: true, attributeFilter: ["lang"] });
})();
