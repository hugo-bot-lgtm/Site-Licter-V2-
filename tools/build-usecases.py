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
import html, json, pathlib, re, subprocess, sys

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
    "example": ("Un exemple, en direct", "An example, live"),
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
            <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" decoding="async" />
            <span class="reel__play" aria-hidden="true"></span>
            <span class="reel__time">{time}</span>
          </span>
          <span class="ucf__voice-k">{T(L["voice"], lang)}</span>
          <span class="reel__quote">{esc(q)}</span>
          <span class="reel__meta"><b class="reel__brand">{esc(brand)}</b> <em class="reel__who">{esc(who)}</em></span>
        </a>'''

# ------------------------------------------------------------------- page
def page(lang, path, alt_path, title, meta, body, ld, og_type="website"):
    v = version()
    other = 1 - lang
    fr_path, en_path = (path, alt_path) if lang == FR else (alt_path, path)
    ld_tags = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    scripts = ([f'<script src="/js/fr.js?v={v}"></script>'] if lang == FR else []) + [
        f'<script src="/js/i18n.js?v={v}"></script>',
        f'<script src="/js/communities.js?v={v}"></script>',
        f'<script src="/js/ui.js?v={v}"></script>',
        f'<script src="/js/usecases.js?v={v}"></script>',
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
<meta name="twitter:card" content="summary" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet" />
<meta name="theme-color" content="#FCF6EF" />
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
def head_block(kicker, h1, intro, lang, actions=True, cls="ucp__head"):
    act = ""
    if actions:
        act = f'''
        <div class="page__actions">
          <a class="btn btn--primary" href="#book">{T(L["book"], lang)} <span aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="#live">{T(L["live"], lang)}</a>
        </div>'''
    return f'''  <section class="page {cls}">
    <div class="shell">
      <div class="page__head">
        <p class="page__eyebrow"><span class="rule" aria-hidden="true"></span>{kicker}</p>
        <h1 class="page__title ucp__title">{h1}</h1>
        <p class="page__lead">{intro}</p>{act}
      </div>
    </div>
  </section>'''

def case_body(c, lang):
    f = FAM[c["family"]]
    n = C.CASES.index(c) % 3 + 1
    qs = "".join("<li>%s</li>" % T(q, lang) for q in c["questions"])
    gets = "".join("<li>%s</li>" % T(g, lang) for g in c["deliverables"])
    src = "".join('<li><b>%s</b><span>%s</span></li>' % (T(a, lang), T(b, lang)) for a, b in c["sources"])
    steps = "".join('<li><span class="ucp__n">0%d</span><b>%s</b><p>%s</p></li>' % (i + 1, T(C.STEPS[i], lang), T(s, lang))
                    for i, s in enumerate(c["steps"]))
    siblings = [x for x in C.CASES if x["family"] == c["family"] and x is not c]
    rel = "".join('<li><a href="%s">%s <span aria-hidden="true">→</span></a></li>' % (case_path(x, lang), T(x["name"], lang)) for x in siblings)
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], hub_path(lang)), (f["name"][lang], fam_path(f, lang)), (c["name"][lang], None)]
    return "\n".join([
        crumbs(items, lang),
        head_block("%s · 0%d" % (T(f["name"], lang), n), T(c["h1"], lang), T(c["intro"], lang), lang),
        f'''  <section class="ucp">
    <div class="shell ucp__cols">
      <div class="ucp__block">
        <h2 class="ucp__h2">{T(L["questions"], lang)}</h2>
        <ul class="ucp__qs">{qs}</ul>
      </div>
      <div class="ucp__block ucp__block--get">
        <h2 class="ucp__h2">{T(L["get"], lang)}</h2>
        <ul class="ucp__ticks">{gets}</ul>
      </div>
    </div>
  </section>
  <section class="ucp">
    <div class="shell">
      <h2 class="ucp__h2">{T(L["read"], lang)}</h2>
      <ul class="ucp__sources">{src}</ul>
    </div>
  </section>
  <section class="ucp">
    <div class="shell">
      <h2 class="ucp__h2">{T(L["how"], lang)}</h2>
      <ol class="ucp__steps">{steps}</ol>
    </div>
  </section>
  <section class="ucp" id="live">
    <div class="shell">
      <h2 class="ucp__h2">{T(L["example"], lang)}</h2>
      <p class="ucp__example">{T(c["example"], lang)}</p>
{stage(f["key"], lang)}
      <p class="ucp__note">{T(L["example_note"], lang)}</p>
    </div>
  </section>
  <section class="ucp">
    <div class="shell ucp__cols ucp__cols--faq">
      <div>
        <h2 class="ucp__h2">{T(L["faq"], lang)}</h2>
        <div class="faq">{faq_html(c["faq"], lang)}</div>
      </div>
      <aside class="ucp__related" aria-labelledby="rel-{c["key"]}">
        <h2 class="ucp__h2" id="rel-{c["key"]}">{T(L["same"], lang)}</h2>
        <ul>{rel}</ul>
        <a class="ucp__up" href="{fam_path(f, lang)}">{esc(typo(L["family_all"][lang] % f["name"][lang], lang))} <span aria-hidden="true">→</span></a>
      </aside>
    </div>
  </section>''',
        book(lang),
    ]), items

def family_body(f, lang):
    cases = [x for x in C.CASES if x["family"] == f["key"]]
    idx = C.FAMILIES.index(f) + 1
    cards = "".join(f'''
        <li><a class="ucp__card" href="{case_path(x, lang)}">
          <span class="ucp__n">0{i + 1}</span>
          <b class="ucp__card-t">{T(x["name"], lang)}</b>
          <span class="ucp__card-d">{T(x["meta"], lang)}</span>
          <span class="ucp__card-get">{T(x["deliverables"][0], lang)}</span>
          <span class="ucp__card-go">{T(L["read_case"], lang)} <span aria-hidden="true">→</span></span>
        </a></li>''' for i, x in enumerate(cases))
    others = "".join('<li><a href="%s">%s <span aria-hidden="true">→</span></a></li>' % (fam_path(o, lang), T(o["name"], lang))
                     for o in C.FAMILIES if o is not f)
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], hub_path(lang)), (f["name"][lang], None)]
    return "\n".join([
        crumbs(items, lang),
        head_block("0%d · %s" % (idx, T(f["name"], lang)), T(f["h1"], lang), T(f["intro"], lang), lang),
        f'''  <section class="ucp" id="live">
    <div class="shell">
{stage(f["key"], lang)}
      <p class="ucp__note">{T(L["example_note"], lang)}</p>
    </div>
  </section>
  <section class="ucp">
    <div class="shell">
      <h2 class="ucp__h2">{T(L["three"], lang)}</h2>
      <ul class="ucp__cards">{cards}
      </ul>
    </div>
  </section>
  <section class="ucp">
    <div class="shell ucp__cols ucp__cols--why">
      <div>
        <h2 class="ucp__h2">{T(L["why"], lang)}</h2>
        <p class="ucp__why">{T(f["why"], lang)}</p>
      </div>
{reel(f["video"], lang)}
    </div>
  </section>
  <section class="ucp">
    <div class="shell ucp__cols ucp__cols--faq">
      <div>
        <h2 class="ucp__h2">{T(L["faq"], lang)}</h2>
        <div class="faq">{faq_html(f["faq"], lang)}</div>
      </div>
      <aside class="ucp__related" aria-labelledby="rel-{f["key"]}">
        <h2 class="ucp__h2" id="rel-{f["key"]}">{T(L["others"], lang)}</h2>
        <ul>{others}</ul>
      </aside>
    </div>
  </section>''',
        book(lang),
    ]), items

def hub_body(lang):
    fams = []
    for i, f in enumerate(C.FAMILIES):
        cases = [x for x in C.CASES if x["family"] == f["key"]]
        links = "".join('<li><a href="%s"><b>%s</b><span>%s</span></a></li>' % (case_path(x, lang), T(x["name"], lang), T(x["meta"], lang)) for x in cases)
        fams.append(f'''      <li class="ucp__fam">
        <div class="ucp__fam-head">
          <p class="ucf__kicker"><span>0{i + 1}</span>{T(f["name"], lang)}</p>
          <h2 class="ucp__fam-t"><a href="{fam_path(f, lang)}">{T(f["h1"], lang)}</a></h2>
          <p class="ucp__fam-d">{T(f["intro"], lang)}</p>
        </div>
        <ul class="ucp__fam-cases">{links}</ul>
      </li>''')
    items = [(L["home"][lang], "/"), (C.HUB["kicker"][lang], None)]
    return "\n".join([
        crumbs(items, lang),
        head_block(T(C.HUB["kicker"], lang), T(C.HUB["h1"], lang), T(C.HUB["intro"], lang), lang, actions=False),
        f'''  <section class="ucp">
    <div class="shell">
      <h2 class="visually-hidden">{T(L["families"], lang)}</h2>
      <ol class="ucp__fams">
{chr(10).join(fams)}
      </ol>
    </div>
  </section>''',
        book(lang),
    ]), items

# ------------------------------------------------------------------- build
def main():
    urls = []   # (fr_path, en_path)
    for lang in (FR, EN):
        body, items = hub_body(lang)
        ld = [breadcrumb_ld([(a, b or hub_path(lang)) for a, b in items]),
              {"@context": "https://schema.org", "@type": "CollectionPage", "name": typo(C.HUB["h1"][lang], lang),
               "url": SITE + hub_path(lang), "inLanguage": LANGS[lang], "publisher": ORG}]
        write(hub_path(lang), page(lang, hub_path(lang), hub_path(1 - lang), C.HUB["seo_title"][lang], C.HUB["meta"][lang], body, ld))
    urls.append((hub_path(FR), hub_path(EN)))

    for f in C.FAMILIES:
        for lang in (FR, EN):
            body, items = family_body(f, lang)
            ld = [breadcrumb_ld([(a, b or fam_path(f, lang)) for a, b in items]), faq_ld(f["faq"], lang)]
            write(fam_path(f, lang), page(lang, fam_path(f, lang), fam_path(f, 1 - lang), f["seo_title"][lang], f["meta"][lang], body, ld))
        urls.append((fam_path(f, FR), fam_path(f, EN)))

    for c in C.CASES:
        for lang in (FR, EN):
            body, items = case_body(c, lang)
            ld = [breadcrumb_ld([(a, b or case_path(c, lang)) for a, b in items]),
                  {"@context": "https://schema.org", "@type": "Service", "name": typo(c["name"][lang], lang),
                   "description": typo(c["meta"][lang], lang), "serviceType": FAM[c["family"]]["name"][lang],
                   "provider": ORG, "areaServed": "FR", "inLanguage": LANGS[lang], "url": SITE + case_path(c, lang)},
                  faq_ld(c["faq"], lang)]
            write(case_path(c, lang), page(lang, case_path(c, lang), case_path(c, 1 - lang), c["seo_title"][lang], c["meta"][lang], body, ld))
        urls.append((case_path(c, FR), case_path(c, EN)))

    # sitemap: the site's pages, and every use-case page with its twin
    root_pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in ("404.html", "use-cases.html"))
    entries = []
    for name in root_pages:
        loc = SITE + ("/" if name == "index.html" else "/" + name)
        entries.append("  <url><loc>%s</loc></url>" % loc)
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
    print("%d pages written (%d use-case pages x 2 languages), sitemap.xml, robots.txt" % (len(urls) * 2, len(urls)))

if __name__ == "__main__":
    main()
