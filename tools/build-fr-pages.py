#!/usr/bin/env python3
"""Static French twins of four root pages, so that French is in the HTML
itself (search engines and AI crawlers read it without running js/i18n.js):

    why-licter.html  ->  /fr/pourquoi-licter/
    clients.html     ->  /fr/clients/
    blog.html        ->  /fr/blog/
    guide.html       ->  /fr/guide/

The English page stays the source (edit it, or tools/build-blog.py for the
blog): this script marks it as the English twin and writes the French one,
text translated with js/fr.js (the same walk as the browser), French title and
description, absolute links. tools/build-seo.py then adds the canonical and
hreflang pair. Run by tools/build-usecases.py and tools/build-blog.py, or:

    python3 tools/build-fr-pages.py
"""
import html, importlib.util, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ucb", ROOT / "tools" / "build-usecases.py")
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)

HEAD = {
    "why-licter.html": ("Pourquoi Licter | Cabinet de conseil en social data intelligence",
                        "Licter est un cabinet de conseil en social data intelligence fondé à Paris en 2022 par les responsables de la cellule data de l'Élysée. 50+ clients, 160+ projets."),
    "clients.html": ("Nos clients | Licter, social data intelligence",
                     "Plus de 50 organisations lisent leur marché avec Licter : Chanel, LVMH, L'Oréal, Danone, Unilever, Renault, Orange, Société Générale, l'UNESCO…"),
    "blog.html": ("Blog : social listening, audiences et prospective | Licter",
                  "Social listening, veille, consumer insights et influence : ce que nos consultants apprennent en mission, et nos entretiens avec L'Oréal, AXA, LVMH ou Kantar."),
    "guide.html": ("Les 12 questions auxquelles répond la social data | Licter",
                   "Un guide offert : les douze questions auxquelles la social data répond mieux qu'une étude, les données que chacune demande et ce qu'elle ne dit pas."),
    "diagnostic.html": ("Diagnostic social data | Licter",
                        "Un diagnostic indépendant de votre dispositif social data : audit, score de maturité sur six dimensions, gains rapides et feuille de route en deux à trois semaines."),
    "book-a-meeting.html": ("Prendre rendez-vous avec un consultant | Licter",
                            "Trente minutes avec un consultant Licter : décrivez votre décision, et voyez ce que la social data peut vous dire, et ce qu'elle ne peut pas dire."),
    "events.html": ("Événements : nos études sectorielles en présentiel | Licter",
                    "Nous présentons ce que la conversation dit d'un secteur, avec les marques qui y travaillent. Sur inscription, à Paris."),
    "event-toys-games.html": ("Étude sectorielle Jeux & jouets, 16 octobre 2026 | Licter",
                              "Notre étude sectorielle : ce que parents, enfants et collectionneurs publient, cherchent et demandent à l'IA sur les jeux et jouets. À Paris, sur inscription."),
    "event-luxury.html": ("Étude sectorielle Luxe, 3 novembre 2026 | Licter",
                          "Notre étude sectorielle : comment le désir d'une maison se construit en ligne, qui le porte, et ce que clients et curieux disent vraiment. À Paris, sur inscription."),
    "event-food.html": ("Étude sectorielle Alimentation, 19 novembre 2026 | Licter",
                        "Notre étude sectorielle : ce que les consommateurs publient, cherchent et demandent à l'IA sur ce qu'ils mangent, et les attentes que les marques peuvent saisir."),
    "legal.html": ("Mentions légales | Licter",
                   "Mentions légales du site Licter : éditeur (Licter SAS, RCS Paris 915 259 394), hébergeur, conditions d'utilisation et propriété intellectuelle."),
    "privacy.html": ("Politique de confidentialité | Licter",
                     "Comment Licter traite les données personnelles laissées sur ce site : ce que nous collectons, pourquoi, combien de temps, et vos droits."),
}
# head lines tools/build-seo.py writes again for each language
SEO_LINES = re.compile(r'\n<link rel="canonical"[^>]*>|\n<link rel="alternate" hreflang="[^"]*"[^>]*>|\n<meta property="og:url"[^>]*>'
                       r'|\n<meta property="og:image" content="[^"]*/og/p-[^"]*" />\n<meta property="og:image:width"[^>]*>\n<meta property="og:image:height"[^>]*>')


def html_tag(lang, fr_url, en_file):
    return '<html lang="%s" data-i18n-static data-alt-fr="%s" data-alt-en="/%s">' % (lang, fr_url, en_file)


def main():
    for en_file, fr_url in U.PAGE_FR.items():
        p = ROOT / en_file
        en = p.read_text()
        en = re.sub(r"<html[^>]*>", html_tag("en", fr_url, en_file), en, count=1)
        en = SEO_LINES.sub("", en)
        p.write_text(en)

        title, desc = HEAD[en_file]
        t, d = html.escape(U.typo(title, U.FR)), html.escape(U.typo(desc, U.FR))
        fr = re.sub(r"<html[^>]*>", html_tag("fr", fr_url, en_file), en, count=1)
        fr = re.sub(r"<title>.*?</title>", "<title>%s</title>" % t, fr, count=1, flags=re.S)
        for pat, val in ((r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % d),
                         (r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % t),
                         (r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % d),
                         (r'<meta name="twitter:title" content="[^"]*" />', '<meta name="twitter:title" content="%s" />' % t),
                         (r'<meta name="twitter:description" content="[^"]*" />', '<meta name="twitter:description" content="%s" />' % d)):
            fr = re.sub(pat, val, fr, count=1)
        # the page now lives one folder down: every relative URL becomes absolute
        fr = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', r'\1="/\2"', fr)
        fr = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="%s"' % ", ".join(
            (q if q.startswith(("/", "http")) else "/" + q) for q in (y.strip() for y in m.group(1).split(","))), fr)
        b0, b1 = fr.index("<body"), fr.index("</body>")
        fr = fr[:b0] + U.translate(fr[b0:b1]).replace(">Skip to content<", ">Aller au contenu<") + fr[b1:]
        out = ROOT / fr_url.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("<!-- Generated by tools/build-fr-pages.py from /%s: edit that page. -->\n" % en_file + fr)
    print("French twins: %s" % ", ".join(U.PAGE_FR.values()))


if __name__ == "__main__":
    main()
