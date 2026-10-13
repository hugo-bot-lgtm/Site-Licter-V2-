"""Shared page components for the builders.

qa_roller: the question-and-answer roller (after the "FAQ roller" design
picked in October 2026): cards on two rows that drift sideways, each row
the other way, pausing under the pointer, on focus or on a tap. It is the
standard for every long-form "in detail" section. The HTML holds each card
once; js/ui.js clones the cards for the loop (aria-hidden), so search
engines read the text once. Without JS, or with reduced motion, the rows
simply scroll by hand.
"""


def slug(text):
    """an anchor from a heading: lower case, ascii, hyphens"""
    import re, unicodedata
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


def guide_article(cards, toc_label, by=""):
    """the long-form section as a readable article (audit of 12 October 2026: on
    a page that competes for a definition query, the roller showed a quarter of
    each answer): a table of contents, then every question with its full answer"""
    import html as _h, re
    # numbered anchors: text extractors (trafilatura) drop any element whose id
    # contains "social", taken for share buttons, which hid half the guide
    ids = ["guide-%d" % (k + 1) for k in range(len(cards))]
    toc = "".join('<li><a href="#%s">%s</a></li>' % (i, q) for i, (q, _) in zip(ids, cards))
    body = "".join('<section class="lg__b" id="%s"><h3>%s</h3>%s</section>' % (i, q, "".join(x if x.startswith("<table") else "<p>%s</p>" % x for x in a))
                   for i, (q, a) in zip(ids, cards))
    # the contents fold on a phone (js/ui.js closes them there): 14 entries stood before the text
    return (by + '<div class="lg"><nav class="lg__toc" aria-label="%s"><details class="lg__toc-d" open><summary class="lg__toc-k">%s <span>(%d)</span></summary><ol>%s</ol></details></nav>'
            '<div class="lg__body">%s</div></div>') % (toc_label, toc_label, len(cards), toc, body)


def qa_roller(cards, label, more, rows=2, by=""):
    """cards: [(question_html, [paragraph_html, ...])], already translated;
    one card per question, all its paragraphs in it"""
    lanes = [[] for _ in range(rows)]
    for i, c in enumerate(cards):
        lanes[i % rows].append(c)
    out = []
    for n, lane in enumerate(lanes):
        if not lane:
            continue
        items = "".join(('<div class="qa-card"><h3>%s</h3><div class="qa-card__a">%s</div>'
             '<button class="qa-card__more" type="button">%s<span class="visually-hidden"> : </span><span class="visually-hidden">%s</span> <span aria-hidden="true">→</span></button></div>')
            % (q, "".join("<p>%s</p>" % x for x in a), more, q) for q, a in lane)
        out.append('<div class="qa-roller__row" data-dir="%s"><div class="qa-roller__track">%s</div></div>' % ("right" if n % 2 else "left", items))
    return by + '<div class="qa-roller" role="region" aria-label="%s">%s</div>' % (label, "".join(out))


def authors_line(written, and_, role):
    """who wrote a long-form section: the founders, linked to their profiles
    on Why Licter (already translated words passed in), and when the page last
    changed (tools/build-seo.py puts the real date in the <time>)"""
    import datetime
    d = datetime.date.today()
    fr = not written.startswith("Written")
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    label = "%d %s %d" % (d.day, mois[d.month - 1], d.year) if fr else "%d %s" % (d.day, d.strftime("%B %Y"))
    # a span, not a <time>: text extractors (trafilatura) drop <time> with its text,
    # which left "publié le" without a date (audit of 9 October 2026)
    when = ('<span class="qa-by__when"> · <span>%s</span> <span class="by-date" data-datetime="%s">%s</span></span>'
            % ("mis à jour le" if fr else "updated", d.isoformat(), label))
    return ('<p class="qa-by">%s <a href="why-licter.html#antoine-khaitrine">Antoine Khaitrine</a> %s '
            '<a href="why-licter.html#adrien-krebs">Adrien Krebs</a>%s%s</p>') % (written, and_, role, when)


# the title of each source document, shown instead of its address (audit of 9 October 2026)
SOURCE_TITLE = {
    "https://blog.google/intl/fr-fr/nouveautes-produits/explorez-obtenez-des-reponses/recherche-ia-apercus-mode/": "Google · Aperçus IA et Mode IA",
    "https://developers.google.com/search/docs/appearance/ai-features": "Google Search Central · Fonctionnalités d'IA",
    "https://claude.com/blog/web-search": "Anthropic · Claude can now search the web",
    "https://docs.perplexity.ai/docs/resources/perplexity-crawlers": "Perplexity · Perplexity crawlers",
    "https://developers.openai.com/api/docs/bots": "OpenAI · Overview of OpenAI crawlers",
    "https://arxiv.org/abs/2311.09735": "arXiv · GEO: Generative Engine Optimization (2023)",
    "https://arxiv.org/html/2311.09735v3": "arXiv · GEO-bench, version 3",
    "https://arxiv.org/abs/2005.14165": "arXiv · Language Models are Few-Shot Learners (GPT-3)",
    "https://tech.eu/2022/12/05/audiense/": "Tech.eu · Audiense acquires SoPrism (2022)",
    "https://help.audiense.com/knowledge/audiense-data-sources": "Audiense · Data sources",
    "https://www.cnil.fr": "CNIL · site officiel",
    "https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre2": "CNIL · RGPD, chapitre II\u00a0: les principes",
    "https://www.cnil.fr/fr/les-bases-legales/interet-legitime": "CNIL · L'intérêt légitime",
    "https://www.cnil.fr/fr/recommandations-reutilisateurs-donnees-internet": "CNIL · Recommandations aux réutilisateurs de données publiées sur internet",
    "https://datareportal.com/reports/digital-2026-two-in-three-people-use-social-media": "DataReportal · Digital 2026",
    "https://help.openai.com/en/articles/8590148-memory-faq": "OpenAI · Memory FAQ",
    "https://techcrunch.com/snippet/2932195/openai-brings-search-to-all-users/": "TechCrunch · OpenAI brings search to all users",
    "https://seroundtable.com/chatgpt-search-open-38588.html": "Search Engine Roundtable · ChatGPT search open to all (2024)",
    "https://help.openai.com/en/articles/9237897-chatgpt-search": "OpenAI · ChatGPT search",
    "https://help.openai.com/en/articles/12627856-publishers-and-developers-faq": "OpenAI · Publishers and developers FAQ",
    "https://claude.com/blog/memory": "Anthropic · Memory in Claude",
    "https://support.claude.com/en/articles/10684626-enable-and-use-web-search": "Anthropic · Enable and use web search",
    "https://www.anthropic.com/transparency": "Anthropic · Transparency hub",
    "https://privacy.claude.com/en/articles/7996885-how-do-you-use-personal-data-in-model-training": "Anthropic · Personal data in model training",
    "https://platform.claude.com/docs/en/about-claude/models/overview": "Anthropic · Models overview",
    "https://www.anthropic.com/constitution": "Anthropic · Claude's constitution",
    "https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations": "Anthropic · Reduce hallucinations",
    "https://www.anthropic.com/news/the-anthropic-economic-index": "Anthropic · The Anthropic Economic Index",
    "https://claude.com/blog/claude-for-enterprise": "Anthropic · Claude for Enterprise (2024)",
    "https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler": "Anthropic · Does Anthropic crawl data from the web?",
    "https://support.google.com/gemini/answer/13695044": "Google Gemini Help · Public information Gemini uses",
    "https://support.google.com/gemini/answer/14143489": "Google Gemini Help · Sources and double-check",
    "https://support.google.com/business/answer/7091": "Google Business Profile Help · Local ranking",
    "https://blog.google/products-and-platforms/products/maps/ask-maps-immersive-navigation/": "Google · Ask Maps and immersive navigation",
    "https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers": "Google Search Central · Google's common crawlers",
    "https://blog.google/products-and-platforms/products/search/new-controls-website-owners/": "Google · New controls for website owners",
    "https://gemini.google/overview/personalization/": "Google · Gemini personalization",
    "https://support.google.com/gemini/answer/13275746": "Google Gemini Help · Rate and report responses",
    "https://fr.wikipedia.org/wiki/Wikipédia:Conflit_d'intérêts": "Wikipédia · Conflit d'intérêts",
    "https://x.ai/news/grok": "xAI · Announcing Grok (2023)",
    "https://help.x.com/en/using-x/about-grok": "X · About Grok",
    "https://x.ai/news/grok-1212": "xAI · Grok update (December 2024)",
    "https://techcrunch.com/2025/03/07/x-now-lets-you-query-grok-by-mentioning-it-in-replies": "TechCrunch · Query Grok by mentioning it in replies (2025)",
    "https://tech.yahoo.com/articles/ask-grok-supposed-x-better-182752572.html": "Business Insider · Asking Grok on X (2025)",
    "https://www.perplexity.ai/help-center/en/articles/10352895-how-does-perplexity-work": "Perplexity · How does Perplexity work?",
    "https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search": "Perplexity · What is Pro Search?",
    "https://www.perplexity.ai/help-center/en/articles/10352155-what-is-perplexity": "Perplexity · What is Perplexity?",
    "https://www.talkwalker.com/press-release/hootsuite": "Talkwalker · Hootsuite acquires Talkwalker",
    "https://talkwalker.com/products/bluesilkai": "Talkwalker · Blue Silk AI",
    "https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you": "TikTok · How TikTok recommends videos #ForYou",
    "https://ads.tiktok.com/help/article/how-to-use-trends": "TikTok · How to use Trends",
    "https://developers.tiktok.com/products/research-api/": "TikTok · Research API",
    "https://newsroom.tiktok.com/en-eu/compliance-digital-services-act-eu": "TikTok · Digital Services Act compliance",
}


# network page sources, in the page's language (audit of 13 October 2026: labels cut from the address read badly)
SOURCE_PAIR = {
    'https://abc17news.com/money/cnn-social-media-technology/2022/04/28/chinas-weibo-shows-user-locations-to-combat-bad-behavior/': ('CNN · Weibo affiche la localisation des utilisateurs (2022)', 'CNN · Weibo shows user locations (2022)'),
    'https://about.fb.com/news/2019/08/groups-privacy-settings/': ('Meta · Confidentialité des groupes Facebook (2019)', 'Meta · Facebook Groups privacy settings (2019)'),
    'https://about.fb.com/news/2023/08/new-features-and-additional-transparency-measures-as-the-digital-services-act-comes-into-effect/': ('Meta · Transparence et Digital Services Act (2023)', 'Meta · Transparency and the Digital Services Act (2023)'),
    'https://about.fb.com/news/2023/12/default-end-to-end-encryption-on-messenger/': ('Meta · Chiffrement de bout en bout sur Messenger (2023)', 'Meta · End-to-end encryption on Messenger (2023)'),
    'https://anderegg.ca/2024/05/23/digging-into-bluesky-dms': ('Anderegg · Les messages privés de Bluesky (2024)', 'Anderegg · Digging into Bluesky DMs (2024)'),
    'https://blog.whatsapp.com/introducing-whatsapp-channels-a-private-way-to-follow-what-matters': ('WhatsApp · Lancement des chaînes', 'WhatsApp · Introducing Channels'),
    'https://bsky.network/docs/protocol-services': ('Bluesky · Services du protocole AT', 'Bluesky · AT Protocol services'),
    'https://bsky.social/about/blog/05-22-2024-direct-messages': ('Bluesky · Messages privés (2024)', 'Bluesky · Direct messages (2024)'),
    'https://bsky.social/about/blog/7-27-2023-custom-feeds': ('Bluesky · Fils personnalisés (2023)', 'Bluesky · Custom feeds (2023)'),
    'https://core.telegram.org/api/channel': ('Telegram · API des canaux', 'Telegram · Channels API'),
    'https://dev.twitch.tv/docs/chat/': ('Twitch · Documentation du chat', 'Twitch · Chat documentation'),
    'https://dev.vk.ru/en/wall.get': ('VK · API wall.get', 'VK · wall.get API'),
    'https://developer.x.com/en/docs/x-api/compliance/streams/integrate/honoring-user-intent': ("X · Respect des suppressions dans l'API", 'X · Honoring user intent in the API'),
    'https://developers.facebook.com/docs/content-library-and-api/content-library': ('Meta · Content Library', 'Meta · Content Library'),
    'https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/hashtag-search': ("Meta · Recherche par hashtag de l'API Instagram", 'Meta · Instagram API hashtag search'),
    'https://developers.facebook.com/documentation/threads/keyword-search': ("Meta · Recherche par mot-clé de l'API Threads", 'Meta · Threads API keyword search'),
    'https://developers.google.com/youtube/terms/developer-policies': ('YouTube · Règles pour les développeurs', 'YouTube · Developer policies'),
    'https://developers.weixin.qq.com/doc/service/en/api/leaving/api_listcomment': ('WeChat · API des commentaires', 'WeChat · Comments API'),
    'https://docs.discord.com/developers/gateway/you-might-not-need-a-privileged-intent': ("Discord · Accès aux messages par l'API", 'Discord · Message access in the API'),
    'https://docs.x.com/x-api/getting-started/pricing': ("X · Tarifs de l'API", 'X · API pricing'),
    'https://faq.whatsapp.com/1053543185312573': ("WhatsApp · Centre d'aide", 'WhatsApp · Help Center'),
    'https://help.instagram.com/1729008150678239/': ("Instagram · Centre d'aide", 'Instagram · Help Center'),
    'https://help.pinterest.com/business/article/pinterest-trends': ('Pinterest · Pinterest Trends', 'Pinterest · Pinterest Trends'),
    'https://help.pinterest.com/en/articles/secret-boards': ('Pinterest · Tableaux secrets', 'Pinterest · Secret boards'),
    'https://help.snapchat.com/hc/en-us/articles/7012334940948-When-does-Snapchat-delete-Snaps-and-Chats': ('Snapchat · Suppression des Snaps et des chats', 'Snapchat · When Snaps and Chats are deleted'),
    'https://help.snapchat.com/hc/en-us/articles/7012338216468-What-s-the-difference-between-posting-to-My-Story-Public-and-My-Story-Friends': ('Snapchat · Story publique et Story amis', 'Snapchat · Public Story and Friends Story'),
    'https://help.snapchat.com/hc/en-us/articles/7012347065876-What-is-a-Public-Profile-on-Snapchat': ('Snapchat · Le profil public', 'Snapchat · Public Profile'),
    'https://help.x.com/en/using-x/community-notes': ('X · Notes de la communauté', 'X · Community Notes'),
    'https://ir.bilibili.com/': ('Bilibili · Relations investisseurs', 'Bilibili · Investor relations'),
    'https://jingdaily.com/intels/2024-12/16/xiaohongshu-search-volume-doubles-baidu-s-lead-shrinks': ('Jing Daily · Le volume de recherche de Xiaohongshu double (2024)', 'Jing Daily · Xiaohongshu search volume doubles (2024)'),
    'https://kr-asia.com/xiaohongshu-sues-ghostwriter-brokers-over-fraudulent-promotional-content': ('KrASIA · Xiaohongshu contre les faux contenus promotionnels', 'KrASIA · Xiaohongshu sues fake promotion brokers'),
    'https://redditinc.com/policies/data-api-terms': ("Reddit · Conditions de l'API de données", 'Reddit · Data API terms'),
    'https://research.youtube.com/': ('YouTube · Programme pour les chercheurs', 'YouTube · Researcher Program'),
    'https://support.discord.com/hc/en-us/articles/360030843331-Enabling-Server-Discovery': ('Discord · Découverte des serveurs', 'Discord · Server Discovery'),
    'https://support.google.com/youtube/answer/9483359?hl=en': ('Aide YouTube · Google', 'YouTube Help · Google'),
    'https://techcrunch.com/2024/09/12/threads-makes-it-easier-to-evangelize-the-open-social-web-with-a-new-direct-link-feature': ('TechCrunch · Threads et le web social ouvert (2024)', 'TechCrunch · Threads and the open social web (2024)'),
    'https://telegram.org/tour/channels': ('Telegram · Les canaux', 'Telegram · Channels'),
    'https://transparency.meta.com/en-gb/researchtools/meta-content-library/': ('Meta · Meta Content Library pour la recherche', 'Meta · Meta Content Library for research'),
    'https://walkthechat.com/new-wechat-comments-function-subscription-accounts/': ('WalktheChat · Les commentaires sur WeChat', 'WalktheChat · WeChat comments'),
    'https://weixin.sogou.com/': ('Sogou · Recherche WeChat', 'Sogou · WeChat search'),
    'https://www.bellingcat.com/resources/2026/04/20/xiaohongshu-rednote-open-source-guide/': ("Bellingcat · Guide d'enquête sur Xiaohongshu (2026)", 'Bellingcat · Xiaohongshu open-source guide (2026)'),
    'https://www.goldthread2.com/culture/gain-full-access-these-videos-you-must-pass-exam-100-very-niche-questions/article/2157030': ("Goldthread · L'examen d'entrée de Bilibili", "Goldthread · Bilibili's membership exam"),
    'https://www.hrw.org/news/2017/05/16/ukraine-revoke-ban-dozens-russian-web-companies': ("Human Rights Watch · L'Ukraine bloque des services russes (2017)", 'Human Rights Watch · Ukraine bans Russian web companies (2017)'),
    'https://www.jonesday.com/en/insights/2021/09/highlights-of-chinas-new-personal-information-protection-law': ('Jones Day · La loi chinoise sur les données personnelles (2021)', "Jones Day · China's personal information law (2021)"),
    'https://www.linkedin.com/help/linkedin/answer/a1341387': ("LinkedIn · Centre d'aide", 'LinkedIn · Help Center'),
    'https://www.opb.org/article/2022/03/11/russia-widens-social-media-crackdown-by-blocking-instagram/': ('OPB · La Russie bloque Instagram (2022)', 'OPB · Russia blocks Instagram (2022)'),
    'https://www.opb.org/article/2024/08/14/meta-shutters-tool-used-to-fight-disinformation-despite-outcry': ('OPB · Meta ferme CrowdTangle (2024)', 'OPB · Meta shuts down CrowdTangle (2024)'),
    'https://www.pcgamer.com/twitch-eliminates-save-forever-option-as-it-moves-to-improve-video-on-demand-service/': ('PC Gamer · Twitch limite la conservation des vidéos', 'PC Gamer · Twitch limits video storage'),
    'https://www.sixthtone.com/news/1005795': ('Sixth Tone · Weibo', 'Sixth Tone · Weibo'),
    'https://www.snap.com/terms/spotlight-terms': ('Snap · Conditions de Spotlight', 'Snap · Spotlight terms'),
    'https://www.whatsapp.com/privacy': ('WhatsApp · Politique de confidentialité', 'WhatsApp · Privacy policy'),
    'https://www.whatsonweibo.com/are-douyin-and-tiktok-the-same/': ("What's on Weibo · Douyin et TikTok", "What's on Weibo · Douyin and TikTok"),
}

def comma_join(links):
    """links separated by commas, each comma kept with its link: when the links
    are boxes, a line could otherwise start with a lone comma (audit of 13 October 2026)"""
    return " ".join('<span class="xp-i">%s%s</span>' % (l, "," if k < len(links) - 1 else "") for k, l in enumerate(links))


def source_label(u, note="", lang=1):
    """a readable label for a source link: its title when known, the note written
    next to it, otherwise the host and the page name (audit of 12 October 2026:
    bare domain names said nothing about the document)"""
    import re
    if u in SOURCE_PAIR:
        return SOURCE_PAIR[u][lang]
    if u in SOURCE_TITLE:
        return SOURCE_TITLE[u]
    host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
    note = re.split(r"[:;,]| \(|\d{1,2} \w+ 20\d\d", note)[0].strip(" \"'")
    if 4 <= len(note) <= 60:
        return host + " · " + note
    path = u.split(host, 1)[1].split("?")[0].strip("/")
    parts = [x for x in path.split("/") if x and not re.fullmatch(r"[a-z]{2}(-[a-z]{2})?|\d+|hc|articles?|docs?|answer|news|blog|about", x)]
    tail = re.sub(r"^\d{1,2}-\d{1,2}-\d{4}-|^\d+[-_]?", "", parts[-1] if parts else "")
    tail = re.sub(r"\.(html?|pdf)$", "", tail).replace("-", " ").replace("_", " ").strip()
    tail = re.sub(r"^\d{1,2} \d{1,2} \d{4} ", "", tail)
    if re.fullmatch(r"[\d ]*", tail):
        tail = ""
    return host + (" · " + (tail[:40].rsplit(" ", 1)[0] if len(tail) > 40 else tail) if tail else "")


def sources_line(module_file, label):
    """the public sources a long-form section relies on: the "# source:" notes
    of its module (every public fact there is checked and noted), shown as
    links under the section (SEO audit of 8 October 2026)"""
    import html, pathlib, re
    urls = []
    for u in re.findall(r"# source: (https?://[^\s)]+)", pathlib.Path(module_file).read_text()):
        u = u.rstrip(".,;")
        if u not in urls:
            urls.append(u)
    if not urls:
        return ""
    # a readable label: the note written next to the source when there is one,
    # otherwise the page name without its numeric id and hyphens
    notes = {}
    for u_, n_ in re.findall(r"# source: (https?://[^\s)]+)\s*\(([^)]*)\)", pathlib.Path(module_file).read_text()):
        notes.setdefault(u_.rstrip(".,;"), n_)
    name = lambda u: source_label(u, notes.get(u, ""))
    links = comma_join(['<a href="%s" rel="noopener" target="_blank">%s</a>' % (html.escape(u, quote=True), html.escape(name(u))) for u in urls])
    return '<p class="qa-src"><span>%s</span> %s</p>' % (label, links)
