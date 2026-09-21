# Refreshing the client-voices pool

`js/voices.js` holds a hand-checked list of episodes from the Licter channel.
It is a snapshot, not a live feed — see the note at the top of that file for
why. When new interviews go up, refresh it like this.

1. Open <https://www.youtube.com/@audience_first/videos> in a browser.
   The **Videos** tab holds the long-form episodes only (~45). The other
   ~380 items on the channel are Shorts and live in their own tab: they must
   not end up in the pool.

2. Scroll to the bottom so every card has been rendered at least once, then
   run this in the console. The grid recycles its nodes, so it accumulates
   while scrolling instead of reading the page once at the end:

   ```js
   const seen = new Map();
   const grab = () => document.querySelectorAll('ytd-rich-item-renderer').forEach(r => {
     const a = r.querySelector('a[href*="watch?v="]');
     const m = a && a.getAttribute('href').match(/v=([\w-]{11})/);
     if (!m || seen.has(m[1])) return;
     const t = r.querySelector('a[title]');
     const b = r.querySelector('yt-thumbnail-bottom-overlay-view-model');
     seen.set(m[1], [m[1], t ? t.getAttribute('title') : '', b ? b.innerText.trim() : '']);
   });
   grab();
   for (let i = 0; i < 60; i++) { window.scrollBy(0, 2400); await new Promise(r => setTimeout(r, 650)); grab(); }
   copy([...seen.values()].map(v => v.join(' | ')).join('\n'));
   ```

3. Keep only **brand and institution interviews**. The channel also carries
   webinars, masterclasses, podcast trailers and political interviews; none of
   those belong under a heading that says clients tell it better than we do.

4. For each kept episode write one line in `js/voices.js`: `id`, `brand`,
   `who` (only what the title or description actually states — do not invent a
   name), `time` (the duration YouTube shows) and `quote` (a faithful English
   rendering of the French quote burnt into the thumbnail).

5. Check the thumbnail. `maxresdefault.jpg` does not exist for every video, and
   YouTube answers those with a grey 120×90 placeholder **and a 200 status**,
   so a plain `onerror` will not catch it. `voices.js` already handles this by
   starting on `hqdefault.jpg` and upgrading only when maxres proves real —
   nothing to do, but do not "simplify" it back.

The first three entries are the ones hard-coded in `clients.html`, so they are
what a visitor without JavaScript sees. Keep the strongest three there.
