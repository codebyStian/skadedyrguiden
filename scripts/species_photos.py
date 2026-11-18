"""Ekte artsfoto med fri lisens fra Wikimedia Commons (via Wikidata P18, ellers Commons-søk).
Godtar bare CC0, Public domain, CC BY og CC BY-SA. Lagrer site/assets/img/foto-<id>.webp og site/data/photos.json med fotograf, lisens og lenke.
Bildene brukes uendret (bare skalert), med kreditering ved bildet."""
import html as H, io, json, pathlib, re, urllib.parse, urllib.request
from PIL import Image

REPO = pathlib.Path(__file__).resolve().parent.parent
IMG = REPO / "site/assets/img"; OUT = REPO / "site/data/photos.json"
UA = {"User-Agent": "Skadedyrguiden/1.0 (https://codebystian.github.io/skadedyrguiden; species photos)"}
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


# Arter der Commons-bildet var dårlig: hent fra iNaturalist (forskningsgodkjente observasjoner, lisens som tillater kommersiell bruk).
INAT = {"stokkmaur", "jordmaur", "kakerlakk", "rotte"}


def inat(taxon):
    t = api("https://api.inaturalist.org/v1/taxa", q=taxon, rank="species", per_page=1)["results"]
    if not t: return None
    obs = api("https://api.inaturalist.org/v1/observations", taxon_id=t[0]["id"], quality_grade="research", photo_license="cc0,cc-by,cc-by-sa",
              order_by="votes", per_page=10, photos="true")["results"]
    for o in obs:
        for ph in o.get("photos", []):
            if (ph.get("license_code") or "") in ("cc0", "cc-by", "cc-by-sa"):
                code = ph["license_code"]
                return {"file": f"iNaturalist foto {ph['id']}", "thumb": ph["url"].replace("square", "large"), "page": f"https://www.inaturalist.org/photos/{ph['id']}",
                        "license": {"cc0": "CC0", "cc-by": "CC BY 4.0", "cc-by-sa": "CC BY-SA 4.0"}[code],
                        "license_url": {"cc0": "https://creativecommons.org/publicdomain/zero/1.0/", "cc-by": "https://creativecommons.org/licenses/by/4.0/", "cc-by-sa": "https://creativecommons.org/licenses/by-sa/4.0/"}[code],
                        "author": re.sub(r"^\(c\)\s*|,.*$", "", ph.get("attribution", "")).strip()[:80] or "iNaturalist-bruker", "w": 1000, "source": "iNaturalist"}
    return None


photos = json.loads(OUT.read_text()) if OUT.exists() else {}
for sid in INAT:
    if photos.get(sid, {}).get("source") != "iNaturalist": photos.pop(sid, None)
for sid, taxon in TAXON.items():
    if sid in photos and (IMG / f"foto-{sid}.webp").exists(): continue
    got = inat(taxon) if sid in INAT else None
    for fn in ([] if got else list(p18(taxon)) + list(search(taxon))):
        try:
            got = info(fn)
        except Exception as e:
            print("  ", fn, e); continue
        if got and got["w"] >= 800: break
        got = None
    if not got: print(sid, "fant ikke fritt lisensiert bilde"); continue
    raw = urllib.request.urlopen(urllib.request.Request(got["thumb"], headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((1400, 1400))
    im.save(IMG / f"foto-{sid}.webp", "WEBP", quality=84)
    got.pop("thumb"); got.pop("w"); got["taxon"] = taxon
    photos[sid] = got
    print(sid, "->", got["file"], "|", got["license"], "|", got["author"])
OUT.write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(photos), "foto")
