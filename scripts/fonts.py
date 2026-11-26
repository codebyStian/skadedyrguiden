"""Lager de selvhostede fontene i site/assets/fonts/ (kjøres bare når fontene skal byttes eller oppdateres).

Kilde: woff2-filene fra Fontsource (npm-pakkene @fontsource/instrument-serif og @fontsource-variable/schibsted-grotesk),
som er de samme filene Google Fonts leverer. Vi beholder bare tegnene og OpenType-funksjonene nettstedet bruker
(norsk latin, typografiske tegn, kerning, ligaturer, tabelltall), og bare vektene 400–800 av Schibsted Grotesk.
Resultatet er ca. 65 KB i stedet for ca. 90 KB, og alt kommer fra kryp.as selv – ingen kall til Google.

Bruk: pip install fonttools brotli && python scripts/fonts.py <mappe med fontsource-filer>
Lisens: SIL Open Font License 1.1 (site/assets/fonts/OFL.txt). Ingen av fontene har reservert fontnavn.
"""
import io, pathlib, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = pathlib.Path(__file__).resolve().parent.parent / "site/assets/fonts"

# Tegnene i latin-filen. Alt annet (latin-ext) ligger i en egen fil som bare lastes hvis en side faktisk bruker slike tegn.
LATIN = "U+0020-007E,U+00A0-00FF,U+2010-2011,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2039-203A,U+20AC,U+2122,U+2212,U+2009,U+202F,U+2192"
LATIN_EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
FEATURES = ["ccmp", "locl", "liga", "kern", "mark", "mkmk", "tnum"]

FILES = [  # (kilde, utfil, unicode-område, instansiering)
    ("schibsted-grotesk-latin-wght-normal.woff2", "schibsted-grotesk.woff2", LATIN, {"wght": (400, 800)}),
    ("schibsted-grotesk-latin-ext-wght-normal.woff2", "schibsted-grotesk-ext.woff2", LATIN_EXT, {"wght": (400, 800)}),
    ("instrument-serif-latin-400-normal.woff2", "instrument-serif.woff2", LATIN, None),
    ("instrument-serif-latin-400-italic.woff2", "instrument-serif-italic.woff2", LATIN, None),
    ("instrument-serif-latin-ext-400-normal.woff2", "instrument-serif-ext.woff2", LATIN_EXT, None),
    ("instrument-serif-latin-ext-400-italic.woff2", "instrument-serif-italic-ext.woff2", LATIN_EXT, None),
]


def unicodes(spec):
    out = set()
    for part in spec.split(","):
        a, _, b = part.strip()[2:].partition("-")
        out |= set(range(int(a, 16), int(b or a, 16) + 1))
    return out


def build(src_dir):
    OUT.mkdir(parents=True, exist_ok=True)
    for src, dst, rng, axes in FILES:
        font = TTFont(pathlib.Path(src_dir) / src)
        wanted = sorted(unicodes(rng) & set(font.getBestCmap()))
        if axes:
            font = instancer.instantiateVariableFont(font, axes)
        opt = subset.Options()
        opt.flavor, opt.layout_features, opt.name_IDs = "woff2", FEATURES, ["*"]
        opt.hinting, opt.desubroutinize, opt.notdef_outline = False, True, not axes
        sub = subset.Subsetter(opt)
        sub.populate(unicodes=wanted)
        sub.subset(font)
        buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
        (OUT / dst).write_bytes(buf.getvalue())
        print(f"{dst}: {len(buf.getvalue()):,} B, {len(wanted)} tegn")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "fontsource")
