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
        "lead_past": ("Nous avons présenté notre étude sectorielle : ce que parents, enfants et collectionneurs publient, recherchent et demandent à l'IA sur les jeux et les jouets, et ce que les marques peuvent en tirer avant les fêtes.",
                      "We presented our sector study: what parents, children and collectors post, search and ask AI about toys and games, and what brands can make of it before the holidays."),
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
        "lead_past": ("Nous avons présenté notre étude sectorielle : comment se construit le désir d'une maison en ligne, qui le porte, et ce que les clients et les curieux disent vraiment des prix, des créations et de l'expérience.",
                      "We presented our sector study: how desire for a house is built online, who carries it, and what clients and onlookers say about prices, creations and experience."),
        "points": [("Créateurs, ambassadeurs, clients : qui fait vraiment parler d'une maison.", "Creators, ambassadors, clients: who really gets a house talked about."),
                   ("La seconde main et la revente, dans la conversation.", "Resale and second hand, in the conversation."),
                   ("Ce que les audiences internationales disent, dans leur langue.", "What international audiences say, in their own language.")],
    },
    {
        "slug": "food", "date": "2026-11-19",
        "sector": ("Alimentation", "Food"),
        "venue": "Madame Rêve", "address": "48 rue du Louvre, 75001 Paris",
        "h1": ("Alimentation : ce que la conversation dit de nos assiettes.", "Food: what the conversation says about what we eat."),
        "lead": ("Nous présentons notre étude sectorielle : ce que les consommateurs publient, recherchent et demandent à l'IA sur ce qu'ils mangent, et les attentes que les marques peuvent encore saisir.",
                 "We present our sector study: what consumers post, search and ask AI about what they eat, and the expectations brands can still take up."),
        "lead_past": ("Nous avons présenté notre étude sectorielle : ce que les consommateurs publient, recherchent et demandent à l'IA sur ce qu'ils mangent, et les attentes que les marques pouvaient encore saisir.",
                      "We presented our sector study: what consumers post, search and ask AI about what they eat, and the expectations brands could still take up."),
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
    "heard_t": ("Au programme de l'étude", "The study's programme"),
    "over_v": ("Événement terminé", "Event over"),
    "kicker_past": ("Étude sectorielle · a eu lieu", "Sector study · took place"),
    "closed_t": ("Inscriptions closes", "Registration closed"),
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
    "consent_club": ("Vos coordonnées servent uniquement à traiter votre demande d'adhésion.", "We use your details only to handle your membership request."),
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


def past(e, today=None):
    """the event's day is over: the page is written in its past state, so the
    HTML read by search engines and AI never announces it as upcoming (the
    browser script did it alone until 19 October 2026)"""
    return iso(e) < (today or datetime.date.today())


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
    # the shells too: the tool and network pages kept a past event (audit of 19 October 2026)
    for p in sorted(ROOT.glob("*.html")) + [ROOT / "tools" / "article-shell.html", ROOT / "tools" / "tech-shell.html"]:
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


def past_card(e):
    nxt = next_event()
    # two elements: the French twin translates text node by text node
    more = ('<a href="%s"><span>%s</span> <b>%s</b> <span aria-hidden="true">→</span></a>' % (
        file(nxt), t(("Voir le prochain :", "See the next one:")), t((S["kicker"][FR] + " · " + nxt["sector"][FR], S["kicker"][EN] + " · " + nxt["sector"][EN])))) if nxt else ""
    return '<p class="ev__done is-past"><span>%s</span> %s</p>' % (t(("Cet événement a eu lieu.", "This event has taken place.")), more)


def event_body(e):
    pts = "".join("<li>%s</li>" % t(p) for p in e["points"])
    when = (long_date(e, FR), long_date(e, EN))
    gone = past(e)
    entry = t(S["over_v"] if gone else S["entry_v"])
    hear = S["heard_t"] if gone else S["hear_t"]
    hour = "" if gone else '\n          <div><dt>%s</dt><dd>%s</dd></div>' % (t(S["time"]), t(S["time_v"]))
    if gone:
        card = """      <div class="ev__card" id="register">
        <h2 class="ev__h2">%s</h2>
        <p class="ev__date"><span>%s</span> · %s</p>
        %s
      </div>""" % (t(S["closed_t"]), t(when), html.escape(e["venue"]), past_card(e))
    else:
        card = f'''      <div class="ev__card" id="register">
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
      </div>'''
    return f'''<main id="content">
{crumbs([(S["home"], "index.html"), (S["events"], "events.html"), (e["sector"], None)])}

  <!-- MOCK: the form sends nothing yet (js/events.js); wire it to the CRM. -->
  <section class="xh ev" data-ev-date="{e["date"]}">
    <div class="shell ev__grid">
      <div class="ev__copy">
        <p class="xh__kick"><span>{t(S["kicker"])}</span> · <span>{t(e["sector"])}</span></p>
        <h1 class="xh__title">{t(e["h1"])}</h1>
        <p class="xh__lead">{t(e["lead_past"] if gone else e["lead"])}</p>
        <dl class="ev__facts">
          <div><dt>{t(S["when"])}</dt><dd>{t(when)}</dd></div>
          <div><dt>{t(S["where"])}</dt><dd>{html.escape(e["venue"])}<small>{html.escape(e["address"])} · <a href="{maps(e)}" target="_blank" rel="noopener">{t(S["map"])} <span aria-hidden="true">↗</span></a></small></dd></div>{hour}
          <div><dt>{t(S["entry"])}</dt><dd>{entry}</dd></div>
        </dl>
        <h2 class="ev__h2">{t(hear)}</h2>
        <ul class="ev__points">{pts}</ul>
      </div>
{card}
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
        '<li data-ev-date="%s"%s><a href="%s"><span class="evl__d"><b>%d</b>%s</span>'
        '<span class="evl__t"><small>%s</small><b>%s</b><span>%s</span></span><i aria-hidden="true">→</i></a></li>' % (
            e["date"], ' class="is-past"' if past(e) else "", file(e), iso(e).day, t((ABBR[FR][iso(e).month - 1], ABBR[EN][iso(e).month - 1])),
            t(S["kicker_past"] if past(e) else S["kicker"]), t(e["sector"]), html.escape(e["venue"])) for e in evs)


def list_body():
    # what is coming first, then what has taken place
    rows = event_rows([e for e in EVENTS if not past(e)] + [e for e in EVENTS if past(e)])
    # the dates in a sentence as well: a list of links alone was dropped by text
    # extractors, the page read as 26 words (audit of 13 October 2026)
    up = [e for e in EVENTS if iso(e) >= datetime.date.today()]
    def say(lang):
        items = ["%s, %s, %s" % (e["sector"][lang], (long_date(e, lang)[0].lower() + long_date(e, lang)[1:]) if lang == FR else long_date(e, lang), e["venue"]) for e in up]
        return ((" ; " if lang == FR else "; ").join(items) + ".") if items else ""
    # two text nodes: the French twin is made by translating each node (tools/build-fr-pages.py)
    agenda = ('\n      <p class="evl__agenda"><b>%s</b> <span>%s</span></p>' % (t(("Au programme :", "Coming up:")), t((say(FR), say(EN))))) if up else ""
    return f'''<main id="content">
{crumbs([(S["home"], "index.html"), (S["events"], None)])}

  <section class="xh evl">
    <div class="shell">
      <p class="xh__kick">{t(S["events"])}</p>
      <h1 class="xh__title">{t(S["list_h1"])}</h1>
      <p class="xh__lead">{t(S["list_lead"])}</p>
      <ul class="evl__list">{rows}</ul>{agenda}
      <p class="evl__agenda evl__club"><b>{t(CLUB["hub"])}</b> <a href="{CLUB["file"]}">{t(CLUB["hub_link"])} <span aria-hidden="true">→</span></a></p>
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


# ------------------------------------------------------------------ the Luxury Social Club
# The club's page and its membership form (owner request, 2 November 2026): the
# event page's layout, the Social Intelligence Club's fields. Requests leave as
# action "club" (js/events.js, api/lead.js), to Anaïs and Victor.
CLUB = {
    "file": "luxury-social-club.html",
    "kicker": ("Luxury Social Club", "Luxury Social Club"),
    "h1": ("Ce qui se dit ici n'est pas encore sur LinkedIn.", "What is said here is not on LinkedIn yet."),
    "lead": ("Le Luxury Social Club réunit les experts de la social intelligence et de la data. IA, outils, méthodes, signaux faibles : on y parle des avancées du métier avant qu'elles ne deviennent des slides de conférence.",
             "The Luxury Social Club brings together social intelligence and data experts. AI, tools, methods, weak signals: we discuss where the field is going before it turns into conference slides."),
    "facts": [(("Pour qui", "Who for"), ("Les experts de la social intelligence et de la data", "Social intelligence and data experts"),
               ("Marques, agences, éditeurs d'outils, conseil, recherche", "Brands, agencies, tool makers, consultants, researchers")),
              (("Format", "Format"), ("En petit comité", "Small groups"), ("Des échanges entre pairs, sans pitch commercial", "Peer conversations, no sales pitch")),
              (("Entrée", "Entry"), ("Sur demande", "On request"), ("Chaque profil est relu par l'équipe du club", "Every profile is read by the club's team")),
              (("Prochaine rencontre", "Next meeting"), ("Annoncée aux membres", "Announced to members"), ("Par e-mail, une fois l'adhésion validée", "By email, once membership is confirmed"))],
    "hear_t": ("Ce qu'on s'y dit", "What gets discussed"),
    "points": [("Les IA qui changent vraiment la lecture des réseaux, et celles qui font surtout du bruit.", "The AI that really changes how social media is read, and the AI that mostly makes noise."),
               ("Les méthodes que les meilleures équipes gardent pour elles.", "The methods the best teams keep to themselves."),
               ("Les signaux faibles qui annoncent la prochaine crise, ou la prochaine tendance.", "The weak signals that announce the next crisis, or the next trend."),
               ("Ce qui marche et ce qui ne marche pas : des retours d'expérience sans langue de bois.", "What works and what does not: field experience, no spin.")],
    "why_t": ("Pourquoi le rejoindre", "Why join"),
    "why": [(("Un réseau de pairs", "A network of peers"), ("Ceux qui font la social intelligence, côté marques, agences, outils et recherche.", "The people who do social intelligence, at brands, agencies, tool makers and research labs.")),
            (("Une longueur d'avance", "A head start"), ("Les sujets qui comptent, discutés avant d'être partout.", "The topics that matter, discussed before they are everywhere.")),
            (("Des échanges sans filtre", "Unfiltered conversations"), ("Entre experts, en confiance, loin des démonstrations commerciales.", "Between experts, in confidence, far from sales demos."))],
    "form_t": ("Demande d'adhésion", "Membership request"),
    "form_sub": ("Luxury Social Club · Adhésion sur validation", "Luxury Social Club · Membership subject to approval"),
    "fields": [("first", ("Prénom", "First name"), "given-name"), ("last", ("Nom", "Last name"), "family-name"),
               ("company", ("Société", "Company"), "organization"), ("role", ("Fonction", "Job title"), "organization-title")],
    "profile": ("Vous êtes", "You are"),
    "profile_ph": ("Choisissez votre profil", "Choose your profile"),
    "profiles": [("Annonceur ou marque", "Advertiser or brand"), ("Agence de communication ou de marketing", "Communication or marketing agency"),
                 ("Plateforme ou éditeur d'outil de social listening", "Social listening platform or tool maker"), ("Cabinet de conseil ou freelance", "Consultancy or freelance"),
                 ("Université ou institut de recherche", "University or research institute"), ("Étudiant ou professionnel en reconversion", "Student or career changer")],
    "email": ("E-mail professionnel", "Work email"),
    "expect": ("Ce que vous attendez du club (facultatif)", "What you expect from the club (optional)"),
    "err": ("Remplissez tous les champs obligatoires, avec un e-mail valide.", "Fill in all required fields, with a valid email."),
    "reserve": ("Chaque demande est relue par l'équipe du club. Nous vous répondons par e-mail.", "Every request is read by the club's team. We reply by email."),
    "submit": ("Demander à rejoindre", "Request to join"),
    "consent": ("Vos coordonnées servent uniquement à traiter votre demande d'adhésion.", "We use your details only to handle your membership request."),
    "title": ("Luxury Social Club : le cercle des experts de la social intelligence | Licter", "Luxury Social Club: the circle of social intelligence experts | Licter"),
    "desc": ("Le club des experts de la social intelligence et de la data : IA, outils, méthodes et signaux faibles, discutés entre pairs. Entrée sur demande.",
             "The club of social intelligence and data experts: AI, tools, methods and weak signals, discussed among peers. Entry on request."),
    "hub": ("Le Luxury Social Club : le cercle des experts de la social intelligence.", "The Luxury Social Club: the circle of social intelligence experts."),
    "hub_link": ("Demander à rejoindre", "Request to join"),
}


def club_body():
    c = CLUB
    facts = "".join('<div><dt>%s</dt><dd>%s<small>%s</small></dd></div>' % (t(k), t(v), t(n)) for k, v, n in c["facts"])
    pts = "".join("<li>%s</li>" % t(x) for x in c["points"])
    why = "".join('<li><b>%s</b> <span>%s</span></li>' % (t(h), t(x)) for h, x in c["why"])
    def fld(name, lab, auto):
        return ('<div><label class="fld__label" for="lsc-%s">%s</label><input class="fld__input" id="lsc-%s" name="%s" type="text" autocomplete="%s" required /></div>' % (
            name, t(lab), name, name, auto))
    f = c["fields"]
    opts = "".join('<option>%s</option>' % t(o) for o in c["profiles"])
    return f'''<main id="content">
{crumbs([(S["home"], "index.html"), (S["events"], "events.html"), (c["kicker"], None)])}

  <section class="xh ev lsc">
    <div class="shell ev__grid">
      <div class="ev__copy">
        <p class="xh__kick"><span>{t(c["kicker"])}</span></p>
        <h1 class="xh__title">{t(c["h1"])}</h1>
        <p class="xh__lead">{t(c["lead"])}</p>
        <a class="btn btn--primary xe-lmh__jump" href="#rejoindre">{t(c["submit"])} <span aria-hidden="true">↓</span></a>
        <dl class="ev__facts">{facts}</dl>
        <h2 class="ev__h2">{t(c["hear_t"])}</h2>
        <ul class="ev__points">{pts}</ul>
        <h2 class="ev__h2">{t(c["why_t"])}</h2>
        <ul class="ev__points lsc__why">{why}</ul>
      </div>
      <div class="ev__card" id="rejoindre">
        <h2 class="ev__h2">{t(c["form_t"])}</h2>
        <p class="ev__date"><span>{t(c["form_sub"])}</span></p>
        <form class="ev__form" data-club novalidate>
          <div class="ev__row">{fld(*f[0])}{fld(*f[1])}</div>
          <div class="ev__row">{fld(*f[2])}{fld(*f[3])}</div>
          <label class="fld__label" for="lsc-profile">{t(c["profile"])}</label>
          <select class="fld__input" id="lsc-profile" name="profile" required><option value="">{t(c["profile_ph"])}</option>{opts}</select>
          <label class="fld__label" for="lsc-email">{t(c["email"])}</label>
          <input class="fld__input" id="lsc-email" name="email" type="email" autocomplete="email" required />
          <label class="fld__label" for="lsc-expect">{t(c["expect"])}</label>
          <textarea class="fld__input" id="lsc-expect" name="expect" rows="3"></textarea>
          <p class="fld__error" id="lsc-err" role="alert" hidden>{t(c["err"])}</p>
          <p class="ev__reserve">{t(c["reserve"])}</p>
          <button class="btn btn--primary ev__submit" type="submit">{t(c["submit"])} <span aria-hidden="true">→</span></button>
          <p class="consent">{t(S["consent_club"])} <a href="privacy.html">{t(S["privacy"])}</a>.</p>
        </form>
        <p class="ev__done" role="status" hidden></p>
      </div>
    </div>
  </section>
</main>'''


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
    write(CLUB["file"], CLUB["title"][EN], CLUB["desc"][EN], club_body(), [], offers_html)
    for k in ("title", "desc"):          # the French head comes from tools/build-fr-pages.py; the strings stay registered
        t(CLUB[k])
    for e in EVENTS:      # both tenses in js/fr.js, whatever the date of the build
        t(e["lead"]); t(e["lead_past"])
    for k in ("all", "upcoming", "time", "time_v", "entry_v", "hear_t", "heard_t", "form_t", "closed_t", "kicker_past", "over_v"):
        t(S[k])
    t(("Cet événement a eu lieu.", "This event has taken place."))
    t(("Voir le prochain", "See the next one"))
    O.write_dict("event pages", "build-events.py", O.NEW)
    write_js()
    print("%d event pages + events.html written, banner set on %d pages (next: %s), %d strings in js/fr.js" % (
        len(EVENTS), n, nxt["slug"] if nxt else "none, back to the guide", len(O.NEW)))


if __name__ == "__main__":
    main()
