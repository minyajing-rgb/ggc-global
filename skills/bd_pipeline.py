#!/usr/bin/env python3
# LEGACY ENTRYPOINT - DISABLED 2026-10-10
"""
Retired because the 2026-09-17 implementation:
  * placed investors/third-party service providers in game-client lead pools;
  * scheduled +5 / +10 day automatic chasing after no response;
  * used a partial ledger and could overlook genuine replies and company-level HOLD;
  * did not check new-company approval or confirmed Gmail SENT.
Do not reactivate for higher quotas.

Read skills/ggc-annual-client-development/SKILL.md (v2.5+) and
bd/BD_REPLY_FIRST_10000_EXECUTIVES_SOP_v1.md for the authoritative protocol.

For evidence-based read-only Gmail export auditing:
  python skills/bd_reply_audit.py --inbox /private/inbox.json --sent /private/sent.json

The actual authorized Gmail connector must be used to read/act on emails.
This script does not create tasks, send or label emails.
"""
raise SystemExit("LEGACY BD PIPELINE DISABLED: use v2.5 Skill + Reply First SOP; do not auto-chase old no-reply contacts.")
