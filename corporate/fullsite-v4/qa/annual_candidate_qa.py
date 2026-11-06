#!/usr/bin/env python3
"""Read-only S12 candidate journey. Runs against a local generated site."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit
import json
import subprocess
import sys

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1]
OUT = BASE.parents[1] / "annual-candidate-evidence"
SITE = OUT / "site"
OUT.mkdir(exist_ok=True)
subprocess.run([
    sys.executable, str(BASE / "build_ready.py"), "--out", str(SITE),
    "--mode", "release", "--base-url", "https://ggcgames.com/", "--google-form",
], check=True)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Handler, directory=str(SITE)))
Thread(target=server.serve_forever, daemon=True).start()
origin = f"http://127.0.0.1:{server.server_port}"
report = {"origin": "local generated candidate", "checks": [], "posts": [], "page_errors": []}


def check(name, condition, detail=""):
    report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(f"{name}: {detail}")


try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        for locale in ("zh", "en"):
            for width in (390, 1440):
                mobile = width == 390
                context = browser.new_context(
                    viewport={"width": width, "height": 844 if mobile else 900},
                    has_touch=mobile, is_mobile=mobile, reduced_motion="reduce",
                )
                context.route("https://fonts.googleapis.com/**", lambda route: route.fulfill(status=200, content_type="text/css", body=""))
                context.on("request", lambda request: report["posts"].append(request.url) if request.method == "POST" else None)
                page = context.new_page()
                page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
                tag = f"{locale}-{width}"
                page.goto(f"{origin}/{locale}/index.html", wait_until="domcontentloaded")
                cta = page.locator('main a[href="service-s12.html"]')
                check(f"hero_s12_{tag}", cta.count() == 1)
                check(f"layout_home_{tag}", page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
                page.screenshot(path=str(OUT / f"{tag}-home.png"), full_page=True)
                if mobile:
                    cta.tap()
                else:
                    cta.focus()
                    page.keyboard.press("Enter")
                page.wait_for_url(f"**/{locale}/service-s12.html")
                check(f"s12_navigation_{tag}", urlsplit(page.url).path == f"/{locale}/service-s12.html", page.url)
                detail_link = page.locator('main a[href="contact.html?service=S12"]')
                check(f"s12_contact_link_{tag}", detail_link.count() == 1)
                check(f"layout_s12_{tag}", page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
                page.screenshot(path=str(OUT / f"{tag}-service.png"), full_page=True)
                detail_link.click()
                page.wait_for_url(f"**/{locale}/contact.html?service=S12")
                check(f"contact_query_{tag}", parse_qs(urlsplit(page.url).query).get("service") == ["S12"])
                form_link = page.locator('.google-inquiry a[href*="docs.google.com/forms/"]')
                form_link.wait_for()
                form_query = parse_qs(urlsplit(form_link.get_attribute("href")).query)
                check(f"form_service_prefill_{tag}", form_query.get("entry.2092759400") == ["S12"], str(form_query))
                check(f"form_prefill_mode_{tag}", form_query.get("usp") == ["pp_url"])
                check(f"service_note_{tag}", "S12" in page.locator(".google-inquiry").inner_text())
                check(f"layout_contact_{tag}", page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
                page.screenshot(path=str(OUT / f"{tag}-contact.png"), full_page=True)
                page.reload(wait_until="domcontentloaded")
                check(f"refresh_prefill_{tag}", "entry.2092759400=S12" in page.locator('.google-inquiry a[href*="docs.google.com/forms/"]').get_attribute("href"))
                page.locator("[data-locale]").click()
                other_locale = "en" if locale == "zh" else "zh"
                page.wait_for_url(f"**/{other_locale}/contact.html?service=S12")
                check(f"locale_query_{tag}", parse_qs(urlsplit(page.url).query).get("service") == ["S12"])
                context.close()
        browser.close()
    check("no_business_posts", not report["posts"], str(report["posts"]))
    check("no_page_errors", not report["page_errors"], str(report["page_errors"]))
finally:
    server.shutdown()
    report["passed"] = all(item["passed"] for item in report["checks"])
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"checks": len(report["checks"]), "passed": report["passed"], "posts": len(report["posts"]), "page_errors": len(report["page_errors"])}))
