# DESIGN.md · Licter

La référence de design du site Licter. Elle s'adresse à toute personne, ou à tout agent IA, qui ajoute une page, une section ou un composant. Elle décrit ce qui est en ligne aujourd'hui, pas un idéal. En cas de doute, la source de vérité est `css/styles.css`. Ce fichier dit pourquoi.

> La section « Palette » du README date du thème ambre `#FDBA11`. Elle est obsolète : la charte actuelle est décrite ici.

---

## 1. Positionnement visuel

Licter est un cabinet de conseil en social listening. Le site doit se lire comme **un cabinet, pas comme un logiciel**.

- **Des humains d'abord.** Photos réelles de l'équipe et des clients, visages, citations signées. Jamais d'illustration générique « IA » ni de photo de banque d'images.
- **Montrer plutôt que dire.** Une démo, un livrable, une vidéo client valent mieux qu'un adjectif. Chaque affirmation (« nous lisons les verbatims ») doit avoir sa preuve visible à côté.
- **Sobre et institutionnel.** Le navy porte tout, l'or signe. Pas de dégradé violet, pas de néon, pas d'effet gratuit.
- **Une seule demande principale par écran :** « Parler à un consultant ».

---

## 2. Couleurs

### Charte

| Nom | Hex | Rôle |
|---|---|---|
| Bleu Élysée (navy) | `#13162D` | texte en clair, fond en sombre, **toutes les actions** |
| Crème | `#FCF6EF` | fond en clair, texte en sombre |
| Or | `#EAA93D` | **signature uniquement** : filets sous les titres, badge de classement, progression |
| Gris | `#84919A` | libellés discrets, réseau de fond |

### Règle qui commande tout

**L'or ne porte jamais de texte et ne remplit jamais un bouton ni un bandeau.** Il fait 1,9:1 sur la crème. Il reste un trait : filet de 3 à 4 px sous un titre, tiret devant un surtitre, jauge, pastille.
Le texte d'accent passe par `--amber-ink`. Malgré son nom historique, c'est un bleu (`#2C3566` en clair, `#B9C3F2` en sombre).

### Tokens (rôles)

Toujours utiliser le rôle, jamais l'hex en dur, pour que le thème sombre suive.

| Token | Clair | Sombre | Usage |
|---|---|---|---|
| `--bg` | `#FCF6EF` | `#13162D` | fond de page |
| `--band` | `#F6EFE4` | `#171B36` | une section sur deux |
| `--surface` / `--card-bg` | `#FFFFFF` | `#1C2142` | cartes, panneaux, menus |
| `--raise` | | `#252B55` | surface surélevée en sombre |
| `--ink` | `#13162D` | `#FCF6EF` | texte principal, titres |
| `--text-2` | `#56606A` | `#B7BFC8` | texte courant secondaire, chapôs |
| `--text-3` | `#6F7A82` | `#9EA8B2` | libellés, métadonnées |
| `--text-4` | `#84919A` | `#84919A` | décor uniquement (3:1, pas pour du texte utile) |
| `--line` | navy 10,5 % | crème 12 % | toutes les bordures et séparateurs |
| `--field-bg` / `--field-br` | blanc / navy 16 % | `#181C3A` / crème 22 % | champs de formulaire |
| `--amber-ink` | `#2C3566` | `#B9C3F2` | texte d'accent, `em` dans les titres |

Les ombres et voiles utilisent `rgba(var(--ink-rgb), a)` ou `rgba(var(--surf-rgb), a)` : elles sont teintées navy, jamais noir pur sur clair.

### Thèmes

- **Sombre par défaut** (`js/theme.js`, clé `licter-theme`). Le clair est à un clic et il est mémorisé.
- Le thème est posé sur `html[data-theme]` avant le premier rendu : aucun flash de crème.
- Tout nouveau composant se vérifie **dans les deux thèmes**. Une surface codée en `#fff` doit recevoir sa règle `html[data-theme="dark"]`.

---

## 3. Typographie

| Rôle | Police | Graisse | Où |
|---|---|---|---|
| Titres | **Aiglon Pro Wide** (`--title-font`) | Demi (600 à 800) ; Thin (100 à 300) en réserve | H1, H2, gros chiffres |
| Texte | **Raleway** (`--body-font`), variable 400 à 700 | 400 courant, **500 pour les chapôs**, 600 à 700 pour les libellés et boutons | tout le reste |

Les deux polices sont hébergées dans `assets/fonts/` : aucun appel à Google Fonts (RGPD). Raleway affiche des chiffres elzéviriens par défaut, d'où `font-feature-settings: "lnum"` sur `body`.

### Échelle

| Élément | Taille | Interligne | Approche |
|---|---|---|---|
| H1 hero (accueil) | `clamp(46px, 5.2vw, 80px)` | 1 | -2px |
| H1 page | `clamp(34px, 4.6vw, 62px)` | 1.04 | -1.2px |
| H2 section (`.block__title`) | `clamp(26px, 2.8vw, 38px)` | 1.1 | -0.7px |
| Chapô (`.page__lead`) | `clamp(15px, 1.15vw, 18px)`, 500 | 1.65 | |
| Texte courant | 15 à 16px | 1.6 | |
| Surtitre (`.block__kicker`) | 10,5 à 12px, 700, majuscules | 1 | +2px |
| Bouton | 12 à 14px, 700 | 1 | +1.2px en majuscules |

Règles :
- `text-wrap: balance` sur les titres. Largeur de lecture : 620 à 680px maximum.
- **Un titre de section = surtitre + H2 + filet or** (`.block__title::after`, 64 × 3px). Le H1 du hero porte un filet plus long (42 %, 4px).
- Pour souligner un mot dans un titre : `<em>`, qui passe en `--amber-ink` sans italique. Jamais une autre police.
- **Plancher : 12px** pour tout texte utile, y compris le menu, le bandeau, les surtitres et les titres du pied de page.
- **Cibles :** 44px sur mobile, 24px sur ordinateur. Pour les liens en ligne et les petites pastilles, la zone s'agrandit avec du padding ou un `::after` invisible, sans bouger la mise en page.

---

## 4. Mise en page

- **Colonne :** `.shell`, largeur `--maxw: clamp(1097px, 86vw, 1340px)`, marges `--gutter: clamp(20px, 5.83vw, 64px)`.
- **Section :** `.block`, padding vertical `clamp(62px, 9vh, 108px)`. En-tête de section `.block__head`, 680px maximum, puis `clamp(32px, 5vh, 58px)` d'air avant le contenu.
- **Alternance :** une section sur deux pose un fond `--band` bord à bord (`::before`). C'est un changement de valeur, pas de couleur. Pas de filet en plus.
- **Grilles :** CSS Grid, `repeat(auto-fit, minmax(270px, 1fr))` pour les cartes.
- **Trois catégories d'écran :**

  | Catégorie | Largeur | Règle |
  |---|---|---|
  | Mobile | 720px et moins | mise en page propre à l'accueil (voir plus bas), chat plein écran |
  | Tablette | 721 à 1199px | **le contenu de l'ordinateur, les réflexes du mobile** : barre CTA en bas avec Antoine sur l'accueil (l'en-tête n'a plus la place pour le CTA), chat en panneau latéral ; en portrait (721 à 960px), la démo de l'accueil tient en un écran, visuel et lecture côte à côte |
  | Ordinateur | 1200px et plus | la version complète, CTA dans l'en-tête |

- **Champs à 16px sur tout écran tactile** (`(pointer: coarse)`) : sous 16px, iOS et iPadOS zooment sur la page et y restent.
- **Points de rupture utilisés :** 1200 (CTA de l'en-tête masqué en dessous), 960 (hero sur une colonne), 860 (menu replié dans la pilule), 720 (mobile), 560 (une colonne, boutons pleine largeur), 420.
- **Mobile :** 16 à 20px de marge, aucun défilement horizontal, `min-height: 100svh` et jamais `100vh`.
- **Sur téléphone (720px et moins), l'accueil a sa propre mise en forme**, avec le même HTML et le même ordre (environ 7,5 écrans). Règle : **tout est aligné à gauche**.
  - **Premier écran :** la promesse et les logos clients. Le hero est resserré et le bandeau d'événement tient sur deux lignes.
  - **Retiré :** la cartographie du hero. Les scripts de la démo et de la carte (`usecases.js`, `communities.js`, environ 120 Ko) ne sont pas téléchargés sous 720px ; ils se chargent si la fenêtre s'élargit.
  - **Familles :** même carte que sur ordinateur, en carrousel au doigt (86 % de largeur, la suivante dépasse), sans flèches.
  - **Vidéos :** une à la fois, sans la note sur la chaîne.
- **Pied de page sur téléphone (tout le site) :** les quatre colonnes deviennent des volets, un seul ouvert à la fois (`js/ui.js`), et le paragraphe de présentation est retiré.
- **Vidéos de l'accueil :** la citation sous la miniature est masquée visuellement, puisque la miniature l'affiche déjà. Elle reste le nom du lien pour les lecteurs d'écran et Google.
  - **« Pourquoi pas un outil seul » + Équipe :** le titre, le badge et les visages, puis un tableau à deux colonnes « Un outil seul / Notre équipe ». Le chapô et la phrase de fin, redondants avec le tableau, sont retirés ; le mot des fondateurs est replié. Les éléments d'équipe sont déplacés en JS (`js/home.js`), jamais copiés.
  - **Démo retirée :** ses 4 questions répètent les 4 familles, et chaque page famille a sa propre démo mobile.
  - **Méthode :** mêmes cartes que sur ordinateur (photo, étapes, flèches).
  - **Diagnostic :** replié derrière un bouton. Un lien `#diagnostic` l'ouvre.
  - **FAQ :** deux questions, puis « Voir les 3 autres questions ».
- **Sous le quiz (tous écrans) :** le lien « Plutôt lire d'abord ? Le guide des 12 questions → », pour qui ne veut pas répondre tout de suite.
  - **Une seule action :** la barre du bas, avec l'avatar d'Antoine qui ouvre le chat. Les boutons de section et le lanceur flottant sont retirés.

---

## 5. Formes, profondeur, mouvement

### Rayons

| Rayon | Usage |
|---|---|
| 8px | boutons, champs |
| 14 à 18px | cartes, vignettes, lecteurs vidéo |
| 22 à 24px | panneaux (tiroir d'Antoine, popups) |
| 999px | pilules : navigation, lanceur du chat, filtres, puces |
| 50 % | avatars |

### Ombres

Toujours longues, douces et teintées :
- au repos : `0 14px 32px -28px rgba(var(--ink-rgb), .24)` ;
- au survol : `0 26px 50px -28px rgba(var(--ink-rgb), .42)` ;
- pour les panneaux flottants : `0 40px 90px -30px rgba(19, 22, 45, .55)`.

### Mouvement

- **Courbe maison :** `cubic-bezier(.16, .84, .34, 1)`, et `cubic-bezier(.16, 1, .3, 1)` pour les panneaux qui glissent.
- **Apparitions :** `[data-reveal]`, 16px vers le haut avec un fondu en 0,6 s. Elles sont échelonnées avec `--d` et `--i`.
- **Survol de carte :** `translateY(-3px)`. **Appui sur un bouton :** `translateY(1px)`.
- **Animer uniquement** `transform` et `opacity`.
- **`prefers-reduced-motion` :** tout est visible tout de suite, sans transition. Sans JavaScript, rien n'est jamais caché, car le masquage dépend de `html.reveal`.
- **Une démo qui change de taille en jouant doit prendre sa hauteur hors écran.** La démo de l'accueil se construit un écran avant d'apparaître, puis rejoue son animation une fois visible.

---

## 6. Composants

### Boutons

| Classe | Rendu | Usage |
|---|---|---|
| `.btn--primary` | fond navy, texte crème ; survol `#2C3566` | **l'action** : « Parler à un consultant » |
| `.btn--primary` sur fond navy | fond blanc, texte navy | quiz, blocs sombres |
| `.btn--ghost` | transparent, bordure ink 35 % | action secondaire, au plus une à côté d'un primaire |
| lien texte + `→` | souligné | action tertiaire (« Pourquoi Licter ») |

Le libellé tient sur une ligne et compte trois à quatre mots au maximum. La flèche est `<span aria-hidden="true">→</span>`.

### Pages cas d'usage (`/fr/cas-usage/…`, `/en/use-cases/…`)

- **Leur aimant, c'est le cas réel** (« Recevez un cas réel de ce type, dans votre secteur », e-mail et secteur), avec en dessous « Plutôt lire d'abord ? Le guide des 12 questions ». **Le popup du magazine ne s'y ouvre jamais tout seul.**
- **CTA :** « Parler à un consultant » partout (hero, barre mobile), qui ouvre le popup de rappel ; « Me faire rappeler » reste le bouton du formulaire.
- **Barre du bas sur téléphone :** Antoine (ouvre le chat), « Recevoir un cas réel », « Parler à un consultant ». Le bouton flottant d'Antoine et la couverture du magazine n'apparaissent pas sur ces pages.
- **Téléphone, pour rester autour de 6 à 7 écrans :**
  - le livrable montre le haut de sa maquette, en fondu ;
  - « Comment ça se passe » devient une liste compacte ;
  - les bénéfices ne gardent que leurs titres ;
  - la vidéo est placée à côté de la citation ;
  - la FAQ est repliée après une question (deux sur le sommaire) ;
  - les articles liés et les chiffres sont masqués ;
  - le sommaire reprend le tableau compact « Pourquoi pas un outil seul » et les vidéos à faire glisser.
- **Plancher de 12 px partout**, maquettes comprises.
- **Sur grand écran,** le bouton d'Antoine se réduit à l'avatar une fois le hero passé. Le sommaire a ses propres blocs « Une question, pas un tableau de bord » et ses propres vidéos (Kantar, SEB, Dassault) : aucun doublon de l'accueil. Les pages famille n'ont qu'une vidéo sur téléphone.

### Pages offres (`tools/build-offers.py`, `offers.html`)

- **Deux langues statiques :** `offers.html` et `offer-*.html` en anglais à la racine, leurs jumelles françaises sous `/fr/offres/…/`, avec `hreflang` et des titres et données structurées propres à chaque langue. `offers.html` reste le fichier source de la page Offres : son contenu est généré par `hub_main()` entre `<!-- offers-main … -->` et `<!-- /offers-main -->`, seul le rappel (`#book`) y est écrit à la main. Les exemples des heros des pages d'offre sont dans `tools/offer_demos.html`. Les autres générateurs copient la coque via `shell_source()`, sans son propre bloc SEO.
- **La page Offres (environ 5 écrans sur ordinateur, 6 sur mobile) :**
  1. le hero : la promesse à gauche, à droite « Quelle est votre situation ? » dans le style de l'ancienne liste : la situation, une flèche, l'offre en pastille (au survol, la ligne glisse et la pastille se remplit). Un clic fait défiler jusqu'à l'offre dans le carrousel et la met en évidence ; puis les logos ;
  2. **les quatre offres**, en cartes photo comme les quatre familles des cas d'usage (`.ucc`) : la couleur de l'offre en filet, son nom, sa promesse, « Pour vous si », trois éléments inclus et « Découvrir l'offre » ; elles défilent de côté sous 1100 px ;
  3. le comparatif détaillé, replié (`#compare`) ;
  4. ce qui ne change pas, en cartes à reflet (glare) : deux photos de l'équipe, deux grands chiffres (20+, S1), qui s'inclinent et accrochent la lumière sous le pointeur (immobiles si l'utilisateur réduit les animations) ;
  5. trois interviews clients (AXA, Dassault Systèmes, SNCF) ;
  6. l'aimant « Recevoir la grille tarifaire » (`#offre`) ;
  7. la FAQ ;
  8. le rappel.
- **Une page d'offre (environ 6 écrans sur ordinateur, 7 sur mobile) :** chaque page porte la couleur de son offre (`of-acc--si|vig|sla|nox` sur `<main>`), en filets, points et coches seulement, jamais sur du texte.
  1. le hero et son exemple (masqué sur mobile : un seul exemple par page), puis **l'offre en bref** (rythme, démarrage, qui lit, tarif, repris du comparatif) et les logos ;
  2. « Est-ce pour vous ? » : pour vous si, et pas le bon choix si, chaque ligne menant à l'offre qui convient mieux ;
  3. **ce que vous recevez**, liste numérotée à côté d'un livrable réel en maquette (collant au défilement), relié à son cas d'usage ;
  4. comment ça se passe ;
  5. une interview en bandeau, choisie pour son propos (Vigie 360 : AXA, Social Insights : Dassault Systèmes, SLaaS : SNCF, Nox : Orange) ;
  6. l'aimant « Recevez un exemple… » propre à l'offre ;
  7. la FAQ (6 questions, dont le démarrage et la propriété des livrables) ;
  8. les trois autres offres en mini-cartes (défilement de côté sur mobile) et le lien vers le comparatif ;
  9. le rappel.
- **Pas de popup magazine automatique.** Sur téléphone, la barre du bas (Antoine, l'aimant, le consultant), « Ce qui est inclus » en liste compacte, la méthode sans photos.
- **Aucun prix n'est affiché** tant que la grille n'est pas validée : le comparatif dit « Grille sur demande » et renvoie vers l'aimant.

### Pages expertise (`tools/build-expertise.py`)

- **Deux langues statiques :** `expertise*.html` à la racine (anglais) et leurs jumelles françaises sous `/fr/expertise/…/`, avec `hreflang`, une URL canonique propre à chaque langue et le texte dans le HTML. Les liens du site vers ces pages pointent vers la version française quand la page est en français (`js/i18n.js`, `translate()` dans `build-usecases.py`).
- **Ordre d'une sous-page :**
  1. le hero, avec un exemple, puis les logos clients ;
  2. « Ce qu'elle entend, et ses limites » ;
  3. les questions auxquelles elle répond ;
  4. « Comment ça se passe » (délais) ;
  5. une interview client liée au sujet ;
  6. l'aimant « Recevez un exemple de livrable … » (e-mail et secteur) avec le lien vers le guide ;
  7. les plateformes et les offres ;
  8. la FAQ (4 questions) ;
  9. le rappel.
- **La page principale** a ses logos, l'aimant, et une FAQ de 4 questions.
- **Pas de popup magazine automatique** sur ces pages, comme sur les cas d'usage : leur aimant est l'exemple de livrable.
- **L'exemple du hero** est une page de rapport (logo, document, client anonymisé, source), et le titre du bloc de contact est propre à chaque écoute (« Parlons de votre veille en temps réel. »).
- **La page principale** a aussi une interview (Kantar) ; sur téléphone, les six écoutes s'affichent en liste compacte et les plateformes sont repliées.
- **La page principale montre aussi trois livrables** (bilan de campagne, cartes des communautés, fiche d'alerte), réduits depuis `tools/uc_deliverables.py` et reliés à leur cas d'usage, ainsi qu'un lien « Voir les 12 cas d'usage ».
- **Noms des écoutes :** on garde le terme anglais (« Social listening », celui que les gens cherchent), suivi en français d'un sous-titre (« l'écoute des conversations ») dans l'en-tête et la liste des six écoutes (`GLOSS`).
- **Sur téléphone,** « Les autres écoutes » et les trois livrables défilent sur une ligne.
- **Sur téléphone :** la même barre du bas que les cas d'usage (Antoine, « Recevoir un exemple », « Parler à un consultant »), la FAQ repliée, un seul signal dans l'exemple du hero.

### Maquettes de livrables (`tools/uc_deliverables.py`)

Chaque cas d'usage montre son livrable sous la forme d'une **vraie page de rapport Licter** : papier blanc dans les deux thèmes, avec une seconde feuille qui dépasse derrière.
- **En-tête :** le logo, le nom du document, le client anonymisé (« Marque alimentaire · Octobre 2026 ») et l'étiquette « Données illustratives ».
- **Corps :** le titre de section, avec un filet or et un sous-titre.
- **Pied :** la source et le volume analysé, puis « Licter · p. 4 / 16 ».
- **Graphiques :** axes gradués, grilles, courbes annotées, mini-tendances. Plancher de 12 px.

Les métadonnées de chaque livrable sont dans `META`. Les chiffres restent illustratifs, et sont signalés comme tels.

**Sous chaque maquette,** le lien « Recevoir un cas réel de ce type ↓ ». Le cas type porte la mention « Cas type · chiffres illustratifs » et se termine par « Les vrais chiffres d'une mission comparable, anonymisés : recevoir un cas réel → ».

### Horaires de rappel

Un consultant rappelle **dans les 30 minutes en semaine, de 9 h à 19 h** (heure de Paris). En dehors de ces horaires, aucun texte ne promet « 30 minutes » : le badge du popup, la confirmation et le chat disent quand le rappel aura lieu, et tous les textes de rappel du site précisent « en semaine » (« ce matin dès 9 h », « demain dès 9 h », « lundi dès 9 h »). L'utilitaire commun est `window.LicterHours`, dans `js/ui.js`.

### Appels à l'action

- **Primaire, partout :** « Parler à un consultant » (« Talk to a consultant »), qui mène à `#book`.
- `.cta-row` ferme une section qui argumente. Il est centré et contient un primaire, plus éventuellement un lien.
- Sur l'accueil, le CTA de la barre de navigation est placé **avant** le bouton de thème et le sélecteur EN/FR.

### Barres fixes (échelle de z-index)

| z | Élément |
|---|---|
| 30 | `.stickybar` : barre compacte avec le CTA, après le hero. En haut quand on remonte ; sur l'accueil mobile, **en bas et permanente** (`.stickybar--bottom`), masquée sur le formulaire |
| 35 | `.ucp-bar` : barre d'actions mobile des pages cas d'usage |
| 40 | `.banner` : bandeau du prochain événement, ou du guide, **collé en haut de toutes les pages**. Sa hauteur est publiée dans `--banner-h` (`js/events.js`) : la barre compacte se place juste dessous, et les ancres comme les panneaux collants en tiennent compte. Sur mobile, il tient sur deux lignes courtes, **s'efface quand on descend** et revient dès qu'on remonte |
| 45 | `.langoffer` : proposition de langue |
| 55 | `.ppd` : le bouton du magazine, en bas à gauche, **discret** : la couverture seule, inclinée, avec une petite étiquette dorée « Recevoir gratuitement » sur deux lignes. Il apparaît une fois le popup fermé sans envoi, jamais par-dessus le hero de l'accueil, ni par-dessus le formulaire de contact ou le pied de page. Sur l'accueil, sous 1200 px, la couverture passe **dans la barre du bas**, à côté d'Antoine, au lieu de flotter |
| 60 | `.lx__launch` : lanceur du chat Antoine, en bas à droite |
| 70 | `.lx__panel` : tiroir chat et rappel |
| 80 | `.pp` : popup magazine |

Un nouvel élément fixe prend sa place dans cette échelle, jamais `9999`.

### Bandeau d'événement

Il est généré par `tools/build-events.py` et mis à jour par `js/events.js`. Il contient l'étiquette « Prochain événement », le titre en gras, la date et le lieu, puis « S'inscrire → ». Il bascule seul sur l'événement suivant le lendemain de chaque date.

### Cartes

- `.card` : surface 72 %, `backdrop-filter: blur(6px)`, bordure `--line`, rayon 14px. Une carte n'existe que si c'est un objet cliquable ou un livrable. Sinon, on groupe avec de l'air ou un filet.
- `.ucc` : carte photo avec voile noir transparent et texte blanc par-dessus (familles de questions).

### Formulaires

- Hauteur 48 à 52px, rayon 8px, `--field-bg` / `--field-br`.
- Erreurs en ligne avec `aria-invalid` ; le message est placé sous le formulaire, puis le focus va au premier champ invalide.
- La confirmation remplace le formulaire et reçoit le focus. Elle reprend le prénom et l'e-mail saisis.
- **Tous les formulaires sont des maquettes** (commentaire `MOCK`) : rien n'est envoyé tant que le CRM n'est pas branché.

### Panneaux et popups

- **Le rappel** (« Trente minutes avec un consultant ») s'ouvre sur **chaque « Parler à un consultant »** : tout lien vers `#book`, ou qui porte ces mots. Un cmd-clic suit toujours le lien. Il est en deux volets : la photo de l'équipe avec les badges « Réponse sous 30 min » et « 160+ projets depuis 2022 », puis le formulaire. Sur téléphone, la photo devient un bandeau et le clavier ne s'ouvre pas tout seul. Il ne s'ouvre jamais de lui-même.
- **Le magazine** s'ouvre une seule fois par visiteur, **centré**, après 3 s, **sur tous les écrans, mobile compris**. Il ne demande **que l'e-mail**.
- **Sur téléphone, les popups sont des panneaux qui montent du bas**, pas des plein-écrans : la page reste visible au-dessus. Le magazine y garde une petite couverture, le titre et le champ (322 px de haut). Sur l'accueil, il attend que l'argument soit passé : après la démo sur grand écran, après « Pourquoi pas un outil seul » sur téléphone. Une fois fermé sans envoi, il reste accessible depuis son bouton en bas à gauche. Il est réservé aux écrans larges et ne s'ouvre jamais sur une page de formulaire. Une fois fermé, il reste accessible dans le dock `.ppd`.
- **Le tiroir d'Antoine** glisse depuis la droite. Il a deux onglets, chat et rappel. Chaque réponse du chat se termine par un CTA.
  - **Sur téléphone, il occupe tout l'écran.** Sa hauteur suit le clavier (visual viewport). Les champs sont en 16px, pour qu'iOS ne zoome pas. Le clavier ne s'ouvre pas tout seul. La page derrière est bloquée. Les questions suggérées défilent sur une ligne.
- Aucune autre popup automatique : le magazine est le seul à s'ouvrir sans clic.

---

### Mesure d'audience

`js/track.js` (chargé par `js/ui.js` sur toutes les pages) expose `window.LicterTrack(nom, props)`. Chaque événement part dans `dataLayer` (prêt pour Google Tag Manager), et vers Plausible ou GA4 s'ils sont présents sur la page. Aucun outil externe n'est chargé par défaut. Pour activer Plausible (sans cookie, sans bandeau), il suffit de renseigner `PLAUSIBLE_DOMAIN`. GA4 et GTM demandent d'abord un bandeau de consentement.

| Événement | Quand |
|---|---|
| `popup_open`, `popup_close`, `popup_submit` | magazine ou rappel ; `close` = fermé sans envoi |
| `cta_click` | un « Parler à un consultant », avec la section d'origine |
| `bar_click` | la barre compacte : `cta`, `chat` ou `mag` |
| `chat_open` | le tiroir d'Antoine |
| `quiz_complete`, `quiz_email` | le quiz terminé (avec le score), puis l'e-mail laissé |
| `form_submit` | rappel, guide, diagnostic, rendez-vous, newsletter, événement |

Tout nouveau formulaire ou aimant envoie son événement.

## 7. Images

- **Formats :** WebP en `-800` et pleine taille, servis via `srcset`. Avatars en `-160`. Les JPEG d'origine restent dans `assets/img/` comme sources (Pillow, qualité 80).
- **Contenu :** photos réelles de l'équipe Licter, des clients et des événements. Les visages des consultants sont présentés en rond, sur une ligne.
- **Logos clients :** silhouettes monochromes, navy en clair et crème en sombre.
- **Vidéos clients :** YouTube en `youtube-nocookie`, chargées au clic. **La vidéo `l-OevQ4q8js` (Paris 2024) ne doit jamais apparaître.**
- Chaque image porte un `alt` qui décrit la scène, ou `alt=""` si elle est purement décorative.

---

## 8. Rédaction

- **Langue :** le français est la langue par défaut. Le HTML source est en anglais ; la traduction est appliquée par `js/i18n.js` + `js/fr.js`, ou écrite en dur dans les pages générées sous `/fr/`.
- **Pas de tiret cadratin ni demi-cadratin** dans le texte visible. On utilise un point, une virgule, deux-points ou des parenthèses. Le « · » sert de séparateur dans les étiquettes courtes.
- **Typographie française :** espace insécable avant `: ; ? !` et à l'intérieur des « ». Les textes affichés par la démo (`js/usecases.js`) la reçoivent automatiquement.
- **Le ton :** concret et à la première personne du pluriel. On écrit « nous lisons », pas « solution innovante ». Aucun mot creux du type « révolutionner », « booster » ou « next-gen ».
- **Les titres sont en casse de phrase,** jamais en Title Case.
- **Les chiffres sont réels et sourcés,** ou bien la donnée est signalée comme illustrative.

---

## 9. Accessibilité (plancher)

- **Contraste AA** sur tout texte utile, à vérifier dans les deux thèmes avec axe-core (0 violation aujourd'hui).
- **Focus visible** sur chaque élément interactif. `Échap` ferme les menus, le tiroir et les popups. Les liens d'évitement restent en place.
- **Zones cliquables d'au moins 44px** sur mobile.
- **Un seul H1 par page,** et une hiérarchie de titres sans saut.

---

## 10. Ajouter quelque chose : la marche à suivre

1. **Écrire le CSS dans `css/styles.css`,** jamais dans `styles.min.css`.
2. **Pour une page générée** (cas d'usage, offres, expertises, événements, `/fr/`), éditer le générateur dans `tools/`, puis lancer :
   ```bash
   python3 tools/build-usecases.py   # lance aussi events, offers, expertise, home
   python3 tools/build-css.py        # TOUJOURS après le build
   ```
   `build-css.py` supprime les sélecteurs absents du HTML et du JS : s'il tourne avant la génération des pages, les nouvelles classes disparaissent.
3. **Mettre à jour la version de cache** `?v=` dans tous les HTML.
4. **Vérifier :**
   - en clair et en sombre ;
   - en 1440 et en 390px ;
   - en FR et en EN ;
   - axe ;
   - aucun défilement horizontal ;
   - aucun tiret dans le texte visible.

---

## 11. Dettes connues

- La police Aiglon est préchargée avec `?v=`, alors que le CSS la charge sans : elle est téléchargée deux fois.
- Les formulaires ne sont pas branchés au CRM.

### Citations des interviews

Chaque citation reprend **mot pour mot** la phrase incrustée sur la miniature de sa vidéo YouTube : le visiteur voit les deux côte à côte. Elles vivent dans `VOICES` (`tools/uc_content.py`) pour les pages générées, dans `js/voices.js` et `index.html` pour l'accueil, et leur traduction dans `js/fr.js`. Une nouvelle interview : recopier la phrase de la miniature, ne jamais la résumer.

### Techno & outils (menu et `tech-tools.html`)

- **Le menu** (`js/ui.js`, `MENUS.tech`) : les cinq plateformes avec leur description (Talkwalker, Visibrain, YouScan, SoPrism, Radarly), puis « Et, selon la question » : les huit outils d'appoint, par leur nom seul (Semrush, Google Trends, AnswerThePublic, ChatGPT, GEO, Meta Ads, Google Actualités, Social Blade). À droite, « D'où viennent les données » : les 22 réseaux en deux colonnes. Le tout tient dans un écran de 900 px de haut. Sur téléphone, le menu ne montre que les liens : le détail est sur la page.
- **La page** : la liste des plateformes (Radarly n'a pas de page à lui, sa ligne n'est pas un lien), les outils d'appoint en cartes (`#more`), et `#sources` : les réseaux en cinq groupes (réseaux sociaux, vidéo et live, messageries et communautés, Chine et Russie, recherche, presse et IA).
- **Les glyphes des réseaux** sont des SVG Simple Icons (CC0) dans `assets/img/networks/`, affichés en monochrome par `mask-image` avec un chemin absolu (`--g:url(/assets/...)`) : un chemin relatif se résoudrait depuis la feuille de style et ne s'afficherait pas.

### Pages outils et réseaux (`tools/build-tech.py`)

- **40 pages générées, en deux langues statiques** : 17 outils (`tech-<outil>.html`, `/fr/outils/<outil>/`, contenu dans `tools/tools_data.py`), dont les 5 assistants IA (ChatGPT, Claude, Gemini, Perplexity, Grok) ; 22 réseaux (`source-<réseau>.html`, `/fr/sources/<réseau>/`, contenu dans `tools/networks.py`) ; la page Techno & outils (`/fr/outils/`). Coque : `tools/tech-shell.html`. Canonique, `hreflang`, fil d'Ariane et FAQ en données structurées sur chacune.
- **Aucune donnée illustrative** : les visuels sont réels. Hero : le site officiel de l'outil ou du réseau, capturé en octobre 2026 (`assets/img/shots/`, source affichée sous l'image) ; pour Douyin, une photo Wikimedia Commons créditée ; sur Weibo, les publications d'utilisateurs sont floutées. Les cas d'usage et les livrables montrent les photos de l'équipe Licter. Les logos des outils sont dans `assets/img/tools/`.
- **Structure d'une page outil** : hero (H1 « Agence X »), « Qu'est-ce que X ? » avec la fiche, « Ce que X permet d'analyser » en bento (la première carte en couleur de marque, sur un extrait du site réel), « Pourquoi passer par une agence X ? » (X seul contre X avec Licter, puis les trois étapes en frise), « Ce que nous livrons » (carrousel connecté : la carte active au centre, les autres en capsules avec leur titre vertical), les cas d'usage (carrousel progressif : une photo, les cas en onglets avec barre de progression), « Limites et compléments » (carrousel de cartes : les limites, puis les outils qui les compensent), la FAQ, l'appel final.
- **Structure d'une page réseau** : hero (H1 « Social listening X ») sur un panneau aux couleurs du réseau, « Pourquoi écouter X ? » en bento, « Données et limites » (carrousel : ce que nous collectons, ce que nous ne lisons pas, puis les outils dont l'éditeur dit couvrir ce réseau), la méthode, les cas d'usage, les autres réseaux, la FAQ.
- **Les carrousels** (`js/ui.js`) défilent seuls quand ils sont à l'écran, s'arrêtent au survol et au focus, et restent fixes si l'utilisateur réduit les animations. Les liens vers les cas d'usage et les outils sont de vrais liens, lisibles par les moteurs.
- **La page Techno & outils** : une orbite en hero (le logo Licter au centre, les outils et les réseaux autour) ; les quatre couches en sélecteur (un panneau ouvert sur une photo de l'équipe, les autres repliés avec leur titre sur la tranche, en accordéon sur téléphone) ; les outils en catalogue compact (5 plateformes en cartes, 12 outils d'appoint en lignes logo + nom) ; les sources en deux bandeaux de logos qui défilent, comme le mur des clients, chaque logo prenant sa couleur au survol ; « Collecter, qualifier, décider » en étapes à gauche et image à droite qui change avec l'étape. Script : `js/ui.js` (« Tech & tools hub »).
- **« Agence X »** (outils) et **« agence social listening X »** (réseaux) reviennent dans le titre, la description, l'accroche, une question de FAQ et l'appel final.

### Pourquoi Licter (`why-licter.html`) : une page studio

Écrite à la main, traduite par `js/fr.js`, styles `.wl-*`, script « Why Licter » dans `js/ui.js`. Huit temps :
1. **le manifeste** : « Remplacer l'intuition par la donnée » en très grande capitale, mot à mot, « l'intuition » en contour barrée d'un trait ambre ; quelques visages de l'équipe flottent autour ;
2. **un bandeau ambre incliné** qui défile (écouter, lire, décider, les quatre couches) ;
3. **l'origine** : « 2022 » en filigrane, l'histoire, les deux fondateurs et leur photo ;
4. **en chiffres**, sur fond navy, les nombres comptent jusqu'à leur valeur ;
5. **la différence**, en grandes lignes : au survol, une photo suit le pointeur (sur mobile, la photo est dans la ligne) ;
6. **trois équipes** en cartes photo, celle du milieu décalée ;
7. **l'équipe** : la photo de groupe en pleine largeur avec un léger parallaxe, puis les portraits qui défilent ;
8. **l'appel final** en très grande capitale, avec le formulaire.
La taille des grands titres suit la largeur de leur colonne (`cqi`) pour tenir en français comme en anglais. Tout reste immobile si l'utilisateur réduit les animations.

### Clients (`clients.html`) : une page éditoriale

Une direction différente de « Pourquoi Licter » : le registre d'un rapport annuel. Styles `.cl-*`, script « Clients » dans `js/ui.js`.
1. **Le hero** : la promesse en titre posé, à droite une planche « Index des clients » (9 logos en grille au filet, ombre ambre décalée) ;
2. **un registre de chiffres** entre deux filets (organisations, projets, langues, secteurs) ;
3. **l'index des 39 clients** (liste fournie par Licter, chaque client compté une fois), numérotés, en grille au filet, logos en gris qui prennent leur couleur au survol, avec un filtre par secteur (Luxe, beauté & mode · Grande consommation & santé · Distribution, mobilité & tech · Finance & services · Institutions, culture & médias) ; une 40e case invite à prendre rendez-vous. La même liste alimente le bandeau de logos de toutes les pages (`CLIENTS` dans `js/ui.js`) ; les logos posés sur un aplat (LEGO, Orange, Bandai, Fleury Michon, Norauto) portent `box: true` et restent gris en mode sombre au lieu de virer au blanc.
4. **les entretiens vidéo** : la liste des intervenants à gauche, une seule citation à la une avec sa vidéo ;
5. **les quatre questions** en grille 2 × 2, chacune avec une photo de l'équipe en noir et blanc qui prend sa couleur au survol ;
6. **l'appel final** dans un panneau navy filet ambre.

### Expertise (`tools/build-expertise.py`) : refonte d'octobre 2026

- **Les mêmes composants que les pages outils** (`.tk-*`) et la page Offres (`.ucc`), une seule couleur (l'ambre Licter) ; aucune donnée illustrative.
- **Le hero est un aimant à leads : le guide des 12 questions.** À gauche, le titre dans le registre de l'accueil (deux lignes en capitales, la seconde en ambre), le chapô, « Gratuit · Envoyé immédiatement · Sans relance » et un lien vers le rappel. À droite, la couverture du guide (le « 12 » et les douze numéros) et le même formulaire que `guide.html` (prénom, nom, e-mail, entreprise facultative), puis « Écrit par les consultants qui les mènent » avec le lien vers le sommaire. La barre mobile pointe vers ce formulaire (`#offre`).
- **Page d'une écoute** : ce qu'elle entend (bento, photo de l'équipe), les questions auxquelles elle répond (carrousel de cas d'usage), comment ça se passe (quatre étapes), ses limites et ce qui la complète (carrousel : la limite, les plateformes, les offres), une interview, les cinq autres écoutes, la FAQ, le rappel.
- **Page Expertise** : les six écoutes en cartes photo comme les familles de cas d'usage, l'exemple « une question, plusieurs écoutes », une interview, la FAQ, le rappel.
