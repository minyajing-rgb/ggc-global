#!/usr/bin/env python3
"""Check the frozen source; prepare exact batches; validate recorded visual reviews.

This does not OCR images or establish the truth of business claims. Image text,
style, portrait and book checks must be performed by a human or visual reviewer.
Preflight/preparation use only the standard library. Review requires Pillow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CHECKS = (
    "title_and_full_text", "numbers_units_and_qualifiers", "style_reference",
    "no_clipping_or_colored_blocks", "original_assets", "privacy",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def sections(text: str) -> dict[str, tuple[str, str]]:
    matches = list(re.finditer(r"^### (\d{2})｜(.+)$", text, re.M))
    result: dict[str, tuple[str, str]] = {}
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():stop].strip()
        if block.endswith("---"):
            block = block[:-3].rstrip()
        page_id = f"S{match.group(1)}"
        require(page_id not in result, f"Duplicate page {page_id}")
        result[page_id] = (match.group(2), block)
    return result


def preflight() -> tuple[dict[str, Any], dict[str, tuple[str, str]]]:
    manifest = read_json(ROOT / "manifest.json")
    raw = (ROOT / manifest["master_file"]).read_bytes()
    require(digest(raw) == manifest["master_sha256"], "MASTER changed: stop; do not silently regenerate hashes")
    blocks = sections(raw.decode("utf-8"))
    expected = [f"S{n:02}" for n in range(1, 30)]
    require(manifest["page_count"] == 29, "Manifest must contain 29 pages")
    require(list(blocks) == expected, "Missing, duplicate or out-of-order master pages")
    require([p["id"] for p in manifest["pages"]] == expected, "Manifest page order differs")
    for page in manifest["pages"]:
        title, block = blocks[page["id"]]
        require(title == page["title"], f"Title differs: {page['id']}")
        require(digest(block.encode("utf-8")) == page["sha256"], f"Text differs: {page['id']}")
    coverage = (ROOT / "OUTLINE_AND_COVERAGE.md").read_text(encoding="utf-8")
    original_ids = re.findall(r"^\| (P\d{2}) \|", coverage, re.M)
    require(original_ids == [f"P{n:02}" for n in range(1, 41)], "40-page source mapping is incomplete")
    print("PASS: master checksum, 29 page checksums/order/titles, 40 source-page mappings")
    return manifest, blocks


def prepare(spec: str, commit: str, manifest: dict[str, Any], blocks: dict[str, tuple[str, str]]) -> None:
    match = re.fullmatch(r"(\d{1,2})-(\d{1,2})", spec)
    require(match is not None, "Use --prepare 01-10, 11-20 or 21-29")
    start, end = map(int, match.groups())
    require(1 <= start <= end <= 29, "Page range outside 01-29")
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "Supply the actual baseline Git commit with --commit")
    selected = [p for p in manifest["pages"] if start <= int(p["id"][1:]) <= end]
    folder = ROOT / "batches" / f"B{start:02}-{end:02}"
    require(not folder.exists(), f"Batch already exists: {folder}; preserve previous review instead of overwriting")
    folder.mkdir(parents=True)
    style = (ROOT / "STYLE_AND_QA.md").read_text(encoding="utf-8")
    input_text = f"# Batch B{start:02}-{end:02}\n\nBaseline: {manifest['baseline_id']}\nCommit: {commit}\n\n{style}\n\n## Exact page inputs\n\n"
    reviews = []
    for page in selected:
        page_id = page["id"]
        exact = blocks[page_id][1]
        (folder / f"{page_id}.md").write_text(exact + "\n", encoding="utf-8")
        input_text += f"Source SHA256: {page['sha256']}\n\n{exact}\n\n---\n\n"
        reviews.append({
            "page_id": page_id, "source_sha256": page["sha256"],
            "image": page["image"], "image_sha256": "", "status": "pending_generation",
            "reviewer": "", "checks": {name: False for name in CHECKS},
            "differences": [], "review_note": "",
        })
    (folder / "input.md").write_text(input_text, encoding="utf-8")
    record = {
        "baseline_id": manifest["baseline_id"], "master_sha256": manifest["master_sha256"],
        "baseline_commit": commit, "batch_pages": [p["id"] for p in selected],
        "reviews": reviews,
    }
    (folder / "qa.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PREPARED {len(selected)} exact page inputs: {folder.relative_to(ROOT)}")
    print("No images generated; all visual checks remain pending/false.")


def review(path: Path, manifest: dict[str, Any]) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("Image integrity review needs Pillow: pip install Pillow") from exc
    record = read_json(path)
    require(record.get("baseline_id") == manifest["baseline_id"], "Review uses a different baseline")
    require(record.get("master_sha256") == manifest["master_sha256"], "Review uses a different master")
    require(re.fullmatch(r"[0-9a-f]{40}", record.get("baseline_commit", "")) is not None, "Missing baseline commit")
    ids = record.get("batch_pages", [])
    require(isinstance(ids, list) and len(ids) > 0 and len(set(ids)) == len(ids), "Invalid batch page list")
    expected = {p["id"]: p for p in manifest["pages"]}
    require(all(pid in expected for pid in ids), "Unknown page in review")
    require(ids == sorted(ids), "Review pages must remain ordered")
    reviews = record.get("reviews", [])
    require([r.get("page_id") for r in reviews] == ids, "Missing, duplicate or out-of-order review rows")
    dimensions = set()
    for item in reviews:
        pid = item["page_id"]
        require(item.get("source_sha256") == expected[pid]["sha256"], f"Different text: {pid}")
        require(item.get("status") == "reviewed", f"Not visually reviewed: {pid}")
        require(bool(item.get("reviewer", "").strip()), f"Missing visual reviewer: {pid}")
        require(all(item.get("checks", {}).get(key) is True for key in CHECKS), f"Incomplete visual checks: {pid}")
        require(item.get("differences") == [], f"Unresolved differences: {pid}")
        require(len(item.get("review_note", "").strip()) >= 10, f"Add specific review observations: {pid}")
        require(item.get("image") == expected[pid]["image"], f"Unexpected image path: {pid}")
        image_path = (ROOT / item["image"]).resolve()
        image_path.relative_to(ROOT)
        raw = image_path.read_bytes()
        require(digest(raw) == item.get("image_sha256"), f"Image changed after review: {pid}")
        with Image.open(image_path) as image:
            require(image.format == "PNG", f"Expected independent PNG: {pid}")
            width, height = image.size
            require(width >= 1600 and height > 0, f"Image resolution too low: {pid}")
            require(abs(width / height - 16 / 9) < 0.002, f"Not 16:9: {pid}")
            dimensions.add(image.size)
            image.verify()
    require(len(dimensions) == 1, "Use the same image dimensions throughout this batch")
    print(f"PASS: {len(ids)} image files, hashes, dimensions and explicit visual-review records")
    print("Record validation only; this is not automated OCR, business verification or user approval.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", metavar="01-10")
    parser.add_argument("--commit", default="", help="Actual 40-character Git baseline commit")
    parser.add_argument("--review", type=Path, help="Path to the completed per-page visual review JSON")
    args = parser.parse_args()
    try:
        manifest, blocks = preflight()
        require(not (args.prepare and args.review), "Choose preparation or review, not both")
        if args.prepare:
            prepare(args.prepare, args.commit, manifest, blocks)
        if args.review:
            review(args.review, manifest)
        return 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
