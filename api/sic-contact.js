// Formulaires du Social Intelligence Club → e-mail à l'équipe, via Resend.
// Le navigateur poste ici (/api/sic-contact). La clé RESEND_API_KEY est celle du projet Vercel licter-website-new.
// Les autres formulaires du site passent par api/lead.js.

const { FORMS, build } = require("./_sic-email");

const FROM = process.env.SIC_FORM_FROM || "Social Intelligence Club <club@contact.licter.com>";
const TO = (process.env.SIC_FORM_TO || "anais.bremand@licter.com").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const ORIGINS = /^https:\/\/(www\.)?licter\.com$|^https:\/\/(socialintelligenceclub|licter-website)(-[a-z0-9-]+)?\.vercel\.app$|^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/;

function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 300);
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false });
  }
  const origin = req.headers.origin;
  if (origin && !ORIGINS.test(origin)) return res.status(403).json({ ok: false });

  let body = req.body || {};
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch (e) { body = {}; }
  }

  // champ piège : rempli uniquement par les robots
  if (body._honey) return res.status(200).json({ ok: true });

  const form = clean(body.form, 40);
  if (!FORMS[form]) return res.status(400).json({ ok: false });

  const data = {
    prenom: clean(body.prenom, 80),
    nom: clean(body.nom, 80),
    societe: clean(body.societe, 120),
    fonction: clean(body.fonction, 120),
    profil: clean(body.profil, 120),
    email: clean(body.email, 200),
    attentes: clean(body.attentes, 2000),
  };
  if (!EMAIL.test(data.email)) return res.status(400).json({ ok: false });

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.error("RESEND_API_KEY manquante");
    return res.status(503).json({ ok: false });
  }

  const page = clean(body.page, 300) || "https://www.licter.com/socialintelligenceclub/";
  const mail = build(form, data, page);

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: FROM,
        to: TO,
        reply_to: data.email,
        subject: mail.subject,
        html: mail.html,
        text: mail.text,
        tags: [{ name: "form", value: form }],
      }),
    });
    if (r.ok) return res.status(200).json({ ok: true });
    console.error("resend", r.status, await r.text().catch(function () { return ""; }));
    return res.status(502).json({ ok: false });
  } catch (e) {
    console.error("resend", e);
    return res.status(502).json({ ok: false });
  }
};
