"""What Licter has actually done with a tool or on a network (SEO plan, step
17): only published work, its figures as published, each with its source.
Pages without real material get no block. Read by tools/build-tech.py."""

GP = "article-gp-explorer-3-squeezie-bat-les-records-daudience.html"
HUDA = "article-le-bad-buzz-huda-beauty-decrypte.html"
XEXIT = "article-departs-de-x-quels-reseaux-sociaux-peuvent-rivaliser-avec-la-plateforme-delon-musk.html"
LUXE = "offer-vigie-360.html"

PROOF = {
    "visibrain": [
        (("GP Explorer 3, lu avec Visibrain", "GP Explorer 3, read with Visibrain"),
         ("Plus de 185 000 tweets pendant le pic d'audience, 95 % de mentions positives ou neutres : notre analyse de l'événement de Squeezie, menée avec Visibrain.",
          "More than 185,000 tweets at peak audience, 95% positive or neutral mentions: our analysis of Squeezie's event, run with Visibrain."), GP),
        (("Le bad buzz Huda Beauty", "The Huda Beauty backlash"),
         ("Avec Visibrain, nous avons suivi le boycott sur TikTok, Instagram et X, dans 51 langues, jusqu'au record de 26,1 millions de vues en une journée.",
          "With Visibrain, we followed the boycott on TikTok, Instagram and X, in 51 languages, up to a record of 26.1 million views in a day."), HUDA)],
    "talkwalker": [
        (("Talkwalker, vu de l'intérieur", "Talkwalker, from the inside"),
         ("Dans notre podcast Audience First, Charlotte, qui a ouvert le bureau parisien de Talkwalker, explique comment les marques utilisent la plateforme, et pourquoi l'humain reste nécessaire.",
          "In our Audience First podcast, Charlotte, who opened Talkwalker's Paris office, explains how brands use the platform, and why people are still needed."), "article-licter-talkwalker-podcast.html")],
    "radarly": [
        (("Radarly et le luxe", "Radarly and luxury"),
         ("Dans notre podcast Audience First, Nathalie Litvine (Meltwater) raconte comment les grands comptes du luxe exploitent la donnée de Radarly.",
          "In our Audience First podcast, Nathalie Litvine (Meltwater) explains how large luxury accounts use Radarly's data."), "article-licter-meltwater.html")],
    "twitch": [
        (("GP Explorer 3 : 1,4 million de spectateurs sur Twitch", "GP Explorer 3: 1.4 million viewers on Twitch"),
         ("Notre analyse de l'événement de Squeezie : 1,4 million de spectateurs en simultané sur Twitch, plus que le Grand Prix de Singapour diffusé le même jour.",
          "Our analysis of Squeezie's event: 1.4 million concurrent viewers on Twitch, more than the Singapore Grand Prix broadcast the same day."), GP)],
    "x-twitter": [
        (("185 000 tweets en un pic d'audience", "185,000 tweets at one audience peak"),
         ("Pendant le GP Explorer 3, plus de 185 000 tweets ont été publiés au pic de l'événement : notre lecture du volume et de la tonalité.",
          "During GP Explorer 3, more than 185,000 tweets were posted at the event's peak: our read of the volume and the tone."), GP),
        (("Une crise mondiale lue sur X", "A global crisis read on X"),
         ("Le boycott de Huda Beauty sur X : 40 000 tweets et 228 000 retweets, multipliés par 230 en 24 heures.",
          "The Huda Beauty boycott on X: 40,000 tweets and 228,000 retweets, up 230-fold in 24 hours."), HUDA)],
    "tiktok": [
        (("Huda Beauty : 26,1 millions de vues en un jour", "Huda Beauty: 26.1 million views in a day"),
         ("Notre décryptage du bad buzz Huda Beauty : 9 000 mentions sur TikTok, un record de 26,1 millions de vues en une journée, porté surtout par des micro-influenceurs.",
          "Our read of the Huda Beauty backlash: 9,000 mentions on TikTok, a record 26.1 million views in a single day, carried mostly by micro-influencers."), HUDA)],
    "instagram": [
        (("Huda Beauty sur Instagram", "Huda Beauty on Instagram"),
         ("Pendant le boycott, 6 000 publications sur Instagram, 28 fois plus que la période précédente, et 198 000 commentaires en une journée.",
          "During the boycott, 6,000 posts on Instagram, 28 times the previous period, and 198,000 comments in a single day."), HUDA)],
    "bluesky": [
        (("Départs de X : qui prend le relais ?", "Leaving X: who takes over?"),
         ("Notre lecture des départs de médias et d'organisations de X, et de ce que Bluesky, Threads et Mastodon peuvent offrir aux marques.",
          "Our read of media and organisations leaving X, and what Bluesky, Threads and Mastodon can offer brands."), XEXIT)],
    "threads": [
        (("Départs de X : qui prend le relais ?", "Leaving X: who takes over?"),
         ("Notre lecture des départs de médias et d'organisations de X, et de la place que Threads peut prendre pour les marques.",
          "Our read of media and organisations leaving X, and the room Threads can take for brands."), XEXIT)],
    "telegram": [
        (("La veille d'une dirigeante, Telegram compris", "Monitoring an executive, Telegram included"),
         ("Pour la PDG monde d'un leader du luxe, une veille 24 h/24 en cinq langues, dont Telegram, Wikipédia et le dark web, avec des alertes en moins de 15 minutes.",
          "For a luxury leader's global CEO, 24/7 monitoring in five languages, including Telegram, Wikipedia and the dark web, with alerts within 15 minutes."), LUXE)],
}
