# GGC 10K Executive Network — Sourcing Registry and QA

Updated: 2026-10-10 | Owner: Joyce/GGC

## Goal and boundaries

Build enough correctly identified Chinese-speaking/Chinese-led game-company decision makers to support at least **10,000 unique, legitimate, approved first touches**. This is not 10,000 generic addresses or 10,000 replies. The million-RMB annual-client buyer pool is a narrower commercial tier, NOT a cap on the total network.

**Human buyer replies take priority over all net-new research and all third-party activity.** Read BD_REPLY_FIRST_10000_EXECUTIVES_SOP_v1.md first.

## Upstream bulk-discovery sources

| Source | Research use | Caveat |
|---|---|---|
| TapTap developer services (https://developer.taptap.io/) | Search/identify developer accounts, studio names and actual games. The service site has publicly displayed more than 10,178 registered developer accounts. | These are NOT 10,178 verified companies, named leaders or potential buyers; dedupe parent groups and filter individuals. |
| ChinaJoy 2026 BTOB (https://btb.chinajoy.net/) | 2026 exhibitor/game/company discovery, language/region hints, updated professional roles. An official indexed directory showed 576 exhibitors. | Many vendors, ad networks, payments, media and technology providers are not game-owning principals. |
| Steam store (https://store.steampowered.com/) | Title → developer/publisher → owner/entity resolution, China/Asia PC teams. | Publishing credit need not imply development/rights ownership. |
| Google Play Games (https://play.google.com/store/games) | Package/app → publisher account → studio games/links. | Publisher account != operating company or real IP owner. |
| Apple App Store (https://apps.apple.com/) | App/game/developer IDs, app portfolio and regional signals. | App legal seller may differ from group/game rights owner. |
| Public company/team pages, securities filings | Verify own IP, parent entities, actual financial scale, founder and studio leaders. | Public support/IR inboxes are not person-level business routes. |
| Events/speaker/exhibitor listings and official product announcements | Identify current executives, product triggers and business role. | Confirm up-to-date position; no guessed email formats. |
| Existing 2026-09 GGC researched reserve | A starting RESEARCH seed only; cross-check with current Gmail and entity ledger. | The older 128-entry reserve includes bans, investors, giant groups, vendors and previously contacted companies. Never treat it as contact-ready. |

## Independent production queues

1. Raw source discoveries (100–300 company candidates per batch as feasible)
2. Canonical parent/entity and own-product checks
3. Chinese-led relevant game-company network qualified; core categories tagged, not the entire network limit
4. Current real names and jobs for 3–5 C-level/BU/Studio/Publishing/Product leaders per priority company
5. Legitimate public executive or warm business routes, separately verified
6. Cross-channel company first-touch/no-reply HOLD/STOP/bounce and banned-entity checks
7. Private company+person+proposed pitch approval queue for Joyce
8. Approved first-touch attempt and SENT/channel read-back
9. Genuine human reply routing into P0; need/meeting/opportunity conversion

## Actual software component

Runnable offline queue generator: [scripts/bd_source_graph_v1.py](../scripts/bd_source_graph_v1.py).

- Inputs: private companies.csv, people.csv, contact_history.csv, optional stop.csv.
- Exports: approval_queue.csv, needs_enrichment.csv, metrics.json to a user-chosen PRIVATE directory.
- Canonicalizes group/company aliases, dedupes named people, detects prior human engagement/no-reply and opt-outs, blocks user-excluded groups and invalid/generic routes.
- Does not crawl the web or send emails. Does not imply 10,000 records have been sourced or contacted.
- Never commit actual prospect names, addresses, email threads or outreach ledgers to this PUBLIC repository.

## QA output and decision gate

Report unique SOURCE COMPANIES, REAL NAMED EXECUTIVES, VERIFIED LEGITIMATE ROUTES, APPROVAL-READY PEOPLE, JOYCE APPROVED PEOPLE, CONFIRMED FIRST-TOUCH UNIQUE PEOPLE, HUMAN REPLIES, QUALIFIED NEED, MEETINGS, PROPOSALS, SIGNED, CASH. Show per-period and cumulative actuals; never relabel researched/approved as sent.

Approval is required before new cold outreach. Preserve company-level no-reply HOLD and the permanent Yoozoo/游族 and NetDragon/网龙 affiliation bans. If send endpoints fail, do not endlessly retry or invent delivery.

## Research-to-action pacing

- 10,000 legitimate unique first touches in 180 calendar days would mathematically require ~56/day; in 90 days ~112/day. These are sensitivity scenarios, not a current promise or proven email quota.
- A single Gmail account and approval workflow are meaningful throughput limits; do not try to evade mailbox restrictions with guessed accounts or burst sends.
- Prefer warm introducers and permitted business channels in addition to verified corporate addresses.
- Before each bulk sourcing wave: resolve P0 inbound buyer backlog, then replenish untouched qualified accounts/people and submit compact approval batches.

## Verification status

Source counts above are discovery-capacity indicators, NOT a completed sourced/contact-ready universe. The first implementation is a reusable normalization and approval-queue component, not a working 10k outbound machine. It needs real authorized input data and a tested delivery channel before any production throughput claim.