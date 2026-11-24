"""Henter offentlige data til siden (kjøres i GitHub Actions, ukentlig):
- FHI Statistikk Open API: skadedyrstatistikken (antall bekjempelser per år og måned).
  FHI publiserer statistikken årlig, i etterkant. Vi bruker de to siste hele årene (MONTH_YEARS),
  ikke snittet fra 2007, fordi bildet har endret seg de siste årene.
  Statistikken gjelder 11 utvalgte skadeinsekter – mus og rotter er ikke med.
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


def jsonstat_rows(d):
    """Gjør json-stat2 om til en liste av dict med kategorietiketter."""
    ids = d["id"]; sizes = d["size"]; vals = d["value"]
    cats = []
    for k in ids:
        c = d["dimension"][k]["category"]
        idx = c["index"]; order = sorted(idx, key=lambda x: idx[x]) if isinstance(idx, dict) else idx
        cats.append([c["label"][o] for o in order])
    rows = []
    for n, v in enumerate(vals if isinstance(vals, list) else []):
        r, rem = {}, n
        for k, sz, cl in zip(reversed(ids), reversed(sizes), reversed(cats)):
            r[k] = cl[rem % sz]; rem //= sz
        r["v"] = v; rows.append(r)
    return rows


def fhi_parse():
    """Lager {yearly: {art: {år: n}}, monthly: {art: [12 andeler i %]}, years: "2024–2025"} fra råfilene.
    Månedsfordelingen er snittet av de to siste årene, vektet med antall bekjempelser hvert år."""
    out = {"source": "FHI Statistikk – Skadedyrstatistikk (statistikk.fhi.no/skast)", "scope": "11 utvalgte skadeinsekter. Mus og rotter er ikke med.",
           "yearly": {}, "monthly": {}}
    per_year = {}
    for f in RAW.glob("fhi_skast_*_data.json"):
        d = json.loads(f.read_text())
        rows = jsonstat_rows(d)
        if "MND" in d["id"]:
            for r in rows:
                if r["AAR"].isdigit() and r["v"] is not None:
                    per_year.setdefault(r["ART"].replace(" og ", " eller "), {}).setdefault(r["AAR"], {})[r["MND"]] = r["v"]
        else:
            for r in rows:
                if r["v"] is not None and r["AAR"].isdigit():
                    out["yearly"].setdefault(r["ART"], {})[r["AAR"]] = r["v"]
    M = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]
    last = max(int(y) for a in out["yearly"].values() for y in a)
    years = [str(last - 1), str(last)]
    out["years"] = f"{years[0]}–{years[1]}"
    for art, by in per_year.items():
        w = {y: (out["yearly"].get(art, {}).get(y) or 0) for y in years if y in by}
        tot = sum(w.values())
        if not w: continue
        out["monthly"][art] = [round(sum((by[y].get(m) or 0) * (w[y] if tot else 1) for y in w) / (tot or len(w)), 1) for m in M]
    return out


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


def main():
    stats = {"updated": datetime.date.today().isoformat()}
    try:
        stats["fhi_tables"] = fhi()
    except Exception as e:
        print("FHI failed:", e)
    try:
        stats["fhi"] = fhi_parse()
    except Exception as e:
        print("FHI parse failed:", e)
    f = ROOT / "site/data/stats.json"
    prev = json.loads(f.read_text()) if f.exists() else {}
    prev.update(stats)
    prev.pop("gbif", None)
    f.write_text(json.dumps(prev, ensure_ascii=False, indent=1))


main()
