"""Henter produktkatalogen fra skadedyrbutikken.no til data/products.json.
Prøver sitemap først, ellers kryper den gjennom /produkter/-kategoriene. Leser JSON-LD Product, Open Graph og itemprop."""
import collections, html as H, json, pathlib, re, sys, time, urllib.parse, urllib.request

BASE = "https://skadedyrbutikken.no"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data/products.json"
UA = {"User-Agent": "Mozilla/5.0 (Kryp.as produktkatalog)", "Accept-Language": "nb-NO"}
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 2500


def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
            return r.geturl(), r.read().decode("utf-8", "replace")
    except Exception as e:
        print("  fail", u, str(e)[:80]); return u, ""


def meta(h, key):
    m = re.search(rf'<meta[^>]+(?:property|name|itemprop)=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']*)', h, re.I) or \
        re.search(rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:property|name|itemprop)=["\']{re.escape(key)}["\']', h, re.I)
    return H.unescape(m.group(1)).strip() if m else ""


def ld_products(h):
    out = []
    for raw in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        try: d = json.loads(raw.strip())
        except Exception: continue
        stack = d if isinstance(d, list) else [d]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type"); t = t if isinstance(t, list) else [t]
                if "Product" in t: out.append(x)
                stack += [v for v in x.values() if isinstance(v, (dict, list))]
            elif isinstance(x, list): stack += x
    return out


def text(h):
    h = re.sub(r"<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def product(url, h):
    lds = ld_products(h)
    p = lds[0] if len(lds) == 1 else {}
    offers = p.get("offers") or {}
    if isinstance(offers, list): offers = offers[0] if offers else {}
    price = offers.get("price") or meta(h, "product:price:amount") or meta(h, "price")
    if not price:
        m = re.search(r'itemprop=["\']price["\'][^>]*content=["\']([\d.,]+)', h) or re.search(r'(\d[\d .]*,\d{2})\s*(?:kr|NOK)', h)
        price = m.group(1) if m else ""
    cart = re.search(r'add.?to.?cart|legg i handlekurv|kjøp nå|AddToCart|cartcmd=add', h, re.I)
    if not (p or (price and cart and len(lds) <= 1)): return None
    name = p.get("name") or meta(h, "og:title") or (re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S) or [None, ""])[1]
    name = re.sub(r"\s*[|–-]\s*Skadedyrbutikken.*$", "", re.sub("<[^>]+>", "", H.unescape(str(name)))).strip()
    img = p.get("image"); img = img[0] if isinstance(img, list) else img
    img = (img.get("url") if isinstance(img, dict) else img) or meta(h, "og:image")
    desc = p.get("description") or meta(h, "og:description") or meta(h, "description")
    path = urllib.parse.urlparse(url).path.strip("/").split("/")
    brand = p.get("brand"); brand = brand.get("name", "") if isinstance(brand, dict) else (brand or "")
    return {"url": url, "name": name, "price": str(price).replace(" ", ""), "image": urllib.parse.urljoin(BASE, img or ""), "brand": brand,
            "sku": p.get("sku", ""), "category": path[1:-1], "description": re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", H.unescape(str(desc))))[:700],
            "available": "OutOfStock" not in str(offers.get("availability", "")), "text": text(h)[:1500]}


def links(u, h):
    for href in re.findall(r'href=["\']([^"\'#]+)', h):
        v = urllib.parse.urljoin(u, H.unescape(href)).split("?")[0].rstrip("/")
        if v.startswith(BASE + "/produkter/") and not re.search(r"\.(jpg|png|pdf|webp|svg)$", v, re.I): yield v


seeds = [BASE + "/produkter/" + c for c in ["gnagere", "insekter", "fugler", "andre-dyr", "inneklima", "hus-og-hage", "verktoey-og-verneutstyr",
         "rengjoering-og-hygiene", "elektrisk-insektfanger", "proff-produkter", "rentokil-produkter", "lagersalg"]]
_, robots = get(BASE + "/robots.txt"); print("robots.txt:", robots[:300].replace("\n", " | "))
sm = re.findall(r"(?im)^sitemap:\s*(\S+)", robots) or [BASE + "/sitemap.xml"]
smurls, todo = set(), list(sm)
while todo:
    _, x = get(todo.pop())
    for l in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x):
        l = H.unescape(l)
        if l.endswith(".xml"): todo.append(l)
        elif "/produkter/" in l: smurls.add(l.split("?")[0].rstrip("/"))
print("sitemap product-ish urls:", len(smurls))

seen, q, products = set(), collections.deque(sorted(smurls) + seeds), {}
while q and len(seen) < MAX:
    u = q.popleft()
    if u in seen: continue
    seen.add(u)
    final, h = get(u)
    if not h: continue
    p = product(final, h)
    if p and p["name"]: products[p["url"]] = p
    else:
        for v in links(final, h):
            if v not in seen: q.append(v)
    if len(seen) % 100 == 0: print(f"  {len(seen)} sider, {len(products)} produkter, kø {len(q)}")
    time.sleep(0.25)

items = sorted(products.values(), key=lambda p: p["url"])
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps({"updated": time.strftime("%Y-%m-%d"), "count": len(items), "products": items}, ensure_ascii=False, indent=0), encoding="utf-8")
print("produkter:", len(items), "| sider besøkt:", len(seen))
for p in items[:20]: print(" -", p["name"], "|", p["price"], "|", "/".join(p["category"]))
