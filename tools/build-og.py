#!/usr/bin/env python3
"""Share images for the use-case pages (LinkedIn, X, Slack previews).

    python3 tools/build-og.py

Writes assets/img/og/uc-<hub|family>-<fr|en>.png, 1200 x 630, from
tools/uc_content.py, in the charter: navy ground, amber accent, Aiglon."""
import pathlib, sys, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import uc_content as C  # noqa: E402

W, H = 1200, 630
NAVY, CREAM, AMBER = (19, 22, 45), (252, 246, 239), (234, 169, 61)
DEMI = str(ROOT / "assets/fonts/AiglonProWide-Demi.otf")
OUT = ROOT / "assets/img/og"
OUT.mkdir(parents=True, exist_ok=True)


def card(kicker, title, name):
    im = Image.new("RGB", (W, H), NAVY)
    glow = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(glow)
    d.ellipse((760, -260, 1460, 440), fill=(92, 72, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    im = Image.blend(im, glow, .85)
    d = ImageDraw.Draw(im)
    k = ImageFont.truetype(DEMI, 26)
    d.text((80, 86), kicker.upper(), font=k, fill=AMBER)
    size = 64
    for size in (64, 58, 52, 46):
        f = ImageFont.truetype(DEMI, size)
        lines = textwrap.wrap(title, width=int(1040 / (size * .62)))
        if len(lines) <= 4:
            break
    y = 150
    for line in lines:
        d.text((80, y), line, font=f, fill=CREAM)
        y += int(size * 1.18)
    d.rounded_rectangle((80, y + 18, 176, y + 24), 3, fill=AMBER)
    logo = Image.open(ROOT / "assets/img/logo-white.png").convert("RGBA")
    logo = logo.resize((round(logo.width * 58 / logo.height), 58), Image.LANCZOS)
    im.paste(logo, (80, H - 108), logo)
    small = ImageFont.truetype(DEMI, 20)
    d.text((W - 80, H - 76), "Social Data Intelligence", font=small, fill=(200, 196, 210), anchor="ra")
    im.save(OUT / name, optimize=True)


for lang, code in ((0, "fr"), (1, "en")):
    card(C.HUB["kicker"][lang], C.HUB["h1"][lang], "uc-hub-%s.png" % code)
    for f in C.FAMILIES:
        card("%s · %s" % (C.HUB["kicker"][lang], f["name"][lang]), f["h1"][lang], "uc-%s-%s.png" % (f["key"], code))
for lang, code in ((0, "fr"), (1, "en")):
    card(("Cabinet de conseil en social data intelligence", "Social data intelligence consultancy")[lang],
         "Stop guessing, start listening.", "home-%s.png" % code)
print("share images:", len(list(OUT.glob("uc-*.png"))))
