# Søkeordsanalyse – Skadedyrguiden (november 2026)

Datagrunnlag: Google-forslag (autocomplete, norsk) for 40 hovedord × a–å, ca. 5 000 søkefraser i `data/keywords.json`.
Autocomplete viser *hva* folk søker etter og rekkefølgen sier noe om popularitet, men gir ikke volum. Volum og klikk får vi fra Google Search Console etter lansering.

## Funn

1. **«Forsikring» dukker opp overalt** – «mus i huset forsikring», «stokkmaur forsikring», «veggedyr forsikring», «borebiller forsikring», «klesmøll forsikring». Ingen av våre sider svarer på det. → Største enkeltgap.
2. **Folk søker på sanser, ikke arter** – «mus på loftet lyd», «husbukk lyd», «grevling lyd», «grevling bæsj», «små svarte insekter i huset», «små hvite insekter i huset». → Identifikasjonssider for lyd, spor og «små insekter».
3. **Sammenligninger er populære** – «skjeggkre vs sølvkre», «stokkmaur vs skogsmaur», «sukkermaur vs stokkmaur», «veggedyr bitt vs mygg», «melmøll vs klesmøll». Leksikonets «Kan forveksles med» treffer dette; bør få egne titler.
4. **Hjelp-intensjon** – «… hva gjør jeg», «bli kvitt …», «hvordan bli kvitt …». Våre artikkeltitler bør bruke de ordene.
5. **Kommersielle søk** – «musefelle» (197 varianter: «musefelle elektrisk», «musefeller utendørs», «musefelle bøtte»), «skjeggkrefelle», «vepsespray». → Kjøpeguider som lenker til skadedyrbutikken.no.
6. **Sesong og «i år»** – «smågnagerår 2026», «er det smågnagerår i år», «maur i huset om våren». Vi har FHI- og GBIF-data og kan svare bedre enn noen andre.
7. **Lokale søk** – «skadedyrkontroll oslo/bergen/trondheim/drammen/tromsø», «rotter i oslo», «hoggorm bergen». → Regionsider/bysider.
8. **Folk skriver «brunsnegle», ikke «brunskogsnegl».** Tittelen bør bruke folkets ord.
9. Støy å ignorere: «rotterdam», «vepsebol godteri/oppskrift», «hoggorm pizza», «lemen» (mest dyret).

## Dekning i dag

| Søkeklynge | Vår side | Status |
|---|---|---|
| mus i huset / bli kvitt mus | artikler/mus-om-hosten | ✅ – legg til «hva gjør jeg» og «farlig» i FAQ |
| mus i hytta | fjellhytta, hytta-ved-sjoen | ✅ |
| rotter / rotte i hagen | rotter-i-byen | ⚠️ mangler «rotte i hagen» og «rotter i veggen/taket» |
| veggedyr, veggedyr bitt | veggedyr-pa-reise, leksikon/veggedyr | ⚠️ mangler bitt, symptomer, «vs mygg» |
| skjeggkre/sølvkre | fukt-solvkre-skjeggkre, leksikon | ✅ |
| stokkmaur, maur i huset | stokkmaur-eller-skogsmaur | ⚠️ «maur i huset» bredere |
| sukkermaur | – | ❌ mangler |
| vepsebol | vepsebol | ✅ |
| grevling | grevling-pa-tomta | ✅ – legg til «lyd», «bæsj», «under huset» |
| flått / flått i hagen | flatt-langs-kysten | ⚠️ mangler hagen |
| hoggorm, flaggermus, husbukk, borebille, måker, klesmøll/pelsbille, brunsnegle | egne artikler | ✅ |
| melmøll, fruktfluer, kakerlakk | kun leksikon / – | ❌ |
| musefelle (kommersielt) | – | ❌ |
| forsikring | – | ❌ |
| smågnagerår 2026 | data på forsiden | ⚠️ trenger egen side |

## Prioritert liste over nye sider

1. **Dekker forsikringen skadedyr?** (mus, maur, veggedyr, borebille, møll) – ett oppslag med tabell per skadedyr.
2. **Smågnagerår 2026 – er det mye mus der du bor?** – levende side med FHI- og GBIF-tall per fylke.
3. **Små insekter i huset: hva er det?** – visuell guide (svarte, hvite, flygende) med bildeanalysen.
4. **Lyder i veggen og på loftet** – mus, rotte, husbukk, grevling, flaggermus.
5. **Veggedyrbitt: slik ser de ut (og forskjellen fra myggstikk)**.
6. **Sukkermaur** og **Fruktfluer** – korte artikler og leksikonsider.
7. **Kjøpeguide: musefeller** (bøtte, elektrisk, utendørs, slagfelle) → skadedyrbutikken.no.
8. **Rotte i hagen – hva gjør jeg?**
9. **Flått i hagen**.
10. Bysider: Oslo, Bergen, Trondheim, Stavanger, Tromsø, Drammen (lokale data + kommunens rotteansvar).

## Teknisk SEO som er på plass

- `<title>` og `meta description` på alle sider, `rel=canonical`, Open Graph og Twitter-kort.
- Strukturerte data: Organization, WebSite, Article, BreadcrumbList, FAQPage (sporsmal-og-svar), PodcastSeries.
- `sitemap.xml`, `robots.txt`, `llms.txt` (for AI-søk), intern lenking artikkel ↔ leksikon ↔ FAQ.
- Forhåndsvisningen har fortsatt `noindex`. Ved lansering: sett repo-variabelen `PREVIEW=0` og `SITE_URL` til det ekte domenet.

## Google Search Console

1. Bestem domene (f.eks. skadedyrguiden.no) og pek det til GitHub Pages (CNAME).
2. Legg til **domeneeiendom** i Search Console og bekreft med TXT-post i DNS (anbefalt), eller URL-prefiks med HTML-fil (vi legger fila i `site/`).
3. Send inn `sitemap.xml`.
4. Etter 4–6 uker: hent søkeord med visninger og klikk, og oppdater denne lista (dette kan automatiseres med Search Console-API og en servicekonto).
