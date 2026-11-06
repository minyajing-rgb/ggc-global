#!/usr/bin/env python3
"""Read-only public Google Form prefill inspection; never fills or submits."""
from pathlib import Path
from urllib.parse import urlencode
import json

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[3] / "annual-form-evidence"
OUT.mkdir(exist_ok=True)
base = "https://docs.google.com/forms/d/e/1FAIpQLSeWUmuNsdE8QNOFOMW1XpVBSV4C89UNN0wXaeKpMq7DPzYvoA/viewform"
url = base + "?" + urlencode({"usp": "pp_url", "entry.2092759400": "S12"})
report = {"url": url, "visible_service_fields": [], "page_title": "", "body_excerpt": "", "error": None, "business_posts": []}

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.route("**/formResponse*", lambda route: route.abort())
        page.on("request", lambda request: report["business_posts"].append(request.url) if request.method == "POST" and "formResponse" in request.url else None)
        response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1200)
        report["status"] = response.status if response else None
        report["page_title"] = page.title()
        report["body_excerpt"] = page.locator("body").inner_text()[:2200]
        report["visible_service_fields"] = page.locator("input,textarea,select").evaluate_all("""fields => fields
            .filter(field => field.value === 'S12' && field.getClientRects().length > 0)
            .map(field => ({tag: field.tagName, aria_label: field.getAttribute('aria-label') || '',
                question: (field.closest('[role=listitem]') || field.parentElement?.parentElement)?.innerText?.slice(0,320) || ''}))""")
        page.screenshot(path=str(OUT / "google-form-s12-prefill.png"), full_page=True)
        browser.close()
except Exception as exc:
    report["error"] = str(exc)
finally:
    report["verified"] = not report["error"] and not report["business_posts"] and any(
        "service" in (field["aria_label"] + " " + field["question"]).lower()
        or "服务" in (field["aria_label"] + " " + field["question"])
        for field in report["visible_service_fields"]
    )
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"status": report.get("status"), "verified": report["verified"],
                      "visible_service_fields": report["visible_service_fields"],
                      "business_posts": report["business_posts"], "error": report["error"]}, ensure_ascii=False))
    if not report["verified"]:
        raise SystemExit(1)
