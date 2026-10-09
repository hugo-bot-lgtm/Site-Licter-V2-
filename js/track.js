/* =========================================================================
   Audience measurement: one call, every tool.

   window.LicterTrack(name, props) records what the visitors do with the
   lead magnets. Each event goes to:
   - window.dataLayer (Google Tag Manager reads it as is);
   - Plausible, if its script is on the page (window.plausible);
   - Google Analytics 4, if gtag is on the page (window.gtag).

   Google Analytics 4 (GA4_ID below) loads only after the visitor accepts
   the cookie banner (see "consent and GA4"). Plausible, cookie-free, needs
   no banner: set PLAUSIBLE_DOMAIN to switch it on.

   Events sent by the site:
   popup_open      { popup: "mag" | "call", auto: true | false }
   popup_close     { popup }            closed without sending
   popup_submit    { popup }
   cta_click       { where: section id }   any "Talk to a consultant"
   bar_click       { target: "cta" | "chat" | "mag" }   the compact bar
   chat_open       {}
   quiz_complete   { score }
   quiz_email      {}
   form_submit     { form: "callback" | "guide" | "diagnostic" | "booking" | "event" | … }

   Loaded by js/ui.js on every page, before the popups and the chat.
   ========================================================================= */
(function () {
  "use strict";
  if (window.LicterTrack) return;

  var PLAUSIBLE_DOMAIN = ""; /* e.g. "licter.com" */

  if (PLAUSIBLE_DOMAIN) {
    window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); };
    var s = document.createElement("script");
    s.defer = true;
    s.setAttribute("data-domain", PLAUSIBLE_DOMAIN);
    s.src = "https://plausible.io/js/script.js";
    document.head.appendChild(s);
  }

  window.dataLayer = window.dataLayer || [];

  /* ------------------------------------------------ consent and GA4
     Google Analytics 4 sets cookies, so it waits for the visitor's consent
     (CNIL): nothing from Google loads, and no cookie is set, until
     "Accept". The choice is kept six months, then asked again; it can be
     changed at any time from "Cookies" in the footer. Until a choice is
     made, the magazine popup waits (js/popups.js listens to the
     "licter:consent" event). */
  var GA4_ID = "G-FMNYXB14XW";
  var KEY = "licter-consent", SIX_MONTHS = 182 * 864e5;
  var html = document.documentElement;
  function fr() { return (html.lang || "fr").slice(0, 2) === "fr"; }
  function stored() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY) || "null");
      return c && (c.v === "granted" || c.v === "denied") && Date.now() - c.t < SIX_MONTHS ? c.v : null;
    } catch (e) { return null; }
  }
  function save(v) { try { localStorage.setItem(KEY, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {} }
  var gaLoaded = false;
  function loadGA() {
    /* only on the real site: local tests and Vercel previews never reach the GA4 property */
    if (gaLoaded || !GA4_ID || !/(^|\.)licter\.com$/.test(location.hostname)) return;
    gaLoaded = true;
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "granted" });
    window.gtag("js", new Date());
    window.gtag("config", GA4_ID, { cookie_expires: 13 * 30 * 24 * 3600, cookie_update: false });   /* 13 months at most from consent, not renewed on each visit */   /* 13 months at most (CNIL) */
    var g = document.createElement("script");
    g.async = true;
    g.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    document.head.appendChild(g);
  }
  function dropGA() {
    if (typeof window.gtag === "function") window.gtag("consent", "update", { analytics_storage: "denied" });
    /* the cookies GA set, on this host and on the parent domain */
    document.cookie.split(";").forEach(function (c) {
      var n = c.split("=")[0].trim();
      if (!/^_ga(_|$)/.test(n)) return;
      var host = location.hostname, dom = host.replace(/^www\./, "");
      ["", "; domain=" + host, "; domain=." + dom].forEach(function (d) {
        document.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
      });
    });
  }
  var bar = null;
  function decide(v) {
    save(v);
    if (v === "granted") loadGA(); else dropGA();
    if (bar) { bar.remove(); bar = null; }
    html.classList.remove("cc-open");
    try { document.dispatchEvent(new CustomEvent("licter:consent", { detail: v })); } catch (e) {}
  }
  function ask() {
    if (bar) return;
    var priv = fr() ? "/fr/confidentialite/#cookies" : "/privacy.html#cookies";
    bar = document.createElement("div");
    bar.className = "cc";
    bar.setAttribute("data-nosnippet", "");   /* never part of a search snippet */
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-live", "polite");
    bar.setAttribute("aria-label", fr() ? "Cookies de mesure d'audience" : "Audience measurement cookies");
    bar.innerHTML = '<p class="cc__t">' + (fr()
        ? "Mesure d'audience Google Analytics\u00a0: cookies déposés seulement si vous acceptez."
        : "Google Analytics audience measurement: cookies are set only if you accept.") +
      ' <a href="' + priv + '">' + (fr() ? "Politique de cookies" : "Cookie policy") + "</a></p>" +
      '<div class="cc__b"><button class="cc__no" type="button">' + (fr() ? "Refuser" : "Decline") + '</button>' +
      '<button class="cc__yes" type="button">' + (fr() ? "Accepter" : "Accept") + "</button></div>";
    bar.querySelector(".cc__no").addEventListener("click", function () { decide("denied"); });
    bar.querySelector(".cc__yes").addEventListener("click", function () { decide("granted"); });
    document.body.appendChild(bar);
    html.classList.add("cc-open");
  }
  /* "Cookies" in the footer, next to the privacy link: the choice again */
  function footLink() {
    var priv = document.querySelector('.site-foot__legal a[href*="privacy"], .site-foot__legal a[href*="confidentialite"]');
    if (!priv || document.querySelector(".cc-manage")) return;
    var b = document.createElement("button");
    b.type = "button"; b.className = "cc-manage";
    b.textContent = "Cookies";
    b.addEventListener("click", function () { try { localStorage.removeItem(KEY); } catch (e) {} ask(); });
    priv.after(document.createTextNode(" · "), b);
  }
  window.LicterConsent = { state: stored, decided: function () { return !!stored(); }, ask: ask };
  function start() {
    footLink();
    var c = stored();
    /* a choice older than six months: asked again, and the old GA cookies go */
    try { if (!c && localStorage.getItem(KEY)) { localStorage.removeItem(KEY); dropGA(); } } catch (e) {}
    if (c === "granted") loadGA();
    else if (!c) ask();
  }
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);

  /* ------------------------------------------------ the forms
     Every form sends what the visitor typed to /api/lead (Vercel function),
     which emails the team through Resend. Fire and forget: the page shows its
     confirmation whatever happens, and a failure is only logged.
     LicterSend(action, detail, fields): fields is { label: value } or a form,
     whose named fields are read with their visible labels. */
  function labelOf(el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]');
    var box = l || el.closest("label");
    var txt = box ? (box.querySelector("span") || box).textContent : "";
    txt = (txt || el.getAttribute("aria-label") || el.getAttribute("placeholder") || el.name || "").replace(/\s+/g, " ").trim();
    return txt.replace(/\s*\(.*?\)\s*$/, "") || el.name;
  }
  function read(form) {
    var out = {};
    Array.prototype.forEach.call(form.querySelectorAll("input[name], select[name], textarea[name]"), function (el) {
      if (el.type === "hidden" || el.type === "submit" || ((el.type === "radio" || el.type === "checkbox") && !el.checked)) return;
      var v = el.tagName === "SELECT" ? (el.options[el.selectedIndex] || {}).text || "" : el.value;
      if (v && String(v).trim()) out[labelOf(el)] = String(v).trim();
    });
    return out;
  }
  /* the page has already thanked the visitor: if the request did not reach
     the team, say so, and offer to send it by e-mail instead */
  function failed(data) {
    var box = document.getElementById("lead-failed");
    if (box) box.remove();
    var lines = Object.keys(data).map(function (k) { return k + " : " + data[k]; }).join("\n");
    var mail = "mailto:contact@licter.com?subject=" + encodeURIComponent(fr() ? "Demande depuis licter.com" : "Request from licter.com") +
      "&body=" + encodeURIComponent(lines + "\n\n" + location.href);
    box = document.createElement("div");
    box.id = "lead-failed";
    box.setAttribute("role", "alert");
    box.style.cssText = "position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:520px;margin:0 auto;" +
      "background:#13162D;color:#FCF6EF;border:1px solid #EAA93D;border-radius:14px;padding:16px 48px 16px 18px;" +
      "font:15px/1.5 Raleway,system-ui,sans-serif;box-shadow:0 12px 40px rgba(0,0,0,.35)";
    box.innerHTML = "<b>" + (fr() ? "Votre demande n’est pas partie." : "Your request did not go through.") + "</b> " +
      (fr() ? "Le réseau l’a bloquée. " : "The network blocked it. ") +
      "<a style=\"color:#EAA93D;font-weight:700\" href=\"" + mail + "\">" +
      (fr() ? "Envoyez-la par e-mail" : "Send it by e-mail") + "</a> " +
      (fr() ? "à contact@licter.com, elle est déjà rédigée." : "to contact@licter.com, it is already written.") +
      "<button type=\"button\" aria-label=\"" + (fr() ? "Fermer" : "Close") + "\" style=\"position:absolute;top:8px;right:8px;width:36px;height:36px;" +
      "border:0;background:none;color:inherit;font-size:22px;cursor:pointer\">×</button>";
    box.querySelector("button").addEventListener("click", function () { box.remove(); });
    document.body.appendChild(box);
  }
  window.LicterSend = function (action, detail, fields) {
    try {
      var data = fields && fields.tagName === "FORM" ? read(fields) : (fields || {});
      var body = JSON.stringify({ action: action, detail: detail || "", title: document.title, page: location.href, lang: fr() ? "fr" : "en", fields: data });
      var post = function () {
        return fetch("/api/lead", {
          method: "POST", keepalive: true,
          headers: { "Content-Type": "application/json", "X-Licter-Form": "1" }, body: body
        }).then(function (r) { if (!r.ok) throw new Error("status " + r.status); });
      };
      /* one more try after a short wait, then the visitor is told */
      post().catch(function () {
        return new Promise(function (ok) { setTimeout(ok, 1500); }).then(post);
      }).catch(function (e) { console.warn("form not sent", e); failed(data); });
    } catch (e) { /* a form never breaks the page */ }
  };
  /* the title of the section a form sits in: says which form it was */
  window.LicterSend.where = function (el) {
    var sec = el.closest("section, aside, footer, .pp, .lx, [role=dialog]") || document.body;
    var h = sec.querySelector("h1, h2, h3, .ucp__cta-t, .nl__title");
    return h ? h.textContent.replace(/\s+/g, " ").trim() : "";
  };

  window.LicterTrack = function (name, props) {
    props = props || {};
    var page = location.pathname;
    try {
      window.dataLayer.push(Object.assign({ event: name, page: page }, props));
      if (typeof window.plausible === "function") window.plausible(name, { props: props });
      if (typeof window.gtag === "function") window.gtag("event", name, props);
    } catch (e) { /* measuring never breaks the page */ }
  };

  /* the compact bar: which of its three buttons is used */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".stickybar a, .stickybar button");
    if (!b) return;
    var target = b.classList.contains("stickybar__chat") ? "chat" : b.classList.contains("stickybar__mag") ? "mag" : b.classList.contains("stickybar__cta") ? "cta" : "logo";
    window.LicterTrack("bar_click", { target: target });
  }, true);
})();
