"""The long-form section of the AI listening expertise page (SEO audit of 9
October 2026: the page was 424 words, unsigned and undated). It reads what AI
assistants answer about a brand; acting on those answers is the GEO page
(tools/geo_guide.py), so the two do not repeat each other. Each block is
(heading, [paragraphs]), every string a (French, English) pair. Same
structure as tools/sl_guide.py and tools/al_guide.py.

Licter facts come from the site's own files: the method and the steps of the
AI listening page (tools/build-expertise.py: the same questions put to each
model, read by an analyst, a first measure then monthly or quarterly). Public
facts about the assistants are noted below with their source. Generic
scenarios are marked "par exemple" and are not Licter cases."""

KICKER = ("L'AI LISTENING, EN DÉTAIL", "AI LISTENING, IN DETAIL")
TITLE = ("Ce qu'il faut savoir avant d'écouter ce que les IA disent de vous.", "What to know before you listen to what AI says about you.")

BLOCKS = [
    (("Qu'est-ce que l'AI listening ?", "What is AI listening?"), [
        ("L'AI listening consiste à interroger les assistants d'intelligence artificielle comme le feraient vos clients, puis à lire ce qu'ils répondent sur votre marque et votre catégorie : les marques qu'ils recommandent, les faits qu'ils citent, les sources qu'ils mettent en lien, et ce qu'ils oublient.",
         "AI listening means questioning AI assistants the way your customers would, then reading what they answer about your brand and your category: the brands they recommend, the facts they quote, the sources they link to, and what they leave out."),
        ("C'est une écoute, au même titre que le social listening ou le search listening : on ne lit plus une conversation entre des personnes, mais la synthèse qu'un modèle en tire. Pour beaucoup de recherches, cette synthèse est désormais la première chose qu'un client lit.",
         "It is a form of listening, like social or search listening: instead of a conversation between people, you read the summary a model draws from it. For many searches, that summary is now the first thing a customer reads."),
    ]),
    (("AI listening et GEO : quelle différence ?", "AI listening and GEO: what is the difference?"), [
        ("L'AI listening mesure et lit. Le GEO, pour Generative Engine Optimization, agit : il cherche à améliorer la place d'une marque dans ces réponses, en travaillant les sources que les modèles utilisent. Le premier sert de point de départ et de mesure au second : sans lecture régulière, on ne sait ni où l'on part ni si ce que l'on change fonctionne.",
         "AI listening measures and reads. GEO, for Generative Engine Optimization, acts: it tries to improve a brand's place in those answers by working on the sources the models use. The first is the starting point and the yardstick of the second: without a regular reading, you know neither where you start nor whether what you change works."),
    ]),
    (("Quelles IA écouter ?", "Which AI assistants should you listen to?"), [
        ("Celles que vos clients utilisent pour la question qui vous intéresse. En pratique : ChatGPT, les réponses générées par l'IA dans Google (Aperçus IA et Mode IA, fondés sur Gemini), Gemini lui-même, Claude, Perplexity et Grok. Chacun a ses propres sources et sa propre façon de répondre, ce qui explique qu'une marque puisse être citée par l'un et ignorée par l'autre.",
         "The ones your customers use for the question that matters to you. In practice: ChatGPT, the AI-generated answers in Google (AI Overviews and AI Mode, built on Gemini), Gemini itself, Claude, Perplexity and Grok. Each has its own sources and its own way of answering, which is why a brand can be cited by one and ignored by another."),
        ("Plusieurs de ces assistants cherchent désormais sur le web avant de répondre et citent leurs sources : ChatGPT avec sa recherche, Claude depuis 2025, Perplexity par construction, et Google pour ses Aperçus IA. Ce qu'ils disent dépend donc aussi de ce que le web dit de vous aujourd'hui, pas seulement de leurs données d'entraînement.",
         "Several of these assistants now search the web before answering and cite their sources: ChatGPT with its search, Claude since 2025, Perplexity by design, and Google for its AI Overviews. What they say therefore also depends on what the web says about you today, not only on their training data."),
    ]),
    (("Quelles questions poser aux IA ?", "Which questions should you ask AI?"), [
        ("Les questions de vos clients, pas celles de votre service marketing. On en distingue trois familles : les questions de choix, par exemple « quelle mutuelle pour une famille ? », où l'assistant recommande des marques ; les questions sur la marque elle-même, son prix, ses produits, sa réputation ; et les comparaisons avec un concurrent nommé.",
         "Your customers' questions, not your marketing team's. There are three families: choice questions, for example \"which health insurance for a family?\", where the assistant recommends brands; questions about the brand itself, its price, its products, its reputation; and comparisons with a named competitor."),
        ("Ce sont les questions de choix qui comptent le plus : c'est là qu'une marque gagne ou perd une recommandation sans que personne ne l'ait cherchée par son nom. Une même question est posée plusieurs fois, et à chaque modèle, parce que les réponses varient d'une fois sur l'autre.",
         "Choice questions matter most: that is where a brand wins or loses a recommendation without anyone having searched for it by name. The same question is asked several times, and to each model, because answers vary from one time to the next."),
    ]),
    (("Que mesurer ?", "What should you measure?"), [
        ("Cinq choses, question par question. La présence : la marque est-elle citée, et dans combien de réponses ? Le rang : apparaît-elle en premier ou en fin de liste ? Le ton : ce qui en est dit est-il favorable, neutre ou critique ? L'exactitude : les faits sont-ils justes et à jour ? Les sources : quelles pages l'assistant met-il en lien pour appuyer sa réponse ?",
         "Five things, question by question. Presence: is the brand cited, and in how many answers? Rank: does it appear first or at the end of a list? Tone: is what is said favourable, neutral or critical? Accuracy: are the facts right and current? Sources: which pages does the assistant link to back its answer?"),
        ("Les erreurs sont souvent l'enseignement le plus utile. Par exemple, un tarif de 2022 repris comme actuel, ou une gamme arrêtée présentée comme disponible : la correction passe par les sources que le modèle consulte, pas par le modèle lui-même.",
         "Mistakes are often the most useful finding. For example, a 2022 price quoted as current, or a discontinued range presented as available: the fix goes through the sources the model consults, not through the model itself."),
    ]),
    (("D'où viennent les réponses ?", "Where do the answers come from?"), [
        ("De deux endroits. D'abord des données d'entraînement du modèle, figées à une date, qui expliquent qu'un assistant puisse décrire une marque telle qu'elle était il y a deux ans. Ensuite, pour les assistants qui cherchent en ligne, des pages qu'ils consultent au moment de répondre. Chez Google, une page doit être indexée et pouvoir apparaître avec un extrait pour servir de lien dans les Aperçus IA.",
         "From two places. First, the model's training data, frozen at a date, which is why an assistant can describe a brand as it was two years ago. Then, for assistants that search online, the pages they consult at the moment of answering. At Google, a page must be indexed and able to appear with a snippet to serve as a link in AI Overviews."),
        ("Les robots de ces assistants se règlent séparément : chez OpenAI, celui qui alimente la recherche de ChatGPT et celui qui collecte pour l'entraînement sont indépendants. Un site qui bloque le premier n'apparaît pas dans les réponses de recherche de ChatGPT. Vérifier ces réglages fait partie de l'écoute.",
         "These assistants' crawlers are set separately: at OpenAI, the one that feeds ChatGPT search and the one that collects for training are independent. A site that blocks the first does not appear in ChatGPT search answers. Checking these settings is part of the listening."),
    ]),
    (("Les limites de l'AI listening", "The limits of AI listening"), [
        ("Les réponses ne sont pas stables : elles changent d'une session à l'autre, d'une version de modèle à la suivante, et parfois selon l'historique de l'utilisateur. Une mesure isolée ne dit donc pas grand-chose ; c'est la répétition des mêmes questions, dans le temps, qui donne une tendance fiable.",
         "Answers are not stable: they change from one session to another, from one model version to the next, and sometimes with the user's history. A single measure says little; it is asking the same questions again, over time, that gives a reliable trend."),
        ("L'AI listening ne dit pas non plus combien de personnes posent ces questions. Pour le volume, il faut le croiser avec le search listening, qui lit ce que les gens cherchent sur Google, YouTube et Amazon.",
         "AI listening does not say how many people ask these questions either. For volume, it has to be crossed with search listening, which reads what people search for on Google, YouTube and Amazon."),
    ]),
    (("Comment Licter mène une étude d'AI listening", "How Licter runs an AI listening study"), [
        ("Le cadrage fixe les questions que posent vos clients et les modèles à interroger. Les mêmes questions sont ensuite posées à chaque modèle, plusieurs fois, puis un analyste lit les réponses : ce qu'elles recommandent, citent, oublient ou déforment. La restitution se termine par un plan : les sources à corriger ou à nourrir.",
         "The framing sets the questions your customers ask and the models to question. The same questions are then put to each model, several times, and an analyst reads the answers: what they recommend, cite, leave out or get wrong. The readout ends with a plan: the sources to correct or to feed."),
        ("Après une première mesure, nous recommençons chaque mois ou chaque trimestre avec les mêmes questions, pour que les résultats se comparent. Licter est un cabinet indépendant : nous n'éditons aucun assistant et ne vendons pas de visibilité dans leurs réponses.",
         "After a first measure, we start again every month or quarter with the same questions, so the results can be compared. Licter is an independent consultancy: we publish no assistant and do not sell visibility in their answers."),
    ]),
]

# source: https://blog.google/intl/fr-fr/nouveautes-produits/explorez-obtenez-des-reponses/recherche-ia-apercus-mode/
# source: https://developers.google.com/search/docs/appearance/ai-features
# source: https://claude.com/blog/web-search
# source: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
# source: https://developers.openai.com/api/docs/bots
# source: https://arxiv.org/abs/2311.09735
