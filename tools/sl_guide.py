"""The long-form section of the social listening expertise page (SEO plan,
step 15): what social listening is, how it differs from monitoring, where the
data comes from, the method, the tools, and what an agency or a consultancy
adds. Each block is (heading, [paragraphs]), every string a (French, English)
pair. Read by tools/build-expertise.py."""

KICKER = ("LE SOCIAL LISTENING, EN DÉTAIL", "SOCIAL LISTENING, IN DETAIL")
TITLE = ("Tout ce qu'il faut savoir avant de lancer une étude.", "What to know before you start a study.")

BLOCKS = [
    (("Qu'est-ce que le social listening ?", "What is social listening?"), [
        ("Le social listening, ou écoute sociale, consiste à collecter et analyser ce que les gens publient en ligne sur une marque, un produit, un concurrent ou un sujet : réseaux sociaux, forums, sites d'avis, blogs et presse en ligne. L'objectif n'est pas de compter des mentions, mais de comprendre une perception et de décider quoi en faire.",
         "Social listening means collecting and analysing what people publish online about a brand, a product, a competitor or a subject: social networks, forums, review sites, blogs and online press. The goal is not to count mentions, but to understand a perception and decide what to do about it."),
        ("Là où une étude classique interroge quelques centaines de personnes, le social listening observe ce que des milliers de personnes disent spontanément, sans qu'on leur ait posé la question. C'est sa force : un comportement observé plutôt qu'une réponse déclarée. C'est aussi sa limite : on n'y lit que ce qui est public, et seulement ce que les gens choisissent de dire.",
         "Where a classic survey asks a few hundred people, social listening observes what thousands say spontaneously, without being asked. That is its strength: observed behaviour rather than a declared answer. It is also its limit: it only reads what is public, and only what people choose to say."),
    ]),
    (("Social listening, veille, monitoring : les différences", "Social listening, monitoring, tracking: the differences"), [
        ("Le social media monitoring, ou veille, signale ce qui se passe : une mention, un pic, une crise qui démarre. Il sert à réagir, souvent en temps réel. Le social listening va plus loin : il analyse la conversation dans la durée pour expliquer pourquoi elle bouge, qui la porte et ce qu'elle dit d'un marché.",
         "Social media monitoring signals what happens: a mention, a spike, a crisis taking off. It serves to react, often in real time. Social listening goes further: it analyses the conversation over time to explain why it moves, who carries it and what it says about a market."),
        ("Les deux utilisent les mêmes données et les mêmes plateformes. La différence tient à la question posée et au travail de lecture. Une veille répond à « s'est-il passé quelque chose ? » ; une étude de social listening répond à « que faut-il en conclure, et que décider ? ». Pour la veille et la gestion de crise, voir notre guide de la veille des réseaux sociaux et notre offre Vigie 360.",
         "Both use the same data and the same platforms. The difference lies in the question asked and in the reading. Monitoring answers \"did something happen?\"; a social listening study answers \"what should we conclude, and what should we decide?\". For monitoring and crisis management, see our guide to social media monitoring and our Vigie 360 offer."),
    ]),
    (("Ce que le social listening permet de décider", "What social listening helps you decide"), [
        ("La réputation d'une marque : ce qui se dit d'elle, sur quels sujets, avec quelle tonalité, et comment cela évolue face aux concurrents. Une campagne : ce qu'elle a changé dans la conversation, audience par audience, et ce qui a vraiment porté. Un produit : ce que les clients aiment, ce qui les irrite, et le vocabulaire qu'ils emploient pour en parler.",
         "A brand's reputation: what is said about it, on which subjects, in which tone, and how that evolves against competitors. A campaign: what it changed in the conversation, audience by audience, and what really carried it. A product: what customers like, what irritates them, and the words they use to talk about it."),
        ("Les tendances d'un marché, enfin : les sujets qui accélèrent, les attentes mal couvertes, les signaux faibles qui annoncent un basculement. Dans chaque cas, la valeur n'est pas dans le tableau de bord, mais dans la décision qu'il permet de prendre et de défendre.",
         "And a market's trends: the subjects gaining speed, the expectations nobody covers well, the weak signals that announce a shift. In each case, the value is not in the dashboard, but in the decision it lets you make and defend."),
    ]),
    (("D'où viennent les données", "Where the data comes from"), [
        ("Des publications publiques : X, TikTok, Instagram, Facebook, YouTube, LinkedIn, Reddit, et une vingtaine d'autres réseaux selon les pays et les sujets, dont Weibo, Douyin ou VK pour les marchés où ils comptent. S'y ajoutent les forums, les sites d'avis, les blogs et la presse en ligne, parce qu'un sujet circule constamment de l'un à l'autre.",
         "From public posts: X, TikTok, Instagram, Facebook, YouTube, LinkedIn, Reddit, and some twenty other networks depending on countries and subjects, including Weibo, Douyin or VK in the markets where they matter. Add forums, review sites, blogs and online press, because a subject keeps travelling from one to the other."),
        ("Les messageries privées, les comptes fermés et les groupes privés restent hors de portée. La couverture varie aussi selon les réseaux, qui encadrent l'accès à leurs données : avant chaque étude, nous vérifions ce qui est réellement couvert pour la question posée. Nos pages réseaux détaillent ce que chaque plateforme permet de lire.",
         "Private messaging, closed accounts and private groups remain out of reach. Coverage also varies by network, as each one regulates access to its data: before every study, we check what is really covered for the question asked. Our network pages detail what each platform lets us read."),
    ]),
    (("La méthode, en cinq temps", "The method, in five steps"), [
        ("Tout commence par la question : la décision que l'étude doit éclairer, et ce qui compterait comme une réponse. Viennent ensuite le périmètre et les requêtes : marques, produits, concurrents, marchés, langues, et des requêtes booléennes testées pour écarter les homonymes et le bruit. C'est le travail le plus sous-estimé, et celui dont dépend tout le reste.",
         "It all starts with the question: the decision the study must inform, and what would count as an answer. Then come the perimeter and the queries: brands, products, competitors, markets, languages, and Boolean queries tested to rule out homonyms and noise. It is the most underestimated part, and everything else depends on it."),
        ("Puis la collecte et le nettoyage, sur les sources adaptées. Puis la lecture : un analyste qui parle la langue du marché qualifie les publications, relie les signaux et vérifie ce que l'outil a classé. Enfin la restitution : une recommandation présentée aux équipes concernées, avec ce qui la fonde et ce qu'il faudra suivre ensuite.",
         "Then collection and cleaning, on the right sources. Then the reading: an analyst who speaks the market's language qualifies the posts, connects the signals and checks what the tool has classified. Finally the readout: a recommendation presented to the teams concerned, with what supports it and what to follow next."),
    ]),
    (("Les outils, et pourquoi un outil ne suffit pas", "The tools, and why a tool is not enough"), [
        ("Le marché compte de nombreuses plateformes de social listening : Talkwalker, Brandwatch, Sprinklr, Radarly, YouScan, Visibrain, entre autres, chacune avec ses points forts. Certaines excellent dans l'historique long, d'autres dans le temps réel, l'image ou les audiences. Aucune ne couvre tout, et la plupart des questions se règlent en croisant deux outils.",
         "The market counts many social listening platforms: Talkwalker, Brandwatch, Sprinklr, Radarly, YouScan, Visibrain, among others, each with its strengths. Some excel at long history, others at real time, images or audiences. None covers everything, and most questions are answered by crossing two tools."),
        ("Surtout, un outil collecte et classe ; il ne décide pas. Le sentiment automatique se trompe sur l'ironie, les requêtes mal écrites ramènent du bruit, et un pic de volume ne dit jamais pourquoi il existe. C'est pourquoi tant de licences restent sous-utilisées : le logiciel est là, mais personne n'a le temps de le faire parler.",
         "Above all, a tool collects and sorts; it does not decide. Automatic sentiment gets irony wrong, badly written queries bring back noise, and a volume spike never says why it exists. That is why so many licences stay underused: the software is there, but nobody has the time to make it speak."),
    ]),
    (("Agence ou cabinet de social listening : ce que vous achetez", "Social listening agency or consultancy: what you buy"), [
        ("Avec une agence ou un cabinet de social listening, vous n'achetez pas un accès à un logiciel, mais une réponse. Le choix des outils, l'écriture des requêtes, la lecture dans la langue du marché et la recommandation sont pris en charge. Vos équipes gardent leur temps pour la décision.",
         "With a social listening agency or consultancy, you do not buy access to software, but an answer. The choice of tools, the writing of queries, the reading in the market's language and the recommendation are taken care of. Your teams keep their time for the decision."),
        ("Licter est un cabinet de conseil en social data intelligence : nous opérons les plateformes du marché sans en être l'éditeur, et nous choisissons l'outil selon la question. Si vous avez déjà une licence, nous pouvons la reprendre et la faire servir. Une première lecture prend une dizaine de jours, du cadrage à la restitution.",
         "Licter is a social data intelligence consultancy: we run the market's platforms without being their publisher, and we pick the tool by the question. If you already have a licence, we can take it over and make it work. A first read takes about ten days, from scoping to readout."),
    ]),
]
