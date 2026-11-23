"""Interaktive verktøysider: «Tett huset»-sjekkliste og fellekalkulator. Bygges av scripts/page.py."""

SHOP = "https://skadedyrbutikken.no/produkter/{}?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign={}"

STYLE = """<style>
.tool-hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:end}
.prog{background:var(--soft);border-radius:20px;padding:22px 24px}
.prog .big{font:400 64px/1 "Instrument Serif",Georgia,serif}
.pbar2{height:10px;border-radius:5px;background:var(--bg);overflow:hidden;margin:12px 0 6px}.pbar2 i{display:block;height:100%;background:var(--y);transition:width .4s}
.grp{margin-top:40px}.grp h2{font-size:clamp(28px,3vw,38px)}
.item{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 18px;align-items:center;padding:16px 0;border-bottom:1px solid var(--line)}
.item b{display:block;font-size:17px}.item span{color:var(--mute);font-size:15px}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.seg button{min-height:42px;padding:0 16px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);font:600 14.5px "Schibsted Grotesk",sans-serif;cursor:pointer}
.seg button[aria-pressed=true].ok{background:#2c4a3f;border-color:#2c4a3f;color:#fff}
.seg button[aria-pressed=true].fix{background:var(--y);border-color:var(--y);color:#111715}
.side2{position:sticky;top:96px;background:var(--pine);color:var(--onDark);border-radius:22px;padding:26px}
.side2 h3{font:400 34px/1 "Instrument Serif",Georgia,serif;margin-bottom:10px}
.side2 ul{padding-left:1.1em;margin:0 0 16px}.side2 li{margin:6px 0}
.side2 .mute{color:var(--muteDark)}
.cols2{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:start}
.form{display:grid;gap:22px}
.field label,.field legend{display:block;font-weight:600;margin-bottom:8px}
.field fieldset{border:0;padding:0;margin:0}
.chips2{display:flex;gap:8px;flex-wrap:wrap}
.chips2 label{position:relative;display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;border:1.5px solid var(--line);cursor:pointer;font-weight:500}
.chips2 input{position:absolute;opacity:0;pointer-events:none}
.chips2 label:has(input:checked){background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chips2 label:has(input:focus-visible){outline:3px solid var(--y);outline-offset:3px}
.result2 .num{font:400 96px/1 "Instrument Serif",Georgia,serif;color:var(--y)}
.result2 table{width:100%;border-collapse:collapse;margin:14px 0;font-size:15px}.result2 td{padding:7px 0;border-bottom:1px solid #2a4840}.result2 td:last-child{text-align:right;font-variant-numeric:tabular-nums}
.warn{background:#7a2a1d;border-radius:14px;padding:14px 16px;margin:12px 0}
@media(max-width:860px){.tool-hero,.cols2{grid-template-columns:1fr}.side2{position:static}}
@media(max-width:600px){.item{grid-template-columns:1fr}}
@media print{.top,.note,footer,.seg,.side2 .btn{display:none!important}.side2{position:static;color:#000;background:#fff;border:1px solid #000}}
</style>"""

CHECK = [
 ("Ute rundt huset", [
   ("grunnmur", "Overgangen mellom grunnmur og vegg", "Ofte utsatt. Se etter sprekker og åpninger hele veien rundt.", "tettemasse"),
   ("kledning", "Under nederste del av kledningen", "Mus kommer ofte inn her.", "musebørste"),
   ("ventiler", "Lufteventiler og luftehull", "Åpne ventiler må ha netting.", "netting"),
   ("ror", "Rør, kabler og slanger som går inn i veggen", "Åpninger større enn 6 mm slipper inn mus.", "tettemasse"),
   ("gress", "Høyt gress, kratt og ved inntil veggen", "Gir skjul. Hold gresset nede og legg veden et stykke unna.", ""),
   ("fuglemat", "Fuglemat og nedfallsfrukt", "Ikke mat fugler på bakken.", "")]),
 ("Dører og porter", [
   ("dorer", "Ytterdører slutter tett mot terskelen", "En spalte under døra er nok for en mus.", "børsteliste"),
   ("karm", "Sprekker mellom karm og vegg", "Sjekk både dører og vinduer.", "tettemasse"),
   ("garasje", "Garasjeport og boddør", "Porter har ofte store åpninger nederst.", "børsteliste")]),
 ("Inne", [
   ("vask", "Under kjøkkenvasken der rørene kommer inn", "En klassisk vei inn.", "tettemasse"),
   ("komfyr", "Bak komfyr, kjøleskap og oppvaskmaskin", "Se etter hull og ekskrementer.", ""),
   ("kjeller", "Kjeller og krypkjeller", "Sjekk hjørner, sluk og rørgjennomføringer.", "tettemasse"),
   ("loft", "Loft og takfot", "Lytt etter krafsing om kvelden.", "netting")]),
 ("Mat og avfall", [
   ("torrvarer", "Tørrvarer i tette bokser", "Mel, gryn, frø og dyrefôr.", "bokser"),
   ("avfall", "Avfall i lukket beholder", "Både inne og ute.", ""),
   ("dyrefor", "Ikke mat til kjæledyr ute", "Trekker til seg både mus og rotter.", "")]),
]

NEEDS = {"tettemasse": ("Tettemasse eller tetteremser for gnagere", "gnagere"), "musebørste": ("Musebørster til kledning", "gnagere"),
         "netting": ("Metallnetting til ventiler", "gnagere"), "børsteliste": ("Børstelister til dører og porter", "gnagere"),
         "bokser": ("Tette oppbevaringsbokser", "hus-og-hage")}


def _check_body():
    import json
    items = "".join(f'''<div class="grp"><h2>{g}</h2>''' + "".join(f'''<div class="item" data-id="{i}" data-need="{n}"><div><b>{t}</b><span>{d}</span></div>
<div class="seg" role="group" aria-label="{t}"><button type="button" class="ok" aria-pressed="false">Tett / OK</button><button type="button" class="fix" aria-pressed="false">Må fikses</button></div></div>''' for i, t, d, n in its) + "</div>" for g, its in CHECK)
    total = sum(len(i) for _, i in CHECK)
    return STYLE + f'''<section class="band" style="padding-bottom:0"><div class="wrap tool-hero">
<div><span class="kicker">Verktøy · Sjekkliste</span><h1 style="font-size:clamp(40px,5.4vw,72px)">Tett huset før <em>vinteren</em></h1>
<p class="mute" style="font-size:19px;max-width:48ch">Gå runden med lommelykt. Merk hvert punkt som tett eller «må fikses», så lager vi handlelisten for deg. Alle åpninger større enn 6 mm bør stenges.</p></div>
<div class="prog"><span class="small mute">Sjekket</span><div class="big"><span id="done">0</span> / {total}</div><div class="pbar2"><i id="pbar" style="width:0"></i></div><span class="small mute" id="pmsg">Lagres i nettleseren din.</span></div>
</div></section>
<section class="band"><div class="wrap cols2"><div>{items}</div>
<aside class="side2" aria-live="polite"><h3>Handleliste</h3><div id="list"><p class="mute">Merk punkter som «må fikses», så dukker det du trenger opp her.</p></div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn" type="button" id="copy">Kopier listen</button><button class="btn" type="button" id="reset">Nullstill</button></div>
<p class="small mute" style="margin-top:14px">Har du allerede mus? <a href="fellekalkulator.html" style="color:var(--y)">Regn ut hvor mange feller du trenger</a>.</p></aside>
</div></section>
<script>{{
const NEEDS={json.dumps(NEEDS, ensure_ascii=False)},SHOP=(c)=>"https://skadedyrbutikken.no/produkter/"+c+"?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=tett-huset";
let st={{}};try{{st=JSON.parse(localStorage.getItem("sg-tett"))||{{}}}}catch(e){{}}
const items=[...document.querySelectorAll(".item")];
function save(){{try{{localStorage.setItem("sg-tett",JSON.stringify(st))}}catch(e){{}}}}
function render(){{
 items.forEach(it=>{{const v=st[it.dataset.id];it.querySelector(".ok").setAttribute("aria-pressed",v==="ok");it.querySelector(".fix").setAttribute("aria-pressed",v==="fix")}});
 const n=Object.keys(st).length;document.getElementById("done").textContent=n;document.getElementById("pbar").style.width=(100*n/items.length)+"%";
 document.getElementById("pmsg").textContent=n===items.length?"Ferdig! Huset er gått gjennom.":"Lagres i nettleseren din.";
 const fix=items.filter(it=>st[it.dataset.id]==="fix"),needs=[...new Set(fix.map(it=>it.dataset.need).filter(Boolean))];
 const todo=fix.filter(it=>!it.dataset.need).map(it=>it.querySelector("b").textContent);
 document.getElementById("list").innerHTML=!fix.length?'<p class="mute">Merk punkter som «må fikses», så dukker det du trenger opp her.</p>':
  (needs.length?"<ul>"+needs.map(k=>`<li><a href="${{SHOP(NEEDS[k][1])}}" style="color:#fff">${{NEEDS[k][0]}}</a></li>`).join("")+"</ul>":"")+
  (todo.length?'<p class="small mute" style="margin:0 0 6px">Uten innkjøp:</p><ul>'+todo.map(t=>`<li>${{t}}</li>`).join("")+"</ul>":"")+
  (needs.length?`<a class="btn y arrow" href="${{SHOP("gnagere")}}" style="margin-bottom:12px">Handle hos Skadedyrbutikken </a>`:"");
}}
items.forEach(it=>it.querySelector(".seg").addEventListener("click",e=>{{const b=e.target.closest("button");if(!b)return;const v=b.classList.contains("ok")?"ok":"fix";if(st[it.dataset.id]===v)delete st[it.dataset.id];else st[it.dataset.id]=v;save();render()}}));
document.getElementById("reset").onclick=()=>{{st={{}};save();render()}};
document.getElementById("copy").onclick=async()=>{{const t=[...document.querySelectorAll("#list li")].map(l=>"- "+l.textContent).join("\\n")||"Ingenting å kjøpe ennå.";try{{await navigator.clipboard.writeText(t);document.getElementById("copy").textContent="Kopiert"}}catch(e){{document.getElementById("copy").textContent="Kunne ikke kopiere"}}}};
render();
}}</script>'''


def _calc_body():
    rooms = ["Kjøkken", "Under vasken", "Loft", "Kjeller / krypkjeller", "Bod / garasje", "Stue", "Soverom", "Vaskerom"]
    return STYLE + f'''<section class="band" style="padding-bottom:0"><div class="wrap">
<span class="kicker">Verktøy · Kalkulator</span><h1 style="font-size:clamp(40px,5.4vw,72px)">Hvor mange <em>feller</em> trenger du?</h1>
<p class="mute" style="font-size:19px;max-width:56ch">Mus beveger seg ofte bare noen meter fra bolet. Derfor må fellene stå tett, der du faktisk ser spor. Svar på fire spørsmål, så får du et forslag og en plan for plasseringen.</p>
</div></section>
<section class="band"><div class="wrap cols2">
<form class="form" id="f" onsubmit="return false">
 <div class="field"><fieldset><legend>Hva sliter du med?</legend><div class="chips2">
  <label><input type="radio" name="pest" value="mus" checked>Mus</label><label><input type="radio" name="pest" value="rotte">Rotter</label></div></fieldset></div>
 <div class="field"><fieldset><legend>Hvor bor du?</legend><div class="chips2">
  <label><input type="radio" name="type" value="enebolig" checked>Enebolig</label><label><input type="radio" name="type" value="rekkehus">Rekkehus</label><label><input type="radio" name="type" value="leilighet">Leilighet</label><label><input type="radio" name="type" value="hytte">Hytte</label></div></fieldset></div>
 <div class="field"><fieldset><legend>Hvor mange etasjer, medregnet kjeller og loft?</legend><div class="chips2">
  {"".join(f'<label><input type="radio" name="floors" value="{n}"{" checked" if n == 2 else ""}>{n}</label>' for n in range(1, 5))}</div></fieldset></div>
 <div class="field"><fieldset><legend>Hvor har du sett spor (ekskrementer, gnag, lyder)?</legend><div class="chips2">
  {"".join(f'<label><input type="checkbox" name="room" value="{r}"{" checked" if r == "Kjøkken" else ""}>{r}</label>' for r in rooms)}</div></fieldset></div>
 <div class="field"><fieldset><legend>Hvor mye spor?</legend><div class="chips2">
  <label><input type="radio" name="amount" value="1">Litt</label><label><input type="radio" name="amount" value="2" checked>En del</label><label><input type="radio" name="amount" value="3">Mye</label></div></fieldset></div>
</form>
<aside class="side2 result2" aria-live="polite" id="out"></aside>
</div></section>
<section class="band" style="padding-top:0"><div class="wrap" style="max-width:860px">
<h2>Slik setter du fellene</h2>
<ul>
<li>Sett fellene langs veggene der musene ferdes – på gulvet og gjerne oppe ved taket – med utløseren inn mot veggen.</li>
<li>Sett to feller ved siden av hverandre, omtrent 2–3 cm fra hverandre, eller to og to etter hverandre langs veggen.</li>
<li>Jo flere feller, jo bedre. Mus har ofte kort aksjonsradius, så fellene må stå tett.</li>
<li>Bruk åte som lukter godt. Det må konkurrere med all annen mat musene har tilgang på.</li>
<li>Sjekk fellene daglig, og sett feller i alle etasjer – også bod, kaldtloft og krypkjeller.</li>
</ul>
<h2>Vanlige spørsmål om musefeller</h2>
<h3>Hvorfor går ikke musa i fella?</h3>
<p>Som regel står fella feil eller er for få. Mus holder seg ofte innenfor noen få meter fra reiret og går langs veggene, så en felle midt på gulvet blir ofte gått forbi. Flytt fellene inn mot veggen der du ser spor, og sett flere. Rotter er i tillegg forsiktige med nye ting: sett ut fellene uspente med åte i noen dager først, så de venner seg til dem.</p>
<h3>Hva er det beste åtet?</h3>
<p>FHI nevner peanøttsmør, bacon, sjokolade, rosiner, nøtter, frukt og leverpostei. Reirmateriale som bomull eller papir kan også lokke. Vet du ikke hva musene spiser, prøv 3–4 typer og fortsett med den som blir tatt.</p>
<h3>Hvor ofte skal jeg sjekke fellene?</h3>
<p>Så ofte du kan, helst daglig. Får du fangst i flere uker, kommer det fortsatt inn mus et sted. Se <a href="../artikler/mus-i-veggen.html">slik finner du inngangen</a>.</p>
<h3>Er limfeller lov?</h3>
<p>Nei. Limfeller og drukningsfeller er ikke tillatt. Elektriske feller må gi umiddelbart og varig bevissthetstap.</p>
<p class="small mute">Kilder: <a href="https://fhi.no/sk/skadedyrhandboka/gnagere/husmus">FHI: Husmus</a>, <a href="https://fhi.no/sk/skadedyrhandboka/gnagere/brunrotte">FHI: Brunrotte</a>, <a href="https://fhi.no/sk/skadedyrhandboka/gnagere/klatremus">FHI: Klatremus</a>, <a href="https://fhi.no/sk/skadedyrhandboka/gnagere/rodmus">FHI: Rødmus</a>, <a href="https://www.huseierne.no/alt-om-bolig/inneklima-og-miljo/mus-som-skadedyr-forebygge-og-bekjempe/">Huseierne: Mus som skadedyr</a>. Antallet er vår tommelfingerregel ut fra disse rådene, ikke en fast norm.</p>
</div></section>
<script>{{
const f=document.getElementById("f"),out=document.getElementById("out");
const SHOP="https://skadedyrbutikken.no/produkter/gnagere?utm_source=skadedyrguiden&utm_medium=referral&utm_campaign=fellekalkulator";
function calc(){{
 const d=new FormData(f),pest=d.get("pest"),type=d.get("type"),floors=+d.get("floors"),amount=+d.get("amount"),rooms=d.getAll("room");
 const pairsPer=amount,active=rooms.map(r=>[r,pairsPer*2]);
 const monitor=Math.max(0,floors-Math.min(floors,new Set(rooms.map(r=>/Loft/.test(r)?"loft":/Kjeller/.test(r)?"kjeller":"hoved")).size))*2;
 let total=active.reduce((a,[,n])=>a+n,0)+monitor;
 const multi=type==="hytte";
 let html=`<span class="small mute">Forslag</span><div class="num">${{total}}</div><p style="margin:0">${{pest==="rotte"?"rottefeller":multi?"feller – gjerne noen fleremusfeller":"musefeller (klappfeller)"}}</p>`;
 if(pest==="rotte")html+=`<div class="warn"><b>Rotter innendørs?</b><br>Rotter er ofte sky for nye gjenstander, og bekjempelsen er vanskeligere enn for mus. Vi anbefaler å kontakte en skadedyrbekjemper.</div>`;
 html+="<table>"+active.map(([r,n])=>`<tr><td>${{r}}</td><td>${{n}} feller</td></tr>`).join("")+(monitor?`<tr><td>Overvåking i øvrige etasjer</td><td>${{monitor}} feller</td></tr>`:"")+"</table>";
 if(!rooms.length)html+=`<p class="mute small">Ingen spor ennå? Sett et par feller i hver etasje for å følge med, og <a href="tett-huset.html" style="color:var(--y)">tett huset</a>.</p>`;
 if(multi)html+=`<p class="mute small">I en hytte som står tom lenge, passer fleremusfeller som ikke må tømmes etter hver fangst.</p>`;
 html+=`<a class="btn y arrow" href="${{SHOP}}">Se feller hos Skadedyrbutikken </a><p class="small mute" style="margin:12px 0 0">Tetter du ikke inngangene, kommer nye mus inn. <a href="tett-huset.html" style="color:var(--y)">Bruk sjekklisten</a>.</p>`;
 out.innerHTML=html;
}}
f.addEventListener("change",calc);calc();
}}</script>'''


TOOLS = {
 "tett-huset": ("Tett huset før vinteren", "Interaktiv sjekkliste: gå runden og få en handleliste for å stenge mus ute.", _check_body()),
 "fellekalkulator": ("Hvor mange musefeller trenger du? Fellekalkulator", "Regn ut hvor mange musefeller du trenger, hvor de skal stå, hvilket åte som virker og hvorfor musa noen ganger ikke går i fella.", _calc_body()),
}
