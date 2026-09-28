---
name: ggc-validate-paid-demand
description: Validate real willingness to pay before GGC approves, builds, launches, or scales a product. Use for new product ideas, MVPs, AI tools, services, game concepts, preorders, paid betas, pricing tests, landing-page tests, product approval reviews, release decisions, and requests to decide whether to advance, iterate, or stop. Require payments, deposits, card-backed trials, paid pilots, or budget-backed commitments; do not treat praise, likes, comments, surveys, or waitlists as proof of demand.
---

# GGC Paid-Demand Gate

## Purpose

Prevent GGC from investing substantial time or money in products that people praise but will not buy. Design the smallest honest transaction test, collect behavioral evidence, and issue one decision: `ADVANCE`, `ITERATE`, or `PARK`.

Treat this skill as a gate, not a brainstorming exercise. Validate the buyer, problem, offer, price, and purchase action before recommending a full build or public release.

## Operating Rule

Use this sequence:

1. Support current paying customers first when an urgent payment, access, or retention issue exists.
2. Choose one product or experiment as the day's primary project.
3. Put a real price and a purchase-capable action in front of a defined buyer.
4. Deliver manually or with a concierge workflow before automating.
5. Build only what paid evidence says is necessary.
6. Release publicly only after delivery and repeat-use evidence.
7. Scale only after retention, contribution margin, and support capacity are acceptable.

Do not recommend parallel product builds merely because several ideas appear promising.

## Classify The Evidence

Read [references/paid-demand-gates.md](references/paid-demand-gates.md) before designing or judging a test.

Use the evidence ladder strictly:

- `L0 Attention`: impressions, views, visits.
- `L1 Curiosity`: likes, comments, survey interest, waitlist signups.
- `L2 Purchase motion`: pricing-page visits, quote requests, checkout starts, qualified buying conversations.
- `L3 Commercial commitment`: payment, deposit, card-backed paid trial, paid pilot, or signed budget-backed commitment.
- `L4 Delivered value`: the buyer uses the product and accepts the promised outcome.
- `L5 Repeat economics`: repeat use or payment with workable acquisition, delivery, refund, and support costs.

Allow `L1` or `L2` evidence to justify another message or price test. Require `L3` evidence before substantial development. Require `L4` before broad public release and `L5` before scale.

## Build The Paid Demand Brief

Before creating assets, state:

- Product and mode: `consumer`, `saas`, `b2b`, or `game`.
- One primary buyer, including purchasing authority.
- Painful job or desired result in the buyer's words.
- Current alternative and why changing now matters.
- Narrow paid offer and explicit price.
- Delivery promise, exclusions, refund terms, and fulfillment date.
- Strongest feasible commitment action.
- Reach source and why it contains qualified buyers.
- Budget cap, time box, pass threshold, iteration threshold, and kill threshold.
- Named owner and decision date.

If the user omits thresholds, propose conservative defaults from the reference. Label them as defaults, not universal market benchmarks.

## Design The Smallest Honest Test

Create only what is required to ask for money or budget commitment:

- One focused landing page or direct sales message.
- One specific problem, outcome, buyer, offer, price, and CTA.
- A working checkout, deposit link, paid-pilot agreement, or budget-backed commitment route.
- Manual fulfillment plan that can serve early buyers without building the full product.
- Instrumentation for qualified reach, CTA action, checkout, payment, refund, delivery, and repeat use.

Do not use a disabled purchase button, fake scarcity, hidden price, fabricated testimonials, or a waitlist presented as sales proof. Disclose when the product is a preorder, prototype, concierge service, or paid beta.

## Adapt The Test By Mode

### Consumer or SaaS

Test a clear price with working checkout. Prefer a paid preorder, paid trial, founder plan, or concierge version. Count payments and refunds, not merely emails.

### High-Ticket B2B

Contact qualified decision-makers around a live trigger. Ask for a paid diagnostic, paid pilot, deposit, or signed commitment that names budget, scope, owner, and timing. A friendly letter with no budget or authority is not `L3`.

### Game or Entertainment Product

Test the promise with concept assets and a paid founder pack, refundable deposit, paid beta, or budget-backed publisher/platform commitment. Do not approve full production from clicks or creative-test performance alone. Combine commercial commitment with playable-prototype or delivery evidence before expanding production.

## Keep An Evidence Ledger

Record for every experiment:

- Date, variant, audience, source, spend, and reach quality.
- Exact promise, price, CTA, and objection handling.
- Counts at every evidence level.
- Payment amount, refunds, cancellations, delivery status, and repeat behavior.
- Direct buyer language and top objections.
- What changed from the previous variant.

Do not merge audiences, offers, or prices into a single conversion rate when they differ materially.

## Make The Gate Decision

Run [scripts/score_demand_gate.py](scripts/score_demand_gate.py) when structured counts are available. Treat its result as a reproducible default, then check evidence quality and fulfillment risk before issuing the final decision.

### ADVANCE

Advance only to the next smallest stage. State the paid evidence, what is now de-risked, what remains unknown, the next deliverable, budget cap, owner, and next gate date.

### ITERATE

Change exactly one primary variable: buyer, problem, promise, proof, price, channel, or CTA. Preserve a comparable control when possible. Specify the next test and its stopping rule.

### PARK

Stop active work and preserve the evidence. Park by default when any reference kill condition is met, including three materially different tests with no `L3` commitment. Do not disguise a parked idea as a continuing research project.

Joyce may override a gate explicitly. Record the rationale, maximum budget, deadline, and automatic kill condition; never silently override it.

## Deliverables

Return these artifacts in concise form:

1. `Paid Demand Brief`
2. `Test Asset`: landing-page or direct-sales copy with price and CTA
3. `Acquisition Plan`: qualified source, budget, sample, and timing
4. `Evidence Ledger`
5. `Gate Decision Memo`: `ADVANCE`, `ITERATE`, or `PARK`
6. `Next Action`: one experiment, one owner, one budget cap, one decision date

When asked only for a decision, still show the evidence level and the missing proof. When asked to build a full product before `L3`, propose the paid-demand test first unless the user explicitly records an override.
