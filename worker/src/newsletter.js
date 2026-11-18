// Skadedyrbrevet: dobbel bekreftelse (double opt-in) uten egen database.
// Lenkene signeres med HMAC (nøkkel avledet fra BREVO_API_KEY), og Brevo er abonnentlisten.
// Flyt: POST /subscribe -> bekreftelses-e-post -> GET /confirm -> lagt i lista + får månedens brev -> GET /unsubscribe.

const enc = new TextEncoder();
const MAIL_RE = /^[^\s@<>"]{1,64}@[^\s@<>"]{1,190}\.[a-z]{2,}$/i;

async function key(env) {
  const raw = await crypto.subtle.digest("SHA-256", enc.encode("skadedyrbrevet:" + env.BREVO_API_KEY));
  return crypto.subtle.importKey("raw", raw, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
}
async function sign(env, s) {
  const sig = await crypto.subtle.sign("HMAC", await key(env), enc.encode(s));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "").slice(0, 32);
}
const eq = (a, b) => a.length === b.length && [...a].every((c, i) => c === b[i]);

async function brevo(env, path, body, method = "POST") {
  const r = await fetch("https://api.brevo.com/v3" + path, { method, headers: { "api-key": env.BREVO_API_KEY, "Content-Type": "application/json", accept: "application/json" }, body: body ? JSON.stringify(body) : undefined });
  if (!r.ok && r.status !== 204) throw new Error(`brevo ${path} ${r.status} ${(await r.text()).slice(0, 200)}`);
  return r.status === 204 ? {} : r.json().catch(() => ({}));
}
const send = (env, to, subject, html) => brevo(env, "/smtp/email", { sender: { name: "Skadedyrguiden", email: env.NL_SENDER }, to: [{ email: to }], subject, htmlContent: html });

const shell = (inner) => `<!doctype html><html lang="no"><body style="margin:0;background:#f4f1ea;font-family:Arial,Helvetica,sans-serif;color:#13201c">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" style="max-width:560px;background:#fff;border-radius:14px" cellpadding="0" cellspacing="0"><tr><td style="padding:30px 30px 26px">
<p style="margin:0 0 18px;font-weight:bold;font-size:18px">Skadedyrguiden<span style="color:#f2c230">●</span></p>${inner}</td></tr></table></td></tr></table></body></html>`;
const page = (env, path) => Response.redirect(`${env.SITE_URL}/nyhetsbrev/${path}`, 302);

export async function newsletter(req, env, url, h, json) {
  if (!env.BREVO_API_KEY || !env.NL_SENDER) return json({ error: "Påmeldingen er ikke koblet til ennå." }, 503, h);
  const self = url.origin;

  if (url.pathname === "/subscribe" && req.method === "POST") {
    if (h["Access-Control-Allow-Origin"] === "null") return json({ error: "origin not allowed" }, 403, h);
    let b; try { b = await req.json(); } catch { return json({ error: "bad json" }, 400, h); }
    if (b.website) return json({ ok: true }, 200, h);                       // honningkrukke mot roboter
    const email = String(b.email || "").trim().toLowerCase();
    if (!MAIL_RE.test(email)) return json({ error: "Sjekk e-postadressen." }, 400, h);
    const ts = Date.now().toString(36), t = await sign(env, `c|${email}|${ts}`);
    const link = `${self}/confirm?e=${encodeURIComponent(email)}&ts=${ts}&t=${t}`;
    await send(env, email, "Bekreft påmeldingen til Skadedyrbrevet", shell(`
<h1 style="font-family:Georgia,serif;font-weight:normal;font-size:28px;margin:0 0 12px">Bekreft e-postadressen din</h1>
<p style="font-size:16px;line-height:1.55">Noen (forhåpentligvis du) ba om å få Skadedyrbrevet – ett kort brev i måneden om hva som er i sesong, og hva du bør gjøre før det blir et problem.</p>
<p style="margin:24px 0"><a href="${link}" style="background:#f2c230;color:#13201c;text-decoration:none;font-weight:bold;padding:14px 24px;border-radius:999px;display:inline-block">Ja, meld meg på</a></p>
<p style="font-size:13px;color:#5d6b66;line-height:1.5">Lenken virker i 7 dager. Ba du ikke om dette, kan du se bort fra e-posten – da skjer ingenting.</p>`));
    return json({ ok: true, message: "Sjekk innboksen din og trykk på lenken for å bekrefte." }, 200, h);
  }

  if (url.pathname === "/confirm") {
    const email = (url.searchParams.get("e") || "").toLowerCase(), ts = url.searchParams.get("ts") || "", t = url.searchParams.get("t") || "";
    const age = Date.now() - parseInt(ts, 36);
    if (!MAIL_RE.test(email) || !(age >= 0 && age < 7 * 864e5) || !eq(t, await sign(env, `c|${email}|${ts}`))) return page(env, "ugyldig.html");
    await brevo(env, "/contacts", { email, listIds: [Number(env.BREVO_LIST_ID)], updateEnabled: true, attributes: { KILDE: "skadedyrguiden", BEKREFTET: new Date().toISOString().slice(0, 10) } });
    // Månedens brev rett til den nye abonnenten
    try {
      const issue = await (await fetch(`${env.SITE_URL}/nyhetsbrev/latest.json`, { cf: { cacheTtl: 300 } })).json();
      const html = (await (await fetch(`${env.SITE_URL}/nyhetsbrev/${issue.slug}.email.html`)).text())
        .replaceAll("{{ unsubscribe }}", `${self}/unsubscribe?e=${encodeURIComponent(email)}&t=${await sign(env, `u|${email}`)}`);
      await send(env, email, issue.subject, html);
    } catch (e) { console.log("welcome issue failed", String(e)); }
    return page(env, "bekreftet.html");
  }

  if (url.pathname === "/unsubscribe") {
    const email = (url.searchParams.get("e") || "").toLowerCase(), t = url.searchParams.get("t") || "";
    if (!MAIL_RE.test(email) || !eq(t, await sign(env, `u|${email}`))) return page(env, "ugyldig.html");
    await brevo(env, `/contacts/${encodeURIComponent(email)}`, { unlinkListIds: [Number(env.BREVO_LIST_ID)] }, "PUT").catch(() => {});
    return page(env, "avmeldt.html");
  }
  return null;
}
