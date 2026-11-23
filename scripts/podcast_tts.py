"""Lager podkastlyd med Gemini TTS (to stemmer) fra podcast/*.txt til site/assets/podcast/<navn>.mp3.
Krever GEMINI_API_KEY og ffmpeg. Hopper over episoder som finnes (FORCE=1 lager på nytt)."""
import base64, json, os, pathlib, subprocess, sys, tempfile, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site/assets/podcast"; OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY mangler: legg den inn som repository secret")
MODELS = ["gemini-3.8-flash-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-flash-preview-tts"]
# Faste stemmer for Kryp.as (egne folk, ikke Trustcom-vertene).
VOICES = {"Marte": "Despina", "Jonas": "Rasalgethi"}
STYLE = ("Les denne samtalen på norsk bokmål med østnorsk uttale, som en rolig og vennlig podkast mellom to "
         "kolleger som liker temaet. Naturlig tempo, små pauser mellom replikkene, aldri overdrevet.")


def tts(lines):
    text = STYLE + "\n\n" + "\n".join(lines)
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"multiSpeakerVoiceConfig": {
                "speakerVoiceConfigs": [{"speaker": s, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}} for s, v in VOICES.items()]}}}}
    errs = []
    for m in MODELS:
        for attempt in range(3):
            try:
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
                with urllib.request.urlopen(req, timeout=300) as r:
                    j = json.load(r)
                part = j["candidates"][0]["content"]["parts"][0]["inlineData"]
                return m, base64.b64decode(part["data"])
            except urllib.error.HTTPError as e:
                msg = e.read()[:200].decode(errors="replace"); errs.append(f"{m}: HTTP {e.code} {msg}")
                if e.code in (404, 400, 403): break
                time.sleep(10 * (attempt + 1))
            except Exception as e:
                errs.append(f"{m}: {e}"); time.sleep(5)
    raise RuntimeError(" | ".join(errs[-4:]))


def main():
    for src in sorted((ROOT / "podcast").glob("*.txt")):
        mp3 = OUT / (src.stem + ".mp3")
        if mp3.exists() and not os.environ.get("FORCE"):
            print("skip", src.stem); continue
        lines = [l.strip() for l in src.read_text().splitlines() if l.strip() and not l.startswith("#")]
        chunks = [lines[i:i + 8] for i in range(0, len(lines), 8)]
        with tempfile.TemporaryDirectory() as d:
            parts = []
            for n, ch in enumerate(chunks):
                model, pcm = tts(ch)
                p = pathlib.Path(d) / f"{n:02}.pcm"; p.write_bytes(pcm); parts.append(p)
                print(src.stem, "part", n, model, len(pcm) // 48000, "s")
            raw = pathlib.Path(d) / "all.pcm"
            gap = b"\x00\x00" * 12000  # 0.5 s pause between chunks
            raw.write_bytes(gap.join(p.read_bytes() for p in parts))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(raw),
                            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-codec:a", "libmp3lame", "-b:a", "96k", str(mp3)], check=True)
        print("ok", mp3.name, mp3.stat().st_size // 1024, "KB")


main()
