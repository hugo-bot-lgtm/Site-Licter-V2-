/* =========================================================================
   Client voices — the rotating wall on clients.html

   The pool is a snapshot of the long-form episodes on the Licter channel
   (youtube.com/@audience_first). It is baked in on purpose: the site has no
   backend, YouTube's RSS feed sends no CORS header, and the Data API would
   put a key in public JavaScript for a list that changes once a week. To
   refresh it, run tools/harvest-voices.md and paste the result below.

   Only brand and institution interviews are in the pool: the channel also
   carries Shorts and off-topic clips, and a wall titled "they tell it better
   than we do" cannot roll a two-minute short about fighter jets.
   ========================================================================= */

window.LicterVoices = [
  { id: "1PXRd4_JgEc", brand: "Groupe SEB",        who: "Hélène Classine",            time: "1:03:49",
    quote: "It is not a study if there is no action plan." },
  { id: "cnwA-t0Vqk4", brand: "Dassault Systèmes", who: "Jean-Stéphane Bou",          time: "1:00:32",
    quote: "Social media helps us build better products." },
  { id: "l-OevQ4q8js", brand: "Paris 2024",        who: "C. Legall",                  time: "55:08",
    quote: "Millions of tweets to handle, live." },
  { id: "z3EkLWjQXMQ", brand: "SNCF",              who: "M. Fleurbaey",               time: "56:29",
    quote: "The social room changed the way we work." },
  { id: "UElJ_Pdd0wo", brand: "Orange",            who: "B. Hoang",                   time: "58:39",
    quote: "Every trend now starts on TikTok." },
  { id: "moW2HYtTor8", brand: "L'Oréal",           who: "C. Besson",                  time: "51:29",
    quote: "The internet, to capture the consumer's voice." },
  { id: "0HfWWSB0v78", brand: "AXA",               who: "Z. Gebran",                  time: "54:27",
    quote: "What media diversity actually buys you." },
  { id: "NwA84KwnDKU", brand: "Kantar",            who: "G. Lefloch",                 time: "53:14",
    quote: "Consumption has become an act of activism." },
  { id: "CEFJc7tP4hU", brand: "LVMH",              who: "Clara Mallien",              time: "41:22",
    quote: "600k followers in two years." },
  { id: "JSI5LBi8K-g", brand: "Ville de Paris",    who: "B. Tailly & F. Lootvoet",    time: "51:52",
    quote: "Can you capture the voice of Parisians?" },
  { id: "yEe6j9oLmQY", brand: "Transat Café l'Or", who: "Antoine Robin",              time: "53:28",
    quote: "I have lived through two revolutions." },
  { id: "EOkpQ_v-3kw", brand: "France Digitale",   who: "A. Labarrière",              time: "45:24",
    quote: "The best money is your customers' money." }
];

(function () {
  var pool = window.LicterVoices || [];
  var reels = document.querySelector(".reels");
  if (!reels || pool.length < 4) return;

  var cards = Array.prototype.slice.call(reels.querySelectorAll(".reel"));
  if (!cards.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  /* below this the three cards stack, so only one is on screen at a time and
     swapping it would change what someone is reading under their thumb */
  var narrow = window.matchMedia("(max-width: 860px)");
  function still() { return reduced.matches || narrow.matches; }
  var EVERY = 7000;          /* one card changes, not all three */
  var FADE = 260;

  /* the three already in the markup stay first: they are the strongest, and
     they are what a no-JS visitor sees anyway */
  var shown = cards.map(function (card) {
    var m = (card.getAttribute("href") || "").match(/v=([\w-]{11})/);
    return m ? m[1] : null;
  });

  /* the three in the markup start on hqdefault: upgrade them too */
  cards.forEach(function (card, i) {
    var img = card.querySelector(".reel__shot img");
    if (img && shown[i]) { img.dataset.id = shown[i]; setThumb(img, shown[i]); }
  });

  var queue = [];
  function refill() {
    var rest = pool.filter(function (v) { return shown.indexOf(v.id) === -1; });
    for (var i = rest.length - 1; i > 0; i--) {         /* Fisher-Yates */
      var j = (Math.random() * (i + 1)) | 0;
      var t = rest[i]; rest[i] = rest[j]; rest[j] = t;
    }
    queue = rest;
  }
  refill();

  /* YouTube answers 200 with a grey 120x90 placeholder when maxresdefault does
     not exist, so onerror never fires: show hqdefault (which always exists and
     crops to exactly the 16:9 frame) and upgrade only once maxres proves real */
  function thumb(id) { return "https://i.ytimg.com/vi/" + id + "/hqdefault.jpg"; }

  function setThumb(img, id) {
    img.src = thumb(id);
    var probe = new Image();
    probe.onload = function () {
      if (probe.naturalWidth > 320 && img.dataset.id === id) img.src = probe.src;
    };
    probe.src = "https://i.ytimg.com/vi/" + id + "/maxresdefault.jpg";
  }

  function paint(card, v) {
    card.setAttribute("href", "https://www.youtube.com/watch?v=" + v.id);
    var img = card.querySelector(".reel__shot img");
    img.dataset.id = v.id;
    setThumb(img, v.id);
    card.querySelector(".reel__time").textContent = v.time;
    card.querySelector(".reel__quote").textContent = "“" + v.quote + "”";
    card.querySelector(".reel__brand").textContent = v.brand;
    card.querySelector(".reel__who").textContent = v.who;
  }

  var slot = 0;

  function swap() {
    if (!queue.length) refill();
    if (!queue.length) return;

    var card = cards[slot % cards.length];
    var next = queue.shift();
    slot++;

    /* load the frame before showing it, so the card never blinks empty */
    var pre = new Image();
    var done = false;
    function go() {
      if (done) return;
      done = true;
      card.classList.add("is-swapping");
      setTimeout(function () {
        shown[cards.indexOf(card)] = next.id;
        paint(card, next);
        card.classList.remove("is-swapping");
      }, FADE);
    }
    pre.onload = pre.onerror = go;
    pre.src = thumb(next.id);
    setTimeout(go, 1200);                 /* never wait on a slow thumbnail */
  }

  /* it only runs while it is worth running: on screen, tab in front, and the
     visitor not reading or hovering the cards */
  var visible = false, held = false, timer = null;

  function tick() {
    clearTimeout(timer);
    if (!visible || held || document.hidden || still() || reels.classList.contains("has-player")) return;
    timer = setTimeout(function () { swap(); tick(); }, EVERY);
  }

  reels.addEventListener("pointerenter", function () { held = true; tick(); });
  reels.addEventListener("pointerleave", function () { held = false; tick(); });
  reels.addEventListener("focusin", function () { held = true; tick(); });
  reels.addEventListener("focusout", function () { held = false; tick(); });
  document.addEventListener("visibilitychange", tick);

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible = e.isIntersecting; });
      tick();
    }, { threshold: 0.2 }).observe(reels);
  } else {
    visible = true;
    tick();
  }

  /* no movement here, but still variety: a different three on each visit */
  if (still()) {
    var picks = pool.slice();
    for (var i = picks.length - 1; i > 0; i--) {
      var j = (Math.random() * (i + 1)) | 0;
      var t = picks[i]; picks[i] = picks[j]; picks[j] = t;
    }
    cards.forEach(function (card, i) {
      shown[i] = picks[i].id;
      paint(card, picks[i]);
    });
    refill();
  }

  /* a phone turned sideways, or a window dragged wider, gets the rotation */
  if (narrow.addEventListener) narrow.addEventListener("change", tick);
})();

/* =========================================================================
   Play in place
   A click swaps the thumbnail for the player, on the page. The card stops
   being a link while it plays, and the wall stops rotating. A new-tab or
   modified click still goes to YouTube, as a link should.
   ========================================================================= */
(function () {
  var reels = document.querySelector(".reels");
  if (!reels) return;

  function restore() {
    var playing = reels.querySelector(".reel.is-playing");
    if (playing && playing._link) playing.parentNode.replaceChild(playing._link, playing);
  }

  reels.addEventListener("click", function (e) {
    var card = e.target.closest ? e.target.closest("a.reel") : null;
    if (!card || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var m = (card.getAttribute("href") || "").match(/v=([\w-]{11})/);
    if (!m) return;
    e.preventDefault();
    restore();

    var box = document.createElement("div");
    box.className = card.className + " is-playing";
    box.setAttribute("style", card.getAttribute("style") || "");
    box.innerHTML = card.innerHTML;
    box._link = card;

    var brand = card.querySelector(".reel__brand");
    var frame = document.createElement("iframe");
    frame.src = "https://www.youtube-nocookie.com/embed/" + m[1] + "?autoplay=1&rel=0&modestbranding=1";
    frame.title = "Audience First interview" + (brand ? ", " + brand.textContent : "");
    frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    frame.allowFullscreen = true;
    var shot = box.querySelector(".reel__shot");
    shot.innerHTML = "";
    shot.appendChild(frame);

    card.parentNode.replaceChild(box, card);
    reels.classList.add("has-player");
    frame.focus();
  });
})();
