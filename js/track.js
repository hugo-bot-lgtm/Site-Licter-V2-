/* =========================================================================
   Audience measurement: one call, every tool.

   window.LicterTrack(name, props) records what the visitors do with the
   lead magnets. Each event goes to:
   - window.dataLayer (Google Tag Manager reads it as is);
   - Plausible, if its script is on the page (window.plausible);
   - Google Analytics 4, if gtag is on the page (window.gtag).

   Nothing third-party is loaded by default: no cookie, no banner needed.
   To switch Plausible on (no cookie, no consent banner required), set
   PLAUSIBLE_DOMAIN below to the site's domain. GA4 or GTM need a consent
   banner first (CNIL): add them only with one.

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
