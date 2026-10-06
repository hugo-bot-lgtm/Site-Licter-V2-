#!/usr/bin/env python3
"""Builds the tool pages and the network pages, in English and French:

    tech-<tool>.html        and /fr/outils/<tool>/     (13 tools, tools/tools_data.py)
    source-<network>.html   and /fr/sources/<network>/ (22 networks, tools/networks.py)

plus the SEO head and the French twin of tech-tools.html (/fr/outils/).

Every page follows one SEO structure: a keyword H1 ("Agence X", "Social
listening X"), question-shaped H2s (What is X? Why work with an X agency?
What we collect on X...), a FAQ marked up as FAQPage, and links to the
other tools and networks. The shell (head, header, footer) comes from
tools/tech-shell.html. The French of every string goes to its own block of
js/fr.js.

Run by tools/build-usecases.py (before the sitemap), or on its own:

    python3 tools/build-tech.py

MOCK: the descriptions say how Licter uses each tool; to be validated by
Licter (A-FAIRE.md, section 5).
"""
import html, importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bo", ROOT / "tools" / "build-offers.py")
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
U, C = O.U, O.C
FR, EN = 0, 1
t, a = O.t, O.a

S = {
    "kick": ("TECHNO & OUTILS", "TECH & TOOLS"),
    "all": ("Voir tous nos outils", "See all our tools"),
    "book": ("Prendre rendez-vous", "Book a meeting"),
    "steps_k": ("NOTRE APPROCHE EN TROIS ÉTAPES", "OUR APPROACH IN THREE STEPS"),
    "steps_t": ("Comment nous l'utilisons.", "How we put it to work."),
    "steps_lead": ("Trois étapes entre votre question et une lecture sur laquelle agir, les mêmes quel que soit l'outil qui y répond.",
                   "Three steps between your question and a readout you can act on, the same three whichever tool answers it."),
    "steps": [(("Cadrage", "Framing"), ("Nous partons de la décision à prendre, pas d'une liste de mots-clés : le périmètre suit la question.",
                                        "We start from the decision to make, not from a keyword list: the perimeter follows the question.")),
              (("Collecte", "Collection"), ("Requêtes, sources, langues et périodes, réglées par les consultants qui liront eux-mêmes le résultat.",
                                            "Queries, sources, languages and periods, set by the consultants who will read the output themselves.")),
              (("Lecture", "Reading"), ("Une analyse croisée avec nos autres sources, et une recommandation que vos équipes peuvent appliquer.",
                                        "An analysis crossed with our other sources, and a recommendation your teams can act on."))],
    "strengths_t": ("Ce qu'il apporte à la lecture.", "What it brings to the reading."),
    "sol_k": ("CE QUE NOUS LIVRONS AVEC", "WHAT WE DELIVER WITH IT"),
    "sol_t": ("Ce que nous livrons concrètement.", "What we actually deliver on it."),
    "uses_k": ("LES QUESTIONS QU'IL ÉCLAIRE", "THE QUESTIONS IT ANSWERS"),
    "uses_t": ("Les cas d'usage où il compte.", "The use cases where it counts."),
    "uses_lead": ("Chaque carte mène au cas d'usage auquel il contribue.", "Each card leads to the use case it contributes to."),
    "see_case": ("Voir le cas d'usage →", "See the use case →"),
    "faq_k": ("FAQ", "FAQ"),
    "act_k": ("PASSER À L'ACTION", "TIME TO ACT"),
    "diag": ("Demander un diagnostic", "Request a diagnostic"),
    "expert": ("Parler à un expert", "Talk to an expert"),
    "cta_text": ("Envoyez-nous la question. Si un autre outil y répond mieux, nous vous le dirons : nous en utilisons une quinzaine.",
                 "Send us the question. If another tool answers it better, we will tell you: we use about fifteen."),
}

FAMILY = {f["key"]: f for f in C.FAMILIES}
CASES = {c["key"]: c for c in C.CASES}

sys.path.insert(0, str(ROOT / "tools"))
from tools_data import TOOLS          # noqa: E402
from networks import NETWORKS         # noqa: E402
TOOL = {x["slug"]: x for x in TOOLS}
NET = {n["slug"]: n for n in NETWORKS}

S.update({
    "net_kick": ("D'OÙ VIENNENT LES DONNÉES", "WHERE THE DATA COMES FROM"),
    "what_k": ("%s EN BREF", "%s AT A GLANCE"),
    "what_t": ("Qu'est-ce que %s ?", "What is %s?"),
    "feat_k": ("CE QU'IL PERMET", "WHAT IT DOES"),
    "feat_t": ("Ce que %s permet d'analyser.", "What %s lets you analyse."),
    "ag_t": ("Pourquoi passer par une agence %s ?", "Why work with a %s agency?"),
    "ag_lead": ("%s fournit des données. Une agence %s comme Licter en tire une décision : voici comment nous l'utilisons.",
                "%s provides data. A %s agency like Licter turns it into a decision: here is how we use it."),
    "del_k": ("CE QUE NOUS LIVRONS", "WHAT WE DELIVER"),
    "del_t": ("Ce que nous livrons avec %s.", "What we deliver with %s."),
    "uses_k2": ("CAS D'USAGE", "USE CASES"),
    "uses_t2": ("%s : les cas d'usage où il compte.", "%s: the use cases where it counts."),
    "lim_k": ("LIMITES ET COMPLÉMENTS", "LIMITS AND COMPLEMENTS"),
    "lim_t": ("Les limites de %s, et comment nous les compensons.", "The limits of %s, and how we make up for them."),
    "pair": ("Nous le croisons avec", "We cross it with"),
    "faq_t2": ("Questions fréquentes sur %s.", "Frequently asked questions about %s."),
    "nwhy_k": ("POURQUOI %s", "WHY %s"),
    "nwhy_t": ("Pourquoi écouter %s ?", "Why listen to %s?"),
    "nacc_k": ("DONNÉES ET LIMITES", "DATA AND LIMITS"),
    "nacc_t": ("Ce que nous collectons sur %s, et ce que nous ne lisons pas.", "What we collect on %s, and what we do not read."),
    "nacc_yes": ("CE QUE NOUS COLLECTONS", "WHAT WE COLLECT"),
    "nacc_no": ("CE QUE NOUS NE LISONS PAS", "WHAT WE DO NOT READ"),
    "nmet_k": ("MÉTHODE", "METHOD"),
    "nmet_t": ("Comment nous écoutons %s.", "How we listen to %s."),
    "nmet_tools": ("Les outils que nous croisons sur %s", "The tools we cross on %s"),
    "nuses_t": ("Social listening %s : les cas d'usage.", "%s social listening: use cases."),
    "noth_k": ("TOUS LES RÉSEAUX", "EVERY NETWORK"),
    "noth_t": ("Les autres réseaux que nous écoutons.", "The other networks we listen to."),
    "nfaq_t": ("Questions fréquentes sur le social listening %s.", "Social listening on %s: frequently asked questions."),
})


TINT = {"communication": "amber", "brand": "slate", "audiences": "mute", "trends": "ochre"}

# Every tool page says "agence <tool>" several times, for search: in its
# title, its description, its kicker, a question of its FAQ and its last
# call to action. Licter operates these tools; it is not their publisher, and
# the FAQ says so.
SHORT = {
    "talkwalker": ("écoute sociale opérée par des consultants", "social listening run by consultants"),
    "visibrain": ("veille temps réel et alertes", "real-time monitoring and alerts"),
    "youscan": ("écoute visuelle des réseaux sociaux", "visual social listening"),
    "soprism": ("analyse des audiences", "audience intelligence"),
    "radarly": ("suivi de marque et écoute sociale", "brand tracking and social listening"),
    "semrush": ("écoute de la recherche", "search listening"),
    "google-trends": ("lire les tendances de recherche", "reading search trends"),
    "answerthepublic": ("les questions de votre marché", "your market's questions"),
    "chatgpt": ("ce que l'IA dit de votre marque", "what AI says about your brand"),
    "geo": ("votre visibilité dans les réponses des IA", "your visibility in AI answers"),
    "meta-ads": ("veille publicitaire sur Meta", "Meta ad monitoring"),
    "google-news": ("la presse face au social", "the press against social"),
    "social-blade": ("vérifier les comptes et les créateurs", "checking accounts and creators"),
}
HUB = {"title": ("Techno & outils : nos plateformes d'écoute et nos sources | Licter", "Tech & tools: our listening platforms and data sources | Licter"),
       "desc": ("Les plateformes d'écoute que Licter opère, les outils de recherche, de presse et d'IA qui les complètent, et les 22 réseaux d'où viennent les données.",
                "The listening platforms Licter runs, the search, press and AI tools around them, and the 22 networks the data comes from.")}


def agency(slug, name, fr_name=None):
    """the agency wording of one tool page, in both languages"""
    fn = fr_name or name
    sh = SHORT[slug]
    return {
        "title": ("Agence %s : %s | Licter" % (fn, sh[FR]), "%s agency: %s | Licter" % (name, sh[EN])),
        "desc": ("Licter, agence %s : %s. Nos consultants configurent l'outil, lisent les données et vous livrent une recommandation, pas un tableau de bord." % (fn, sh[FR]),
                 "Licter, %s agency: %s. Our consultants set the tool up, read the data and deliver a recommendation, not a dashboard." % (name, sh[EN])),
        "kick": ("AGENCE %s" % fn.upper(), "%s AGENCY" % name.upper()),
        "q": ("Licter est-elle une agence %s ?" % fn, "Is Licter a %s agency?" % name),
        "a": ("Oui : en tant qu'agence %s, nous opérons l'outil pour nos clients, nous le configurons, le lisons et livrons l'analyse. Licter n'en est pas l'éditeur ; nous sommes un cabinet indépendant, qui choisit l'outil selon la question." % fn,
              "Yes: as a %s agency, we run the tool for our clients, set it up, read it and deliver the analysis. Licter is not its publisher; we are an independent consultancy that picks the tool by the question." % name),
        "band": ("Vous cherchez une agence %s ?" % fn, "Looking for a %s agency?" % name),
    }




def agency_net(n):
    """the agency wording of one network page: a social listening agency,
    not an agency that runs your accounts"""
    nm, tag = n["name"], n["tag"]
    return {
        "title": ("Agence social listening %s : %s | Licter" % (nm, tag[FR]), "%s social listening agency: %s | Licter" % (nm, tag[EN])),
        "desc": ("Licter, agence social listening %s : %s. Nos consultants écoutent %s et vous livrent une recommandation, pas un export." % (nm, tag[FR], nm),
                 "Licter, %s social listening agency: %s. Our consultants listen to %s and deliver a recommendation, not an export." % (nm, tag[EN], nm)),
        "q": ("Licter est-elle une agence social listening %s ?" % nm, "Is Licter a %s social listening agency?" % nm),
        "a": ("Oui : nous écoutons %s pour nos clients, avec les plateformes adaptées, et nos consultants lisent ce qui s'y dit. Nous ne gérons ni vos comptes ni vos publicités : nous lisons la conversation et vous disons quoi décider." % nm,
              "Yes: we listen to %s for our clients, with the right platforms, and our consultants read what is said there. We do not run your accounts or your ads: we read the conversation and tell you what to decide." % nm),
        "band": ("Vous cherchez une agence social listening %s ?" % nm, "Looking for a %s social listening agency?" % nm),
    }


def fmt(pair, *args):
    """a pair of templates, each filled with the same-language arguments"""
    return tuple(p % tuple(x[i] for x in args) for i, p in enumerate(pair))


def block(id_, kick, title, inner, lead=None):
    return ('      <section class="block" id="%s">\n        <div class="block__head" data-dim data-reveal>\n'
            '          <p class="block__kicker block__kicker--slash"><i>//</i>%s</p>\n          <h2 class="block__title">%s</h2>\n%s'
            '        </div>\n%s\n      </section>\n\n') % (id_, kick, title, ('          <p class="block__lead">%s</p>\n' % lead) if lead else "", inner)


def card_grid(items, two=False):
    return '        <div class="grid%s">%s</div>' % (" grid--two" if two else "", "".join(
        '<article class="card card--hover" data-reveal><span class="card__num">0%d</span><h3 class="card__title">%s</h3><p class="card__text">%s</p></article>' % (
            i + 1, t(ti), t(tx)) for i, (ti, tx) in enumerate(items)))


FLOW_ITEM = """          <li class="flow__item" data-reveal style="--d:%dms">
            <span class="flow__n" aria-hidden="true">%d</span>
            <div class="flow__card">
              <h3 class="flow__title"><span class="flow__tick" aria-hidden="true"></span>%s</h3>
              <p class="flow__text">%s</p>
            </div>
          </li>
"""


def flow():
    return '        <ol class="flow">\n' + "".join(FLOW_ITEM % (i * 90, i + 1, t(ti), t(tx)) for i, (ti, tx) in enumerate(S["steps"])) + "        </ol>"


def covers(keys):
    out = ""
    for key in keys:
        c = CASES[key]; f = FAMILY[c["family"]]
        fam = (f["name"][FR].upper(), f["name"][EN].upper())
        out += ('<a class="cover-card cover-card--%s" href="%s" data-en="%s" data-reveal>'
                '<span class="cover"><span class="cover__kicker">%s</span><span class="cover__title">%s</span></span>'
                '<span class="cover-card__body"><span class="cover-card__label">%s</span><h3 class="cover-card__title">%s</h3>'
                '<span class="cover-card__link">%s</span></span></a>') % (
            TINT[c["family"]], U.case_path(c, FR), U.case_path(c, EN), t(("// " + fam[FR], "// " + fam[EN])),
            t((c["name"][FR].upper(), c["name"][EN].upper())), t(fam), t(c["name"]), t(S["see_case"]))
    return '        <div class="covers covers--three">%s</div>' % out


def faq(items):
    return '        <div class="faq" data-dim data-reveal>%s</div>' % "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in items)


def chips(items):
    """links to other pages, each with a glyph or a monogram"""
    return '<ul class="tchips">%s</ul>' % "".join(
        '<li><a href="%s">%s<span>%s</span></a></li>' % (href, mark, t(name) if isinstance(name, tuple) else html.escape(name)) for href, mark, name in items)


def tool_chip(slug):
    x = TOOL[slug]
    return ("tech-%s.html" % slug, '<span class="tchips__mono" aria-hidden="true">%s</span>' % x["letter"], (x.get("fr_name", x["name"]), x["name"]))


def net_chip(slug):
    n = NET[slug]
    return ("source-%s.html" % slug, '<i class="xt__glyph" style="--g:url(/assets/img/networks/%s.svg)" aria-hidden="true"></i>' % n["glyph"], n["name"])


TAIL = """      <section class="band" data-reveal>
        <div>
          <p class="block__kicker block__kicker--slash"><i>//</i>%(act)s</p>
          <h2 class="band__title">%(band)s</h2>
        </div>
        <div class="band__actions">
          <a class="btn btn--solid" href="diagnostic.html">%(diag)s <span aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="book-a-meeting.html">%(expert)s <span aria-hidden="true">→</span></a>
        </div>
      </section>

      <section class="cta" data-reveal>
        <h2 class="cta__title">%(cta)s</h2>
        <p class="cta__text">%(cta_text)s</p>
        <form class="signup" novalidate>
          <label class="visually-hidden" for="email-%(slug)s">Your work email</label>
          <input class="signup__input" id="email-%(slug)s" name="email" type="email"
                 placeholder="Your work email..." autocomplete="email" required />
          <button class="signup__btn" type="submit">BOOK A MEETING</button>
        </form>
        <p class="consent">We use your email only to reply to you. <a href="privacy.html">Privacy policy</a>.</p>
        <p class="signup__note" role="status">
          <span class="signup__check" aria-hidden="true">✓</span>
          NOTED - WE GET BACK TO YOU WITHIN 24 HOURS
        </p>
      </section>
    </div>
  </section>
</main>"""

HEAD = """<main id="content">
  <section class="page">
    <div class="shell">
      <div class="page__head">
        <p class="page__eyebrow" data-dim data-reveal><span class="rule" aria-hidden="true"></span>%(eyebrow)s</p>
        <h1 class="%(cls)s" data-dim data-reveal>%(h1)s</h1>
        <p class="page__lead" data-dim data-reveal>%(lead)s</p>
        <div class="page__actions" data-reveal>
          <a class="btn btn--primary" href="book-a-meeting.html">%(book)s <span aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="%(ghost_href)s">%(ghost)s</a>
        </div>
      </div>

"""


def head_block(eyebrow, h1, lead, ghost_href, ghost, fr_h1=""):
    # a word of more than 12 letters (ANSWERTHEPUBLIC, PROFESSIONNELLE) does not fit a phone at the usual size
    words = re.sub(r"<[^>]+>|&[a-z]+;", " ", h1 + " " + fr_h1).replace(",", " ").replace(".", " ").split()
    cls = "page__title page__title--long" if max(len(w) for w in words) > 12 else "page__title"
    return HEAD % {"eyebrow": eyebrow, "h1": h1, "lead": lead, "book": t(S["book"]), "ghost_href": ghost_href, "ghost": t(ghost), "cls": cls}


def tail_block(band, cta, slug):
    return TAIL % {"act": t(S["act_k"]), "band": band, "diag": t(S["diag"]), "expert": t(S["expert"]), "cta": cta, "cta_text": t(S["cta_text"]), "slug": slug}


def tool_body(x):
    name = x["name"]; fn = x.get("fr_name", name); nm = (fn, name); NM = (fn.upper(), name.upper())
    ag = agency(x["slug"], name, x.get("fr_name"))
    h1 = "<br>".join(t(p) for p in [("AGENCE %s," % fn.upper(), "%s AGENCY," % name.upper()), (x["tag"][FR].upper() + ".", x["tag"][EN].upper() + ".")])
    eyebrow = '<span class="tool-mark"><img src="assets/img/tools/%s.png" alt="%s" onerror="this.parentNode.remove()" /></span>%s' % (x["slug"], html.escape(name), t(S["kick"]))
    sheet = '        <dl class="tsheet" data-reveal>%s</dl>' % "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (t(k), t(v)) for k, v in x["facts"])
    sols = '        <div class="solutions">%s</div>' % "".join(
        '<article class="solution" data-reveal><span class="solution__band" aria-hidden="true"></span><div class="solution__body"><h3>%s</h3><ul>%s</ul></div></article>' % (
            t(ti), "".join("<li>%s</li>" % t(b) for b in bullets)) for ti, bullets in x["deliver"])
    lims = card_grid(x["limits"], two=len(x["limits"]) == 2) + '\n        <div class="tpair" data-reveal><p class="tpair__k">%s</p>%s</div>' % (
        t(S["pair"]), chips([tool_chip(p) for p in x["pair"]]))
    out = head_block(eyebrow, h1, t(x["lead"]), "tech-tools.html", S["all"], "AGENCE %s %s" % (fn.upper(), x["tag"][FR].upper()))
    out += block("what", t(fmt(S["what_k"], NM)), t(fmt(S["what_t"], nm)), sheet, t(x["what"]))
    out += block("features", t(S["feat_k"]), t(fmt(S["feat_t"], nm)), card_grid(x["features"]))
    out += block("agency", t(ag["kick"]), t(fmt(S["ag_t"], nm)), flow(), t(fmt(S["ag_lead"], nm, nm)))
    out += block("deliverables", t(S["del_k"]), t(fmt(S["del_t"], nm)), sols)
    out += block("uses", t(S["uses_k2"]), t(fmt(S["uses_t2"], nm)), covers(x["uses"]), t(S["uses_lead"]))
    out += block("limits", t(S["lim_k"]), t(fmt(S["lim_t"], nm)), lims)
    out += block("faq", t(S["faq_k"]), t(fmt(S["faq_t2"], nm)), faq([(ag["q"], ag["a"])] + x["faq"]))
    return out + tail_block(t(ag["band"]), t(("Pas sûr que %s soit le bon outil ?" % fn, "Not sure %s is the right tool?" % name)), x["slug"])


def net_body(n):
    nm = n["name"]; NMx = (nm, nm); NMU = (nm.upper(), nm.upper())
    ag = agency_net(n)
    h1 = "<br>".join(t(p) for p in [("SOCIAL LISTENING %s," % nm.upper(), "%s SOCIAL LISTENING," % nm.upper()), (n["tag"][FR].upper() + ".", n["tag"][EN].upper() + ".")])
    eyebrow = '<i class="xt__glyph" style="--g:url(/assets/img/networks/%s.svg)" aria-hidden="true"></i>%s' % (n["glyph"], t(S["net_kick"]))
    acc = ('        <div class="grid grid--two"><article class="card" data-reveal><span class="card__num">%s</span><p class="card__text">%s</p></article>'
           '<article class="card" data-reveal><span class="card__num">%s</span><p class="card__text">%s</p></article></div>') % (
        t(S["nacc_yes"]), t(n["access"]), t(S["nacc_no"]), t(n["limits"]))
    met = flow()
    if n["tools"]:   # only the tools whose vendors state they cover this network
        met += '\n        <div class="tpair" data-reveal><p class="tpair__k">%s</p>%s</div>' % (t(fmt(S["nmet_tools"], NMx)), chips([tool_chip(p) for p in n["tools"]]))
    others = "        " + chips([net_chip(o["slug"]) for o in NETWORKS if o is not n])
    out = head_block(eyebrow, h1, t(n["lead"]), "tech-tools.html#sources", ("Tous les réseaux", "Every network"), n["tag"][FR].upper())
    out += block("why", t(fmt(S["nwhy_k"], NMU)), t(fmt(S["nwhy_t"], NMx)), card_grid(n["reads"]))
    out += block("data", t(S["nacc_k"]), t(fmt(S["nacc_t"], NMx)), acc)
    out += block("method", t(S["nmet_k"]), t(fmt(S["nmet_t"], NMx)), met)
    out += block("uses", t(S["uses_k2"]), t(fmt(S["nuses_t"], NMx)), covers(n["uses"]), t(S["uses_lead"]))
    out += block("networks", t(S["noth_k"]), t(S["noth_t"]), others)
    out += block("faq", t(S["faq_k"]), t(fmt(S["nfaq_t"], NMx)), faq([(ag["q"], ag["a"])] + n["faq"]))
    return out + tail_block(t(ag["band"]), t(("Une question sur %s ?" % nm, "A question about %s?" % nm)), "src-" + n["slug"])


def seo(src, file, title, desc, fr_url):
    """title, description and Open Graph in English, the language attributes,
    and canonical / hreflang / structured data between markers"""
    ti, de = html.escape(U.typo(title[EN], EN)), html.escape(U.typo(desc[EN], EN))
    src = re.sub(r"<title>.*?</title>", "<title>%s</title>" % ti, src, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % de),
                     (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % ti),
                     (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % de)):
        src = re.sub(pat, val, src, count=1)
    src = re.sub(r"<html[^>]*>", '<html lang="en" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (fr_url, file), src, count=1)
    src = re.sub(r"\s*<!-- seo:tech -->.*?<!-- /seo:tech -->", "", src, flags=re.S)
    block = ('<!-- seo:tech -->\n<link rel="canonical" href="{s}/{f}" />\n<link rel="alternate" hreflang="fr" href="{s}{fr}" />\n'
             '<link rel="alternate" hreflang="en" href="{s}/{f}" />\n<link rel="alternate" hreflang="x-default" href="{s}{fr}" />\n'
             '<!--ld-->\n<!-- /seo:tech -->').format(s=O.SITE, f=file, fr=fr_url)
    return src.replace('<meta name="twitter:card"', block + '\n<meta name="twitter:card"', 1)


def ld(body, lang, name, url, file):
    """breadcrumb and FAQ, read from the page itself"""
    fr = lang == FR
    crumbs = [("Accueil" if fr else "Home", O.SITE + ("/fr/" if fr else "/")),
              ("Techno & outils" if fr else "Tech & tools", O.SITE + ("/fr/outils/" if fr else "/tech-tools.html"))]
    if file != "tech-tools.html":
        crumbs.append((name, url))
    out = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]
    qa = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", body, re.S)
    if qa:
        clean = lambda x: html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"\s+", " ", x))).strip()
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(r)}} for q, r in qa]})
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in out)


def to_fr(page, file, fr_url, title, desc, name):
    """the French twin: the same page, its text translated in the HTML"""
    fr = re.sub(r"<html[^>]*>", '<html lang="fr" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (fr_url, file), page, count=1)
    fr = re.sub(r'href="([^"]*)" data-fr="([^"]*)"', r'href="\2"', fr)
    fr = re.sub(r'href="(?:/)?index\.html(#[^"]*)?"', lambda m: 'href="/fr/%s"' % (m.group(1) or ""), fr)
    ti, de = html.escape(U.typo(title[FR], FR)), html.escape(U.typo(desc[FR], FR))
    fr = re.sub(r"<title>.*?</title>", "<title>%s</title>" % ti, fr, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % de),
                     (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % ti),
                     (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % de)):
        fr = re.sub(pat, val, fr, count=1)
    fr = fr.replace('<link rel="canonical" href="%s/%s" />' % (O.SITE, file), '<link rel="canonical" href="%s%s" />' % (O.SITE, fr_url), 1)
    fr = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|data:)([^"]+)"', r'\1="/\2"', fr)
    b0, b1 = fr.index("<body"), fr.index("</body>")
    body = U.translate(fr[b0:b1]).replace(">Skip to content<", ">Aller au contenu<")
    fr = fr[:b0] + body + fr[b1:]
    fr = re.sub(r"<!--ld-->.*?(?=\n<!-- /seo:tech -->)", lambda m: ld(body, FR, name, O.SITE + fr_url, file), fr, count=1, flags=re.S)
    fr = fr.replace('placeholder="name@company.com"', 'placeholder="nom@entreprise.com"')
    out = ROOT / fr_url.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("<!-- Generated by tools/build-tech.py from /%s: edit the English page or that script. -->\n" % file + fr)


def main():
    shell = (ROOT / "tools" / "tech-shell.html").read_text()
    m0, m1 = shell.index('<main id="content">'), shell.index("</main>") + len("</main>")
    gen = "<!-- Generated by tools/build-tech.py: edit that script (tools/tools_data.py, tools/networks.py), not this file. -->\n"
    pages = []   # (file, name, title, desc, html)
    for x in TOOLS:
        ag = agency(x["slug"], x["name"], x.get("fr_name"))
        foot = shell[m1:].replace("email-nl-tech-talkwal", "email-nl-" + x["slug"][:10])
        pages.append(("tech-%s.html" % x["slug"], x["name"], ag["title"], ag["desc"], gen + shell[:m0] + tool_body(x) + foot))
    for n in NETWORKS:
        ag = agency_net(n)
        foot = shell[m1:].replace("email-nl-tech-talkwal", "email-nl-src-" + n["slug"][:8])
        pages.append(("source-%s.html" % n["slug"], n["name"], ag["title"], ag["desc"], gen + shell[:m0] + net_body(n) + foot))
    pages.append(("tech-tools.html", "Tech & tools", HUB["title"], HUB["desc"], (ROOT / "tech-tools.html").read_text()))
    for f, name, title, desc, src in pages:
        t(title); t(desc)
    O.write_dict("tech pages", "build-tech.py", O.NEW)
    U.DICT.update(U.fr_dict())
    U.DICT.update(O.NEW)
    for f, name, title, desc, src in pages:
        fr_url = U.expertise_fr(f)
        src = seo(src, f, title, desc, fr_url)
        b0, b1 = src.index("<body"), src.index("</body>")
        en = re.sub(r"<!--ld-->", lambda m: ld(src[b0:b1], EN, name, "%s/%s" % (O.SITE, f), f), src, count=1)
        to_fr(src, f, fr_url, title, desc, name)
        (ROOT / f).write_text(en)
    print("%d tool and network pages written in English and French, %d strings in js/fr.js" % (len(pages), len(O.NEW)))


if __name__ == "__main__":
    main()
