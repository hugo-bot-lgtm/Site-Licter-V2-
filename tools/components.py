"""Shared page components for the builders.

qa_roller: the question-and-answer roller (after the "FAQ roller" design
picked in October 2026): cards on two rows that drift sideways, each row
the other way, pausing under the pointer, on focus or on a tap. It is the
standard for every long-form "in detail" section. The HTML holds each card
once; js/ui.js clones the cards for the loop (aria-hidden), so search
engines read the text once. Without JS, or with reduced motion, the rows
simply scroll by hand.
"""


def qa_roller(cards, label, more, rows=2):
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
    return '<div class="qa-roller" role="region" aria-label="%s">%s</div>' % (label, "".join(out))
