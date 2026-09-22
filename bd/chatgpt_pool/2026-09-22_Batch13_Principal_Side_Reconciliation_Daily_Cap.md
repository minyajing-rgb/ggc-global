# GGC Strategic BD — Batch13 Principal-Side Reconciliation / Daily Cap

**Date:** 2026-09-22  
**Owner:** ChatGPT-B / GGC Strategic BD  
**Status:** HARD BLOCKER FOR ADDITIONAL SCALE TONIGHT — daily production ceiling / sender-protection gate.

## Canonical inputs read
- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- `bd/chatgpt_pool/2026-09-21_China_Principal_Reserve_for_2026-09-22.md`
- `bd/chatgpt_pool/2026-09-21_Principal_Side_Buyer_Pool_v1.md`
- newest prior deliverability files under `bd/chatgpt_pool/`

GitHub remains the canonical system of record. Google Drive is not used for this pipeline.

## Gmail reconciliation — 2026-09-22
Gmail SENT search for the local-date window returned **183 total SENT actions**.

The earlier same-day principal-side reconciliation had **163 raw SENT / 161 qualified principal-side SENT**, with two non-principal/service-provider actions excluded. Since that checkpoint, Gmail shows **20 additional qualified principal-side actions**: 19 new first-touch principals plus 1 investor follow-up.

### Current auditable totals
- Raw Gmail SENT: **183**
- Qualified principal-side SENT: **181**
- Excluded non-principal/service-provider SENT: **2**
- Qualified new first-touch: **132**
- Qualified follow-ups: **49**
- Hard bounce / blocked: **14**
- Temporary delivery delay: **1**
- No hard failure visible: **167** qualified actions, of which **1** is still delayed and **166** have no bounce/delay notice visible
- Qualified human replies visible today: **2**
- Positive replies: **0**
- Meetings attributable to today: **0**

### Latest principal-side sends visible before this reconciliation
Examples include Mercuri, Drilo Ventures, Space Ape Games, Nexters/GDEV, Headup, Sometimes You, Super Rare Games, Playtonic, Fulqrum, Modern Wolf, Armor Games, Slug Disco, GreaterThan Group, 格来云游戏, 疯狂体育, 百奥/天梯互娱, 龙渊, 掌趣科技, 心动/XD, plus one due investor follow-up to MindWorks.

## Deliverability gate
A broader DSN / postmaster reconciliation found **14 permanent failure / blocked messages** plus **1 temporary delay** in the current date window. The hard-failure rate is **14 / 183 = 7.65%** on raw SENT, still below the 10% source-pattern emergency cutoff but too high to justify another large burst near the daily ceiling.

The hard failures include stale/nonexistent routes at multiple companies and funds; the latest cohort also produced a failure on the generic `hello@drilo.vc` route. The temporary delay is on `bd@shengyugame.com`.

The canonical production plan defines **30–200/day** as the acceptable operating range. Continuing another 100-email batch tonight would push the account far above the 200/day ceiling and materially increase sender-reputation risk.

## Decision
**Do not launch another 100-message batch tonight.** The account is already at 183 raw / 181 qualified sends for the day, leaving only 17 sender actions before the canonical 200/day ceiling. Because the next-run rule also requires a reserve >=2× the remaining run gap and current verified-route logging is incomplete, scale is blocked tonight by sender-protection + reserve-verification requirements.

This is a run-level blocker, not a reason to disable the recurring BD pipeline.

## Principal-side reply status
- Human reply #1: current need is experienced paid-acquisition cooperation; not a fit for current GGC proposal → **Neutral / Not positive**.
- Human reply #2: currently not looking for additional operating partners → **Negative / Not positive**.
- Service-provider discovery reply(s) are explicitly excluded from principal-side success metrics.
- Automated investment inbox acknowledgements are not counted as positive replies.

## Logging gap discovered
The earlier 2026-09-22 execution had not yet written a same-day production ledger under `bd/chatgpt_pool/`. This file repairs the top-line reconciliation, but exact pre-send `sourced` and `rejected-as-service-provider-before-send` counts cannot be reconstructed reliably from Gmail alone. Do not invent them.

For the next run, every sourced company must be logged before send with:
- Company
- Buyer type: Investor / R&D-IP / Publisher / Strategic Buyer
- Principal-side qualification evidence
- Source / current hard signal
- Decision-maker / route
- Gmail dedupe result
- Variant
- Missing-corner diagnosis
- Sent / bounce / reply / meeting / next action

## Next-run priority
1. Mainland China / Chinese-speaking R&D and IP owners first.
2. Publisher principals with real title/portfolio P&L second.
3. Game/AI-entertainment investors with current thesis or recent deal evidence.
4. Named current decision-maker or independently confirmed current business route over generic aliases.
5. Keep service providers completely outside qualified-send and success counts.

## Exact status for this reconciliation run
- Newly sourced in this reconciliation run: **0** (scale stopped at the gate before new sourcing/sending)
- Newly rejected as service-provider in this reconciliation run: **0**
- Newly verified principals in this reconciliation run: **0**
- Newly SENT in this reconciliation run: **0**
- Daily qualified principal-side SENT already achieved before gate: **181**
- Daily gap to canonical 200/day sender-action ceiling: **17 raw sender actions**
- Gap to this run's requested 100 qualified sends: **100**, blocked by the daily ceiling before new sending began
- Hard blocker: **YES — daily production ceiling + incomplete 2× verified-route reserve for another 100-send batch**
