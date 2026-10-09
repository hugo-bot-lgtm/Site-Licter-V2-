#!/usr/bin/env python3
"""Builds js/min/<name>.js, a compact copy of every script in js/ (terser),
and points the pages at it (SEO audit of 8 October 2026: unminified
JavaScript cost 90 to 260 ms on mobile). js/*.js stay the files you edit.

Run by tools/build-css.py at its end, so after every build; on its own:

    python3 tools/build-js.py

A script that terser cannot compact is copied as is. The scripts find their
siblings next to themselves (js/ui.js loads track.js, popups.js, assistant.js,
events.js; js/i18n.js loads fr.js), so every file goes to the same folder."""
import pathlib, re, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "js", ROOT / "js" / "min"


def main():
    OUT.mkdir(exist_ok=True)
    before = after = 0
    names = []
    for f in sorted(SRC.glob("*.js")):
        dest = OUT / f.name
        names.append(f.stem)
        if dest.exists() and dest.stat().st_mtime >= f.stat().st_mtime:
            before += f.stat().st_size; after += dest.stat().st_size
            continue
        r = subprocess.run(["npx", "-y", "terser@5", str(f), "-c", "-m", "--comments", "false", "-o", str(dest)],
                           capture_output=True, text=True)
        if r.returncode != 0 or not dest.exists() or dest.stat().st_size == 0:
            print("  terser failed on %s, copied as is" % f.name)
            shutil.copyfile(f, dest)
        before += f.stat().st_size; after += dest.stat().st_size
    for stale in OUT.glob("*.js"):
        if stale.stem not in names:
            stale.unlink()
    # the pages load the compact copies
    link = re.compile(r'((?:src|href)="(?:/|\.\./)*)js/(%s)\.js(\?v=\d+)?"' % "|".join(map(re.escape, names)))
    n = 0
    for p in ROOT.rglob("*.html"):
        if {"node_modules", "tools", "shots"} & set(p.parts):
            continue
        s = p.read_text()
        s2 = link.sub(lambda m: '%sjs/min/%s.js%s"' % (m.group(1), m.group(2), m.group(3) or ""), s)
        if s2 != s:
            p.write_text(s2)
            n += 1
    # js/theme.js is tiny and must run before the first paint: written into each
    # page instead of fetched (one render-blocking request less on mobile)
    theme = (OUT / "theme.js").read_text().strip()
    tag = re.compile(r'<script src="(?:/|\.\./)*js/(?:min/)?theme\.js(?:\?v=\d+)?"></script>|<script data-inline="theme">.*?</script>', re.S)
    inline = '<script data-inline="theme">%s</script>' % theme
    for p in ROOT.rglob("*.html"):
        if {"node_modules", "tools", "shots"} & set(p.parts):
            continue
        s = p.read_text()
        s2 = tag.sub(lambda m: inline, s, count=1)
        if s2 != s:
            p.write_text(s2)
    print("js/min: %d KB -> %d KB, %d pages pointed at it" % (before // 1024, after // 1024, n))


if __name__ == "__main__":
    main()
