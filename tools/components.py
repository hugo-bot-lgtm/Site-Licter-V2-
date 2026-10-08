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
        items = "".join(('<article class="qa-card"><h3>%s</h3><div class="qa-card__a">%s</div>'
             '<button class="qa-card__more" type="button">%s<span class="visually-hidden"> : </span><span class="visually-hidden">%s</span> <span aria-hidden="true">→</span></button></article>')
            % (q, "".join("<p>%s</p>" % x for x in a), more, q) for q, a in lane)
        out.append('<div class="qa-roller__row" data-dir="%s"><div class="qa-roller__track">%s</div></div>' % ("right" if n % 2 else "left", items))
    return by + '<div class="qa-roller" role="region" aria-label="%s">%s</div>' % (label, "".join(out))


def authors_line(written, and_, role):
    """who wrote a long-form section: the founders, linked to their profiles
    on Why Licter (already translated words passed in)"""
    return ('<p class="qa-by">%s <a href="why-licter.html#antoine-khaitrine">Antoine Khaitrine</a> %s '
            '<a href="why-licter.html#adrien-krebs">Adrien Krebs</a>%s</p>') % (written, and_, role)


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
    def name(u):
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        path = u.split(host, 1)[1].strip("/")
        tail = path.split("/")[-1] if path else ""
        return host + (" · " + tail[:38] if tail else "")
    links = ", ".join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (html.escape(u, quote=True), html.escape(name(u))) for u in urls)
    return '<p class="qa-src"><span>%s</span> %s</p>' % (label, links)
