# skadedyrguiden
## Bilder (Cloudflare Workers AI)
Bildene lages av `.github/workflows/images.yml` med Cloudflare Workers AI (FLUX) fra `scripts/images.json`
(krever secrets `CF_ACCOUNT_ID` og `CF_API_TOKEN`). Den kjører når `images.json` endres og lager bare manglende bilder.
Kjør den manuelt fra Actions-fanen; skriv navn (f.eks. `hero mus`) for å lage bilder på nytt.
