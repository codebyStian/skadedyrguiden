"""Lager bilder med Gemini (Imagen) fra scripts/images.json til site/assets/img/<navn>.webp.
Hopper over bilder som finnes. Krever miljøvariabelen GEMINI_API_KEY.
Bruk: python scripts/gen_images.py [navn ...]   (FORCE=1 lager på nytt)"""
import base64, io, json, os, pathlib, sys, time, urllib.request, urllib.error
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site/assets/img"; OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ["GEMINI_API_KEY"]
API = "https://generativelanguage.googleapis.com/v1beta/models/"
IMAGEN = ["imagen-4.0-generate-001", "imagen-4.0-ultra-generate-001", "imagen-3.0-generate-002"]
GEMINI = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview"]

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)

def gen(prompt, ar):
    errs = []
    for m in IMAGEN:
        try:
            d = post(API + m + ":predict", {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": ar, "personGeneration": "allow_adult"}})
            return m, base64.b64decode(d["predictions"][0]["bytesBase64Encoded"])
        except Exception as e:
            errs.append(f"{m}: {e}")
    for m in GEMINI:
        try:
            d = post(API + m + ":generateContent", {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ar}}})
            for p in d["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    return m, base64.b64decode(p["inlineData"]["data"])
            errs.append(f"{m}: no image in response")
        except Exception as e:
            errs.append(f"{m}: {e}")
    raise RuntimeError("; ".join(errs))

def main():
    spec = json.loads((ROOT / "scripts/images.json").read_text())
    style = spec.pop("_style")
    names = sys.argv[1:] or list(spec)
    failed = 0
    for n in names:
        f = OUT / f"{n}.webp"
        if f.exists() and not os.environ.get("FORCE"):
            print("skip", n); continue
        s = spec[n]
        try:
            model, raw = gen(f"{s['prompt']} {style}", s["ar"])
        except Exception as e:
            print("FAIL", n, e); failed += 1; continue
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > s["w"]:
            im = im.resize((s["w"], round(im.height * s["w"] / im.width)), Image.LANCZOS)
        im.save(f, "WEBP", quality=82, method=6)
        print("ok", n, model, im.size, f.stat().st_size // 1024, "KB")
        time.sleep(2)
    sys.exit(1 if failed == len(names) else 0)

main()
