/* =========================================================================
   Two popups, centred:
   - "call": thirty minutes with a consultant, the callback;
   - "mag":  the Audience First magazine, sent as a PDF by email.

   When they open by themselves (large screens only, never on a phone):
   - the callback, half-way down a page or after 40 seconds; not on the
     home, which has its own callback at the end;
   - the magazine, when the pointer leaves the window towards the tabs
     (exit intent), after 15 seconds on the page.
   Never both in the same visit, never after a form has been sent, never
   on a page whose point is a form (booking, diagnostic, guide, events),
   and a closed popup stays closed for 7 days.

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
  function sget(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  var C = {
    close: ["Fermer", "Close"],
    privacy: ["Politique de confidentialité", "Privacy policy"],
    /* the callback: the words of the home */
    callK: ["Être rappelé", "Call me back"],
    callT: ["Trente minutes avec un consultant.", "Thirty minutes with a consultant."],
    callL: ["Laissez votre e-mail ou votre téléphone. Un consultant vous rappelle dans les 30 minutes.", "Leave your email or phone number. A consultant calls you back within 30 minutes."],
    callF: ["E-mail ou téléphone", "Email or phone"],
    callP: ["nom@entreprise.com ou 06 12 34 56 78", "name@company.com or 06 12 34 56 78"],
    callB: ["Me faire rappeler", "Call me back"],
    callPr: ["Un consultant, pas un commercial. Dans les 30 minutes.", "A consultant, not a sales team. Within 30 minutes."],
    callC: ["Vos coordonnées servent uniquement à vous rappeler.", "We use your contact details only to call you back."],
    callE: ["Indiquez un e-mail professionnel ou un numéro de téléphone.", "Enter a work email or a phone number."],
    callOkM: ["C'est noté. Un consultant vous écrit à ", "Noted. A consultant writes to you at "],
    callOkP: ["C'est noté. Un consultant vous appelle au ", "Noted. A consultant calls you on "],
    callOkE: [" dans les 30 minutes.", " within 30 minutes."],
    /* the magazine */
    magK: ["Magazine gratuit", "Free magazine"],
    magT: ["Audience First, le magazine.", "Audience First, the magazine."],
    magL: ["Les conversations du podcast avec celles et ceux qui pilotent l'écoute dans leur organisation, et nos lectures de la donnée sociale, réunies en PDF.",
           "The podcast's conversations with the people who run listening inside their organisation, and our reads of social data, together in one PDF."],
    magFirst: ["Prénom", "First name"],
    magMail: ["E-mail professionnel", "Work email"],
    magCo: ["Société", "Company"],
    magB: ["Recevoir le magazine", "Send me the magazine"],
    magC: ["Vos coordonnées servent uniquement à vous envoyer le magazine.", "We use your details only to send you the magazine."],
    magE: ["Indiquez votre prénom, votre société et un e-mail valide.", "Enter your first name, your company and a valid email."],
    magOk: ["C'est noté. Le magazine arrive à ", "Noted. The magazine is on its way to "],
    magOkE: [", en PDF.", ", as a PDF."],
    cover: ["Le magazine", "The magazine"],
    issue: ["N° 1", "Issue 1"],
    coverLine: ["Ce que la conversation dit des marques", "What the conversation says about brands"]
  };

  /* ------------------------------------------------------------ the DOM */
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
      return '<img src="/assets/img/team/morning/' + n + '-face-160.webp" alt="" width="48" height="48" loading="lazy" decoding="async" />';
    }).join("");
  }

  function render() {
    var k = current;
    var head = '<button class="pp__x" type="button" data-close><span aria-hidden="true">×</span><span class="visually-hidden">' + esc(T(C.close)) + "</span></button>";
    if (k === "call") {
      box.className = "pp__box pp__box--call";
      box.innerHTML = head +
        '<div class="pp__body">' +
          '<p class="pp__k"><span class="pp__faces" aria-hidden="true">' + faces() + "</span>" + esc(T(C.callK)) + "</p>" +
          '<h2 class="pp__t" id="pp-title">' + esc(T(C.callT)) + "</h2>" +
          '<p class="pp__l">' + esc(T(C.callL)) + "</p>" +
          (sent.call ? '<p class="pp__done" role="status">' + esc(T(sent.call.k === "phone" ? C.callOkP : C.callOkM)) + "<b>" + esc(sent.call.v) + "</b>" + esc(T(C.callOkE)) + "</p>" :
          '<form class="pp__form" novalidate data-form="call">' +
            '<label class="fld__label" for="pp-contact">' + esc(T(C.callF)) + "</label>" +
            '<div class="pp__row"><input class="fld__input" id="pp-contact" name="contact" type="text" inputmode="email" autocomplete="email" placeholder="' + esc(T(C.callP)) + '" required />' +
            '<button class="btn btn--primary" type="submit">' + esc(T(C.callB)) + ' <span aria-hidden="true">→</span></button></div>' +
            '<p class="fld__error" hidden>' + esc(T(C.callE)) + "</p>" +
            '<p class="pp__promise"><span class="pp__dot" aria-hidden="true"></span>' + esc(T(C.callPr)) + "</p>" +
            '<p class="consent">' + esc(T(C.callC)) + ' <a href="/privacy.html">' + esc(T(C.privacy)) + "</a>.</p>" +
          "</form>") +
        "</div>";
    } else {
      box.className = "pp__box pp__box--mag";
      box.innerHTML = head +
        '<div class="pp__cover" aria-hidden="true"><div class="pp__mag">' +
          '<span class="pp__mag-k">' + esc(T(C.cover)) + "</span>" +
          '<span class="pp__mag-t">Audience<br />First</span>' +
          '<span class="pp__mag-l">' + esc(T(C.coverLine)) + "</span>" +
          '<span class="pp__mag-n">' + esc(T(C.issue)) + " · PDF</span>" +
        "</div></div>" +
        '<div class="pp__body">' +
          '<p class="pp__k">' + esc(T(C.magK)) + "</p>" +
          '<h2 class="pp__t" id="pp-title">' + esc(T(C.magT)) + "</h2>" +
          '<p class="pp__l">' + esc(T(C.magL)) + "</p>" +
          (sent.mag ? '<p class="pp__done" role="status">' + esc(T(C.magOk)) + "<b>" + esc(sent.mag.email) + "</b>" + esc(T(C.magOkE)) + "</p>" :
          '<form class="pp__form" novalidate data-form="mag">' +
            '<div class="pp__two">' +
              '<div><label class="fld__label" for="pp-first">' + esc(T(C.magFirst)) + '</label><input class="fld__input" id="pp-first" name="first" type="text" autocomplete="given-name" required /></div>' +
              '<div><label class="fld__label" for="pp-co">' + esc(T(C.magCo)) + '</label><input class="fld__input" id="pp-co" name="company" type="text" autocomplete="organization" required /></div>' +
            "</div>" +
            '<label class="fld__label" for="pp-mail">' + esc(T(C.magMail)) + "</label>" +
            '<input class="fld__input" id="pp-mail" name="email" type="email" autocomplete="email" required />' +
            '<p class="fld__error" hidden>' + esc(T(C.magE)) + "</p>" +
            '<button class="btn btn--primary pp__wide" type="submit">' + esc(T(C.magB)) + ' <span aria-hidden="true">→</span></button>' +
            '<p class="consent">' + esc(T(C.magC)) + ' <a href="/privacy.html">' + esc(T(C.privacy)) + "</a>.</p>" +
          "</form>") +
        "</div>";
    }
    var lead = window.LicterLead ? window.LicterLead.get() : "";
    var m = box.querySelector('[name="email"], [name="contact"]');
    if (m && lead && EMAIL.test(lead)) m.value = lead;
  }

  /* ----------------------------------------------------- open and close */
  function open(k, auto) {
    if (current) close(true);
    current = k;
    lastFocus = document.activeElement;
    render();
    root.hidden = false;
    html.classList.add("pp-open");
    requestAnimationFrame(function () { root.classList.add("is-open"); });
    var first = box.querySelector("input") || box;
    setTimeout(function () { first.focus({ preventScroll: true }); }, 60);
    if (auto) sset("pp-shown", "1");
  }
  function close(quiet) {
    if (!current) return;
    if (!quiet && !sent[current]) set("pp-closed-" + current, String(Date.now()));
    root.classList.remove("is-open");
    html.classList.remove("pp-open");
    current = null;
    setTimeout(function () { if (!current) root.hidden = true; }, 220);
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
        /* MOCK: send { contact: v, kind } to the CRM */
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
        /* MOCK: send { first, company, email } to the CRM, which emails the PDF */
        if (window.LicterLead) window.LicterLead.set(d.email);
        sent.mag = d;
      }
    }
    if (bad) { bad.setAttribute("aria-invalid", "true"); err.hidden = false; bad.focus(); return; }
    sset("pp-sent", "1");
    render();
    var ok = box.querySelector(".pp__done");
    if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
  });

  /* ------------------------------------------------ the automatic opening */
  var path = location.pathname;
  var formPage = /\/(book-a-meeting|diagnostic|guide|events|event-[a-z0-9-]+)\.html$/.test(path);
  var isHome = document.body.classList.contains("home");
  var wide = window.matchMedia("(min-width: 900px)");
  function recently(k) { var t = +get("pp-closed-" + k); return t && Date.now() - t < 7 * 864e5; }
  function may(k) {
    return wide.matches && !formPage && !current && !sget("pp-shown") && !sget("pp-sent") && !recently(k) &&
      !html.classList.contains("lx-open") && !(document.activeElement && document.activeElement.matches("input, textarea, select"));
  }

  if (!isHome) {
    var callTimer = setTimeout(function () { if (may("call")) open("call", true); }, 40000);
    var onScroll = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && scrollY / h > 0.5) {
        window.removeEventListener("scroll", onScroll);
        clearTimeout(callTimer);
        if (may("call")) open("call", true);
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  var armed = false;
  setTimeout(function () { armed = true; }, 15000);
  document.addEventListener("mouseout", function (e) {
    if (!armed || e.relatedTarget || e.clientY > 8) return;
    if (may("mag")) open("mag", true);
  });

  new MutationObserver(function () { if (current) render(); }).observe(html, { attributes: true, attributeFilter: ["lang"] });

  window.LicterPopups = { open: function (k) { open(k === "mag" ? "mag" : "call", false); } };
})();
