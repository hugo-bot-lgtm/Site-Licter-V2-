# Licter — landing page

HTML / CSS / JS vanille, aucune dépendance, aucun build. Déployable tel quel
(Vercel : « Other / no framework », racine = ce dossier).

```
index.html          ← hero + use cases + colonne vertébrale du funnel
use-cases.html      ← les 4 familles, 12 cas d'usage
offers.html         ← les 3 offres + méthode en 4 étapes
why-licter.html     ← origine, chiffres, différenciateurs
tech-tools.html     ← les 4 couches de signal, sources, stack
clients.html        ← mur de clients, 4 questions récurrentes
blog.html           ← 4 fils éditoriaux (à brancher sur le vrai blog)
tech-talkwalker.html ┐
tech-visibrain.html  │ une page par plateforme, structure Flowt
tech-youscan.html    │
tech-soprism.html    ┘
guide.html          ← aimant à leads : le guide des 12 questions
diagnostic.html     ← diagnostic social data (milieu de funnel)
book-a-meeting.html ← prise de rendez-vous (bas de funnel)
css/styles.css
js/cartography.js   ← la carto animée (canvas)
js/i18n.js          ← bascule EN / FR
js/fr.js            ← dictionnaire français
js/ui.js            ← logo, bandeau, onglets, console, menus, formulaires
assets/fonts/       ← AiglonProWide Demi + Thin (charte)
assets/img/         ← logo navy (pages claires) + logo blanc (réserve)
```

Chaque page partage le même en-tête, la même carto de fond, le même pied de
page et un bloc de conversion final (email + « Book a meeting »). Tous les
formulaires sont câblés au même gestionnaire — il ne reste qu'un endpoint à
brancher (`js/ui.js`, commentaire `wire to the real endpoint here`).

Lancer en local :

```bash
python3 serve.py 8765
```

`serve.py` est un `http.server` qui ajoute `Cache-Control: no-store`. Sans ça,
le navigateur garde CSS et JS en cache, répond 304 et **les modifications
semblent ne pas avoir eu lieu** — piège qui a coûté deux allers-retours. Les
liens vers les assets portent aussi un `?v=` à bumper à chaque livraison.

(un vrai serveur est nécessaire : en `file://`, le détourage du logo est
bloqué par le canvas tainting et retombe sur l'image brute.)

## Palette — thème clair

Le site est passé en **fond clair** : la crème domine, le navy porte le texte.
L'or `#BEA76B` du brief initial est abandonné, remplacé par l'ambre `#fdba11`.

| Rôle | Hex | Usage |
|---|---|---|
| Fond | `#FCF6EF` | fond de page (dominant) |
| Surfaces | `#FFFFFF` | navbar, panneaux déroulants, console, carte de survol |
| Texte | `#13162D` | titres, texte courant, amas sombres de la carto |
| Ambre | `#FDBA11` | **aplats uniquement** : bouton, onglet actif, pastilles, aire du graphe |
| Gris | `#84919A` | bandeau de l'écran 2, réseau de fond, libellés discrets |
| Noir | `#000000` | réserve |

### Le point qui commande tout le reste

**L'ambre pur fait 1.6:1 sur la crème.** Il ne peut porter aucun texte, pas
même du très grand : le seuil AA large est à 3:1. D'où la règle appliquée
partout : l'ambre reste un **aplat** (fond de bouton, onglet actif, pastille,
remplissage du graphe), et tout ce qui est *écrit* en ambre passe sur
`--amber-ink` `#9A6F08` — un ambre assombri, 4.2:1 sur la crème. Ça concerne
la 2e ligne des titres, les `//` de l'accroche, le libellé `OUR USE CASES`,
l'indicateur `+23%`, le lien final et les survols de menu.

### Tons dérivés

| Token | Hex | Pourquoi |
|---|---|---|
| `--amber-ink` | `#9A6F08` | l'ambre pour du texte sur clair (4.2:1) |
| `--amber-deep` | `#C08C0E` | tracés fins : courbe du graphe, filets, pastilles d'onglet |
| `--text-2` | `#56606A` | texte secondaire (5.4:1 — le gris `#84919A` n'est qu'à 3:1) |
| `--text-3` | `#6F7A82` | libellés micro |
| `--line` | `rgba(19,22,45,.12)` | toutes les bordures |
| carto | `#13162D` `#C08C0E` `#9A6F08` `#6E7A82` `#46505A` `#96A1A8` | amas, du plus sombre au plus clair |
| carto fond | `#5F6A72` / `#94A0A7` | communautés d'arrière-plan et poussière |

### Ce que le passage au clair a changé d'autre

- **Logo** : c'est la version **bleue** de la charte qui est utilisée
  (`assets/img/logo-navy.png`). La version blanche est conservée dans
  `assets/img/` si un bloc sombre revient.
- **Logos clients** : silhouettes **navy** et non plus blanches. Le brief
  demandait du blanc parce que le fond était navy ; la logique s'inverse.
- **Cartographie** : dessinée en tons sombres sur la crème. Les opacités ont
  été refaites — les arêtes descendent (une ligne sombre sur clair se voit
  beaucoup plus qu'une ligne claire sur sombre), les points montent
  (plancher d'opacité à 0.5, en dessous ils lisaient comme des salissures),
  et les halos de hub deviennent des ombres colorées douces plutôt que des
  lueurs. La couche d'arrière-plan a été redessinée (voir arbitrage 11) :
  recolorée en `#5F6A72`, traits épaissis de 0.4 à 0.6 px et opacité doublée.
  Sur le navy elle vivait de la lueur des traits fins ; sur la crème il faut
  de la matière.
- **Nappe de l'écran 2** : c'est maintenant un lavis **gris** de la charte,
  pas un voile blanc. Éclaircir la crème n'aurait rien donné : la console
  blanche a besoin d'un fond plus soutenu pour se détacher.

## Ce qui est conforme au brief

- Tokens typos de la charte ; Aiglon Pro Wide chargée en
  `@font-face` (les .otf fonctionnent en web, fallback Outfit ExtraBold),
  Josefin Sans via Google Fonts.
- Hero : logo détouré à la volée, pilule de nav blanche à 62 % / bordure
  navy 12 %, accroche, titre, description, formulaire, bandeau clients en
  plein débord.
- Navbar : deux entrées portent un panneau déroulant (`USE CASES` et
  `TECH & TOOLS`), sur le principe de la capture Browserbase — colonnes
  d'entrées icône + titre + description, colonne annexe séparée d'un filet,
  bandeau d'actions en bas. Ouverture au survol (70 ms d'attente, 180 ms de
  tolérance à la sortie) et au clic, fermeture à `Échap`, au clic extérieur,
  à la perte de focus et au scroll ; `aria-expanded`, `aria-controls` et
  `ArrowDown` pour entrer dans le panneau au clavier. Sous 860 px le panneau
  devient un bloc dépliable dans la pilule.
- Carto : amas définis dans le repère 600 × 500 et mis à l'échelle au
  viewport, double passe large/dense, distribution en somme de trois tirages,
  chaîne détachée, satellites, hubs pulsants (1 → 1.45, ~2.6 s, déphasés),
  trois familles d'arêtes, réseau de communautés d'arrière-plan sur grille
  irrégulière, poussière.
- Voyageurs : graphe d'adjacence reconstruit depuis les arêtes réellement
  dessinées, marche aléatoire de 4-6 sauts sans retour arrière, parcours
  < 110 px rejetés, vitesse constante `largeur / 14` px/s, fondu 0.35 s,
  ~70 simultanés, couleur héritée de la communauté de départ.
  **Plus 46 voyageurs sur le réseau d'arrière-plan** (voir arbitrage 12) :
  mêmes règles, plus petits, plus lents (`largeur / 20`), à 80 % d'opacité,
  et dont les points de départ sont tirés en priorité dans la moitié gauche
  de la page.
- ~~Survol des points~~ : l'infobulle du brief (logo + nom de la plateforme au
  survol d'un nœud) a été **retirée** — les cartes story de l'arbitrage 21
  font la même démonstration, en mieux, sans demander au visiteur de viser le
  bon pixel. Avec elle sont partis la grille de hachage de détection, le test
  de collision à chaque frame et les écouteurs de souris.
- Lisibilité : masque `destination-out` appliqué sur le composite (donc
  voyageurs compris) sous chaque bloc marqué `data-dim`, atténuation 50 %
  avec dégradé de 26 px. Le masque suit le scroll — un test par élément
  n'aurait été juste qu'à une seule position de scroll.
- Écran 2 : filet + libellé, titre, sous-titre de section, puis un bloc en
  deux colonnes — questions + lien à gauche, barre d'onglets à pastilles et
  console à droite (libellé, indicateur chiffré, répartition, courbe,
  légende). Trois paliers : deux colonnes avec rail latéral au-delà de
  1300 px, deux colonnes avec rail en bandeau entre 861 et 1300 px, tout
  empilé en dessous.
- `prefers-reduced-motion` : voyageurs et pulsation figés, bandeau arrêté.
  Le bandeau se met aussi en pause au survol.

## Arbitrages pris (à valider)

1. **Bouton / mention.** Le bouton reste `BOOK A MEETING` ; la mention devient
   `NOTED - WE GET BACK TO YOU WITHIN 24 HOURS`. Les deux promesses sont
   alignées sur le rendez-vous, qui est l'action réellement déclenchée. Si
   c'est l'analyse qu'on veut promettre, c'est le bouton qu'il faut changer
   (`GET YOUR ANALYSIS`), pas la mention.
2. **Logos clients — placeholders, liste étendue.** Le bandeau compte
   désormais **16 marques**, issues de la liste « safe » validée en interne :
   HP, Decathlon, UNESCO, L'Oréal, Danone, Société Générale, Galeries
   Lafayette, Celio, La Poste, Sisley, Bouygues Telecom, Studi, TV5 Monde,
   PMU, La Marine Recrute, Bioparc de Doué La Fontaine.

   Les fichiers n'ont toujours pas été fournis : `js/ui.js` génère des
   wordmarks navy, écart 44 px, fondus de 96 px. La durée du cycle est
   calculée depuis la largeur du jeu (`largeur / 126`), donc la vitesse de
   défilement ne change pas quand on ajoute des marques — le jeu fait
   maintenant ~3020 px et défile en ~19 s. Remplacer `CLIENTS` par les vraies
   silhouettes navy en gardant les couples largeur/hauteur. HP et UNESCO sont
   à 78 % d'opacité (aplats pleins). « Bioparc de Doué La Fontaine » s'affiche
   en « BIOPARC », nom complet en `aria-label` : en toutes lettres le wordmark
   tombait à 10 px.

   **À trancher** : *Celio* vient de la maquette Figma mais ne figure pas sur
   la liste « safe ». Il est conservé pour l'instant — à confirmer ou à
   retirer. Les marques du « cas par cas » (LVMH, Chanel, 3DS) ne sont pas
   intégrées.
3. **Logos plateformes — placeholders.** Mêmes réserves que le brief : les
   chartes des plateformes interdisent la recoloration. Les glyphes actuels
   (`window.LicterIcons`) sont des tracés monochromes qui prennent la couleur
   du contexte, à remplacer par les assets officiels avant mise en ligne — sur
   fond clair, la version couleur officielle passe d'ailleurs bien mieux
   qu'elle ne passait sur le navy.
4. **Écran 2 en deux colonnes.** À gauche les quatre questions du client
   (liste cliquable à flèche) suivies du lien « Discover the use cases » ;
   à droite la barre d'onglets puis la console. Les questions sont communes
   aux quatre onglets : c'est la console qui change de catégorie. Inventer
   seize questions aurait été du remplissage — à remplacer par la vraie
   matrice quand elle existe.

   La console reprend le principe de la fenêtre produit de topo.io, transposée
   à la charte : carte translucide à halo ambre, en-tête (pastille + libellé +
   indicateur + sous-titre), rail de répartition à barres, courbe en aire sur
   douze points, légende en pied. Onglets juste au-dessus, tout centré sur la
   colonne.

   **Fond du bloc : généré, pas photographique** (`.field` dans
   `css/styles.css`). Là où topo.io met une photo de ciel, on a une **nappe
   de lumière chaude** — un halo ambré large et bas, un accent en haut à
   droite, un halo blanc, et un voile blanc vertical — plus un **quadrillage de points** (26 px, navy à 12 %, masqué
   en fondu) qui évoque le papier millimétré plutôt qu'une texture décorative.

   *Version précédente abandonnée* : un lavis gris de la charte, qui servait à
   détacher la console blanche. Une fois le voile crème ajouté par-dessus la
   carto (arbitrage 17), ces deux gris se superposaient et le bloc lisait
   comme une ombre sale. La console se détache maintenant sur sa seule ombre
   portée, et la nappe n'a plus qu'à porter la chaleur.

   *Second réglage* : **deux** halos ambrés se trouvaient derrière la barre
   d'onglets, ce qui lui donnait une auréole jaune. Celui de la nappe, centré
   à `50% 14%`, est descendu à `50% 62%`, élargi et affaibli (.26 → .13) ;
   celui de la console — ancré sur son bord haut et débordant de 60 px vers le
   haut, donc pile autour de la pilule — a été **supprimé**, la console se
   détachant déjà sur son ombre portée. La pilule est passée à 86 % de blanc
   pour reposer sur son propre fond. Aucun fichier à livrer,
   net à tous les DPI, insensible au recadrage, et une dérive très lente
   (64 s, `transform` uniquement, coupée sous `prefers-reduced-motion`).
   Le dégradé de masque en haut et en bas évite la bande horizontale qui
   couperait la page. Contrepartie assumée : dans cette zone la nappe atténue
   la carto — c'est ce qui détache le bloc et fait lire la console comme une
   fenêtre posée dessus.
5. **Chiffres de la console** (+23 %, +17 %, ×2.4, +41 %, les courbes et
   toutes les répartitions du rail) : illustratifs. Le +23 % vient du croquis
   client, le reste est à remplacer par de vraies mesures avant publication.
6. **Contenu des menus déroulants.** Les quatre catégories reprennent celles
   des onglets, la colonne annexe de `USE CASES` reprend les quatre questions
   du client, et `TECH & TOOLS` liste les six plateformes du brief plus
   Search et Generative AI (cités dans la description du hero). En revanche
   **les phrases de description sont de moi** — à relire ou remplacer.
   `OFFERS` et `WHY LICTER` restent de simples liens : pas de contenu réel
   pour les remplir. Ajouter un panneau = une entrée dans `MENUS`
   (`js/ui.js`) et un `data-menu` sur le lien.
7. **Badge « Backed by Y Combinator » : non intégré.** C'est une affirmation
   vérifiable publiquement ; à confirmer avant de l'afficher.
8. **Grandir plutôt que resserrer.** Sur un grand écran, le problème n'est
   pas l'espace entre les blocs mais la taille des blocs : laissés à leur
   dimension de 1097 px, ils flottent. Au-delà de 1248 px de large, tout
   grandit avec la colonne — H1 56 → 78 px, description 14 → 18, champ
   460 → 610 de large et 48 → 60 de haut, bouton 159 → 204, navbar 46 → 58,
   logo 44 → 56, logos clients ×1.28, et de même sur l'écran 2 (titre
   44 → 58, sous-titre 26 → 32, questions 16 → 19, indicateur 34 → 42).
   Les tailles sont en `clamp(..., min(Xvw, Yvh), ...)` : elles suivent le
   plus petit des deux axes, donc un écran large mais court ne fait pas
   déborder le hero. En dessous de 1248 px, rien ne change : la maquette
   reste la référence exacte. Le hero est plafonné à 900 px de haut, ce qui
   laisse apparaître le haut de l'écran 2, qui sert d'appel au scroll (le
   libellé `EXPLORE` du brief a été retiré : le bloc suivant qui dépasse fait
   le même travail).
9. **Colonne centrée, élastique.** Toute la page vit dans une colonne
   centrée (`--maxw`, classe `.shell`) : 1097 px — la largeur de la maquette,
   gutters compris — comme plancher, puis 88 vw jusqu'à 1420 px. Au-delà de
   1440 px de viewport, les titres et le corps montent d'un cran (56 → 64 px
   pour le H1) pour rester en proportion. Le bandeau clients garde son débord,
   mais à l'intérieur de cette colonne.
   La carto, elle, grandit à ~55 % de la vitesse de l'écran (plafond 1750 px
   de repère) : elle couvre un grand écran sans que les amas ne deviennent
   énormes. Le réseau de fond et la poussière sont indexés sur la surface
   réelle — grille jusqu'à 12 × 7 cellules — pour que les bandes latérales
   restent peuplées, et un léger vignettage fixe assombrit les bords.
10. **Carte et scroll.** Les communautés vivent dans l'écran 1 et défilent en
   parallaxe à 0.3 ; le réseau de fond et la poussière couvrent toute la
   page. Sous 820 px, la carte est calée sur la largeur plutôt que recadrée,
   et la densité descend jusqu'à 50 %.

11. **Arrière-plan : réseau, pas constellations.** Le brief demandait des
    figures où chaque point n'est relié qu'à ses deux plus proches voisins,
    plus des filaments longs entre figures éloignées. Appliqué à la lettre,
    ça produit exactement un ciel étoilé — des polygones anguleux et de
    grandes diagonales qui traversent la page. Or le sujet est le social
    listening : le fond doit lire comme une toile de communautés reliées.

    La couche a donc été refaite sur le même objet que le premier plan, une
    échelle en dessous : une petite communauté par cellule de grille (9 à 18
    points, distribution gaussienne), un **maillage interne** (toutes les
    paires sous 46 px, degré plafonné à 4) au lieu de la chaîne à deux
    voisins, un nœud central légèrement plus gros qui fait office de mini-hub,
    et des **ponts vers les communautés adjacentes uniquement** — plus aucune
    ligne longue en travers de la page. Une communauté de fond sur sept prend
    l'ambre, pour que l'arrière-plan appartienne à la même famille que les
    amas du premier plan.

12. **Circulation sur l'arrière-plan.** Les amas principaux occupent le
    centre-droit : la moitié gauche n'avait aucun mouvement. Le réseau de
    fond sert donc aussi de graphe de circulation — ses arêtes sont
    enregistrées pendant qu'il est dessiné, une seconde table d'adjacence est
    construite dessus (en pixels, alors que celle du premier plan est en
    unités de maquette), et 46 voyageurs y marchent.

    Deux détails qui comptent : les points de départ sont **tirés dans une
    liste pré-filtrée** des nœuds de gauche plutôt que tirés au hasard puis
    rejetés — le rejet consommait les essais et la gauche restait deux fois
    moins animée ; et les délais de départ sont exprimés **en secondes** puis
    convertis avec la vitesse de chaque voyageur. Passés en distance, comme
    c'était le cas au départ, les points d'arrière-plan (plus lents)
    attendaient onze secondes avant d'apparaître.

13. **Console en deck animé** (réf. : les templates de showreel Reelfolio).
    La console n'est plus une carte posée : c'est une pile de trois cartes en
    perspective (1600 px), dont deux dépassent derrière la première.

    - **Construction à l'entrée** : la pile s'assemble au premier passage dans
      le viewport, carte du fond d'abord, décalages de 0.04 / 0.16 / 0.30 s.
    - **Changement d'onglet** : la carte de devant pivote et s'éloigne
      (`rotateY(-13deg)` + `translateZ`), la pile avance d'un cran, la
      nouvelle arrive de l'autre côté. 220 ms de sortie, 440 ms d'entrée.
    - **Inclinaison au curseur** : ±7° en Y, ±4.5° en X, suivies en `rAF`.
      Désactivée sans survol (tactile).
    - **Flottement** : ±5 px sur 14 s.
    - Tout est coupé sous `prefers-reduced-motion`.

    Deux précautions qui ne se voient pas : les animations sont en
    `animation-fill-mode: backwards` et non `both` — chacune se termine sur
    l'état naturel de l'élément, donc une animation qui ne démarre jamais
    (onglet en arrière-plan) laisse la console **visible** au lieu de la figer
    invisible. Et la révélation a trois déclencheurs (observer, test de
    position au scroll, minuteur de secours à 4 s) : un reveal qui ne part pas
    laisserait la console invisible pour toujours.

14. **Chorégraphie d'entrée et animation des données.** Quatre couches, en
    plus du deck :

    - **Hero** : les blocs entrent en cascade au chargement (en-tête, accroche,
      titre, description, formulaire, bandeau, footer), 90 ms d'écart, et les
      deux lignes du titre sont décalées de 100 ms entre elles.
    - **Écran 2** : révélation au scroll (observer + test de position + filet
      de sécurité à 6 s), les quatre questions arrivant une par une avec
      70 ms d'écart.
    - **Données** : à chaque rendu de la console — au chargement comme au
      changement d'onglet — la courbe **se dessine** (`stroke-dasharray`
      calculée depuis `getTotalLength()`), l'aire se remplit derrière, les
      douze points apparaissent en cascade, les barres du rail **poussent**
      jusqu'à leur valeur, et l'indicateur **compte** de 0 à sa valeur en
      820 ms.
    - **Menus** : les entrées des panneaux déroulants entrent décalées de
      35 ms.

    La règle qui masque les blocs avant révélation est portée par une classe
    `reveal` posée par le script sur `<html>` : sans JS, ou sous
    `prefers-reduced-motion`, rien n'est jamais masqué et la page s'affiche
    telle quelle. Même logique que pour le deck : aucune animation ne doit
    pouvoir laisser un bloc invisible.

15. **Contenu : d'où il vient, et ce qui est de moi.**

    **Repris de la propale** (`PROPALE LICTER - V3.pptx`, dont la police
    substitue les glyphes — O→Q, N→H — il a fallu la décoder) : la taxonomie
    des quatre familles **Communication / Brand health / Audiences / Trends &
    innovation** et leurs **douze cas d'usage**, mot pour mot. Les onglets de
    la home ont été renommés en conséquence (`INFLUENCE` → `COMMUNICATION`,
    `BRAND` → `BRAND HEALTH`, `TRENDS` → `INNOVATION`) et les trois questions
    affichées changent maintenant avec la famille sélectionnée.

    **Repris de licter.com** (consulté en septembre 2026) : les trois offres
    (Social Insights « forfait fixe, études illimitées » ; Vigie 360 « alerte
    en 15 min, 24/7 », 20+ langues, 25+ clients protégés ; Social Listening as
    a Service), les quatre couches de méthode (social listening, audience
    intelligence, digital panel, search listening), l'origine (créée en 2022
    par Antoine Khaitrine et Adrien Krebs, ex-cellule Data & Digital Analysis
    de l'Élysée), les trois segments servis, les langues de l'équipe, et les
    chiffres : **50+ clients, 160+ projets, ~3 Md de profils, Top 50 mondial
    SI Lab 2024, 5 000+ critères de persona**.

    **De moi** : toute la rédaction anglaise (titres, descriptions, lignes
    « You get », textes des blocs de conversion). À relire par Licter —
    en particulier les formulations qui ressemblent à des engagements
    (« 15-minute alerts », « unlimited studies »). Les chiffres sont ceux
    revendiqués publiquement par Licter : à revalider avant mise en ligne.

    **Outils** : le panneau « TECH & TOOLS » et une section de `tech-tools.html`
    listent les quatre plateformes réellement utilisées — **Talkwalker,
    Visibrain, YouScan, SoPrism**. Les descriptions d'une ligne sont de moi et
    décrivent ce pour quoi chaque outil est connu ; à relire par Licter. Les
    logos ne sont pas reproduits (marques tierces) : un monogramme tient la
    place, à remplacer par les vrais si les licences le permettent.

    **Restent des placeholders** : les logos clients (wordmarks texte), les
    glyphes de plateformes, les chiffres de la console de la home, et le blog
    — quatre thèmes réels mais aucun article, à brancher sur le vrai blog.

16. **Funnel d'acquisition, repris de Flowt.** Le modèle de flowt.fr tient en
    **trois chemins selon l'intention**, et c'est ça qui a été transposé — pas
    la mise en page.

    | Intention | Flowt | Licter |
    |---|---|---|
    | Froide | Guide « Les 10 étapes clés pour implémenter l'IA », bandeau collant en haut de toutes les pages | [`guide.html`](guide.html) — « Les 12 questions auxquelles la social data répond mieux qu'une étude », même bandeau collant ambre |
    | Tiède | `/audit-diagnostic-data-ia/` — 4 étapes, scoring de maturité, quick wins, roadmap | [`diagnostic.html`](diagnostic.html) — mêmes 4 étapes transposées aux 6 dimensions de la social data |
    | Chaude | « Réserver un appel » | [`book-a-meeting.html`](book-a-meeting.html) — 30 min, ce qui se passe pendant l'appel |

    Les détails repris tels quels parce qu'ils font le travail : le **bandeau
    collant** sur toutes les pages, les **lignes de réassurance** (« 100 %
    gratuit · envoi immédiat », « sans engagement · réponse sous 24 h »), le
    **formulaire court** pour le guide (4 champs) contre le **formulaire
    qualifiant** pour le diagnostic (5 champs dont un champ contexte libre),
    et le CTA à la première personne (« Request **my** diagnostic »).

    La home reprend aussi l'ordre de Flowt : hero + CTA → logos clients →
    **chiffres de preuve** → use cases → **offres** → **méthode en 4 étapes**
    → **FAQ (5 questions)** → **trois portes d'entrée**. S'y ajoutent les CTA
    de milieu de page (« Talk to an expert ») et de pied de page
    (« Request a diagnostic »), comme chez eux.

    **Ce qui n'a pas été repris** : leurs chiffres (4× ROI, 98 % de
    satisfaction, < 3 semaines) — ce sont les leurs, pas ceux de Licter. Les
    chiffres affichés restent ceux revendiqués par Licter.

    **Le guide n'existe pas encore.** Le contenu est prêt (les 12 cas d'usage
    de la propale font les 12 chapitres), mais il faut produire le PDF et
    brancher l'envoi avant d'activer le bandeau en production.

17. **Lisibilité du texte sur la carto (thème clair).** Deux réglages, parce
    qu'un seul ne suffisait pas :

    - **Le masque de lisibilité** est passé de 50 % à 86 % de retrait, puis
      redescendu à **42 %** une fois les feuilles de l'arbitrage 18 en place :
      à trois couches (masque + voile + feuille), 86 % effaçait complètement
      le réseau derrière le texte. Dégradé élargi de 26 à 34 px. La valeur de 50 % venait du brief, écrite
      pour un fond navy : un trait clair sur sombre se lit à travers le texte
      bien moins qu'un trait sombre sur crème.
    - **Un voile crème** (`--veil`) recouvre la carto dès qu'on quitte le
      hero : 0 dans le hero, jusqu'à 0.30 une fois dans le contenu, piloté au
      scroll en `requestAnimationFrame`. Les pages internes, qui n'ont pas de
      hero, démarrent directement voilées. La carto reste le sujet du hero et
      redevient une texture partout ailleurs.

18. **Une feuille de lumière par section.** Le masque de
    l'arbitrage 17 amincit la carto derrière le texte, mais sur des lignes
    pleine largeur (les étapes, la FAQ, les chiffres) le réseau passait encore
    entre les lignes. Ces blocs reposent désormais sur une **vraie surface** :
    un pseudo-élément blanc, sans bordure ni coin visible, débordant de
    22 × 30 px et **dissous en dégradé** — il lit comme de la lumière, pas
    comme une carte de plus.

    **Deux corrections successives.** D'abord, une feuille par *élément* (titre, liste,
    formulaire…). Une section avec un titre et une liste se retrouvait avec
    deux feuilles superposées, de largeurs différentes, et la couture se
    voyait. Il n'y en a plus qu'**une par section**, à **48 % d'opacité** avec
    un flou d'arrière-plan de 2.5 px : les pôles de communauté se lisent au
    travers, le texte reste net. Ensuite, ces feuilles débordaient verticalement (`inset:
    -14px`) et **se chevauchaient entre sections voisines**, puisque les
    sections se suivent sans marge. Le débord vertical est passé à zéro : les
    blocs portent déjà 48 à 84 px de padding, ce qui donne son air au texte,
    et la feuille du titre de page s'arrête net à son bord bas. Deux feuilles
    se touchent, aucune ne croise l'autre. Enfin, la feuille du titre de page
    se dessinant sur un bloc de 820 px alors que celle des sections suit la
    colonne entière, leurs bords droits ne tombaient pas au même endroit et la
    jonction lisait comme un escalier : `.page__head` occupe désormais toute
    la colonne et c'est le **titre** qui porte sa largeur maximale. Sous
    640 px, le débord latéral se resserre.

19. **Rythme des blocs et variantes d'animation.** Toutes les sections des
    pages internes suivaient le même gabarit — titre en haut, trois cartes
    identiques dessous — et la page se lisait comme une liste de la même
    chose. Deux gabarits alternent maintenant (au-delà de 900 px, en
    `:nth-of-type`, donc sans toucher au HTML des dix pages) :

    - **Sections impaires** : titre pleine largeur, et la **première carte est
      promue** — elle occupe deux colonnes, passe en deux colonnes internes
      (titre à gauche, texte à droite) et monte d'un cran en taille. Elle
      porte la section au lieu d'être un item parmi trois.
    - **Sections paires** : le titre passe dans une **colonne de gauche
      collante** (`position: sticky`) qui accompagne le défilement des cartes.

    L'animation suit le gabarit : les blocs pairs entrent par la gauche, les
    impairs par le bas, la carte promue arrive avec une légère mise à
    l'échelle, et les cartes d'une même rangée s'échelonnent de 70 ms. Au
    survol, un filet ambre se déploie verticalement sur le bord gauche de la
    carte — la même information que l'élévation, mais lisible.

    **Au passage** : les feuilles de lumière de l'arbitrage 18 avaient un
    bord franc à gauche et en bas, ce qui les faisait lire comme des dalles
    blanches flottantes. Elles sont désormais **masquées sur tous les côtés**
    par un dégradé radial.

20. **Moins d'amas, plus denses.** Demande de Licter, appliquée aux deux
    couches de la carto :

    - **Communautés principales** : 5 → **4** (steel supprimé), et les quatre
      restantes gonflées d'environ 45 % (core passe de 140 à 204 points).
    - **Satellites** : 5 → **2** (sage et ochre, les plus éloignés l'un de
      l'autre), chacun doublé et élargi.
    - **Ponts** : moins de paires de communautés, donc chaque paire porte plus
      de liens (6-7 → 9-12) — sans quoi le graphe se serait délité.
    - **Réseau d'arrière-plan** : la grille passe de 7 × 4 à **5 × 3** cellules
      de base (plafond 12 × 7 → 8 × 5), mais chaque communauté passe de 9-18 à
      **18-32 points**, avec un rayon de maillage porté de 46 à 54 px et un
      degré maximal de 4 à 5.

    Le nombre total de points bouge à peine — c'est la **répartition** qui
    change : quelques pôles francs au lieu d'un semis régulier.

21. **Stories sur la moitié droite du hero.** Un point qui circule *est* une
    story : un voyageur vivant situé dans la zone indiquée par Licter — de
    53 % à 97 % de la largeur, de 11 % à 77 % de la hauteur du hero, soit sous
    la navbar et au-dessus du bandeau clients — « s'ouvre » en carte **16:9**
    (en-tête plateforme, celle du voyageur et pas une au hasard, barre de
    progression, emplacement média, légende), tient 5,2 s, puis se referme.
    **Une seule carte à la fois**, garanti par deux verrous : la suivante
    n'est programmée qu'une fois la précédente retirée du DOM, *et* `open()`
    refuse d'ouvrir si une carte est encore présente — un retour d'onglet en
    avant-plan reprogrammait sinon une ouverture par-dessus la carte vivante.

    La carte est **ancrée sur la position réelle du point** au moment de
    l'ouverture, reliée à lui par un fil et une pastille de la couleur de sa
    communauté, et bascule à gauche du point si elle devait sortir du cadre.
    `js/cartography.js` expose pour ça `window.LicterCarto.pickTraveller()`,
    qui rend un voyageur vivant dans une zone donnée, en coordonnées écran.

    **Pour brancher les vraies vidéos** : la fonction `renderMedia()` dans
    `js/ui.js` ne renvoie aujourd'hui qu'un bouton lecture. Y retourner
    `<video src="…" autoplay muted loop playsinline></video>` suffit — le
    conteneur `.story__media` est déjà au format 16:9 avec `object-fit:
    cover`. Les légendes (« Story · 2 h », « Reel · 14 min ») sont des
    placeholders.

    Désactivé sous 900 px et sous `prefers-reduced-motion` ; en pause quand
    l'onglet passe en arrière-plan.

22. **Méthode et FAQ côte à côte, en accordéon.** Les quatre étapes de la
    méthode étaient une liste déroulée, la FAQ un accordéon, et les deux
    occupaient chacune une section pleine largeur — beaucoup de hauteur pour
    peu de densité. Elles sont désormais **dans un même bloc, en deux
    colonnes**, toutes les deux en accordéon : les étapes gardent leur
    numérotation dans l'en-tête dépliable (`.faq__n`) et leur description
    devient le contenu. Sous 900 px, les deux colonnes s'empilent.

23. **Ordre de la home revu.** Les chiffres de preuve puis les offres
    remontent juste après le bandeau de logos. L'ordre est désormais :
    accroche → logos clients → **chiffres** → **offres** → use cases →
    méthode & FAQ → trois portes d'entrée. La preuve sociale, la preuve
    chiffrée et la proposition commerciale se suivent, et le détail (les douze
    cas d'usage) vient après.

24. **Une page par plateforme, sur la structure Flowt.** Relevé sur
    `flowt.fr/technologies/agence-google-cloud-bigquery/` : hero → logos
    clients → pourquoi cette techno → approche en 3 étapes → atouts (4 cartes)
    → ce qu'on en fait → chiffres → cas clients → articles liés → FAQ →
    double CTA. Les quatre outils ont chacun leur page sur ce plan.

    **Deux écarts assumés** :
    - **Pas de « cas clients »** : Licter n'a pas d'études de cas publiables.
      Le bloc est remplacé par « Questions this platform answers », qui renvoie
      vers les cas d'usage correspondants — même fonction (montrer à quoi ça
      sert), sans inventer de références.
    - **« Articles liés » pointe vers les quatre fils du blog**, pas vers des
      articles : ils n'existent pas encore.

    Les chiffres affichés sont ceux de **Licter** (50+ clients, 20+ langues,
    15 min d'alerte, 3 Md de profils), jamais des chiffres attribués aux
    éditeurs. Les descriptions de ce que fait chaque outil sont de moi et
    **doivent être relues** : c'est le contenu le plus exposé à l'erreur
    factuelle de tout le site.

25. **Bascule EN / FR.** Un sélecteur `EN | FR` dans l'en-tête, sur toutes
    les pages. Le choix est mémorisé (`localStorage`) et suit la navigation.

    **Le mécanisme, et pourquoi celui-là** : plutôt qu'un second jeu de
    fichiers HTML à maintenir en parallèle (14 pages × 2), la traduction est
    appliquée à l'exécution. `js/fr.js` est un dictionnaire **indexé sur la
    chaîne anglaise**, `js/i18n.js` parcourt les nœuds de texte et remplace ce
    qu'il trouve. Conséquences assumées :

    - toute chaîne **absente du dictionnaire reste en anglais** — la
      dégradation est partielle, jamais cassée ;
    - un `MutationObserver` retraduit ce que `js/ui.js` rend après coup
      (menus, console, questions, cartes story) ;
    - le retour à l'anglais **recharge la page** : le HTML d'origine est la
      source de vérité, aucun dictionnaire inverse à maintenir ;
    - le français étant plus long, `html[lang="fr"]` élargit le bouton du
      formulaire (159 → 212 px) et réduit d'un cran le H1 du hero.

    **Couverture actuelle** : bandeau, navigation et ses trois panneaux, pied
    de page, formulaires, boutons, **toute la home**, et les titres /
    accroches / CTA des dix autres pages. **Le corps de texte des pages
    internes reste en anglais** — il suffit d'ajouter les entrées à
    `js/fr.js`, sans toucher au HTML.

26. **Le traitement visuel des blocs Flowt, pas seulement leur ordre.**
    L'arbitrage 24 reprenait l'enchaînement des sections ; celui-ci reprend la
    *forme* de quatre d'entre elles, relevée sur les captures de
    `flowt.fr/technologies/…`, et l'applique aux quatre pages plateformes :

    - **Approche en 3 étapes** (`.numbered`) : le numéro dans un carré bordé
      d'ambre, le titre en petites capitales espacées, le texte dessous —
      trois colonnes sans carte ni fond, séparées par le seul rythme.
    - **Ce qu'on en fait** (`.solutions`) : trois cartes à bandeau supérieur
      (`.solution__band`, dégradé ambre → transparent) dont le contenu est
      une liste à puces ambre, et non plus un paragraphe. C'est le bloc qui
      porte le concret : il fallait qu'il se lise en diagonale.
    - **Questions / Articles** (`.covers`, `.cover-card`) : chaque carte
      s'ouvre sur une zone de couverture teintée (`.cover`) portant un
      sur-titre et un titre en capitales, façon vignette d'article. Faute
      d'images, la couverture est un dégradé — ambre pour les cartes
      « questions », gris-bleu pour les cartes « lecture » —, ce qui
      distingue les deux familles sans légende.
    - **Bande de rappel** (`.band`) : un cadre bordé, fond transparent, où le
      nom de la plateforme est surligné d'ambre (`.band__title em`), suivi
      des deux CTA — dont un bouton plein navy (`.btn--solid`), le seul du
      site, réservé à cette bande pour qu'il reste un point d'appui unique.

    **Écarts** : les sur-titres des sections passent en `//` + libellé
    (`.block__kicker--slash`) comme chez Flowt ; les couvertures restent des
    dégradés tant que Licter n'a pas fourni de visuels ; le CTA principal du
    hero pointe désormais sur `book-a-meeting.html` plutôt que sur le
    formulaire de la home, pour ne pas renvoyer l'utilisateur en arrière.

27. **Cartes à dégradé sur `tech-tools.html`.** Reprise d'un composant
    shadcn/framer-motion fourni par Licter (badge + titre + texte + CTA +
    visuel d'angle, survol qui soulève la carte). Les quatre plateformes
    remplacent la grille de cartes plates : c'est le seul endroit du site où
    il y a exactement quatre entités de même rang, chacune avec sa page.

    **Ce qui a été transposé, et pourquoi** :
    - **Pas de React.** Le site n'a pas de build step : `cva` devient quatre
      classes modificatrices (`.gcard--ochre / --slate / --cream`) et
      `framer-motion` devient deux transitions CSS. Le survol soulève de 4 px
      et agrandit de 1,2 % — assez pour répondre, pas assez pour flotter.
    - **Les quatre dégradés restent dans la charte.** L'original propose
      orange / gris / violet / vert ; la charte n'a que navy, ambre, crème et
      gris. Les quatre teintes sont donc ambre, ocre profond (`#C08C0E`),
      navy dilué et gris neutre — deux chaudes, deux froides, ce qui sépare
      les cartes deux à deux sans rien inventer.
    - **Le visuel d'angle est un mini-amas**, généré en SVG avec le même
      vocabulaire que la cartographie de fond (un hub, deux satellites, des
      liens locaux et des ponts). Chaque carte a le sien, déterministe, tiré
      du nom de la plateforme. Il pivote de 3° et grossit au survol. Aucun
      asset à fournir, et il occupe la place que les logos éditeurs n'ont
      jamais remplie : les quatre 404 de `assets/img/tools/` ont disparu de
      cette page.
    - **La section sort du rythme alterné** (`.block--wide`) : elle prenait
      la colonne étroite de droite, où un titre de 32 px ne tient pas. Le
      modificateur est générique, réutilisable pour toute section dont le
      contenu a besoin de la pleine largeur.
    - **Spécificité** : `.reveal [data-reveal].is-in` impose
      `transform: none` avec une priorité supérieure à `.gcard:hover` — le
      survol était mort une fois la carte révélée. D'où la règle
      `.gcard[data-reveal].is-in:hover`, qui reprend aussi la transition
      (0,28 s au lieu des 0,6 s du reveal).
    - Les huit chaînes nouvelles sont dans `js/fr.js` : le bloc bascule en
      français comme le reste.

    Reste ouvert : si Licter fournit les logos éditeurs, ils peuvent prendre
    la place du mini-amas sur ces quatre cartes — mais le mini-amas est plus
    cohérent avec le reste du site, et ne pose aucune question de droit
    d'usage des marques.

28. **Champ d'icônes flottantes sur « Where the data comes from ».**
    Second composant fourni par Licter (hero plein écran, icônes qui fuient
    le curseur). Il n'a pas été posé en hero : la cartographie animée occupe
    déjà le fond de toutes les pages, et deux systèmes flottants dans le même
    écran font du bruit. Il est donc devenu un **champ délimité** dans la
    section des sources, la seule du site où des logos tiers ont une raison
    d'être — ce sont littéralement les sources de la donnée.

    **Ce qui a été transposé** :
    - **Neuf glyphes monochromes** dessinés à la main (TikTok, Instagram, X,
      LinkedIn, YouTube, Facebook, Google, Amazon, et une étincelle pour les
      assistants). L'original est en couleurs de marque : neuf palettes
      étrangères dans une charte qui n'a que navy, ambre, crème et gris,
      c'était non. Navy à 50 %, **ambre au moment où le glyphe est repoussé**.
    - **Une écoute `pointermove` et une boucle `rAF` pour tout le champ**, au
      lieu d'un `useSpring` et d'un listener par icône. Le ressort devient un
      lerp amorti (0,14) : à cette taille, la différence ne se voit pas. La
      boucle ne tourne que quand la section est à l'écran
      (`IntersectionObserver`) et s'arrête d'elle-même quand tout est au
      repos.
    - **Les positions sont mesurées, pas devinées** : la section réserve une
      bande libre au-dessus du titre (`padding-top`), et les neuf glyphes
      occupent cette bande plus la zone à droite du titre, qui s'arrête à
      64 % de la largeur. Rien ne passe derrière le texte.
    - **Dégradations** : sous 900 px il ne reste que quatre glyphes, plus
      petits, plus discrets, décalés sous le bandeau ; un `pointerdown` qui
      n'est pas une souris coupe la répulsion (un doigt n'a pas de survol) ;
      `prefers-reduced-motion` fige tout.

    **Défaut trouvé en le testant** : le bandeau du haut est `sticky` et fait
    38 px, et aucune section n'avait de `scroll-margin-top`. Toute arrivée
    par une ancre — dont le lien « Where the data comes from » du menu
    déroulant — déposait donc le haut de la section sous le bandeau, ce qui
    mangeait exactement la bande où vivent les glyphes : on arrivait sur le
    titre et les cartes, sans rien voir du champ. `scroll-margin-top: 58px`
    sur toute section portant un `id` corrige le champ **et** toutes les
    autres ancres du site, qui avaient le même défaut sans que ça se voie.

    **Point à trancher côté Licter, pas côté code** : les logos de réseaux
    sociaux employés pour désigner des sources de données relèvent de l'usage
    nominatif, ce qui passe en général, et le traitement monochrome réduit
    encore le risque — mais c'est une décision de marque. Les **logos
    clients**, eux, demandent l'accord de chacun : c'est sans doute pourquoi
    le marquee affiche des noms en texte et non des logos, et je ne l'ai pas
    changé.

## Reste à faire

- Brancher les formulaires sur un vrai endpoint (`js/ui.js`, deux
  commentaires `wire to the real endpoint here` : capture email et formulaires
  du funnel).
- Produire le PDF du guide et brancher son envoi automatique.
- Fournir les clips des stories du hero (`renderMedia()` dans `js/ui.js`).
- Logos des quatre éditeurs (`assets/img/tools/*.png`) : encore attendus
  par le dropdown « Tech & Tools », qui retombe sur un monogramme. La page
  `tech-tools.html` ne les demande plus (voir l'arbitrage 27).
- Compléter `js/fr.js` avec le corps de texte des pages internes (cas
  d'usage, offres, pourquoi, techno, clients, blog, guide, diagnostic, RDV).
- Relire les quatre pages plateformes : ce que fait réellement chaque outil
  chez Licter, et ce qu'on a le droit d'en dire publiquement.
- Blog : les quatre fils existent, les articles non — à brancher sur le vrai
  blog Licter.
- Pages légales (mentions, confidentialité) : absentes, le pied de page les
  attend.
- Accessibilité : sur la crème, le texte courant `#56606A` passe l'AA (5.4:1)
  et le navy est à 15:1. Restent sous le seuil pour du petit texte le gris
  `#84919A` (3:1, utilisé sur `EXPLORE` et les libellés de rail) — à revoir si
  l'AA est un critère. L'ambre pur n'est jamais utilisé pour du texte.
- Le token GitHub du dépôt Licter était expiré — à renouveler avant le
  premier push.
