// Gabarits des e-mails envoyés à l'équipe quand un formulaire du site est rempli.
// Mise en page en tableaux et styles en ligne : c'est ce que les messageries (Gmail, Outlook) affichent correctement.

const FORMS = {
  "rejoindre": {
    subject: "Nouvelle demande d'adhésion",
    title: "Nouvelle demande d'adhésion",
    intro: "Quelqu'un souhaite rejoindre le Social Intelligence Club. L'inscription est à valider.",
    next: "Répondez pour confirmer (ou non) l'adhésion.",
    fields: ["prenom", "nom", "societe", "fonction", "profil", "email", "attentes"],
  },
  "replay-pde": {
    subject: "Demande du replay du Printemps des Études",
    title: "Demande du replay",
    intro: "Quelqu'un souhaite recevoir le replay du Social Intelligence Morning (Printemps des Études 2026).",
    next: "Répondez avec le lien du replay.",
    fields: ["prenom", "nom", "societe", "email"],
  },
  "etude-100-dircom": {
    subject: "Demande de l'étude 100 dircom",
    title: "Demande de l'étude « 100 dircom »",
    intro: "Quelqu'un souhaite recevoir l'étude « Social listening : ce que pensent vraiment les 100 dircom que nous avons interrogés ».",
    next: "Répondez avec l'étude en pièce jointe ou en lien.",
    fields: ["email"],
  },
};

const LABELS = {
  prenom: "Prénom",
  nom: "Nom",
  societe: "Société",
  fonction: "Fonction",
  profil: "Profil",
  email: "E-mail",
  attentes: "Attentes",
};

function esc(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function build(form, data, page) {
  const f = FORMS[form];
  const name = [data.prenom, data.nom].filter(Boolean).join(" ");
  const who = name || data.email;
  const date = new Date().toLocaleString("fr-FR", { timeZone: "Europe/Paris", dateStyle: "long", timeStyle: "short" });
  const rows = f.fields.filter(function (k) { return data[k]; });

  const rowsHtml = rows.map(function (k, i) {
    const v = k === "email"
      ? '<a href="mailto:' + esc(data[k]) + '" style="color:#13162D;text-decoration:underline;">' + esc(data[k]) + "</a>"
      : esc(data[k]).replace(/\n/g, "<br>");
    return '<tr>' +
      '<td style="padding:14px 0;' + (i ? "border-top:1px solid #EFE7DA;" : "") + 'width:120px;vertical-align:top;font:600 12px/1.4 Arial,Helvetica,sans-serif;letter-spacing:.6px;text-transform:uppercase;color:#84919A;">' + LABELS[k] + "</td>" +
      '<td style="padding:14px 0;' + (i ? "border-top:1px solid #EFE7DA;" : "") + 'vertical-align:top;font:15px/1.5 Arial,Helvetica,sans-serif;color:#13162D;">' + v + "</td>" +
      "</tr>";
  }).join("");

  const reply = "mailto:" + encodeURIComponent(data.email) + "?subject=" + encodeURIComponent("Social Intelligence Club · " + f.subject);

  const html = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>' + esc(f.subject) + "</title></head>" +
    '<body style="margin:0;padding:0;background:#FCF6EF;">' +
    '<div style="display:none;max-height:0;overflow:hidden;">' + esc(f.title + " · " + who) + "</div>" +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FCF6EF;"><tr><td align="center" style="padding:32px 16px;">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;">' +

    // en-tête
    '<tr><td style="padding:0 4px 18px;font:700 11px/1 Arial,Helvetica,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#56606A;">Social Intelligence Club</td></tr>' +

    // carte
    '<tr><td style="background:#FFFFFF;border:1px solid #EFE7DA;border-radius:16px;overflow:hidden;">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">' +
    '<tr><td style="height:4px;background:#EAA93D;font-size:0;line-height:0;">&nbsp;</td></tr>' +
    '<tr><td style="padding:30px 32px 6px;">' +
    '<div style="display:inline-block;padding:5px 10px;border-radius:999px;background:#FBEBD0;font:700 11px/1 Arial,Helvetica,sans-serif;letter-spacing:1px;text-transform:uppercase;color:#A86C0A;">Formulaire du site</div>' +
    '<h1 style="margin:16px 0 0;font:700 24px/1.25 Arial,Helvetica,sans-serif;color:#13162D;">' + esc(f.title) + "</h1>" +
    '<p style="margin:10px 0 0;font:15px/1.55 Arial,Helvetica,sans-serif;color:#56606A;">' + esc(f.intro) + "</p>" +
    "</td></tr>" +
    '<tr><td style="padding:18px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">' + rowsHtml + "</table></td></tr>" +
    '<tr><td style="padding:18px 32px 32px;">' +
    '<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:8px;background:#13162D;">' +
    '<a href="' + reply + '" style="display:inline-block;padding:14px 22px;font:700 13px/1 Arial,Helvetica,sans-serif;letter-spacing:.6px;color:#FCF6EF;text-decoration:none;">' + (data.prenom ? "Répondre à " + esc(data.prenom) : "Répondre") + " →</a>" +
    "</td></tr></table>" +
    '<p style="margin:14px 0 0;font:13px/1.5 Arial,Helvetica,sans-serif;color:#84919A;">' + esc(f.next) + " Le bouton « Répondre » de votre messagerie écrit aussi directement à cette personne.</p>" +
    "</td></tr>" +
    "</table></td></tr>" +

    // pied
    '<tr><td style="padding:18px 4px 0;font:12px/1.6 Arial,Helvetica,sans-serif;color:#84919A;">Reçu le ' + esc(date) +
    ' depuis <a href="' + esc(page) + '" style="color:#84919A;">' + esc(page.replace(/^https?:\/\//, "")) + "</a></td></tr>" +

    "</table></td></tr></table></body></html>";

  const text = [
    "Social Intelligence Club · " + f.title,
    "",
    f.intro,
    "",
  ].concat(rows.map(function (k) { return LABELS[k] + " : " + data[k]; }))
    .concat(["", f.next, "", "Reçu le " + date + " depuis " + page])
    .join("\n");

  return { subject: "SIC · " + f.subject + " · " + who, html: html, text: text };
}

module.exports = { FORMS: FORMS, build: build };
