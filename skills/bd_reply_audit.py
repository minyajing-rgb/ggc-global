#!/usr/bin/env python3
"""GGC BD reply evidence audit (offline, read-only).

Reads JSON exported by an authorized Gmail connector. Never authenticates to Gmail,
sends email, guesses addresses, or interprets sent-message labels as human replies.
This is a validation layer, NOT a production Gmail polling integration.
"""
import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BUSINESS_SIGNAL = re.compile(r"(预算|价格|报价|费用|合作|负责人|加微信|介绍|对接|项目|发行|产品|计划|聊聊|开会|时间|meeting|budget|pricing|quote|proposal|opportunit|project|we are improving|scalab|publishing|launch|please share|case stud|demo|contract|procurement|kpi)", re.I)
DECLINE = re.compile(r"(后面再聊|暂时不需要|暂无需求|不适合|不考虑|不要再发|停止联系|not a fit|no immediate need|not looking|no longer interested|do not contact)", re.I)
AUTO = re.compile(r"(automated response|auto.?reply|out of office|delivery status notification|mail delivery failure|undeliverable|ticket has been|已收到您的来信|系统自动回复|此为系統自動回覆)", re.I)
FREE_DOMAINS = {"gmail.com", "qq.com", "163.com", "hotmail.com", "outlook.com", "yahoo.com"}


def items(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get("emails", data.get("result", {}).get("emails", data.get("messages", [])))


def email_address(value):
    match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", str(value or ""))
    return match.group(0).lower() if match else ""


def role(message):
    labels = set(message.get("labels") or [])
    if "SENT" in labels:
        return "sent"
    if "INBOX" in labels:
        return "inbox"
    return "unknown"  # No proof of direction: never count it as inbound.


def company_key(message, aliases):
    address = email_address(message.get("from", ""))
    if role(message) == "sent":
        destinations = message.get("to") or []
        if isinstance(destinations, str):
            destinations = [destinations]
        address = next((email_address(x) for x in destinations if email_address(x)), "")
    if address in aliases:
        return aliases[address]
    domain = address.split("@")[-1] if "@" in address else ""
    if domain in aliases:
        return aliases[domain]
    return domain if domain not in FREE_DOMAINS else ""


def parse_date(message):
    value = str(message.get("email_ts") or message.get("date") or "")
    if not value:
        return None
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return date.replace(tzinfo=timezone.utc) if date.tzinfo is None else date.astimezone(timezone.utc)
    except ValueError:
        return None


def audit(inbox, sent, aliases=None):
    aliases = aliases or {}
    labeled_inbox = [x for x in inbox if role(x) == "inbox"]
    labeled_sent = [x for x in sent if role(x) == "sent"]
    sent_by_company, sent_by_thread = {}, {}
    for message in labeled_sent:
        company = company_key(message, aliases)
        if company:
            sent_by_company.setdefault(company, []).append(message)
        if message.get("thread_id"):
            sent_by_thread.setdefault(message["thread_id"], []).append(message)
    rows = []
    for message in labeled_inbox:
        content = (message.get("subject") or "") + "\n" + (message.get("body") or message.get("snippet") or "")[:1600]
        if AUTO.search(content):
            state = "AUTO_OR_SUPPORT"
        elif DECLINE.search(content):
            state = "HOLD_DECLINE"
        elif BUSINESS_SIGNAL.search(content):
            state = "HUMAN_BUSINESS_SIGNAL"
        else:
            state = "REVIEW_HUMAN_UNKNOWN"
        company = company_key(message, aliases)
        related_sent = sent_by_company.get(company, []) if company else []
        latest_in = parse_date(message)
        latest_out = max((parse_date(x) for x in related_sent if parse_date(x)), default=None)
        close_in_time = bool(latest_in and latest_out and abs((latest_out - latest_in).total_seconds()) < 86400)
        if state != "HUMAN_BUSINESS_SIGNAL":
            action = "NO_AUTO_REPLY"
        elif latest_in and latest_out and latest_out >= latest_in:
            action = "ANSWERED_OR_LATER_SENT_REVIEW_CONTENT"
        elif close_in_time:
            action = "SAME_DAY_CROSS_THREAD_MANUAL_REVIEW"
        elif not related_sent:
            action = "P0_MANUAL_REVIEW_NO_COMPANY_SENT_FOUND"
        else:
            action = "P0_MANUAL_REVIEW_NO_LATER_COMPANY_SENT"
        rows.append({
            "id": message.get("id"), "company_key": company, "thread_id": message.get("thread_id"),
            "timestamp": message.get("email_ts"), "state": state, "action": action,
            "related_company_sent": len(related_sent),
            "same_thread_sent": len(sent_by_thread.get(message.get("thread_id"), []))
        })
    return {
        "inbox_count": len(labeled_inbox),
        "sent_count": len(labeled_sent),
        "skipped_unknown_or_wrong_direction": len(inbox) - len(labeled_inbox),
        "counts_by_state": dict(Counter(x["state"] for x in rows)),
        "candidates": rows
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inbox", required=True, help="Connector-exported INBOX JSON")
    parser.add_argument("--sent", required=True, help="Connector-exported SENT JSON")
    parser.add_argument("--aliases", help="Optional private mapping from email/domain to canonical company")
    parser.add_argument("--output", help="Private JSON output path")
    args = parser.parse_args()
    aliases = json.loads(Path(args.aliases).read_text(encoding="utf-8")) if args.aliases else {}
    result = audit(items(args.inbox), items(args.sent), aliases)
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        k: result[k] for k in ("inbox_count", "sent_count", "skipped_unknown_or_wrong_direction", "counts_by_state")
    }, ensure_ascii=False, indent=2))
    print("Manual review required: this classifier does not authorize email sending.")


if __name__ == "__main__":
    main()
