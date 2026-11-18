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
    for s in kb:
        slug = SLUG[s["id"]]; img = IMG.get(s["id"])
        rel = [r for r in REL.get(s["id"], []) if r in titles]
        conf = "".join(f'<li><a href="{SLUG[c["id"]]}.html">{H.escape(byid[c["id"]]["name"])}</a>: {H.escape(c["how"])}</li>' for c in s["confusable"] if c["id"] in byid)
        body = f'''<section class="band" style="padding-bottom:0"><div class="wrap ahero">
<div><span class="kicker"><a href="index.html" style="color:inherit">Skadedyrleksikon</a> · {"Skadedyr" if s["pest"] else "Ikke et skadedyr"}</span>
<h1 style="font-size:clamp(40px,5vw,64px)">{H.escape(s["name"])}</h1><p class="mute" style="font-size:19px"><em>{H.escape(s["latin"])}</em></p>
<p><a class="btn y arrow" href="../index.html#hvadet">Usikker? Last opp et bilde </a></p></div>
<div class="ph" data-label="{H.escape(s["name"])}">{f'<img src="../assets/img/{img}.webp" alt="" onerror="this.parentNode.dataset.ph=1;this.remove()">' if img else ""}</div>
</div></section>
<article class="band"><div class="art">
<h2>Kjennetegn</h2><ul>{"".join(f"<li>{H.escape(f)}</li>" for f in s["features"])}</ul>
{f"<h2>Kan forveksles med</h2><ul>{conf}</ul>" if conf else ""}
{f'<h2>Les mer</h2><ul>{"".join(f"""<li><a href="../artikler/{r}.html">{H.escape(titles[r])}</a></li>""" for r in rel)}</ul>' if rel else ""}
{prod("Utstyr hos Skadedyrbutikken", "Produkter mot " + s["name"].lower() + ".", CAT.get(s["group"], "insekter"), "leksikon-" + slug) if s["pest"] else '<div class="box"><b>Ikke et skadedyr</b>Denne arten gjør normalt ingen skade og trenger ikke bekjempes.</div>'}
<p class="small mute">Kilde: <a href="{s["source"]["url"]}" rel="noopener">{H.escape(s["source"]["title"])}</a>.</p>
</div></article>'''
        desc = f'{s["name"]} ({s["latin"]}): kjennetegn, forvekslingsarter og hva du gjør. Basert på Folkehelseinstituttets skadedyrhåndbok.'
        (L / f"{slug}.html").write_text(head(f'{s["name"]} – kjennetegn og råd – Skadedyrguiden', desc, "../") + body + foot("../"), encoding="utf-8")
        cards.append(f'<a class="lx" href="{slug}.html"><b>{H.escape(s["name"])}</b><em>{H.escape(s["latin"])}</em><span>{"Skadedyr" if s["pest"] else "Ufarlig"}</span></a>')
    idx = f'''<style>.lxg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:12px;margin-top:30px}}.lx{{display:grid;gap:2px;padding:20px 22px;border:1px solid var(--line);border-radius:16px;text-decoration:none}}.lx:hover{{background:var(--soft)}}.lx b{{font-size:19px}}.lx em{{color:var(--mute)}}.lx span{{font-size:13px;color:var(--mute);margin-top:6px}}</style>
<section class="band"><div class="wrap"><span class="kicker">Skadedyrleksikon</span><h1 style="font-size:clamp(40px,5.4vw,72px)">Kjenn igjen <em>dyret</em></h1>
<p class="mute" style="font-size:19px;max-width:56ch">Kjennetegn og forvekslingsarter for {len(kb)} dyr du kan møte i og rundt huset. Basert på Folkehelseinstituttets skadedyrhåndbok.</p>
<div class="lxg">{"".join(cards)}</div></div></section>'''
    (L / "index.html").write_text(head("Skadedyrleksikon – Skadedyrguiden", "Kjennetegn og forvekslingsarter for vanlige skadedyr i Norge, fra husmus og rotter til skjeggkre, veggedyr og veps.", "../") + idx + foot("../"), encoding="utf-8")
