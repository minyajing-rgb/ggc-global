---
name: ggc-ai-native-game-build-to-revenue
description: >
  GGC reusable development-to-commercialization reference skill for AI-assisted game projects.
  Use as a practical reference when scoping a new game, turning an idea into an MVP, planning
  solo/small-team development, preparing App Store/Google Play launch, setting up IAP, collecting
  player feedback, designing community launch, deciding what to iterate, or moving a playable
  product toward repeatable revenue. The patterns in this skill are reference frameworks rather
  than mandatory gates; adapt them to project stage, genre, budget, team, platform, and commercial goal.
version: 1.0
---

# GGC AI-Native Game Build-to-Revenue Skill

> **Usage note:** This is a reference framework, not a hard rulebook. Different game genres, team sizes, budgets, platforms, lifecycle stages, and strategic goals may require different sequencing, thresholds, or artifacts. Use judgment; keep what improves decision quality and discard what does not.


## 0. Purpose

Turn AI-assisted game development into a reusable set of commercial-development references.

This skill is not a mandatory production process and is not "use AI to generate a full game."
It provides patterns that may help a project move from a narrow product hypothesis to:
- a playable build,
- a store-ready release,
- real players,
- first payment,
- structured criticism,
- repeatable monetization,
- and only then broader scale.

The user-provided Harpagia / Ken Law case is the source case for the first version of this skill.
Case figures are treated as anecdotal self-reported evidence unless independently verified later.
The skill preserves useful operating lessons as references rather than treating the case's revenue numbers or workflow as universal rules.

---

# 1. Reference Principles

## 1.1 Prefer a first scope that is small enough to finish

The first version should be deliberately narrow:
- one core gameplay loop;
- at most three essential screens for the smallest prototype;
- one progression mechanism;
- one save-state path;
- one reason to return the next day.

Delete:
- secondary modes;
- social systems not required for the core loop;
- large content trees;
- complex live events;
- unnecessary currencies;
- premature polish that does not affect play, payment, or retention evidence.

The first milestone is not "feature complete."
It is **finished enough that a real player can play, understand, return, and potentially pay.**

## 1.2 AI is a production multiplier; product judgment remains human-owned

AI may assist with:
- ideation;
- code generation and debugging;
- UI implementation;
- asset iteration;
- icon / copy iteration;
- build scripts;
- test generation;
- analytics query support;
- store copy;
- review clustering.

Human owner must still decide:
- what game to make;
- what to remove;
- whether the game is understandable;
- whether the loop is fun enough to continue;
- whether monetization is acceptable;
- whether the build is safe to release;
- what player criticism should and should not change.

Do not confuse "one person + AI" with "everything generated from zero."
Use existing engines, SDKs, asset stores, freelancers, APIs, and platform services when faster and economically rational.

## 1.3 Prefer development tasks that can be manually verified

Do not ask Codex/Cursor/AI coding tools to "build the whole game."

Break work into independent tasks where each task states:
1. files/components to create or change;
2. expected visible result on device/browser;
3. manual test steps;
4. expected data/state change;
5. likely failure modes;
6. rollback or acceptance condition.

Rule:
**one task -> run -> manually verify -> record -> next task.**

## 1.4 Consider shipping before the game feels fully finished

A rough live product with real players creates more decision value than an internal polished prototype with no users.

Release when the smallest honest version can:
- run reliably;
- explain the core loop;
- save progress;
- complete the basic gameplay loop;
- collect analytics;
- support the intended purchase flow if monetization is being tested;
- comply with store/platform requirements.

Do not delay release merely to remove all criticism.

## 1.5 Treat real payment as stronger evidence than praise

Likes, comments, waitlists and compliments are weak evidence.

Strong evidence includes:
- completed IAP;
- paid beta;
- founder pack;
- deposit;
- subscription payment;
- repeat purchase;
- budget-backed publisher/platform commitment.

For pre-build demand validation, use the existing:
`skills/ggc-validate-paid-demand/SKILL.md`.

For a live game, treat first payment as proof that at least one player perceived paid value.
It does not prove scale, retention, or profitability.

## 1.6 Player criticism can be operating input

Collect criticism after release and classify it before changing the roadmap.

Default buckets:
- cannot understand the game;
- control / usability friction;
- insufficient content;
- monetization concern;
- technical defect;
- subjective preference.

For each feedback cycle:
- preserve original quote;
- count recurrence;
- identify affected stage/player segment;
- choose no more than three priority changes for the next small release;
- define how each change will be tested.

Do not turn every complaint into a feature request.

## 1.7 Treat distribution as part of product development when useful

A finished build with no distribution is not a completed commercial experiment.

Use channels where the target player already gathers:
- Reddit / Discord / genre forums;
- creator communities;
- short-form video;
- app-store search / ASO;
- relevant social communities;
- existing audience / owned community;
- publisher/platform featuring opportunities.

Community post minimum:
- real gameplay screenshot or video;
- one-sentence game loop;
- exactly what can be played for free;
- one specific question for players;
- direct playable/store link when appropriate.

Do not pretend rough work is polished.
Use the roughness as an invitation for specific feedback, not fake hype.

## 1.8 Consider keeping the fixed-cost base low until evidence supports more spend

Before repeatable revenue:
- prefer small team / solo-compatible architecture;
- buy proven assets when cheaper than producing from zero;
- outsource isolated art/video/screenshot work when it saves critical-path time;
- keep recurring SaaS/infra costs visible;
- do not add headcount because the roadmap looks large.

Scale cost only after evidence shows the bottleneck is production capacity rather than product-market/commercial fit.

---

# 2. Reference Build-to-Revenue Stages

## Reference Stage 0 — Product Thesis

Required:
- target player;
- one-sentence fantasy/promise;
- core action;
- progression loop;
- reason to return;
- monetization hypothesis;
- target platform;
- what is explicitly cut from v1.

Output:
`PRODUCT_THESIS.md`

Decision:
`BUILD PROTOTYPE` / `RE-SCOPE` / `PARK`

---

## Reference Stage 1 — Playable Core

Required:
- one working core loop;
- save/load;
- basic progression;
- no blocker in first session;
- basic event logging;
- manual test checklist.

Minimum question:
**Can a new player understand what to do, complete the loop, and want one more cycle?**

Output:
`PLAYABLE_ACCEPTANCE.md`

Do not build large content systems before this passes.

---

## Reference Stage 2 — Commercial Instrumentation

Required before serious monetization testing:
- analytics events;
- payer funnel;
- product/SKU definitions;
- price table;
- currency/resource ledger;
- purchase success/failure logging;
- refund/error handling;
- payer segmentation fields where relevant.

For IAP games, track at minimum:
- store impression;
- offer open;
- purchase start;
- purchase success;
- purchase failure;
- SKU;
- price/currency;
- player progression state at purchase.

Output:
`MONETIZATION_SPEC.md`

---

## Reference Stage 3 — Store / Release Readiness

For App Store / Google Play or equivalent:
- developer account;
- installable production candidate;
- app name;
- icon;
- screenshots/video;
- store description;
- privacy/data disclosures;
- IAP/subscription configuration;
- test account/build;
- platform review checklist;
- crash/blocker check;
- analytics verification.

Use current official platform documentation when performing an actual submission.
Do not rely on old checklist details when platform policy may have changed.

Output:
`RELEASE_CHECKLIST.md`

---

## Reference Stage 4 — Real Player / Real Payment

Required evidence:
- actual external players;
- session and progression data;
- raw player comments;
- at least one commercial signal appropriate to the stage;
- explicit top friction points.

Commercial evidence strength:
1. store visit / install;
2. meaningful play;
3. offer interaction;
4. first purchase;
5. repeat purchase / repeat payer;
6. workable contribution economics.

Output:
`EARLY_EVIDENCE_LEDGER.md`

Do not call the project commercially validated because of downloads alone.

---

## Reference Stage 5 — Iteration Loop

After every meaningful release:
1. collect reviews/support/community feedback;
2. cluster problems;
3. connect qualitative feedback to behavioral data;
4. select top three changes;
5. ship a small update;
6. measure the before/after effect;
7. record the decision.

Output:
`ITERATION_LOG.md`

Rule:
**criticism -> classification -> priority -> change -> measurement**

---

## Reference Stage 6 — Distribution Repeatability

Before paid scale, prove at least one repeatable acquisition path or one economically justified channel.

Track per channel:
- reach;
- click/store visit;
- install;
- activated player;
- retained player;
- payer;
- revenue;
- direct cost;
- content/production time.

Separate:
- organic community;
- creator/KOL;
- store discovery;
- referral;
- paid UA;
- publisher/platform traffic.

Output:
`CHANNEL_LEDGER.md`

Do not mix all traffic into one blended conversion rate when channel quality differs.

---

## Reference Stage 7 — Scale

Scale only after the project has evidence for:
- playable quality;
- retention/return behavior appropriate to the game;
- monetization behavior;
- a stable purchase path;
- support/bug capacity;
- at least one functioning acquisition source;
- contribution economics or a deliberate investment thesis.

Then decide:
- increase content production;
- increase UA;
- add live operations;
- hire;
- expand market;
- localize;
- add deeper monetization;
- add platform/partner distribution.

Output:
`SCALE_DECISION.md`

---

# 3. Small-Team Development Workflow

Use this default sequence:

**Idea**
-> shrink to one loop
-> clickable/playable prototype
-> save/progression
-> analytics
-> monetization stub
-> device/browser QA
-> closed external test
-> store-ready build
-> public release
-> player feedback
-> payment evidence
-> small update
-> repeat
-> scale only after evidence.

For each phase, keep one named owner and one acceptance test.

---

# 4. Commercialization Minimum

Every commercial game project must answer these questions before launch:

## Player Value
- What is fun without payment?
- Why does the player return tomorrow?
- What becomes more desirable after progression?

## Purchase Value
- What exactly is being sold?
- Is the purchase convenience, acceleration, content, status, collection, power, subscription, ad removal, or access?
- Why is this offer relevant at this exact player state?

## Price / SKU
- What are the first 3–5 SKUs?
- What is the entry-price purchase?
- What is the repeatable mid-tier purchase?
- What is the high-intent/high-value purchase?
- Are prices consistent with the game's economy?

## Timing
- What event/state triggers the offer?
- Does the player understand value before being asked to pay?
- Is the first purchase path short and reliable?

## Measurement
- offer view rate;
- purchase-start rate;
- purchase completion;
- payer conversion;
- ARPPU / revenue by SKU;
- repeat payer behavior;
- refund/failure;
- revenue by progression stage.

Do not add more monetization surfaces when the current one is not measured.

---

# 5. Community Launch SOP

When posting to a player community:

1. Choose a community with genre-fit players.
2. Use real gameplay media.
3. Explain the game in one sentence.
4. State what is free and what is paid.
5. Admit the current stage honestly.
6. Ask one concrete question.
7. Stay in the thread and answer.
8. Capture every useful comment into the feedback ledger.
9. Ship a visible update.
10. Return later only when there is meaningful change.

Never treat community posting as a one-off PR event.
It is a feedback + distribution loop.

---

# 6. AI Tool Role Split

Default GGC pattern:

## ChatGPT / reasoning model
- concept reduction;
- system design;
- economy / monetization thinking;
- review synthesis;
- store copy drafts;
- qualitative feedback clustering.

## Codex / coding agent
- repository inspection;
- implementation;
- debugging;
- tests;
- instrumentation;
- build/release scripts;
- data transforms;
- FFmpeg / creative automation where relevant.

## Engine / framework
Choose based on product:
- web/H5;
- React Native;
- Unity;
- native;
- other fit-for-purpose stack.

## Backend / analytics
Use managed services when they reduce operations burden:
- auth;
- save data;
- analytics;
- remote config;
- crash reporting;
- push;
- payment validation.

## Assets / freelancers
Buy/outsource non-differentiating production work when speed/cost is superior.

Rule:
**AI handles throughput; owner handles taste, product judgment and commercial decisions.**

---

# 7. Suggested Repository Artifacts

For future GGC game projects, consider maintaining:

```
/docs
  PRODUCT_THESIS.md
  PLAYABLE_ACCEPTANCE.md
  MONETIZATION_SPEC.md
  RELEASE_CHECKLIST.md
  EARLY_EVIDENCE_LEDGER.md
  ITERATION_LOG.md
  CHANNEL_LEDGER.md
  SCALE_DECISION.md
```

For very small prototypes, these may be sections in one `PROJECT_OPERATING_LOG.md`. Use only the stages and artifacts that add decision value for that project.

---

# 8. Reference Review Questions

At any checkpoint, answer:

1. What can the player do today?
2. What is the one core loop?
3. What did we remove?
4. What does the player understand in the first session?
5. Why return tomorrow?
6. What event creates purchase intent?
7. What has a real player actually paid for?
8. What are the top three repeated complaints?
9. What did the last update change in behavior?
10. Which acquisition source produced the best players?
11. What is the current bottleneck: product, content, monetization, distribution, or production capacity?
12. What evidence justifies the next unit of spend?

If these cannot be answered, do not hide the gap behind more feature development.

---

# 9. Suggested Decision Vocabulary

When useful, end a cycle with one primary decision:

- `SHIP` — release the current smallest viable build.
- `FIX` — correct a specific blocker before wider exposure.
- `ITERATE` — change up to three evidence-backed product/commercial items.
- `MONETIZE` — current engagement is strong enough to deepen purchase testing.
- `DISTRIBUTE` — product is ready for broader qualified player acquisition.
- `SCALE` — economics/retention/operations support larger spend.
- `PARK` — evidence does not justify more active investment.

State:
- evidence used;
- unknowns;
- next owner;
- maximum time/budget before the next gate;
- next decision date.

---

# 10. Source-Derived Prompt Patterns

## Scope Reduction

"Take this game idea and reduce it to a first version one person/small team can finish. Keep one core loop and no more than three essential screens. Define player action, feedback, saved progression, return reason, and what to delete."

## Development Task

"Break this build into no more than 10 independently testable tasks, ordered by 'first make it run, then add capability.' For each task list files/components, visible result, manual test, expected state/data change, and likely errors. Give only the first task until it is verified."

## Store Readiness

"Check this game's current App Store/Google Play submission readiness against current official platform requirements. Ask for evidence item by item and separate known requirements from items that must be confirmed in the current developer console."

## Review Clustering

"Classify these raw player comments into comprehension, usability, content, monetization, technical defects, and personal preference. Preserve quotes and counts. Recommend only three next-release changes and define how each will be tested."

## Community Post

"Write a direct player-community post using real gameplay, one-sentence loop, exact free content, current development stage, and one concrete feedback question. Do not use hype unsupported by the build."

---

# 11. Relationship to Other GGC Skills

Use together with:
- `ggc-validate-paid-demand` for pre-build or paid-demand gates;
- project/category-specific competitor research skills for category evidence;
- project-specific launch KPI and economy models;
- GGC creative/UA systems after product and monetization instrumentation exist.

This skill provides a **build -> release -> real-player -> payment -> iteration -> distribution -> scale** reference loop. Project owners may skip, reorder, combine, or override stages when the project context justifies it.
