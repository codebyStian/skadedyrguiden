# skadedyrguiden
## Bilder (Cloudflare Workers AI)
Bildene lages av `.github/workflows/images.yml` med Cloudflare Workers AI (FLUX) fra `scripts/images.json`
(krever secrets `CF_ACCOUNT_ID` og `CF_API_TOKEN`). Den kjører når `images.json` endres og lager bare manglende bilder.
Kjør den manuelt fra Actions-fanen; skriv navn (f.eks. `hero mus`) for å lage bilder på nytt.

## Artikler
Brødteksten til artiklene ligger i `content/artikler/<slug>.html`. Hver fil starter med en `<!--meta {json} -->`-blokk med
`title`, `seo_title` (≤ 60 tegn), `desc` (≤ 160 tegn), `lead`, `alt`, `updated`, `faq` og `sources`. Region, måneder, kategori,
bilde og produktboks står i `scripts/articles.py`. `scripts/page.py` bygger sidene (innholdsliste, FAQ), og `scripts/seo.py`
legger på Article-, FAQPage- og BreadcrumbList-data og sitemap.

## Ytelse (PageSpeed)
`scripts/perf.py` kjøres etter `page.py` og `seo.py` (se `pages.yml`) og gjør sidene raske uten å endre utseendet:
fontene hentes fra `site/assets/fonts/` (lages av `scripts/fonts.py`, ikke fra Google Fonts), `site.css` legges inline i `<head>`,
bildene får mindre varianter i `site/assets/img/r/` (Pillow, lages på nytt når originalen endres), og Chrome forhåndslaster
neste side når du holder over en lenke (speculation rules). Bygg lokalt slik:
`python scripts/page.py && PREVIEW=0 python scripts/seo.py && python scripts/perf.py`.
På forsiden lastes kart, statistikk og produkttips først når du scroller mot dem, og årstidseffekten starter etter at siden er lastet.
