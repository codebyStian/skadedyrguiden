/* Søk i hele Kryp.as + små navigasjonshjelpere. Lastes på alle sider (defer).
   - Søkeknappen i toppmenyen (eller «/» på tastaturet) åpner et søkevindu. Indeksen (assets/search.json, lages av
     scripts/search.py) hentes først når søket åpnes, så sidene ikke blir tyngre.
   - Treff kan lenke rett til riktig avsnitt i en artikkel eller til riktig spørsmål.
   - Menyen markerer siden du er på, og viser på mobil at den kan rulles sideveis.
   - Lenker til et spørsmål (#id på <details>) åpner svaret. */
(() => {
  const ROOT = (document.querySelector(".logo")?.getAttribute("href") || "index.html").replace(/index\.html$/, "");
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  let data = null, dlg, input, list, sel = -1;

  const load = () => data || (data = fetch(ROOT + "assets/search.json").then((r) => r.json()).then((d) => d.map((e) => ({
    ...e, nt: norm(e.t), nh: (e.h || []).map(([t, id]) => [t, id, norm(t)]), nd: norm(e.d || ""),
    nx: norm([e.c || "", ...(e.q || [])].join(" ")),
  }))).catch(() => (data = null, [])));

  // Hvert ord i søket må finnes et sted (som del av et ord, så «felle» finner «musefeller»). Tittel teller mest.
  function score(e, words) {
    let s = 0, head = null;
    for (const w of words) {
      let best = 0;
      if (e.nt.includes(w)) best = e.nt.startsWith(w) || e.nt.includes(" " + w) ? 12 : 9;
      for (const h of e.nh) if (h[2].includes(w) && best < 6) { best = Math.max(best, 6); head = head || h; }
      if (!best && e.nx.includes(w)) best = 4;
      if (!best && e.nd.includes(w)) best = 2;
      if (!best) return [0];
      s += best;
    }
    return [s + (e.k === "Artikkel" ? 1.5 : e.k === "Leksikon" ? 1 : 0), head];
  }

  async function run() {
    const q = norm(input.value.trim()), words = q.split(/\s+/).filter((w) => w.length > 1 || /\d/.test(w));
    if (!words.length) { list.innerHTML = '<p class="s-tip">Skriv for eksempel «mus i veggen», «veps», «bitt» eller «felle».</p>'; sel = -1; return; }
    const all = await load();
    const hits = all.map((e) => [e, ...score(e, words)]).filter((x) => x[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, 12);
    sel = hits.length ? 0 : -1;
    list.innerHTML = hits.length ? hits.map(([e, , h], i) => {
      const url = ROOT + e.u + (h && !e.u.includes("#") ? "#" + h[1] : "");
      const sub = h ? "Avsnitt: " + h[0] : e.d || "";
      return `<a class="s-hit" role="option" id="s-${i}" aria-selected="${i === 0}" href="${esc(url)}"><span class="s-k">${esc(e.k)}${e.c ? " · " + esc(e.c) : ""}</span><b>${esc(e.t)}</b><span class="s-d">${esc(sub.slice(0, 150))}</span></a>`;
    }).join("") : `<p class="s-tip">Ingen treff på «${esc(input.value.trim())}». Prøv et annet ord, se <a href="${ROOT}leksikon/index.html">leksikonet</a> eller <a href="${ROOT}sporsmal-og-svar.html">spørsmål og svar</a>.</p>`;
    input.setAttribute("aria-activedescendant", hits.length ? "s-0" : "");
  }

  function move(d) {
    const a = [...list.querySelectorAll(".s-hit")]; if (!a.length) return;
    sel = (sel + d + a.length) % a.length;
    a.forEach((x, i) => x.setAttribute("aria-selected", i === sel));
    a[sel].scrollIntoView({ block: "nearest" }); input.setAttribute("aria-activedescendant", "s-" + sel);
  }

  function build() {
    dlg = document.createElement("dialog");
    dlg.className = "s-dlg"; dlg.setAttribute("aria-label", "Søk i Kryp.as");
    dlg.innerHTML = `<form method="dialog" class="s-bar" role="search"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><input type="search" placeholder="Søk i artikler, leksikon og spørsmål" aria-label="Søk" autocomplete="off" enterkeyhint="search" role="combobox" aria-expanded="true" aria-controls="s-list" aria-autocomplete="list"><button type="button" class="s-x" aria-label="Lukk søket">Esc</button></form><div class="s-list" id="s-list" role="listbox" aria-label="Treff"></div>`;
    document.body.append(dlg);
    input = dlg.querySelector("input"); list = dlg.querySelector(".s-list");
    let t; input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(run, 60); });
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { e.preventDefault(); const a = list.querySelectorAll(".s-hit")[Math.max(sel, 0)]; if (a) location.href = a.href; }
    });
    dlg.querySelector(".s-x").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });           // klikk utenfor lukker
    list.addEventListener("click", (e) => { if (e.target.closest(".s-hit")) dlg.close(); });  // samme side + #anker
  }

  function open(q) {
    if (!dlg) build();
    load();
    if (typeof q === "string") input.value = q;
    if (!dlg.open) dlg.showModal();
    input.focus(); input.select(); run();
  }
  window.KrypSearch = { open };

  document.addEventListener("click", (e) => { const b = e.target.closest("[data-search]"); if (b) { e.preventDefault(); open(); } });
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !e.ctrlKey && !e.metaKey && !/^(input|textarea|select)$/i.test(e.target.tagName) && !e.target.isContentEditable) { e.preventDefault(); open(); }
  });
  document.querySelectorAll("[data-search]").forEach((b) => b.addEventListener("pointerenter", load, { once: true }));

  // Menyen: marker siden du er på
  const here = location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".nav a").forEach((a) => {
    const u = new URL(a.href, location.href); if (u.hash) return;
    const p = u.pathname.replace(/index\.html$/, "");
    if (p === here || (p.endsWith("/") && p !== "/" && here.startsWith(p))) a.setAttribute("aria-current", "page");
  });
  // Mobilmenyen: skygge mot høyre kant så lenge det finnes mer å rulle til
  const nav = document.querySelector(".nav");
  if (nav) requestAnimationFrame(() => setTimeout(() => {  // etter første opptegning: les ikke layout mens siden bygges
    const edge = () => nav.classList.toggle("nav-fade", nav.scrollWidth - nav.clientWidth - nav.scrollLeft > 8);
    nav.addEventListener("scroll", edge, { passive: true }); addEventListener("resize", edge); edge();
    const cur = nav.querySelector("[aria-current]");  // aktiv lenke inn i synsfeltet uten å rulle selve siden
    if (cur && nav.scrollWidth > nav.clientWidth) { nav.scrollLeft += cur.getBoundingClientRect().right - nav.getBoundingClientRect().right + 24 > 0 ? cur.getBoundingClientRect().left - nav.getBoundingClientRect().left - 16 : 0; edge(); }
  }));
  // Lenke til et spørsmål: åpne svaret
  const openHash = () => { const d = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); if (d && d.tagName === "DETAILS") d.open = true; };
  addEventListener("hashchange", openHash); openHash();
})();
