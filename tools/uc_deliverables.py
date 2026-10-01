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
        (("Des personas sortis d'un atelier", "Personas from a workshop"), ("Des profils bâtis sur 5 000+ critères", "Profiles built on 5,000+ criteria")),
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


def render(key, lang, esc, typo):
    t = lambda fr, en: esc(typo(_t(lang, fr, en), lang))
    body = globals()["_" + key.replace("-", "_")](lang, t, esc)
    return ('<figure class="dlv dlv--%s">'
            '<figcaption class="dlv__head"><b>%s</b><span>%s</span></figcaption>'
            '<div class="dlv__body">%s</div></figure>') % (
        key, t(*TITLES[key]), t("Exemple illustratif", "Illustrative example"), body)


# ------------------------------------------------------------------ 12 deliverables
def _campaign_impact(lang, t, esc):
    pts = [32, 34, 31, 33, 30, 35, 33, 92, 70, 58, 66, 61, 55, 57]
    cat = [40] * 14
    W, H = 560, 170
    def path(a):
        return " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", 20 + i * (W - 40) / 13, H - 18 - v * 1.4) for i, v in enumerate(a))
    x7 = 20 + 6.5 * (W - 40) / 13
    svg = ('<svg class="dlv-chart" viewBox="0 0 %d %d" role="img" aria-label="%s">'
           '<rect class="after" x="%.1f" y="8" width="%.1f" height="%d"/>'
           '<line class="launch" x1="%.1f" x2="%.1f" y1="8" y2="%d"/>'
           '<path class="cat" d="%s"/><path class="brand" d="%s"/>'
           '<circle class="pk" cx="%.1f" cy="%.1f" r="5"/>'
           '<text class="lbl" x="%.1f" y="%.1f">%s</text>'
           '<text class="ax" x="20" y="%d">%s</text><text class="ax" x="%.1f" y="%d">%s</text>'
           '</svg>') % (W, H, t("Volume quotidien avant et après le lancement", "Daily volume before and after the launch"),
                        x7, W - 20 - x7, H - 26, x7, x7, H - 18, path(cat), path(pts),
                        20 + 7 * (W - 40) / 13, H - 18 - 92 * 1.4, 20 + 7 * (W - 40) / 13 + 10, H - 18 - 92 * 1.4 + 4,
                        t("Vidéo créateur, 1,2 M de vues", "Creator video, 1.2M views"),
                        H - 2, t("Avant", "Before"), x7 + 8, H - 2, t("Après le lancement", "After launch"))
    kpi = ('<div class="dlv-kpis"><span><small>%s</small><b>805/%s</b></span><span><small>%s</small><b>2 062/%s</b></span>'
           '<span class="hi"><small>%s</small><b>+156 %%</b></span><span><small>%s</small><b>46 %%</b></span></div>') % (
        t("Avant", "Before"), t("j", "d"), t("Après", "After"), t("j", "d"), t("Gain", "Uplift"), t("portés par les créateurs", "carried by creators"))
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
    bars = "".join('<span><i style="height:%d%%"></i><small>%s</small></span>' % (v, t(*m)) for v, m in zip(vals, months))
    topics = [(("Accueil en boutique", "In-store welcome"), "+38 %", "down"), (("Hausse de prix", "Price increase"), "+12 %", "flat"), (("Savoir-faire", "Craftsmanship"), "+9 %", "up")]
    tl = "".join('<li><span>%s</span><b class="%s">%s</b></li>' % (t(*n), c, esc(v)) for n, v, c in topics)
    return ('<div class="dlv-bull"><div><p class="k">%s</p><div class="dlv-cols">%s</div></div>'
            '<div><p class="k">%s</p><ul class="dlv-list">%s</ul>'
            '<p class="dlv-alert"><b>%s</b>%s</p></div></div>') % (
        t("Sentiment positif, 6 mois", "Positive sentiment, 6 months"), bars, t("Sujets qui montent", "Rising subjects"), tl,
        t("Alerte · il y a 15 min", "Alert · 15 min ago"),
        t("« Accueil en boutique » rompt la tendance à Paris et Milan.", "\"In-store welcome\" breaks the trend in Paris and Milan."))


def _messaging(lang, t, esc):
    adopt = [(("silence", "silence"), 92), (("coffre", "boot space"), 78), (("coût d'usage", "running cost"), 71), (("confort", "comfort"), 64)]
    drop = [(("0 à 100 km/h", "0 to 62 mph"), 14), (("disruptif", "disruptive"), 9), (("premium", "premium"), 11), (("connecté", "connected"), 18)]
    col = lambda items, cls: "".join('<li><span>%s</span>%s<em>%d</em></li>' % (t(*w), _bar(v, cls), v) for w, v in items)
    return ('<div class="dlv-2col"><div><p class="k ok">%s</p><ul class="dlv-lex">%s</ul></div>'
            '<div><p class="k ko">%s</p><ul class="dlv-lex">%s</ul></div></div><p class="dlv-legend">%s</p>') % (
        t("À adopter", "Adopt"), col(adopt, ""), t("À abandonner", "Drop"), col(drop, " dlv-bar--ko"),
        t("Traction : part des conversations qui reprennent le mot, sur 100.", "Traction: share of conversations that pick up the word, out of 100."))


def _brand_risk(lang, t, esc):
    return ('<div class="dlv-alertcard"><p class="lvl"><span class="dots"><i class="on"></i><i class="on"></i><i></i></span>%s</p>'
            '<p class="subj">%s</p>'
            '<dl><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd></dl>'
            '<p class="reco"><b>%s</b>%s</p><p class="ts">%s</p></div>') % (
        t("Niveau 2 sur 3 · à traiter aujourd'hui", "Level 2 of 3 · handle today"),
        t("Crashs serveurs le week-end de sortie", "Server crashes on launch weekend"),
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
    return '<div class="dlv-personas">%s</div>' % out


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
    return ('<ol class="dlv-journey">%s</ol><p class="dlv-callout">%s</p>') % (
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
    pts = [(("VE d'occasion certifiés", "Certified used EVs"), 18, 82, True), (("Citadines électriques", "Compact EVs"), 70, 88, False),
           (("Abonnement auto", "Car subscription"), 30, 42, False), (("Hybrides", "Hybrids"), 82, 60, False), (("Recharge à domicile", "Home charging"), 24, 66, True)]
    dots = "".join('<span class="pt%s" style="left:%d%%;bottom:%d%%"><i></i>%s</span>' % (" free" if f else "", x, y, t(*n)) for n, x, y, f in pts)
    return ('<div class="dlv-matrix"><div class="zone">%s</div>%s'
            '<span class="ax ax--y">%s →</span><span class="ax ax--x">%s →</span></div>'
            '<p class="dlv-callout">%s</p>') % (
        t("Espace libre", "Open space"), dots, t("Demande", "Demand"), t("Couverture des concurrents", "Competitor coverage"),
        t("Deux besoins forts, presque pas couverts : l'occasion certifiée en tête.", "Two strong needs, barely covered: certified used EVs first."))


def _stakeholders(lang, t, esc):
    cols = [(("Lancer", "Build"), "go", [(("Cozy games", "Cozy games"), "↑"), (("LEGO pour adultes", "LEGO for adults"), "↑")]),
            (("Surveiller", "Watch"), "watch", [(("Jeux de société", "Board games"), "↗"), (("Consoles rétro", "Retro consoles"), "↗"), (("Réalité virtuelle", "Virtual reality"), "→")]),
            (("Arrêter", "Stop"), "stop", [(("Battle royale", "Battle royale"), "↓"), (("Jeux NFT", "NFT games"), "↓")])]
    out = "".join('<div class="dlv-trend %s"><p class="k">%s</p><ul>%s</ul></div>' % (
        cls, t(*n), "".join('<li><span>%s</span><b>%s</b></li>' % (t(*x), a) for x, a in items)) for n, cls, items in cols)
    return ('<div class="dlv-3col">%s</div><p class="dlv-legend">%s</p>') % (
        out, t("Portés par : audiences des streamers, collectionneurs adultes, groupes d'amis. Lecture sur 18 mois.",
               "Carried by: streamers' audiences, adult collectors, groups of friends. Read over 18 months."))
