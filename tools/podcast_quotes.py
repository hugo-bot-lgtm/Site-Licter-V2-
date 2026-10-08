"""What the guests of the Audience First podcast actually said (SEO plan,
step 18): verbatim quotes taken from the YouTube transcripts, each linked to
its moment in the video, and the key points of each conversation. Appended to
the matching article by tools/build-blog.py. Nothing here is paraphrased
inside quotation marks; punctuation was added to the automatic captions."""


def q(vid, ts, text):
    m, s = ts.split(":")
    sec = int(m) * 60 + int(s)
    return ('<blockquote class="bl-quote"><p>« %s »</p><cite><a href="https://www.youtube.com/watch?v=%s&amp;t=%ds" target="_blank" rel="noopener">%s dans l\'entretien</a></cite></blockquote>'
            % (text, vid, sec, ts))


def block(title, intro, quotes, points_title, points):
    return ("<h2>%s</h2><p>%s</p>%s<h2>%s</h2><ul>%s</ul>"
            % (title, intro, "".join(quotes), points_title, "".join("<li>%s</li>" % p for p in points)))


V_LVMH, V_MELT, V_TW, V_VB = "CEFJc7tP4hU", "myQGpVHeNFg", "8m0u-E-XMJk", "L385-w4lLzU"

EXTRA = {
    "article-licter-lvmh.html": block(
        "Ce que Clara Mallien nous a dit",
        "Clara Mallien est head of e-réputation et social média chez LVMH : elle porte à la fois la veille de la réputation du groupe et sa stratégie sur les réseaux sociaux. Quelques passages de l'entretien, enregistré à l'été 2024.",
        [q(V_LVMH, "07:19", "Ça peut paraître assez éloigné, mais c'est très lié quand même, puisque tout ce que je peux observer, faire en e-réputation va alimenter ma stratégie de contenu édito sur les réseaux sociaux."),
         q(V_LVMH, "07:55", "Ce qu'on va poster va alimenter ces conversations. Donc en fait c'est un cercle qui peut être soit vertueux, soit vicieux ; on essaie de faire en sorte qu'il soit le plus vertueux possible."),
         q(V_LVMH, "11:55", "LVMH, c'est un peu différent parce que c'est un groupe qui est extrêmement polarisant."),
         q(V_LVMH, "04:08", "On réalise tous nos contenus nous-mêmes, et en un peu plus d'un an et demi, en 2 ans, on a dépassé 600 000 abonnés."),
         q(V_LVMH, "32:12", "On s'est pas contenté de dire « voilà, il faut qu'Antoine Arnault soit sur LinkedIn » et après on voit. En fait, il y a eu un énorme travail qui a été fait en amont pour mapper les territoires de communication sur lesquels on le voyait prendre la parole."),
         q(V_LVMH, "38:49", "Ce que j'attends d'un outil, évidemment c'est la fiabilité des données, mais j'attends aussi d'avoir en face des gens qui sont capables de répondre à mes questions.")],
        "Les points clés",
        ["L'e-réputation et la stratégie social média se nourrissent l'une l'autre : ce que la veille observe oriente les contenus, et les contenus relancent la conversation.",
         "Sur TikTok, le groupe produit lui-même tous ses contenus corporate, pour toucher une jeune génération et soutenir le recrutement ; le compte a dépassé 600 000 abonnés en deux ans environ.",
         "LVMH est un groupe polarisant : sa réputation se joue sur des sujets qui dépassent les produits (la famille Arnault, l'environnement, l'empreinte économique).",
         "La leader advocacy d'Antoine Arnault sur LinkedIn a été préparée en amont, en resserrant ses prises de parole sur trois ou quatre thèmes.",
         "Pour choisir un outil de social listening : des données fiables, un support réactif et une interface compréhensible par des non-spécialistes."]),

    "article-licter-meltwater.html": block(
        "Ce que Nathalie Litvine nous a dit",
        "Nathalie Litvine travaille depuis sept ans chez Meltwater, ex-Linkfluence, où elle accompagne de grands comptes, notamment dans le luxe, sur la plateforme Radarly. Quelques passages de l'entretien.",
        [q(V_MELT, "01:31", "Radarly, c'est notre plateforme. C'est une plateforme en SaaS qui fait de la captation de données sur le Web social, captation de données publiques de façon tout à fait compliant avec les plateformes et avec la législation."),
         q(V_MELT, "09:22", "Pour les grands comptes, en règle générale, on traite un certain nombre de use cases à travers le social listening. Des use cases qu'on va appeler finalement très opérationnels, qui vont être des use cases d'analyse de performance de campagne ou d'événements ou d'influenceur marketing."),
         q(V_MELT, "15:32", "On sait aujourd'hui que la connaissance client et que l'insight client a une valeur incroyable en innovation, en choix de stratégie de marque, en choix de stratégie produit, en push commercial."),
         q(V_MELT, "18:03", "La brand equity, c'est la mesure de tous les éléments qui constituent la valeur immatérielle de la marque, de son rôle dans la société, de son impact sur l'affectif des individus, sur leurs propres convictions."),
         q(V_MELT, "26:30", "C'est génial d'avoir l'intelligence artificielle et en même temps, il faut avoir un cerveau aussi pour ensuite en faire quelque chose."),
         q(V_MELT, "26:50", "C'est une industrie qui sait investir dans le Consumer Insight absolument et qui a besoin du Consumer Insight pour aller plus loin. Donc, ça, oui, c'est un top matching.")],
        "Les points clés",
        ["Les grands comptes utilisent le social listening pour des usages opérationnels (campagnes, événements, influence), pour l'inspiration éditoriale et pour se comparer à leurs concurrents.",
         "L'IA fait ressortir des sujets que personne n'avait cherchés, mais c'est l'humain qui décide quoi en faire.",
         "Comparé aux études et aux brand trackers d'il y a dix ans, le coût du social listening est faible ; sa valeur se mesure à moyen terme.",
         "Une cible luxe qui publie peu reste lisible : on identifie des communautés, puis on suit leurs comportements à des moments clés, pays par pays.",
         "Pour elle, des agences comme Licter sont utiles pour « réconcilier » les données et aller plus loin dans les insights."]),

    "article-licter-talkwalker-podcast.html": block(
        "Ce que Charlotte nous a dit",
        "Charlotte Clemens a rejoint Talkwalker il y a une dizaine d'années, quand c'était une start-up d'une quarantaine de personnes, puis a ouvert le bureau parisien. Quelques passages de l'entretien.",
        [q(V_TW, "01:17", "Le social listening, si on fait une traduction française, c'est un outil de veille, donc un outil de veille du web et des réseaux sociaux. C'est un collecteur de datas en temps réel qui va chercher la data sur les blogs, les forums, les sites d'actualité et les réseaux sociaux."),
         q(V_TW, "08:53", "Pour du consumer insight, du trends, du market research, l'humain aura toujours sa place pour vraiment donner de la perspective à la data."),
         q(V_TW, "10:16", "On est complémentaire. Il y a le spontané, le social listening, c'est quand même de l'opinion spontanée. Je dis ce que je pense. Et après il y a donc le non spontané où vraiment ce sont les instituts d'études."),
         q(V_TW, "06:53", "Peu importe si on est agence ou annonceur, déjà on part du principe que c'est le même usage. Nous on est très focus use case. C'est quoi ton cas d'usage ?"),
         q(V_TW, "16:09", "Vous savez que vous pouvez enlever toute la partie chronophage dans une agence."),
         q(V_TW, "27:18", "Banque, finance, assurances, je trouve qu'ils sont quand même très précis.")],
        "Les points clés",
        ["Talkwalker collecte en temps réel blogs, forums, sites d'actualité et réseaux sociaux, et restitue des tableaux de bord rafraîchis toutes les quinze minutes, ainsi que des alertes.",
         "D'abord vendu aux agences, l'outil s'est ouvert aux marques ; l'enjeu est désormais l'adoption et la formation des équipes.",
         "Le social listening (l'opinion spontanée) et les instituts d'études (l'opinion déclarée) sont complémentaires.",
         "Sans ressources internes, mieux vaut se faire accompagner par une agence plutôt que de rester seul face à l'outil.",
         "Les secteurs les plus avancés : banque, finance, assurance, puis grande consommation, luxe et mode."]),

    "article-licter-visibrain-podcast.html": block(
        "Ce que Jean-Christophe Gatuingt nous a dit",
        "Jean-Christophe Gatuingt est l'un des trois cofondateurs de Visibrain, dont la première version est sortie début 2012. Quelques passages de l'entretien.",
        [q(V_VB, "01:16", "Visibrain, en deux mots, c'est un logiciel SaaS, une plateforme de social listening, de veille des réseaux sociaux."),
         q(V_VB, "01:58", "Il y a tout ce qui est la réputation de la marque, veiller à la réputation de la marque, anticiper les bad buzz, gérer une communication de crise."),
         q(V_VB, "03:52", "Nous, ça a été notre opportunité puisque Twitter, c'était le temps réel. Ça n'existait pas avant."),
         q(V_VB, "10:22", "C'est juste un signal parmi d'autres au service d'une méthodologie plus complète."),
         q(V_VB, "17:41", "On ne se rend pas compte mais aussi sur TikTok, il y a de grandes chances qu'on parle de votre marque, quelle que soit votre marque."),
         q(V_VB, "27:10", "Les réseaux sociaux, c'est le temps réel et c'est réagir vite, que ce soit sur le risque ou les opportunités.")],
        "Les points clés",
        ["Visibrain sert trois usages : la réputation et la gestion de crise, l'influence et les opportunités, la veille stratégique.",
         "La plateforme s'est construite sur le temps réel de Twitter, au moment où les réseaux remplaçaient les blogs.",
         "Les réseaux sociaux sont un signal parmi d'autres, pas un substitut aux instituts de sondage ; le dernier mot revient à l'humain.",
         "Pour choisir un outil : la couverture des plateformes, l'interface (tester plusieurs mois) et l'accompagnement.",
         "Visibrain achète l'accès entreprise aux données de X, ce qui l'a protégé des fermetures d'accès."]),
}


V_LOREAL = "moW2HYtTor8"

# the L'Oréal article, rewritten from the interview itself: the former text
# was generic and credited Licter with work the guest never mentions
PROSE = {
    "article-comment-loreal-utilise-le-social-listening-pour-capter-la-voix-du-consommateur.html": (
        '<p class="bl-dek">« L\'advocacy est en train de dépasser l\'influence » : entretien avec Charles Besson, à la tête du social listening monde chez L\'Oréal.</p>'
        "<p>Charles Besson a lancé le social listening chez Coca-Cola en 2012, avant de rejoindre L'Oréal, un groupe de 90 000 personnes, où il pilote aujourd'hui le social listening à l'échelle mondiale. Dans cet épisode d'Audience First, il raconte comment on installe l'écoute dans une organisation aussi vaste, ce qu'il faut mesurer, et ce que l'IA change au métier.</p>"
        "%(video)s"
        "<h2>Être consumer centric, avant tout</h2>"
        "<p>Pour lui, la raison d'être du social listening chez L'Oréal tient en une idée : comprendre les attentes des consommateurs, assez tôt pour y répondre.</p>"
        + q(V_LOREAL, "06:00", "La motivation de L'Oréal à installer le social listening le plus rapidement possible, c'est qu'on veut être consumer centrique. Donc on veut vraiment se dire qu'on veut comprendre les attentes de la consommatrice et du consommateur pour être sûr qu'on répond à leurs besoins.")
        + "<p>Dans la beauté, le rythme impose cette vigilance : ingrédients, polémiques et tendances circulent vite, et des concurrents peuvent sortir un produit en quelques mois. Il faut donc détecter les tendances tôt.</p>"
        "<h2>Un complément aux études, pas un remplaçant</h2>"
        "<p>À son arrivée, les équipes études étaient réticentes : le social listening n'est pas représentatif, et certains imaginaient qu'il allait remplacer une partie des études. Le déclic est venu du jour où il a été présenté comme un complément.</p>"
        + q(V_LOREAL, "03:40", "À partir du moment où on a réussi à dire : non, ça va venir en plus de ça, ça va venir ajouter des choses qu'on peut pas forcément voir par des études traditionnelles, ou simplement donner un autre angle.")
        + "<h2>Mesurer juste : des KPI harmonisés et un sentiment en trois</h2>"
        "<p>Dans un groupe international, chaque outil arrive avec ses indicateurs maison. Sans harmonisation, impossible de comparer deux pays.</p>"
        + q(V_LOREAL, "08:36", "Pour une société assez internationale par exemple, c'est l'enfer, parce que du coup on se retrouve, si on n'est pas harmonisé, à avoir 50 KPI différents qui veulent plus ou moins dire la même chose mais qui sont pas calculés pareil.")
        + "<p>Même exigence sur le sentiment : il refuse de fondre le neutre dans le positif.</p>"
        + q(V_LOREAL, "12:35", "Ma grosse bataille chez L'Oréal quand je suis arrivé, ça a été de garder le sentiment séparé en trois, c'est-à-dire positif, négatif et neutre, parce que le neutre est pour moi plus intéressant que si on le merge. Si on arrive devant des gens en disant 98 % de sentiment positif, ça ne veut rien dire parce que c'est faux.")
        + "<h2>Parler la langue des consommateurs</h2>"
        "<p>Dans la beauté, les gens citent rarement la marque : il faut trouver les mots qu'ils emploient. Son exemple le plus parlant vient de Chine.</p>"
        + q(V_LOREAL, "27:07", "Un des produits phares chez nous en anti-âge skincare, ça va être Génifique, et ce sérum en Chine va s'appeler la petite bouteille grise ou la petite bouteille bleue. Et c'est clair que si on le sait pas, on a beau faire du listening depuis la France avec un outil, on a rien sur Génifique.")
        + "<p>Même constat pour les tendances : la technique de maquillage du « baking », partie d'Australie, a failli lui échapper faute de connaître le vocabulaire cosmétique de l'époque.</p>"
        "<h2>L'advocacy dépasse l'influence</h2>"
        + q(V_LOREAL, "14:39", "Je pense qu'aujourd'hui l'advocacy est en train de dépasser l'influence.")
        + "<p>Le social listening sert de plus en plus à identifier ces ambassadeurs, et à cartographier des communautés aux centres d'intérêt multiples plutôt que des cibles définies par un seul critère.</p>"
        "<h2>Déployer un outil auprès de milliers de personnes</h2>"
        "<p>L'Oréal a choisi son outil par un appel d'offres en bonne et due forme, avec des tests et un jury d'une dizaine de personnes. Le critère décisif : la simplicité.</p>"
        + q(V_LOREAL, "20:27", "Quand on est 90 000 dans un groupe et qu'on va dire que l'outil va peut-être toucher 2 000 personnes, on peut pas avoir un truc trop trop complexe. Il faut quelque chose qui soit facile d'utilisation, sinon la personne revient pas.")
        + "<p>Pour l'adoption, il mise sur un réseau de champions formés en amont, et sur la démonstration par les cas d'usage.</p>"
        + q(V_LOREAL, "21:28", "Pour moi il faut vraiment réussir à avoir un système de champions, qui est hyper important, où c'est des personnes qui vont vraiment en amont être formées, vont pouvoir découvrir l'outil, pouvoir voir les inconvénients, les avantages.")
        + "<h2>En interne ou avec une agence</h2>"
        "<p>Les rapports courts se font désormais en interne. Les études de fond, longues et complexes, restent confiées à des agences, pour leur expertise et leur regard multi-secteurs.</p>"
        + q(V_LOREAL, "41:02", "Mobiliser quelqu'un sur un deep dive pendant, je sais pas moi, 3 semaines, c'est pas rentable pour nous en fait chez L'Oréal de faire ça. Une agence oui, pas nous.")
        + "<h2>Ce que l'IA change, et ce qu'elle ne change pas</h2>"
        + q(V_LOREAL, "41:57", "Quand j'en faisais, j'avais 2 000 mentions ; sur ces 2 000 mentions je faisais du sampling et j'allais regarder. Aujourd'hui tu as un million de mentions et tu as une IA générative qui en 2 secondes te fait 5 bullet points sur ce qui se dit.")
        + "<p>Mais l'humain reste indispensable. Il en veut pour preuve un outil interne de détection de tendances qu'il a piloté :</p>"
        + q(V_LOREAL, "47:00", "Ce projet d'utiliser massivement du social listening pour détecter et prédire, sans l'humain il pouvait pas fonctionner. Et d'ailleurs c'est l'humain qui a fait qu'il n'a plus fonctionné, parce qu'à partir du moment où des gens ont arrêté de faire la modération de cet outil-là, la machine s'est déréglée.")
        + "<h2>Le métier : un état d'esprit</h2>"
        + q(V_LOREAL, "47:45", "Le social listening, tu as pas besoin d'avoir fait d'études pour ça en fait, particulièrement. C'est juste un état d'esprit : pour moi c'est être curieux, aller chercher des trucs, c'est chercher des indices, avoir envie d'aller faire l'extra mile.")
        + "<p>Il rappelle enfin une limite saine : il n'y a pas de conversation sur tout, et un bon social listener sait aussi dire quand la donnée ne répond pas à la question.</p>"
        "<div class=\"takeaways\"><h3>Ce qu'il faut retenir</h3><ul>"
        "<li>Le social listening complète les études ; il ne les remplace pas.</li>"
        "<li>Dans un groupe international, harmoniser les indicateurs est un préalable.</li>"
        "<li>Garder le sentiment neutre à part rend les résultats plus honnêtes.</li>"
        "<li>Il faut écouter les mots des consommateurs, pas seulement le nom des marques.</li>"
        "<li>L'adoption d'un outil passe par la simplicité, des champions et des cas d'usage.</li>"
        "<li>L'IA résume, mais l'humain reste nécessaire pour lire et décider.</li></ul></div>"),
}
