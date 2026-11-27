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
NAME = "Kryp.as"
ORG = {"@type": "Organization", "name": NAME, "url": BASE + "/",
       "description": "Norsk fagside om skadedyr i hus, hage, hytte og bedrift, drevet av folkene bak Skadedyrbutikken.",
       "publishingPrinciples": BASE + "/om-kryp.html", "knowsAbout": ["Skadedyr", "Skadedyrkontroll", "Mus og rotter", "Skadeinsekter", "Forebygging av skadedyr"],
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
    import page as _page
    EPS = [e for e in _page.episodes() if e["audio"]]
    EP_BY_ART = {}
    for e in EPS:
        for s_ in e["articles"]: EP_BY_ART[s_] = e
    pages = []
    lastmod = {}
    for p in sorted(SITE.rglob("*.html")):
        h = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in h or p.name.startswith("google") or "<title>" not in h:
            continue
        rel = p.relative_to(SITE).as_posix()
        u = url_of(p)
        title = re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
        desc = meta(h, "description")
        img = BASE + "/assets/img/hero.webp"
        ld = []
        extra_meta = []
        home = (NAME, BASE + "/")
        if rel == "index.html":
            ld += [{**ORG, "@context": "https://schema.org"}, {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + "/", "inLanguage": "nb-NO"}]
            otype = "website"
        elif rel.startswith("artikler/"):
            slug = rel[9:-5]; a = arts.get(slug, {})
            if a.get("img") and (SITE / f"assets/img/{a['img']}.webp").exists():
                img = f"{BASE}/assets/img/{a['img']}.webp"
            plain = lambda x: re.sub(r"<[^>]+>", "", x)
            art = {"@context": "https://schema.org", "@type": "Article", "headline": a.get("title", title)[:110], "description": desc,
                   "image": {"@type": "ImageObject", "url": img, "caption": a.get("alt", "")} if a.get("alt") else img,
                   "datePublished": a.get("published", "2026-11-18"), "dateModified": a.get("updated", TODAY), "inLanguage": "nb-NO",
                   "articleSection": a.get("cat", ""), "author": ORG, "publisher": ORG, "mainEntityOfPage": u,
                   "citation": [x[1] for x in a.get("sources", [])]}
            if a.get("words"): art["wordCount"] = a["words"]
            if a.get("kort"): art["abstract"] = " ".join(a["kort"])
            if slug in EP_BY_ART:
                e = EP_BY_ART[slug]
                art["audio"] = {"@type": "AudioObject", "name": f"Kryp & kunnskap #{e['n']}: {e['title']}", "description": e["desc"],
                                "contentUrl": f"{BASE}/assets/podcast/{e['slug']}.mp3", "encodingFormat": "audio/mpeg", "inLanguage": "nb-NO"}
            if a.get("about"): art["about"] = [{"@type": "Thing", "name": n} for n in a["about"]]
            ld += [art, {"@context": "https://schema.org", **crumbs([home, ("Råd og løsninger", BASE + "/artikler/"), (a.get("title", title), u)])}]
            if a.get("faq"):
                ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(ans)}} for q, ans in a["faq"]]})
            extra_meta = [f'<meta property="article:published_time" content="{a.get("published", "2026-11-18")}">',
                          f'<meta property="article:modified_time" content="{a.get("updated", TODAY)}">',
                          f'<meta property="article:section" content="{H.escape(a.get("cat", ""))}">']
            if a.get("alt"): extra_meta.append(f'<meta property="og:image:alt" content="{H.escape(a["alt"])}">')
            lastmod[u] = a.get("updated", TODAY)
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
            if rel.endswith("index.html"):
                spp = re.findall(r'<a class="lx" href="([a-z0-9-]+)\.html">(?:(?!</a>).)*?<b>(.*?)</b>', h, re.S)
                ld.append({"@context": "https://schema.org", "@type": "CollectionPage", "name": title.split(" – ")[0], "description": desc, "url": u,
                           "inLanguage": "nb-NO", "publisher": ORG, "mainEntity": {"@type": "ItemList", "itemListElement": [
                               {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/leksikon/{sl}.html", "name": re.sub("<[^>]+>", "", n).strip()}
                               for i, (sl, n) in enumerate(spp)]}})
            else:
                # Artssiden: artsfotoet øverst blir delingsbilde, og siden beskrives som en artikkel om arten (Taxon).
                m = re.search(r'<section class="sx">.*?<img[^>]+src="\.\./(assets/img/[^"]+)"[^>]*?(?:alt="([^"]*)")?', h, re.S)
                if m: img = f"{BASE}/{m.group(1)}"
                lat = re.search(r'<p class="lat">(.*?)</p>', h, re.S)
                taxon = {"@type": "Taxon", "name": H.unescape(lat.group(1)) if lat else name, "alternateName": name}
                ld.append({"@context": "https://schema.org", "@type": "Article", "headline": title.split(" – ")[0][:110], "description": desc,
                           "image": img, "inLanguage": "nb-NO", "author": ORG, "publisher": ORG, "mainEntityOfPage": u, "about": taxon,
                           "isPartOf": {"@type": "CollectionPage", "name": "Skadedyrleksikon", "url": BASE + "/leksikon/"}})
                extra_meta = [f'<meta property="og:image:alt" content="{H.escape(name)}">']
            ld += [{"@context": "https://schema.org", **crumbs(items)}]
            otype = "website" if rel.endswith("index.html") else "article"
        elif rel == "om-kryp.html":
            ld += [{"@context": "https://schema.org", "@type": "AboutPage", "name": title, "url": u, "inLanguage": "nb-NO", "about": ORG},
                   {"@context": "https://schema.org", **crumbs([home, ("Om Kryp.as", u)])}]
            otype = "website"
        elif rel == "podkast.html":
            ld += [{"@context": "https://schema.org", "@type": "PodcastSeries", "name": "Kryp & kunnskap", "url": u, "inLanguage": "nb-NO", "publisher": ORG,
                    "description": "Podkast om skadedyr i hus, hage og hytte. Marte og Jonas tar ett skadedyr per episode, med råd fra fagartiklene på Kryp.as.",
                    "episode": [{"@type": "PodcastEpisode", "episodeNumber": e["n"], "name": e["title"], "description": e["desc"], "url": f"{u}#ep-{e['n']}",
                                 "associatedMedia": {"@type": "MediaObject", "contentUrl": f"{BASE}/assets/podcast/{e['slug']}.mp3"},
                                 **({"about": {"@type": "Article", "url": f"{BASE}/artikler/{e['articles'][0]}.html"}} if e["articles"] else {})} for e in EPS]},
                   {"@context": "https://schema.org", **crumbs([home, ("Podkast", u)])}]
            img = BASE + "/assets/img/studio.webp"; otype = "website"
        else:
            ld += [{"@context": "https://schema.org", **crumbs([home, (title.split(" – ")[0], u)])}]
            otype = "website"
        # E-postversjonen av nyhetsbrevet og bekreftelsessidene skal aldri indekseres (duplikat / tynt innhold).
        NEWSLETTER = os.environ.get("NEWSLETTER", "0") == "1"   # skjult til Brevo er koblet til
        hidden = rel.endswith(".email.html") or rel in ("nyhetsbrev/bekreftet.html", "nyhetsbrev/avmeldt.html", "nyhetsbrev/ugyldig.html") or (rel.startswith("nyhetsbrev/") and not NEWSLETTER)
        if rel.endswith(".email.html"):
            u = BASE + "/" + rel.replace(".email.html", ".html")
        robots = "noindex, nofollow, noarchive" if PREVIEW else ("noindex, follow" if hidden else "index, follow, max-image-preview:large")
        block = "\n".join([
            "<!--seo-->",
            f'<link rel="canonical" href="{u}">',
            f'<meta property="og:type" content="{otype}">', f'<meta property="og:site_name" content="{NAME}">', '<meta property="og:locale" content="nb_NO">',
            f'<meta property="og:title" content="{H.escape(title.split(" – ")[0])}">', f'<meta property="og:description" content="{H.escape(desc)}">',
            f'<meta property="og:url" content="{u}">', f'<meta property="og:image" content="{img}">',
            *extra_meta, '<meta name="twitter:card" content="summary_large_image">', '<meta name="theme-color" content="#0f2a24">',
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
        "".join(f"  <url><loc>{u}</loc><lastmod>{lastmod.get(u, TODAY)}</lastmod><priority>{pr}</priority></url>\n" for u, pr in pages) + "</urlset>\n", encoding="utf-8")
    # AI-søk (GEO): søkemotorer og KI-assistenter skal få lese og sitere alt offentlig innhold.
    bots = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "CCBot", "meta-externalagent", "DuckAssistBot"]
    (SITE / "robots.txt").write_text("".join(f"User-agent: {b}\n" for b in bots) + "Allow: /\n\nUser-agent: *\nAllow: /\n\n"
                                     f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    plain = lambda x: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
    allart = ARTICLES + EXTRA
    lines = [f"# {NAME}", "", "> Norsk fagside om skadedyr i hus, hage, hytte og bedrift. Fagartikler med kilder (Folkehelseinstituttet, Miljødirektoratet, Mattilsynet, kommuner, NIBIO, NINA), skadedyrleksikon, verktøy og podkast. Drevet av folkene bak Skadedyrbutikken; all handel skjer på skadedyrbutikken.no.", "",
             "Viktig å vite når du siterer oss:",
             "- FHIs skadedyrstatistikk gjelder 11 utvalgte skadeinsekter. Mus og rotter er ikke med.",
             "- Fra juni 2026 er det forbudt å selge musegift til privatpersoner i Norge (FHI).",
             f"- Redaksjonelle prinsipper: {BASE}/om-kryp.html",
             f"- Fulltekst av alle artikler: {BASE}/llms-full.txt", "",
             "## Artikler"] + [f"- [{a['title']}]({BASE}/artikler/{a['slug']}.html): {a.get('desc') or a.get('lead', '')}" for a in allart] + ["", "## Oppslag",
             f"- [Spørsmål og svar]({BASE}/sporsmal-og-svar.html)", f"- [Skadedyrleksikon]({BASE}/leksikon/)", f"- [Fellekalkulator]({BASE}/verktoy/fellekalkulator.html)",
             f"- [Tett huset-sjekkliste]({BASE}/verktoy/tett-huset.html)", f"- [Podkast]({BASE}/podkast.html)", f"- [Om Kryp.as]({BASE}/om-kryp.html)"]
    (SITE / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    full = [f"# {NAME} – fulltekst", "", f"Kilde: {BASE}/  ·  Lisens: sitér gjerne med lenke til artikkelen.", ""]
    for a in allart:
        if not a.get("body"): continue
        body = re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m: "\n\n## " + plain(m.group(1)) + "\n", a["body"])
        body = re.sub(r"<li>", "\n- ", body); body = re.sub(r"</p>|</tr>", "\n", body)
        body = "\n".join(re.sub(r"[ \t]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", ln))).strip() for ln in body.split("\n"))
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        full += [f"# {a['title']}", f"URL: {BASE}/artikler/{a['slug']}.html", f"Oppdatert: {a.get('updated', TODAY)}", "", a.get("lead", ""), ""]
        if a.get("kort"): full += ["Kort fortalt:"] + [f"- {k}" for k in a["kort"]] + [""]
        full += [body, ""]
        if a.get("faq"): full += ["## Vanlige spørsmål"] + [f"\n**{q}**\n{plain(ans)}" for q, ans in a["faq"]] + [""]
        full += ["Kilder:"] + [f"- {t}: {u}" for t, u in a.get("sources", [])] + ["", "---", ""]
    (SITE / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
    print("seo:", len(pages), "pages", "PREVIEW" if PREVIEW else "LIVE", BASE)


main()
