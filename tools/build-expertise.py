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
import html, importlib, importlib.util, json, math, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bo", ROOT / "tools" / "build-offers.py")
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
U, C = O.U, O.C
FR, EN = 0, 1
SITE = O.SITE
t, a = O.t, O.a
GUIDE = {"social": "sl_guide", "audience": "al_guide"}   # expertise key -> tools/<module>.py, a qa_roller section

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
        "seo_title": ("Agence et cabinet de social listening | Licter", "Social listening agency and consultancy | Licter"),
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
        "seo_title": ("Audience intelligence : qui sont vraiment vos audiences | Licter", "Audience intelligence: who your audiences really are | Licter"),
        "seo_desc": ("Audience intelligence : centres d'intérêt, affinités de marque et médias. Nous profilons vos communautés à partir de leur comportement observé, pas déclaré.",
                     "Audience intelligence: interests, brand affinities and media. We profile your communities from observed behaviour, not declared answers."),
        "h1": ("Audience intelligence : qui sont vraiment vos audiences, au-delà de l'âge et du sexe.", "Audience intelligence: who your audiences really are, beyond age and gender."),
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
        "faq": [(("Audience intelligence ou social listening : quelle différence ?", "Audience intelligence or social listening: what is the difference?"),
                 ("Le social listening lit ce qui se dit sur votre marque et votre marché. L'audience intelligence, que nous appelons audience listening, décrit les gens eux-mêmes : ce qu'ils suivent, partagent et consomment, qu'ils parlent de vous ou non. L'un mesure une conversation, l'autre dessine une communauté ; les deux se croisent souvent dans une même étude.",
                  "Social listening reads what is said about your brand and your market. Audience intelligence, which we call audience listening, describes the people themselves: what they follow, share and consume, whether they talk about you or not. One measures a conversation, the other draws a community; the two often meet in the same study.")),
                (("D'où viennent les données d'audience ?", "Where does the audience data come from?"),
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


# ------------------------------------------------------------------ additions
# Per listening: how it runs (with its timing), the client interview that fits
# it, and two more questions. MOCK: timings and answers to be validated.
EXTRA = {
    "social": {
        "book_t": ("Parlons de ce qui se dit sur vous.", "Let's talk about what is said about you."),
        "doc": (("Synthèse de veille", "Monitoring summary"), ("Constructeur automobile", "Car maker"), ("Forums, presse auto · 30 jours · 8 400 posts", "Forums, motoring press · 30 days · 8,400 posts")),
        "voice": "orange",
        "steps": [(("J0", "Day 0"), ("Cadrage", "Framing"), ("Le périmètre, les marchés, les langues et les sources.", "The perimeter, the markets, the languages and the sources.")),
                  (("J+2", "Day 2"), ("Collecte", "Collection"), ("Les requêtes paramétrées, le bruit écarté.", "Queries set up, the noise removed.")),
                  (("J+5", "Day 5"), ("Lecture", "Reading"), ("Un analyste lit les sujets, la tonalité et qui les porte.", "An analyst reads the topics, the tone and who carries them.")),
                  (("J+7", "Day 7"), ("Restitution", "Readout"), ("Une synthèse, et ce qu'il faut en faire.", "A summary, and what to do with it."))],
        "faq": [(("Combien de temps avant une première lecture ?", "How long before a first read?"),
                 ("Environ une semaine après le cadrage, plus vite pour un sujet urgent.", "About a week after framing, faster for an urgent topic.")),
                (("Faut-il déjà avoir un outil de veille ?", "Do we need a monitoring tool already?"),
                 ("Non. Nous travaillons avec nos plateformes. Si vous en avez une, nous pouvons aussi la reprendre et la faire parler.",
                  "No. We work with our own platforms. If you have one, we can also take it over and make it speak."))],
    },
    "audience": {
        "book_t": ("Parlons de vos audiences.", "Let's talk about your audiences."),
        "doc": (("Profil d'audience", "Audience profile"), ("Marque alimentaire", "Food brand"), ("Panel comportemental · 1,2 M de profils", "Behavioural panel · 1.2M profiles")),
        "voice": "loreal",
        "steps": [(("J0", "Day 0"), ("Cadrage", "Framing"), ("Les audiences à profiler, et la décision à éclairer.", "The audiences to profile, and the decision to inform.")),
                  (("J+3", "Day 3"), ("Profilage", "Profiling"), ("Le panel comportemental fait apparaître les communautés.", "The behavioural panel brings out the communities.")),
                  (("J+7", "Day 7"), ("Analyse", "Analysis"), ("Affinités, médias et recoupements, lus par un analyste.", "Affinities, media and overlaps, read by an analyst.")),
                  (("J+10", "Day 10"), ("Restitution", "Readout"), ("Les communautés à prioriser, et comment les toucher.", "The communities to prioritise, and how to reach them."))],
        "faq": [(("Est-ce conforme au RGPD ?", "Is it GDPR-compliant?"),
                 ("Oui : uniquement des données publiques, agrégées en communautés, jamais de profils individuels.", "Yes: public data only, aggregated into communities, never individual profiles.")),
                (("Que fait-on des résultats ?", "What do we do with the results?"),
                 ("Un plan média, des messages et des créateurs par communauté : la restitution se termine par des recommandations.",
                  "A media plan, messages and creators for each community: the readout ends with recommendations."))],
    },
    "influence": {
        "book_t": ("Parlons des voix qui comptent pour vous.", "Let's talk about the voices that matter to you."),
        "doc": (("Shortlist d'influence", "Influence shortlist"), ("Marque de mode", "Fashion brand"), ("Instagram, TikTok, presse · 90 jours", "Instagram, TikTok, press · 90 days")),
        "voice": "lvmh",
        "steps": [(("J0", "Day 0"), ("Cadrage", "Framing"), ("La catégorie, l'objectif et les audiences visées.", "The category, the goal and the target audiences.")),
                  (("J+3", "Day 3"), ("Repérage", "Mapping"), ("Qui lance les sujets, et qui les relaie.", "Who starts topics, and who relays them.")),
                  (("J+6", "Day 6"), ("Vérification", "Vetting"), ("Recouvrement d'audience, prises de position, risques.", "Audience overlap, past stances, risks.")),
                  (("J+8", "Day 8"), ("Shortlist", "Shortlist"), ("Une liste classée et argumentée, prête pour l'agence.", "A ranked, argued list, ready for the agency."))],
        "faq": [(("Comment repérez-vous les risques ?", "How do you spot the risks?"),
                 ("Nous relisons les prises de position publiques passées et les controverses, et les signalons avant tout contrat.",
                  "We go through past public stances and controversies, and flag them before any contract.")),
                (("Faut-il de gros comptes pour être efficace ?", "Do you need big accounts to be effective?"),
                 ("Non. Le recouvrement avec votre audience compte plus que le nombre d'abonnés : les comptes moyens portent souvent mieux.",
                  "No. The overlap with your audience matters more than the follower count: mid-sized accounts often carry better."))],
    },
    "ai": {
        "book_t": ("Parlons de ce que les IA disent de vous.", "Let's talk about what AI says about you."),
        "doc": (("Audit des réponses IA", "AI answers audit"), ("Mutuelle santé", "Health insurer"), ("5 assistants IA · 40 questions testées", "5 AI assistants · 40 questions tested")),
        "voice": "dassault",
        "steps": [(("J0", "Day 0"), ("Cadrage", "Framing"), ("Les questions que posent vos clients, et les modèles à interroger.", "The questions your customers ask, and the models to question.")),
                  (("J+2", "Day 2"), ("Interrogation", "Prompting"), ("Les mêmes questions, posées à chaque modèle.", "The same questions, put to each model.")),
                  (("J+5", "Day 5"), ("Lecture", "Reading"), ("Ce qu'ils recommandent, citent, oublient ou déforment.", "What they recommend, cite, leave out or get wrong.")),
                  (("J+7", "Day 7"), ("Plan", "Plan"), ("Les sources à corriger ou à nourrir.", "The sources to correct or to feed."))],
        "faq": [(("À quelle fréquence mesurez-vous ?", "How often do you measure?"),
                 ("Une première mesure, puis chaque mois ou chaque trimestre, avec les mêmes questions pour comparer.",
                  "A first measure, then every month or quarter, with the same questions so it can be compared.")),
                (("Est-ce différent du SEO ?", "Is it different from SEO?"),
                 ("Oui. Les assistants IA ne classent pas des pages, ils synthétisent des sources. Nous lisons ces synthèses, et les sources qui les nourrissent.",
                  "Yes. AI assistants do not rank pages, they synthesise sources. We read those syntheses, and the sources feeding them."))],
    },
    "live": {
        "book_t": ("Parlons de votre veille en temps réel.", "Let's talk about your real-time monitoring."),
        "doc": (("Journal d'alerte", "Alert log"), ("Groupe agroalimentaire", "Food group"), ("Suivi 24/7 · réseaux, presse, forums", "24/7 watch · social, press, forums")),
        "voice": "sncf",
        "steps": [(("48 h", "48 h"), ("Paramétrage", "Set-up"), ("Les requêtes, les seuils et les personnes à alerter.", "The queries, the thresholds and the people to alert.")),
                  (("24/7", "24/7"), ("Veille", "Watch"), ("La conversation suivie en continu, nuits et week-ends compris.", "The conversation followed continuously, nights and weekends included.")),
                  (("15 min", "15 min"), ("Alerte", "Alert"), ("Un analyste qualifie le signal avant de vous prévenir.", "An analyst qualifies the signal before alerting you.")),
                  (("Hebdo", "Weekly"), ("Bilan", "Review"), ("Ce qui a bougé, et ce qu'il faut surveiller ensuite.", "What moved, and what to watch next."))],
        "faq": [(("En combien de temps êtes-vous opérationnels ?", "How fast can you be up and running?"),
                 ("48 heures pour paramétrer les requêtes, les seuils et les contacts d'alerte.", "48 hours to set up the queries, thresholds and alert contacts.")),
                (("Qui reçoit les alertes ?", "Who receives the alerts?"),
                 ("Les personnes que vous désignez, par e-mail ou messagerie, avec la qualification de l'analyste et une recommandation.",
                  "The people you name, by email or messaging, with the analyst's qualification and a recommendation."))],
    },
    "search": {
        "book_t": ("Parlons de ce que vos clients cherchent.", "Let's talk about what your customers search for."),
        "doc": (("Étude des recherches", "Search study"), ("Marque alimentaire", "Food brand"), ("Google, YouTube, Amazon · 12 mois", "Google, YouTube, Amazon · 12 months")),
        "voice": "seb",
        "steps": [(("J0", "Day 0"), ("Cadrage", "Framing"), ("Les marchés, les langues et les produits à lire.", "The markets, the languages and the products to read.")),
                  (("J+2", "Day 2"), ("Collecte", "Collection"), ("Les recherches sur Google, YouTube et Amazon.", "Searches on Google, YouTube and Amazon.")),
                  (("J+5", "Day 5"), ("Lecture", "Reading"), ("Les questions, les problèmes et les besoins qui montent.", "The questions, the problems and the rising needs.")),
                  (("J+7", "Day 7"), ("Restitution", "Readout"), ("Les besoins non couverts, et ce qu'il faut lancer.", "The unmet needs, and what to launch."))],
        "faq": [(("Sur quels marchés ?", "On which markets?"),
                 ("Tous ceux de votre périmètre, dans leur langue : nous lisons les formulations locales, pas des traductions.",
                  "All those in your perimeter, in their own language: we read local phrasings, not translations.")),
                (("Combien de temps pour une première lecture ?", "How long for a first read?"),
                 ("Environ une semaine après le cadrage.", "About a week after framing."))],
    },
}
HUB_VOICE = "kantar"
HUB_FAQ = [
    (("Quelle écoute choisir ?", "Which way of listening should we pick?"),
     ("Celle que demande votre question. Nous les combinons souvent, et le premier échange sert justement à le déterminer.",
      "The one your question calls for. We often combine them, and the first conversation is there to decide it.")),
    (("Faut-il acheter un outil ou une licence ?", "Do we need to buy a tool or a licence?"),
     ("Non. Nos consultants utilisent nos plateformes : vous recevez la lecture, pas une licence à faire tourner.",
      "No. Our consultants use our platforms: you receive the read, not a licence to run.")),
    (("Dans quelles langues ?", "In which languages?"),
     ("Plus de vingt, lues par des analystes qui les parlent.", "More than twenty, read by analysts who speak them.")),
    (("Combien de temps pour une première réponse ?", "How long for a first answer?"),
     ("Une à deux semaines selon les écoutes, 48 heures pour une veille en direct.", "One to two weeks depending on the listening, 48 hours for live monitoring.")),
]
for _x in LISTENINGS:
    _x["faq"] = _x["faq"] + EXTRA[_x["key"]]["faq"]

S.update({
    "how_runs": ("Comment ça se passe", "How it runs"),
    "how_note": ("Durées indicatives pour une première lecture.", "Indicative timings for a first read."),
    "proof_k": ("Dans leurs mots", "In their words"),
    "proof_t": ("Ils en parlent", "They talk about it"),
    "magnet_k": ("Et chez vous ?", "And for you?"),
    "magnet_t": ("Recevez un exemple de livrable %s, dans votre secteur.", "Get a sample %s deliverable, in your sector."),
    "magnet_t_hub": ("Recevez un exemple de livrable, dans votre secteur.", "Get a sample deliverable, in your sector."),
    "magnet_d": ("Anonymisé, envoyé par un consultant sous 48 h : ce que vous recevriez vraiment.", "Anonymised, sent by a consultant within 48 hours: what you would actually receive."),
    "magnet_email": ("E-mail professionnel", "Work email"),
    "magnet_sector": ("Votre secteur", "Your sector"),
    "magnet_pick": ("Choisir…", "Choose…"),
    "magnet_btn": ("Recevoir l'exemple", "Get the sample"),
    "magnet_err": ("Indiquez un e-mail professionnel valide.", "Enter a valid work email."),
    "magnet_pick_err": ("Choisissez votre secteur.", "Choose your sector."),
    "magnet_consent": ("Votre e-mail sert uniquement à vous répondre.", "We use your email only to reply to you."),
    "privacy": ("Politique de confidentialité", "Privacy policy"),
    "magnet_done": ("C'est noté. Un consultant vous envoie un exemple sous 48 h.", "Noted. A consultant sends you a sample within 48 hours."),
    "magnet_alt": ("Plutôt lire d'abord ?", "Rather read first?"),
    "magnet_alt_link": ("Le guide des 12 questions", "The guide to the 12 questions"),
    "bar_offer": ("Mon flash offert", "My free flash"),
    "bar_call": ("Parler à un consultant", "Talk to a consultant"),
    "bar_chat": ("Discuter avec Antoine", "Chat with Antoine"),
    "hub_faq_t": ("Questions fréquentes", "Frequently asked questions"),
    "data_illus": ("Données illustratives", "Illustrative data"),
    "source": ("Source :", "Source:"),
    "oct": ("Octobre 2026", "October 2026"),
})
# 6. On French pages each English name gets a French gloss beside it: the
# English term is what people search for, the gloss is what it means.
GLOSS = {"social": "l'écoute des conversations", "audience": "l'écoute des audiences", "influence": "l'écoute de l'influence",
         "ai": "l'écoute des IA", "live": "l'écoute en temps réel", "search": "l'écoute des recherches"}
# 3. The overview shows three deliverables, drawn like those of the use cases
HUB_DLV = ["campaign-impact", "segmentation", "brand-risk"]
S.update({
    "dlv_t": ("Ce que vous recevez", "What you receive"),
    "dlv_lead": ("Trois livrables parmi d'autres : chaque écoute aboutit à un document que vos équipes peuvent utiliser.",
                 "Three deliverables among others: every way of listening ends in a document your teams can use."),
    "dlv_link": ("Voir le cas d'usage", "See the use case"),
    "all_cases": ("Voir les 12 cas d'usage", "See the 12 use cases"),
})

# French slugs of the static twins
FR_PATH = {"expertise.html": "/fr/expertise/"}
for _x in LISTENINGS:
    FR_PATH[_x["file"]] = "/fr/expertise/%s/" % _x["file"][len("expertise-"):-len(".html")]



# ------------------------------------------------------------------ new blocks
def logos():
    """the client logo wall, as on the use-case pages (English here)"""
    return U.clients(EN)


def steps_block(x):
    e = EXTRA[x["key"]]
    lis = "".join('<li><span class="ucv-day">%s</span><b>%s</b><p>%s</p></li>' % (t(d), t(n), t(p_)) for d, n, p_ in e["steps"])
    return ('  <section class="ucp ucv-how xe-steps">\n    <div class="shell">\n'
            '      <div class="xs__head"><h2 class="xs__title">%s</h2></div>\n'
            '      <ol class="ucv-time">%s</ol>\n      <p class="ucv-note">%s</p>\n    </div>\n  </section>') % (
        t(S["how_runs"]), lis, t(S["how_note"]))


def proof_block(x, voice=None):
    vid, time, quote, brand, who = C.VOICES[voice or EXTRA[x["key"]]["voice"]]
    q = ("« %s »" % quote[FR], "“%s”" % quote[EN])
    return ('  <section class="ucp xe-proof">\n    <div class="shell">\n'
            '      <a class="ucv-video xe-video" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">\n'
            '        <span class="ucv-video__shot"><img src="https://i.ytimg.com/vi_webp/%s/hqdefault.webp" width="480" height="360" alt="" loading="lazy" decoding="async" /><span class="reel__play" aria-hidden="true"></span><span class="reel__time">%s</span></span>\n'
            '        <span class="xe-video__k">%s</span>\n'
            '        <span class="ucv-video__q">%s</span>\n'
            '        <span class="ucv-video__who"><b>%s</b> · %s</span>\n'
            '      </a>\n    </div>\n  </section>') % (vid, vid, time, t(S["proof_k"]), t(q), html.escape(brand), html.escape(who))


def magnet_block(key, title):
    opts = '<option value="" disabled selected>%s</option>' % t(S["magnet_pick"]) + "".join('<option>%s</option>' % t(x) for x in U.SECTORS)
    return ('  <!-- MOCK: sends nothing yet (js/ui.js, .ucp-lead); wire to the CRM with the listening and the sector. -->\n'
            '  <section class="ucp ucp--cta" id="offre">\n    <div class="shell">\n      <div class="ucp__cta">\n'
            '        <div class="ucp__cta-copy">\n          <p class="ucp__cta-k">%s</p>\n          <h2 class="ucp__cta-t">%s</h2>\n          <p class="ucp__cta-d">%s</p>\n        </div>\n'
            '        <form class="ucp-lead" data-case="%s" novalidate>\n          <div class="ucp-lead__row">\n'
            '            <label class="ucp-lead__f"><span>%s</span><input class="fld__input" name="email" type="email" autocomplete="email" placeholder="name@company.com" required /></label>\n'
            '            <label class="ucp-lead__f"><span>%s</span><select class="fld__input" name="sector" required>%s</select></label>\n'
            '          </div>\n          <button class="btn btn--primary" type="submit">%s <span aria-hidden="true">→</span></button>\n'
            '          <p class="fld__error" hidden>%s</p>\n          <p class="fld__error ucp-lead__sector-err" hidden>%s</p>\n'
            '          <p class="consent">%s <a href="privacy.html">%s</a>.</p>\n        </form>\n'
            '        <p class="ucp-lead__alt">%s <a href="guide.html">%s&nbsp;<span aria-hidden="true">→</span></a></p>\n'
            '        <p class="ucp-lead__done" role="status" hidden>%s</p>\n      </div>\n    </div>\n  </section>') % (
        t(S["magnet_k"]), title, t(S["magnet_d"]), key, t(S["magnet_email"]), t(S["magnet_sector"]), opts, t(S["magnet_btn"]),
        t(S["magnet_err"]), t(S["magnet_pick_err"]), t(S["magnet_consent"]), t(S["privacy"]), t(S["magnet_alt"]), t(S["magnet_alt_link"]), t(S["magnet_done"]))


def bar():
    return ('<div class="ucp-bar" aria-hidden="true" hidden>\n'
            '  <button class="ucp-bar__chat" type="button" tabindex="-1" aria-label="%s"><img src="/assets/img/team/founder-antoine-160.webp" alt="" width="44" height="44" /><i aria-hidden="true"></i></button>\n'
            '  <a class="btn btn--primary" href="#offre" tabindex="-1">%s</a>\n'
            '  <a class="btn btn--ghost" href="#book" tabindex="-1">%s</a>\n</div>') % (a(S["bar_chat"]), t(S["bar_offer"]), t(S["bar_call"]))

# ------------------------------------------------------------------ blocks
def uc_link(key):
    """a use case, linked in the visitor's language (js/i18n.js swaps it)"""
    c = next(x for x in C.CASES if x["key"] == key)
    return U.case_path(c, FR), U.case_path(c, EN), c


def crumbs(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (h, t(l)) if h else '<li aria-current="page">%s</li>' % t(l) for l, h in items)
    return '  <nav class="crumbs shell" aria-label="%s"><ol>%s</ol></nav>' % (a(S["crumbs"]), lis)


# ------------------------------------------------------------------ the six listenings
# These pages use the components of the tool and offer pages (.tk-*, .ucc):
# a hero with a visual, a bento, the use cases as a photo carousel, limits
# and complements as a card carousel, the FAQ beside its title. Each way of
# listening keeps its own colour (--brand). No illustrative figure.
CHANNEL = {k: "#EAA93D" for k in ("social", "audience", "influence", "ai", "live", "search")}   # one colour: Licter's amber
PHOTO = {"social": "team/morning/work-three-800", "audience": "team/morning/work-sofa-800", "influence": "team/meeting-portrait-800",
         "ai": "team/consultant-dashboard-800", "live": "team/morning/work-standing-800", "search": "team/morning/work-laptop-800"}
UC_PHOTO = {"communication": "working-session-1200", "brand": "client-conversation-1200", "audiences": "team-sofa-1200", "trends": "two-colleagues-1200"}

S.update({
    "of6": ("sur 6", "of 6"),
    "hears_k": ("CE QU'ELLE ENTEND", "WHAT IT PICKS UP"),
    "hears_t": ("Ce que %s permet d'entendre.", "What %s lets you hear."),
    "answers_k": ("CAS D'USAGE", "USE CASES"),
    "answers_lead": ("Chaque question mène au cas d'usage où cette écoute fait la différence.", "Each question leads to the use case where this listening makes the difference."),
    "runs_k": ("MÉTHODE", "METHOD"),
    "lim_k": ("LIMITES ET COMPLÉMENTS", "LIMITS AND COMPLEMENTS"),
    "lim_t": ("Ses limites, et ce qui la complète.", "Its limits, and what completes it."),
    "lim_tag": ("Sa limite", "Its limit"),
    "lim_sub": ("Ce qu'elle ne dit pas seule", "What it cannot say on its own"),
    "tool_tag": ("La plateforme", "The platform"),
    "offer_tag": ("Dans l'offre", "In the offer"),
    "see_page": ("Voir la page", "See the page"),
    "voice_k": ("DANS LEURS MOTS", "IN THEIR WORDS"),
    "voice_t": ("Ils en parlent.", "They talk about it."),
    "others_k": ("TOUTES LES ÉCOUTES", "EVERY WAY OF LISTENING"),
    "others_t2": ("Les cinq autres écoutes.", "The five other ways of listening."),
    "six_k": ("SIX FAÇONS D'ÉCOUTER", "SIX WAYS OF LISTENING"),
    "six_lead": ("Chaque écoute répond à une partie de la question. Ouvrez celle qui vous concerne.", "Each one answers part of the question. Open the one that concerns you."),
    "discover": ("Découvrir", "Discover"),
    "ex_k": ("EXEMPLE", "EXAMPLE"),
    "photo_cap": ("L'équipe Licter au travail", "The Licter team at work"),
})


def head(kick, title, lead=None):
    return '<div class="tk-head" data-reveal><p class="tk-k">%s</p><h2 class="tk-h2">%s</h2>%s</div>' % (
        kick, title, '<p class="tk-sub">%s</p>' % lead if lead else "")


def sec(id_, inner, band=False):
    return '  <section class="tk-sec%s"%s>\n    <div class="shell">\n%s\n    </div>\n  </section>\n\n' % (
        " tk-sec--band" if band else "", ' id="%s"' % id_ if id_ else "", inner)


def tk_crumbs(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (h, t(l)) if h else '<li aria-current="page">%s</li>' % t(l) for l, h in items)
    return '<nav class="tk-crumbs" aria-label="%s"><ol>%s</ol></nav>' % (a(S["crumbs"]), lis)


def art(photo, icon):
    """the hero visual: a photo of the team on a panel in the listening's colour"""
    return ('<div class="tk-net"><span class="tk-net__wm xe-wm" aria-hidden="true">%s</span>'
            '<figure class="tk-shot"><img src="/assets/img/%s.webp" alt="%s" width="800" height="1200" decoding="async" fetchpriority="high" /></figure>'
            '<div class="tk-tile"><span class="tk-tile__net">%s</span></div></div>') % (icon, photo, a(S["photo_cap"]), icon)


def prog(keys):
    """the use cases: a large photo, the cases as tabs with a progress bar (js/ui.js)"""
    slides, tabs = "", ""
    for i, key in enumerate(keys):
        fr, en, c = uc_link(key)
        fam = next(f for f in C.FAMILIES if f["key"] == c["family"])
        q = ("« %s »" % c["questions"][0][FR], "“%s”" % c["questions"][0][EN])
        slides += ('<a class="tk-prog__slide%s" href="%s" data-en="%s" data-i="%d"%s><img src="/assets/img/team/%s.webp" alt="" width="1200" height="800" loading="%s" decoding="async" />'
                   '<span class="tk-prog__go"><b>%s</b><span>%s</span></span></a>') % (
            " is-on" if i == 0 else "", fr, en, i, "" if i == 0 else ' tabindex="-1"', UC_PHOTO[c["family"]], "eager" if i == 0 else "lazy", t(q), t(S["dlv_link"]))
        tabs += ('<button class="tk-prog__tab%s" type="button" role="tab" aria-selected="%s" data-i="%d"><span class="tk-prog__pill">%s</span>'
                 '<span class="tk-prog__name">%s</span><i class="tk-prog__bar" aria-hidden="true"></i></button>') % (
            " is-on" if i == 0 else "", "true" if i == 0 else "false", i, t(fam["name"]), t(c["name"]))
    return '<div class="tk-prog" data-auto="5500"><div class="tk-prog__stage">%s</div><div class="tk-prog__tabs" role="tablist">%s</div></div>' % (slides, tabs)


def offer_cards(x):
    """limits and complements: the limit, the platforms, the offers"""
    icon = ICON_SVG.get(x["icon"], "")
    mark = '<span class="tk-offer__net">%s</span>' % icon
    cards = '<article class="tk-offer tk-offer--limit"><div class="tk-offer__img"><span class="tk-offer__art tk-offer__art--limit" aria-hidden="true">!</span></div><div class="tk-offer__body"><p class="tk-offer__tag"><i aria-hidden="true">!</i>%s</p><h3>%s</h3><p>%s</p></div><p class="tk-offer__foot"><span class="tk-offer__logo">%s</span><span><b>%s</b><small>%s</small></span></p></article>' % (
        t(S["lim_tag"]), t(x["name"]), t(x["cannot"][0]), mark, t(x["name"]), t(S["lim_sub"]))
    for k in x["tools"]:
        f, nm, d = TOOLS[k]
        cards += ('<article class="tk-offer tk-offer--tool"><div class="tk-offer__img"><img src="/assets/img/shots/%s.webp" alt="" width="1200" height="750" loading="lazy" decoding="async" /></div>'
                  '<div class="tk-offer__body"><p class="tk-offer__tag"><i aria-hidden="true">＋</i>%s</p><h3>%s</h3><p>%s</p></div>'
                  '<a class="tk-offer__foot" href="%s"><span class="tk-offer__logo"><img src="/assets/img/tools/%s.png" alt="" width="96" height="96" loading="lazy" decoding="async" /></span><span><b>%s</b><small>%s</small></span><i aria-hidden="true">↗</i></a></article>') % (
            k, t(S["tool_tag"]), nm, t(d), f, k, nm, t(S["see_page"]))
    for k in x["offers"]:
        o = OFFERS[k]
        cards += ('<article class="tk-offer tk-offer--offer of-acc--%s"><div class="tk-offer__img"><img src="/assets/img/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" /></div>'
                  '<div class="tk-offer__body"><p class="tk-offer__tag"><i aria-hidden="true">0%d</i>%s</p><h3>%s</h3><p>%s</p></div>'
                  '<a class="tk-offer__foot" href="%s"><span class="tk-offer__logo xe-offer-n">0%d</span><span><b>%s</b><small>%s</small></span><i aria-hidden="true">↗</i></a></article>') % (
            O.CARD_ACCENT[k], "team/" + O.HUB_PHOTO[k], o["n"], t(S["offer_tag"]), t(o["name"]), t(o["short"]), o["file"], o["n"], t(o["name"]), t(S["see_page"]))
    return ('<div class="tk-offers"><div class="tk-offers__track" tabindex="0">%s</div>'
            '<button class="tk-offers__nav tk-offers__nav--prev" type="button" aria-label="%s">‹</button>'
            '<button class="tk-offers__nav tk-offers__nav--next" type="button" aria-label="%s">›</button></div>') % (
        cards, a(("Précédent", "Previous")), a(("Suivant", "Next")))


def others_list(x=None):
    return '<ul class="tk-nets">%s</ul>' % "".join(
        '<li><a href="%s" style="--c:%s;--i:#13162D"><span class="tk-nets__mark">%s</span><span>%s</span></a></li>' % (
            y["file"], CHANNEL[y["key"]], ICON_SVG.get(y["icon"], ""), t(y["name"])) for y in LISTENINGS if y is not x)


def faq_block(title, items):
    return ('<div class="tk-faq"><div class="tk-head" data-reveal><p class="tk-k">%s</p><h2 class="tk-h2">%s</h2></div>'
            '<div class="faq" data-reveal>%s</div></div>') % (t(S["faq"]), t(title), "".join(
                "<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in items))


def voice(key):
    return sec("", '<div class="xe-voice__grid">%s<div class="xe-voice__reel">%s</div></div>' % (head(t(S["voice_k"]), t(S["voice_t"])), O.reel(key)))



# ------------------------------------------------------------------ the lead-magnet hero
# The hero of every expertise page sells one thing: a real, anonymised
# deliverable of that listening, sent by a consultant. Title in the home's
# register (two lines, the second in the channel colour), the cover of the
# sample and its form on the right. The form is the .ucp-lead of js/ui.js.
H1L = {"social": (("Ce que les gens disent,", "lu par des gens."), ("What people say,", "read by people.")),
       "audience": (("Qui sont vraiment", "vos audiences."), ("Who your audiences", "really are.")),
       "influence": (("Les voix qui portent,", "pas les plus suivies."), ("The voices that carry,", "not the most followed.")),
       "ai": (("Ce que les IA", "disent de vous."), ("What AI", "says about you.")),
       "live": (("Ce qui se passe,", "pendant que ça se passe."), ("What happens,", "while it happens.")),
       "search": (("Ce que les gens", "cherchent vraiment."), ("What people", "really search for.")),
       "hub": (("Six façons", "d'écouter un marché."), ("Six ways", "of listening to a market."))}
S.update({
    "lm_k": ("FLASH OFFERT", "FREE FLASH READ"),
    "lm_brand_ph": ("Votre marque", "Your brand"),
    "lm_yours": ("Sur votre marque", "On your brand"),
    "lm_btn": ("Recevoir mon flash offert", "Get my free flash read"),
    "lm_done": ("C'est noté. Un consultant vous envoie votre flash sous 48 h.", "Noted. A consultant sends you your flash read within 48 hours."),
    "lm_anon": ("Anonymisé · dans votre secteur", "Anonymised · in your sector"),
    "lm_t": ("Le flash %s de votre marque, offert.", "Your brand's %s flash read, free."),
    "lm_t_hub": ("Le flash de votre marque, offert.", "Your brand's flash read, free."),
    "lm_free": ("Gratuit", "Free"), "lm_anon2": ("Anonymisé", "Anonymised"), "lm_48": ("Sous 48 h", "Within 48 h"),
    "lm_from": ("Préparé et lu par un consultant, pas par un robot.", "Prepared and read by a consultant, not a robot."),
    "lm_call": ("Ou parler à un consultant", "Or talk to a consultant"),
    "lm_six": ("Les six écoutes", "The six listenings"),
})


# What the flash contains, per listening: what a consultant reads on the
# visitor's own brand, offered. MOCK: to be validated by Licter (A-FAIRE.md).
FLASH = {
    "social": [("Les 3 sujets qui montent autour de votre marque", "The 3 topics rising around your brand"), ("Leur tonalité, sujet par sujet", "Their tone, topic by topic"), ("Ce qu'il faut surveiller ensuite", "What to watch next")],
    "audience": [("Les 3 communautés qui suivent votre marque", "The 3 communities following your brand"), ("Ce qui les passionne", "What they care about"), ("Où les toucher", "Where to reach them")],
    "influence": [("Les 5 voix qui portent dans votre catégorie", "The 5 voices that carry in your category"), ("Leur recouvrement avec votre audience", "Their overlap with your audience"), ("Les risques à vérifier", "The risks to check")],
    "ai": [("Ce que ChatGPT, Gemini et Perplexity disent de vous", "What ChatGPT, Gemini and Perplexity say about you"), ("Les concurrents qu'ils recommandent", "The competitors they recommend"), ("Les sources qu'ils citent", "The sources they cite")],
    "live": [("Ce qui a fait bouger votre marque en 30 jours", "What moved your brand in 30 days"), ("Qui l'a porté", "Who carried it"), ("Les signaux à surveiller", "The signals to watch")],
    "search": [("Les 10 questions que votre marché tape le plus", "The 10 questions your market types most"), ("Les besoins qui montent", "The rising needs"), ("Ceux auxquels personne ne répond", "The ones nobody answers")],
    "hub": [("Ce qui se dit de votre marque", "What is said about your brand"), ("Ce que les IA en répondent", "What AI answers about it"), ("Ce que votre marché cherche", "What your market searches for")],
}


# articles and hubs each expertise page sends readers to (SEO audit, internal links)
READS = {
    "social": [("article-veille-reseaux-sociaux-entreprise.html", ("Veille des réseaux sociaux en entreprise : le guide", "Social media monitoring for companies: the guide")),
               ("sources.html", ("Les 22 réseaux que nous écoutons", "The 22 networks we listen to")),
               ("article-comment-doubler-limpact-de-votre-strategie-social-listening-en-6-mois.html", ("Doubler l'impact de votre social listening en 6 mois", "Doubling your social listening impact in 6 months"))],
    "live": [("article-veille-reseaux-sociaux-entreprise.html", ("Veille des réseaux sociaux en entreprise : le guide", "Social media monitoring for companies: the guide")),
             ("article-identifier-les-breaking-news-de-votre-secteur-comment-rester-informe-en-temps-reel.html", ("Identifier les breaking news de votre secteur", "Spotting your sector's breaking news")),
             ("article-shein-vs-bhv-dissection-d-une-crise-digitale-a-travers-la-social-data-intelligence.html", ("Shein vs BHV : dissection d'une crise digitale", "Shein vs BHV: anatomy of a digital crisis"))],
    "audience": [("use-cases.html", ("Nos cas d'usage audiences", "Our audience use cases")),
                 ("article-comment-orange-analyse-tiktok-grace-au-social-listening.html", ("Comment Orange analyse TikTok", "How Orange reads TikTok")),
                 ("article-comment-conquerir-le-marche-de-la-cosmetique-de-luxe-grace-au-social-listening.html", ("Conquérir la cosmétique de luxe", "Winning luxury cosmetics"))],
    "influence": [("article-licter-lvmh.html", ("LVMH : leader advocacy et social listening", "LVMH: leader advocacy and social listening")),
                  ("article-gp-explorer-3-squeezie-bat-les-records-daudience.html", ("GP Explorer 3 : Squeezie bat les records d'audience", "GP Explorer 3: Squeezie breaks audience records")),
                  ("article-comment-origins-associe-influence-et-technologie-pour-transformer-le-capital-risque.html", ("Origins : influence et capital-risque", "Origins: influence and venture capital"))],
    "ai": [("article-comment-loreal-utilise-le-social-listening-pour-capter-la-voix-du-consommateur.html", ("L'Oréal : ce que l'IA change au social listening", "L'Oréal: what AI changes in social listening")),
           ("article-social-listening-et-politique-comment-capter-la-voix-des-citoyens.html", ("Social listening et politique", "Social listening and politics"))],
    "search": [("article-la-consommation-devient-un-acte-militant-les-insights-de-kantar-sur-les-tendances-dachat.html", ("La consommation devient un acte militant, avec Kantar", "Consumption becomes activism, with Kantar")),
               ("article-veille-social-listening-2024.html", ("Les 7 changements de la veille en 2024", "The 7 changes in monitoring in 2024"))],
}


def reads(key):
    items = READS.get(key)
    if not items:
        return ""
    links = ", ".join(('<a href="/fr/cas-usage/audiences/" data-en="/en/use-cases/audiences/">%s</a>' % t(l)) if h == "use-cases.html"
                      else '<a href="%s">%s</a>' % (h, t(l)) for h, l in items)
    return sec("", '<p class="xp-line"><span>%s</span> %s</p>' % (t(("À lire", "Further reading")), links))


def lm_hero(kick, lines, lead, key, title, color, icon, cover_name, logos_html, bands=None, flash_key="hub"):
    """the hero offers a free flash read of the visitor's own brand"""
    items = "".join("<li>%s</li>" % t(it) for it in FLASH[flash_key])
    faces = "".join('<img src="/assets/img/team/%s-160.webp" alt="" width="160" height="160" />' % f for f in ("founder-antoine", "headshot-1", "headshot-2"))
    def fld(id_, lab, typ, auto, ph):
        return ('<div class="form__field"><label for="%s">%s</label><input id="%s" name="%s" type="%s" autocomplete="%s" placeholder="%s" required /></div>') % (
            id_, t(lab), id_, id_, typ, auto, ph)
    return f'''  <section class="xe-lmh">
    <div class="shell xe-lmh__grid">
      <div class="xe-lmh__copy">
        <h1 class="xe-lmh__h1"><span class="xe-lmh__kick">{kick}</span><span class="xe-lmh__l">{t((lines[0][0], lines[1][0]))}</span><span class="xe-lmh__l xe-lmh__l--c">{t((lines[0][1], lines[1][1]))}</span></h1>
        <p class="xe-lmh__lead">{t(lead)}</p>
        <ul class="xe-lmh__pills"><li>{t(S["lm_free"])}</li><li>{t(S["lm_yours"])}</li><li>{t(S["lm_48"])}</li></ul>
        <a class="xe-lmh__call" href="#book">{t(S["lm_call"])} <span aria-hidden="true">→</span></a>
      </div>
      <div class="xe-lm" id="offre">
        <div class="xe-cover" aria-hidden="true">
          <span class="xe-cover__sheet xe-cover__sheet--3"></span><span class="xe-cover__sheet xe-cover__sheet--2"></span>
          <span class="xe-cover__sheet xe-cover__sheet--1">
            <span class="xe-cover__band"></span>
            <span class="xe-cover__top"><img src="/assets/img/logo-navy.webp" alt="" width="44" height="48" /><small>{t(S["lm_k"])}</small></span>
            <span class="xe-cover__ico">{icon}</span>
            <b class="xe-cover__brand" data-empty="{a(S["lm_brand_ph"])}">{t(S["lm_brand_ph"])}</b>
            <small class="xe-cover__anon">{cover_name}</small>
          </span>
        </div>
        <div class="xe-lm__body">
          <!-- MOCK: sends nothing yet (js/ui.js, .form); wire to the CRM with the brand and the listening. -->
          <p class="xe-lm__t">{title}</p>
          <ul class="xe-lm__items">{items}</ul>
          <form class="form xe-gform" id="flash-{key}-form" novalidate>
            <div class="form__row">{fld("fl-brand", ("Votre marque", "Your brand"), "text", "organization", "E.g. Danone")}{fld("fl-email", ("E-mail professionnel", "Work email"), "email", "email", "camille@company.com")}</div>
            <button class="form__submit" type="submit">{t(S["lm_btn"])} <span aria-hidden="true">→</span></button>
            <p class="form__done" role="status"><span aria-hidden="true">✓</span><span>{t(S["lm_done"])}</span></p>
          </form>
          <p class="consent">{t(S["magnet_consent"])} <a href="privacy.html">{t(S["privacy"])}</a>.</p>
          <p class="xe-lm__from"><span class="xe-lm__faces">{faces}</span><span>{t(S["lm_from"])}</span></p>
        </div>
      </div>
    </div>
{logos_html}
  </section>

'''


def listening_body(x, offers_html):
    i = LISTENINGS.index(x) + 1
    col = CHANNEL[x["key"]]
    icon = ICON_SVG.get(x["icon"], "")
    e = EXTRA[x["key"]]
    copy = (tk_crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], "expertise.html"), (x["name"], None)]) +
            '<p class="tk-kick">%s · <span>0%d</span> <span>%s</span></p>' % (t(x["name"]), i, t(S["of6"])) +
            '<h1 class="tk-h1">%s</h1>' % t(x["h1"]) +
            '<p class="tk-lead">%s</p>' % t(x["lead"]) +
            '<div class="tk-actions"><a class="btn btn--primary" href="#book">%s <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--ghost" href="#answers">%s</a></div>' % (t(S["book"]), t(S["answers_link"])))
    feats = '<div class="tk-feats tk-feats--3">%s</div>' % "".join(
        '<article class="tk-feat tk-feat--%d" data-reveal><span class="tk-feat__n" aria-hidden="true">0%d</span><div class="tk-feat__t"><h3>%s</h3></div>%s</article>' % (
            k + 1, k + 1, t(h), ('<img class="tk-feat__shot" src="/assets/img/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" />' % PHOTO[x["key"]]) if k == 0 else "")
        for k, h in enumerate(x["hears"]))
    steps = '<ol class="tk-steps tk-steps--4">%s</ol>' % "".join(
        '<li data-reveal><span class="tk-steps__n">%s</span><h3>%s</h3><p>%s</p></li>' % (t(d), t(n), t(p_)) for d, n, p_ in e["steps"])
    nm = x["name"]
    out = '<main id="content" class="tk tk--net xe-tk" style="--brand:%s;--brand-ink:#13162D;--brand-2:%s">\n' % (col, col)
    out += '%s\n' % tk_crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], "expertise.html"), (x["name"], None)]).replace('class="tk-crumbs"', 'class="tk-crumbs shell"')
    out += lm_hero('%s<!--glossk:%s-->' % (t(x["name"]), x["key"]), H1L[x["key"]], x["lead"], "xp-" + x["key"],
                   t((S["lm_t"][0] % x["name"][0], S["lm_t"][1] % x["name"][1])), col, icon, t(x["name"]), logos(), flash_key=x["key"])
    art_fr = ("l'" if nm[FR][0].lower() in "aeiou" else "le ") + nm[FR][0].lower() + nm[FR][1:] if not nm[FR].startswith("AI") else "l'" + nm[FR]
    out += sec("", head(t(S["hears_k"]), t((S["hears_t"][0] % art_fr, S["hears_t"][1] % nm[EN]))) + feats, band=True)
    out += sec("answers", head(t(S["answers_k"]), t(S["answers_t"]), t(S["answers_lead"])) + prog(x["cases"]))
    out += reads(x["key"])
    guide = GUIDE.get(x["key"])
    if guide and (ROOT / "tools" / (guide + ".py")).exists():   # the long-form sections (SEO plan step 15, audit of October 2026)
        G = importlib.import_module(guide)
        from components import qa_roller
        out += sec("guide", head(t(G.KICKER), t(G.TITLE)) + qa_roller(
            [(t(h), [t(p_) for p_ in ps]) for h, ps in G.BLOCKS], t(G.KICKER),
            t(("Lire la réponse", "Read the answer"))), band=True)
    out += sec("", head(t(S["runs_k"]), t(S["how_runs"])) + steps + '<p class="tk-sub xe-note">%s</p>' % t(S["how_note"]), band=True)
    out += sec("", head(t(S["lim_k"]), t(S["lim_t"])) + offer_cards(x))
    out += voice(e["voice"])
    out += sec("", head(t(S["others_k"]), t(S["others_t2"])) + others_list(x) +
               '<a class="xe-all" href="expertise.html">%s <span aria-hidden="true">→</span></a>' % t(S["all"]), band=True)
    out += sec("", faq_block(S["faq"], x["faq"]))
    return out + book(EXTRA[x["key"]]["book_t"], offers_html) + "\n</main>"


def hub_body(offers_html):
    copy = (tk_crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], None)]) +
            '<p class="tk-kick">%s</p>' % t(S["kicker"]) +
            '<h1 class="tk-h1">%s</h1>' % t(HUB["h1"]) + '<p class="tk-lead">%s</p>' % t(HUB["lead"]) +
            '<div class="tk-actions"><a class="btn btn--primary" href="#book">%s <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--ghost" href="#six">%s</a></div>' % (t(S["book"]), t(S["list_t"])))
    tiles = "".join('<li style="--c:%s"><a href="%s"><span>%s</span><b>%s</b></a></li>' % (CHANNEL[y["key"]], y["file"], ICON_SVG.get(y["icon"], ""), t(y["name"])) for y in LISTENINGS)
    hero_art = ('<div class="tk-net xe-hubart"><figure class="tk-shot"><img src="/assets/img/team/morning/team-all-800.webp" alt="%s" width="800" height="533" decoding="async" fetchpriority="high" /></figure>'
                '<ul class="xe-hubart__six">%s</ul></div>') % (a(S["photo_cap"]), tiles)
    cards = "".join(('<li class="ucc__card of-ucc xe-ucc" id="ecoute-%s" style="--acc:%s">'
                     '<img src="/assets/img/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" />'
                     '<div class="ucc__top"><p class="ucc__k"><span class="xe-ucc__ico" aria-hidden="true">%s</span><span>0%d</span></p>'
                     '<h3 class="ucc__t"><a href="%s">%s<!--gloss:%s--></a></h3><p class="of-ucc__promise">%s</p></div>'
                     '<div class="ucc__foot"><ul class="ucc__cases">%s</ul><a class="ucc__all" href="%s">%s <span aria-hidden="true">→</span></a></div></li>') % (
        y["key"], CHANNEL[y["key"]], PHOTO[y["key"]], ICON_SVG.get(y["icon"], ""), k + 1, y["file"], t(y["name"]), y["key"], t(y["short"]),
        "".join('<li><a href="%s">%s <i aria-hidden="true">→</i></a></li>' % (y["file"], t(h)) for h in y["hears"]), y["file"], t(("%s %s" % (S["discover"][0], y["name"][0]), "%s %s" % (S["discover"][1], y["name"][1]))))
        for k, y in enumerate(LISTENINGS))
    six = ('<div class="ucc xe-six-ucc"><div class="ucc__head xe-six-head">%s<div class="ucc__nav">'
           '<button class="ucc__btn" type="button" data-dir="-1" aria-label="%s" disabled><span aria-hidden="true">←</span></button>'
           '<button class="ucc__btn" type="button" data-dir="1" aria-label="%s"><span aria-hidden="true">→</span></button></div></div>'
           '<ol class="ucc__track">%s</ol></div>') % (head(t(S["six_k"]), t(S["list_t"]), t(S["six_lead"])), a(("Écoute précédente", "Previous")), a(("Écoute suivante", "Next")), cards)
    ex = "".join('<li style="--c:%s"><a href="%s"><b>%s</b></a><span>%s</span></li>' % (CHANNEL[k], LIST[k]["file"], t(LIST[k]["name"]), t(v)) for k, v in HUB["ex"])
    exb = ('<div class="xe-ex__grid"><p class="xe-ex__q">%s</p><ul class="xe-ex__list">%s</ul><p class="xe-ex__read"><span>%s</span>%s</p></div>'
           '<a class="xe-all" href="/fr/cas-usage/" data-en="/en/use-cases/">%s <span aria-hidden="true">→</span></a>') % (
        t(HUB["ex_q"]), ex, t(HUB["ex_read_k"]), t(HUB["ex_read"]), t(S["all_cases"]))
    out = '<main id="content" class="tk tk--tool xe-tk xe-tk--hub" style="--brand:#EAA93D">\n'
    out += '%s\n' % tk_crumbs([(("Accueil", "Home"), "index.html"), (S["expertise"], None)]).replace('class="tk-crumbs"', 'class="tk-crumbs shell"')
    out += lm_hero(t(("Social intelligence", "Social intelligence")), H1L["hub"], HUB["lead"], "xp-hub", t(S["lm_t_hub"]), "#EAA93D",
                   ICON_SVG.get("chart", ""), t(S["lm_six"]), logos(), bands=[CHANNEL[y["key"]] for y in LISTENINGS])
    out += sec("six", six)
    out += sec("", head(t(S["ex_k"]), t(HUB["ex_t"])) + exb, band=True)
    out += voice(HUB_VOICE)
    out += sec("", faq_block(S["hub_faq_t"], HUB_FAQ), band=True)
    return out + book(HUB["book_t"], offers_html) + "\n</main>"


def book(title, offers_html):
    m = re.search(r'  <!-- MOCK: the callback form.*?</section>', offers_html, re.S)
    return re.sub(r'<h2 class="block__title">.*?</h2>', '<h2 class="block__title">%s</h2>' % t(title), m.group(0), count=1)


def ld(file, name, desc, crumbs_, faq=None, lang=EN):
    url = SITE + FR_PATH[file] if lang == FR else "%s/%s" % (SITE, file)
    out = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (("/fr/" if f == "" else FR_PATH.get(f, "/" + f)) if lang == FR else "/" + f)} for i, (n, f) in enumerate(crumbs_)]},
        {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "provider": U.ORG, "url": url, "areaServed": "Worldwide"}]
    if faq:
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": U.typo(q[lang], lang), "acceptedAnswer": {"@type": "Answer", "text": U.typo(r[lang], lang)}} for q, r in faq]})
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in out)


def write(file, seo_title, seo_desc, body, ld_tags, offers_html, ld_fr=""):
    """the English page at the root and its French twin under /fr/expertise/,
    both with their text in the HTML (Google reads each in its language)"""
    fr_url = FR_PATH[file]
    alts = ('<link rel="alternate" hreflang="fr" href="%s%s" />\n<link rel="alternate" hreflang="en" href="%s/%s" />\n'
            '<link rel="alternate" hreflang="x-default" href="%s/%s" />\n') % (SITE, fr_url, SITE, file, SITE, file)
    head = offers_html[:offers_html.index("</head>")]
    title, desc = html.escape(seo_title[EN]), html.escape(seo_desc[EN])
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % desc, head)
    head = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % title, head)
    head = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % desc, head)
    head = head.replace('<meta name="twitter:card"', '<link rel="canonical" href="%s/%s" />\n%s<meta name="twitter:card"' % (SITE, file, alts), 1)
    head = re.sub(r'<html[^>]*>', '<html lang="en" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (fr_url, file), head, count=1)
    en_head = head + ld_tags + "\n"
    main0, main1 = offers_html.index('<main id="content">'), offers_html.index("</main>") + len("</main>")
    shell = offers_html[offers_html.index("</head>"):main0] + "%s" + offers_html[main1:]
    shell = shell.replace('<body class="xpage">', '<body class="xpage xepage">', 1)
    page = en_head + shell % body
    page = page.replace("</main>", "</main>\n\n" + bar(), 1)
    D = U.D if hasattr(U, "D") else __import__("uc_deliverables")
    def per_lang(html_, lang):
        html_ = re.sub(r"<!--gloss:(\w+)-->", lambda m: '<span class="xe-gloss">, %s</span>' % GLOSS[m.group(1)] if lang == FR else "", html_)
        html_ = re.sub(r"<!--glossk:(\w+)-->", lambda m: '<span class="xe-gloss">· %s</span>' % GLOSS[m.group(1)] if lang == FR else "", html_)
        return re.sub(r"<!--dlv:([\w-]+)-->", lambda m: D.render(m.group(1), lang, U.esc, U.typo), html_)
    # 1. English: static, links to the use cases in English, no dictionary
    page_en, page = per_lang(page, EN), page
    en = re.sub(r'href="(/fr/cas-usage/[^"]*)" data-en="([^"]*)"', r'href="\2" data-fr="\1"', page_en)
    en = re.sub(r'\s*<script src="(?:/)?js/fr\.js[^"]*"(?: defer)?></script>', "", en)
    (ROOT / file).write_text("<!-- Generated by tools/build-expertise.py: edit that file, not this one. -->\n" + en)
    # 2. French: the same page, translated in the HTML
    fr = page
    fr = re.sub(r'<html[^>]*>', '<html lang="fr" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (fr_url, file), fr, count=1)
    ft, fd = html.escape(U.typo(seo_title[FR], FR)), html.escape(U.typo(seo_desc[FR], FR))
    fr = re.sub(r"<title>.*?</title>", "<title>%s</title>" % ft, fr, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % fd),
                     (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % ft),
                     (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % fd)):
        fr = re.sub(pat, val, fr, count=1)
    fr = fr.replace('<link rel="canonical" href="%s/%s" />' % (SITE, file), '<link rel="canonical" href="%s%s" />' % (SITE, fr_url), 1)
    fr = fr.replace(ld_tags, ld_fr or ld_tags, 1)
    fr = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', r'\1="/\2"', fr)
    fr = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="%s"' % ", ".join(
        (q if q.startswith(("/", "http")) else "/" + q) for q in (y.strip() for y in m.group(1).split(","))), fr)
    b0, b1 = fr.index("<body"), fr.index("</body>")
    fr = fr[:b0] + per_lang(U.translate(fr[b0:b1]).replace(">Skip to content<", ">Aller au contenu<"), FR) + fr[b1:]
    fr = fr.replace('placeholder="name@company.com"', 'placeholder="nom@entreprise.com"')
    out = ROOT / fr_url.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("<!-- Generated by tools/build-expertise.py from the same source as %s: edit that script. -->\n" % file + fr)


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
    offers_html = O.shell_source()
    pages = []
    for x in LISTENINGS:
        body = listening_body(x, offers_html)
        crumbs_ = [("Home", ""), ("Expertise", "expertise.html"), (x["name"][EN], x["file"])]
        crumbs_fr = [("Accueil", ""), ("Expertise", "expertise.html"), (x["name"][FR], x["file"])]
        pages.append((x["file"], x["seo_title"], x["seo_desc"], body,
                      ld(x["file"], x["name"][EN], x["seo_desc"][EN], crumbs_, x["faq"]),
                      ld(x["file"], x["name"][FR], U.typo(x["seo_desc"][FR], FR), crumbs_fr, x["faq"], FR)))
    body = hub_body(offers_html)
    pages.append((HUB["file"], HUB["seo_title"], HUB["seo_desc"], body,
                  ld(HUB["file"], "Social intelligence", HUB["seo_desc"][EN], [("Home", ""), ("Expertise", "expertise.html")], HUB_FAQ),
                  ld(HUB["file"], "Social intelligence", U.typo(HUB["seo_desc"][FR], FR), [("Accueil", ""), ("Expertise", "expertise.html")], HUB_FAQ, FR)))
    for k in ("menu_label", "menu_aside", "all", "foot_link", "bar_offer", "bar_call", "bar_chat"):
        t(S[k])
    for x in LISTENINGS + [HUB]:
        t(x["seo_title"])
    O.write_dict("expertise pages", "build-expertise.py", O.NEW)
    # the dictionary now holds every string of these pages: translate them
    U.DICT.update(U.fr_dict())
    U.DICT.update(O.NEW)
    for file, st, sd, body, ld_en, ld_fr in pages:
        write(file, st, sd, body, ld_en, offers_html, ld_fr)
    print("%d expertise pages written in English and French, %d strings in js/fr.js" % (len(pages), len(O.NEW)))


if __name__ == "__main__":
    main()
