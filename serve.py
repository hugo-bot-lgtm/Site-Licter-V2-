#!/usr/bin/env python3
"""Local dev server. Same as `python3 -m http.server`, but tells the browser
never to cache: without this, an edited CSS or JS file keeps being served
from the browser cache and changes look like they did not happen."""
import http.server, socketserver, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), NoCache) as httpd:
    print("Licter — http://localhost:%d  (Ctrl+C pour arrêter)" % PORT)
    httpd.serve_forever()
