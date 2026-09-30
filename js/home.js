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
    /* next: the step that fits the score, from the lightest to the most direct */
    { max: 4, name: ["Listening, not yet reading", "Vous écoutez, sans encore lire"],
      next: { text: ["Start with the guide: the 12 questions social data answers better than a survey.", "Commencez par le guide : les 12 questions auxquelles la donnée sociale répond mieux qu'un sondage."],
              cta: ["Get the free guide", "Recevoir le guide gratuit"], href: "/guide.html" },
      text: ["You collect the conversation. The next step is to frame it around a decision, so the data answers something.",
             "Vous collectez la conversation. L'étape suivante : la cadrer autour d'une décision, pour que la donnée réponde à quelque chose."] },
    { max: 8, name: ["Reading, not yet deciding", "Vous lisez, sans encore décider"],
      next: { text: ["A 30-minute review of your setup shows where the reading stops before the decision.", "Une revue de 30 minutes de votre dispositif montre où la lecture s'arrête avant la décision."],
              cta: ["Book a free 30-minute review", "Réserver une revue gratuite de 30 min"], href: "#book" },
      text: ["The reading is there. What is missing is the path from the analysis to the people who decide.",
             "La lecture est là. Il manque le chemin entre l'analyse et celles et ceux qui décident."] },
    { max: 12, name: ["Deciding with the data", "Vous décidez avec la donnée"],
      next: { text: ["Your setup is mature: the conversation worth having is about coverage, languages and speed.", "Votre dispositif est mûr : la conversation à avoir porte sur la couverture, les langues et la vitesse."],
              cta: ["Talk to a consultant", "Parler à un consultant"], href: "#book" },
      text: ["Your setup already informs decisions. The gains now are in coverage, languages and speed.",
             "Votre dispositif éclaire déjà des décisions. Les gains sont désormais dans la couverture, les langues et la vitesse."] }
  ];

  var stage = document.getElementById("quiz-stage");
  if (stage) {
    var stepsEl = document.getElementById("quiz-steps");
    var answers = [];
    var step = 0, sent = false;
    var N = QUIZ.length;
    function L(pair) { return fr() ? pair[1] : pair[0]; }
    function two(n) { return (n < 10 ? "0" : "") + n; }
    function score() { return answers.reduce(function (s, v) { return s + v; }, 0); }
    function lead() { return window.LicterLead ? window.LicterLead.get() : ""; }
    function weakest() { return answers.indexOf(Math.min.apply(null, answers)); }

    /* the six dimensions across the top: done, current, to come */
    function renderSteps() {
      if (!stepsEl) return;
      var done = step >= N, weak = done ? weakest() : -1;
      stepsEl.innerHTML = QUIZ.map(function (q, i) {
        var cls = i === weak ? "is-weak" : i < step ? "is-done" : i === step ? "is-now" : "";
        return '<li class="' + cls + '"><span>' + two(i + 1) + "</span>" + L(q.dim) + "</li>";
      }).join("");
    }

    function renderQuestion() {
      var item = QUIZ[step];
      stage.innerHTML =
        '<p class="quiz__count">' + t("Question", "Question") + " " + (step + 1) + " " + t("of", "sur") + " " + N + "</p>" +
        '<h3 class="quiz__q">' + L(item.q) + "</h3>" +
        '<div class="quiz__opts" role="group" aria-label="' + L(item.q).replace(/"/g, "&quot;") + '">' +
          item.a.map(function (a, i) {
            var on = answers[step] === i ? " is-on" : "";
            return '<button class="quiz__opt' + on + '" type="button" data-v="' + i + '"><span class="qopt__k" aria-hidden="true">' + "ABC".charAt(i) + "</span>" + L(a) + "</button>";
          }).join("") +
        "</div>" +
        (step ? '<button class="quiz__back" type="button">← ' + t("Back", "Retour") + "</button>" : "");
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
    }

    function renderResult() {
      var s = score();
      var band = BANDS.filter(function (b) { return s <= b.max; })[0];
      var w = weakest();
      stage.innerHTML =
        '<div class="qres">' +
        '<div class="qres__head">' +
          '<p class="quiz__count">' + t("Your score", "Votre score") + "</p>" +
          '<p class="quiz__score"><b>' + s + "</b><span>/ " + N * 2 + "</span></p>" +
          '<h3 class="quiz__q">' + L(band.name) + "</h3>" +
        "</div>" +
        '<div class="qres__body">' +
        '<p class="quiz__text">' + L(band.text) + " " +
          t("Start with ", "Commencez par ") + "<b>" + L(QUIZ[w].dim).toLowerCase() + "</b>.</p>" +
        '<div class="qnext"><p><span>' + t("Your next step", "Votre prochaine étape") + "</span>" + L(band.next.text) + "</p>" +
          '<a class="btn btn--primary" href="' + band.next.href + '">' + L(band.next.cta) + ' <span aria-hidden="true">→</span></a></div>' +
        (sent
          ? '<p class="quiz__sent">' + t("Noted. The full readout arrives by email.", "C'est noté. Le détail arrive par e-mail.") + "</p>"
          : '<form class="quiz__form" novalidate>' +
              '<label class="fld__label" for="quiz-email">' + t("And the full readout, dimension by dimension, by email", "Et le détail, dimension par dimension, par e-mail") + "</label>" +
              '<div class="quiz__row"><input class="fld__input" id="quiz-email" type="email" autocomplete="email" value="' + lead().replace(/"/g, "&quot;") + '" required />' +
              '<button class="btn btn--primary" type="submit">' + t("Send it to me", "Me l'envoyer") + "</button></div>" +
              '<p class="fld__error" hidden>' + t("Enter a work email, like name@company.com.", "Saisissez un e-mail professionnel, par exemple nom@entreprise.com.") + "</p>" +
              '<p class="consent">' + t("We use your email only to reply to you. ", "Votre e-mail sert uniquement à vous répondre. ") +
                '<a href="/privacy.html">' + t("Privacy policy", "Politique de confidentialité") + "</a>.</p>" +
            "</form>") +
        '<button class="quiz__back" type="button" data-restart>' + t("Start again", "Recommencer") + "</button>" +
        "</div></div>";
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
    }

    function render(moveFocus) {
      if (step < N) renderQuestion(); else renderResult();
      renderSteps();
      /* the stage is rebuilt: without this, focus falls back to the page top */
      if (moveFocus) {
        var q = stage.querySelector(".quiz__q");
        q.setAttribute("tabindex", "-1");
        q.focus({ preventScroll: true });
      }
    }

    stage.addEventListener("click", function (e) {
      var opt = e.target.closest(".quiz__opt");
      if (opt) {
        answers[step] = +opt.dataset.v;
        opt.classList.add("is-on");
        /* a beat so the choice registers before the next question arrives */
        setTimeout(function () { step++; render(true); }, 200);
        return;
      }
      var back = e.target.closest(".quiz__back");
      if (back) {
        if (back.hasAttribute("data-restart")) { answers = []; step = 0; sent = false; }
        else step = Math.max(0, step - 1);
        render(true);
      }
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
      if (window.LicterLead) window.LicterLead.set(field.value.trim());
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
    /* an email left elsewhere on the page is already there */
    function prefill(v) { if (!contact.value && EMAIL.test(v || "")) contact.value = v; }
    if (window.LicterLead) { prefill(window.LicterLead.get()); window.LicterLead.on(prefill); }
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
      if (k === "email" && window.LicterLead) window.LicterLead.set(v);
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
   Method: a horizontal track of cards, the current one centred. The step
   bar, the arrows and the track stay in step whichever one moves, and the
   four steps loop: past the fourth comes the first again.
   ========================================================================= */
(function () {
  var track = document.querySelector(".htrack");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".mstep"));
  var steps = Array.prototype.slice.call(document.querySelectorAll(".hstep"));
  var bar = document.querySelector(".hsteps");
  if (!track || !cards.length) return;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var last = cards.length - 1, active = 0;

  /* room on both sides, so the first and the last card can come to the centre */
  function pad() {
    track.style.setProperty("--side", Math.max(0, (track.clientWidth - cards[0].offsetWidth) / 2) + "px");
  }
  function leftOf(i) { return cards[i].offsetLeft - (track.clientWidth - cards[i].offsetWidth) / 2; }
  pad();
  window.addEventListener("resize", function () { pad(); track.scrollTo({ left: leftOf(active), behavior: "auto" }); });

  function set(i) {
    active = i;
    steps.forEach(function (b, k) {
      b.classList.toggle("is-on", k === i);
      b.classList.toggle("is-done", k < i);
      if (k === i) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current");
    });
    cards.forEach(function (c, k) { c.classList.toggle("is-on", k === i); });
    if (bar) bar.style.setProperty("--p", (i / last).toFixed(3));
  }
  var wrapping = false;
  function go(i) {
    /* the steps loop both ways */
    if (i > last) i = 0;
    if (i < 0) i = last;
    wrapping = Math.abs(i - active) > 1;
    track.scrollTo({ left: leftOf(i), behavior: reduced.matches ? "auto" : "smooth" });
    set(i);
    if (wrapping) setTimeout(function () { wrapping = false; }, 900);
  }
  steps.forEach(function (b, i) { b.addEventListener("click", function () { go(i); }); });
  document.querySelectorAll(".hmethod__arrow").forEach(function (a) {
    a.addEventListener("click", function () { go(active + (+a.dataset.dir)); });
  });
  track.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); go(active + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); go(active - 1); }
  });

  /* swipe or trackpad: the card nearest the centre is the current one */
  var t = null;
  track.addEventListener("scroll", function () {
    clearTimeout(t);
    t = setTimeout(function () {
      if (wrapping) return;
      var mid = track.scrollLeft + track.clientWidth / 2, best = 0, d = Infinity;
      cards.forEach(function (c, k) { var dd = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid); if (dd < d) { d = dd; best = k; } });
      set(best);
    }, 80);
  }, { passive: true });

  /* scrolling on past the fourth card brings the first one back */
  function atEnd() { return track.scrollLeft >= track.scrollWidth - track.clientWidth - 4; }
  var cool = 0, push = 0;
  track.addEventListener("wheel", function (e) {
    if (Math.abs(e.deltaX) <= Math.abs(e.deltaY) || e.deltaX <= 0) { push = 0; return; }
    if (active !== last || !atEnd() || Date.now() < cool) return;
    /* a deliberate push, not the tail of the inertia that brought us here */
    push += e.deltaX;
    if (push > 60) { push = 0; cool = Date.now() + 1200; go(0); }
  }, { passive: true });
  var x0 = null;
  track.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  track.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    x0 = null;
    if (dx < -50 && active === last && atEnd()) go(0);
  }, { passive: true });

  set(0);
})();

/* =========================================================================
   Use-case pages: "get a real case" (email + sector). MOCK: nothing is sent;
   wire to the CRM with the case (data-case) and the sector.
   ========================================================================= */
(function () {
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  Array.prototype.forEach.call(document.querySelectorAll("form.ucp-lead"), function (form) {
    var field = form.querySelector('input[type="email"]');
    var err = form.querySelector(".fld__error");
    var done = form.parentNode.querySelector(".ucp-lead__done");
    if (window.LicterLead) {
      var known = window.LicterLead.get();
      if (known && EMAIL.test(known)) field.value = known;
    }
    field.addEventListener("input", function () {
      if (!err.hidden) { err.hidden = true; field.setAttribute("aria-invalid", "false"); }
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = field.value.trim(), ok = EMAIL.test(v);
      field.setAttribute("aria-invalid", ok ? "false" : "true");
      err.hidden = ok;
      if (!ok) { field.focus(); return; }
      /* MOCK: send { email: v, case: form.dataset.case, sector: form.sector.value } */
      if (window.LicterLead) window.LicterLead.set(v);
      form.hidden = true;
      done.hidden = false;
      done.setAttribute("tabindex", "-1");
      done.focus({ preventScroll: true });
    });
  });
})();
