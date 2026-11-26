# skadedyrguiden
## Bilder (Cloudflare Workers AI)
Bildene lages av `.github/workflows/images.yml` med Cloudflare Workers AI (FLUX) fra `scripts/images.json`
(krever secrets `CF_ACCOUNT_ID` og `CF_API_TOKEN`). Den kjører når `images.json` endres og lager bare manglende bilder.
Kjør den manuelt fra Actions-fanen; skriv navn (f.eks. `hero mus`) for å lage bilder på nytt.

### Bildestørrelser
Originalene i `site/assets/img` er 1200–1500 px brede. `scripts/img_variants.py` lager mindre utgaver (`s/`, `p/`, `m/`),
og sidene velger riktig størrelse med `srcset` (se `scripts/img.py`). `images.yml` og `species.yml` kjører skriptet etter
at de har lagt til bilder. Legger du inn et bilde for hånd: kjør `python scripts/img_variants.py` (krever `pillow>=11.3`).

Produktbildene fra Skadedyrbutikken er originalfiler på opptil 1,7 MB. `shop.yml` lager miniatyrer av dem
(`scripts/prod_images.py` → `site/assets/prod`). Kun miniatyrer: kjør `shop.yml` med `crawl=false` og `match=false`.

### Publisering
`pages.yml` bygger sidene på nytt, legger stilarket rett inn i hver side (`INLINE_CSS=1`) og minifiserer skriptene før
publisering. Filene i repoet er den lesbare utgaven.

## Artikler
Brødteksten til artiklene ligger i `content/artikler/<slug>.html`. Hver fil starter med en `<!--meta {json} -->`-blokk med
`title`, `seo_title` (≤ 60 tegn), `desc` (≤ 160 tegn), `lead`, `alt`, `updated`, `faq` og `sources`. Region, måneder, kategori,
bilde og produktboks står i `scripts/articles.py`. `scripts/page.py` bygger sidene (innholdsliste, FAQ), og `scripts/seo.py`
legger på Article-, FAQPage- og BreadcrumbList-data og sitemap.
