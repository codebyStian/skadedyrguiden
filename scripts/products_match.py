"""Produktagenten: velger 3–5 presise produkter fra skadedyrbutikken.no for hver side på Kryp.as.

1. Forhåndsfilter: tekstlikhet mellom siden og produktene (navn, kategori, beskrivelse) gir ~60 kandidater.
2. Gemini velger og begrunner (rolle + hvorfor) – bare blant kandidatene, med regler om riktig art og trygg bruk.
3. Kontroll: ukjente produkter, utsolgte og profesjonelle gifter som krever godkjenning, forkastes.
Skriver site/data/recs.json: {sidenøkkel: [{url,name,price,image,role,why}]}.
"""
import json, math, os, pathlib, re, sys, collections, urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from articles import ARTICLES  # noqa: E402

CAT = json.loads((REPO / "data/products.json").read_text())["products"]
KB = json.loads((REPO / "kb/species.json").read_text())["species"]
MODELS = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
OUT = REPO / "site/data/recs.json"
ONLY = set(sys.argv[1:])

STOP = set("og i på av til for med som er det den en et å at om har kan ikke du de vi fra eller men så når hva hvor seg sin der også mer bare".split())
SYN = {"mus": "mus musefelle gnagere", "rotte": "rotte rottefelle rotter gnagere", "skogmus": "mus gnagere", "veggedyr": "veggedyr", "svaletege": "veggedyr tege",
       "skjeggkre": "skjeggkre sølvkre", "solvkre": "sølvkre skjeggkre", "veps": "veps vepsebol", "kjempetreveps": "treveps", "stokkmaur": "maur stokkmaur",
       "skogsmaur": "maur", "jordmaur": "maur", "melmoll": "møll matmøll melmøll", "kakerlakk": "kakerlakk", "flatt": "flått"}


def toks(s):  # enkel stemming: de første 6 bokstavene (grevling/grevlinger, sølvkre/sølvkreet)
    return [w[:6] for w in re.findall(r"[a-zæøå]{3,}", s.lower()) if w not in STOP]


docs = [toks(" ".join([p["name"]] * 3 + p["category"] * 2 + [p["description"], p.get("text", "")[:600]])) for p in CAT]
df = collections.Counter(w for d in docs for w in set(d))
N = len(docs)


def candidates(query, k=60):
    q = collections.Counter(toks(query))
    scores = []
    for i, d in enumerate(docs):
        c = collections.Counter(d); L = len(d) or 1
        s = sum(qw * (c[w] * 2.2 / (c[w] + 1.2 * (0.25 + 0.75 * L / 120))) * math.log(1 + N / (1 + df[w])) for w, qw in q.items() if w in c)
        if s > 0: scores.append((s, i))
    return [i for _, i in sorted(scores, reverse=True)[:k]]


def gemini(prompt):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}}
    for m in MODELS:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", data=json.dumps(body).encode(),
                                       headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            d = json.load(urllib.request.urlopen(r, timeout=120))
            return json.loads("".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]))
        except Exception as e:
            print("   ", m, str(e)[:150])
    return {}


def strip(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or ""))


# Produkter artiklene sier ikke virker, eller som ikke kan selges til private (giftforbud fra juni 2026).
BLOCK = re.compile(r"ultralyd|vibrasjon|lavfrekvent|elektronisk skremm|avvisende spray|repellent|møllkul|huggormfri|hoggorm.{0,20}skremm|jordrotteskremm", re.I)
RODENTICIDE = re.compile(r"\båte\b|gift|rodenticid|bromadiolon|difenakum|brodifakum", re.I)

pages = {}
for a in ARTICLES:
    pages[f"art:{a['slug']}"] = (a["title"], f"{a['title']}. {a['lead']} {strip(a['body'])[:2500]}")
for s in KB:
    pages[f"sp:{s['id']}"] = (s["name"], f"{s['name']} ({s['latin']}). {SYN.get(s['id'], '')}. Kjennetegn: {'; '.join(s['features'])}. Skadedyr: {'ja' if s['pest'] else 'nei, skal ikke bekjempes'}.")
REG = {"ost": "Østlandet: mus i hus og hytte, rotter i byene, stokkmaur, skjeggkre i leiligheter, flått, veps", "sor": "Sørlandet: flått langs kysten, mus i sjøhytter, veps, maur, brunsnegl",
       "vest": "Vestlandet: fukt, skjeggkre og sølvkre, rotter, mus, måker på taket, brunsnegl", "midt": "Midt-Norge: mus og smågnagere i hus, hytte og gårdsbruk, stokkmaur, husbukk",
       "nord": "Nord-Norge: smågnagerår med mye mus og lemen, mus på hytta, mygg og fluer, måker"}
for r, q in REG.items():
    pages[f"reg:{r}"] = (r, q)
pages["tool:tett-huset"] = ("Tett huset", "Tett huset mot mus og rotter: tetningsnett, stålull, gnagersikker tetningsskum, børstelister for dører, ventilgitter, musenett, overvåkingsfeller.")
pages["tool:fellekalkulator"] = ("Fellekalkulator", "Antall musefeller og rottefeller: slagfeller, klappfeller, åtestasjoner, levendefeller, overvåking i kjeller og loft.")
pages["hytte:fjell"] = ("Fjellhytte", "Fjellhytte: mus om vinteren, tette hull, musefeller som står mens hytta er tom, overvåking, vintersikring.")
pages["hytte:sjo"] = ("Sjøhytte", "Hytte ved sjøen: stenge for vinteren mot mus og rotter, tetting, feller mens hytta står tom, veps og maur om våren og sommeren.")

old = json.loads(OUT.read_text()) if OUT.exists() else {}
recs = dict(old)
for key, (title, text) in pages.items():
    if ONLY and key not in ONLY: continue
    cand = candidates(text)
    if not cand: print(key, "ingen kandidater"); continue
    listing = [{"id": n, "name": CAT[i]["name"], "kategori": "/".join(CAT[i]["category"]), "pris": CAT[i]["price"], "beskrivelse": CAT[i]["description"][:260]}
               for n, i in enumerate(cand)]
    prompt = f"""Du er produktansvarlig for Kryp.as og velger utstyr fra Skadedyrbutikken til denne siden.
SIDE: {title}
INNHOLD: {text[:3000]}

Velg 4–6 produkter fra KANDIDATENE (minst 3 hvis det finnes så mange som passer) som passer nøyaktig til problemet på siden – riktig dyr, riktig sted (inne/ute/hytte) og det siden faktisk anbefaler.
Regler:
- Bare produkter som virker mot akkurat dette dyret. Aldri et produkt for et annet dyr (f.eks. ikke musefelle på en flåttside, ikke åte mot maur på en skjeggkreside).
- Følg rådene på siden: anbefaler den mekaniske feller og tetting framfor gift, velg det.
- Ikke produkter som krever godkjenning/sertifikat eller er «kun for profesjonelle».
- Ikke gift mot gnagere (musegift/rottegift/åte med rodenticid): salg til privatpersoner er forbudt fra juni 2026.
- Ikke produkter siden sier har usikker eller ingen dokumentert effekt (f.eks. møllkuler av sedertre, skremmere med lyd/vibrasjon, avvisende spray).
- Ikke ultralydskremmere mot gnagere eller insekter (FHI: dårlig dokumentert effekt).
- Levende fangst av vilt (f.eks. grevling) krever tillatelse – velg heller skremsel/avvisning og tetting, og nevn aldri at fellen kan brukes fritt.
- Siden handler om en art som ikke er et skadedyr eller er fredet/vernet (f.eks. grevling, flaggermus, humler, hoggorm): velg bare forebygging, skremsel, tetting eller verneutstyr – aldri noe som dreper dyret. Finnes ikke noe passende: returner tom liste.
- Varier: hovedtiltaket først, så forebygging/tetting, overvåking eller verneutstyr.
- role: ett av «Bekjemp», «Forebygg», «Tett», «Overvåk», «Beskytt», «Fang levende», «Skrem bort».
- why: hvorfor akkurat dette produktet passer her, maks 14 ord, norsk, ingen superlativer, ikke finn på egenskaper som ikke står i beskrivelsen.
Svar som JSON: {{"picks":[{{"id":0,"role":"","why":""}}]}}

KANDIDATER:
{json.dumps(listing, ensure_ascii=False)}"""
    res = gemini(prompt)
    out = res.get("picks", []) if isinstance(res, dict) else res if isinstance(res, list) else []
    chosen, used = [], set()
    for p in out:
        if not isinstance(p, dict): continue
        i = p.get("id")
        if not isinstance(i, int) or i >= len(cand) or i in used: continue
        prod = CAT[cand[i]]
        if not prod.get("available", True) or re.search(r"proff|profesjonell|sertifi", "/".join(prod["category"]) + prod["name"], re.I): continue
        if BLOCK.search(prod["name"]): continue
        if re.search(r"gnager|mus|rotte", "/".join(prod["category"]), re.I) and RODENTICIDE.search(prod["name"]): continue
        used.add(i)
        chosen.append({"url": prod["url"], "name": prod["name"], "price": prod["price"], "image": prod["image"], "role": p.get("role", ""), "why": p.get("why", "")})
    recs[key] = chosen[:6]
    print(f"{key}: " + " | ".join(f"{c['role']}: {c['name']}" for c in chosen[:6]))

OUT.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
print("skrev", len(recs), "sider")
