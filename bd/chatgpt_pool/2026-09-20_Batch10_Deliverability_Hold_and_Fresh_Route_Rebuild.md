# GGC Strategic BD — Batch 10 Deliverability Hold + Fresh-Route Rebuild

**Date:** 2026-09-20  
**Owner:** ChatGPT Strategic BD Pool (`ChatGPT B`)  
**Mode:** China-first / sender-protection / fresh-route sourcing

## 1. Canonical inputs read before touching any company

- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- newest prior state: `bd/chatgpt_pool/2026-09-19_Batch09_Deliverability_Stop_and_Gmail_Reconciliation.md`
- Gmail SENT / bounce / inbound history

Company-level ownership remains mandatory. Base44 A-owned first-wave companies remain excluded. Companies already touched in Batches 01–09 remain historical-touch accounts; do not re-first-touch them through alternate addresses.

## 2. Live Gmail opening checkpoint — 2026-09-20

| Metric | Result |
|---|---:|
| 2026-09-20 SENT before this run | **0** |
| New human replies since prior checkpoint | **0** |
| Positive replies | **0** |
| Meetings | **0** |
| New automated reply | **0** |

### Deliverability correction from 2026-09-19

Batch09 recorded 20 hard / envelope failures at its checkpoint. A fresh Gmail reconciliation now returns **21 permanent failure notices** for 2026-09-19 against **140 SENT**, so the observed day-level permanent-failure rate is now:

**21 / 140 = 15.0%**

This is above the 10% source-quality cutoff and materially outside the desired >=90% no-hard-bounce delivery quality.

Separately, `bd@boxgames.com` remains in a **temporary delayed-delivery** state and is not counted as a hard failure yet.

One of the 21 permanent failures is `bd@joymore.cn`, which returned a **554 5.7.1 policy/block response** rather than a simple nonexistent-address error. This strengthens the sender-reputation risk diagnosis.

## 3. Run decision — no cold send while systemic sender risk is active

**New SENT this run: 0.**

The current per-run target is 100 SENT, but the hard-blocker policy explicitly permits stopping below 100 for systemic deliverability failure that risks the Gmail/domain reputation. That condition remains active today:

1. The prior day permanent-failure rate is now **15.0% (21/140)**.
2. Several failures are 550/551/554 address or policy failures, not only transient delays.
3. The prior evergreen/public-contact-page sourcing pattern already exceeded the 10% cutoff.
4. A recipient-policy 554 block is now present.
5. Sending a fresh 100-message batch before route quality and sender health are repaired would optimize quantity at the expense of sender reputation and future inbox placement.

Therefore this run did **not** transmit even the newly verified routes below. They are held as a fresh-route reserve for a later sender-health-approved batch.

## 4. Fresh sourcing channel rebuild

This run deliberately abandoned the old evergreen-contact-page pattern and screened current 2026 sources: official corporate sites crawled/current in 2026, dated 2026 ChinaJoy exhibitor/partner announcements, and current public business contacts.

### A. Fresh-route reserve — route verified, **not sent**

| Company | Current evidence | Public business route | Fit / missing corner | GGC mapping | Status |
|---|---|---|---|---|---|
| 360 Games | Current official 360 Games site; global publishing / localization cooperation | `360game-bd@360.cn` | Strong publishing platform; potential cross-title global operating / LiveOps / portfolio standards | Publishing / Strategic Copilot | ROUTE VERIFIED — HOLD |
| Hippydog Studio / 上海逸派玩 | Current official site; PC game mobile publishing and developer cooperation | `hippydogstudio@gmail.com` | Publisher with China localization/porting strength; opportunity to extend lifecycle / commercialization / global operating standards | Publishing Copilot | ROUTE VERIFIED — HOLD |
| FantaPass MR Studio | Current official studio site + active MR titles | `contact@fantapassmr.com` | Founder-led original MR studio; market validation, monetization, LiveOps and scale system | Incubation / GTM / Copilot | ROUTE VERIFIED — HOLD |
| AppMobio | Dated 2026 ChinaJoy official exhibitor announcement with named contact Tom Pan | `tom@appmobio.com` | UA / performance-marketing ecosystem partner for GGC portfolio | Strategic Partner / UA ecosystem | ROUTE VERIFIED — HOLD |
| Dataify | Dated 2026 ChinaJoy BTOB official announcement | `sales@dataify.com` | AI/data/token infrastructure; potential AI workflow/data partner | AI Workflow / Strategic Partner | ROUTE VERIFIED — HOLD |
| Linguitronics | Current public Shanghai contact + China game-localization relevance | `info_cn@linguitronics.com` | Localization/globalization layer; potential delivery partner | Global GTM / Strategic Partner | ROUTE VERIFIED — HOLD |
| MetaX | 2026 ChinaJoy current ecosystem evidence; public commercial inquiry route | `marketing@metaxsoft.com` | CTV / monetization / distribution ecosystem | Strategic Partner | ROUTE VERIFIED — HOLD |
| The Node | 2026 ChinaJoy INDIE GAME exhibitor + current public business email | `business@thenode.gg` | Gaming influencer marketing / creator distribution | Global GTM / Strategic Partner | ROUTE VERIFIED — HOLD |
| CCHANGE / 择变科技 | Dated 2026 ChinaJoy official BTOB announcement; marketing + own products + game publishing | `sales@thecchange.net` | UA + monetization + publishing stack; cross-portfolio operating opportunity | Publishing / Growth / Strategic Partner | ROUTE VERIFIED — HOLD |
| Playio / GNA | 2026 ChinaJoy official exhibitor + current public sales route | `sales@gna.company` | Rewarded UA / retention; growth ecosystem partner | UA / Strategic Partner | ROUTE VERIFIED — HOLD |
| ANNO Global Game Localization | Dated 2026 ChinaJoy official exhibitor announcement with named business managers | `eve@annobe.cn` (primary) | Game localization at scale; potential portfolio localization/QA partner | Global GTM / Strategic Partner | ROUTE VERIFIED — HOLD |
| 旺脉集团 / AdWangmai | Dated 2026 ChinaJoy official BTOB announcement with named BD Kelly Lu | `kelly.lu@adwangmai.com` | AI marketing / SDK monetization / DSP; potential growth and monetization partner | Growth / Strategic Partner | ROUTE VERIFIED — HOLD |
| Novabeyond | Dated 2026 ChinaJoy official BTOB announcement with current sales route | `sales@novabeyond.com` | Emerging media / OEM / CTV global growth | UA / Strategic Partner | ROUTE VERIFIED — HOLD |

**Exact-route Gmail dedupe:** no prior Gmail history was returned for the above tested routes at this checkpoint.

### B. Screened but not approved for production send

| Candidate | Reason not approved |
|---|---|
| TapTap cooperation route | Current route exists, but XD is already in prior-touch / ownership exclusions; treat group-level ownership conservatively |
| Miracle Games | Current 2026 activity verified, but no sufficiently current corroborated business email found |
| Joycoal Games / 乐炭网络 | Current 2026 studio signal; no public business email found |
| 杭州黑岩网络 | Current ChinaJoy signal; available business email lacks a second current official corroboration |
| 创天互娱 | Strong 2026 global/IP signal; no current legitimate email route found in this run |
| 厦门玲央奈软件 | Current 2026 game-company signal; no current legitimate email route found |
| 游戏曙光 | Current 2026 indie/studio signal; no current legitimate email route found |
| 排得游戏 | Current 2026 BTOB partnership signal; no explicit company business email surfaced |
| 玩咖欢聚 / Wanka | Strong current 2026 signal; third-party email exists but not accepted under the new current-source standard |
| Veewo Games | Public address surfaced as support; excluded by contact rules |
| 无事生游工作室 | Current founder contact exists, but the three-person pre-launch indie profile is below the preferred high-value commercial-size filter |

## 5. Production-resume gate

Do not restore 100-SENT production simply because a public email exists. Before a future high-volume batch, require all of the following:

1. **Sender health:** no active evidence of systemic policy blocking / abnormal hard-bounce behavior from the prior batch.
2. **Fresh-route reserve:** at least **100 send-ready** targets, preferably **200** for a 2× reserve, using current/double-corroborated routes.
3. **ICP quality:** core China/Chinese-speaking game companies remain first priority; ecosystem partners are supplementary, not quota filler.
4. **Ownership:** Base44 A-owned and prior ChatGPT-touched companies excluded at company/group level.
5. **Route quality:** current named BD/executive/business route; no guessed patterns, support/privacy/legal/abuse inboxes, or stale address reuse.
6. **Bounce suppression:** all prior hard-failure routes remain suppressed; do not retry via alternate company email in the same outreach window.

## 6. Exact run metrics

| Metric | Result |
|---|---:|
| Candidates screened / researched | **24** |
| Fresh route-verified companies added to reserve | **13** |
| Send-approved while sender-health hold is active | **0** |
| New SENT | **0** |
| New hard bounce | **0** |
| New likely delivered | **0** |
| New human replies | **0** |
| Positive replies | **0** |
| Meetings | **0** |
| Per-run target | **100 SENT** |
| Gap to target | **100** |
| Target achieved | **NO** |
| Hard blocker | **YES — systemic deliverability / sender-reputation risk; plus insufficient 100-route fresh reserve** |

## 7. Next operational state

- Continue using current-year event/corporate/partnership sources to rebuild a 100–200-company verified reserve.
- Maintain all Batches 01–09 company-level ownership exclusions.
- Do not use volume to mask deliverability failure.
- Re-check `bd@boxgames.com` only for its final delivery status; do not resend while Gmail is still retrying.
- Resume production outbound only after sender-health and reserve gates above are satisfied.
