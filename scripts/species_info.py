"""Fagagent for leksikonet: henter FHIs skadedyrhåndbok-side for hver art og trekker ut utfyllende kjennetegn og råd.
Bare det som står på kildesiden skal med. Et eget kontrollkall stryker punkter uten dekning i kildeteksten.
Skriver kb/species_info.json."""
import html as H, json, os, pathlib, re, urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
KB = json.loads((REPO / "kb/species.json").read_text())["species"]
OUT = REPO / "kb/species_info.json"
MODELS = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
FIELDS = {"storrelse": "Størrelse", "utseende": "Utseende", "hvor": "Hvor du finner den", "tegn": "Spor og tegn", "livssyklus": "Livssyklus og sesong",
          "skade": "Skade og helse", "forebygg": "Forebygging", "tiltak": "Slik blir du kvitt den"}


def page_text(url):
    h = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Kryp.as)"}), timeout=40).read().decode("utf-8", "replace")
    m = re.search(r"<main.*?</main>", h, re.S) or re.search(r"<article.*?</article>", h, re.S)
    h = m.group(0) if m else h
    h = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def gemini(prompt):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}}
    for m in MODELS:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", data=json.dumps(body).encode(),
                                       headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            d = json.load(urllib.request.urlopen(r, timeout=120))
            return json.loads("".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]))
        except Exception as e:
            print("   ", m, str(e)[:150])
    return {}


info = json.loads(OUT.read_text()) if OUT.exists() else {}
for s in KB:
    if s["id"] in info and not os.environ.get("FORCE"): continue
    try:
        src = page_text(s["source"]["url"])
    except Exception as e:
        print(s["id"], "kilde feilet:", e); continue
    if len(src) < 400: print(s["id"], "for lite tekst"); continue
    keys = ", ".join(f'"{k}"' for k in FIELDS)
    draft = gemini(f"""Trekk ut fakta om {s['name']} ({s['latin']}) fra kildeteksten under (Folkehelseinstituttets skadedyrhåndbok).
For hvert felt ({keys}): 1–4 korte punkter på norsk bokmål, egne ord, konkret (mål i mm/cm, farger, steder, måneder).
Bare det som står i kildeteksten. Står ingenting om et felt: tom liste. Ikke nevn produktnavn.
Svar som JSON med feltene som nøkler og lister med strenger som verdier.

KILDETEKST:
{src[:12000]}""")
    check = gemini(f"""Faktasjekk: Stryk hvert punkt som ikke støttes av kildeteksten. Behold resten uendret.
Svar som JSON med samme struktur.

PUNKTER:
{json.dumps(draft, ensure_ascii=False)}

KILDETEKST:
{src[:12000]}""") or draft
    info[s["id"]] = {k: [x for x in check.get(k, []) if isinstance(x, str) and x.strip()][:4] for k in FIELDS}
    info[s["id"]]["kilde"] = s["source"]
    print(s["id"], {k: len(v) for k, v in info[s["id"]].items() if k != "kilde"})
OUT.write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
