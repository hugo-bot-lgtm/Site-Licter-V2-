#!/usr/bin/env python3
"""The last pass over every page: what search engines and share previews read.

For each page of the site (the root pages, /fr/ and /en/):
  - the title ends in "| Licter" (no dash in the copy, titles included),
    unless that makes it longer than 65 characters;
  - a canonical URL, and hreflang links (to the twin page when there is one,
    otherwise x-default to itself);
  - og:url, and a share image: pages without one get a card drawn in the
    charter of tools/build-og.py (navy, amber, Aiglon), from their title,
    saved as assets/img/og/p-<page>.jpg;
  - a meta description of 160 characters at most;
  - French pages written in French load js/fr-core.js, the part of the
    dictionary the scripts need (menus, popups, chat), not the whole js/fr.js;
  - an honest "updated" date: the builders stamp the build date, and this
    pass keeps, per page, the date its content last changed (tools/page-dates.json,
    from a hash of the page without its dates and asset versions).
404.html and use-cases.html (a redirect) are left alone.

Run by tools/build-usecases.py and tools/build-blog.py at the end, or alone:

    python3 tools/build-seo.py
"""
import hashlib, html, json, pathlib, re, sys, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.licter.com"
SKIP = {"404.html", "use-cases.html"}
W, H = 1200, 630
NAVY, CREAM, AMBER = (19, 22, 45), (252, 246, 239), (234, 169, 61)
DEMI = str(ROOT / "assets/fonts/AiglonProWide-Demi.otf")
OG = ROOT / "assets/img/og"
DATES = ROOT / "tools" / "page-dates.json"   # per page: content hash and the date it last changed
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
STAMP = ROOT / "tools" / "og-cards.json"   # what each card was drawn from, so unchanged cards are not redrawn

THREAD_FR = {"SOCIAL DATA & FORESIGHT": "Social data & prospective", "MONITORING & SOCIAL LISTENING": "Veille & social listening",
             "CONSUMER INSIGHTS": "Consumer insights", "INFLUENCE": "Influence"}
ARTS = {a["file"]: a for a in json.loads((ROOT / "tools/blog_articles.json").read_text())}
_spec = __import__("importlib.util").util.spec_from_file_location("ucb_seo", ROOT / "tools" / "build-usecases.py")
U = __import__("importlib.util").util.module_from_spec(_spec)
_spec.loader.exec_module(U)
TWIN = re.compile(r'href="/?((?:why-licter|clients|blog|guide|diagnostic|book-a-meeting|events|event-[a-z-]+|legal|privacy|sources|offers'
                  r'|offer-[a-z0-9-]+|expertise(?:-[a-z]+-listening)?|tech-[a-z0-9-]+|source-[a-z0-9-]+)\.html)(#[^"]*)?"')


def pages():
    out = [p for p in sorted(ROOT.glob("*.html")) if p.name not in SKIP]
    for d in ("fr", "en"):
        out += sorted((ROOT / d).rglob("index.html"))
    return out


def url_of(p):
    rel = p.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    return "/" + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel)


def kicker(rel, fr):
    name = rel.split("/")[-2] if rel.endswith("index.html") else rel
    if rel.startswith("article-"):
        a = ARTS.get(rel)
        return "Blog · " + (THREAD_FR.get(a["thread"], "") if a else "")
    table = [
        (lambda: rel.startswith("tech-") or rel.startswith("fr/outils/"), "Techno & outils", "Tech & tools"),
        (lambda: rel.startswith("source-") or rel.startswith("fr/sources/"), "D'où viennent les données", "Where the data comes from"),
        (lambda: rel.startswith("offer") or rel.startswith("fr/offres/"), "Offres", "Offers"),
        (lambda: rel.startswith("expertise") or rel.startswith("fr/expertise/"), "Expertise", "Expertise"),
        (lambda: rel.startswith("event"), "Événements", "Events"),
        (lambda: rel == "blog.html", "Blog", "Blog"),
        (lambda: rel == "clients.html", "Clients", "Clients"),
        (lambda: rel == "why-licter.html", "Pourquoi Licter", "Why Licter"),
        (lambda: rel == "diagnostic.html", "Diagnostic", "Diagnostic"),
        (lambda: rel == "guide.html", "Guide offert", "Free guide"),
        (lambda: rel == "book-a-meeting.html", "Rendez-vous", "Book a meeting"),
        (lambda: rel in ("legal.html", "privacy.html"), "Licter", "Licter"),
    ]
    for test, f, e in table:
        if test():
            return f if fr else e
    return "Licter"


def card(kick, title, name):
    """the share image, unless the same card is already drawn"""
    stamps = json.loads(STAMP.read_text()) if STAMP.exists() else {}
    key = hashlib.md5(("%s|%s" % (kick, title)).encode()).hexdigest()
    if stamps.get(name) == key and (OG / name).exists():
        return
    im = Image.new("RGB", (W, H), NAVY)
    glow = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(glow)
    d.ellipse((760, -260, 1460, 440), fill=(92, 72, 50))
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(140)), .85)
    d = ImageDraw.Draw(im)
    d.text((80, 86), kick.upper(), font=ImageFont.truetype(DEMI, 26), fill=AMBER)
    for size in (64, 58, 52, 46, 40):
        f = ImageFont.truetype(DEMI, size)
        lines = textwrap.wrap(title, width=int(1040 / (size * .62)))
        if len(lines) <= 4:
            break
    y = 150
    for line in lines[:5]:
        d.text((80, y), line, font=f, fill=CREAM)
        y += int(size * 1.18)
    d.rounded_rectangle((80, y + 18, 176, y + 24), 3, fill=AMBER)
    logo = Image.open(ROOT / "assets/img/logo-white.png").convert("RGBA")
    logo = logo.resize((round(logo.width * 58 / logo.height), 58), Image.LANCZOS)
    im.paste(logo, (80, H - 108), logo)
    d.text((W - 80, H - 76), "Social Data Intelligence", font=ImageFont.truetype(DEMI, 20), fill=(200, 196, 210), anchor="ra")
    im.save(OG / name, "JPEG", quality=84, optimize=True, progressive=True)
    stamps[name] = key
    STAMP.write_text(json.dumps(stamps, indent=0, sort_keys=True))


def add_head(s, tag):
    return s.replace("</head>", tag + "\n</head>", 1)


def shorten(t, n):
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0].rstrip(" ,:;.") + "…"


DM = re.compile(r'("dateModified": ")(\d{4}-\d{2}-\d{2})(")')
BYLINE = re.compile(r'(<time datetime=")(\d{4}-\d{2}-\d{2})(">)([^<]*)(</time>)')


def honest_dates(rel, s, dates, today):
    """put back the date the content last changed, instead of the build date"""
    if rel.startswith("article-"):      # tools/build-blog.py dates its articles itself
        m = re.search(r'"dateModified": "(\d{4}-\d{2}-\d{2})"', s)
        if m:
            dates[rel] = {"hash": "", "date": m.group(1)}
        return s
    bare = BYLINE.sub(r"\1\3\5", DM.sub(r"\1\3", s))
    bare = re.sub(r"\?v=\d+", "", bare)
    h = hashlib.md5(bare.encode()).hexdigest()
    rec = dates.get(rel)
    if not rec or rec["hash"] != h:
        rec = dates[rel] = {"hash": h, "date": today}
    if not DM.search(s) and not BYLINE.search(s):
        return s
    y, m, d = (int(x) for x in rec["date"].split("-"))
    def label(fr_):
        return "%d %s %d" % (d, MOIS[m - 1], y) if fr_ else "%d %s %d" % (d, MONTHS[m - 1], y)
    s = DM.sub(lambda m_: m_.group(1) + rec["date"] + m_.group(3), s)
    return BYLINE.sub(lambda m_: m_.group(1) + rec["date"] + m_.group(3) + label(not re.search(r"[A-Z][a-z]+ \d{4}$", m_.group(4))) + m_.group(5), s)


LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
ORG_REF = {"@type": "Organization", "@id": SITE + "/#org", "name": "Licter", "url": SITE + "/",
           "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo-navy.png"}}
AUTHORS = {"Antoine Khaitrine": ["https://www.linkedin.com/in/antoine-khaitrine/", "https://www.thesilab.com/insider-50/antoine-khaitrine"],
           "Adrien Krebs": ["https://www.linkedin.com/in/adrien-krebs/"], "Mina Cantone": []}
ABOUT = {"why-licter.html", "fr/pourquoi-licter/index.html"}
COLLECTION = {"blog.html", "fr/blog/index.html", "clients.html", "fr/clients/index.html", "events.html"}


def structured(rel, s, fr, url):
    """a page-level entity and a breadcrumb where a page has none, and the
    articles completed (image, dateModified, author profiles, publisher)"""
    # the blocks this pass added before are dropped first: builders copy the
    # head of one page into another, and a block must never describe a page
    # other than its own
    s = re.sub(r'<script type="application/ld\+json" data-seo>.*?</script>\n?', "", s, flags=re.S)
    def foreign(m):
        try:
            b = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        if isinstance(b, dict) and b.get("@type") in ("WebPage", "AboutPage", "CollectionPage") and b.get("url") not in (None, url):
            return ""
        return m.group(0)
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>\n?', foreign, s, flags=re.S)
    blocks = []
    for m in LD.finditer(s):
        try:
            blocks.append(json.loads(m.group(1)))
        except ValueError:
            pass
    types = {b.get("@type") for b in blocks if isinstance(b, dict)}
    title = html.unescape(re.search(r"<title>([^<]*)</title>", s).group(1)).strip()
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(desc_m.group(1)) if desc_m else ""
    add = []
    if not types & {"WebPage", "AboutPage", "CollectionPage", "Article", "Event", "Service"}:
        kind = "AboutPage" if rel in ABOUT else "CollectionPage" if rel in COLLECTION else "WebPage"
        add.append({"@context": "https://schema.org", "@type": kind, "@id": url + "#webpage", "url": url, "name": title,
                    "description": desc, "inLanguage": "fr" if fr else "en", "isPartOf": {"@id": SITE + "/#website"},
                    "publisher": ORG_REF, "about": {"@id": SITE + "/#org"} if kind == "AboutPage" else None})
        add[-1] = {k: v for k, v in add[-1].items() if v is not None}
    if "BreadcrumbList" not in types and url not in (SITE + "/", SITE + "/fr/"):
        home = (SITE + "/fr/", "Accueil") if fr else (SITE + "/", "Home")
        items = [home]
        if rel.startswith("article-"):
            items.append((SITE + "/fr/blog/", "Blog"))
        name = re.sub(r"\s*\|\s*Licter.*$", "", title)
        items.append((url, ARTS[rel]["title"].replace("\u00a0", " ") if rel in ARTS else name))
        add.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": html.unescape(n), "item": u} for i, (u, n) in enumerate(items)]})
    for m in list(LD.finditer(s)):
        try:
            b = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(b, dict) and b.get("@type") == "Article":
            og = re.search(r'<meta property="og:image" content="([^"]*)"', s)
            if og:
                b["image"] = [og.group(1)]
            b.setdefault("dateModified", b.get("datePublished"))
            b["mainEntityOfPage"] = {"@id": url + "#webpage"}
            b["publisher"] = ORG_REF
            a = b.get("author") or {}
            if a.get("@type") == "Person" and AUTHORS.get(a.get("name")):
                a["sameAs"] = AUTHORS[a["name"]]
            b["mainEntityOfPage"] = {"@type": "WebPage", "@id": url}
            s = s.replace(m.group(0), '<script type="application/ld+json">%s</script>' % json.dumps(b, ensure_ascii=False), 1)
    if add:
        s = s.replace("</head>", "".join('<script type="application/ld+json" data-seo>%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in add) + "</head>", 1)
    return s


JS_DICT_USERS = ["ui", "popups", "assistant", "events", "home", "voices", "usecases", "communities", "i18n", "track"]
# strings the scripts build from parts, so not found as such in their source
CORE_EXTRA = re.compile(r"^See all \d+ clients$")


def fr_core():
    """js/fr-core.js: the entries of js/fr.js that the scripts themselves put on a page"""
    import subprocess
    full = json.loads(subprocess.run(["node", "-e", "global.window={};eval(require('fs').readFileSync(process.argv[1],'utf8'));"
                                      "process.stdout.write(JSON.stringify(window.LicterFR))", str(ROOT / "js/fr.js")],
                                     capture_output=True, text=True, check=True).stdout)
    src = "\n".join((ROOT / "js" / (n + ".js")).read_text() for n in JS_DICT_USERS)
    core = {k: v for k, v in full.items() if k in src or json.dumps(k)[1:-1] in src or CORE_EXTRA.match(k)}
    (ROOT / "js/fr-core.js").write_text("/* Generated by tools/build-seo.py from js/fr.js: the part of the dictionary the scripts need.\n"
                                        "   Pages already written in French load this instead of the whole js/fr.js. */\n"
                                        "window.LicterFR = %s;\n" % json.dumps(core, ensure_ascii=False, indent=0))
    return len(core), len(full)


def main():
    import datetime
    n_core, n_full = fr_core()
    OG.mkdir(parents=True, exist_ok=True)
    dates = json.loads(DATES.read_text()) if DATES.exists() else {}
    today = datetime.date.today().isoformat()
    done = 0
    for p in pages():
        s0 = s = p.read_text()
        rel = p.relative_to(ROOT).as_posix()
        url = SITE + url_of(p)
        m = re.search(r'<html[^>]*\blang="(\w+)"', s)
        fr = bool(m and m.group(1) == "fr")
        # titles: "| Licter", never a dash
        s = re.sub(r"(<title>[^<]*?)\s+[—–]\s+Licter</title>", r"\1 | Licter</title>", s)
        s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content="[^"]*?)\s+[—–]\s+Licter"', r'\1 | Licter"', s)
        # a title longer than 65 characters drops the brand: the subject is what shows in results
        s = re.sub(r"<title>([^<]*?) \| Licter</title>", lambda m_: "<title>%s</title>" % m_.group(1) if len(html.unescape(m_.group(1))) > 56 else m_.group(0), s)
        # description: 160 characters at most
        def desc(m_):
            d = html.unescape(m_.group(2))
            return m_.group(1) + html.escape(shorten(d, 160), quote=True) + '"' if len(d) > 160 else m_.group(0)
        s = re.sub(r'(<meta (?:name="description"|property="og:description") content=")([^"]*)"', desc, s)
        # canonical
        if 'rel="canonical"' not in s:
            s = add_head(s, '<link rel="canonical" href="%s" />' % url)
        # hreflang
        if "hreflang=" not in s:
            alt_fr = re.search(r'data-alt-fr="([^"]+)"', s)
            alt_en = re.search(r'data-alt-en="([^"]+)"', s)
            if alt_fr and alt_en and alt_fr.group(1) != alt_en.group(1) and not rel.startswith("article-"):
                s = add_head(s, '<link rel="alternate" hreflang="fr" href="%s%s" />\n<link rel="alternate" hreflang="en" href="%s%s" />\n'
                                '<link rel="alternate" hreflang="x-default" href="%s%s" />' % (SITE, alt_fr.group(1), SITE, alt_en.group(1), SITE, alt_fr.group(1)))
            elif fr:
                s = add_head(s, '<link rel="alternate" hreflang="fr" href="%s" />\n<link rel="alternate" hreflang="x-default" href="%s" />' % (url, url))
            else:
                s = add_head(s, '<link rel="alternate" hreflang="x-default" href="%s" />' % url)
        if 'property="og:url"' not in s:
            s = add_head(s, '<meta property="og:url" content="%s" />' % url)
        # share image: the cards drawn here are redrawn each time (title changes)
        s = re.sub(r'<meta property="og:image" content="%s/assets/img/og/p-[^"]+" />\n<meta property="og:image:width" content="1200" />\n'
                   r'<meta property="og:image:height" content="630" />\n' % re.escape(SITE), "", s)
        if 'property="og:image"' not in s:
            t = re.search(r'<meta property="og:title" content="([^"]*)"', s) or re.search(r"<title>([^<]*)</title>", s)
            title = re.sub(r"\s*\|\s*Licter$", "", html.unescape(t.group(1)).strip())
            if rel in ARTS:      # the whole title of an article, not the shortened tab title
                title = html.unescape(ARTS[rel]["title"]).replace("\u00a0", " ")
            name = "p-%s.jpg" % (re.sub(r"[^a-z0-9]+", "-", re.sub(r"\.html$", "", url_of(p)).lower()).strip("-") or "home")
            card(kicker(rel, fr), title, name)
            s = add_head(s, '<meta property="og:image" content="%s/assets/img/og/%s" />\n<meta property="og:image:width" content="1200" />\n'
                            '<meta property="og:image:height" content="630" />' % (SITE, name))
        s = s.replace('<meta name="twitter:card" content="summary" />', '<meta name="twitter:card" content="summary_large_image" />')
        if fr and "data-i18n-static" in s[:400]:
            s = re.sub(r'(<script src="/?js/)fr\.js(\?v=\d+"[^>]*></script>)', r"\1fr-core.js\2", s)
        # both web fonts early, so the text does not jump when they arrive (CLS)
        if 'href="/assets/fonts/AiglonProWide-Demi.woff2"' not in s:
            s = s.replace("<title>", '<link rel="preload" href="/assets/fonts/AiglonProWide-Demi.woff2" as="font" type="font/woff2" crossorigin />\n'
                                     '<link rel="preload" href="/assets/fonts/Raleway-latin.woff2" as="font" type="font/woff2" crossorigin />\n<title>', 1)
        # the footer: who we are and how to reach us, and an award stated as the founder's
        foot_fr = ("Licter SAS · 173 rue de Courcelles, 75017 Paris · <a href=\"mailto:contact@licter.com\">contact@licter.com</a> · "
                   "50+ clients · 160+ projets · Antoine Khaitrine, Top 50 Insider mondial (SI Lab) depuis 2022")
        foot_en = ("Licter SAS · 173 rue de Courcelles, 75017 Paris · <a href=\"mailto:contact@licter.com\">contact@licter.com</a> · "
                   "50+ clients · 160+ projects · Antoine Khaitrine, Top 50 Insider worldwide (SI Lab) since 2022")
        s = re.sub(r'<span>(?:Licter SAS ·.*?|50\+ clients · 160\+ (?:projects|projets) · Top 50 Insider[^<]*)</span>(?=\s*</div>\s*</footer>)',
                   "<span>%s</span>" % (foot_fr if fr else foot_en), s, flags=re.S)
        # French pages link to French pages in their HTML, not through a script
        if fr:
            s = s.replace('href="/"', 'href="/fr/"')
            s = re.sub(r'href="([^"]*)" data-fr="([^"]*)"', r'href="\2" data-en="\1"', s)
            s = TWIN.sub(lambda m_: 'href="%s%s"' % (U.expertise_fr(m_.group(1)), m_.group(2) or ""), s)
        # the home without a redirect: /fr/ for French pages, / for English ones
        home = "/fr/" if fr else "/"
        s = re.sub(r'href="(?:/fr/|/)?index\.html(#[^"]*)?"', lambda m_: 'href="%s%s"' % (home, m_.group(1) or ""), s)
        s = structured(rel, s, fr, url)
        s = honest_dates(rel, s, dates, today)
        if s != s0:
            p.write_text(s)
            done += 1
    DATES.write_text(json.dumps(dates, indent=0, sort_keys=True))
    # the sitemap gets the date each page last changed
    by_url = {SITE + url_of(ROOT / r): d["date"] for r, d in dates.items() if (ROOT / r).exists()}
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        x = re.sub(r"\s*<lastmod>[^<]*</lastmod>", "", sm.read_text())
        x = re.sub(r"(<loc>([^<]+)</loc>)", lambda m_: m_.group(1) + ("<lastmod>%s</lastmod>" % by_url[m_.group(2)] if m_.group(2) in by_url else ""), x)
        sm.write_text(x)
    print("seo: %d pages updated; js/fr-core.js: %d of %d entries" % (done, n_core, n_full))


if __name__ == "__main__":
    main()
