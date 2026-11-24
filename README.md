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
