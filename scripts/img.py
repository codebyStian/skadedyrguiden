"""Bilder i riktig størrelse: srcset/sizes for bildene i site/assets/img.

Originalene er 1200–1500 px brede. scripts/img_variants.py lager mindre utgaver av hvert bilde:
  s/<navn>-320|480|680|800.webp  maks 320–800 px bred (kort, miniatyrer, toppbilder på mobil)
  p/<navn>-320|640.webp  stående 3:4-utsnitt (artskortene på forsiden)
  m/<navn>.webp          stående utsnitt til forsidebildet på mobil
Funksjonene her brukes av sidebyggerne (page.py, extra.py, lexicon.py). De leser bildemålene rett fra WebP-filene
(ingen avhengigheter) og legger bare til srcset når den lille utgaven faktisk finnes – ellers brukes originalen som før.
"""
import pathlib

IMG = pathlib.Path(__file__).resolve().parent.parent / "site/assets/img"
_SIZE = {}


def size(path):
    """(bredde, høyde) for en WebP-fil, eller None."""
    path = pathlib.Path(path)
    if path not in _SIZE:
        try:
            with open(path, "rb") as f: b = f.read(32)
            if b[:4] != b"RIFF" or b[8:12] != b"WEBP": raise ValueError
            c = b[12:16]
            if c == b"VP8 ": wh = (int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF)
            elif c == b"VP8L": n = int.from_bytes(b[21:25], "little"); wh = ((n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1)
            elif c == b"VP8X": wh = (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
            else: raise ValueError
            _SIZE[path] = wh
        except Exception:
            _SIZE[path] = None
    return _SIZE[path]


# Hvor bredt bildet vises (CSS-piksler) i hver plassering, fra smal til bred skjerm, formatet på bildeflaten, og om
# originalen skal være med som største valg. Tallene følger rutenettene i site.css og er kontrollmålt i nettleser på
# 390 px og 1440 px bredde. Kort og miniatyrer får aldri mer enn 800 px: mer synes ikke på så små flater, selv på skjermer
# med 3x tetthet, og originalene veier to–tre ganger så mye. Toppbildene kan gå helt opp til originalen.
SLOTS = {
    "ahero": ([("max-width:860px", 90, "vw"), ("max-width:1377px", 47, "vw"), (None, 620, "px")], 4 / 3, True),     # toppbilde i artikkel og podkast
    "lxhero": ([("max-width:900px", 100, "vw"), ("max-width:1240px", 47, "vw"), (None, 581, "px")], 4 / 3, True),   # toppbilde på artssidene
    "also":  ([("max-width:640px", 46, "vw"), (None, 224, "px")], 4 / 3, False),                                     # «Les også»
    "agrid": ([("max-width:646px", 90, "vw"), ("max-width:981px", 45, "vw"), ("max-width:1317px", 30, "vw"), (None, 294, "px")], 4 / 3, False),  # artikkeloversikten
    "lxg":   ([("max-width:590px", 90, "vw"), ("max-width:892px", 45, "vw"), ("max-width:1195px", 30, "vw"), (None, 301, "px")], 4 / 3, False),  # leksikonoversikten
    "cmp":   ([("max-width:900px", 50, "vw"), (None, 422, "px")], 4 / 3, False),                                     # side-om-side-sammenligning
    "rel":   ([("max-width:560px", 100, "vw"), ("max-width:900px", 50, "vw"), (None, 272, "px")], 16 / 10, False),   # «Hva gjør jeg?»-kort på artssidene
    "thumb": ([(None, 96, "px")], 4 / 3, False),                                                                     # 96 px miniatyr i tabell
}


def rs(name, slot, base):
    """Attributtene srcset og sizes (med innledende mellomrom) for bildet <navn> i en gitt plassering.
    base er stien til bildemappen sett fra siden, f.eks. "../assets/img/".
    Tom streng hvis de små utgavene mangler – da laster nettleseren originalen fra src, som før."""
    big = size(IMG / f"{name}.webp")
    if not big: return ""
    cands = []                               # (bredde, sti) for utgavene som finnes, minst først
    for w in (320, 480, 680, 800):
        v = size(IMG / "s" / f"{name}-{w}.webp")
        if v and v[0] <= big[0] and (not cands or v[0] > cands[-1][0]): cands.append((v[0], f"{base}s/{name}-{w}.webp"))
    if not cands: return ""
    widths, aspect, full = SLOTS[slot]
    if full and big[0] > cands[-1][0]: cands.append((big[0], f"{base}{name}.webp"))
    # Bildet fyller flaten (object-fit: cover). Er bildet bredere i formatet enn flaten, må det være tilsvarende bredere.
    grow = max(1.0, (big[0] / big[1]) / aspect)
    sizes = ", ".join((f"({m}) " if m else "") + f"{round(v * grow)}{u}" for m, v, u in widths)
    return f' srcset="{", ".join(f"{u} {w}w" for w, u in cands)}" sizes="{sizes}"'
