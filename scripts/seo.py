"""SEO for alle sider i site/: canonical, Open Graph/Twitter, strukturerte data (JSON-LD), sitemap.xml, robots.txt og llms.txt.
Kjøres etter page.py. Idempotent: alt legges mellom <!--seo--> og <!--/seo--> i <head>.
SITE_URL settes når domenet er bestemt. PREVIEW=1 (standard) beholder noindex på alle sider."""
import datetime, html as H, json, os, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = REPO / "site"
sys.path.insert(0, str(REPO / "scripts"))
BASE = os.environ.get("SITE_URL", "https://kryp.as").rstrip("/")
PREVIEW = os.environ.get("PREVIEW", "1") == "1"
TODAY = datetime.date.today().isoformat()
NAME = "Skadedyrguiden"
ORG = {"@type": "Organization", "name": NAME, "url": BASE + "/",
       "parentOrganization": {"@type": "Organization", "name": "Skadedyrbutikken", "url": "https://skadedyrbutikken.no/"}}


def url_of(p):
    rel = p.relative_to(SITE).as_posix()
    return BASE + "/" + (rel[:-10] if rel.endswith("index.html") else rel)


def meta(html, name, attr="name"):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', html)
    return H.unescape(m.group(1)) if m else ""


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def main():
    from articles import ARTICLES, EXTRA
    from faq import FAQ
    arts = {a["slug"]: a for a in ARTICLES + EXTRA}
    pages = []
    for p in sorted(SITE.rglob("*.html")):
        h = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in h:
            continue
        rel = p.relative_to(SITE).as_posix()
        u = url_of(p)
        title = re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
        desc = meta(h, "description")
        img = BASE + "/assets/img/hero.webp"
        ld = []
        home = (NAME, BASE + "/")
        if rel == "index.html":
            ld += [{**ORG, "@context": "https://schema.org"}, {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + "/", "inLanguage": "nb-NO"}]
            otype = "website"
        elif rel.startswith("artikler/"):
            slug = rel[9:-5]; a = arts.get(slug, {})
            if a.get("img") and (SITE / f"assets/img/{a['img']}.webp").exists():
                img = f"{BASE}/assets/img/{a['img']}.webp"
            ld += [{"@context": "https://schema.org", "@type": "Article", "headline": a.get("title", title), "description": desc, "image": img,
                    "datePublished": "2026-11-18", "dateModified": TODAY, "inLanguage": "nb-NO", "author": ORG, "publisher": ORG, "mainEntityOfPage": u},
                   {"@context": "https://schema.org", **crumbs([home, ("Artikler", BASE + "/#artikler"), (a.get("title", title), u)])}]
            otype = "article"
        elif rel == "sporsmal-og-svar.html":
            ld += [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for _, qs in FAQ for q, ans, _ in qs]},
                   {"@context": "https://schema.org", **crumbs([home, ("Spørsmål og svar", u)])}]
            otype = "website"
        elif rel.startswith("leksikon/"):
            name = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)
            name = re.sub("<[^>]+>", "", name)
            items = [home, ("Skadedyrleksikon", BASE + "/leksikon/")] + ([] if rel.endswith("index.html") else [(name, u)])
            ld += [{"@context": "https://schema.org", **crumbs(items)}]
            otype = "website"
        elif rel == "podkast.html":
            ld += [{"@context": "https://schema.org", "@type": "PodcastSeries", "name": "Kryp & kunnskap", "url": u, "inLanguage": "nb-NO", "publisher": ORG},
                   {"@context": "https://schema.org", **crumbs([home, ("Podkast", u)])}]
            img = BASE + "/assets/img/studio.webp"; otype = "website"
        else:
            ld += [{"@context": "https://schema.org", **crumbs([home, (title.split(" – ")[0], u)])}]
            otype = "website"
        # E-postversjonen av nyhetsbrevet og bekreftelsessidene skal aldri indekseres (duplikat / tynt innhold).
        hidden = rel.endswith(".email.html") or rel in ("nyhetsbrev/bekreftet.html", "nyhetsbrev/avmeldt.html", "nyhetsbrev/ugyldig.html")
        if rel.endswith(".email.html"):
            u = BASE + "/" + rel.replace(".email.html", ".html")
        robots = "noindex, nofollow, noarchive" if PREVIEW else ("noindex, follow" if hidden else "index, follow, max-image-preview:large")
        block = "\n".join([
            "<!--seo-->",
            f'<link rel="canonical" href="{u}">',
            f'<meta property="og:type" content="{otype}">', f'<meta property="og:site_name" content="{NAME}">', '<meta property="og:locale" content="nb_NO">',
            f'<meta property="og:title" content="{H.escape(title.split(" – ")[0])}">', f'<meta property="og:description" content="{H.escape(desc)}">',
            f'<meta property="og:url" content="{u}">', f'<meta property="og:image" content="{img}">',
            '<meta name="twitter:card" content="summary_large_image">', '<meta name="theme-color" content="#0f2a24">',
            *[f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld],
            "<!--/seo-->"])
        h = re.sub(r"\n?<!--seo-->.*?<!--/seo-->", "", h, flags=re.S)
        h = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', h)
        if 'name="robots"' not in h:
            block = block.replace("<!--seo-->", f'<!--seo-->\n<meta name="robots" content="{robots}">', 1)
        h = h.replace("</head>", block + "\n</head>", 1)
        p.write_text(h, encoding="utf-8")
        pr = "1.0" if rel == "index.html" else "0.8" if rel.startswith(("artikler/", "sporsmal")) else "0.6"
        if not hidden:
            pages.append((u, pr))
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in pages) + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    lines = [f"# {NAME}", "", "> Norsk fagside om skadedyr i hus, hage og bedrift: fagartikler med kilder (FHI m.fl.), skadedyrleksikon, verktøy og podkast. Kjøp skjer hos skadedyrbutikken.no.", "",
             "## Artikler"] + [f"- [{a['title']}]({BASE}/artikler/{a['slug']}.html)" for a in ARTICLES + EXTRA] + ["", "## Oppslag",
             f"- [Spørsmål og svar]({BASE}/sporsmal-og-svar.html)", f"- [Skadedyrleksikon]({BASE}/leksikon/)", f"- [Fellekalkulator]({BASE}/verktoy/fellekalkulator.html)",
             f"- [Tett huset-sjekkliste]({BASE}/verktoy/tett-huset.html)", f"- [Podkast]({BASE}/podkast.html)"]
    (SITE / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("seo:", len(pages), "pages", "PREVIEW" if PREVIEW else "LIVE", BASE)


main()
