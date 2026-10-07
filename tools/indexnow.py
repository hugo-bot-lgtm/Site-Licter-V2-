#!/usr/bin/env python3
"""Tells Bing, Yandex, Seznam and Naver (IndexNow) which pages changed.

Run it only after a deploy is live, never before: the engines fetch the key
file from the site to check the request.

    python3 tools/indexnow.py            # every URL in sitemap.xml
    python3 tools/indexnow.py URL ...    # only these

The key is the name of the .txt file at the root of the site."""
import json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = "e10c5e36b39d2fa66036bbc13330fa92"
HOST = "www.licter.com"

urls = sys.argv[1:] or re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": "https://%s/%s.txt" % (HOST, KEY), "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow: %d URLs sent, HTTP %d" % (len(urls), r.status))
