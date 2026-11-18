"""Felles topp/bunn for undersider. Kjør: python scripts/page.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
SHOP = "https://skadedyrbutikken.no/produkter/{}?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign={}"

def head(title, desc, base):
    return f'''<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/site.css">
</head>
<body>
<div class="concept">Konseptskisse – eksempeltekst som må faktasjekkes før publisering.</div>
<header class="top"><div class="wrap">
  <a class="logo" href="{base}index.html"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#f4c430"/><path d="M11 25c0-6 4-10 9-10s9 4 9 10" fill="none" stroke="#18201d" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="25" r="5" fill="#18201d"/><path d="M15 13l-3-4M25 13l3-4" stroke="#18201d" stroke-width="2.5" stroke-linecap="round"/></svg>Skadedyrguiden</a>
  <nav class="nav" aria-label="Hovedmeny"><a href="{base}index.html#artikler">Artikler</a><a href="{base}index.html#hvadet">Hva er det?</a><a href="{base}podkast.html">Podkast</a><a href="{base}index.html#kalender">Sesong</a><a href="{base}index.html#faq">Spørsmål</a></nav>
  <a class="btn red shop" href="https://skadedyrbutikken.no/?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=header">Til butikken →</a>
</div></header>
<main>
'''

def foot(base):
    return f'''</main>
<footer class="band"><div class="wrap cols">
  <div><h3>Skadedyrguiden</h3><p>Kunnskap om skadedyr i hus, hage og bedrift. Et konsept fra Skadedyrbutikken.</p></div>
  <div><h3>Les</h3><ul><li><a href="{base}index.html#artikler">Artikler</a></li><li><a href="{base}podkast.html">Podkast</a></li><li><a href="{base}index.html#kalender">Sesongkalender</a></li></ul></div>
  <div><h3>Handle</h3><ul><li><a href="{SHOP.format('gnagere','footer')}">Gnagere</a></li><li><a href="{SHOP.format('insekter','footer')}">Insekter</a></li><li><a href="https://skadedyrbutikken.no/kundeservice/frakt-og-levering">Frakt og levering</a></li></ul></div>
</div></footer>
</body>
</html>
'''

def prod(title, text, cat, camp):
    return f'''<div class="prod"><svg viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="25" fill="#18201d"/><path d="M16 22h20l-2 16H18z" fill="#f4c430"/><path d="M20 22a6 6 0 0 1 12 0" fill="none" stroke="#f4c430" stroke-width="3"/></svg><div><b>{title}</b><br>{text}</div><a class="btn fill" href="{SHOP.format(cat,camp)}">Se utvalget →</a></div>'''

ARTICLES = {
"artikler/mus-om-hosten.html": ("Mus i huset om høsten – Skadedyrguiden",
 "Slik finner du inngangene mus bruker om høsten, hva du tetter med, og hvor fellene gjør mest nytte.",
 f'''<article class="band"><div class="art">
<p class="small mute">Gnagere · 6 minutter lesing</p>
<h1>Mus i huset om høsten: finn hullet før musa gjør det</h1>
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
{prod("Feller og tettemidler for mus", "Mekaniske feller, åtestasjoner og tettematerialer.", "gnagere", "art-mus")}
<h2>Når bør du ringe en fagperson?</h2>
<p>Hvis problemet kommer tilbake etter at du har tettet, hvis du finner tegn på rotter, eller hvis du har en bedrift der du må dokumentere skadedyrkontrollen.</p>
<p class="small mute">Eksempelartikkel i konseptet. Fakta skal kvalitetssikres mot fagkilder, for eksempel Folkehelseinstituttet, før publisering.</p>
</div></article>'''),
"artikler/veggedyr-pa-reise.html": ("Veggedyr på reise – Skadedyrguiden",
 "Slik sjekker du hotellrommet for veggedyr og unngår å ta dem med hjem.",
 f'''<article class="band"><div class="art">
<p class="small mute">Insekter · 5 minutter lesing</p>
<h1>Veggedyr på reise: sjekk hotellrommet på to minutter</h1>
<p class="lead">Veggedyr kommer sjelden inn av seg selv. De blir båret inn, oftest i bagasjen. Med en rask sjekk når du kommer frem og noen enkle vaner når du kommer hjem, reduserer du risikoen mye.</p>
<h2>Slik ser veggedyr ut</h2>
<p>Voksne veggedyr er flate, rødbrune og omtrent på størrelse med et eplefrø. Ungene er mindre og lysere. De gjemmer seg i sprekker nær der folk sover, og kommer fram om natten.</p>
<h2>To-minutters-sjekken</h2>
<ul><li>Sett bagasjen på badet eller på et bagasjestativ, ikke på sengen eller gulvet.</li><li>Trekk av lakenet i ett hjørne og se langs madrassens sømmer og kanter.</li><li>Se etter små svarte prikker, hudskall eller levende dyr.</li><li>Sjekk bak sengegavlen hvis den lar seg flytte.</li></ul>
<div class="box"><b>Finner du noe?</b> Si fra i resepsjonen og be om et rom som ikke ligger vegg i vegg med det første.</div>
<h2>Når du kommer hjem</h2>
<p>Pakk ut i gangen eller på badet, ikke på soverommet. Vask klær du har brukt på høyeste temperatur tøyet tåler, og tørk dem i tørketrommel. Ting som ikke tåler vask kan legges i fryseren i flere døgn. Støvsug kofferten og ta posen ut med en gang.</p>
{prod("Utstyr mot veggedyr", "Feller, overvåking og utstyr til reise og hjem.", "insekter", "art-veggedyr")}
<h2>Mistenker du veggedyr hjemme?</h2>
<p>Ikke flytt madrasser og møbler mellom rom, og ikke kast dem uinnpakket. Da sprer du problemet. Veggedyr er vanskelige å bli kvitt på egen hånd, så kontakt en skadedyrtekniker tidlig.</p>
<p class="small mute">Eksempelartikkel i konseptet. Fakta skal kvalitetssikres mot fagkilder, for eksempel Folkehelseinstituttet, før publisering.</p>
</div></article>'''),
}

PODCAST = '''<section class="band slate"><div class="wrap" style="max-width:900px">
<h1>Kryp &amp; kunnskap</h1>
<p class="mute" style="font-size:18px;max-width:60ch">En podkast om skadedyr i hus, hage og bedrift. To programledere, ett skadedyr per episode, og konkrete råd du kan bruke samme dag.</p>
</div></section>
<section class="band"><div class="wrap" style="max-width:900px">
<h2>Episoder</h2>
<div style="display:grid;gap:14px">
''' + "".join(f'''<div style="display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:16px;align-items:center;background:var(--card);border-radius:16px;padding:16px 20px"><span style="width:52px;height:52px;border-radius:50%;background:var(--y);display:grid;place-items:center"><svg width="18" height="18" viewBox="0 0 16 16"><path d="M4 2l10 6-10 6z" fill="#18201d"/></svg></span><span><span class="small mute">Episode {n}</span><br><b>{t}</b><br><span class="small mute">{d}</span></span><span class="small mute" style="white-space:nowrap">{l}</span></div>
''' for n,t,d,l in [
 (3,"Skjeggkre: hvorfor nye boliger får dem","Om fukt, byggematerialer og hvorfor tålmodighet er nøkkelen.","22 min"),
 (2,"Veggedyr: den uønskede souveniren","Hvordan de sprer seg med bagasje, og hva du gjør når du kommer hjem.","27 min"),
 (1,"Mus: småkrypet som kommer inn med høsten","Inngangsveier, feller og de vanligste feilene folk gjør.","24 min")]) + '''</div>
<div class="box"><b>Om konseptet:</b> Episodene lages med manus fra fagartiklene, to faste stemmer og ett stillbilde fra studio per episode. Lydavspilling er ikke koblet på i denne skissen.</div>
</div></section>
'''

if __name__ == "__main__":
    for path, (title, desc, body) in ARTICLES.items():
        f = ROOT / path; f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(head(title, desc, "../") + body + foot("../"), encoding="utf-8")
    (ROOT / "podkast.html").write_text(head("Podkast – Skadedyrguiden", "Podkasten Kryp & kunnskap om skadedyr.", "") + PODCAST + foot(""), encoding="utf-8")
    print("ok")
