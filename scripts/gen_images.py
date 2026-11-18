"""Lager bilder med Cloudflare Workers AI fra scripts/images.json til site/assets/img/<navn>.webp.
Hopper over bilder som finnes. Krever CF_ACCOUNT_ID og CF_API_TOKEN (Workers AI-tilgang).
Bruk: python scripts/gen_images.py [navn ...]   (FORCE=1 lager på nytt, MODEL=... velger modell)"""
import base64, io, json, os, pathlib, sys, time, uuid, urllib.request, urllib.error
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site/assets/img"; OUT.mkdir(parents=True, exist_ok=True)
ACCT = (os.environ.get("CF_ACCOUNT_ID") or "").strip()
TOK = (os.environ.get("CF_API_TOKEN") or "").strip()
if not (ACCT and TOK):
    sys.exit("CF_ACCOUNT_ID / CF_API_TOKEN mangler: legg dem inn som repository secrets")
BASE = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/ai/run/"
# Best først. Faller tilbake hvis en modell ikke er tilgjengelig på kontoen.
MODELS = [m for m in (os.environ.get("MODEL") or "").split(",") if m] or [
    "@cf/black-forest-labs/flux-2-dev", "@cf/leonardo/lucid-origin", "@cf/black-forest-labs/flux-1-schnell"]
AR = {"16:9": (16, 9), "4:3": (4, 3), "3:2": (3, 2), "1:1": (1, 1)}


def size_for(ar, long=1536):
    a, b = AR[ar]
    w = long; h = round(long * b / a / 16) * 16
    return w, h


def run_json(model, body):
    req = urllib.request.Request(BASE + model, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOK})
    with urllib.request.urlopen(req, timeout=240) as r:
        ct = r.headers.get("Content-Type", ""); data = r.read()
    if ct.startswith("image/"):
        return data
    j = json.loads(data)
    if not j.get("success", True):
        raise RuntimeError(json.dumps(j.get("errors"))[:300])
    res = j.get("result", j)
    return base64.b64decode(res["image"])


def run_multipart(model, fields):
    bnd = uuid.uuid4().hex; body = b""
    for k, v in fields.items():
        body += f"--{bnd}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += f"--{bnd}--\r\n".encode()
    req = urllib.request.Request(BASE + model, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={bnd}", "Authorization": "Bearer " + TOK})
    with urllib.request.urlopen(req, timeout=300) as r:
        j = json.load(r)
    if not j.get("success", True):
        raise RuntimeError(json.dumps(j.get("errors"))[:300])
    return base64.b64decode(j["result"]["image"])


def gen(prompt, ar):
    w, h = size_for(ar)
    errs = []
    for m in MODELS:
        try:
            if "flux-2" in m:
                return m, run_multipart(m, {"prompt": prompt, "width": w, "height": h, "steps": 28})
            if "lucid-origin" in m or "phoenix" in m:
                return m, run_json(m, {"prompt": prompt, "width": w, "height": h, "num_steps": 40, "guidance": 4.5})
            return m, run_json(m, {"prompt": prompt, "steps": 8})
        except urllib.error.HTTPError as e:
            errs.append(f"{m}: HTTP {e.code} {e.read()[:200].decode(errors='replace')}")
        except Exception as e:
            errs.append(f"{m}: {e}")
    raise RuntimeError(" | ".join(errs))


def fit(im, ar, width):
    a, b = AR[ar]
    tw, th = im.width, round(im.width * b / a)
    if th > im.height:
        th, tw = im.height, round(im.height * a / b)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((l, t, l + tw, t + th))
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return im


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
        im = fit(Image.open(io.BytesIO(raw)).convert("RGB"), s["ar"], s["w"])
        im.save(f, "WEBP", quality=84, method=6)
        print("ok", n, model, im.size, f.stat().st_size // 1024, "KB")
        time.sleep(1)
    sys.exit(0)  # manglende bilder prøves igjen neste natt


main()
