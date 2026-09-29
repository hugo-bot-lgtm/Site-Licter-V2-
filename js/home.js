/* =========================================================================
   Licter — home page interactions: hero questions, budget estimator,
   diagnostic, guide preview, booking.

   Everything marked MOCK below is placeholder content or logic. None of it
   sends data anywhere. Replace before going live:
     - ESTIMATE: the pricing formula
     - QUIZ: the six questions and the score bands
     - SLOTS: the availability (swap for the real calendar embed)
     - the three submit handlers (wire to the CRM)

   Text rendered here is not in the HTML, so js/i18n.js cannot translate it
   from the page. Each string carries its French beside it, and the parts
   re-render when the language changes.
   ========================================================================= */
(function () {
  "use strict";

  var html = document.documentElement;
  function fr() { return html.lang === "fr"; }
  function t(en, frText) { return fr() ? frText : en; }
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var renders = [];
  function onLang(fn) { renders.push(fn); fn(); }
  if (window.MutationObserver) {
    new MutationObserver(function () { renders.forEach(function (fn) { fn(); }); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }

  /* ------------------------------------------------------ hero questions */
  /* A question in the hero opens the matching family in the use cases. */
  Array.prototype.forEach.call(document.querySelectorAll(".ask[data-case], .chip[data-case]"), function (chip) {
    chip.addEventListener("click", function () {
      var tab = document.getElementById("tab-" + chip.dataset.case);
      var target = document.getElementById("use-cases");
      if (tab) tab.click();
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      /* the answer changed further down: take keyboard and screen-reader
         users there too, once the new readout is in */
      var panel = document.getElementById("cases-panel");
      if (panel) {
        panel.setAttribute("tabindex", "-1");
        setTimeout(function () { panel.focus({ preventScroll: true }); }, 450);
      }
    });
  });

  /* ----------------------------------------------------------- estimator */
  /* MOCK: placeholder formula, not Licter's pricing. */
  var ESTIMATE = {
    base: { insights: 3900, vigie: 2900, slaas: 3400 },
    market: 650,
    language: 450,
    alerts: 1600
  };

  var est = document.getElementById("estimator");
  if (est) {
    var out = document.getElementById("est-out");
    var markets = document.getElementById("est-markets");
    var langs = document.getElementById("est-langs");
    var alerts = document.getElementById("est-alerts");

    function money(n) {
      return fr()
        ? n.toLocaleString("fr-FR").replace(/ | /g, " ") + " €"
        : "€" + n.toLocaleString("en-GB");
    }
    function round(n) { return Math.round(n / 100) * 100; }

    function update() {
      var offer = est.querySelector('input[name="offer"]:checked').value;
      var m = +markets.value, l = +langs.value;
      document.getElementById("est-markets-out").textContent = m;
      document.getElementById("est-langs-out").textContent = l;
      var mid = ESTIMATE.base[offer] + (m - 1) * ESTIMATE.market + (l - 1) * ESTIMATE.language +
        (alerts.checked ? ESTIMATE.alerts : 0);
      out.innerHTML =
        '<span class="estimator__range">' + money(round(mid * 0.85)) + " " + t("to", "à") + " " +
        money(round(mid * 1.15)) + "</span>" +
        '<span class="estimator__per">' + t("per month, excl. VAT", "par mois, HT") + "</span>";
      /* the range track fills up to the thumb */
      [markets, langs].forEach(function (r) {
        r.style.setProperty("--fill", ((r.value - r.min) / (r.max - r.min)) * 100 + "%");
      });
    }
    est.addEventListener("input", update);
    est.addEventListener("submit", function (e) { e.preventDefault(); });
    onLang(update);
  }

  /* ---------------------------------------------------------- diagnostic */
  /* MOCK: a draft of the six dimensions, to be checked by the team. */
  var QUIZ = [
    { dim: ["Framing", "Cadrage"],
      q: ["When a listening project starts, what comes first?", "Quand un projet d'écoute démarre, qu'est-ce qui vient en premier ?"],
      a: [["The keywords", "Les mots-clés"], ["A topic we want to follow", "Un sujet à suivre"], ["The decision it has to inform", "La décision qu'il doit éclairer"]] },
    { dim: ["Coverage", "Couverture"],
      q: ["Which sources do you read today?", "Quelles sources lisez-vous aujourd'hui ?"],
      a: [["One social network", "Un seul réseau social"], ["Several networks", "Plusieurs réseaux"], ["Social, search and generative AI", "Réseaux, recherche et IA générative"]] },
    { dim: ["Languages", "Langues"],
      q: ["How do you read a foreign market?", "Comment lisez-vous un marché étranger ?"],
      a: [["Machine translation", "Traduction automatique"], ["A local agency, case by case", "Une agence locale, au cas par cas"], ["Analysts who speak the language", "Des analystes qui parlent la langue"]] },
    { dim: ["Audiences", "Audiences"],
      q: ["Do you know who is behind the conversation?", "Savez-vous qui est derrière la conversation ?"],
      a: [["No, we see volumes", "Non, nous voyons des volumes"], ["Roughly, from platform data", "À peu près, via la plateforme"], ["Yes, profiled and segmented", "Oui, profilés et segmentés"]] },
    { dim: ["Alerting", "Alerte"],
      q: ["When something moves, how do you hear about it?", "Quand quelque chose bouge, comment l'apprenez-vous ?"],
      a: [["From the press", "Par la presse"], ["From a keyword alert", "Par une alerte mots-clés"], ["From an analyst who has read it", "Par un analyste qui l'a lu"]] },
    { dim: ["Use", "Usage"],
      q: ["What happens to the analysis?", "Que devient l'analyse ?"],
      a: [["It sits in a dashboard", "Elle reste dans un tableau de bord"], ["It goes into a monthly report", "Elle part dans un rapport mensuel"], ["It changes a decision", "Elle change une décision"]] }
  ];
  var BANDS = [
    { max: 4, name: ["Listening, not yet reading", "Vous écoutez, sans encore lire"],
      text: ["You collect the conversation. The next step is to frame it around a decision, so the data answers something.",
             "Vous collectez la conversation. L'étape suivante : la cadrer autour d'une décision, pour que la donnée réponde à quelque chose."] },
    { max: 8, name: ["Reading, not yet deciding", "Vous lisez, sans encore décider"],
      text: ["The reading is there. What is missing is the path from the analysis to the people who decide.",
             "La lecture est là. Il manque le chemin entre l'analyse et celles et ceux qui décident."] },
    { max: 12, name: ["Deciding with the data", "Vous décidez avec la donnée"],
      text: ["Your setup already informs decisions. The gains now are in coverage, languages and speed.",
             "Votre dispositif éclaire déjà des décisions. Les gains sont désormais dans la couverture, les langues et la vitesse."] }
  ];

  var stage = document.getElementById("quiz-stage");
  if (stage) {
    var quiz = document.getElementById("quiz");
    var radarEl = document.getElementById("quiz-radar");
    var reducedQ = window.matchMedia("(prefers-reduced-motion: reduce)");
    var answers = [];
    var step = 0, sent = false;
    function L(pair) { return fr() ? pair[1] : pair[0]; }
    function two(n) { return (n < 10 ? "0" : "") + n; }
    function weakest() { return answers.indexOf(Math.min.apply(null, answers)); }

    /* ---- the listening radar: six axes, one per dimension. An answer
       pushes its axis out (level 1, 2 or 3 of 3); hovering an answer
       previews it; at the end the weakest axis shows in pink. */
    var RW = 400, RH = 360, CX = 200, CY = 182, RR = 122, N = QUIZ.length;
    var shown = QUIZ.map(function () { return 0.07; }), preview = null, tweenId = 0;
    function pt(i, f) {
      var a = -Math.PI / 2 + i * 2 * Math.PI / N;
      return [CX + Math.cos(a) * RR * f, CY + Math.sin(a) * RR * f];
    }
    function target(i) {
      var v = i === step && preview !== null ? preview : answers[i];
      return v === undefined || v === null ? 0.07 : (v + 1) / 3;
    }
    function ring(f) { return QUIZ.map(function (_, i) { return pt(i, f).map(function (x) { return x.toFixed(1); }).join(","); }).join(" "); }
    function buildRadar() {
      if (!radarEl) return;
      var done = step >= N, weak = done ? weakest() : -1;
      var axes = "", labels = "";
      QUIZ.forEach(function (q, i) {
        var e = pt(i, 1), l = pt(i, 1.2), a = Math.cos(-Math.PI / 2 + i * 2 * Math.PI / N);
        var anchor = Math.abs(a) < 0.2 ? "middle" : a > 0 ? "start" : "end";
        var dy = i === 0 ? -4 : Math.abs(a) < 0.2 ? 14 : 4;
        var cls = done ? (i === weak ? "is-weak" : "is-done") : i === step ? "is-now" : answers[i] !== undefined ? "is-done" : "";
        axes += '<line class="qr__axis ' + cls + '" x1="' + CX + '" y1="' + CY + '" x2="' + e[0].toFixed(1) + '" y2="' + e[1].toFixed(1) + '"/>';
        labels += '<text class="qr__label ' + cls + '" x="' + l[0].toFixed(1) + '" y="' + (l[1] + dy).toFixed(1) + '" text-anchor="' + anchor + '">' +
          '<tspan class="qr__n">' + two(i + 1) + "</tspan> " + L(q.dim) + "</text>";
      });
      radarEl.innerHTML =
        '<svg viewBox="0 0 ' + RW + " " + RH + '" class="qr' + (done ? " is-done" : "") + '">' +
          '<defs><radialGradient id="qr-fill" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#EAA93D" stop-opacity=".55"/><stop offset="1" stop-color="#EAA93D" stop-opacity=".18"/></radialGradient></defs>' +
          '<circle class="qr__sonar" cx="' + CX + '" cy="' + CY + '" r="' + RR + '"/>' +
          '<circle class="qr__sonar qr__sonar--2" cx="' + CX + '" cy="' + CY + '" r="' + RR + '"/>' +
          [1 / 3, 2 / 3, 1].map(function (f) { return '<polygon class="qr__ring" points="' + ring(f) + '"/>'; }).join("") +
          axes +
          '<polygon class="qr__shape" id="qr-shape" points="' + ring(0.07) + '"/>' +
          QUIZ.map(function (_, i) { return '<circle class="qr__dot' + (i === weak ? " is-weak" : "") + '" id="qr-dot-' + i + '" r="' + (i === step || i === weak ? 5.5 : 4) + '"/>'; }).join("") +
          labels +
        "</svg>";
      paint();
    }
    function paint() {
      var shape = document.getElementById("qr-shape");
      if (!shape) return;
      shape.setAttribute("points", shown.map(function (f, i) { return pt(i, f).map(function (x) { return x.toFixed(1); }).join(","); }).join(" "));
      shown.forEach(function (f, i) {
        var d = document.getElementById("qr-dot-" + i), p = pt(i, f);
        if (d) { d.setAttribute("cx", p[0].toFixed(1)); d.setAttribute("cy", p[1].toFixed(1)); }
      });
    }
    /* eases the shape to where the answers put it */
    function morph() {
      var from = shown.slice(), to = QUIZ.map(function (_, i) { return target(i); }), my = ++tweenId, t0 = performance.now();
      if (reducedQ.matches) { shown = to; paint(); return; }
      (function frame(now) {
        if (my !== tweenId) return;
        var k = Math.min(1, (now - t0) / 480), e = 1 - Math.pow(1 - k, 3);
        shown = from.map(function (f, i) { return f + (to[i] - f) * e; });
        paint();
        if (k < 1) requestAnimationFrame(frame);
      })(t0);
    }
    function score() { return answers.reduce(function (s, v) { return s + v; }, 0); }

    var LEVELS = [["Level 1", "Niveau 1"], ["Level 2", "Niveau 2"], ["Level 3", "Niveau 3"]];
    function renderQuestion() {
      var item = QUIZ[step];
      stage.innerHTML =
        '<div class="qhead">' +
          '<p class="qnum"><b>' + two(step + 1) + "</b><span>/ " + two(N) + "</span></p>" +
          '<p class="qdim">' + L(item.dim) + "</p>" +
        "</div>" +
        '<div class="qseg" aria-hidden="true">' + QUIZ.map(function (_, i) {
          return "<i" + (i < step ? ' class="is-done"' : i === step ? ' class="is-now"' : "") + "></i>";
        }).join("") + "</div>" +
        '<h3 class="quiz__q">' + L(item.q) + "</h3>" +
        '<div class="quiz__opts" role="group" aria-label="' + L(item.q).replace(/"/g, "&quot;") + '">' +
          item.a.map(function (a, i) {
            var on = answers[step] === i ? " is-on" : "";
            return '<button class="quiz__opt' + on + '" type="button" data-v="' + i + '">' +
              '<span class="qsig" data-l="' + (i + 1) + '" aria-hidden="true"><i></i><i></i><i></i></span>' +
              '<span class="qopt__t">' + L(a) + '<small>' + L(LEVELS[i]) + "</small></span>" +
              '<kbd aria-hidden="true">' + (i + 1) + "</kbd></button>";
          }).join("") +
        "</div>" +
        '<div class="qfoot">' +
          (step ? '<button class="quiz__back" type="button">← ' + t("Back", "Retour") + "</button>" : "<span></span>") +
          '<p class="qkeys">' + t("Keys 1, 2, 3 work too", "Les touches 1, 2, 3 marchent aussi") + "</p>" +
        "</div>";
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
    }

    function renderResult() {
      var s = score();
      var band = BANDS.filter(function (b) { return s <= b.max; })[0];
      var w = weakest();
      stage.innerHTML =
        '<div class="qhead"><p class="qnum"><b>' + s + "</b><span>/ " + N * 2 + "</span></p>" +
          '<p class="qdim">' + t("Your score", "Votre score") + "</p></div>" +
        '<div class="qseg is-full" aria-hidden="true">' + QUIZ.map(function () { return '<i class="is-done"></i>'; }).join("") + "</div>" +
        '<h3 class="quiz__q quiz__q--band">' + L(band.name) + "</h3>" +
        '<p class="quiz__text">' + L(band.text) + "</p>" +
        '<p class="qweak"><span>' + t("Where to start", "Par où commencer") + "</span><b>" + two(w + 1) + " " + L(QUIZ[w].dim) + "</b></p>" +
        (sent
          ? '<p class="quiz__sent">' + t("Noted. The full readout arrives by email.", "C'est noté. Le détail arrive par e-mail.") + "</p>"
          : '<form class="quiz__form" novalidate>' +
              '<label class="fld__label" for="quiz-email">' + t("Get the full readout, dimension by dimension", "Recevez le détail, dimension par dimension") + "</label>" +
              '<div class="quiz__row"><input class="fld__input" id="quiz-email" type="email" autocomplete="email" placeholder="' + t("name@company.com", "nom@entreprise.com") + '" required />' +
              '<button class="btn btn--primary" type="submit">' + t("Send it to me", "Me l'envoyer") + "</button></div>" +
              '<p class="fld__error" hidden>' + t("Enter a work email, like name@company.com.", "Saisissez un e-mail professionnel, par exemple nom@entreprise.com.") + "</p>" +
              '<p class="consent">' + t("We use your email only to reply to you. ", "Votre e-mail sert uniquement à vous répondre. ") +
                '<a href="privacy.html">' + t("Privacy policy", "Politique de confidentialité") + "</a>.</p>" +
            "</form>") +
        '<div class="qfoot">' +
          '<button class="quiz__back" type="button" data-restart>↺ ' + t("Start again", "Recommencer") + "</button>" +
          '<p class="quiz__more"><a href="guide.html">' + t("Or start with the free guide", "Ou commencez par le guide gratuit") +
            ' <span aria-hidden="true">\u2192</span></a></p>' +
        "</div>";
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
    }

    function render(moveFocus) {
      preview = null;
      if (step < QUIZ.length) renderQuestion(); else renderResult();
      buildRadar(); morph();
      /* the stage is rebuilt: without this, focus falls back to the page top */
      if (moveFocus) {
        var q = stage.querySelector(".quiz__q");
        q.setAttribute("tabindex", "-1");
        q.focus({ preventScroll: true });
      }
    }

    function choose(v) {
      var opt = stage.querySelector('.quiz__opt[data-v="' + v + '"]');
      if (!opt || step >= QUIZ.length) return;
      answers[step] = v;
      Array.prototype.forEach.call(stage.querySelectorAll(".quiz__opt"), function (o) { o.classList.toggle("is-on", o === opt); });
      /* a beat so the choice registers before the next question arrives */
      preview = v; morph();
      setTimeout(function () { step++; render(true); }, 260);
    }

    stage.addEventListener("click", function (e) {
      var opt = e.target.closest(".quiz__opt");
      if (opt) { choose(+opt.dataset.v); return; }
      var back = e.target.closest(".quiz__back");
      if (back) {
        if (back.hasAttribute("data-restart")) { answers = []; step = 0; sent = false; }
        else step = Math.max(0, step - 1);
        render(true);
      }
    });
    /* hovering or focusing an answer previews it on the radar */
    function onPreview(e) {
      var opt = e.target.closest && e.target.closest(".quiz__opt");
      var v = opt ? +opt.dataset.v : null;
      if (v === preview) return;
      preview = v; morph();
    }
    stage.addEventListener("mouseover", onPreview);
    stage.addEventListener("focusin", onPreview);
    stage.addEventListener("mouseleave", function () { if (preview !== null && step < QUIZ.length) { preview = null; morph(); } });
    /* 1, 2, 3 answer while the diagnostic is on screen */
    var inView = false;
    if ("IntersectionObserver" in window && quiz) {
      new IntersectionObserver(function (en) { inView = en[0].isIntersecting && en[0].intersectionRatio > 0.5; }, { threshold: [0, 0.5, 1] }).observe(quiz);
    }
    document.addEventListener("keydown", function (e) {
      if (!inView || e.metaKey || e.ctrlKey || e.altKey) return;
      if (/^(INPUT|TEXTAREA|SELECT)$/.test((e.target || {}).tagName || "")) return;
      if (e.key === "1" || e.key === "2" || e.key === "3") { e.preventDefault(); choose(+e.key - 1); }
    });

    stage.addEventListener("submit", function (e) {
      e.preventDefault();
      var field = stage.querySelector("#quiz-email");
      var err = stage.querySelector(".quiz__form .fld__error");
      var ok = EMAIL.test(field.value.trim());
      field.setAttribute("aria-invalid", ok ? "false" : "true");
      err.hidden = ok;
      if (!ok) { field.focus(); return; }
      /* MOCK: wire to the CRM here (score, answers, email) */
      sent = true;
      render(true);
    });

    onLang(render);
  }

  /* --------------------------------------------------------------- guide */
  /* The twelve questions are the use-case questions: three open, nine
     unlocked by the email. */
  var GUIDE = [
    ["Analyze the impact of an event or campaign", "Mesurer l'impact d'un événement ou d'une campagne"],
    ["Optimize your leader advocacy strategy", "Optimiser la prise de parole de vos dirigeants"],
    ["Identify the right ambassadors", "Identifier les bons ambassadeurs"],
    ["Monitor your brand image and reputation", "Surveiller l'image et la réputation de votre marque"],
    ["Develop your brand messaging", "Construire votre discours de marque"],
    ["Identify and mitigate brand risks", "Identifier et désamorcer les risques de marque"],
    ["Segment your target profiles", "Segmenter vos profils cibles"],
    ["Rejuvenate your audiences", "Rajeunir vos audiences"],
    ["Understand expectations at every touchpoint", "Comprendre les attentes à chaque point de contact"],
    ["Test and evaluate your products", "Tester et évaluer vos produits"],
    ["Analyze markets and identify opportunities", "Analyser les marchés et repérer les opportunités"],
    ["Map out your stakeholders and future trends", "Cartographier vos parties prenantes et les tendances à venir"]
  ];
  var list = document.getElementById("guide-list");
  var box = document.getElementById("guide-box");
  if (list && box) {
    var open = false;
    function renderGuide() {
      list.innerHTML = GUIDE.map(function (g, i) {
        var locked = !open && i > 2;
        return '<li class="guide__item' + (locked ? " is-locked" : "") + '" style="--i:' + i + '"' +
          (locked ? ' aria-hidden="true"' : "") + ">" +
          '<span class="guide__n">' + (i < 9 ? "0" : "") + (i + 1) + "</span>" +
          '<span class="guide__q">' + (fr() ? g[1] : g[0]) + "</span></li>";
      }).join("");
    }
    onLang(renderGuide);

    var form = box.querySelector(".guide__form");
    if (form) form.addEventListener("submit", function () {
      /* js/ui.js validates first; it marks the field valid on success */
      var field = form.querySelector(".signup__input");
      if (field.getAttribute("aria-invalid") !== "false") return;
      /* MOCK: wire to the CRM here */
      open = true;
      box.classList.add("is-open");
      renderGuide();
    });
  }

  /* ------------------------------------------------------------- callback
     One field, email or phone. MOCK: nothing is sent yet; wire to the CRM. */
  var bookForm = document.getElementById("book-form");
  if (bookForm) {
    var contact = document.getElementById("book-contact");
    var contactErr = document.getElementById("book-contact-error");
    var sentTo = null;
    function kind(v) {
      if (EMAIL.test(v)) return "email";
      var digits = v.replace(/[\s.()-]/g, "");
      if (/^\+?\d{9,15}$/.test(digits)) return "phone";
      return null;
    }
    contact.addEventListener("input", function () {
      if (!contactErr.hidden) { contactErr.hidden = true; contact.setAttribute("aria-invalid", "false"); }
    });
    bookForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = contact.value.trim(), k = kind(v);
      contact.setAttribute("aria-invalid", k ? "false" : "true");
      contactErr.hidden = !!k;
      if (!k) { contact.focus(); return; }
      /* MOCK: wire to the CRM here (contact, kind) */
      sentTo = { v: v, k: k };
      bookForm.hidden = true;
      document.getElementById("book-done").hidden = false;
      renderDone();
    });
    function renderDone() {
      if (!sentTo) return;
      document.getElementById("book-done").innerHTML = "<b>" + t("Noted.", "C'est noté.") + "</b> " +
        (sentTo.k === "phone"
          ? t("A consultant calls you on ", "Un consultant vous appelle au ") + "<b>" + sentTo.v.replace(/</g, "&lt;") + "</b>" + t(" within 30 minutes.", " dans les 30 minutes.")
          : t("A consultant writes to you at ", "Un consultant vous écrit à ") + "<b>" + sentTo.v.replace(/</g, "&lt;") + "</b>" + t(" within 30 minutes.", " dans les 30 minutes."));
    }
    onLang(renderDone);
  }
})();

/* =========================================================================
   Method: a horizontal track of cards. The step bar, the arrows and the
   track stay in step whichever one moves.
   ========================================================================= */
(function () {
  var track = document.querySelector(".htrack");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".mstep"));
  var steps = Array.prototype.slice.call(document.querySelectorAll(".hstep"));
  var bar = document.querySelector(".hsteps");
  if (!track || !cards.length) return;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var active = 0;

  /* room after the last card, so every card, the last one included,
     can come to rest against the left edge */
  function pad() {
    var last = cards[cards.length - 1];
    var start = parseFloat(getComputedStyle(track).paddingLeft) || 0;
    /* padding-right does not extend a scroll area everywhere: a spacer item does */
    var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    track.style.setProperty("--end", Math.max(0, track.clientWidth - last.offsetWidth - 2 * start - gap) + "px");
  }
  pad();
  window.addEventListener("resize", pad);

  function set(i) {
    active = i;
    steps.forEach(function (b, k) {
      b.classList.toggle("is-on", k === i);
      b.classList.toggle("is-done", k < i);
      if (k === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    cards.forEach(function (c, k) { c.classList.toggle("is-on", k === i); });
    if (bar) bar.style.setProperty("--p", (i / (cards.length - 1)).toFixed(3));
    document.querySelectorAll(".hmethod__arrow").forEach(function (a) {
      var d = +a.dataset.dir;
      a.disabled = (d < 0 && i === 0) || (d > 0 && i === cards.length - 1);
    });
  }
  function go(i) {
    i = Math.max(0, Math.min(cards.length - 1, i));
    track.scrollTo({ left: cards[i].offsetLeft - cards[0].offsetLeft, behavior: reduced.matches ? "auto" : "smooth" });
    set(i);
  }
  steps.forEach(function (b, i) { b.addEventListener("click", function () { go(i); }); });
  document.querySelectorAll(".hmethod__arrow").forEach(function (a) {
    a.addEventListener("click", function () { go(active + (+a.dataset.dir)); });
  });
  track.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); go(active + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); go(active - 1); }
  });
  /* swipe or trackpad: the card nearest the left edge is the current one */
  var t = null;
  track.addEventListener("scroll", function () {
    clearTimeout(t);
    t = setTimeout(function () {
      var x = track.scrollLeft + cards[0].offsetLeft, best = 0, d = Infinity;
      cards.forEach(function (c, k) { var dd = Math.abs(c.offsetLeft - x); if (dd < d) { d = dd; best = k; } });
      set(best);
    }, 80);
  }, { passive: true });
  set(0);
})();
