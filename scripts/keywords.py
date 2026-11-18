"""Søkeordsanalyse uten betalte verktøy: henter Google-forslag (autocomplete, norsk) for frøord + a–å-utvidelse.
Forslag sier hva folk faktisk skriver, men ikke volum. Volum kommer fra Search Console når siden er lansert.
Skriver data/keywords.json. Kjøres i GitHub Actions (workflow keywords.yml)."""
import json, pathlib, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEEDS = ["mus i huset", "mus på loftet", "mus i hytta", "musefelle", "bli kvitt mus", "rotter", "rotte i hagen", "bli kvitt rotter",
         "veggedyr", "veggedyr bitt", "skjeggkre", "sølvkre", "maur i huset", "stokkmaur", "sukkermaur", "vepsebol", "veps",
         "grevling", "grevling under huset", "flått", "flått i hagen", "flaggermus på loftet", "hoggorm", "brunsnegl", "brunskogsnegl",
         "måker", "klesmøll", "pelsbille", "melmøll", "fruktfluer", "fluer på loftet", "husbukk", "borebille", "kakerlakk",
         "skadedyr", "skadedyrkontroll", "skadedyrbekjemper", "skadedyr i huset", "insekter i huset", "smågnagerår", "lemen"]
ALPHA = "abcdefghijklmnoprstuvøå"


def suggest(q):
    u = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({"client": "firefox", "hl": "no", "gl": "no", "q": q})
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "replace"))[1]


def main():
    out = {}
    for s in SEEDS:
        found = []
        for q in [s, s + " "] + [f"{s} {c}" for c in ALPHA]:
            try:
                for x in suggest(q):
                    if x not in found: found.append(x)
            except Exception as e:
                print("fail", q, e)
            time.sleep(0.25)
        out[s] = found
        print(s, len(found))
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/keywords.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


main()
