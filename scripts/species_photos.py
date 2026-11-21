"""Ekte artsfoto med fri lisens fra Wikimedia Commons (via Wikidata P18, ellers Commons-søk).
Godtar bare CC0, Public domain, CC BY og CC BY-SA. Lagrer site/assets/img/foto-<id>.webp og site/data/photos.json med fotograf, lisens og lenke.
Bildene brukes uendret (bare skalert), med kreditering ved bildet."""
import html as H, io, json, pathlib, re, urllib.parse, urllib.request
from PIL import Image

REPO = pathlib.Path(__file__).resolve().parent.parent
IMG = REPO / "site/assets/img"; OUT = REPO / "site/data/photos.json"
UA = {"User-Agent": "Skadedyrguiden/1.0 (https://kryp.as; species photos)"}
TAXON = {"mus": "Mus musculus", "skogmus": "Apodemus sylvaticus", "rotte": "Rattus norvegicus", "veggedyr": "Cimex lectularius", "svaletege": "Oeciacus hirundinis",
         "skjeggkre": "Ctenolepisma longicaudatum", "solvkre": "Lepisma saccharinum", "veps": "Vespula vulgaris", "kjempetreveps": "Urocerus gigas",
         "stokkmaur": "Camponotus herculeanus", "skogsmaur": "Formica rufa", "jordmaur": "Lasius niger", "melmoll": "Plodia interpunctella",
         "kakerlakk": "Blattella germanica", "flatt": "Ixodes ricinus"}
OK = re.compile(r"^(cc0|pd|public domain|cc[- ]by(-sa)?[- ]?\d|cc[- ]by(-sa)?$)", re.I)


def api(url, **p):
    return json.load(urllib.request.urlopen(urllib.request.Request(url + "?" + urllib.parse.urlencode({**p, "format": "json"}), headers=UA), timeout=30))


def info(filename):
    d = api("https://commons.wikimedia.org/w/api.php", action="query", titles="File:" + filename, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1400)
    page = next(iter(d["query"]["pages"].values()))
    ii = (page.get("imageinfo") or [None])[0]
    if not ii: return None
    m = ii.get("extmetadata", {})
    g = lambda k: re.sub(r"<[^>]+>", "", H.unescape(m.get(k, {}).get("value", ""))).strip()
    lic = g("LicenseShortName")
    if not OK.search(lic): return None
    return {"file": filename, "thumb": ii.get("thumburl") or ii["url"], "page": ii["descriptionurl"], "license": lic, "license_url": g("LicenseUrl"),
            "author": re.sub(r"\s+", " ", g("Artist"))[:80] or "Ukjent", "w": ii.get("width", 0)}


def p18(taxon):
    d = api("https://www.wikidata.org/w/api.php", action="wbsearchentities", search=taxon, language="en", type="item", limit=3)
    for hit in d.get("search", []):
        e = api("https://www.wikidata.org/w/api.php", action="wbgetentities", ids=hit["id"], props="claims")
        for c in e["entities"][hit["id"]]["claims"].get("P18", []):
            yield c["mainsnak"]["datavalue"]["value"]


def search(taxon):
    d = api("https://commons.wikimedia.org/w/api.php", action="query", list="search", srsearch=f'"{taxon}" filetype:bitmap', srnamespace=6, srlimit=10)
    for s in d["query"]["search"]:
        yield s["title"].removeprefix("File:")


LIC = {"cc0": ("CC0", "https://creativecommons.org/publicdomain/zero/1.0/"), "cc-by": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
       "cc-by-sa": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/")}


def inat_cands(taxon, n=8):
    t = api("https://api.inaturalist.org/v1/taxa", q=taxon, per_page=1)["results"]
    if not t: return []
    out = []
    dp = t[0].get("default_photo") or {}
    obs = api("https://api.inaturalist.org/v1/observations", taxon_id=t[0]["id"], quality_grade="research", photo_license="cc0,cc-by,cc-by-sa",
              order_by="votes", per_page=30, photos="true")["results"]
    phs = ([dp] if dp else []) + [ph for o in obs for ph in o.get("photos", [])[:1]]
    for ph in phs:
        code = ph.get("license_code") or ""
        if code not in LIC or not ph.get("url"): continue
        out.append({"file": f"iNaturalist foto {ph['id']}", "thumb": ph["url"].replace("square", "large"), "small": ph["url"].replace("square", "medium"),
                    "page": f"https://www.inaturalist.org/photos/{ph['id']}", "license": LIC[code][0], "license_url": LIC[code][1], "source": "iNaturalist",
                    "author": re.sub(r"^\(c\)\s*|,.*$", "", ph.get("attribution", "")).strip()[:80] or "iNaturalist-bruker", "w": 1000})
        if len(out) >= n: break
    return out


def commons_cands(taxon, n=5):
    out = []
    for fn in list(p18(taxon)) + list(search(taxon)):
        try: c = info(fn)
        except Exception: continue
        if c and c["w"] >= 800:
            c["small"] = c["thumb"]; c["source"] = "Wikimedia Commons"; out.append(c)
        if len(out) >= n: break
    return out


def pick(sid, name, taxon, cands):
    """Gemini ser på kandidatene og velger det beste identifikasjonsbildet (eller ingen)."""
    import base64, os
    key = os.environ.get("GEMINI_API_KEY")
    if not key or len(cands) < 2: return cands[0] if cands else None
    parts = [{"text": f"""Du velger bilde til et norsk skadedyrleksikon, oppslaget «{name}» ({taxon}).
Under følger {len(cands)} kandidatbilder nummerert fra 0. Vurder hvert: viser det tydelig ett eksemplar av nettopp denne arten, skarpt, hele dyret synlig, god størrelse i bildet, nøytral eller naturlig bakgrunn, egnet til å kjenne igjen arten? Trekk ned for: dyret lite eller delvis skjult, uskarpt, glass/beholder/hånd/sko foran, bare egg/larver, døde/knuste dyr, tegninger, flere arter.
Svar som JSON: {{"best": <nummer eller -1 hvis ingen er gode nok>, "scores": [<0-10 per bilde>], "why": "<kort>"}}"""}]
    keep = []
    for i, c in enumerate(cands):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(c["small"], headers=UA), timeout=40).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((512, 512)); b = io.BytesIO(); im.save(b, "JPEG", quality=80)
        except Exception: continue
        parts += [{"text": f"Bilde {len(keep)}:"}, {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}]
        keep.append(c)
    for m in ["gemini-3.8-flash", "gemini-flash-latest"]:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                data=json.dumps({"contents": [{"role": "user", "parts": parts}], "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}).encode(),
                headers={"Content-Type": "application/json", "x-goog-api-key": key})
            d = json.loads(json.load(urllib.request.urlopen(r, timeout=180))["candidates"][0]["content"]["parts"][0]["text"])
            print(f"  {sid}: best={d.get('best')} scores={d.get('scores')} – {d.get('why', '')[:120]}")
            b = d.get("best", -1)
            return keep[b] if isinstance(b, int) and 0 <= b < len(keep) else None
        except Exception as e:
            print("   ", m, str(e)[:150])
    return keep[0] if keep else None


import os
FORCE = set(filter(None, os.environ.get("REPICK", "").split(",")))
photos = json.loads(OUT.read_text()) if OUT.exists() else {}
for sid, taxon in TAXON.items():
    if sid in photos and (IMG / f"foto-{sid}.webp").exists() and sid not in FORCE and "all" not in FORCE: continue
    name = sid
    got = pick(sid, name, taxon, commons_cands(taxon) + inat_cands(taxon))
    if not got: print(sid, "fant ikke godt nok fritt lisensiert bilde"); photos.pop(sid, None); continue
    raw = urllib.request.urlopen(urllib.request.Request(got["thumb"], headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((1400, 1400))
    im.save(IMG / f"foto-{sid}.webp", "WEBP", quality=84)
    for k in ("thumb", "w", "small"): got.pop(k, None)
    got["taxon"] = taxon
    photos[sid] = got
    print(sid, "->", got["file"], "|", got["license"], "|", got["author"])
OUT.write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(photos), "foto")


# ---------- Beskjæring: dyret skal fylle bildet ----------
def bbox(path):
    import base64, os
    key = os.environ.get("GEMINI_API_KEY")
    if not key: return None
    im = Image.open(path).convert("RGB"); sm = im.copy(); sm.thumbnail((768, 768)); b = io.BytesIO(); sm.save(b, "JPEG", quality=85)
    parts = [{"text": 'Finn hele dyret (inkludert bein, antenner og haletråder) i bildet. Svar som JSON: {"box_2d": [ymin, xmin, ymax, xmax]} med verdier 0–1000.'},
             {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}]
    for m in ["gemini-3.8-flash", "gemini-flash-latest"]:
        try:
            r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                data=json.dumps({"contents": [{"role": "user", "parts": parts}], "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}).encode(),
                headers={"Content-Type": "application/json", "x-goog-api-key": key})
            d = json.loads(json.load(urllib.request.urlopen(r, timeout=120))["candidates"][0]["content"]["parts"][0]["text"])
            box = d["box_2d"] if isinstance(d, dict) else d[0]["box_2d"]
            return [v / 1000 for v in box]
        except Exception as e:
            print("    bbox", m, str(e)[:120])
    return None


for sid in list(photos):
    p = photos[sid]; f = IMG / f"foto-{sid}.webp"
    if p.get("cropped") is not None or not f.exists(): continue
    bx = bbox(f)
    if not bx: continue
    im = Image.open(f).convert("RGB"); W, Hh = im.size
    y0, x0, y1, x1 = bx[0] * Hh, bx[1] * W, bx[2] * Hh, bx[3] * W
    bw, bh = x1 - x0, y1 - y0
    if bw * bh > 0.45 * W * Hh:  # dyret fyller allerede bildet
        p["cropped"] = False; continue
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = max(bw * 1.35, bh * 1.35 * 4 / 3); h = w * 3 / 4          # 4:3 med luft rundt dyret
    w, h = min(w, W), min(h, Hh)
    l = min(max(cx - w / 2, 0), W - w); t = min(max(cy - h / 2, 0), Hh - h)
    crop = im.crop((int(l), int(t), int(l + w), int(t + h)))
    if crop.width < 500: p["cropped"] = False; continue
    crop.save(f, "WEBP", quality=86); p["cropped"] = True
    print(sid, "beskåret til", crop.size)
OUT.write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
