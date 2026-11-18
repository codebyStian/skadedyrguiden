"""Lager site/data/norge.json (SVG-stier + forenklede polygoner) fra data/src/fylker-2024.geojson.
Kilde: Kartverket via github.com/robhop/fylker-og-kommuner (CC BY 4.0).
Projeksjon: sinusoidal rundt 15°Ø – samme formel brukes i nettleseren (x=(lon-15)*cos(lat), y=-lat)."""
import json, math, pathlib
from shapely.geometry import shape, Polygon, MultiPolygon, mapping
from shapely.ops import transform, unary_union

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data/src/fylker-2024.geojson"
OUT = ROOT / "site/data/norge.json"

REGION = {"03": "ost", "31": "ost", "32": "ost", "33": "ost", "34": "ost", "39": "ost", "40": "ost",
          "42": "sor", "11": "vest", "46": "vest", "15": "vest", "50": "midt", "18": "nord", "55": "nord", "56": "nord"}
NAMES = {"ost": "Østlandet", "sor": "Sørlandet", "vest": "Vestlandet", "midt": "Trøndelag", "nord": "Nord-Norge"}

def proj(lon, lat, z=None):
    return ((lon - 15) * math.cos(math.radians(lat)), -lat)

feats = json.load(open(SRC))["features"]
geoms = {}
for f in feats:
    g = shape(f["geometry"]).buffer(0)
    geoms[f["properties"]["fylkesnummer"]] = (f["properties"]["fylkesnavn"].split(" - ")[0], g)

allp = unary_union([transform(proj, g) for _, g in geoms.values()])
minx, miny, maxx, maxy = allp.bounds
S = 1000 / (maxy - miny); PAD = 10
W = round((maxx - minx) * S + 2 * PAD); H = round((maxy - miny) * S + 2 * PAD)
def px(x, y): return (round((x - minx) * S + PAD, 1), round((y - miny) * S + PAD, 1))

def big_parts(g, min_area):
    parts = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    keep = [p for p in parts if p.area >= min_area] or [max(parts, key=lambda p: p.area)]
    return keep

def svg_path(g):
    out = []
    for p in big_parts(g, 0.0004):
        for ring in [p.exterior]:
            pts = [px(x, y) for x, y in ring.coords]
            out.append("M" + "L".join(f"{a:g},{b:g}" for a, b in pts[:-1]) + "Z")
    return "".join(out)

res = {"viewBox": [0, 0, W, H], "proj": {"minx": minx, "miny": miny, "S": S, "PAD": PAD}, "regions": NAMES, "fylker": []}
for fid, (name, g) in sorted(geoms.items()):
    pg = transform(proj, g).simplify(0.006, preserve_topology=True)
    ll = g.simplify(0.02, preserve_topology=True)
    polys = [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in big_parts(ll, 0.003)]
    hull = g.convex_hull.simplify(0.05)
    ring = list(hull.exterior.coords)
    if Polygon(ring).exterior.is_ccw is False: ring = ring[::-1]
    c = g.representative_point()
    res["fylker"].append({"id": fid, "name": name, "region": REGION[fid], "d": svg_path(pg),
                          "c": [round(c.x, 3), round(c.y, 3)], "poly": polys,
                          "wkt": "POLYGON((" + ",".join(f"{x:.2f} {y:.2f}" for x, y in ring) + "))"})
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")))
print(OUT, OUT.stat().st_size // 1024, "KB", W, H)
