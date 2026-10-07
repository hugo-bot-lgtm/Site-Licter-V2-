#!/usr/bin/env python3
"""Tells Bing, Yandex, Seznam and Naver (IndexNow) which pages changed.

Run it only after a deploy is live, never before: the engines fetch the key
file from the site to check the request.

    python3 tools/indexnow.py            # every URL in sitemap.xml
    python3 tools/indexnow.py URL ...    # only these

The key is the name of the .txt file at the root of the site."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = "e10c5e36b39d2fa66036bbc13330fa92"
HOST = "www.licter.com"

urls = sys.argv[1:] or re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": "https://%s/%s.txt" % (HOST, KEY), "urlList": urls[:10000]}).encode()
# sent with curl: the python.org builds of Python ship without system certificates
import subprocess
r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "https://api.indexnow.org/indexnow",
                    "-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@-"], input=body, capture_output=True)
print("IndexNow: %d URLs sent, HTTP %s" % (len(urls), r.stdout.decode()))
