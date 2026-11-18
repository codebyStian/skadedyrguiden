"""Leksikonside per art: mørk hero, nøkkeltall fra FHI, kjennetegn, forveksling, sesongkurve, relaterte artikler og sidekolonne."""
import html as H

E = H.escape
MN = ["jan", "feb", "mar", "apr", "mai", "jun", "jul", "aug", "sep", "okt", "nov", "des"]
MNL = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
GROUP = {"gnager": "Gnager", "insekt": "Insekt", "midd": "Midd"}
FHI = {"skjeggkre": "Skjeggkre", "veggedyr": "Veggedyr", "veps": "Stikkeveps", "stokkmaur": "Stokkmaur", "jordmaur": "Svart jordmaur", "kakerlakk": "Tysk kakerlakk"}

CSS = """<style>
.sx{background:#0f2a24;color:#fff;padding:64px 0 90px}.sx .wrap{display:grid;grid-template-columns:1.05fr 1fr;gap:48px;align-items:center}
.sx h1{font-size:clamp(48px,6.4vw,92px);margin:.15em 0 .05em;color:#fff}.sx .lat{font-style:italic;color:#b9c6c1;font-size:20px;margin:0 0 22px}
.sx .crumb{font-size:14px;color:#b9c6c1;margin:0}.sx .crumb a{color:#fff}.badges{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 26px}
.badge{border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 14px;font-size:14px}.badge.y{background:#f2c230;color:#13201c;border-color:#f2c230;font-weight:600}
.sx .ph{aspect-ratio:4/3;border-radius:22px;overflow:hidden}.sx .ph img{width:100%;height:100%;object-fit:cover}.sx .ctas{display:flex;flex-wrap:wrap;gap:10px}
.sx .btn.ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.4)}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden;margin:-46px 0 0;position:relative;box-shadow:0 18px 40px -24px rgba(0,0,0,.35)}
.tiles.n3{grid-template-columns:repeat(3,1fr)}.tile{background:#fff;padding:22px 24px}.tile small{display:block;color:var(--mute);font-size:13px;margin-bottom:8px}.tile b{font-family:"Instrument Serif",serif;font-weight:400;font-size:40px;line-height:1}.tile span{display:block;font-size:13px;color:var(--mute);margin-top:8px}
.lxb{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:56px;padding:64px 0 80px}.lxb h2{font-size:clamp(28px,3vw,40px);margin:0 0 18px}.lxb section+section{margin-top:60px}
.feat{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;list-style:none;padding:0;margin:0}.feat li{display:flex;gap:14px;align-items:center;border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:0}
.feat li i{flex:none;width:30px;height:30px;border-radius:50%;background:#f2c230;display:grid;place-items:center;font-style:normal;font-size:13px;font-weight:700;color:#13201c}
.bars{display:grid;grid-template-columns:repeat(12,1fr);gap:6px;align-items:end;height:180px;border-bottom:1px solid var(--line);margin-bottom:34px}.bars div{background:#dfe7e3;border-radius:6px 6px 0 0;position:relative}.bars div.top{background:#f2c230}
.bars div span{position:absolute;bottom:-26px;left:0;right:0;text-align:center;font-size:12px;color:var(--mute)}
.vs{display:grid;grid-template-columns:1fr auto 1fr;border:1px solid var(--line);border-radius:18px;overflow:hidden;margin-bottom:12px}.vs>div{padding:20px 22px}.vs .mid{display:grid;place-items:center;background:var(--soft);font-family:"Instrument Serif",serif;font-size:22px;padding:0 16px}
.cred{font-size:12px;color:var(--mute);margin-top:6px}.cred a{color:inherit}.cred.dk{color:#9fb0aa}.th-f{margin:0 0 14px}.th-f .th{margin-bottom:0!important}
.fxg{display:grid;gap:14px}.fx{border-radius:18px;padding:22px 24px;background:var(--soft)}.fx small{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-bottom:10px}
.fx ul,.fx ol{margin:0;padding:0;list-style:none}.fx li{margin:0 0 8px;line-height:1.45}
.fx.id{display:grid;grid-template-columns:240px 1fr;gap:28px;background:#fff;border:1px solid var(--line)}.fx.id .big b{font-family:"Instrument Serif",serif;font-weight:400;font-size:54px;line-height:1;display:block;margin-bottom:12px}.fx.id .big li{font-size:14px;color:var(--mute)}
.fx ul.ok li{padding-left:28px;position:relative}.fx ul.ok li::before{content:"✓";position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;background:#f2c230;font-size:12px;font-weight:700;display:grid;place-items:center}
.fx.sign{background:#0f2a24;color:#fff}.fx.sign small{color:#9fb0aa}.fx.sign ol{counter-reset:s;display:grid;grid-template-columns:1fr 1fr;gap:10px 22px}.fx.sign li{counter-increment:s;padding-left:38px;position:relative}
.fx.sign li::before{content:counter(s);position:absolute;left:0;top:-2px;width:26px;height:26px;border-radius:50%;background:#f2c230;color:#13201c;font-weight:700;font-size:13px;display:grid;place-items:center}
.fx.where li{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;margin:0 6px 8px 0;font-size:14.5px}.fx.where li::before{content:"📍 "}
.fx.life ol{border-left:2px solid #f2c230;margin-left:6px}.fx.life li{padding-left:22px;position:relative}.fx.life li::before{content:"";position:absolute;left:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:#f2c230}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.fx.harm{background:#fbe9e4}.fx.prev{background:#e4efe8}.fx.act{background:#fdf3d0}.trio li{font-size:15px;padding-left:16px;position:relative}.trio li::before{content:"–";position:absolute;left:0}
.icg{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.ic{border:1px solid var(--line);border-radius:16px;padding:20px 22px}.ic h3{margin:0 0 8px;font-size:17px}.ic ul{margin:0;padding-left:18px}.ic li{margin:4px 0;font-size:15.5px}
.vs b{font-size:19px;display:block}.vs .th{aspect-ratio:4/3;border-radius:12px;overflow:hidden;margin-bottom:14px}.vs .th img{width:100%;height:100%;object-fit:cover}.vs .th[data-ph]{min-height:0}.vs em{color:var(--mute);font-size:14px}.vs p{margin:10px 0 0;font-size:15px}
.aside{position:sticky;top:96px;display:grid;gap:14px;align-self:start}.card{border-radius:18px;padding:24px}.card.dk{background:#0f2a24;color:#fff}.card.dk p{color:#b9c6c1}.card.sf{background:var(--soft)}
.card h3{margin:0 0 6px;font-size:20px}.card p{margin:0 0 16px;font-size:15px}.card .btn{width:100%;justify-content:center;box-sizing:border-box}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr));gap:14px}.rel a{text-decoration:none;border-radius:16px;overflow:hidden;border:1px solid var(--line);display:block}.rel a:hover{background:var(--soft)}.rel .ph{aspect-ratio:16/10;border-radius:0}.rel .ph img{width:100%;height:100%;object-fit:cover}.rel b{display:block;padding:14px 16px 16px;font-size:16px;line-height:1.35}
.more{display:flex;flex-wrap:wrap;gap:8px}.more a{border:1px solid var(--line);border-radius:999px;padding:9px 16px;text-decoration:none;font-size:15px}.more a:hover{background:var(--soft)}
@media(max-width:900px){.sx .wrap,.lxb{grid-template-columns:1fr}.tiles,.tiles.n3{grid-template-columns:repeat(2,1fr)}.tiles.n3 .tile:last-child{grid-column:span 2}.feat,.icg,.trio,.fx.id,.fx.sign ol{grid-template-columns:1fr}.aside{position:static}.vs{grid-template-columns:1fr}.vs .mid{padding:6px}}
</style>"""


PHOTOS, INFO = {}, {}
FIELDS = [("storrelse", "Størrelse"), ("utseende", "Utseende"), ("hvor", "Hvor du finner den"), ("tegn", "Spor og tegn"), ("livssyklus", "Livssyklus og sesong"),
          ("skade", "Skade og helse"), ("forebygg", "Forebygging"), ("tiltak", "Slik blir du kvitt den")]


def who(p):
    a = p.get("author") or ""
    return "iNaturalist-bruker" if not a or a.lower().startswith("no rights") else a


def credit(sid):
    p = PHOTOS.get(sid)
    if not p: return ""
    lic = f'<a href="{E(p["license_url"])}" rel="license noopener">{E(p["license"])}</a>' if p.get("license_url") else E(p["license"])
    return f'<figcaption class="cred">Foto: {E(who(p))}{" (beskåret)" if p.get("cropped") else ""} · {lic} · <a href="{E(p["page"])}" rel="noopener">Wikimedia Commons</a></figcaption>'


def thumb(sid, fallback, name):
    if sid in PHOTOS:
        return f'<figure class="th-f"><div class="ph th"><img src="../assets/img/foto-{sid}.webp" alt="{E(name)} ({E(PHOTOS[sid]["taxon"])})" loading="lazy"></div>{credit(sid)}</figure>'
    # Navngitte arter vises aldri med illustrasjonsbilde – mangler ekte foto, vises navnekort.
    return f'<figure class="th-f"><div class="ph th" data-ph="1" data-label="{E(name)}"></div></figure>'
    fb = ""
    return f'<div class="ph th" data-label="{E(name)}"><img src="../assets/img/art-{sid}.webp" alt="{E(name)}" loading="lazy" onerror="{fb}"></div>'


def cap(t):
    return t[:1].upper() + t[1:]


RECS = None


def page(s, *, kb, byid, slugs, img, imgs=None, rel, titles, artimg, stats, shop):
    mon = stats["monthly"].get(FHI.get(s["id"], ""))
    yr = stats["yearly"].get(FHI.get(s["id"], ""))
    tiles = []
    if mon:
        t = max(range(12), key=lambda i: mon[i])
        tiles.append(("Mest aktiv", cap(MNL[t]), f"{mon[t]:.0f} % av årets oppdrag"))
    if yr:
        last = max(yr); prev = str(int(last) - 5)
        tiles.append((f"Oppdrag i {last}", f"{yr[last]:,}".replace(",", " "), "hos skadedyrfirma (FHI)"))
        if yr.get(prev):
            ch = round((yr[last] - yr[prev]) / yr[prev] * 100)
            tiles.append(("Endring på fem år", f"{'+' if ch > 0 else '−' if ch < 0 else ''}{abs(ch)} %", f"fra {yr[prev]} i {prev}"))
    tiles += [("Kjennetegn", str(len(s["features"])), "å se etter"), ("Forveksles med", str(len(s["confusable"])), "art" if len(s["confusable"]) == 1 else "arter"),
              ("Gruppe", GROUP.get(s["group"], cap(s["group"])), "i leksikonet")]
    tiles_h = f'<div class="tiles n{min(4, len(tiles))}">' + "".join(f"<div class='tile'><small>{a}</small><b>{b}</b><span>{c}</span></div>" for a, b, c in tiles[:4]) + "</div>"
    feats = "".join(f"<li><i>{i + 1}</i><span>{E(cap(f))}</span></li>" for i, f in enumerate(s["features"]))
    bars = ""
    if mon:
        mx = max(mon); top = max(range(12), key=lambda i: mon[i])
        bars = ("<section><h2>Når den er mest aktiv</h2><div class='bars' role='img' aria-label='Andel oppdrag per måned'>" +
                "".join(f"<div class='{'top' if i == top else ''}' style='height:{max(4, v / mx * 100):.0f}%' title='{MN[i]}: {v} %'><span>{MN[i]}</span></div>" for i, v in enumerate(mon)) +
                "</div><p class='small mute'>Andel av skadedyrfirmaenes oppdrag per måned. Kilde: FHI Statistikk, skadedyrstatistikken.</p></section>")
    cmp = "".join(compare_block(s["id"], c["id"], byid, slugs) for c in s["confusable"] if c["id"] in byid)
    vs = cmp or "".join(f'<div class="vs"><div>{thumb(s["id"], img, s["name"])}<b>{E(s["name"])}</b><em>{E(s["latin"])}</em></div><div class="mid">eller</div>'
                 f'<div><a href="{slugs[c["id"]]}.html" style="display:block">{thumb(c["id"], (imgs or {}).get(c["id"]), byid[c["id"]]["name"])}</a><b><a href="{slugs[c["id"]]}.html">{E(byid[c["id"]]["name"])}</a></b><em>{E(byid[c["id"]]["latin"])}</em><p>{E(cap(c["how"]))}.</p></div></div>'
                 for c in s["confusable"] if c["id"] in byid)
    relh = "".join(f'<a href="../artikler/{r}.html"><div class="ph" data-label="Artikkel">' +
                   (f'<img src="../assets/img/{artimg[r]}.webp" alt="" loading="lazy" onerror="this.parentNode.dataset.ph=1;this.remove()">' if artimg.get(r) else "") +
                   f'</div><b>{E(titles[r])}</b></a>' for r in rel)
    more = "".join(f'<a href="{slugs[o["id"]]}.html">{E(o["name"])}</a>' for o in kb if o is not s)
    if s["id"] in PHOTOS:
        image = f'<img src="../assets/img/foto-{s["id"]}.webp" alt="{E(s["name"])}">'
    else:
        image = ""
    inf = INFO.get(s["id"], {})
    li = lambda k: "".join(f"<li>{E(cap(x))}</li>" for x in inf.get(k, []))
    import re as _re
    texts = inf.get("storrelse", []) + s["features"]
    rng = r"\d+(?:[,.]\d+)?\s*(?:[–-]|til)\s*\d+(?:[,.]\d+)?\s*(?:mm|cm)"
    pref = [x for x in texts if not _re.search(r"dronning|hann", x, _re.I)] + texts
    size = next((m.group(0) for x in pref for m in [_re.search(rng, x)] if m), "") or \
           next((m.group(0) for x in pref for m in [_re.search(r"\d+(?:[,.]\d+)?\s*(?:mm|cm)", x)] if m), "")
    size = _re.sub(r"\s*til\s*", "–", size)
    parts = []
    if inf.get("storrelse") or inf.get("utseende"):
        parts.append(f'''<div class="fx id"><div class="big"><small>Størrelse</small><b>{E(size) or "–"}</b><ul>{li("storrelse")}</ul></div><div><small>Utseende</small><ul class="ok">{li("utseende")}</ul></div></div>''')
    if inf.get("tegn"):
        parts.append(f'''<div class="fx sign"><small>Spor og tegn – dette ser du etter</small><ol>{li("tegn")}</ol></div>''')
    if inf.get("hvor"):
        parts.append(f'''<div class="fx where"><small>Hvor du finner den</small><ul>{li("hvor")}</ul></div>''')
    if inf.get("livssyklus"):
        parts.append(f'''<div class="fx life"><small>Livssyklus og sesong</small><ol>{li("livssyklus")}</ol></div>''')
    trio = "".join(f'<div class="fx {c}"><small>{t}</small><ul>{li(k)}</ul></div>' for k, t, c in [("skade", "Skade og helse", "harm"), ("forebygg", "Forebygging", "prev"), ("tiltak", "Slik blir du kvitt den", "act")] if inf.get(k))
    if trio: parts.append(f'<div class="trio">{trio}</div>')
    infoh = "".join(parts)
    infoh = f'<section><h2>Fakta om {E(s["name"].lower())}</h2><div class="fxg">{infoh}</div><p class="small mute">Kilde: <a href="{E(s["source"]["url"])}" rel="noopener">{E(s["source"]["title"])}</a>.</p></section>' if infoh else ""
    pest_card = (f'<div class="card sf"><h3>Utstyr mot {E(s["name"].lower())}</h3><p>Feller, åter og forebygging hos Skadedyrbutikken.</p><a class="btn arrow" href="{shop}">Se utvalget </a></div>'
                 if s["pest"] else '<div class="card sf"><h3>Ikke et skadedyr</h3><p>Denne arten gjør normalt ingen skade og trenger ikke bekjempes.</p></div>')
    return f'''{CSS}{CMP_CSS}<section class="sx"><div class="wrap"><div>
<p class="crumb"><a href="index.html">Skadedyrleksikon</a> / {E(GROUP.get(s["group"], ""))}</p>
<h1>{E(s["name"])}</h1><p class="lat">{E(s["latin"])}</p>
<div class="badges"><span class="badge {"y" if s["pest"] else ""}">{"Skadedyr" if s["pest"] else "Ikke et skadedyr"}</span><span class="badge">{E(GROUP.get(s["group"], ""))}</span>{'<span class="badge">Kontrollert mot FHI</span>' if s.get("checked") else ""}</div>
<div class="ctas"><a class="btn y arrow" href="../index.html#hvadet">Usikker? Last opp et bilde </a>{f'<a class="btn ghost arrow" href="{shop}">Se utstyr </a>' if s["pest"] else ""}</div></div>
<figure style="margin:0"><div class="ph" data-label="{E(s["name"])}">{image}</div>{credit(s["id"]).replace('class="cred"', 'class="cred dk"')}</figure></div></section>
<div class="wrap">{tiles_h}<div class="lxb"><div>
<section><h2>Slik kjenner du den igjen</h2><ul class="feat">{feats}</ul></section>
{infoh}
{RECS("sp:" + s["id"], "leksikon-" + s["id"], "Utstyr mot " + s["name"].lower()) if s["pest"] and RECS else ""}
{f"<section><h2>Kan forveksles med</h2>{vs}</section>" if vs else ""}
{bars}
{f'<section><h2>Les mer</h2><div class="rel">{relh}</div></section>' if relh else ""}
<section><h2>Flere i leksikonet</h2><div class="more">{more}</div></section>
</div><aside class="aside">
<div class="card dk"><h3>Er du usikker?</h3><p>Last opp et bilde. Du får et forslag til art og kjennetegnene vurderingen bygger på, kontrollert mot FHIs skadedyrhåndbok.</p><a class="btn y arrow" href="../index.html#hvadet">Finn ut hvilket dyr det er </a></div>
{pest_card}
<div class="card sf"><h3>Kilde</h3><p><a href="{s["source"]["url"]}" rel="noopener">{E(s["source"]["title"])}</a></p><p class="small mute" style="margin:0">Ved større angrep bør du kontakte et godkjent skadedyrfirma.</p></div>
</aside></div></div>'''


# ---------- Side-om-side-sammenligning ----------
COMPARE = {}
CMP_CSS = """<style>
.cmpx{border:1px solid var(--line);border-radius:22px;overflow:hidden;margin:2em 0;background:#fff}
.cmpx .test{background:#0f2a24;color:#fff;padding:18px 24px;display:flex;gap:14px;align-items:flex-start}.cmpx .test b{color:#f2c230;white-space:nowrap;flex:none}
.cmpx .pics{display:grid;grid-template-columns:1fr 1fr}.cmpx .pic{position:relative}.cmpx .pic .ph{aspect-ratio:4/3;border-radius:0}.cmpx .pic img{width:100%;height:100%;object-fit:cover}
.cmpx .pic .nm{position:absolute;left:14px;bottom:14px;background:rgba(15,42,36,.86);color:#fff;border-radius:12px;padding:8px 14px}.cmpx .pic .nm b{display:block;font-size:18px}.cmpx .pic .nm em{font-size:13px;color:#cfdad6}
.cmpx .pic .nm a{color:#fff}.cmpx .pic+.pic{border-left:3px solid #fff}
.cmpx table{width:100%;border-collapse:collapse;font-size:15.5px}.cmpx th,.cmpx td{padding:13px 18px;border-top:1px solid var(--line);vertical-align:top;text-align:left}
.cmpx th{width:22%;font-weight:600;color:var(--mute);font-size:14px}.cmpx td{width:39%}.cmpx tr.key{background:#fdf3d0}.cmpx tr.key th{color:#13201c}
.cmpx tr.key th::after{content:"Sikreste forskjell";display:block;font-size:11px;font-weight:700;color:#8a6a00;margin-top:3px;text-transform:uppercase;letter-spacing:.04em}
.cmpx .cr{font-size:11.5px;color:var(--mute);padding:10px 18px;border-top:1px solid var(--line)}.cmpx .cr a{color:inherit}
@media(max-width:640px){.cmpx th{width:28%}.cmpx th,.cmpx td{padding:10px 10px;font-size:14px}.cmpx .pic .nm{left:8px;bottom:8px;padding:6px 10px}.cmpx .pic .nm b{font-size:15px}}
</style>"""


def compare_block(a, b, kb_by_id, slugs, base="../", link=True):
    d = COMPARE.get(f"{a}|{b}") or COMPARE.get(f"{b}|{a}")
    if not d: return ""
    flip = f"{a}|{b}" not in COMPARE
    A, B = kb_by_id[a], kb_by_id[b]

    def pic(s):
        img = f'<img src="{base}assets/img/foto-{s["id"]}.webp" alt="{E(s["name"])}" loading="lazy">' if s["id"] in PHOTOS else ""
        nm = f'<a href="{base}leksikon/{slugs[s["id"]]}.html">{E(s["name"])}</a>' if link else E(s["name"])
        return f'<div class="pic"><div class="ph" data-label="{E(s["name"])}"{"" if img else " data-ph=1"}>{img}</div><div class="nm"><b>{nm}</b><em>{E(s["latin"])}</em></div></div>'
    rows = "".join(f'<tr class="{"key" if r.get("key") else ""}"><th>{E(r["trait"])}</th><td>{E(cap(r["b"] if flip else r["a"]))}</td><td>{E(cap(r["a"] if flip else r["b"]))}</td></tr>' for r in d["rows"])
    creds = " · ".join(f'{E(kb_by_id[i]["name"])}: {E(who(PHOTOS[i]))}{" (beskåret)" if PHOTOS[i].get("cropped") else ""}, <a href="{E(PHOTOS[i].get("license_url") or PHOTOS[i]["page"])}" rel="license noopener">{E(PHOTOS[i]["license"])}</a>' for i in (a, b) if i in PHOTOS)
    return f'''<div class="cmpx">{f'<div class="test"><b>Raskeste test</b><span>{E(d["test"])}</span></div>' if d.get("test") else ""}
<div class="pics">{pic(A)}{pic(B)}</div><table><thead><tr><th></th><td><b>{E(A["name"])}</b></td><td><b>{E(B["name"])}</b></td></tr></thead><tbody>{rows}</tbody></table>
{f'<div class="cr">Foto: {creds}</div>' if creds else ""}</div>'''


def load(repo):
    import json, pathlib
    repo = pathlib.Path(repo)
    for target, f in ((PHOTOS, repo / "site/data/photos.json"), (INFO, repo / "kb/species_info.json"), (COMPARE, repo / "kb/compare.json")):
        if f.exists(): target.update(json.loads(f.read_text()))
    return {s["id"]: s for s in json.loads((repo / "kb/species.json").read_text())["species"]}


ARTICLE_PAIRS = {"stokkmaur-eller-skogsmaur": [("stokkmaur", "skogsmaur"), ("stokkmaur", "jordmaur")], "fukt-solvkre-skjeggkre": [("skjeggkre", "solvkre")],
                 "mus-pa-garden": [("mus", "skogmus")], "rotter-i-byen": [("rotte", "mus")], "smagnagerar": [("mus", "skogmus")],
                 "vepsebol": [("veps", "kjempetreveps")], "humler-og-bier-i-veggen": [], "veggedyr-pa-reise": [("veggedyr", "svaletege")]}
SLUGS = {"mus": "husmus", "skogmus": "skogmus", "rotte": "brunrotte", "veggedyr": "veggedyr", "svaletege": "svaletege", "skjeggkre": "skjeggkre",
         "solvkre": "solvkre", "veps": "stikkeveps", "kjempetreveps": "kjempetreveps", "stokkmaur": "stokkmaur", "skogsmaur": "rod-skogsmaur",
         "jordmaur": "svart-jordmaur", "melmoll": "melmoll", "kakerlakk": "tysk-kakerlakk", "flatt": "skogflatt"}


def article_compare(slug, byid):
    blocks = "".join(compare_block(a, b, byid, SLUGS) for a, b in ARTICLE_PAIRS.get(slug, []))
    return (CMP_CSS + '<h2>Se forskjellen</h2>' + blocks) if blocks else ""
