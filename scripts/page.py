"""Felles topp/bunn for undersider. Kjør: python scripts/page.py"""
import json, os, pathlib, re, urllib.parse, html as H
import img as PIC
ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
SHOP = "https://skadedyrbutikken.no/produkter/{}?utm_source=kryp.as&utm_medium=referral&utm_campaign={}"

# --- Stilark ----------------------------------------------------------------------------------------------------
# site/assets/site.css er kilden. I filene som ligger i repoet lenkes det til på vanlig måte. Når nettstedet publiseres
# (INLINE_CSS=1 i .github/workflows/pages.yml) legges det i stedet rett inn i hver side: 5 kB ekstra per side, men
# nettleseren slipper å hente en egen fil før den kan tegne noe. Slik holder repoet seg lite (en CSS-endring endrer
# én fil, ikke alle sidene), og besøkende får siden opp ett nettverkskall raskere.
INLINE_CSS = os.environ.get("INLINE_CSS") == "1"
CSS_LINK = '<link rel="stylesheet" href="{}assets/site.css">'


def css_head(base):
    if not INLINE_CSS: return CSS_LINK.format(base)
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8").strip()
    css = re.sub(r"url\((['\"]?)(?!data:|https?:|/|#)", lambda m: f"url({m.group(1)}{base}assets/", css)   # stier i stilarket gjelder fra assets/
    assert "</style" not in css.lower()
    return f"<style>{css}</style>"


# --- Skrifter ---------------------------------------------------------------------------------------------------
# Nettskriftene ligger i site/assets/fonts (ikke hos Google Fonts). Skriptet under står rett etter stilarket i <head>.
#   Mobil, første besøk: siden tegnes med reserveskriftene fra site.css (de tar like stor plass), og skriftene hentes
#   først når første skjermbilde er vist, så de ikke konkurrerer med toppbildet om en treg mobillinje.
#   Bred skjerm, eller den besøkende kommer fra en annen side på Kryp.as (da ligger skriftene alt i nettleserens
#   mellomlager), laster siden på nytt eller går tilbake: hentes med en gang.
# Er skriftene framme før siden er tegnet, brukes de direkte. Er siden alt tegnet, byttes de inn på prøve: flytter noe
# på skjermen seg, angres byttet, og siden beholder reserveskriftene på denne visningen. Teksten hopper derfor aldri.
FONT_RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
}
FONT_FILES = [("Schibsted Grotesk", "normal", "400 900", "schibsted-grotesk-{}-wght-normal"), ("Instrument Serif", "normal", "400", "instrument-serif-{}-400-normal"),
              ("Instrument Serif", "italic", "400", "instrument-serif-{}-400-italic")]


def font_faces(prefix, subsets=("latin", "latin-ext")):
    """@font-face-regler (brukes i assets/fonts.css for nettlesere uten skript, og for latin-ext i site.css)."""
    return "".join(f'@font-face{{font-family:"{fam}";font-style:{style};font-weight:{weight};font-display:swap;src:url({prefix}{name.format(sub)}.woff2) format("woff2");unicode-range:{FONT_RANGES[sub]}}}'
                   for sub in subsets for fam, style, weight, name in FONT_FILES)


def fonts_head(base):
    faces = ",".join(f'["{fam}","{name.format("latin")}","{weight}","{style}"]' for fam, style, weight, name in FONT_FILES)
    js = ('(function(d,w){var p=w.performance,c,f,q=[],n=0,j=0,T;'
          # SGshown(f): kjør f når siden er lastet OG første skjermbilde faktisk står på skjermen (ikke bare «load»:
          # nettleseren viser ofte bildet litt etterpå) – eller med en gang den besøkende trykker, skriver eller ruller.
          # Alt som kan vente – skrifter på mobil, app.js, datafiler – går gjennom her, så det ikke konkurrerer med
          # det første skjermbildet om en treg mobillinje.
          'function S(){try{if(!p.getEntriesByType("paint").length&&j++<20)return A()}catch(e){}n=1;q.splice(0).forEach(function(x){setTimeout(x,0)})}'
          'function A(){if(!n){clearTimeout(T);T=setTimeout(S,250)}}'
          'function L(){try{new PerformanceObserver(A).observe({type:"largest-contentful-paint",buffered:true})}catch(e){}A()}'
          'd.readyState=="complete"?L():w.addEventListener("load",L);'
          '["pointerdown","keydown","touchstart","scroll"].forEach(function(e){w.addEventListener(e,function(){j=99;clearTimeout(T);S()},{once:true,passive:true,capture:true})});'
          'w.SGshown=function(x){n?x():q.push(x)};'
          'if(!w.FontFace||!d.fonts)return;f=[' + faces + '].map(function(x){return new FontFace(x[0],"url(' + base + 'assets/fonts/"+x[1]+".woff2) format(\'woff2\')",'
          '{weight:x[2],style:x[3],display:"swap",unicodeRange:"' + FONT_RANGES["latin"] + '"})});'
          'function add(){f.forEach(function(x){d.fonts.add(x)})}'
          'function go(t){Promise.all(f.map(function(x){return x.load()})).then(function(){'
          'if(!d.body||!(t||p.getEntriesByType("paint").length))return add();'                           # ikke tegnet ennå: bruk skriftene
          'var h=w.innerHeight,m=[];(function k(e){for(e=e.firstElementChild;e;e=e.nextElementSibling){var r=e.getBoundingClientRect();'
          'if(r.bottom>0&&r.top<h){m.push(e,r.top);k(e)}}})(d.body);add();'                              # tegnet: bytt på prøve ...
          'for(var i=0;i<m.length;i+=2)if(Math.abs(m[i].getBoundingClientRect().top-m[i+1])>2){f.forEach(function(x){d.fonts.delete(x)});break}'  # ... og angre hvis noe flyttet seg
          '},function(){})}'
          'try{c=d.referrer.indexOf(location.origin+"/")==0||p.getEntriesByType("navigation")[0].type!="navigate"}catch(e){}'
          'if(c||w.innerWidth>700)go(0);'                                                                # trolig mellomlagret, eller bred skjerm: hent nå
          'else w.SGshown(function(){go(1)})'                                                            # mobil, første besøk: når første skjermbilde er vist
          '})(document,window)')
    return f'<!--fonts--><script>{js}</script>\n<noscript><link rel="stylesheet" href="{base}assets/fonts.css"></noscript><!--/fonts-->'


def sync_fonts():
    """fonts.css (for nettlesere uten skript), og stilark og skriftblokk i den håndskrevne forsiden holdes like resten av sidene."""
    (ROOT / "assets/fonts.css").write_text(font_faces("fonts/") + "\n", encoding="utf-8")
    f = ROOT / "index.html"; h = f.read_text(encoding="utf-8"); link = CSS_LINK.format("")
    h2 = re.sub(r"\n?<!--fonts-->.*?<!--/fonts-->", "", h, flags=re.S)
    h2 = re.sub(r"<!--css-->.*?<!--/css-->", lambda m: link, h2, flags=re.S)        # tilbake til lenken hvis forrige bygg la stilarket inn
    assert h2.count(link) == 1, "forsiden skal lenke til assets/site.css nøyaktig én gang"
    h2 = h2.replace(link, (f"<!--css-->{css_head('')}<!--/css-->" if INLINE_CSS else link) + "\n" + fonts_head(""), 1)
    if h2 != h: f.write_text(h2, encoding="utf-8")


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
<link rel="icon" href="{base}favicon.ico" sizes="32x32"><link rel="icon" href="{base}favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
{css_head(base)}
{fonts_head(base)}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="logo" href="{base}index.html">Kryp.as<i></i></a>
  <nav class="nav" aria-label="Hovedmeny"><a href="{base}leksikon/index.html">Kjenn igjen</a><a href="{base}artikler/index.html">Råd og løsninger</a><a href="{base}index.html#hvadet">Hva er det?</a><a href="{base}podkast.html">Podkast</a><a href="{base}sporsmal-og-svar.html">Spørsmål og svar</a></nav>
  <a class="btn y arrow" href="https://skadedyrbutikken.no/?utm_source=kryp.as&utm_medium=referral&utm_campaign=header">Butikken </a>
</div></header>
<main>
'''

def foot(base):
    return f'''</main>
<footer class="band"><div class="wrap">
  <div class="cols">
    <div><a class="logo" href="{base}index.html">Kryp.as<i></i></a><p>Kunnskap om skadedyr i hus, hage og bedrift. Fra Skadedyrbutikken.</p></div>
    <div><h2>Les</h2><ul><li><a href="{base}leksikon/index.html">Kjenn igjen (leksikon)</a></li><li><a href="{base}artikler/index.html">Råd og løsninger</a></li><li><a href="{base}podkast.html">Podkast</a></li></ul></div>
    <div><h2>Verktøy</h2><ul><li><a href="{base}index.html#hvadet">Hva er det?</a></li><li><a href="{base}index.html#kalender">Sesongkalender</a></li><li><a href="{base}om-kryp.html">Om Kryp.as</a></li></ul></div>
    <div><h2>Handle</h2><ul><li><a href="{SHOP.format('gnagere','footer')}">Gnagere</a></li><li><a href="{SHOP.format('insekter','footer')}">Insekter</a></li><li><a href="https://skadedyrbutikken.no/kundeservice/frakt-og-levering?utm_source=kryp.as&utm_medium=referral&utm_campaign=footer">Frakt og levering</a></li></ul></div>
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
    return url + ("&" if "?" in url else "?") + f"utm_source=kryp.as&utm_medium=referral&utm_campaign={camp}"


def price(p):
    try: return f"{float(str(p).replace(',', '.')):,.0f} kr".replace(",", " ")
    except Exception: return ""


# Butikkens egen bildeskalering (Dynamicweb). Brukes bare som reserve når miniatyren mangler.
SHOP_RESIZE = "https://skadedyrbutikken.no/Admin/Public/GetImage.ashx?Image={}&Width=480&Height=480&Crop=5&Format=jpg&Quality=75"


def prod_img(r, base="../", compact=False):
    """Bildet i et produktkort. Originalfilene hos butikken er opptil 1,7 MB og lenkes aldri direkte:
    vi bruker miniatyrene fra scripts/prod_images.py (240 og 480 px), eller butikkens nedskalering hvis de mangler."""
    t = r.get("thumb")
    if t and (ROOT / t).is_file():
        w, h, s, sw = int(r.get("tw") or 0), int(r.get("th") or 0), r.get("thumb_s"), int(r.get("tsw") or 0)
        wh = f' width="{w}" height="{h}"' if w and h else ""
        ss = ""
        if s and sw and w and h and (ROOT / s).is_file():
            # Bildet vises i sin helhet i en kvadratisk flate: 80 px i kortene på mobil (68 px i de kompakte), opptil ca. 240 px ellers.
            # Et høyt og smalt bilde fyller bare en del av bredden, derfor regnes bredden ut per bilde.
            k = min(1, w / h); px = lambda n: f"{max(1, round(n * k))}px"
            ss = f' srcset="{base}{H.escape(s)} {sw}w, {base}{H.escape(t)} {w}w" sizes="{px(68) if compact else f"(max-width:560px) {px(80)}, {px(240)}"}"'
        return f'<img src="{base}{H.escape(t)}"{ss}{wh} alt="" loading="lazy" onerror="this.remove()">'
    u = r.get("image") or ""
    if not u: return ""
    p = urllib.parse.urlsplit(u)
    if p.netloc == "skadedyrbutikken.no" and p.path.startswith("/Files/"):
        u = SHOP_RESIZE.format(urllib.parse.quote(urllib.parse.unquote(p.path), safe="/"))
    return f'<img src="{H.escape(u)}" alt="" loading="lazy" onerror="this.remove()">'


def recs(key, camp, title="Riktig utstyr", compact=False, base="../"):
    """Produktkort valgt av produktagenten (scripts/products_match.py). Tom streng hvis ingen tips finnes."""
    items = recs_for(key)
    if not items: return ""
    cards = "".join(f'''<a class="rc" href="{H.escape(utm(r["url"], camp))}" rel="sponsored noopener">
<div class="rci">{prod_img(r, base, compact)}</div>
<div class="rcb"><span class="rcr">{H.escape(r.get("role", ""))}</span><b>{H.escape(r["name"])}</b><span class="rcw">{H.escape(r.get("why", ""))}</span>
<span class="rcp">{price(r.get("price"))}<i>Se produktet →</i></span></div></a>''' for r in items)
    return f'''<section class="recs{" cmp" if compact else ""}"><div class="rch"><h2>{title}</h2><span class="small mute">Valgt for denne siden · kjøp hos Skadedyrbutikken</span></div><div class="rcg">{cards}</div></section>'''


def prod(title, text, cat, camp):
    return f'''<div class="prod"><div><b>{title}</b><span>{text}</span></div><a class="btn y arrow" href="{SHOP.format(cat,camp)}">Se utvalget </a></div>'''

ARTICLES = {}  # alle artikler bygges nå fra scripts/articles.py + content/artikler/

ABOUT = '''<section class="band"><div class="wrap art">
<span class="kicker">Om oss</span><h1>Om Kryp.as</h1>
<p class="lead">Kryp.as er en norsk fagside om skadedyr i hus, hage, hytte og bedrift. Siden drives av folkene bak Skadedyrbutikken, nettbutikken for skadedyrkontroll.</p>
<h2 id="hva">Hva du finner her</h2>
<ul><li><b>Råd og løsninger:</b> artikler om konkrete problemer – hva du gjør, hvordan du forebygger og når du bør få hjelp. For eksempel – mus i veggen, veggedyr på reise, stokkmaur, vepsebol, flått og mye mer.</li>
<li><b>Kjenn igjen:</b> skadedyrleksikonet med kjennetegn, bilder og forvekslingsarter – én side per dyr.</li>
<li><b>Verktøy</b>: bildeanalyse som foreslår art, fellekalkulator og sjekklisten «Tett huset».</li>
<li><b>Podkasten</b> «Kryp &amp; kunnskap».</li></ul>
<h2 id="kilder">Slik skriver vi</h2>
<ul><li><b>Primærkilder først.</b> Fakta om biologi, helse og bekjempelse bygger på Folkehelseinstituttets skadedyrhåndbok og smittevernhåndbok, Miljødirektoratet, Mattilsynet, kommunene, NIBIO og NINA. Hver artikkel lister kildene den bygger på.</li>
<li><b>Tall fra FHI.</b> Skadedyrstatistikken er FHIs tall for antall bekjempelser hos skadedyrfirmaer. Den gjelder 11 utvalgte skadeinsekter – mus og rotter er ikke med. Vi bruker de to siste hele årene FHI har publisert.</li>
<li><b>Hjelp deg selv først.</b> Vi forklarer hva du kan gjøre selv, og sier tydelig fra når det er lurt å få hjelp av lege, veterinær eller godkjent skadedyrbekjemper.</li>
<li><b>Datert og oppdatert.</b> Hver artikkel viser når den sist ble oppdatert.</li>
<li><b>KI som verktøy.</b> Vi bruker KI-verktøy i skrivearbeidet og til illustrasjonsbildene. Fakta skal kunne spores til kildene som er lenket i artikkelen, og illustrasjonene er merket som KI-genererte.</li></ul>
<h2 id="produkter">Produkter og lenker</h2>
<p>All handel skjer hos Skadedyrbutikken. Produktene som vises i artiklene, er valgt fordi de passer til problemet artikkelen handler om, og er merket «kjøp hos Skadedyrbutikken». Vi anbefaler ikke ultralydapparater mot gnagere, og vi viser ikke musegift, som etter juni 2026 ikke kan selges til privatpersoner.</p>
<h2 id="feil">Har du funnet en feil?</h2>
<p>Si fra til oss via <a href="https://skadedyrbutikken.no/?utm_source=kryp.as&utm_medium=referral&utm_campaign=om">Skadedyrbutikken</a>, så retter vi det.</p>
<p class="small mute"><a href="kilder-og-lisenser.html">Kilder, foto og lisenser</a></p>
</div></section>
'''

PODCAST_T = '''<section class="band dark"><div class="wrap ahero">
<div><span class="kicker">Podkast</span><h1>Kryp &amp; kunnskap</h1>
<p class="mute" style="font-size:19px;max-width:44ch">En podkast om skadedyr i hus, hage og bedrift. To programledere, ett skadedyr per episode, og konkrete råd du kan bruke samme dag.</p></div>
<div class="ph"><img src="assets/img/studio.webp"{STUDIO} alt="Podkaststudio" fetchpriority="high" onerror="this.remove()"></div>
</div></section>
<section class="band"><div class="wrap" style="max-width:900px">
{PLAYER}
<h2 style="margin-top:64px">Alle episoder</h2>
{EPISODES}
<p class="small mute" style="margin-top:18px">Stemmene er laget med kunstig intelligens (Gemini). Manus er skrevet fra fagartiklene.</p>
</div></section>
'''

def episodes():
    import html
    eps = []
    for f in sorted((pathlib.Path(__file__).resolve().parent.parent / "podcast").glob("*.txt")):
        lines = f.read_text().splitlines()
        meta = {l[2:].split(":", 1)[0].strip(): l.split(":", 1)[1].strip() for l in lines if l.startswith("# ") and ":" in l and l[2:].split(":", 1)[0].strip() in ("title", "desc", "article")}
        rows = [l.split(":", 1) for l in lines if l.strip() and not l.startswith("#")]
        eps.append({"n": int(f.stem[:2]), "slug": f.stem, "title": meta.get("title", f.stem), "desc": meta.get("desc", ""),
                    "articles": [x.strip() for x in meta.get("article", "").split(",") if x.strip()],
                    "audio": (ROOT / "assets/podcast" / (f.stem + ".mp3")).exists(),
                    "tr": "".join(f'<p><b>{html.escape(n)}</b> {html.escape(t.strip())}</p>' for n, t in rows)})
    return eps


def episode_list():
    import html
    import sys; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from articles import ARTICLES as _A
    T = {a["slug"]: a["title"] for a in _A}
    rel = lambda e: "".join(f'<a class="small" href="artikler/{s}.html">Les artikkelen: {html.escape(T[s])} →</a><br>' for s in e["articles"] if s in T)
    return '<div style="display:grid;gap:14px">' + "".join(f'''<div id="ep-{e["n"]}" style="border-bottom:1px solid var(--line);padding:20px 0;scroll-margin-top:90px"><span class="small mute">Episode {e["n"]}</span><br><b>{html.escape(e["title"])}</b><br><span class="small mute">{html.escape(e["desc"])}</span><br>{rel(e)}
<audio controls preload="none" src="assets/podcast/{e["slug"]}.mp3" style="width:100%;margin-top:10px"></audio>
<details class="trans"><summary>Les hele samtalen</summary>{e["tr"]}</details></div>''' for e in reversed(episodes()) if e["audio"]) + '</div>'


def player():
    import html
    e = [x for x in episodes() if x["audio"]][-1]
    tr = e["tr"]
    return f'''<div class="player" id="pl">
<span class="kicker">Episode {e["n"]} · Nyeste</span>
<h2 style="font-size:clamp(30px,3.6vw,44px)">{html.escape(e["title"])}</h2>
<p class="mute">{html.escape(e["desc"])}</p>
<audio id="au" preload="metadata" src="assets/podcast/{e["slug"]}.mp3"></audio>
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
             "brunskogsnegl": "Brunskogsnegl eller annen snegl?", "hoggorm": "Hoggorm eller buorm?", "mus-i-veggen": "Mus eller rotte?", "musebaesj": "Mus, rotte eller flaggermus?", "rengjoring-etter-mus": "Hvilken gnager har du?",
             "mus-om-hosten": "Mus eller rotte?", "veggedyr-pa-reise": "Veggedyr eller noe annet?"}
    import lexicon
    BYID = lexicon.load(ROOT.parent)
    import re as _re, datetime as _dt
    MND = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
    def _slug(t):
        t = _re.sub(r"<[^>]+>", "", t).lower()
        for x, y in (("æ", "ae"), ("ø", "o"), ("å", "a")): t = t.replace(x, y)
        return _re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]
    EPS = episodes()
    for a in RA:
        cmpb = lexicon.article_compare(a["slug"], BYID)
        q = CHECK.get(a["slug"])
        chk = f'<p style="margin-top:22px"><a class="btn y arrow" href="../index.html#hvadet">{q} Last opp et bilde </a></p>' if q else ""
        box = f'<div class="box"><b>Usikker på hva du har funnet?</b>Last opp et bilde, så får du et forslag til art med kjennetegnene vurderingen bygger på, kontrollert mot Folkehelseinstituttets skadedyrhåndbok. <a href="../index.html#hvadet">Finn ut hvilket dyr det er →</a></div>' if q else ""
        regs = ", ".join(RN[r] for r in a["regions"])
        same = [b for b in RA if b is not a and b["cat"] == a["cat"]]
        others = (same + [b for b in RA if b is not a and b not in same and set(b["regions"]) & set(a["regions"])])[:3]
        # Overskrifter får id-er, og lange artikler får en innholdsliste.
        heads = []
        def _h2(m):
            txt = m.group(1); i = _slug(txt); heads.append((i, _re.sub(r"<[^>]+>", "", txt))); return f'<h2 id="{i}">{txt}</h2>'
        body = _re.sub(r"<h2>(.*?)</h2>", _h2, a["body"])
        body = _re.sub(r'(<table class="tbl">.*?</table>)', r'<div class="tblw">\1</div>', body, flags=_re.S)
        if cmpb: body = body.replace("</p>", "</p>" + cmpb, 1)
        toc = ('<nav class="toc" aria-label="Innhold"><b>I denne artikkelen</b><ol>' + "".join(f'<li><a href="#{i}">{H.escape(t)}</a></li>' for i, t in heads) +
               ('<li><a href="#vanlige-sporsmal">Vanlige spørsmål</a></li>' if a.get("faq") else "") + '</ol></nav>') if len(heads) >= 4 else ""
        faq = ('<h2 id="vanlige-sporsmal">Vanlige spørsmål</h2><div class="faqs">' +
               "".join(f'<details><summary>{H.escape(qq)}</summary><p>{aa}</p></details>' for qq, aa in a["faq"]) + '</div>') if a.get("faq") else ""
        kort = ('<aside class="kort" aria-label="Kort fortalt"><b>Kort fortalt</b><ul>' + "".join(f"<li>{H.escape(k)}</li>" for k in a["kort"]) + '</ul></aside>') if a.get("kort") else ""
        ep = next((e for e in reversed(EPS) if a["slug"] in e["articles"] and e["audio"]), None)
        a["episode"] = ep
        pod = (f'''<aside class="podbox" aria-label="Podkast"><div class="pbh"><span class="pbi" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1v-6h3zM3 19a2 2 0 0 0 2 2h1v-6H3z"/></svg></span><div><span class="kicker">Hør episoden · Kryp &amp; kunnskap #{ep["n"]}</span><b>{H.escape(ep["title"])}</b></div></div>
<p class="small mute">{H.escape(ep["desc"])}</p><audio controls preload="none" src="../assets/podcast/{ep["slug"]}.mp3"></audio>
<a class="small" href="../podkast.html#ep-{ep["n"]}">Les hele samtalen og hør flere episoder →</a></aside>''') if ep else ""
        upd = a.get("updated", "2026-11-24"); d = _dt.date.fromisoformat(upd)
        alt = H.escape(a.get("alt", ""))
        body = f'''<section class="band" style="padding-bottom:0"><div class="wrap ahero">
<div><span class="kicker">{a["cat"]} · {a["min"]} min · {regs}</span><h1 style="font-size:clamp(34px,4.6vw,56px)">{H.escape(a["title"])}</h1><p class="mute" style="font-size:19px;max-width:46ch">{H.escape(a["lead"])}</p><div class="meta"><span>Av redaksjonen i Kryp.as</span><span>Oppdatert <time datetime="{upd}">{d.day}. {MND[d.month - 1]} {d.year}</time></span></div>{chk}</div>
<div class="ph" data-label="{H.escape(a["cat"])}"><img src="../assets/img/{a["img"]}.webp"{PIC.rs(a["img"], "ahero", "../assets/img/")} alt="{alt}" fetchpriority="high" onerror="this.parentNode.dataset.ph=1;this.remove()"></div>
</div></section>
<article class="band"><div class="art">{kort}{pod}{toc}{body}
{box}
{(f'<div class="box"><b>Vil du ha en trinn-for-trinn-guide?</b>Skadedyrbutikken har en egen guide til dette: <a href="{H.escape(a["guide"][1])}" rel="noopener">{H.escape(a["guide"][0])} →</a></div>') if a.get("guide") else ""}
{recs("art:" + a["slug"], "art-" + a["slug"]) or (prod(*a["prod"], "art-" + a["slug"]) if a["prod"] else "")}
{faq}
<h2 id="kilder">Kilder</h2><ul class="small">{"".join(f'<li><a href="{u}" rel="noopener">{H.escape(t)}</a></li>' for t, u in a["sources"])}</ul>
<p class="small mute">Artikkelen er skrevet av redaksjonen i Kryp.as og bygger på kildene over. Den erstatter ikke råd fra lege, veterinær eller fagperson.</p>
{('<h2>Les også</h2><div class="also">' + "".join(f'<a href="{b["slug"]}.html"><div class="ph" data-label="{H.escape(b["cat"])}"><img src="../assets/img/{b["img"]}.webp"{PIC.rs(b["img"], "also", "../assets/img/")} alt="" loading="lazy" onerror="this.parentNode.dataset.ph=1;this.remove()"></div><span class="small mute">{H.escape(b["cat"])}</span><b>{H.escape(b["title"])}</b></a>' for b in others) + '</div>') if others else ""}
</div></article>'''
        st = a.get("seo_title") or a["title"]
        title_tag = st + " – Kryp.as" if len(st) <= 50 else st
        (ROOT / "artikler" / (a["slug"] + ".html")).write_text(head(H.escape(title_tag), H.escape(a.get("desc") or a["lead"]), "../") + body + foot("../"), encoding="utf-8")
    allart = [{k: a[k] for k in ("slug", "title", "cat", "img", "regions", "months")} for a in RA]
    (ROOT / "data" / "articles.json").write_text(json.dumps(allart, ensure_ascii=False, indent=1), encoding="utf-8")
    old = ROOT / "data" / "regions.json"
    if old.exists(): old.unlink()
    for slug, (title, desc, body) in TOOLS.items():
        f = ROOT / "verktoy" / (slug + ".html"); f.parent.mkdir(exist_ok=True)
        r = recs("tool:" + slug, slug, "Utstyret du trenger")
        r = f'<section class="band" style="padding-top:0"><div class="wrap">{r}</div></section>' if r else ""
        f.write_text(head(title + " – Kryp.as", desc, "../") + body + r + foot("../"), encoding="utf-8")


if __name__ == "__main__":
    sync_fonts()
    regional_pages()
    import extra; extra.build(head, foot, prod, recs); extra.newsletter_pages(head, foot); extra.credits_page(head, foot); extra.articles_index(head, foot)
    for path, (title, desc, body) in ARTICLES.items():
        f = ROOT / path; f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(head(title, desc, "../") + body + foot("../"), encoding="utf-8")
    (ROOT / "om-kryp.html").write_text(head("Om Kryp.as – hvem vi er og hvordan vi skriver", "Kryp.as er en norsk fagside om skadedyr, drevet av folkene bak Skadedyrbutikken. Slik velger vi kilder, skriver artikler og velger produkter.", "") + ABOUT + foot(""), encoding="utf-8")
    (ROOT / "data" / "episodes.json").write_text(json.dumps([{"n": e["n"], "title": e["title"], "articles": e["articles"]} for e in reversed(episodes()) if e["audio"]], ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "podkast.html").write_text(head("Podkast – Kryp.as", "Podkasten Kryp & kunnskap om skadedyr.", "") + PODCAST_T.replace("{STUDIO}", PIC.rs("studio", "ahero", "assets/img/")).replace("{PLAYER}", player()).replace("{EPISODES}", episode_list()) + foot(""), encoding="utf-8")
    print("ok")
