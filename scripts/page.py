"""Felles topp/bunn for undersider. Kjør: python scripts/page.py"""
import json, pathlib, html as H
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
SHOP = "https://skadedyrbutikken.no/produkter/{}?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign={}"

def head(title, desc, base):
    return f'''<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="light">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Schibsted+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="logo" href="{base}index.html">Skadedyrguiden<i></i></a>
  <nav class="nav" aria-label="Hovedmeny"><a href="{base}leksikon/index.html">Leksikon</a><a href="{base}artikler/index.html">Artikler</a><a href="{base}index.html#hvadet">Hva er det?</a><a href="{base}podkast.html">Podkast</a><a href="{base}sporsmal-og-svar.html">Spørsmål og svar</a></nav>
  <a class="btn y arrow" href="https://skadedyrbutikken.no/?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=header">Butikken </a>
</div></header>
<main>
'''

def foot(base):
    return f'''</main>
<footer class="band"><div class="wrap">
  <div class="cols">
    <div><a class="logo" href="{base}index.html">Skadedyrguiden<i></i></a><p>Kunnskap om skadedyr i hus, hage og bedrift. Fra Skadedyrbutikken.</p></div>
    <div><h3>Les</h3><ul><li><a href="{base}index.html#leksikon">Leksikon</a></li><li><a href="{base}artikler/index.html">Artikler</a></li><li><a href="{base}podkast.html">Podkast</a></li></ul></div>
    <div><h3>Verktøy</h3><ul><li><a href="{base}index.html#hvadet">Hva er det?</a></li><li><a href="{base}index.html#kalender">Sesongkalender</a></li></ul></div>
    <div><h3>Handle</h3><ul><li><a href="{SHOP.format('gnagere','footer')}">Gnagere</a></li><li><a href="{SHOP.format('insekter','footer')}">Insekter</a></li><li><a href="https://skadedyrbutikken.no/kundeservice/frakt-og-levering">Frakt og levering</a></li></ul></div>
  </div>
  <div class="base">Illustrasjonsbildene er AI-genererte. Artsfoto er ekte fotografier med fri lisens. <a href="{base}kilder-og-lisenser.html" style="color:inherit">Kilder, foto og lisenser</a></div>
</div></footer>
<script src="{base}assets/nl.js" defer></script>
</body>
</html>
'''

_RECS = None


def recs_for(key):
    global _RECS
    if _RECS is None:
        f = pathlib.Path(__file__).resolve().parent.parent / "site/data/recs.json"
        _RECS = json.loads(f.read_text()) if f.exists() else {}
    return _RECS.get(key) or []


def utm(url, camp):
    return url + ("&" if "?" in url else "?") + f"utm_source=skadedyrguiden&utm_medium=referral&utm_campaign={camp}"


def price(p):
    try: return f"{float(str(p).replace(',', '.')):,.0f} kr".replace(",", " ")
    except Exception: return ""


def recs(key, camp, title="Riktig utstyr", compact=False):
    """Produktkort valgt av produktagenten (scripts/products_match.py). Tom streng hvis ingen tips finnes."""
    items = recs_for(key)
    if not items: return ""
    cards = "".join(f'''<a class="rc" href="{H.escape(utm(r["url"], camp))}" rel="sponsored noopener">
<div class="rci">{f'<img src="{H.escape(r["image"])}" alt="" loading="lazy" onerror="this.remove()">' if r.get("image") else ""}</div>
<div class="rcb"><span class="rcr">{H.escape(r.get("role", ""))}</span><b>{H.escape(r["name"])}</b><span class="rcw">{H.escape(r.get("why", ""))}</span>
<span class="rcp">{price(r.get("price"))}<i>Se produktet →</i></span></div></a>''' for r in items)
    return f'''<section class="recs{" cmp" if compact else ""}"><div class="rch"><h2>{title}</h2><span class="small mute">Valgt for denne siden · kjøp hos Skadedyrbutikken</span></div><div class="rcg">{cards}</div></section>'''


def prod(title, text, cat, camp):
    return f'''<div class="prod"><div><b>{title}</b><span>{text}</span></div><a class="btn y arrow" href="{SHOP.format(cat,camp)}">Se utvalget </a></div>'''

ARTICLES = {
"artikler/mus-om-hosten.html": ("Mus i huset om høsten – Skadedyrguiden",
 "Slik finner du inngangene mus bruker om høsten, hva du tetter med, og hvor fellene gjør mest nytte.",
 f'''<section class="band" style="padding-bottom:0"><div class="wrap ahero">
<div><span class="kicker">Gnagere · 6 min</span><h1 style="font-size:clamp(34px,4.6vw,56px)">Mus i huset om høsten: finn hullet før musa gjør det</h1><p class="mute" style="font-size:19px;max-width:44ch">Om høsten flytter mange mus inn der det er varmt. Det viktigste verktøyet er en lommelykt, ikke gift.</p><div class="meta"><span>Av redaksjonen</span><span>Oppdatert november 2026</span></div><p style="margin-top:22px"><a class="btn y arrow" href="../index.html#hvadet">Mus eller rotte? Last opp et bilde </a></p></div>
<div class="ph"><img src="../assets/img/mus.webp" alt="Husmus ved gulvlist" onerror="this.remove()"></div>
</div></section>
<article class="band"><div class="art">
<p class="lead">Når nettene blir kalde, flytter mange mus inn der det er varmt og tørt. Det beste du kan gjøre er å stenge døra før de finner den, og det handler mer om en lommelykt enn om gift.</p>
<h2>Hvorfor kommer musa akkurat nå?</h2>
<p>Om sommeren finner musa mat og ly ute. Når temperaturen faller og maten blir knappere, søker den mot bygninger. Kjellere, loft, garasjer og hytter som står tomme er de første stedene den prøver.</p>
<h2>Se etter disse tegnene</h2>
<ul><li>Små, mørke ekskrementer, omtrent på størrelse med riskorn.</li><li>Gnagemerker på matpakker, isolasjon eller kartonger.</li><li>Krafsing og tassing i tak eller vegger, særlig om kvelden og natten.</li><li>Mørke smussmerker langs lister der musa går fast.</li></ul>
<div class="box"><b>Tommelfingerregel:</b> Kommer en blyant gjennom hullet, kommer en mus også gjennom. Mus kan presse seg gjennom åpninger som virker altfor små.</div>
<h2>Slik tetter du</h2>
<p>Gå rundt huset med lommelykt. Sjekk særlig der rør og kabler går inn, under dører, langs grunnmuren, i lufteventiler og i takfoten. Bruk materialer musa ikke gnager gjennom, som stålull kombinert med fugemasse, metallnetting eller børstelister på dører. Skum alene stopper sjelden en mus.</p>
<h2>Feller: plassering betyr mer enn antall</h2>
<p>Mus går helst langs vegger. Sett fellene vinkelrett mot veggen der du har sett spor, og bruk flere feller i stedet for én. Sjekk dem ofte. Hvis du får fangst i flere uker, er det fortsatt en åpen inngang et sted.</p>
{recs("art:mus-om-hosten", "art-mus") or prod("Feller og tettemidler for mus", "Mekaniske feller, åtestasjoner og tettematerialer.", "gnagere", "art-mus")}
<h2>Når bør du ringe en fagperson?</h2>
<p>Hvis problemet kommer tilbake etter at du har tettet, hvis du finner tegn på rotter, eller hvis du har en bedrift der du må dokumentere skadedyrkontrollen.</p>
</div></article>'''),
"artikler/veggedyr-pa-reise.html": ("Veggedyr på hotellet: sjekk rommet på to minutter – Skadedyrguiden",
 "Slik sjekker du hotellsengen for veggedyr på to minutter, og hva du gjør hvis du finner noe.",
 f'''<section class="band" style="padding-bottom:0"><div class="wrap ahero">
<div><span class="kicker">Insekter · 5 min</span><h1 style="font-size:clamp(34px,4.6vw,56px)">Veggedyr på hotellet: sjekk rommet på to minutter</h1><p class="mute" style="font-size:19px;max-width:44ch">Det du ser etter i sengen, og hva du gjør hvis du finner noe.</p><div class="meta"><span>Av redaksjonen</span><span>Oppdatert november 2026</span></div></div>
<div class="ph"><img src="../assets/img/veggedyr.webp" alt="Hotellrom med koffert på bagasjestativ" onerror="this.remove()"></div>
</div></section>
<article class="band"><div class="art">
<p class="lead">Veggedyr kommer sjelden inn av seg selv. De blir båret inn, oftest i bagasjen. Hotellrommet er stedet der du oftest kan oppdage dem før de blir med deg – og det tar bare to minutter.</p>
<h2>Slik ser veggedyr ut</h2>
<p>Voksne veggedyr er flate, rødbrune og omtrent på størrelse med et eplefrø. Ungene er mindre og lysere. De gjemmer seg i sprekker nær der folk sover, og kommer fram om natten.</p>
<h2>To-minutters-sjekken</h2>
<ul><li>Sett bagasjen på badet eller på et bagasjestativ, ikke på sengen eller gulvet.</li><li>Trekk av lakenet i ett hjørne og se langs madrassens sømmer og kanter.</li><li>Se etter små svarte prikker, hudskall eller levende dyr.</li><li>Sjekk bak sengegavlen hvis den lar seg flytte.</li></ul>
<div class="box"><b>Finner du noe?</b> Si fra i resepsjonen og be om et rom som ikke ligger vegg i vegg med det første.</div>
<h2>Når du kommer hjem</h2>
<p>Pakk ut på badet eller i gangen, ikke på soverommet. Skadedyrbutikken har en egen guide til bagasjen og klærne etter reisen: <a href="https://skadedyrbutikken.no/tips-og-raad/insekter/slik-unngaar-du-aa-faa-med-veggedyr-hjem-i-bagasjen?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=art-veggedyr" rel="noopener">Slik unngår du å få med veggedyr hjem i bagasjen →</a></p>
{recs("art:veggedyr-pa-reise", "art-veggedyr") or prod("Utstyr mot veggedyr", "Feller, overvåking og utstyr til reise og hjem.", "insekter", "art-veggedyr")}
<h2>Mistenker du veggedyr hjemme?</h2>
<p>Ikke flytt madrasser og møbler mellom rom, og ikke kast dem uinnpakket. Da sprer du problemet. Veggedyr er vanskelige å bli kvitt på egen hånd, så kontakt en skadedyrtekniker tidlig.</p>
</div></article>'''),
}

PODCAST_T = '''<section class="band dark"><div class="wrap ahero">
<div><span class="kicker">Podkast</span><h1>Kryp &amp; kunnskap</h1>
<p class="mute" style="font-size:19px;max-width:44ch">En podkast om skadedyr i hus, hage og bedrift. To programledere, ett skadedyr per episode, og konkrete råd du kan bruke samme dag.</p></div>
<div class="ph"><img src="assets/img/studio.webp" alt="Podkaststudio" onerror="this.remove()"></div>
</div></section>
<section class="band"><div class="wrap" style="max-width:900px">
{PLAYER}
<h2 style="margin-top:64px">Episoder</h2>
<div style="display:grid;gap:14px">
''' + "".join(f'''<div style="display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:16px;align-items:center;border-bottom:1px solid var(--line);padding:20px 0"><span style="width:52px;height:52px;border-radius:50%;border:1.5px solid var(--ink);display:grid;place-items:center"><svg width="18" height="18" viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z" fill="currentColor"/></svg></span><span><span class="small mute">Episode {n}</span><br><b>{t}</b><br><span class="small mute">{d}</span></span><span class="small mute" style="white-space:nowrap">{l}</span></div>
''' for n,t,d,l in [
 (1,"Mus: småkrypet som kommer inn med høsten","Inngangsveier, feller og de vanligste feilene folk gjør.","24 min")]) + '''</div>
<p class="small mute" style="margin-top:18px">Stemmene er laget med kunstig intelligens (Gemini). Manus er skrevet fra fagartiklene. Nye episoder kommer.</p>
</div></section>
'''

def player():
    import html
    src = pathlib.Path(__file__).resolve().parent.parent / "podcast/01-mus-om-hosten.txt"
    rows = [l.split(":", 1) for l in src.read_text().splitlines() if l.strip() and not l.startswith("#")]
    tr = "".join(f'<p><b>{html.escape(n)}</b> {html.escape(t.strip())}</p>' for n, t in rows)
    return f'''<div class="player" id="pl">
<span class="kicker">Episode 1 · Nyeste</span>
<h2 style="font-size:clamp(30px,3.6vw,44px)">Mus: småkrypet som kommer inn med høsten</h2>
<p class="mute">Marte og Jonas om hvorfor musa kommer inn akkurat nå, hvilke tegn du ser etter, og hvordan du tetter riktig.</p>
<audio id="au" preload="metadata" src="assets/podcast/01-mus-om-hosten.mp3"></audio>
<div class="pbar"><button class="pbtn" id="pb" type="button" aria-label="Spill av"><svg viewBox="0 0 24 24" width="22" height="22"><path id="pi" d="M7 4.5v15l13-7.5z" fill="currentColor"/></svg></button>
<div class="ptrack"><input id="ps" type="range" min="0" max="1000" value="0" aria-label="Posisjon"><div class="ptime"><span id="pc">0:00</span><span id="pd">–:––</span></div></div></div>
<p class="small mute" id="pmsg" style="margin:10px 0 0"></p>
<details class="trans"><summary>Les hele samtalen</summary>{tr}</details>
</div>
<script>{{
const a=document.getElementById('au'),b=document.getElementById('pb'),i=document.getElementById('pi'),s=document.getElementById('ps'),c=document.getElementById('pc'),d=document.getElementById('pd');
const f=t=>isFinite(t)?Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0'):'–:––';
b.onclick=()=>{{if(a.paused){{a.play().catch(()=>{{document.getElementById('pmsg').textContent='Lyden er ikke klar ennå.'}})}}else a.pause()}};
a.onplay=()=>{{i.setAttribute('d','M7 4.5h3.5v15H7zM13.5 4.5H17v15h-3.5z');b.setAttribute('aria-label','Pause')}};
a.onpause=()=>{{i.setAttribute('d','M7 4.5v15l13-7.5z');b.setAttribute('aria-label','Spill av')}};
a.onloadedmetadata=()=>{{d.textContent=f(a.duration)}};
a.ontimeupdate=()=>{{c.textContent=f(a.currentTime);if(a.duration)s.value=1000*a.currentTime/a.duration}};
s.oninput=()=>{{if(a.duration)a.currentTime=s.value/1000*a.duration}};
a.onerror=()=>{{document.getElementById('pmsg').textContent='Lyden lages fortsatt. Prøv igjen om litt.'}};
}}</script>'''


def regional_pages():
    import json, html as H, sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from articles import ARTICLES as RA, REGION_ARTICLES, EXTRA
    from tools import TOOLS
    RN = {"ost": "Østlandet", "sor": "Sørlandet", "vest": "Vestlandet", "midt": "Trøndelag", "nord": "Nord-Norge"}
    CHECK = {"fukt-solvkre-skjeggkre": "Sølvkre eller skjeggkre?", "stokkmaur-eller-skogsmaur": "Stokkmaur eller skogsmaur?", "vepsebol": "Veps, humle eller bie?",
             "humler-og-bier-i-veggen": "Humle, bie eller veps?", "husbukk": "Husbukk eller borebille?", "stripet-borebille": "Borebille eller husbukk?",
             "klesmoll-og-pelsbille": "Møll eller pelsbille?", "rotter-i-byen": "Rotte eller mus?", "mus-pa-garden": "Husmus eller skogmus?",
             "smagnagerar": "Hvilken gnager er det?", "fluer-om-hosten": "Hvilket insekt er det?", "flatt-langs-kysten": "Flått eller noe annet?",
             "brunskogsnegl": "Brunskogsnegl eller annen snegl?", "hoggorm": "Hoggorm eller buorm?"}
    import lexicon
    BYID = lexicon.load(ROOT.parent)
    for a in RA:
        cmpb = lexicon.article_compare(a["slug"], BYID)
        q = CHECK.get(a["slug"])
        chk = f'<p style="margin-top:22px"><a class="btn y arrow" href="../index.html#hvadet">{q} Last opp et bilde </a></p>' if q else ""
        box = f'<div class="box"><b>Usikker på hva du har funnet?</b>Last opp et bilde, så får du et forslag til art med kjennetegnene vurderingen bygger på, kontrollert mot Folkehelseinstituttets skadedyrhåndbok. <a href="../index.html#hvadet">Finn ut hvilket dyr det er →</a></div>' if q else ""
        regs = ", ".join(RN[r] for r in a["regions"])
        same = [b for b in RA if b is not a and b["cat"] == a["cat"]]
        others = (same + [b for b in RA if b is not a and b not in same and set(b["regions"]) & set(a["regions"])])[:3]
        body = f'''<section class="band" style="padding-bottom:0"><div class="wrap ahero">
<div><span class="kicker">{a["cat"]} · {a["min"]} min · {regs}</span><h1 style="font-size:clamp(34px,4.6vw,56px)">{H.escape(a["title"])}</h1><p class="mute" style="font-size:19px;max-width:46ch">{H.escape(a["lead"])}</p><div class="meta"><span>Av redaksjonen</span><span>Oppdatert november 2026</span></div>{chk}</div>
<div class="ph" data-label="{H.escape(a["cat"])}"><img src="../assets/img/{a["img"]}.webp" alt="" onerror="this.parentNode.dataset.ph=1;this.remove()"></div>
</div></section>
<article class="band"><div class="art">{a["body"].replace("</p>", "</p>" + cmpb, 1) if cmpb else a["body"]}
{box}
{(f'<div class="box"><b>Skal du bekjempe dem?</b>Denne artikkelen handler om å forstå og forebygge. Skadedyrbutikken har en egen trinn-for-trinn-guide til bekjempelse: <a href="{H.escape(a["guide"][1])}" rel="noopener">{H.escape(a["guide"][0])} →</a></div>') if a.get("guide") else ""}
{recs("art:" + a["slug"], "art-" + a["slug"]) or (prod(*a["prod"], "art-" + a["slug"]) if a["prod"] else "")}
<h2>Kilder</h2><ul class="small">{"".join(f'<li><a href="{u}" rel="noopener">{H.escape(t)}</a></li>' for t, u in a["sources"])}</ul>
<p class="small mute">Artikkelen er skrevet for Skadedyrguiden og bygger på kildene over. Den erstatter ikke råd fra en fagperson.</p>
{('<h2>Les også</h2><div class="also">' + "".join(f'<a href="{b["slug"]}.html"><div class="ph" data-label="{H.escape(b["cat"])}"><img src="../assets/img/{b["img"]}.webp" alt="" loading="lazy" onerror="this.parentNode.dataset.ph=1;this.remove()"></div><span class="small mute">{H.escape(b["cat"])}</span><b>{H.escape(b["title"])}</b></a>' for b in others) + '</div>') if others else ""}
</div></article>'''
        (ROOT / "artikler" / (a["slug"] + ".html")).write_text(head(a["title"] + " – Skadedyrguiden", a["lead"], "../") + body + foot("../"), encoding="utf-8")
    allart = [{k: a[k] for k in ("slug", "title", "cat", "img", "regions", "months")} for a in RA] + EXTRA
    (ROOT / "data" / "articles.json").write_text(json.dumps(allart, ensure_ascii=False, indent=1), encoding="utf-8")
    old = ROOT / "data" / "regions.json"
    if old.exists(): old.unlink()
    for slug, (title, desc, body) in TOOLS.items():
        f = ROOT / "verktoy" / (slug + ".html"); f.parent.mkdir(exist_ok=True)
        r = recs("tool:" + slug, slug, "Utstyret du trenger")
        r = f'<section class="band" style="padding-top:0"><div class="wrap">{r}</div></section>' if r else ""
        f.write_text(head(title + " – Skadedyrguiden", desc, "../") + body + r + foot("../"), encoding="utf-8")


if __name__ == "__main__":
    regional_pages()
    import extra; extra.build(head, foot, prod, recs); extra.newsletter_pages(head, foot); extra.credits_page(head, foot); extra.articles_index(head, foot)
    for path, (title, desc, body) in ARTICLES.items():
        f = ROOT / path; f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(head(title, desc, "../") + body + foot("../"), encoding="utf-8")
    (ROOT / "podkast.html").write_text(head("Podkast – Skadedyrguiden", "Podkasten Kryp & kunnskap om skadedyr.", "") + PODCAST_T.replace("{PLAYER}", player()) + foot(""), encoding="utf-8")
    print("ok")
