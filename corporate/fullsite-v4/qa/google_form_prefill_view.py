#!/usr/bin/env python3
"""Read-only public Google Form prefill inspection; never fills or submits."""
from pathlib import Path
from urllib.parse import urlencode
import json

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[3] / "annual-form-evidence"
OUT.mkdir(exist_ok=True)
base = "https://docs.google.com/forms/d/e/1FAIpQLSeWUmuNsdE8QNOFOMW1XpVBSV4C89UNN0wXaeKpMq7DPzYvoA/viewform"
annual = "S12 — 全球游戏经营Copilot年框 / Annual Global Game Copilot"
advisory = "战略咨询与经营诊断 / Strategy & operations advisory"
url = base + "?" + urlencode({"usp": "pp_url", "entry.2092759400": annual, "entry.627383357": advisory})
report = {"url": url, "visible_service_fields": [], "selected_direction": [], "questions": [], "page_title": "", "body_excerpt": "", "error": None, "business_posts": []}

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
            .filter(field => field.value.startsWith('S12 —') && field.getClientRects().length > 0)
            .map(field => ({tag: field.tagName, value: field.value, aria_label: field.getAttribute('aria-label') || '',
                question: (field.closest('[role=listitem]') || field.parentElement?.parentElement)?.innerText?.slice(0,320) || ''}))""")
        report["selected_direction"] = page.locator('[role=listitem]').filter(has_text='合作方向 / Enquiry type').first.locator('[role=radio]').evaluate_all("""radios => radios
            .filter(radio => radio.getAttribute('aria-checked') === 'true')
            .map(radio => radio.getAttribute('data-value') || radio.getAttribute('data-answer-value') || radio.getAttribute('aria-label') || radio.innerText)""")
        report["questions"] = page.locator("[role=listitem]").evaluate_all("""items => items.map(item => ({
            text: item.innerText.slice(0, 420),
            controls: Array.from(item.querySelectorAll('input,textarea,select')).slice(0, 12).map(field => ({
                tag: field.tagName, name: field.name, type: field.type, value: field.value,
                aria_label: field.getAttribute('aria-label') || ''
            })),
            html_excerpt: item.outerHTML.slice(0, 1300)
        }))""")
        page.screenshot(path=str(OUT / "google-form-s12-prefill.png"), full_page=True)
        browser.close()
except Exception as exc:
    report["error"] = str(exc)
finally:
    report["verified"] = not report["error"] and not report["business_posts"] and any(
        field["value"] == annual and "项目与需求 / Project and message" in field["question"]
        for field in report["visible_service_fields"]
    ) and advisory in report["selected_direction"]
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"status": report.get("status"), "verified": report["verified"],
                      "visible_service_fields": report["visible_service_fields"],
                      "selected_direction": report["selected_direction"],
                      "business_posts": report["business_posts"], "error": report["error"]}, ensure_ascii=False))
    if not report["verified"]:
        raise SystemExit(1)
