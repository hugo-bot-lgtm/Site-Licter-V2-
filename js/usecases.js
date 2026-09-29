/* =========================================================================
   Licter — use cases (home). Four questions, each with its own visual, and
   each told through four sectors (food, luxury, toys & video games,
   automotive). Every time a question is opened the next sector is shown, so
   a visitor does not see the same case twice in a row.

     communication  a volume curve that draws itself; drag the launch line
     brand          a word cloud that fills word by word; filter, click a word
     audiences      communities that form one by one on a map, with scores
     trends         topics racing over 18 months

   The panel on the right follows the visual: posts read, two posts, then
   our read (the finding, two facts, a recommendation).

   MOCK: every post, handle and figure below is illustrative. Replace with
   anonymised client material before going live.
   ========================================================================= */
(function () {
  "use strict";

  var stage = document.getElementById("cases-panel");
  var topics = Array.prototype.slice.call(document.querySelectorAll(".lf__topic[data-topic]"));
  if (!stage || !topics.length) return;

  var html = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  function fr() { return html.lang === "fr"; }
  function t(en, frText) { return fr() ? frText : en; }
  function L(pair) { return fr() ? pair[1] : pair[0]; }
  function num(n) { return Math.round(n).toLocaleString(fr() ? "fr-FR" : "en-GB"); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;"); }

  var PLATFORM_NAMES = { TIKTOK: "TikTok", INSTAGRAM: "Instagram", X: "X", YOUTUBE: "YouTube", LINKEDIN: "LinkedIn", FACEBOOK: "Facebook", TWITCH: "Twitch" };

  /* ============================================================ sectors */
  var SECTORS = [
    { key: "food", name: ["Food", "Agroalimentaire"] },
    { key: "luxury", name: ["Luxury", "Luxe"] },
    { key: "toys", name: ["Toys & video games", "Jouets & jeux vidéo"] },
    { key: "auto", name: ["Automotive", "Automobile"] }
  ];
  /* the next sector each time a question is opened: a random start, then
     round the four, so the same case never shows twice in a row */
  var STORE = "licter-cases";
  function nextSector(topic) {
    var seen = {};
    try { seen = JSON.parse(sessionStorage.getItem(STORE) || "{}") || {}; } catch (e) { seen = {}; }
    var i = typeof seen[topic] === "number" ? (seen[topic] + 1) % SECTORS.length : Math.floor(Math.random() * SECTORS.length);
    seen[topic] = i;
    try { sessionStorage.setItem(STORE, JSON.stringify(seen)); } catch (e) { /* private mode */ }
    return i;
  }

  /* ============================================================== data
     posts:   [platform, handle, sentiment -1/0/1, EN, FR]
     read:    posts read for the case; every other count on screen adds up
              to it (the campaign's is the sum of its own curve)
     tones:   brand only, % of posts negative / neutral / positive
     insight: a headline, two facts, a recommendation */
  var CASES = {

    /* ------------------------------------------------ 1. communication
       curve: daily volume before and after the launch; bumps are later
       waves [day, extra posts, width]. peaks: what happened there. */
    communication: {
      food: {
        subject: ["Spring sauce campaign", "Campagne sauce de printemps"],
        curve: { base: 800, launch: 21, spike: 2500, plateau: 760, bumps: [[27, 520, 2], [34, 420, 3]] },
        peaks: [
          { d: 23, pf: "TIKTOK", h: "@chef.maud", tag: ["Creator video", "Vidéo créateur"], txt: ["The recipe video that started it: 1.2M views in 48 hours.", "La vidéo recette qui a tout lancé : 1,2 M de vues en 48 heures."] },
          { d: 27, pf: "INSTAGRAM", h: "@thomas.run", tag: ["Stories wave", "Vague de stories"], txt: ["Stories reshare the recipe three days in a row.", "Les stories repartagent la recette trois jours d'affilée."] },
          { d: 34, pf: "YOUTUBE", h: "@foodtest", tag: ["YouTube test", "Test YouTube"], txt: ["A long test of the three recipes brings it back.", "Un long test des trois recettes relance la conversation."] }
        ],
        posts: [
          ["TIKTOK", "@lea.cuisine", 1, "Okay, the recipe @chef.maud made with the new sauce is actually insane.", "Ok, la recette que @chef.maud a faite avec la nouvelle sauce est vraiment folle."],
          ["INSTAGRAM", "@thomas.run", 1, "Saw it in three stories today. Buying it this weekend.", "Vu dans trois stories aujourd'hui. Je l'achète ce week-end."],
          ["X", "@nadia_b", 0, "The TV ad is fine, but nobody I know watches TV anymore.", "La pub télé est correcte, mais plus personne autour de moi ne regarde la télé."],
          ["TIKTOK", "@sarah.k", 1, "Added to cart, no questions asked.", "Ajouté au panier, sans réfléchir."]
        ],
        insight: {
          head: ["Creators carried it, not the ad.", "Ce sont les créateurs qui l'ont portée, pas la pub."],
          facts: [["46 % of posts share creator videos; the ad itself, 14 %.", "46 % des posts partagent des vidéos de créateurs ; la pub elle-même, 14 %."],
                  ["28 % say they want to buy, three times the category average.", "28 % disent vouloir acheter, trois fois la moyenne de la catégorie."]],
          reco: ["Move a third of paid media to creator partnerships for the autumn launch.", "Basculer un tiers du média payé vers des partenariats créateurs pour le lancement d'automne."]
        }
      },
      luxury: {
        subject: ["Fragrance launch at Fashion Week", "Lancement parfum à la Fashion Week"],
        curve: { base: 520, launch: 20, spike: 1900, plateau: 880, bumps: [[26, 760, 3], [33, 420, 3]] },
        peaks: [
          { d: 21, pf: "INSTAGRAM", h: "@maison.critique", tag: ["Runway show", "Défilé"], txt: ["The show goes viral on Instagram within the hour.", "Le défilé devient viral sur Instagram dans l'heure."] },
          { d: 26, pf: "TIKTOK", h: "@scentdiaries", tag: ["Unboxings", "Unboxings"], txt: ["Unboxing videos: the bottle becomes the star.", "Vidéos d'unboxing : le flacon devient la star."] },
          { d: 33, pf: "YOUTUBE", h: "@perfumecritic", tag: ["Long review", "Critique vidéo"], txt: ["A 40-minute review keeps collectors talking.", "Une critique de 40 minutes fait parler les collectionneurs."] }
        ],
        posts: [
          ["INSTAGRAM", "@maison.critique", 1, "The show was pure poetry. That bottle, though.", "Le défilé, de la poésie pure. Et ce flacon…"],
          ["TIKTOK", "@scentdiaries", 1, "Unboxing the new one. The box alone is a gift.", "Unboxing du nouveau. L'écrin à lui seul est un cadeau."],
          ["X", "@luxwatcher", 0, "Nice campaign, but who is it for at that price?", "Belle campagne, mais pour qui à ce prix ?"],
          ["YOUTUBE", "@perfumecritic", 1, "Long review: the top notes are better than the ad suggests.", "Critique complète : les notes de tête valent mieux que la pub."]
        ],
        insight: {
          head: ["The show made noise; the unboxings made desire.", "Le défilé a fait du bruit ; les unboxings ont créé le désir."],
          facts: [["Buzz peaks at the show; purchase intent peaks six days later.", "Le buzz culmine au défilé ; l'intention d'achat, six jours plus tard."],
                  ["62 % of intent posts mention the bottle, 11 % the scent.", "62 % des posts d'intention citent le flacon, 11 % le parfum."]],
          reco: ["Seed 30 unboxing creators before the next drop, not after.", "Équiper 30 créateurs d'unboxing avant le prochain lancement, pas après."]
        }
      },
      toys: {
        subject: ["Video game trailer reveal", "Révélation du trailer d'un jeu"],
        curve: { base: 1500, launch: 22, spike: 6200, plateau: 1600, bumps: [[28, 2600, 3], [33, 1700, 2]] },
        peaks: [
          { d: 23, pf: "X", h: "@leakhunter", tag: ["Trailer", "Trailer"], txt: ["The trailer: 4M views on day one.", "Le trailer : 4 M de vues le premier jour."] },
          { d: 28, pf: "TWITCH", h: "@gamerzone", tag: ["Twitch streams", "Streams Twitch"], txt: ["Beta streams keep the conversation going for a week.", "Les streams de la bêta font durer la conversation une semaine."] },
          { d: 33, pf: "X", h: "@pricewatch", tag: ["Price reveal", "Annonce du prix"], txt: ["The price announcement: a second spike, this one negative.", "L'annonce du prix : un second pic, négatif celui-là."] }
        ],
        posts: [
          ["X", "@leakhunter", 1, "That trailer. I've watched it ten times.", "Ce trailer. Je l'ai regardé dix fois."],
          ["TWITCH", "@gamerzone", 1, "Three hours of beta tonight, chat is going wild.", "Trois heures de bêta ce soir, le chat s'enflamme."],
          ["X", "@pricewatch", -1, "€80 for the standard edition? No thanks.", "80 € l'édition standard ? Non merci."],
          ["YOUTUBE", "@reviewgamer", 0, "Gameplay deep dive: the combat is great, the menus less so.", "Analyse du gameplay : les combats sont top, les menus moins."]
        ],
        insight: {
          head: ["The trailer spiked; the streams kept it alive.", "Le trailer a fait le pic ; les streams l'ont fait durer."],
          facts: [["Twitch streams drive 3× more posts per viewer than the trailer.", "Les streams Twitch génèrent 3× plus de posts par spectateur que le trailer."],
                  ["The price reveal brings a second spike, 64 % negative.", "L'annonce du prix provoque un second pic, négatif à 64 %."]],
          reco: ["Give early access to 20 mid-size streamers and announce the price with a bundle.", "Donner un accès anticipé à 20 streamers moyens et annoncer le prix avec un pack."]
        }
      },
      auto: {
        subject: ["Electric model launch", "Lancement d'un modèle électrique"],
        curve: { base: 620, launch: 21, spike: 1700, plateau: 520, bumps: [[27, 800, 3], [35, 760, 3]] },
        peaks: [
          { d: 22, pf: "LINKEDIN", h: "@auto.press", tag: ["Press reveal", "Révélation presse"], txt: ["The press reveal sets the tone: design first.", "La révélation presse donne le ton : le design d'abord."] },
          { d: 27, pf: "YOUTUBE", h: "@testdrive", tag: ["Test drives", "Essais"], txt: ["Test-drive videos: 71 % positive posts in their wake.", "Vidéos d'essai : 71 % de posts positifs dans leur sillage."] },
          { d: 35, pf: "X", h: "@ev_owners", tag: ["Range debate", "Débat autonomie"], txt: ["A thread on winter range restarts the conversation, colder.", "Un fil sur l'autonomie en hiver relance la conversation, en plus froid."] }
        ],
        posts: [
          ["LINKEDIN", "@auto.press", 0, "First look at the new EV: bold design, familiar platform.", "Premier regard sur la nouvelle électrique : design audacieux, plateforme connue."],
          ["YOUTUBE", "@testdrive", 1, "Test drive: the silence and the acceleration won me over.", "Essai : le silence et les accélérations m'ont conquis."],
          ["X", "@ev_owners", -1, "420 km claimed. In winter, on the motorway? Let's see.", "420 km annoncés. En hiver, sur autoroute ? On verra."],
          ["FACEBOOK", "@famille.martin", 1, "Booked a test drive for Saturday with the kids.", "Essai réservé samedi avec les enfants."]
        ],
        insight: {
          head: ["Test drives convinced; the range debate cooled things down.", "Les essais ont convaincu ; le débat sur l'autonomie a refroidi."],
          facts: [["Posts after test-drive videos are 71 % positive.", "Les posts qui suivent les vidéos d'essai sont positifs à 71 %."],
                  ["The range debate in week 6 halves purchase intent.", "Le débat sur l'autonomie en semaine 6 divise l'intention d'achat par deux."]],
          reco: ["Answer the range question in the launch content, with real winter tests.", "Répondre à la question de l'autonomie dans les contenus de lancement, avec de vrais tests en hiver."]
        }
      }
    },

    /* ------------------------------------------------------- 2. brand
       words: [EN, FR, weight, tone]; the common FILLER words are added */
    brand: {
      food: {
        subject: ["Food brand, last month", "Marque food, le mois dernier"], read: 8230,
        tones: [52, 21, 27],
        words: [["delivery", "livraison", 10, -1], ["late", "retard", 8, -1], ["parcel", "colis", 7, -1], ["product", "produit", 6, 1],
          ["tracking", "suivi", 5, -1], ["waiting", "attente", 5, -1], ["expensive", "cher", 4, -1], ["taste", "goût", 4, 1],
          ["customer service", "service client", 4, 1], ["pack", "format", 4, 0], ["refund", "remboursement", 3, -1], ["quick reply", "réponse rapide", 3, 1],
          ["cancelled", "annulé", 3, -1], ["courier", "livreur", 3, -1], ["recipe", "recette", 2, 1], ["damaged", "abîmé", 2, -1],
          ["out of stock", "rupture", 2, -1], ["fresh", "frais", 2, 1], ["kids", "enfants", 2, 1], ["breakfast", "petit-déj", 2, 1],
          ["smaller", "plus petit", 2, -1], ["supermarket", "supermarché", 2, 0], ["rain", "pluie", 1, -1], ["crunchy", "croustillant", 1, 1]],
        posts: [
          ["X", "@karim_d", -1, "Ordered on the 3rd, still nothing. Tracking says 'in preparation' for a week.", "Commandé le 3, toujours rien. Le suivi indique « en préparation » depuis une semaine."],
          ["FACEBOOK", "@martine.g", -1, "Parcel left in front of the building, in the rain. Great.", "Colis laissé devant l'immeuble, sous la pluie. Génial."],
          ["INSTAGRAM", "@lucie.m", 1, "The product is still great, that's why the delivery annoys me this much.", "Le produit est toujours top, c'est pour ça que la livraison m'agace autant."],
          ["X", "@alex_r", -1, "Two euros more in a year, same size. We noticed.", "Deux euros de plus en un an, même format. On a remarqué."],
          ["LINKEDIN", "@s.dubois", 1, "Customer service called me back within the hour. Rare enough to say it.", "Le service client m'a rappelé dans l'heure. Assez rare pour le dire."],
          ["FACEBOOK", "@nathalie.r", 0, "Still worth it, just less than before.", "Ça reste intéressant, juste moins qu'avant."]
        ],
        insight: {
          head: ["A delivery problem, not a reputation crisis.", "Un problème de livraison, pas une crise de réputation."],
          facts: [["62 % of negative posts are about late or damaged parcels.", "62 % des posts négatifs parlent de colis en retard ou abîmés."],
                  ["The product is praised in one post in three, even among complaints.", "Le produit est salué dans un post sur trois, même parmi les plaintes."]],
          reco: ["Change carrier and say so publicly. No crisis communication.", "Changer de transporteur et le dire publiquement. Pas de communication de crise."]
        }
      },
      luxury: {
        subject: ["Leather goods house", "Maison de maroquinerie"], read: 5140,
        tones: [38, 30, 32],
        words: [["boutique", "boutique", 9, 0], ["sales associate", "vendeur", 8, -1], ["price increase", "hausse de prix", 8, 0], ["waitlist", "liste d'attente", 7, -1],
          ["craftsmanship", "savoir-faire", 6, 1], ["iconic", "iconique", 6, 1], ["counterfeit", "contrefaçon", 5, -1], ["resale", "revente", 5, 0],
          ["leather", "cuir", 5, 1], ["rude", "désagréable", 5, -1], ["timeless", "intemporel", 4, 1], ["heritage", "héritage", 4, 1],
          ["overpriced", "trop cher", 4, -1], ["queue", "file d'attente", 4, -1], ["investment", "investissement", 3, 1], ["elegant", "élégant", 3, 1],
          ["logo", "logo", 3, 0], ["exclusive", "exclusif", 3, 1], ["dream", "rêve", 3, 1], ["ignored", "ignoré", 3, -1],
          ["packaging", "écrin", 2, 1], ["repair", "réparation", 2, -1], ["trainers", "baskets", 2, -1], ["mother", "mère", 1, 1]],
        posts: [
          ["INSTAGRAM", "@claire.paris", -1, "Waited 20 minutes in the boutique before anyone said hello.", "20 minutes dans la boutique avant qu'on me dise bonjour."],
          ["X", "@stylenotes", 0, "Another price increase. Still buying, still sighing.", "Encore une hausse de prix. J'achète quand même, en soupirant."],
          ["INSTAGRAM", "@vintage.bags", 1, "Twelve years old and the leather is still perfect. Craftsmanship.", "Douze ans et le cuir est toujours parfait. Le savoir-faire."],
          ["TIKTOK", "@lux.dupes", -1, "Spotted three counterfeits in one market. The logo is everywhere.", "Trois contrefaçons repérées sur un seul marché. Le logo est partout."],
          ["X", "@paul_r", -1, "The sales associate ignored us because we came in trainers.", "Le vendeur nous a ignorés parce qu'on était en baskets."],
          ["INSTAGRAM", "@heritage.lover", 1, "Iconic, timeless, worth every euro.", "Iconique, intemporel, chaque euro le vaut."]
        ],
        insight: {
          head: ["Price rises are forgiven; the boutique welcome is not.", "Les hausses de prix sont pardonnées ; l'accueil en boutique, non."],
          facts: [["38 % of negative posts are about the in-store welcome.", "38 % des posts négatifs portent sur l'accueil en boutique."],
                  ["70 % of posts about price increases are neutral.", "70 % des posts sur les hausses de prix sont neutres."]],
          reco: ["Train boutique teams before the next price increase, not after.", "Former les équipes boutique avant la prochaine hausse, pas après."]
        }
      },
      toys: {
        subject: ["Video game launch weekend", "Week-end de sortie d'un jeu vidéo"], read: 31200,
        tones: [47, 18, 35],
        words: [["servers", "serveurs", 10, -1], ["crash", "crash", 8, -1], ["bugs", "bugs", 8, -1], ["story", "scénario", 7, 1],
          ["graphics", "graphismes", 6, 1], ["patch", "patch", 6, 0], ["lag", "lag", 5, -1], ["masterpiece", "chef-d'œuvre", 5, 1],
          ["microtransactions", "microtransactions", 5, -1], ["multiplayer", "multijoueur", 4, 0], ["soundtrack", "bande-son", 4, 1], ["pay-to-win", "pay-to-win", 4, -1],
          ["fun", "fun", 4, 1], ["refund", "remboursement", 3, -1], ["kids", "enfants", 3, 1], ["Christmas", "Noël", 3, 1],
          ["update", "mise à jour", 3, 0], ["devs", "dévs", 3, 0], ["addictive", "addictif", 3, 1], ["login", "connexion", 3, -1],
          ["console", "console", 2, 0], ["controller", "manette", 2, 0], ["ending", "fin", 2, 1], ["crossplay", "crossplay", 1, 1]],
        posts: [
          ["X", "@gamer_jules", -1, "Servers down again. Launch weekend and I can't log in.", "Serveurs encore en panne. Week-end de sortie et je ne peux pas me connecter."],
          ["TWITCH", "@lena.plays", 1, "The story is a masterpiece. I cried at the ending.", "Le scénario est un chef-d'œuvre. J'ai pleuré à la fin."],
          ["X", "@f2p_hater", -1, "Pay-to-win microtransactions in a €70 game. Seriously?", "Des microtransactions pay-to-win dans un jeu à 70 €. Sérieusement ?"],
          ["YOUTUBE", "@techcheck", 0, "Patch 1.02 fixes the crash, not the lag.", "Le patch 1.02 corrige le crash, pas le lag."],
          ["FACEBOOK", "@papa.gamer", 1, "Bought it for my son for Christmas. We play together every evening.", "Acheté pour mon fils à Noël. On joue ensemble tous les soirs."],
          ["INSTAGRAM", "@artofgames", 1, "The graphics and the soundtrack are unreal.", "Les graphismes et la bande-son sont irréels."]
        ],
        insight: {
          head: ["Players love the game; they hate the servers.", "Les joueurs adorent le jeu ; ils détestent les serveurs."],
          facts: [["Server crashes drive 54 % of negative posts on launch weekend.", "Les crashs serveurs font 54 % des posts négatifs le week-end de sortie."],
                  ["'Masterpiece' and 'story' lead the positive posts.", "« Chef-d'œuvre » et « scénario » dominent les posts positifs."]],
          reco: ["Post daily on server fixes and give players an in-game apology gift.", "Communiquer chaque jour sur les correctifs et offrir un cadeau en jeu pour s'excuser."]
        }
      },
      auto: {
        subject: ["Car maker, first quarter", "Constructeur automobile, premier trimestre"], read: 12700,
        tones: [44, 24, 32],
        words: [["charging", "recharge", 10, -1], ["range", "autonomie", 9, -1], ["charging point", "borne", 7, -1], ["design", "design", 7, 1],
          ["silence", "silence", 6, 1], ["software", "logiciel", 5, -1], ["dealer", "concession", 5, 0], ["acceleration", "accélération", 5, 1],
          ["battery", "batterie", 5, 0], ["winter", "hiver", 4, -1], ["recall", "rappel", 4, -1], ["comfort", "confort", 4, 1],
          ["test drive", "essai", 4, 1], ["delivery delay", "délai de livraison", 4, -1], ["bonus", "bonus écologique", 3, 0], ["lease", "LOA", 3, 0],
          ["screen", "écran", 3, 0], ["warranty", "garantie", 3, 1], ["reliability", "fiabilité", 3, 1], ["motorway", "autoroute", 2, -1],
          ["boot", "coffre", 2, 1], ["app", "appli", 2, -1], ["heat pump", "pompe à chaleur", 1, 1], ["tyres", "pneus", 1, 0]],
        posts: [
          ["X", "@ev.daily", -1, "Forty minutes to find a working charging point. Again.", "Quarante minutes pour trouver une borne qui marche. Encore."],
          ["FACEBOOK", "@nathalie.drive", 1, "The silence in town is addictive. And the design turns heads.", "Le silence en ville, c'est addictif. Et le design fait tourner les têtes."],
          ["X", "@winter_range", -1, "Range drops to 280 km in winter on the motorway.", "L'autonomie tombe à 280 km en hiver sur autoroute."],
          ["LINKEDIN", "@fleet.manager", 0, "The software update fixed the app; the dealer still can't explain the lease.", "La mise à jour a réparé l'appli ; la concession n'explique toujours pas la LOA."],
          ["YOUTUBE", "@carreview", 1, "Comfort and acceleration: better than the German rivals.", "Confort et accélération : mieux que les rivales allemandes."],
          ["INSTAGRAM", "@thomas.ev", -1, "Delivery pushed back three months. Still waiting.", "Livraison repoussée de trois mois. J'attends toujours."]
        ],
        insight: {
          head: ["People like the car; they dislike charging it.", "Les gens aiment la voiture ; ils n'aiment pas la recharger."],
          facts: [["Charging accounts for 47 % of negative posts; the car itself, 12 %.", "La recharge fait 47 % des posts négatifs ; la voiture elle-même, 12 %."],
                  ["Design and silence lead the positive posts.", "Le design et le silence dominent les posts positifs."]],
          reco: ["Partner with a charging network and put it at the heart of the message.", "S'allier à un réseau de recharge et le mettre au cœur du discours."]
        }
      }
    },

    /* --------------------------------------------------- 3. audiences
       groups: five communities, largest first; aff, pen, opp out of 100 */
    audiences: {
      food: {
        subject: ["Food brand", "Marque food"], read: 15640,
        groups: [
          { name: ["Pragmatic parents", "Parents pragmatiques"], short: ["Parents", "Parents"], share: 41, aff: 78, pen: 61, opp: 52, color: "#EAA93D", note: ["Your base. Loyal, already buying: keep them, do not chase them.", "Votre socle. Fidèles, déjà clients : à garder, pas à conquérir."] },
          { name: ["Food creators' followers", "Abonnés des créateurs food"], short: ["Creators", "Créateurs"], share: 19, aff: 74, pen: 18, opp: 86, color: "#E2468D", note: ["Love the brand, barely buy it. The biggest opportunity on the map.", "Aiment la marque, l'achètent peu. La plus grosse opportunité de la carte."] },
          { name: ["Sport fans", "Sportifs"], short: ["Sport fans", "Sportifs"], share: 16, aff: 57, pen: 24, opp: 69, color: "#3CC2A6", note: ["Interested if the proof is there: labels, protein, tests.", "Intéressés si la preuve suit : étiquettes, protéines, tests."] },
          { name: ["Loyal seniors", "Seniors fidèles"], short: ["Seniors", "Seniors"], share: 10, aff: 82, pen: 70, opp: 24, color: "#4292F2", note: ["Already won. Do not change the recipe.", "Déjà acquis. Ne changez pas la recette."] },
          { name: ["Students", "Étudiants"], short: ["Students", "Étudiants"], share: 14, aff: 36, pen: 15, opp: 31, color: "#7B6CF2", note: ["The brief's target. Low affinity: expensive to convince.", "La cible du brief. Faible affinité : chers à convaincre."] }
        ],
        posts: [
          ["FACEBOOK", "@claire.maman", 1, "The only thing my kids eat without negotiating.", "La seule chose que mes enfants mangent sans négocier."],
          ["TIKTOK", "@chef.maud", 1, "Three recipes with it this week, my followers keep asking.", "Trois recettes avec cette semaine, mes abonnés en redemandent."],
          ["TIKTOK", "@student.budget", 0, "Student budget meal of the week.", "Repas budget étudiant de la semaine."],
          ["FACEBOOK", "@jacqueline.m", 1, "Been buying it for twenty years. Please don't change it.", "Je l'achète depuis vingt ans. Ne le changez pas, s'il vous plaît."]
        ],
        insight: {
          head: ["The opportunity is not in the brief.", "L'opportunité n'est pas dans le brief."],
          facts: [["Food creators' followers love the brand but barely buy it: opportunity 86 / 100.", "Les abonnés des créateurs food adorent la marque mais l'achètent peu : opportunité 86 / 100."],
                  ["Students, the brief's target, score 31.", "Les étudiants, cible du brief, font 31."]],
          reco: ["Shift the media plan toward food creators' audiences.", "Réorienter le plan média vers les audiences des créateurs food."]
        }
      },
      luxury: {
        subject: ["Leather goods house", "Maison de maroquinerie"], read: 9870,
        groups: [
          { name: ["Heritage collectors", "Collectionneurs historiques"], short: ["Collectors", "Collectionneurs"], share: 34, aff: 88, pen: 64, opp: 30, color: "#EAA93D", note: ["Already won. Keep them close with private events.", "Déjà acquis. Les garder proches avec des événements privés."] },
          { name: ["Aspirational Gen Z", "Gen Z aspirationnelle"], short: ["Gen Z", "Gen Z"], share: 24, aff: 71, pen: 9, opp: 84, color: "#E2468D", note: ["Dream about the brand, cannot afford it yet. The biggest opportunity.", "Rêvent de la marque, ne peuvent pas encore se l'offrir. La plus grosse opportunité."] },
          { name: ["International travellers", "Voyageurs internationaux"], short: ["Travellers", "Voyageurs"], share: 18, aff: 76, pen: 42, opp: 61, color: "#3CC2A6", note: ["Buy abroad and at airports. Reach them before the trip.", "Achètent à l'étranger et en aéroport. Les toucher avant le voyage."] },
          { name: ["Fashion insiders", "Initiés de la mode"], short: ["Insiders", "Initiés"], share: 12, aff: 69, pen: 55, opp: 44, color: "#4292F2", note: ["Small, but everyone reads them.", "Peu nombreux, mais tout le monde les lit."] },
          { name: ["Resellers", "Revendeurs"], short: ["Resellers", "Revendeurs"], share: 12, aff: 40, pen: 35, opp: 18, color: "#7B6CF2", note: ["Buy to resell. Not a community to court.", "Achètent pour revendre. Pas une communauté à séduire."] }
        ],
        posts: [
          ["TIKTOK", "@gen.z.style", 1, "Saving for my first piece. It's the dream bag.", "J'économise pour ma première pièce. C'est le sac de rêve."],
          ["INSTAGRAM", "@heritage.lover", 1, "My mother's bag, now mine. That's the brand.", "Le sac de ma mère, maintenant le mien. C'est ça, la marque."],
          ["X", "@resell.king", 0, "Bought at retail, sold for 40 % more the same week.", "Acheté en boutique, revendu 40 % plus cher la même semaine."],
          ["INSTAGRAM", "@travel.lux", 1, "Always buy it at the airport, better prices.", "Je l'achète toujours à l'aéroport, meilleurs prix."]
        ],
        insight: {
          head: ["Your next clients are 22, not 45.", "Vos prochains clients ont 22 ans, pas 45."],
          facts: [["Aspirational Gen Z: affinity 71, penetration 9, opportunity 84.", "Gen Z aspirationnelle : affinité 71, pénétration 9, opportunité 84."],
                  ["Heritage collectors are already won: opportunity 30.", "Les collectionneurs sont déjà acquis : opportunité 30."]],
          reco: ["Build an entry product and a creator programme for Gen Z.", "Créer un produit d'entrée et un programme créateurs pour la Gen Z."]
        }
      },
      toys: {
        subject: ["Video game publisher", "Éditeur de jeux vidéo"], read: 22400,
        groups: [
          { name: ["Parents buying gifts", "Parents qui offrent"], short: ["Parents", "Parents"], share: 38, aff: 62, pen: 48, opp: 55, color: "#EAA93D", note: ["Buy in November and December; ask about age and price.", "Achètent en novembre et décembre ; demandent l'âge et le prix."] },
          { name: ["Streamers' audiences", "Audiences des streamers"], short: ["Streams", "Streams"], share: 22, aff: 80, pen: 21, opp: 83, color: "#E2468D", note: ["Watch before they buy. The biggest opportunity.", "Regardent avant d'acheter. La plus grosse opportunité."] },
          { name: ["Core gamers", "Joueurs assidus"], short: ["Core", "Assidus"], share: 18, aff: 74, pen: 66, opp: 38, color: "#3CC2A6", note: ["Already playing. They decide the reputation.", "Déjà joueurs. Ce sont eux qui font la réputation."] },
          { name: ["Casual mobile players", "Joueurs mobiles"], short: ["Mobile", "Mobile"], share: 12, aff: 45, pen: 12, opp: 49, color: "#7B6CF2", note: ["Curious, but need a mobile or cheaper way in.", "Curieux, mais il leur faut une porte d'entrée mobile ou moins chère."] },
          { name: ["Retro collectors", "Collectionneurs rétro"], short: ["Retro", "Rétro"], share: 10, aff: 71, pen: 30, opp: 57, color: "#4292F2", note: ["Pay for collector's editions and figurines.", "Paient pour les éditions collector et les figurines."] }
        ],
        posts: [
          ["TWITCH", "@nova.stream", 1, "Chat voted, we're playing it all weekend.", "Le chat a voté, on y joue tout le week-end."],
          ["FACEBOOK", "@maman.cadeaux", 0, "Which age is it for? Asking for Christmas.", "C'est pour quel âge ? Je demande pour Noël."],
          ["X", "@retro.collector", 1, "The collector's edition figurine is gorgeous.", "La figurine de l'édition collector est magnifique."],
          ["TIKTOK", "@casual.gamer", 0, "Is there a mobile version? No console at home.", "Il y a une version mobile ? Pas de console à la maison."]
        ],
        insight: {
          head: ["Parents buy it; streamers' audiences want it.", "Les parents l'achètent ; les audiences des streamers le veulent."],
          facts: [["Streamers' audiences: affinity 80, penetration 21, opportunity 83.", "Audiences des streamers : affinité 80, pénétration 21, opportunité 83."],
                  ["Parents buying gifts make 38 % of the conversation, most of it in December.", "Les parents qui offrent font 38 % de la conversation, surtout en décembre."]],
          reco: ["Sponsor streams all year; speak to parents only in Q4.", "Sponsoriser des streams toute l'année ; parler aux parents seulement au T4."]
        }
      },
      auto: {
        subject: ["Car maker", "Constructeur automobile"], read: 13300,
        groups: [
          { name: ["Urban families", "Familles urbaines"], short: ["Families", "Familles"], share: 36, aff: 68, pen: 14, opp: 81, color: "#EAA93D", note: ["Need space, safety and low running costs. The next step.", "Veulent de la place, de la sécurité et un coût d'usage bas. La prochaine étape."] },
          { name: ["Tech early adopters", "Pionniers tech"], short: ["Early adopters", "Pionniers"], share: 20, aff: 84, pen: 58, opp: 34, color: "#E2468D", note: ["Already convinced. They are your ambassadors.", "Déjà convaincus. Ce sont vos ambassadeurs."] },
          { name: ["Company-car drivers", "Conducteurs de voitures de fonction"], short: ["Company cars", "Fonction"], share: 18, aff: 55, pen: 33, opp: 62, color: "#3CC2A6", note: ["Choose from a list. Win the fleet managers.", "Choisissent sur une liste. Convaincre les gestionnaires de flotte."] },
          { name: ["Rural commuters", "Navetteurs ruraux"], short: ["Rural", "Ruraux"], share: 14, aff: 38, pen: 9, opp: 40, color: "#4292F2", note: ["Held back by access to charging.", "Freinés par l'accès à la recharge."] },
          { name: ["Classic car fans", "Passionnés d'anciennes"], short: ["Classic fans", "Anciennes"], share: 12, aff: 22, pen: 4, opp: 12, color: "#7B6CF2", note: ["Not your audience. Do not chase them.", "Pas votre audience. Inutile de les chasser."] }
        ],
        posts: [
          ["FACEBOOK", "@famille.martin", 0, "Does a pram fit in the boot? Asking before the test drive.", "Une poussette rentre dans le coffre ? Je demande avant l'essai."],
          ["X", "@early.ev", 1, "Third EV for me. This one has the best software so far.", "Ma troisième électrique. Le meilleur logiciel jusqu'ici."],
          ["LINKEDIN", "@fleet.manager", 0, "Considering it for our company fleet next year.", "On l'envisage pour la flotte de l'entreprise l'an prochain."],
          ["X", "@rural.driver", -1, "Nearest fast charger is 50 km away. Not for me yet.", "La borne rapide la plus proche est à 50 km. Pas encore pour moi."]
        ],
        insight: {
          head: ["The early adopters are won; families are next.", "Les pionniers sont acquis ; les familles sont la suite."],
          facts: [["Urban families: affinity 68, penetration 14, opportunity 81.", "Familles urbaines : affinité 68, pénétration 14, opportunité 81."],
                  ["Tech early adopters are at 58 % penetration: little room left.", "Les pionniers tech sont à 58 % de pénétration : peu de marge."]],
          reco: ["Talk boot space, safety and running costs, not 0–100 times.", "Parler coffre, sécurité et coût d'usage, pas de 0 à 100."]
        }
      }
    },

    /* ------------------------------------------------------ 4. trends
       topics: [EN, FR, colour, shape, driven by, verdict]; see shape() */
    trends: {
      food: {
        subject: ["Food topics", "Sujets food"], read: 42300,
        topics: [
          ["High-protein snacks", "Snacks protéinés", "#EAA93D", ["log", 18, 75, 8, 2.2], ["Parents, then gyms", "Les parents, puis les salles de sport"], ["go", "Mainstream within a year. Build it now.", "Grand public d'ici un an. À lancer maintenant."]],
          ["Gut health", "Santé intestinale", "#3CC2A6", ["lin", 28, 2.4, 0], ["Food creators", "Créateurs food"], ["watch", "Steady climb. A safe angle for messaging.", "Montée régulière. Un angle sûr pour le discours."]],
          ["Upcycled food", "Alimentation upcyclée", "#7B6CF2", ["emg", 5, 2, 1.35, 1.5], ["Zero-waste communities", "Communautés zéro déchet"], ["go", "From nowhere to fourth. Pilot it before it is obvious.", "Parti de rien, 4e place. À tester avant que ce soit évident."]],
          ["Plant-based milk", "Laits végétaux", "#9DB33A", ["lin", 78, -0.3, 3], ["Everyone", "Tout le monde"], ["watch", "Big and flat. Compete on price, not novelty.", "Gros et stable. Se battre sur le prix, pas la nouveauté."]],
          ["Zero-sugar drinks", "Boissons zéro sucre", "#4292F2", ["lin", 60, -0.45, 2], ["Sport fans", "Sportifs"], ["watch", "Mature. No reason to lead with it.", "Mature. Aucune raison d'en faire un argument."]],
          ["Meal kits", "Box repas", "#E2468D", ["lin", 74, -2.9, 0], ["Busy couples", "Couples pressés"], ["stop", "Fading since the pandemic. Do not build here.", "En recul depuis le confinement. Ne pas investir ici."]],
          ["Fermented drinks", "Boissons fermentées", "#F2656F", ["lin", 12, 1.9, 2], ["Health optimisers", "Adeptes du bien-être"], ["watch", "Rising slowly. Watch for a creator to tip it.", "Monte lentement. Guetter le créateur qui la fera basculer."]],
          ["Mushroom coffee", "Café aux champignons", "#B77FD0", ["emg", 9, 1, 3.6, 1], ["Remote workers", "Télétravailleurs"], ["watch", "Brand new. Too early to bet, worth monitoring.", "Tout nouveau. Trop tôt pour parier, à surveiller."]]
        ],
        posts: [
          ["TIKTOK", "@nutri.jade", 1, "High-protein snack ranking, part 4.", "Classement des snacks protéinés, partie 4."],
          ["LINKEDIN", "@m.laurent", 1, "Bread made from brewers' grain: the startup raised again.", "Du pain fait avec des drêches de brasserie : la startup a encore levé des fonds."],
          ["X", "@kit.fatigue", -1, "Cancelled my meal kit. Cooking again.", "J'ai résilié ma box repas. Je recuisine."],
          ["INSTAGRAM", "@happy.gut", 1, "Kefir in everything this month.", "Du kéfir partout ce mois-ci."]
        ],
        insight: {
          head: ["Protein is the loudest; upcycled food is the one to watch.", "Le protéiné fait le plus de bruit ; l'upcyclé est à surveiller."],
          facts: [["High-protein snacks have led the conversation for nine months.", "Les snacks protéinés mènent la conversation depuis neuf mois."],
                  ["Upcycled food went from nowhere to fourth place in a year.", "L'upcyclé est passé de rien à la 4e place en un an."]],
          reco: ["Pilot an upcycled range in one market before competitors notice.", "Tester une gamme upcyclée sur un marché avant que la concurrence ne s'en aperçoive."]
        }
      },
      luxury: {
        subject: ["Luxury topics", "Sujets luxe"], read: 18600,
        topics: [
          ["Quiet luxury", "Luxe discret", "#EAA93D", ["log", 20, 68, 7, 2.5], ["Fashion insiders", "Initiés de la mode"], ["go", "The new norm. Make it the house's language.", "La nouvelle norme. En faire le langage de la maison."]],
          ["Certified pre-owned", "Seconde main certifiée", "#3CC2A6", ["lin", 14, 3.4, 1], ["Gen Z and collectors", "Gen Z et collectionneurs"], ["go", "The real shift. Own it before a reseller does.", "Le vrai basculement. À prendre avant un revendeur."]],
          ["Personalisation", "Personnalisation", "#4292F2", ["lin", 30, 1.2, 2], ["Gift buyers", "Acheteurs de cadeaux"], ["watch", "Steady. Good for loyalty, not for reach.", "Stable. Bon pour la fidélité, pas pour la portée."]],
          ["Bold logos", "Logos voyants", "#E2468D", ["lin", 72, -2.6, 2], ["Resellers", "Revendeurs"], ["stop", "Fading fast. Do not build a line on it.", "En chute rapide. Ne pas bâtir une ligne dessus."]],
          ["Vintage watches", "Montres vintage", "#9DB33A", ["lin", 26, 1.5, 3], ["Collectors", "Collectionneurs"], ["watch", "Solid niche. Worth a heritage story.", "Niche solide. Mérite un récit patrimonial."]],
          ["Lab-grown diamonds", "Diamants de synthèse", "#7B6CF2", ["emg", 4, 2, 1.5, 1.45], ["Young couples", "Jeunes couples"], ["go", "Fastest riser. Decide your position now.", "Plus forte hausse. Décider de sa position maintenant."]],
          ["Jewellery for men", "Bijoux pour hommes", "#F2656F", ["emg", 8, 1, 3.2, 1], ["Streetwear fans", "Fans de streetwear"], ["watch", "New and growing. Test with a capsule.", "Nouveau et en hausse. À tester avec une capsule."]],
          ["Rental", "Location", "#B77FD0", ["lin", 40, -1.1, 2], ["Event goers", "Adeptes d'événements"], ["watch", "Plateau. Not a priority.", "Plateau. Pas une priorité."]]
        ],
        posts: [
          ["INSTAGRAM", "@quiet.lux", 1, "No logo, perfect cut. That's the new luxury.", "Pas de logo, une coupe parfaite. C'est ça le nouveau luxe."],
          ["TIKTOK", "@preloved.finds", 1, "Found a certified pre-owned piece at half the price.", "Trouvé une pièce de seconde main certifiée à moitié prix."],
          ["X", "@watch.talk", 0, "Vintage watch prices are up again this quarter.", "Les prix des montres vintage remontent ce trimestre."],
          ["INSTAGRAM", "@labgrown.love", 1, "Lab-grown diamond, same sparkle, clear conscience.", "Diamant de synthèse, même éclat, conscience tranquille."]
        ],
        insight: {
          head: ["Quiet luxury leads; pre-owned is the real shift.", "Le luxe discret mène ; la seconde main est le vrai basculement."],
          facts: [["Certified pre-owned grew fivefold in 18 months.", "La seconde main certifiée a été multipliée par cinq en 18 mois."],
                  ["Bold logos lost two thirds of their share.", "Les logos voyants ont perdu deux tiers de leur part."]],
          reco: ["Launch a certified pre-owned programme before a reseller owns it.", "Lancer une seconde main certifiée avant qu'un revendeur ne s'en empare."]
        }
      },
      toys: {
        subject: ["Toys & games topics", "Sujets jouets & jeux"], read: 51900,
        topics: [
          ["Cozy games", "Cozy games", "#EAA93D", ["log", 15, 70, 8, 2.4], ["Streamers' audiences", "Audiences des streamers"], ["go", "The rising genre. Build the next title around it.", "Le genre qui monte. Bâtir le prochain titre autour."]],
          ["LEGO for adults", "LEGO pour adultes", "#3CC2A6", ["emg", 3, 5, 1.6, 1.4], ["Adult collectors", "Collectionneurs adultes"], ["go", "Adults buy for themselves now. Price for them.", "Les adultes achètent pour eux. Fixer les prix pour eux."]],
          ["Board games revival", "Retour du jeu de société", "#4292F2", ["lin", 20, 2.1, 2], ["Groups of friends", "Groupes d'amis"], ["watch", "Healthy growth. Good for co-op spin-offs.", "Croissance saine. Bon pour des déclinaisons coop."]],
          ["Retro consoles", "Consoles rétro", "#9DB33A", ["lin", 30, 1.5, 2], ["Retro collectors", "Collectionneurs rétro"], ["watch", "Nostalgia holds. Re-releases sell.", "La nostalgie tient. Les rééditions se vendent."]],
          ["Collectible figurines", "Figurines de collection", "#7B6CF2", ["lin", 40, 1.3, 3], ["Core gamers", "Joueurs assidus"], ["watch", "Steady. Bundle them with collector's editions.", "Stable. Les associer aux éditions collector."]],
          ["Battle royale", "Battle royale", "#E2468D", ["lin", 80, -2.8, 2], ["Teen players", "Joueurs ados"], ["stop", "Fatigue is real. Do not launch a new one.", "La lassitude est réelle. Ne pas en lancer un nouveau."]],
          ["Virtual reality", "Réalité virtuelle", "#F2656F", ["lin", 28, 0, 3], ["Tech early adopters", "Pionniers tech"], ["watch", "Flat for 18 months. Wait.", "Plat depuis 18 mois. Attendre."]],
          ["NFT games", "Jeux NFT", "#B77FD0", ["lin", 46, -2.6, 1], ["Crypto communities", "Communautés crypto"], ["stop", "Collapsed. Avoid the word entirely.", "Effondré. Éviter jusqu'au mot."]]
        ],
        posts: [
          ["TIKTOK", "@cozy.corner", 1, "Farming, crafting, no stress. Cozy games forever.", "Ferme, artisanat, zéro stress. Les cozy games pour toujours."],
          ["X", "@br.veteran", -1, "Battle royale fatigue is real. Same game, new skin.", "La lassitude du battle royale est réelle. Même jeu, nouveau skin."],
          ["INSTAGRAM", "@lego.adult", 1, "LEGO set for adults, 3,000 pieces, best weekend.", "Set LEGO pour adultes, 3 000 pièces, meilleur week-end."],
          ["FACEBOOK", "@boardgame.night", 1, "Board game night is back in our group.", "Les soirées jeux de société reviennent dans notre groupe."]
        ],
        insight: {
          head: ["Cozy games are rising; battle royale is fading.", "Les cozy games montent ; le battle royale décline."],
          facts: [["Cozy games overtook battle royale in month 9.", "Les cozy games ont dépassé le battle royale au 9e mois."],
                  ["LEGO for adults is the fastest riser of the period.", "Le LEGO pour adultes est la plus forte hausse de la période."]],
          reco: ["Market the next title on cozy and co-op, not competition.", "Axer le marketing du prochain titre sur le cozy et la coop, pas la compétition."]
        }
      },
      auto: {
        subject: ["Automotive topics", "Sujets auto"], read: 27400,
        topics: [
          ["Compact EVs", "Petites électriques", "#EAA93D", ["log", 18, 66, 8, 2.3], ["Urban families", "Familles urbaines"], ["go", "Where the market is going. Lead with a compact.", "Là où va le marché. Mener avec une citadine."]],
          ["Used EVs", "Électrique d'occasion", "#3CC2A6", ["emg", 4, 4, 1.1, 1.45], ["First-time EV buyers", "Primo-acheteurs"], ["go", "Grew tenfold. Build a certified used offer.", "Multiplié par dix. Créer une offre d'occasion certifiée."]],
          ["Hybrids", "Hybrides", "#9DB33A", ["lin", 70, -0.2, 3], ["Rural commuters", "Navetteurs ruraux"], ["watch", "Big and stable. The safe middle.", "Gros et stable. Le milieu sûr."]],
          ["SUVs", "SUV", "#4292F2", ["lin", 82, -1.4, 2], ["Families", "Familles"], ["watch", "Still big, slowly losing ground.", "Toujours gros, perd lentement du terrain."]],
          ["Chinese brands", "Marques chinoises", "#E2468D", ["lin", 12, 2.6, 2], ["Price-sensitive buyers", "Acheteurs sensibles au prix"], ["watch", "Rising competition. Answer on value.", "Concurrence en hausse. Répondre sur la valeur."]],
          ["Car subscription", "Abonnement auto", "#7B6CF2", ["lin", 18, 1.2, 2], ["Young city dwellers", "Jeunes urbains"], ["watch", "Slow but steady. Test in two cities.", "Lent mais régulier. Tester dans deux villes."]],
          ["Driver assistance", "Aides à la conduite", "#F2656F", ["lin", 35, 0.9, 2], ["Tech early adopters", "Pionniers tech"], ["watch", "Expected now, no longer a difference.", "Attendu désormais, plus une différence."]],
          ["Hydrogen", "Hydrogène", "#B77FD0", ["lin", 30, -1.4, 1], ["Engineers", "Ingénieurs"], ["stop", "Stations closing. Do not bet on it.", "Les stations ferment. Ne pas miser dessus."]]
        ],
        posts: [
          ["X", "@city.ev", 1, "A small EV for town is all we need.", "Une petite électrique pour la ville, c'est tout ce qu'il nous faut."],
          ["FACEBOOK", "@used.ev.fr", 1, "Bought a three-year-old EV, battery at 94 %.", "Acheté une électrique de trois ans, batterie à 94 %."],
          ["LINKEDIN", "@mobility.analyst", 0, "Chinese brands took 8 % of EV registrations this year.", "Les marques chinoises font 8 % des immatriculations électriques cette année."],
          ["X", "@h2.skeptic", -1, "Hydrogen stations keep closing. That ship has sailed.", "Les stations hydrogène ferment les unes après les autres. C'est fini."]
        ],
        insight: {
          head: ["Compact and used EVs are where the market is going.", "Petites électriques et occasion : c'est là que va le marché."],
          facts: [["Compact EVs took the lead in month 11.", "Les petites électriques ont pris la tête au 11e mois."],
                  ["Used EVs grew more than tenfold, from almost nothing.", "L'électrique d'occasion a été multiplié par plus de dix, en partant de presque rien."]],
          reco: ["Build a certified used-EV offer and a compact-model message.", "Créer une offre d'électrique d'occasion certifiée et un discours citadine."]
        }
      }
    }
  };

  /* the curves behind the race: logistic, linear with a wobble, emerging */
  function shape(s) {
    if (s[0] === "log") return function (m) { return s[1] + s[2] / (1 + Math.exp(-(m - s[3]) / s[4])); };
    if (s[0] === "emg") return function (m) { return m < s[1] ? s[2] + m * 0.15 : s[2] + s[1] * 0.15 + Math.pow(m - s[1], s[4]) * s[3]; };
    return function (m) { return s[1] + s[2] * m + s[3] * Math.sin(m * 1.1); };
  }

  /* words everybody uses, whatever the sector: they make the mass */
  var FILLER = [
    ["order", "commande", 2, 0], ["website", "site", 2, 0], ["app", "appli", 2, 0], ["review", "avis", 2, 0], ["recommend", "recommande", 2, 1],
    ["thanks", "merci", 2, 1], ["again", "encore", 2, -1], ["never", "jamais", 2, -1], ["week", "semaine", 1, 0], ["email", "mail", 1, 0],
    ["weekend", "week-end", 1, 0], ["brand", "marque", 2, 0], ["since", "depuis", 1, 0], ["family", "famille", 1, 1], ["friends", "amis", 1, 1],
    ["today", "aujourd'hui", 1, 0], ["finally", "enfin", 1, 1], ["honestly", "franchement", 1, 0], ["worth it", "ça vaut le coup", 2, 1],
    ["disappointed", "déçu", 2, -1], ["angry", "énervé", 1, -1], ["love it", "j'adore", 2, 1], ["great", "top", 2, 1], ["slow", "lent", 1, -1],
    ["fast", "rapide", 1, 1], ["new", "nouveau", 1, 0], ["video", "vidéo", 1, 0], ["stories", "stories", 1, 0], ["comment", "commentaire", 1, 0],
    ["answer", "réponse", 1, 1], ["team", "équipe", 1, 1], ["help", "aide", 1, 1], ["wait", "attendre", 1, -1], ["month", "mois", 1, 0],
    ["quality", "qualité", 2, 1], ["price", "prix", 3, -1], ["complaint", "réclamation", 1, -1], ["gift", "cadeau", 1, 1], ["favourite", "préféré", 1, 1],
    ["problem", "problème", 2, -1], ["perfect", "parfait", 1, 1], ["tweet", "tweet", 1, 0], ["support", "support", 1, 0], ["deal", "offre", 1, 0]
  ];

  /* ============================================================ frame */
  var current = null, sector = 0, timers = [], cleanup = [];
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function every(fn, ms) { var id = setInterval(fn, ms); timers.push(id); return id; }
  function stopAll() {
    timers.forEach(function (id) { clearTimeout(id); clearInterval(id); });
    timers = [];
    cleanup.forEach(function (fn) { fn(); });
    cleanup = [];
  }
  function data() { return CASES[current][SECTORS[sector].key]; }

  function frame(title, hint, body) {
    var d = data();
    return '<div class="uv">' +
        '<div class="uv__head">' +
          '<span class="uv__live"><i></i>' + t("Live", "En direct") + "</span>" +
          '<p class="uv__title">' + title + "</p>" +
          '<span class="uv__tag">' + t("Illustrative data", "Données illustratives") + "</span>" +
          '<button class="uv__close" type="button" id="uv-close" aria-label="' + t("Close", "Fermer") + '"><span aria-hidden="true">×</span></button>' +
        "</div>" +
        '<div class="uv__case">' +
          '<p class="uv__sector"><b>' + esc(L(SECTORS[sector].name)) + "</b><span>" + esc(L(d.subject)) + "</span></p>" +
          '<button class="uv__next" type="button" id="uv-next">' + t("Another case", "Voir un autre cas") + ' <span aria-hidden="true">↻</span></button>' +
        "</div>" +
        '<p class="uv__hint"><span aria-hidden="true">✦</span>' + hint + "</p>" +
        '<div class="uv__body">' + body + "</div>" +
      "</div>" +
      '<aside class="lf__read">' +
        '<p class="lf__k">' + t("Posts read", "Posts lus") + "</p>" +
        '<p class="lf__count" id="uv-count">0</p>' +
        '<p class="lf__k">' + t("Latest posts", "Derniers posts") + "</p>" +
        '<div class="mps" id="uv-posts"></div>' +
        '<div class="lf__answer" id="uv-answer" aria-live="polite"><p class="lf__reading">' + t("Reading", "Lecture en cours") +
          '<span class="lf__dots"><i></i><i></i><i></i></span></p></div>' +
        '<div class="lf__get" id="uv-get"></div>' +
        '<a class="lf__book" href="#book">' + t("Or talk to a consultant", "Ou parler à un consultant") + ' <span aria-hidden="true">→</span></a>' +
      "</aside>";
  }

  function postHTML(p) {
    return '<div class="mp">' +
      '<p class="mp__meta">' + ((window.LicterIcons || {})[p[0]] || "") + "<b>" + esc(p[1]) + "</b><span>" + PLATFORM_NAMES[p[0]] + "</span></p>" +
      '<p class="mp__text">' + esc(fr() ? p[4] : p[3]) + "</p></div>";
  }

  /* The side panel: two posts rotate; the count and our read follow the
     visual. A visual calls progress(k), k from 0 to 1; at 1 our read lands. */
  var gen = 0, answered = false, total = 0;
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, sentCases = {};

  /* The offer once the read has landed: the full case of the sector on
     screen, by email. The lead arrives with its sector and its question. */
  function renderGet() {
    var el = document.getElementById("uv-get");
    if (!el) return;
    var key = current + ":" + SECTORS[sector].key, name = L(SECTORS[sector].name);
    if (sentCases[key]) {
      el.innerHTML = '<p class="lf__sent">' + t("Sent. The full " + name.toLowerCase() + " case arrives by email.", "C'est envoyé. Le cas complet " + name.toLowerCase() + " arrive par e-mail.") + "</p>";
      return;
    }
    el.innerHTML =
      '<form class="lf__form" novalidate>' +
        '<label class="lf__k" for="uv-email">' + t("Get the full case", "Recevez le cas complet") + " · " + esc(name) + "</label>" +
        '<p class="lf__sub">' + t("Method, figures and recommendation, as a PDF.", "Méthode, chiffres et recommandation, en PDF.") + "</p>" +
        '<div class="lf__row"><input class="fld__input" id="uv-email" type="email" autocomplete="email" placeholder="' + t("name@company.com", "nom@entreprise.com") + '" required />' +
        '<button class="btn btn--primary" type="submit">' + t("Send", "Recevoir") + "</button></div>" +
        '<p class="fld__error" hidden>' + t("Enter a work email, like name@company.com.", "Saisissez un e-mail professionnel, par exemple nom@entreprise.com.") + "</p>" +
      "</form>";
    el.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var field = el.querySelector("#uv-email"), err = el.querySelector(".fld__error"), ok = EMAIL.test(field.value.trim());
      field.setAttribute("aria-invalid", ok ? "false" : "true");
      err.hidden = ok;
      if (!ok) { field.focus(); return; }
      /* MOCK: send { email, topic: current, sector: SECTORS[sector].key } to the CRM */
      sentCases[key] = true;
      renderGet();
      var msg = el.querySelector(".lf__sent");
      if (msg) { msg.setAttribute("tabindex", "-1"); msg.focus({ preventScroll: true }); }
    });
  }
  function runSide() {
    var posts = data().posts, postsEl = document.getElementById("uv-posts"), i = 0;
    function show() {
      postsEl.innerHTML = postHTML(posts[i % posts.length]) + postHTML(posts[(i + 1) % posts.length]);
      postsEl.classList.remove("is-in"); void postsEl.offsetWidth; postsEl.classList.add("is-in");
      i += 1;
    }
    show();
    every(show, 3600);
  }
  function progress(k) {
    var countEl = document.getElementById("uv-count"), answerEl = document.getElementById("uv-answer");
    if (!countEl) return;
    k = Math.max(0, Math.min(1, k));
    countEl.textContent = num(Math.round(total * k));
    if (k >= 1 && !answered) {
      answered = true;
      var ins = data().insight;
      answerEl.classList.add("is-in");
      answerEl.innerHTML =
        '<p class="lf__k">' + t("Our read", "Notre lecture") + "</p>" +
        '<p class="ins__head">' + esc(L(ins.head)) + "</p>" +
        '<ul class="ins__facts">' + ins.facts.map(function (f) { return "<li>" + esc(L(f)) + "</li>"; }).join("") + "</ul>" +
        '<p class="ins__reco"><span>' + t("We recommend", "Notre recommandation") + "</span>" + esc(L(ins.reco)) + "</p>";
      renderGet();
      var get = document.getElementById("uv-get");
      if (get) { get.classList.remove("is-in"); void get.offsetWidth; get.classList.add("is-in"); }
    }
  }
  /* runs fn(k) from 0 to 1 over ms, frame by frame, until the case changes */
  function tween(ms, fn, done) {
    var my = gen, start = performance.now();
    if (reduced.matches) { fn(1); if (done) done(); return; }
    (function step(now) {
      if (my !== gen) return;
      var k = Math.min(1, (now - start) / ms);
      fn(k);
      if (k < 1) requestAnimationFrame(step); else if (done) done();
    })(start);
  }
  function autoProgress(ms) { tween(ms || 3200, function (k) { progress(1 - Math.pow(1 - k, 3)); }); }

  /* ================================================= 1. communication */
  function communication() {
    var d = data(), c = d.curve, D = 42, V = [], CAT = [];
    for (var i = 0; i < D; i++) {
      var v = c.base * (1 + 0.07 * Math.sin(i * 1.3) + 0.04 * Math.cos(i * 0.7));
      if (i >= c.launch) {
        v += c.spike * Math.exp(-Math.pow(i - c.launch - 1.5, 2) / 5) + c.plateau * (1 - Math.exp(-(i - c.launch) / 5));
        c.bumps.forEach(function (b) { v += b[1] * Math.exp(-Math.pow(i - b[0], 2) / b[2]); });
      }
      V.push(Math.round(v));
      CAT.push(Math.round(c.base * (1.16 + 0.05 * Math.sin(i * 0.5))));
    }
    var TOP = Math.ceil(Math.max.apply(null, V) * 1.12 / 1000) * 1000;
    var CUM = [], acc = 0; V.forEach(function (x) { acc += x; CUM.push(acc); });
    total = acc;
    var W = 640, H = 290, P = { l: 44, r: 16, t: 26, b: 30 };
    function X(x) { return P.l + x * (W - P.l - P.r) / (D - 1); }
    function Y(x) { return P.t + (1 - x / TOP) * (H - P.t - P.b); }
    function line(a) { return a.map(function (x, k) { return (k ? "L" : "M") + X(k).toFixed(1) + " " + Y(x).toFixed(1); }).join(" "); }
    function at(f) { var k = Math.max(0, Math.min(D - 2, Math.floor(f))); return V[k] + (V[k + 1] - V[k]) * (f - k); }
    var area = line(V) + " L" + X(D - 1) + " " + (H - P.b) + " L" + X(0) + " " + (H - P.b) + " Z";
    var grid = [0, .25, .5, .75, 1].map(function (q) {
      var val = TOP * q, lab = val ? (val / 1000).toLocaleString(fr() ? "fr-FR" : "en-GB", { maximumFractionDigits: 1 }) + "k" : "0";
      return '<line class="g" x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + Y(val) + '" y2="' + Y(val) + '"/>' +
        '<text class="ax" x="' + (P.l - 8) + '" y="' + (Y(val) + 3.5) + '" text-anchor="end">' + lab + "</text>";
    }).join("");
    var weeks = [0, 7, 14, 21, 28, 35].map(function (x, k) {
      return '<text class="ax" x="' + X(x + 3) + '" y="' + (H - 8) + '" text-anchor="middle">' + t("Week ", "Sem. ") + (k + 1) + "</text>";
    }).join("");
    /* each pin sits on the top of its wave, and carries its own label, placed
       where it covers nothing: above the pin, else right, left, below */
    var PK = d.peaks.map(function (p) {
      var best = p.d;
      for (var j = p.d - 1; j <= p.d + 1; j++) if (j > c.launch - 1 && j < D && V[j] > V[best]) best = j;
      return { d: best, x: X(best), y: Y(V[best]) };
    });
    var boxes = [[X(c.launch - 0.5) - 42, 0, 84, P.t + 2]];
    PK.forEach(function (q) { boxes.push([q.x - 8, q.y - 8, 16, 16]); });
    function overlap(bx, by, w, h) {
      return boxes.reduce(function (s, b) {
        var ox = Math.min(bx + w + 4, b[0] + b[2]) - Math.max(bx - 4, b[0]), oy = Math.min(by + h + 3, b[1] + b[3]) - Math.max(by - 3, b[1]);
        return s + (ox > 0 && oy > 0 ? ox * oy : 0);
      }, 0);
    }
    var pins = d.peaks.map(function (p, k) {
      var label = L(p.tag), w = Math.round(label.length * 6.4 + 22), h = 20, px = PK[k].x, py = PK[k].y;
      var cands = [[-w / 2, -h - 12], [14, -h / 2], [-14 - w, -h / 2], [-w / 2, 12], [14, -h - 16], [-14 - w, -h - 16], [-w / 2, -h - 34], [-w / 2, 34]];
      var pick = null, least = Infinity;
      cands.forEach(function (cd) {
        var bx = px + cd[0], by = py + cd[1];
        if (bx < P.l || bx + w > W - P.r || by < 2 || by + h > H - P.b) return;
        var o = overlap(bx, by, w, h);
        if (o < least - 0.5) { least = o; pick = cd; }
      });
      pick = pick || cands[0];
      boxes.push([px + pick[0], py + pick[1], w, h]);
      return '<g class="pin is-hidden" tabindex="0" role="button" data-i="' + k + '" transform="translate(' + px.toFixed(1) + "," + py.toFixed(1) + ')" aria-label="' + esc(label + ". " + L(p.txt)) + '">' +
        '<g class="pin__tag" transform="translate(' + pick[0].toFixed(1) + "," + pick[1].toFixed(1) + ')"><rect width="' + w + '" height="' + h + '" rx="10"/>' +
        '<text x="' + (w / 2) + '" y="14" text-anchor="middle">' + esc(label) + "</text></g>" +
        '<circle class="pin__halo" r="12"/><circle class="pin__dot" r="5.5"/></g>';
    }).join("");
    var svg =
      '<svg class="uv-svg is-locked" id="c-svg" viewBox="0 0 ' + W + " " + H + '" role="group" aria-label="' + t("Daily volume of posts over six weeks", "Volume quotidien de posts sur six semaines") + '">' +
        '<defs><linearGradient id="c-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAA93D" stop-opacity=".38"/><stop offset="1" stop-color="#EAA93D" stop-opacity="0"/></linearGradient>' +
          '<clipPath id="c-clip"><rect id="c-reveal" x="0" y="0" width="' + P.l + '" height="' + H + '"/></clipPath></defs>' +
        grid + weeks +
        '<rect class="after" id="c-after" y="' + P.t + '" height="' + (H - P.t - P.b) + '"/>' +
        '<path class="cat" d="' + line(CAT) + '"/>' +
        '<text class="cat__t" x="' + (W - P.r) + '" y="' + (Y(CAT[D - 1]) + 16) + '" text-anchor="end">' + t("Category average", "Moyenne de la catégorie") + "</text>" +
        '<g clip-path="url(#c-clip)"><path class="area" d="' + area + '"/><path class="brand" d="' + line(V) + '"/></g>' +
        '<circle class="head" id="c-head" r="5"/>' +
        '<g id="c-launch" class="launch"><line y1="' + (P.t - 4) + '" y2="' + (H - P.b) + '"/>' +
          '<rect x="-38" y="' + (P.t - 24) + '" width="76" height="20" rx="10"/>' +
          '<text y="' + (P.t - 10) + '" text-anchor="middle">' + t("Launch", "Lancement") + "</text>" +
          '<circle class="launch__grip" id="c-grip" r="8"/></g>' +
        pins +
      "</svg>";
    var body =
      '<div class="kchips">' +
        '<div class="kchip"><span>' + t("Before", "Avant") + '</span><b id="c-b">–</b></div>' +
        '<div class="kchip"><span>' + t("After", "Après") + '</span><b id="c-a">–</b></div>' +
        '<div class="kchip kchip--hi"><span>' + t("Uplift", "Gain") + '</span><b id="c-u">–</b></div>' +
        '<span class="kchip__day" id="c-day"></span>' +
      "</div>" +
      '<div class="uv-chart" id="c-chart">' + svg + '<div class="uv-tip" id="c-tip" hidden></div></div>' +
      '<input class="visually-hidden" type="range" id="c-range" min="4" max="37" value="' + c.launch + '" disabled aria-label="' + t("Campaign launch day", "Jour du lancement") + '" />';
    stage.innerHTML = frame(t("Posts per day, six weeks", "Posts par jour, six semaines"),
      '<span id="c-hint">' + t("Reading the six weeks…", "Lecture des six semaines…") + "</span>", body);

    var svgEl = document.getElementById("c-svg"), g = document.getElementById("c-launch"), grip = document.getElementById("c-grip");
    var after = document.getElementById("c-after"), range = document.getElementById("c-range"), tip = document.getElementById("c-tip");
    var chart = document.getElementById("c-chart"), reveal = document.getElementById("c-reveal"), head = document.getElementById("c-head");
    var launch = c.launch, shown = 0, ready = false;
    function avg(a) { return a.reduce(function (s, x) { return s + x; }, 0) / (a.length || 1); }
    function update() {
      var x = (X(launch - 1) + X(launch)) / 2;
      g.setAttribute("transform", "translate(" + x.toFixed(1) + ",0)");
      /* the grip rides the curve, wherever the line is dragged */
      grip.setAttribute("cy", Y(at(launch - 0.5)).toFixed(1));
      after.setAttribute("x", x.toFixed(1)); after.setAttribute("width", Math.max(0, X(Math.max(launch, shown)) - x).toFixed(1));
      var b = V.slice(Math.max(0, launch - 14), Math.min(launch, shown + 1));
      var a = shown >= launch ? V.slice(launch, Math.min(launch + 14, shown + 1)) : [];
      document.getElementById("c-b").textContent = b.length ? num(avg(b)) + t("/day", "/jour") : "–";
      document.getElementById("c-a").textContent = a.length ? num(avg(a)) + t("/day", "/jour") : "–";
      var up = a.length && b.length ? (avg(a) / avg(b) - 1) * 100 : null;
      document.getElementById("c-u").textContent = up === null ? "–" : (up >= 0 ? "+" : "") + Math.round(up) + " %";
      range.value = launch;
    }
    /* the curve draws itself day by day; the chips and the count follow it */
    tween(4200, function (k) {
      var f = k * (D - 1);
      shown = Math.floor(f);
      var x = X(f);
      reveal.setAttribute("width", x.toFixed(1));
      head.setAttribute("cx", x.toFixed(1)); head.setAttribute("cy", Y(at(f)).toFixed(1));
      Array.prototype.forEach.call(chart.querySelectorAll(".pin"), function (el) {
        if (PK[+el.dataset.i].d <= f) el.classList.remove("is-hidden");
      });
      if (f >= launch - 0.5) g.classList.add("is-in");
      document.getElementById("c-day").textContent = t("Day ", "Jour ") + (shown + 1) + " / " + D;
      update();
      progress(CUM[shown] / CUM[D - 1]);
    }, function () {
      shown = D - 1; ready = true; g.classList.add("is-in", "is-done"); update(); progress(1);
      Array.prototype.forEach.call(chart.querySelectorAll(".pin"), function (el) { el.classList.remove("is-hidden"); });
      svgEl.classList.remove("is-locked"); range.disabled = false;
      head.style.opacity = "0";
      document.getElementById("c-day").textContent = "";
      document.getElementById("c-hint").textContent = t("Now drag the launch line. Hover the peaks.", "Déplacez maintenant la ligne de lancement. Survolez les pics.");
    });

    function fromPointer(e) {
      var r = svgEl.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * W;
      launch = Math.max(4, Math.min(37, Math.round((x - P.l) / ((W - P.l - P.r) / (D - 1)) + 0.5)));
      update();
    }
    var dragging = false;
    svgEl.addEventListener("pointerdown", function (e) {
      if (!ready || e.target.closest(".pin")) return;
      dragging = true; svgEl.setPointerCapture(e.pointerId); fromPointer(e);
    });
    svgEl.addEventListener("pointermove", function (e) { if (dragging) fromPointer(e); });
    svgEl.addEventListener("pointerup", function () { dragging = false; });
    range.addEventListener("input", function () { launch = +range.value; update(); });

    function showTip(k) {
      var p = d.peaks[k], q = PK[k];
      tip.innerHTML = '<p class="uv-tip__meta">' + ((window.LicterIcons || {})[p.pf] || "") + "<b>" + p.h + "</b> · " + PLATFORM_NAMES[p.pf] + "</p><p>" + esc(L(p.txt)) + "</p>";
      tip.style.left = (q.x / W * 100) + "%";
      tip.style.top = (q.y / H * 100) + "%";
      tip.hidden = false;
    }
    Array.prototype.forEach.call(chart.querySelectorAll(".pin"), function (el) {
      var k = +el.dataset.i;
      el.addEventListener("mouseenter", function () { showTip(k); });
      el.addEventListener("focus", function () { showTip(k); });
      el.addEventListener("click", function () { showTip(k); });
      el.addEventListener("mouseleave", function () { tip.hidden = true; });
      el.addEventListener("blur", function () { tip.hidden = true; });
    });
    update();
  }

  /* ======================================================== 2. brand */
  var TONE = { "-1": "neg", "0": "neu", "1": "pos" };

  function brand() {
    var d = data(), on = { neg: true, neu: true, pos: true };
    /* the sector's words first, then the common ones it does not already have */
    var seenW = {};
    var WORDS = d.words.concat(FILLER).filter(function (w) {
      var k = w[1].toLowerCase();
      if (seenW[k]) return false;
      seenW[k] = 1; return true;
    });
    var body =
      '<div class="tones" role="group" aria-label="' + t("Tone", "Tonalité") + '">' +
        [["neg", t("Negative", "Négatif")], ["neu", t("Neutral", "Neutre")], ["pos", t("Positive", "Positif")]].map(function (x) {
          return '<button class="tone tone--' + x[0] + ' is-on" type="button" data-t="' + x[0] + '" aria-pressed="true"><i></i>' + x[1] +
            ' <b class="tone__n" data-n="' + x[0] + '">0</b></button>';
        }).join("") +
      "</div>" +
      '<div class="cloud" id="b-cloud"></div>' +
      '<div class="quotes" id="b-q"><p class="quotes__hint">' + t("Words appear as we read. Click one to see what people actually wrote.", "Les mots apparaissent à mesure que nous lisons. Cliquez-en un pour lire ce que les gens ont vraiment écrit.") + "</p></div>";
    stage.innerHTML = frame(t("What people say about the brand", "Ce que les gens disent de la marque"),
      t("Filter by tone. Click a word.", "Filtrez par ton. Cliquez un mot."), body);

    var cloud = document.getElementById("b-cloud"), q = document.getElementById("b-q");
    var font = getComputedStyle(document.body).fontFamily;
    var ctx = document.createElement("canvas").getContext("2d");
    var revealed = 0;
    /* reading order: the four loudest first, then the rest shuffled */
    var rest = WORDS.map(function (_, i) { return i; }).slice(4);
    for (var k = rest.length - 1; k > 0; k--) { var j = (k * 7 + 3) % (k + 1), tmp = rest[k]; rest[k] = rest[j]; rest[j] = tmp; }
    var order = [0, 1, 2, 3].concat(rest), rankOf = [];
    order.forEach(function (w, r) { rankOf[w] = r; });

    function layout() {
      var Wc = cloud.clientWidth || 600, Hc = cloud.clientHeight || 300, cx = Wc / 2, cy = Hc / 2;
      var scale = Math.max(.72, Math.min(1, Wc / 640));
      var placed = [], out = "";
      WORDS.forEach(function (w, i) {
        var label = fr() ? w[1] : w[0], size = Math.round((9 + w[2] * 3.6) * scale);
        ctx.font = "700 " + size + "px " + font;
        var bw = ctx.measureText(label).width + 6, bh = size * 1.02;
        for (var s = 0; s < 4000; s += 1) {
          var a = s * 0.21, r = 1.35 * a;
          var x = cx + r * Math.cos(a) * 1.7 - bw / 2, y = cy + r * Math.sin(a) - bh / 2;
          if (x < 2 || y < 2 || x + bw > Wc - 2 || y + bh > Hc - 2) continue;
          var hit = placed.some(function (p) { return x < p[0] + p[2] + 1 && x + bw + 1 > p[0] && y < p[1] + p[3] && y + bh > p[1]; });
          if (hit) continue;
          placed.push([x, y, bw, bh]);
          out += '<button class="word word--' + TONE[w[3]] + (rankOf[i] < revealed ? " is-shown" : "") + '" type="button" data-i="' + i +
            '" style="left:' + x.toFixed(0) + "px;top:" + y.toFixed(0) + "px;font-size:" + size + 'px">' + esc(label) + "</button>";
          break;
        }
      });
      cloud.innerHTML = out;
      filter();
    }
    function filter() {
      Array.prototype.forEach.call(cloud.querySelectorAll(".word"), function (el) {
        var tone = TONE[WORDS[+el.dataset.i][3]];
        el.classList.toggle("is-off", !on[tone]);
        el.tabIndex = on[tone] && el.classList.contains("is-shown") ? 0 : -1;
      });
    }
    /* the three tones share the posts read: they always add up to the count */
    function counts(k) {
      var read = Math.round(total * k), neg = Math.round(read * d.tones[0] / 100), neu = Math.round(read * d.tones[1] / 100);
      var n = { neg: neg, neu: neu, pos: read - neg - neu };
      Array.prototype.forEach.call(stage.querySelectorAll(".tone__n"), function (b) { b.textContent = num(n[b.dataset.n]); });
    }
    /* posts that use a word: the loudest word is in about a quarter of them */
    function mentions(w) { return Math.round(total * 0.026 * w[2]); }
    layout();
    tween(5200, function (k) {
      var target = Math.round(k * WORDS.length);
      while (revealed < target) {
        var el = cloud.querySelector('.word[data-i="' + order[revealed] + '"]');
        if (el) el.classList.add("is-shown");
        revealed++;
      }
      filter(); counts(k);
      progress(k);
    });

    function quotesFor(w) {
      var posts = d.posts, key = w[0].split(" ")[0].toLowerCase();
      var hits = posts.filter(function (p) { return p[3].toLowerCase().indexOf(key) >= 0; });
      if (hits.length < 2) hits = hits.concat(posts.filter(function (p) { return p[2] === w[3] && hits.indexOf(p) < 0; }));
      if (hits.length < 2) hits = hits.concat(posts.filter(function (p) { return hits.indexOf(p) < 0; }));
      return hits.slice(0, 2);
    }
    cloud.addEventListener("click", function (e) {
      var el = e.target.closest(".word"); if (!el) return;
      Array.prototype.forEach.call(cloud.querySelectorAll(".word"), function (x) { x.classList.toggle("is-on", x === el); });
      var w = WORDS[+el.dataset.i];
      q.innerHTML = '<p class="quotes__head"><b class="word--' + TONE[w[3]] + '">' + esc(fr() ? w[1] : w[0]) + "</b> · " +
        num(mentions(w)) + " " + t("posts", "posts") + "</p>" +
        quotesFor(w).map(function (p) {
          return '<blockquote class="quote"><p>' + esc(fr() ? p[4] : p[3]) + "</p><cite>" + esc(p[1]) + " · " + PLATFORM_NAMES[p[0]] + "</cite></blockquote>";
        }).join("");
    });
    stage.querySelector(".tones").addEventListener("click", function (e) {
      var b = e.target.closest(".tone"); if (!b) return;
      on[b.dataset.t] = !on[b.dataset.t];
      b.classList.toggle("is-on", on[b.dataset.t]); b.setAttribute("aria-pressed", on[b.dataset.t] ? "true" : "false");
      filter();
    });
    var rt = null;
    function onResize() { clearTimeout(rt); rt = setTimeout(layout, 150); }
    window.addEventListener("resize", onResize);
    cleanup.push(function () { window.removeEventListener("resize", onResize); });
  }

  /* ===================================================== 3. audiences
     The communities form one after the other on a map laid out like the
     hero's, then their scores: gauges for the one in focus, and a matrix
     of all of them (affinity against penetration, size = opportunity). */
  /* close enough that the communities overlap, as they do in the hero */
  var SLOTS = [
    { x: 0.4, y: 0.54, r: 0.33, n: 2200, swirl: 0.55 },
    { x: 0.59, y: 0.38, r: 0.27, n: 1500, swirl: -0.6 },
    { x: 0.6, y: 0.68, r: 0.25, n: 1300, swirl: 0.5 },
    { x: 0.24, y: 0.36, r: 0.21, n: 900, swirl: 0.6 },
    { x: 0.77, y: 0.52, r: 0.23, n: 1000, swirl: -0.55 }
  ];
  var OUT = [{ x: 0.08, y: 0.76, r: 0.05, n: 12 }, { x: 0.46, y: 0.1, r: 0.04, n: 9 }, { x: 0.93, y: 0.14, r: 0.04, n: 9 }, { x: 0.44, y: 0.92, r: 0.04, n: 10 }];

  function ring(v, color, label) {
    var C = 2 * Math.PI * 26;
    return '<div class="gauge"><svg viewBox="0 0 64 64" aria-hidden="true"><circle class="gauge__bg" cx="32" cy="32" r="26"/>' +
      '<circle class="gauge__v" cx="32" cy="32" r="26" stroke="' + color + '" stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + C.toFixed(1) + '" data-v="' + v + '"/></svg>' +
      '<b>' + v + "</b><span>" + label + "</span></div>";
  }

  function audiences() {
    var d = data(), G = d.groups, map = null;
    var sel = G.reduce(function (b, g, i) { return g.opp > G[b].opp ? i : b; }, 0);
    var comms = G.map(function (g, i) { var s = SLOTS[i]; return { x: s.x, y: s.y, r: s.r, n: s.n, swirl: s.swirl, color: g.color }; });
    var MW = 320, MH = 230, MP = { l: 30, r: 14, t: 14, b: 28 };
    /* the axes cover the range the scores use, so the bubbles spread out */
    var pens = G.map(function (g) { return g.pen; }), affs = G.map(function (g) { return g.aff; });
    var p0 = Math.max(0, Math.min.apply(null, pens) - 8), p1 = Math.min(100, Math.max.apply(null, pens) + 10);
    var a0 = Math.max(0, Math.min.apply(null, affs) - 10), a1 = Math.min(100, Math.max.apply(null, affs) + 8);
    function MX(v) { return MP.l + (v - p0) / (p1 - p0) * (MW - MP.l - MP.r); }
    function MY(v) { return MP.t + (1 - (v - a0) / (a1 - a0)) * (MH - MP.t - MP.b); }
    var midP = Math.max(p0 + 4, Math.min(p1 - 4, 40)), midA = Math.max(a0 + 4, Math.min(a1 - 4, 60));
    /* each name goes where it covers no other bubble or name */
    var pts = G.map(function (a) { return { x: MX(a.pen), y: MY(a.aff), rr: 5 + a.opp / 11 }; });
    var taken = pts.map(function (q) { return [q.x - q.rr, q.y - q.rr, q.rr * 2, q.rr * 2]; });
    var bubbles = G.map(function (a, i) {
      var q = pts[i], label = L(a.short), w = label.length * 5.9 + 2, h = 12;
      var cands = [[q.rr + 5, 4, "start"], [-(q.rr + 5), 4, "end"], [0, -(q.rr + 5), "middle"], [0, q.rr + 13, "middle"]];
      var pick = cands[0], least = Infinity;
      cands.forEach(function (cd) {
        var bx = cd[2] === "start" ? q.x + cd[0] : cd[2] === "end" ? q.x + cd[0] - w : q.x - w / 2, by = q.y + cd[1] - 10;
        if (bx < MP.l || bx + w > MW - 2 || by < 2 || by + h > MH - MP.b + 6) return;
        var o = taken.reduce(function (s2, t2, j) {
          if (j === i) return s2;
          var ox = Math.min(bx + w + 2, t2[0] + t2[2]) - Math.max(bx - 2, t2[0]), oy = Math.min(by + h + 1, t2[1] + t2[3]) - Math.max(by - 1, t2[1]);
          return s2 + (ox > 0 && oy > 0 ? ox * oy : 0);
        }, 0);
        if (o < least - 0.5) { least = o; pick = cd; pick.box = [bx, by, w, h]; }
      });
      if (pick.box) taken.push(pick.box);
      return '<g class="mb" data-i="' + i + '" tabindex="0" role="button" transform="translate(' + q.x.toFixed(1) + "," + q.y.toFixed(1) + ')" style="--c:' + a.color + '" aria-label="' +
        esc(L(a.name)) + ", " + t("affinity", "affinité") + " " + a.aff + ", " + t("penetration", "pénétration") + " " + a.pen + ", " + t("opportunity", "opportunité") + " " + a.opp + '">' +
        '<circle class="mb__halo" r="' + (8 + a.opp / 5).toFixed(1) + '"/><circle class="mb__dot" r="' + q.rr.toFixed(1) + '"/>' +
        '<text class="mb__t" x="' + pick[0].toFixed(1) + '" y="' + pick[1].toFixed(1) + '" text-anchor="' + pick[2] + '">' + esc(label) + "</text></g>";
    }).join("");
    var matrix =
      '<svg class="uv-svg matrix" viewBox="0 0 ' + MW + " " + MH + '" role="group" aria-label="' + t("Affinity against penetration", "Affinité et pénétration") + '">' +
        '<rect class="mz" x="' + MP.l + '" y="' + MP.t + '" width="' + (MX(midP) - MP.l).toFixed(1) + '" height="' + (MY(midA) - MP.t).toFixed(1) + '" rx="10"/>' +
        '<text class="mz__t" x="' + (MP.l + 8) + '" y="' + (MP.t + 15) + '">' + t("Opportunity zone", "Zone d'opportunité") + "</text>" +
        '<line class="g" x1="' + MX(midP).toFixed(1) + '" x2="' + MX(midP).toFixed(1) + '" y1="' + MP.t + '" y2="' + (MH - MP.b) + '"/>' +
        '<line class="g" x1="' + MP.l + '" x2="' + (MW - MP.r) + '" y1="' + MY(midA).toFixed(1) + '" y2="' + MY(midA).toFixed(1) + '"/>' +
        '<text class="ax" x="' + (MW - MP.r) + '" y="' + (MH - 8) + '" text-anchor="end">' + t("Penetration →", "Pénétration →") + "</text>" +
        '<text class="ax" x="11" y="' + ((MP.t + MH - MP.b) / 2) + '" text-anchor="middle" transform="rotate(-90 11 ' + ((MP.t + MH - MP.b) / 2) + ')">' + t("Affinity →", "Affinité →") + "</text>" +
        bubbles +
      "</svg>";
    var body =
      '<div class="aud3">' +
        '<div class="aud3__map aud3__map--mixed" id="a-map" aria-hidden="true"></div>' +
        '<div class="aud3__row">' +
          '<div class="aud2__focus" id="a-focus" aria-live="polite"></div>' +
          '<div class="aud3__matrix"><p class="aud3__k">' + t("Where each community sits", "Où se place chaque communauté") +
            ' <span>' + t("bubble size = opportunity", "taille = opportunité") + "</span></p>" + matrix + "</div>" +
        "</div>" +
      "</div>";
    stage.innerHTML = frame(t("Audience communities and their scores", "Communautés d'audience et leurs scores"),
      t("Watch the communities form. Hover the map or a bubble.", "Regardez les communautés se former. Survolez la carte ou une bulle."), body);
    var focusEl = document.getElementById("a-focus"), mx = stage.querySelector(".matrix");

    function focusCard(i) {
      var a = G[i];
      focusEl.style.setProperty("--c", a.color);
      focusEl.innerHTML =
        '<p class="afocus__name"><i></i>' + esc(L(a.name)) + "</p>" +
        '<p class="afocus__meta">' + a.share + " % " + t("of the conversation", "de la conversation") + " · " + num(total * a.share / 100) + " " + t("posts", "posts") + "</p>" +
        '<div class="gauges">' +
          ring(a.aff, "#EAA93D", t("Affinity", "Affinité")) +
          ring(a.pen, "#4292F2", t("Penetration", "Pénétration")) +
          ring(a.opp, "#2E9E6B", t("Opportunity", "Opportunité")) +
        "</div>" +
        '<p class="afocus__note">' + esc(L(a.note)) + "</p>";
      var C = 2 * Math.PI * 26;
      requestAnimationFrame(function () {
        Array.prototype.forEach.call(focusEl.querySelectorAll(".gauge__v"), function (el) {
          el.style.strokeDashoffset = (C * (1 - (+el.dataset.v) / 100)).toFixed(1);
        });
      });
      Array.prototype.forEach.call(mx.querySelectorAll(".mb"), function (b) { b.classList.toggle("is-on", +b.dataset.i === i); });
    }
    function pick(i) { sel = i; if (map) map.select(i); focusCard(i); }
    mx.addEventListener("click", function (e) { var b = e.target.closest(".mb"); if (b) pick(+b.dataset.i); });
    mx.addEventListener("keydown", function (e) { var b = e.target.closest(".mb"); if (b && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(+b.dataset.i); } });
    mx.addEventListener("mouseover", function (e) { var b = e.target.closest(".mb"); if (b) { if (map) map.select(+b.dataset.i); focusCard(+b.dataset.i); } });
    mx.addEventListener("mouseleave", function () { if (map) map.select(sel); focusCard(sel); });

    if (window.LicterMap) {
      map = window.LicterMap(document.getElementById("a-map"), {
        communities: comms, outliers: OUT, labels: G.map(function (a) { return L(a.name); }), grow: true,
        onHover: function (i) { focusCard(i >= 0 ? i : sel); },
        onSelect: function (i) { pick(i); }
      });
      if (map) { map.select(sel); cleanup.push(function () { map.destroy(); }); }
    }
    focusCard(sel);
    /* the count follows the communities forming, 0.65 s apart, 1.5 s each */
    autoProgress(650 * (G.length - 1) + 1500);
  }

  /* ======================================================== 4. trends
     A race: topics by share of the conversation, month by month over
     eighteen months. Rows reorder as topics overtake one another. */
  var MONTHS = 18;

  function trends() {
    var d = data();
    var RACE = d.topics.map(function (x) { return { name: [x[0], x[1]], color: x[2], f: shape(x[3]), lead: x[4], verdict: x[5] }; });
    /* the curves are shapes; scaled so that every post of every month adds
       up to the posts read, and the count grows month by month */
    var raw = 0, peak = 0, CUM = [];
    for (var m0 = 0; m0 <= MONTHS; m0++) {
      RACE.forEach(function (r) { var x = Math.max(0, r.f(m0)); raw += x; peak = Math.max(peak, x); });
      CUM.push(raw);
    }
    var scale = d.read / raw;
    total = d.read;
    /* pos: where the race is, in months, as a real number so it plays smoothly */
    var pos = 0, month = 0, sel = 0, playing = false, prevRank = null;
    var start = new Date(2024, 3, 1);
    function monthLabel(m, long) {
      var dt = new Date(start.getFullYear(), start.getMonth() + m, 1);
      return dt.toLocaleDateString(fr() ? "fr-FR" : "en-GB", { month: long ? "long" : "short", year: "numeric" });
    }
    /* open on the fastest riser */
    var bestRise = -Infinity;
    RACE.forEach(function (r, i) { var rise = r.f(MONTHS) - r.f(0); if (rise > bestRise) { bestRise = rise; sel = i; } });
    var ROW = 38;
    var body =
      '<div class="rc">' +
        '<div class="rc__top">' +
          '<p class="rc__when" id="t-when"></p>' +
          '<div class="rc__ctrl">' +
            '<button class="play2__btn" type="button" id="t-play">▶</button>' +
            '<input type="range" id="t-range" min="0" max="' + MONTHS + '" step="any" value="0" aria-label="' + t("Month", "Mois") + '" />' +
          "</div>" +
        "</div>" +
        '<div class="rc__list" id="t-race" style="height:' + (RACE.length * ROW) + 'px">' +
          RACE.map(function (r, i) {
            return '<button class="rc__row" type="button" data-i="' + i + '" style="--c:' + r.color + '">' +
              '<span class="rc__rank"></span>' +
              '<span class="rc__name"><i></i>' + esc(L(r.name)) + "</span>" +
              '<span class="rc__track"><span class="rc__bar"></span><b class="rc__v"></b></span>' +
              '<span class="rc__move"></span></button>';
          }).join("") +
        "</div>" +
        '<div class="rc__detail" id="t-card"></div>' +
      "</div>";
    stage.innerHTML = frame(t("Topics, posts per month over 18 months", "Sujets, posts par mois sur 18 mois"),
      t("Watch them overtake each other. Click a topic.", "Regardez-les se dépasser. Cliquez un sujet."), body);
    var race = document.getElementById("t-race"), rows = Array.prototype.slice.call(race.querySelectorAll(".rc__row"));
    var range = document.getElementById("t-range"), btn = document.getElementById("t-play");

    function vals(m) { return RACE.map(function (r) { return Math.max(0, r.f(m)) * scale; }); }
    function draw() {
      month = Math.min(MONTHS, Math.floor(pos + 1e-6));
      var v = vals(pos);
      var order = v.map(function (x, i) { return i; }).sort(function (a, b) { return v[b] - v[a]; });
      var rank = []; order.forEach(function (i, k) { rank[i] = k; });
      rows.forEach(function (row, i) {
        row.style.transform = "translateY(" + (rank[i] * ROW) + "px)";
        row.querySelector(".rc__rank").textContent = rank[i] + 1;
        row.querySelector(".rc__bar").style.width = Math.max(1.5, v[i] / (peak * scale) * 100).toFixed(1) + "%";
        row.querySelector(".rc__v").textContent = num(v[i]);
        var mv = row.querySelector(".rc__move");
        if (prevRank && prevRank[i] !== rank[i]) {
          var up = prevRank[i] > rank[i];
          mv.textContent = up ? "↑" : "↓"; mv.className = "rc__move " + (up ? "is-up" : "is-down");
        }
        row.classList.toggle("is-on", i === sel);
        row.setAttribute("aria-label", (rank[i] + 1) + ". " + L(RACE[i].name) + ", " + num(v[i]) + " " + t("posts", "posts"));
      });
      prevRank = rank;
      document.getElementById("t-when").innerHTML = "<b>" + monthLabel(month, true) + "</b><span>" + t("Month ", "Mois ") + month + " / " + MONTHS + "</span>";
      range.value = pos; range.style.setProperty("--fill", (pos / MONTHS * 100) + "%");
      range.setAttribute("aria-valuetext", monthLabel(month, true));
      detail();
      var i = Math.min(MONTHS - 1, Math.floor(pos));
      progress((CUM[i] + (CUM[i + 1] - CUM[i]) * (pos - i)) / raw);
    }
    function detail() {
      var r = RACE[sel], s = [], lo = Infinity, hi = -Infinity;
      for (var m = 0; m <= MONTHS; m++) { var x = Math.max(0, r.f(m)) * scale; s.push(x); lo = Math.min(lo, x); hi = Math.max(hi, x); }
      var sw = 220, sh = 46, span = (hi - lo) || 1;
      function SY(x) { return (sh - 5 - (x - lo) / span * (sh - 10)).toFixed(1); }
      var path = s.map(function (x, m) { return (m ? "L" : "M") + (m / MONTHS * sw).toFixed(1) + " " + SY(x); }).join(" ");
      var fill = path + " L" + sw + " " + sh + " L0 " + sh + " Z";
      var now = s[month], ch = Math.round(now - s[0]);
      document.getElementById("t-card").innerHTML =
        '<div class="rcd__id" style="--c:' + r.color + '"><p class="rcd__name"><i></i>' + esc(L(r.name)) + "</p>" +
          '<p class="rcd__lead">' + t("Driven by ", "Porté par ") + "<b>" + esc(L(r.lead)) + "</b></p></div>" +
        '<div class="rcd__num"><b>' + num(now) + "</b><span>" + t("posts this month", "posts ce mois-ci") + "</span></div>" +
        '<div class="rcd__num"><b class="' + (ch >= 0 ? "is-up" : "is-down") + '">' + (ch >= 0 ? "+" : "−") + num(Math.abs(ch)) + "</b><span>" + t("vs ", "vs ") + monthLabel(0) + "</span></div>" +
        '<svg class="rcd__spark" viewBox="0 0 ' + sw + " " + sh + '" preserveAspectRatio="none" aria-hidden="true" style="--c:' + r.color + '"><path class="f" d="' + fill + '"/><path class="l" d="' + path + '"/>' +
          '<circle cx="' + (pos / MONTHS * sw).toFixed(1) + '" cy="' + SY(Math.max(0, r.f(pos)) * scale) + '" r="3.5"/></svg>' +
        '<p class="rcd__verdict rcd__verdict--' + r.verdict[0] + '">' + esc(fr() ? r.verdict[2] : r.verdict[1]) + "</p>";
    }
    function stopPlay() { playing = false; btn.textContent = "▶"; btn.setAttribute("aria-label", t("Play 18 months", "Lire 18 mois")); }
    /* one frame at a time, about 0.36 s a month */
    var MS_PER_MONTH = 360;
    function play() {
      if (pos >= MONTHS) { pos = 0; prevRank = null; }
      if (reduced.matches) { pos = MONTHS; draw(); return; }
      btn.textContent = "❚❚"; btn.setAttribute("aria-label", t("Pause", "Pause"));
      playing = true;
      var my = gen, last = performance.now();
      (function step(now) {
        if (!playing || my !== gen) return;
        pos = Math.min(MONTHS, pos + (now - last) / MS_PER_MONTH);
        last = now;
        draw();
        if (pos >= MONTHS) { stopPlay(); return; }
        requestAnimationFrame(step);
      })(last);
    }
    btn.addEventListener("click", function () { if (playing) stopPlay(); else play(); });
    range.addEventListener("input", function () { stopPlay(); pos = +range.value; draw(); });
    /* the arrow keys still move a whole month */
    range.addEventListener("keydown", function (e) {
      var dir = e.key === "ArrowRight" || e.key === "ArrowUp" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -1 : 0;
      if (!dir) return;
      e.preventDefault(); stopPlay();
      pos = Math.max(0, Math.min(MONTHS, (dir > 0 ? Math.floor(pos + 1e-6) : Math.ceil(pos - 1e-6)) + dir));
      draw();
    });
    race.addEventListener("click", function (e) { var r = e.target.closest(".rc__row"); if (!r) return; sel = +r.dataset.i; draw(); });
    stopPlay(); draw();
    later(play, 500);
    cleanup.push(stopPlay);
  }

  /* ============================================================ switch */
  var RENDER = { communication: communication, brand: brand, audiences: audiences, trends: trends };

  function render() {
    stopAll();
    gen += 1; answered = false; total = data().read || 0;
    RENDER[current]();
    var close = document.getElementById("uv-close");
    if (close) close.addEventListener("click", closeCase);
    var next = document.getElementById("uv-next");
    if (next) next.addEventListener("click", function () { sector = nextSector(current); render(); document.getElementById("uv-next").focus(); });
    stage.classList.remove("is-in"); void stage.offsetWidth; stage.classList.add("is-in");
    runSide();
  }

  /* back to the empty state: no question open */
  var EMPTY = stage.innerHTML;
  function closeCase() {
    var tab = document.getElementById("tab-" + current);
    stopAll(); gen += 1; current = null;
    topics.forEach(function (b) { b.classList.remove("is-on"); b.setAttribute("aria-selected", "false"); });
    stage.removeAttribute("aria-labelledby");
    stage.classList.remove("has-feed", "is-in");
    stage.innerHTML = EMPTY;
    if (tab) tab.focus();
  }

  function select(key) {
    current = key;
    sector = nextSector(key);
    topics.forEach(function (b) {
      var on = b.dataset.topic === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    stage.setAttribute("aria-labelledby", "tab-" + key);
    stage.classList.add("has-feed");
    render();
  }

  topics.forEach(function (b, i) {
    b.addEventListener("click", function () { select(b.dataset.topic); });
    b.addEventListener("keydown", function (e) {
      var dir = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!dir) return;
      e.preventDefault();
      var n = topics[(i + dir + topics.length) % topics.length];
      n.focus(); select(n.dataset.topic);
    });
  });

  /* the first question plays on its own when the section comes into view:
     the visual is the point of the section, it should not wait for a click */
  var section = document.getElementById("use-cases"), launched = false;
  if (section && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      if (launched) return;
      if (current) { launched = true; io.disconnect(); return; }
      if (entries[0].isIntersecting) { launched = true; io.disconnect(); select(topics[0].dataset.topic); }
    }, { threshold: 0.35 });
    io.observe(section);
  }

  if (window.MutationObserver) {
    new MutationObserver(function () { if (current) render(); })
      .observe(html, { attributes: true, attributeFilter: ["lang"] });
  }
})();
