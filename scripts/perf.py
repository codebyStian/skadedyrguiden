"""Ytelse for alle sider i site/. Kjøres etter page.py og seo.py: python scripts/perf.py

Endrer ikke utseendet, bare hvordan sidene lastes:
 1. Fontene kommer fra kryp.as selv (assets/fonts/, se fonts.py) i stedet for Google Fonts.
    Det sparer to ekstra tilkoblinger og en CSS-fil som blokkerte visningen.
 2. site.css legges direkte i <head>, så siden kan tegnes uten å vente på en egen CSS-fil.
 3. Bildene får mindre varianter (srcset/sizes), så en mobil ikke laster ned 1500 px brede bilder.
    Variantene lages med Pillow i assets/img/r/ og lages på nytt når originalbildet endres.
 4. Speculation rules: Chrome og Edge forhåndslaster neste side når du holder over en lenke,
    så klikket føles øyeblikkelig.
Idempotent: blokken mellom <!--perf--> og <!--/perf--> byttes ut hver gang.
"""
import hashlib, html as H, json, pathlib, re
from html.parser import HTMLParser

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = REPO / "site"
IMG = SITE / "assets/img"
VAR = IMG / "r"
MANIFEST = VAR / "manifest.json"
WIDTHS = (480, 800, 1200)
Q = 74
# Bilder som brukes som helsides hero på forsiden: får et eget utsnitt for smale mobiler (se index.html og app.js).
HERO = re.compile(r"^(hero|by-.+|region-.+)$")
HERO_ASPECT, HERO_Q = 0.68, 58

FONTS = [  # (familie, stil, vekt, fil, unicode-område, preload)
    ("Schibsted Grotesk", "normal", "400 800", "schibsted-grotesk", "LATIN", True),
    ("Schibsted Grotesk", "normal", "400 800", "schibsted-grotesk-ext", "EXT", False),
    ("Instrument Serif", "normal", "400", "instrument-serif", "LATIN", True),
    ("Instrument Serif", "normal", "400", "instrument-serif-ext", "EXT", False),
    ("Instrument Serif", "italic", "400", "instrument-serif-italic", "LATIN", True),
    ("Instrument Serif", "italic", "400", "instrument-serif-italic-ext", "EXT", False),
]
RANGES = {
    "LATIN": "U+0020-007E,U+00A0-00FF,U+2010-2011,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2039-203A,U+20AC,U+2122,U+2212,U+2009,U+202F,U+2192",
    "EXT": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
}
GOOGLE_FONTS = re.compile(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"(?: crossorigin)?>'
                          r'|<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">\n?')
SITE_CSS = re.compile(r'<link rel="stylesheet" href="(?:\.\./)*assets/site\.css">')
BLOCK = re.compile(r"<!--perf-->.*?<!--/perf-->\n?", re.S)
SPECULATION = ('<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},'
               '{"not":{"href_matches":"/*.mp3"}},{"not":{"href_matches":"/*.json"}},{"not":{"selector_matches":"[download],[rel~=nofollow]"}}]},'
               '"eagerness":"moderate"}]}</script>')

# sizes per sammenheng: nærmeste forelder med en av disse klassene avgjør. Tallene følger rutenettene i CSS-en:
# klasse: (boksens bredde/høyde, [(maks skjermbredde, plassens bredde), ...], plassens bredde på store skjermer i px).
# Bildene fyller boksen med object-fit: cover, så et bredt bilde i en høy boks trenger flere piksler enn boksens bredde.
SIZES = {
    "sx": (4 / 3, [(900, "92vw")], 600),                      # leksikon: artsbilde øverst
    "ahero": (4 / 3, [(860, "92vw")], 620),                   # artikkel, verktøy, podkast: bilde øverst
    "also": (4 / 3, [(640, "46vw")], 230),                    # «Les også»
    "lxi": (4 / 3, [(600, "92vw"), (1000, "46vw")], 300),     # leksikonoversikten
    "agrid": (4 / 3, [(660, "92vw"), (1000, "46vw")], 300),   # artikkeloversikten
    "rel": (16 / 10, [(600, "92vw")], 280),                   # leksikon: artikler
    "pic": (4 / 3, [(900, "46vw")], 360),                     # forvekslingsarter side om side
    "sp": (3 / 4, [(600, "45vw"), (980, "45vw")], 300),       # forsiden: leksikonkort
    "lead-art": (16 / 11, [(860, "92vw")], 720),              # forsiden: hovedartikkel
    "feat": (4 / 5, [(860, "92vw")], 560),                    # forsiden: hyttetips (4:3 på mobil)
    "pod": (4 / 3, [(860, "92vw")], 600),                     # forsiden: podkast
}
DEFAULT_SIZES = "(max-width: 860px) 92vw, 50vw"
HERO_CONTEXTS = ("sx", "ahero")  # bildet her er det største elementet på skjermen (LCP)


def sizes_for(ctx, e):
    if ctx not in SIZES: return DEFAULT_SIZES
    box, small, big = SIZES[ctx]
    k = max(1.0, (e["w"] / e["h"]) / box)                     # hvor mye bredere enn boksen bildet blir når det fyller høyden
    km = max(1.0, (e["w"] / e["h"]) / (4 / 3)) if ctx == "feat" else k
    scale = lambda s, f: f"{round(float(s[:-2]) * f)}vw" if s.endswith("vw") else f"{round(float(s[:-2]) * f)}px"
    return ", ".join([f"(max-width: {bp}px) {scale(s, km)}" for bp, s in small] + [f"{round(big * k)}px"])


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def purge_css(css, corpus):
    """Fjerner regler i site.css som ikke kan treffe noe på siden: hver del av selektoren har en klasse eller id
    som ikke står noe sted i sidens HTML eller skript. Alt annet beholdes (forsiktig, så dynamiske klasser overlever)."""
    words = set(re.findall(r"[A-Za-z0-9_-]+", corpus))
    def dead(sel):  # [attributt] og :not(...) teller ikke – de kan treffe selv om navnet ikke finnes
        bare = lambda part: re.sub(r":not\([^)]*\)|\[[^\]]*\]", "", part)
        return all(any(n not in words for n in re.findall(r"[.#]([A-Za-z0-9_-]+)", bare(part))) for part in sel.split(","))
    def walk(s):
        out, i = [], 0
        while i < len(s):
            j = s.find("{", i)
            if j < 0: out.append(s[i:]); break
            head, depth, k = s[i:j], 1, j + 1
            while depth and k < len(s):
                depth += {"{": 1, "}": -1}.get(s[k], 0); k += 1
            inner = s[j + 1:k - 1]
            if head.startswith(("@media", "@supports")):
                kept = walk(inner)
                if kept: out.append(f"{head}{{{kept}}}")
            elif head.startswith("@") or not dead(head):
                out.append(s[i:k])
            i = k
        return "".join(out)
    return walk(css)


def font_css(base):
    return "".join(f'@font-face{{font-family:"{fam}";font-style:{st};font-weight:{w};font-display:swap;'
                   f'src:url({base}assets/fonts/{f}.woff2) format("woff2");unicode-range:{RANGES[r]}}}' for fam, st, w, f, r, _ in FONTS)


def head_block(base, css):
    pre = "".join(f'<link rel="preload" href="{base}assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for *_, f, _, p in FONTS if p)
    icons = f'<link rel="icon" href="{base}favicon.svg" type="image/svg+xml"><link rel="icon" href="{base}favicon.ico" sizes="any"><link rel="apple-touch-icon" href="{base}apple-touch-icon.png">'
    return f"<!--perf-->\n{pre}{icons}\n<style>{font_css(base)}{css}</style>\n{SPECULATION}\n<!--/perf-->\n"


# ---------- bilder ----------
def load_manifest():
    try: return json.loads(MANIFEST.read_text())
    except Exception: return {}


def build_variants():
    """Lager manglende/utdaterte varianter. Uten Pillow brukes bare varianter som allerede er laget for samme originalbilde."""
    try:
        from PIL import Image
    except ImportError:
        Image = None
    man, out = load_manifest(), {}
    VAR.mkdir(parents=True, exist_ok=True)
    for src in sorted(IMG.glob("*.webp")):
        name, data = src.stem, src.read_bytes()
        sha = hashlib.sha1(data).hexdigest()[:12]
        old = man.get(name)
        files = lambda e: [VAR / f"{name}-{w}.webp" for w in e["v"]] + ([VAR / f"{name}-m.webp"] if e.get("m") else [])
        if old and old["sha"] == sha and all(f.exists() for f in files(old)):
            out[name] = old; continue
        if Image is None:
            continue
        im = Image.open(src); im.load()
        if im.mode not in ("RGB", "RGBA"): im = im.convert("RGB")
        W, Ht = im.size
        e = {"sha": sha, "w": W, "h": Ht, "v": []}
        for w in WIDTHS:
            if w < W * 0.9:
                im.resize((w, round(Ht * w / W)), Image.LANCZOS).save(VAR / f"{name}-{w}.webp", "WEBP", quality=Q, method=6)
                e["v"].append(w)
        if HERO.match(name):
            cw = min(W, round(Ht * HERO_ASPECT)); x = (W - cw) // 2
            im.crop((x, 0, x + cw, Ht)).save(VAR / f"{name}-m.webp", "WEBP", quality=HERO_Q, method=6)
            e["m"] = [cw, Ht]
        out[name] = e
    for f in VAR.glob("*.webp"):  # rydd bort varianter av bilder som ikke finnes lenger
        n, _, w = f.stem.rpartition("-")
        if n not in out or (w != "m" and int(w) not in out[n]["v"]) or (w == "m" and not out[n].get("m")):
            f.unlink()
    MANIFEST.write_text(json.dumps(out, indent=0, sort_keys=True))
    return out


def srcset(name, e, base):
    parts = [f"{base}assets/img/r/{name}-{w}.webp {w}w" for w in e["v"]] + [f"{base}assets/img/{name}.webp {e['w']}w"]
    return ", ".join(parts)


class ImgScanner(HTMLParser):
    """Finner <img> med forelderklassene, så vi vet hvor bildet står i oppsettet."""
    VOID = {"img", "br", "input", "meta", "link", "source", "hr", "wbr", "area", "col", "embed", "param", "track"}

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.lines = [0]  # HTMLParser teller linjer bare på \n
        for ln in text.split("\n"): self.lines.append(self.lines[-1] + len(ln) + 1)
        self.stack, self.imgs, self.raw = [], [], text

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            line, col = self.getpos(); start = self.lines[line - 1] + col
            raw = self.get_starttag_text() or ""
            if not self.raw.startswith(raw, start) or not raw: return
            self.imgs.append((start, start + len(raw), a, [c for _, cls in self.stack for c in cls], any(t == "picture" for t, _ in self.stack)))
        elif tag not in self.VOID:
            self.stack.append((tag, (a.get("class") or "").split()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag: del self.stack[i:]; break


def responsive_images(h, base, man):
    sc = ImgScanner(h)
    try: sc.feed(h); sc.close()
    except Exception: return h
    for start, end, a, classes, in_picture in reversed(sc.imgs):
        src = a.get("src") or ""
        m = re.fullmatch(re.escape(base) + r"assets/img/([\w-]+)\.webp", src)
        if not m or "srcset" in a or in_picture or "${" in src: continue
        name = m.group(1); e = man.get(name)
        if not e: continue
        tag = h[start:end]
        ctx = next((c for c in reversed(classes) if c in SIZES), None)
        sizes = sizes_for(ctx, e)
        add = []
        if e["v"]: add += [f'srcset="{srcset(name, e, base)}"', f'sizes="{sizes}"']
        if "width" not in a: add += [f'width="{e["w"]}"', f'height="{e["h"]}"']
        if a.get("loading") == "lazy" and "decoding" not in a: add.append('decoding="async"')
        hero_ctx = next((c for c in HERO_CONTEXTS if c in classes), None)
        if hero_ctx and "fetchpriority" not in a and a.get("loading") != "lazy":
            add.append('fetchpriority="high"')
        if not add: continue
        new = tag[:-1].rstrip("/").rstrip() + " " + " ".join(add) + ">"
        h = h[:start] + new + h[end:]
    return h


def image_widths_js(man):
    """Liten oversikt over hvilke bredder som finnes, så forsidens skript kan bruke srcset på bilder det lager selv."""
    return json.dumps({n: e["v"] + [e["w"]] for n, e in sorted(man.items()) if e["v"]}, separators=(",", ":"))


def main():
    css = minify_css((SITE / "assets/site.css").read_text(encoding="utf-8"))
    man = build_variants()
    n = 0
    for p in sorted(SITE.rglob("*.html")):
        rel = p.relative_to(SITE).as_posix()
        if p.name.startswith("google") or rel.endswith(".email.html"):
            continue
        h = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in h or "</head>" not in h:
            continue
        base = "../" * rel.count("/")
        # Ved ny kjøring: legg CSS-lenken tilbake der blokken stod, så rekkefølgen i <head> (og dermed CSS-kaskaden) beholdes.
        h = BLOCK.sub(lambda _: f'<link rel="stylesheet" href="{base}assets/site.css">\n', h, count=1)
        h = GOOGLE_FONTS.sub("", h)
        scripts = "".join((p.parent / s).read_text(encoding="utf-8") for s in re.findall(r'<script src="([^"]+\.js)"', h)
                          if not s.startswith("http") and (p.parent / s).exists())
        block = head_block(base, purge_css(css, h + scripts))
        if SITE_CSS.search(h):
            h = SITE_CSS.sub(lambda _: block.rstrip("\n"), h, count=1)
        else:
            h = h.replace("</head>", block + "</head>", 1)
        h = responsive_images(h, base, man)
        p.write_text(h, encoding="utf-8"); n += 1
    hj = SITE / "assets/home.js"  # forsidens skript bygger egne kort: fortell det hvilke bredder som finnes
    if hj.exists():
        t = hj.read_text(encoding="utf-8")
        t2 = re.sub(r"^window\.IMGW=\{.*?\};", lambda m: "window.IMGW=" + image_widths_js(man) + ";", t, count=1, flags=re.M)
        if t2 != t: hj.write_text(t2, encoding="utf-8")
    print(f"perf: {n} sider, {len(man)} bilder med varianter")


if __name__ == "__main__":
    main()
