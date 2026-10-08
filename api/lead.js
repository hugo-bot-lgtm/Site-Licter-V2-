/* =========================================================================
   Every form of the site lands here (js/track.js, window.LicterSend), and
   leaves as one email to the team, sent with Resend from website@contact.licter.com.
   The visitor gets no email: the page shows the confirmation.

   The Resend key is the RESEND_API_KEY environment variable of the Vercel
   project (Production): it never reaches the browser.

   Body (JSON): { action, detail, title, page, lang, fields: { label: value } }
   The Social Intelligence Club has its own forms and does not use this.
   ========================================================================= */
const TEAM = [
  "anais.bremand@licter.com",
  "antoine.khaitrine@licter.com",
  "victor.phouangsavath@licter.com",
  "adrien.krebs@licter.com",
  "balqis.sekkai@licter.com",
  "elsa.wallet@licter.com",
];
/* LEAD_TO (Vercel env, comma separated) narrows the list during a test; only team addresses are kept */
const TO = (process.env.LEAD_TO || "").split(",").map((s) => s.trim().toLowerCase()).filter((s) => TEAM.includes(s));
if (!TO.length) TO.push(...TEAM);
const FROM = "Site Licter <website@contact.licter.com>";

/* per action: what the visitor asked for, and what the team does next */
const ACTIONS = {
  callback: ["Demande de rappel", "Rappeler la personne, ou lui écrire si elle n'a laissé qu'un e-mail."],
  meeting: ["Demande de rendez-vous", "Proposer un créneau de trente minutes avec un consultant."],
  diagnostic: ["Demande de diagnostic", "Lire son contexte et proposer un échange pour le diagnostic."],
  quiz: ["Résultat du quiz", "Envoyer la lecture détaillée de son score."],
  real_case: ["Demande de cas réel", "Envoyer un cas réel de ce type, dans son secteur."],
  offer_example: ["Demande d'exemple d'offre", "Envoyer l'exemple de l'offre de la page d'origine, dans son secteur."],
  quote: ["Demande de devis", "Cadrer le périmètre avec la personne, puis envoyer le devis."],
  flash: ["Demande de flash offert", "Préparer le flash sur la marque indiquée."],
  guide: ["Demande de guide", "Envoyer le guide."],
  magazine: ["Demande du magazine", "Envoyer Audience First, le magazine."],
  event: ["Inscription à un événement", "Confirmer l'inscription et envoyer les informations pratiques."],
  newsletter: ["Inscription à la newsletter", "Ajouter l'adresse à la liste de la newsletter."],
};

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE = /^\+?\d{9,15}$/;
const ALLOWED_HOST = /(^|\.)licter\.com$|\.vercel\.app$/;
const FIRST = /^(pr[ée]nom|first ?name)$/i;
const LAST = /^(nom|name|last ?name|nom complet|full ?name)$/i;
const COMPANY = /entreprise|soci[ée]t[ée]|company|organisation|marque|brand/i;
const LONG = /^(la |votre |your )?(question|contexte|context|message|besoin|projet)/i;

const C = { navy: "#13162D", amber: "#EAA93D", cream: "#FCF6EF", line: "#E7E1D8", mute: "#6B6F82", page: "#F3EEE7" };
const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function clip(s, n) {
  s = String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}
/* "E-MAIL PROFESSIONNEL" (an uppercased label) reads "E-mail professionnel" */
function label(k) {
  return /[a-zà-ÿ]/.test(k) ? k : k.charAt(0) + k.slice(1).toLowerCase();
}

/* a block of rows: [label, value html] */
function rows(list) {
  return list.map(([k, v]) =>
    '<tr><td style="padding:9px 0;border-top:1px solid ' + C.line + ";color:" + C.mute + ';font-size:13px;width:150px;vertical-align:top">' + esc(k) +
    '</td><td style="padding:9px 0;border-top:1px solid ' + C.line + ';font-size:14px;vertical-align:top;color:' + C.navy + '">' + v + "</td></tr>").join("");
}
function heading(t) {
  return '<p style="margin:28px 0 6px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:' + C.mute + ';font-weight:700">' + esc(t) + "</p>";
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false });
  }
  /* only the site's own pages (a header other origins cannot send without a preflight) */
  const origin = req.headers.origin || req.headers.referer || "";
  let host = "";
  try { host = new URL(origin).hostname; } catch (e) { /* no origin */ }
  if (!ALLOWED_HOST.test(host) || req.headers["x-licter-form"] !== "1") {
    return res.status(403).json({ ok: false });
  }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== "object") return res.status(400).json({ ok: false });

  const action = String(body.action || "");
  if (!ACTIONS[action]) return res.status(400).json({ ok: false });
  const [what, todo] = ACTIONS[action];
  const raw = body.fields && typeof body.fields === "object" ? body.fields : {};
  const fields = Object.keys(raw).slice(0, 15).map((k) => [label(clip(k, 80)), clip(raw[k], 2000)]).filter(([k, v]) => k && v);

  /* a way to reach the person, or nothing is sent */
  const email = (fields.find(([, v]) => EMAIL.test(v)) || [])[1] || "";
  const phone = (fields.find(([, v]) => PHONE.test(v.replace(/[\s.()-]/g, ""))) || [])[1] || "";
  if (!email && !phone) return res.status(400).json({ ok: false });

  /* who: name and company first, then what they wrote, then the rest */
  const first = (fields.find(([k]) => FIRST.test(k)) || [])[1] || "";
  const last = (fields.find(([k]) => LAST.test(k)) || [])[1] || "";
  const company = (fields.find(([k]) => COMPANY.test(k)) || [])[1] || "";
  const name = [first, last].filter(Boolean).join(" ");
  const used = (k, v) => v === email || v === phone || FIRST.test(k) || LAST.test(k) || (company && v === company && COMPANY.test(k));
  const notes = fields.filter(([k, v]) => !used(k, v) && (LONG.test(k) || v.length > 90));
  const extra = fields.filter(([k, v]) => !used(k, v) && !notes.some(([n]) => n === k));

  const MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  const detail = clip(body.detail, 200).replace(/\b(\d{4})-(\d{2})-(\d{2})\b/, (m, y, mo, d) => +d + " " + (MONTHS[+mo - 1] || mo) + " " + y);
  const title = clip(body.title, 160).replace(/\s*[|·–-]\s*Licter.*$/i, "");
  let page = clip(body.page, 300);
  try { page = new URL(page, "https://www.licter.com").href; } catch (e) { page = ""; }
  const path = page ? new URL(page).pathname : "";
  const lang = body.lang === "en" ? "Anglais" : "Français";
  const when = new Date().toLocaleString("fr-FR", { timeZone: "Europe/Paris", dateStyle: "full", timeStyle: "short" });

  const who = name ? name + (company ? ", " + company : "") : company ? company + " · " + (email || phone) : email || phone;
  /* what it was about, when the page or the event says it */
  const about = action === "event" ? detail.split(" · ").map((x) => x.replace(/\s*:.*$/, "").replace(/\.$/, "")).join(" · ") : /^(offer_example|real_case)$/.test(action) ? title.replace(/\s*:.*$/, "") : "";
  const subject = clip([what, clip(about, 60), who].filter(Boolean).join(" · "), 200);
  const tel = phone ? phone.replace(/[^\d+]/g, "").replace(/^0(\d{9})$/, "+33$1") : "";
  const reply = email
    ? { href: "mailto:" + email + "?subject=" + encodeURIComponent("Licter · " + what), text: name ? "Répondre à " + (first || name) : "Répondre" }
    : { href: "tel:" + tel, text: name ? "Appeler " + (first || name) : "Appeler" };

  const contact = [];
  if (email && name) contact.push(["E-mail", '<a href="mailto:' + esc(email) + '" style="color:' + C.navy + ';font-weight:600">' + esc(email) + "</a>"]);
  if (phone && (name || email)) contact.push(["Téléphone", '<a href="tel:' + esc(tel) + '" style="color:' + C.navy + ';font-weight:600">' + esc(phone) + "</a>"]);

  const origin_ = [];
  if (page) origin_.push(["Page", '<a href="' + esc(page) + '" style="color:' + C.navy + '">' + esc(title || path) + "</a>" +
    (title ? '<br><span style="color:' + C.mute + ';font-size:12px">' + esc(path) + "</span>" : "")]);
  if (detail) origin_.push([action === "event" ? "Événement" : "Formulaire", esc(detail)]);
  origin_.push(["Langue", lang], ["Reçu le", esc(when)]);

  const html =
    '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">' +
    '<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>' + esc(subject) + "</title></head>" +
    '<body style="margin:0;padding:0;background:' + C.page + '">' +
    '<div style="display:none;max-height:0;overflow:hidden">' + esc(what + " · " + who + (title ? " · " + title : "")) + "</div>" +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:' + C.page + ';font-family:' + FONT + '"><tr><td align="center" style="padding:28px 12px">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:14px;overflow:hidden">' +
    /* header */
    '<tr><td style="background:' + C.navy + ';padding:22px 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>' +
    '<td style="vertical-align:middle"><img src="https://www.licter.com/assets/img/logo-white.png" width="48" height="48" alt="Licter" style="display:block;border:0"></td>' +
    '<td align="right" style="vertical-align:middle;color:' + C.amber + ';font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700">Nouvelle demande du site</td>' +
    "</tr></table></td></tr>" +
    /* who and what */
    '<tr><td style="padding:30px 32px 0">' +
    '<p style="margin:0 0 10px"><span style="display:inline-block;background:' + C.cream + ";border:1px solid " + C.amber + ";color:" + C.navy + ';border-radius:999px;padding:4px 12px;font-size:12px;font-weight:700">' + esc(what) + "</span></p>" +
    '<h1 style="margin:0;font-size:26px;line-height:1.25;color:' + C.navy + ';font-weight:700">' + esc(name || email || phone) + "</h1>" +
    (company ? '<p style="margin:4px 0 0;font-size:16px;color:' + C.mute + '">' + esc(company) + "</p>" : "") +
    (contact.length ? '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:18px">' + rows(contact) + "</table>" : "") +
    '<table role="presentation" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr><td style="background:' + C.amber + ';border-radius:999px">' +
    '<a href="' + esc(reply.href) + '" style="display:inline-block;padding:13px 26px;color:' + C.navy + ';font-weight:700;font-size:15px;text-decoration:none">' + esc(reply.text) + " →</a></td></tr></table>" +
    "</td></tr>" +
    /* next step */
    '<tr><td style="padding:24px 32px 0"><div style="background:' + C.cream + ";border-left:4px solid " + C.amber + ';border-radius:8px;padding:14px 16px;font-size:14px;color:' + C.navy + ';line-height:1.5">' +
    "<b>À faire&nbsp;:</b> " + esc(todo) + "</div></td></tr>" +
    /* the request */
    (notes.length || extra.length
      ? '<tr><td style="padding:0 32px">' + heading("Sa demande") +
        notes.map(([k, v]) => '<p style="margin:10px 0 4px;color:' + C.mute + ';font-size:13px">' + esc(k) + "</p>" +
          '<div style="background:#FAF8F5;border-radius:8px;padding:12px 14px;font-size:15px;line-height:1.55;color:' + C.navy + ';white-space:pre-wrap">' + esc(v) + "</div>").join("") +
        (extra.length ? '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px">' + rows(extra.map(([k, v]) => [k, "<b>" + esc(v) + "</b>"])) + "</table>" : "") +
        "</td></tr>"
      : "") +
    /* where it came from */
    '<tr><td style="padding:0 32px 30px">' + heading("Origine") +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">' + rows(origin_) + "</table></td></tr>" +
    "</table>" +
    '<p style="margin:16px 0 0;font-size:12px;color:' + C.mute + ';line-height:1.5;max-width:560px">Envoyé automatiquement par un formulaire de licter.com. ' +
    (email ? "Répondre à cet e-mail écrit directement à " + esc(email) + "." : "La personne n'a pas laissé d'e-mail&nbsp;: rappeler au " + esc(phone) + ".") + "</p>" +
    "</td></tr></table></body></html>";

  const text = [what + " · " + who, "", "À faire : " + todo, ""]
    .concat(email ? ["E-mail : " + email] : []).concat(phone ? ["Téléphone : " + phone] : []).concat(company ? ["Entreprise : " + company] : [])
    .concat(notes.concat(extra).length ? ["", "Sa demande"].concat(notes.concat(extra).map(([k, v]) => k + " : " + v)) : [])
    .concat(["", "Origine", "Page : " + (title ? title + " (" + page + ")" : page)])
    .concat(detail ? [(action === "event" ? "Événement" : "Formulaire") + " : " + detail] : [])
    .concat(["Langue : " + lang, "Reçu le : " + when]).join("\n");

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, error: "no key" });
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({ from: FROM, to: TO, subject: subject, html: html, text: text, reply_to: email || undefined }),
    });
    if (!r.ok) {
      console.error("resend", r.status, await r.text());
      return res.status(502).json({ ok: false });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error("resend", e);
    return res.status(502).json({ ok: false });
  }
};
