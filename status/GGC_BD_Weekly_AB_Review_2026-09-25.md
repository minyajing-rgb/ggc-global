# GGC BD Weekly A/B Review — 2026-09-25

## Decision

**No A/B winner can be declared this week.**

The current qualification rule was applied retrospectively to the seven-day send population:

1. Chinese-speaking / Chinese-led principal-side company;
2. controls its own product or IP;
3. Casino / Arcade / Sims / AI wellness;
4. annual profit approximately RMB 30M+ or equivalent strong, durable cash-generation evidence;
5. a verified operating gap (internal publishing missing or self-publishing being built);
6. company-level STOP clear;
7. valid route to a budget-owning executive.

No sent sample completed all seven gates. Therefore the valid experiment denominator is zero, regardless of raw opens, replies, or meetings.

## Review window

2026-09-19 00:00 through 2026-09-25 18:32, Asia/Hong_Kong.

The profit-first rule became effective on 2026-09-24 but is used here as the only canonical qualification rule. Earlier mixed-pool sends are retained as operating telemetry only and are excluded from conversion claims.

## Strict A/B scorecard

| Variant | Eligible delivered companies | Human need replies | Qualified meetings | Result |
|---|---:|---:|---:|---|
| A — capability / operator-first | 0 | 0 | 0 | N/A |
| B — target / product-trigger-first | 0 | 0 | 0 | N/A |

Target-first messages generated some raw engagement in the mixed pool, but every engaged thread failed at least one current hard gate. This is not evidence that B wins with the intended buyer population.

## Raw operating telemetry — not A/B conversion

| Metric | Result |
|---|---:|
| BD-like SENT messages | 696 |
| Distinct threads | 649 |
| Distinct recipient routes | 648 |
| Distinct final-failure routes | 68 |
| Final-failure rate by distinct route | 10.5% |
| Delay-only routes at checkpoint | 4 |
| Human business-reply threads identified | 13 |
| Strict qualified buyer replies | 0 |
| Strict qualified meetings | 0 |
| Exact accidental duplicate pairs | 1 |

These figures show activity volume, not qualified acquisition. SENT is not delivery; absence of a bounce is not proof of delivery.

## Why the experiment is invalid

- The send population mixed principal-side studios with publishers, investors, service providers, channels, outsourcing companies, platforms, very large companies, small CPs, and companies whose payment capacity was not verified.
- Many messages were sent before profit / cash-generation evidence became the first gate.
- Variant and segment were not captured consistently as structured fields at send time.
- Old no-reply threads were followed up in bulk, so first-touch and follow-up effects are confounded.
- Route quality was too weak: 68 distinct recipient routes ended in final failure.
- Company-level STOP was not consistently enforced across tasks.

## Compliance and quality findings

### 1. STOP failures

Two known company-level no-demand / rejection cases were contacted again after the stop signal. They must remain permanent HOLD / STOP and be excluded from all future sequences.

### 2. Bounce suppression failure

At least two recipient routes were reused after a hard failure had already been observed within the review window. This is a company-wide suppression defect, not a copy problem.

### 3. Duplicate send

One reply was sent twice within 12 seconds after a connector error was treated as a send failure. Future retry logic must check the Sent folder and message/thread state before retrying.

### 4. Legacy no-reply follow-up contamination

Large follow-up blocks were sent to historical no-reply threads. Under the current rule, all such threads are HOLD until the company passes the full qualification gate again and the route, ownership, STOP state, and latest reply are rechecked.

## Current company-first funnel

| Funnel layer | Count |
|---|---:|
| Research Universe | 33 |
| Category + own-IP fit | 29 |
| Payment-capacity likely | 13 |
| Economic gate verified | 3 |
| Reachable, unsuppressed decision-makers | 0 |

The bottleneck is not message volume. It is the final conversion from economic evidence to a valid executive route with a verified operating gap and clean company-level history.

## Stop and repair actions

1. **Invalidate the mixed-pool A/B result.** Do not carry forward a B-winner claim.
2. **Make company qualification a pre-send object.** Required fields: normalized company, parent, Chinese leadership, own IP, category, profit/cash-flow evidence, operating gap, company STOP status, owner, decision-maker, route source, route confidence.
3. **Randomize only after qualification.** A company enters A/B only when every required field is complete.
4. **Use company as the experimental unit.** Multiple contacts at one company stay in one variant.
5. **Separate first touch from follow-up.** Historical no-reply threads remain HOLD; they do not enter the experiment automatically.
6. **Enforce suppression before draft creation and again before send.** One company-wide ledger must cover every task and agent.
7. **Route quality rule:** pause a source after two hard bounces or a source-level bounce rate above 5%; keep the global target below 3%.
8. **Retry rule:** after any connector error, search Sent by thread/recipient/subject before resending.
9. **Count only buyer outcomes:** human need, qualified discovery, meeting booked/held, proposal, and paid scope. Auto replies, service desks, relationship-only replies, and generic networking are excluded.
10. **Minimum evidence before calling a winner:** at least 15 delivered companies per variant within the same segment, with clean route and qualification data.

## Next valid test

Run a clean company-level test inside one homogeneous segment only after enough qualified routes exist:

- **A:** profit / portfolio context → executive operating gap → relevant Joyce proof → one scoped hypothesis → 30-minute CTA.
- **B:** fresh product signal → one operating tension → relevant Joyce proof → one scoped hypothesis → 30-minute CTA.

Primary metric: qualified meeting rate. Secondary metrics: human need reply rate and paid diagnostic / proposal rate. Bounce and STOP violations are guardrails, not conversion outcomes.

## Bottom line

This week produced learning about list quality and control failures, not a valid copy winner. The next gain comes from expanding and validating the company map, then routing to real budget owners. Copy optimization should resume only after the qualified, reachable denominator is large enough.

---

## 2026-09-26 Execution Correction

The retrospective A/B result remains invalid, but the execution rule has been corrected.

### Root-cause correction
The previous Profit-first implementation accidentally used the **RMB 1M-class Sales Qualification standard as a pre-send gate**. For private mid-market companies, exact profit, confirmed procurement budget and a fully verified operating gap are often not public before first contact. That implementation converted a quality-control rule into a funnel freeze.

From 2026-09-26, the canonical funnel separates:
- **Outreach Eligible:** principal-side, own IP, core category, correct company scale, payment capacity at least Strongly Inferred, evidence-based why-now / missing-corner hypothesis, STOP clear.
- **Contact Ready:** legitimate unsuppressed executive/business route exists.
- **Sales Qualified:** after reply/discovery, confirm economics/budget, real purchasable gap, decision-maker and timing.

Exact private-company profit is no longer required for first touch when strong current operating evidence exists. The RMB 30M+ annual-profit / equivalent cash-generation standard remains the qualification standard for the RMB 1M-class pipeline.

### Target-profile correction
High revenue or famous companies are not automatically good targets. Companies that already have mature global publishing/operations are downgraded unless a specific external missing-corner is evidenced.

Priority sourcing now looks for mid-market / vertical-leader Chinese principal-side companies with observable transition signals such as:
- building overseas publishing / operations / UA / LiveOps teams;
- moving from publisher-dependent to self-publishing;
- launching the first owned product overseas;
- opening a new overseas publishing entity;
- domestic strength with a current global-execution build-out.

### Next-cycle operating model
- Build reserve Outreach Eligible pool >= 2× the next send wave.
- Map 3–5 relevant executives/account; first wave normally contacts 1–2.
- Normal production target remains 50–100 qualified emails/day when enough clean routes exist.
- A/B randomization starts at Outreach Eligible + Contact Ready, not after post-reply Sales Qualification.
- Primary KPI: Meeting Rate; secondary: Positive/Need Reply Rate and Reply Rate.
- Guardrails: bounce <3%, STOP violations = 0, duplicate sends = 0.

No outreach was sent as part of this review/correction task.