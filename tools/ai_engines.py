"""What sets each AI assistant apart (SEO audit, October 2026: the five
assistant pages were too close to each other). Only public, stable facts
about how each one builds its answers, then what Licter checks on it.
Read by tools/build-tech.py.

INTENT also renames the pages whose "Agence X" title drew the wrong search
(buying ads, partnering with the AI publisher)."""

INTENT = {
    "chatgpt": {"title": ("Votre marque dans ChatGPT : audit des réponses | Licter", "Your brand in ChatGPT: an audit of its answers | Licter"),
                "h1": ("VOTRE MARQUE DANS CHATGPT,", "YOUR BRAND IN CHATGPT,"),
                "kick": ("CHATGPT ET VOTRE MARQUE", "CHATGPT AND YOUR BRAND")},
    "claude": {"title": ("Votre marque dans Claude : ce que l'IA répond | Licter", "Your brand in Claude: what the AI answers | Licter"),
               "h1": ("VOTRE MARQUE DANS CLAUDE,", "YOUR BRAND IN CLAUDE,"),
               "kick": ("CLAUDE ET VOTRE MARQUE", "CLAUDE AND YOUR BRAND")},
    "gemini": {"title": ("Votre marque dans Gemini et les réponses IA de Google | Licter", "Your brand in Gemini and Google's AI answers | Licter"),
               "h1": ("VOTRE MARQUE DANS GEMINI,", "YOUR BRAND IN GEMINI,"),
               "kick": ("GEMINI ET VOTRE MARQUE", "GEMINI AND YOUR BRAND")},
    "perplexity": {"title": ("Votre marque dans Perplexity : sources et citations | Licter", "Your brand in Perplexity: sources and citations | Licter"),
                   "h1": ("VOTRE MARQUE DANS PERPLEXITY,", "YOUR BRAND IN PERPLEXITY,"),
                   "kick": ("PERPLEXITY ET VOTRE MARQUE", "PERPLEXITY AND YOUR BRAND")},
    "grok": {"title": ("Votre marque dans Grok : ce que l'IA de X répond | Licter", "Your brand in Grok: what X's AI answers | Licter"),
             "h1": ("VOTRE MARQUE DANS GROK,", "YOUR BRAND IN GROK,"),
             "kick": ("GROK ET VOTRE MARQUE", "GROK AND YOUR BRAND")},
    "geo": {"title": ("GEO : votre visibilité dans les réponses des IA | Licter", "GEO: your visibility in AI answers | Licter"),
            "h1": ("LE GEO,", "GEO,"),
            "kick": ("GENERATIVE ENGINE OPTIMIZATION", "GENERATIVE ENGINE OPTIMIZATION")},
    "google-trends": {"title": ("Google Trends : lire les tendances de recherche | Licter", "Google Trends: reading search trends | Licter"),
                      "h1": ("GOOGLE TRENDS,", "GOOGLE TRENDS,"), "kick": ("TENDANCES DE RECHERCHE", "SEARCH TRENDS")},
    "answerthepublic": {"title": ("AnswerThePublic : les questions de votre marché | Licter", "AnswerThePublic: your market's questions | Licter"),
                        "h1": ("ANSWERTHEPUBLIC,", "ANSWERTHEPUBLIC,"), "kick": ("LES QUESTIONS DU MARCHÉ", "THE MARKET'S QUESTIONS")},
    "semrush": {"title": ("Semrush : ce que vos clients cherchent sur Google | Licter", "Semrush: what your customers search for on Google | Licter"),
                "h1": ("SEMRUSH,", "SEMRUSH,"), "kick": ("ÉCOUTE DE LA RECHERCHE", "SEARCH LISTENING")},
    "social-blade": {"title": ("Social Blade : vérifier les comptes et les créateurs | Licter", "Social Blade: checking accounts and creators | Licter"),
                     "h1": ("SOCIAL BLADE,", "SOCIAL BLADE,"), "kick": ("VÉRIFIER UNE AUDIENCE", "CHECKING AN AUDIENCE")},
    "google-news": {"title": ("Google Actualités : la presse face au social | Licter", "Google News: the press against social | Licter"),
                    "h1": ("GOOGLE ACTUALITÉS,", "GOOGLE NEWS,"), "kick": ("PRESSE ET RÉSEAUX", "PRESS AND SOCIAL")},
    "meta-ads": {"title": ("Veille Meta Ads : les publicités de vos concurrents | Licter", "Meta Ads monitoring: your competitors' ads | Licter"),
                 "h1": ("VEILLE META ADS,", "META ADS MONITORING,"),
                 "kick": ("VEILLE PUBLICITAIRE", "AD MONITORING")},
}

AG_T = ("Pourquoi confier ce suivi à un cabinet ?", "Why hand this tracking to a consultancy?")
AG_LEAD_BY = {"semrush": ("Semrush donne des volumes de recherche. Ce que nous apportons, c'est la lecture : ce que ces recherches disent de votre marché, croisé avec la conversation sociale.",
                          "Semrush gives search volumes. What we bring is the reading: what those searches say about your market, crossed with the social conversation."),
              "geo": ("Le GEO ne s'achète pas comme un logiciel : c'est une méthode, appliquée question après question. Voici comment nous la menons.",
                      "GEO is not bought like software: it is a method, applied question by question. Here is how we run it.")}
AG_LEAD = ("%s est ouvert à tous. Ce que nous apportons, c'est la méthode, la lecture et le croisement avec vos autres sources : voici comment nous procédons.",
           "%s is open to everyone. What we bring is the method, the reading and the cross-check with your other sources: here is how we go about it.")
FAQ_Q = {"meta-ads": ("Licter fait-elle de la veille sur la bibliothèque publicitaire Meta ?", "Does Licter monitor the Meta Ad Library?")}
FAQ_Q_AI = ("Licter suit-elle ce que %s dit des marques ?", "Does Licter track what %s says about brands?")

# the "on its own / with Licter" block, rewritten for a free assistant and for the ad library
VS = {
    "ai": ([("Une question posée une fois, par une seule personne", "A question asked once, by one person"),
            ("Des réponses qui changent d'un essai à l'autre", "Answers that change from one try to the next"),
            ("Aucune trace des sources citées", "No record of the sources cited"),
            ("Pas de comparaison avec vos concurrents", "No comparison with your competitors")],
           [("Les mêmes questions posées plusieurs fois, chaque mois", "The same questions asked several times, every month"),
            ("Les sources citées relevées et classées", "The sources cited, collected and sorted"),
            ("Votre place face à vos concurrents", "Your place against your competitors"),
            ("Ce qu'il faut corriger, et où agir", "What to correct, and where to act")],
           ("Vous savez ce que l'IA dit de vous, et pourquoi.", "You know what the AI says about you, and why.")),
    "meta-ads": ([("Une bibliothèque à parcourir annonce par annonce", "A library to browse ad by ad"),
                  ("Des campagnes vues au hasard des recherches", "Campaigns seen by chance"),
                  ("Aucune lecture des messages ni des formats", "No reading of messages or formats"),
                  ("Pas de lien avec la conversation sur les réseaux", "No link with the social conversation")],
                 [("Les campagnes de vos concurrents relevées chaque mois", "Your competitors' campaigns collected every month"),
                  ("Messages, formats et calendriers comparés", "Messages, formats and timing compared"),
                  ("Le croisement avec ce qui se dit sur les réseaux", "Cross-checked with what is said on social media"),
                  ("Une note pour vos arbitrages", "A note for your decisions")],
                 ("Vous voyez ce que vos concurrents poussent, et ce que cela vous dit.", "You see what your competitors push, and what it tells you.")),
}

HEAD = (("COMMENT %s RÉPOND", "HOW %s ANSWERS"), ("Ce qui fait la réponse de %s.", "What shapes %s's answer."))

ENGINE = {
    "chatgpt": [
        (("D'où viennent ses réponses", "Where its answers come from"),
         ("Sans recherche, ChatGPT répond depuis ses données d'entraînement, arrêtées à une date. Avec la recherche web, ouverte à tous ses utilisateurs depuis fin 2024, il lit des pages en direct et cite ses liens.",
          "Without search, ChatGPT answers from its training data, frozen at a date. With web search, open to all its users since late 2024, it reads pages live and cites its links.")),
        (("Ce qui le distingue", "What sets it apart"),
         ("C'est l'assistant le plus utilisé : c'est souvent là qu'un client pose d'abord la question « quelle marque choisir ? ». Sa réponse mêle ce qu'il a appris et ce qu'il trouve, et les deux ne disent pas toujours la même chose.",
          "It is the most used assistant: it is often where a customer first asks \"which brand should I choose?\". Its answer mixes what it learned and what it finds, and the two do not always agree.")),
        (("Ce que nous vérifions", "What we check"),
         ("Nous posons chaque question avec et sans recherche web. L'écart entre les deux montre ce qui est daté dans sa mémoire, et quelles pages il va lire aujourd'hui pour se corriger.",
          "We ask each question with and without web search. The gap between the two shows what is outdated in its memory, and which pages it reads today to correct itself."))],
    "claude": [
        (("D'où viennent ses réponses", "Where its answers come from"),
         ("Claude, l'assistant d'Anthropic, répond d'abord depuis ses données d'entraînement. Depuis 2025, il peut aussi chercher sur le web ; il cite alors les pages qu'il a lues.",
          "Claude, Anthropic's assistant, answers first from its training data. Since 2025 it can also search the web; it then cites the pages it read.")),
        (("Ce qui le distingue", "What sets it apart"),
         ("Il est beaucoup utilisé au travail, pour rédiger, analyser et préparer des décisions : ses réponses touchent des acheteurs, des analystes, des journalistes. Il signale volontiers ce qu'il ne sait pas : une marque mal documentée y est plus souvent absente que mal décrite.",
          "It is widely used at work, to write, analyse and prepare decisions: its answers reach buyers, analysts and journalists. It readily says what it does not know: a poorly documented brand is more often missing than misdescribed.")),
        (("Ce que nous vérifions", "What we check"),
         ("Si Claude connaît votre marque sans chercher, et ce qu'il en dit quand il cherche. Une absence se traite par la documentation publique : site, presse, pages de référence.",
          "Whether Claude knows your brand without searching, and what it says when it searches. An absence is fixed through public documentation: your site, the press, reference pages."))],
    "gemini": [
        (("D'où viennent ses réponses", "Where its answers come from"),
         ("Gemini est l'IA de Google. Il s'appuie sur la recherche Google, la même famille de modèles que les réponses générées en haut des résultats (AI Overviews et mode IA).",
          "Gemini is Google's AI. It relies on Google Search, the same family of models as the generated answers at the top of results (AI Overviews and AI Mode).")),
        (("Ce qui le distingue", "What sets it apart"),
         ("Ce que Google sait de vous compte directement : vos pages indexées, votre fiche d'établissement, les avis, YouTube. Une erreur dans Gemini se retrouve souvent dans les résultats de recherche, et l'inverse.",
          "What Google knows about you counts directly: your indexed pages, your Business Profile, reviews, YouTube. An error in Gemini often shows up in search results, and the other way round.")),
        (("Ce que nous vérifions", "What we check"),
         ("Nous comparons Gemini et les réponses IA de la recherche Google sur les mêmes questions, puis nous remontons aux pages et aux fiches qui les nourrissent.",
          "We compare Gemini and Google Search's AI answers on the same questions, then trace back to the pages and listings that feed them."))],
    "perplexity": [
        (("D'où viennent ses réponses", "Where its answers come from"),
         ("Perplexity cherche sur le web à chaque question et affiche ses sources, numérotées, à côté de la réponse. Il se présente comme un moteur de réponses plus que comme un assistant.",
          "Perplexity searches the web for every question and shows its sources, numbered, next to the answer. It presents itself as an answer engine more than an assistant.")),
        (("Ce qui le distingue", "What sets it apart"),
         ("Chaque réponse dit d'où elle vient : on peut mesurer quelles pages comptent vraiment pour votre catégorie. Les pages récentes, la presse et les forums y pèsent lourd.",
          "Every answer says where it comes from: you can measure which pages really count for your category. Recent pages, the press and forums weigh heavily.")),
        (("Ce que nous vérifions", "What we check"),
         ("La liste des sites cités sur les questions de votre marché, la part qui parle de vous, et les sources de vos concurrents que vous n'avez pas.",
          "The list of sites cited on your market's questions, the share that talks about you, and the sources your competitors have and you do not."))],
    "grok": [
        (("D'où viennent ses réponses", "Where its answers come from"),
         ("Grok est l'IA de xAI, intégrée à X. Il lit les publications publiques de X en temps réel, en plus du web.",
          "Grok is xAI's AI, built into X. It reads public posts on X in real time, as well as the web.")),
        (("Ce qui le distingue", "What sets it apart"),
         ("Il reflète la conversation de X presque en direct : une polémique sur X peut entrer dans ses réponses en quelques heures, bien avant les autres assistants.",
          "It mirrors the conversation on X almost live: a controversy on X can enter its answers within hours, well before other assistants.")),
        (("Ce que nous vérifions", "What we check"),
         ("Ce que Grok dit de vous pendant et après un pic sur X, quels comptes et quelles publications il reprend, et si une rumeur y survit une fois retombée sur le réseau.",
          "What Grok says about you during and after a spike on X, which accounts and posts it picks up, and whether a rumour survives there once it has died down on the network."))],
}
