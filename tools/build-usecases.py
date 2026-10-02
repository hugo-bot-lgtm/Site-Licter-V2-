#!/usr/bin/env python3
"""Builds the use-case pages, in French and English, as static HTML.

    python3 tools/build-usecases.py

Writes, from tools/uc_content.py:
  /fr/cas-usage/                          the hub (and /en/use-cases/)
  /fr/cas-usage/<famille>/                one page per family (4)
  /fr/cas-usage/<famille>/<cas>/          one page per use case (12)
  and the same under /en/use-cases/, plus sitemap.xml and robots.txt.

Why static: Google indexes what is in the HTML. The rest of the site is
written in English and translated in the browser, so only its English is
indexed; these pages carry their French in the HTML itself, each linked to
its English twin with hreflang.

The header, banner and footer are taken from offers.html so they stay in
step with the rest of the site; the French ones are translated with the
site's own dictionary (js/fr.js).
"""
import datetime, html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import uc_content as C  # noqa: E402

SITE = C.SITE.rstrip("/")
FR, EN = 0, 1
LANGS = ("fr", "en")

# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(s, quote=True)

def typo(s, lang):
    """French typography: non-breaking spaces before : ; ? ! and inside « »."""
    if lang != FR:
        return s
    s = re.sub(r" ([:;?!»])", " \\1", s)
    s = s.replace("« ", "« ")
    return s

def T(pair, lang):
    return esc(typo(pair[lang], lang))

def version():
    m = re.search(r"styles\.min\.css\?v=(\d+)", (ROOT / "index.html").read_text())
    return m.group(1) if m else "1"

# ------------------------------------------------------------- dictionary
def fr_dict():
    js = (ROOT / "js" / "fr.js").read_text()
    out = subprocess.run(["node", "-e", "var window={};" + js + ";process.stdout.write(JSON.stringify(window.LicterFR||{}))"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

DICT = fr_dict()

def translate(fragment):
    """The same walk as js/i18n.js: text nodes and a few attributes."""
    def text(m):
        raw = m.group(1)
        key = re.sub(r"\s+", " ", html.unescape(raw)).strip()
        hit = DICT.get(key)
        if not hit:
            return m.group(0)
        lead = re.match(r"^\s*", raw).group(0)
        trail = re.search(r"\s*$", raw).group(0)
        return ">" + lead + esc(hit).replace("&#x27;", "'") + trail + "<"
    fragment = re.sub(r">([^<>]+)<", text, fragment)
    def attr(m):
        key = html.unescape(m.group(2)).strip()
        hit = DICT.get(key)
        return m.group(0) if not hit else '%s="%s"' % (m.group(1), esc(hit))
    return re.sub(r'(placeholder|aria-label|alt)="([^"]*)"', attr, fragment)

# ---------------------------------------------------------------- URLs
def hub_path(lang):
    return "/%s/%s/" % (LANGS[lang], C.HUB["slug"][lang])

def fam_path(f, lang):
    return hub_path(lang) + f["slug"][lang] + "/"

def case_path(c, lang):
    return fam_path(FAM[c["family"]], lang) + c["slug"][lang] + "/"

FAM = {f["key"]: f for f in C.FAMILIES}
CASE = {c["key"]: c for c in C.CASES}

UC_ANCHORS = {  # old anchors of use-cases.html -> family keys
    "communication": "communication", "brand-health": "brand", "audiences": "audiences", "trends": "trends",
}

def absolutize(fragment, lang):
    """Links of the shared header/footer, made to work from a sub-folder, and
    pointed at the new use-case pages in the page's language."""
    def uc(m):
        anchor = m.group(1)
        if anchor and anchor[1:] in UC_ANCHORS:
            return 'href="%s"' % fam_path(FAM[UC_ANCHORS[anchor[1:]]], lang)
        return 'href="%s"' % hub_path(lang)
    fragment = re.sub(r'href="use-cases\.html(#[\w-]+)?"', uc, fragment)
    # links already pointing at the use-case pages carry their English twin
    fragment = re.sub(r'href="([^"]+)" data-en="([^"]+)"', lambda m: 'href="%s"' % m.group(1 + lang), fragment)
    fragment = re.sub(r'(href|src)="(?!https?:|/|#|mailto:)([^"]+)"', r'\1="/\2"', fragment)
    return fragment

# ------------------------------------------------------------ shared parts
SRC = (ROOT / "offers.html").read_text()   # any inner page: same banner, header and footer
BANNER = re.search(r'<aside class="banner".*?</aside>', SRC, re.S).group(0)
HEADER = re.search(r'<div class="site-head">.*?</header>\s*</div>', SRC, re.S).group(0)
FOOTER = re.search(r'<footer class="site-foot">.*?</footer>', SRC, re.S).group(0)

def shared(part, lang):
    part = re.sub(r"\s*<!-- newsletter band -->.*?(?=<div class=\"site-foot__in)", "\n  ", part, flags=re.S)
    part = absolutize(part, lang)
    return translate(part) if lang == FR else part

L = {  # interface words of these pages
    "home": ("Accueil", "Home"),
    "crumbs": ("Fil d'Ariane", "Breadcrumb"),
    "book": ("Prendre rendez-vous", "Book a meeting"),
    "live": ("Voir un cas en direct", "See a live case"),
    "questions": ("Les questions auxquelles on répond", "The questions we answer"),
    "get": ("Ce que vous obtenez", "What you get"),
    "read": ("Ce que nous lisons", "What we read"),
    "how": ("Comment on s'y prend", "How we go about it"),
    "example": ("Un exemple", "An example"),
    "example_note": ("Données illustratives. Le cas change de secteur à chaque visite : agroalimentaire, luxe, jeux vidéo, automobile.",
                     "Illustrative data. The case changes sector on every visit: food, luxury, video games, automotive."),
    "faq": ("Questions fréquentes", "Frequently asked questions"),
    "same": ("Dans la même famille", "In the same family"),
    "family_all": ("Toute la famille %s", "The whole %s family"),
    "three": ("Trois cas d'usage", "Three use cases"),
    "read_case": ("Lire le cas", "Read the use case"),
    "why": ("Une lecture, pas un tableau de bord", "A read, not a dashboard"),
    "voice": ("Dans leurs mots", "In their own words"),
    "others": ("Les autres familles", "The other families"),
    "families": ("Quatre familles de questions", "Four families of questions"),
    "loading": ("Lecture de la conversation…", "Reading the conversation…"),
    "cases_n": ("3 cas d'usage", "3 use cases"),
}

BOOK = {
    "h2": ("Laquelle de ces questions est la vôtre ?", "Which of these questions is yours?"),
    "lead": ("Laissez votre e-mail ou votre téléphone. Un consultant vous rappelle dans les 30 minutes pour en parler.",
             "Leave your email or phone number. A consultant calls you back within 30 minutes to talk it through."),
    "label": ("E-mail ou téléphone", "Email or phone"),
    "ph": ("nom@entreprise.com ou 06 12 34 56 78", "name@company.com or 06 12 34 56 78"),
    "btn": ("Me faire rappeler", "Call me back"),
    "err": ("Saisissez un e-mail professionnel ou un numéro de téléphone.", "Enter a work email or a phone number."),
    "promise": ("Un consultant, pas un commercial. Dans les 30 minutes.", "A consultant, not a sales team. Within 30 minutes."),
    "consent": ("Vos coordonnées servent uniquement à vous rappeler.", "We use your contact details only to call you back."),
    "privacy": ("Politique de confidentialité", "Privacy policy"),
    "diag": ("Vous faites déjà du social listening ?", "Already running social listening?"),
    "diag_link": ("Demandez plutôt un diagnostic", "Request a diagnostic instead"),
    "proof": [("50+", ("organisations accompagnées", "organisations served")),
              ("160+", ("projets depuis 2022", "projects since 2022")),
              ("20+", ("langues suivies", "languages monitored"))],
}

def book(lang):
    b = BOOK
    proof = "".join('<li><b>%s</b><span>%s</span></li>' % (n, T(t, lang)) for n, t in b["proof"])
    return f'''  <!-- MOCK: the callback form sends nothing yet (js/home.js); wire to the CRM. -->
  <section class="ucf ucf--book" id="book">
    <div class="shell">
      <div class="book book--uc">
        <div class="book__main">
          <h2 class="block__title">{T(b["h2"], lang)}</h2>
          <p class="block__lead">{T(b["lead"], lang)}</p>
          <form class="callback" id="book-form" novalidate>
            <div class="fld">
              <label class="fld__label" for="book-contact">{T(b["label"], lang)}</label>
              <div class="callback__row">
                <input class="fld__input" id="book-contact" name="contact" type="text" inputmode="email" autocomplete="email" placeholder="{T(b["ph"], lang)}" required />
                <button class="btn btn--primary" type="submit">{T(b["btn"], lang)} <span aria-hidden="true">→</span></button>
              </div>
              <p class="fld__error" id="book-contact-error" hidden>{T(b["err"], lang)}</p>
            </div>
            <p class="callback__promise"><span class="callback__dot" aria-hidden="true"></span>{T(b["promise"], lang)}</p>
            <p class="consent">{T(b["consent"], lang)} <a href="/privacy.html">{T(b["privacy"], lang)}</a>.</p>
          </form>
          <p class="book__done" id="book-done" role="status" hidden></p>
          <p class="ucf__diag">{T(b["diag"], lang)} <a href="/diagnostic.html">{T(b["diag_link"], lang)} →</a></p>
        </div>
        <ul class="book__proof book__proof--side">{proof}</ul>
      </div>
    </div>
  </section>'''

def crumbs(items, lang):
    """items: [(label, path or None)]"""
    lis = []
    for label, path in items:
        lis.append('<li><a href="%s">%s</a></li>' % (path, esc(label)) if path else '<li aria-current="page">%s</li>' % esc(label))
    return '  <nav class="crumbs shell" aria-label="%s"><ol>%s</ol></nav>' % (T(L["crumbs"], lang), "".join(lis))

def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": label, "item": SITE + path}
                                for i, (label, path) in enumerate(items)]}

def faq_ld(faq, lang):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": typo(q[lang], lang),
                            "acceptedAnswer": {"@type": "Answer", "text": typo(a[lang], lang)}} for q, a in faq]}

ORG = {"@type": "Organization", "name": "Licter", "url": SITE + "/", "logo": SITE + "/assets/img/logo-navy.png"}

def faq_html(faq, lang):
    return "".join('<details><summary>%s</summary><p>%s</p></details>' % (T(q, lang), T(a, lang)) for q, a in faq)

def stage(topic, lang):
    return f'''      <!-- MOCK: an illustrative case, four sectors (js/usecases.js) -->
      <div class="lf__stage ucf__stage" data-uc-stage="{topic}" data-mock>
        <div class="lf__empty"><p class="lf__empty-title">{T(L["loading"], lang)}</p></div>
      </div>'''

def reel(v, lang):
    vid, time, quote, brand, who = v
    q = typo("« %s »" % quote[FR], FR) if lang == FR else "“%s”" % quote[EN]
    return f'''        <a class="reel ucf__voice" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">
          <span class="reel__shot">
            <img src="https://i.ytimg.com/vi_webp/{vid}/hqdefault.webp" width="480" height="360" alt="" loading="lazy" decoding="async" />
            <span class="reel__play" aria-hidden="true"></span>
            <span class="reel__time">{time}</span>
          </span>
          <span class="ucf__voice-k">{T(L["voice"], lang)}</span>
          <span class="reel__quote">{esc(q)}</span>
          <span class="reel__meta"><b class="reel__brand">{esc(brand)}</b> <em class="reel__who">{esc(who)}</em></span>
        </a>'''

# ------------------------------------------------------------------- page
def page(lang, path, alt_path, title, meta, body, ld, og_type="website", og_image="hub"):
    v = version()
    other = 1 - lang
    fr_path, en_path = (path, alt_path) if lang == FR else (alt_path, path)
    ld = ld + [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITE + path,
                "inLanguage": LANGS[lang], "dateModified": TODAY.isoformat(), "author": ORG, "publisher": ORG}]
    ld_tags = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    scripts = ([f'<script src="/js/fr.js?v={v}"></script>'] if lang == FR else []) + [
        f'<script src="/js/i18n.js?v={v}"></script>',
        f'<script src="/js/ui.js?v={v}"></script>',
        f'<script src="/js/home.js?v={v}"></script>',
    ]
    skip = "Aller au contenu" if lang == FR else "Skip to content"
    return f'''<!doctype html>
<!-- Generated by tools/build-usecases.py from tools/uc_content.py: edit those, not this file. -->
<html lang="{LANGS[lang]}" data-i18n-static data-alt-fr="{fr_path}" data-alt-en="{en_path}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(typo(title, lang))}</title>
<meta name="description" content="{esc(typo(meta, lang))}" />
<link rel="canonical" href="{SITE}{path}" />
<link rel="alternate" hreflang="fr" href="{SITE}{fr_path}" />
<link rel="alternate" hreflang="en" href="{SITE}{en_path}" />
<link rel="alternate" hreflang="x-default" href="{SITE}{fr_path}" />
<link rel="icon" type="image/png" href="/assets/img/favicon.png" />
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
<meta property="og:site_name" content="Licter" />
<meta property="og:type" content="{og_type}" />
<meta property="og:locale" content="{'fr_FR' if lang == FR else 'en_GB'}" />
<meta property="og:locale:alternate" content="{'en_GB' if lang == FR else 'fr_FR'}" />
<meta property="og:url" content="{SITE}{path}" />
<meta property="og:title" content="{esc(typo(title, lang))}" />
<meta property="og:description" content="{esc(typo(meta, lang))}" />
<meta property="og:image" content="{SITE}/assets/img/og/uc-{og_image}-{LANGS[lang]}.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#13162D" />
<script src="/js/theme.js?v={v}"></script>
<link rel="stylesheet" href="/css/styles.min.css?v={v}" />
{ld_tags}
</head>
<body class="ucx ucp-page">
<a class="skip-link" href="#content">{skip}</a>

{shared(BANNER, lang)}

{shared(HEADER, lang)}

<main id="content">
{body}
</main>

<div class="ucp-bar" aria-hidden="true" hidden>
  <a class="btn btn--primary" href="#offre" tabindex="-1">{T(L["bar_offer"], lang)}</a>
  <a class="btn btn--ghost" href="#book" tabindex="-1">{T(L["bar_call"], lang)}</a>
</div>

{shared(FOOTER, lang)}

{chr(10).join(scripts)}
</body>
</html>
'''

def write(path, text):
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    return out

# ------------------------------------------------------------------ bodies
# the site's own icon set (the menus in js/ui.js), reused rather than redrawn
_UI = (ROOT / "js" / "ui.js").read_text()
ICON = dict(re.findall(r"^\s{4}(\w+): '(<svg.*?</svg>)',?$",
                       re.search(r"var ICONS = \{(.*?)\n  \};", _UI, re.S).group(1), re.M))
FAM_ICON = {"communication": "influence", "brand": "brand", "audiences": "audiences", "trends": "trends"}


def icon(name):
    return '<span class="ucp__ico" aria-hidden="true">%s</span>' % ICON.get(name, ICON["chart"])


def source_icon(label_en):
    l = label_en.lower()
    table = (
        (("search",), "search"),
        (("generative ai",), "ai"),
        (("panel", "audience", "communit", "affinit", "base"), "audiences"),
        (("press", "blog", "media", "expert", "institution"), "layers"),
        (("review", "forum", "customer"), "panel"),
        (("competit", "peer", "controvers", "trend"), "chart"),
        (("social", "linkedin", "tiktok", "creator", "x and", "networks"), "influence"),
        (("language",), "bell"),
    )
    for keys, name in table:
        if any(k in l for k in keys):
            return name
    return "chart"


# the same four lines on every family page: what sets a read apart from a tool
VERSUS = [
    (("Des volumes de mentions", "Mention volumes"),
     ("Qui parle, avec quelle influence, et ce qui a changé", "Who is talking, with what influence, and what changed")),
    (("Des alertes sur des mots-clés", "Keyword alerts"),
     ("Un analyste qui qualifie chaque signal avant de vous prévenir", "An analyst who qualifies each signal before alerting you")),
    (("La traduction automatique", "Machine translation"),
     ("Des analystes qui parlent la langue du marché", "Analysts who speak the market's language")),
    (("Un export à interpréter", "An export to interpret"),
     ("Une recommandation présentée à celles et ceux qui décident", "A recommendation presented to the people who decide")),
]

L.update({
    "tool": ("Un outil de veille vous donne", "A monitoring tool gives you"),
    "licter": ("Licter vous donne", "Licter gives you"),
    "found": ("Ce que la conversation a montré", "What the conversation showed"),
    "reco": ("Notre recommandation", "Our recommendation"),
    "illus": ("Exemple illustratif", "Illustrative example"),
    "presented": ("Présenté par le consultant qui a mené l'analyse.", "Presented by the consultant who ran the analysis."),
    "see_q": ("Voir les questions", "See the questions"),
    "jump": ("Aller à une famille", "Go to a family"),
})


def split_example(text):
    """'Exemple illustratif : situation. Recommandation : action.' -> (situation, action)"""
    t = re.sub(r"^(Exemple illustratif|Illustrative example)\s*:\s*", "", text)
    m = re.split(r"\s*(?:Recommandation|Recommendation)\s*:\s*", t, maxsplit=1)
    cap = lambda x: x[:1].upper() + x[1:]
    return (cap(m[0]), cap(m[1])) if len(m) == 2 else (cap(t), "")


TODAY = datetime.date.today()
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def byline(lang):
    d = ("%d %s %d" % (TODAY.day, MONTHS_FR[TODAY.month - 1], TODAY.year)) if lang == FR else TODAY.strftime("%-d %B %Y")
    by = ("Par l'équipe d'analyse Licter", "By the Licter analysis team")[lang]
    up = ("Mis à jour le", "Updated")[lang]
    return '\n        <p class="ucp__byline">%s · %s <time datetime="%s">%s</time></p>' % (esc(by), up, TODAY.isoformat(), d)


def hero(kicker_html, h1, intro, lang, aside="", actions=True, extra="", after=""):
    act = ""
    if actions:
        act = ('\n          <div class="page__actions">'
               '\n            <a class="btn btn--primary" href="#book">%s <span aria-hidden="true">→</span></a>%s'
               '\n          </div>') % (T(L["book"], lang), extra)
    split = " ucp__head--split" if aside else ""
    return ('  <section class="page ucp__head%s">\n'
            '    <div class="shell ucp__hero">\n'
            '      <div class="ucp__hero-main">\n'
            '        <p class="ucp__kicker">%s</p>\n'
            '        <h1 class="ucp__title%s">%s</h1>\n'
            '        <p class="ucp__lead">%s</p>%s%s%s\n'
            '      </div>%s\n'
            '    </div>\n'
            '%s\n'
            '  </section>') % (split, kicker_html, " ucp__title--long" if len(html.unescape(h1)) > 52 else "", h1, intro, act, after, byline(lang), aside, clients(lang))


def related(title_id, title, links, extra=""):
    return ('      <aside class="ucp__related" aria-labelledby="%s">\n'
            '        <h2 class="ucp__h2" id="%s">%s</h2>\n'
            '        <ul>%s</ul>%s\n'
            '      </aside>') % (title_id, title_id, title, links, extra)


def faq_block(faq, lang, aside):
    return ('  <section class="ucp">\n'
            '    <div class="shell ucp__cols ucp__cols--faq">\n'
            '      <div>\n'
            '        <h2 class="ucp__h2">%s</h2>\n'
            '        <div class="faq">%s</div>\n'
            '      </div>\n%s\n'
            '    </div>\n'
            '  </section>') % (T(L["faq"], lang), faq_html(faq, lang), aside)


def section(inner, sid=""):
    return '  <section class="ucp"%s>\n    <div class="shell">\n%s\n    </div>\n  </section>' % (
        ' id="%s"' % sid if sid else "", inner)


def case_body(c, lang):
    """A use case in six blocks: the client's problem, the deliverable they
    receive (its own for each case), how it runs, the proof, the offer."""
    import uc_deliverables as D
    f = FAM[c["family"]]
    x = C.EXTRA[c["key"]]
    n = [y for y in C.CASES if y["family"] == c["family"]].index(c) + 1
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], hub_path(lang)), (f["name"][lang], fam_path(f, lang)), (c["name"][lang], None)]
    long = " ucr__title--long" if len(c["h1"][lang]) > 52 else ""
    lead = c["meta"][lang]
    gets = "".join("<li>%s</li>" % T(g, lang) for g in c["deliverables"][:3])
    kicker = '%s<a href="%s">%s</a><span class="ucp__kicker-n">0%d / 03</span>' % (
        icon(FAM_ICON[f["key"]]), fam_path(f, lang), T(f["name"], lang), n)

    # 1. hero
    hero = ('  <section class="ucr-hero ucv-hero">\n'
            '    <div class="shell">\n'
            '      <p class="ucp__kicker">%s</p>\n'
            '      <div class="ucv-hero__row">\n'
            '        <div>\n'
            '          <h1 class="ucr__title%s">%s</h1>\n'
            '          <p class="ucr__lead">%s</p>\n'
            '          <div class="page__actions">\n'
            '            <a class="btn btn--primary" href="#book">%s <span aria-hidden="true">→</span></a>\n'
            '            <a class="ucp__textlink" href="#livrable">%s <span aria-hidden="true">↓</span></a>\n'
            '          </div>%s\n'
            '        </div>\n'
            '        <div class="ucr-hero__get">\n'
            '          <p class="ucr__label">%s</p>\n'
            '          <ul class="ucr__ticks">%s</ul>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n'
            '%s\n'
            '  </section>') % (kicker, long, T(c["h1"], lang), esc(typo(lead, lang)), T(L["book"], lang), T(L["see_dlv"], lang),
                               byline(lang), T(L["get"], lang), gets, clients(lang))

    # 2. the problem, in the client's words
    sym = "".join('<li><span class="ucv-sym__now">%s</span><span class="ucv-sym__arr" aria-hidden="true">→</span><span class="ucv-sym__miss">%s</span></li>' % (
        T(a, lang), T(b, lang)) for a, b in D.SYMPTOMS[c["key"]])
    q = typo(("« %s »" if lang == FR else "“%s”") % c["questions"][0][lang], lang)
    problem = ('  <section class="ucp ucv-problem">\n'
               '    <div class="shell">\n'
               '      <p class="ucr__label">%s</p>\n'
               '      <h2 class="ucv-quote">%s</h2>\n'
               '      <div class="ucv-sym">\n'
               '        <p class="ucv-sym__head"><span>%s</span><span>%s</span></p>\n'
               '        <ul>%s</ul>\n'
               '      </div>\n'
               '    </div>\n'
               '  </section>') % (T(L["problem_k"], lang), esc(q), T(L["now"], lang), T(L["missing"], lang), sym)

    # 3. the deliverable, its own for each case
    dlv = ('  <section class="ucp ucv-dlv" id="livrable">\n'
           '    <div class="shell ucv-dlv__grid">\n'
           '      <div class="ucv-dlv__copy">\n'
           '        <p class="ucr__label">%s</p>\n'
           '        <h2 class="ucp__h2">%s</h2>\n'
           '        <p class="ucv-p">%s</p>\n'
           '        <ul class="ucr__ticks">%s</ul>\n'
           '      </div>\n'
           '      %s\n'
           '    </div>\n'
           '  </section>') % (T(L["dlv_k"], lang), T(D.TITLES[c["key"]], lang), T(x["approach"], lang),
                              "".join("<li>%s</li>" % T(g, lang) for g in c["deliverables"]), D.render(c["key"], lang, esc, typo))

    # 4. how it runs: a dated timeline, the sources beneath
    days = ["J0", "J+3", "J+7", "J+10"] if lang == FR else ["Day 0", "Day 3", "Day 7", "Day 10"]
    steps = "".join('<li><span class="ucv-day">%s</span><b>%s</b><p>%s</p></li>' % (days[i], T(C.STEPS[i], lang), T(s, lang))
                    for i, s in enumerate(c["steps"]))
    src = "".join('<li>%s<span>%s</span></li>' % (icon(source_icon(a[EN])), T(a, lang)) for a, b in c["sources"])
    how = ('  <section class="ucp ucv-how">\n'
           '    <div class="shell">\n'
           '      <h2 class="ucp__h2">%s</h2>\n'
           '      <ol class="ucv-time">%s</ol>\n'
           '      <p class="ucv-note">%s</p>\n'
           '      <div class="ucv-src"><p class="ucr__label">%s</p><ul>%s</ul></div>\n'
           '    </div>\n'
           '  </section>') % (T(L["how_t"], lang), steps, T(L["days_note"], lang), T(L["sources_k"], lang), src)

    # 5. the proof: client interview, typical case, what it pays back
    ctx, rest = split_context(c["example"][lang])
    found, reco = split_example(rest)
    vid, time, quote, brand, who = C.VOICES[x["voice"]]
    vq = typo("« %s »" % quote[FR], FR) if lang == FR else "“%s”" % quote[EN]
    roi = "".join('<li><b>%s</b><span>%s</span></li>' % (T(a, lang), T(b, lang)) for a, b in x["roi"])
    proof = ('  <section class="ucp ucv-proof" id="cas">\n'
             '    <div class="shell">\n'
             '      <h2 class="ucp__h2">%s</h2>\n'
             '      <div class="ucv-proof__grid">\n'
             '        <a class="ucv-video" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">\n'
             '          <span class="ucv-video__shot"><img src="https://i.ytimg.com/vi_webp/%s/hqdefault.webp" width="480" height="360" alt="" loading="lazy" decoding="async" /><span class="reel__play" aria-hidden="true"></span><span class="reel__time">%s</span></span>\n'
             '          <span class="ucv-video__q">%s</span>\n'
             '          <span class="ucv-video__who"><b>%s</b> · %s</span>\n'
             '        </a>\n'
             '        <article class="ucv-case">\n'
             '          <p class="ucr-case__tag">%s</p>\n'
             '          <p class="ucv-case__ctx">%s</p>\n'
             '          <p class="ucv-case__found">%s</p>\n'
             '          <p class="ucv-case__reco"><span>%s</span>%s</p>\n'
             '        </article>\n'
             '      </div>\n'
             '      <ul class="ucv-roi">%s</ul>\n'
             '    </div>\n'
             '  </section>') % (T(L["proof_t"], lang), vid, vid, time, esc(vq), esc(brand), esc(who), T(L["illus"], lang),
                                esc(typo(ctx, lang)), esc(typo(found, lang)), T(L["reco"], lang), esc(typo(reco, lang)), roi)

    # 6. the offer, the FAQ with the links beside it, the callback
    siblings = [y for y in C.CASES if y["family"] == c["family"] and y is not c]
    rel = "".join('<li><a href="%s">%s <span aria-hidden="true">→</span></a></li>' % (case_path(y, lang), T(y["name"], lang)) for y in siblings)
    return "\n".join([
        crumbs(items, lang),
        hero,
        problem,
        dlv,
        how,
        proof,
        cta(c, lang).replace('class="ucp ucp--cta"', 'class="ucp ucp--cta ucr-offer"', 1),
        faq_block(c["faq"], lang, further(lang, "rel-" + c["key"], T(L["same"], lang), rel + up_li(f, lang), x["articles"])),
        book(lang),
    ]), items


L.update({
    "contents": ("Dans cette page", "On this page"),
    "see_dlv": ("Voir un livrable possible", "See a possible deliverable"),
    "problem_k": ("La question qu'on nous pose", "The question we get"),
    "now": ("Aujourd'hui, vous voyez", "Today, you see"),
    "missing": ("Ce qui vous manque", "What is missing"),
    "dlv_k": ("Ce que vous recevez", "What you receive"),
    "how_t": ("Comment ça se passe", "How it runs"),
    "days_note": ("Durées indicatives pour une première lecture ; la veille continue démarre dès le cadrage.",
                  "Indicative timings for a first read; continuous monitoring starts as soon as framing is done."),
    "proof_t": ("Ils en parlent, et un cas type", "They talk about it, and a typical case"),
})


def family_body(f, lang):
    cases = [x for x in C.CASES if x["family"] == f["key"]]
    idx = C.FAMILIES.index(f) + 1
    aside = '\n      <div class="ucp__hero-voice">\n%s\n      </div>' % reel(f["video"], lang)
    kicker = '%s<span>0%d · %s</span>' % (icon(FAM_ICON[f["key"]]), idx, T(f["name"], lang))
    vs = "".join('<tr><td>%s</td><td>%s</td></tr>' % (T(a, lang), T(b, lang)) for a, b in VERSUS)
    others = "".join('<li><a href="%s">%s%s <span aria-hidden="true">→</span></a></li>' % (
        fam_path(o, lang), icon(FAM_ICON[o["key"]]), T(o["name"], lang)) for o in C.FAMILIES if o is not f)
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], hub_path(lang)), (f["name"][lang], None)]
    return "\n".join([
        crumbs(items, lang),
        hero(kicker, T(f["h1"], lang), T(f["intro"], lang), lang, aside),
        wheel(f, cases, lang),
        client_block(next((x for x in cases if C.VOICES[C.EXTRA[x["key"]]["voice"]][0] != f["video"][0]), cases[0]), lang),
        cta({"key": f["key"]}, lang),
        faq_block(f["faq"], lang, further(lang, "rel-" + f["key"], T(L["others"], lang), others,
                                          list(dict.fromkeys(a for x in cases for a in C.EXTRA[x["key"]]["articles"]))[:3], ico=True)),
        book(lang),
    ]), items


def wheel(f, cases, lang):
    """the family's three cases: pills on the left, a stack of cards on the
    right, the front card showing the deliverable of that case (js/ui.js
    turns it, and stops as soon as the visitor takes over)"""
    import uc_deliverables as D
    k = f["key"]
    pos = ("is-on", "is-next", "is-prev")
    tabs = "".join(
        '<button class="ucw__tab%s" type="button" role="tab" id="ucw-%s-t%d" aria-controls="ucw-%s-p%d" aria-selected="%s"%s>'
        '<span class="ucw__n">0%d</span><span class="ucw__name">%s</span><i class="ucw__bar" aria-hidden="true"></i></button>' % (
            " is-on" if i == 0 else "", k, i, k, i, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"',
            i + 1, T(x["name"], lang)) for i, x in enumerate(cases))
    cards = "".join(
        '\n        <div class="ucw__card %s" role="tabpanel" id="ucw-%s-p%d" aria-labelledby="ucw-%s-t%d">'
        '<div class="ucw__peek" aria-hidden="true"><div class="ucw__scale">%s</div></div>'
        '<div class="ucw__body"><h3 class="ucw__badge">0%d · %s</h3>'
        '<p class="ucw__q">%s</p>'
        '<p class="ucw__get"><span>%s</span>%s</p>'
        '<a class="ucw__go" href="%s">%s <span aria-hidden="true">→</span></a></div></div>' % (
            pos[i], k, i, k, i, D.render(x["key"], lang, esc, typo), i + 1, T(x["name"], lang),
            esc(typo(("« %s »" if lang == FR else "“%s”") % x["questions"][0][lang], lang)),
            T(L["get"], lang), T(x["deliverables"][0], lang), case_path(x, lang), T(L["read_case"], lang))
        for i, x in enumerate(cases))
    return ('  <section class="ucp ucw">\n'
            '    <div class="shell ucw__grid">\n'
            '      <div class="ucw__side">\n'
            '        <h2 class="xs__title">%s</h2>\n'
            '        <p class="xs__lead">%s</p>\n'
            '        <div class="ucw__tabs" role="tablist" aria-label="%s">%s</div>\n'
            '      </div>\n'
            '      <div class="ucw__stage">%s\n      </div>\n'
            '    </div>\n'
            '  </section>') % (T(L["three"], lang), T(L["wheel_lead"], lang), T(L["three"], lang), tabs, cards)


L.update({
    "wheel_lead": ("Trois questions qu'on nous pose, et le livrable qui répond à chacune.",
                   "Three questions we get, and the deliverable that answers each one."),
})


def families(lang):
    """the four families as a carousel of photo cards: the hub and the home"""
    fams = []
    for i, f in enumerate(C.FAMILIES):
        cases = [x for x in C.CASES if x["family"] == f["key"]]
        links = "".join('<li><a href="%s">%s <i aria-hidden="true">→</i></a></li>' % (case_path(x, lang), T(x["name"], lang)) for x in cases)
        photo = HUB_PHOTO[f["key"]]
        fams.append(
            '        <li class="ucc__card" id="fam-%s">\n'
            '          <img src="/assets/img/team/morning/%s-800.webp" srcset="/assets/img/team/morning/%s-800.webp 800w, /assets/img/team/morning/%s-1600.webp 1600w" sizes="(max-width: 640px) 82vw, 420px" alt="" width="800" height="1197" loading="lazy" decoding="async" />\n'
            '          <div class="ucc__top">\n'
            '            <p class="ucc__k">%s<span>0%d · %s</span></p>\n'
            '            <h3 class="ucc__t"><a href="%s">%s</a></h3>\n'
            '          </div>\n'
            '          <div class="ucc__foot">\n'
            '            <ul class="ucc__cases">%s</ul>\n'
            '            <a class="ucc__all" href="%s">%s <span aria-hidden="true">→</span></a>\n'
            '          </div>\n'
            '        </li>' % (f["key"], photo, photo, photo, icon(FAM_ICON[f["key"]]), i + 1, T(f["name"], lang),
                            fam_path(f, lang), T(f["h1"], lang), links,
                            fam_path(f, lang), esc(typo(L["family_all"][lang] % f["name"][lang], lang))))
    carousel = ('  <section class="ucp ucc" aria-labelledby="ucc-t">\n'
                '    <div class="shell ucc__head">\n'
                '      <div>\n'
                '        <h2 class="xs__title" id="ucc-t">%s</h2>\n'
                '        <p class="xs__lead">%s</p>\n'
                '      </div>\n'
                '      <div class="ucc__nav">\n'
                '        <button class="ucc__btn" type="button" data-dir="-1" aria-label="%s" disabled><span aria-hidden="true">←</span></button>\n'
                '        <button class="ucc__btn" type="button" data-dir="1" aria-label="%s"><span aria-hidden="true">→</span></button>\n'
                '      </div>\n'
                '    </div>\n'
                '    <div class="shell">\n    <ol class="ucc__track">\n%s\n    </ol>\n    </div>\n'
                '  </section>') % (T(L["families"], lang), T(L["fam_lead"], lang), T(L["prev"], lang), T(L["next"], lang), "\n".join(fams))
    return carousel


def hub_body(lang):
    carousel = families(lang)
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], None)]
    return "\n".join([
        crumbs(items, lang),
        hero('<span>%s</span>' % T(C.HUB["kicker"], lang), T(C.HUB["h1"], lang), T(C.HUB["intro"], lang), lang,
             aside=bubbles(lang), actions=True, extra='\n            <a class="ucp__textlink" href="#offre">%s <span aria-hidden="true">↓</span></a>' % T(L["bar_offer"], lang)),
        carousel,
        compare(lang),
        section('      <h2 class="ucp__h2">%s</h2>\n      <div class="ucp__voices">\n%s\n      </div>' % (
            T(L["hub_voices"], lang), "\n".join(reel(C.VOICES[k], lang) for k in ("lvmh", "loreal", "orange")))),
        cta({"key": "hub"}, lang).replace(T(L["cta_t"], lang), T(L["hub_offer_t"], lang), 1),
        faq_block(C.HUB_FAQ, lang, related("hub-more", T(L["by_family"], lang), "".join(
            '<li><a href="%s">%s <span aria-hidden="true">→</span></a></li>' % (fam_path(f, lang), T(f["name"], lang)) for f in C.FAMILIES))),
        book(lang),
    ]), items


HUB_PHOTO = {"communication": "work-three", "brand": "work-table", "audiences": "work-sofa", "trends": "work-laptop"}
L.update({
    "fam_lead": ("Choisissez la famille de votre question, puis le cas qui lui ressemble.",
                 "Pick the family your question belongs to, then the case that looks like it."),
    "prev": ("Famille précédente", "Previous family"),
    "next": ("Famille suivante", "Next family"),
})


def bubbles(lang):
    """the hero's right column: the twelve questions clients ask, drifting
    upwards; each one opens its case. The second copy only closes the loop."""
    items = []
    for x in C.CASES:
        f = FAM[x["family"]]
        q = typo(("« %s »" if lang == FR else "“%s”") % x["questions"][0][lang], lang)
        items.append((case_path(x, lang), icon(FAM_ICON[f["key"]]), T(f["name"], lang), esc(q)))
    one = lambda hidden: "".join(
        '<li><a href="%s"%s><span class="ucq__f">%s%s</span><span class="ucq__q">%s</span></a></li>' % (
            h, ' tabindex="-1"' if hidden else "", ic, fam, q) for h, ic, fam, q in items)
    return ('\n      <div class="ucq">\n'
            '        <p class="visually-hidden">%s</p>\n'
            '        <div class="ucq__win">\n'
            '          <ul class="ucq__list">%s</ul>\n'
            '          <ul class="ucq__list" aria-hidden="true">%s</ul>\n'
            '        </div>\n'
            '      </div>') % (T(L["bubbles_sr"], lang), one(False), one(True))


def compare(lang):
    X = C.COMPARE
    head = "".join('<th scope="col"%s>%s</th>' % (' class="is-us"' if i == 2 else "", T(c, lang)) for i, c in enumerate(X["cols"]))
    rows = "".join('<tr><th scope="row">%s</th>%s</tr>' % (T(r[0], lang), "".join(
        '<td data-l="%s"%s>%s</td>' % (T(X["cols"][i], lang), ' class="is-us"' if i == 2 else "", T(v, lang)) for i, v in enumerate(r[1:])))
        for r in X["rows"])
    return ('  <section class="ucp ucx" aria-labelledby="ucx-t">\n'
            '    <div class="shell">\n'
            '      <div class="xs__head">\n'
            '        <h2 class="xs__title" id="ucx-t">%s</h2>\n'
            '        <p class="xs__lead">%s</p>\n'
            '      </div>\n'
            '      <table class="ucx__table">\n'
            '        <thead><tr><td></td>%s</tr></thead>\n'
            '        <tbody>%s</tbody>\n'
            '      </table>\n'
            '    </div>\n'
            '  </section>') % (T(X["title"], lang), T(X["lead"], lang), head, rows)


L.update({
    "bubbles_sr": ("Les questions que nos clients nous posent :", "The questions our clients ask us:"),
    "by_family": ("Explorer par famille", "Explore by family"),
})


# ------------------------------------------------------------------ extras
# the client logo band of the home, at the foot of every hero
CLIENTS = re.search(r'<div class="clients" id="clients"[^>]*>.*?</div>\s*</div>\s*</div>', (ROOT / "index.html").read_text(), re.S).group(0)
CLIENTS = CLIENTS.replace(' data-reveal', '')


def clients(lang):
    band = CLIENTS.replace('class="clients"', 'class="clients ucp__clients"')
    return translate(band) if lang == FR else band


L.update({
    "approach": ("Notre approche sur ce cas", "Our approach to this case"),
    "roi": ("Ce que ça rapporte", "What it pays back"),
    "roi_k": ("ROI", "ROI"),
    "roi_foot": ("Un forfait mensuel, sans engagement, avec des études illimitées à l'intérieur.",
                 "A fixed monthly fee, no commitment, with unlimited studies inside it."),
    "client": ("Un cas type", "A typical case"),
    "context": ("Le contexte", "The context"),
    "articles": ("Articles liés", "Related articles"),
    "read_article": ("Lire l'article", "Read the article"),
    "blog_k": ("Le blog", "The blog"),
    "voice_more": ("Ils en parlent", "They talk about it"),
    "cta_k": ("Et chez vous ?", "And for you?"),
    "cta_t": ("Recevez un cas réel de ce type, dans votre secteur.", "Get a real case of this kind, in your sector."),
    "cta_d": ("Anonymisé, envoyé par un consultant sous 48 h. Pour voir concrètement ce que la lecture donne chez une entreprise comme la vôtre.",
              "Anonymised, sent by a consultant within 48 hours. To see what the read actually gives for a company like yours."),
    "cta_email": ("E-mail professionnel", "Work email"),
    "cta_sector": ("Votre secteur", "Your sector"),
    "cta_btn": ("Recevoir le cas", "Get the case"),
    "cta_err": ("Saisissez un e-mail professionnel, par exemple nom@entreprise.com.", "Enter a work email, like name@company.com."),
    "cta_done": ("C'est noté. Un consultant vous envoie un cas réel sous 48 h.", "Noted. A consultant sends you a real case within 48 hours."),
    "cta_consent": ("Votre e-mail sert uniquement à vous répondre.", "We use your email only to reply to you."),
    "privacy": ("Politique de confidentialité", "Privacy policy"),
    "cta_pick": ("Choisir…", "Choose…"),
    "cta_pick_err": ("Choisissez votre secteur.", "Choose your sector."),
    "bar_offer": ("Recevoir un cas réel", "Get a real case"),
    "bar_call": ("Être rappelé", "Get a call back"),
    "note_lead": ("Un tableau de bord s'arrête au chiffre. Voici ce que nous remettons à la place : une note, écrite et présentée par le consultant qui a lu la conversation.",
                  "A dashboard stops at the number. Here is what we hand over instead: a note, written and presented by the consultant who read the conversation."),
    "note_stop": ("… et après ?", "… and then?"),
    "note_kind": ("Note d'analyse", "Analysis note"),
    "ann_what": ("ce qui s'est passé", "what happened"),
    "ann_proof": ("la preuve", "the proof"),
    "ann_reco": ("quoi faire", "what to do"),
    "note_by": ("Le consultant qui a mené l'analyse", "The consultant who ran the analysis"),
    "note_sig": ("présentée en rendez-vous, pas envoyée par e-mail", "presented in a meeting, not sent by email"),
    "dash_t": ("Ce que montre un tableau de bord", "What a dashboard shows"),
    "dash_foot": ("À vous d'interpréter.", "Yours to interpret."),
    "note_t": ("Ce que vous remet Licter", "What Licter hands you"),
    "same_case": ("Exemple illustratif : les deux côtés portent sur la même conversation.", "Illustrative example: both sides read the same conversation."),
    "up": ("en hausse", "up"),
    "down": ("en baisse", "down"),
    "hub_voices": ("Ils le racontent mieux que nous", "They tell it better than we do"),
    "hub_offer_t": ("Recevez un cas réel, dans votre secteur.", "Get a real case, in your sector."),
})

SECTORS = [("Agroalimentaire", "Food & drink"), ("Luxe & mode", "Luxury & fashion"), ("Beauté", "Beauty"),
           ("Jouets & jeux vidéo", "Toys & video games"), ("Automobile & mobilité", "Automotive & mobility"),
           ("Banque & assurance", "Banking & insurance"), ("Distribution", "Retail"), ("Secteur public", "Public sector"),
           ("Autre", "Other")]


def cta(c, lang):
    opts = '<option value="" disabled selected>%s</option>' % T(L["cta_pick"], lang) + "".join('<option>%s</option>' % T(s, lang) for s in SECTORS)
    return ('  <!-- MOCK: sends nothing yet (js/home.js, .ucp-lead); wire to the CRM with the case and the sector. -->\n'
            '  <section class="ucp ucp--cta" id="offre">\n'
            '    <div class="shell">\n'
            '      <div class="ucp__cta">\n'
            '        <div class="ucp__cta-copy">\n'
            '          <p class="ucp__cta-k">%s</p>\n'
            '          <h2 class="ucp__cta-t">%s</h2>\n'
            '          <p class="ucp__cta-d">%s</p>\n'
            '        </div>\n'
            '        <form class="ucp-lead" data-case="%s" novalidate>\n'
            '          <div class="ucp-lead__row">\n'
            '            <label class="ucp-lead__f"><span>%s</span><input class="fld__input" name="email" type="email" autocomplete="email" placeholder="%s" required /></label>\n'
            '            <label class="ucp-lead__f"><span>%s</span><select class="fld__input" name="sector" required>%s</select></label>\n'
            '          </div>\n'
            '          <button class="btn btn--primary" type="submit">%s <span aria-hidden="true">→</span></button>\n'
            '          <p class="fld__error" hidden>%s</p>\n'
            '          <p class="fld__error ucp-lead__sector-err" hidden>%s</p>\n'
            '          <p class="consent">%s <a href="/privacy.html">%s</a>.</p>\n'
            '        </form>\n'
            '        <p class="ucp-lead__done" role="status" hidden>%s</p>\n'
            '      </div>\n'
            '    </div>\n'
            '  </section>') % (T(L["cta_k"], lang), T(L["cta_t"], lang), T(L["cta_d"], lang), c["key"],
                               T(L["cta_email"], lang), "nom@entreprise.com" if lang == FR else "name@company.com",
                               T(L["cta_sector"], lang), opts, T(L["cta_btn"], lang), T(L["cta_err"], lang), T(L["cta_pick_err"], lang),
                               T(L["cta_consent"], lang), T(L["privacy"], lang), T(L["cta_done"], lang))


def articles_block(keys, lang):
    cards = "".join('<li><a class="ucp__art" href="/%s"><span class="ucp__art-k">%s</span><b>%s</b>'
                    '<span class="ucp__art-go">%s <span aria-hidden="true">→</span></span></a></li>' % (
                        k, T(L["blog_k"], lang), T(C.ARTICLES[k], lang), T(L["read_article"], lang)) for k in keys)
    return section('      <h2 class="ucp__h2">%s</h2>\n      <ul class="ucp__arts">%s</ul>' % (T(L["articles"], lang), cards))


def voice_card(key, lang):
    return reel(C.VOICES[key], lang).replace(
        '<span class="ucf__voice-k">%s</span>' % T(L["voice"], lang),
        '<span class="ucf__voice-k">%s</span>' % T(L["voice_more"], lang))


def case_extras(c, lang):
    """approach, ROI and client case, in page order"""
    x = C.EXTRA[c["key"]]
    steps = "".join('<li><span class="ucp__dot">%d</span><b>%s</b><p>%s</p></li>' % (i + 1, T(C.STEPS[i], lang), T(s, lang))
                    for i, s in enumerate(c["steps"]))
    approach = section('      <h2 class="ucp__h2">%s</h2>\n      <p class="ucp__approach">%s</p>\n      <ol class="ucp__steps">%s</ol>' % (
        T(L["approach"], lang), T(x["approach"], lang), steps))
    roi = "".join('<li><span class="ucp__roi-n">0%d</span><b>%s</b><p>%s</p></li>' % (i + 1, T(a, lang), T(b, lang))
                  for i, (a, b) in enumerate(x["roi"]))
    roi_sec = ('  <section class="ucp ucp--roi">\n'
               '    <div class="shell">\n'
               '      <div class="ucp__roi">\n'
               '        <div class="ucp__roi-head"><p class="ucp__roi-k">%s</p><h2 class="ucp__h2">%s</h2>%s</div>\n'
               '        <ol class="ucp__roi-list">%s</ol>\n'
               '      </div>\n'
               '    </div>\n'
               '  </section>') % (T(L["roi_k"], lang), T(L["roi"], lang),
                                  "" if any("forfait" in b[FR] for a, b in x["roi"]) else '<p class="ucp__roi-foot">%s</p>' % T(L["roi_foot"], lang),
                                  roi)
    ctx, rest = split_context(c["example"][lang])
    sit_rec = split_example(rest)
    case = ('      <h2 class="ucp__h2">%s</h2>\n'
            '      <div class="ucp__client">\n'
            '        <article class="ucp__case">\n'
            '          <p class="ucp__case-k">%s</p>\n'
            '          <p class="ucp__case-h">%s</p><p class="ucp__case-ctx">%s</p>\n'
            '          <div class="ucp__case-cols">\n'
            '            <div><p class="ucp__case-h">%s</p><p>%s</p></div>\n'
            '            <div class="ucp__case-reco"><p class="ucp__case-h">%s</p><p>%s</p></div>\n'
            '          </div>\n'
            '        </article>\n'
            '%s\n'
            '      </div>') % (T(L["client"], lang), T(L["illus"], lang), T(L["context"], lang), esc(typo(ctx, lang)),
                              T(L["found"], lang), esc(typo(sit_rec[0], lang)), T(L["reco"], lang), esc(typo(sit_rec[1], lang)),
                              voice_card(x["voice"], lang))
    return [approach, roi_sec, section(case)]


L.update({
    "recognise": ("Vous vous posez ces questions ?", "Are these your questions?"),
    "see_case": ("Voir un cas type", "See a typical case"),
    "further": ("Pour aller plus loin", "Going further"),
    "sources_k": ("Ce que nous lisons", "What we read"),
})


def roi_block(c, lang):
    return case_extras(c, lang)[1]


def client_block(c, lang):
    return case_extras(c, lang)[2].replace('<section class="ucp">', '<section class="ucp" id="cas-client">', 1)


def how_block(c, lang, src):
    """the approach, its four steps and the sources, in one place"""
    return case_extras(c, lang)[0].replace(
        '</ol>\n    </div>',
        '</ol>\n      <h3 class="ucp__h3">%s</h3>\n      <ul class="ucp__sources">%s</ul>\n    </div>' % (T(L["sources_k"], lang), src), 1)


def up_li(f, lang):
    return '<li class="ucp__up-li"><a href="%s">%s <span aria-hidden="true">→</span></a></li>' % (
        fam_path(f, lang), esc(typo(L["family_all"][lang] % f["name"][lang], lang)))


def further(lang, rid, title, links, arts, ico=False):
    """beside the FAQ: the neighbouring pages, then the related articles"""
    art = "".join('<li><a class="ucp__art-l" href="/%s"><span>%s</span>%s <span aria-hidden="true">→</span></a></li>' % (
        k, T(L["blog_k"], lang), T(C.ARTICLES[k], lang)) for k in arts)
    return ('      <aside class="ucp__related%s" aria-labelledby="%s">\n'
            '        <h2 class="ucp__h2" id="%s">%s</h2>\n'
            '        <ul>%s</ul>\n'
            '        <h2 class="ucp__h2 ucp__h2--sub">%s</h2>\n'
            '        <ul class="ucp__arts-l">%s</ul>\n'
            '      </aside>') % (" ucp__related--ico" if ico else "", rid, rid, title, links, T(L["articles"], lang), art)


def split_context(text):
    """first sentence = the context, the rest = what was found and done"""
    t = re.sub(r"^(Exemple illustratif|Illustrative example)\s*:\s*", "", text)
    m = re.match(r"(.+?[.])\s+(.*)$", t)
    cap = lambda s: s[:1].upper() + s[1:]
    return (cap(m.group(1)), m.group(2)) if m else (cap(t), "")


# ------------------------------------------------------------------- build
def main():
    urls = []   # (fr_path, en_path)
    for lang in (FR, EN):
        body, items = hub_body(lang)
        ld = [breadcrumb_ld([(a, b or hub_path(lang)) for a, b in items]),
              {"@context": "https://schema.org", "@type": "CollectionPage", "name": typo(C.HUB["h1"][lang], lang),
               "url": SITE + hub_path(lang), "inLanguage": LANGS[lang], "publisher": ORG},
              faq_ld(C.HUB_FAQ, lang)]
        write(hub_path(lang), page(lang, hub_path(lang), hub_path(1 - lang), C.HUB["seo_title"][lang], C.HUB["meta"][lang], body, ld))
    urls.append((hub_path(FR), hub_path(EN)))

    for f in C.FAMILIES:
        for lang in (FR, EN):
            body, items = family_body(f, lang)
            ld = [breadcrumb_ld([(a, b or fam_path(f, lang)) for a, b in items]), faq_ld(f["faq"], lang)]
            write(fam_path(f, lang), page(lang, fam_path(f, lang), fam_path(f, 1 - lang), f["seo_title"][lang], f["meta"][lang], body, ld, og_image=f["key"]))
        urls.append((fam_path(f, FR), fam_path(f, EN)))

    for c in C.CASES:
        for lang in (FR, EN):
            body, items = case_body(c, lang)
            ld = [breadcrumb_ld([(a, b or case_path(c, lang)) for a, b in items]),
                  {"@context": "https://schema.org", "@type": "Service", "name": typo(c["name"][lang], lang),
                   "description": typo(c["meta"][lang], lang), "serviceType": FAM[c["family"]]["name"][lang],
                   "provider": ORG, "areaServed": "FR", "inLanguage": LANGS[lang], "url": SITE + case_path(c, lang)},
                  faq_ld(c["faq"], lang)]
            write(case_path(c, lang), page(lang, case_path(c, lang), case_path(c, 1 - lang), c["seo_title"][lang], c["meta"][lang], body, ld, og_type="article", og_image=c["family"]))
        urls.append((case_path(c, FR), case_path(c, EN)))

    # sitemap: the site's pages, and every use-case page with its twin
    root_pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in ("404.html", "use-cases.html"))
    entries = []
    for name in root_pages:
        if name == "index.html":
            continue   # the home goes in with its French twin, below
        entries.append("  <url><loc>%s</loc></url>" % (SITE + "/" + name))
    urls.insert(0, ("/fr/", "/"))
    for fr_p, en_p in urls:
        for p in (fr_p, en_p):
            entries.append('''  <url><loc>{s}{p}</loc>
    <xhtml:link rel="alternate" hreflang="fr" href="{s}{fr}" />
    <xhtml:link rel="alternate" hreflang="en" href="{s}{en}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{s}{fr}" />
  </url>'''.format(s=SITE, p=p, fr=fr_p, en=en_p))
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    print("%d use-case pages written (FR + EN), sitemap.xml, robots.txt" % ((len(urls) - 1) * 2))

if __name__ == "__main__":
    # the offer pages first: they write their French into js/fr.js, which the
    # shared header and footer of the pages below are translated with
    import runpy
    runpy.run_path(str(ROOT / "tools" / "build-offers.py"), run_name="__main__")
    DICT.update(fr_dict())
    main()
    # the home in both languages, from the same dictionary
    runpy.run_path(str(ROOT / "tools" / "build-home.py"), run_name="__main__")
