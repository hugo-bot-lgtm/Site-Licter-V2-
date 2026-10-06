#!/usr/bin/env python3
"""Builds a page for each tool around the listening platforms:

    tech-radarly.html, tech-semrush.html, tech-google-trends.html,
    tech-answerthepublic.html, tech-chatgpt.html, tech-geo.html,
    tech-meta-ads.html, tech-google-news.html, tech-social-blade.html

They follow the four hand-written platform pages (tech-talkwalker.html and
its siblings): same shell, same sections, translated at runtime by js/fr.js.
The shell (head, header, footer) is copied from tech-talkwalker.html; the
French of every new string goes to its own block of js/fr.js.

Run by tools/build-usecases.py (before the sitemap), or on its own:

    python3 tools/build-tech.py

MOCK: the descriptions say how Licter uses each tool; to be validated by
Licter (A-FAIRE.md, section 5).
"""
import html, importlib.util, json, pathlib, re

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

TOOLS = [
    {"slug": "radarly", "name": "Radarly", "letter": "R",
     "h1": ("RADARLY,<br>LU PAR NOS ANALYSTES.", "RADARLY,<br>READ BY ANALYSTS."),
     "lead": ("Une plateforme d'écoute sociale pensée pour suivre une marque dans la durée : des conversations classées, des tableaux de bord partagés, et une lecture qui arrive sous forme de réponse.",
              "A social listening platform built to follow a brand over time: conversations sorted, dashboards shared, and a reading that arrives as an answer."),
     "desc": ("Radarly, plateforme d'écoute sociale opérée par les consultants de Licter : suivi de marque dans la durée, analyse des conversations et des communautés.",
              "Radarly, the social listening platform operated by Licter's consultants: long-running brand tracking, conversation and community analysis."),
     "why_lead": ("Nous la prenons quand une marque doit être suivie sur la durée par plusieurs équipes, avec un même référentiel de sujets.",
                  "We pick it when a brand has to be followed over time by several teams, with one shared set of topics."),
     "why": [(("DURÉE", "TIME"), ("Un suivi qui tient dans le temps", "Tracking that holds over time"),
              ("Les mêmes sujets, classés de la même façon, mois après mois : les évolutions se comparent vraiment.",
               "The same topics, sorted the same way, month after month: changes can really be compared.")),
             (("PARTAGE", "SHARING"), ("Des tableaux de bord pour plusieurs équipes", "Dashboards for several teams"),
              ("Communication, marketing et service client lisent le même référentiel, chacun à son niveau.",
               "Communication, marketing and customer service read the same frame, each at its own level."))],
     "strengths": [(("Classement des conversations", "Conversation sorting"), ("Des catégories et des sujets définis avec vous, appliqués à toute la collecte.", "Categories and topics set with you, applied to the whole collection.")),
                   (("Analyse des communautés", "Community analysis"), ("Qui parle, avec quels centres d'intérêt, et quelles communautés se recoupent.", "Who is talking, with which interests, and which communities overlap.")),
                   (("Alertes par sujet", "Alerts per topic"), ("Des seuils par sujet, pour qu'un pic sur l'un ne noie pas les autres.", "Thresholds per topic, so a spike on one does not drown the others.")),
                   (("Une configuration tenue par nous", "A setup we maintain"), ("Requêtes, taxonomie et maintenance restent de notre côté ; vous recevez la lecture.", "Queries, taxonomy and maintenance stay on our side; you receive the reading."))],
     "solutions": [(("Suivi de marque continu", "Continuous brand tracking"), [("Périmètre par marque, gamme et marché", "Perimeter per brand, range and market"), ("Sujets et tonalité suivis semaine après semaine", "Topics and tone tracked week after week"), ("Comparaison avec vos concurrents", "Comparison with your competitors"), ("Une note mensuelle : ce qui a bougé et pourquoi", "A monthly note: what moved and why")]),
                   (("Lecture des communautés", "Community reads"), [("Les communautés qui parlent de la marque", "The communities talking about the brand"), ("Leurs centres d'intérêt et leurs relais", "Their interests and their relays"), ("Les recoupements avec vos cibles", "Overlaps with your targets"), ("Les prises de parole à privilégier", "The ways to speak to them")]),
                   (("Tableaux de bord pour vos équipes", "Dashboards for your teams"), [("Une vue par équipe, un même référentiel", "One view per team, one shared frame"), ("Des indicateurs choisis avec vous", "Indicators chosen with you"), ("Une revue trimestrielle du périmètre", "A quarterly review of the perimeter"), ("La formation de vos équipes à la lecture", "Training your teams to read them")])],
     "uses": ["reputation", "segmentation", "messaging"],
     "faq": [(("Faut-il notre propre licence Radarly ?", "Do we need our own Radarly licence?"), ("Non. Nous travaillons avec nos accès ; si vous avez déjà une licence, nous pouvons la reprendre et la faire produire.", "No. We work with our own access; if you already have a licence, we can take it over and make it produce.")),
             (("Quelle différence avec Talkwalker ?", "How is it different from Talkwalker?"), ("Les deux couvrent l'écoute sociale. Nous choisissons selon la question : la couverture et l'historique pour l'un, le suivi partagé dans la durée pour l'autre, et souvent les deux ensemble.", "Both cover social listening. We choose by the question: coverage and history for one, shared long-running tracking for the other, and often both together.")),
             (("Peut-on garder nos tableaux de bord actuels ?", "Can we keep our current dashboards?"), ("Oui, s'ils servent. Nous commençons par un audit : ce qui est lu reste, ce qui ne l'est pas est revu.", "Yes, if they are used. We start with an audit: what is read stays, what is not gets reworked."))]},

    {"slug": "semrush", "name": "Semrush", "letter": "S",
     "h1": ("SEMRUSH,<br>LU AU-DELÀ DU SEO.", "SEMRUSH,<br>READ BEYOND SEO."),
     "lead": ("Ce que votre marché tape dans les moteurs de recherche, et qui y répond. Nous l'utilisons pour la recherche, pas pour le référencement : la demande déclarée, avant qu'elle n'arrive chez vous.",
              "What your market types into search engines, and who answers it. We use it for search listening, not for SEO: declared demand, before it reaches you."),
     "desc": ("Semrush pour l'écoute de la recherche : ce que votre marché cherche, sur quels mots, et quelles marques y répondent, lu par les consultants de Licter.",
              "Semrush for search listening: what your market looks for, in which words, and which brands answer it, read by Licter's consultants."),
     "why_lead": ("La conversation dit ce que les gens pensent ; la recherche dit ce qu'ils veulent savoir. Les deux ensemble évitent de confondre bruit et demande.",
                  "The conversation says what people think; search says what they want to know. Together they keep noise from passing for demand."),
     "why": [(("DEMANDE", "DEMAND"), ("La demande avant l'achat", "Demand before the purchase"), ("Les volumes de recherche montrent ce qu'un marché cherche, sans qu'on le lui demande.", "Search volumes show what a market looks for, without anyone asking it.")),
             (("CONCURRENCE", "COMPETITION"), ("Qui occupe la réponse", "Who owns the answer"), ("Les marques et les contenus qui ressortent sur les questions qui vous concernent.", "The brands and content that come up on the questions that matter to you."))],
     "strengths": [(("Volumes par mot et par pays", "Volumes per word and country"), ("La taille réelle d'un sujet, marché par marché.", "The real size of a topic, market by market.")),
                   (("Les mots exacts du marché", "The market's own words"), ("Les formulations que les gens utilisent, pas celles de la marque.", "The phrasing people use, not the brand's.")),
                   (("La place des concurrents", "Where competitors stand"), ("Qui ressort sur vos sujets, et avec quels contenus.", "Who comes up on your topics, and with which content.")),
                   (("Les évolutions dans le temps", "Changes over time"), ("Ce qui monte, ce qui baisse, ce qui revient chaque saison.", "What rises, what falls, what comes back every season."))],
     "solutions": [(("Lecture de la demande", "Demand reads"), [("Les questions d'une catégorie, classées par volume", "A category's questions, ranked by volume"), ("Les besoins mal couverts", "The needs nobody covers well"), ("Les écarts entre marchés", "The gaps between markets"), ("Une synthèse pour le marketing", "A summary for marketing")]),
                   (("Benchmark concurrentiel", "Competitive benchmark"), [("Votre visibilité face à vos concurrents", "Your visibility against competitors"), ("Les sujets où ils vous devancent", "The topics where they lead"), ("Les contenus qui captent la demande", "The content that captures demand"), ("Les priorités à traiter", "The priorities to address")]),
                   (("Croisement avec la conversation", "Crossed with the conversation"), [("Ce qui se cherche et ce qui se dit", "What is searched and what is said"), ("Les sujets bruyants sans demande", "Loud topics with no demand"), ("Les demandes silencieuses", "Silent demand"), ("Une recommandation commune", "One joint recommendation")])],
     "uses": ["market-opportunities", "product-test", "touchpoints"],
     "faq": [(("Faites-vous du SEO ?", "Do you do SEO?"), ("Non. Nous lisons la recherche pour comprendre un marché ; l'optimisation de votre site reste le travail de votre agence.", "No. We read search to understand a market; optimising your site remains your agency's job.")),
             (("Faut-il notre propre compte Semrush ?", "Do we need our own Semrush account?"), ("Non, nous utilisons nos accès. Vous recevez l'analyse, pas des exports.", "No, we use our own access. You receive the analysis, not exports.")),
             (("Quels marchés couvrez-vous ?", "Which markets do you cover?"), ("Ceux que l'outil couvre, avec une lecture dans la langue du marché par nos consultants.", "Those the tool covers, read in the language of the market by our consultants."))]},

    {"slug": "google-trends", "name": "Google Trends", "letter": "G",
     "h1": ("GOOGLE TRENDS,<br>MIS EN CONTEXTE.", "GOOGLE TRENDS,<br>PUT IN CONTEXT."),
     "lead": ("L'intérêt de recherche dans le temps, par pays et par région. Une courbe simple, que nous lisons avec le reste : elle date un sujet, le compare à un autre, et dit s'il monte vraiment.",
              "Search interest over time, by country and region. A simple curve that we read with the rest: it dates a topic, compares it to another, and says whether it is really rising."),
     "desc": ("Google Trends lu par les consultants de Licter : dater un sujet, comparer des tendances, vérifier qu'une hausse de conversation correspond à une vraie demande.",
              "Google Trends read by Licter's consultants: date a topic, compare trends, check that a rise in conversation matches real demand."),
     "why_lead": ("C'est le juge de paix d'une tendance : si la conversation monte mais pas la recherche, il faut se méfier.",
                  "It is the referee of a trend: if the conversation rises but search does not, be careful."),
     "why": [(("DATER", "DATING"), ("Le début d'un sujet", "When a topic started"), ("La courbe montre quand l'intérêt a démarré, et s'il revient chaque année.", "The curve shows when interest started, and whether it comes back every year.")),
             (("COMPARER", "COMPARING"), ("Deux sujets sur la même échelle", "Two topics on one scale"), ("Votre marque face à un concurrent, ou une tendance face à une autre.", "Your brand against a competitor, or one trend against another."))],
     "strengths": [(("Gratuit et public", "Free and public"), ("Une source que tout le monde peut vérifier.", "A source anyone can check.")),
                   (("Par pays et par région", "By country and region"), ("Où un sujet prend, avant qu'il ne s'étende.", "Where a topic takes off, before it spreads.")),
                   (("Les requêtes associées", "Related queries"), ("Ce que les gens cherchent autour du sujet.", "What people look for around the topic.")),
                   (("Saisonnalité", "Seasonality"), ("Distinguer une tendance d'un retour annuel.", "Tell a trend from a yearly return."))],
     "solutions": [(("Validation de tendance", "Trend validation"), [("La courbe de recherche du sujet", "The topic's search curve"), ("La comparaison avec la conversation", "The comparison with the conversation"), ("Le verdict : monte, plafonne ou retombe", "The verdict: rising, flat or falling"), ("Les marchés où elle prend", "The markets where it takes off")]),
                   (("Comparaison de marques", "Brand comparison"), [("Votre marque face à vos concurrents", "Your brand against competitors"), ("Sur plusieurs pays", "Across several countries"), ("Les moments qui ont fait bouger la courbe", "The moments that moved the curve"), ("Une lecture mensuelle", "A monthly read")]),
                   (("Calendrier des sujets", "Topic calendar"), [("Les pics saisonniers de votre catégorie", "Your category's seasonal peaks"), ("Le bon moment pour prendre la parole", "The right time to speak"), ("Les sujets qui reviennent chaque année", "The topics that come back every year"), ("Un calendrier pour vos équipes", "A calendar for your teams")])],
     "uses": ["stakeholders", "market-opportunities", "campaign-impact"],
     "faq": [(("Google Trends est gratuit : pourquoi passer par vous ?", "Google Trends is free: why go through you?"), ("La courbe est publique, la lecture ne l'est pas. Seule, elle se lit mal : nous la croisons avec la conversation et les volumes réels.", "The curve is public, the reading is not. On its own it reads badly: we cross it with the conversation and real volumes.")),
             (("Les chiffres sont-ils des volumes ?", "Are the figures volumes?"), ("Non, ce sont des indices relatifs de 0 à 100. C'est pourquoi nous les complétons par des volumes de recherche.", "No, they are relative indices from 0 to 100. That is why we complete them with search volumes."))]},

    {"slug": "answerthepublic", "name": "AnswerThePublic", "letter": "A",
     "h1": ("ANSWERTHEPUBLIC,<br>LES QUESTIONS DU MARCHÉ.", "ANSWERTHEPUBLIC,<br>THE MARKET'S QUESTIONS."),
     "lead": ("Les questions que les gens posent autour d'un sujet, telles qu'ils les tapent : pourquoi, comment, lequel, est-ce que. Nous nous en servons pour entendre un marché avant qu'il ne s'adresse à vous.",
              "The questions people ask around a subject, as they type them: why, how, which, is it. We use it to hear a market before it speaks to you."),
     "desc": ("AnswerThePublic lu par les consultants de Licter : les questions qu'un marché pose sur un sujet, classées pour nourrir vos contenus et vos produits.",
              "AnswerThePublic read by Licter's consultants: the questions a market asks about a subject, sorted to feed your content and your products."),
     "why_lead": ("Une question tapée dans un moteur de recherche est un besoin dit sans filtre. C'est souvent là que se trouve l'idée de contenu ou de produit.",
                  "A question typed into a search engine is a need said without a filter. That is often where the content or product idea sits."),
     "why": [(("QUESTIONS", "QUESTIONS"), ("Les doutes avant l'achat", "Doubts before the purchase"), ("Ce que les gens ne savent pas encore, et qu'ils cherchent.", "What people do not know yet, and look for.")),
             (("MOTS", "WORDS"), ("Le vocabulaire du public", "The public's vocabulary"), ("Les mots qu'il emploie, pour parler comme lui.", "The words it uses, so you can speak like it."))],
     "strengths": [(("Les questions par type", "Questions by type"), ("Pourquoi, comment, lequel, quand : chaque famille dit autre chose.", "Why, how, which, when: each family says something else.")),
                   (("Les comparaisons", "Comparisons"), ("« X ou Y », « X contre Y » : ce que le marché met en balance.", "\"X or Y\", \"X versus Y\": what the market weighs up.")),
                   (("Par langue et par pays", "By language and country"), ("Les questions changent d'un marché à l'autre.", "Questions change from one market to the next.")),
                   (("Rapide à lire", "Quick to read"), ("Une vue d'ensemble d'un sujet en quelques minutes.", "An overview of a subject in minutes."))],
     "solutions": [(("Cartographie des questions", "Question map"), [("Les questions d'un sujet, regroupées", "A subject's questions, grouped"), ("Les doutes qui freinent l'achat", "The doubts that hold back a purchase"), ("Les comparaisons avec vos concurrents", "Comparisons with your competitors"), ("Les priorités de réponse", "What to answer first")]),
                   (("Plan de contenus", "Content plan"), [("Les sujets à traiter, dans les mots du public", "The topics to cover, in the public's words"), ("Les formats adaptés à chaque question", "The format for each question"), ("Le croisement avec la conversation", "Crossed with the conversation"), ("Un calendrier pour vos équipes", "A calendar for your teams")]),
                   (("Pistes produit", "Product leads"), [("Les besoins qui reviennent", "The needs that come back"), ("Les irritants exprimés", "The irritants people express"), ("Ce que les offres actuelles ne règlent pas", "What current offers do not solve"), ("Une synthèse pour l'innovation", "A summary for innovation")])],
     "uses": ["touchpoints", "product-test", "messaging"],
     "faq": [(("C'est un outil gratuit : pourquoi passer par vous ?", "It is a free tool: why go through you?"), ("La liste des questions est accessible ; la lecture, le tri et le croisement avec le reste du marché, non. C'est la partie que nous faisons.", "The list of questions is open; the reading, the sorting and the crossing with the rest of the market are not. That is the part we do.")),
             (("D'où viennent les questions ?", "Where do the questions come from?"), ("Des suggestions des moteurs de recherche : ce que les gens commencent à taper, et ce que le moteur complète.", "From search engine suggestions: what people start typing, and what the engine completes."))]},

    {"slug": "chatgpt", "name": "ChatGPT", "letter": "C",
     "h1": ("CHATGPT,<br>CE QUE L'IA DIT DE VOUS.", "CHATGPT,<br>WHAT AI SAYS ABOUT YOU."),
     "lead": ("De plus en plus de gens posent leurs questions à une IA plutôt qu'à un moteur de recherche. Nous lisons ce que ChatGPT et les autres assistants répondent sur votre marque et votre catégorie.",
              "More and more people ask an AI rather than a search engine. We read what ChatGPT and the other assistants answer about your brand and your category."),
     "desc": ("Ce que ChatGPT et les IA génératives répondent sur votre marque et votre catégorie, lu par les consultants de Licter.",
              "What ChatGPT and generative AI answer about your brand and your category, read by Licter's consultants."),
     "why_lead": ("La réponse d'une IA est devenue une source d'opinion à part entière. Elle peut citer vos concurrents, se tromper sur vous, ou ne pas vous citer du tout.",
                  "An AI's answer has become a source of opinion in its own right. It can cite your competitors, get you wrong, or not mention you at all."),
     "why": [(("RÉPONSES", "ANSWERS"), ("Ce que l'IA recommande", "What AI recommends"), ("Les marques citées, dans quel ordre, et avec quels arguments.", "The brands cited, in which order, and with which arguments.")),
             (("SOURCES", "SOURCES"), ("D'où l'IA tient ce qu'elle dit", "Where AI gets what it says"), ("Les contenus qui nourrissent la réponse, et ceux qui manquent.", "The content that feeds the answer, and what is missing."))],
     "strengths": [(("Des questions réelles", "Real questions"), ("Les questions que se pose votre marché, posées à l'IA.", "The questions your market asks, put to the AI.")),
                   (("Plusieurs assistants", "Several assistants"), ("ChatGPT, et les autres assistants grand public, comparés.", "ChatGPT and the other mainstream assistants, compared.")),
                   (("Erreurs repérées", "Errors spotted"), ("Les informations fausses ou datées sur votre marque.", "False or outdated information about your brand.")),
                   (("Suivi dans le temps", "Tracking over time"), ("Les réponses changent : nous les suivons.", "Answers change: we follow them."))],
     "solutions": [(("Audit des réponses de l'IA", "AI answer audit"), [("Les questions clés de votre catégorie", "The key questions of your category"), ("Ce que répondent les assistants", "What the assistants answer"), ("Votre place face aux concurrents", "Your place against competitors"), ("Les erreurs à corriger", "The errors to correct")]),
                   (("Suivi régulier", "Regular tracking"), [("Les mêmes questions, chaque mois", "The same questions, every month"), ("Les évolutions des réponses", "How the answers change"), ("Les nouvelles marques citées", "Newly cited brands"), ("Une note pour la communication", "A note for communication")]),
                   (("Plan d'action", "Action plan"), [("Les contenus qui manquent", "The missing content"), ("Les sources à renforcer", "The sources to strengthen"), ("Les messages à clarifier", "The messages to clarify"), ("Le lien avec votre stratégie GEO", "The link with your GEO strategy")])],
     "uses": ["reputation", "brand-risk", "messaging"],
     "faq": [(("Pourquoi suivre ce que répond une IA ?", "Why track what an AI answers?"), ("Parce qu'une partie de vos clients s'y informe avant d'acheter, et que la réponse ne vient pas de vous.", "Because part of your customers get their information there before buying, and the answer does not come from you.")),
             (("Pouvez-vous changer ce que l'IA répond ?", "Can you change what the AI answers?"), ("Pas directement. Nous identifions les contenus et les sources qui nourrissent la réponse ; c'est sur eux qu'on agit, voir notre page GEO.", "Not directly. We identify the content and sources that feed the answer; that is where you act, see our GEO page.")),
             (("Utilisez-vous vos données dans l'IA ?", "Do you put your data into the AI?"), ("Non. Nous posons des questions publiques ; aucune donnée client n'est transmise.", "No. We ask public questions; no client data is sent."))]},

    {"slug": "geo", "name": "GEO", "letter": "G",
     "h1": ("GEO,<br>VOTRE PLACE DANS LES RÉPONSES DES IA.", "GEO,<br>YOUR PLACE IN AI ANSWERS."),
     "lead": ("Le GEO (generative engine optimisation) mesure et améliore la visibilité d'une marque dans les réponses des moteurs d'IA. Nous partons de ce que les IA répondent, puis des sources qui les nourrissent.",
              "GEO (generative engine optimisation) measures and improves a brand's visibility in the answers of AI engines. We start from what the AIs answer, then from the sources that feed them."),
     "desc": ("GEO avec Licter : mesurer la visibilité de votre marque dans les réponses des IA, comprendre pourquoi, et savoir sur quelles sources agir.",
              "GEO with Licter: measure your brand's visibility in AI answers, understand why, and know which sources to act on."),
     "why_lead": ("Le référencement classique ne suffit plus : une IA répond sans renvoyer vers votre site. Il faut savoir si elle vous cite, et pourquoi.",
                  "Classic SEO is no longer enough: an AI answers without sending people to your site. You need to know whether it cites you, and why."),
     "why": [(("MESURE", "MEASURE"), ("Votre part de réponse", "Your share of answer"), ("Sur les questions de votre catégorie, combien de fois vous êtes cité.", "On your category's questions, how often you are cited.")),
             (("CAUSES", "CAUSES"), ("Les sources qui comptent", "The sources that count"), ("Les sites, articles et forums que les IA reprennent.", "The sites, articles and forums the AIs draw on."))],
     "strengths": [(("Un panel de questions", "A panel of questions"), ("Les questions réelles de votre marché, posées régulièrement.", "Your market's real questions, asked regularly.")),
                   (("Plusieurs moteurs", "Several engines"), ("Les assistants et moteurs IA grand public, comparés.", "The mainstream AI assistants and engines, compared.")),
                   (("Lien avec la conversation", "Linked to the conversation"), ("Les sources citées par l'IA, croisées avec l'écoute sociale.", "The sources the AI cites, crossed with social listening.")),
                   (("Des actions concrètes", "Concrete actions"), ("Quels contenus produire ou corriger, et où.", "Which content to produce or correct, and where."))],
     "solutions": [(("Diagnostic GEO", "GEO diagnostic"), [("Votre part de réponse face aux concurrents", "Your share of answer against competitors"), ("Les questions où vous êtes absent", "The questions where you are absent"), ("Les sources qui vous citent ou non", "The sources that cite you or not"), ("Les priorités", "The priorities")]),
                   (("Suivi mensuel", "Monthly tracking"), [("Le même panel de questions", "The same question panel"), ("L'évolution de votre visibilité", "How your visibility changes"), ("Les nouveaux concurrents cités", "Newly cited competitors"), ("Une note de synthèse", "A summary note")]),
                   (("Recommandations de contenus", "Content recommendations"), [("Les sujets à couvrir", "The topics to cover"), ("Les sources à travailler", "The sources to work on"), ("Les informations à corriger", "The information to correct"), ("Le lien avec vos équipes et vos agences", "The link with your teams and agencies")])],
     "uses": ["reputation", "messaging", "market-opportunities"],
     "faq": [(("Quelle différence entre GEO et SEO ?", "How is GEO different from SEO?"), ("Le SEO vise une place dans une liste de liens ; le GEO vise une mention dans une réponse rédigée par une IA. Les leviers se recoupent en partie, pas entièrement.", "SEO aims for a place in a list of links; GEO aims for a mention in an answer written by an AI. The levers overlap in part, not entirely.")),
             (("Produisez-vous les contenus ?", "Do you produce the content?"), ("Non. Nous mesurons, expliquons et recommandons ; la production reste à vos équipes ou à vos agences.", "No. We measure, explain and recommend; production stays with your teams or agencies.")),
             (("En combien de temps voit-on un effet ?", "How soon is there an effect?"), ("Cela dépend des moteurs et des sources ; c'est pourquoi nous suivons le même panel de questions dans le temps.", "It depends on the engines and the sources; that is why we follow the same question panel over time."))]},

    {"slug": "meta-ads", "name": "Meta Ads", "letter": "M",
     "h1": ("META ADS,<br>LES CAMPAGNES À DÉCOUVERT.", "META ADS,<br>CAMPAIGNS IN THE OPEN."),
     "lead": ("La bibliothèque publicitaire de Meta montre les publicités en cours sur Facebook et Instagram. Nous la lisons pour voir ce que vos concurrents poussent, depuis quand, et avec quels messages.",
              "Meta's Ad Library shows the ads running on Facebook and Instagram. We read it to see what your competitors push, since when, and with which messages."),
     "desc": ("La bibliothèque publicitaire de Meta lue par les consultants de Licter : les campagnes de vos concurrents, leurs messages et leur rythme.",
              "Meta's Ad Library read by Licter's consultants: your competitors' campaigns, their messages and their pace."),
     "why_lead": ("La conversation montre ce que le public dit ; la publicité montre ce que les marques veulent qu'il dise. L'écart entre les deux est souvent instructif.",
                  "The conversation shows what the public says; advertising shows what brands want it to say. The gap between the two is often telling."),
     "why": [(("CONCURRENCE", "COMPETITION"), ("Ce que poussent vos concurrents", "What your competitors push"), ("Leurs publicités actives, leurs visuels et leurs messages.", "Their active ads, their visuals and their messages.")),
             (("PAYANT", "PAID"), ("Séparer le payant de l'organique", "Separate paid from organic"), ("Savoir si un sujet monte seul ou parce qu'il est acheté.", "Know whether a topic rises on its own or because it is paid for."))],
     "strengths": [(("Public et vérifiable", "Public and checkable"), ("Une source officielle, ouverte à tous.", "An official source, open to all.")),
                   (("Durée des campagnes", "Campaign duration"), ("Depuis quand une publicité tourne, signe de ce qui marche.", "How long an ad has been running, a sign of what works.")),
                   (("Messages et formats", "Messages and formats"), ("Les angles, les visuels et les appels à l'action.", "The angles, visuals and calls to action.")),
                   (("Plusieurs pays", "Several countries"), ("Les variations d'une campagne d'un marché à l'autre.", "How a campaign varies from one market to another."))],
     "solutions": [(("Veille publicitaire concurrentielle", "Competitive ad monitoring"), [("Les campagnes actives de vos concurrents", "Your competitors' active campaigns"), ("Leurs messages, classés", "Their messages, sorted"), ("Les nouveautés du mois", "What is new this month"), ("Une note pour le marketing", "A note for marketing")]),
                   (("Lecture de campagne", "Campaign reads"), [("La part payante d'un pic de conversation", "The paid share of a conversation spike"), ("Ce que l'organique a ajouté", "What organic added"), ("Les messages repris par le public", "The messages the public picked up"), ("Le bilan avant / après", "The before / after review")]),
                   (("Benchmark créatif", "Creative benchmark"), [("Les angles de votre catégorie", "Your category's angles"), ("Les formats qui durent", "The formats that last"), ("Les territoires libres", "The open territories"), ("Des pistes pour vos agences", "Leads for your agencies")])],
     "uses": ["campaign-impact", "messaging", "market-opportunities"],
     "faq": [(("La bibliothèque est publique : pourquoi passer par vous ?", "The library is public: why go through you?"), ("Elle montre les publicités, une par une. Nous les classons, les relions à la conversation, et vous disons ce qu'elles révèlent de la stratégie de vos concurrents.", "It shows the ads, one by one. We sort them, link them to the conversation, and tell you what they reveal about your competitors' strategy.")),
             (("Voit-on les budgets ?", "Can you see the budgets?"), ("Pour la plupart des publicités, non : la bibliothèque montre les publicités, pas les montants. Nous en déduisons le rythme et la durée, pas des dépenses.", "For most ads, no: the library shows the ads, not the amounts. We infer pace and duration from it, not spend."))]},

    {"slug": "google-news", "name": "Google News", "fr_name": "Google Actualités", "letter": "G",
     "h1": ("GOOGLE ACTUALITÉS,<br>LA PRESSE EN FACE DU SOCIAL.", "GOOGLE NEWS,<br>THE PRESS AGAINST SOCIAL."),
     "lead": ("La couverture presse au fil de l'eau. Nous la mettons en face de la conversation sociale : un sujet né dans les médias ne se lit pas comme un sujet né sur TikTok.",
              "Press coverage as it lands. We set it against the social conversation: a topic born in the media does not read like a topic born on TikTok."),
     "desc": ("Google Actualités lu par les consultants de Licter : la couverture presse de votre marque, confrontée à la conversation sociale.",
              "Google News read by Licter's consultants: your brand's press coverage, set against the social conversation."),
     "why_lead": ("Savoir d'où part un sujet change la réponse : un article repris sur les réseaux ne se traite pas comme une polémique née sur les réseaux.",
                  "Knowing where a topic starts changes the answer: an article picked up on social is not handled like a row born on social."),
     "why": [(("ORIGINE", "ORIGIN"), ("D'où part un sujet", "Where a topic starts"), ("Presse d'abord, ou réseaux d'abord : la chronologie le dit.", "Press first or social first: the timeline tells.")),
             (("PORTÉE", "REACH"), ("Les titres qui comptent", "The outlets that matter"), ("Quels médias ont couvert le sujet, et lesquels ont été repris.", "Which media covered the topic, and which were picked up."))],
     "strengths": [(("Couverture large", "Broad coverage"), ("La presse nationale, régionale et spécialisée, dans de nombreux pays.", "National, regional and trade press, in many countries.")),
                   (("Au fil de l'eau", "As it lands"), ("Les articles dès leur publication.", "Articles as soon as they are published.")),
                   (("Recoupement avec le social", "Crossed with social"), ("Les articles repris, commentés et partagés.", "The articles picked up, commented on and shared.")),
                   (("Historique", "History"), ("La couverture d'un sujet dans la durée.", "A topic's coverage over time."))],
     "solutions": [(("Veille presse et social", "Press and social monitoring"), [("La couverture de votre marque", "Your brand's coverage"), ("Les reprises sur les réseaux", "The pick-ups on social"), ("Les alertes quand un article circule", "Alerts when an article spreads"), ("Une revue mensuelle", "A monthly review")]),
                   (("Lecture de crise", "Crisis reads"), [("La chronologie presse et réseaux", "The press and social timeline"), ("Les médias qui ont amplifié", "The media that amplified"), ("Les angles repris", "The angles picked up"), ("Les recommandations de réponse", "Response recommendations")]),
                   (("Bilan de prise de parole", "Announcement review"), [("Les retombées d'une annonce", "The coverage of an announcement"), ("Leur écho sur les réseaux", "Their echo on social"), ("Les messages restés, les messages perdus", "The messages that stuck, and those lost"), ("Le bilan pour la direction", "The review for leadership")])],
     "uses": ["brand-risk", "leader-advocacy", "reputation"],
     "faq": [(("Remplacez-vous une revue de presse ?", "Do you replace a press review?"), ("Pas forcément. Nous ajoutons ce qu'une revue de presse ne fait pas : le lien avec la conversation sociale, et ce qu'il faut en faire.", "Not necessarily. We add what a press review does not: the link with the social conversation, and what to do about it.")),
             (("Couvrez-vous la presse payante ?", "Do you cover paywalled press?"), ("Nous voyons les articles publiés et leurs titres ; l'accès au texte complet dépend des titres et de vos abonnements.", "We see the published articles and their headlines; access to the full text depends on the outlets and your subscriptions."))]},

    {"slug": "social-blade", "name": "Social Blade", "letter": "S",
     "h1": ("SOCIAL BLADE,<br>LA CROISSANCE DES COMPTES.", "SOCIAL BLADE,<br>HOW ACCOUNTS GROW."),
     "lead": ("L'évolution des abonnés et des vues des comptes et des créateurs, dans le temps. Nous l'utilisons pour vérifier une audience avant de travailler avec elle.",
              "How accounts and creators gain followers and views over time. We use it to check an audience before working with it."),
     "desc": ("Social Blade lu par les consultants de Licter : la croissance des comptes et des créateurs, pour vérifier une audience avant de la payer.",
              "Social Blade read by Licter's consultants: how accounts and creators grow, to check an audience before you pay for it."),
     "why_lead": ("Un nombre d'abonnés dit peu de chose. Sa courbe en dit plus : une croissance régulière, un pic suspect, une audience qui s'essouffle.",
                  "A follower count says little. Its curve says more: steady growth, a suspicious spike, an audience running out of steam."),
     "why": [(("VÉRIFIER", "CHECK"), ("Avant de payer un créateur", "Before paying a creator"), ("Une croissance anormale se voit sur la courbe.", "Abnormal growth shows on the curve.")),
             (("COMPARER", "COMPARE"), ("Votre compte face aux autres", "Your account against others"), ("Votre progression face à vos concurrents et aux créateurs de votre catégorie.", "Your progress against competitors and the creators in your category."))],
     "strengths": [(("L'historique des comptes", "Account history"), ("Abonnés et vues, jour après jour.", "Followers and views, day after day.")),
                   (("Plusieurs plateformes", "Several platforms"), ("YouTube, TikTok, Instagram, Twitch et d'autres.", "YouTube, TikTok, Instagram, Twitch and others.")),
                   (("Les pics suspects", "Suspicious spikes"), ("Les hausses brutales qui méritent une question.", "The sudden jumps that deserve a question.")),
                   (("Comparaisons simples", "Simple comparisons"), ("Plusieurs comptes sur la même échelle.", "Several accounts on one scale."))],
     "solutions": [(("Vérification de créateurs", "Creator checks"), [("La courbe de chaque créateur pressenti", "The curve of each shortlisted creator"), ("Les pics à expliquer", "The spikes to explain"), ("Le croisement avec son audience réelle", "Crossed with their real audience"), ("Un avis avant contrat", "An opinion before signing")]),
                   (("Benchmark de comptes", "Account benchmark"), [("Vos comptes face à vos concurrents", "Your accounts against competitors"), ("Par plateforme", "Per platform"), ("Les périodes de croissance", "The growth periods"), ("Ce qui les explique", "What explains them")]),
                   (("Suivi d'un programme d'influence", "Influence programme tracking"), [("La progression des créateurs partenaires", "Partner creators' progress"), ("L'effet de vos campagnes sur leurs comptes", "Your campaigns' effect on their accounts"), ("Les créateurs à renouveler", "The creators to renew"), ("Le bilan du programme", "The programme review")])],
     "uses": ["ambassadors", "leader-advocacy", "rejuvenate"],
     "faq": [(("Social Blade suffit-il pour choisir un créateur ?", "Is Social Blade enough to pick a creator?"), ("Non. Il dit comment un compte grandit, pas qui le suit. Nous le croisons avec l'analyse de l'audience réelle du créateur.", "No. It says how an account grows, not who follows it. We cross it with an analysis of the creator's real audience.")),
             (("Les chiffres sont-ils exacts ?", "Are the figures exact?"), ("Ce sont des données publiques relevées par l'outil, parfois arrondies. Elles servent à repérer des tendances et des anomalies, pas à facturer.", "They are public data collected by the tool, sometimes rounded. They serve to spot trends and anomalies, not to invoice."))]},
]

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
HAND = [("talkwalker", "Talkwalker"), ("visibrain", "Visibrain"), ("youscan", "YouScan"), ("soprism", "SoPrism")]
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


def page_body(x):
    name = x["name"]
    nm = (x.get("fr_name", name), name)
    why = "".join('<article class="card card--hover" data-reveal><span class="card__num">%s</span><h3 class="card__title">%s</h3><p class="card__text">%s</p></article>' % (
        t(k), t(ti), t(tx)) for k, ti, tx in x["why"])
    steps = "".join('''          <li class="flow__item" data-reveal style="--d:%dms">
            <span class="flow__n" aria-hidden="true">%d</span>
            <div class="flow__card">
              <h3 class="flow__title"><span class="flow__tick" aria-hidden="true"></span>%s</h3>
              <p class="flow__text">%s</p>
            </div>
          </li>
''' % (i * 90, i + 1, t(ti), t(tx)) for i, (ti, tx) in enumerate(S["steps"]))
    strengths = "".join('<article class="card card--hover" data-reveal><span class="card__num">0%d</span><h3 class="card__title">%s</h3><p class="card__text">%s</p></article>' % (
        i + 1, t(ti), t(tx)) for i, (ti, tx) in enumerate(x["strengths"]))
    sols = "".join('<article class="solution" data-reveal><span class="solution__band" aria-hidden="true"></span><div class="solution__body"><h3>%s</h3><ul>%s</ul></div></article>' % (
        t(ti), "".join("<li>%s</li>" % t(b) for b in bullets)) for ti, bullets in x["solutions"])
    uses = ""
    for key in x["uses"]:
        c = CASES[key]; f = FAMILY[c["family"]]
        fam = (f["name"][FR].upper(), f["name"][EN].upper())
        uses += ('<a class="cover-card cover-card--%s" href="%s" data-en="%s" data-reveal>'
                 '<span class="cover"><span class="cover__kicker">%s</span><span class="cover__title">%s</span></span>'
                 '<span class="cover-card__body"><span class="cover-card__label">%s</span><h3 class="cover-card__title">%s</h3>'
                 '<span class="cover-card__link">%s</span></span></a>') % (
            TINT[c["family"]], U.case_path(c, FR), U.case_path(c, EN), t(("// " + fam[FR], "// " + fam[EN])), t((c["name"][FR].upper(), c["name"][EN].upper())),
            t(fam), t(c["name"]), t(S["see_case"]))
    ag = agency(x["slug"], name, x.get("fr_name"))
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in [(ag["q"], ag["a"])] + x["faq"])
    why_k = t(("POURQUOI %s" % nm[FR].upper(), "WHY %s" % name.upper()))
    why_t = t(("Pourquoi nous utilisons %s." % nm[FR], "Why we use %s." % name))
    str_k = t(("%s : SES ATOUTS" % nm[FR].upper(), "%s: ITS STRENGTHS" % name.upper()))
    faq_t = t(("Ce que nos clients demandent sur %s." % nm[FR], "What clients ask about %s." % name))
    band_t = t(ag["band"])
    cta_t = t(("Pas sûr que %s soit le bon outil ?" % nm[FR], "Not sure %s is the right tool?" % name))
    return f'''<main id="content">
  <section class="page">
    <div class="shell">
      <div class="page__head">
        <p class="page__eyebrow" data-dim data-reveal><span class="rule" aria-hidden="true"></span><span class="tool-mark"><img src="assets/img/tools/{x["slug"]}.png" alt="{html.escape(name)}" onerror="this.parentNode.remove()" /></span>{t(ag["kick"])}</p>
        <h1 class="page__title" data-dim data-reveal>{"<br>".join(t(pair) for pair in zip(x["h1"][FR].split("<br>"), x["h1"][EN].split("<br>")))}</h1>
        <p class="page__lead" data-dim data-reveal>{t(x["lead"])}</p>
        <div class="page__actions" data-reveal>
          <a class="btn btn--primary" href="book-a-meeting.html">{t(S["book"])} <span aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="tech-tools.html">{t(S["all"])}</a>
        </div>
      </div>

      <section class="block" id="why">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{why_k}</p>
          <h2 class="block__title">{why_t}</h2>
          <p class="block__lead">{t(x["why_lead"])}</p>
        </div>
        <div class="grid grid--two">{why}</div>
      </section>

      <section class="block block--flow" id="approach">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{t(S["steps_k"])}</p>
          <h2 class="block__title">{t(S["steps_t"])}</h2>
          <p class="block__lead">{t(S["steps_lead"])}</p>
        </div>
        <ol class="flow">
{steps}        </ol>
      </section>

      <section class="block" id="strengths">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{str_k}</p>
          <h2 class="block__title">{t(S["strengths_t"])}</h2>
        </div>
        <div class="grid">{strengths}</div>
      </section>

      <section class="block" id="solutions">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{t(S["sol_k"])}</p>
          <h2 class="block__title">{t(S["sol_t"])}</h2>
        </div>
        <div class="solutions">{sols}</div>
      </section>

      <section class="block" id="uses">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{t(S["uses_k"])}</p>
          <h2 class="block__title">{t(S["uses_t"])}</h2>
          <p class="block__lead">{t(S["uses_lead"])}</p>
        </div>
        <div class="covers covers--three">{uses}</div>
      </section>

      <section class="block" id="faq">
        <div class="block__head" data-dim data-reveal>
          <p class="block__kicker block__kicker--slash"><i>//</i>{t(S["faq_k"])}</p>
          <h2 class="block__title">{faq_t}</h2>
        </div>
        <div class="faq" data-dim data-reveal>{faq}</div>
      </section>

      <section class="band" data-reveal>
        <div>
          <p class="block__kicker block__kicker--slash"><i>//</i>{t(S["act_k"])}</p>
          <h2 class="band__title">{band_t}</h2>
        </div>
        <div class="band__actions">
          <a class="btn btn--solid" href="diagnostic.html">{t(S["diag"])} <span aria-hidden="true">→</span></a>
          <a class="btn btn--ghost" href="book-a-meeting.html">{t(S["expert"])} <span aria-hidden="true">→</span></a>
        </div>
      </section>

      <section class="cta" data-reveal>
        <h2 class="cta__title">{cta_t}</h2>
        <p class="cta__text">{t(S["cta_text"])}</p>
        <form class="signup" novalidate>
          <label class="visually-hidden" for="email-{x["slug"]}">Your work email</label>
          <input class="signup__input" id="email-{x["slug"]}" name="email" type="email"
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
</main>'''


def hand_agency(src, slug, name):
    """the four hand-written platform pages get the same agency wording,
    applied again on every build without piling up"""
    ag = agency(slug, name)
    src = re.sub(r'(<span class="tool-mark">.*?</span>)[^<]*(</p>)', lambda m: m.group(1) + t(ag["kick"]) + m.group(2), src, count=1, flags=re.S)
    src = re.sub(r'\s*<details data-agency>.*?</details>', "", src, flags=re.S)
    src = re.sub(r'(<section class="block" id="faq">.*?<div class="faq"[^>]*>)', lambda m: m.group(1) + '\n          <details data-agency>\n            <summary>%s</summary>\n            <p>%s</p>\n          </details>' % (t(ag["q"]), t(ag["a"])), src, count=1, flags=re.S)
    src = re.sub(r'<h2 class="band__title">.*?</h2>', '<h2 class="band__title">%s</h2>' % t(ag["band"]), src, count=1, flags=re.S)
    return src


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
    shell = (ROOT / "tech-talkwalker.html").read_text()
    m0, m1 = shell.index('<main id="content">'), shell.index("</main>") + len("</main>")
    pages = []   # (file, slug, name, title, desc, html)
    for x in TOOLS:
        foot = shell[m1:].replace("email-nl-tech-talkwal", "email-nl-tech-" + x["slug"][:8])
        out = "<!-- Generated by tools/build-tech.py: edit that script, not this file. -->\n" + shell[:m0] + page_body(x) + foot
        ag = agency(x["slug"], x["name"], x.get("fr_name"))
        pages.append(("tech-%s.html" % x["slug"], x["name"], ag["title"], ag["desc"], out))
    for slug, name in HAND:
        f = "tech-%s.html" % slug
        ag = agency(slug, name)
        pages.append((f, name, ag["title"], ag["desc"], hand_agency((ROOT / f).read_text(), slug, name)))
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
    print("%d tool pages written in English and French, %d strings in js/fr.js" % (len(pages), len(O.NEW)))


if __name__ == "__main__":
    main()
