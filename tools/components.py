"""Shared page components for the builders.

qa_roller: the question-and-answer roller (after the "FAQ roller" design
picked in October 2026): cards on two rows that drift sideways, each row
the other way, pausing under the pointer, on focus or on a tap. It is the
standard for every long-form "in detail" section. The HTML holds each card
once; js/ui.js clones the cards for the loop (aria-hidden), so search
engines read the text once. Without JS, or with reduced motion, the rows
simply scroll by hand.
"""


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
    "https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre2": "CNIL · RGPD, chapitre II : les principes",
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
    def name(u):
        if u in SOURCE_TITLE:
            return SOURCE_TITLE[u]
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        note = re.split(r"[:;,]| \(|\d{1,2} \w+ 20\d\d", notes.get(u, ""))[0].strip(" \"'")
        if 4 <= len(note) <= 60:
            return host + " · " + note
        path = u.split(host, 1)[1].strip("/")
        tail = re.sub(r"^\d+[-_]?", "", path.split("/")[-1] if path else "")
        tail = re.sub(r"\.(html?|pdf)$", "", tail).replace("-", " ").replace("_", " ").strip()
        return host + (" · " + (tail[:40].rsplit(" ", 1)[0] if len(tail) > 40 else tail) if tail else "")
    links = ", ".join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (html.escape(u, quote=True), html.escape(name(u))) for u in urls)
    return '<p class="qa-src"><span>%s</span> %s</p>' % (label, links)
