# GGC Strategic BD — Batch12 Deliverability Gate After 91 Sent

**Date:** 2026-09-21  
**Owner:** ChatGPT-B / Strategic Acquisition  
**Status:** HARD BLOCKER — sender/deliverability protection gate triggered before the remaining quota was filled.

## Canonical inputs read
- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- newest files under `bd/chatgpt_pool/`, especially `2026-09-20_Batch11_Production_100_Completed.md` and `2026-09-20_Batch11_Fresh_Route_Restart_and_Positive_Replies.md`

Company-level ownership remained enforced. No Base44 Agent-A first-wave account was intentionally re-touched. Gmail history was reconciled before deciding whether to continue sending.

## Opening Gmail checkpoint
At the 2026-09-21 production checkpoint, Gmail showed **91 SENT actions** in the current date window. The 91 consisted of **90 new first-touch / partnership emails plus 1 warm threaded reply to The Node**.

### Deliverability outcome visible at checkpoint
- SENT actions: **91**
- Permanent / blocked delivery failures already visible: **10**
- No-hard-failure visible yet: **81**
- Observed hard/blocked rate: **10.99%**
- New human replies visible in the 2026-09-21 inbox window: **0**
- Positive replies attributable to these 91: **0**
- Meetings attributable to these 91: **0**
- Automated acknowledgement: **1** — Metacore general info route
- Remaining gap to the 100-SENT run target: **9**

## New hard suppressions / route failures
The following routes produced permanent or blocked delivery outcomes and must not be reused:
- `sales@goodgamestudios.com` — 550 address not found
- `admin@mmo-ho.com` — 550 address not found
- `hello@stg.ro` — 550 address not found
- `Info@bodevstudios.com` — remote-server delivery failure / misconfiguration
- `info@sightlinegames.com` — account not found / unable to receive
- `publishing@ae-mobile.com` — message blocked by recipient system
- `info@hanlian.com` — address not found
- `contact@crabbystudio.com` — 550 address not found
- `partnership@lightcore.games` — 550 address not found
- `business@gamecafe.co` — target group missing / sender not permitted

## Pattern diagnosis
The failing routes are not concentrated in one company/domain, but they are concentrated in one sourcing style: generic role aliases (`info@`, `contact@`, `sales@`, `admin@`, `business@`, `publishing@`, `partnership@`) on company pages that may still look current while the mailbox itself is stale, disabled, group-restricted or policy-blocked.

Because the observed cohort failure rate is **10/91 = 10.99%**, the current route pattern has crossed the user-defined **>10% stop threshold**. One failure is also a policy block (`publishing@ae-mobile.com`), which materially raises sender-reputation risk.

## Decision
**Do not send the remaining 9 emails simply to make the counter reach 100.** The run is therefore incomplete at 91 SENT because the explicit hard-blocker rule has been met: systemic deliverability / sender-reputation risk.

## Required remediation before scale resumes
1. Stop promoting generic role inboxes to send-ready solely because they appear on a company/contact page.
2. For the next reserve, require one of:
   - named current Founder/CEO/COO/Head of Publishing/Head of Overseas/BD contact from a 2026 event/company page;
   - current partnership/publishing form or email independently confirmed by a second current source;
   - company-domain mailbox observed in a recent 2026 announcement, exhibitor page, press kit, investor filing or named business profile.
3. Prefer named-person routes over generic aliases for the next production cohort.
4. Build at least **200 current verified reserve contacts** before attempting another 100-SENT run.
5. Keep all 10 failed routes in the hard suppression ledger.
6. Resume only after the new route pattern is tested below the 10% hard-failure line.

## Exact run status
- Sourced/attempted in current production window: **91 SENT actions visible**
- Verified enough to send before DSN feedback arrived: **91**
- SENT: **91**
- Bounced/blocked: **10**
- Likely delivered / no hard failure yet: **81**
- Human replies: **0**
- Positive replies: **0**
- Meetings: **0**
- 100-SENT target achieved: **NO**
- Gap: **9**
- Hard blocker: **YES — deliverability/source-pattern failure >10% plus recipient-policy block**
