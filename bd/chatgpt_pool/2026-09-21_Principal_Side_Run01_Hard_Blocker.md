# GGC Principal-Side BD — Run01 Hard Blocker

**Date:** 2026-09-21  
**Owner:** ChatGPT / Joyce Copilot  
**Status:** HARD BLOCKER — principal-side reserve + deliverability remediation gate not yet cleared; no new sends executed in this run.

## Canonical inputs read
- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- newest `bd/chatgpt_pool/` files, especially:
  - `2026-09-21_Batch12_Deliverability_Gate_After_91_Sent.md`
  - `2026-09-21_Principal_Side_Buyer_Pool_v1.md`
  - `2026-09-20_Batch11_Production_100_Completed.md`

Company-level ownership and Gmail-history dedupe were enforced before any possible send. Base44 Agent-A first-wave accounts were not intentionally touched.

## Opening Gmail checkpoint
Gmail `SENT` for the account date window `2026-09-21` returned **98 sent messages** before this run. These are account-level messages from earlier activity and are **not counted as this run's qualified principal-side quota**.

### This run
- Qualified principal-side SENT: **0**
- Hard bounces caused by this run: **0**
- Replies attributable to this run: **0**
- Positive replies attributable to this run: **0**
- Meetings attributable to this run: **0**
- Gap to 100-SENT run target: **100**

## Principal-side sourcing / screening performed
Started from the 23-company principal-side seed pool and added 13 additional principal candidates / investor routes for a total of **36 companies/funds screened** in this run/rebuild pass.

### Live Gmail dedupe invalidated several seed-pool assumptions
The following companies are **not new first-touch targets** despite appearing in the seed pool or fresh research:
- X.D. / 心动 — direct GGC first-touch 2026-08-21 + follow-up 2026-09-18.
- Bilibili Game — direct GGC first-touch 2026-09-19 to `gamebd@bilibili.com`.
- Infold / Papergames / 叠纸 — direct GGC first-touch 2026-09-18 to `dzbd@papegames.net`.
- First Fun — direct GGC first-touch 2026-09-18 to `contact@firstfun.com`.
- Lilith Games — direct GGC first-touch 2026-09-18; older `bd@lilithgames.com` route also previously hard-bounced.
- Perfect World — direct GGC first-touch 2026-08-21 + follow-up 2026-09-18 to `global@wanmei.com`.
- BoogieGames — direct GGC first-touch 2026-09-19 and `biz@boogie.games` hard-bounced.
- Qiming Venture Partners — SAGA/Bunny financing outreach already sent 2026-08-30; company-level ownership therefore blocks a new cold first-touch in this principal BD run.

These are not counted as current-run qualified new targets.

## Current newly verified principal routes after tightening the gate
Verified/current public principal-side routes with no direct prior Gmail outreach found in this pass include:
- **CMC Capital** — investor principal; official current contact route `contactus@cmccap.com`; route is generic, therefore HOLD pending a named investment-side route if possible.
- **ApoWo / 爱扑网络** — game R&D/IP principal; current official company contact `contact@apowo.com`; Gmail clean.
- **Top Chop Games** — game studio principal; current business inquiry route `hello@topchopgames.com`; Gmail clean; global fallback, not China-first.
- **ZhenFund / 真格基金** — capital principal; current official BP routes `dream@zhenfund.com` and AI `prompt@zhenfund.com`; Gmail has no prior direct outreach to ZhenFund.
- **Linear Capital / 线性资本** — capital principal; current official project route `bp@linear.vc`; Gmail has no prior direct outreach.
- **Shunwei Capital / 顺为资本** — capital principal; current official site exposes a BP-submission contact, but the address is email-protected/obfuscated in retrieval; HOLD until the exact address can be copied from a reliable public source.
- **Yunqi Partners / 云启资本** — capital principal; current public `community@yunqi.vc`; because this is a community route rather than an investment decision-maker/BP route, HOLD under the stricter principal routing standard.

Under the tightened post-Batch12 routing rule, only **4 routes are currently clean enough to be considered immediately send-ready** (ApoWo, Top Chop, ZhenFund BP, Linear BP). CMC/Yunqi/Shunwei remain route-quality holds.

## Service-provider exclusion
Service/agency/tool/media/exhibition results encountered during discovery were rejected at the discovery gate and **not admitted into the buyer pipeline or quota**. Examples include UA/rewarded-acquisition vendors, event organizers, ad/marketing companies and non-game peripheral vendors. They do not count as prospects, replies or meetings.

## Hard blocker
Batch12 ended with **10/91 = 10.99% permanent/blocked delivery failure**, including a recipient-policy block. Its explicit remediation gate requires:
1. stop relying on generic stale role aliases;
2. prefer named current decision-makers or current investment/publishing routes;
3. build at least **200 current verified reserve contacts** before attempting another 100-SENT production run;
4. resume only after the new route pattern is safely below the 10% failure line.

That remediation is **not yet complete**. Current strict principal-side send-ready reserve is 4, far below the required 200 reserve and below the 100 legitimate targets required for this run. Sending now would violate both the reserve-first workflow and the previous sender-reputation protection gate.

## Exact run metrics
- Account-level SENT today before this run: **98**
- Principal candidates screened/re-screened: **36**
- Confirmed duplicate / prior company-level touch discovered in live Gmail pass: **8**
- Newly verified principal routes: **7**
- Strict send-ready routes after route-quality gate: **4**
- Service providers admitted: **0**
- This-run qualified principal SENT: **0**
- This-run bounced: **0**
- This-run likely delivered: **0**
- Replies / positive replies / meetings attributable to this run: **0 / 0 / 0**
- Target achieved: **NO**
- Gap to 100: **100**
- Hard blocker: **YES — unresolved systemic deliverability remediation + insufficient verified principal-side reserve**

## Required remediation
Continue building the principal-only reserve from current official 2026 sources and named investment/publishing/studio decision-makers until there are >=200 current verified contacts. Prioritize Mainland China and Chinese-speaking R&D/IP owners, publishers, CVC/VC/growth funds and strategic game buyers. Do not resume generic service-provider sourcing or stale role aliases.
