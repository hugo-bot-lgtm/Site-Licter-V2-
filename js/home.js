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
    var bar = document.getElementById("quiz-bar");
    var answers = [];
    var step = 0, sent = false;
    function L(pair) { return fr() ? pair[1] : pair[0]; }

    var dims = document.querySelectorAll("#quiz-dims li");
    function progress() {
      if (bar) bar.style.transform = "scaleX(" + Math.min(step, QUIZ.length) / QUIZ.length + ")";
      Array.prototype.forEach.call(dims, function (li, i) {
        li.classList.toggle("is-done", i < step);
        li.classList.toggle("is-now", i === step);
      });
    }

    function renderQuestion() {
      var item = QUIZ[step];
      stage.innerHTML =
        '<p class="quiz__count">' + t("Question", "Question") + " " + (step + 1) + " " + t("of", "sur") + " " + QUIZ.length +
          " <span>" + L(item.dim) + "</span></p>" +
        '<h3 class="quiz__q">' + L(item.q) + "</h3>" +
        '<div class="quiz__opts" role="group" aria-label="' + L(item.q).replace(/"/g, "&quot;") + '">' +
          item.a.map(function (a, i) {
            var on = answers[step] === i ? " is-on" : "";
            return '<button class="quiz__opt' + on + '" type="button" data-v="' + i + '">' + L(a) + "</button>";
          }).join("") +
        "</div>" +
        (step ? '<button class="quiz__back" type="button">' + t("Back", "Retour") + "</button>" : "");
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
      progress();
    }

    function renderResult() {
      var score = answers.reduce(function (s, v) { return s + v; }, 0);
      var band = BANDS.filter(function (b) { return score <= b.max; })[0];
      var weakest = answers.indexOf(Math.min.apply(null, answers));
      stage.innerHTML =
        '<p class="quiz__count">' + t("Your score", "Votre score") + "</p>" +
        '<p class="quiz__score"><b>' + score + "</b><span>/ 12</span></p>" +
        '<h3 class="quiz__q">' + L(band.name) + "</h3>" +
        '<p class="quiz__text">' + L(band.text) + " " +
          t("Your weakest dimension: ", "Votre dimension la plus faible : ") + "<b>" + L(QUIZ[weakest].dim).toLowerCase() + "</b>.</p>" +
        (sent
          ? '<p class="quiz__sent">' + t("Noted. The full readout arrives by email.", "C'est noté. Le détail arrive par e-mail.") + "</p>"
          : '<form class="quiz__form" novalidate>' +
              '<label class="fld__label" for="quiz-email">' + t("Get the full readout, dimension by dimension", "Recevez le détail, dimension par dimension") + "</label>" +
              '<div class="quiz__row"><input class="fld__input" id="quiz-email" type="email" autocomplete="email" required />' +
              '<button class="btn btn--primary" type="submit">' + t("Send it to me", "Me l'envoyer") + "</button></div>" +
              '<p class="fld__error" hidden>' + t("Enter a work email, like name@company.com.", "Saisissez un e-mail professionnel, par exemple nom@entreprise.com.") + "</p>" +
              '<p class="consent">' + t("We use your email only to reply to you. ", "Votre e-mail sert uniquement à vous répondre. ") +
                '<a href="privacy.html">' + t("Privacy policy", "Politique de confidentialité") + "</a>.</p>" +
            "</form>") +
        '<p class="quiz__more"><a href="guide.html">' + t("Or start with the free guide", "Ou commencez par le guide gratuit") +
          ' <span aria-hidden="true">\u2192</span></a></p>' +
        '<button class="quiz__back" type="button" data-restart>' + t("Start again", "Recommencer") + "</button>";
      stage.classList.remove("is-swap"); void stage.offsetWidth; stage.classList.add("is-swap");
      progress();
    }

    function render(moveFocus) {
      if (step < QUIZ.length) renderQuestion(); else renderResult();
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
        setTimeout(function () { step++; render(true); }, 180);
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

  /* ------------------------------------------------------------- booking */
  /* MOCK: generated availability. The real calendar replaces this block. */
  var slots = document.getElementById("slots");
  var bookForm = document.getElementById("book-form");
  if (slots && bookForm) {
    var picked = null, booked = false;
    var TIMES = ["09:30", "11:00", "14:00", "16:30"];

    function days() {
      var out = [], d = new Date();
      d.setHours(12, 0, 0, 0);
      while (out.length < 5) {
        d.setDate(d.getDate() + 1);
        if (d.getDay() !== 0 && d.getDay() !== 6) out.push(new Date(d));
      }
      return out;
    }
    /* a few slots taken, always the same ones, so the grid looks lived in */
    function taken(di, ti) { return (di * 7 + ti * 3) % 5 === 0; }

    function dayLabel(d) {
      return d.toLocaleDateString(fr() ? "fr-FR" : "en-GB", { weekday: "short", day: "numeric", month: "short" });
    }

    function renderSlots() {
      if (booked) return;
      var list = days();
      slots.innerHTML = list.map(function (d, di) {
        return '<div class="slots__day"><p class="slots__date">' + dayLabel(d) + "</p>" +
          TIMES.map(function (tm, ti) {
            var key = di + "-" + ti;
            var off = taken(di, ti);
            return '<button class="slot' + (picked && picked.key === key ? " is-on" : "") + '" type="button"' +
              (off ? " disabled" : "") + ' data-key="' + key + '" data-day="' + di + '" data-time="' + tm + '">' +
              tm + (off ? '<span class="visually-hidden"> ' + t("unavailable", "indisponible") + "</span>" : "") + "</button>";
          }).join("") + "</div>";
      }).join("");
      if (picked) {
        picked.label = dayLabel(list[picked.day]) + ", " + picked.time;
        document.getElementById("book-picked").textContent = t("Your slot: ", "Votre créneau : ") + picked.label;
      }
    }

    slots.addEventListener("click", function (e) {
      var b = e.target.closest(".slot");
      if (!b || b.disabled) return;
      picked = { key: b.dataset.key, day: +b.dataset.day, time: b.dataset.time };
      bookForm.hidden = false;
      renderSlots();
      document.getElementById("book-email").focus({ preventScroll: true });
    });

    var bookEmail = document.getElementById("book-email");
    var bookErr = document.getElementById("book-email-error");
    bookEmail.addEventListener("input", function () {
      if (!bookErr.hidden) { bookErr.hidden = true; bookEmail.setAttribute("aria-invalid", "false"); }
    });

    bookForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = EMAIL.test(bookEmail.value.trim());
      bookEmail.setAttribute("aria-invalid", ok ? "false" : "true");
      bookErr.hidden = ok;
      if (!ok) { bookEmail.focus(); return; }
      /* MOCK: wire to the calendar / CRM here */
      booked = true;
      var done = document.getElementById("book-done");
      bookForm.hidden = true;
      slots.hidden = true;
      done.hidden = false;
      renderDone();
    });

    function renderDone() {
      if (!booked) return;
      document.getElementById("book-done").innerHTML =
        "<b>" + t("Booked for ", "Réservé pour ") + picked.label + ".</b> " +
        t("A calendar invitation is on its way, with the consultant's name.",
          "Une invitation arrive dans votre agenda, avec le nom du consultant.");
    }

    onLang(function () { renderSlots(); renderDone(); });
  }
})();
