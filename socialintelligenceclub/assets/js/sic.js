/* Social Intelligence Club — comportements de la page */
(function () {
  "use strict";

  /* Les formulaires sont envoyés à la fonction api/sic-contact.js, qui prévient l'équipe par e-mail (Resend). */
  var FORM_ENDPOINT = "/api/sic-contact";

  var root = document.documentElement;
  root.classList.add("js");

  function store(key, val) {
    try {
      if (val === undefined) return window.localStorage.getItem(key);
      window.localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ---------- bandeau événement ---------- */
  var banner = document.querySelector(".banner");
  var BANNER_KEY = "sic-banner-off:" + (banner ? banner.getAttribute("data-event") : "");
  if (banner && store(BANNER_KEY) === "1") root.classList.add("banner-off");

  function syncBannerHeight() {
    var h = banner && !root.classList.contains("banner-off") ? banner.offsetHeight : 0;
    root.style.setProperty("--banner-h", h + "px");
  }
  if (banner) {
    var x = banner.querySelector(".banner__x");
    if (x) x.addEventListener("click", function () {
      root.classList.add("banner-off");
      store(BANNER_KEY, "1");
      syncBannerHeight();
    });
  }
  syncBannerHeight();
  window.addEventListener("resize", syncBannerHeight);

  /* ---------- barre collante ---------- */
  var bar = document.querySelector(".stickybar");
  var top = document.querySelector(".site-top");
  if (bar && top && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      var shown = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
      bar.classList.toggle("is-shown", shown);
      bar.setAttribute("aria-hidden", shown ? "false" : "true");
    }, { threshold: 0 }).observe(top);
  }

  /* ---------- menu mobile ---------- */
  var toggle = document.querySelector(".nav__toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = root.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        root.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && root.classList.contains("nav-open")) {
        root.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* ---------- apparition au scroll ---------- */
  var items = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-in");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el, i) {
      var d = el.getAttribute("data-reveal");
      if (d) el.style.transitionDelay = d + "ms";
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- carrousel « squeeze » : un grand panneau, les trois suivants compressés, le reste en bandes ---------- */
  document.querySelectorAll("[data-squeeze]").forEach(function (root) {
    var viewport = root.querySelector(".sq__viewport");
    var track = root.querySelector(".sq__track");
    var items = Array.prototype.slice.call(track.children);
    var texts = Array.prototype.slice.call(root.querySelectorAll(".sq__text"));
    var bar = root.querySelector(".sq__bar i");
    var scope = root.closest("section") || document;
    var counter = scope.querySelector("[data-sq-current]");
    var GAP = 16, SLAT = 8, SLAT_GAP = 8, WEIGHTS = [0.61, 0.3, 0.15];
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var active = 0, hover = -1;

    function layout() {
      var w = viewport.clientWidth, h = viewport.clientHeight, n = items.length;
      var mobile = w < 640;
      var heroBase = mobile ? w : Math.min(h * 16 / 9, w * 0.56);
      var followers = n - 1 - active;
      var widths = [], margins = [];
      for (var i = 0; i < n; i++) { widths[i] = 0; margins[i] = 0; }

      if (mobile) {
        var peek = followers > 0 ? 18 : 0;
        widths[active] = w - (peek ? peek + 12 : 0);
        if (peek) { widths[active + 1] = peek; margins[active + 1] = 12; }
      } else {
        var n3 = Math.min(3, followers), slats = followers - n3;
        var hero = followers ? heroBase : w;
        var room = Math.max(0, w - hero - n3 * GAP - slats * (SLAT + SLAT_GAP));
        var fw = WEIGHTS.slice(0, n3).map(function (x) { return room * x / 1.06; });
        hero += room - fw.reduce(function (a, b) { return a + b; }, 0);
        var j = hover - active - 1;
        if (j >= 0 && j < n3) {
          var gain = hero * 0.06;
          hero -= gain;
          fw = fw.map(function (x, k) {
            if (k === j) return x;
            gain += x * 0.03;
            return x * 0.97;
          });
          fw[j] += gain;
        }
        widths[active] = hero;
        for (var k = 0; k < n3; k++) { widths[active + 1 + k] = fw[k]; margins[active + 1 + k] = GAP; }
        for (var s = active + 1 + n3; s < n; s++) { widths[s] = SLAT; margins[s] = SLAT_GAP; }
      }

      root.style.setProperty("--sq-hero", Math.round(heroBase) + "px");
      items.forEach(function (it, i) {
        it.style.width = widths[i] + "px";
        it.style.marginLeft = margins[i] + "px";
        it.style.borderRadius = widths[i] && widths[i] < 28 ? "4px" : "";
      });
    }

    function restartBar() {
      if (!bar || reduced) return;
      root.classList.remove("is-auto");
      void bar.offsetWidth;
      root.classList.add("is-auto");
    }

    function go(i, focus) {
      var n = items.length;
      active = (i + n) % n;
      hover = -1;
      items.forEach(function (it, k) {
        var on = k === active;
        it.setAttribute("aria-selected", on ? "true" : "false");
        it.tabIndex = on ? 0 : -1;
      });
      texts.forEach(function (t, k) {
        t.classList.toggle("is-on", k === active);
        if (k === active) t.removeAttribute("aria-hidden"); else t.setAttribute("aria-hidden", "true");
      });
      document.getElementById("sq-panel").setAttribute("aria-labelledby", items[active].id);
      if (counter) counter.textContent = (active < 9 ? "0" : "") + (active + 1);
      layout();
      restartBar();
      if (focus) items[active].focus({ preventScroll: true });
    }

    items.forEach(function (it, i) {
      it.addEventListener("click", function () { if (i !== active) go(i); });
      it.addEventListener("mouseenter", function () { if (i > active) { hover = i; layout(); } });
      it.addEventListener("mouseleave", function () { if (hover === i) { hover = -1; layout(); } });
    });
    track.addEventListener("keydown", function (e) {
      var map = { ArrowRight: active + 1, ArrowLeft: active - 1, Home: 0, End: items.length - 1 };
      if (!(e.key in map)) return;
      e.preventDefault();
      go(map[e.key], true);
    });
    var prev = scope.querySelector("[data-sq-prev]"), next = scope.querySelector("[data-sq-next]");
    if (prev) prev.addEventListener("click", function () { go(active - 1); });
    if (next) next.addEventListener("click", function () { go(active + 1); });

    /* lecture automatique : la barre de progression pilote le passage au suivant */
    var pauses = {};
    function pause(reason, on) {
      if (on) pauses[reason] = true; else delete pauses[reason];
      root.classList.toggle("is-paused", Object.keys(pauses).length > 0);
    }
    if (bar && !reduced) {
      bar.addEventListener("animationend", function () { go(active + 1); });
      root.addEventListener("mouseenter", function () { pause("hover", true); });
      root.addEventListener("mouseleave", function () { pause("hover", false); });
      root.addEventListener("focusin", function () { pause("focus", true); });
      root.addEventListener("focusout", function (e) { if (!root.contains(e.relatedTarget)) pause("focus", false); });
      document.addEventListener("visibilitychange", function () { pause("hidden", document.hidden); });
      if ("IntersectionObserver" in window) {
        pause("offscreen", true);
        new IntersectionObserver(function (en) { pause("offscreen", !en[0].isIntersecting); }, { threshold: 0.35 }).observe(root);
      }
    }

    if ("ResizeObserver" in window) new ResizeObserver(layout).observe(viewport);
    else window.addEventListener("resize", layout);
    go(0);
    requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add("is-ready"); }); });
  });

  /* ---------- pop-up d'arrivée (étude 100 dircom) ---------- */
  var pp = document.getElementById("pp-etude");
  if (pp && typeof pp.showModal === "function") {
    pp.querySelectorAll("[data-pp-close]").forEach(function (b) {
      b.addEventListener("click", function () { pp.close(); });
    });
    pp.addEventListener("click", function (e) { if (e.target === pp) pp.close(); });
    /* à chaque arrivée sur la page, sauf retour depuis une autre page du site ou formulaire déjà envoyé */
    var internal = false;
    try { internal = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
    if (store("sic-pp-done") !== "1" && !internal) {
      setTimeout(function () {
        if (document.querySelector("dialog[open]")) return;
        pp.showModal();
      }, 1200);
    }
  }

  /* ---------- formulaires ---------- */
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  document.querySelectorAll("form.form").forEach(function (form) {
    var card = form.closest(".form-card, .pp");
    var error = form.querySelector(".fld__error");
    var fields = form.querySelectorAll("[required]");

    fields.forEach(function (f) {
      f.addEventListener("input", function () {
        f.setAttribute("aria-invalid", "false");
        if (error) error.hidden = true;
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      fields.forEach(function (f) {
        var v = (f.value || "").trim();
        var ok = f.type === "email" ? EMAIL.test(v) : v.length > 1;
        f.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !firstBad) firstBad = f;
      });
      if (firstBad) {
        if (error) error.hidden = false;
        firstBad.focus();
        return;
      }

      var data = { form: form.getAttribute("data-form"), page: location.href };
      new FormData(form).forEach(function (v, k) { data[k] = String(v).trim(); });

      var btn = form.querySelector("button[type=submit]");
      function done() {
        if (card) card.classList.add("is-sent");
        if (data.form === "etude-100-dircom") store("sic-pp-done", "1");
        var h = card && card.querySelector(".form-done h3");
        if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
      }

      if (!FORM_ENDPOINT) { done(); return; }
      if (btn) btn.disabled = true;
      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        done();
      }).catch(function () {
        if (btn) btn.disabled = false;
        if (error) {
          error.textContent = "L'envoi n'a pas abouti. Réessayez dans un instant.";
          error.hidden = false;
        }
      });
    });
  });
})();
