// Skadedyrguiden – bildeanalyse. Bildet lagres ikke. To trinn:
// 1) visjonsmodell beskriver hva som faktisk synes og velger blant artene i faktagrunnlaget (kb/species.json, FHI-kilder)
// 2) en egen kontrollmodell sjekker at begrunnelsen stemmer med faktaarket; i tillegg faste regler i koden.
import KB from "../../kb/species.json";

const VISION = ["@cf/meta/llama-4-scout-17b-16e-instruct", "@cf/mistralai/mistral-small-3.1-24b-instruct"];
const CHECKER = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
const MAX_BYTES = 2_000_000;
const SPECIES = KB.species;
const BY_ID = Object.fromEntries(SPECIES.map((s) => [s.id, s]));

function cors(req, env) {
  const o = req.headers.get("Origin") || "";
  const ok = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).includes(o);
  return { "Access-Control-Allow-Origin": ok ? o : "null", "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" };
}
const json = (obj, status, h) => new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json; charset=utf-8", ...h } });

const norm = (s) => String(s).toLowerCase().replace(/[^a-zæøå0-9 ]/g, " ").split(/\s+/).filter((w) => w.length > 2);
// Kobler modellens formulering til et kjennetegn som faktisk står i faktaarket (ordoverlapp), ellers forkastes det.
const same = (x, y) => x === y || (x.length > 4 && y.length > 4 && x.slice(0, 5) === y.slice(0, 5) && x.endsWith("løs") === y.endsWith("løs"));
function toFact(claim, facts) {
  const c = norm(claim); if (!c.length) return [];
  return facts.filter((f) => {
    const w = norm(f), hits = c.filter((x) => w.some((y) => same(x, y))).length;
    if (["ikke", "mindre", "uten", "kortere"].some((n) => w.includes(n) !== c.includes(n))) return false;   // ikke la «sølvglinsende» treffe «mindre sølvglinsende»
    return hits >= Math.min(2, c.length, w.length) && Math.max(hits / c.length, hits / w.length) >= 0.6;
  });
}

function parseJSON(t) {
  if (typeof t !== "string") return t;
  const m = t.match(/\{[\s\S]*\}/);
  try { return JSON.parse(m ? m[0] : t); } catch { return null; }
}

function factSheet() {
  return SPECIES.map((s) => `- id=${s.id}: ${s.name} (${s.latin}). Kjennetegn: ${s.features.join("; ")}.` +
    (s.confusable.length ? ` Forveksles med: ${s.confusable.map((c) => c.id + " (" + c.how + ")").join("; ")}.` : "")).join("\n");
}

async function vision(env, dataUrl, hint) {
  const system = `Du er en nøktern assistent som hjelper folk i Norge å identifisere mulige skadedyr fra et bilde.
Du skal KUN bruke artene og kjennetegnene i faktaarket under (kilde: Folkehelseinstituttet). Ikke gjett utover dette.
Beskriv først nøytralt hva som faktisk er synlig i bildet. Velg deretter blant id-ene i faktaarket.
Hvis bildet er uskarpt, for mørkt, viser flere dyr, eller ikke passer noen art: si det og gi lav sikkerhet.
"matched" kan bare inneholde kjennetegn som står ordrett i faktaarket for den arten OG som faktisk synes i bildet.
Svar KUN med JSON: {"visible": "kort nøytral beskrivelse på norsk", "image_quality": "god|middels|dårlig",
"animal_visible": true|false, "candidates": [{"id": "...", "confidence": 0.0-1.0, "matched": ["..."], "against": ["..."]}]}
Maks 3 kandidater, sortert etter sikkerhet.

FAKTAARK:
${factSheet()}`;
  const user = [{ type: "text", text: "Hva er dette?" + (hint ? ` Brukeren oppgir: «${String(hint).slice(0, 200)}».` : "") },
    { type: "image_url", image_url: { url: dataUrl } }];
  let lastErr;
  for (const model of VISION) {
    try {
      const r = await env.AI.run(model, { messages: [{ role: "system", content: system }, { role: "user", content: user }], max_tokens: 700, temperature: 0.1 });
      const out = parseJSON(r.response ?? r);
      if (out && Array.isArray(out.candidates)) return { model, out };
      lastErr = "unparseable";
    } catch (e) { lastErr = String(e); }
  }
  throw new Error("vision failed: " + lastErr);
}

async function check(env, v, top) {
  const s = BY_ID[top.id];
  const prompt = `Du er faglig kvalitetskontrollør. En bildemodell har foreslått arten "${s.name}".
Modellens beskrivelse av bildet: "${v.visible}". Kjennetegn den mener stemmer: ${JSON.stringify(top.matched || [])}.
Kjennetegn mot: ${JSON.stringify(top.against || [])}.
Faktaark for ${s.name} (FHI): ${s.features.join("; ")}. Forveksling: ${s.confusable.map((c) => c.how).join("; ") || "ingen oppgitt"}.
Vurder strengt: Henger beskrivelsen sammen med faktaarket? Er det tegn på at det heller er en forvekslingsart?
Svar KUN med JSON: {"verdict": "bekreftet|usikker|avvist", "confidence": 0.0-1.0, "reason": "én setning på norsk"}`;
  try {
    const r = await env.AI.run(CHECKER, { messages: [{ role: "user", content: prompt }], max_tokens: 200, temperature: 0 });
    return parseJSON(r.response ?? r) || { verdict: "usikker", confidence: 0.3, reason: "Kontrollen kunne ikke tolkes." };
  } catch { return { verdict: "usikker", confidence: 0.3, reason: "Kontrollen var ikke tilgjengelig." }; }
}

export default {
  async fetch(req, env) {
    const h = cors(req, env);
    if (req.method === "OPTIONS") return new Response(null, { headers: h });
    const url = new URL(req.url);
    if (url.pathname === "/health") return json({ ok: true, species: SPECIES.length }, 200, h);
    if (req.method !== "POST" || url.pathname !== "/identify") return json({ error: "not found" }, 404, h);
    if (h["Access-Control-Allow-Origin"] === "null") return json({ error: "origin not allowed" }, 403, h);
    let body;
    try { body = await req.json(); } catch { return json({ error: "bad json" }, 400, h); }
    const img = String(body.image || "");
    if (!/^data:image\/(jpeg|png|webp);base64,/.test(img)) return json({ error: "bildet må være jpeg, png eller webp" }, 400, h);
    if (img.length * 0.75 > MAX_BYTES) return json({ error: "bildet er for stort" }, 413, h);

    const { model, out: v } = await vision(env, img, body.hint);
    const cands = (v.candidates || []).filter((c) => BY_ID[c.id]).map((c) => {
      const matched = [...new Set((c.matched || []).flatMap((m) => toFact(m, BY_ID[c.id].features)))];   // bare kjennetegn fra faktaarket
      const conf = Math.max(0, Math.min(1, Number(c.confidence) || 0));
      return { id: c.id, confidence: matched.length ? conf : Math.min(conf, 0.35), matched, against: c.against || [] };
    }).sort((a, b) => b.confidence - a.confidence);

    if (!v.animal_visible || !cands.length) {
      return json({ level: "ukjent", visible: v.visible, quality: v.image_quality, message: "Vi fant ikke et dyr vi kjenner igjen i bildet.", model }, 200, h);
    }
    const top = cands[0];
    const c = await check(env, v, top);
    let conf = Math.min(top.confidence, Number(c.confidence) || 0);
    if (c.verdict === "avvist") conf = Math.min(conf, 0.25);
    if (v.image_quality === "dårlig") conf = Math.min(conf, 0.4);
    if (cands[1] && cands[1].confidence > top.confidence - 0.15) conf = Math.min(conf, 0.55);
    const level = conf >= 0.75 && c.verdict === "bekreftet" ? "sannsynlig" : conf >= 0.45 ? "mulig" : "usikker";
    const s = BY_ID[top.id];
    return json({
      level, confidence: Math.round(conf * 100), id: s.id, name: s.name, latin: s.latin, pest: s.pest,
      visible: v.visible, quality: v.image_quality, matched: top.matched, check: c.reason,
      checkedFacts: s.checked, source: s.source,
      alternatives: cands.slice(1).map((a) => ({ id: a.id, name: BY_ID[a.id].name, confidence: Math.round(a.confidence * 100) })),
      confusable: s.confusable.map((x) => ({ name: BY_ID[x.id]?.name || x.id, how: x.how })), model,
    }, 200, h);
  },
};
