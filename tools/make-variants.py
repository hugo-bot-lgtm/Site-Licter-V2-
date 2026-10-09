#!/usr/bin/env python3
"""Small copies of the photos, screenshots and logos the pages show at a
fraction of their size on a phone (audit of 9 October 2026: 80 to 220 KB of
images to save per page). Run once after adding an image; already made
copies are kept. tools/build-seo.py then lists every copy in the image's
srcset, so the browser downloads the one that fits.

    python3 tools/make-variants.py
"""
import pathlib, re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
# folder, width of the copy, files it is made from
JOBS = [("team", 480, "*.webp"), ("team/morning", 480, "*.webp"), ("shots", 480, "*.webp"),
        ("yt", 240, "*.webp"), ("tools", 96, "*.png"), ("magazine", 260, "*.webp")]
SIZED = re.compile(r"^(.*)-(\d+)$")


def main():
    made = 0
    for folder, width, pattern in JOBS:
        families = {}
        for f in sorted((IMG / folder).glob(pattern)):
            m = SIZED.match(f.stem)
            base = m.group(1) if m else f.stem
            if base.endswith("-face"):          # the round faces already have their own small sizes
                continue
            families.setdefault(base, []).append(f)
        for base, files in families.items():
            out = IMG / folder / ("%s-%d.webp" % (base, width))
            if out.exists():
                continue
            src = max(files, key=lambda f: Image.open(f).width)
            im = Image.open(src)
            if im.width <= width * 1.25:        # not worth a copy
                continue
            im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
            im.resize((width, round(im.height * width / im.width)), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)
            made += 1
            print("made", out.relative_to(ROOT), "%d KB" % (out.stat().st_size // 1024))
    print(made, "copies made")


if __name__ == "__main__":
    main()
