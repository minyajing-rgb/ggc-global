#!/usr/bin/env python3
"""Score a GGC paid-demand experiment from a JSON object."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MODES = {"consumer", "saas", "b2b", "game"}
COUNT_FIELDS = (
    "qualified_reach",
    "qualified_buyers_contacted",
    "cta_clicks",
    "checkout_starts",
    "human_need_replies",
    "qualified_conversations",
    "paid_commitments",
    "budget_backed_lois",
    "repeat_users",
    "repeat_payers",
    "variants_tested",
)


def as_nonnegative_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key, 0)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{key} must be a non-negative integer")
    return value


def decision(status: str, reason: str, next_evidence: str) -> dict[str, str]:
    return {
        "decision": status,
        "reason": reason,
        "next_required_evidence": next_evidence,
    }


def score(data: dict[str, Any]) -> dict[str, Any]:
    mode = data.get("mode")
    if mode not in MODES:
        raise ValueError(f"mode must be one of: {', '.join(sorted(MODES))}")
    if not isinstance(data.get("price_tested"), bool):
        raise ValueError("price_tested must be true or false")
    if "prototype_evidence" in data and not isinstance(data["prototype_evidence"], bool):
        raise ValueError("prototype_evidence must be true or false")

    counts = {key: as_nonnegative_int(data, key) for key in COUNT_FIELDS}
    paid = counts["paid_commitments"]
    backed = counts["budget_backed_lois"]
    strong = paid + backed
    price_tested = data["price_tested"]
    prototype = data.get("prototype_evidence", False)

    if counts["variants_tested"] >= 3 and strong == 0:
        return decision(
            "PARK",
            "Three or more materially different tests produced no commercial commitment.",
            "Redefine the buyer, problem, or offer before reopening the project.",
        )

    if mode in {"consumer", "saas", "game"}:
        if counts["qualified_reach"] >= 1000 and counts["checkout_starts"] == 0:
            return decision(
                "PARK",
                "At least 1,000 qualified visits produced no checkout starts.",
                "Reposition the buyer, promise, price presentation, or offer before more development.",
            )

    if mode == "b2b" and counts["qualified_buyers_contacted"] >= 30 and counts["human_need_replies"] == 0:
        return decision(
            "PARK",
            "Thirty qualified decision-makers produced no genuine need replies.",
            "Redefine the ICP, trigger, problem, or offer before further outreach.",
        )

    if price_tested:
        if mode in {"consumer", "saas"} and paid >= 3:
            return decision(
                "ADVANCE",
                "The priced offer has at least three paid commitments.",
                "Fulfill manually, measure delivery and repeat behavior, then gate the MVP.",
            )
        if mode == "b2b" and strong >= 1 and counts["qualified_conversations"] >= 2:
            return decision(
                "ADVANCE",
                "Qualified B2B conversations produced a paid or budget-backed commitment.",
                "Run the smallest paid pilot and measure delivered value.",
            )
        if mode == "game" and (paid >= 5 or (backed >= 1 and prototype)):
            return decision(
                "ADVANCE",
                "The game has sufficient paid commitments or a backed commitment plus prototype evidence.",
                "Build only the next playable milestone and measure delivery, refunds, and return behavior.",
            )

    missing = []
    if not price_tested:
        missing.append("show a real price")
    if mode in {"consumer", "saas"} and paid < 3:
        missing.append(f"reach 3 paid commitments ({paid}/3)")
    elif mode == "b2b":
        if counts["qualified_conversations"] < 2:
            missing.append(f"reach 2 qualified buying conversations ({counts['qualified_conversations']}/2)")
        if strong < 1:
            missing.append("obtain a paid pilot, deposit, or budget-backed commitment")
    elif mode == "game":
        missing.append("reach 5 paid commitments or pair a backed commitment with prototype evidence")

    return decision(
        "ITERATE",
        "The test has not yet met an advance or park condition.",
        "; ".join(missing) if missing else "Run the next single-variable purchase-intent test.",
    )


def load_input(path: str | None) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", nargs="?", help="JSON file; omit to read stdin")
    args = parser.parse_args()
    try:
        result = score(load_input(args.json_file))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
