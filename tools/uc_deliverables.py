# -*- coding: utf-8 -*-
"""One deliverable per use case, drawn in HTML: what the client actually
receives, with illustrative figures (taken from the typical cases).

    render(key, lang, esc, typo) -> HTML

Also SYMPTOMS: per case, what the client sees today and what is missing.
MOCK: every figure is illustrative.
"""

FR, EN = 0, 1


def _t(lang, fr, en):
    return fr if lang == FR else en


# what the client sees today -> what is missing
SYMPTOMS = {
    "campaign-impact": [
        (("Des vues, des impressions, des likes", "Views, impressions, likes"), ("Ce que la campagne a changé dans les têtes", "What the campaign changed in people's minds")),
        (("Un pic de mentions le jour J", "A spike of mentions on launch day"), ("Qui l'a déclenché, et s'il a duré", "Who triggered it, and whether it lasted")),
        (("Un bilan agence trois mois après", "An agency report three months later"), ("Une lecture assez tôt pour corriger", "A read early enough to adjust")),
    ],
    "leader-advocacy": [
        (("Le nombre d'abonnés du dirigeant", "Your leader's follower count"), ("Les sujets sur lesquels il est attendu", "The subjects they are expected on")),
        (("Des posts qui tombent à plat", "Posts that fall flat"), ("Où sa parole porte, et où elle fait du bruit", "Where their voice carries, and where it is noise")),
        (("Une impression face aux concurrents", "A feeling about competitors"), ("Une mesure face à un panel de pairs", "A measure against a peer set")),
    ],
    "ambassadors": [
        (("Des listes d'influenceurs triées par abonnés", "Influencer lists sorted by followers"), ("Le recouvrement réel avec votre audience", "The real overlap with your audience")),
        (("Des tarifs qui montent avec la notoriété", "Fees that rise with fame"), ("Les voix émergentes, avant qu'elles coûtent cher", "Emerging voices, before they get expensive")),
        (("Un risque découvert après signature", "A risk found after signing"), ("Les signaux de risque vérifiés avant", "Risk flags checked beforehand")),
    ],
    "reputation": [
        (("Des milliers de mentions à trier", "Thousands of mentions to sort"), ("Les trois sujets qui comptent ce mois-ci", "The three subjects that matter this month")),
        (("Un score de sentiment qui bouge", "A sentiment score that moves"), ("Pourquoi il bouge, et chez qui", "Why it moves, and among whom")),
        (("Des alertes pour un simple pic de volume", "Alerts for a mere volume spike"), ("Une alerte quand un sujet rompt la tendance", "An alert when a subject breaks the trend")),
    ],
    "messaging": [
        (("Une plateforme de marque écrite en interne", "A brand platform written internally"), ("Les mots que vos clients emploient vraiment", "The words your customers actually use")),
        (("Des promesses répétées dans chaque campagne", "Claims repeated in every campaign"), ("Celles qui sont reprises, et celles qui ne prennent pas", "Which ones get repeated, and which do not land")),
        (("Des tests de messages coûteux", "Expensive message tests"), ("Une grille appuyée sur la conversation réelle", "A grid based on the real conversation")),
    ],
    "brand-risk": [
        (("Une crise découverte dans la presse", "A crisis found in the press"), ("Le signal faible, quand il est encore maîtrisable", "The weak signal, while still containable")),
        (("Des alertes mots-clés à chaque pic", "Keyword alerts at every spike"), ("Un analyste qui qualifie avant de prévenir", "An analyst who qualifies before alerting")),
        (("Un débat en interne sur « faut-il répondre »", "An internal debate on whether to respond"), ("Une réponse recommandée, prête à valider", "A recommended response, ready to approve")),
    ],
    "segmentation": [
        (("Des cibles décrites par l'âge et le sexe", "Targets described by age and gender"), ("Des communautés décrites par ce qu'elles font", "Communities described by what they do")),
        (("Des personas sortis d'un atelier", "Personas from a workshop"), ("Des profils bâtis sur 7 000+ critères", "Profiles built on 7,000+ criteria")),
        (("Un plan média calé sur le brief", "A media plan set by the brief"), ("La communauté où l'opportunité est la plus forte", "The community with the strongest opportunity")),
    ],
    "rejuvenate": [
        (("Une base fidèle qui vieillit", "A loyal base that is ageing"), ("Ce qui compte pour la génération suivante", "What the next generation cares about")),
        (("Des campagnes « jeunes » qui ne prennent pas", "\"Young\" campaigns that do not land"), ("Où et avec qui leur parler", "Where and with whom to speak to them")),
        (("La peur de froisser vos clients actuels", "The fear of alienating current customers"), ("Les points communs entre les deux audiences", "What the two audiences share")),
    ],
    "touchpoints": [
        (("Une note de satisfaction globale", "An overall satisfaction score"), ("L'étape du parcours où ça se casse", "The step of the journey where it breaks")),
        (("Des réclamations traitées une à une", "Complaints handled one by one"), ("Les irritants classés par fréquence", "Irritants ranked by frequency")),
        (("Des chantiers lancés au feeling", "Projects started on instinct"), ("Ce qu'il faut corriger en premier", "What to fix first")),
    ],
    "product-test": [
        (("Une note moyenne sur les sites marchands", "An average rating on retail sites"), ("Les forces et les défauts, cités et chiffrés", "Strengths and flaws, quoted and counted")),
        (("Des retours produits sans explication", "Returns with no explanation"), ("Le défaut qui fait renvoyer", "The flaw that makes people return it")),
        (("Une vague idée des concurrents", "A vague idea of competitors"), ("Votre produit face au leur, point par point", "Your product against theirs, point by point")),
    ],
    "market-opportunities": [
        (("Des études de marché déjà connues de tous", "Market studies everyone has read"), ("Les besoins qui reviennent sans réponse", "The needs that keep coming up unanswered")),
        (("Des concurrents partout en apparence", "Competitors everywhere, it seems"), ("Les espaces que personne n'occupe", "The spaces nobody holds")),
        (("Un go / no go à l'intuition", "A go / no-go on instinct"), ("Une recommandation argumentée", "A reasoned recommendation")),
    ],
    "stakeholders": [
        (("Une veille qui empile les sujets", "Monitoring that piles up topics"), ("Ce qui monte vraiment, et ce qui fait du bruit", "What is really rising, and what is noise")),
        (("Des tendances vues dans la presse", "Trends seen in the press"), ("Les communautés où elles naissent", "The communities where they are born")),
        (("Une liste d'acteurs sans hiérarchie", "A flat list of players"), ("Qui compte, et quand leur parler", "Who matters, and when to talk to them")),
    ],
}

TITLES = {
    "campaign-impact": ("Lecture avant / après", "Before / after read"),
    "leader-advocacy": ("Carte de part de voix", "Share-of-voice map"),
    "ambassadors": ("Shortlist de créateurs", "Creator shortlist"),
    "reputation": ("Bulletin mensuel", "Monthly bulletin"),
    "messaging": ("Lexique de marque", "Brand lexicon"),
    "brand-risk": ("Fiche d'alerte", "Alert sheet"),
    "segmentation": ("Cartes des communautés", "Community cards"),
    "rejuvenate": ("Analyse d'écart", "Gap analysis"),
    "touchpoints": ("Carte du parcours", "Journey map"),
    "product-test": ("Fiche produit", "Product sheet"),
    "market-opportunities": ("Matrice des opportunités", "Opportunity matrix"),
    "stakeholders": ("Radar des tendances", "Trend radar"),
}


def _bar(v, cls=""):
    return '<span class="dlv-bar%s"><i style="width:%d%%"></i></span>' % (cls, max(2, min(100, v)))


# The frame of a real Licter report page: who it is for (anonymised), when,
# the section, and at the foot where the figures come from and the page.
# (document, client, subtitle, source, page)
META = {
    "campaign-impact": (("Bilan de campagne", "Campaign review"), ("Marque alimentaire", "Food brand"),
                        ("Posts par jour, 7 jours avant et après le lancement", "Posts per day, 7 days before and after launch"),
                        ("Réseaux sociaux, presse, forums · 48 300 posts", "Social media, press, forums · 48,300 posts"), "4 / 16"),
    "leader-advocacy": (("Étude de prise de parole", "Leadership voice study"), ("Groupe industriel", "Industrial group"),
                        ("Part de voix par thème, 90 jours", "Share of voice by theme, 90 days"),
                        ("LinkedIn, X, presse · 12 400 prises de parole", "LinkedIn, X, press · 12,400 statements"), "6 / 22"),
    "ambassadors": (("Sélection de créateurs", "Creator selection"), ("Marque de mode", "Fashion brand"),
                    ("Classement par recouvrement avec votre audience", "Ranked by overlap with your audience"),
                    ("Instagram, TikTok, YouTube · panel d'audience", "Instagram, TikTok, YouTube · audience panel"), "3 / 12"),
    "reputation": (("Bulletin e-réputation", "Reputation bulletin"), ("Maison de luxe", "Luxury house"),
                   ("Synthèse du mois", "The month in brief"),
                   ("Réseaux, avis, presse · 21 langues · 64 900 mentions", "Social, reviews, press · 21 languages · 64,900 mentions"), "1 / 8"),
    "messaging": (("Plateforme de discours", "Messaging platform"), ("Constructeur automobile", "Car maker"),
                  ("Les mots que votre public reprend, et ceux qu'il ignore", "The words your public picks up, and those it ignores"),
                  ("Forums, avis, réseaux · 12 mois · 210 000 posts", "Forums, reviews, social · 12 months · 210,000 posts"), "9 / 24"),
    "brand-risk": (("Alerte Vigie 360", "Vigie 360 alert"), ("Éditeur de jeux vidéo", "Video game publisher"),
                   ("Envoyée à la direction de la communication", "Sent to the communications team"),
                   ("Twitch, X, Reddit, YouTube · suivi 24/7", "Twitch, X, Reddit, YouTube · 24/7 monitoring"), "1 / 1"),
    "segmentation": (("Segmentation d'audience", "Audience segmentation"), ("Marque alimentaire", "Food brand"),
                     ("Les trois communautés à prioriser", "The three communities to prioritise"),
                     ("Panel comportemental · 1,2 M de profils · 7 000+ critères", "Behavioural panel · 1.2M profiles · 7,000+ criteria"), "7 / 19"),
    "rejuvenate": (("Étude Gen Z", "Gen Z study"), ("Maison de maroquinerie", "Leather goods house"),
                   ("Votre base actuelle face à la génération visée", "Your current base against the target generation"),
                   ("Panel comportemental, TikTok, Instagram · 18-25 ans", "Behavioural panel, TikTok, Instagram · 18 to 25"), "5 / 18"),
    "touchpoints": (("Parcours client", "Customer journey"), ("Enseigne e-commerce", "E-commerce retailer"),
                    ("Satisfaction et premier irritant, étape par étape", "Satisfaction and top irritant, step by step"),
                    ("Avis, réseaux, SAV public · 6 mois · 31 800 verbatims", "Reviews, social, public support · 6 months · 31,800 verbatims"), "4 / 14"),
    "product-test": (("Test produit", "Product test"), ("Éditeur de jeux vidéo", "Video game publisher"),
                     ("Votre jeu face au concurrent principal, 30 jours après la sortie", "Your game against the main competitor, 30 days after release"),
                     ("Steam, Reddit, YouTube · 9 200 avis", "Steam, Reddit, YouTube · 9,200 reviews"), "2 / 10"),
    "market-opportunities": (("Étude d'opportunités", "Opportunity study"), ("Constructeur automobile", "Car maker"),
                             ("La demande face à ce que proposent les concurrents", "Demand against what competitors offer"),
                             ("Google, YouTube, forums · 12 mois · 1,8 M de recherches", "Google, YouTube, forums · 12 months · 1.8M searches"), "8 / 20"),
    "stakeholders": (("Radar des tendances", "Trend radar"), ("Fabricant de jouets", "Toy maker"),
                     ("Ce qu'il faut lancer, surveiller ou arrêter", "What to build, watch or stop"),
                     ("Réseaux, recherche, streams · 18 mois", "Social, search, streams · 18 months"), "3 / 15"),
}


def _bar(v, cls=""):
    return '<span class="dlv-bar%s"><i style="width:%d%%"></i></span>' % (cls, max(2, min(100, v)))


def render(key, lang, esc, typo):
    t = lambda fr, en: esc(typo(_t(lang, fr, en), lang))
    body = globals()["_" + key.replace("-", "_")](lang, t, esc)
    doc, client, sub, src, page = META[key]
    return ('<figure class="dlv dlv--%s">'
            '<div class="dlv__top" aria-hidden="true"><img class="dlv__logo" src="/assets/img/logo-navy.webp" alt="" width="44" height="48" loading="lazy" decoding="async" />'
            '<span class="dlv__doc"><b>%s</b><small>%s · %s</small></span><span class="dlv__tag">%s</span></div>'
            '<figcaption class="dlv__head"><b>%s</b><small>%s</small></figcaption>'
            '<div class="dlv__body">%s</div>'
            '<div class="dlv__foot"><span>%s %s</span><span>Licter · %s</span></div></figure>') % (
        key, t(*doc), t(*client), t("Octobre 2026", "October 2026"), t("Données illustratives", "Illustrative data"),
        t(*TITLES[key]), t(*sub), body, t("Source :", "Source:"), t(*src), "p. " + page)


# ------------------------------------------------------------------ 12 deliverables
def _campaign_impact(lang, t, esc):
    brand = [780, 820, 760, 805, 790, 840, 810, 3120, 2480, 2010, 2160, 2050, 1910, 1960]
    cat = [1080, 1100, 1060, 1090, 1110, 1070, 1100, 1180, 1150, 1120, 1130, 1100, 1090, 1110]
    W, H, L0, R0, T0, B0 = 560, 210, 44, 12, 14, 26
    PW, PH, YM = W - L0 - R0, H - T0 - B0, 3500
    X = lambda i: L0 + i * PW / 13
    Y = lambda v: T0 + PH - v / YM * PH
    path = lambda a: " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", X(i), Y(v)) for i, v in enumerate(a))
    area = path(brand) + " L%.1f %.1f L%.1f %.1f Z" % (X(13), Y(0), X(0), Y(0))
    grid = "".join('<line class="gl" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (
        L0, W - R0, Y(v), Y(v), L0 - 6, Y(v) + 4, ("%d" % v if v < 1000 else ("%d %03d" % (v // 1000, v % 1000) if lang == FR else "{:,}".format(v)))) for v in (0, 1000, 2000, 3000))
    days = "".join('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (
        X(i), H - 6, ("J%+d" % (i - 7) if lang == FR else "D%+d" % (i - 7)) if i != 7 else ("J0" if lang == FR else "D0")) for i in range(0, 14, 2))
    x7 = (X(6) + X(7)) / 2
    svg = ('<svg class="dlv-chart" viewBox="0 0 %d %d" role="img" aria-label="%s">%s'
           '<rect class="after" x="%.1f" y="%d" width="%.1f" height="%d"/>'
           '<line class="launch" x1="%.1f" x2="%.1f" y1="%d" y2="%.1f"/>'
           '<text class="lbl lbl--launch" x="%.1f" y="%d" text-anchor="end">%s</text>'
           '<path class="area" d="%s"/><path class="cat" d="%s"/><path class="brand" d="%s"/>'
           '<circle class="pk" cx="%.1f" cy="%.1f" r="5"/>'
           '<text class="lbl" x="%.1f" y="%.1f">%s</text>%s</svg>') % (
        W, H, t("Posts par jour, avant et après le lancement", "Posts per day, before and after the launch"), grid,
        x7, T0, W - R0 - x7, PH, x7, x7, T0, Y(0), x7 - 6, T0 + 12, t("Lancement", "Launch"),
        area, path(cat), path(brand), X(7), Y(3120), X(7) + 10, Y(3120) + 4,
        t("Vidéo créateur · 1,2 M de vues", "Creator video · 1.2M views"), days)
    kpi = ('<div class="dlv-kpis"><span><small>%s</small><b>805</b><i>%s</i></span><span><small>%s</small><b>2 062</b><i>%s</i></span>'
           '<span class="hi"><small>%s</small><b>+156 %%</b><i>%s</i></span><span><small>%s</small><b>46 %%</b><i>%s</i></span></div>') % (
        t("Avant", "Before"), t("posts/jour", "posts/day"), t("Après", "After"), t("posts/jour", "posts/day"),
        t("Gain", "Uplift"), t("vs avant", "vs before"), t("Portés par", "Carried by"), t("les créateurs", "creators"))
    return kpi + svg + '<p class="dlv-legend"><i class="sw sw--brand"></i>%s <i class="sw sw--cat"></i>%s</p>' % (
        t("Votre marque", "Your brand"), t("Moyenne de la catégorie", "Category average"))


def _leader_advocacy(lang, t, esc):
    topics = [("Innovation", "Innovation"), ("Emploi", "Jobs"), ("Industrie en région", "Regional industry"), ("Climat", "Climate"), ("Résultats", "Results")]
    rows = [(("Votre PDG", "Your CEO"), [9, 31, 28, 6, 12], True), (("Pair A", "Peer A"), [34, 8, 4, 22, 18], False),
            (("Pair B", "Peer B"), [29, 6, 3, 18, 25], False), (("Pair C", "Peer C"), [22, 10, 2, 30, 14], False)]
    head = "".join('<th scope="col">%s</th>' % t(*x) for x in topics)
    body = ""
    for name, vals, you in rows:
        cells = "".join('<td><span class="hm" style="--v:%.2f">%d %%</span></td>' % (v / 34, v) for v in vals)
        body += '<tr%s><th scope="row">%s</th>%s</tr>' % (' class="you"' if you else "", t(*name), cells)
    return ('<table class="dlv-heat"><thead><tr><th><span class="visually-hidden">%s</span></th>%s</tr></thead><tbody>%s</tbody></table>'
            '<p class="dlv-callout">%s</p>') % (t("Porte-parole", "Spokesperson"), head, body, t(
                "Votre PDG est attendu sur l'emploi et l'industrie en région, là où ses pairs sont absents.",
                "Your CEO is expected on jobs and regional industry, where peers are absent."))


def _ambassadors(lang, t, esc):
    rows = [("@lea.mode", "Instagram", "86 k", 64, 82, 0), ("@studio.zoe", "TikTok", "142 k", 58, 77, 0),
            ("@theo.style", "YouTube", "51 k", 55, 74, 1), ("@grande.icone", "Instagram", "2,4 M", 18, 61, 2),
            ("@clara.vintage", "TikTok", "39 k", 47, 80, 0)]
    risk = [("faible", "low"), ("à vérifier", "check"), ("élevé", "high")]
    body = "".join('<tr%s><td class="rk">%d</td><td><b>%s</b><small>%s · %s</small></td><td>%s<em>%d %%</em></td><td>%d</td><td><span class="risk r%d">%s</span></td></tr>' % (
        ' class="dim"' if r == 2 else "", i + 1, esc(h), esc(pf), esc(f), _bar(ov), ov, aff, r, t(*risk[r])) for i, (h, pf, f, ov, aff, r) in enumerate(rows))
    return ('<table class="dlv-table"><thead><tr><th>#</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            '<p class="dlv-callout">%s</p>') % (
        t("Créateur", "Creator"), t("Recouvrement d'audience", "Audience overlap"), t("Affinité", "Affinity"), t("Risque", "Risk"), body,
        t("Le plus gros compte arrive 4e : son audience recoupe peu la vôtre.", "The biggest account ranks 4th: its audience barely overlaps yours."))


def _reputation(lang, t, esc):
    months = [("mai", "May"), ("juin", "Jun"), ("juil.", "Jul"), ("août", "Aug"), ("sept.", "Sep"), ("oct.", "Oct")]
    vals = [62, 64, 61, 58, 52, 49]
    bars = "".join('<span class="%s"><em>%d</em><i style="height:%d%%"></i><small>%s</small></span>' % (
        "now" if k == len(vals) - 1 else "", v, v * 1.3, t(*m)) for k, (v, m) in enumerate(zip(vals, months)))
    topics = [(("Accueil en boutique", "In-store welcome"), "+38 %", "down", [8, 9, 8, 10, 14, 22]),
              (("Hausse de prix", "Price increase"), "+12 %", "flat", [10, 11, 10, 12, 12, 13]),
              (("Savoir-faire", "Craftsmanship"), "+9 %", "up", [9, 9, 10, 10, 11, 12])]
    tl = "".join('<li><span>%s</span>%s<b class="%s">%s</b></li>' % (t(*n), _spark(sp), c, esc(v)) for n, v, c, sp in topics)
    return ('<div class="dlv-score"><span><small>%s</small><b>49</b><i class="down">−3 %s</i></span>'
            '<span><small>%s</small><b>64 900</b><i>%s</i></span><span><small>%s</small><b>21</b><i>%s</i></span></div>'
            '<div class="dlv-bull"><div><p class="k">%s</p><div class="dlv-cols">%s</div></div>'
            '<div><p class="k">%s</p><ul class="dlv-list">%s</ul>'
            '<p class="dlv-alert"><b>%s</b>%s</p></div></div>') % (
        t("Sentiment positif", "Positive sentiment"), t("pts", "pts"), t("Mentions", "Mentions"), t("ce mois", "this month"),
        t("Langues", "Languages"), t("lues par des natifs", "read by natives"),
        t("Sentiment positif, 6 mois (%)", "Positive sentiment, 6 months (%)"), bars, t("Sujets qui montent", "Rising subjects"), tl,
        t("Alerte · il y a 15 min", "Alert · 15 min ago"),
        t("« Accueil en boutique » rompt la tendance à Paris et Milan.", "\"In-store welcome\" breaks the trend in Paris and Milan."))


def _spark(vals, cls=""):
    lo, hi = min(vals), max(vals)
    span = max(hi - lo, hi * .6)
    mid = (hi + lo) / 2
    pts = " ".join("%.1f,%.1f" % (i * 48 / (len(vals) - 1), 8 - (v - mid) / span * 12) for i, v in enumerate(vals))
    return '<svg class="dlv-spark%s" viewBox="-1 0 50 16" aria-hidden="true"><polyline points="%s"/></svg>' % (cls, pts)


def _messaging(lang, t, esc):
    adopt = [(("silence", "silence"), 92), (("coffre", "boot space"), 78), (("coût d'usage", "running cost"), 71), (("confort", "comfort"), 64)]
    drop = [(("0 à 100 km/h", "0 to 62 mph"), 14), (("disruptif", "disruptive"), 9), (("premium", "premium"), 11), (("connecté", "connected"), 18)]
    col = lambda items, cls: "".join('<li><span>%s</span>%s<em>%d</em></li>' % (t(*w), _bar(v, cls), v) for w, v in items)
    return ('<div class="dlv-2col"><div><p class="k ok">%s</p><ul class="dlv-lex">%s</ul></div>'
            '<div><p class="k ko">%s</p><ul class="dlv-lex">%s</ul></div></div><p class="dlv-legend">%s</p>') % (
        t("À adopter", "Adopt"), col(adopt, ""), t("À abandonner", "Drop"), col(drop, " dlv-bar--ko"),
        t("Traction : part des conversations qui reprennent le mot, sur 100.", "Traction: share of conversations that pick up the word, out of 100."))


def _brand_risk(lang, t, esc):
    hours = [120, 130, 125, 140, 210, 380, 520]
    lo, hi = 0, 560
    pts = " ".join("%.1f,%.1f" % (24 + i * 500 / 6, 66 - v / hi * 58) for i, v in enumerate(hours))
    ticks = "".join('<text class="ax" x="%.1f" y="92" text-anchor="middle">%s</text>' % (24 + i * 500 / 6, h) for i, h in enumerate(
        ["8 h", "9 h", "10 h", "11 h", "12 h", "13 h", "14 h"] if lang == FR else ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm"]))
    curve = ('<svg class="dlv-alertcurve" viewBox="0 0 548 98" role="img" aria-label="%s">'
             '<line class="gl" x1="0" x2="548" y1="66" y2="66"/><polyline class="ln" points="%s"/>'
             '<circle class="pk" cx="524" cy="%.1f" r="5"/><text class="v" x="466" y="14" text-anchor="end">%s</text>%s</svg>') % (
        t("Mentions par heure, de 8 h à 14 h", "Mentions per hour, 8am to 2pm"), pts, 66 - 520 / hi * 58,
        t("520 mentions/h", "520 mentions/h"), ticks)
    return ('<div class="dlv-alertcard"><p class="mail"><b>%s</b> · %s</p>'
            '<p class="lvl"><span class="dots"><i class="on"></i><i class="on"></i><i></i></span>%s</p>'
            '<p class="subj">%s</p>%s'
            '<dl><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd></dl>'
            '<p class="reco"><b>%s</b>%s</p><p class="ts">%s</p></div>') % (
        t("Vigie Licter", "Licter Vigie"), t("à : direction de la communication", "to: communications team"),
        t("Niveau 2 sur 3 · à traiter aujourd'hui", "Level 2 of 3 · handle today"),
        t("Crashs serveurs le week-end de sortie", "Server crashes on launch weekend"), curve,
        t("Porté par", "Carried by"), t("3 streamers (1,2 M d'abonnés cumulés)", "3 streamers (1.2M followers combined)"),
        t("Vitesse", "Speed"), t("× 4 en 6 heures", "× 4 in 6 hours"),
        t("Langues", "Languages"), t("français, anglais, espagnol", "French, English, Spanish"),
        t("Tonalité", "Tone"), t("colère sur les serveurs, pas sur le jeu", "anger at the servers, not the game"),
        t("Réponse recommandée", "Recommended response"),
        t("Un point quotidien sur les correctifs, sans communication de crise.", "A daily update on fixes, no crisis communication."),
        t("Envoyée à 14 h 32 · qualifiée par l'analyste de garde", "Sent at 2:32 pm · qualified by the analyst on duty"))


def _segmentation(lang, t, esc):
    cards = [(("Abonnés des créateurs food", "Food creators' followers"), 19, 74, 86, [("TikTok", "TikTok"), ("Instagram", "Instagram")], True),
             (("Parents pragmatiques", "Pragmatic parents"), 41, 78, 52, [("Facebook", "Facebook"), ("Recherche", "Search")], False),
             (("Sportifs", "Sport fans"), 16, 57, 69, [("YouTube", "YouTube"), ("Strava", "Strava")], False)]
    out = ""
    for name, size, aff, opp, media, top in cards:
        chips = "".join("<span>%s</span>" % t(*m) for m in media)
        out += ('<div class="dlv-persona%s"><b>%s</b><small>%d %% %s</small>'
                '<p><span>%s</span>%s<em>%d</em></p><p><span>%s</span>%s<em>%d</em></p><div class="chips">%s</div></div>') % (
            " top" if top else "", t(*name), size, t("de l'audience", "of the audience"),
            t("Affinité", "Affinity"), _bar(aff), aff, t("Opportunité", "Opportunity"), _bar(opp, " dlv-bar--hi"), opp, chips)
    split = [(("Parents pragmatiques", "Pragmatic parents"), 41, "c2"), (("Abonnés créateurs food", "Food creators' followers"), 19, "c1"),
             (("Sportifs", "Sport fans"), 16, "c3"), (("Autres", "Others"), 24, "c4")]
    bar = "".join('<i class="%s" style="width:%d%%" title="%s"></i>' % (c, v, t(*n)) for n, v, c in split)
    leg = "".join('<span><i class="%s"></i>%s %d %%</span>' % (c, t(*n), v) for n, v, c in split)
    return ('<p class="k">%s</p><div class="dlv-split">%s</div><div class="dlv-split__leg">%s</div>'
            '<div class="dlv-personas">%s</div>') % (t("Composition de votre audience", "Your audience, by community"), bar, leg, out)


def _rejuvenate(lang, t, esc):
    rows = [(("Plateforme principale", "Main platform"), ("Facebook", "Facebook"), ("TikTok", "TikTok"), 3),
            (("Sujet n° 1", "Top subject"), ("héritage", "heritage"), ("seconde main", "pre-owned"), 2),
            (("Créateurs suivis", "Creators followed"), ("presse mode", "fashion press"), ("créateurs de 20 à 150 k", "20 to 150k creators"), 3),
            (("Premier achat", "First purchase"), ("sac iconique", "iconic bag"), ("petite maroquinerie", "small leather goods"), 1),
            (("Budget", "Budget"), ("2 000 € et plus", "€2,000 and up"), ("moins de 400 €", "under €400"), 3)]
    body = "".join('<tr><th scope="row">%s</th><td>%s</td><td><b>%s</b></td><td><span class="gap g%d">%s</span></td></tr>' % (
        t(*k), t(*a), t(*b), g, t(*[("proche", "close"), ("à combler", "to bridge"), ("fort", "wide")][g - 1])) for k, a, b, g in rows)
    return ('<table class="dlv-table dlv-gap"><thead><tr><th><span class="visually-hidden">%s</span></th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'
            '<p class="dlv-callout">%s</p>') % (
        t("Critère", "Criterion"), t("Base actuelle", "Current base"), t("Gen Z visée", "Target Gen Z"), t("Écart", "Gap"), body,
        t("Le pont : la petite maroquinerie, déjà désirée par les deux audiences.", "The bridge: small leather goods, already wanted by both audiences."))


def _touchpoints(lang, t, esc):
    steps = [(("Découverte", "Discovery"), 82, ("pubs trop répétées", "ads repeated too often"), 6),
             (("Choix", "Choice"), 76, ("formats peu clairs", "unclear pack sizes"), 9),
             (("Achat", "Purchase"), 71, ("frais de port", "shipping fees"), 11),
             (("Livraison", "Delivery"), 34, ("colis en retard ou abîmés", "late or damaged parcels"), 62),
             (("Après-vente", "After-sales"), 68, ("remboursement lent", "slow refunds"), 12)]
    out = "".join('<li class="%s"><span class="dot" style="--v:%d"></span><b>%s</b><small>%d %% %s</small><p>%s <em>%d %%</em></p></li>' % (
        "worst" if s < 50 else "", s, t(*n), s, t("satisfaits", "satisfied"), t(*irr), share) for n, s, irr, share in steps)
    sat = [s for n, s, i, sh in steps]
    X = lambda k: 80 + k * 440 / 4
    pts = " ".join("%.1f,%.1f" % (X(k), 70 - v * 0.6) for k, v in enumerate(sat))
    dots = "".join('<circle class="%s" cx="%.1f" cy="%.1f" r="5"/><text class="v" x="%.1f" y="%.1f" text-anchor="middle">%d %%</text>' % (
        "pk" if v < 50 else "pt", X(k), 70 - v * 0.6, X(k), 70 - v * 0.6 - 10, v) for k, v in enumerate(sat))
    curve = ('<svg class="dlv-journeycurve" viewBox="0 0 560 78" role="img" aria-label="%s">'
             '<line class="gl" x1="44" x2="550" y1="40" y2="40"/><text class="ax" x="0" y="44">50 %%</text>'
             '<polyline class="ln" points="%s"/>%s</svg>') % (t("Satisfaction à chaque étape", "Satisfaction at each step"), pts, dots)
    return (curve.replace("%", "%%") + '<ol class="dlv-journey">%s</ol><p class="dlv-callout">%s</p>') % (
        out, t("62 % des posts négatifs portent sur la livraison : c'est là qu'il faut agir.", "62% of negative posts are about delivery: that is where to act."))


def _product_test(lang, t, esc):
    you_s = [(("scénario", "story"), 41), (("graphismes", "graphics"), 33), (("bande-son", "soundtrack"), 18)]
    you_i = [(("lag en ligne", "online lag"), 29), (("microtransactions", "microtransactions"), 24)]
    them_s = [(("multijoueur", "multiplayer"), 37), (("prix", "price"), 21)]
    them_i = [(("scénario court", "short story"), 31), (("bugs", "bugs"), 19)]
    li = lambda items, cls: "".join('<li class="%s"><span>%s</span><em>%d %%</em></li>' % (cls, t(*w), v) for w, v in items)
    col = lambda title, score, s, i: ('<div class="dlv-prod"><p class="k">%s</p><p class="score"><b>%s</b>/10</p>'
                                       '<ul>%s%s</ul></div>') % (title, score, li(s, "plus"), li(i, "minus"))
    return '<div class="dlv-2col">%s%s</div><p class="dlv-legend">%s</p>' % (
        col(t("Votre jeu", "Your game"), "7,8" if lang == FR else "7.8", you_s, you_i),
        col(t("Concurrent principal", "Main competitor"), "7,1" if lang == FR else "7.1", them_s, them_i),
        t("+ forces, − irritants, en part des avis qui les citent.", "+ strengths, − irritants, as a share of the reviews that mention them."))


def _market_opportunities(lang, t, esc):
    pts = [(("VE d'occasion certifiés", "Certified used EVs"), 18, 82, True, 26), (("Citadines électriques", "Compact EVs"), 70, 88, False, 22),
           (("Abonnement auto", "Car subscription"), 30, 42, False, 12), (("Hybrides", "Hybrids"), 82, 60, False, 18), (("Recharge à domicile", "Home charging"), 24, 66, True, 18)]
    dots = "".join('<span class="pt%s" style="left:%d%%;bottom:%d%%;--s:%dpx"><i></i>%s</span>' % (" free" if f else "", x, y, z, t(*n)) for n, x, y, f, z in pts)
    return ('<div class="dlv-matrix"><div class="zone">%s</div><span class="q q--tr">%s</span><span class="q q--br">%s</span>%s'
            '<span class="ax ax--y">%s →</span><span class="ax ax--x">%s →</span></div>'
            '<p class="dlv-callout">%s</p>') % (
        t("Espace libre", "Open space"), t("Marché disputé", "Crowded market"), t("Marché saturé", "Saturated market"), dots,
        t("Demande", "Demand"), t("Couverture des concurrents", "Competitor coverage"),
        t("Deux besoins forts, presque pas couverts : l'occasion certifiée en tête.", "Two strong needs, barely covered: certified used EVs first."))


def _stakeholders(lang, t, esc):
    up, rise, flat, down = [3, 4, 4, 6, 7, 9, 12], [5, 5, 6, 6, 7, 8, 8], [7, 6, 7, 7, 6, 7, 7], [12, 11, 9, 8, 6, 5, 4]
    cols = [(("Lancer", "Build"), "go", [(("Cozy games", "Cozy games"), "+182 %", up), (("LEGO pour adultes", "LEGO for adults"), "+64 %", up)]),
            (("Surveiller", "Watch"), "watch", [(("Jeux de société", "Board games"), "+31 %", rise), (("Consoles rétro", "Retro consoles"), "+22 %", rise), (("Réalité virtuelle", "Virtual reality"), "+2 %", flat)]),
            (("Arrêter", "Stop"), "stop", [(("Battle royale", "Battle royale"), "−48 %", down), (("Jeux NFT", "NFT games"), "−71 %", down)])]
    out = "".join('<div class="dlv-trend %s"><p class="k">%s</p><ul>%s</ul></div>' % (
        cls, t(*n), "".join('<li><span>%s</span>%s<b>%s</b></li>' % (t(*x), _spark(sp), a.replace(" ", "\u00a0")) for x, a, sp in items)) for n, cls, items in cols)
    return ('<div class="dlv-3col">%s</div><p class="dlv-legend">%s</p>') % (
        out, t("Portés par : audiences des streamers, collectionneurs adultes, groupes d'amis. Lecture sur 18 mois.",
               "Carried by: streamers' audiences, adult collectors, groups of friends. Read over 18 months."))
