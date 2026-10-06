#!/usr/bin/env python3
"""Expertise: social intelligence, and one page per way of listening.

    python3 tools/build-expertise.py

Writes expertise.html (the overview) and expertise-*.html (social, audience,
influence, AI, live and search listening) at the root, in English like the
other root pages, with the shared header and footer of offers.html. Their
French goes into a block of js/fr.js of its own ("expertise pages"): edit the
French here, not there.

Built on tools/build-offers.py (same head, same callback, same dictionary
mechanism). tools/build-usecases.py runs it after the offer pages.
"""
import html, importlib.util, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bo", ROOT / "tools" / "build-offers.py")
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
U, C = O.U, O.C
FR, EN = 0, 1
SITE = O.SITE
t, a = O.t, O.a

S = {
    "home": ("Accueil", "Home"),
    "expertise": ("Expertise", "Expertise"),
    "kicker": ("SOCIAL INTELLIGENCE", "SOCIAL INTELLIGENCE"),
    "book": ("Parler à un consultant", "Talk to a consultant"),
    "answers_link": ("Les questions auxquelles elle répond", "The questions it answers"),
    "demo_cap": ("Un exemple de ce qu'elle entend", "An example of what it picks up"),
    "illus": ("Exemple illustratif", "Illustrative example"),
    "limits_t": ("Ce qu'elle entend, et ses limites", "What it picks up, and its limits"),
    "hears": ("Ce qu'elle entend", "What it picks up"),
    "cannot": ("Ce qu'elle ne vous dira pas", "What it cannot tell you on its own"),
    "answers_t": ("Les questions auxquelles elle répond", "The questions it answers"),
    "how_t": ("Avec quoi, et dans quelle offre", "With what, and in which offer"),
    "tools_k": ("Les plateformes", "The platforms"),
    "offers_k": ("Les offres qui l'incluent", "The offers that include it"),
    "others_t": ("Les autres écoutes", "The other ways of listening"),
    "all": ("Toute notre expertise", "All our expertise"),
    "faq": ("Questions fréquentes", "Frequently asked questions"),
    "crumbs": ("Fil d'Ariane", "Breadcrumb"),
    "list_t": ("Six façons d'écouter", "Six ways of listening"),
    "menu_label": ("SOCIAL INTELLIGENCE", "SOCIAL INTELLIGENCE"),
    "menu_aside": ("DANS NOS OFFRES", "IN OUR OFFERS"),
    "foot_link": ("Expertise", "Expertise"),
}

TOOLS = {
    "talkwalker": ("tech-talkwalker.html", "Talkwalker", ("Couverture large, sur la durée", "Broad coverage, over time")),
    "visibrain": ("tech-visibrain.html", "Visibrain", ("Le temps réel et les médias", "Real time and the media")),
    "youscan": ("tech-youscan.html", "YouScan", ("Ce qui apparaît dans l'image", "What appears in the image")),
    "soprism": ("tech-soprism.html", "SoPrism", ("Les audiences, en détail", "Audiences, in detail")),
}
OFFERS = {x["key"]: x for x in O.OFFERS}

# MOCK: the examples in each hero are illustrative; the AI listening page in
# particular describes the practice from a one-line brief, to be validated.
LISTENINGS = [
    {
        "key": "social", "file": "expertise-social-listening.html", "icon": "chart",
        "name": ("Social listening", "Social listening"),
        "short": ("Ce qui se dit sur vous, vos concurrents et votre marché.", "What is said about you, your competitors and your market."),
        "seo_title": ("Social listening : ce qui se dit sur votre marque | Licter", "Social listening: what is said about your brand | Licter"),
        "seo_desc": ("Réseaux sociaux, presse, forums et avis, collectés sur votre périmètre et lus par un analyste : sujets, tonalité, et ce que ça veut dire pour vous.",
                     "Social networks, news, forums and reviews, collected on your perimeter and read by an analyst: topics, tone, and what it means for you."),
        "h1": ("Ce que les gens disent, lu par des gens.", "What people say, read by people."),
        "lead": ("Les réseaux sociaux, la presse, les forums et les avis, collectés sur votre périmètre et lus par un analyste : volumes, sujets, tonalité, et surtout ce que ça veut dire pour vous.",
                 "Social networks, news, forums and reviews, collected on your perimeter and read by an analyst: volumes, topics, tone, and above all what it means for you."),
        "demo": [(("Sujet en hausse", "Rising topic"), ("« Autonomie en hiver », +64 % en 30 jours", "“Winter range”, +64% in 30 days")),
                 (("Tonalité", "Tone"), ("Négative sur le prix, positive sur le design", "Negative on price, positive on design")),
                 (("Qui le porte", "Who carries it"), ("Deux forums spécialisés, puis la presse auto", "Two specialist forums, then the motoring press"))],
        "hears": [("Les sujets qui montent, et ceux qui retombent", "The topics rising, and the ones fading"),
                  ("La tonalité, sujet par sujet, pas en moyenne", "The tone, topic by topic, not on average"),
                  ("Comment une conversation circule, et qui la porte", "How a conversation travels, and who carries it")],
        "cannot": [("Qui sont ces gens au-delà de leur publication : c'est l'audience listening.", "Who these people are beyond their post: that is audience listening.")],
        "cases": ["reputation", "messaging", "campaign-impact"],
        "tools": ["talkwalker", "visibrain"], "offers": ["social-insights", "vigie"],
        "faq": [(("Quelles sources lisez-vous ?", "Which sources do you read?"),
                 ("Les réseaux sociaux, la presse en ligne, les forums, les blogs et les avis, dans plus de vingt langues, selon le périmètre fixé avec vous.",
                  "Social networks, online news, forums, blogs and reviews, in more than twenty languages, depending on the perimeter set with you.")),
                (("Quelle différence avec un outil de veille ?", "How is it different from a monitoring tool?"),
                 ("L'outil collecte. Nous choisissons les sources, écartons le bruit et lisons le résultat, pour vous dire ce qu'il faut en faire.",
                  "The tool collects. We pick the sources, remove the noise and read the result, to tell you what to do with it."))],
    },
    {
        "key": "audience", "file": "expertise-audience-listening.html", "icon": "audiences",
        "name": ("Audience listening", "Audience listening"),
        "short": ("Qui sont vraiment les gens qui parlent de vous.", "Who the people talking about you really are."),
        "seo_title": ("Audience listening : qui sont vraiment vos audiences | Licter", "Audience listening: who your audiences really are | Licter"),
        "seo_desc": ("Centres d'intérêt, affinités de marque et médias : nous profilons vos communautés à partir de leur comportement observé, pas déclaré.",
                     "Interests, brand affinities and media: we profile your communities from observed behaviour, not declared answers."),
        "h1": ("Qui sont vraiment vos audiences, au-delà de l'âge et du sexe.", "Who your audiences really are, beyond age and gender."),
        "lead": ("Nous profilons les communautés à partir de ce qu'elles suivent, partagent et consomment : centres d'intérêt, affinités de marque, médias. De quoi remplacer un persona déclaratif par un comportement observé.",
                 "We profile communities from what they follow, share and consume: interests, brand affinities, media. Enough to replace a declared persona with observed behaviour."),
        "demo": [(("Communauté", "Community"), ("Parents pragmatiques, 41 % de l'audience", "Pragmatic parents, 41% of the audience")),
                 (("Affinités", "Affinities"), ("Cuisine du quotidien, bricolage, économies d'énergie", "Everyday cooking, DIY, energy saving")),
                 (("Où les toucher", "Where to reach them"), ("Facebook et la recherche, peu Instagram", "Facebook and search, little Instagram"))],
        "hears": [("Les centres d'intérêt et les passions d'une communauté", "A community's interests and passions"),
                  ("Les marques et les médias qu'elle suit", "The brands and media it follows"),
                  ("Les recoupements entre communautés", "The overlaps between communities")],
        "cannot": [("Ce que ces personnes pensent de vous en particulier : c'est le social listening.", "What these people think of you in particular: that is social listening.")],
        "cases": ["segmentation", "rejuvenate", "touchpoints"],
        "tools": ["soprism"], "offers": ["social-insights"],
        "faq": [(("D'où viennent les données d'audience ?", "Where does the audience data come from?"),
                 ("Des interactions publiques : comptes suivis, contenus partagés, engagements. Nous travaillons sur des communautés agrégées, jamais sur des individus.",
                  "From public interactions: accounts followed, content shared, engagement. We work on aggregated communities, never on individuals.")),
                (("Peut-on comparer nos audiences à celles d'un concurrent ?", "Can we compare our audiences with a competitor's?"),
                 ("Oui, et c'est souvent le plus parlant : ce qui distingue vos communautés des siennes, et celles qu'il touche et pas vous.",
                  "Yes, and it is often the most telling: what sets your communities apart from theirs, and the ones they reach and you do not."))],
    },
    {
        "key": "influence", "file": "expertise-influence-listening.html", "icon": "influence",
        "name": ("Influence listening", "Influence listening"),
        "short": ("Les voix qui portent vraiment dans votre catégorie.", "The voices that actually carry in your category."),
        "seo_title": ("Influence listening : les voix qui portent vraiment | Licter", "Influence listening: the voices that actually carry | Licter"),
        "seo_desc": ("Créateurs, experts, journalistes, dirigeants : qui influence vraiment votre catégorie, avec le recouvrement d'audience et les risques.",
                     "Creators, experts, journalists, executives: who really shapes your category, with audience overlap and risks."),
        "h1": ("Les voix qui portent, pas celles qui ont le plus d'abonnés.", "The voices that carry, not the ones with the most followers."),
        "lead": ("Créateurs, experts, journalistes, dirigeants : nous identifions qui influence vraiment la conversation de votre catégorie, mesurons le recouvrement avec votre audience et signalons les risques avant un partenariat.",
                 "Creators, experts, journalists, executives: we identify who really shapes your category's conversation, measure the overlap with your audience and flag the risks before a partnership."),
        "demo": [(("Créatrice", "Creator"), ("@studio.zoe, 142 k abonnés, 58 % de recouvrement", "@studio.zoe, 142k followers, 58% overlap")),
                 (("Expert", "Expert"), ("Un ingénieur cité par trois médias spécialisés", "An engineer quoted by three specialist outlets")),
                 (("À vérifier", "To check"), ("Un grand compte, mais une audience éloignée de la vôtre", "A big account, but an audience far from yours"))],
        "hears": [("Qui lance un sujet, et qui le relaie", "Who starts a topic, and who relays it"),
                  ("Le recouvrement entre leur audience et la vôtre", "The overlap between their audience and yours"),
                  ("Les prises de position passées, et les risques", "Past stances, and the risks")],
        "cannot": [("L'effet d'une campagne sur vos ventes : il faut le croiser avec d'autres données.", "A campaign's effect on your sales: it has to be crossed with other data.")],
        "cases": ["ambassadors", "leader-advocacy", "stakeholders"],
        "tools": ["talkwalker", "youscan"], "offers": ["social-insights"],
        "faq": [(("Travaillez-vous avec des agences d'influence ?", "Do you work with influencer agencies?"),
                 ("Oui, souvent en amont : nous leur donnons une liste lue et argumentée, elles gèrent la relation et la production.",
                  "Yes, often upstream: we give them a read, argued shortlist, and they handle the relationship and the production.")),
                (("Peut-on mesurer l'effet d'un partenariat ?", "Can you measure a partnership's effect?"),
                 ("Oui, sur la conversation : ce qu'il a déplacé, auprès de quelles audiences, comparé à la période précédente.",
                  "Yes, on the conversation: what it moved, with which audiences, compared with the period before."))],
    },
    {
        "key": "ai", "file": "expertise-ai-listening.html", "icon": "ai",
        "name": ("AI listening", "AI listening"),
        "short": ("Ce que les IA génératives disent de votre marque.", "What generative AI says about your brand."),
        "seo_title": ("AI listening : ce que les IA disent de votre marque | Licter", "AI listening: what AI says about your brand | Licter"),
        "seo_desc": ("Nous interrogeons les assistants IA sur votre marque et votre catégorie, comme vos clients, et lisons ce qu'ils recommandent, citent ou oublient.",
                     "We question AI assistants about your brand and your category, the way your customers do, and read what they recommend, cite or leave out."),
        "h1": ("Ce que les IA répondent quand on leur parle de vous.", "What AI answers when people ask about you."),
        "lead": ("De plus en plus de recherches passent par un assistant IA. Nous interrogeons les principaux modèles sur votre marque et votre catégorie, comme le feraient vos clients, et lisons ce qu'ils recommandent, citent ou oublient.",
                 "More and more searches go through an AI assistant. We question the main models about your brand and your category, the way your customers would, and read what they recommend, cite or leave out."),
        "demo": [(("Question testée", "Prompt tested"), ("« Quelle mutuelle pour une famille ? »", "“Which health insurance for a family?”")),
                 (("Cité", "Cited"), ("Votre marque, dans 2 réponses sur 5", "Your brand, in 2 answers out of 5")),
                 (("À corriger", "To fix"), ("Un tarif de 2022 repris comme actuel", "A 2022 price quoted as current"))],
        "hears": [("Les marques recommandées dans votre catégorie", "The brands recommended in your category"),
                  ("Les sources que les modèles citent", "The sources the models cite"),
                  ("Les erreurs ou les informations datées sur vous", "Mistakes or outdated facts about you")],
        "cannot": [("Combien de personnes posent ces questions : c'est le search listening.", "How many people ask these questions: that is search listening.")],
        "cases": ["reputation", "messaging", "market-opportunities"],
        "tools": [], "offers": ["social-insights", "nox"],
        "faq": [(("Quels modèles interrogez-vous ?", "Which models do you question?"),
                 ("Les assistants les plus utilisés par vos clients, définis avec vous, toujours avec les mêmes questions pour suivre l'évolution dans le temps.",
                  "The assistants your customers use most, set with you, always with the same questions so the change can be followed over time.")),
                (("Peut-on influencer ce que répondent les IA ?", "Can you influence what AI answers?"),
                 ("Indirectement : les modèles s'appuient sur des sources publiques. Nous identifions celles qu'ils citent, et ce qu'il faudrait y corriger ou y ajouter.",
                  "Indirectly: the models rely on public sources. We identify the ones they cite, and what should be corrected or added there."))],
    },
    {
        "key": "live", "file": "expertise-live-listening.html", "icon": "bell",
        "name": ("Live listening", "Live listening"),
        "short": ("La conversation en temps réel, une alerte en 15 minutes.", "The conversation in real time, an alert within 15 minutes."),
        "seo_title": ("Live listening : la conversation en temps réel | Licter", "Live listening: the conversation in real time | Licter"),
        "seo_desc": ("Événement, lancement, crise : la conversation suivie en direct, 24 h/24, et un analyste qui vous alerte en 15 minutes quand quelque chose bouge.",
                     "Event, launch, crisis: the conversation followed live, 24/7, and an analyst who alerts you within 15 minutes when something moves."),
        "h1": ("Savoir ce qui se passe pendant que ça se passe.", "Knowing what happens while it happens."),
        "lead": ("Événement, lancement, crise : nous suivons la conversation en direct, 24 h/24, et un analyste vous alerte en 15 minutes quand quelque chose bouge vraiment.",
                 "Event, launch, crisis: we follow the conversation live, 24/7, and an analyst alerts you within 15 minutes when something really moves."),
        "demo": [(("14:32", "14:32"), ("Pic sur « rappel produit », ×4 en 2 h", "Spike on “product recall”, ×4 in 2 h")),
                 (("14:41", "14:41"), ("Qualifié par l'analyste : un concurrent, pas vous", "Qualified by the analyst: a competitor, not you")),
                 (("14:47", "14:47"), ("Pas d'alerte envoyée, le suivi continue", "No alert sent, still being watched"))],
        "hears": [("Les pics de volume, et ce qui les cause", "Volume spikes, and what causes them"),
                  ("Les voix qui font basculer un sujet", "The voices that tip a topic"),
                  ("Le passage d'un réseau social à la presse", "The jump from a social network to the press")],
        "cannot": [("Pourquoi votre image évolue sur un an : c'est une étude, pas une alerte.", "Why your image shifts over a year: that is a study, not an alert.")],
        "cases": ["reputation", "brand-risk", "campaign-impact"],
        "tools": ["visibrain"], "offers": ["vigie", "nox"],
        "faq": [(("Couvrez-vous les nuits et les week-ends ?", "Do you cover nights and weekends?"),
                 ("Oui : c'est souvent là que les sujets démarrent.", "Yes: that is often when topics start.")),
                (("Peut-on suivre un événement ponctuel ?", "Can you cover a one-off event?"),
                 ("Oui. Un salon, un lancement ou une prise de parole peuvent être suivis en direct sur la période, avec un bilan à la fin.",
                  "Yes. A trade show, a launch or a speech can be followed live over the period, with a debrief at the end."))],
    },
    {
        "key": "search", "file": "expertise-search-listening.html", "icon": "search",
        "name": ("Search listening", "Search listening"),
        "short": ("Ce que les gens cherchent sur Google, YouTube et Amazon.", "What people search for on Google, YouTube and Amazon."),
        "seo_title": ("Search listening : ce que les gens cherchent vraiment | Licter", "Search listening: what people really search for | Licter"),
        "seo_desc": ("Les recherches sur Google, YouTube et Amazon disent ce que les gens veulent savoir : nous les lisons pour repérer les besoins non couverts.",
                     "Searches on Google, YouTube and Amazon say what people want to know: we read them to spot unmet needs."),
        "h1": ("Ce que les gens cherchent quand personne ne les regarde.", "What people search for when nobody is watching."),
        "lead": ("Les recherches sur Google, YouTube et Amazon disent ce que les gens veulent vraiment savoir, avant l'achat et après le problème. Nous les lisons pour repérer les besoins non couverts et les questions sans réponse.",
                 "Searches on Google, YouTube and Amazon say what people really want to know, before the purchase and after the problem. We read them to spot unmet needs and unanswered questions."),
        "demo": [(("Recherche en hausse", "Rising search"), ("« Format individuel recyclable », +38 % sur un an", "“Single-portion recyclable”, +38% over a year")),
                 (("Question fréquente", "Frequent question"), ("« Peut-on le congeler ? », sans réponse claire en ligne", "“Can it be frozen?”, with no clear answer online")),
                 (("Opportunité", "Opportunity"), ("Une FAQ produit, et un format à lancer", "A product FAQ, and a format to launch"))],
        "hears": [("Les questions posées avant l'achat", "The questions asked before buying"),
                  ("Les problèmes rencontrés après", "The problems met afterwards"),
                  ("Les besoins qui montent, saison après saison", "The needs rising, season after season")],
        "cannot": [("Le ton du débat public : c'est le social listening.", "The tone of the public debate: that is social listening.")],
        "cases": ["market-opportunities", "product-test", "rejuvenate"],
        "tools": [], "offers": ["social-insights"],
        "faq": [(("Quelles données de recherche utilisez-vous ?", "Which search data do you use?"),
                 ("Les volumes et les formulations de recherche sur Google, YouTube et Amazon, agrégés et anonymes, sur les marchés et les langues de votre périmètre.",
                  "Search volumes and phrasings on Google, YouTube and Amazon, aggregated and anonymous, on the markets and languages of your perimeter.")),
                (("Est-ce du SEO ?", "Is this SEO?"),
                 ("Non, même si vos équipes SEO s'en servent. Nous lisons les recherches pour comprendre les besoins, pas pour positionner des pages.",
                  "No, even if your SEO teams use it. We read searches to understand needs, not to rank pages."))],
    },
]

HUB = {
    "file": "expertise.html",
    "seo_title": ("Expertise : la social intelligence, six façons d'écouter | Licter", "Expertise: social intelligence, six ways of listening | Licter"),
    "seo_desc": ("Social, audience, influence, IA, temps réel et recherche : six façons d'écouter, combinées et lues par un analyste pour répondre à une question business.",
                 "Social, audience, influence, AI, live and search: six ways of listening, combined and read by an analyst to answer a business question."),
    "h1": ("La social intelligence, six façons d'écouter.", "Social intelligence, six ways of listening."),
    "lead": ("Chaque question demande sa façon d'écouter : ce que les gens disent, qui ils sont, qui les influence, ce qu'ils demandent à l'IA, ce qui se passe en direct, ce qu'ils cherchent. Nous les combinons, et un analyste lit l'ensemble.",
             "Each question calls for its own way of listening: what people say, who they are, who influences them, what they ask AI, what happens live, what they search for. We combine them, and an analyst reads the whole."),
    "ex_t": ("Une question, plusieurs écoutes", "One question, several ways of listening"),
    "ex_q": ("« Pourquoi notre nouvelle gamme ne décolle pas ? »", "“Why is our new range not taking off?”"),
    "ex": [("social", ("On en parle peu, et surtout du prix.", "Little talk about it, and mostly about the price.")),
           ("audience", ("Ceux qui en parlent ne sont pas la cible visée.", "The people talking about it are not the intended target.")),
           ("influence", ("Aucune voix de la catégorie ne l'a encore reprise.", "No voice in the category has picked it up yet.")),
           ("search", ("Les recherches portent sur un format que la gamme n'a pas.", "Searches are about a format the range does not have.")),
           ("ai", ("Les assistants IA recommandent deux concurrents.", "AI assistants recommend two competitors."))],
    "ex_read_k": ("Notre lecture", "Our read"),
    "ex_read": ("Un problème de format et de relais, pas de notoriété : lancer le format recherché, et le confier aux voix que la cible suit déjà.",
                "A format and relay problem, not an awareness one: launch the format people search for, and hand it to the voices the target already follows."),
    "book_t": ("Quelle question voulez-vous écouter ?", "Which question do you want to listen to?"),
}
LIST = {x["key"]: x for x in LISTENINGS}


# ------------------------------------------------------------------ blocks
def uc_link(key):
    """a use case, linked in the visitor's language (js/i18n.js swaps it)"""
    c = next(x for x in C.CASES if x["key"] == key)
    return U.case_path(c, FR), U.case_path(c, EN), c


def crumbs(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (h, t(l)) if h else '<li aria-current="page">%s</li>' % t(l) for l, h in items)
    return '  <nav class="crumbs shell" aria-label="%s"><ol>%s</ol></nav>' % (a(S["crumbs"]), lis)


def listening_body(x, offers_html):
    i = LISTENINGS.index(x) + 1
    demo = "".join('<li><small>%s</small><b>%s</b></li>' % (t(k), t(v)) for k, v in x["demo"])
    hears = "".join("<li>%s</li>" % t(h) for h in x["hears"])
    cannot = "".join("<li>%s</li>" % t(h) for h in x["cannot"])
    answers = ""
    for key in x["cases"]:
        fr, en, c = uc_link(key)
        q = ("« %s »" % c["questions"][0][FR], "“%s”" % c["questions"][0][EN])
        answers += ('<li><a href="%s" data-en="%s"><span class="xw__s">%s</span><span class="xw__arrow" aria-hidden="true">→</span>'
                    '<span class="xw__o">%s</span></a></li>') % (fr, en, t(q), t(c["name"]))
    tools = "".join('<li><a href="%s"><span class="of-oth__n">%s</span><b>%s</b><span>%s</span><i aria-hidden="true">→</i></a></li>' % (
        TOOLS[k][0], TOOLS[k][1][0], TOOLS[k][1], t(TOOLS[k][2])) for k in x["tools"])
    offs = "".join('<li><a href="%s"><span class="of-oth__n">0%d</span><b>%s</b><span>%s</span><i aria-hidden="true">→</i></a></li>' % (
        OFFERS[k]["file"], OFFERS[k]["n"], t(OFFERS[k]["name"]), t(OFFERS[k]["short"])) for k in x["offers"])
    how = ""
    if tools:
        how += '<div><p class="of-fit__k">%s</p><ul class="of-oth">%s</ul></div>' % (t(S["tools_k"]), tools)
    how += '<div><p class="of-fit__k">%s</p><ul class="of-oth">%s</ul></div>' % (t(S["offers_k"]), offs)
    others = "".join('<li><a href="%s">%s</a></li>' % (y["file"], t(y["name"])) for y in LISTENINGS if y is not x)
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in x["faq"])
    return f'''<main id="content">
{crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], "expertise.html"), (x["name"], None)])}

  <section class="xh of-hero xe-hero">
    <div class="shell xh__grid">
      <div class="xh__copy">
        <p class="xh__kick">{t(S["kicker"])} <span>0{i}</span> · {t(x["name"])}</p>
        <h1 class="xh__title">{t(x["h1"])}</h1>
        <p class="xh__lead">{t(x["lead"])}</p>
        <div class="xh__actions">
          <a class="btn btn--primary" href="#book">{t(S["book"])} <span aria-hidden="true">→</span></a>
          <a class="xh__link" href="#answers">{t(S["answers_link"])} <span aria-hidden="true">↓</span></a>
        </div>
      </div>
      <div class="of-hero__demo">
        <figure class="xo__demo" aria-label="{a(S["demo_cap"])}">
          <figcaption>{t(S["demo_cap"])} <span>{t(S["illus"])}</span></figcaption>
          <ul class="xe-sig">{demo}</ul>
        </figure>
      </div>
    </div>
  </section>

  <section class="of-fit">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["limits_t"])}</h2></div>
      <div class="of-fit__grid">
        <div class="of-fit__col of-fit__col--yes"><p class="of-fit__k">{t(S["hears"])}</p><ul>{hears}</ul></div>
        <div class="of-fit__col of-fit__col--no"><p class="of-fit__k">{t(S["cannot"])}</p><ul>{cannot}</ul></div>
      </div>
    </div>
  </section>

  <section class="xw" id="answers">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["answers_t"])}</h2></div>
      <ul class="xw__list">{answers}</ul>
    </div>
  </section>

  <section class="of-steps xe-how">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["how_t"])}</h2></div>
      <div class="xe-how__grid">{how}</div>
      <p class="of-fit__k xe-others__k">{t(S["others_t"])}</p>
      <ul class="xe-others">{others}<li><a href="expertise.html">{t(S["all"])} <span aria-hidden="true">→</span></a></li></ul>
    </div>
  </section>

  <section class="of-faq">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["faq"])}</h2></div>
      <div class="faq">{faq}</div>
    </div>
  </section>

{book(HUB["book_t"], offers_html)}
</main>'''


def hub_body(offers_html):
    six = "".join(
        '<li><a href="%s"><span class="xe-six__n">0%d</span><span class="xe-six__ico" aria-hidden="true">%s</span>'
        '<b>%s</b><span class="xe-six__d">%s</span><i aria-hidden="true">→</i></a></li>' % (
            x["file"], i + 1, ICON_SVG.get(x["icon"], ""), t(x["name"]), t(x["short"]))
        for i, x in enumerate(LISTENINGS))
    ex = "".join('<li><a href="%s"><b>%s</b></a><span>%s</span></li>' % (LIST[k]["file"], t(LIST[k]["name"]), t(v)) for k, v in HUB["ex"])
    return f'''<main id="content">
{crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], None)])}

  <section class="xh of-hero xe-hero">
    <div class="shell xh__grid">
      <div class="xh__copy">
        <p class="xh__kick"><span>{t(S["expertise"])}</span> · <span>{t(S["kicker"])}</span></p>
        <h1 class="xh__title">{t(HUB["h1"])}</h1>
        <p class="xh__lead">{t(HUB["lead"])}</p>
        <div class="xh__actions">
          <a class="btn btn--primary" href="#book">{t(S["book"])} <span aria-hidden="true">→</span></a>
        </div>
      </div>
      <nav class="xe-six-wrap" aria-label="{a(S["list_t"])}">
        <ol class="xe-six">{six}</ol>
      </nav>
    </div>
  </section>

  <section class="of-fit xe-ex">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(HUB["ex_t"])}</h2></div>
      <p class="xe-ex__q">{t(HUB["ex_q"])}</p>
      <ul class="xe-ex__list">{ex}</ul>
      <p class="xe-ex__read"><span>{t(HUB["ex_read_k"])}</span>{t(HUB["ex_read"])}</p>
    </div>
  </section>

{book(HUB["book_t"], offers_html)}
</main>'''


def book(title, offers_html):
    m = re.search(r'  <!-- MOCK: the callback form.*?</section>', offers_html, re.S)
    return re.sub(r'<h2 class="block__title">.*?</h2>', '<h2 class="block__title">%s</h2>' % t(title), m.group(0), count=1)


def ld(file, name, desc, crumbs_, faq=None):
    url = "%s/%s" % (SITE, file)
    out = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + f} for i, (n, f) in enumerate(crumbs_)]},
        {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "provider": U.ORG, "url": url, "areaServed": "Worldwide"}]
    if faq:
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q[EN], "acceptedAnswer": {"@type": "Answer", "text": r[EN]}} for q, r in faq]})
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in out)


def write(file, seo_title, seo_desc, body, ld_tags, offers_html):
    head = offers_html[:offers_html.index("</head>")]
    title, desc = html.escape(seo_title[EN]), html.escape(seo_desc[EN])
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % desc, head)
    head = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % title, head)
    head = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % desc, head)
    head = head.replace('<meta name="twitter:card"', '<link rel="canonical" href="%s/%s" />\n<meta name="twitter:card"' % (SITE, file), 1)
    head += ld_tags + "\n"
    main0, main1 = offers_html.index('<main id="content">'), offers_html.index("</main>") + len("</main>")
    shell = offers_html[offers_html.index("</head>"):main0] + "%s" + offers_html[main1:]
    shell = shell.replace('<body class="xpage">', '<body class="xpage xepage">', 1)
    (ROOT / file).write_text("<!-- Generated by tools/build-expertise.py: edit that file, not this one. -->\n" + head + shell % body)


# the icons of the menu (js/ui.js), as inline SVG for the overview
ICON_SVG = {}


def main():
    global ICON_SVG
    ui = (ROOT / "js" / "ui.js").read_text()
    for k in ("chart", "audiences", "influence", "ai", "bell", "search"):
        m = re.search(r"\n    %s: '(<svg.*?</svg>)'," % k, ui)
        if m:
            ICON_SVG[k] = m.group(1)
    O.NEW.clear()
    offers_html = (ROOT / "offers.html").read_text()
    for x in LISTENINGS:
        write(x["file"], x["seo_title"], x["seo_desc"], listening_body(x, offers_html),
              ld(x["file"], x["name"][EN], x["seo_desc"][EN], [("Home", ""), ("Expertise", "expertise.html"), (x["name"][EN], x["file"])], x["faq"]),
              offers_html)
    write(HUB["file"], HUB["seo_title"], HUB["seo_desc"], hub_body(offers_html),
          ld(HUB["file"], "Social intelligence", HUB["seo_desc"][EN], [("Home", ""), ("Expertise", "expertise.html")]), offers_html)
    for k in ("menu_label", "menu_aside", "all", "foot_link"):
        t(S[k])
    O.write_dict("expertise pages", "build-expertise.py", O.NEW)
    print("%d expertise pages written, %d strings in js/fr.js" % (len(LISTENINGS) + 1, len(O.NEW)))


if __name__ == "__main__":
    main()
