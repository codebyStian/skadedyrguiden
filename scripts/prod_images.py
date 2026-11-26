"""Små produktbilder til produktkortene.

Produktbildene hos Skadedyrbutikken er originalfiler på opptil 1,7 MB (snitt ca. 350 kB), mens Kryp.as viser dem i
kort på 70–240 px. Dette skriptet henter hvert bilde som er i bruk i site/data/recs.json og lager to WebP-utgaver i
site/assets/prod/: én på maks 480 px (store kort og skarpe skjermer) og én på maks 240 px (kortene på mobil, der
bildet er 80 px bredt). Stiene (thumb, thumb_s) og målene (tw, th, tsw) skrives inn i recs.json.

Sidene bruker miniatyren. Mangler den, brukes butikkens egen nedskalering (prod_img i page.py, pimg i app.js) –
originalfilen lenkes aldri direkte.

Kjør: python scripts/prod_images.py          (krever pillow og nett; kjøres av .github/workflows/shop.yml)
      python scripts/prod_images.py --force  (lag alle på nytt)
"""
import hashlib, io, json, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageOps

REPO = pathlib.Path(__file__).resolve().parent.parent
RECS = REPO / "site/data/recs.json"
OUT = REPO / "site/assets/prod"
CACHE = REPO / "data/prod_thumbs.json"   # hva hver miniatyr er laget fra, så uendrede bilder ikke hentes på nytt
HOST = "skadedyrbutikken.no"
SIZE, QUALITY = 480, 80                    # lengste side i piksler (2x av største visning) og WebP-kvalitet
SMALL = 240                                # liten utgave: 3x av bildet i mobilkortet, 1x av de store kortene
MAX_BYTES = 25 * 1024 * 1024
UA = {"User-Agent": "Mozilla/5.0 (Kryp.as produktbilder)"}


def filename(url):
    """Lesbart, stabilt filnavn: navnet på originalen + kort hash av hele adressen (to bilder kan hete det samme)."""
    stem = urllib.parse.unquote(urllib.parse.urlsplit(url).path).rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
    for a, b in (("æ", "ae"), ("ø", "o"), ("å", "a")): stem = stem.replace(a, b)
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")[:60] or "produkt"
    return f"{stem}-{hashlib.sha1(url.encode()).hexdigest()[:6]}.webp"


def request(url, method="GET"):
    p = urllib.parse.urlsplit(url)
    safe = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path), safe="/"), p.query, ""))
    return urllib.request.urlopen(urllib.request.Request(safe, headers=UA, method=method), timeout=30)


def validator(url):
    """Etag/dato/størrelse fra et HEAD-kall. None = fikk ikke kontakt, "" = serveren oppgir ingenting."""
    try:
        with request(url, "HEAD") as r:
            return "|".join(r.headers.get(k) or "" for k in ("ETag", "Last-Modified", "Content-Length")).strip("|")
    except urllib.error.HTTPError as e:
        return "" if e.code in (405, 501) else None      # serveren støtter ikke HEAD: hent bildet på vanlig måte
    except Exception:
        return None


def download(url):
    for attempt in range(3):
        try:
            with request(url) as r:
                data = r.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES: raise ValueError("for stor fil")
            return data
        except Exception as e:
            err = e; time.sleep(1 + attempt)
    raise err


def thumbnail(data):
    im = Image.open(io.BytesIO(data)); im.load()
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")                      # gjennomsiktig bakgrunn blir hvit (kortet legger bildet «multiply» på lys flate)
        bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.getchannel("A")); im = bg
    else:
        im = im.convert("RGB")
    def webp(i):
        out = io.BytesIO(); i.save(out, "WEBP", quality=QUALITY, method=6); return out.getvalue()
    small, sw = None, 0
    if max(im.size) > SMALL:                         # den lille lages fra originalen, ikke fra den store miniatyren
        s = im.copy(); s.thumbnail((SMALL, SMALL), Image.LANCZOS); small, sw = webp(s), s.width
    im.thumbnail((SIZE, SIZE), Image.LANCZOS)        # skalerer bare ned, beholder formatet (ingen beskjæring)
    return webp(im), im.width, im.height, small, sw


def main():
    force = "--force" in sys.argv
    recs = json.loads(RECS.read_text(encoding="utf-8"))
    before = json.dumps(recs, ensure_ascii=False, sort_keys=True)
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    urls = sorted({r["image"] for items in recs.values() for r in items if r.get("image")})
    ok, made, kept, failed = {}, 0, 0, []
    for url in urls:
        p = urllib.parse.urlsplit(url)
        if p.scheme != "https" or p.netloc != HOST:
            failed.append((url, "ligger ikke hos Skadedyrbutikken – hentes ikke")); continue
        old = cache.get(url)
        have = bool(old) and (OUT / old["file"]).is_file() and "small" in old and (not old["small"] or (OUT / old["small"]).is_file())
        v = validator(url)
        if have and not force and (v is None or (v and v == old.get("v"))):
            ok[url] = old; kept += 1; continue           # uendret hos butikken, eller butikken svarer ikke: behold den vi har
        try:
            data = download(url); webp, w, h, small, sw = thumbnail(data)
        except Exception as e:
            if have: ok[url] = old; kept += 1
            else: failed.append((url, str(e)[:80]))
            continue
        f = OUT / filename(url); fs = f.with_name(f.stem + f"-{SMALL}.webp")
        for path, blob in ((f, webp), (fs, small)):
            if blob and (not path.is_file() or path.read_bytes() != blob): path.write_bytes(blob)
        ok[url] = {"file": f.name, "small": fs.name if small else "", "w": w, "h": h, "sw": sw, "v": v or "", "src_bytes": len(data), "bytes": len(webp)}
        made += 1; time.sleep(0.1)

    for items in recs.values():
        for r in items:
            t = ok.get(r.get("image"))
            for k in ("thumb", "tw", "th", "thumb_s", "tsw"): r.pop(k, None)
            if t:
                r.update(thumb=f"assets/prod/{t['file']}", tw=t["w"], th=t["h"])
                if t.get("small"): r.update(thumb_s=f"assets/prod/{t['small']}", tsw=t["sw"])
    used = {n for t in ok.values() for n in (t["file"], t.get("small")) if n}
    for f in OUT.glob("*.webp"):
        if f.name not in used: f.unlink()                # produktet er ikke lenger i bruk
    if json.dumps(recs, ensure_ascii=False, sort_keys=True) != before:
        RECS.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    CACHE.write_text(json.dumps(dict(sorted(ok.items())), ensure_ascii=False, indent=0), encoding="utf-8")

    src = sum(t.get("src_bytes", 0) for t in ok.values()); out = sum((OUT / t["file"]).stat().st_size for t in ok.values())
    sm = sum((OUT / (t.get("small") or t["file"])).stat().st_size for t in ok.values())
    print(f"produktbilder: {len(urls)} i bruk, {made} laget, {kept} uendret, {len(failed)} feilet")
    if src: print(f"  originaler {src / 1048576:.1f} MB -> miniatyrer {out / 1048576:.2f} MB ({100 - out * 100 / src:.0f} % mindre), på mobil {sm / 1048576:.2f} MB")
    for url, why in failed:
        print(f"::warning::Ingen miniatyr for {url} ({why}). Sidene faller tilbake til bildet fra butikken.")


if __name__ == "__main__":
    main()
