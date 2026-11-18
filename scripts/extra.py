"""FAQ-side og leksikonsider (én side per art). Kalles fra page.py."""
import json, html as H, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
ROOT = REPO / "site"
SHOP = "https://skadedyrbutikken.no/produkter/{}?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign={}"

# Hvilke artikler hører til hvilken art (for intern lenking)
REL = {"mus": ["mus-om-hosten", "fjellhytta", "hytta-ved-sjoen"], "skogmus": ["mus-pa-garden", "smagnagerar"], "rotte": ["rotter-i-byen"],
       "veggedyr": ["veggedyr-pa-reise"], "svaletege": ["veggedyr-pa-reise"], "skjeggkre": ["fukt-solvkre-skjeggkre"], "solvkre": ["fukt-solvkre-skjeggkre"],
       "veps": ["vepsebol", "humler-og-bier-i-veggen"], "kjempetreveps": ["vepsebol"], "stokkmaur": ["stokkmaur-eller-skogsmaur"],
       "skogsmaur": ["stokkmaur-eller-skogsmaur"], "jordmaur": ["stokkmaur-eller-skogsmaur"], "melmoll": [], "kakerlakk": [], "flatt": ["flatt-langs-kysten"]}
CAT = {"gnager": "gnagere", "insekt": "insekter", "midd": "hus-og-hage"}
SLUG = {"mus": "husmus", "skogmus": "skogmus", "rotte": "brunrotte", "veggedyr": "veggedyr", "svaletege": "svaletege", "skjeggkre": "skjeggkre",
        "solvkre": "solvkre", "veps": "stikkeveps", "kjempetreveps": "kjempetreveps", "stokkmaur": "stokkmaur", "skogsmaur": "rod-skogsmaur",
        "jordmaur": "svart-jordmaur", "melmoll": "melmoll", "kakerlakk": "tysk-kakerlakk", "flatt": "skogflatt"}
IMG = {"mus": "mus", "rotte": "rotte", "veggedyr": "veggedyr", "skjeggkre": "skjeggkre", "solvkre": "skjeggkre", "veps": "veps", "stokkmaur": "maur",
       "jordmaur": "maur", "melmoll": "melmoll", "skogmus": "region-midt", "flatt": "region-sor"}


def build(head, foot, prod):
    from faq import FAQ
    from articles import ARTICLES, EXTRA
    titles = {a["slug"]: a["title"] for a in ARTICLES + EXTRA}
    kb = json.loads((REPO / "kb/species.json").read_text())["species"]
    byid = {s["id"]: s for s in kb}

    # --- FAQ ---
    groups = "".join(f'''<section class="faqg"><h2>{H.escape(g)}</h2>''' + "".join(
        f'''<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p>{f'<p class="small"><a href="artikler/{s}.html">Les mer: {H.escape(titles.get(s, s))} →</a></p>' if s else ""}</details>'''
        for q, a, s in qs) + "</section>" for g, qs in FAQ)
    n = sum(len(q) for _, q in FAQ)
    body = f'''<style>.faqg{{margin-top:44px}}.faqg h2{{font-size:clamp(28px,3vw,38px)}}details{{border-bottom:1px solid var(--line);padding:18px 0}}details:first-of-type{{border-top:1px solid var(--line)}}
summary{{font-weight:600;font-size:18px;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px}}summary::-webkit-details-marker{{display:none}}summary::after{{content:"+";font-size:24px;line-height:1;color:var(--mute)}}details[open] summary::after{{content:"−"}}details p{{margin:10px 0 0;max-width:66ch}}
.qsearch{{width:100%;max-width:560px;min-height:52px;border-radius:999px;border:1.5px solid var(--line);padding:0 22px;font:17px "Schibsted Grotesk",sans-serif;background:var(--bg);color:var(--ink);margin-top:10px}}</style>
<section class="band" style="padding-bottom:0"><div class="wrap" style="max-width:900px"><span class="kicker">Spørsmål og svar</span>
<h1 style="font-size:clamp(40px,5.4vw,72px)">{n} svar om <em>skadedyr</em></h1>
<p class="mute" style="font-size:19px;max-width:52ch">Korte svar på det folk lurer mest på – med lenke til artikkelen som forklarer mer. Bygger på Folkehelseinstituttet og andre offentlige kilder.</p>
<input class="qsearch" id="qs" type="search" placeholder="Søk i spørsmålene, f.eks. «grevling»" aria-label="Søk i spørsmålene"></div></section>
<section class="band" style="padding-top:10px"><div class="wrap" style="max-width:900px">{groups}
<p class="small mute" style="margin-top:30px">Finner du ikke svaret? Folkehelseinstituttet har skadedyrtelefon på 21 07 77 00 hverdager kl. 13–14.</p></div></section>
<script>{{const q=document.getElementById("qs");q.addEventListener("input",()=>{{const v=q.value.trim().toLowerCase();document.querySelectorAll("details").forEach(d=>{{const hit=!v||d.textContent.toLowerCase().includes(v);d.hidden=!hit;if(v&&hit)d.open=true}});document.querySelectorAll(".faqg").forEach(g=>g.hidden=![...g.querySelectorAll("details")].some(d=>!d.hidden))}})}}</script>'''
    (ROOT / "sporsmal-og-svar.html").write_text(head("Spørsmål og svar om skadedyr – Skadedyrguiden",
        "Korte svar om mus, rotter, veggedyr, skjeggkre, veps, grevling, flått og andre skadedyr, med lenker til fagartikler.", "") + body + foot(""), encoding="utf-8")

    # --- Leksikon ---
    L = ROOT / "leksikon"; L.mkdir(exist_ok=True)
    cards = []
    import lexicon
    stats = json.loads((ROOT / "data/stats.json").read_text())["fhi"]
    artimg = {x["slug"]: x.get("img") for x in ARTICLES + EXTRA}
    for s in kb:
        slug = SLUG[s["id"]]
        body = lexicon.page(s, kb=kb, byid=byid, slugs=SLUG, img=IMG.get(s["id"]), imgs=IMG, rel=[r for r in REL.get(s["id"], []) if r in titles], titles=titles,
                            artimg=artimg, stats=stats, shop=SHOP.format(CAT.get(s["group"], "insekter"), "leksikon-" + slug))
        desc = f'{s["name"]} ({s["latin"]}): kjennetegn, forvekslingsarter og hva du gjør. Basert på Folkehelseinstituttets skadedyrhåndbok.'
        (L / f"{slug}.html").write_text(head(f'{s["name"]} – kjennetegn og råd – Skadedyrguiden', desc, "../") + body + foot("../"), encoding="utf-8")
        cards.append(f'<a class="lx" href="{slug}.html"><b>{H.escape(s["name"])}</b><em>{H.escape(s["latin"])}</em><span>{"Skadedyr" if s["pest"] else "Ufarlig"}</span></a>')
    idx = f'''<style>.lxg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:12px;margin-top:30px}}.lx{{display:grid;gap:2px;padding:20px 22px;border:1px solid var(--line);border-radius:16px;text-decoration:none}}.lx:hover{{background:var(--soft)}}.lx b{{font-size:19px}}.lx em{{color:var(--mute)}}.lx span{{font-size:13px;color:var(--mute);margin-top:6px}}</style>
<section class="band"><div class="wrap"><span class="kicker">Skadedyrleksikon</span><h1 style="font-size:clamp(40px,5.4vw,72px)">Kjenn igjen <em>dyret</em></h1>
<p class="mute" style="font-size:19px;max-width:56ch">Kjennetegn og forvekslingsarter for {len(kb)} dyr du kan møte i og rundt huset. Basert på Folkehelseinstituttets skadedyrhåndbok.</p>
<div class="lxg">{"".join(cards)}</div></div></section>'''
    (L / "index.html").write_text(head("Skadedyrleksikon – Skadedyrguiden", "Kjennetegn og forvekslingsarter for vanlige skadedyr i Norge, fra husmus og rotter til skjeggkre, veggedyr og veps.", "../") + idx + foot("../"), encoding="utf-8")


def newsletter_pages(head, foot):
    """Arkiv for Skadedyrbrevet + landingssider for bekreft/avmeld."""
    N = ROOT / "nyhetsbrev"; N.mkdir(exist_ok=True)
    form = '''<form class="nlf" data-nl><input type="email" required placeholder="din@epost.no" aria-label="E-postadresse"><input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true"><button class="btn y" type="submit">Meld meg på</button><p class="small mute" data-nlmsg aria-live="polite"></p></form>'''
    css = "<style>.nlf{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}.nlf input[type=email]{flex:1;min-width:220px;min-height:50px;border-radius:999px;border:1.5px solid var(--line);padding:0 20px;font:16px 'Schibsted Grotesk',sans-serif}.nlf p{flex-basis:100%;margin:0}.iss{display:block;padding:20px 0;border-top:1px solid var(--line);text-decoration:none}.iss b{font-size:20px;display:block}</style>"
    issues = sorted((json.loads(p.read_text()) for p in N.glob("20??-??.json")), key=lambda d: d["slug"], reverse=True)
    for d in issues:
        items = "".join(f'<h2>{H.escape(i["title"])}</h2><p>{H.escape(i["text"])}</p><p><a href="{H.escape(i["link"])}">{H.escape(i.get("link_label") or "Les mer")} →</a></p>' for i in d["items"])
        body = f'''<article class="band"><div class="art"><span class="kicker"><a href="index.html" style="color:inherit">Skadedyrbrevet</a> · {d["month"].capitalize()} {d["year"]}</span>
<h1 style="font-size:clamp(36px,4.6vw,58px)">{H.escape(d["subject"])}</h1><p style="font-size:19px">{H.escape(d["intro"])}</p>{items}
<div class="box"><b>Gjør dette i {d["month"]}</b><ul>{"".join(f"<li>{H.escape(c['text'])}</li>" for c in d["checklist"])}</ul></div>
<h2>Kilder</h2><ul class="small">{"".join(f'<li><a href="{H.escape(u)}" rel="noopener">{H.escape(u)}</a></li>' for u in d["sources"])}</ul>
<div class="box"><b>Få neste brev på e-post</b>Ett kort brev i måneden. Du bekrefter adressen før du får noe.{form}</div></div></article>'''
        (N / f'{d["slug"]}.html').write_text(head(f'{d["subject"]} – Skadedyrbrevet {d["month"]} {d["year"]}', d["preheader"], "../") + css + body + foot("../"), encoding="utf-8")
    lst = "".join(f'<a class="iss" href="{d["slug"]}.html"><span class="small mute">{d["month"].capitalize()} {d["year"]}</span><b>{H.escape(d["subject"])}</b><span class="mute">{H.escape(d["preheader"])}</span></a>' for d in issues) or '<p class="mute">Første brev kommer snart.</p>'
    idx = f'''<section class="band"><div class="wrap" style="max-width:820px"><span class="kicker">Nyhetsbrev</span><h1 style="font-size:clamp(40px,5.4vw,72px)">Skadedyr<em>brevet</em></h1>
<p class="mute" style="font-size:19px">Ett kort brev i måneden om hva som er i sesong – og hva du bør gjøre før det blir et problem. Basert på aktuelle saker og offentlige kilder, faktasjekket mot kildene før utsending.</p>{form}<div style="margin-top:40px">{lst}</div></div></section>'''
    (N / "index.html").write_text(head("Skadedyrbrevet – månedlig nyhetsbrev om skadedyr", "Ett kort brev i måneden om hvilke skadedyr som er i sesong og hva du bør gjøre nå.", "../") + css + idx + foot("../"), encoding="utf-8")
    for slug, h1, txt in [("bekreftet", "Takk – du er påmeldt", "E-postadressen er bekreftet. Månedens Skadedyrbrev er på vei til innboksen din, og du får et nytt brev hver måned."),
                          ("avmeldt", "Du er meldt av", "Du får ikke flere Skadedyrbrev. Ombestemmer du deg, kan du melde deg på igjen når som helst."),
                          ("ugyldig", "Lenken virker ikke", "Lenken er utløpt eller ufullstendig. Meld deg på på nytt, så sender vi en ny bekreftelse.")]:
        b = f'<section class="band"><div class="wrap" style="max-width:720px"><span class="kicker">Skadedyrbrevet</span><h1 style="font-size:clamp(40px,5vw,64px)">{h1}</h1><p style="font-size:19px">{txt}</p><p><a class="btn arrow" href="../index.html">Til forsiden </a> <a class="btn arrow" href="index.html">Tidligere brev </a></p>{form if slug == "ugyldig" else ""}</div></section>'
        (N / f"{slug}.html").write_text(head(f"{h1} – Skadedyrbrevet", txt, "../").replace("<title>", "<title>", 1) + css + b + foot("../"), encoding="utf-8")
