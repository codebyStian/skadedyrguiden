"""Lager mindre utgaver av bildene i site/assets/img, så sidene ikke laster 1200–1500 px brede bilder til små flater.

  s/<navn>-320|480|680|800.webp  maks 320–800 px bred – kort, miniatyrer, «Les også» og toppbilder på mobil.
                         Fire trinn, så nettleseren finner en utgave nær det skjermen trenger. 680 dekker kort i full
                         bredde på en vanlig Android-telefon (ca. 370 px bredt kort × 1,75 i pikseltetthet = 650 px).
  p/<navn>-320|640.webp  stående 3:4-utsnitt – artskortene på forsiden (bare artsfoto og bildene i PORTRAIT)
  m/<navn>.avif|webp     stående utsnitt til forsidebildet på mobil (bare forsidebildene: hero, by-* og region-*).
                         AVIF er det nettleserne velger; WebP er reserve for eldre nettlesere.

Originalene røres ikke. data/img_variants.json husker hvilken original hver utgave er laget fra, så bare nye eller
endrede bilder lages på nytt. Sidene virker også uten utgavene (da brukes originalen), se scripts/img.py.

Kjør: python scripts/img_variants.py [--force]     (krever pillow 11.3 eller nyere, med AVIF; kjøres av images.yml og species.yml)
"""
import hashlib, io, json, pathlib, sys
from PIL import Image, features

if not features.check("avif"):   # uten AVIF ville mobilutsnittene til forsiden blitt slettet som «ikke lenger i bruk»
    sys.exit("img_variants.py: Pillow mangler AVIF-støtte. Installer pillow>=11.3 (pip install -U pillow).")

REPO = pathlib.Path(__file__).resolve().parent.parent
IMG = REPO / "site/assets/img"
STATE = REPO / "data/img_variants.json"
VERSION = 5                                  # øk for å lage alt på nytt etter endret oppskrift
SMALL_W, SMALL_Q = (320, 480, 680, 800), 78
PORTRAIT = {"fluer"}                         # i tillegg til alle foto-*: bilder som vises som 3:4-kort på forsiden
PORTRAIT_W, PORTRAIT_Q = (320, 640), 76
# Detaljrike bilder (gress, løv, bylandskap) blir store selv på god kvalitet. De komprimeres litt hardere, ned til
# MIN_Q, til de er under TARGET_BPP byte per piksel. Grensen ligger like under det PageSpeed Insights regner som
# «godt nok komprimert» (1/6 byte per piksel); de fleste bildene er godt under og kodes på vanlig kvalitet.
MIN_Q, TARGET_BPP = 62, 0.155
HERO_ASPECT = 0.72                           # bredde/høyde på mobilutsnittet
HERO_AVIF_Q, HERO_WEBP_Q = 45, 62            # bildet ligger under mørk toning og tåler mer komprimering enn kortbildene


def webp(im, q, floor=None):
    """WebP på kvalitet q. Med floor: senk kvaliteten i trinn (ikke under floor) til fila er under TARGET_BPP."""
    while True:
        b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6); data = b.getvalue()
        if floor is None or q <= floor or len(data) <= TARGET_BPP * im.width * im.height: return data
        q = max(floor, q - 4)


def avif(im, q):
    b = io.BytesIO(); im.save(b, "AVIF", quality=q, speed=4); return b.getvalue()


def center_crop(im, aspect):
    w, h = im.size
    if w / h > aspect: nw = round(h * aspect); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = round(w / aspect); y = (h - nh) // 2; return im.crop((0, y, w, y + nh))


def variants(name, im):
    """{relativ sti: bytes} for alle utgavene av ett bilde."""
    out = {}
    for w in SMALL_W:
        w2 = min(w, im.width)                # smalere originaler skaleres ikke opp, men kodes mer kompakt
        out[f"s/{name}-{w}.webp"] = webp(im if w2 == im.width else im.resize((w2, round(im.height * w2 / im.width)), Image.LANCZOS), SMALL_Q, MIN_Q)
    if name.startswith("foto-") or name in PORTRAIT:
        c = center_crop(im, 3 / 4)
        for w in PORTRAIT_W:
            w2 = min(w, c.width)             # aldri oppskalering
            out[f"p/{name}-{w}.webp"] = webp(c.resize((w2, round(w2 * 4 / 3)), Image.LANCZOS), PORTRAIT_Q, MIN_Q)
    if name == "hero" or name.startswith(("by-", "region-")):
        c = center_crop(im, HERO_ASPECT)
        out[f"m/{name}.avif"] = avif(c, HERO_AVIF_Q); out[f"m/{name}.webp"] = webp(c, HERO_WEBP_Q)
    return out


def main():
    force = "--force" in sys.argv
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if state.get("version") != VERSION: state = {"version": VERSION, "images": {}}
    seen, made, kept = {}, 0, 0
    for f in sorted(IMG.glob("*.webp")):
        name = f.stem; digest = hashlib.sha1(f.read_bytes()).hexdigest()[:16]
        old = state["images"].get(name)
        if old and old["src"] == digest and not force and all((IMG / p).is_file() for p in old["files"]):
            seen[name] = old; kept += 1; continue
        im = Image.open(f).convert("RGB"); files = variants(name, im)
        for rel, data in files.items():
            p = IMG / rel; p.parent.mkdir(exist_ok=True)
            if not p.is_file() or p.read_bytes() != data: p.write_bytes(data)
        seen[name] = {"src": digest, "files": sorted(files)}; made += 1
    keep = {p for v in seen.values() for p in v["files"]}
    for d in ("s", "p", "m"):
        for p in [*(IMG / d).glob("*.webp"), *(IMG / d).glob("*.avif")] if (IMG / d).is_dir() else []:
            if f"{d}/{p.name}" not in keep: p.unlink()      # originalen er borte eller byttet navn
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps({"version": VERSION, "images": seen}, indent=0, sort_keys=True), encoding="utf-8")
    orig = sum(f.stat().st_size for f in IMG.glob("*.webp")); var = sum((IMG / p).stat().st_size for p in keep)
    print(f"bildeutgaver: {len(seen)} bilder, {made} laget på nytt, {kept} uendret; {len(keep)} filer, {var / 1024:.0f} kB (originaler {orig / 1024:.0f} kB)")


if __name__ == "__main__":
    main()
