"""Forskjellsagent: lager side-om-side-sammenligninger for arter som forveksles (fra kb/species.json).
Bygger bare på faktaarkene (kb/species.json + kb/species_info.json, hentet fra FHI). Et kontrollkall stryker rader uten dekning.
Skriver kb/compare.json: {"a|b": {"rows":[{"trait","a","b","key"}], "test": "..."}}"""
import json, os, pathlib, urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
KB = {s["id"]: s for s in json.loads((REPO / "kb/species.json").read_text())["species"]}
INFO = json.loads((REPO / "kb/species_info.json").read_text()) if (REPO / "kb/species_info.json").exists() else {}
OUT = REPO / "kb/compare.json"


def gemini(prompt):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}}
    for m in ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", data=json.dumps(body).encode(),
                                       headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            return json.loads(json.load(urllib.request.urlopen(r, timeout=120))["candidates"][0]["content"]["parts"][0]["text"])
        except Exception as e:
            print("   ", m, str(e)[:150])
    return {}


def sheet(i):
    s = KB[i]
    return {"navn": s["name"], "latin": s["latin"], "kjennetegn": s["features"], "forveksling": s["confusable"], "fakta": {k: v for k, v in INFO.get(i, {}).items() if k != "kilde"}}


pairs = sorted({tuple(sorted((s, c["id"]))) for s in KB for c in KB[s]["confusable"] if c["id"] in KB})
out = json.loads(OUT.read_text()) if OUT.exists() else {}
for a, b in pairs:
    key = f"{a}|{b}"
    if key in out and not os.environ.get("FORCE"): continue
    src = json.dumps({"A": sheet(a), "B": sheet(b)}, ensure_ascii=False)
    d = gemini(f"""Lag en tydelig sammenligning av A ({KB[a]['name']}) og B ({KB[b]['name']}) for en vanlig huseier som vil vite hvilken av dem hen har.
Bruk BARE opplysninger fra faktaarkene under. 4–7 rader, hver med en egenskap (trait, f.eks. Størrelse, Farge, Hode, Kropp, Haletråder, Atferd, Hvor, Skade) og kort verdi for A og B (maks 10 ord hver).
Marker med key=true de 1–2 radene som skiller dem sikrest. Ta bare med rader der begge verdiene står i faktaarkene.
test: én setning med den raskeste måten å skille dem på (maks 22 ord).
Svar som JSON: {{"rows":[{{"trait":"","a":"","b":"","key":false}}],"test":""}}

FAKTAARK:
{src}""")
    chk = gemini(f"""Faktasjekk sammenligningen mot faktaarkene. Fjern rader der A- eller B-verdien ikke støttes. Behold resten uendret, samme JSON-struktur.

SAMMENLIGNING:
{json.dumps(d, ensure_ascii=False)}

FAKTAARK:
{src}""") or d
    rows = [r for r in chk.get("rows", []) if r.get("a") and r.get("b")]
    if len(rows) >= 2:
        out[key] = {"rows": rows[:7], "test": chk.get("test", "")}
        print(key, len(rows), "rader |", chk.get("test", "")[:90])
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
