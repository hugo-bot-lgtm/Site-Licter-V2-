/* =========================================================================
   Licter — light / dark theme.

   Loaded in <head>, before the stylesheet paints, so a dark page never
   flashes cream first. The visitor's choice is kept in this browser; with no
   choice made, the page opens in the dark theme. The switch sits next to
   EN / FR in the header.
   ========================================================================= */
(function () {
  "use strict";

  var KEY = "licter-theme";
  var root = document.documentElement;
  var system = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function current() {
    var s = stored();
    if (s === "dark" || s === "light") return s;
    /* dark by default: the light theme is one click away, and remembered */
    return "dark";
  }
  function apply(theme) {
    root.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#13162D" : "#FCF6EF");
    var btn = document.querySelector(".theme__btn");
    if (btn) {
      var dark = theme === "dark";
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
      var fr = root.lang === "fr";
      btn.setAttribute("aria-label", dark
        ? (fr ? "Passer en mode clair" : "Switch to light mode")
        : (fr ? "Passer en mode sombre" : "Switch to dark mode"));
    }
  }

  apply(current());

  /* French is the default language (js/i18n.js). The HTML is written in
     English, so until French is applied the page stays hidden: no English
     flash on first paint. A safety net lifts it anyway after 2.5 s. */
  var lang = null;
  try { lang = localStorage.getItem("licter-lang"); } catch (e) { /* private mode */ }
  if (lang !== "en" && !root.hasAttribute("data-i18n-static")) {
    root.classList.add("i18n-pending");
    setTimeout(function () { root.classList.remove("i18n-pending"); }, 2500);
  }

  if (system && system.addEventListener) {
    system.addEventListener("change", function () { if (!stored()) apply(current()); });
  }

  function build() {
    var host = document.querySelector(".hero__end") || document.querySelector(".hero__top");
    if (!host || host.querySelector(".theme__btn")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme__btn";
    /* a half-filled disc: reads as "contrast", not as sun or moon */
    btn.innerHTML = '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7.25" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 2.75a7.25 7.25 0 0 1 0 14.5z" fill="currentColor"/></svg>';
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      try { localStorage.setItem(KEY, next); } catch (e) { /* private mode */ }
      root.classList.add("theme-switching");
      apply(next);
      setTimeout(function () { root.classList.remove("theme-switching"); }, 400);
    });
    host.insertBefore(btn, host.firstChild);
    apply(current());
    /* the label follows the language switch */
    if (window.MutationObserver) {
      new MutationObserver(function () { apply(current()); })
        .observe(root, { attributes: true, attributeFilter: ["lang"] });
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
