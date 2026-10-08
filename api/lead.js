/* =========================================================================
   Every form of the site lands here (js/track.js, window.LicterSend), and
   leaves as one email to the team, sent with Resend from contact@licter.com.
   The visitor gets no email: the page shows the confirmation.

   The Resend key is the RESEND_API_KEY environment variable of the Vercel
   project (Production): it never reaches the browser.

   Body (JSON): { action, detail, page, lang, fields: { label: value } }
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
const FROM = "Site Licter <contact@licter.com>";

/* one email subject per action: what the visitor asked for */
const ACTIONS = {
  callback: "Rappel demandé",
  meeting: "Rendez-vous demandé",
  diagnostic: "Diagnostic demandé",
  quiz: "Résultat du quiz demandé",
  real_case: "Cas réel demandé",
  offer_example: "Exemple d'offre demandé",
  quote: "Devis demandé",
  flash: "Flash offert demandé",
  guide: "Guide demandé",
  magazine: "Magazine demandé",
  event: "Inscription à un événement",
  newsletter: "Inscription à la newsletter",
};

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE = /^\+?\d{9,15}$/;
const ALLOWED_HOST = /(^|\.)licter\.com$|\.vercel\.app$/;

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function clip(s, n) {
  s = String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
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
  const raw = body.fields && typeof body.fields === "object" ? body.fields : {};
  const fields = Object.keys(raw).slice(0, 15).map((k) => [clip(k, 80), clip(raw[k], 2000)]).filter(([k, v]) => k && v);

  /* a way to reach the person, or nothing is sent */
  const values = fields.map(([, v]) => v);
  const email = values.find((v) => EMAIL.test(v)) || "";
  const phone = values.find((v) => PHONE.test(v.replace(/[\s.()-]/g, ""))) || "";
  if (!email && !phone) return res.status(400).json({ ok: false });

  const detail = clip(body.detail, 160);
  let page = clip(body.page, 300);
  try { page = new URL(page, "https://www.licter.com").href; } catch (e) { page = ""; }
  const lang = body.lang === "en" ? "anglais" : "français";
  const when = new Date().toLocaleString("fr-FR", { timeZone: "Europe/Paris", dateStyle: "full", timeStyle: "short" });
  const path = page ? new URL(page).pathname : "";

  const subject = clip(["[licter.com] " + ACTIONS[action], detail, email || phone].filter(Boolean).join(" · "), 200);
  const rows = fields.concat([["Page", page], ["Langue de la page", lang], ["Reçu le", when]]);
  const html =
    '<div style="font-family:Arial,sans-serif;font-size:14px;color:#13162D">' +
    "<h2 style=\"margin:0 0 6px;font-size:18px\">" + esc(ACTIONS[action]) + "</h2>" +
    (detail ? '<p style="margin:0 0 14px;color:#555">' + esc(detail) + "</p>" : "") +
    '<table cellpadding="6" style="border-collapse:collapse">' +
    rows.map(([k, v]) => '<tr><td style="color:#777;vertical-align:top;white-space:nowrap">' + esc(k) + '</td><td style="vertical-align:top"><b>' +
      (k === "Page" && v ? '<a href="' + esc(v) + '">' + esc(path) + "</a>" : esc(v)) + "</b></td></tr>").join("") +
    "</table>" +
    '<p style="margin:16px 0 0;color:#999;font-size:12px">Envoyé par le formulaire du site. ' +
    (email ? "Répondre à cet e-mail écrit directement à " + esc(email) + "." : "Pas d'e-mail : rappeler au " + esc(phone) + ".") + "</p></div>";
  const text = ACTIONS[action] + (detail ? " · " + detail : "") + "\n\n" + rows.map(([k, v]) => k + " : " + v).join("\n");

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
