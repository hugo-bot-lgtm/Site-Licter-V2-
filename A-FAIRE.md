# À faire en dernier

Deux chantiers restent avant que le site rapporte vraiment des leads. Le design et le parcours sont terminés (accueil noté 9/10 au dernier audit). Ce qui manque est en coulisses :

| Chantier | Effet attendu |
|---|---|
| 1. Brancher les formulaires au CRM | aimants à leads 8,5 → 9,5 : les demandes arrivent enfin quelque part |
| 2. Activer l'outil d'audience (Plausible recommandé) | les prochaines décisions se prennent sur des chiffres, pas à l'intuition |

Avant de commencer : choisir le CRM (HubSpot, Brevo, Pipedrive…) et l'outil d'audience.

---

## 1. Brancher les formulaires au CRM

### Ce qui se passe aujourd'hui

Tous les formulaires valident la saisie et affichent leur confirmation, mais **n'envoient rien**. Chaque endroit à brancher est marqué dans le code par un commentaire `MOCK` (ou `wire to the real endpoint here`). On le retrouve avec :

```bash
grep -rn "MOCK\|wire to the real endpoint" js/
```

### Les formulaires à brancher

| Formulaire | Où il apparaît | Fichier (repère dans le code) | Données | Suite à donner côté CRM |
|---|---|---|---|---|
| **Rappel, popup** « Trente minutes avec un consultant » | toutes les pages, sur chaque « Parler à un consultant » | `js/popups.js`, `MOCK: send { contact: v, kind }` | e-mail **ou** téléphone, et son type | alerte immédiate à un consultant ; rappel sous 30 min en semaine (9 h à 19 h) |
| **Rappel, bas de page** | accueil, offres, expertises, cas d'usage (section contact) | `js/ui.js`, `MOCK: wire to the CRM here (contact, kind)` | idem | idem |
| **Rappel, chat d'Antoine** | onglet « Être rappelé » du chat, toutes les pages | `js/assistant.js`, `MOCK: wire to the CRM here (v, k)` | idem | idem |
| **Magazine Audience First** | popup automatique (toutes les pages) | `js/popups.js`, `MOCK: send { email } to the CRM` | e-mail | envoi automatique du PDF par e-mail ; inscription aux numéros suivants si consentement |
| **Guide des 12 questions** | `guide.html` | `js/ui.js`, formulaires `.form`, `wire to the real endpoint here` | prénom, nom, e-mail, entreprise (facultative) | envoi automatique du guide |
| **Demande de diagnostic** | `diagnostic.html` | `js/ui.js`, même gestionnaire | nom, entreprise, e-mail, téléphone, contexte | tâche pour un consultant |
| **Prise de rendez-vous** | `book-a-meeting.html` | `js/ui.js`, même gestionnaire | nom, entreprise, e-mail, question | tâche pour un consultant |
| **Quiz diagnostic (e-mail final)** | accueil | `js/home.js`, `MOCK: wire to the CRM here (score, answers, email)` | e-mail, score sur 12, réponses | envoi du détail par e-mail ; lead qualifié par le score |
| **Inscription aux événements** | `event-*.html` | `js/events.js`, `MOCK: send { event, first, last, company, email }` | prénom, nom, société, e-mail, date de l'événement | e-mail de confirmation **manuel** (la place n'est garantie qu'après confirmation) |
| **« Recevoir un cas réel »** | pages famille et cas d'usage | `js/home.js` (`.ucp-lead`), `MOCK: send { email, case, sector }` | e-mail, cas, secteur | envoi du cas correspondant |
| **Cas réel depuis la démo** | démo des pages cas d'usage | `js/usecases.js`, `MOCK: send { email, topic, sector }` | e-mail, sujet, secteur | idem |
| **Newsletter et bandeaux d'e-mail** | pied de page et blocs « signup » (blog, articles…) | `js/ui.js`, second `wire to the real endpoint here` | e-mail | inscription newsletter (double opt-in) |

### La méthode recommandée

1. **Une seule fonction d'envoi pour tout le site**, par exemple `window.LicterSubmit(type, données)` dans `js/ui.js`. Chaque repère `MOCK` l'appelle au lieu de ne rien faire. Un seul endroit à maintenir.
2. **Passer par une fonction serveur Vercel** (`/api/lead`), qui relaie vers le CRM. Les clés d'accès au CRM ne doivent **jamais** apparaître dans le JavaScript du site, qui est public.
3. **Ne montrer la confirmation qu'après la réponse du serveur.** En cas d'échec, afficher un message clair (« L'envoi n'a pas abouti. Réessayez, ou écrivez-nous à … ») au lieu d'une fausse confirmation.
4. **Garder le suivi d'audience** : chaque envoi réussi déclenche déjà un événement (`popup_submit`, `form_submit`, `quiz_email`). Il ne faut pas le retirer.

### À prévoir côté CRM et e-mails

- **Les automatisations d'envoi :** PDF du magazine, guide, détail du quiz, cas réel.
- **L'alerte aux consultants pour les rappels.** La promesse affichée est « dans les 30 minutes, en semaine de 9 h à 19 h ». En dehors, le site annonce le moment du rappel (« lundi dès 9 h »), voir `window.LicterHours` dans `js/ui.js`. Les horaires du CRM doivent correspondre.
- **Le consentement (RGPD) :** chaque formulaire dit à quoi servent les coordonnées. Pour envoyer ensuite d'autres contenus (newsletter, numéros suivants du magazine), il faut un consentement explicite, ou un double opt-in.
- **La politique de confidentialité** (`privacy.html`) doit nommer le CRM et l'outil d'audience retenus.

### Vérifications avant mise en ligne

- [ ] Chaque formulaire du tableau arrive dans le CRM, avec les bons champs.
- [ ] Les e-mails automatiques partent (magazine, guide, quiz, cas réel), et ne tombent pas en spam.
- [ ] Un rappel laissé un samedi soir annonce bien « lundi dès 9 h », et le consultant le reçoit lundi.
- [ ] Une panne du CRM affiche un message d'erreur clair, pas une fausse confirmation.
- [ ] Les commentaires `MOCK` sont retirés du code.
- [ ] La politique de confidentialité est à jour.

---

## 2. Activer l'outil d'audience

### Ce qui est déjà prêt

`js/track.js` est chargé sur toutes les pages et enregistre déjà ce que font les visiteurs. Rien n'est encore envoyé à un outil : les événements restent dans `window.dataLayer`.

| Événement | Ce qu'il mesure |
|---|---|
| `popup_open`, `popup_close`, `popup_submit` | ouverture, fermeture sans envoi et envoi, pour le magazine et pour le rappel |
| `cta_click` | quel « Parler à un consultant » est cliqué, avec sa section d'origine |
| `bar_click` | la barre du bas : contact, Antoine ou magazine |
| `chat_open` | ouverture du chat d'Antoine |
| `quiz_complete`, `quiz_email` | quiz terminé (avec le score), puis e-mail laissé |
| `form_submit` | chaque formulaire envoyé : rappel, guide, diagnostic, rendez-vous, newsletter, événement |

### Option recommandée : Plausible

Plausible fonctionne **sans cookie**, donc **sans bandeau de consentement**, et ses données sont hébergées en Europe.

1. Créer un compte sur plausible.io et y ajouter le domaine du site.
2. Dans `js/track.js`, remplir la ligne `var PLAUSIBLE_DOMAIN = "";` avec le domaine (par exemple `"licter.com"`).
3. Dans Plausible, créer un **objectif personnalisé** (Goal) pour chacun des 10 événements du tableau.
4. Mettre à jour la version de cache (`?v=`) de tous les HTML, puis vérifier dans Plausible que les visites et les événements arrivent.

Coût : environ 9 € par mois pour 10 000 visites mensuelles.

### Alternative : Google Analytics 4 ou Google Tag Manager

Ils déposent des cookies. **Il faut d'abord un bandeau de consentement conforme CNIL** (accepter et refuser au même niveau, rien de chargé avant l'accord). Une fois le bandeau en place, GTM lit directement `window.dataLayer`, et GA4 reçoit les événements via `gtag`, sans autre modification de `js/track.js`.

### Les chiffres à suivre dès le premier mois

| Indicateur | Calcul | Décision qu'il éclaire |
|---|---|---|
| Taux de fermeture du popup magazine | `popup_close` ÷ `popup_open` (mag) | s'il dépasse environ 85 %, ouvrir le popup plus tard ou le retirer sur mobile |
| Conversion du magazine | `popup_submit` ÷ `popup_open` (mag) | valeur de l'aimant ; comparer ordinateur et mobile |
| « Parler à un consultant » le plus utile | `cta_click` par section | garder les bons emplacements, retirer les autres |
| Usage de la barre du bas | `bar_click` par cible | la place du magazine et d'Antoine dans la barre |
| Taux de fin du quiz | `quiz_complete` ÷ visites de l'accueil | si le quiz est peu terminé, le raccourcir |
| Leads par aimant | `form_submit` et `popup_submit` par type | où investir le prochain contenu |

---

## 3. Remplacer les chiffres illustratifs par de vrais cas

Les maquettes de livrables (`tools/uc_deliverables.py`) et les cas types (`tools/uc_content.py`, `example` et `EXTRA`) utilisent des **chiffres inventés**, signalés « Données illustratives » et « Cas type · chiffres illustratifs ». Ils ne doivent pas être présentés comme réels.

Dès que des missions réelles sont validées pour publication (anonymisées, avec l'accord du client) :
- remplacer les chiffres de la maquette correspondante et du cas type ;
- retirer l'étiquette « illustratif » de ces seules pages ;
- garder le client anonymisé (« Marque alimentaire »), sauf accord écrit.

Ce sont aussi ces cas réels qu'envoie l'aimant « Recevoir un cas réel » : il faut en préparer au moins un par cas d'usage (12) avant de brancher le formulaire.

De même pour les pages expertise : l'aimant « Recevez un exemple de livrable » promet un envoi sous 48 h. Il faut **un exemple anonymisé par écoute (6)** : social, audience, influence, IA, temps réel, recherche. Les exemples des heros de ces pages (`tools/build-expertise.py`, `demo` et `doc`) sont illustratifs eux aussi.

## Le jour de la bascule sur le vrai domaine

Le site pointe déjà vers `https://www.licter.com` pour les URL canoniques, les `hreflang` et le sitemap (`SITE` dans `tools/uc_content.py`). Il faudra vérifier ces liens une fois le domaine branché, et utiliser ce même domaine dans Plausible.
