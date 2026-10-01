/* =========================================================================
   Licter — EN / FR switch.

   The site is written in English. Rather than maintaining a second set of
   HTML files, translation is applied at runtime: a dictionary keyed by the
   English string, walked over the text nodes of the page. Anything absent
   from the dictionary stays in English, so a partial dictionary degrades
   gracefully instead of breaking the page.

   A MutationObserver re-applies it to anything js/ui.js renders afterwards
   (menus, console, questions, story cards).
   ========================================================================= */
(function () {
  "use strict";

  var FR = window.LicterFR || null;
  /* The dictionary is loaded by the page itself, before this script, now that
     French is the default. If it is missing, it is fetched from this script's
     own URL, with the file name swapped. */
  var SELF = document.currentScript && document.currentScript.src;
  function loadFR(done) {
    if (FR) { done(); return; }
    var tag = document.createElement("script");
    tag.src = SELF ? SELF.replace(/i18n\.js/, "fr.js") : "js/fr.js";
    tag.onload = function () { FR = window.LicterFR || {}; done(); };
    tag.onerror = function () { FR = {}; done(); };
    document.head.appendChild(tag);
  }
  var STORE = "licter-lang";
  var current = "en";
  var observer = null;

  /* ---------------------------------------------------------------- walk */

  var SKIP = { SCRIPT: 1, STYLE: 1, CANVAS: 1, NOSCRIPT: 1, SVG: 1 };

  function translateTree(root, dict) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = node.parentNode;
        /* nodeName is "svg" in lower case for SVG elements, so match on the
           upper-cased form or the chart's month labels get walked too */
        if (!p || SKIP[p.nodeName.toUpperCase()]) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var node, hits = 0;
    while ((node = walker.nextNode())) {
      var raw = node.nodeValue;
      var key = raw.replace(/\s+/g, " ").trim();
      var hit = dict[key];
      if (!hit) continue;
      /* The key is the whitespace-collapsed form, so it cannot be found in a
         multi-line source string: replace the node value outright and keep
         only its leading and trailing spaces. */
      node.nodeValue = raw.match(/^\s*/)[0] + hit + raw.match(/\s*$/)[0];
      hits++;
    }

    /* the home has a French page of its own */
    if (dict === FR) {
      Array.prototype.forEach.call(root.querySelectorAll ? root.querySelectorAll('a[href="index.html"], a[href="/index.html"], a[href="/"], a[href^="index.html#"], a[href^="/index.html#"], a[href^="/#"]') : [], function (a) {
        var h = a.getAttribute("href"), hash = h.indexOf("#") >= 0 ? h.slice(h.indexOf("#")) : "";
        if (!(document.getElementById("content") && hash && location.pathname.replace(/index\.html$/, "") === "/fr/")) a.setAttribute("href", "/fr/" + hash);
      });
    }

    /* attributes that are read by users too */
    Array.prototype.forEach.call(root.querySelectorAll("[placeholder]"), function (el) {
      var k = el.getAttribute("placeholder").trim();
      if (dict[k]) el.setAttribute("placeholder", dict[k]);
    });
    Array.prototype.forEach.call(root.querySelectorAll("[aria-label]"), function (el) {
      var k = el.getAttribute("aria-label").trim();
      if (dict[k]) el.setAttribute("aria-label", dict[k]);
    });
    return hits;
  }

  /* --------------------------------------------------------------- apply */

  /* js/theme.js hides the page until French is on it: lift that once done */
  function reveal() { document.documentElement.classList.remove("i18n-pending"); }

  function apply(lang) {
    if (lang === "fr" && current !== "fr") {
      if (!FR) { loadFR(function () { apply("fr"); }); return; }
      translateTree(document.body, FR);
      if (FR[document.title]) document.title = FR[document.title];
      document.documentElement.lang = "fr";
      current = "fr";
      watch();
      reveal();
    } else if (lang === "en" && current !== "en") {
      /* going back to English: the source of truth is the HTML file itself */
      unwatch();
      document.documentElement.lang = "en";
      current = "en";
      location.reload();
      return;
    }
    mark();
  }

  function watch() {
    if (observer || !window.MutationObserver) return;

    /* Two things went wrong here before. The handler dropped any batch that
       arrived while one was pending, so a second render in the same frame was
       lost outright — and it waited on requestAnimationFrame, which never
       fires in a background tab, so the queue jammed for good. Records are
       now queued rather than discarded, and flushed on a timeout. */
    var queue = [], scheduled = false;

    function flush() {
      scheduled = false;
      var batch = queue;
      queue = [];
      batch.forEach(function (n) {
        if (n.nodeType === 1) {
          translateTree(n, FR);
        } else if (n.nodeType === 3) {
          var k = (n.nodeValue || "").replace(/\s+/g, " ").trim();
          if (FR[k]) n.nodeValue = FR[k];
        }
      });
    }

    observer = new MutationObserver(function (records) {
      records.forEach(function (r) {
        Array.prototype.forEach.call(r.addedNodes, function (n) { queue.push(n); });
      });
      if (scheduled || !queue.length) return;
      scheduled = true;
      setTimeout(flush, 0);
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  function unwatch() {
    if (!observer) return;
    observer.disconnect();
    observer = null;
  }

  /* -------------------------------------------------------------- switch */

  function mark() {
    Array.prototype.forEach.call(document.querySelectorAll(".lang__btn"), function (b) {
      var on = b.dataset.lang === current;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function build() {
    var host = document.querySelector(".hero__end") || document.querySelector(".hero__top") || document.querySelector(".site-head .shell");
    if (!host) return;

    var box = document.createElement("div");
    box.className = "lang";
    box.setAttribute("role", "group");
    box.setAttribute("aria-label", "Language");
    box.innerHTML =
      '<button class="lang__btn" type="button" data-lang="en" aria-pressed="true">EN</button>' +
      '<span class="lang__sep" aria-hidden="true"></span>' +
      '<button class="lang__btn" type="button" data-lang="fr" aria-pressed="false">FR</button>';
    host.appendChild(box);

    box.addEventListener("click", function (e) {
      var btn = e.target.closest(".lang__btn");
      if (!btn) return;
      var lang = btn.dataset.lang;
      try { localStorage.setItem(STORE, lang); } catch (err) { /* private mode */ }
      /* a page written in both languages: go to its twin */
      if (STATIC) {
        var alt = html.getAttribute("data-alt-" + lang);
        if (lang !== current && alt) location.href = alt + location.hash;
        return;
      }
      apply(lang);
    });
  }

  /* French by default: the site speaks to French organisations first.
     English is one click away, and remembered once chosen. */
  var saved = "fr";
  try { saved = localStorage.getItem(STORE) || "fr"; } catch (e) { /* private mode */ }

  /* Pages generated in both languages (the use-case pages, see
     tools/build-usecases.py) carry their text in the HTML and point to their
     twin; the dictionary only covers what the scripts render on them. */
  var html = document.documentElement;
  var STATIC = html.hasAttribute("data-i18n-static");

  /* the other pages link to the use-case pages in French; in English, to
     their English twins */
  function localLinks(lang) {
    Array.prototype.forEach.call(document.querySelectorAll("a[data-en]"), function (a) {
      if (!a.hasAttribute("data-fr")) a.setAttribute("data-fr", a.getAttribute("href"));
      a.setAttribute("href", a.getAttribute(lang === "en" ? "data-en" : "data-fr"));
    });
  }

  function init() {
    build();
    if (STATIC) {
      /* a page written in a language sets it for the rest of the visit,
         unless the visitor has already chosen */
      try { if (!localStorage.getItem(STORE)) localStorage.setItem(STORE, html.lang); } catch (e) { /* private mode */ }
      if (html.lang === "fr") {
        FR = window.LicterFR || FR || {};
        translateTree(document.body, FR);
        current = "fr";
        watch();
      } else {
        current = "en";
      }
      mark(); reveal();
      return;
    }
    if (saved === "fr") apply("fr"); else { localLinks("en"); mark(); reveal(); }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
