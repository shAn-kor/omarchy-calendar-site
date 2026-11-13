"""Exercise the proposed public homepage -> privacy policy path over HTTP."""
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []
        self.h1_count = 0
        self.lang = None
        self.viewport = False
        self.active_tags = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag in {"script", "iframe", "form", "img"}:
            self.active_tags.append(tag)

    def handle_data(self, data):
        self.text.append(data)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class SiteTest(unittest.TestCase):
    def test_homepage_links_to_accessible_privacy_policy(self):
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
        )
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}/"
        try:
            try:
                with urlopen(base, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn("text/html", response.headers["Content-Type"])
                    home_html = response.read().decode("utf-8")
            except HTTPError as error:
                self.fail(f"Homepage must return HTTP 200, received {error.code}")
            home = Page()
            home.feed(home_html)
            self.assertIn("privacy.html", home.links,
                          "Homepage must link to its actual privacy policy")
            privacy_url = urljoin(base, "privacy.html")
            with urlopen(privacy_url, timeout=5) as response:
                self.assertEqual(response.status, 200)
                privacy_html = response.read().decode("utf-8")
            privacy = Page()
            privacy.feed(privacy_html)
            for name, parsed in (("homepage", home), ("privacy", privacy)):
                with self.subTest(page=name):
                    self.assertEqual(parsed.lang, "ko")
                    self.assertTrue(parsed.viewport)
                    self.assertEqual(parsed.h1_count, 1)
                    self.assertIn("Omarchy Calendar", " ".join(parsed.text))
                    self.assertIn("mailto:kjn0406@gmail.com", parsed.links)
                    self.assertEqual(parsed.active_tags, [],
                                     "Static pages must not collect OAuth or calendar data")
                    for href in parsed.links:
                        if not href or href.startswith(("#", "mailto:")):
                            continue
                        target = urljoin(base, href)
                        if urlsplit(target).netloc == urlsplit(base).netloc:
                            with urlopen(target, timeout=5) as response:
                                self.assertEqual(response.status, 200)
            self.assertIn("index.html", privacy.links)
            self.assertIn("https://www.googleapis.com/auth/calendar.readonly",
                          privacy_html)
            self.assertIn("https://developers.google.com/terms/api-services-user-data-policy",
                          privacy.links)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
