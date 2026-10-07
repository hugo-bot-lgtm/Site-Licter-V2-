#!/usr/bin/env python3
"""One-off: brings the articles of the former Webflow site (www.licter.com/article/...)
into tools/blog_articles.json, in French, with their images saved under
assets/img/blog/ and their YouTube videos as play cards.

    python3 tools/migrate-webflow-articles.py <folder of saved Webflow pages>

The folder holds the pages saved as article__<slug>.html. Run it once; after
that, edit tools/blog_articles.json and run tools/build-blog.py.
"""
import datetime, html, io, json, pathlib, re, subprocess, sys
from bs4 import BeautifulSoup, NavigableString, Comment
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1])
BANNED = {"l-OevQ4q8js"}            # never on the site (Paris 2024, C. Legall)
SKIP = {"surveiller-les-jeux-olympiques-lart-de-la-veille-et-de-la-gestion-de-crise",   # the write-up of that same interview
        "choisir-outil-social-listening"}   # a page around one video, now private on YouTube
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

THREAD = {
    "listening": "MONITORING & SOCIAL LISTENING", "insights": "CONSUMER INSIGHTS",
    "foresight": "SOCIAL DATA & FORESIGHT", "influence": "INFLUENCE"}
PLAN = {  # old slug: (thread, related use-case keys)
    "analyser-les-succes-publicitaire-en-moins-d1h-spotlight-1-licter-x-petit-bateau": ("insights", ["campaign", "messaging"]),
    "axa-x-licter-gerer-une-crise-cest-dabord-lanticiper": ("listening", ["crisis", "reputation"]),
    "choisir-outil-social-listening": ("listening", ["reputation", "crisis"]),
    "comment-conquerir-le-marche-de-la-cosmetique-de-luxe-grace-au-social-listening": ("insights", ["market", "segmentation"]),
    "comment-creer-une-social-listening-squad-pour-doubler-ladoption-de-votre-outil": ("listening", ["reputation", "stakeholders"]),
    "comment-doubler-limpact-de-votre-strategie-social-listening-en-6-mois": ("listening", ["reputation", "market"]),
    "comment-france-digitale-juge-lefficacite-de-ses-actions-de-communication": ("insights", ["campaign", "messaging"]),
    "comment-loreal-utilise-le-social-listening-pour-capter-la-voix-du-consommateur": ("insights", ["expectations", "product"]),
    "comment-orange-analyse-tiktok-grace-au-social-listening": ("insights", ["younger", "segmentation"]),
    "comment-origins-associe-influence-et-technologie-pour-transformer-le-capital-risque-2": ("influence", ["ambassadors", "leaders"]),
    "departs-de-x-quels-reseaux-sociaux-peuvent-rivaliser-avec-la-plateforme-delon-musk": ("foresight", ["stakeholders", "market"]),
    "gp-explorer-3-squeezie-bat-les-records-daudience": ("influence", ["ambassadors", "campaign"]),
    "identifier-les-breaking-news-de-votre-secteur-comment-rester-informe-en-temps-reel": ("listening", ["crisis", "stakeholders"]),
    "la-consommation-devient-un-acte-militant-les-insights-de-kantar-sur-les-tendances-dachat": ("foresight", ["market", "expectations"]),
    "licter-lvmh": ("influence", ["leaders", "reputation"]),
    "licter-meltwater": ("listening", ["reputation", "crisis"]),
    "licter-talkwalker-podcast": ("listening", ["reputation", "market"]),
    "licter-visibrain-podcast": ("listening", ["crisis", "reputation"]),
    "social-intelligence-insider-50": ("foresight", ["stakeholders", "market"]),
    "social-listening-et-politique-comment-capter-la-voix-des-citoyens": ("foresight", ["stakeholders", "leaders"]),
    "veille-social-listening-2024": ("foresight", ["market", "reputation"]),
    "veiller-lactivite-digitale-autour-de-votre-marque": ("listening", ["reputation", "crisis"]),
    "le-bad-buss-huda-beauty-decrypte": ("listening", ["crisis", "ambassadors"]),
    "shein-vs-bhv-dissection-d-une-crise-digitale-a-travers-la-social-data-intelligence": ("listening", ["crisis", "reputation"]),
}
RENAME = {"le-bad-buss-huda-beauty-decrypte": "le-bad-buzz-huda-beauty-decrypte"}
DATES = {  # pages without a dated share image: the date is read from the story
    "shein-vs-bhv-dissection-d-une-crise-digitale-a-travers-la-social-data-intelligence": datetime.date(2025, 12, 2)}
FIX = [("bad buss", "bad buzz"), ("succès publicitaire en", "succès publicitaires en"), ("Départs de X\u00a0: Quels", "Départs de X\u00a0: quels"),
       ("militant\u00a0: Les insights", "militant\u00a0: les insights"), ("en 2024.", "en 2024"),
       ("Shein vs BHV", "Shein vs BHV\u00a0: dissection d'une crise digitale")]
EDITS = [  # typos and a placeholder left in the original texts (regex, replacement)
    # what the guests say of themselves in the interviews (podcast transcripts)
    (r"le COO de Visibrain", "Jean-Christophe Gatuingt, cofondateur de Visibrain"),
    (r"la DG France de Talkwalker", "Charlotte, qui a ouvert le bureau parisien de Talkwalker"),
    (r"Sur Tik Tok[\s\u00a0]*:[\s\u00a0]*9K mentions</strong>, qui correspond à une augmentation de XX%, un 1e p<strong>ic",
     "Sur TikTok\u00a0: 9K mentions</strong>, un premier <strong>pic"),
    (r"la “crise'”Huda", "la «\u00a0crise\u00a0» Huda"),
    # words glued together in the original Kantar article
    (r"Audience Firts", "Audience First"),
    (r"en nous avons pu discuter", "et nous avons pu discuter"),
    (r"<li>Ce qu'elle pense de <a [^>]*>Licter</a>[^<]*</li>", ""),
    (r" d'une heure(?= avec| d'| de )", ""), (r"avons eule plaisir", "avons eu le plaisir"), (r"insightsstratégiques", "insights stratégiques"),
    (r"30 ansd’expérience", "30 ans d’expérience"), (r"àl'inflation", "à l'inflation"), (r"grandestransformations", "grandes transformations"),
    (r"articleexplore", "article explore"), (r"descircuits", "des circuits"),
]
UC = {  # key: (French path, English path, French label)
    "reputation": ("/fr/cas-usage/sante-de-marque/e-reputation-image-de-marque/", "/en/use-cases/brand-health/brand-reputation-monitoring/", "Surveiller l'image et la réputation de votre marque"),
    "crisis": ("/fr/cas-usage/sante-de-marque/risques-de-marque-crise/", "/en/use-cases/brand-health/brand-risk-crisis/", "Identifier et désamorcer les risques de marque"),
    "messaging": ("/fr/cas-usage/sante-de-marque/discours-de-marque/", "/en/use-cases/brand-health/brand-messaging/", "Affiner le discours de votre marque"),
    "campaign": ("/fr/cas-usage/communication/mesurer-impact-campagne/", "/en/use-cases/communication/measure-campaign-impact/", "Mesurer l'impact d'une campagne"),
    "ambassadors": ("/fr/cas-usage/communication/identifier-ambassadeurs/", "/en/use-cases/communication/find-brand-ambassadors/", "Identifier les bons ambassadeurs"),
    "leaders": ("/fr/cas-usage/communication/prise-de-parole-dirigeants/", "/en/use-cases/communication/leader-advocacy/", "Construire la prise de parole des dirigeants"),
    "segmentation": ("/fr/cas-usage/audiences/segmentation-cibles/", "/en/use-cases/audiences/audience-segmentation/", "Segmenter vos cibles"),
    "expectations": ("/fr/cas-usage/audiences/parcours-client-attentes/", "/en/use-cases/audiences/customer-expectations-touchpoints/", "Comprendre les attentes de vos clients"),
    "younger": ("/fr/cas-usage/audiences/rajeunir-audience/", "/en/use-cases/audiences/reach-younger-audiences/", "Toucher une audience plus jeune"),
    "market": ("/fr/cas-usage/tendances-innovation/analyse-marche-opportunites/", "/en/use-cases/trends-innovation/market-opportunities/", "Analyser un marché et ses opportunités"),
    "product": ("/fr/cas-usage/tendances-innovation/tester-evaluer-produits/", "/en/use-cases/trends-innovation/product-testing/", "Tester et évaluer vos produits"),
    "stakeholders": ("/fr/cas-usage/tendances-innovation/cartographie-parties-prenantes-tendances/", "/en/use-cases/trends-innovation/stakeholder-trend-mapping/", "Cartographier parties prenantes et tendances"),
}
AVATAR = {"Antoine Khaitrine": "assets/img/team/founder-antoine-160.webp", "Adrien Krebs": "assets/img/team/founder-adrien-160.webp",
          "Mina Cantone": "assets/img/team/morning/mina-face-160.webp"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆↔-⇿️‍​]")
NBSP = " "


def typo(s):
    """French typography: no em or en dashes, non-breaking spaces before : ; ! ? and inside « »"""
    s = EMOJI.sub("", s).replace("\u2028", " ")
    s = re.sub(r"d['’](?:1|A)H\b", "d'une heure", s).replace("( ", "(").replace(" )", ")")
    s = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1-\2", s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    s = re.sub(r"[  ]+([:;!?»])", NBSP + r"\1", s)
    s = re.sub(r"«[  ]*", "«" + NBSP, s)
    s = re.sub(r"(\d) %", r"\1" + NBSP + "%", s)
    return s


def save_image(url, slug, n):
    folder = ROOT / "assets" / "img" / "blog" / slug[:40]
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / ("%d.webp" % n)
    if not out.exists():
        data = subprocess.run(["curl", "-sL", "-m", "60", "-A", "Mozilla/5.0", url], capture_output=True, check=True).stdout  # curl: system certificates
        im = Image.open(io.BytesIO(data))
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=80, method=6)
    im = Image.open(out)
    return "/" + str(out.relative_to(ROOT)), im.width, im.height


def video(vid, title):
    return ('<figure class="bl-video"><a class="reel bl-video__card" href="https://www.youtube.com/watch?v=%s" data-yt="%s" target="_blank" rel="noopener" aria-label="%s">'
            '<span class="reel__shot"><img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" width="480" height="360" alt="" loading="lazy" decoding="async" />'
            '<span class="reel__play" aria-hidden="true"></span></span></a><figcaption>%s</figcaption></figure>') % (
        vid, vid, html.escape("Lire la vidéo : " + typo(title)), vid, html.escape(typo(title)))


def clean(body, slug, old_map):
    for c in body.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    n = 0
    for fig in body.find_all("figure"):
        ifr = fig.find("iframe")
        img = fig.find("img")
        if ifr:
            m = re.search(r"embed/([\w-]{11})", ifr.get("src", ""))
            if not m or m.group(1) in BANNED:
                fig.decompose(); continue
            fig.replace_with(BeautifulSoup(video(m.group(1), ifr.get("title") or "La vidéo"), "html.parser"))
        elif img and img.get("src"):
            n += 1
            src, w, h = save_image(img["src"], slug, n)
            cap = fig.find("figcaption")
            alt = typo(img.get("alt") or (cap.get_text(" ", strip=True) if cap else ""))
            new = '<figure class="bl-fig"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async" />%s</figure>' % (
                src, w, h, html.escape(alt), ("<figcaption>%s</figcaption>" % html.escape(typo(cap.get_text(" ", strip=True)))) if cap and cap.get_text(strip=True) else "")
            fig.replace_with(BeautifulSoup(new, "html.parser"))
        else:
            fig.decompose()
    CHECK = re.compile(r"^[\s\u00a0]*(?:[\u2705\u2714\u2611\U0001F449\u27A1\u2022]|-\s)")
    for p_ in body.find_all("p"):
        if p_.find_parent("ul") or not CHECK.match(p_.get_text()):
            continue
        prev = p_.find_previous_sibling()
        if prev is not None and prev.name == "ul" and prev.get("data-checks"):
            ul = prev
        else:
            ul = BeautifulSoup("", "html.parser").new_tag("ul"); ul["data-checks"] = "1"; p_.insert_before(ul)
        p_.name = "li"; ul.append(p_.extract())
    for e in body.find_all(["iframe", "script", "style"]):
        e.decompose()
    for e in body.select(".w-embed"):
        e.unwrap()
    for h in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        h.name = {"h1": "h2", "h2": "h2", "h3": "h3"}.get(h.name, "h3")
        for s in h.find_all(["strong", "b", "em"]):
            s.unwrap()
    for h in body.find_all(["h2", "h3"]):
        if re.match(r"^\s*sommaire", h.get_text(), re.I):
            nxt = h.find_next_sibling()
            if nxt is not None and nxt.name in ("ol", "ul"):
                nxt.decompose()
            h.decompose()
    first = next((c for c in body.children if getattr(c, "name", None)), None)
    if first is not None and first.name in ("h2", "h3"):
        first.name = "p"; first["class"] = "bl-dek"
    for h in body.find_all(["h2", "h3", "p"]):
        if not re.sub(r"[\s\u200b-\u200d\ufeff]+", "", h.get_text()) and not h.find(["img", "iframe", "figure"]):
            h.decompose()
    if not body.find("h2"):
        for h in body.find_all("h3"):
            h.name = "h2"
    DEAD = {"veille.licter.com": "/guide.html", "webinar.licter.com": "/events.html",
            "linkedin.licter.com": "https://www.linkedin.com/company/licter/"}   # former subdomains, all gone
    for h in body.find_all(["h2", "h3"]):
        if h.find("a") and h.get_text(strip=True).startswith("→"):   # a call to action set as a heading
            h.name = "p"
    for a in body.find_all("a"):
        if a.find_parent("figure"):
            continue
        if a.find_parent(["h2", "h3"]) or a.get("href", "#") in ("#", "") or not a.get_text(strip=True):
            a.unwrap()       # no link inside a heading, no empty or dead-end link
            continue
        for host, to in DEAD.items():
            if host in a.get("href", ""):
                a["href"] = to
        href = a.get("href", "")
        p = re.sub(r"^https?://(www\.)?licter\.com", "", href)
        if (p != href or href.startswith("/")) and href not in DEAD.values():
            a["href"] = old_map.get(p.rstrip("/") or "/", "/")
        attrs = {"href": a.get("href", "")}
        if attrs["href"].startswith("http"):
            attrs.update(target="_blank", rel="noopener")
        a.attrs = attrs
    for e in body.find_all(True):
        if e.name == "figure" or e.find_parent("figure") or "bl-dek" in (e.get("class") or []):
            continue
        if e.name in ("a", "img"):
            continue
        e.attrs = {}
    # text: French typography
    for t in body.find_all(string=True):
        if t.find_parent("figure"):
            continue
        t.replace_with(typo(str(t)))
    s = body.decode_contents()
    # "<br>- item<br>- item" paragraphs become lists
    def listify(m):
        inner = m.group(1)
        parts = [x.strip() for x in re.split(r"<br\s*/?>", inner)]
        items = [x for x in parts if re.match(r"^[-•✓]\s", x)]
        if len(items) < 2:
            return m.group(0)
        out, ul = [], []
        for x in parts:
            if re.match(r"^[-•✓]\s", x):
                ul.append("<li>%s</li>" % x[2:].strip())
            else:
                if ul:
                    out.append("<ul>%s</ul>" % "".join(ul)); ul = []
                if x:
                    out.append("<p>%s</p>" % x)
        if ul:
            out.append("<ul>%s</ul>" % "".join(ul))
        return "".join(out)
    s = re.sub(r"<p>(.*?)</p>", listify, s, flags=re.S)
    s = re.sub(r"(<br\s*/?>\s*){2,}", "</p><p>", s)
    s = re.sub(r"<li>(.*?)(<br\s*/?>\s*)+</li>", r"<li>\1</li>", s, flags=re.S)
    s = re.sub(r"<p>[\s ‍]*(<br\s*/?>)?[\s ‍]*</p>", "", s)
    s = re.sub(r"<(strong|em)>[\s ]*</\1>", "", s)
    s = s.replace("‍", "")
    s = re.sub(r"(<br\s*/?>\s*)+</(p|li|h2|h3)>", r"</\2>", s)
    s = re.sub(r"<(p|li|h2|h3)>[\s ]+", r"<\1>", s)
    s = re.sub(r"[  ]+</(p|li|h2|h3)>", r"</\1>", s)
    for a_, b_ in EDITS:
        s = re.sub(a_, b_, s)
    return s


def main():
    old_map = {o: n for o, n in json.loads((ROOT / "tools" / "redirects.json").read_text()).items()}
    arts = json.loads((ROOT / "tools" / "blog_articles.json").read_text())
    arts = [a for a in arts if a.get("lang") != "fr" or not a.get("old")]   # keeps the drafts and the articles written since
    for f in sorted(SRC.glob("article__*.html")):
        old = f.stem[len("article__"):]
        if old in SKIP:
            continue
        thread, ucs = PLAN[old]
        slug = RENAME.get(old, re.sub(r"-2$", "", old))
        s = BeautifulSoup(f.read_text(), "html.parser")
        title = typo(s.find("h1").get_text(" ", strip=True))
        for a_, b_ in FIX:
            title = title.replace(a_, b_)
        desc = s.find("meta", attrs={"name": "description"})
        lead = typo(re.sub(r"\s*\(avec un tuto vidéo\s*!?\)", "", (desc.get("content") if desc else "")).strip())
        for a_, b_ in EDITS:
            lead = re.sub(a_, b_, lead)
        og = s.find("meta", property="og:image")
        m = re.search(r"/([0-9a-f]{24})_", og.get("content", "") if og else "")
        d = DATES.get(old) or datetime.datetime.fromtimestamp(int(m.group(1)[:8], 16), datetime.timezone.utc).date()
        a = s.select_one(".hero-article-author-name")
        author = a.get_text(strip=True) if a else "Antoine Khaitrine"
        body = s.select(".w-richtext")[0]
        prose = clean(body, slug, old_map)
        if "lorem" in prose.lower():
            raise SystemExit("placeholder text in " + old)
        plain = lambda t: re.sub(r"\W+", " ", t).strip().lower()
        if len(lead) < 40 or plain(lead) in plain(title) or plain(title) in plain(lead):     # the opening of the text instead
            prose_ = re.sub(r'<p class="bl-dek">.*?</p>', "", prose)
            first = next(t for t in (re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<p>(.*?)</p>", prose_, re.S)) if len(t) > 50)
            sents = re.split(r"(?<=[.!?])\s+", first)
            lead = sents[0] if len(sents[0]) > 60 or len(sents) == 1 else " ".join(sents[:2])
        words = len(re.sub(r"<[^>]+>", " ", prose).split())
        uc = ('<aside class="uc-links" aria-labelledby="uc-links-t">\n        <p class="uc-links__k" id="uc-links-t">Cas d\'usage liés</p>\n        <ul>%s</ul>\n      </aside>') % "".join(
            '<li><a href="%s" data-en="%s">%s <span aria-hidden="true">→</span></a></li>' % (UC[k][0], UC[k][1], html.escape(typo(UC[k][2]), quote=False)) for k in ucs)
        arts.append({"file": "article-%s.html" % slug, "lang": "fr", "old": "/article/" + old, "thread": THREAD[thread],
                     "title": title, "lead": lead, "date": "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year),
                     "read": "%d min read" % max(2, round(words / 220)), "author": author, "avatar": AVATAR.get(author, AVATAR["Antoine Khaitrine"]),
                     "prose": prose, "uc": uc})
        print(slug[:60].ljust(62), d, author, words, "words")
    (ROOT / "tools" / "blog_articles.json").write_text(json.dumps(arts, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
