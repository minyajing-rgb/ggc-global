#!/usr/bin/env python3
"""Read-only GEO production-host audit for owned public GGC / SAGA1001 sites.

HTTP 200 alone is insufficient: Base44's SPA fallback may return HTML for
nonexistent /ai-discovery.txt or /sitemap.xml. This script never deploys,
changes DNS, submits URLs, authenticates, scrapes private routes or writes
customer data. Run after each approved release and record results.
"""
from __future__ import annotations
import argparse
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SITES = {
    "ggc-zh": "https://ggcgames.com/zh/index.html",
    "ggc-en": "https://ggcgames.com/en/index.html",
    "bunny": "https://bunny.saga1001.com/",
    "kolmatrix": "https://kol.saga1001.com/website",
    "opsgo": "https://opsgo.ggcgames.com/",
    "oracle": "https://oracle.saga1001.com/",
    "tianji": "https://tianji.saga1001.com/",
    "astro": "https://astro.saga1001.com/",
    "portal": "https://portal.saga1001.com/",
    "memo": "https://memo.saga1001.com/",
    "dreamplot": "https://dreamplot.saga1001.com/",
}


def fetch(url, timeout):
    req = urllib.request.Request(
        url, headers={"User-Agent": "GGC-Public-GEO-Audit/1.0 (+read-only; no user data)", "Accept": "text/html,application/xml,text/plain,*/*"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, response.headers.get("Content-Type", ""), response.url, response.read(350_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), url, exc.read(16_000).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, ssl.SSLError) as exc:
        return None, "", url, str(exc)


def check_site(name, url, timeout):
    origin = urllib.parse.urlsplit(url)
    base = f"{origin.scheme}://{origin.netloc}"
    status, ctype, final_url, homepage = fetch(url, timeout)
    title_match = re.search(r"<title\b[^>]*>([\s\S]*?)</title>", homepage, re.I)
    entry = {
        "site": name,
        "url": url,
        "final_url": final_url,
        "page_status": status,
        "title": re.sub(r"\s+", " ", title_match.group(1)).strip()[:140] if title_match else None,
        "https_host_preserved": urllib.parse.urlsplit(final_url).hostname == origin.hostname and final_url.startswith("https://"),
        "has_title": bool(title_match),
        "has_description": bool(re.search(r'<meta\b[^>]*name=["\']description["\']', homepage, re.I)),
        "has_h1_in_response": bool(re.search(r"<h1\b", homepage, re.I)),
        "resources": {},
    }
    for suffix in ("robots.txt", "sitemap.xml", "ai-discovery.txt", "llms.txt"):
        path = f"{base}/{suffix}"
        state, content_type, _, payload = fetch(path, timeout)
        is_html = bool(re.search(r"<!doctype\s+html|<html\b|<div\s+id=['\"]root['\"]", payload[:4000], re.I))
        if suffix == "robots.txt":
            valid = bool(state == 200 and not is_html and re.search(r"^User-agent\s*:", payload, re.M | re.I))
        elif suffix == "sitemap.xml":
            try:
                parsed = ET.fromstring(payload)
                valid = bool(state == 200 and parsed.tag.endswith("urlset") and not is_html)
            except ET.ParseError:
                valid = False
        else:
            valid = bool(state == 200 and not is_html and len(payload.strip()) >= 60 and not content_type.lower().startswith("text/html"))
        entry["resources"][suffix] = {
            "status": state,
            "content_type": content_type.split(";")[0],
            "html_fallback": is_html,
            "valid": valid,
        }
    entry["ready_for_indexing_review"] = (
        status == 200 and entry["https_host_preserved"] and entry["has_title"]
        and entry["resources"]["robots.txt"]["valid"] and entry["resources"]["sitemap.xml"]["valid"]
    )
    # AI text files are supplemental, not required for SEO or inclusion.
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=9)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--only", choices=list(SITES), nargs="*")
    args = parser.parse_args()
    names = args.only or list(SITES)
    results = [check_site(n, SITES[n], args.timeout) for n in names]
    output = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "public GET/read-only; availability != indexing or conversion",
        "sites_checked": len(results),
        "entry_200": sum(r["page_status"] == 200 for r in results),
        "sitemaps_valid": sum(r["resources"]["sitemap.xml"]["valid"] for r in results),
        "fact_texts_valid": sum(r["resources"]["ai-discovery.txt"]["valid"] for r in results),
        "sites": results,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
