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
        ? "Nous mesurons l'audience du site avec Google Analytics, pour savoir quelles pages sont utiles. Ses cookies ne sont déposés que si vous acceptez."
        : "We measure the site's audience with Google Analytics, to learn which pages are useful. Its cookies are set only if you accept.") +
      ' <a href="' + priv + '">' + (fr() ? "Lire la politique de cookies" : "Read the cookie policy") + "</a></p>" +
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
