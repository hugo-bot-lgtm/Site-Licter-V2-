#!/usr/bin/env python3
"""One page per offer: Social Insights, Vigie 360, Social Listening as a
Service and Nox.

    python3 tools/build-offers.py

Writes offer-*.html at the root, in English like the other root pages, with
the shared header and footer taken from offers.html. Their French comes from
js/fr.js at runtime: this script writes its strings into a block of that
file, between the "offer pages" markers, so edit the French here, not there.

The demo mockups of Social Insights, Vigie 360 and SLaaS are taken from the
tabs of offers.html, so the two pages always show the same thing.

tools/build-usecases.py runs this first, so one command rebuilds everything.
"""
import html, importlib.util, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ucb", ROOT / "tools" / "build-usecases.py")
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)
C = U.C

FR, EN = 0, 1
SITE = U.SITE
NEW = {}   # English -> French, for js/fr.js
# every generated block of js/fr.js, and this script's own
BLOCKS = re.compile(r"\n  /\* ---- ([a-z ]+) \(tools/build-[a-z]+\.py\) ---- \*/.*?/\* ---- end \1 ---- \*/\n", re.S)


def block_re(label):
    return re.compile(r"\n  /\* ---- %s \(tools/build-[a-z]+\.py\) ---- \*/.*?/\* ---- end %s ---- \*/\n" % (label, label), re.S)


def base_dict():
    """js/fr.js without any generated block, so a rerun registers its strings
    again instead of finding them already there"""
    import subprocess
    js = BLOCKS.sub("\n", (ROOT / "js" / "fr.js").read_text())
    out = subprocess.run(["node", "-e", "var window={};" + js + ";process.stdout.write(JSON.stringify(window.LicterFR||{}))"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


BASE = base_dict()


def t(pair):
    """the English, escaped for HTML; the French goes to the dictionary"""
    fr, en = pair
    if en not in BASE:
        NEW[en] = U.typo(fr, FR)
    return html.escape(en, quote=False)


def a(pair):
    """the same, for an attribute value"""
    t(pair)
    return html.escape(pair[EN])


# ------------------------------------------------------------------ content
S = {
    "home": ("Accueil", "Home"),
    "offers": ("Offres", "Offers"),
    "book": ("Parler à un consultant", "Talk to a consultant"),
    "incl_link": ("Ce qui est inclus", "What's included"),
    "fit_t": ("Est-ce pour vous ?", "Is it for you?"),
    "fit_yes": ("Pour vous si", "For you if"),
    "fit_no": ("Pas le bon choix si", "Not the right fit if"),
    "incl_t": ("Ce qui est inclus", "What's included"),
    "steps_t": ("Comment ça se passe", "How it runs"),
    "steps_note": ("Durées indicatives, ajustées avec vous au cadrage.", "Indicative timings, adjusted with you at framing."),
    "voice_t": ("Ils en parlent", "They talk about it"),
    "voice_k": ("Dans leurs mots", "In their words"),
    "others_t": ("Les autres offres", "The other offers"),
    "compare": ("Comparer les offres", "Compare the offers"),
    "faq": ("Questions fréquentes", "Frequently asked questions"),
    "illus": ("Exemple illustratif", "Illustrative example"),
    "crumbs": ("Fil d'Ariane", "Breadcrumb"),
    "contact": ("E-mail ou téléphone", "Email or phone"),
    "call": ("Rappelez-moi", "Call me back"),
}

OFFERS = [
    {
        "key": "social-insights", "file": "offer-social-insights.html", "voice": "dassault", "n": 1,
        "name": ("Social Insights", "Social Insights"),
        "short": ("Des études à la demande, lues par des experts.", "Studies on demand, read by experts."),
        "seo_title": ("Social Insights : études social data à la demande | Licter",
                      "Social Insights: social data studies on demand | Licter"),
        "seo_desc": ("Des études social data à la demande, cadrées par un consultant et présentées à ceux qui décident.",
                     "Social data studies on demand, framed by a consultant and presented to the people who decide."),
        "h1": ("Vos analyses de données sociales méritent des experts.", "Your social data analyses deserve experts."),
        "lead": ("Nos consultants cadrent la question, configurent la collecte et produisent l'analyse. Vous obtenez la réponse, pas une licence d'outil et un plan de formation.",
                 "Our consultants frame the question, configure the collection and produce the analysis. You get the answer, not a tool licence and a training plan."),
        "yes": [("Vous avez des questions récurrentes : campagnes, concurrents, audiences, chaque mois.",
                 "You have recurring questions: campaigns, competitors, audiences, every month."),
                ("Personne dans l'équipe n'a le temps, ni la formation, de faire tourner une plateforme d'écoute.",
                 "Nobody in the team has the time, or the training, to run a listening platform."),
                ("Vous avez besoin de réponses présentées à ceux qui décident, pas d'exports.",
                 "You need answers presented to the people who decide, not exports.")],
        "no": [("Vous devez être alerté dès que quelque chose casse : c'est Vigie 360.",
                "You need an alert the moment something breaks: that is Vigie 360."),
               ("Vous payez déjà une plateforme et voulez qu'elle serve : c'est Social Listening as a Service.",
                "You already pay for a platform and want it used: that is Social Listening as a Service.")],
        "incl": [(("Des études à la demande", "Studies on demand"),
                  ("Lectures de campagne, benchmarks concurrents, études d'audience, veilles de tendances : selon les questions du trimestre.",
                   "Campaign reads, competitor benchmarks, audience studies, trend scans: driven by the questions of the quarter.")),
                 (("Un consultant dédié", "A dedicated consultant"),
                  ("La même personne cadre chaque question avec vous, et connaît votre marque, votre marché et votre historique.",
                   "The same person frames every question with you, and knows your brand, your market and your history.")),
                 (("Quatre couches de signal", "Four layers of signal"),
                  ("Ce que les gens publient, qui ils sont, ce qu'ils font et ce qu'ils recherchent, choisies question par question.",
                   "What people post, who they are, what they do and what they search for, chosen question by question.")),
                 (("Une restitution, pas un deck", "A readout, not a deck"),
                  ("Chaque étude se termine par une recommandation présentée à ceux qui décident.",
                   "Each study ends with a recommendation presented to the people who decide.")),
                 (("Une note mensuelle", "A monthly note"),
                  ("Ce qui a bougé sur votre marché dans le mois, en une page, pour le comité de direction.",
                   "What moved in your market this month, on one page, for the executive team."))],
        "steps": [(("Semaine 1", "Week 1"), ("Cadrage", "Framing"),
                   ("Nous listons avec vous les questions du trimestre, classées selon la décision qu'elles nourrissent.",
                    "We list the questions of the quarter with you, ranked by the decision each one feeds.")),
                  (("En continu", "Ongoing"), ("Études", "Studies"),
                   ("Chaque question devient une étude, livrée en une dizaine de jours.",
                    "Each question becomes a study, delivered in about ten days.")),
                  (("À chaque étude", "Each study"), ("Restitution", "Readout"),
                   ("Un consultant présente la réponse, et ce qu'il faut en faire.",
                    "A consultant presents the answer, and what to do with it.")),
                  (("Chaque mois", "Each month"), ("Note mensuelle", "Monthly note"),
                   ("Une page sur ce qui a bougé, pour le comité de direction.",
                    "One page on what moved, for the executive team."))],
        "faq": [(("Combien d'études pouvons-nous demander ?", "How many studies can we ask for?"),
                 ("Cela dépend du périmètre défini avec vous. Nous planifions le trimestre ensemble pour traiter d'abord les questions les plus utiles.",
                  "It depends on the perimeter set with you. We plan the quarter together so the most useful questions come first.")),
                (("En combien de temps une étude est-elle livrée ?", "How fast is a study delivered?"),
                 ("Une dizaine de jours pour une première lecture, du cadrage à la restitution. Une vérification rapide sur un sujet en cours peut revenir dans la semaine.",
                  "About ten days for a first read, from framing to readout. A quick check on a running topic can come back within the week.")),
                (("Faut-il avoir notre propre plateforme ?", "Do we need our own platform?"),
                 ("Non. Nous apportons les licences et les sources, et choisissons la bonne plateforme pour chaque question.",
                  "No. We bring the licences and the sources, and pick the right platform for each question."))],
        "book_t": ("Quelle serait votre première question ?", "What would you ask first?"),
    },
    {
        "key": "vigie", "file": "offer-vigie-360.html", "voice": "axa", "n": 2,
        "name": ("Vigie 360", "Vigie 360"),
        "short": ("Alerté en 15 minutes, 24 h/24.", "Alerted in 15 minutes, 24/7."),
        "seo_title": ("Vigie 360 : veille réseaux sociaux et gestion de crise, 24/7 | Licter",
                      "Vigie 360: 24/7 monitoring, alerts within 15 minutes | Licter"),
        "seo_desc": ("Veille des réseaux sociaux et de la presse, 24 h/24, pour anticiper et gérer les crises : votre marque, vos dirigeants et vos marchés, lus par un analyste.",
                     "Continuous monitoring of your brand, your executives and your markets in over twenty languages, read by an analyst before it alerts you."),
        "h1": ("Nous vous alertons en 15 minutes, 24 h/24.", "We alert you in 15 minutes, 24/7."),
        "lead": ("Une veille des réseaux sociaux et de la presse sur votre marque, vos dirigeants et vos marchés, dans plus de vingt langues, pour prévenir et gérer les crises. Une personne lit le signal avant qu'il ne vous parvienne : une alerte veut dire qu'il s'est passé quelque chose, pas qu'un mot-clé s'est déclenché.",
                 "Social media and press monitoring of your brand, your executives and your markets, in more than twenty languages, to prevent and manage crises. A person reads the signal before it reaches you, so an alert means something happened, not that a keyword fired."),
        "yes": [("Votre marque, vos dirigeants ou vos produits sont exposés à des sujets qui vont vite.",
                 "Your brand, your executives or your products are exposed to fast-moving subjects."),
                ("Vous avez déjà appris une crise par la presse, ou par votre PDG.",
                 "You have already learnt about a crisis from the press, or from your CEO."),
                ("Vous opérez dans plusieurs pays et plusieurs langues.",
                 "You operate in several countries and languages.")],
        "no": [("Vous avez besoin d'une étude pour décider, pas d'une alerte : c'est Social Insights.",
                "You need a study to decide, not an alert: that is Social Insights."),
               ("Vous voulez suivre la conversation à votre rythme : c'est Nox.",
                "You want to follow the conversation at your own pace: that is Nox.")],
        "incl": [(("Un périmètre sur mesure", "A tailored perimeter"),
                  ("Marque, dirigeants, produits, concurrents et sujets sensibles, fixés avec vous et revus chaque trimestre.",
                   "Brand, executives, products, competitors and sensitive topics, set with you and reviewed every quarter.")),
                 (("Des alertes lues par un analyste", "Alerts read by an analyst"),
                  ("Chaque signal est qualifié avant de vous parvenir : son niveau, sa portée, et ce qu'il faut faire.",
                   "Every signal is qualified before it reaches you: its level, its reach, and what to do.")),
                 (("Trois niveaux d'alerte", "Three alert levels"),
                  ("Du signal à surveiller à la crise en cours, chacun avec son canal et son délai.",
                   "From a signal to watch to a crisis in progress, each with its own channel and delay.")),
                 (("Un suivi de crise", "Crisis follow-up"),
                  ("Quand le sujet monte, un point quotidien sur l'évolution de la conversation, jusqu'à ce qu'elle retombe.",
                   "When it escalates, a daily update on how the conversation evolves, until it settles.")),
                 (("Une revue mensuelle", "A monthly review"),
                  ("Ce qui a été signalé, ce qui ne l'a pas été et pourquoi, et le périmètre ajusté en conséquence.",
                   "What was flagged, what was not and why, and the perimeter adjusted accordingly."))],
        "steps": [(("Semaine 1", "Week 1"), ("Périmètre", "Perimeter"),
                   ("Nous définissons ce qu'il faut surveiller, qui alerter et par quel canal.",
                    "We set what to watch, who to alert and through which channel.")),
                  (("Semaine 2", "Week 2"), ("Calibrage", "Calibration"),
                   ("Des alertes de test pour régler les seuils avec vous.",
                    "Test alerts to set the thresholds with you.")),
                  (("Ensuite, 24/7", "Then, 24/7"), ("Veille", "Monitoring"),
                   ("Les analystes lisent le signal jour et nuit, et vous alertent en 15 minutes.",
                    "Analysts read the signal day and night, and alert you within 15 minutes.")),
                  (("Chaque mois", "Each month"), ("Revue", "Review"),
                   ("Ce qui s'est passé, ce qui a été signalé, et ce qui change.",
                    "What happened, what was flagged, and what changes."))],
        "faq": [(("Qu'est-ce qui déclenche une alerte ?", "What triggers an alert?"),
                 ("Pas un mot-clé. Un analyste lit le signal et vous alerte quand il s'est passé quelque chose : une histoire qui se propage, une voix qui porte, un changement de ton. Le bruit est filtré avant de vous parvenir.",
                  "Not a keyword. An analyst reads the signal and alerts you when something happened: a story spreading, a voice that carries, a change of tone. The noise is filtered before it reaches you.")),
                (("Comment les alertes sont-elles envoyées ?", "How are alerts sent?"),
                 ("Par e-mail, SMS ou messagerie, selon le niveau. Une alerte de crise s'accompagne aussi d'un appel.",
                  "By email, text or messaging, depending on the level. A crisis-level alert also comes with a phone call.")),
                (("Quelles langues couvrez-vous ?", "Which languages do you cover?"),
                 ("Plus de vingt, dont l'anglais, l'espagnol, le chinois, l'arabe et l'hindi.",
                  "More than twenty, including English, Spanish, Chinese, Arabic and Hindi.")),
                (("Vigie 360 peut-elle couvrir nos dirigeants ?", "Can Vigie 360 cover our executives?"),
                 ("Oui. Les dirigeants sont souvent les premiers exposés ; nous suivons leurs mentions avec les mêmes niveaux d'alerte que la marque.",
                  "Yes. Executives are often the first exposed; we follow their mentions with the same alert levels as the brand."))],
        "book_t": ("Que devrions-nous surveiller pour vous ?", "What should we be watching for you?"),
    },
    {
        "key": "slaas", "file": "offer-slaas.html", "voice": "sncf", "n": 3,
        "name": ("Social Listening as a Service", "Social Listening as a Service"),
        "short": ("Votre plateforme, enfin utilisée.", "Your platform, finally used."),
        "seo_title": ("Social Listening as a Service : faire servir votre plateforme | Licter",
                      "Social Listening as a Service: make your platform useful | Licter"),
        "seo_desc": ("Vous payez une plateforme d'écoute sous-utilisée : nous reprenons la taxonomie, les tableaux de bord et les analyses, et formons vos équipes.",
                     "You pay for an under-used listening platform: we take over the taxonomy, the dashboards and the analyses, and train your teams."),
        "h1": ("Nous augmentons l'adoption et l'impact de votre social listening.", "We increase the adoption and impact of your social listening."),
        "lead": ("Vous possédez déjà une plateforme et elle est sous-utilisée. Nous reprenons la taxonomie, les tableaux de bord et les analyses récurrentes, et formons vos équipes à les lire, pour que la licence que vous payez produise des décisions.",
                 "You already own a platform and it is under-used. We take over the taxonomy, the dashboards and the recurring analyses, and train your teams to read them, so the licence you pay for produces decisions."),
        "yes": [("Vous payez une plateforme d'écoute que peu de gens ouvrent.",
                 "You pay for a listening platform that few people open."),
                ("Vos tableaux de bord ont été configurés une fois, et jamais revus.",
                 "Your dashboards were set up once and never revisited."),
                ("Vos équipes reçoivent des exports, mais pas de conclusions.",
                 "Your teams receive exports, but no conclusions.")],
        "no": [("Vous n'avez pas de plateforme et ne voulez pas en avoir : c'est Social Insights.",
                "You have no platform and do not want one: that is Social Insights."),
               ("Vous avez besoin d'alertes jour et nuit : c'est Vigie 360.",
                "You need alerts day and night: that is Vigie 360.")],
        "incl": [(("Un audit de votre configuration", "An audit of your setup"),
                  ("Requêtes, taxonomie, tableaux de bord et usages, revus au regard des questions que vos équipes se posent vraiment.",
                   "Queries, taxonomy, dashboards and usage, reviewed against the questions your teams actually ask.")),
                 (("Une taxonomie refaite", "A rebuilt taxonomy"),
                  ("Sujets, marques et produits classés comme votre entreprise en parle.",
                   "Topics, brands and products tagged the way your business talks about them.")),
                 (("Des tableaux de bord utilisés", "Dashboards people use"),
                  ("Moins nombreux, chacun construit pour une équipe et une décision.",
                   "Fewer of them, each built for one team and one decision.")),
                 (("Des analyses récurrentes", "Recurring analyses"),
                  ("Les lectures hebdomadaires et mensuelles produites par nos analystes, dans votre plateforme.",
                   "The weekly and monthly reads produced by our analysts, inside your platform.")),
                 (("La formation des équipes", "Team training"),
                  ("Des sessions courtes, par rôle, pour que chaque équipe lise ses propres données.",
                   "Short sessions, by role, so each team reads its own data."))],
        "steps": [(("Semaines 1 et 2", "Weeks 1 and 2"), ("Audit", "Audit"),
                   ("Nous passons en revue la configuration et la confrontons à vos questions.",
                    "We review the setup and test it against your questions.")),
                  (("Semaines 3 à 6", "Weeks 3 to 6"), ("Reconstruction", "Rebuild"),
                   ("Taxonomie et tableaux de bord repris, une équipe après l'autre.",
                    "Taxonomy and dashboards reworked, one team at a time.")),
                  (("Dès le mois 2", "From month 2"), ("Livraison", "Delivery"),
                   ("Les analyses récurrentes arrivent dans votre plateforme.",
                    "Recurring analyses delivered inside your platform.")),
                  (("Chaque trimestre", "Each quarter"), ("Revue", "Review"),
                   ("L'usage est mesuré, et la configuration ajustée.",
                    "Usage is measured, and the setup adjusted."))],
        "faq": [(("Avec quelles plateformes travaillez-vous ?", "Which platforms do you work with?"),
                 ("Talkwalker, Visibrain, YouScan et SoPrism au quotidien, et la plupart des autres plateformes d'écoute du marché.",
                  "Talkwalker, Visibrain, YouScan and SoPrism every day, and most other listening platforms on the market.")),
                (("Gardons-nous notre licence ?", "Do we keep our licence?"),
                 ("Oui. La licence reste la vôtre ; nous la faisons produire des décisions. Si l'audit montre qu'elle ne correspond pas à vos besoins, nous vous le disons.",
                  "Yes. The licence stays yours; we make it produce decisions. If the audit shows it does not fit your needs, we tell you.")),
                (("Combien de temps avant que les équipes s'en servent ?", "How long before teams use it?"),
                 ("En général dans le premier trimestre : l'audit et la reconstruction prennent environ six semaines, puis l'usage est mesuré chaque mois.",
                  "Usually within the first quarter: the audit and rebuild take about six weeks, then usage is measured every month.")),
                (("Formez-vous nos équipes ?", "Do you train our teams?"),
                 ("Oui. La formation fait partie de l'offre, par rôle et sur vos propres données, pas sur un compte de démonstration.",
                  "Yes. Training is part of the offer, by role and on your own data, not on a demo account."))],
        "book_t": ("Pour quelle plateforme payez-vous ?", "Which platform are you paying for?"),
    },
    {
        # MOCK: Nox's copy describes the tool from a one-line brief ("an
        # AI-assisted monitoring tool"); features and FAQ to be validated.
        "key": "nox", "file": "offer-nox.html", "voice": "orange", "n": 4,
        "name": ("Nox", "Nox"),
        "short": ("La veille assistée par l'IA.", "AI-assisted monitoring."),
        "seo_title": ("Nox : l'outil de veille assisté par l'IA | Licter",
                      "Nox: the AI-assisted monitoring tool | Licter"),
        "seo_desc": ("Nox lit la conversation sur votre marque en continu, la regroupe par sujets, résume ce qui a changé et signale ce qui sort de l'ordinaire.",
                     "Nox reads the conversation about your brand continuously, groups it into topics, summarises what changed and flags what looks unusual."),
        "h1": ("Votre veille, triée par l'IA, vérifiée par un analyste.", "Your monitoring, sorted by AI, checked by an analyst."),
        "lead": ("Nox est notre outil de veille assisté par l'IA. Il lit en continu la conversation sur votre marque, la regroupe par sujets, résume ce qui a changé et signale ce qui sort de l'ordinaire. Nos analystes le règlent avec vous, pour que ce qu'il fait remonter mérite votre temps.",
                 "Nox is our AI-assisted monitoring tool. It reads the conversation about your brand continuously, groups it into topics, summarises what changed and flags what looks unusual. Our analysts tune it with you, so what it surfaces is worth your time."),
        "yes": [("Vous voulez suivre votre marque au jour le jour, sans lire chaque publication.",
                 "You want to follow your brand day to day, without reading every post."),
                ("Votre équipe a besoin d'une vue partagée de ce qui se dit, au même endroit.",
                 "Your team needs a shared view of what is being said, in one place."),
                ("Vous voulez que l'IA fasse le tri, et que des gens de confiance le vérifient.",
                 "You want AI to do the sorting, and people you trust to check it.")],
        "no": [("Vous avez besoin d'une étude complète avec une recommandation : c'est Social Insights.",
                "You need a full study with a recommendation: that is Social Insights."),
               ("Vous avez besoin qu'une personne vous appelle quand une crise démarre : c'est Vigie 360.",
                "You need a person to call you when a crisis starts: that is Vigie 360.")],
        "incl": [(("Des sujets regroupés", "Topics, not mentions"),
                  ("Les publications sont regroupées par sujet automatiquement : vous voyez de quoi on parle, pas une liste de mentions.",
                   "Posts are grouped into topics automatically: you see what is being discussed, not a list of mentions.")),
                 (("Un brief chaque matin", "A brief every morning"),
                  ("Ce qui a changé en quelques lignes, avec les publications derrière chaque point.",
                   "What changed in a few lines, with the posts behind each point.")),
                 (("L'inhabituel signalé", "The unusual, flagged"),
                  ("Un sujet qui grossit plus vite que d'habitude, une nouvelle voix, un changement de ton : Nox le pointe.",
                   "A topic growing faster than usual, a new voice, a change of tone: Nox points it out.")),
                 (("Configuré par nos analystes", "Set up by our analysts"),
                  ("Nous fixons le périmètre, vérifions les sujets et corrigeons le modèle avec vous, pour tenir le bruit à l'écart.",
                   "We set the perimeter, check the topics and correct the model with you, to keep the noise out.")),
                 (("Un analyste en relais", "An analyst to hand over to"),
                  ("Quand Nox signale un sujet que vous voulez faire lire pour de bon, un analyste le reprend.",
                   "When Nox flags something you want properly read, an analyst picks it up."))],
        "steps": [(("Semaine 1", "Week 1"), ("Configuration", "Setup"),
                   ("Nous fixons le périmètre avec vous : marques, sujets, sources et langues.",
                    "We set the perimeter with you: brands, topics, sources and languages.")),
                  (("Semaine 2", "Week 2"), ("Réglage", "Tuning"),
                   ("Nos analystes vérifient ce que Nox regroupe et signale, et le corrigent.",
                    "Our analysts check what Nox groups and flags, and correct it.")),
                  (("Chaque jour", "Every day"), ("Brief", "Brief"),
                   ("Votre équipe reçoit le brief et explore les sujets dans Nox.",
                    "Your team receives the brief and explores the topics in Nox.")),
                  (("Chaque mois", "Each month"), ("Revue", "Review"),
                   ("Nous revoyons ce qui a été signalé, et ajustons le périmètre.",
                    "We review what was flagged, and adjust the perimeter."))],
        "faq": [(("Que fait l'IA, et que font les analystes ?", "What does the AI do, and what do people do?"),
                 ("L'IA lit, regroupe et résume à un volume qu'aucune équipe ne pourrait suivre. Nos analystes la configurent, vérifient ce qu'elle produit, la corrigent, et lisent tout ce qui demande du jugement.",
                  "The AI reads, groups and summarises at a volume no team could follow. Our analysts set it up, check what it produces, correct it, and read anything that needs judgement.")),
                (("Quelles sources Nox lit-il ?", "Which sources does Nox read?"),
                 ("Les réseaux sociaux, la presse, les forums et les avis de votre périmètre, définis avec vous au démarrage.",
                  "The social networks, news, forums and reviews in your perimeter, set with you at the start.")),
                (("Quelle différence avec Vigie 360 ?", "How is Nox different from Vigie 360?"),
                 ("Nox donne à votre équipe une vue quotidienne à explorer à son rythme. Vigie 360 est un service : des analystes veillent pour vous jour et nuit, et vous appellent en 15 minutes quand il se passe quelque chose.",
                  "Nox gives your team a daily view to explore at its own pace. Vigie 360 is a service: analysts watch for you day and night, and call you within 15 minutes when something happens.")),
                (("Peut-on combiner Nox avec une autre offre ?", "Can Nox be combined with another offer?"),
                 ("Oui. Nox sert au suivi quotidien, et Social Insights prend le relais pour les questions qui demandent une étude complète.",
                  "Yes. Nox covers the day-to-day, and Social Insights takes over for the questions that need a full study."))],
        "book_t": ("Envie de voir ce que Nox ferait remonter pour vous ?", "Want to see what Nox would surface for you?"),
    },
]

# the Nox brief, as a mockup (the other three come from offers.html)
NOX_DEMO = [
    ("Le brief du matin de Nox", "A Nox morning brief"),
    ("Nox · brief du matin", "Nox · morning brief"),
    ("Aujourd'hui en trois lignes", "Today in three lines"),
    [("On parle deux fois plus de la nouvelle gamme, portée par deux créateurs culinaires.",
      "Talk about the new range has doubled, driven by two cooking creators."),
     ("Les retards de livraison reviennent dans les avis, surtout en Espagne.",
      "Delivery delays are back in reviews, mostly in Spain."),
     ("La baisse de prix d'un concurrent circule beaucoup ; peu de comparaisons avec vous pour l'instant.",
      "A competitor's price cut is widely shared; few comparisons with you so far.")],
    ("Sujets", "Topics"),
    [("", ("Nouvelle gamme", "New range"), ("1 284 posts", "1,284 posts"), ("up", ("+112 %", "+112%"))),
     ("flag", ("Retards de livraison", "Delivery delays"), ("356 posts", "356 posts"), ("up", ("+48 %", "+48%"))),
     ("", ("Baisse de prix concurrente", "Competitor price cut"), ("902 posts", "902 posts"), ("new", ("Nouveau", "New"))),
     ("", ("Service client", "Customer service"), ("211 posts", "211 posts"), ("down", ("−9 %", "−9%")))],
    ("Inhabituel", "Unusual"),
    ("Signalé par Nox · vérifié par un analyste", "Flagged by Nox · checked by an analyst"),
]

# offers.html: the new strings around the fourth offer
OFFERS_PAGE = {
    "lead": ("Quatre façons de travailler avec nous, de l'étude à la demande à l'outil de veille assisté par l'IA. Nos consultants cadrent, collectent et lisent. Vous obtenez la décision, pas une plateforme à faire tourner.",
             "Four ways to work with us, from a study on demand to an AI-assisted monitoring tool. Our consultants frame, collect and read. You get the decision, not a platform to staff."),
    "title": ("Quatre offres. Voyez ce que chacune livre.", "Four offers. See what each one delivers."),
    "tablist": ("Les quatre offres", "The four offers"),
    "nox_tab": ("La veille, triée par l'IA.", "Monitoring, sorted by AI."),
    "nox_for": ("Les équipes qui veulent suivre leur marque au quotidien", "Teams who want to follow their brand day to day"),
    "nox_model": ("Abonnement · configuré et réglé par nos analystes", "Subscription · set up and tuned by our analysts"),
    "for": ("Pour", "For"),
    "model": ("Modèle", "Model"),
    "which_nox": ("Vous voulez suivre votre marque chaque jour, et que l'IA fasse le tri.",
                  "You want to follow your brand every day, with AI doing the sorting."),
    "footer_nox": ("Nox, la veille assistée par l'IA", "Nox, AI-assisted monitoring"),
    "menu_label": ("QUATRE FAÇONS DE TRAVAILLER AVEC NOUS", "FOUR WAYS TO WORK WITH US"),
    "menu_nox": ("La veille assistée par l'IA, réglée par nos analystes.", "AI-assisted monitoring, tuned by our analysts."),
}
for k, v in [("more_si", ("Tout sur Social Insights", "Everything about Social Insights")),
             ("more_vigie", ("Tout sur Vigie 360", "Everything about Vigie 360")),
             ("more_slaas", ("Tout sur Social Listening as a Service", "Everything about Social Listening as a Service")),
             ("more_nox", ("Tout sur Nox", "Everything about Nox"))]:
    OFFERS_PAGE[k] = v


# ------------------------------------------------------------------ additions
# French twins of the offer pages (static, with hreflang)
FR_PATH = {"offers.html": "/fr/offres/", "offer-social-insights.html": "/fr/offres/social-insights/",
           "offer-vigie-360.html": "/fr/offres/vigie-360/", "offer-slaas.html": "/fr/offres/social-listening-as-a-service/",
           "offer-nox.html": "/fr/offres/nox/"}
HUB_SEO = {"title": ("Nos offres : études, veille 24/7, outil IA | Licter", "Our offers: studies, 24/7 monitoring, an AI tool | Licter"),
           "desc": ("Quatre façons de travailler avec Licter : études social data à la demande, veille et alertes 24/7, reprise de votre plateforme, outil de veille assisté par l'IA.",
                    "Four ways to work with Licter: social data studies on demand, 24/7 monitoring and alerts, a takeover of your platform, an AI-assisted monitoring tool.")}
# Per offer: the magnet, the deliverable shown, and two buying questions.
# MOCK: the buying answers (start, ownership) are to be validated by Licter.
MORE = {
    "social-insights": {
        "magnet": ("Recevez un exemple d'étude Social Insights, dans votre secteur.", "Get a sample Social Insights study, in your sector."),
        "dlv": "segmentation",
        "faq": [(("Comment démarre-t-on ?", "How do we start?"),
                 ("Par un échange de cadrage, puis la liste des questions du trimestre, classées avec vous la première semaine.",
                  "With a framing call, then the list of the quarter's questions, ranked with you in the first week."))],
    },
    "vigie": {
        "magnet": ("Recevez un exemple d'alerte et de revue mensuelle Vigie 360.", "Get a sample Vigie 360 alert and monthly review."),
        "dlv": "brand-risk",
        "faq": [(("En combien de temps êtes-vous opérationnels ?", "How fast are you up and running?"),
                 ("Le périmètre et les contacts d'alerte sont fixés la première semaine, les seuils réglés avec des alertes de test la deuxième.",
                  "The perimeter and alert contacts are set in the first week, the thresholds tuned with test alerts in the second."))],
    },
    "slaas": {
        "magnet": ("Recevez un exemple de reporting repris, dans votre secteur.", "Get a sample reworked reporting, in your sector."),
        "dlv": "campaign-impact",
        "faq": [(("Comment démarre-t-on ?", "How do we start?"),
                 ("Par un audit de deux semaines de votre configuration actuelle, confrontée à vos questions.",
                  "With a two-week audit of your current setup, tested against your questions."))],
    },
    "nox": {
        "magnet": ("Recevez un exemple de brief Nox, dans votre secteur.", "Get a sample Nox brief, in your sector."),
        "dlv": "reputation",
        "faq": [(("Comment démarre-t-on ?", "How do we start?"),
                 ("Le périmètre est configuré la première semaine, puis réglé par nos analystes la deuxième.",
                  "The perimeter is set up in the first week, then tuned by our analysts in the second."))],
    },
}
OWN = (("À qui appartiennent les livrables ?", "Who owns the deliverables?"),
       ("À vous. Les études, rapports et tableaux produits pour vous restent les vôtres, y compris si vous arrêtez. Nous travaillons sur des données publiques, agrégées, dans le respect du RGPD.",
        "You do. The studies, reports and dashboards produced for you stay yours, including if you stop. We work on public, aggregated data, in line with GDPR."))
# prices are given on quote only (no public price list)
def price_q(o):
    return (("Combien coûte %s ?" % o["name"][0], "How much does %s cost?" % o["name"][1]),
            ("Le prix est établi sur devis. Il dépend des marchés, des langues et des sujets à couvrir, et de la durée. Un consultant vous le prépare après un premier échange.",
             "The price is set on quote. It depends on the markets, languages and topics to cover, and on the duration. A consultant prepares it after a first conversation."))
for _o in OFFERS:
    _o["faq"] = _o["faq"] + MORE[_o["key"]]["faq"] + [price_q(_o), OWN]

# The comparison: every value comes from the offer pages themselves.
COMPARE_ROWS = [
    (("Ce que vous recevez", "What you receive"),
     [("Des études à la demande, une note mensuelle", "Studies on demand, a monthly note"),
      ("Des alertes en 15 minutes, une revue mensuelle", "Alerts within 15 minutes, a monthly review"),
      ("Votre plateforme reprise, des analyses récurrentes", "Your platform reworked, recurring analyses"),
      ("Un brief quotidien, des sujets triés par l'IA", "A daily brief, topics sorted by AI")]),
    (("Pour qui", "For whom"),
     [("Des questions récurrentes, personne pour faire tourner un outil", "Recurring questions, nobody to run a tool"),
      ("Une marque ou des dirigeants exposés", "An exposed brand or executives"),
      ("Une plateforme payée, peu utilisée", "A platform paid for, little used"),
      ("Suivre sa marque au quotidien", "Following your brand day to day")]),
    (("Rythme", "Pace"),
     [("Une étude en une dizaine de jours", "A study in about ten days"),
      ("24 h/24, alerte en 15 minutes", "24/7, alert within 15 minutes"),
      ("Analyses dès le mois 2, revue trimestrielle", "Analyses from month 2, quarterly review"),
      ("Un brief chaque jour", "A brief every day")]),
    (("Démarrage", "Start"),
     [("Cadrage la première semaine", "Framing in week 1"),
      ("Opérationnel en deux semaines", "Running within two weeks"),
      ("Audit en deux semaines, reprise en six", "Audit in two weeks, rework in six"),
      ("Réglé en deux semaines", "Tuned within two weeks")]),
    (("Qui lit", "Who reads"),
     [("Un consultant dédié", "A dedicated consultant"),
      ("Des analystes, jour et nuit", "Analysts, day and night"),
      ("Vos équipes, formées par nous", "Your teams, trained by us"),
      ("L'IA trie, un analyste vérifie", "AI sorts, an analyst checks")]),
    (("Modèle", "Model"),
     [("Études à la demande, tarif selon le périmètre", "Studies on demand, priced to the scope"),
      ("Abonnement de veille", "Monitoring subscription"),
      ("Accompagnement sur votre plateforme", "Support on your own platform"),
      ("Abonnement, réglé par nos analystes", "Subscription, tuned by our analysts")]),
]
HUB_FAQ = [
    (("Quelle offre choisir ?", "Which offer should we pick?"),
     ("Celle qui répond à votre situation : des questions ponctuelles, une veille permanente, une plateforme à faire servir, ou un suivi quotidien. Le premier échange sert justement à le décider.",
      "The one that fits your situation: questions as they come, permanent monitoring, a platform to put to use, or day-to-day tracking. The first conversation is there to decide it.")),
    (("Peut-on combiner plusieurs offres ?", "Can we combine several offers?"),
     ("Oui. Une veille au quotidien avec Vigie 360 ou Nox, et des études Social Insights quand une question se pose, par exemple.",
      "Yes. Day-to-day monitoring with Vigie 360 or Nox, and Social Insights studies when a question comes up, for example.")),
    (("Combien ça coûte ?", "How much does it cost?"),
     ("Chaque offre est établie sur devis, selon le périmètre : marchés, langues, sujets et durée. Un consultant vous le prépare après un premier échange.",
      "Each offer is priced on quote, by perimeter: markets, languages, topics and duration. A consultant prepares it after a first conversation.")),
    (("Faut-il avoir une plateforme d'écoute ?", "Do we need a listening platform?"),
     ("Non. Nous apportons les licences et les sources. Social Listening as a Service est justement pour ceux qui en ont déjà une.",
      "No. We bring the licences and the sources. Social Listening as a Service is precisely for those who already have one.")),
]
S.update({
    "price_row": ("Tarif", "Price"),
    "price_cell": ("Sur devis", "On quote"),
    "price_link": ("Demander un devis", "Ask for a quote"),
    "hub_magnet_k": ("Avant d'en parler", "Before we talk"),
    "hub_magnet_t": ("Demandez un devis pour votre périmètre.", "Ask for a quote for your perimeter."),
    "hub_magnet_d": ("Un consultant revient vers vous sous 48 h pour cadrer le périmètre et vous envoyer un devis, sans relance commerciale.",
                     "A consultant gets back to you within 48 hours to frame the perimeter and send you a quote, with no sales follow-up."),
    "hub_magnet_btn": ("Demander un devis", "Ask for a quote"),
    "magnet_k": ("Et chez vous ?", "And for you?"),
    "magnet_d": ("Anonymisé, envoyé par un consultant sous 48 h : ce que vous recevriez vraiment.", "Anonymised, sent by a consultant within 48 hours: what you would actually receive."),
    "magnet_btn": ("Recevoir l'exemple", "Get the sample"),
    "magnet_email": ("E-mail professionnel", "Work email"),
    "magnet_sector": ("Votre secteur", "Your sector"),
    "magnet_pick": ("Choisir…", "Choose…"),
    "magnet_err": ("Indiquez un e-mail professionnel valide.", "Enter a valid work email."),
    "magnet_pick_err": ("Choisissez votre secteur.", "Choose your sector."),
    "magnet_consent": ("Votre e-mail sert uniquement à vous répondre.", "We use your email only to reply to you."),
    "privacy": ("Politique de confidentialité", "Privacy policy"),
    "magnet_done": ("C'est noté. Un consultant vous envoie un exemple sous 48 h.", "Noted. A consultant sends you a sample within 48 hours."),
    "hub_magnet_done": ("C'est noté. Un consultant revient vers vous sous 48 h.", "Noted. A consultant gets back to you within 48 hours."),
    "magnet_alt": ("Plutôt comparer d'abord ?", "Rather compare first?"),
    "magnet_alt_link": ("Les quatre offres côte à côte", "The four offers side by side"),
    "dlv_t": ("Ce que vous recevez", "What you receive"),
    "dlv_link": ("Voir le cas d'usage", "See the use case"),
    "get_lead": ("Le détail de l'offre, et un exemple de livrable tel qu'il arrive chez vous.",
                 "The detail of the offer, and a sample deliverable as it reaches you."),
    "bar_offer": ("Recevoir un exemple", "Get a sample"),
    "bar_price": ("Demander un devis", "Ask for a quote"),
    "bar_call": ("Parler à un consultant", "Talk to a consultant"),
    "bar_chat": ("Discuter avec Antoine", "Chat with Antoine"),
    "diag3": ("Le diagnostic en 3 minutes", "The 3-minute diagnostic"),
    "home": ("Accueil", "Home"),
})


def magnet(key, title, done, btn, alt=True):
    opts = '<option value="" disabled selected>%s</option>' % t(S["magnet_pick"]) + "".join('<option>%s</option>' % t(x) for x in U.SECTORS)
    alt_html = ('        <p class="ucp-lead__alt">%s <a href="offers.html#compare">%s&nbsp;<span aria-hidden="true">→</span></a></p>\n' % (
        t(S["magnet_alt"]), t(S["magnet_alt_link"]))) if alt else ""
    return ('  <!-- MOCK: sends nothing yet (js/ui.js, .ucp-lead); wire to the CRM. -->\n'
            '  <section class="ucp ucp--cta" id="offre">\n    <div class="shell">\n      <div class="ucp__cta">\n'
            '        <div class="ucp__cta-copy">\n          <p class="ucp__cta-k">%s</p>\n          <h2 class="ucp__cta-t">%s</h2>\n          <p class="ucp__cta-d">%s</p>\n        </div>\n'
            '        <form class="ucp-lead" data-case="%s" novalidate>\n          <div class="ucp-lead__row">\n'
            '            <label class="ucp-lead__f"><span>%s</span><input class="fld__input" name="email" type="email" autocomplete="email" placeholder="name@company.com" required /></label>\n'
            '            <label class="ucp-lead__f"><span>%s</span><select class="fld__input" name="sector" required>%s</select></label>\n'
            '          </div>\n          <button class="btn btn--primary" type="submit">%s <span aria-hidden="true">→</span></button>\n'
            '          <p class="fld__error" hidden>%s</p>\n          <p class="fld__error ucp-lead__sector-err" hidden>%s</p>\n'
            '          <p class="consent">%s <a href="privacy.html">%s</a>.</p>\n        </form>\n%s'
            '        <p class="ucp-lead__done" role="status" hidden>%s</p>\n      </div>\n    </div>\n  </section>') % (
        t(S["hub_magnet_k"] if key == "of-prices" else S["magnet_k"]), title,
        t(S["hub_magnet_d"] if key == "of-prices" else S["magnet_d"]), key, t(S["magnet_email"]), t(S["magnet_sector"]), opts, btn,
        t(S["magnet_err"]), t(S["magnet_pick_err"]), t(S["magnet_consent"]), t(S["privacy"]), alt_html, done)


def logos():
    return U.clients(EN)


def faq_section(items):
    return ('  <section class="of-faq">\n    <div class="shell">\n      <div class="xs__head"><h2 class="xs__title">%s</h2></div>\n'
            '      <div class="faq">%s</div>\n    </div>\n  </section>') % (
        t(S["faq"]), "".join("<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in items))


def bar(offer_label):
    return ('<div class="ucp-bar" aria-hidden="true" hidden>\n'
            '  <button class="ucp-bar__chat" type="button" tabindex="-1" aria-label="%s"><img src="/assets/img/team/founder-antoine-160.webp" alt="" width="44" height="44" /><i aria-hidden="true"></i></button>\n'
            '  <a class="btn btn--primary" href="#offre" tabindex="-1">%s</a>\n'
            '  <a class="btn btn--ghost" href="#book" tabindex="-1">%s</a>\n</div>') % (a(S["bar_chat"]), offer_label, t(S["bar_call"]))


def shell_source(src=None):
    """offers.html as the shell other generators copy: without its own SEO
    block and its language attributes"""
    src = src if src is not None else (ROOT / "offers.html").read_text()
    src = re.sub(r"\s*<!-- seo:offers -->.*?<!-- /seo:offers -->", "", src, flags=re.S)
    src = re.sub(r"\s*<!-- offers-bar -->.*?<!-- /offers-bar -->", "", src, flags=re.S)
    return re.sub(r"<html[^>]*>", '<html lang="en">', src, count=1)


def seo_block(file, ld_tags):
    fr_url = FR_PATH[file]
    return ('<!-- seo:offers -->\n<link rel="canonical" href="%s/%s" />\n'
            '<link rel="alternate" hreflang="fr" href="%s%s" />\n<link rel="alternate" hreflang="en" href="%s/%s" />\n'
            '<link rel="alternate" hreflang="x-default" href="%s/%s" />\n%s\n<!-- /seo:offers -->') % (
        SITE, file, SITE, fr_url, SITE, file, SITE, file, ld_tags)


def to_fr(page, file, seo_title, seo_desc, ld_en, ld_fr):
    """the French twin: same page, text translated in the HTML, French head"""
    fr_url = FR_PATH[file]
    fr = re.sub(r'<html[^>]*>', '<html lang="fr" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (fr_url, file), page, count=1)
    fr = re.sub(r'href="([^"]*)" data-fr="([^"]*)"', r'href="\2"', fr)
    fr = re.sub(r'href="(?:/)?index\.html(#[^"]*)?"', lambda m: 'href="/fr/%s"' % (m.group(1) or ""), fr)
    ft, fd = html.escape(U.typo(seo_title[FR], FR)), html.escape(U.typo(seo_desc[FR], FR))
    fr = re.sub(r"<title>.*?</title>", "<title>%s</title>" % ft, fr, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % fd),
                     (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % ft),
                     (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % fd)):
        fr = re.sub(pat, val, fr, count=1)
    fr = fr.replace('<link rel="canonical" href="%s/%s" />' % (SITE, file), '<link rel="canonical" href="%s%s" />' % (SITE, fr_url), 1)
    fr = fr.replace(ld_en, ld_fr, 1)
    fr = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', r'\1="/\2"', fr)
    fr = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="%s"' % ", ".join(
        (q if q.startswith(("/", "http")) else "/" + q) for q in (y.strip() for y in m.group(1).split(","))), fr)
    b0, b1 = fr.index("<body"), fr.index("</body>")
    fr = fr[:b0] + per_lang(U.translate(fr[b0:b1]).replace(">Skip to content<", ">Aller au contenu<"), FR) + fr[b1:]
    fr = fr.replace('placeholder="name@company.com"', 'placeholder="nom@entreprise.com"')
    out = ROOT / fr_url.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("<!-- Generated by tools/build-offers.py: edit that script (or offers.html for the overview). -->\n" + fr)


def per_lang(html_, lang):
    D = __import__("uc_deliverables")
    return re.sub(r"<!--dlv:([\w-]+)-->", lambda m: D.render(m.group(1), lang, U.esc, U.typo), html_)


def to_en(page):
    page = re.sub(r'href="(/fr/cas-usage/[^"]*)" data-en="([^"]*)"', r'href="\2" data-fr="\1"', page)
    return per_lang(page, EN)


# ------------------------------------------------------------------ blocks
def nox_demo():
    aria, cap, k1, brief, k2, topics, unusual, foot = NOX_DEMO
    tops = "".join('<li%s><b>%s</b><span>%s</span><i class="%s">%s</i>%s</li>' % (
        ' class="flag"' if cls else "", t(name), t(n), d, t(v), "<em>%s</em>" % t(unusual) if cls else "")
        for cls, name, n, (d, v) in topics)
    return ('<figure class="xo__demo" aria-label="%s">\n'
            '            <figcaption>%s <span>%s</span></figcaption>\n'
            '            <div class="xo-nox">\n'
            '              <p class="xo-nox__k">%s</p>\n'
            '              <ul class="xo-nox__brief">%s</ul>\n'
            '              <p class="xo-nox__k">%s</p>\n'
            '              <ul class="xo-nox__topics">%s</ul>\n'
            '              <p class="xo-nox__foot">%s</p>\n'
            '            </div>\n'
            '          </figure>') % (a(aria), t(cap), t(S["illus"]), t(k1), "".join("<li>%s</li>" % t(x) for x in brief),
                                      t(k2), tops, t(foot))


def demo(o, offers_html):
    if o["key"] == "nox":
        return nox_demo()
    src = (ROOT / "tools" / "offer_demos.html").read_text()
    return re.search(r"<!-- demo:%s -->\n(.*?)\n<!-- /demo:%s -->" % (o["key"], o["key"]), src, re.S).group(1)


def reel(key):
    """a client interview, the same markup as on the use-case pages"""
    vid, time, quote, brand, who = C.VOICES[key]
    q = ("« %s »" % quote[FR], "“%s”" % quote[EN])
    return ('<a class="reel ucf__voice" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">'
            '<span class="reel__shot"><img src="https://i.ytimg.com/vi_webp/%s/hqdefault.webp" width="480" height="360" alt="" loading="lazy" decoding="async" />'
            '<span class="reel__play" aria-hidden="true"></span><span class="reel__time">%s</span></span>'
            '<span class="ucf__voice-k">%s</span><span class="reel__quote">%s</span>'
            '<span class="reel__meta"><b class="reel__brand">%s</b> <em class="reel__who">%s</em></span></a>') % (
        vid, vid, time, t(S["voice_k"]), t(q), html.escape(brand), html.escape(who))


def case(o):
    """the use case whose deliverable illustrates this offer"""
    return next(x for x in C.CASES if x["key"] == MORE[o["key"]]["dlv"])


def dots(n):
    """position dots under a list that swipes sideways on a phone (js/ui.js)"""
    return '<div class="of-dots" aria-hidden="true">%s</div>' % ("<i></i>" * n)


# real engagements, as Licter published them on its former site (/work/...)
REAL = {
    "vigie": [{"k": ("Luxe · 2024 · client sous NDA", "Luxury · 2024 · client under NDA"),
               "t": ("Veille 24 h/24 de la PDG monde d'un leader du luxe", "24/7 monitoring of a luxury leader's global CEO"),
               "d": ("Cinq veilleurs, en chinois, en hindi, en français, en espagnol et en anglais, des alertes garanties en moins de 15 minutes, et un périmètre complet : réseaux sociaux, Wikipédia, Telegram et dark web. Huit mois de protection de la réputation de la dirigeante.",
                     "Five monitors, in Chinese, Hindi, French, Spanish and English, alerts guaranteed within 15 minutes, and a full scope: social networks, Wikipedia, Telegram and the dark web. Eight months protecting the executive's reputation."),
               "f": [("8 mois", "8 months"), ("5 langues", "5 languages"), ("Alerte en moins de 15 min", "Alert within 15 min")]}],
    "social-insights": [{"k": ("HP · États-Unis · 2023", "HP · United States · 2023"),
                         "t": ("Segmenter des niches de consommateurs pour HP", "Segmenting consumer niches for HP"),
                         "d": ("Une segmentation hybride, croisant les données de panel et celles des réseaux sociaux sur plus de 5 000 critères, et des user stories, pour renforcer la stratégie produit d'HP à partir d'études existantes.",
                               "A hybrid segmentation, crossing panel and social data on more than 5,000 criteria, with user stories, to strengthen HP's product strategy from existing studies."),
                         "f": [("6 mois", "6 months"), ("Plus de 5 000 critères", "More than 5,000 criteria")]},
                        {"k": ("La Poste · France · 2023", "La Poste · France · 2023"),
                         "t": ("Calculer le ROI marketing de La Poste avec la social data", "Measuring La Poste's marketing ROI with social data"),
                         "d": ("Pour un service public de plus de 200 000 salariés, nous avons mesuré l'efficacité de ses actions marketing en termes de positionnement et d'engagement des publics visés.",
                               "For a public service of more than 200,000 employees, we measured how well its marketing actions worked, in positioning and in engagement of the audiences they targeted."),
                         "f": [("1 an", "1 year"), ("Plus de 200 000 salariés", "More than 200,000 employees")]}],
}

REAL_SECTION = (
    '  <section class="of-real">\n'
    '    <div class="shell">\n'
    '      <div class="xs__head"><p class="xs__kick">%s</p><h2 class="xs__title">%s</h2></div>\n'
    '      <ul class="of-real__list">%s</ul>\n'
    '    </div>\n'
    '  </section>\n')


def real_cases(o):
    cs = REAL.get(o["key"])
    if not cs:
        return ""
    cards = "".join('<li class="of-real__c"><p class="of-real__k">%s</p><h3>%s</h3><p>%s</p><ul class="of-real__f">%s</ul></li>' % (
        t(c["k"]), t(c["t"]), t(c["d"]), "".join("<li>%s</li>" % t(f) for f in c["f"])) for c in cs)
    return REAL_SECTION % (t(("CAS RÉELS", "REAL CASES")), t(("Ce que nous avons fait, pour qui.", "What we did, and for whom.")), cards)


def crisis_line(key):
    """a crisis does not wait for a form: the phone, on the monitoring offer"""
    if key != "vigie":
        return ""
    return '<p class="xp-line of-crisis"><span>%s</span> <a href="tel:+33636406600">+33 6 36 40 66 00</a></p>' % t(("Crise en cours ? Appelez-nous", "Crisis under way? Call us"))


def xp_line(key):
    """the expertise pages behind an offer (French added by to_fr)"""
    keys = U.XP_OF.get(key, [])
    guide = ('<p class="xp-line"><span>%s</span> <a href="/article-veille-reseaux-sociaux-entreprise.html">%s</a></p>' % (
        t(("À lire", "Further reading")), t(("Veille des réseaux sociaux en entreprise : le guide", "Social media monitoring for companies: the guide (in French)")))) if key in ("vigie", "nox") else ""
    return (('<p class="xp-line"><span>%s</span> %s</p>' % (t(("Expertise associée", "Related expertise")), ", ".join(
        '<a href="expertise-%s.html">%s</a>' % (k, U.XP_NAME[k]) for k in keys))) if keys else "") + guide


def body(o, offers_html):
    i = OFFERS.index(o)
    others = [x for x in OFFERS if x is not o]
    yes = "".join("<li>%s</li>" % t(x) for x in o["yes"])

    def no_item(x):
        # "not for you if…: that is <offer>": the line leads to that offer
        alt = next((y for y in others if y["name"][EN] in x[EN]), None)
        if not alt:
            return "<li>%s</li>" % t(x)
        return '<li><a href="%s"><span>%s</span><i aria-hidden="true">→</i></a></li>' % (alt["file"], t(x))
    no = "".join(no_item(x) for x in o["no"])
    incl = "".join('<li><span class="of-get__n">0%d</span><b>%s</b><p>%s</p></li>' % (k + 1, t(x), t(y)) for k, (x, y) in enumerate(o["incl"]))
    steps = "".join('<li><span class="ucv-day">%s</span><b>%s</b><p>%s</p></li>' % (t(w), t(x), t(y)) for w, x, y in o["steps"])
    faq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (t(q), t(r)) for q, r in o["faq"])
    spec = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (t(COMPARE_ROWS[r][0]), t(COMPARE_ROWS[r][1][i])) for r in (2, 3, 4))
    spec += '<div><dt>%s</dt><dd><a href="#offre">%s</a></dd></div>' % (t(S["price_row"]), t(S["price_cell"]))
    nxt = "".join('<li class="of-next__card of-acc--%s"><a href="%s"><span class="of-next__n">0%d</span><b>%s</b><span>%s</span><i aria-hidden="true">→</i></a></li>' % (
        CARD_ACCENT[x["key"]], x["file"], x["n"], t(x["name"]), t(x["short"])) for x in others)
    c = case(o)
    # the kicker is two text nodes, "OFFER" and the number, so each translates
    return f'''<main id="content" class="of-acc--{CARD_ACCENT[o["key"]]}">
  <nav class="crumbs shell" aria-label="{a(S["crumbs"])}"><ol><li><a href="index.html">{t(S["home"])}</a></li><li><a href="offers.html">{t(S["offers"])}</a></li><li aria-current="page">{t(o["name"])}</li></ol></nav>

  <section class="xh of-hero">
    <div class="shell xh__grid">
      <div class="xh__copy">
        <p class="xh__kick">{t(("OFFRE", "OFFER"))} <span>0{o["n"]}</span> · {t(o["name"])}</p>
        <h1 class="xh__title">{t(o["h1"])}</h1>
        <p class="xh__lead">{t(o["lead"])}</p>
        <div class="xh__actions">
          <a class="btn btn--primary" href="#book">{t(S["book"])} <span aria-hidden="true">→</span></a>
          <a class="xh__link" href="#included">{t(S["incl_link"])} <span aria-hidden="true">↓</span></a>
        </div>
        {xp_line(o["key"])}{crisis_line(o["key"])}
      </div>
      <div class="of-hero__demo">
        {demo(o, offers_html)}
      </div>
    </div>
    <div class="shell"><dl class="of-spec">{spec}</dl></div>
{logos()}
  </section>

{real_cases(o)}
  <section class="of-fit">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["fit_t"])}</h2></div>
      <div class="of-fit__grid">
      <div class="of-fit__yes">
        <p class="of-fit__k">{t(S["fit_yes"])}</p>
        <ul>{yes}</ul>
      </div>
      <div class="of-fit__no">
        <p class="of-fit__k">{t(S["fit_no"])}</p>
        <ul>{no}</ul>
      </div>
      </div>
    </div>
  </section>

  <section class="of-get" id="included">
    <div class="shell of-get__grid">
      <div>
        <div class="xs__head"><h2 class="xs__title">{t(S["dlv_t"])}</h2><p class="xs__lead">{t(S["get_lead"])}</p></div>
        <ol class="of-get__list">{incl}</ol>
      </div>
      <figure class="of-get__doc">
        <!--dlv:{c["key"]}-->
        <figcaption><a class="xh__link" href="{U.case_path(c, FR)}" data-en="{U.case_path(c, EN)}">{t(S["dlv_link"])} <span aria-hidden="true">→</span></a></figcaption>
      </figure>
    </div>
  </section>

  <section class="of-steps">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["steps_t"])}</h2></div>
      <ol class="ucv-time">{steps}</ol>
      <p class="ucv-note">{t(S["steps_note"])}</p>
    </div>
  </section>

  <section class="of-quote">
    <div class="shell">
      {reel(o["voice"])}
    </div>
  </section>

{magnet("of-" + o["key"], t(MORE[o["key"]]["magnet"]), t(S["magnet_done"]), t(S["magnet_btn"]))}

  <section class="of-faq">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(S["faq"])}</h2></div>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <section class="of-next">
    <div class="shell">
      <div class="of-next__head"><h2 class="xs__title">{t(S["others_t"])}</h2><a class="xh__link" href="offers.html#compare">{t(S["compare"])} <span aria-hidden="true">→</span></a></div>
      <ul class="of-next__list">{nxt}</ul>
      {dots(len(others))}
    </div>
  </section>

{book(o, offers_html)}
</main>'''


def book(o, offers_html):
    m = re.search(r'  <!-- (?:MOCK: the )?callback form.*?</section>', offers_html, re.S)
    sec = m.group(0)
    return re.sub(r'<h2 class="block__title">.*?</h2>', '<h2 class="block__title">%s</h2>' % t(o["book_t"]), sec, count=1)


def ld(o, lang=EN):
    fr = lang == FR
    url = SITE + FR_PATH[o["file"]] if fr else "%s/%s" % (SITE, o["file"])
    out = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil" if fr else "Home", "item": SITE + ("/fr/" if fr else "/")},
            {"@type": "ListItem", "position": 2, "name": "Offres" if fr else "Offers", "item": SITE + (FR_PATH["offers.html"] if fr else "/offers.html")},
            {"@type": "ListItem", "position": 3, "name": o["name"][lang], "item": url}]},
        {"@context": "https://schema.org", "@type": "Service", "name": o["name"][lang], "description": U.typo(o["seo_desc"][lang], lang),
         "provider": U.ORG, "url": url, "areaServed": "Worldwide"},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": U.typo(q[lang], lang), "acceptedAnswer": {"@type": "Answer", "text": U.typo(r[lang], lang)}} for q, r in o["faq"]]},
    ]
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in out)


def page(o, offers_html):
    head_end = offers_html.index("</head>")
    head = offers_html[:head_end]
    title, desc = html.escape(o["seo_title"][EN]), html.escape(o["seo_desc"][EN])
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % desc, head)
    head = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % title, head)
    head = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % desc, head)
    head = re.sub(r'<html[^>]*>', '<html lang="en" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (FR_PATH[o["file"]], o["file"]), head, count=1)
    ld_en = ld(o)
    head = head.replace('<meta name="twitter:card"', seo_block(o["file"], ld_en) + '\n<meta name="twitter:card"', 1)
    start = offers_html.index("</head>")
    main0, main1 = offers_html.index("<main id=\"content\">"), offers_html.index("</main>") + len("</main>")
    shell = offers_html[start:main0] + "%s" + offers_html[main1:]
    shell = shell.replace('<body class="xpage">', '<body class="xpage ofpage">', 1)
    out = "<!-- Generated by tools/build-offers.py: edit that file, not this one. -->\n" + head + shell % body(o, offers_html)
    out = out.replace("</main>", "</main>\n\n" + bar(t(S["bar_offer"])), 1)
    return out, ld_en


def hub_ld(lang):
    fr = lang == FR
    url = SITE + (FR_PATH["offers.html"] if fr else "/offers.html")
    out = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil" if fr else "Home", "item": SITE + ("/fr/" if fr else "/")},
            {"@type": "ListItem", "position": 2, "name": "Offres" if fr else "Offers", "item": url}]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": HUB_SEO["title"][lang], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": o["name"][lang], "description": U.typo(o["seo_desc"][lang], lang),
             "provider": U.ORG, "url": SITE + (FR_PATH[o["file"]] if fr else "/" + o["file"])}} for i, o in enumerate(OFFERS)]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": U.typo(q[lang], lang), "acceptedAnswer": {"@type": "Answer", "text": U.typo(r[lang], lang)}} for q, r in HUB_FAQ]},
    ]
    return "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in out)


# ------------------------------------------------------------------ the overview
HUB = {
    "kick": ("OFFRES", "OFFERS"),
    "h1": ("Achetez des réponses, pas des licences.", "Buy answers, not licences."),
    "lead": OFFERS_PAGE["lead"],
    "cmp_link": ("Comparer en détail", "Compare in detail"),
    "guide_t": ("Quelle est votre situation ?", "What is your situation?"),
    "guide": [("social-insights", ("J'ai des questions, et personne pour faire tourner un outil.", "I have questions, and no one to run a tool.")),
              ("vigie", ("Je dois savoir dans l'heure quand quelque chose casse.", "I need to know within the hour when something breaks.")),
              ("slaas", ("Je paie une plateforme que personne n'ouvre.", "I pay for a platform nobody opens.")),
              ("nox", ("Je veux suivre ma marque chaque jour, et que l'IA fasse le tri.", "I want to follow my brand every day, with AI doing the sorting."))],
    "guide_diag": ("Je ne sais pas où en est mon écoute.", "I am not sure where my listening stands."),
    "cards_t": ("Quatre offres, une même équipe.", "Four offers, one team."),
    "cards_lead": ("Choisissez selon ce que vous voulez recevoir. Toutes sont cadrées et lues par nos consultants.",
                   "Choose by what you want to receive. All of them are framed and read by our consultants."),
    "for": ("Pour vous si", "For you if"),
    "get": ("Vous recevez", "You receive"),
    "model": ("Modèle", "Model"),
    "price": ("Tarif", "Price"),
    "see": ("Voir l'offre", "See the offer"),
    "cmp_sum": ("Comparer les quatre offres en détail", "Compare the four offers in detail"),
    "common_t": ("Ce qui ne change pas, quelle que soit l'offre", "What stays the same, whichever offer"),
    "common": [(("Un consultant dédié", "A dedicated consultant"), ("qui cadre et lit pour vous", "who frames and reads for you")),
               (("20+ langues", "20+ languages"), ("suivies en continu", "monitored continuously")),
               (("Vos livrables", "Your deliverables"), ("vous appartiennent", "belong to you")),
               (("Un démarrage rapide", "A quick start"), ("cadrage dès la première ou la deuxième semaine", "framing in week one or two"))],
    "proof_t": ("Ils en parlent", "They talk about it"),
}
CARD_ACCENT = {"social-insights": "si", "vigie": "vig", "slaas": "sla", "nox": "nox"}
# the overview's photos: the Licter team at work (assets/img/team)
HUB_PHOTO = {"social-insights": "working-session-800", "vigie": "meeting-portrait-800", "slaas": "consultant-dashboard-800", "nox": "two-colleagues-800"}
# what never changes: each glare card shows a photo or a big figure
HUB_GLARE = [("img", "consultant-portrait-800"), ("big", ("20+", "20+")), ("img", "client-conversation-800"), ("big", ("S1", "W1"))]


def fmt_see(o):
    return ("Découvrir %s" % o["name"][FR], "Discover %s" % o["name"][EN])


def hub_main():
    # "what is your situation": the situation, an arrow, the offer it leads to (the animation of the old list)
    guide = "".join('<li><a href="#card-%s" data-card="%s"><span class="of-guide__s">%s</span><i aria-hidden="true">→</i><span class="of-guide__o">%s</span></a></li>' % (
        k, k, t(txt), t(next(o["name"] for o in OFFERS if o["key"] == k))) for k, txt in HUB["guide"])
    guide += '<li class="of-guide__diag"><a href="index.html#diagnostic"><span class="of-guide__s">%s</span><i aria-hidden="true">→</i><span class="of-guide__o">%s</span></a></li>' % (
        t(HUB["guide_diag"]), t(S["diag3"]))
    # the four offers, as the four families of the use-cases hub
    cards = ""
    for i, o in enumerate(OFFERS):
        gets = "".join('<li><a href="%s#included">%s <i aria-hidden="true">→</i></a></li>' % (o["file"], t(x)) for x, _ in o["incl"][:3])
        cards += ('<li class="ucc__card of-ucc of-acc--%s" id="card-%s">'
                  '<img src="/assets/img/team/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" />'
                  '<div class="ucc__top"><p class="ucc__k"><span class="of-ucc__dot" aria-hidden="true"></span><span>0%d · <span>%s</span></span></p>'
                  '<h3 class="ucc__t"><a href="%s">%s</a></h3><p class="of-ucc__promise">%s</p></div>'
                  '<div class="ucc__foot"><p class="of-ucc__for"><b>%s</b> %s</p><ul class="ucc__cases">%s</ul>'
                  '<a class="ucc__all" href="%s">%s <span aria-hidden="true">→</span></a></div></li>') % (
            CARD_ACCENT[o["key"]], o["key"], HUB_PHOTO[o["key"]], o["n"], t(("Offre", "Offer")), o["file"], t(o["name"]), t(o["short"]),
            t(HUB["for"]), t(COMPARE_ROWS[1][1][i]), gets, o["file"], t(fmt_see(o)))
    # what never changes: glare cards
    gl = ""
    for k, ((x, y), art) in enumerate(zip(HUB["common"], HUB_GLARE)):
        kind, val = art
        visual = ('<img src="/assets/img/team/%s.webp" alt="" width="800" height="1200" loading="lazy" decoding="async" />' % val) if kind == "img" else '<span class="of-glare__big" aria-hidden="true">%s</span>' % t(val)
        gl += ('<li class="of-glare of-glare--%s" data-glare>%s<span class="of-glare__shine" aria-hidden="true"></span>'
               '<div class="of-glare__t"><b>%s</b><span>%s</span></div></li>') % (kind, visual, t(x), t(y))
    proof = "".join(reel(k) for k in ("axa", "dassault", "sncf"))
    head = "".join('<th scope="col"><a href="%s">%s</a></th>' % (o["file"], t(o["name"])) for o in OFFERS)
    rows = "".join('<tr><th scope="row">%s</th>%s</tr>' % (t(k), "".join("<td>%s</td>" % t(v) for v in vals)) for k, vals in COMPARE_ROWS)
    rows += '<tr class="of-cmp__price"><th scope="row">%s</th><td colspan="4"><span>%s</span> · <a href="#offre">%s</a></td></tr>' % (
        t(S["price_row"]), t(S["price_cell"]), t(S["price_link"]))
    crumbs = '  <nav class="crumbs shell" aria-label="%s"><ol><li><a href="index.html">%s</a></li><li aria-current="page">%s</li></ol></nav>' % (
        a(S["crumbs"]), t(S["home"]), t(S["offers"]))
    return f'''{crumbs}

  <section class="xh of-hub-hero">
    <div class="shell of-hub-hero__grid">
      <div class="xh__copy">
        <p class="xh__kick">{t(HUB["kick"])}</p>
        <h1 class="xh__title">{t(HUB["h1"])}</h1>
        <p class="xh__lead">{t(HUB["lead"])}</p>
        <div class="xh__actions">
          <a class="btn btn--primary" href="#book">{t(S["bar_call"])} <span aria-hidden="true">→</span></a>
          <a class="xh__link" href="#compare">{t(HUB["cmp_link"])} <span aria-hidden="true">↓</span></a>
        </div>
      </div>
      <nav class="of-guide" aria-labelledby="of-guide-t">
        <p class="of-guide__t" id="of-guide-t">{t(HUB["guide_t"])}</p>
        <ol class="of-guide__list">{guide}</ol>
      </nav>
    </div>
{logos()}
  </section>

  <section class="ucp ucc of-offers" id="offers" aria-labelledby="of-offers-t">
    <div class="shell ucc__head">
      <div>
        <h2 class="xs__title" id="of-offers-t">{t(HUB["cards_t"])}</h2>
        <p class="xs__lead">{t(HUB["cards_lead"])}</p>
      </div>
      <div class="ucc__nav">
        <button class="ucc__btn" type="button" data-dir="-1" aria-label="{a(("Offre précédente", "Previous offer"))}" disabled><span aria-hidden="true">←</span></button>
        <button class="ucc__btn" type="button" data-dir="1" aria-label="{a(("Offre suivante", "Next offer"))}"><span aria-hidden="true">→</span></button>
      </div>
    </div>
    <div class="shell">
    <ol class="ucc__track">{cards}</ol>
    </div>
  </section>

  <section class="of-cmp" id="compare">
    <div class="shell">
      <details class="of-cmp__fold">
        <summary>{t(HUB["cmp_sum"])}</summary>
        <div class="of-cmp__wrap" tabindex="0"><table class="of-cmp__t"><thead><tr><td></td>{head}</tr></thead><tbody>{rows}</tbody></table></div>
      </details>
    </div>
  </section>

  <section class="of-common">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(HUB["common_t"])}</h2></div>
      <ul class="of-glares">{gl}</ul>
    </div>
  </section>

  <section class="of-proof">
    <div class="shell">
      <div class="xs__head"><h2 class="xs__title">{t(HUB["proof_t"])}</h2></div>
      <div class="of-proof__list">{proof}</div>
    </div>
  </section>

{magnet("of-prices", t(S["hub_magnet_t"]), t(S["hub_magnet_done"]), t(S["hub_magnet_btn"]), alt=False)}

{faq_section(HUB_FAQ)}
'''


def hub(src):
    """offers.html: its generated blocks, its SEO head, its language"""
    main = hub_main()
    src = re.sub(r"<!-- offers-main: generated by tools/build-offers.py \(hub_main\) -->.*?<!-- /offers-main -->",
                 lambda m: "<!-- offers-main: generated by tools/build-offers.py (hub_main) -->\n%s\n<!-- /offers-main -->" % main, src, count=1, flags=re.S)
    title, desc = html.escape(HUB_SEO["title"][EN]), html.escape(HUB_SEO["desc"][EN])
    src = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, src, count=1, flags=re.S)
    for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % desc),
                     (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % title),
                     (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % desc)):
        src = re.sub(pat, val, src, count=1)
    src = re.sub(r"\s*<!-- seo:offers -->.*?<!-- /seo:offers -->", "", src, flags=re.S)
    ld_en = hub_ld(EN)
    src = src.replace('<meta name="twitter:card"', seo_block("offers.html", ld_en) + '\n<meta name="twitter:card"', 1)
    src = re.sub(r'<html[^>]*>', '<html lang="en" data-i18n-static data-alt-fr="/fr/offres/" data-alt-en="/offers.html">', src, count=1)
    src = re.sub(r"\s*<!-- offers-bar -->.*?<!-- /offers-bar -->", "", src, flags=re.S)
    src = src.replace("</main>", "</main>\n<!-- offers-bar -->\n%s\n<!-- /offers-bar -->" % bar(t(S["bar_price"])), 1)
    return src, ld_en


def write_dict(label="offer pages", script="build-offers.py", entries=None):
    """the French of these pages, in a block of js/fr.js of their own"""
    entries = NEW if entries is None else entries
    p = ROOT / "js" / "fr.js"
    src = block_re(label).sub("\n", p.read_text())
    # removing a block left its blank line behind: never more than one in a row
    src = re.sub(r"\n{3,}", "\n\n", src)
    lines = "\n".join("  %s:\n    %s," % (json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False)) for k, v in entries.items())
    block = "\n  /* ---- %s (tools/%s) ---- */\n%s\n  /* ---- end %s ---- */\n" % (label, script, lines, label)
    i = src.rindex("};")
    p.write_text(src[:i].rstrip() + "\n" + block + src[i:])


def main():
    src = (ROOT / "offers.html").read_text()
    src, hub_ld_en = hub(src)
    (ROOT / "offers.html").write_text(src)
    offers_html = shell_source(src)
    pages = [(o, page(o, offers_html)) for o in OFFERS]
    for v in OFFERS_PAGE.values():
        t(v)
    for k in ("diag3", "bar_offer", "bar_price", "bar_call", "bar_chat"):
        t(S[k])
    for o in OFFERS:
        t(o["seo_title"])
    t(HUB_SEO["title"])
    write_dict()
    # every string is in the dictionary now: write both languages
    U.DICT.update(U.fr_dict())
    U.DICT.update(NEW)
    U.DICT.setdefault("The 3-minute diagnostic", U.typo(S["diag3"][FR], FR))
    for o, (out, ld_en) in pages:
        (ROOT / o["file"]).write_text(to_en(out))
        to_fr(out, o["file"], o["seo_title"], o["seo_desc"], ld_en, ld(o, FR))
    to_fr(src, "offers.html", HUB_SEO["title"], HUB_SEO["desc"], hub_ld_en, hub_ld(FR))
    (ROOT / "offers.html").write_text(to_en(src))
    print("%d offer pages and the overview written in English and French, %d strings in js/fr.js" % (len(OFFERS), len(NEW)))


if __name__ == "__main__":
    main()
