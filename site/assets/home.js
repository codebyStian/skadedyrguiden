/* Kryp.as – forsiden: søk, hurtigknapper, tegn-velger og artikkellister. Lastes med defer før app.js. */
window.IMGW={"bedrift":[480,640,800,1200],"borebille":[480,640,800,1195],"by-bergen":[480,640,800,1200,1365],"by-bodo":[480,640,800,1200,1365],"by-kristiansand":[480,640,800,1200,1365],"by-oslo":[480,640,800,1200,1365],"by-stavanger":[480,640,800,1200,1365],"by-tonsberg":[480,640,800,1200,1365],"by-tromso":[480,640,800,1200,1365],"by-trondheim":[480,640,800,1200,1365],"flaggermus":[480,640,800,1195],"fluer":[480,640,800,1200],"foto-flatt":[480,640,830],"foto-jordmaur":[480,640,800,944],"foto-kakerlakk":[480,640,800,889],"foto-kjempetreveps":[480,640,800,1200,1400],"foto-melmoll":[480,640,799],"foto-mus":[480,640,832],"foto-rotte":[480,640,800,1175],"foto-skjeggkre":[480,640,800,1303],"foto-skogmus":[480,640,800,1200,1400],"foto-skogsmaur":[480,640,800,1024],"foto-solvkre":[480,640,800,1200,1400],"foto-stokkmaur":[480,640,832],"foto-svaletege":[480,640,783],"foto-veggedyr":[480,640,739],"foto-veps":[480,640,800,1200,1400],"grevling":[480,640,800,1195],"hero":[480,640,800,1200,1536],"hoggorm":[480,640,800,1195],"humle":[480,640,800,1195],"husbukk":[480,640,800,1195],"hytte":[480,640,800,1200],"klesmoll":[480,640,800,1195],"loftsfluer":[480,640,800,1195],"maker":[480,640,800,1195],"maur":[480,640,800,1200],"melmoll":[480,640,800,1200],"mus":[480,640,800,1200],"region-midt":[480,640,800,1200,1365],"region-nord":[480,640,800,1200,1365],"region-ost":[480,640,800,1200,1365],"region-sor":[480,640,800,1200,1365],"region-vest":[480,640,800,1200,1365],"rotte":[480,640,800,1200],"skjeggkre":[480,640,800,1200],"smagnager":[480,640,800,1195],"snegl":[480,640,800,1195],"studio":[480,640,800,1200,1400],"veggedyr":[480,640,800,1200],"veps":[480,640,800,1200]}; // bredder per bilde i assets/img/r/ – fylles av scripts/perf.py
{
// Kjører fn når elementet nærmer seg skjermen (eller med en gang hvis nettleseren ikke støtter det). Brukes også av app.js.
const near=(el,fn,m='800px')=>{el=typeof el==='string'?document.querySelector(el):el;if(!el||!('IntersectionObserver' in window)){fn();return}const io=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting)){io.disconnect();fn()}},{rootMargin:m});io.observe(el)};
window.SG_near=near;
const U=(p,c)=>'https://skadedyrbutikken.no/produkter/'+p+'?utm_source=kryp.as&utm_medium=referral&utm_campaign='+c;
// Bildene får mindre varianter (assets/img/r/) via srcset. IMGW (bredder per bilde) fylles av scripts/perf.py.
const SZ={side:'(max-width: 600px) 128px, 176px',card:'(max-width: 600px) 92vw, (max-width: 980px) 45vw, 400px'};
const IMG=(n,z)=>{const w=(window.IMGW||{})[n],ss=w?` srcset="${w.map((x,i)=>i<w.length-1?`assets/img/r/${n}-${x}.webp ${x}w`:`assets/img/${n}.webp ${x}w`).join(', ')}" sizes="${SZ[z]||SZ.card}"`:'';return `<img src="assets/img/${n}.webp"${ss} alt="" loading="lazy" decoding="async" onerror="this.parentNode.dataset.ph=1;this.remove()">`};
window.SG_img=IMG;
const P=[
 {k:'mus',n:'Mus',l:'Husmus · Mus musculus',s:'Sep–mar',where:'Loft, kjeller, hytte',size:'7–10 cm + hale',signs:['Små mørke ekskrementer på størrelse med riskorn','Gnagemerker på isolasjon og matpakker','Krafsing i tak og vegger om natten'],first:'Finn og tett åpninger rundt rør, under dører og i takfoten. Sett feller langs veggene der musa går.',cat:'gnagere',art:'artikler/mus-om-hosten.html',tags:'mus gnager loft krafsing ekskrementer'},
 {k:'rotte',n:'Rotte',l:'Brunrotte · Rattus norvegicus',s:'Okt–mar',where:'Kjeller, avløp, uthus',size:'20–27 cm + hale',signs:['Ekskrementer på 1–2 cm','Mørke fettstriper langs vegger','Gnag på rør, ledninger og dører'],first:'Kontakt en skadedyrtekniker. Rotter innendørs er sjelden et gjør-det-selv-prosjekt.',cat:'gnagere',art:'artikler/rotter-i-byen.html',tags:'rotte rotter kjeller avløp'},
 {k:'veggedyr',n:'Veggedyr',l:'Cimex lectularius',s:'Hele året',where:'Seng og soverom',size:'Rundt 5 mm',signs:['Små mørke prikker og blodflekker på lakenet','Kløende bitt, ofte flere på rad','Hudskall langs madrassens sømmer'],first:'Ikke flytt madrasser eller møbler mellom rom. Vask tekstiler varmt og kontakt fagfolk tidlig.',cat:'insekter',art:'artikler/veggedyr-pa-reise.html',tags:'veggedyr bitt seng hotell reise'},
 {k:'maur',n:'Maur',l:'Flere arter',s:'Apr–aug',where:'Kjøkken og terrasse',size:'2–12 mm',signs:['Maurstier langs benk og lister','Små hauger med sagflis kan bety stokkmaur','Bevingede maur innendørs om våren'],first:'Følg stien til inngangen, tett den og fjern søl. Bruk åte slik at maurene tar det med til tuet.',cat:'insekter',art:'artikler/stokkmaur-eller-skogsmaur.html',tags:'maur stokkmaur kjøkken sti'},
 {k:'skjeggkre',n:'Skjeggkre',l:'Ctenolepisma longicaudatum',s:'Hele året',where:'Hele boligen',size:'Opptil 2 cm',signs:['Grå insekter med lange haletråder','Sees ofte om natten når lyset slås på','Finnes også i tørre rom, ikke bare på badet'],first:'Tett sprekker langs lister og bruk åtestasjoner over tid. Det krever tålmodighet, ofte flere måneder.',cat:'insekter',art:'artikler/fukt-solvkre-skjeggkre.html',tags:'skjeggkre sølvkre bad sluk'},
 {k:'veps',n:'Veps',l:'Vespula-arter',s:'Jul–sep',where:'Takskjegg, hekk, bakken',size:'12–18 mm',signs:['Mange veps flyr inn og ut på samme sted','Bol under takskjegg, i hekk eller i bakken','Summing inne i en vegg'],first:'Hold avstand fra bolet. Små bol tidlig i sesongen er lettest å fjerne; bol i vegg bør fagfolk ta.',cat:'insekter',art:'artikler/vepsebol.html',tags:'veps vepsebol stikk tak'},
 {k:'melmoll',n:'Melmøll',l:'Ephestia kuehniella',s:'Hele året',where:'Matskap',size:'Vingespenn ca. 2 cm',signs:['Spinn og larver i mel, gryn og frø','Små møll som flyr i skumringen','Klumper i tørrvarer'],first:'Kast angrepne varer, støvsug og vask skapet, og oppbevar tørrvarer i tette bokser.',cat:'insekter',art:'',tags:'melmøll møll mel matskap larver'},
 {k:'fluer',n:'Fluer',l:'Stueflue · Musca domestica',s:'Jun–aug',where:'Kjøkken og avfall',size:'6–7 mm',signs:['Mange fluer rundt avfall og vinduer','Larver i søppeldunk eller kompost','Fluer som kommer igjen hver sommer'],first:'Hold avfallet tett, tøm ofte og sett insektnett i vinduer som står åpne.',cat:'elektrisk-insektfanger',art:'',tags:'fluer flue sommer søppel'}];
const LX={mus:'husmus',rotte:'brunrotte',veggedyr:'veggedyr',maur:'stokkmaur',skjeggkre:'skjeggkre',veps:'stikkeveps',melmoll:'melmoll'};
// Kort og treff går rett til en egen side (leksikon, ellers artikkel) – ingen skuff fra høyre.
function DEST(k){const p=P.find(x=>x.k===k)||{};return LX[k]?'leksikon/'+LX[k]+'.html':({fluer:'artikler/fluer-om-hosten.html'}[k]||p.art||'leksikon/index.html')}
function open(k){location.href=DEST(k)}

window.SG_open=open;

const q=document.getElementById('q'),hits=document.getElementById('hits');
function find(v){v=v.trim().toLowerCase();if(!v){hits.classList.remove('on');return}
 const r=P.filter(p=>(p.n+' '+p.tags+' '+p.signs.join(' ')).toLowerCase().includes(v));
 hits.innerHTML=r.length?r.map(p=>`<a href="${DEST(p.k)}" data-k="${p.k}"><b>${p.n}</b><span>${p.where}</span></a>`).join(''):'<p>Ingen treff ennå. Prøv «mus», «bitt» eller «veps».</p>';hits.classList.add('on')}
q.addEventListener('input',()=>find(q.value));
document.getElementById('sf').addEventListener('submit',e=>{e.preventDefault();find(q.value);const a=hits.querySelector('a');if(a){hits.classList.remove('on');open(a.dataset.k)}});

document.addEventListener('click',e=>{if(!e.target.closest('.search'))hits.classList.remove('on')});
const chips=document.getElementById('chips');
chips.addEventListener('click',e=>{const b=e.target.closest('button');if(b)open(P.find(p=>p.n===b.textContent).k)});

const S=[['ekskr','Små mørke ekskrementer'],['store','Store ekskrementer'],['gnag','Gnagemerker'],['natt','Lyder om natten'],['bitt','Bitt om morgenen'],['laken','Prikker på lakenet'],['sti','Maurstier'],['mat','Spinn i matvarer'],['gra','Grå insekter om natten'],['summ','Mange veps ute'],['avfall','Fluer ved avfall']];
const W={Mus:{ekskr:3,gnag:2,natt:3},Rotte:{store:4,gnag:3,natt:2},Veggedyr:{bitt:3,laken:4},Maur:{sti:4},Melmøll:{mat:4},Skjeggkre:{gra:4},Veps:{summ:4,natt:1},Fluer:{avfall:4}};
const sEl=document.getElementById('signs'),rEl=document.getElementById('res');
sEl.innerHTML=S.map(([k,t])=>`<label><input type="checkbox" value="${k}">${t}</label>`).join('');
function score(){const on=[...sEl.querySelectorAll('input:checked')].map(i=>i.value);
 if(!on.length){rEl.innerHTML='<span class="kicker">Resultat</span><div class="top1">Velg et tegn</div><p class="mute" style="max-width:36ch">Resultatet oppdateres mens du velger. Jo flere tegn, jo sikrere svar.</p>';return}
 const rows=Object.entries(W).map(([p,w])=>{const m=Object.values(w).reduce((a,b)=>a+b,0);return[p,Math.round(100*on.reduce((a,k)=>a+(w[k]||0),0)/m)]}).filter(r=>r[1]>0).sort((a,b)=>b[1]-a[1]);
 const best=P.find(p=>p.n===rows[0][0]);
 rEl.innerHTML=`<span class="kicker">Mest sannsynlig</span><div class="top1">${best.n}</div>${rows.slice(0,5).map(([p,v])=>`<div class="row"><span>${p}</span><span class="bar"><i style="width:${v}%"></i></span><span class="pct">${v} %</span></div>`).join('')}<div style="margin-top:22px"><button class="btn y arrow" type="button" data-k="${best.k}">Les om ${best.n.toLowerCase()} </button></div><p class="small mute" style="margin:16px 0 0">Prosenten viser hvor mange av kjennetegnene du har valgt. Usikker? Ta bilde og spør en fagperson.</p>`}
sEl.addEventListener('change',score);rEl.addEventListener('click',e=>{const b=e.target.closest('[data-k]');if(b)open(b.dataset.k)});score();

// Artikkellistene bygges fra data/articles.json: aktuelle denne måneden først, så resten med filter per kategori.
near('#artikler',()=>fetch('data/articles.json').then(r=>r.json()).then(all=>{
  const m=new Date().getMonth()+1, lead='mus-om-hosten';
  const list=all.filter(a=>a.slug!==lead).sort((a,b)=>((b.months||[]).includes(m))-((a.months||[]).includes(m)));
  const card=a=>`<a href="artikler/${a.slug}.html"><div class="ph" data-label="${a.cat}">${IMG(a.img,'card')}</div><span class="cat">${a.cat}${(a.months||[]).includes(m)?' · aktuelt nå':''}</span><h3>${a.title}</h3></a>`;
  document.getElementById('side').innerHTML=list.slice(0,4).map(a=>`<a href="artikler/${a.slug}.html"><div><span class="cat">${a.cat}</span><h3>${a.title}</h3></div><div class="ph" data-label="">${IMG(a.img,'side')}</div></a>`).join('');
  document.getElementById('row3').innerHTML=list.slice(4,7).map(card).join('');
  const rest=list.slice(7), cats=['Alle',...new Set(rest.map(a=>a.cat))];
  const draw=c=>{document.getElementById('allArts').innerHTML=rest.filter(a=>c==='Alle'||a.cat===c).map(card).join('');
    document.querySelectorAll('#artChips button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.c===c))};
  document.getElementById('artChips').innerHTML=cats.map(c=>`<button type="button" class="chip" data-c="${c}">${c}</button>`).join('');
  document.getElementById('artChips').onclick=e=>{const b=e.target.closest('button');if(b)draw(b.dataset.c)};
  draw('Alle');
}).catch(()=>{}));

near('#podkast',()=>fetch('data/episodes.json').then(r=>r.ok?r.json():[]).then(E=>{document.getElementById('eps').innerHTML=E.slice(0,3).map(e=>`<a class="ep" href="podkast.html#ep-${e.n}" style="text-decoration:none"><span class="play" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 16 16"><path d="M4.5 2.5l9 5.5-9 5.5z" fill="#f2c230"/></svg></span><span><small>Episode ${e.n}</small><br><b>${e.title}</b></span><span class="len">Lytt nå</span></a>`).join('')}).catch(()=>{}));




document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-tab]').forEach(x=>{x.setAttribute('aria-selected',x===b);document.getElementById(x.dataset.tab).hidden=x!==b})}));
document.getElementById('aiOut').addEventListener('click',e=>{const b=e.target.closest('[data-k]');if(!b)return;const m={jordmaur:'maur',stokkmaur:'maur',skogmus:'mus'};const k=m[b.dataset.k]||b.dataset.k;if(P.find(p=>p.k===k))open(k);else location.hash='leksikon'});
}
