"""Søkeindeks for hele Kryp.as: python scripts/search.py (etter page.py, før perf.py)

Leser de ferdige sidene i site/ og skriver site/assets/search.json, som assets/search.js henter første gang
noen åpner søket. Med i indeksen: artikler (med mellomtitler, så treff kan lenke rett til riktig avsnitt),
leksikonet, hvert spørsmål i «Spørsmål og svar», verktøyene, podkastepisodene og «Om Kryp.as».
Sider som ikke skal indekseres (noindex, nyhetsbrev, omdirigeringer) tas ikke med.
"""
import html as H, json, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


def text(x):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def first(p, h, default=""):
    m = re.search(p, h, re.S)
    return text(m.group(1)) if m else default


def page_entry(rel, h, kind):
    title = first(r"<h1[^>]*>(.*?)</h1>", h) or first(r"<title>(.*?)</title>", h).split(" – ")[0]
    e = {"t": title, "u": rel, "k": kind, "d": first(r'<meta name="description" content="([^"]*)"', h)}
    heads = [(text(t), i) for i, t in re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', h, re.S)]
    heads = [x for x in heads if x[0] and x[0].lower() not in ("kilder", "ofte stilte spørsmål", "les også")]
    if heads: e["h"] = heads
    return e


def main():
    out = []
    for p in sorted(SITE.rglob("*.html")):
        rel = p.relative_to(SITE).as_posix()
        h = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in h or rel.startswith(("nyhetsbrev/", "google")) or rel.endswith(".email.html"):
            continue
        if rel.startswith("artikler/") and rel != "artikler/index.html":
            e = page_entry(rel, h, "Artikkel")
            cat = first(r'<span class="kicker">(.*?)</span>', h)
            if cat: e["c"] = cat.split("·")[0].strip()
            faq = re.findall(r"<details><summary>(.*?)</summary>", h, re.S)
            if faq: e["q"] = [text(q) for q in faq]  # artikkelens egne spørsmål gjør den søkbar på hvordan folk spør
            out.append(e)
        elif rel.startswith("leksikon/") and rel != "leksikon/index.html":
            e = page_entry(rel, h, "Leksikon")
            lat = first(r'<p class="lat">(.*?)</p>', h)
            if lat: e["c"] = lat
            out.append(e)
        elif rel == "sporsmal-og-svar.html":
            for qid, q, a in re.findall(r'<details id="([^"]+)"><summary>(.*?)</summary><p>(.*?)</p>', h, re.S):
                out.append({"t": text(q), "u": f"{rel}#{qid}", "k": "Spørsmål", "d": text(a)[:220]})
        elif rel.startswith("verktoy/"):
            out.append(page_entry(rel, h, "Verktøy"))
        elif rel == "podkast.html":
            for n, t, d in re.findall(r'id="ep-(\d+)"[^>]*>(?:(?!id="ep-).)*?<b>(.*?)</b><br><span class="small mute">(.*?)</span>', h, re.S):
                out.append({"t": text(t), "u": f"{rel}#ep-{n}", "k": "Podkast", "d": f"Episode {n}: {text(d)}"})
        elif rel in ("om-kryp.html", "artikler/index.html", "leksikon/index.html", "kilder-og-lisenser.html"):
            out.append(page_entry(rel, h, "Side"))
    (SITE / "assets/search.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"search: {len(out)} oppføringer")


if __name__ == "__main__":
    main()
