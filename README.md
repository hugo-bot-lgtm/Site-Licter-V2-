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

28. **Icônes flottantes : essayé, retiré.** Licter avait fourni un second
    composant (hero plein écran, icônes qui fuient le curseur) à placer sur le
    site. Il a été installé dans la section des sources de `tech-tools.html`,
    en deux versions, puis **supprimé à la demande de Licter** — l'élément ne
    convenait pas esthétiquement. Le code est parti avec : markup, styles et
    boucle d'animation. Ce qui reste consigné, parce que ça vaut pour la
    suite :

    - **Ne pas le poser en hero.** La cartographie animée occupe déjà le fond
      de toutes les pages. Deux systèmes flottants dans le même écran font du
      bruit, quelle que soit la qualité du second.
    - **Le premier jet mettait les glyphes dans des pastilles blanches
      bordées, alignées en bande au-dessus du titre.** Retour : « on dirait
      que c'est juste posé là ». Juste : la pastille est un vocabulaire
      d'interface que ce site n'a nulle part, et une bande libre au-dessus
      d'un titre n'offre qu'une dimension, donc forcément une rangée.
    - **Le second jet en faisait des nœuds câblés au réseau**, positions
      générées sur des anneaux pour qu'aucun trait ne se croise, avec des
      points anonymes pour que les plateformes ne soient que quelques nœuds
      parmi d'autres. Techniquement propre, toujours pas retenu. Conclusion
      utile : sur ce site, **le fond est déjà l'élément graphique** ; tout ce
      qu'on ajoute à côté entre en concurrence avec lui.

    Un défaut trouvé en le testant a en revanche été **gardé** : le bandeau du
    haut est `sticky` et fait 38 px, et aucune section n'avait de
    `scroll-margin-top`. Toute arrivée par une ancre déposait le haut de la
    section cible sous le bandeau. `scroll-margin-top: 58px` sur toute section
    portant un `id` corrige toutes les ancres du site.

29. **La console devient un tableau de bord.** Licter a fourni une capture
    d'un kit admin (Shadcnblocks) : la version précédente — un chiffre, une
    courbe et cinq barres horizontales — était jugée trop pauvre en données.
    Le contenu du panneau est refait sur ce modèle, dans la charte, **sans
    toucher aux animations** déjà en place.

    **La structure**, reprise de la capture : une barre de tête avec trois
    puces (90 days / 12 months / Export, décoratives), puis trois cellules de
    KPI avec chiffre, variation et micro-courbe, la figure de tête à côté ;
    en dessous la courbe de tendance en large et un histogramme *owned /
    earned* par mois ; en bas un tableau des sources (part, volume, variation
    à 30 jours) et une liste de signaux à surveiller. Huit cellules, séparées
    par des filets d'1 px : la grille a un `gap: 1px` sur fond `--line`, donc
    les rainures *sont* les traits — pas de bordure à gérer.

    **Les animations existantes couvrent tout le nouveau contenu**, en
    généralisant leurs sélecteurs plutôt qu'en les dupliquant : `[data-draw]`
    pour tout tracé qui se dessine (la grande courbe et les trois
    micro-courbes), `[data-grow]` pour toute barre qui pousse (le tableau),
    `[data-count]` pour tout chiffre qui monte (les trois KPI, la figure de
    tête, le total). Les colonnes de l'histogramme ont leur propre montée
    depuis l'axe, décalée mois par mois. Le deck, la distribution de carte au
    changement d'onglet et l'inclinaison au scroll sont inchangés.

    **Deux pièges rencontrés** :
    - La cellule de la figure de tête s'appelait `.hero`. C'est déjà le nom de
      la section d'en-tête de la page : la cellule héritait de ses règles et
      faisait **900 px de haut**. Renommée `.vizhero`. Un composant injecté en
      JS dans une feuille de style unique doit préfixer ses classes.
    - Le canevas de la cartographie se dimensionnait sur `window.innerWidth`,
      qui **inclut la barre de défilement** : il dépassait de 18 px sur mobile.
      Corrigé sur `clientWidth`, avec un recalcul différé, parce que
      l'apparition d'une barre de défilement ne déclenche pas de `resize`.

    **Sur mobile**, le tableau de bord complet montait à 1 400 px. Sous 640 px
    il ne garde que les trois KPI sur une ligne, la figure de tête, la courbe
    et le tableau des sources — 712 px, lisible d'un coup d'œil.

    **Les cellules de KPI, corrigées après coup.** La micro-courbe était posée
    à droite du chiffre : dans une cellule de 142 px, soit 108 px de contenu,
    un chiffre de 91 px et une courbe de 58 px ne tiennent pas côte à côte —
    ils se chevauchaient. La courbe passe donc **sous** le chiffre, sur toute
    la largeur, et le libellé a une hauteur minimale de deux lignes pour que
    les trois chiffres restent alignés quelle que soit la longueur du libellé.
    Sur mobile la courbe disparaît : les trois KPI y tiennent sur une ligne.

    **La colonne de gauche suit.** Une fois la console densifiée, la liste de
    questions à côté paraissait vide. Elle emprunte la même grammaire sans
    devenir un second tableau de bord : une tête avec la puce ambre, le nom de
    la famille (qui change avec l'onglet) et un compteur `03 / 12` dans la
    même puce que les `90 days` de la console ; des lignes **numérotées**
    `01 / 02 / 03` sur filets ; une ligne de pied qui répond à la légende de
    la console. Les deux moitiés se lisent comme un seul instrument, et la
    gauche reste plus légère — c'est la voix éditoriale, pas la donnée.

    **Tous les chiffres restent illustratifs** et doivent être remplacés par
    Licter avant mise en ligne. Ils sont désormais bien plus nombreux : c'est
    autant de matière à relire.

30. **Les interviews clients, reprises de l'ancien site.** Bloc « Ils le
    racontent mieux que nous. En vidéo. » sur `clients.html`, entre les quatre
    questions et le CTA de fin.

    **Les vidéos sont les vraies.** Elles ont été retrouvées sur la chaîne
    **Audience First by Licter** (`youtube.com/@audience_first`, 427 vidéos) :

    | Marque | Invité·e | Durée | ID |
    |---|---|---|---|
    | Groupe SEB | Hélène Classine | 1:03:49 | `1PXRd4_JgEc` |
    | Dassault Systèmes | Jean-Stéphane Bou | 1:00:32 | `cnwA-t0Vqk4` |
    | Paris 2024 | C. Legall | 55:08 | `l-OevQ4q8js` |

    Les trois durées correspondent exactement à celles de l'ancienne maquette,
    ce qui confirme que ce sont bien ces épisodes-là.

    **Choix techniques** :
    - **Pas de lecteur embarqué.** La vignette vient de
      `i.ytimg.com/vi/<id>/maxresdefault.jpg` (repli sur `hqdefault`) et le clic
      part sur YouTube dans un nouvel onglet. Un `iframe` YouTube dépose des
      cookies tiers sur tout visiteur qui n'a rien demandé ; une image, non.
      C'est aussi beaucoup plus léger.
    - **La citation sort de la vignette.** Les miniatures portent déjà leur
      citation incrustée en français : un calque par-dessus faisait double
      emploi. La version anglaise est passée sous l'image, où elle sert de
      titre de carte, avec `MARQUE · Invité·e` en dessous.
    - **Le sur-titre n'est pas « NOS CLIENTS »**, conformément à la note de
      Licter sur l'ancienne maquette (« ils nous font confiance » plutôt que
      « nos clients »). Ce n'est pas non plus « THEY TRUST US » : la page
      ouvre déjà là-dessus pour le mur de logos. C'est **« IN THEIR OWN
      WORDS »** — même prudence, sans répétition.
    - **Capture email en pied de bloc**, comme demandé sur la note : « Get the
      next one », branchée sur le même gestionnaire que les autres
      formulaires du site (donc toujours sans endpoint réel).
    - **La chaîne est atteignable de partout** : « Audience First ↗ » dans la
      colonne COMPANY du pied de page des quatorze pages, et « the channel ↗ »
      dans le bloc lui-même. C'était le seul lien sortant du site ; jusque-là
      on parlait de la chaîne sans jamais y mener.

31. **Le mur d'interviews tourne tout seul.** Demande de Licter : que les
    vidéos changent de temps en temps plutôt que d'être figées sur trois.

    **Le vivier, d'abord.** La chaîne annonce 427 vidéos, mais l'onglet
    *Videos* n'en contient que **45** : les ~380 autres sont des Shorts, dans
    leur propre onglet. Sur ces 45, beaucoup sont des webinars, des
    masterclasses, des bandes-annonces de podcast ou des entretiens
    politiques. Un bloc titré « ils le racontent mieux que nous » ne peut pas
    tirer au sort un short sur le Rafale ni une interview d'ancien ministre.
    Le vivier retenu est donc **douze interviews de marques et
    d'institutions**, vérifiées une à une : SEB, Dassault Systèmes, Paris
    2024, SNCF, Orange, L'Oréal, AXA, Kantar, LVMH, Ville de Paris, Transat
    Café l'Or, France Digitale.

    **Pourquoi une liste en dur et pas un flux.** Trois options :
    l'API YouTube Data mettrait une clé dans du JavaScript public pour une
    liste qui bouge une fois par semaine ; le flux RSS de la chaîne n'envoie
    pas d'en-tête CORS, donc le navigateur ne peut pas le lire ; une fonction
    serverless marcherait mais ajouterait un back-end à un site qui n'en a
    aucun. La liste est donc figée dans `js/voices.js`, et
    `tools/harvest-voices.md` explique comment la régénérer en une minute.
    Si Licter veut du vraiment temps réel, la fonction Vercel est la voie —
    c'est une demi-journée et une clé d'API à créer.

    **Le comportement** : une seule carte change à la fois, toutes les 7 s, en
    tourniquet gauche → milieu → droite, avec fondu. La rotation s'arrête
    quand le bloc sort de l'écran, quand l'onglet passe en arrière-plan, et
    **quand le curseur ou le clavier est sur les cartes** — on ne change pas
    une carte que quelqu'un est en train de lire ou de cliquer. La miniature
    suivante est préchargée avant l'échange, avec un délai de secours de 1,2 s
    pour ne jamais attendre une image lente.

    **Sous 860 px et en `prefers-reduced-motion`, la rotation est coupée** :
    les cartes y sont empilées, une seule est visible, et la faire changer
    sous le pouce du lecteur serait hostile. À la place, un tirage différent à
    chaque visite — la variété sans le mouvement.

    **Deux pièges** :
    - **La grille YouTube recycle ses nœuds** : lire la page une fois après
      avoir scrollé ne rend que 45 cartes au maximum, jamais l'historique. Il
      faut accumuler pendant le défilement. C'est ce que fait le script de
      `tools/harvest-voices.md`.
    - **`maxresdefault.jpg` n'existe pas pour toutes les vidéos** (ici :
      L'Oréal), et YouTube répond alors une image grise de 120×90 **avec un
      statut 200** — donc `onerror` ne se déclenche jamais et la carte affiche
      un placeholder. Les cartes partent donc sur `hqdefault.jpg`, qui existe
      toujours et se recadre exactement sur le 16:9, et ne montent en maxres
      qu'une fois celle-ci prouvée réelle.

    Les trois cartes écrites en dur dans `clients.html` restent les plus
    fortes : c'est ce que voit un visiteur sans JavaScript.

32. **Neuf articles de blog, en contenu de remplissage.** Demande de Licter :
    peupler la partie blog. Ce sont des **textes d'attente écrits par moi**,
    pas de l'expertise Licter relue. Chaque page porte un commentaire HTML en
    tête qui le dit.

    **Ce que j'ai refusé de fabriquer** : aucun résultat client, aucun chiffre
    présenté comme une étude, aucune citation attribuée à une personne réelle,
    aucun nom d'auteur inventé — la signature est « Licter analysis team ».
    Les articles tiennent par le raisonnement, pas par des données que
    personne n'a produites. C'est la seule façon d'écrire du faux contenu qui
    ne devienne pas un problème s'il part en ligne par accident.

    **Répartition** sur les quatre fils qui existaient déjà : 2 en
    *foresight*, 3 en *monitoring & social listening*, 3 en *consumer
    insights*, 1 en *influence*.

    **Structure d'une page article** : sur-titre du fil, titre en casse
    normale (`.page__title--article` — les autres pages crient leur titre en
    capitales, un article non), chapô, signature (date · temps de lecture ·
    équipe), puis le corps en `.prose` avec une citation détachée après la
    première section et un encadré « what to take away » en fin. Ensuite trois
    cartes « keep reading » et le formulaire de capture.

    **Trois décisions de mise en page** :
    - La largeur de lecture est plafonnée en **caractères** (`68ch`), pas en
      pixels : elle tient quelle que soit la taille de police du lecteur.
    - `.prose` a reçu **la feuille de lumière** des autres blocs. Sans elle,
      le corps de texte reposait directement sur la cartographie — exactement
      le défaut de lisibilité corrigé deux fois ailleurs.
    - L'index et les blocs « keep reading » utilisent `.block--wide` : neuf
      cartes n'ont rien à faire dans la colonne étroite du rythme alterné.

    **Les pages technologies sont enfin branchées.** Leurs quatre cartes
    « related reading » portaient depuis le début les titres de pièces qui
    n'existaient pas et pointaient toutes sur `blog.html`. J'ai écrit les
    articles sous ces titres exacts, et les seize cartes (quatre pages × quatre
    cartes) pointent maintenant sur la bonne page — le libellé passe de
    « Read the thread » à « Read the piece ».

    **Non traduit** : le corps des articles reste en anglais, comme le reste
    du corps de texte des pages internes. Traduire neuf articles n'est pas un
    travail de dictionnaire.

33. **Les cartes à couverture, reprises.** Retour de Licter : elles faisaient
    pauvre à côté du reste. Le composant est utilisé à **soixante-huit
    endroits** (les quatre pages plateformes, l'index du blog, les neuf pages
    articles), donc le diagnostic valait d'être fait avant de toucher quoi que
    ce soit. Quatre défauts, quatre corrections :

    - **La couverture était un aplat teinté vide**, ce qui la fait lire comme
      l'emplacement d'une image qui n'a pas chargé. Elle porte maintenant un
      **petit amas de nœuds**, dessiné dans le vocabulaire de la cartographie
      de fond. Il est généré par `js/ui.js` à partir du titre de la carte
      comme graine : une carte donnée dessine toujours le même amas, et aucun
      fichier HTML n'a eu à être touché. Sans JavaScript, il reste le dégradé
      — soit exactement ce qu'on avait avant.
    - **Les couvertures n'avaient pas la même hauteur.** Un titre sur trois
      lignes poussait son corps plus bas que celui d'à côté, et la rangée
      partait en escalier. Hauteur minimale fixe et titre **calé en bas** :
      les titres s'alignent quel que soit le nombre de lignes.
    - **Une couture nette séparait la couverture du corps** (`border-bottom`),
      ce qui donnait deux boîtes empilées plutôt qu'une carte. Le dégradé
      s'éteint maintenant avant le corps, il n'y a plus de trait à voir.
    - **Les teintes alternaient par position** (`nth-child`), d'où un « SOCIAL
      DATA » ambre suivi d'un « INSIGHTS » gris sans logique lisible. Elles
      suivent maintenant **le sujet** : ambre pour social data et
      communication, ardoise pour l'écoute et la santé de marque, ocre pour
      les insights et les tendances, gris pour l'influence et les audiences.

    Au passage : rayon 12 → 18 px, fond translucide avec flou comme les autres
    feuilles du site, ombre de survol plus douce, et le filet au-dessus du
    lien s'arrête avant les bords — un trait qui ne touche pas les bords pèse
    visuellement moins qu'un trait pleine largeur.

34. **Passe esthétique d'ensemble : épurer, aérer, replacer.** Carte blanche
    de Licter, avec un point de retour posé avant de commencer
    (`git tag avant-polish`). Trois familles de corrections.

    **Le positionnement, d'abord — c'est là qu'était le vrai problème.**
    Le rythme alterné faisait descendre un titre collant à gauche et les
    cartes à droite une section sur deux. Avec trois cartes, ça produisait
    **deux trous** : un sous le titre, un à droite de la troisième carte. Et
    les sections impaires promouvaient leur première carte sur deux colonnes
    d'une grille qui en comptait trois, ce qui laissait la dernière carte
    seule sur sa ligne. Le bloc « Related reading » que Licter avait signalé
    n'était pas un cas isolé : c'était la règle qui produisait le défaut.

    - **Le split est désormais réservé aux listes longues** — étapes, FAQ,
      formulaires — et aux conteneurs de cartes à partir de six. Un titre
      collant ne gagne sa place que si la colonne d'en face est assez haute
      pour défiler devant lui. En dessous, pleine largeur.
    - **La grille des sections impaires passe à six pistes**, qui se divisent
      proprement par deux et par trois : trois cartes donnent une carte large
      puis une paire, quatre donnent une carte large puis une rangée de trois.
      Plus de ligne qui finit court.
    - **Quatre cartes à couverture** sont épinglées à deux colonnes, et à
      quatre dans les sections impaires au-delà de 1200 px : la page alterne
      un carré et une rangée au lieu d'empiler trois rangées identiques.

    Vérifié par mesure sur toutes les pages : plus aucune grille dont la
    dernière ligne s'arrête avant le bord.

    **L'air.** Padding des sections 48–84 → 62–108 px, écart entre un
    sur-titre et ce qu'il introduit 26–42 → 32–58 px, gouttière des grilles
    16–22 → 18–28 px, interlignage du corps des cartes 1,6 → 1,7.

    **Le dépouillement.** Les filets passent de 12 % à 10,5 % d'opacité, le
    fond des cartes de 80 % à 72 % de blanc et leur ombre est deux fois plus
    discrète : la page compte moins de surfaces et laisse mieux voir la
    cartographie. Enfin la colonne plafonne à 1340 px au lieu de 1420 — au
    delà, le texte s'étirait sans que la page y gagne.

    **Pour revenir en arrière** : `git checkout avant-polish -- css/styles.css`
    puis un commit. Tout tient dans la feuille de style, aucun HTML n'a été
    touché par cette passe.

35. **La traduction française, terminée et réparée.** Retour de Licter :
    certaines pages passaient mal en français. Mesure avant correction, en
    comparant chaque nœud de texte au dictionnaire :

    | Page | Couverture |
    |---|---|
    | Accueil | 69 % |
    | Offres · Guide · RDV | 60–67 % |
    | Cas d'usage · Clients · Pourquoi · Techno | 45–49 % |
    | Blog | 34 % |
    | Les quatre pages plateformes | **19 %** |

    Ce n'était donc pas « mal traduit » mais **à moitié traduit** : le
    dictionnaire couvrait la navigation, le pied de page, les titres et les
    CTA, et laissait tout le corps de texte en anglais. 586 chaînes
    manquaient. Elles sont traduites, une par une. Le dictionnaire passe de
    173 à 864 entrées, et les quatorze pages principales sont à **100 %**.

    **Deux vrais bugs trouvés au passage**, tous deux dans `js/i18n.js` :

    - **Le `MutationObserver` jetait des lots de mutations.** Le gardien
      `if (pending) return;` ignorait purement et simplement tout lot arrivant
      pendant qu'un autre attendait — le second rendu d'une même frame était
      perdu. Et il attendait sur `requestAnimationFrame`, **qui ne se
      déclenche jamais dans un onglet en arrière-plan** : la file se bloquait
      définitivement. C'est ce qui laissait toute la console de la home en
      anglais. Les enregistrements sont maintenant mis en file au lieu d'être
      jetés, et vidés sur un `setTimeout`.
    - **`SKIP[p.nodeName]` ne filtrait pas les SVG.** `nodeName` vaut `"svg"`
      en minuscules pour un élément SVG, jamais `"SVG"` : les libellés de mois
      du graphique étaient parcourus. Comparaison en majuscules.

    **Les 112 chaînes de la console** (rendues par `js/ui.js`, quatre familles)
    sont dans le dictionnaire : le `MutationObserver` réparé les traduit à
    chaque changement d'onglet.

    **Les neuf pages articles restent en anglais**, volontairement : c'est du
    contenu de remplissage (arbitrage 32) et traduire 4 500 mots qui seront
    remplacés n'a pas de sens. Plutôt que de servir une page à moitié
    française, chacune porte un encart visible uniquement en français — « Cet
    article n'est disponible qu'en anglais » — avec son propre fond, parce
    qu'il se place au-dessus de `.prose` et n'est donc pas couvert par la
    feuille de lumière de la colonne de lecture. Si Licter veut les traduire,
    c'est une demi-journée.

36. **Nouveau pied de page, sur une référence fournie par Licter.** La
    structure est reprise telle quelle : une bande newsletter en tête — titre,
    accroche, champ email et bouton à gauche, un visuel à droite posé sur une
    seconde carte en biais — puis la marque avec sa description et ses réseaux,
    les colonnes de liens, et la ligne légale.

    **Trois adaptations** :
    - **La référence est sombre, le pied de page reste clair.** L'instruction
      « la couleur claire domine l'ensemble » est globale, et inverser le seul
      pied de page en navy en ferait l'élément le plus lourd de la page. La
      bascule est d'une règle si Licter préfère le contraire.
    - **Le visuel de la référence est une photographie.** Ce site n'en a
      aucune. La carte porte donc le motif de la cartographie — trois amas
      reliés, générés dans le même vocabulaire que le fond — sur le dégradé
      ambre de la charte. Rien à commander, et c'est cohérent avec le reste.
    - **Les réseaux sont ceux qui existent vraiment**, vérifiés :
      `linkedin.com/company/licter`, `instagram.com/licter_listening`,
      `youtube.com/@audience_first`. Pas de X ni de Facebook : je n'ai pas pu
      confirmer de compte, et une icône qui mène à une 404 coûte plus qu'elle
      ne rapporte. L'icône YouTube remplace le lien « Audience First » qui
      était dans la colonne COMPANY.

    **Deux défauts corrigés au passage**, tous deux présents dans l'ancien
    pied de page :
    - **La grille avait quatre pistes pour cinq enfants**, donc la colonne
      COMPANY passait à la ligne sous la marque. Cinq pistes.
    - **`.site-foot ul` (0,1,1) battait `.social` (0,1,0)**, donc les icônes
      héritaient du `display: grid` des listes de liens et s'empilaient à la
      verticale. Sélecteur préfixé.

    Le formulaire est branché sur le même gestionnaire que les autres (donc
    toujours sans endpoint), avec un `id` unique par page, et les trois
    chaînes nouvelles sont traduites.

37. **Le mur de logos passe en carte à faisceau.** Composant fourni par
    Licter : une carte bordée, un faisceau qui parcourt son périmètre, et une
    légende à cheval sur la bordure haute dont le texte est balayé par une
    vague de couleur **au moment exact où le faisceau passe derrière elle**.

    **La synchronisation, qui est tout l'intérêt du composant.** La référence
    tient deux horloges en parallèle — une pour le faisceau, une pour la vague
    — et compte sur elles pour rester en phase. Ici le faisceau est une
    animation CSS, donc plutôt que de doubler le compteur en JavaScript, la
    boucle lit `currentTime` directement sur l'objet Web Animations du
    faisceau. Une seule horloge, aucune dérive possible. Mesuré : quand la
    vague démarre, le faisceau est à 193 px et la légende commence à 178 ;
    quand elle finit, 624 contre 617. L'écart est la demi-largeur du faisceau.

    **Les adaptations** :
    - **Le faisceau est ambre**, pas orange-violet. Il monte sur un
      `offset-path: rect()`, ce qui lui fait suivre les coins arrondis.
    - **La vague reprend le même principe** que la référence : elle vit dans la
      bande 47–53 % d'un dégradé large de 250 %, garée à 0 % ou 100 % le reste
      du temps — positions où l'élément ne voit que de la couleur unie, donc
      aucun clignotement à l'entrée ni à la sortie.
    - **La légende remplace le sur-titre « THEY TRUST US »** et porte un
      chiffre vérifiable : « Trusted by 50+ organisations, from CAC 40 groups
      to institutions », reprise d'une formule déjà employée ailleurs sur le
      site. La queue de phrase disparaît sous 720 px.
    - **Dégradation** : si `offset-path` n'est pas supporté, le faisceau est
      masqué plutôt que garé dans un coin, et la vague ne démarre pas. En
      `prefers-reduced-motion`, ni l'un ni l'autre.

    **Un piège de `background-clip: text`** : mettre `color: transparent` sur
    l'élément rend invisible tout ce que le dégradé peint en `currentColor`,
    c'est-à-dire tout le texte sauf la vague. La couleur doit rester réelle ;
    seul `-webkit-text-fill-color` passe à `transparent`.

38. **Un seul motif pour toutes les étapes.** Composant fourni par Licter :
    des repères numérotés sur une règle verticale, une carte par étape, et le
    titre de la section à côté. Il remplace **deux formes différentes qui
    faisaient le même travail** — `.steps` sur les pages offres et diagnostic
    (des lignes séparées par des filets, avec un gros chiffre ambre) et
    `.numbered` sur les quatre pages plateformes (trois colonnes). Une étape
    se lit désormais pareil partout : 16 étapes converties sur 6 sections.

    **Adaptations** : le duo turquoise-magenta de la référence devient navy et
    ambre — pastille navy à texte crème, coche ambre. La coche est dessinée en
    CSS plutôt qu'importée. La règle verticale est un dégradé qui s'éteint à
    ses deux extrémités, et chaque pastille porte un halo de 5 px de la
    couleur du fond, pour qu'elle paraisse posée sur la règle et non traversée
    par elle.

    **La section garde sa tête à gauche** (`.block--flow`), mais **centrée
    verticalement**, pas collée en haut. Premier jet : tête collante alignée
    en haut, d'où un titre de deux lignes flottant au-dessus de 400 px de
    vide face à quatre étapes — retour de Licter, justifié. La référence, elle,
    centre sa colonne de texte : c'est ce que je n'avais pas repris.

    **Le texte est ensuite rentré depuis le bord.** Mesuré, la tête de la
    frise était alignée sur la même verticale que tous les autres titres de la
    page — 91 px à 1150, 210 px à 1600, exactement comme le titre de page et
    les autres sur-titres. Mais dans une composition à deux colonnes, la
    colonne de gauche n'a rien à sa gauche, et la même valeur qui convient
    ailleurs colle ici au bord. La tête rentre donc de 14 à 48 px selon la
    largeur (37 px à 1440), et sa mesure est plafonnée à 34 caractères. Elle
    n'est plus alignée sur les autres titres de la page : c'est assumé, c'est
    un encart à deux colonnes, pas une section pleine largeur.

    **Et la colonne a maintenant quelque chose à dire.** La référence remplit
    la sienne avec trois éléments — sur-titre, titre, chapô — alors que cinq
    des six blocs Licter n'en avaient que deux. Un chapô a donc été écrit pour
    chacun, qui reformule ce que les étapes établissent déjà en dessous :
    aucune affirmation ni chiffre nouveau. La colonne passe de 89 à 174 px de
    contenu utile.

    **Ce que je n'ai pas converti** : le bloc « Four steps, no black box. » de
    la home. Il décrit bien des étapes, mais il est en accordéon, en colonne
    étroite, appairé avec la FAQ (arbitrage 22). Y mettre une frise casserait
    le couple. À trancher si Licter préfère l'uniformité à cet endroit.

    Les deux composants remplacés ont été supprimés de la feuille de style, ce
    qui retire une cinquantaine de lignes.

39. **Page clients : le mur de logos et le trou de la grille.**

    **Le mur** affichait seize noms en texte brut, tous au même poids, dans
    une grille bordée — un tableur. Et avec seize noms sur six colonnes, la
    dernière ligne laissait **deux cases vides encadrées**. Il est refait en
    **quatre colonnes**, qui divisent seize exactement, sur une feuille réglée
    (filets intérieurs seulement, plus de cadre autour du tout), et chaque nom
    reprend **le poids, l'espacement et l'opacité que le marquee lui donne
    déjà** : les marques gardent leur caractère sans devenir un alphabet de
    tailles au hasard.

    **Ce que je n'ai pas réutilisé** : le SVG du marquee. Ses boîtes sont
    dimensionnées marque par marque, ce qui convient à un défilement mais
    rend, dans une grille, « HP » à 10 px à côté de « DANONE » à 21 px.
    Une seule taille de police avec le poids par marque garde l'identité et
    l'homogénéité — hauteur de caractère mesurée : 18 px pour les seize.

    **Le trou de la grille.** La passe de l'arbitrage 34 n'avait traité que
    les sections impaires : quatre cartes y deviennent une carte large plus
    une rangée de trois. Les sections **paires** gardaient un `auto-fit` qui
    tombe sur trois colonnes à la largeur de la colonne, d'où une quatrième
    carte seule sur sa ligne — visible sur clients, why-licter et diagnostic.
    Elles prennent maintenant un **2 × 2**. Balayage refait sur toutes les
    pages : plus aucune grille dont la dernière ligne s'arrête avant le bord.

40. **La cartographie se limite au hero.** Demande de Licter : retirer les
    communautés animées du fond du site, les garder uniquement sur le hero.

    **Le mécanisme remplacé.** Le canevas était `fixed` derrière toute la
    page, avec un voile crème que `js/ui.js` montait de 0 à 30 % dès le début
    du contenu. La carte restait donc derrière chaque paragraphe du site,
    simplement atténuée. Le voile est supprimé ; c'est le canevas lui-même qui
    s'efface, et la boucle d'animation s'arrête avec lui — plus rien à
    dessiner, plus rien à calculer.

    **Où elle reste** : derrière le hero sur la home, derrière le bandeau de
    tête sur les autres pages. Le fondu se termine au bas de cette zone, **ou
    à la fin du premier écran si elle est plus courte** — sans ça, le bandeau
    court des pages articles faisait pâlir la carte avant même que le lecteur
    n'ait défilé. Mesuré sur la home en 900 px de haut : 1 jusqu'à 400 px de
    défilement, 0,28 à 800, 0 à partir de 1200.

    **Conséquence traitée, pas subie.** Les feuilles de lumière
    (`.block::before`, `.prose::before`, `.cases__asks::before`) n'existaient
    que pour rendre le texte lisible par-dessus la carte. Sans carte, elles
    n'étaient plus qu'un panneau blanc posé sur la crème, avec un
    `backdrop-filter` qui ne floutait rien. Elles sont supprimées. **Celle du
    bandeau de tête reste** : c'est la seule zone où la carte est encore là,
    et c'est précisément le défaut de lisibilité corrigé aux arbitrages 17
    et 18.

    Pas de transition CSS sur l'opacité : elle est déjà recalculée à chaque
    frame de défilement, et une transition par-dessus ne ferait que la mettre
    en retard sur le scroll.

    **Si Licter voulait dire « uniquement sur la home »** et pas « sur le hero
    de chaque page », il suffit de remplacer le sélecteur de zone par
    `document.querySelector(".hero")` seul : les 22 autres pages passeraient
    alors sur fond crème uni de haut en bas.

41. **Le classement SI Lab remplace le sur-titre du hero.** « // AI & DATA
    AGENCY FOR ENTERPRISES » disait ce que Licter est ; « Top 50 des acteurs
    mondiaux de la social intelligence, SI Lab 2024 » dit ce que le marché en
    pense. C'est un meilleur premier argument, et c'est vérifiable.

    L'élément garde **la forme de la carte de chiffre** dont il vient — filet
    ambre à gauche, chiffre dans la police de titre, légende en dessous — mais
    à une taille qui se place **au-dessus** du titre au lieu de lui disputer
    l'attention : 27 px contre 56. Alignement sur la ligne de base, pour que
    le chiffre et sa légende se tiennent.

    **Il est retiré de la bande de preuve** juste en dessous : le garder aux
    deux endroits, à un écran d'intervalle, aurait affaibli les deux. La bande
    passe à trois chiffres, ce qui tombe juste sur trois colonnes — pas de
    ligne courte.

42. **Marquer les sections : un sol par sujet.** Retour de Licter : les
    sections se mélangent, on ne sent pas qu'on passe d'un sujet à un autre.
    Diagnostic : depuis le retrait de la cartographie (arbitrage 40), les
    feuilles de lumière ont disparu avec elle, et la page est devenue **une
    seule grande feuille crème**. Il ne restait qu'un filet d'1 px et du
    padding pour séparer deux sujets — ce n'est pas un signal, c'est une
    respiration.

    **Une section sur deux pose son propre sol, d'un bord à l'autre de
    l'écran.** Le contenu reste dans la colonne centrée ; seul le fond déborde
    (`inset: 0 calc(50% - 50vw)`). Changer de sujet, c'est changer de sol.

    **Le sol a changé deux fois avant d'être juste.** Premier essai en blanc :
    les cartes sont blanches à 72 %, elles disparaissaient purement et
    simplement. Deuxième essai en ambre à 7 % avec filets ambrés : lisible,
    mais retour de Licter — « trop brouillon ». Juste : la page a déjà un
    bandeau ambre, des boutons ambre, des sur-titres ambre et des accents
    ambre sur les cartes ; une bande ambre de plus en faisait une couleur de
    trop, et les deux filets s'ajoutaient à la pile d'horizontales.

    **La version retenue est un pas de valeur, pas de couleur** : `--band`,
    la même crème une nuance plus profonde (`#F6EFE4` contre `#FCF6EF`), sans
    aucun filet. Un changement de ton net se suffit comme ligne, et
    l'alternance n'ajoute plus une seule couleur à la page.

    **La parité se compte sur toutes les sections, pas seulement sur les
    blocs.** Sur la home, la console est une `<section class="cases">` posée
    entre deux `.block` : la compter hors parité laissait **trois sections
    crème d'affilée**. Vérifié sur les dix pages : aucune ne présente deux
    sols identiques qui se suivent.

    **Le sur-titre devient l'étiquette du chapitre** : 700 au lieu de 600,
    interlettrage 2 px, couleur ambre au lieu du gris, et le tiret passe de
    1 à 2 px. C'est lui que l'œil attrape en arrivant sur un nouveau sol.

43. **Photos : les neuf fichiers d'attente sont placés.** Demande de Licter :
    rendre le site plus « humain » avec des photos d'attente, les définitives
    n'étant pas prêtes. Neuf fichiers fournis, copiés dans
    `assets/img/people/` sous des noms parlants pour que le remplacement se
    fasse fichier par fichier, sans toucher au HTML.

    **Les placements retenus** — là où la page parle déjà de personnes :

    - `why-licter.html#origin`, mosaïque de deux photos au-dessus des
      chiffres : la section raconte d'où vient le cabinet, les visages y
      précèdent les statistiques plutôt que de les illustrer.
    - `why-licter.html#who`, mosaïque de deux photos en tête de la section
      « qui nous sommes ».
    - `book-a-meeting.html#what`, portrait à côté du titre : la page promet
      qu'on parle au consultant qui fera la lecture, un visage tient cette
      promesse mieux qu'une phrase de plus. Une accroche a été ajoutée sous
      le titre pour que la colonne de texte tienne la hauteur du portrait.
    - Les neuf articles de blog : vignette de 26 px dans la signature.

    **Les trois photos d'événement sont placées à la demande de Licter**, en
    connaissance de cause : elles portent la marque d'organisations tierces
    et, pour l'une, le nom d'une personne qui n'est pas de la maison.

    - `event-award.jpg` (« Ose ! Le Cercle Business », diplôme de lauréate) →
      **posée puis retirée.** Essayée contre les chiffres de `index.html#proof`,
      refusée par Licter, et la section est revenue exactement à son état
      d'avant. Le fichier reste dans `assets/img/people/`, sans emploi. Elle
      était de toute façon la seule photo du site qui se lisait comme une
      revendication : contre « 50+ / 160+ / 3 bn », elle suggérait que le prix
      était celui du cabinet.
    - `event-conference.jpg` (fond « Les Rencontres Économiques
      d'Aix-en-Provence ») → `clients.html#wall`, juste au-dessus du mur de
      logos, où la section parle déjà d'institutions.
    - `event-talk.jpg` (affiche KEDGE, « Anaïs BREMAND, Fondatrice de Quartz
      Agency ») → `why-licter.html#difference`, « Consultants, not
      dashboards » : un consultant au micro plutôt qu'un écran.

    **L'arbitrage est assumé, pas oublié** : ces trois images n'ont pas
    vocation à survivre à la série définitive, et si le site passe en public
    avant, ce sont les trois premières à retirer.

    **Les deux photos de `#origin` sont calées l'une sur l'autre.** Retour de
    Licter : la seconde n'était pas proportionnée à la première. Deux causes,
    corrigées ensemble — les cadres finissaient sur deux lignes différentes
    (374 px contre 389, chacun tenant son propre ratio), et le recadrage
    `scale(1.5)` grossissait les personnes bien plus qu'à gauche. La photo
    haute abandonne donc son ratio au profit de la hauteur de la rangée
    (`.shots:has(> .shot--wide) > .shot--tall`), et le zoom tombe à 1,22. Le
    logo d'une autre société sur le mur du fond, que le recadrage serré
    sortait du cadre, redevient partiellement visible — cohérent avec la
    décision prise sur les photos d'événement.

    **Une photo seule à côté d'un titre ne tient pas.** Retour de Licter sur
    `#difference` : « on dirait que la photo s'est retrouvée là par hasard ».
    Le diagnostic n'était pas la taille — c'était qu'elle ne partageait aucune
    ligne avec le reste. Trois causes cumulées : `.block__head` se plafonne à
    680 px, ce qui creusait un vide de 200 px entre le texte et la photo ; la
    photo, plus haute que le titre, mangeait la marge qui sépare un chapeau du
    bloc suivant et venait frôler les cartes à 5 px ; et son cadre ne
    s'alignait sur rien.

    **`#difference` bascule donc sur le motif que la page utilise déjà** : une
    bande de deux photos entre le titre et les cartes, exactement comme
    `#origin`, aux bords alignés sur la grille (60 → 964). L'affiche y garde
    son ratio d'origine à 1/1000 près — un document se lit entier ou pas du
    tout — et la photo à côté abandonne le sien pour épouser sa hauteur. C'est
    elle dont l'image sort du flux : laissée dedans, sa hauteur intrinsèque
    imposait la rangée. `portrait-outdoor.jpg` quitte les signatures d'articles
    pour l'accompagner, où elle ne servait qu'en 26 px.

    **Les deux photos restées à côté d'un titre** (`clients.html#wall`,
    `book-a-meeting.html#what`) gardent le motif mais plus
    le vide : le chapeau occupe toute sa colonne, et c'est la paire, pas le
    titre, qui porte la marge vers le bloc suivant.

    **Le cadre des portraits est passé de 300 à 240 px.** Même retour, appliqué
    aux photos posées à côté d'un texte : à 300 px un cadre portrait faisait
    400 px de haut contre 130 à 190 px de titre, soit trois fois son voisin.
    Une seule colonne photo pour toutes les sections (`minmax(200px, 240px)`)
    ramène le rapport entre 1,4 et 2. La rangée de chiffres de la home avait
    été empilée pour la même raison — 84 px de haut, aucune photo ne pouvait
    tenir à côté — elle est revenue à trois colonnes avec le retrait de la
    photo.

    **En mobile, la paire passe côte à côte sous 720 px** : pleine largeur,
    une photo seule laissait un trou sur sa ligne, et le recadrage qu'il
    aurait fallu pour tenir la largeur coupait les visages.

    **Toutes les photos montrent la même personne**, sauf la photo de groupe.
    Neuf placements sur un seul visage, c'est ce que les fichiers permettent —
    la série définitive devra varier, sans quoi le site aura l'air de
    n'employer qu'une personne.

44. **Un flux convergent prend le relais de la cartographie.** La carte
    s'arrête au hero depuis l'arbitrage 40 ; en dessous, la page était nue.
    Composant fourni par Licter (canvas de béziers convergents, enveloppé dans
    une iframe React) ramené à un fichier vanilla, `js/flow.js`, et à la
    charte : trajets navy pointillés entrant par les deux bords et se pliant
    vers un point unique au centre de l'écran, un signal ambre les parcourant.

    **Les deux canvas se croisent, ils ne se superposent jamais.** `js/ui.js`
    pilote déjà l'opacité de la carte au scroll ; la même valeur inversée pilote
    le flux, et chacun coupe sa boucle `requestAnimationFrame` quand il sort de
    vue. À aucun moment deux canvas ne peignent.

    **Les sols alternés deviennent translucides.** `main` porte son propre
    contexte d'empilement, donc un sol opaque masque tout fond posé derrière
    lui : le flux serait apparu sur une section sur deux.
    `rgba(202, 188, 147, .12)` sur la crème recompose exactement `#F6EFE4` —
    même plancher, mêmes frontières de section, les trajets se lisant au
    travers un cran plus faible.

    **Ce qui a été changé au composant** :

    - **z-index 1, pas 0 comme la carte.** À 0 la couche passait sous
      `body::after`, dont le voile blanc est le plus fort à 50 % / 38 % —
      exactement où les trajets convergent. La moitié de l'effet y passait.
    - **Les trajets sont peints une fois dans un canvas hors écran** et
      re-blittés à chaque image ; seuls les points voyageurs sont redessinés.
      Le composant re-trace quatre-vingts béziers pointillés par image, ce qui
      est beaucoup de peinture pour un fond que personne n'est censé regarder.
    - **Quarante trajets au lieu de quatre-vingts**, et le compte suit la
      largeur : une douzaine sur un téléphone. Quatre-vingts traits blancs sur
      du noir font un faisceau ; sur la crème ils font une hachure.
    - **Les trajets s'éteignent avant d'arriver** (dégradé vers l'alpha 0) et
      les points aussi : quarante lignes pleines qui finissent sur le même
      pixel dessinent une étoile sombre au milieu de la page.
    - **Les points sont descendus à .38 d'alpha.** Retour de Licter : ils
      passaient par-dessus le reste du site. Ils sont pourtant derrière tout
      le contenu — `main` porte un z-index supérieur — mais l'ambre est la
      marque la plus claire d'une page pâle et porte bien plus loin que sa
      taille. Le contraste était le seul levier.
    - **Le clic qui repousse les particules n'est pas repris** : sur un site
      où l'on clique des liens et des boutons, un fond qui tressaille à chaque
      clic ressemble à un bug.
    - `setTransform` au lieu de `scale` pour le DPR : `scale()` multiplie la
      transformation en place, donc chaque redimensionnement la cumulait.

    **Le corps des articles reçoit le flux comme le reste.** C'est le seul
    endroit où il passe derrière de la lecture longue ; si Licter le trouve
    gênant, l'opacité s'y baisse en une ligne.

## Reste à faire

- Brancher les formulaires sur un vrai endpoint (`js/ui.js`, deux
  commentaires `wire to the real endpoint here` : capture email et formulaires
  du funnel).
- Produire le PDF du guide et brancher son envoi automatique.
- Fournir les clips des stories du hero (`renderMedia()` dans `js/ui.js`).
- Logos des quatre éditeurs (`assets/img/tools/*.png`) : encore attendus
  par le dropdown « Tech & Tools », qui retombe sur un monogramme. La page
  `tech-tools.html` ne les demande plus (voir l'arbitrage 27).
- Traduire le corps des neuf articles de blog si Licter les garde
  (arbitrage 35) ; le reste du site est couvert à 100 %.
- Rafraîchir `js/voices.js` quand de nouvelles interviews sortent
  (`tools/harvest-voices.md`), ou trancher pour une fonction serverless si le
  temps réel est jugé nécessaire.
- Relire **tous les chiffres de la console** de la home (arbitrage 29) :
  KPI, volumes, parts, variations et signaux des quatre familles.
- Relire les quatre pages plateformes : ce que fait réellement chaque outil
  chez Licter, et ce qu'on a le droit d'en dire publiquement.
- Blog : les neuf articles sont des textes d'attente (arbitrage 32). Les
  remplacer par les vrais articles Licter, ou les faire relire avant toute
  mise en ligne.
- Remplacer les photos d'attente de `assets/img/people/` par la série
  définitive (arbitrage 43) — mêmes noms de fichiers, aucun HTML à toucher.
  Retirer en priorité les trois photos d'événement (« Ose ! », « Rencontres
  Économiques », affiche KEDGE nommant une tierce personne) si le site passe
  en public avant la série définitive, et trancher sur `team.jpg` dont le mur
  porte le logo d'une autre société.

- Pages légales (mentions, confidentialité) : absentes, le pied de page les
  attend.
- Accessibilité : sur la crème, le texte courant `#56606A` passe l'AA (5.4:1)
  et le navy est à 15:1. Restent sous le seuil pour du petit texte le gris
  `#84919A` (3:1, utilisé sur `EXPLORE` et les libellés de rail) — à revoir si
  l'AA est un critère. L'ambre pur n'est jamais utilisé pour du texte.
- Le token GitHub du dépôt Licter était expiré — à renouveler avant le
  premier push.

## ⚠️ Contenu fictif (MOCK) à remplacer avant mise en ligne

La home contient des maquettes interactives marquées `data-mock` dans le HTML
et `MOCK` dans le code. **Rien n'est envoyé nulle part.** À remplacer :

| Élément | Où | À fournir |
|---|---|---|
| Visuels des cas d'usage (courbe, nuage de mots, communautés, radar, posts, réponses) | `js/usecases.js` → `DATA`, `WORDS`, `SEGMENTS`, `TRENDS` | Verbatims et chiffres réels anonymisés |
| Rôles des trois portraits | `index.html#team` | Prénoms et rôles confirmés |
| Diagnostic : 6 dimensions, questions, paliers | `js/home.js` → `QUIZ`, `BANDS` | Validation par l'équipe |
| Créneaux de rendez-vous | `js/home.js` → bloc booking | Calendrier réel (Calendly, Cal.com, HubSpot) |
| Envoi des formulaires (diagnostic, guide, RDV, newsletter) | `js/home.js`, `js/ui.js` (`wire to the real endpoint`) | Outil CRM / formulaires |
| Mot des fondateurs (texte) | `index.html#founders` | Validation par Antoine et Adrien |
