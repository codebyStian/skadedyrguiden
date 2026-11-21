"""Skadedyrbrevet – redaksjonsagenten.

1. Research: Gemini med Google-søk finner aktuelle saker i norske medier/offentlige kilder siste 6 uker.
2. Egne kilder: artiklene på Skadedyrguiden som er i sesong neste måned, med tekst og kildelister.
3. Skriving: ett kort brev (3–4 saker + månedens sjekkliste) i Skadedyrguidens stemme.
4. Faktakontroll: et eget kall sjekker hver påstand mot kildene; saker uten dekning strykes.
5. Utgivelse: arkivside (nyhetsbrev/ÅÅÅÅ-MM.html), e-postversjon, latest.json.
6. Utsending: MODE=draft sender et prøveeksemplar til NL_ADMIN; MODE=send lager og sender Brevo-kampanje til lista.

Miljø: GEMINI_API_KEY, BREVO_API_KEY, NL_SENDER, NL_ADMIN, MODE (draft|send|build), MONTH (ÅÅÅÅ-MM, valgfri).
"""
import datetime, html as H, json, os, pathlib, re, sys, urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = REPO / "site"; OUT = SITE / "nyhetsbrev"; OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(REPO / "scripts"))
from articles import ARTICLES, EXTRA  # noqa: E402

BASE = os.environ.get("SITE_URL", "https://kryp.as").rstrip("/")
MODE = os.environ.get("MODE", "build")
MODELS = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
MND = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
UTM = "utm_source=skadedyrbrevet&utm_medium=email&utm_campaign={}"

today = datetime.date.today()
if os.environ.get("MONTH"):
    y, m = map(int, os.environ["MONTH"].split("-"))
else:  # brevet lages i slutten av måneden for neste måned
    y, m = (today.year + (today.month == 12), today.month % 12 + 1) if today.day >= 15 else (today.year, today.month)
SLUG = f"{y}-{m:02d}"; MONTH = MND[m - 1]


def gemini(prompt, search=False, schema=True):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}
    if search: body["tools"] = [{"google_search": {}}]
    elif schema: body["generationConfig"]["responseMimeType"] = "application/json"
    err = None
    for model in MODELS:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            d = json.load(urllib.request.urlopen(r, timeout=180))
            c = d["candidates"][0]
            text = "".join(p.get("text", "") for p in c["content"]["parts"])
            links = [{"title": g["web"].get("title", ""), "url": g["web"]["uri"]} for g in c.get("groundingMetadata", {}).get("groundingChunks", []) if "web" in g]
            return text, links, model
        except Exception as e:  # prøv neste modell
            err = e; print("model", model, "failed:", str(e)[:200])
    raise SystemExit(f"Gemini failed: {err}")


def parse(t):
    t = re.sub(r"^```(json)?|```$", "", t.strip(), flags=re.M).strip()
    return json.loads(t[t.find("{"): t.rfind("}") + 1] if "{" in t else t)


def resolve(u):  # Google-søk gir omdirigeringslenker; finn den egentlige adressen
    try:
        return urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=15).url
    except Exception:
        return u


# ---------- 6. Utsending (definert her, kalles til slutt) ----------
def brevo(path, body=None, method="POST"):
    r = urllib.request.Request("https://api.brevo.com/v3" + path, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"api-key": os.environ["BREVO_API_KEY"], "Content-Type": "application/json", "accept": "application/json"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        t = resp.read(); return json.loads(t) if t else {}


def dispatch(issue, email_html):
  if MODE in ("draft", "send") and os.environ.get("BREVO_API_KEY") and os.environ.get("NL_SENDER"):
      sender = {"name": "Skadedyrguiden", "email": os.environ["NL_SENDER"]}
      if MODE == "draft" and os.environ.get("NL_ADMIN"):
          for adr in os.environ["NL_ADMIN"].split(","):
              brevo("/smtp/email", {"sender": sender, "to": [{"email": adr.strip()}], "subject": "[UTKAST] " + issue["subject"],
                                    "htmlContent": email_html.replace("{{ unsubscribe }}", BASE)})
          print("Utkast sendt til", os.environ["NL_ADMIN"])
      if MODE == "send":
          list_id = int(os.popen(f"python3 {REPO/'scripts/brevo_list.py'}").read().strip())
          camp = brevo("/emailCampaigns", {"name": f"Skadedyrbrevet {SLUG}", "subject": issue["subject"], "previewText": issue["preheader"],
                                            "sender": sender, "htmlContent": email_html, "recipients": {"listIds": [list_id]}})
          brevo(f"/emailCampaigns/{camp['id']}/sendNow", {})
          print("Kampanje sendt:", camp["id"])
  elif MODE in ("draft", "send"):
      print("BREVO_API_KEY/NL_SENDER mangler – brevet er bare publisert på nettsiden.")


if MODE == "send" and (OUT / f"{SLUG}.json").exists():   # send utkastet som ble laget og gjennomlest tidligere i måneden
    print("Sender eksisterende brev", SLUG)
    dispatch(json.loads((OUT / f"{SLUG}.json").read_text()), (OUT / f"{SLUG}.email.html").read_text())
    raise SystemExit

# ---------- 1. Egne artikler i sesong ----------
own = []
for a in ARTICLES + EXTRA:
    if m in a.get("months", []) or (m % 12 + 1) in a.get("months", []):
        p = SITE / "artikler" / f"{a['slug']}.html"
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", "", p.read_text(encoding="utf-8"), flags=re.S))) if p.exists() else a.get("lead", "")
        art = re.search(r"<article.*?</article>", p.read_text(encoding="utf-8"), re.S) if p.exists() else None
        if art: text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art.group(0)))
        own.append({"slug": a["slug"], "title": a["title"], "url": f"{BASE}/artikler/{a['slug']}.html", "text": text[:2500]})
print(len(own), "egne artikler i sesong")

# ---------- 2. Research: aktuelle saker ----------
research_prompt = f"""Du er research-redaktør for Skadedyrguiden, en norsk fagside om skadedyr i hus, hytte og hage.
Finn 5–8 aktuelle saker fra de siste 6 ukene (før {today.isoformat()}) som er relevante for norske huseiere og hytteeiere i {MONTH} {y}:
nyheter i norske medier, råd eller tall fra Folkehelseinstituttet, Mattilsynet, Miljødirektoratet, kommuner, forsikringsselskaper, Meteorologisk institutt (f.eks. smågnagerår, mus/rotter, veggedyr, skjeggkre, flått, veps, nye arter, regelendringer, værforhold som påvirker skadedyr).
Bare saker du faktisk finner i søket. For hver sak: kort, nøkternt sammendrag med egne ord (2–3 setninger), hvem som står bak, dato og nøyaktig URL.
Svar som JSON: {{"items":[{{"title":"","summary":"","source":"","date":"","url":""}}]}}"""
text, links, model = gemini(research_prompt, search=True)
try:
    news = parse(text).get("items", [])
except Exception:
    news = []
known = {resolve(l["url"]) for l in links}
for n in news:
    n["url"] = resolve(n.get("url", ""))
news = [n for n in news if n.get("url", "").startswith("http")]
print(len(news), "aktuelle saker via", model, "| grounding-lenker:", len(known))

# ---------- 3. Skriving ----------
sources = {"nyheter": news, "artikler": [{k: a[k] for k in ("slug", "title", "url", "text")} for a in own]}
write_prompt = f"""Du skriver Skadedyrbrevet for {MONTH} {y}: ett kort, nyttig månedsbrev fra Skadedyrguiden til norske hus- og hytteeiere.
Stemme: rolig, konkret, faglig og vennlig. Ingen skremsler, ingen utropstegn, ingen klisjeer som «i en verden der». Norsk bokmål.
Bruk BARE fakta som står i kildene under. Ikke finn på tall, datoer eller råd.
Innhold:
- subject: emnefelt, maks 60 tegn, konkret om {MONTH}
- preheader: maks 90 tegn
- intro: 2–3 setninger om hva som skjer med skadedyr i {MONTH}
- items: 3–4 saker. Bland aktuelle nyheter og sesongråd. Hver: title, text (60–110 ord, egne ord), link (URL fra kildene: helst en av våre artikler når det passer, ellers nyhetskilden), link_label, source_urls (liste med URL-er fakta bygger på).
- checklist: 3–5 korte gjøremål for {MONTH} (hver maks 12 ord), med source_urls.
- Tenk på at fjellhytter og sjøhytter har ulike sesonger, og at landsdelene er forskjellige.
Svar som JSON: {{"subject":"","preheader":"","intro":"","items":[{{"title":"","text":"","link":"","link_label":"","source_urls":[]}}],"checklist":[{{"text":"","source_urls":[]}}]}}

KILDER:
{json.dumps(sources, ensure_ascii=False)}"""
issue = parse(gemini(write_prompt)[0])

# ---------- 4. Faktakontroll ----------
check_prompt = f"""Du er faktasjekker. Under er et utkast til nyhetsbrev og kildene det bygger på.
For hver sak (items[i]) og hvert gjøremål (checklist[i]): støttes ALLE faktapåstander av kildene? Små omformuleringer er greit; nye tall, datoer, arter, regler eller råd som ikke står i kildene er ikke greit.
Svar som JSON: {{"items":[{{"i":0,"ok":true,"problem":""}}],"checklist":[{{"i":0,"ok":true,"problem":""}}]}}

UTKAST:
{json.dumps(issue, ensure_ascii=False)}

KILDER:
{json.dumps(sources, ensure_ascii=False)}"""
chk = parse(gemini(check_prompt)[0])
bad_i = {c["i"] for c in chk.get("items", []) if not c.get("ok", True)}
bad_c = {c["i"] for c in chk.get("checklist", []) if not c.get("ok", True)}
for c in chk.get("items", []) + chk.get("checklist", []):
    if not c.get("ok", True): print("STRØKET:", c)
allowed = {n["url"] for n in news} | {a["url"] for a in own}
issue["items"] = [it for i, it in enumerate(issue.get("items", [])) if i not in bad_i and it.get("link") in allowed]
issue["checklist"] = [c for i, c in enumerate(issue.get("checklist", [])) if i not in bad_c]
if len(issue["items"]) < 2:
    raise SystemExit("For få saker besto faktakontrollen – brevet sendes ikke. Se loggen.")
used = sorted({u for it in issue["items"] + issue["checklist"] for u in it.get("source_urls", []) if u in allowed} | {it["link"] for it in issue["items"]})
issue.update(slug=SLUG, month=MONTH, year=y, sources=used, model=model, generated=today.isoformat())


# ---------- 5. Utgivelse ----------
def tagged(u, medium="email"):
    if not u.startswith(BASE): return u
    return u + ("&" if "?" in u else "?") + UTM.format(SLUG).replace("medium=email", f"medium={medium}")


e = H.escape
items_mail = "".join(f'''<tr><td style="padding:18px 0;border-top:1px solid #e6e2d8">
<h2 style="font-family:Georgia,serif;font-weight:normal;font-size:22px;margin:0 0 8px">{e(it["title"])}</h2>
<p style="font-size:16px;line-height:1.55;margin:0 0 10px">{e(it["text"])}</p>
<a href="{e(tagged(it["link"]))}" style="color:#13201c;font-weight:bold">{e(it.get("link_label") or "Les mer")} →</a></td></tr>''' for it in issue["items"])
check_mail = "".join(f'<li style="margin:0 0 6px">{e(c["text"])}</li>' for c in issue["checklist"])
src_mail = "".join(f'<li><a href="{e(u)}" style="color:#5d6b66">{e(re.sub(r"^https?://(www\.)?", "", u)[:70])}</a></li>' for u in used)
shop = "https://skadedyrbutikken.no/?" + UTM.format(SLUG)
email_html = f'''<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{e(issue["subject"])}</title></head>
<body style="margin:0;background:#f4f1ea;font-family:Arial,Helvetica,sans-serif;color:#13201c">
<div style="display:none;max-height:0;overflow:hidden">{e(issue["preheader"])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" style="max-width:600px;background:#fff;border-radius:14px" cellpadding="0" cellspacing="0"><tr><td style="padding:30px">
<p style="margin:0;font-weight:bold;font-size:18px">Skadedyrguiden<span style="color:#f2c230">●</span></p>
<p style="margin:4px 0 22px;color:#5d6b66;font-size:13px">Skadedyrbrevet · {MONTH.capitalize()} {y}</p>
<h1 style="font-family:Georgia,serif;font-weight:normal;font-size:32px;line-height:1.15;margin:0 0 14px">{e(issue["subject"])}</h1>
<p style="font-size:17px;line-height:1.55;margin:0 0 8px">{e(issue["intro"])}</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{items_mail}</table>
<div style="background:#13201c;color:#fff;border-radius:12px;padding:20px 22px;margin:18px 0">
<p style="margin:0 0 10px;font-weight:bold;color:#f2c230">Gjør dette i {MONTH}</p><ul style="margin:0;padding-left:18px;line-height:1.5">{check_mail}</ul></div>
<p style="margin:22px 0"><a href="{shop}" style="background:#f2c230;color:#13201c;text-decoration:none;font-weight:bold;padding:13px 22px;border-radius:999px;display:inline-block">Utstyr hos Skadedyrbutikken</a></p>
<p style="font-size:12px;color:#5d6b66;margin:20px 0 4px">Kilder</p><ul style="font-size:12px;color:#5d6b66;margin:0;padding-left:18px">{src_mail}</ul>
<p style="font-size:12px;color:#5d6b66;margin:22px 0 0">Du får dette fordi du har meldt deg på Skadedyrbrevet. <a href="{{{{ unsubscribe }}}}" style="color:#5d6b66">Meld deg av</a> · <a href="{BASE}/nyhetsbrev/{SLUG}.html" style="color:#5d6b66">Les i nettleseren</a></p>
</td></tr></table></td></tr></table></body></html>'''
(OUT / f"{SLUG}.email.html").write_text(email_html, encoding="utf-8")
(OUT / f"{SLUG}.json").write_text(json.dumps(issue, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "latest.json").write_text(json.dumps({"slug": SLUG, "subject": issue["subject"], "preheader": issue["preheader"]}, ensure_ascii=False), encoding="utf-8")
print("Brev:", issue["subject"], "|", len(issue["items"]), "saker,", len(issue["checklist"]), "gjøremål,", len(used), "kilder")



dispatch(issue, email_html)
