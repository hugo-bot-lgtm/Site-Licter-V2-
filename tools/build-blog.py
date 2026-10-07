#!/usr/bin/env python3
"""Builds the blog: blog.html and the nine article-*.html pages.

The articles live in tools/blog_articles.json (thread, title, lead, date,
read time, author, the prose and the related use cases). Each one gets a
generative cover drawn from its slug: the same article always gets the same
picture, and each thread has its own motif (signal lines for foresight, a
radar for listening, two clouds for insights, a network for influence).
The pictures are drawn, never data.

Head, header and footer are kept from each file; only <main> is rewritten.
The text is in English; js/fr.js translates the blog page at runtime (the
articles carry their "English only" note).

    python3 tools/build-blog.py
"""
import hashlib, html, json, math, pathlib, random, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTS = json.loads((ROOT / "tools" / "blog_articles.json").read_text())
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
for x in ARTS:
    d, m, y = x["date"].split()
    x["key"] = (int(y), MONTHS.index(m), int(d))
    x["slug"] = x["file"][len("article-"):-len(".html")]
ARTS.sort(key=lambda x: x["key"], reverse=True)

THREADS = [("foresight", "SOCIAL DATA & FORESIGHT", "Social data & foresight", "Reading weak signals before they become trends: what actually predicts a shift, and what only looks like it does."),
           ("listening", "MONITORING & SOCIAL LISTENING", "Monitoring & social listening", "How the practice is changing: alerting thresholds, language coverage, and what a platform cannot do on its own."),
           ("insights", "CONSUMER INSIGHTS", "Consumer insights", "Behaviour against declaration: where panels and surveys disagree, and which one turned out to be right."),
           ("influence", "INFLUENCE", "Influence", "Identifying the voices that carry an audience rather than a follower count, and measuring what they move.")]
TH = {t[1]: t for t in THREADS}
for x in ARTS:
    x["t"] = TH[x["thread"]][0]
    x["tname"] = TH[x["thread"]][2]

AMBER, CREAM, NAVY = "#EAA93D", "#FCF6EF", "#13162D"
E = html.escape


# ------------------------------------------------------------------ the covers
def rnd(seed):
    return random.Random(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))


def art(slug, thread, w=600, h=400, cls="bl-art"):
    r = rnd(slug)
    g = []
    if thread == "foresight":            # signal lines: one of them starts to rise
        rows, hot = 22, r.randint(6, 15)
        for i in range(rows):
            y0 = 40 + i * (h - 80) / (rows - 1)
            amp = (34 if i == hot else r.uniform(2, 7))
            mid = r.uniform(.45, .75) * w
            pts = []
            for x in range(0, w + 1, 8):
                bump = amp * math.exp(-((x - mid) / (w * .12)) ** 2) + r.uniform(-.6, .6)
                pts.append("%d,%.1f" % (x, y0 - bump))
            col, op, sw = (AMBER, 1, 2.4) if i == hot else (CREAM, .16 + .5 * (i == hot - 1 or i == hot + 1), 1.2)
            g.append('<polyline points="%s" fill="none" stroke="%s" stroke-opacity="%.2f" stroke-width="%s" />' % (" ".join(pts), col, op, sw))
        g.append('<circle cx="%.0f" cy="%.0f" r="5" fill="%s" class="bl-pulse" />' % (mid, 40 + hot * (h - 80) / (rows - 1) - 34, AMBER))
    elif thread == "listening":          # a radar: rings, a sweep, blips
        cx, cy = w * r.uniform(.55, .7), h * .55
        for k in range(1, 7):
            g.append('<circle cx="%.0f" cy="%.0f" r="%d" fill="none" stroke="%s" stroke-opacity="%.2f" />' % (cx, cy, k * 48, CREAM, .22 - k * .02))
        g.append('<line x1="%.0f" y1="0" x2="%.0f" y2="%d" stroke="%s" stroke-opacity=".08" /><line x1="0" y1="%.0f" x2="%d" y2="%.0f" stroke="%s" stroke-opacity=".08" />' % (cx, cx, h, CREAM, cy, w, cy, CREAM))
        g.append('<g class="bl-sweep" style="transform-origin:%.0fpx %.0fpx"><path d="M%.0f %.0f L%.0f %.0f A300 300 0 0 0 %.0f %.0f Z" fill="url(#sw-%s)" /></g>' % (
            cx, cy, cx, cy, cx + 300, cy, cx + 300 * math.cos(-.6), cy + 300 * math.sin(-.6), slug))
        for _ in range(14):
            a_, d_ = r.uniform(0, 2 * math.pi), r.uniform(30, 270)
            hot = r.random() < .25
            g.append('<circle cx="%.0f" cy="%.0f" r="%s" fill="%s" fill-opacity="%s" />' % (cx + d_ * math.cos(a_), cy + d_ * math.sin(a_), 5 if hot else 2.5, AMBER if hot else CREAM, 1 if hot else .5))
    elif thread == "insights":           # two clouds that do not agree: declared, observed
        for k, (ox, col, op) in enumerate([(.33, CREAM, .45), (.66, AMBER, .95)]):
            for _ in range(70):
                rr, aa = abs(r.gauss(0, 46)), r.uniform(0, 2 * math.pi)
                g.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" fill-opacity="%.2f" />' % (w * ox + rr * math.cos(aa) * 1.3, h * .5 + rr * math.sin(aa), r.uniform(1.6, 3.4), col, op * r.uniform(.4, 1)))
        g.append('<path d="M%.0f %.0f C %.0f %.0f, %.0f %.0f, %.0f %.0f" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 6" stroke-opacity=".7" />' % (
            w * .33, h * .5, w * .45, h * .15, w * .55, h * .85, w * .66, h * .5, CREAM))
    else:                                # influence: a network, a few hubs carry it
        nodes = [(r.uniform(.06, .94) * w, r.uniform(.1, .9) * h) for _ in range(34)]
        hubs = r.sample(range(len(nodes)), 3)
        for i, (x, y) in enumerate(nodes):
            near = sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - x) ** 2 + (nodes[j][1] - y) ** 2)[1:3]
            for j in near:
                hot = i in hubs or j in hubs
                g.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-opacity="%s" stroke-width="%s" />' % (x, y, nodes[j][0], nodes[j][1], AMBER if hot else CREAM, .8 if hot else .18, 1.6 if hot else 1))
        for i, (x, y) in enumerate(nodes):
            if i in hubs:
                g.append('<circle cx="%.0f" cy="%.0f" r="16" fill="%s" fill-opacity=".18" class="bl-pulse" /><circle cx="%.0f" cy="%.0f" r="7" fill="%s" />' % (x, y, AMBER, x, y, AMBER))
            else:
                g.append('<circle cx="%.0f" cy="%.0f" r="3" fill="%s" fill-opacity=".6" />' % (x, y, CREAM))
    defs = '<defs><radialGradient id="glow-%s" cx="70%%" cy="30%%" r="80%%"><stop offset="0" stop-color="%s" stop-opacity=".22" /><stop offset="1" stop-color="%s" stop-opacity="0" /></radialGradient>' \
           '<linearGradient id="sw-%s" x1="0" x2="1"><stop offset="0" stop-color="%s" stop-opacity=".0" /><stop offset="1" stop-color="%s" stop-opacity=".35" /></linearGradient></defs>' % (slug, AMBER, AMBER, slug, AMBER, AMBER)
    return ('<svg class="%s bl-art--%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">%s'
            '<rect width="%d" height="%d" fill="%s" /><rect width="%d" height="%d" fill="url(#glow-%s)" />%s</svg>') % (cls, thread, w, h, defs, w, h, NAVY, w, h, slug, "".join(g))


# ------------------------------------------------------------------ blocks
def meta(x):
    return '<span class="bl-meta"><span>%s</span><span>%s</span></span>' % (x["date"], x["read"])


def card(x, big=False):
    return ('<li class="bl-card%s" data-t="%s"><a href="%s"><span class="bl-card__art">%s<span class="bl-chip">%s</span></span>'
            '<span class="bl-card__body">%s<b class="bl-card__t">%s</b><span class="bl-card__d">%s</span><span class="bl-card__go">Read the piece <i aria-hidden="true">→</i></span></span></a></li>') % (
        " bl-card--big" if big else "", x["t"], x["file"], art(x["slug"], x["t"], 900 if big else 600, 560 if big else 380), x["tname"], meta(x), E(x["title"]), E(x["lead"]))


def mag_block(id_):
    return '''      <section class="bl-mag" aria-labelledby="bl-mag-t">
        <div class="bl-mag__cover"><img src="/assets/img/magazine/audience-first-ed2-440.webp" srcset="/assets/img/magazine/audience-first-ed2-440.webp 440w, /assets/img/magazine/audience-first-ed2-880.webp 880w" sizes="260px" alt="Audience First, the Licter magazine" width="440" height="640" loading="lazy" decoding="async" /></div>
        <div class="bl-mag__copy">
          <p class="bl-k">THE MAGAZINE</p>
          <h2 class="bl-h2" id="bl-mag-t">Audience First, free.</h2>
          <p class="bl-p">Our printed magazine, on what audiences actually do. Leave your email and receive the PDF.</p>
          <button class="btn btn--primary" type="button" data-open="mag">Get the magazine <span aria-hidden="true">→</span></button>
        </div>
      </section>'''


def seismo():
    """the blog as a seismograph: each piece is a spike at its publication
    date, its height its reading time. Real dates, drawn signal around them."""
    import datetime
    days = [datetime.date(*x["key"][:1], x["key"][1] + 1, x["key"][2]) for x in ARTS]
    d0, d1 = min(days) - datetime.timedelta(days=6), max(days) + datetime.timedelta(days=6)
    W, H, base = 1200, 220, 160
    X = lambda d: 30 + (d - d0).days / (d1 - d0).days * (W - 60)
    r = rnd("seismo")
    peaks = [(X(d), 50 + 28 * int(x["read"].split()[0])) for d, x in zip(days, ARTS)]
    pts = []
    for px in range(0, W + 1, 4):
        y = base + r.uniform(-3, 3)
        for cx, hgt in peaks:
            y -= hgt * math.exp(-((px - cx) / 9) ** 2) * (1 if (px // 4) % 2 else .82)
        pts.append("%d,%.1f" % (px, y))
    marks = ""
    for (cx, hgt), x in zip(peaks, ARTS):
        top = base - hgt
        anchor = "end" if cx > W * .8 else ("start" if cx < W * .2 else "middle")
        marks += ('<a class="bl-seis__pk" href="%s"><title>%s</title><rect class="bl-seis__hit" x="%.0f" y="0" width="34" height="%d" /><line x1="%.0f" y1="%.0f" x2="%.0f" y2="%d" />'
                  '<circle cx="%.0f" cy="%.0f" r="7" /><text x="%.0f" y="%.0f" text-anchor="%s">%s</text></a>') % (
            x["file"], E(x["title"]), cx - 17, H - 20, cx, top, cx, H - 26, cx, top, cx, top - 16, anchor, E(x["title"]))
    months, m = "", d0.replace(day=1)
    while m <= d1:
        if m >= d0:
            months += '<text class="bl-seis__m" x="%.0f" y="%d">%s</text>' % (X(m), H - 6, MONTHS[m.month - 1][:3].upper())
        m = (m.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    return ('<figure class="bl-seis"><figcaption><span class="bl-seis__live"><i></i>%s</span><span>%s</span></figcaption>'
            '<svg viewBox="0 0 %d %d" aria-label="%s"><line class="bl-seis__base" x1="0" y1="%d" x2="%d" y2="%d" />'
            '<polyline class="bl-seis__line" points="%s" />%s%s</svg></figure>') % (
        "Blog seismograph", "One spike per piece, height = reading time", W, H, "Our pieces on a timeline", H - 26, W, H - 26, " ".join(pts), marks, months)


# ------------------------------------------------------------------ the blog page
def blog_main():
    lead, rest = ARTS[0], ARTS[1:]
    chips = '<button class="bl-f is-on" type="button" aria-pressed="true" data-f="all">All <small>%d</small></button>' % len(ARTS) + "".join(
        '<button class="bl-f" type="button" aria-pressed="false" data-f="%s">%s <small>%d</small></button>' % (k, n, sum(1 for x in ARTS if x["t"] == k)) for k, _, n, _ in THREADS)
    threads = "".join('<li><button class="bl-thread" type="button" data-f="%s"><span class="bl-thread__art">%s</span><b>%s</b><span>%s</span><small>%d <span>pieces</span> <i aria-hidden="true">→</i></small></button></li>' % (
        k, art("thread-" + k, k, 400, 240, "bl-art bl-art--mini"), n, d, sum(1 for x in ARTS if x["t"] == k)) for k, _, n, d in THREADS)
    return '''<main id="content" class="bl">
  <section class="bl-hero">
    <div class="shell">
      <div class="bl-hero__top">
        <p class="bl-k">BLOG</p>
        <p class="bl-hero__count"><span>%d <span>pieces</span></span><span>4 threads</span><span>Written by the consultants</span></p>
      </div>
      <h1 class="bl-h1">What we see <em>in the data.</em></h1>
      <p class="bl-lead">Methods, market reads and the occasional correction. Written by the consultants who ran the analysis, not by a content team.</p>
      %s
      <ul class="bl-feat">%s</ul>
    </div>
  </section>

  <section class="bl-sec" id="latest">
    <div class="shell">
      <div class="bl-bar">
        <h2 class="bl-h2">Latest pieces</h2>
        <div class="bl-fs" role="group" aria-label="Filter by thread">%s</div>
      </div>
      <ul class="bl-grid">%s</ul>
    </div>
  </section>

  <section class="bl-sec bl-sec--band" id="topics">
    <div class="shell">
      <p class="bl-k">WHAT WE WRITE ABOUT</p>
      <h2 class="bl-h2">Four running threads.</h2>
      <p class="bl-p">What we publish comes out of client work: the methods that held up, the ones that did not, and what the data showed before the market noticed.</p>
      <ul class="bl-threads">%s</ul>
    </div>
  </section>

  <section class="bl-sec">
    <div class="shell">
%s
    </div>
  </section>
</main>''' % (len(ARTS), seismo(), card(lead, True), chips, "".join(card(x) for x in rest), threads, mag_block("bl"))


# ------------------------------------------------------------------ an article
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")


def article_main(x):
    prose, toc = x["prose"], []
    def h2(m):
        sid = slugify(m.group(1)); toc.append((sid, m.group(1)))
        return '<h2 id="%s">%s</h2>' % (sid, m.group(1))
    prose = re.sub(r"<h2>(.*?)</h2>", h2, prose)
    toc_html = "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in toc)
    same = [y for y in ARTS if y is not x and y["t"] == x["t"]]
    more = (same + [y for y in ARTS if y is not x and y not in same])[:3]
    return '''<main id="content" class="bl bl--article">
  <div class="bl-progress" aria-hidden="true"><i></i></div>
  <article>
    <header class="bl-ah">
      <div class="shell bl-ah__grid">
        <div class="bl-ah__copy">
          <nav class="tk-crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li><li><a href="blog.html">Blog</a></li><li aria-current="page">%s</li></ol></nav>
          <p class="bl-chip bl-chip--solid">%s</p>
          <h1 class="bl-ah__t">%s</h1>
          <p class="bl-lead">%s</p>
          <p class="bl-by"><img src="%s" alt="" width="40" height="40" loading="lazy" decoding="async" /><span><b>%s</b>%s</span></p>
        </div>
        <div class="bl-ah__art">%s</div>
      </div>
    </header>
    <div class="shell"><p class="lang-note" role="note">Cet article n’est disponible qu’en anglais. Le reste du site bascule en français.</p></div>
    <div class="shell bl-body">
      <aside class="bl-toc" aria-label="In this piece">
        <p class="bl-k">IN THIS PIECE</p>
        <ol>%s</ol>
        <button class="bl-copy" type="button" data-copied="Link copied">Copy the link</button>
      </aside>
      <div class="prose bl-prose">%s</div>
    </div>
  </article>
  <div class="shell bl-after">
    %s
  </div>
  <section class="bl-sec bl-sec--band">
    <div class="shell">
      <div class="bl-bar"><h2 class="bl-h2">Keep reading</h2><a class="bl-link" href="blog.html">Every piece <span aria-hidden="true">→</span></a></div>
      <ul class="bl-grid">%s</ul>
    </div>
  </section>
  <section class="bl-sec">
    <div class="shell">
%s
    </div>
  </section>
</main>''' % (E(x["title"]), x["tname"], E(x["title"]), E(x["lead"]), x["avatar"], x["author"], meta(x), art(x["slug"], x["t"], 900, 640),
              toc_html, prose, x["uc"].replace('class="uc-links"', 'class="uc-links bl-uc"'), "".join(card(y) for y in more), mag_block(x["slug"][:10]))


def write(file, main):
    p = ROOT / file
    s = p.read_text()
    i, j = s.index('<main id="content"'), s.index("</main>") + len("</main>")
    p.write_text(s[:i] + main + s[j:])


def main():
    write("blog.html", blog_main())
    for x in ARTS:
        write(x["file"], article_main(x))
    print("blog.html and %d articles written" % len(ARTS))


if __name__ == "__main__":
    main()
