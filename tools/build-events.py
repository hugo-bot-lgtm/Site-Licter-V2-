#!/usr/bin/env python3
"""Events: the banner at the top of every page, and one registration page
per event.

    python3 tools/build-events.py

To add an event, add it to EVENTS below (in date order) and run the build
(tools/build-usecases.py runs this first). The script writes:
  - event-<slug>.html, a registration page per event, and events.html;
  - js/events.js, the list the banner reads in the browser: as soon as an
    event's day is over, the banner moves on to the next one by itself;
  - the banner of every root page (and of offers.html, which the generated
    pages copy), set to the next event as of today, so the first paint is
    already right;
  - the French of all of it, in a block of js/fr.js ("event pages").

Past events stay in the list (their page says the event has taken place).
When there is no upcoming event, the banner goes back to the free guide.

MOCK: the registration form sends nothing yet (wire it to the CRM in
js/events.js); the programmes, times and addresses are to be confirmed.
"""
import datetime, html, importlib.util, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bo", ROOT / "tools" / "build-offers.py")
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
U = O.U
FR, EN = 0, 1
SITE = O.SITE
t, a = O.t, O.a

# ------------------------------------------------------------------ events
EVENTS = [
    {
        "slug": "toys-games", "date": "2026-10-16",
        "sector": ("Jeux & jouets", "Toys & games"),
        "venue": "Musée de la Vie romantique", "address": "16 rue Chaptal, 75009 Paris",
        "h1": ("Jeux & jouets : ce que la conversation dit du secteur.", "Toys & games: what the conversation says about the sector."),
        "lead": ("Nous présentons notre étude sectorielle : ce que parents, enfants et collectionneurs publient, recherchent et demandent à l'IA sur les jeux et les jouets, et ce que les marques peuvent en tirer avant les fêtes.",
                 "Our sector study: what parents, children and collectors post, search and ask AI about toys and games, and what brands can make of it before the holidays."),
        "points": [("Qui achète, et qui prescrit : parents, grands-parents, créateurs de contenu.", "Who buys, and who recommends: parents, grandparents, content creators."),
                   ("Les tendances qui montent sur TikTok et YouTube, et celles qui retombent.", "The trends rising on TikTok and YouTube, and the ones fading."),
                   ("Ce que les avis disent des prix, de la qualité et de la durabilité.", "What reviews say about price, quality and durability.")],
    },
    {
        "slug": "luxury", "date": "2026-11-03",
        "sector": ("Luxe", "Luxury"),
        "venue": "Ladurée Champs-Élysées", "address": "75 avenue des Champs-Élysées, 75008 Paris",
        "h1": ("Luxe : ce que la conversation dit des maisons.", "Luxury: what the conversation says about the houses."),
        "lead": ("Nous présentons notre étude sectorielle : comment se construit le désir d'une maison en ligne, qui le porte, et ce que les clients et les curieux disent vraiment des prix, des créations et de l'expérience.",
                 "Our sector study: how desire for a house is built online, who carries it, and what clients and onlookers say about prices, creations and experience."),
        "points": [("Créateurs, ambassadeurs, clients : qui fait vraiment parler d'une maison.", "Creators, ambassadors, clients: who really gets a house talked about."),
                   ("La seconde main et la revente, dans la conversation.", "Resale and second hand, in the conversation."),
                   ("Ce que les audiences internationales disent, dans leur langue.", "What international audiences say, in their own language.")],
    },
    {
        "slug": "food", "date": "2026-11-19",
        "sector": ("Food", "Food"),
        "venue": "Madame Rêve", "address": "48 rue du Louvre, 75001 Paris",
        "h1": ("Food : ce que la conversation dit de nos assiettes.", "Food: what the conversation says about what we eat."),
        "lead": ("Nous présentons notre étude sectorielle : ce que les consommateurs publient, recherchent et demandent à l'IA sur ce qu'ils mangent, et les attentes que les marques peuvent encore saisir.",
                 "We present our sector study: what consumers post, search and ask AI about what they eat, and the expectations brands can still take up."),
        "points": [("Les recettes et les créateurs qui font vendre.", "The recipes and creators that drive sales."),
                   ("Prix, santé, origine : ce qui pèse vraiment dans le choix.", "Price, health, origin: what really weighs in the choice."),
                   ("Les besoins non couverts que révèlent les recherches.", "The unmet needs that searches reveal.")],
    },
]

MONTHS = (["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
          ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
ABBR = (["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
DAYS = (["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

S = {
    "kicker": ("Étude sectorielle", "Sector study"),
    "events": ("Événements", "Events"),
    "home": ("Accueil", "Home"),
    "crumbs": ("Fil d'Ariane", "Breadcrumb"),
    "register": ("S'inscrire", "Register"),
    "hear_t": ("Ce que vous y entendrez", "What you will hear"),
    "more_t": ("Nos autres études sectorielles", "Our other sector studies"),
    "practical": ("Infos pratiques", "Practical details"),
    "when": ("Quand", "When"),
    "where": ("Où", "Where"),
    "time": ("Horaire", "Time"),
    "time_v": ("Précisé dans l'e-mail de confirmation", "Given in the confirmation email"),
    "entry": ("Entrée", "Entry"),
    "entry_v": ("Sur inscription, places limitées", "On registration, limited seats"),
    "map": ("Voir le plan", "See the map"),
    "form_t": ("Inscription", "Registration"),
    "first": ("Prénom", "First name"),
    "last": ("Nom", "Last name"),
    "company": ("Société", "Company"),
    "email": ("E-mail professionnel", "Work email"),
    "submit": ("M'inscrire", "Register"),
    "reserve": ("Inscription sous réserve de confirmation et de places disponibles. Votre place n'est pas garantie avant notre confirmation par e-mail.",
                "Registration is subject to confirmation and availability. Your seat is not guaranteed until we confirm it by email."),
    "consent": ("Vos coordonnées servent uniquement à gérer votre inscription.", "We use your details only to manage your registration."),
    "privacy": ("Politique de confidentialité", "Privacy policy"),
    "err": ("Remplissez les quatre champs, avec un e-mail valide.", "Fill in all four fields, with a valid email."),
    "list_h1": ("Nos études sectorielles, présentées en personne.", "Our sector studies, presented in person."),
    "list_lead": ("Nous présentons ce que la conversation dit d'un secteur, avec les marques qui y travaillent. Sur inscription, à Paris.",
                  "We present what the conversation says about a sector, with the brands that work in it. On registration, in Paris."),
    "upcoming": ("À venir", "Upcoming"),
    "all": ("Tous les événements", "All events"),
}


def iso(e):
    return datetime.date.fromisoformat(e["date"])


def long_date(e, lang):
    d = iso(e)
    s = "%s %d %s %d" % (DAYS[lang][d.weekday()], d.day, MONTHS[lang][d.month - 1], d.year)
    return s[:1].upper() + s[1:]


def short_date(e, lang):
    d = iso(e)
    s = "%s %d %s" % (DAYS[lang][d.weekday()], d.day, MONTHS[lang][d.month - 1])
    return s[:1].upper() + s[1:]


def file(e):
    return "event-%s.html" % e["slug"]


def next_event(today=None):
    today = today or datetime.date.today()
    return next((e for e in EVENTS if iso(e) >= today), None)


# ------------------------------------------------------------------ banner
def banner_html(e):
    if not e:
        return ('<aside class="banner" aria-label="Free guide"><a class="banner__a" href="/guide.html">\n'
                '  <b>Free guide.</b> <span>The 12 questions social data answers better than a survey</span> →\n</a></aside>')
    kicker = (S["kicker"][FR] + " · " + e["sector"][FR], S["kicker"][EN] + " · " + e["sector"][EN])
    when = (short_date(e, FR) + " · " + e["venue"], short_date(e, EN) + " · " + e["venue"])
    return ('<aside class="banner banner--event" aria-label="%s"><a class="banner__a" href="/%s">\n'
            '  <i class="banner__tag">%s</i> <b>%s</b> <span>%s</span> <u>%s <span aria-hidden="true">→</span></u>\n</a></aside>') % (
        a(("Prochain événement", "Next event")), file(e), t(("Prochain événement", "Next event")), t(kicker), t(when), t(S["register"]))


BANNER = re.compile(r'<aside class="banner(?: banner--event)?"[^>]*>.*?</aside>', re.S)


def set_banners(e):
    tag = banner_html(e)
    n = 0
    for p in sorted(ROOT.glob("*.html")) + [ROOT / "tools" / "article-shell.html"]:
        if p.name in ("use-cases.html",):
            continue
        s = p.read_text()
        if BANNER.search(s):
            s2 = BANNER.sub(lambda m: tag, s, count=1)
        elif p.name == "index.html":
            s2 = s.replace('<a class="skip-link" href="#content">Skip to content</a>\n',
                           '<a class="skip-link" href="#content">Skip to content</a>\n\n' + tag + '\n', 1)
        else:
            continue
        if s2 != s:
            p.write_text(s2)
            n += 1
    return n


# ------------------------------------------------------------------ pages
def crumbs(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (h, t(l)) if h else '<li aria-current="page">%s</li>' % t(l) for l, h in items)
    return '  <nav class="crumbs shell" aria-label="%s"><ol>%s</ol></nav>' % (a(S["crumbs"]), lis)


def maps(e):
    return "https://www.google.com/maps/search/?api=1&query=" + html.escape((e["venue"] + ", " + e["address"]).replace(" ", "+"))


def event_body(e):
    pts = "".join("<li>%s</li>" % t(p) for p in e["points"])
    when = (long_date(e, FR), long_date(e, EN))
    return f'''<main id="content">
{crumbs([(S["home"], "index.html"), (S["events"], "events.html"), (e["sector"], None)])}

  <!-- MOCK: the form sends nothing yet (js/events.js); wire it to the CRM. -->
  <section class="xh ev" data-ev-date="{e["date"]}">
    <div class="shell ev__grid">
      <div class="ev__copy">
        <p class="xh__kick"><span>{t(S["kicker"])}</span> · <span>{t(e["sector"])}</span></p>
        <h1 class="xh__title">{t(e["h1"])}</h1>
        <p class="xh__lead">{t(e["lead"])}</p>
        <dl class="ev__facts">
          <div><dt>{t(S["when"])}</dt><dd>{t(when)}</dd></div>
          <div><dt>{t(S["where"])}</dt><dd>{html.escape(e["venue"])}<small>{html.escape(e["address"])} · <a href="{maps(e)}" target="_blank" rel="noopener">{t(S["map"])} <span aria-hidden="true">↗</span></a></small></dd></div>
          <div><dt>{t(S["time"])}</dt><dd>{t(S["time_v"])}</dd></div>
          <div><dt>{t(S["entry"])}</dt><dd>{t(S["entry_v"])}</dd></div>
        </dl>
        <h2 class="ev__h2">{t(S["hear_t"])}</h2>
        <ul class="ev__points">{pts}</ul>
      </div>
      <div class="ev__card" id="register">
        <h2 class="ev__h2">{t(S["form_t"])}</h2>
        <p class="ev__date"><span>{t(when)}</span> · {html.escape(e["venue"])}</p>
        <form class="ev__form" novalidate>
          <div class="ev__row">
            <div><label class="fld__label" for="ev-first">{t(S["first"])}</label><input class="fld__input" id="ev-first" name="first" type="text" autocomplete="given-name" required /></div>
            <div><label class="fld__label" for="ev-last">{t(S["last"])}</label><input class="fld__input" id="ev-last" name="last" type="text" autocomplete="family-name" required /></div>
          </div>
          <label class="fld__label" for="ev-company">{t(S["company"])}</label>
          <input class="fld__input" id="ev-company" name="company" type="text" autocomplete="organization" required />
          <label class="fld__label" for="ev-email">{t(S["email"])}</label>
          <input class="fld__input" id="ev-email" name="email" type="email" autocomplete="email" required />
          <p class="fld__error" id="ev-err" hidden>{t(S["err"])}</p>
          <p class="ev__reserve">{t(S["reserve"])}</p>
          <button class="btn btn--primary ev__submit" type="submit">{t(S["submit"])} <span aria-hidden="true">→</span></button>
          <p class="consent">{t(S["consent"])} <a href="privacy.html">{t(S["privacy"])}</a>.</p>
        </form>
        <p class="ev__done" role="status" hidden></p>
      </div>
    </div>
  </section>

  <!-- each study links to the others: an event page was reached from the
       events hub only (audit of 9 October 2026) -->
  <section class="evl evl--more">
    <div class="shell">
      <h2 class="ev__h2">{t(S["more_t"])}</h2>
      <ul class="evl__list">{event_rows([x for x in EVENTS if x is not e])}</ul>
    </div>
  </section>
</main>'''


def event_rows(evs):
    return "".join(
        '<li data-ev-date="%s"><a href="%s"><span class="evl__d"><b>%d</b>%s</span>'
        '<span class="evl__t"><small>%s</small><b>%s</b><span>%s</span></span><i aria-hidden="true">→</i></a></li>' % (
            e["date"], file(e), iso(e).day, t((ABBR[FR][iso(e).month - 1], ABBR[EN][iso(e).month - 1])),
            t(S["kicker"]), t(e["sector"]), html.escape(e["venue"])) for e in evs)


def list_body():
    rows = event_rows(EVENTS)
    return f'''<main id="content">
{crumbs([(S["home"], "index.html"), (S["events"], None)])}

  <section class="xh evl">
    <div class="shell">
      <p class="xh__kick">{t(S["events"])}</p>
      <h1 class="xh__title">{t(S["list_h1"])}</h1>
      <p class="xh__lead">{t(S["list_lead"])}</p>
      <ul class="evl__list">{rows}</ul>
    </div>
  </section>
</main>'''


def ld_event(e):
    return {"@context": "https://schema.org", "@type": "Event", "name": "%s · %s" % (S["kicker"][EN], e["sector"][EN]),
            "description": e["lead"][EN], "startDate": e["date"], "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "endDate": e["date"], "inLanguage": "en", "image": [SITE + "/assets/img/og/p-%s.jpg" % file(e)[:-len(".html")]],
            "location": {"@type": "Place", "name": e["venue"], "address": postal(e["address"])},
            "organizer": U.ORG, "url": "%s/%s" % (SITE, file(e))}


def postal(a):
    """"16 rue Chaptal, 75009 Paris" as a PostalAddress"""
    street, rest = a.split(", ", 1)
    code, city = rest.split(" ", 1)
    return {"@type": "PostalAddress", "streetAddress": street, "postalCode": code, "addressLocality": city, "addressCountry": "FR"}


def write(name, title, desc, body, ld, offers_html):
    head = offers_html[:offers_html.index("</head>")]
    title, desc = html.escape(title), html.escape(desc)
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="%s" />' % desc, head)
    head = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="%s" />' % title, head)
    head = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="%s" />' % desc, head)
    head = head.replace('<meta name="twitter:card"', '<link rel="canonical" href="%s/%s" />\n<meta name="twitter:card"' % (SITE, name), 1)
    head += "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld) + "\n"
    main0, main1 = offers_html.index('<main id="content">'), offers_html.index("</main>") + len("</main>")
    shell = offers_html[offers_html.index("</head>"):main0] + "%s" + offers_html[main1:]
    shell = shell.replace('<body class="xpage">', '<body class="xpage evpage">', 1)
    (ROOT / name).write_text("<!-- Generated by tools/build-events.py: edit that file, not this one. -->\n" + head + shell % body)


# ------------------------------------------------------------------ js/events.js
def write_js():
    fr_path = {"event-toys-games.html": "/fr/evenements/jeux-jouets/", "event-luxury.html": "/fr/evenements/luxe/",
               "event-food.html": "/fr/evenements/alimentation/"}   # the French twins (tools/build-fr-pages.py)
    data = [{"href": "/" + file(e), "hrefFr": fr_path.get(file(e), "/" + file(e)), "date": e["date"],
             "k": [U.typo(S["kicker"][FR] + " · " + e["sector"][FR], FR), S["kicker"][EN] + " · " + e["sector"][EN]],
             "d": [U.typo(short_date(e, FR) + " · " + e["venue"], FR), short_date(e, EN) + " · " + e["venue"]],
             "long": [long_date(e, FR), long_date(e, EN)]} for e in EVENTS]
    js = (ROOT / "js" / "events.js").read_text()
    js = re.sub(r"(/\* events: generated by tools/build-events\.py \*/\n  var EVENTS = ).*?;\n", lambda m: m.group(1) + json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\n  ") + ";\n", js, count=1, flags=re.S)
    (ROOT / "js" / "events.js").write_text(js)


def main():
    O.NEW.clear()
    nxt = next_event()
    n = set_banners(nxt)                      # offers.html first: the generated pages copy it
    offers_html = (ROOT / "offers.html").read_text()
    # its own SEO head and language stay on offers.html (tools/build-offers.py)
    offers_html = re.sub(r"\s*<!-- seo:offers -->.*?<!-- /seo:offers -->", "", offers_html, flags=re.S)
    offers_html = re.sub(r"<html[^>]*>", '<html lang="en">', offers_html, count=1)
    offers_html = re.sub(r"\s*<!-- offers-bar -->.*?<!-- /offers-bar -->", "", offers_html, flags=re.S)
    for e in EVENTS:
        title = "%s · %s : %s | Licter" % (S["kicker"][EN], e["sector"][EN], long_date(e, EN))
        write(file(e), title.replace(" :", ":"), e["lead"][EN], event_body(e), [ld_event(e)], offers_html)
    write("events.html", "Events: our sector studies, in person | Licter", S["list_lead"][EN], list_body(), [], offers_html)
    for k in ("all", "upcoming"):
        t(S[k])
    t(("Cet événement a eu lieu.", "This event has taken place."))
    t(("Voir le prochain", "See the next one"))
    O.write_dict("event pages", "build-events.py", O.NEW)
    write_js()
    print("%d event pages + events.html written, banner set on %d pages (next: %s), %d strings in js/fr.js" % (
        len(EVENTS), n, nxt["slug"] if nxt else "none, back to the guide", len(O.NEW)))


if __name__ == "__main__":
    main()
