#!/usr/bin/env python3
"""Builds the blog: blog.html and one article-*.html page per article.

The articles live in tools/blog_articles.json (thread, title, lead, date,
read time, author, the prose and the related use cases). Each one gets a
generative cover drawn from its slug: the same article always gets the same
picture, and each thread has its own motif (signal lines for foresight, a
radar for listening, two clouds for insights, a network for influence).
The pictures are drawn, never data.

blog.html keeps its head, header and footer; only <main> is rewritten. The
article pages are built whole from tools/article-shell.html. The articles of
the former site (tools/migrate-webflow-articles.py, "lang": "fr") are pages
written in French; an article marked "draft" is neither built nor listed.

    python3 tools/build-blog.py
"""
import hashlib, html, importlib.util, json, math, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("ucb", ROOT / "tools" / "build-usecases.py")
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)
SITE = "https://www.licter.com"
ALL = json.loads((ROOT / "tools" / "blog_articles.json").read_text())
ARTS = [x for x in ALL if not x.get("draft")]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
for x in ARTS:
    d, m, y = x["date"].split()
    x["key"] = (int(y), MONTHS.index(m), int(d))
    x["slug"] = x["file"][len("article-"):-len(".html")]
ARTS.sort(key=lambda x: x["key"], reverse=True)

THREADS = [("foresight", "SOCIAL DATA & FORESIGHT", "Social data & foresight", "Reading what is shifting before it shows: new networks, consumption as activism, politics and the signals that announce a change."),
           ("listening", "MONITORING & SOCIAL LISTENING", "Monitoring & social listening", "How the practice works in real teams: crisis monitoring, choosing a tool, getting it adopted, catching the news of your sector."),
           ("insights", "CONSUMER INSIGHTS", "Consumer insights", "What brands learn from the conversation: L'Oréal, Orange, France Digitale, and the campaigns that worked."),
           ("influence", "INFLUENCE", "Influence", "The voices that carry an audience: creators, leaders, and the events they turn into records.")]
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
def fr_date(x):
    d, m, y = x["date"].split()
    return "%s %s %s" % ("1er" if d == "1" else d, MOIS[MONTHS.index(m)], y)


def meta(x, fr=False):
    if fr:
        return '<span class="bl-meta"><span>%s</span><span>%s</span></span>' % (fr_date(x), x["read"].replace("min read", "min de lecture"))
    return '<span class="bl-meta"><span>%s</span><span>%s</span></span>' % (x["date"], x["read"])


def card(x, big=False, fr=False):
    # text only: the picture belongs to the article page
    return ('<li class="bl-card%s" data-t="%s"><a href="%s"><span class="bl-card__body"><span class="bl-card__top"><span class="bl-tag">%s</span>%s</span>'
            '<b class="bl-card__t">%s</b><span class="bl-card__d">%s</span><span class="bl-card__go">Read the piece <i aria-hidden="true">→</i></span></span></a></li>') % (
        " bl-card--big" if big else "", x["t"], x["file"], x["tname"], meta(x, fr), E(x["title"]), E(x["lead"]))


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


# ------------------------------------------------------------------ the blog page
def row(x):
    """one line of the index: date, thread, title and lead, an arrow"""
    d, m, y = x["date"].split()
    return ('<li class="bl-row" data-t="%s"><a href="%s"><span class="bl-row__date"><b>%s</b><span>%s %s</span></span>'
            '<span class="bl-row__main"><span class="bl-tag">%s</span><b class="bl-row__t">%s</b><span class="bl-row__d">%s</span></span>'
            '<span class="bl-row__side"><span>%s</span><i aria-hidden="true">→</i></span></a></li>') % (
        x["t"], x["file"], d, m, y, x["tname"], E(x["title"]), E(x["lead"]), x["read"])


def blog_main():
    lead, side = ARTS[0], ARTS[1:3]
    chips = '<button class="bl-f is-on" type="button" aria-pressed="true" data-f="all">All <small>%d</small></button>' % len(ARTS) + "".join(
        '<button class="bl-f" type="button" aria-pressed="false" data-f="%s">%s <small>%d</small></button>' % (k, n, sum(1 for x in ARTS if x["t"] == k)) for k, _, n, _ in THREADS)
    threads = "".join('<li><button class="bl-thread" type="button" data-f="%s"><span class="bl-thread__n">%s</span><b>%s</b><span>%s</span><small>%d <span>pieces</span> <i aria-hidden="true">→</i></small></button></li>' % (
        k, "0%d" % (i + 1), n, d, sum(1 for x in ARTS if x["t"] == k)) for i, (k, _, n, d) in enumerate(THREADS))
    return """<main id="content" class="bl">
  <section class="bl-hero">
    <div class="shell">
      <div class="bl-hero__top">
        <p class="bl-k">BLOG</p>
        <p class="bl-hero__count"><span>%d <span>pieces</span></span><span>4 threads</span><span>Written by the consultants</span></p>
      </div>
      <div class="bl-hero__head">
        <h1 class="bl-h1">What we see <em>in the data.</em></h1>
        <p class="bl-lead">Methods, market reads and the occasional correction. Written by the consultants who ran the analysis, not by a content team.</p>
      </div>
      <div class="bl-mosaic">
        <ul class="bl-feat">%s</ul>
        <ul class="bl-side">%s</ul>
      </div>
    </div>
  </section>

  <section class="bl-sec" id="latest">
    <div class="shell">
      <div class="bl-bar">
        <h2 class="bl-h2">Every piece</h2>
        <div class="bl-view" role="group" aria-label="Display">
          <button class="bl-v is-on" type="button" aria-pressed="true" data-v="grid"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="1" y="1" width="6" height="6" rx="1.5"/><rect x="9" y="1" width="6" height="6" rx="1.5"/><rect x="1" y="9" width="6" height="6" rx="1.5"/><rect x="9" y="9" width="6" height="6" rx="1.5"/></svg>Cards</button>
          <button class="bl-v" type="button" aria-pressed="false" data-v="list"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="1" y="2" width="14" height="2.4" rx="1.2"/><rect x="1" y="6.8" width="14" height="2.4" rx="1.2"/><rect x="1" y="11.6" width="14" height="2.4" rx="1.2"/></svg>List</button>
        </div>
      </div>
      <div class="bl-fs" role="group" aria-label="Filter by thread">%s</div>
      <ul class="bl-grid bl-index" data-view="grid">%s</ul>
    </div>
  </section>

  <section class="bl-sec bl-sec--band" id="topics">
    <div class="shell">
      <div class="bl-split">
        <div>
          <p class="bl-k">WHAT WE WRITE ABOUT</p>
          <h2 class="bl-h2">Four running threads.</h2>
          <p class="bl-p">What we publish comes out of client work: the methods that held up, the ones that did not, and what the data showed before the market noticed.</p>
        </div>
        <ul class="bl-threads">%s</ul>
      </div>
    </div>
  </section>

  <section class="bl-sec">
    <div class="shell">
%s
    </div>
  </section>
</main>""" % (len(ARTS), card(lead, True), "".join(card(x) for x in side), chips, "".join(card(x) for x in ARTS), threads, mag_block("bl"))


# ------------------------------------------------------------------ an article
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")


# links put in the text of the French articles (SEO plan, step 9): the first
# mention of each term, at most four per article, one per destination,
# commercial pages first
TERMS = [
    ("gestion de crise", "/fr/offres/vigie-360/"), ("Social Listening Squad", "/fr/offres/social-listening-as-a-service/"),
    ("consumer insights", "/fr/offres/social-insights/"), ("audience intelligence", "/fr/expertise/audience-listening/"),
    ("e-réputation", "/fr/cas-usage/sante-de-marque/e-reputation-image-de-marque/"),
    ("Talkwalker", "/fr/outils/talkwalker/"), ("Visibrain", "/fr/outils/visibrain/"), ("Brandwatch", "/fr/outils/brandwatch/"),
    ("Radarly", "/fr/outils/radarly/"), ("Meltwater", "/fr/outils/radarly/"), ("Sprinklr", "/fr/outils/sprinklr/"),
    ("TikTok", "/fr/sources/tiktok/"), ("Instagram", "/fr/sources/instagram/"), ("LinkedIn", "/fr/sources/linkedin/"),
    ("YouTube", "/fr/sources/youtube/"), ("Twitch", "/fr/sources/twitch/"), ("Bluesky", "/fr/sources/bluesky/"), ("Threads", "/fr/sources/threads/"),
    ("influenceurs", "/fr/expertise/influence-listening/"), ("influence", "/fr/expertise/influence-listening/"),
    ("intelligence artificielle", "/fr/expertise/ai-listening/"), ("veille", "/fr/expertise/live-listening/"),
    ("social listening", "/fr/expertise/social-listening/"), ("campagne", "/fr/cas-usage/communication/mesurer-impact-campagne/"),
    ("crise", "/fr/cas-usage/sante-de-marque/risques-de-marque-crise/"),
    ("tendances", "/fr/cas-usage/tendances-innovation/"), ("consommateurs", "/fr/cas-usage/audiences/"),
    ("marques", "/fr/cas-usage/sante-de-marque/"),
]


def linkify(prose, cap=4):
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(prose, "html.parser")
    used = {a.get("href") for a in soup.find_all("a")}
    n = 0
    for term, url in TERMS:
        if n >= cap or url in used:
            continue
        rx = re.compile(r"(?<![\w-])(%s)(?![\w-])" % re.escape(term), 0 if term[0].isupper() else re.I)
        for node in soup.find_all(string=rx):
            if node.find_parent(["a", "h2", "h3", "figure", "figcaption"]) or node.find_parent(class_="bl-dek") or not node.find_parent(["p", "li"]):
                continue
            m = rx.search(node)
            a = soup.new_tag("a", href=url); a.string = m.group(1)
            node.replace_with(NavigableString(node[:m.start()]), a, NavigableString(node[m.end():])) if False else None
            before, after = NavigableString(node[:m.start()]), NavigableString(node[m.end():])
            node.insert_before(before); node.insert_before(a); node.insert_before(after); node.extract()
            used.add(url); n += 1
            break
    return str(soup)


def article_main(x):
    fr = x.get("lang") == "fr"
    note = ('<div class="shell"><p class="lang-note lang-note--fr" lang="en" role="note" hidden></p></div>' if fr else
            '<div class="shell"><p class="lang-note" role="note">Cet article n’est disponible qu’en anglais. Le reste du site bascule en français.</p></div>')
    import podcast_quotes as PQ
    src = x["prose"]
    if x["file"] in PQ.PROSE:      # rewritten from the interview (tools/podcast_quotes.py)
        vid = re.search(r'<figure class="bl-video">.*?</figure>', src, re.S)
        src = PQ.PROSE[x["file"]].replace("%(video)s", vid.group(0) if vid else "")
    src += PQ.EXTRA.get(x["file"], "")
    prose, toc = (linkify(src) if fr else src), []
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
    %s
    <div class="shell bl-body">
      <aside class="bl-toc" aria-label="In this piece">
        <p class="bl-k">IN THIS PIECE</p>
        <ol>%s</ol>
        <button class="bl-copy" type="button" data-copied="Link copied">Copy the link</button>
      </aside>
      <div class="prose bl-prose"%s>%s</div>
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
</main>''' % (E(x["title"]), x["tname"], E(x["title"]), E(x["lead"]), x["avatar"], byline(x, fr), meta(x, fr), art(x["slug"], x["t"], 900, 640), note,
              toc_html, ' lang="fr"' if fr else "", prose, x["uc"].replace('class="uc-links"', 'class="uc-links bl-uc"'), "".join(card(y, fr=fr) for y in more), mag_block(x["slug"][:10]))


def write(file, main):
    p = ROOT / file
    s = p.read_text()
    i, j = s.index('<main id="content"'), s.index("</main>") + len("</main>")
    p.write_text(s[:i] + main + s[j:])


# a complete short title for the <title> of long articles: no title cut
# mid-sentence with "…" (audit of 7 October 2026)
SEO_TITLE = {
    "Analyser les succès publicitaires en moins d'une heure ? Spotlight #1 : Licter x Petit Bateau": "Analyser une campagne en moins d'une heure : Petit Bateau",
    "Comment Axa analyse les données du web et de social listening pour sa gestion de crise ?": "Comment AXA lit la donnée sociale pour gérer une crise",
    "Comment conquérir le marché de la cosmétique de luxe grâce au social listening ?": "Conquérir la cosmétique de luxe grâce au social listening",
    "Comment créer une \"Social Listening Squad\" pour doubler l'adoption de votre outil ?": "Créer une Social Listening Squad pour adopter son outil",
    "Comment France Digitale juge l'efficacité de ses actions de communication ?": "Comment France Digitale mesure sa communication",
    "Comment L'Oréal utilise le social listening pour capter la voix du consommateur ?": "Comment L'Oréal capte la voix du consommateur",
    "Comment Origins associe influence et technologie pour transformer le capital-risque ?": "Origins : influence et technologie dans le capital-risque",
    "Départs de X : quels réseaux sociaux peuvent rivaliser avec la plateforme d\u2019Elon Musk ?": "Départs de X : quels réseaux pour prendre le relais ?",
    "La consommation devient un acte militant : les insights de Kantar sur les tendances d\u2019achat": "La consommation, un acte militant : les insights Kantar",
    "Comment Meltwater exploite les données social listening pour ses clients luxe ?": "Comment Meltwater lit le social listening pour le luxe",
    "Comment Talkwalker utilise le social listening pour comprendre ce que vos consommateurs pensent de vous ?": "Talkwalker : ce que vos consommateurs pensent de vous",
    "Comment Visibrain s'est positionné comme pionnier en social listening ?": "Visibrain, pionnier du social listening : entretien",
    "Social Listening et Politique : Comment capter la voix des citoyens ?": "Social listening et politique : capter la voix des citoyens",
}


# authors with a profile (the founders, on Why Licter): bylines link to it
PROFILE = {"Antoine Khaitrine": "antoine-khaitrine", "Adrien Krebs": "adrien-krebs"}


def byline(x, fr):
    """the author names, each linked to its profile; several joined by "et" / "and" """
    page = "/fr/pourquoi-licter/" if fr else "/why-licter.html"
    names = x["author"].split(" et ")
    return (" et " if fr else " and ").join('<a href="%s#%s">%s</a>' % (page, PROFILE[n], n) if n in PROFILE else n for n in names)


def author_ld(x, fr):
    if x["author"] in ("Licter analysis team", "L'équipe Licter"):
        return {"@type": "Organization", "name": "Licter", "url": SITE + "/"}
    page = SITE + ("/fr/pourquoi-licter/" if fr else "/why-licter.html")
    people = [dict({"@type": "Person", "name": n}, **({"url": "%s#%s" % (page, PROFILE[n])} if n in PROFILE else {})) for n in x["author"].split(" et ")]
    return people[0] if len(people) == 1 else people


def title_tag(x):
    t = html.unescape(x["title"])
    return SEO_TITLE.get(re.sub(r"[\u00a0\u202f]", " ", t), t)


# articles substantially rewritten since publication, and when
REWRITTEN = {f: "2026-10-07" for f in ("article-comment-loreal-utilise-le-social-listening-pour-capter-la-voix-du-consommateur.html",
                                      "article-licter-lvmh.html", "article-licter-meltwater.html",
                                      "article-licter-talkwalker-podcast.html", "article-licter-visibrain-podcast.html")}
REWRITTEN["article-le-bad-buzz-huda-beauty-decrypte.html"] = "2026-10-09"   # written up from its slides (audit of 9 October 2026)


def article_page(x):
    """the whole page, from tools/article-shell.html"""
    fr = x.get("lang") == "fr"
    page = (ROOT / "tools" / "article-shell.html").read_text().split("\n", 1)[1]
    # a description written for search results where the lead is too short or too long for one
    desc = x.get("desc") or (x["lead"] if len(x["lead"]) <= 160 else x["lead"][:157].rsplit(" ", 1)[0].rstrip(" ,:;") + "…")
    page = page.replace("<!--TITLE-->", E(title_tag(x) + " | Licter")).replace("<!--DESC-->", E(desc)).replace("<!--MAIN-->", article_main(x))
    if fr:
        page = page.replace("<!--HTML-->", '<html lang="fr" data-i18n-static data-alt-fr="/%s" data-alt-en="/blog.html">' % x["file"])
        b0, b1 = page.index("<body"), page.index("</body>")
        page = page[:b0] + U.translate(page[b0:b1]).replace(">Skip to content<", ">Aller au contenu<") + page[b1:]
    else:
        page = page.replace("<!--HTML-->", '<html lang="en">')
    # the article itself, for search engines
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": html.unescape(x["title"]), "description": html.unescape(x.get("desc") or x["lead"]),
          "datePublished": "%04d-%02d-%02d" % (x["key"][0], x["key"][1] + 1, x["key"][2]),
          "dateModified": REWRITTEN.get(x["file"], "%04d-%02d-%02d" % (x["key"][0], x["key"][1] + 1, x["key"][2])), "inLanguage": "fr" if fr else "en",
          "author": author_ld(x, fr),
          "publisher": {"@type": "Organization", "name": "Licter", "url": SITE + "/"}, "mainEntityOfPage": SITE + "/" + x["file"]}
    page = page.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False), 1)
    (ROOT / x["file"]).write_text(page)


THREADS_FR = {
    "foresight": "Lire ce qui bouge avant que cela se voie : nouveaux réseaux, consommation militante, politique, et les signaux qui annoncent un basculement.",
    "listening": "Comment la pratique fonctionne dans de vraies équipes : veille de crise, choix d'un outil, adoption, actualité de votre secteur.",
    "insights": "Ce que les marques apprennent de la conversation : L'Oréal, Orange, France Digitale, et les campagnes qui ont porté.",
    "influence": "Les voix qui portent une audience : créateurs, dirigeants, et les événements qu'ils transforment en records."}


def french_dictionary():
    """the dates, reading times and thread texts of the blog page, for js/fr.js"""
    p = ROOT / "js" / "fr.js"
    src = p.read_text()
    START, END = "  /* blog dates and threads (tools/build-blog.py) */\n", "  /* end of blog dates */\n"
    if START in src:
        i, j = src.index(START), src.index(END) + len(END)
        src = src[:i] + src[j:]
    pairs = {}
    for x in ARTS:
        pairs[x["date"]] = fr_date(x)
        pairs[x["read"]] = x["read"].replace("min read", "min de lecture")
    for k, _, _, d in THREADS:
        pairs[d] = U.typo(THREADS_FR[k], U.FR)
    pairs = {k: v for k, v in pairs.items() if '"%s":' % k not in src}
    block = START + "".join("  %s: %s,\n" % (json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False)) for k, v in sorted(pairs.items())) + END
    src = src.replace("  /* blog redesign", block + "  /* blog redesign", 1)
    p.write_text(src)


def main():
    french_dictionary()
    write("blog.html", blog_main())
    for x in ARTS:
        article_page(x)
    for x in ALL:
        if x.get("draft") and (ROOT / x["file"]).exists():
            (ROOT / x["file"]).unlink()
    print("blog.html and %d articles written" % len(ARTS))
    import runpy
    runpy.run_path(str(ROOT / "tools" / "build-fr-pages.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "tools" / "build-seo.py"), run_name="__main__")


if __name__ == "__main__":
    main()
