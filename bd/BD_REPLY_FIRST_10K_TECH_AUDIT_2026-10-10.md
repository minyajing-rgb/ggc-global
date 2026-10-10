# GGC BD Reply-First / 10k Executive Sourcing — Technical Audit (2026-10-10)

## What was actually checked

- Gmail labels, individual inbound and outbound messages and company-specific cross-thread examples.
- The connected Base44 GGC DealGraph Company, Person, Candidate and SearchTask entities, using pagination rather than a small first page.
- The existing public BD Skill and legacy Python entrypoints.
- Source-led enrichment using public company profiles and 2026 game-developer industry rankings.

## Faults found

### Fault 1 — Wrong-direction Gmail labels

Actual messages under older labels:
- `GGC/BD/Reply - Opportunity`: 21 messages, **all SENT**, no INBOX.
- `GGC/BD/Status - Human Reply`: 42 messages, **all SENT**, no INBOX.
- `GGC/BD/Reply - Not Fit Now`: 17 messages, **all SENT**, no INBOX.

Do not infer human customer replies from these labels. Rebuild classification from real Gmail message labels/direction, sender, content and whole related-company history. Some targeted replies were sent under a new subject/thread; do not count those as unhandled without company-level review.

### Fault 2 — Unsafe legacy entrypoints

- `skills/bd_pipeline.py` embedded +5/+10 day automatic follow-up and mixed investors/vendors with principal-side clients.
- `skills/bd_reply_monitor.py` only examined eight hardcoded domains and claimed delivery merely because it observed no bounce.

Both legacy executable entrypoints are now **disabled**. Git history preserves the earlier source for investigation; do not reenable them to increase quota.

### Fault 3 — Static/failing source ingestion

At initial audit the Base44 DealGraph had:
- 1,043 Company records (not necessarily canonicalized, some vendor/investor records).
- 345 Person records across 230 company IDs.
- 238 Person records with `Not Contacted`, 87 marked `Drafted`.
- 198 Person records carrying public_email (not a verification of deliverability).
- 77 SearchTask records: 1 Failed, 13 still Running.
- The Sep 1 SearchTask with a target of 3,000 returned **found 0, verified 0, contacts 0, status Failed**.
- HarvestConfig.auto_enabled = false; its status says prior on-app harvesting is unavailable. Merely changing a toggle does not repair the source engine.

## Actions completed this turn

- Created distinct Gmail labels for true buyer action, waiting for reply, and economic/contract readiness. Actual INBOX messages, not SENT, must receive them.
- Activated every-two-hours read-only-first buyer reply condition watch.
- Updated existing twice-daily BD and daily report tasks with genuine buyer-first priority, 10k separately counted and confirmed new-contact approval requirements.
- Activated independent daily executive sourcing (company census + executive graph + approval-ready drafts; cannot treat static research as actual contacts).
- Created `skills/bd_reply_audit.py` read-only Gmail export diagnostic and `skills/test_bd_reply_audit.py`.
- Unit tests verified 4 cases: SENT never counts as inbound; cross-thread same company is recognized; explicit no-need becomes HOLD; ambiguous same-day timeline triggers manual review.
- Archived/disabled two unsafe old Python entrypoints.

### First tangible source enrichment batch

The initial source-led batch created **9 Base44 Candidate records**:
- 2 verified and linked to newly created Company records,
- 3 mapped to already existing Company records and marked Duplicate,
- 4 remain Pending identity/product evidence.

Additionally **2 new Company records** and **6 public-source executive Person records** were created; all new people remain `Not Contacted` and no outbound approval or send is implied. This is initial enrichment, not fulfillment of daily 100–300 new-company research goal or the 10,000-contact target.

## Operational priority

1. P0: true buyer INBOX with concrete signal and no adequate company-level response, then appointments and current qualified opportunities.
2. P1: live buyer need/budget/meeting/proposal.
3. P2: net-new **untouched** relevant company census, 3–5 actual named executives per priority company, source proof and legitimate routes; batch company + person + copy to Joyce before new outbound.
4. P3: vendors, service providers, PR/media/industry events; do not count them toward principal-side buyer conversion.

## Hard controls

- YOOZOO/游族、NetDragon/网龙 and affiliates: permanent proactive exclusion.
- Past no-reply company: HOLD; do not automatically cycle through 3–5 executives.
- No invented personal addresses, no contact in absent approval of specific new company/recipient/copy.
- Do not claim verified delivery from no bounce. Confirm actual SENT for send proof.
- No private buyer email bodies, unpublished deal terms or private contacts in this public report.

## Remaining gaps

- The new Python audit is **offline/export-based**, not a deployed always-on Gmail integration; scheduled tasks use the connected Gmail tools.
- Base44 static harvest is **not fixed** by simply creating a new recurring task; real repeated output must be proven through next-day batch and read-back.
- Exact cumulative 10k **unique relevant first-touched decision makers** is not yet recomputed from a fully canonical cross-channel ledger; report unknown until verified.
- Most historic company records still lack 3–5 independently verified decision makers and reliable routes.
- One validated candidate is not automatically a paying annual-contract buyer. Keep relationship pool and qualified annual-client revenue pipeline separate.

