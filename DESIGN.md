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
  - **Retiré :** la cartographie du hero (elle n'est même pas dessinée).
  - **Familles :** même carte que sur ordinateur, en carrousel au doigt (86 % de largeur, la suivante dépasse), sans flèches.
  - **Vidéos :** une à la fois, sans la note sur la chaîne.
- **Pied de page sur téléphone (tout le site) :** les quatre colonnes deviennent des volets, un seul ouvert à la fois (`js/ui.js`), et le paragraphe de présentation est retiré.
- **Vidéos de l'accueil :** la citation sous la miniature est masquée visuellement, puisque la miniature l'affiche déjà. Elle reste le nom du lien pour les lecteurs d'écran et Google.
  - **« Pourquoi pas un outil seul » + Équipe :** le titre, le badge et les visages, puis un tableau à deux colonnes « Un outil seul / Notre équipe ». Le chapô et la phrase de fin, redondants avec le tableau, sont retirés ; le mot des fondateurs est replié. Les éléments d'équipe sont déplacés en JS (`js/home.js`), jamais copiés.
  - **Démo retirée :** ses 4 questions répètent les 4 familles, et chaque page famille a sa propre démo mobile.
  - **Méthode :** mêmes cartes que sur ordinateur (photo, étapes, flèches).
  - **Diagnostic :** replié derrière un bouton. Un lien `#diagnostic` l'ouvre.
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

### Appels à l'action

- **Primaire, partout :** « Parler à un consultant » (« Talk to a consultant »), qui mène à `#book`.
- `.cta-row` ferme une section qui argumente. Il est centré et contient un primaire, plus éventuellement un lien.
- Sur l'accueil, le CTA de la barre de navigation est placé **avant** le bouton de thème et le sélecteur EN/FR.

### Barres fixes (échelle de z-index)

| z | Élément |
|---|---|
| 30 | `.stickybar` : barre compacte avec le CTA, après le hero. En haut quand on remonte ; sur l'accueil mobile, **en bas et permanente** (`.stickybar--bottom`), masquée sur le formulaire |
| 35 | `.ucp-bar` : barre d'actions mobile des pages cas d'usage |
| 40 | `.banner` : bandeau du prochain événement, ou du guide. Il **défile avec la page** : s'il restait collé, il recouvrirait la barre compacte |
| 45 | `.langoffer` : proposition de langue |
| 55 | `.ppd` : dock « Le magazine », en bas à gauche |
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

### Bloc « Pas encore prêt à parler ? » (accueil)

Il s'adresse au visiteur qui n'est pas prêt pour un rappel. Il est placé après l'équipe, avant le diagnostic, sur ordinateur comme sur mobile, et contient trois cartes :
- **le magazine**, avec un seul champ (e-mail) ;
- **le guide des 12 questions**, avec un seul champ ;
- **le prochain événement**, rempli par `js/events.js`, qui passe seul au suivant.

Une fois le magazine demandé ici, son popup ne s'ouvre plus. Les formulaires sont des maquettes.

### Panneaux et popups

- **Le rappel** (« Trente minutes avec un consultant ») s'ouvre sur **chaque « Parler à un consultant »** : tout lien vers `#book`, ou qui porte ces mots. Un cmd-clic suit toujours le lien. Il est en deux volets : la photo de l'équipe avec les badges « Réponse sous 30 min » et « 160+ projets depuis 2022 », puis le formulaire. Sur téléphone, la photo devient un bandeau et le clavier ne s'ouvre pas tout seul. Il ne s'ouvre jamais de lui-même.
- **Le magazine** s'ouvre une seule fois par visiteur, **centré**, après 3 s. Sur l'accueil, il attend que les vidéos clients soient passées (environ 40 % de la page), et le dock n'y apparaît pas : le magazine a son propre bloc. Il est réservé aux écrans larges et ne s'ouvre jamais sur une page de formulaire. Une fois fermé, il reste accessible dans le dock `.ppd`.
- **Le tiroir d'Antoine** glisse depuis la droite. Il a deux onglets, chat et rappel. Chaque réponse du chat se termine par un CTA.
  - **Sur téléphone, il occupe tout l'écran.** Sa hauteur suit le clavier (visual viewport). Les champs sont en 16px, pour qu'iOS ne zoome pas. Le clavier ne s'ouvre pas tout seul. La page derrière est bloquée. Les questions suggérées défilent sur une ligne.
- Aucune autre popup automatique : le magazine est le seul à s'ouvrir sans clic.

---

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
