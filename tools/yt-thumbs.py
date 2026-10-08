#!/usr/bin/env python3
"""Downloads the YouTube thumbnails the site shows into assets/img/yt/<id>.webp,
so pages never load anything from YouTube (Google) before the visitor asks
for a video (privacy page, cookie section; audit of 8 October 2026).
tools/build-seo.py then points every i.ytimg.com URL at the local copy, and
js/voices.js builds its thumbnails from the same folder.

    python3 tools/yt-thumbs.py        # fetch the missing ones

Run it after adding a video. The banned video is never fetched."""
import pathlib, re, subprocess, io, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "yt"
BANNED = {"l-OevQ4q8js"}
ID = re.compile(r'(?:ytimg\.com/vi(?:_webp)?/|youtube(?:-nocookie)?\.com/(?:watch\?v=|embed/)|youtu\.be/|data-id=")([A-Za-z0-9_-]{11})')


def ids():
    found = set()
    files = [p for p in ROOT.rglob("*.html") if not {"node_modules", "shots"} & set(p.parts)]
    files += list((ROOT / "js").glob("*.js")) + list((ROOT / "tools").glob("*.py")) + list((ROOT / "tools").glob("*.json"))
    for p in files:
        if p.name in ("fr.js", "fr-core.js", "yt-thumbs.py"):
            continue
        found |= set(ID.findall(p.read_text(errors="ignore")))
    return found - BANNED


def fetch(url):
    r = subprocess.run(["curl", "-sfL", "--max-time", "20", url], capture_output=True)
    return r.stdout if r.returncode == 0 and len(r.stdout) > 2000 else None


def main():
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    got = 0
    for vid in sorted(ids()):
        dest = OUT / (vid + ".webp")
        if dest.exists():
            continue
        data = fetch("https://i.ytimg.com/vi_webp/%s/hqdefault.webp" % vid) or fetch("https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid)
        if not data:
            print("  no thumbnail for", vid, file=sys.stderr)
            continue
        Image.open(io.BytesIO(data)).convert("RGB").save(dest, "WEBP", quality=80, method=6)
        got += 1
    print("yt thumbnails: %d fetched, %d on disk" % (got, len(list(OUT.glob("*.webp")))))


if __name__ == "__main__":
    main()
