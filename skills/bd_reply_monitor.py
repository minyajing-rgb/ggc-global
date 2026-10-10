#!/usr/bin/env python3
# LEGACY ENTRYPOINT - DISABLED 2026-10-10
"""
Retired because this monitor checked only eight hard-coded company domains and
incorrectly inferred 'all delivered' merely when no bounce message was found.
It could not distinguish human replies, customer support, sent messages and
company-level cross-thread responses.

Use authorized Gmail connector for current inbox / sent data and
skills/bd_reply_audit.py for read-only export auditing.
NO DELIVERABILITY CLAIM can be inferred from absence of a bounce.
"""
raise SystemExit("LEGACY MONITOR DISABLED: never infer delivery from missing bounce; use INBOX/SENT evidence audit.")
