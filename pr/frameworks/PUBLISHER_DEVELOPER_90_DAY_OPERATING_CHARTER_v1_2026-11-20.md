# The First 90 Days After a Publishing Deal
## A practical operating charter for game developers, publishers and global LiveOps teams

**Joyce | GGC Games** · 20 November 2026  
**Type:** Original public practitioner framework and reusable working template.  
**Scope:** Mobile, PC and web game publishing partnerships; adapt for product stage, jurisdiction, platform, genre and deal structure.  
**Evidence boundary:** This is an operating framework, not legal advice, a model publishing agreement, a report of confidential deals, or evidence of independently measured outcomes. References to possible thresholds are **questions**, not one-size-fits-all KPI promises.

> A publishing contract transfers commercial rights and obligations. It does not automatically transfer a working operating system.

When game studios and publishers work across markets, the first handoff often appears obvious: the developer supplies a build, the publisher acquires players, and both parties report the business results. The hidden failure is that each team may have a different definition of "ready", "user", "revenue" and "success", and no agreed person can make the integrated go/no-go decision.

This public charter is a discussion aid for **business leaders before signing** and **joint teams during the first 90 days**. It makes five things explicit: *what was promised, what can actually be played, what the numbers mean, who can spend money, and who can stop*. It complements the [Handoff Gap operator essay](../articles/2026-11-19-the-handoff-gap-global-game-publishing.md).

### 1. The seven responsibilities that cannot be delegated to a slide deck

| Workstream | Required evidence | Accountable owner to name in the agreement or work plan | Example decision |
|---|---|---|---|
| **Product & build** | Versioned public build, known defects, store or distribution requirements, reproducible core loop | Development product owner | Is this a testable release candidate? |
| **First-play** | Real entrance path from ad/store URL; load/onboarding/first meaningful action on target device and locale | Joint QA + publishing product lead; **one named final owner** | May traffic enter this build? |
| **Rights, safety & compliance** | Chain of title, licensed creative and game IP, use of AI media, privacy/age disclosures, local platform requirements | Rights/compliance owner jointly approved | Which creative or market is blocked? |
| **Data & attribution** | Versioned event dictionary, deduplicated identifiers, acquisition source, cohort windows, first-party vs modeled status | Analytics lead with joint sign-off | Is this claim comparable across markets? |
| **Economy, price & LiveOps** | Offers, sinks/sources, event calendar, pricing and local currency, product changes and rollback procedure | Product/economy owner; publishing counterpart | Is the proposed promotion safe for the economy? |
| **Commercial & P&L** | Actual spend, stores/fees, localization/ops cost, royalty/revenue share accounting, refund and chargeback assumptions | Commercial owner with budget authority | Can we finance the next test? |
| **Governance & escalation** | Decision-rights matrix, communication SLA, dispute path, test cap, stop triggers | One executive decision owner from each party | Who makes the final scale, pause or stop call? |

A party may contribute work without being accountable for the integrated business decision. Assign named *roles* before assigning tasks. Avoid a design in which development is accountable for a marketing return it cannot control, or the publisher is accountable for technical failures it cannot remedy.

### 2. The three independent receipts

A release review should keep three evidence receipts separate:

1. **Build receipt:** exact code and asset version, environment, test execution, known defects, region/platform and reproducible test path. A passed build is **not** a successful first play.
2. **First-play receipt:** what a real first-time person actually encounters from the public acquisition/store URL, on the intended device and locale, with failures, permissions, logins and offers recorded. A demo run by the developer is **not** a sampled user cohort.
3. **Audience-and-economics receipt:** defined and deduplicated activated users, first meaningful actions, D1/D7/D30 retention by acquisition cohort, payer conversion and revenue, attributable marketing costs, refunds, and costs required to operate. Platform ad events or third-party estimated revenues are **not** automatically first-party retained users, LTV or realized profit.

A missing receipt cannot be filled in by repeating the strongest figure from another receipt.

### 3. The operating calendar

| Time window | The business question | Minimum joint action | Deliverable at review |
|---|---|---|---|
| **Before Day 0** | Do both parties mean the same thing by "launch-ready"? | Confirm rights, roles, agreed market hypothesis, release candidate, event dictionary, test cap, and risk stop conditions | One-page **market readiness decision** with unresolved blocks |
| **Days 1–14** | Can the intended player reach the promised game, play and be measured? | Independent first-play checks; QA fixes; event instrumentation reconciliation; low-risk limited traffic subject to agreed controls | First-play trace, issue log, acquisition and activation denominator |
| **Days 15–30** | Is there early evidence worth learning from? | Inspect comparable cohorts, failure reasons, qualitative feedback, payer events, creative-to-product fidelity; review data quality first | Defined early cohort review, uncertainty register, next experiment |
| **Days 31–60** | Are operations and unit economics feasible for the team and market? | Compare product revisions and content cadence with actual operating cost; decide whether marketing/UA expansion is justified | Contribution-economics worksheet, release/LiveOps plan, approved test budget |
| **Days 61–90** | Should the parties scale, revise, renegotiate, hold or stop? | Review cohorts against *pre-agreed* thresholds, operating risks, contract obligations and market fit; record dissent or unresolved evidence | Joint **scale / revise / hold / stop decision memo** and ownership for next cycle |

The calendar is not an instruction to buy ads on Day 1 or to scale on Day 61. A delayed public build, age-compliance issue, rights dispute or missing event instrumentation may require holding the investment until the evidence is reliable.

### 4. Make the economics comparable

A report that mixes country, store, acquisition and player-age cohorts is not sufficient to make a budget decision. At a minimum, define:

| Metric | What must be defined before using it in a decision |
|---|---|
| Activation | Unique qualifying user, denominator, first meaningful action, exclusion of repeats/test accounts |
| D1 / D7 / D30 retention | Cohort start, timezone, eligible users, return action, market and platform |
| CPI / CAC | Attributed spend, window, ad network, install vs new activated user |
| Payer conversion | Eligible cohort, first payment vs repeat, gross vs net, refunded/fraudulent transactions |
| ARPDAU / ARPPU | Currency, payment basis, platform/processing fees, definitions of active and paying users |
| ROAS / payback | User-acquisition cohort, revenue realization basis, attribution, costs excluded and cutoff |
| Contribution margin | Net revenue minus genuinely variable distribution, payment, traffic, operations and content costs |
| Revenue share / CPS | Contractual base, deductions, tax treatment, period, chargebacks, audit and settlement rights |

**Critical warning:** monthly third-party estimated revenue divided by current-month downloads is not acquisition-cohort lifetime value. Historic live-game revenue may come from older cohorts.

### 5. The market decision record — copy and complete

```yaml
product: "[game or anonymized project ID]"
market: "[country / platform / channel]"
build_version: "[commit, release, store build, date]"
decision_date: "YYYY-MM-DD"
joint_owners:
  developer_product: "[role]"
  publisher_operating: "[role]"
  budget_approver: "[role]"
  data_validation: "[role]"
decision: "LIMITED_TEST | IMPROVE | SCALE | HOLD | STOP"
observed_evidence:
  - "Public build first-play trace and limitations"
  - "Cohort/report references with dictionary version"
  - "Actual approved spend and settlement basis"
assumptions:
  - "Market thesis, with explicit source"
modeled_estimates:
  - "Forecast, method, range, owner"
unknowns_or_blocks:
  - "Rights, safety, attribution or payment issues"
limits:
  approved_test_spend: "[amount, currency, period, signatory]"
  cancellation_or_stop_triggers: "[trigger]"
next_owner_and_checkpoint: "[role, date/condition]"
```

No team should label this document "green" merely because an initiative has a launch date. If the evidence is not yet collected, label it **unmeasured**; if it is modeled, label it **modeled**; if consent or rights prevent publication, label it **blocked**.

### 6. Who approves changes?

Before launch, write down the minimum change-control rules for:

- **Creative promise:** which advertising, trailer or localized wording can be published only after verified alignment with real gameplay?
- **LiveOps/economy:** who may deploy a new event, pricing tier, monetization offer or rewards schedule; who can roll it back?
- **Data definitions:** who can change an event dictionary or attribution window after a campaign begins?
- **UA budgets:** who has the authority to increase spend, against what cohort evidence and with which stop limits?
- **Cross-company escalation:** who handles a build blocker, data-quality incident, rights dispute, player safety issue or missed payment settlement?
- **Revenue and IP:** what happens if a title changes owner, store, territory, content rights or monetization mechanism? Refer legal terms to qualified counsel.

The purpose of a collaboration agreement is not to eliminate uncertainty. It is to prevent uncertain facts from silently becoming financial commitments.

### 7. Why this becomes more important with AI

AI-assisted production can accelerate concept art, localization versions, trailers, prototype builds, analytic summaries and test matrices. It does not verify that rights are cleared, players are retained, sales have settled, or market risk has been accepted by a human decision owner.

The most useful AI operating workflow is not "automatic approval". It is a traceable evidence ladder: **prepare → compare → flag exceptions → human judgment → version and audit**. When output generation becomes cheap, the scarce resource is the team's time to make a defensible cross-functional decision.

### How to use this public charter

A founder can use this as a **pre-signing conversation starter**. A developer–publisher pair can turn it into a 60-minute operating kickoff. An investor or executive team can use it to assess whether a promising game launch has evidence and a decision owner, rather than only a polished deck.

The one-page outcome should be an explicit investment decision with remaining uncertainties, not a new slide appendix. In professional engagements, project-specific deal terms and rights require independent review.

---

**Author:** Joyce | Founder, GGC Games; global games product and commercial operator; author of *Game Operations and Global Expansion* (China Machine Press, 2024 Chinese-language edition, under 艾小米; separate English Kindle edition released in November 2026). Previously held product/commercial operating responsibility at Zynga and regional cross-studio game operating roles at Gameloft. 

**Related source:** [The Handoff Gap](../articles/2026-11-19-the-handoff-gap-global-game-publishing.md) · [Global speaker & editorial portfolio](../authority-engine/JOYCE_GLOBAL_SPEAKER_AND_MEDIA_PORTFOLIO_2026-11-19.md) · [Public evidence map](../authority-engine/EVIDENCE_MAP.md)

**Rights note:** © Joyce / GGC Games 2026. Publicly readable as an original practitioner framework; no blanket license or third-party redistribution rights granted. Company-sensitive cases, source documents, live commercial terms and user-level analytics are excluded. 
