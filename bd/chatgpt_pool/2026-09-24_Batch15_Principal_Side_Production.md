# GGC Strategic BD — Batch15 Strict-Core Principal-Side Production

**Date:** 2026-09-24  
**Scope:** Chinese-speaking principal-side founders/bosses in Casino / Arcade / Sims / AI Wellness  
**Customer-level details:** private GGC repository only  

## Process gates applied
- Read private cross-task suppression ledger before sourcing/sending.
- Read current BD execution plan, China ICP and latest principal reserve.
- Checked Gmail company/thread history before each outbound action.
- Company STOP/HOLD and route hard-bounce suppression override volume target.
- Service providers/vendors do not count toward principal-side KPI.
- Historical SENT is not treated as qualified unless current category fit, principal status, route validity, ownership and suppression checks pass.
- No claim of delivery is made from absence of a bounce.

## Run metrics
- Raw Gmail SENT today at checkpoint: **37**
  - Includes one prior relationship-maintenance reply outside this production batch.
- BD outbound actions in this run: **36**
  - Due follow-ups: **31**
  - Fresh first touches: **5**
- Strict four-core-category qualified SENT: **15**
- Legacy principal follow-ups excluded from strict-core KPI due incomplete revalidation against the new category gate: **21**
- Strict-qualified hard failures observed: **1**
- Strict-qualified no-hard-failure-observed / final delivery unknown: **14**
- Delayed at checkpoint: **0**
- Human replies at checkpoint: **0**
- Positive replies: **0**
- Meetings: **0**
- Gap to 100 strict-qualified target: **85**

## Strict category mix
- Arcade / Casino-adjacent: **10**
- Sims: **3**
- AI Wellness / Spirituality: **2**

## QA correction vs. older production reporting
The stricter four-category gate introduced after the earlier batches means a real principal-side company is **not automatically qualified for this run**. Twenty-one outbound actions were to legitimate principal/publisher contacts but their current fit to Casino / Arcade / Sims / AI Wellness was not revalidated strongly enough during this run, so they are excluded from the qualified KPI rather than being inflated into the 100 target.

Likewise, `no hard failure observed` is reported only as a transport-status checkpoint; it is **not** equivalent to delivered.

## Hard blocker
The existing 128-company China reserve is a **sourced reserve**, not a send-ready reserve. The suppression audit surfaced multiple stale/final-failure routes, confirming that the pool cannot safely be treated as ready-to-send.

With 85 strict-qualified sends remaining, the standing reserve rule requires at least **170 send-ready verified contacts**. That threshold is not currently met. The run therefore stopped rather than reuse stale routes or misclassify non-core principals as qualified.

## Next production requirement
Build a new >=170-contact send-ready reserve where every row has:
1. current Casino / Arcade / Sims / AI Wellness proof;
2. principal-side control of product/IP/publishing/P&L/capital;
3. Chinese-speaking founder/CEO/GM/Studio Head preference;
4. legitimate public/current route;
5. Gmail company/thread dedupe;
6. private suppression check;
7. cross-task ownership check.

Only after these gates pass should the remaining quota resume.
