/* =========================================================================
   Two popups, centred:
   - "call": thirty minutes with a consultant, the callback;
   - "mag":  the Audience First magazine, sent as a PDF by email.

   The magazine opens by itself once per visitor, centred, never before 3 s:
   on the home once the demo or the comparison has scrolled by, elsewhere once
   half the page is read or the pointer heads for the tabs; on every
   screen size, never on a page whose point is a form (booking, diagnostic,
   guide, events). One field: the email. Closed without sending, it goes into a small dock at the
   bottom left, to be found again; once sent, it leaves the dock.
   The callback opens on every "Talk to a consultant" (any link to #book on
   the page, or with those words): never by itself.

   window.LicterPopups.open("call" | "mag") opens one on demand (the chat's
   "call me back" button uses it).

   MOCK: nothing is sent yet; wire both forms to the CRM in submit().
   Loaded by js/ui.js on every page.
   ========================================================================= */
(function () {
  "use strict";
  if (window.LicterPopups) return;

  var html = document.documentElement;
  function fr() { return (html.lang || "fr").slice(0, 2) === "fr"; }
  function typo(s) { return s.replace(/ ([?!:;»])/g, " $1").replace(/« /g, "« ").replace(/(\d) %/g, "$1 %"); }
  function T(p) { return fr() ? typo(p[0]) : p[1]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  /* callback hours (js/ui.js): "30 minutes" only when it is true */
  function hours() { return window.LicterHours || { open: function () { return true; }, next: function () { return ""; }, when: function (f) { return f ? " dans les 30 minutes" : " within 30 minutes"; } }; }
  function open30() { return hours().open(); }

  var C = {
    close: ["Fermer", "Close"],
    privacy: ["Politique de confidentialité", "Privacy policy"],
    /* the callback: the words of the home */
    callK: ["Être rappelé", "Call me back"],
    callBadge1: ["Réponse sous 30 min", "Reply within 30 min"],
    callBadge2: ["160+ projets depuis 2022", "160+ projects since 2022"],
    callImgAlt: ["Trois consultantes Licter dans les bureaux", "Three Licter consultants in the office"],
    callT: ["Trente minutes avec un consultant.", "Thirty minutes with a consultant."],
    callL: ["Laissez votre e-mail ou votre téléphone. Un consultant vous rappelle dans les 30 minutes en semaine.", "Leave your email or phone number. A consultant calls you back within 30 minutes on weekdays."],
    callF: ["E-mail ou téléphone", "Email or phone"],
    callP: ["nom@entreprise.com ou 06 12 34 56 78", "name@company.com or 06 12 34 56 78"],
    callB: ["Me faire rappeler", "Call me back"],
    callPr: ["Un consultant, pas un commercial. En semaine, de 9\u00a0h à 19\u00a0h.", "A consultant, not a sales team. Weekdays, 9am to 7pm."],
    callC: ["Vos coordonnées servent uniquement à vous rappeler.", "We use your contact details only to call you back."],
    callE: ["Indiquez un e-mail professionnel ou un numéro de téléphone.", "Enter a work email or a phone number."],
    callOkM: ["C'est noté. Un consultant vous écrit à ", "Noted. A consultant writes to you at "],
    callOkP: ["C'est noté. Un consultant vous appelle au ", "Noted. A consultant calls you on "],
    /* the magazine */
    magK: ["Magazine gratuit", "Free magazine"],
    magT: ["Audience First, le magazine.", "Audience First, the magazine."],
    magL: ["Les conversations du podcast avec celles et ceux qui pilotent l'écoute dans leur organisation, et nos lectures de la donnée sociale, réunies en PDF.",
           "The podcast's conversations with the people who run listening inside their organisation, and our reads of social data, together in one PDF."],
    magMail: ["E-mail professionnel", "Work email"],
    magB: ["Recevoir le magazine", "Send me the magazine"],
    magC: ["Vos coordonnées servent uniquement à vous envoyer le magazine.", "We use your details only to send you the magazine."],
    magE: ["Indiquez un e-mail professionnel valide.", "Enter a valid work email."],
    magOk: ["C'est noté. Le magazine arrive à ", "Noted. The magazine is on its way to "],
    magOkE: [", en PDF.", ", as a PDF."]
  };

  /* ------------------------------------------------------------ the DOM */
  var phone = window.matchMedia("(max-width: 720px)");
  var root = document.createElement("div");
  root.className = "pp";
  root.hidden = true;
  root.innerHTML = '<div class="pp__veil" data-close></div>' +
    '<div class="pp__box" role="dialog" aria-modal="true" aria-labelledby="pp-title" tabindex="-1"></div>';
  document.body.appendChild(root);
  var box = root.querySelector(".pp__box");
  var current = null, sent = {}, lastFocus = null;

  function faces() {
    return ["anushka", "aymeric", "elsa"].map(function (n) {
      return '<img src="/assets/img/team/morning/' + n + '-face-96.webp" alt="" width="48" height="48" loading="lazy" decoding="async" />';
    }).join("");
  }

  function render() {
    var k = current;
    var head = '<button class="pp__x" type="button" data-close><span aria-hidden="true">×</span><span class="visually-hidden">' + esc(T(C.close)) + "</span></button>";
    if (k === "call") {
      box.className = "pp__box pp__box--call";
      box.innerHTML = head +
        '<figure class="pp__photo">' +
          '<img src="/assets/img/team/morning/team-trio-800.webp" srcset="/assets/img/team/morning/team-trio-800.webp 800w, /assets/img/team/morning/team-trio-1080.webp 1080w" sizes="(max-width: 700px) 92vw, 340px" alt="' + esc(T(C.callImgAlt)) + '" width="800" height="1197" decoding="async" />' +
          '<figcaption class="pp__badges">' +
            '<span class="pp__badge pp__badge--live"><span class="pp__dot" aria-hidden="true"></span>' + esc(open30() ? T(C.callBadge1) : (fr() ? "Rappel " : "Call back ") + hours().next(fr())) + "</span>" +
            '<span class="pp__badge">' + esc(T(C.callBadge2)) + "</span>" +
          "</figcaption>" +
        "</figure>" +
        '<div class="pp__body">' +
          '<p class="pp__k"><span class="pp__faces" aria-hidden="true">' + faces() + "</span>" + esc(T(C.callK)) + "</p>" +
          '<h2 class="pp__t" id="pp-title">' + esc(T(C.callT)) + "</h2>" +
          '<p class="pp__l">' + esc(T(C.callL)) + "</p>" +
          (sent.call ? '<p class="pp__done" role="status">' + esc(T(sent.call.k === "phone" ? C.callOkP : C.callOkM)) + "<b>" + esc(sent.call.v) + "</b>" + esc(hours().when(fr())) + ".</p>" :
          '<form class="pp__form" novalidate data-form="call">' +
            '<label class="fld__label" for="pp-contact">' + esc(T(C.callF)) + "</label>" +
            '<input class="fld__input" id="pp-contact" name="contact" type="text" inputmode="email" autocomplete="email" placeholder="' + esc(T(C.callP)) + '" required />' +
            '<button class="btn btn--primary pp__wide" type="submit">' + esc(T(C.callB)) + ' <span aria-hidden="true">→</span></button>' +
            '<p class="fld__error" hidden>' + esc(T(C.callE)) + "</p>" +
            '<p class="pp__promise"><span class="pp__dot" aria-hidden="true"></span>' + esc(T(C.callPr)) + "</p>" +
            '<p class="consent">' + esc(T(C.callC)) + ' <a href="' + ((document.documentElement.lang || "fr").slice(0, 2) === "fr" ? "/fr/confidentialite/" : "/privacy.html") + '">' + esc(T(C.privacy)) + "</a>.</p>" +
          "</form>") +
        "</div>";
    } else {
      box.className = "pp__box pp__box--mag";
      box.innerHTML = head +
        '<div class="pp__cover" aria-hidden="true">' +
          '<img class="pp__cover-img" src="/assets/img/magazine/audience-first-ed2-440.webp" srcset="/assets/img/magazine/audience-first-ed2-440.webp 440w, /assets/img/magazine/audience-first-ed2-880.webp 880w" sizes="260px" alt="" width="440" height="640" decoding="async" />' +
        "</div>" +
        '<div class="pp__body">' +
          '<p class="pp__k">' + esc(T(C.magK)) + "</p>" +
          '<h2 class="pp__t" id="pp-title">' + esc(T(C.magT)) + "</h2>" +
          '<p class="pp__l">' + esc(T(C.magL)) + "</p>" +
          (sent.mag ? '<p class="pp__done" role="status">' + esc(T(C.magOk)) + "<b>" + esc(sent.mag.email) + "</b>" + esc(T(C.magOkE)) + "</p>" :
          '<form class="pp__form" novalidate data-form="mag">' +
            '<label class="fld__label" for="pp-mail">' + esc(T(C.magMail)) + "</label>" +
            '<input class="fld__input" id="pp-mail" name="email" type="email" autocomplete="email" placeholder="' + esc(T(C.callP).split(" ")[0]) + '" required />' +
            '<p class="fld__error" hidden>' + esc(T(C.magE)) + "</p>" +
            '<button class="btn btn--primary pp__wide" type="submit">' + esc(T(C.magB)) + ' <span aria-hidden="true">→</span></button>' +
            '<p class="consent">' + esc(T(C.magC)) + ' <a href="' + ((document.documentElement.lang || "fr").slice(0, 2) === "fr" ? "/fr/confidentialite/" : "/privacy.html") + '">' + esc(T(C.privacy)) + "</a>.</p>" +
          "</form>") +
        "</div>";
    }
    var lead = window.LicterLead ? window.LicterLead.get() : "";
    var m = box.querySelector('[name="email"], [name="contact"]');
    if (m && lead && EMAIL.test(lead)) m.value = lead;
  }

  /* ----------------------------------------------------- open and close */
  /* per visitor: "" (never shown), "seen" (closed, in the dock), "sent" */
  function state(k, v) { if (v === undefined) return get("pp-" + k) || ""; set("pp-" + k, v); paintDock(); }

  function track(n, p) { if (window.LicterTrack) window.LicterTrack(n, p); }
  function open(k, auto) {
    if (current) close(true);
    track("popup_open", { popup: k, auto: !!auto });
    current = k;
    lastFocus = document.activeElement;
    render();
    root.hidden = false;
    if (k !== "mag") html.classList.add("pp-open");   /* the magazine never freezes the page behind it */
    requestAnimationFrame(function () { root.classList.add("is-open"); });
    /* on a phone the focus goes to the popup, not the field: the keyboard
       would cover it before it is read */
    var first = (!phone.matches && box.querySelector("input")) || box;
    setTimeout(function () { first.focus({ preventScroll: true }); }, 60);
    if (state(k) !== "sent") state(k, "seen");
    dock.classList.add("is-hidden");
  }
  function close(quiet) {
    if (!current) return;
    if (!sent[current]) track("popup_close", { popup: current });
    root.classList.remove("is-open");
    dock.classList.remove("is-hidden");
    html.classList.remove("pp-open");
    current = null;
    setTimeout(function () { if (!current) root.hidden = true; }, 220);
    if (queued) { var q = queued; queued = null; setTimeout(function () { if (may(q)) open(q, true); }, 600); }
    if (!quiet && lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  root.addEventListener("click", function (e) { if (e.target.closest("[data-close]")) close(); });
  document.addEventListener("keydown", function (e) {
    if (!current) return;
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key !== "Tab") return;
    /* keep the focus inside the popup */
    var f = Array.prototype.filter.call(box.querySelectorAll("a[href], button, input"), function (x) { return x.offsetParent !== null; });
    if (!f.length) return;
    var a = f[0], z = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
    else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
  });

  /* -------------------------------------------------------------- forms */
  box.addEventListener("input", function (e) {
    if (e.target.matches("input")) { e.target.setAttribute("aria-invalid", "false"); var er = box.querySelector(".fld__error"); if (er) er.hidden = true; }
  });
  box.addEventListener("submit", function (e) {
    e.preventDefault();
    var form = e.target, k = form.getAttribute("data-form"), err = form.querySelector(".fld__error"), bad = null;
    if (k === "call") {
      var i = form.querySelector('[name="contact"]'), v = i.value.trim();
      var kind = EMAIL.test(v) ? "email" : (/^\+?\d{9,15}$/.test(v.replace(/[\s.()-]/g, "")) ? "phone" : null);
      if (!kind) bad = i;
      else {
        if (window.LicterSend) window.LicterSend("callback", "Popup « Trente minutes avec un consultant »", { "E-mail ou téléphone": v });
        if (kind === "email" && window.LicterLead) window.LicterLead.set(v);
        sent.call = { v: v, k: kind };
      }
    } else {
      var d = {};
      Array.prototype.forEach.call(form.querySelectorAll("input"), function (x) {
        d[x.name] = x.value.trim();
        var ok = x.name === "email" ? EMAIL.test(d[x.name]) : !!d[x.name];
        x.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !bad) bad = x;
      });
      if (!bad) {
        if (window.LicterSend) window.LicterSend("magazine", "Popup « Audience First, le magazine »", form);
        if (window.LicterLead) window.LicterLead.set(d.email);
        sent.mag = d;
      }
    }
    if (bad) { bad.setAttribute("aria-invalid", "true"); err.hidden = false; bad.focus(); return; }
    state(k, "sent");
    track("popup_submit", { popup: k });
    render();
    var ok = box.querySelector(".pp__done");
    if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
  });

  /* --------------------------------------------------------- the dock
     the popups a visitor closed without sending, to open them again */
  var ICON_CALL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M6.5 4.5h3l1.5 4-2 1.3a10 10 0 0 0 5.2 5.2l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A15.5 15.5 0 0 1 4.5 6.7a2 2 0 0 1 2-2.2z"/></svg>';
  var dock = document.createElement("div");
  dock.className = "ppd";
  dock.setAttribute("role", "region");
  document.body.appendChild(dock);
  function paintDock() {
    var items = ["mag"].filter(function (k) { return state(k) === "seen"; });
    dock.hidden = !items.length;
    /* the home's bottom bar (phones, tablets) carries the cover instead */
    html.classList.toggle("pp-mag-docked", items.indexOf("mag") !== -1);
    dock.setAttribute("aria-label", fr() ? "Retrouver nos propositions" : "Find our offers again");
    dock.innerHTML = items.map(function (k) {
      if (k === "mag") {
        /* the magazine shows itself: its cover, its name, what it costs */
        /* just the cover and "get it free", on two small lines */
        return '<button type="button" class="ppd__b ppd__b--mag" data-open="mag" aria-label="' +
          esc(fr() ? "Audience First, le magazine gratuit" : "Audience First, the free magazine") + '">' +
          '<img class="ppd__cover" src="/assets/img/magazine/audience-first-ed2-440.webp" alt="" width="440" height="640" decoding="async" />' +
          '<span class="ppd__tag" aria-hidden="true">' + (fr() ? "Recevoir<br />gratuitement" : "Get it<br />free") + "</span></button>";
      }
      return '<button type="button" class="ppd__b ppd__b--' + k + '" data-open="' + k + '">' +
        '<span class="ppd__i" aria-hidden="true">' + ICON_CALL + "</span>" +
        esc(fr() ? "Être rappelé" : "Call me back") + "</button>";
    }).join("");
  }
  /* never over the home's hero: the dock waits until it has scrolled by */
  var hero = document.body.classList.contains("home") && document.getElementById("hero");
  if (hero) {
    var heroWait = function () { dock.classList.toggle("is-waiting", hero.getBoundingClientRect().bottom > window.innerHeight * 0.4); };
    window.addEventListener("scroll", heroWait, { passive: true });
    window.addEventListener("resize", heroWait);
    /* measured on the next frame, not while the page's scripts run (a forced layout) */
    dock.classList.add("is-waiting");
    requestAnimationFrame(heroWait);
  }
  /* nor over the footer or the booking form at the end of a page */
  if ("IntersectionObserver" in window) {
    var ends = [document.querySelector(".site-foot"), document.getElementById("book")].filter(Boolean), seen = [];
    var endIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { var i = ends.indexOf(e.target); seen[i] = e.isIntersecting; });
      dock.classList.toggle("is-footer", seen.some(Boolean));
    }, { rootMargin: "0px 0px -60px 0px" });
    ends.forEach(function (el) { endIO.observe(el); });
  }
  dock.addEventListener("click", function (e) {
    var b = e.target.closest("[data-open]");
    if (b) open(b.getAttribute("data-open"), false);
  });

  /* ------------------------------------------------ the automatic opening */
  var path = location.pathname;
  var formPage = /\/(book-a-meeting|diagnostic|guide|events|event-[a-z0-9-]+)\.html$/.test(path) ||
    /* their French twins, which live in folders */
    /^\/fr\/(rendez-vous|diagnostic|guide|evenements)(\/|$)/.test(path) ||
    /* the use-case pages bring their own magnet (a real case of the same
       kind), and so do the expertise pages (a sample deliverable): the
       magazine never interrupts them; its cover still waits below */
    /^\/(fr\/cas-usage|en\/use-cases|fr\/expertise)\//.test(path) || /^\/expertise(-[a-z]+-listening)?\.html$/.test(path) ||
    /^\/(fr\/offres\/|offers\.html|offer-[a-z0-9-]+\.html)/.test(path);
  var queued = null;
  function may(k) {
    return !formPage && !state(k) && !html.classList.contains("lx-open") && !html.classList.contains("pp-open") &&
      !(document.activeElement && document.activeElement.matches("input, textarea, select"));
  }
  function auto(k) {
    /* never on top of the cookie question: the magazine waits for the answer (js/track.js) */
    if (html.classList.contains("cc-open")) {
      document.addEventListener("licter:consent", function () { setTimeout(function () { auto(k); }, 1500); }, { once: true });
      return;
    }
    if (!may(k)) return;
    if (current) { if (current !== k) queued = k; return; }
    open(k, true);
  }
  /* the home asks for nothing before its proof is seen: the magazine waits
     until the argument has scrolled by (the demo, or "Why not just a tool?"
     on a phone; and the same 3 s at least); every other page opens it after 3 s */
  var after = document.querySelector("[data-mag-after]");
  if (after && !document.body.classList.contains("home")) {
    /* a landing page names the section the magazine waits for (expertise
       pages: once the questions it answers have scrolled by) */
    var tUp = false, past = false;
    var go2 = function () { if (tUp && past) auto("mag"); };
    setTimeout(function () { tUp = true; go2(); }, 3000);
    var onPast = function () {
      if (after.getBoundingClientRect().bottom > window.innerHeight * 0.5) return;
      window.removeEventListener("scroll", onPast);
      past = true; go2();
    };
    window.addEventListener("scroll", onPast, { passive: true });
  } else if (document.body.classList.contains("home")) {
    var timeUp = false, scrolled = false;
    var go = function () { if (timeUp && scrolled) auto("mag"); };
    setTimeout(function () { timeUp = true; go(); }, 3000);
    /* after the live demo where it shows (large screens), else after "Why
       not just a tool?": never in the middle of the main argument */
    var demo = document.getElementById("use-cases");
    var proof = demo && getComputedStyle(demo).display !== "none" ? demo : (document.querySelector(".cmp") || document.getElementById("voices"));
    var onScroll = function () {
      var past = proof ? proof.getBoundingClientRect().bottom < window.innerHeight * 0.5
                       : window.scrollY > (document.documentElement.scrollHeight - window.innerHeight) * 0.4;
      if (!past) return;
      window.removeEventListener("scroll", onScroll);
      scrolled = true; go();
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  } else {
    /* any other page may be the first one a visitor sees, coming from a
       search: the magazine waits until half the page has been read, or (with
       a mouse) until the pointer leaves for the tabs, and never before 3 s */
    var tUp3 = false, wants = false;
    var go3 = function () { if (tUp3 && wants) auto("mag"); };
    setTimeout(function () { tUp3 = true; go3(); }, 3000);
    var onHalf = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (max > 0 && window.scrollY < max * 0.5) return;
      window.removeEventListener("scroll", onHalf);
      wants = true; go3();
    };
    window.addEventListener("scroll", onHalf, { passive: true });
    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      document.addEventListener("mouseout", function onExit(e) {
        if (e.relatedTarget || e.clientY > 8) return;
        document.removeEventListener("mouseout", onExit);
        wants = true; go3();
      });
    }
  }
  paintDock();

  new MutationObserver(function () { if (current) render(); paintDock(); }).observe(html, { attributes: true, attributeFilter: ["lang"] });

  /* every "Talk to a consultant" opens the callback instead of jumping to the
     form at the bottom of the page (a new tab or window still follows the link) */
  var SAYS = /^(ou\s+)?(parler à un consultant|talk to a consultant|or talk to a consultant)/i;
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || root.contains(a)) return;
    var href = a.getAttribute("href");
    if (href !== "#book" && !SAYS.test((a.textContent || "").replace(/\s+/g, " ").trim())) return;
    e.preventDefault();
    var sec = a.closest("section[id], header, aside, .stickybar");
    track("cta_click", { where: sec ? (sec.id || sec.className.split(" ")[0]) : "page" });
    open("call", false);
  });

  window.LicterPopups = { open: function (k) { open(k === "mag" ? "mag" : "call", false); } };
})();
