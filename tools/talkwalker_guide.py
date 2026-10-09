"""The long-form section of the Talkwalker tool page (SEO audit: the page was
too short for "Talkwalker", "agence Talkwalker", "Talkwalker avis",
"Talkwalker formation", "alternative Talkwalker"): what the platform is, what
it does and does not do on its own, how to configure it, how it compares with
Brandwatch and Sprinklr, the alternatives, when an agency helps, how to take
over an under-used licence, and what Charlotte (who opened Talkwalker's Paris
office) told our podcast. Each block is (heading, [paragraphs]), every string
a (French, English) pair. Licter statements come from the site's own pages
(fr/outils/talkwalker, fr/offres/social-listening-as-a-service,
fr/outils/brandwatch, fr/outils/sprinklr, tools/tools_data.py); quotes come
from article-licter-talkwalker-podcast.html / tools/podcast_quotes.py; public
facts about Talkwalker carry a `# source:` comment."""

KICKER = ("TALKWALKER, EN DÉTAIL", "TALKWALKER, IN DETAIL")
TITLE = ("Ce qu'il faut savoir avant de choisir, ou de reprendre, Talkwalker.", "What to know before you choose, or take over, Talkwalker.")

BLOCKS = [
    (("Qu'est-ce que Talkwalker ?", "What is Talkwalker?"), [
        # source: https://www.talkwalker.com/press-release/hootsuite (founded 2009 in Luxembourg; acquisition announced 8 April 2024; Luxembourg office becomes Hootsuite's European HQ)
        ("Talkwalker est une plateforme d'écoute sociale née au Luxembourg en 2009. En avril 2024, Hootsuite, spécialiste canadien de la gestion des réseaux sociaux, a annoncé son rachat. Le siège luxembourgeois est devenu le siège européen de l'ensemble. L'accès à la plateforme est payant, sur devis.",
         "Talkwalker is a social listening platform born in Luxembourg in 2009. In April 2024, Hootsuite, the Canadian social media management company, announced it was buying it. The Luxembourg head office became the European head office of the combined group. Access to the platform is paid, quoted on request."),
        # source: https://talkwalker.com/products/bluesilkai (Blue Silk AI: image recognition in video, memes, GIFs; sentiment and emotion analysis; query assistant with Boolean support; 90-day forecasting)
        ("Son principe est simple : collecter ce qui se publie publiquement sur les réseaux sociaux, la presse en ligne, les blogs, les forums et les avis, puis le classer. Sa couche d'intelligence artificielle, baptisée Blue Silk AI, ajoute la reconnaissance de logos dans les images et les vidéos, l'analyse du sentiment et des émotions, une aide à l'écriture des requêtes et des projections de volumes.",
         "Its principle is simple: collect what is published publicly on social networks, online press, blogs, forums and reviews, then sort it. Its artificial intelligence layer, called Blue Silk AI, adds logo recognition in images and videos, sentiment and emotion analysis, help with writing queries, and volume forecasts."),
    ]),
    (("Que peut-on faire avec Talkwalker ?", "What can you do with Talkwalker?"), [
        ("Suivre une marque dans la durée, d'abord : ses volumes, ses sujets, sa tonalité, et sa place face aux concurrents, semaine après semaine. L'historique permet de comparer une période à une autre, par exemple avant et après une campagne, sur un périmètre identique. C'est l'usage le plus courant, et celui où la plateforme est la plus à l'aise.",
         "First, tracking a brand over time: its volumes, its subjects, its tone, and its position against competitors, week after week. The history lets you compare one period with another, for instance before and after a campaign, on an identical perimeter. It is the most common use, and the one where the platform is most at ease."),
        ("Elle sert aussi à étudier une catégorie entière sur plusieurs marchés, sans reconstruire la requête pays par pays, et à repérer une marque dans les visuels, même quand personne ne la nomme. Enfin, les alertes signalent les hausses anormales de volume : utiles pour voir une crise démarrer, à condition que quelqu'un les lise et sache quoi en faire.",
         "It also serves to study a whole category across several markets, without rebuilding the query country by country, and to spot a brand in visuals, even when nobody names it. Finally, alerts flag abnormal rises in volume: useful to see a crisis starting, provided someone reads them and knows what to do with them."),
    ]),
    (("Ce que Talkwalker ne fait pas tout seul", "What Talkwalker does not do on its own"), [
        ("Talkwalker collecte et classe ; il ne décide pas. Un pic de volume ne dit jamais pourquoi il existe. Le sentiment automatique se trompe sur l'ironie, le second degré et certaines langues. Une requête trop large ramène des homonymes, une requête trop étroite manque la moitié de la conversation. Aucun tableau de bord ne corrige cela de lui-même.",
         "Talkwalker collects and sorts; it does not decide. A volume spike never says why it exists. Automatic sentiment gets irony, tongue-in-cheek posts and some languages wrong. A query that is too broad brings back homonyms, one that is too narrow misses half the conversation. No dashboard fixes this on its own."),
        ("Comme toutes les plateformes d'écoute, il ne lit que le public : ni messages privés, ni comptes fermés. Et sa couverture varie selon les réseaux, qui encadrent l'accès à leurs données. Avant chaque étude, nous vérifions ce qui est réellement couvert pour la question posée, et nous le croisons au besoin avec un autre outil.",
         "Like every listening platform, it only reads what is public: no private messages, no closed accounts. And its coverage varies by network, as each one regulates access to its data. Before every study, we check what is really covered for the question asked, and cross it with another tool when needed."),
    ]),
    (("Bien configurer Talkwalker : requêtes, bruit, langues", "Configuring Talkwalker well: queries, noise, languages"), [
        ("Tout commence par la requête booléenne : les noms de marque, de produits et de concurrents, leurs variantes et leurs fautes courantes, et les exclusions qui écartent les homonymes. Talkwalker propose un assistant pour l'écrire, mais personne ne connaît mieux que vous les mots de votre marché. Une requête se teste sur un échantillon lu à la main avant d'être lancée.",
         "It all starts with the Boolean query: brand, product and competitor names, their variants and common misspellings, and the exclusions that rule out homonyms. Talkwalker offers an assistant to write it, but nobody knows your market's words better than you do. A query is tested on a hand-read sample before it goes live."),
        ("Viennent ensuite la taxonomie, c'est-à-dire les sujets classés comme votre entreprise en parle, puis les langues et les pays. Un produit ne porte pas toujours le même nom d'un marché à l'autre, et le bruit change selon la langue. Une configuration n'est jamais finie : elle se relit à chaque nouveau produit, chaque campagne, chaque concurrent qui apparaît.",
         "Then comes the taxonomy, meaning the subjects sorted the way your company talks about them, then languages and countries. A product does not always carry the same name from one market to another, and the noise changes with the language. A configuration is never finished: it is reread with every new product, every campaign, every competitor that appears."),
    ]),
    # vendor-neutral on purpose: Licter works with every platform and never ranks them (owner rule, audit of 9 October 2026)
    (("Comment choisir sa plateforme de social listening ?", "How do you choose a social listening platform?"), [
        ("Il n'existe pas de meilleure plateforme dans l'absolu. Le bon choix dépend de la question à traiter, puis de quelques critères concrets : les sources et les pays couverts, les langues, la profondeur d'historique, la lecture des images, et la façon dont l'outil s'intègre à ce que vos équipes utilisent déjà.",
         "There is no best platform in absolute terms. The right choice depends on the question at hand, then on a few concrete criteria: the sources and countries covered, the languages, the depth of history, image reading, and how the tool fits with what your teams already use."),
        ("Testez chaque plateforme sur votre propre périmètre, avec vos mots et vos concurrents, plutôt que sur une démonstration. Nous opérons les principales plateformes du marché, Talkwalker comprise, et ne sommes l'éditeur d'aucune : nous choisissons selon la question, et il nous arrive d'en croiser plusieurs.",
         "Test each platform on your own scope, with your words and your competitors, rather than on a demo. We run the main platforms on the market, Talkwalker included, and publish none of them: we choose according to the question, and sometimes cross several."),
    ]),
    (("Faut-il changer de plateforme ?", "Should you switch platforms?"), [
        ("Avant de changer d'outil, posez-vous une question : le problème vient-il de la plateforme, ou de la façon dont elle est configurée et lue ? Une licence mal réglée donnera les mêmes déceptions ailleurs, et une migration coûte des mois d'historique et de réglages.",
         "Before switching tools, ask yourself one question: does the problem come from the platform, or from the way it is configured and read? A badly set-up licence will bring the same disappointments elsewhere, and a migration costs months of history and settings."),
        ("Une reprise de configuration suffit souvent : requêtes relues, taxonomie refaite, tableaux de bord utiles. Nous utilisons 19 outils et ne sommes l'éditeur d'aucun : si une autre plateforme répond mieux à votre question, nous vous le disons.",
         "A configuration overhaul is often enough: queries reread, taxonomy rebuilt, useful dashboards. We use 19 tools and publish none of them: if another platform answers your question better, we tell you."),
    ]),
    (("Faut-il une agence ou une formation Talkwalker ?", "Do you need a Talkwalker agency, or training?"), [
        ("Si vos équipes ont le temps et l'envie d'apprendre l'outil, une formation peut suffire. Sinon, une agence l'opère à votre place. Licter n'est ni l'éditeur ni un revendeur de Talkwalker : nous sommes un cabinet indépendant qui l'utilise pour ses clients. Pour une étude, la licence est la nôtre : vous achetez l'analyse, pas un accès.",
         "If your teams have the time and the will to learn the tool, training may be enough. Otherwise, an agency runs it for you. Licter is neither Talkwalker's publisher nor a reseller: we are an independent consultancy that uses it for its clients. For a study, the licence is ours: you buy the analysis, not a seat."),
        ("Les deux ne s'opposent pas. Quand une entreprise a déjà sa licence, nous la reprenons et formons ses équipes, par rôle et sur leurs propres données, pas sur un compte de démonstration. Le but n'est pas de rendre tout le monde expert de l'outil, mais que chaque équipe sache lire ce qui la concerne et en tirer une décision.",
         "The two are not opposed. When a company already has its licence, we take it over and train its teams, by role and on their own data, not on a demo account. The aim is not to make everyone an expert in the tool, but for each team to read what concerns it and draw a decision from it."),
    ]),
    (("Reprendre un Talkwalker sous-utilisé", "Taking over an under-used Talkwalker"), [
        ("Le cas est fréquent : une licence payée chaque année, des tableaux de bord configurés une fois et jamais revus, des exports envoyés sans conclusion. C'est l'objet de notre offre Social Listening as a Service. La licence reste la vôtre ; nous commençons par un audit de deux semaines, qui confronte la configuration aux questions que vos équipes se posent vraiment.",
         "It is a common case: a licence paid every year, dashboards configured once and never revisited, exports sent without a conclusion. That is what our Social Listening as a Service offer is for. The licence stays yours; we start with a two-week audit that sets the configuration against the questions your teams really ask."),
        ("Viennent ensuite la reprise de la taxonomie et des tableaux de bord, moins nombreux et chacun construit pour une équipe et une décision, en six semaines environ. Les analyses récurrentes arrivent dès le deuxième mois, dans votre plateforme, et l'usage est mesuré chaque trimestre. Si l'audit montre que l'outil ne correspond pas à vos besoins, nous vous le disons.",
         "Then come the rebuild of the taxonomy and dashboards, fewer of them, each built for one team and one decision, in about six weeks. Recurring analyses arrive from the second month, inside your platform, and usage is measured every quarter. If the audit shows the tool does not fit your needs, we tell you."),
    ]),
    (("Talkwalker : l'avis de quelqu'un qui l'a déployé", "Talkwalker: the view of someone who rolled it out"), [
        ("Charlotte Clemens a rejoint Talkwalker quand c'était encore une start-up, puis a ouvert son bureau parisien. Dans notre podcast Audience First, elle décrit l'outil comme « un collecteur de datas en temps réel qui va chercher la data sur les blogs, les forums, les sites d'actualité et les réseaux sociaux ». D'abord vendu aux agences, il s'est ouvert aux marques, et l'enjeu est devenu l'adoption et la formation des équipes.",
         "Charlotte Clemens joined Talkwalker when it was still a start-up, then opened its Paris office. On our Audience First podcast, she describes the tool as a real-time data collector that fetches data from blogs, forums, news sites and social networks. First sold to agencies, it opened up to brands, and the challenge became team adoption and training."),
        ("Elle insiste surtout sur la part humaine : « pour du consumer insight, du trends, du market research, l'humain aura toujours sa place pour vraiment donner de la perspective à la data ». Agence ou annonceur, l'usage est le même à ses yeux, et tout part d'une question : « C'est quoi ton cas d'usage ? ». Et sans ressources internes, elle conseille de se faire accompagner plutôt que de rester seul face à l'outil.",
         "Above all, she stresses the human part: for consumer insight, trends and market research, people will always have a role in giving the data perspective. Agency or advertiser, the use is the same in her eyes, and everything starts from one question: what is your use case? And without internal resources, she advises getting support rather than staying alone with the tool."),
    ]),
]
