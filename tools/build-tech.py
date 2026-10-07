#!/usr/bin/env python3
"""Builds the tool pages and the network pages, in English and French:

    tech-<tool>.html        and /fr/outils/<tool>/     (tools/tools_data.py)
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
    "expert": ("Parler à un consultant", "Talk to a consultant"),
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
    "brandwatch": ("recherche consommateur et écoute sociale", "consumer research and social listening"),
    "sprinklr": ("écoute sociale et voix du client", "social listening and customer voice"),
    "semrush": ("écoute de la recherche", "search listening"),
    "google-trends": ("lire les tendances de recherche", "reading search trends"),
    "answerthepublic": ("les questions de votre marché", "your market's questions"),
    "chatgpt": ("ce que l'IA dit de votre marque", "what AI says about your brand"),
    "geo": ("votre visibilité dans les réponses des IA", "your visibility in AI answers"),
    "meta-ads": ("veille publicitaire sur Meta", "Meta ad monitoring"),
    "google-news": ("la presse face au social", "the press against social"),
    "social-blade": ("vérifier les comptes et les créateurs", "checking accounts and creators"),
    "claude": ("ce que Claude dit de votre marque", "what Claude says about your brand"),
    "gemini": ("ce que l'IA de Google dit de vous", "what Google's AI says about you"),
    "perplexity": ("votre marque dans le moteur de réponses", "your brand in the answer engine"),
    "grok": ("ce que l'IA de X dit de vous", "what X's AI says about you"),
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


# ------------------------------------------------------------------ brand colours
# each network's own colour (Simple Icons), and the ink that reads on it
NET_STYLE = {
    "facebook": ("#0866FF", "#fff"), "instagram": ("#E1306C", "#fff"), "threads": ("#101010", "#fff"), "whatsapp": ("#25D366", "#fff"),
    "messenger": ("#0099FF", "#fff"), "x-twitter": ("#101010", "#fff"), "tiktok": ("#101010", "#fff"), "youtube": ("#FF0000", "#fff"),
    "linkedin": ("#0A66C2", "#fff"), "reddit": ("#FF4500", "#fff"), "snapchat": ("#FFFC00", "#111"), "pinterest": ("#BD081C", "#fff"),
    "discord": ("#5865F2", "#fff"), "twitch": ("#9146FF", "#fff"), "telegram": ("#26A5E4", "#fff"), "bluesky": ("#0285FF", "#fff"),
    "vk": ("#0077FF", "#fff"), "wechat": ("#07C160", "#fff"), "weibo": ("#E6162D", "#fff"), "douyin": ("#101010", "#fff"),
    "xiaohongshu": ("#FF2442", "#fff"), "bilibili": ("#00A1D6", "#fff"),
}
# a second colour for the hero panel's gradient
NET_GLOW = {"instagram": "#F77737", "tiktok": "#FE2C55", "douyin": "#25F4EE", "threads": "#555", "x-twitter": "#3a3a3a", "snapchat": "#FFD500"}
TOOL_STYLE = {
    "talkwalker": "#8C6BFF", "visibrain": "#3DCB9A", "youscan": "#5CB531", "soprism": "#F15A29", "radarly": "#2BBBAD",
    "brandwatch": "#7B4DFF", "sprinklr": "#1E9BE9",
    "semrush": "#A87BFF", "google-trends": "#4285F4", "answerthepublic": "#FF5A1F", "chatgpt": "#10A37F", "geo": "#7C5CFF",
    "meta-ads": "#0866FF", "google-news": "#4285F4", "social-blade": "#C0392B",
    "claude": "#D97757", "gemini": "#4E7BEF", "perplexity": "#1F8A8A", "grok": "#4B4B55",
}
GEO_ENGINES = ["chatgpt", "claude", "gemini", "perplexity"]
# where each screenshot comes from (assets/img/shots/<slug>.webp, captured in October 2026)
SHOT_SRC = {
    "talkwalker": "talkwalker.com", "visibrain": "visibrain.com", "youscan": "youscan.io", "soprism": "audiense.com", "radarly": "meltwater.com",
    "brandwatch": "brandwatch.com", "sprinklr": "sprinklr.com",
    "semrush": "semrush.com", "google-trends": "trends.google.com", "answerthepublic": "answerthepublic.com", "chatgpt": "chatgpt.com",
    "geo": "arxiv.org/abs/2311.09735", "meta-ads": "facebook.com/ads/library", "google-news": "news.google.com", "social-blade": "socialblade.com",
    "claude": "anthropic.com/claude", "perplexity": "perplexity.ai", "gemini": "gemini.google.com", "grok": "grok.com",
    "facebook": "facebook.com", "instagram": "about.instagram.com", "threads": "threads.com", "whatsapp": "whatsapp.com", "messenger": "messenger.com",
    "x-twitter": "about.x.com", "tiktok": "newsroom.tiktok.com", "youtube": "blog.youtube", "linkedin": "linkedin.com", "reddit": "redditinc.com",
    "snapchat": "snap.com", "pinterest": "newsroom.pinterest.com", "discord": "discord.com", "twitch": "twitch.tv", "telegram": "telegram.org",
    "bluesky": "bsky.social", "vk": "vk.company", "wechat": "wechat.com", "weibo": "weibo.com", "douyin": None,
    "xiaohongshu": "xiaohongshu.com", "bilibili": "ir.bilibili.com",
}
# a photo rather than a screenshot: its credit (Wikimedia Commons)
PHOTO_CREDIT = {"douyin": ("Siège de Douyin Group, Pékin. Photo : Wikimedia Commons, CC BY-SA 4.0",
                           "Douyin Group headquarters, Beijing. Photo: Wikimedia Commons, CC BY-SA 4.0",
                           "https://commons.wikimedia.org/wiki/File:Douyin_Group_and_Feishu_logos_on_Fashion_Vanke_Center_20260620143040.jpg")}


def shot(slug, name, mark):
    """the real thing: the official site in a browser frame, its logo on top"""
    if slug in PHOTO_CREDIT:
        fr, en, url = PHOTO_CREDIT[slug]
        cap = '<figcaption><a href="%s" target="_blank" rel="noopener">%s</a></figcaption>' % (url, t((fr, en)))
        bar = ""
    else:
        label = ("L'article de recherche fondateur", "The founding research paper") if slug == "geo" else ("Capture du site officiel", "Official site, captured")
        cap = '<figcaption>%s <span>%s</span></figcaption>' % (t(label), SHOT_SRC[slug])
        bar = '<div class="tk-shot__bar" aria-hidden="true"><i></i><i></i><i></i><span>%s</span></div>' % SHOT_SRC[slug]
    return ('<figure class="tk-shot">%s<img src="/assets/img/shots/%s.webp" alt="%s" width="1200" height="750" decoding="async" fetchpriority="high" />%s</figure>'
            '<div class="tk-tile">%s</div>') % (bar, slug, html.escape(t((("Site officiel de %s" % name), ("%s official site" % name)))), cap, mark)


def glyph(name, cls="tk-glyph"):
    return '<i class="%s" style="--g:url(/assets/img/networks/%s.svg)" aria-hidden="true"></i>' % (cls, name)


def logo(slug, size="", alt=""):
    """a tool's logo: its picture, or for GEO the engines it measures"""
    if slug == "geo":
        return '<span class="tk-logo-geo%s" role="img" aria-label="%s">%s</span>' % (size, html.escape(alt or "GEO"), "".join(
            '<img src="/assets/img/tools/%s.png" alt="" width="48" height="48" loading="lazy" decoding="async" />' % e for e in GEO_ENGINES))
    return '<img src="/assets/img/tools/%s.png" alt="%s" width="96" height="96" loading="lazy" decoding="async" />' % (slug, html.escape(alt))


# ------------------------------------------------------------------ blocks
def head(kick, title, lead=None):
    return ('<div class="tk-head" data-reveal><p class="tk-k">%s</p><h2 class="tk-h2">%s</h2>%s</div>' % (
        kick, title, '<p class="tk-sub">%s</p>' % lead if lead else ""))


def sec(id_, inner, band=False):
    return '  <section class="tk-sec%s" id="%s">\n    <div class="shell">\n%s\n    </div>\n  </section>\n\n' % (" tk-sec--band" if band else "", id_, inner)


def feats(items, slug=None):
    """a bento: the first card large, in the brand colour, over a crop of the
    real site; the others each with their own ground"""
    out = ""
    for i, (ti, tx) in enumerate(items):
        shot_ = ('<img class="tk-feat__shot" src="/assets/img/shots/%s.webp" alt="" width="1200" height="750" loading="lazy" decoding="async" />' % slug) if i == 0 and slug else ""
        out += '<article class="tk-feat tk-feat--%d" data-reveal><span class="tk-feat__n" aria-hidden="true">0%d</span><div class="tk-feat__t"><h3>%s</h3><p>%s</p></div>%s</article>' % (
            i + 1, i + 1, t(ti), t(tx), shot_)
    return '<div class="tk-feats tk-feats--%d">%s</div>' % (len(items), out)


VS_ALONE = [("Un outil à apprendre et à faire tourner", "A tool to learn and to run"),
            ("Des requêtes réglées une fois, jamais revues", "Queries set once, never reviewed"),
            ("Des tableaux de bord que personne n'ouvre", "Dashboards nobody opens"),
            ("Des exports à interpréter seul", "Exports to interpret on your own")]
VS_LICTER = [("Nous l'opérons pour vous : rien à apprendre", "We run it for you: nothing to learn"),
             ("Un consultant qui cadre la question avec vous", "A consultant who frames the question with you"),
             ("Une configuration lue et ajustée en continu", "A setup read and adjusted continuously"),
             ("Une recommandation présentée à ceux qui décident", "A recommendation presented to those who decide")]


def versus(slug, nm):
    """the tool alone, against the tool with Licter"""
    alone = "".join("<li>%s</li>" % t(x) for x in VS_ALONE)
    licter = "".join("<li>%s</li>" % t(x) for x in VS_LICTER)
    return ('<div class="tk-vs">'
            '<div class="tk-vs__col tk-vs__col--alone" data-reveal><p class="tk-vs__k"><span class="tk-vs__logo">%s</span>%s</p><ul>%s</ul></div>'
            '<span class="tk-vs__mid" aria-hidden="true">VS</span>'
            '<div class="tk-vs__col tk-vs__col--licter" data-reveal><p class="tk-vs__k"><span class="tk-vs__logo">%s</span><img class="tk-vs__licter" src="/assets/img/logo-navy.png" alt="" width="22" height="24" />%s</p><ul>%s</ul>'
            '<p class="tk-vs__out">%s</p></div></div>') % (
        logo(slug), t(fmt(("%s seul", "%s on its own"), nm)), alone,
        logo(slug), t(fmt(("%s avec Licter", "%s with Licter"), nm)), licter,
        t(("Vous recevez une recommandation, pas un tableau de bord à faire tourner.", "You receive a recommendation, not a dashboard to run.")))



# ------------------------------------------------------------------ carousels (js/ui.js, "tool and network carousels")
UC_PHOTO = {"communication": "working-session-1200", "brand": "client-conversation-1200", "audiences": "team-sofa-1200", "trends": "two-colleagues-1200"}
DEL_PHOTO = ["consultant-dashboard-800", "meeting-portrait-800", "consultant-armchair-800"]


def prog(keys):
    """use cases: one large photo, the cases as tabs with a progress bar"""
    slides, tabs = "", ""
    for i, key in enumerate(keys):
        c = CASES[key]; f = FAMILY[c["family"]]
        fam = (f["name"][FR], f["name"][EN])
        slides += ('<a class="tk-prog__slide%s" href="%s" data-en="%s" data-i="%d"%s><img src="/assets/img/team/%s.webp" alt="" width="1200" height="800" loading="%s" decoding="async" />'
                   '<span class="tk-prog__go"><b>%s</b><span>%s</span></span></a>') % (
            " is-on" if i == 0 else "", U.case_path(c, FR), U.case_path(c, EN), i, "" if i == 0 else ' tabindex="-1"', UC_PHOTO[c["family"]], "eager" if i == 0 else "lazy",
            t(c["name"]), t(S["see_case"]))
        tabs += ('<button class="tk-prog__tab%s" type="button" role="tab" aria-selected="%s" data-i="%d"><span class="tk-prog__pill">%s</span>'
                 '<span class="tk-prog__name">%s</span><i class="tk-prog__bar" aria-hidden="true"></i></button>') % (
            " is-on" if i == 0 else "", "true" if i == 0 else "false", i, t(fam), t(c["name"]))
    return '<div class="tk-prog" data-auto="5500"><div class="tk-prog__stage">%s</div><div class="tk-prog__tabs" role="tablist">%s</div></div>' % (slides, tabs)


def conn(items):
    """what we deliver: the current deliverable large, the others as linked capsules"""
    cards, dots = "", ""
    n = len(items)
    for i, (ti, bullets) in enumerate(items):
        cards += ('<article class="tk-conn__card%s" data-i="%d"><div class="tk-conn__body"><span class="tk-conn__k">0%d / 0%d</span><h3>%s</h3><ul>%s</ul></div>'
                  '<div class="tk-conn__photo"><img src="/assets/img/team/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" />'
                  '<span class="tk-conn__vt" aria-hidden="true">%s</span></div></article>') % (
            " is-on" if i == 0 else "", i, i + 1, n, t(ti), "".join("<li>%s</li>" % t(b) for b in bullets), DEL_PHOTO[i % len(DEL_PHOTO)], t(ti))
        dots += '<button class="tk-conn__dot%s" type="button" aria-label="%s" data-i="%d"><i></i></button>' % (" is-on" if i == 0 else "", a((ti[FR], ti[EN])), i)
    return '<div class="tk-conn" data-auto="6500"><div class="tk-conn__stage">%s</div><div class="tk-conn__dots">%s</div></div>' % (cards, dots)


def offers(cards):
    """data and limits: a row of cards that scrolls, with arrows"""
    out = ""
    for c in cards:
        img = c.get("img") or '<span class="tk-offer__art tk-offer__art--%s" aria-hidden="true">%s</span>' % (c["kind"], c.get("art", ""))
        foot = ('<a class="tk-offer__foot" href="%s"><span class="tk-offer__logo">%s</span><span><b>%s</b><small>%s</small></span><i aria-hidden="true">↗</i></a>' % (
            c["href"], c["logo"], c["foot"], c["foot_sub"])) if c.get("href") else ('<p class="tk-offer__foot"><span class="tk-offer__logo">%s</span><span><b>%s</b><small>%s</small></span></p>' % (c["logo"], c["foot"], c["foot_sub"]))
        out += ('<article class="tk-offer tk-offer--%s"><div class="tk-offer__img">%s</div><div class="tk-offer__body"><p class="tk-offer__tag"><i aria-hidden="true">%s</i>%s</p>'
                '<h3>%s</h3><p>%s</p></div>%s</article>') % (c["kind"], img, c["icon"], c["tag"], c["title"], c["text"], foot)
    return ('<div class="tk-offers"><div class="tk-offers__track" tabindex="0">%s</div>'
            '<button class="tk-offers__nav tk-offers__nav--prev" type="button" aria-label="%s">‹</button>'
            '<button class="tk-offers__nav tk-offers__nav--next" type="button" aria-label="%s">›</button></div>') % (
        out, a(("Précédent", "Previous")), a(("Suivant", "Next")))


def tool_offer(slug, tag):
    x = TOOL[slug]; nm = (x.get("fr_name", x["name"]), x["name"])
    return {"kind": "tool", "img": '<img src="/assets/img/shots/%s.webp" alt="" width="1200" height="750" loading="lazy" decoding="async" />' % slug,
            "icon": "＋", "tag": t(tag), "title": t(nm), "text": t(x["features"][0][1]),
            "href": "tech-%s.html" % slug, "logo": logo(slug), "foot": t(nm), "foot_sub": t(("Voir la page", "See the page"))}


def steps():
    return '<ol class="tk-steps">%s</ol>' % "".join(
        '<li data-reveal><span class="tk-steps__n">0%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, t(ti), t(tx)) for i, (ti, tx) in enumerate(S["steps"]))


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
    return '<div class="covers covers--three">%s</div>' % out


def faq_block(title, items):
    return ('<div class="tk-faq"><div class="tk-head" data-reveal><p class="tk-k">%s</p><h2 class="tk-h2">%s</h2></div>'
            '<div class="faq" data-reveal>%s</div></div>') % (t(S["faq_k"]), title, "".join(
                "<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in items))


def tool_chips(slugs):
    return '<ul class="tk-chips">%s</ul>' % "".join(
        '<li><a href="tech-%s.html"><span class="tk-chips__logo">%s</span><span>%s</span></a></li>' % (
            s, logo(s), t((TOOL[s].get("fr_name", TOOL[s]["name"]), TOOL[s]["name"]))) for s in slugs)


def crumbs(name, net=False):
    mid = ('sources.html', t(SOURCES_NAME)) if net else ('tech-tools.html', t(("Techno & outils", "Tech & tools")))
    return ('<nav class="tk-crumbs" aria-label="%s"><ol><li><a href="index.html">%s</a></li><li><a href="%s">%s</a></li>'
            '<li aria-current="page">%s</li></ol></nav>') % (a(("Fil d'Ariane", "Breadcrumb")), t(("Accueil", "Home")), mid[0], mid[1], name)


SOURCES_NAME = ("Sources", "Sources")
SOURCES = {"title": ("Sources du social listening : les 22 réseaux que nous écoutons | Licter", "Social listening sources: the 22 networks we listen to | Licter"),
           "desc": ("Les 22 réseaux d'où viennent nos données : ce qu'on peut y lire, ce qui reste privé, et les plateformes qui les couvrent. TikTok, Instagram, X, LinkedIn, Reddit…",
                    "The 22 networks our data comes from: what can be read there, what stays private, and the platforms that cover them. TikTok, Instagram, X, LinkedIn, Reddit…")}


def sources_body():
    """the hub of the network pages"""
    copy = (crumbs(t(SOURCES_NAME)).replace('<li><a href="sources.html">%s</a></li>' % t(SOURCES_NAME), '<li><a href="tech-tools.html">%s</a></li>' % t(("Techno & outils", "Tech & tools"))) +
            '<p class="tk-kick">%s</p>' % t(("D'OÙ VIENNENT LES DONNÉES", "WHERE THE DATA COMES FROM")) +
            '<h1 class="%s">%s<br><span>%s</span></h1>' % (h1_cls("22 RÉSEAUX,", "LUS PAR NOS ANALYSTES."), t(("22 RÉSEAUX,", "22 NETWORKS,")), t(("LUS PAR NOS ANALYSTES.", "READ BY OUR ANALYSTS."))) +
            '<p class="tk-lead">%s</p>' % t(("Chaque réseau a son public, ses formats et ses limites de collecte. Voici ce que nous y lisons, ce qui reste privé, et les plateformes qui le couvrent.",
                                             "Each network has its own audience, formats and collection limits. Here is what we read there, what stays private, and the platforms that cover it.")) +
            '<div class="tk-actions"><a class="btn btn--primary" href="book-a-meeting.html">%s <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--ghost" href="tech-tools.html">%s</a></div>' % (t(S["book"]), t(S["all"])))
    art = '<ul class="tk-nets tk-nets--hero" aria-hidden="true">%s</ul>' % "".join(
        '<li><span style="--c:%s;--i:%s"><span class="tk-nets__mark">%s</span></span></li>' % (NET_STYLE[o["slug"]][0], NET_STYLE[o["slug"]][1], glyph(o["glyph"])) for o in NETWORKS[:12])
    grid = '<ul class="tk-nets tk-nets--hub">%s</ul>' % "".join(
        '<li><a href="source-%s.html" style="--c:%s;--i:%s"><span class="tk-nets__mark">%s</span><span><b>%s</b><small>%s</small></span></a></li>' % (
            o["slug"], NET_STYLE[o["slug"]][0], NET_STYLE[o["slug"]][1], glyph(o["glyph"]), html.escape(o["name"]), t(o["tag"])) for o in NETWORKS)
    out = '<main id="content" class="tk tk--tool tk--sources" style="--brand:#EAA93D">\n'
    out += hero(copy, art)
    out += sec("networks", head(t(("LES 22 RÉSEAUX", "THE 22 NETWORKS")), t(("Choisissez un réseau.", "Pick a network.")),
                                t(("Pour chacun : ce qu'il dit de votre marché, ce que nous pouvons collecter, et comment nous le lisons.",
                                   "For each: what it says about your market, what we can collect, and how we read it."))) + grid)
    out += sec("method", head(t(S["nmet_k"]), t(("Comment nous écoutons un réseau.", "How we listen to a network."))) + steps() +
               xp(None, ["social-listening", "influence-listening"]), band=True)
    return out + cta(t(("Vous cherchez une agence social listening ?", "Looking for a social listening agency?")), t(S["cta_text"]), "", "sources")


def hero(copy, art):
    return '  <section class="tk-hero">\n    <div class="shell tk-hero__grid">\n      <div class="tk-hero__copy">%s</div>\n      <div class="tk-hero__art">%s</div>\n    </div>\n  </section>\n\n' % (copy, art)


def h1_cls(*texts):
    """a word of more than 12 letters (ANSWERTHEPUBLIC, PROFESSIONNELLE) does not fit a phone at the usual size"""
    words = re.sub(r"<[^>]+>|&[a-z]+;", " ", " ".join(texts)).replace(",", " ").replace(".", " ").split()
    return "tk-h1 tk-h1--long" if max(len(w) for w in words) > 12 else "tk-h1"


def cta(band, sub, mark, slug):
    return '''  <section class="tk-sec tk-sec--cta" id="book">
    <div class="shell">
      <div class="tk-cta" data-reveal>
        <div class="tk-cta__mark" aria-hidden="true">%(mark)s</div>
        <div class="tk-cta__copy">
          <p class="tk-k">%(act)s</p>
          <h2 class="tk-h2">%(band)s</h2>
          <p class="tk-sub">%(sub)s</p>
          <div class="tk-actions">
            <a class="btn btn--primary" href="book-a-meeting.html">%(expert)s <span aria-hidden="true">→</span></a>
            <a class="btn btn--ghost" href="diagnostic.html">%(diag)s</a>
          </div>
        </div>
        <div class="tk-cta__form">
          <form class="signup" novalidate>
            <label class="visually-hidden" for="email-%(slug)s">Your work email</label>
            <input class="signup__input" id="email-%(slug)s" name="email" type="email" placeholder="Your work email..." autocomplete="email" required />
            <button class="signup__btn" type="submit">BOOK A MEETING</button>
          </form>
          <p class="consent">We use your email only to reply to you. <a href="privacy.html">Privacy policy</a>.</p>
          <p class="signup__note" role="status"><span class="signup__check" aria-hidden="true">✓</span> NOTED - WE GET BACK TO YOU WITHIN 24 HOURS</p>
        </div>
      </div>
    </div>
  </section>
</main>''' % {"mark": mark, "act": t(S["act_k"]), "band": band, "sub": sub, "expert": t(S["expert"]), "diag": t(S["diag"]), "slug": slug}


# ------------------------------------------------------------------ tool page
def xp(slug, keys=None):
    """the expertise pages a tool or a network serves (French added by to_fr)"""
    keys = keys or O.U.XP_OF.get(slug, [])
    if not keys:
        return ""
    lab = t(("Expertise associée", "Related expertise"))
    return '<p class="xp-line"><span>%s</span> %s</p>' % (lab, ", ".join('<a href="expertise-%s.html">%s</a>' % (k, O.U.XP_NAME[k]) for k in keys))


def tool_body(x):
    name = x["name"]; fn = x.get("fr_name", name); nm = (fn, name); NM = (fn.upper(), name.upper())
    ag = agency(x["slug"], name, x.get("fr_name"))
    l1, l2 = ("AGENCE %s," % fn.upper(), "%s AGENCY," % name.upper()), (x["tag"][FR].upper() + ".", x["tag"][EN].upper() + ".")
    copy = (crumbs(t(nm)) + '<p class="tk-kick">%s</p>' % t(S["kick"]) +
            '<h1 class="%s">%s<br><span>%s</span></h1>' % (h1_cls(l1[0], l1[1], l2[0], l2[1]), t(l1), t(l2)) +
            '<p class="tk-lead">%s</p>' % t(x["lead"]) +
            '<div class="tk-actions"><a class="btn btn--primary" href="book-a-meeting.html">%s <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--ghost" href="tech-tools.html">%s</a></div>' % (t(S["book"]), t(S["all"])))
    art = shot(x["slug"], name, logo(x["slug"], alt=name)) + '<div class="tk-badge"><i>✓</i><span>%s</span></div>' % t(("Lu par un consultant Licter", "Read by a Licter consultant"))
    sheet = ('<aside class="tk-sheet" data-reveal><div class="tk-sheet__top"><span class="tk-sheet__logo">%s</span><b>%s</b></div><dl>%s</dl></aside>' % (
        logo(x["slug"], alt=name), html.escape(name), "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (t(k), t(v)) for k, v in x["facts"])))
    dels = conn(x["deliver"])
    lim_cards = [{"kind": "limit", "icon": "!", "tag": t(("Limite", "Limit")), "title": t(ti), "text": t(tx), "art": "!",
                  "logo": logo(x["slug"]), "foot": html.escape(name), "foot_sub": t(("Ce que nous compensons", "What we make up for"))} for ti, tx in x["limits"]]
    lims = offers(lim_cards + [tool_offer(p_, ("Nous le croisons avec", "We cross it with")) for p_ in x["pair"]])
    out = '<main id="content" class="tk tk--tool" style="--brand:%s">\n' % TOOL_STYLE[x["slug"]]
    out += hero(copy, art)
    out += sec("what", '<div class="tk-split">%s%s</div>' % (
        '<div>%s<p class="tk-prose" data-reveal>%s</p>%s</div>' % (head(t(fmt(S["what_k"], NM)), t(fmt(S["what_t"], nm))), t(x["what"]),
                                                                   xp(x["slug"])), sheet))
    out += sec("features", head(t(S["feat_k"]), t(fmt(S["feat_t"], nm))) + feats(x["features"], x["slug"]), band=True)
    out += sec("agency", head(t(ag["kick"]), t(fmt(S["ag_t"], nm)), t(fmt(S["ag_lead"], nm, nm))) + versus(x["slug"], nm) + steps())
    out += sec("deliverables", head(t(S["del_k"]), t(fmt(S["del_t"], nm))) + dels, band=True)
    out += sec("uses", head(t(S["uses_k2"]), t(fmt(S["uses_t2"], nm)), t(S["uses_lead"])) + prog(x["uses"]))
    out += sec("limits", head(t(S["lim_k"]), t(fmt(S["lim_t"], nm))) + lims, band=True)
    out += sec("faq", faq_block(t(fmt(S["faq_t2"], nm)), [(ag["q"], ag["a"])] + x["faq"]))
    return out + cta(t(ag["band"]), t(S["cta_text"]), logo(x["slug"], alt=""), x["slug"])


# ------------------------------------------------------------------ network page
SPARK = '<svg viewBox="0 0 120 40" preserveAspectRatio="none"><path d="M0 34 L12 31 L24 33 L36 27 L48 29 L60 22 L72 24 L84 15 L96 17 L108 8 L120 4" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def net_body(n):
    nm = n["name"]; NMx = (nm, nm); NMU = (nm.upper(), nm.upper())
    color, ink = NET_STYLE[n["slug"]]
    ag = agency_net(n)
    l1, l2 = ("SOCIAL LISTENING %s," % nm.upper(), "%s SOCIAL LISTENING," % nm.upper()), (n["tag"][FR].upper() + ".", n["tag"][EN].upper() + ".")
    copy = (crumbs(html.escape(nm), net=True) + '<p class="tk-kick">%s</p>' % t(S["net_kick"]) +
            '<h1 class="%s">%s<br><span>%s</span></h1>' % (h1_cls(l1[0], l2[0], l2[1]), t(l1), t(l2)) +
            '<p class="tk-lead">%s</p>' % t(n["lead"]) +
            '<div class="tk-actions"><a class="btn btn--primary" href="book-a-meeting.html">%s <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--ghost" href="sources.html">%s</a></div>' % (t(S["book"]), t(("Tous les réseaux", "Every network"))))
    art = '<div class="tk-net">%s%s</div>' % (glyph(n["glyph"], "tk-net__wm"), shot(n["slug"], nm, '<span class="tk-tile__net">%s</span>' % glyph(n["glyph"])))
    netmark = '<span class="tk-offer__net">%s</span>' % glyph(n["glyph"])
    io_cards = [{"kind": "yes", "icon": "✓", "tag": t(S["nacc_yes"]), "title": t(fmt(("Le public de %s", "The public side of %s"), NMx)), "text": t(n["access"]),
                 "img": '<img src="/assets/img/shots/%s.webp" alt="" width="1200" height="750" loading="lazy" decoding="async" />' % n["slug"],
                 "logo": netmark, "foot": html.escape(nm), "foot_sub": t(("Données publiques", "Public data"))},
                {"kind": "no", "icon": "✕", "tag": t(S["nacc_no"]), "title": t(("Le privé reste privé", "Private stays private")), "text": t(n["limits"]), "art": "",
                 "logo": netmark, "foot": html.escape(nm), "foot_sub": t(("Jamais collecté", "Never collected"))}]
    # only the tools whose vendors state they cover this network
    io = offers(io_cards + [tool_offer(p_, fmt(("Couvre %s selon l'éditeur", "Covers %s, per the vendor"), NMx)) for p_ in n["tools"]])
    method = steps()
    nets = '<ul class="tk-nets">%s</ul>' % "".join(
        '<li><a href="source-%s.html" style="--c:%s;--i:%s"><span class="tk-nets__mark">%s</span><span>%s</span></a></li>' % (
            o["slug"], NET_STYLE[o["slug"]][0], NET_STYLE[o["slug"]][1], glyph(o["glyph"]), html.escape(o["name"])) for o in NETWORKS if o is not n)
    out = '<main id="content" class="tk tk--net" style="--brand:%s;--brand-ink:%s;--brand-2:%s">\n' % (color, ink, NET_GLOW.get(n["slug"], color))
    out += hero(copy, art)
    out += sec("why", head(t(fmt(S["nwhy_k"], NMU)), t(fmt(S["nwhy_t"], NMx))) + feats(n["reads"], n["slug"]) +
               xp(None, ["social-listening"] + (["influence-listening"] if n["slug"] in O.U.XP_INFLUENCE_NETS else [])), band=True)
    out += sec("data", head(t(S["nacc_k"]), t(fmt(S["nacc_t"], NMx))) + io)
    out += sec("method", head(t(S["nmet_k"]), t(fmt(S["nmet_t"], NMx))) + method, band=True)
    out += sec("uses", head(t(S["uses_k2"]), t(fmt(S["nuses_t"], NMx)), t(S["uses_lead"])) + prog(n["uses"]))
    out += sec("networks", head(t(S["noth_k"]), t(S["noth_t"])) + nets, band=True)
    out += sec("faq", faq_block(t(fmt(S["nfaq_t"], NMx)), [(ag["q"], ag["a"])] + n["faq"]))
    return out + cta(t(ag["band"]), t(S["cta_text"]), '<span class="tk-cta__net">%s</span>' % glyph(n["glyph"]), "src-" + n["slug"])


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
    if file.startswith("source-"):
        crumbs[1] = ("Sources", O.SITE + ("/fr/sources/" if fr else "/sources.html"))
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
    body = O.per_lang(U.translate(fr[b0:b1]).replace(">Skip to content<", ">Aller au contenu<"), FR)
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
    pages.append(("sources.html", "Sources", SOURCES["title"], SOURCES["desc"],
                  gen + shell[:m0] + sources_body() + shell[m1:].replace("email-nl-tech-talkwal", "email-nl-sources")))
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
        (ROOT / f).write_text(O.per_lang(en, EN))
    print("%d tool and network pages written in English and French, %d strings in js/fr.js" % (len(pages), len(O.NEW)))


if __name__ == "__main__":
    main()
