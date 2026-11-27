/* Kryp.as – interaktive deler: lokal hero med årstid/vær, Norgeskart med posisjon,
   offentlige data (FHI, GBIF, MET), sesongkalender og bildeanalyse. Ingen sporing; posisjonen
   brukes bare i nettleseren og lagres lokalt hvis du ber om det. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const fmt = (n) => Number(n).toLocaleString("nb-NO");
  const store = { get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }, del(k) { try { localStorage.removeItem(k); } catch {} } };
  const getJSON = async (u, opt) => { try { const r = await fetch(u, opt); if (!r.ok) throw 0; return await r.json(); } catch { return null; } };
  // Ytelse: data og tunge deler lastes først når de trengs, så førstevisningen bare venter på tekst og hero-bilde.
  const once = (f) => { let p; return () => p || (p = f()); };
  const near = (sel, fn, m) => (window.SG_near ? window.SG_near(sel, fn, m) : fn());
  const afterLoad = (fn) => { const go = () => (window.requestIdleCallback || ((f) => setTimeout(f, 300)))(fn, { timeout: 3000 });
    document.readyState === "complete" ? go() : addEventListener("load", go, { once: true }); };

  // Settes når bildeanalysen er publisert på Cloudflare Workers.
  const AI_URL = document.documentElement.dataset.ai || "";

  const MONTHS = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"];
  const now = new Date(), M = now.getMonth();

  const CITIES = [
    ["oslo", "Oslo", 59.913, 10.752], ["bergen", "Bergen", 60.391, 5.322], ["trondheim", "Trondheim", 63.43, 10.395],
    ["stavanger", "Stavanger", 58.97, 5.733], ["kristiansand", "Kristiansand", 58.146, 7.996], ["tonsberg", "Tønsberg", 59.267, 10.407],
    ["tromso", "Tromsø", 69.649, 18.955], ["bodo", "Bodø", 67.28, 14.405]];

  const REGION = {
    ost: { name: "Østlandet", arts: [
      ["Gnagere", "Rotter i byene rundt Oslofjorden: hva kommunen gjør, og hva som er ditt ansvar"],
      ["Flått", "Flått i hagen langs kysten av Vestfold og Østfold"],
      ["Maur", "Stokkmaur i eldre trehus: slik ser du forskjell på dem og skogsmaur"]] },
    sor: { name: "Sørlandet", arts: [
      ["Flått", "Flått på Sørlandet: sjekk deg selv etter turen i skjærgården"],
      ["Treskadedyr", "Husbukk langs kysten av Telemark og Agder: tegn du ser etter"],
      ["Veps", "Sommerhuset og vepsebolet: fjern det tidlig i sesongen"]] },
    vest: { name: "Vestlandet", arts: [
      ["Gnagere", "Rotter i kystbyene: avløp, avfall og kaiområder"],
      ["Fukt", "Fukt, sølvkre og skjeggkre i vestlandsklimaet"],
      ["Treskadedyr", "Stripet borebille i fuktig kystklima"]] },
    midt: { name: "Trøndelag", arts: [
      ["Gnagere", "Mus på gården: låve, stabbur og fôrlager"],
      ["Maur", "Stokkmaur i hytta: når må du kalle inn hjelp?"],
      ["Veps", "Vepsesesongen i Trøndelag: fra dronning i april til bol i august"]] },
    nord: { name: "Nord-Norge", arts: [
      ["Gnagere", "Smågnagerår: når det er mye mus og lemen i naturen"],
      ["Hytte", "Hytta i nord: sikre mot mus før mørketida"],
      ["Treskadedyr", "Stripet borebille finnes langs kysten helt nord til Troms"]] }};

  // FHIs skadedyrstatistikk: 11 utvalgte skadeinsekter, hele landet, publiseres årlig i etterkant. Mus og rotter er ikke med.
  const SP = [["Skjeggkre", "Skjeggkre"], ["Svart jordmaur", "Svart jordmaur"], ["Veggedyr", "Veggedyr"], ["Stikkeveps", "Stikkeveps"], ["Stokkmaur", "Stokkmaur"]];
  const FHI_NOTE = "FHIs statistikk gjelder 11 utvalgte skadeinsekter og bygger på oppdrag hos skadedyrfirmaer. Mus og rotter er ikke med.";

  let geo = null, stats = null, arts = null, loc = store.get("sg-loc"), wx = null;

  /* ---------- geometri ---------- */
  function P(lon, lat) {
    const p = geo.proj;
    return [((lon - 15) * Math.cos(lat * Math.PI / 180) - p.minx) * p.S + p.PAD, (-lat - p.miny) * p.S + p.PAD];
  }
  function inPoly(x, y, ring) {
    let c = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const [xi, yi] = ring[i], [xj, yj] = ring[j];
      if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c;
    }
    return c;
  }
  function fylkeAt(lat, lon) {
    for (const f of geo.fylker) if (f.poly.some((r) => inPoly(lon, lat, r))) return f;
    let best = null, bd = 1e9;   // nær kysten kan punktet falle utenfor forenklet polygon
    for (const f of geo.fylker) for (const r of f.poly) for (const [x, y] of r) {
      const d = (x - lon) ** 2 + (y - lat) ** 2; if (d < bd) { bd = d; best = f; }
    }
    return bd < 0.25 ? best : null;
  }
  const km = (a, b, c, d) => { const R = 6371, t = Math.PI / 180, x = (d - b) * t * Math.cos(((a + c) / 2) * t), y = (c - a) * t; return Math.sqrt(x * x + y * y) * R; };
  function nearestCity(lat, lon) {
    let best = null;
    for (const c of CITIES) { const d = km(lat, lon, c[2], c[3]); if (d < 35 && (!best || d < best.d)) best = { id: c[0], name: c[1], d }; }
    return best;
  }
  function bboxOf(fs) {
    let a = 1e9, b = 1e9, c = -1e9, d = -1e9;
    for (const f of fs) for (const r of f.poly) for (const [lon, lat] of r) { const [x, y] = P(lon, lat); a = Math.min(a, x); b = Math.min(b, y); c = Math.max(c, x); d = Math.max(d, y); }
    return [a, b, c - a, d - b];
  }

  /* ---------- vær (MET, reserve Open-Meteo) ---------- */
  async function weather(lat, lon) {
    lat = +lat.toFixed(2); lon = +lon.toFixed(2);
    const met = await getJSON(`https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=${lat}&lon=${lon}`);
    if (met?.properties?.timeseries) {
      const ts = met.properties.timeseries, cur = ts[0];
      const nights = ts.slice(0, 72).map((t) => t.data.instant.details.air_temperature);
      return { src: "MET Norge", temp: cur.data.instant.details.air_temperature, min: Math.min(...nights),
        sym: cur.data.next_1_hours?.summary?.symbol_code || cur.data.next_6_hours?.summary?.symbol_code || "" };
    }
    const om = await getJSON(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,weather_code&daily=temperature_2m_min&forecast_days=3&timezone=auto`);
    if (om?.current) {
      const c = om.current.weather_code, sym = c >= 71 && c <= 77 || c >= 85 ? "snow" : c >= 51 ? "rain" : c <= 1 ? "clearsky" : "cloudy";
      return { src: "Open-Meteo", temp: om.current.temperature_2m, min: Math.min(...om.daily.temperature_2m_min), sym };
    }
    return null;
  }
  function mouseRisk(w) {
    if (!w) return null;
    const autumn = M >= 7 && M <= 10, winter = M === 11 || M <= 2;
    if (autumn && w.min < 5) return ["Høy", "Kalde netter fremover. Nå leter musene etter vinterkvarter – tett inngangene nå."];
    if (winter) return ["Middels", "Mus som allerede er inne, holder seg inne. Sjekk loft, kjeller og hytte."];
    if (autumn) return ["Middels", "Nettene er fortsatt milde. Bruk tiden til å tette før kulda kommer."];
    return ["Lav", "Mus finner mat ute nå. Godt tidspunkt å se over huset for hull."];
  }

  /* ---------- hero: lokalt bilde + årstids-/væreffekt ---------- */
  const hero = $(".hero"), heroImg = hero && hero.querySelector("img");
  function setHeroImage(names, label) {
    if (!heroImg) return;
    const list = [].concat(names), source = heroImg.closest("picture")?.querySelector("source:not([type])");
    const phone = source && matchMedia(source.media).matches;
    const tryNext = () => {
      const name = list.shift(); if (!name) return;
      const full = `assets/img/${name}.webp`, crop = `assets/img/r/${name}-m.webp`, test = new Image();
      // Bytt uten å tone ut: det gamle bildet ligger som bakgrunn til det nye er tegnet (ingen mørk blink).
      // Valget huskes, så neste besøk starter med riktig bilde (se skriptet etter hero-bildet i index.html).
      test.onload = () => {
        store.set("sg-hero", name);
        if (heroImg.dataset.n === name) return;
        heroImg.style.background = `url("${heroImg.currentSrc}") center/cover`;
        heroImg.closest("picture")?.querySelectorAll("source[type]").forEach((s) => s.remove()); // AVIF-kildene gjelder bare startbildet
        if (source) source.srcset = phone ? test.src : crop;
        heroImg.removeAttribute("srcset"); heroImg.src = full; heroImg.dataset.n = name;
        heroImg.decode?.().catch(() => {}).finally(() => { heroImg.style.background = ""; });
      };
      test.onerror = () => { if (test.src.endsWith(crop) || test.src.endsWith("-m.webp")) { test.onerror = tryNext; test.src = full; } else tryNext(); };
      test.src = phone ? crop : full;
    };
    tryNext();
    const k = $("#heroKicker"); if (k && label) k.textContent = label;
  }
  function season() {
    if (M === 11 || M <= 1) return "winter"; if (M <= 4) return "spring"; if (M <= 7) return "summer"; return "autumn";
  }
  const FX = { winter: "snow", spring: "rain", summer: "motes", autumn: "leaves" };
  let fxKind = FX[season()];
  function startFX() {
    const cv = $("#fx"); if (!cv || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = cv.getContext("2d"); let W, H, parts = [], vis = true, raf;
    const tint = { snow: "rgba(200,220,235,.04)", rain: "rgba(120,150,170,.04)", motes: "rgba(255,210,120,.03)", leaves: "rgba(210,120,40,.03)" };
    function size() { W = cv.width = cv.clientWidth * devicePixelRatio; H = cv.height = cv.clientHeight * devicePixelRatio; }
    function make() {
      const n = { snow: 55, rain: 45, motes: 22, leaves: 9 }[fxKind]; parts = [];
      for (let i = 0; i < n; i++) parts.push({ x: Math.random() * W, y: Math.random() * H, r: Math.random(), a: Math.random() * 6.28, s: 0.4 + Math.random() });
      cv.style.background = tint[fxKind];
    }
    function step() {
      ctx.clearRect(0, 0, W, H); const d = devicePixelRatio;
      for (const p of parts) {
        if (fxKind === "snow") { p.y += (0.25 + p.s * 0.5) * d; p.x += Math.sin((p.a += 0.008)) * 0.35 * d; ctx.fillStyle = "rgba(255,255,255,.55)"; ctx.beginPath(); ctx.arc(p.x, p.y, (0.8 + p.r * 1.6) * d, 0, 6.28); ctx.fill(); }
        else if (fxKind === "rain") { p.y += (7 + p.s * 4) * d; p.x -= 0.8 * d; ctx.strokeStyle = "rgba(220,235,245,.18)"; ctx.lineWidth = d; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + 2 * d, p.y - 14 * d); ctx.stroke(); }
        else if (fxKind === "motes") { p.y -= 0.15 * p.s * d; p.x += Math.sin((p.a += 0.008)) * 0.3 * d; ctx.fillStyle = `rgba(255,236,170,${0.12 + 0.2 * Math.abs(Math.sin(p.a))})`; ctx.beginPath(); ctx.arc(p.x, p.y, (1 + p.r * 2) * d, 0, 6.28); ctx.fill(); }
        else { p.y += (0.35 + p.s * 0.45) * d; p.x += Math.sin((p.a += 0.012)) * 0.9 * d; ctx.save(); ctx.globalAlpha = 0.55; ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = ["#c9672b", "#d99a2b", "#a4472a", "#e0b041"][p.r * 4 | 0]; ctx.beginPath(); ctx.ellipse(0, 0, 5 * d * (0.6 + p.r), 2.4 * d * (0.6 + p.r), 0, 0, 6.28); ctx.fill(); ctx.restore(); }
        if (p.y > H + 20) { p.y = -20; p.x = Math.random() * W; } if (p.y < -20) p.y = H + 10; if (p.x < -20) p.x = W + 10; if (p.x > W + 20) p.x = -10;
      }
      if (vis) raf = requestAnimationFrame(step);
    }
    size(); make(); step();
    addEventListener("resize", () => { size(); make(); });
    new IntersectionObserver(([e]) => { vis = e.isIntersecting; if (vis) { cancelAnimationFrame(raf); step(); } }).observe(cv);
    startFX.set = (k) => { if (k !== fxKind) { fxKind = k; make(); } };
  }
  function fxFromWeather(w) {
    if (!w || !startFX.set) return;
    const s = w.sym || "";
    startFX.set(/snow|sleet/.test(s) ? "snow" : /rain|drizzle/.test(s) ? "rain" : FX[season()]);
  }

  /* ---------- kart ---------- */
  let svg, vb, cur = null;
  function renderMap() {
    const box = $("#map"); if (!box) return;
    vb = geo.viewBox.slice();
    box.innerHTML = `<svg viewBox="${vb.join(" ")}" role="img" aria-label="Kart over Norge med fylker">
      <g id="fy">${geo.fylker.map((f) => `<path d="${f.d}" data-id="${f.id}" data-r="${f.region}" tabindex="0" role="button" aria-label="${esc(f.name)}"><title>${esc(f.name)}</title></path>`).join("")}</g>
      <g id="me"></g></svg>`;
    svg = box.querySelector("svg");
    svg.addEventListener("click", (e) => { const p = e.target.closest("path"); if (p) select(p.dataset.id, true); });
    svg.addEventListener("keydown", (e) => { const p = e.target.closest("path"); if (p && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); select(p.dataset.id, true); } });
    $("#mapReset")?.addEventListener("click", () => { cur = null; zoomTo(geo.viewBox); paint(); panelNational(); });
  }
  function zoomTo(target) {
    const from = vb.slice(), t0 = performance.now(), dur = matchMedia("(prefers-reduced-motion: reduce)").matches ? 1 : 650;
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    (function f(t) {
      const k = ease(Math.min(1, (t - t0) / dur)); vb = from.map((v, i) => v + (target[i] - v) * k);
      svg.setAttribute("viewBox", vb.join(" ")); if (k < 1) requestAnimationFrame(f);
    })(t0);
  }
  function paint() {
    svg.querySelectorAll("#fy path").forEach((p) => {
      p.classList.toggle("on", cur && p.dataset.id === cur.id);
      p.classList.toggle("reg", cur && p.dataset.r === cur.region && p.dataset.id !== cur.id);
      p.classList.toggle("dim", !!cur && p.dataset.r !== cur.region);
    });
  }
  function select(id, user) {
    cur = geo.fylker.find((f) => f.id === id); if (!cur) return;
    const fs = geo.fylker.filter((f) => f.region === cur.region);
    const [x, y, w, h] = bboxOf(user ? [cur] : fs), pad = Math.max(w, h) * 0.18;
    const W = Math.max(w + pad * 2, (h + pad * 2) * 0.82), H = Math.max(h + pad * 2, W / 0.82);
    zoomTo([x + w / 2 - W / 2, y + h / 2 - H / 2, W, H]);
    paint(); panel(cur);
  }
  function drawMe(lat, lon) {
    const [x, y] = P(lon, lat);
    $("#me", svg).innerHTML = `<circle class="pulse" cx="${x}" cy="${y}" r="10"/><circle class="dot" cx="${x}" cy="${y}" r="5"/>`;
  }

  /* ---------- panel ---------- */
  const inSeason = (a) => a.months.includes(M + 1);
  function pickArts(region, n) {
    if (!arts) return [];
    return arts.filter((a) => !region || a.regions.includes(region))
      .sort((x, y) => inSeason(y) - inSeason(x)).slice(0, n);
  }
  /* ---------- produkttips (valgt av produktagenten, data/recs.json) ---------- */
  let RECS = null;
  const loadRecs = once(() => fetch("data/recs.json").then((r) => r.ok ? r.json() : {}).catch(() => ({}))
    .then((d) => { RECS = d; window.dispatchEvent(new Event("sg-recs")); return d; }));
  const price = (p) => { const n = parseFloat(String(p).replace(",", ".")); return isFinite(n) ? Math.round(n).toLocaleString("nb-NO") + " kr" : ""; };
  function recsHTML(key, camp, n = 3, title = "Riktig utstyr") {
    const list = (RECS && RECS[key] || []).slice(0, n); if (!list.length) return "";
    const u = (x) => x + (x.includes("?") ? "&" : "?") + "utm_source=kryp.as&utm_medium=referral&utm_campaign=" + camp;
    return `<div class="recs cmp"><div class="rch"><h3 class="ph3" style="margin:0">${esc(title)}</h3></div><div class="rcg">${list.map((r) =>
      `<a class="rc" href="${esc(u(r.url))}" rel="sponsored noopener"><div class="rci">${r.image ? `<img src="${esc(r.image)}" alt="" loading="lazy" onerror="this.remove()">` : ""}</div><div class="rcb"><span class="rcr">${esc(r.role || "")}</span><b>${esc(r.name)}</b><span class="rcw">${esc(r.why || "")}</span><span class="rcp">${price(r.price)}<i>Se produktet →</i></span></div></a>`).join("")}</div></div>`;
  }
  window.SG_recs = recsHTML;
  window.addEventListener("sg-recs", () => { try { monthTip(); } catch {} });

  function articles(region) {
    const list = pickArts(region, 4); if (!list.length) return "";
    return `<h3 class="ph3">Aktuelt for ${REGION[region].name}</h3><div class="rarts">${list.map((a) =>
      `<a href="artikler/${a.slug}.html"><span class="cat">${esc(a.cat)}</span><b>${esc(a.title)}</b><span class="soon">${inSeason(a) ? "Nå i " + MONTHS[M] : "Les"}</span></a>`).join("")}</div>`;
  }
  function season2() {
    const box = $("#seasonArts"); if (!box || !arts) return;
    const reg = loc && loc.region, list = pickArts(reg, 6).filter(inSeason);
    const t = $("#seasonTitle"); if (t) t.innerHTML = `Aktuelt i <em>${MONTHS[M]}</em>${reg ? " · " + REGION[reg].name : ""}`;
    box.innerHTML = list.map((a) => `<a href="artikler/${a.slug}.html"><div class="ph" data-label="${esc(a.cat)}">${IMG(a.img)}</div><span class="cat">${esc(a.cat)}</span><h3>${esc(a.title)}</h3></a>`).join("");
  }
  const IMG = (n) => window.SG_img ? window.SG_img(n, "card") : `<img src="assets/img/${n}.webp" alt="" loading="lazy" onerror="this.parentNode.dataset.ph=1;this.remove()">`;

  function monthNow() {
    if (!stats?.fhi?.monthly) return "";
    const pick = { "Veggedyr": "Veggedyr", "Stikkeveps": "Stikkeveps", "Svart jordmaur": "Svart jordmaur", "Stokkmaur": "Stokkmaur", "Skjeggkre": "Skjeggkre" };
    const rows = Object.keys(pick).filter((k) => stats.fhi.monthly[k]).map((k) => [k, stats.fhi.monthly[k][M]]).sort((a, b) => b[1] - a[1]);
    return `<h3 class="ph3">I ${MONTHS[M]} i hele Norge</h3><p class="small mute" style="margin:0 0 10px">Andel av årets bekjempelser som skjer denne måneden. Snitt per måned er 8,3 %. ${FHI_NOTE}</p>
      ${rows.map(([k, v]) => `<div class="mrow"><span>${k}</span><span class="mbar"><i style="width:${Math.min(100, v * 4)}%"></i><em style="left:${8.33 * 4}%"></em></span><b>${String(v).replace(".", ",")} %</b></div>`).join("")}
      <p class="src">Kilde: <a href="https://statistikk.fhi.no/skast/" rel="noopener">FHI Statistikk – Skadedyrstatistikk</a>, snitt ${stats.fhi.years || "siste to år"}.</p>`;
  }
  async function panel(f) {
    const p = $("#panel"); if (!p || !stats) return;
    const here = loc && loc.fylke === f.id;
    const city = here && loc.city ? ` · nær ${loc.city}` : "";
    const yr = stats?.fhi?.yearly || {}, ys = (stats?.fhi?.years || "").split("–");
    const [y1, y2] = ys.length === 2 ? ys : ["2024", "2025"];
    const mx = Math.max(...SP.map(([k]) => Math.max(yr[k]?.[y1] || 0, yr[k]?.[y2] || 0)), 1);
    p.innerHTML = `<span class="kicker">${REGION[f.region].name}${city}</span><h2 style="margin-bottom:.3em">${esc(f.name)}</h2>
      <div class="now" id="now"><span class="mute small">Henter vær …</span></div>
      <h3 class="ph3">Bekjempelser i hele Norge, ${y1} og ${y2}</h3>
      <p class="small mute" style="margin:0 0 10px">Antall oppdrag hos skadedyrfirmaer. FHI har ikke tall per fylke. ${FHI_NOTE}</p>
      ${SP.filter(([k]) => yr[k]).map(([k, n]) => `<div class="mrow"><span>${n}</span><span class="mbar"><i style="width:${Math.round(100 * (yr[k][y2] || 0) / mx)}%"></i></span><b>${fmt(yr[k][y1] || 0)} → ${fmt(yr[k][y2] || 0)}</b></div>`).join("")}
      <p class="src">Kilde: <a href="https://www.fhi.no/sk/skadedyrbekjempelse/statistikk-om-skadedyr/" rel="noopener">FHI – Statistikk om skadedyr</a>. Publiseres årlig, i etterkant.</p>
      ${monthNow()}${articles(f.region)}${recsHTML("reg:" + f.region, "region-" + f.region, 3, "Utstyr folk i " + REGION[f.region].name + " trenger nå")}`;
    const [lat, lon] = here ? [loc.lat, loc.lon] : [f.c[1], f.c[0]];
    const w = await weather(lat, lon); wx = w; if (here) fxFromWeather(w);
    const r = mouseRisk(w), n = $("#now");
    if (n) n.innerHTML = w ? `<div class="wx"><b>${Math.round(w.temp)}°</b><span>${here ? "Der du er nå" : "Midt i fylket nå"}<br><small>Laveste neste 3 døgn: ${Math.round(w.min)}°</small></span></div>
      <div class="risk r-${r[0].toLowerCase()}"><small>Musevarsel</small><b>${r[0]}</b><span>${r[1]}</span></div>
      <p class="src" style="grid-column:1/-1">Vær: ${w.src === "MET Norge" ? '<a href="https://api.met.no/doc/License" rel="noopener">Data fra MET Norge</a> (CC BY 4.0)' : '<a href="https://open-meteo.com/" rel="noopener">Weather data by Open-Meteo.com</a> (CC BY 4.0)'}. Musevarselet er vår tommelfingerregel ut fra temperatur og årstid – ikke en måling.</p>`
      : `<p class="small mute">Været er ikke tilgjengelig akkurat nå.</p>`;
  }
  function panelNational() {
    const p = $("#panel"); if (!p) return;
    p.innerHTML = `<span class="kicker">Hele landet</span><h2>Velg et fylke – eller la oss finne deg</h2>
      <p class="mute">Kartet viser vær og musevarsel der du bor, skadedyrstatistikk fra FHI, og artiklene som er mest relevante i din landsdel.</p>
      <button class="btn y arrow" type="button" data-locate>Bruk posisjonen min </button>
      <p class="small mute" style="margin-top:10px">Posisjonen brukes bare i nettleseren din og sendes ikke til oss.</p>${monthNow()}`;
  }

  /* ---------- posisjon ---------- */
  function applyLoc(l, fromUser) {
    loc = l; const f = fylkeAt(l.lat, l.lon);
    if (!f) { alertMsg("Posisjonen ser ut til å være utenfor Norge. Velg et fylke i kartet."); return; }
    loc.fylke = f.id; loc.region = f.region; const c = nearestCity(l.lat, l.lon); loc.city = c ? c.name : null;
    store.set("sg-loc", { lat: +l.lat.toFixed(2), lon: +l.lon.toFixed(2) });
    setHeroImage(c ? ["by-" + c.id, "region-" + f.region] : ["region-" + f.region], `${c ? c.name : f.name} · ${MONTHS[M]}`);
    $("#locChip") && ($("#locChip").innerHTML = `Viser ${esc(c ? c.name : f.name)} · <button type="button" data-forget>Glem</button>`);
    if (svg) { select(f.id, false); drawMe(l.lat, l.lon); }
    season2();
  }
  function alertMsg(t) { const m = $("#locMsg"); if (m) m.textContent = t; }
  function locate() {
    if (!navigator.geolocation) return alertMsg("Nettleseren din støtter ikke posisjon. Velg et fylke i kartet.");
    alertMsg("Finner posisjonen din …");
    navigator.geolocation.getCurrentPosition((p) => { alertMsg(""); mapReady().then((ok) => ok && applyLoc({ lat: p.coords.latitude, lon: p.coords.longitude }, true)); },
      () => alertMsg("Fikk ikke tilgang til posisjonen. Velg et fylke i kartet i stedet."), { enableHighAccuracy: false, timeout: 10000, maximumAge: 600000 });
  }
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-locate]")) locate();
    if (e.target.closest("[data-forget]")) { store.del("sg-loc"); store.del("sg-hero"); loc = null; location.reload(); }
  });

  /* ---------- sesongkalender fra FHI ---------- */
  function calendar() {
    const g = $("#cal"); if (!g || !stats?.fhi?.monthly) return;
    const rows = [["Veggedyr", "Veggedyr"], ["Stikkeveps", "Veps"], ["Svart jordmaur", "Svart jordmaur"], ["Stokkmaur", "Stokkmaur"], ["Skjeggkre", "Skjeggkre"], ["Tysk kakerlakk", "Kakerlakk"]];
    const mm = ["jan", "feb", "mar", "apr", "mai", "jun", "jul", "aug", "sep", "okt", "nov", "des"];
    g.innerHTML = `<span></span>${mm.map((m, i) => `<span class="h${i === M ? " cur" : ""}">${m}</span>`).join("")}` +
      rows.filter(([k]) => stats.fhi.monthly[k]).map(([k, n]) => {
        const a = stats.fhi.monthly[k], lo = Math.min(...a), hi = Math.max(...a);
        return `<span class="p" title="${n}">${n}</span>` + a.map((v, i) => `<span class="c${i === M ? " cur" : ""}" style="background:color-mix(in srgb,var(--y) ${Math.round(8 + 92 * (v - lo) / (hi - lo || 1))}%,var(--soft))" title="${n}, ${mm[i]}: ${String(v).replace(".", ",")} % av bekjempelsene"></span>`).join("");
      }).join("");
    const lg = $("#calLegend"); if (lg) lg.innerHTML = `Mørkest = måneden med flest bekjempelser for hvert skadedyr. Kilde: <a href="https://statistikk.fhi.no/skast/" rel="noopener">FHI Skadedyrstatistikk</a>, snitt ${stats.fhi.years || "siste to år"}. Statistikken gjelder 11 utvalgte skadeinsekter – mus og rotter er ikke med.`;
  }

  /* ---------- bildeanalyse ---------- */
  function photo() {
    const drop = $("#drop"), file = $("#file"), out = $("#aiOut"); if (!drop) return;
    const pick = () => file.click();
    drop.addEventListener("click", (e) => { if (!e.target.closest("button,select")) pick(); });
    drop.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
    ["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add("over"); }));
    ["dragleave", "drop"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
    let data = null; const btn = $("#analyze");
    drop.addEventListener("drop", (e) => { const f = e.dataTransfer.files[0]; if (f) load(f); });
    file.addEventListener("change", () => file.files[0] && load(file.files[0]));
    btn?.addEventListener("click", () => data && run());
    async function load(f) {
      if (!/^image\//.test(f.type)) { out.innerHTML = `<p>Velg en bildefil (jpg, png eller webp).</p>`; return; }
      try { data = await shrink(f); } catch { out.innerHTML = "<p>Kunne ikke lese bildet.</p>"; return; }
      $("#prev").innerHTML = `<img src="${data}" alt="Bildet du lastet opp">`; drop.classList.add("has");
      $("#dzText").textContent = "Bytt bilde"; if (btn) { btn.disabled = false; btn.focus(); }
      out.innerHTML = `<span class="kicker">Klar</span><div class="top1">Bildet er lastet opp</div><p class="mute" style="max-width:36ch">Velg gjerne hvor du fant dyret, og trykk «Analyser bildet».</p>`;
    }
    async function shrink(f) {
      const img = await createImageBitmap(f); const s = Math.min(1, 1024 / Math.max(img.width, img.height));
      const c = document.createElement("canvas"); c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height); return c.toDataURL("image/jpeg", 0.85);
    }
    async function run() {
      if (!AI_URL) { out.innerHTML = `<div class="aicard"><span class="kicker">Ikke koblet på ennå</span><h3>Bildeanalysen er ikke aktivert i denne forhåndsvisningen</h3><p class="mute">Når den er koblet til, sjekkes bildet mot FHIs kjennetegn i to steg før du får svar. Bruk gjerne «Velg tegn» i mellomtiden.</p></div>`; return; }
      out.innerHTML = `<div class="aicard busy"><span class="spin"></span><b>Analyserer bildet …</b><span class="mute small">Steg 1: beskriver det som synes. Steg 2: sjekker mot FHIs kjennetegn.</span></div>`;
      let r = null; try { const res = await fetch(AI_URL + "/identify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ image: data, hint: $("#hint").value }) }); r = await res.json(); } catch {}
      if (!r || r.error) { out.innerHTML = `<div class="aicard"><h3>Det gikk ikke</h3><p class="mute">${esc(r?.error || "Analysen svarte ikke. Prøv igjen om litt.")}</p></div>`; return; }
      if (r.level === "ukjent") { out.innerHTML = `<div class="aicard"><span class="kicker">Ingen sikker match</span><h3>Vi kjente ikke igjen dyret</h3><p class="mute">${esc(r.visible || "")}</p><p>Prøv et skarpere bilde tatt ovenfra, gjerne med en mynt ved siden av for størrelse.</p></div>`; return; }
      const lvl = { sannsynlig: "Sannsynlig", mulig: "Mulig", usikker: "Usikker" }[r.level];
      out.innerHTML = `<div class="aicard"><span class="kicker">${lvl} · ${r.confidence} % sikkerhet</span><h3>${esc(r.name)} <em>${esc(r.latin)}</em></h3>
        <div class="conf"><i style="width:${r.confidence}%"></i></div>
        <p><b>Det vi ser:</b> ${esc(r.visible)}</p>
        ${r.matched?.length ? `<p><b>Kjennetegn som stemmer (FHI):</b></p><ul>${r.matched.map((m) => `<li>${esc(m)}</li>`).join("")}</ul>` : ""}
        <p class="mute small"><b>Kvalitetskontroll:</b> ${esc(r.check)}</p>
        ${r.twin ? `<div class="twin"><p class="small"><b>Ligner mye på ${esc(r.twin.name.toLowerCase())}</b> – ${esc(r.twin.how)}.</p>
          <div class="tw"><span>${esc(r.name)}</span><div class="conf"><i style="width:${r.confidence}%"></i></div><b>${r.confidence} %</b></div>
          <div class="tw"><span>${esc(r.twin.name)}</span><div class="conf alt"><i style="width:${r.twin.confidence ?? 0}%"></i></div><b>${r.twin.confidence != null ? r.twin.confidence + " %" : "–"}</b></div>
          ${LXS[r.id] ? `<a class="btn arrow" href="leksikon/${LXS[r.id]}.html#forveksling">Se forskjellen side om side </a>` : ""}</div>` : ""}
        ${r.alternatives?.filter((a) => a.id !== r.twin?.id).length ? `<p class="mute small">Andre muligheter: ${r.alternatives.filter((a) => a.id !== r.twin?.id).map((a) => `${esc(a.name)} (${a.confidence} %)`).join(", ")}</p>` : ""}
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px">${r.pest ? `<button class="btn y arrow" type="button" data-k="${esc(r.id)}">Hva gjør jeg nå? </button>` : `<span class="btn" style="pointer-events:none">Ikke et skadedyr</span>`}<a class="btn arrow" href="${esc(r.source.url)}" rel="noopener">${esc(r.source.title)} </a></div>
        <p class="small mute" style="margin:14px 0 0">Dette er en automatisk vurdering, ikke en fagdiagnose. Usikker? Send bildet til FHI på skadedyr@fhi.no eller kontakt en skadedyrtekniker. Bildet lagres ikke.</p></div>`;
    }
  }

  const LXS = { mus: "husmus", skogmus: "skogmus", rotte: "brunrotte", veggedyr: "veggedyr", svaletege: "svaletege", skjeggkre: "skjeggkre", solvkre: "solvkre",
    veps: "stikkeveps", kjempetreveps: "kjempetreveps", stokkmaur: "stokkmaur", skogsmaur: "rod-skogsmaur", jordmaur: "svart-jordmaur", melmoll: "melmoll", kakerlakk: "tysk-kakerlakk", flatt: "skogflatt" };

  /* ---------- månedens tips (hytte/hjem) ---------- */
  function monthTip() {
    const box = $("#monthTip"); if (!box) return;
    const g = "Gjør dette i " + MONTHS[M];
    const T = {
      sjo: [
        [[7, 8, 9], "Før du stenger sjøhytta for <em>vinteren</em>", "En tom hytte ved vannet er perfekt vinterkvarter for mus. Tjue minutter med lommelykt før du låser, sparer deg for gnagde madrasser til våren.",
          [["Tett under dører og rundt rør", "Musebørster, netting og tettemasse for gnagere."], ["Ta med deg all mat", "Også tørrvarer, fuglefrø og dyrefôr."], ["Sett feller langs veggene", "Fleremusfeller kan stå hele vinteren."]]],
        [[10, 11, 0, 1, 2], "Når sjøhytta står tom i <em>vinter</em>", "Hytta er stengt, men musene er ikke det. Tar du en tur innom, er dette det viktigste.",
          [["Sjekk fellene", "Tøm dem og sett dem tilbake langs veggene."], ["Se etter ferske spor", "Ekskrementer og gnag viser hvor de kommer inn."], ["Ikke la mat bli igjen", "Heller ikke tørrvarer, fuglefrø eller dyrefôr."]]],
        [[3, 4], "Når du åpner sjøhytta for <em>sesongen</em>", "Nå ser du hvem som har bodd der i vinter. Og vepsedronningene leter etter bolplass.",
          [["Rydd etter mus med hansker", "Unngå å virvle opp støv."], ["Se etter små vepsebol", "Et bol på størrelse med en valnøtt er lett å fjerne nå."], ["Hold gresset kort", "Flåtten er aktiv fra april."]]],
        [[5, 6], "Sommer ved sjøen: <em>veps og flått</em>", "Vepsebolene vokser, og flåtten trives i kratt og høyt gress langs kysten.",
          [["Sjekk deg for flått", "Etter tur i skog, kratt og skjærgård."], ["Hold avstand til store bol", "Bol i vegger bør fagfolk ta."], ["Måker på taket?", "La dem hekke i fred nå – tiltak gjøres før neste vår."]]]],
      fjell: [
        [[9, 10], "Gjør fjellhytta klar før <em>skisesongen</em>", "Når høsten kommer, leter musene etter ly. I et smågnagerår er det ekstra mange.",
          [["Tett åpninger over 6 mm", "Under kledningen, rundt rør og i ventiler."], ["Ingen mat mellom besøkene", "Heller ikke i bod og uthus."], ["Sett fleremusfeller", "Der du har sett spor før."]]],
        [[11, 0, 1, 2, 3], "Ved hvert besøk i <em>vinter</em>", "Fjellhytta står ofte tom mellom vinterferie og påske. Bruk de første minuttene på dette.",
          [["Sjekk og tøm fellene", "Sett dem tilbake på samme sted."], ["Se etter ferske spor", "Ekskrementer og gnag viser hvor de kommer inn."], ["Rydd med hansker", "Og unngå å virvle opp støv."]]],
        [[4, 5], "Når barmarka kommer på <em>fjellet</em>", "Etter en lang vinter er det tid for å rydde og tette før sommeren.",
          [["Rydd grundig etter musene", "Med hansker, uten å virvle opp støv."], ["Tett der de kom inn", "Følg sporene fra vinteren."], ["Se etter vepsebol", "Under takskjegget og i boden."]]],
        [[6, 7, 8], "Sommer på <em>fjellet</em>", "Høysesong for turer – og for vepsebol i bod og under takskjegg.",
          [["Hold avstand til store bol", "Bol i vegger bør fagfolk ta."], ["Hoggorm i lyng og ur", "Bruk støvler, og se deg for i bærlyngen."], ["Planlegg høstens tetting", "Noter hull og sprekker du ser nå."]]]]};
    const art = { sjo: "hytta-ved-sjoen", fjell: "fjellhytta" };
    let type = store.get("sg-hytte") || "fjell";
    const draw = () => {
      const t = T[type].find((x) => x[0].includes(M));
      box.innerHTML = `<div class="htype" role="group" aria-label="Type hytte"><button type="button" data-h="fjell" aria-pressed="${type === "fjell"}">Fjellhytte</button><button type="button" data-h="sjo" aria-pressed="${type === "sjo"}">Hytte ved sjøen</button></div>
        <span class="kicker">${g}</span><h2>${t[1]}</h2><p class="mute">${t[2]}</p><ul class="checks">${t[3].map(([b, s]) => `<li><b>${b}</b><span>${s}</span></li>`).join("")}</ul><a class="btn arrow" href="artikler/${art[type]}.html">Les hele guiden </a>${recsHTML("hytte:" + type, "hytte-" + type, 3, "Til hytta")}`;
      const img = document.querySelector("#monthTip")?.closest(".feat")?.querySelector(".ph img"), want = type === "sjo" ? "region-sor" : "hytte";
      if (img && img.dataset.n !== want) { img.dataset.n = want; img.closest("picture")?.querySelectorAll("source").forEach((s) => s.remove()); img.removeAttribute("srcset"); img.src = `assets/img/${want}.webp`; }
    };
    box.addEventListener("click", (e) => { const b = e.target.closest("[data-h]"); if (b) { type = b.dataset.h; store.set("sg-hytte", type); draw(); } });
    draw();
  }

  /* ---------- oppstart ---------- */
  const loadArts = once(() => getJSON("data/articles.json").then((d) => (arts = d)));
  const loadStats = once(() => getJSON("data/stats.json").then((d) => (stats = d)));
  const mapReady = once(async () => {
    [geo] = await Promise.all([getJSON("data/norge.json"), loadStats(), loadArts()]); loadRecs();
    if (!geo || !stats) { const p = $("#panel"); if (p) p.innerHTML = `<p class="mute">Kartdata er ikke tilgjengelig her.</p>`; return false; }
    renderMap(); panelNational(); return true;
  });
  function init() {
    photo(); monthTip();
    near("#monthTip", loadRecs);
    near("#aktuelt", () => loadArts().then(season2));
    near("#kalender", () => loadStats().then(calendar));
    if (loc) mapReady().then((ok) => ok && applyLoc(loc, false));   // lagret posisjon: lokal hero med en gang
    else near("#lokalt", mapReady, "600px");
    afterLoad(() => { startFX(); if (wx) fxFromWeather(wx); else if (!loc) weather(59.9, 10.75).then(fxFromWeather); });
  }
  init();
})();

// Lenker utenfra til et anker (f.eks. index.html#hvadet): innhold som lastes inn over ankeret flytter siden,
// så vi justerer på nytt mens siden bygges – til brukeren selv begynner å scrolle.
(() => {
  const id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
  let user = false; ["wheel", "touchstart", "keydown"].forEach((e) => addEventListener(e, () => (user = true), { once: true, passive: true }));
  const go = () => { const el = document.getElementById(id); if (el && !user) el.scrollIntoView({ block: "start" }); };
  [0, 300, 800, 1500, 2500, 4000].forEach((t) => setTimeout(go, t)); addEventListener("load", go);
})();
