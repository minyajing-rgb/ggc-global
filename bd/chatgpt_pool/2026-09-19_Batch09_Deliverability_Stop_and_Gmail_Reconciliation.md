# GGC Strategic BD — Batch 09 Deliverability Stop + Gmail Reconciliation

**Date:** 2026-09-19  
**Owner:** ChatGPT Strategic BD Pool (`ChatGPT B`)  
**Mode:** China-first / production outbound guardrail run  

## 1. Canonical inputs read

- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- `bd/chatgpt_pool/2026-09-19_Batch08_Official_Route_Continuation.md`
- Gmail SENT / bounce / inbound state before touching any new company

Company-level ownership and Base44 A-owned exclusions remain in force.

## 2. Live Gmail opening checkpoint

Gmail shows **140 SENT** on 2026-09-19 before this run attempted any new outbound.

| Metric | Live result |
|---|---:|
| 2026-09-19 SENT | **140** |
| Hard / envelope delivery failures observed | **20** |
| Likely delivered / no hard bounce observed yet | **120** |
| Observed hard-bounce rate | **14.3%** |
| Human replies | **0** |
| Positive replies | **0** |
| Meetings | **0** |
| Automated replies | **1** (Rayark support acknowledgement; excluded from KPI) |

The 20 failures include the routes already suppressed in Batches 07/08. A later failure on `bd@joymore.cn` was also visible at this checkpoint as a 554 policy/block response.

## 3. Reconciliation: 15 SENT not yet reflected in Batch08

Batch08 closed at 125 SENT, but live Gmail now shows 140. The following 15 later sends exist in Gmail and are reconciled here so they are not accidentally re-contacted:

| Day # | Company / route | Status at checkpoint |
|---:|---|---|
| 126 | NEOCRAFT — `Justin@neocraftstudio.com` | Sent; no hard bounce observed yet |
| 127 | 机核发行 / GCORES — `publishing@gcores.com` | Sent; no hard bounce observed yet |
| 128 | 大宇資訊 / Softstar — `business@softstar.com.tw` | Sent; no hard bounce observed yet |
| 129 | 弘煜科技 — `public@fy.com.tw` | Sent; no hard bounce observed yet |
| 130 | 天上友嘉 — `shangwubu@youkia.com` | Sent; no hard bounce observed yet |
| 131 | ICAN — `business@icantw.com` | Sent; no hard bounce observed yet |
| 132 | 光宇游戏 — `guojian@gyyx.cn` | Sent; no hard bounce observed yet |
| 133 | 欣盟互動 / All9Fun — `marketing@all9fun.com` | Sent; no hard bounce observed yet |
| 134 | MuMu Global — `business@mumuglobal.com` | Sent; no hard bounce observed yet |
| 135 | 唯數娛樂 / Gamehours — `bd@gamehours.com` | Sent; no hard bounce observed yet |
| 136 | MODO — `business@modo.cn` | Sent; no hard bounce observed yet |
| 137 | HappyTuk — `ht_bd@mangot5.com` | Sent; no hard bounce observed yet |
| 138 | LDPlayer — `Mialin@ldplayer.net` | Sent; no hard bounce observed yet |
| 139 | 浮光遊戲 / Dusklight — `dusklight.game@gmail.com` | Sent; no hard bounce observed yet |
| 140 | 初心网络 / Origin Mood — `bd@originmood.com` | Sent; no hard bounce observed yet |

These companies are now explicitly ChatGPT-owned historical-touch accounts. Do **not** send another first-touch email through an alternate address.

## 4. Hard blocker decision for this run

**No additional cold email was sent in this run.**

The per-run target is 100 SENT, but the prompt explicitly allows stopping below 100 when there is a **systemic deliverability failure that risks the sending domain/account**. That condition is now met:

1. Batch08 source-pattern bounce rate was already **16.0% (4/25)**, above the >10% cutoff.
2. Live day-level hard-bounce rate is **14.3% (20/140)**.
3. The current source pattern — older/public contact-page addresses, including named legacy contacts — has produced repeated 5.1.1 / 550 / 554 failures.
4. At least one route (`bd@joymore.cn`) is being blocked by recipient policy rather than merely returning a stale-address error, increasing sender-reputation risk.
5. The most recent canonical Batch08 already mandated stopping this source pattern and switching to fresher, dated routes.

Continuing to force another 100 sends before rebuilding route quality would violate the deliverability guardrail and unnecessarily risk Gmail/domain reputation.

## 5. Required remediation before high-volume sending resumes

For the next production send set, require a different sourcing channel. Accept only routes that satisfy one of these stronger recency checks:

- Current-year corporate press release / partnership announcement with named business contact.
- Current-year conference / exhibitor / speaker / partner page with a named BD / publishing / executive contact.
- Current corporate filing or official partner page with an explicitly current business-development route.
- Named Founder / CEO / COO / Head of Overseas / Head of Publishing / CMO / BD contact whose route is independently corroborated by a second current source.
- Current official partnership / developer-submission route that is not customer support, legal, privacy, press-only, or generic stale contact-page residue.

Do not resume production volume from evergreen contact pages alone. Do not guess email patterns. Do not retry any bounced route in +5/+10 follow-up.

## 6. Exact run result

| Metric | Result |
|---|---:|
| Opening day SENT | **140** |
| New SENT this run | **0** |
| Per-run target | **100** |
| Gap to per-run target | **100** |
| Sourced / verified for safe production sending | **0 approved under new recency standard** |
| Hard blocker | **YES — systemic deliverability / sender-reputation risk** |
| Human replies | **0** |
| Positive replies | **0** |
| Meetings | **0** |

### Operational interpretation

The day already sits at **140 SENT**, inside the overall 30–200/day operating range, but this run is deliberately stopped below its 100-SENT target because deliverability quality is outside guardrail. The next run should not treat the existence of old public emails as sufficient verification; it must rebuild the prospect reserve using fresher, dated contact evidence before resuming high-volume sends.
