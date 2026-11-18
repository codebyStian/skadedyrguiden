"""Henter offentlige data til siden (kjøres i GitHub Actions, ukentlig):
- FHI Statistikk Open API: skadedyrstatistikken (antall bekjempelser per år og måned)
- GBIF (inkl. Artsdatabanken/Artsobservasjoner): registrerte funn per fylke siste 10 år
Skriver data/raw/*.json (råsvar) og site/data/stats.json (det siden bruker)."""
import json, pathlib, time, datetime, urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"; RAW.mkdir(parents=True, exist_ok=True)
FHI = "https://statistikk-data.fhi.no/api/open/v1"
UA = {"User-Agent": "skadedyrguiden-data/0.1", "Accept": "application/json"}


def get(url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    h = dict(UA); h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        t = r.read().decode("utf-8")
    try:
        return json.loads(t)
    except Exception:
        return t


def save(name, obj):
    (RAW / name).write_text(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=1))


def fhi():
    sources = get(FHI + "/Common/source"); save("fhi_sources.json", sources)
    src = [s for s in sources if "skadedyr" in json.dumps(s, ensure_ascii=False).lower() or "skast" in json.dumps(s).lower()]
    out = {}
    for s in src:
        sid = s.get("id") or s.get("Id")
        tables = get(f"{FHI}/{sid}/table"); save(f"fhi_{sid}_tables.json", tables)
        for t in tables:
            tid = t.get("tableId") or t.get("TableId")
            q = get(f"{FHI}/{sid}/Table/{tid}/query"); save(f"fhi_{sid}_{tid}_query.json", q)
            if isinstance(q, dict):
                q["response"] = {"format": "json-stat2"}
                d = get(f"{FHI}/{sid}/Table/{tid}/data", q); save(f"fhi_{sid}_{tid}_data.json", d)
                out[str(tid)] = t.get("title")
            time.sleep(0.5)
    return out


SPECIES = {"mus": "Mus musculus", "rotte": "Rattus norvegicus", "skjeggkre": "Ctenolepisma longicaudatum",
           "solvkre": "Lepisma saccharinum", "veggedyr": "Cimex lectularius", "veps": "Vespula vulgaris",
           "stokkmaur": "Camponotus herculeanus", "flatt": "Ixodes ricinus"}


def gbif(geo):
    y = datetime.date.today().year
    keys = {}
    for k, name in SPECIES.items():
        m = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": name}))
        keys[k] = m.get("usageKey")
    res = {"years": f"{y-9}-{y}", "keys": keys, "fylker": {}}
    for f in geo["fylker"]:
        row = {}
        for k, key in keys.items():
            qs = urllib.parse.urlencode({"taxonKey": key, "country": "NO", "geometry": f["wkt"], "year": f"{y-9},{y}", "limit": 0})
            try:
                row[k] = get("https://api.gbif.org/v1/occurrence/search?" + qs)["count"]
            except Exception as e:
                row[k] = None; print("gbif", f["id"], k, e)
            time.sleep(0.2)
        res["fylker"][f["id"]] = row
        print("gbif", f["name"], row)
    return res


def main():
    geo = json.loads((ROOT / "site/data/norge.json").read_text())
    stats = {"updated": datetime.date.today().isoformat()}
    try:
        stats["fhi_tables"] = fhi()
    except Exception as e:
        print("FHI failed:", e)
    try:
        stats["gbif"] = gbif(geo)
    except Exception as e:
        print("GBIF failed:", e)
    f = ROOT / "site/data/stats.json"
    prev = json.loads(f.read_text()) if f.exists() else {}
    prev.update(stats)
    f.write_text(json.dumps(prev, ensure_ascii=False, indent=1))


main()
