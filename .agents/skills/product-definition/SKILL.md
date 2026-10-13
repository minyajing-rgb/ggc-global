---
name: product-definition
description: Automatically define complete product/site/feature work before implementation: full PRD, inspected mockups, every flow, architecture and page/branch map.
metadata:
  standard_version: 1.2.0
  canonical_definition_blob: 13fed6c706d8124ca2da881c5852754afe1a288f
  distribution: complete-local-rules
---
# Product definition — mandatory initiation gate

Read actual repo/app, AGENTS.md and latest approved scope; preserve local business/product rules, confirmed visual identity, wording and professional facts. Pair automatically with product-acceptance. Do not ask the owner again to commission review.

First fill INPUT_LEDGER.md for FIVE inspected inputs: complete PRD; actual desktop/mobile mockup pixels for every approved screen; all user flows with decisions/failure/guest/cancel/back; information/component/service/data/auth/release architecture; concrete page/branch/state matrix compared to real router AND visible links. Record source/commit/hash/date, inspection method, findings, conflicts, approval and INSPECTED/BLOCKED. Filenames, summaries, thumbnails or code alone are not visual inspection. Proposed screens remain PROPOSED; missing inputs stay BLOCKED. Recover existing source manifests and actual files before declaring original artwork missing. No invented replacement or repeated request for known user facts.

Produce and read back inside the implementer workspace: PRD.md, PAGE_MATRIX.json, UI_SPEC.md plus actual references, USER_FLOWS.md, ARCHITECTURE.md, BUILD_REQUEST.md, TRACEABILITY.json. PRD includes problem/users/first value, measurable business/product acceptance, scope/non-goals, complete copy/locales, dependencies and failure behavior. Every concrete page/state needs a stable ID, route/parent, purpose, entry/exit, features/priority, required states, mockup/flow/requirement/acceptance IDs. Include every dynamic instance, tab, modal and branch; one reusable template is not a complete page inventory.

UI_SPEC must specify actual desktop/mobile layouts, spacing/type/color, authorized imagery and crops, copy and variants, loading/empty/error/success/disabled/focus/hover, keyboard/touch/zoom and responsive behavior. USER_FLOWS must include alternative and failed paths, deep links, refresh, cancel/undo, guest/auth and permissions. ARCHITECTURE covers routes/components, service/API contracts, data/persistence, identity/RLS, asynchronous state, external-product boundaries, privacy/security, analytics and release/recovery. For every feature specify inputs/validation, output/copy, transitions/storage/side effects, API/errors/permissions, undo/return and measurable tests. TRACEABILITY maps requirement → page/state → flow → component/API → test → evidence.

Establish the full page × required state × locale × viewport denominator before testing. Default is a required state. A justified narrower matrix or nonapplicable case must be explicit, including desktop equivalents of mobile-only controls. Never silently remove failed cases to improve the count. Full localization includes body copy, errors, accessibility labels and legal information, not only navigation. Keep the complete agreed scope; staged delivery is allowed but homepage-only reduction is not.

Separate public pages from administration, local storage from cloud accounts, hosting logs from business analytics, independent product payments from a portal link, and a keyword demo from actual model-backed behavior. Required missing assets/credentials/services remain BLOCKED unless explicitly excluded by the owner. No fabricated contacts, results, customers, model calls, CRM integrations, forms, subscription or payment success.

Respect the builder tool's prompt contract and use one writer per app/branch. Place the complete self-contained BUILD_REQUEST and references into the actual environment; record the send receipt, obtain final reply/status where supported and inspect the real diff/result independently. Accepted messages and stale BUILDER_RESULT files are not proof of completion. Never claim Codex/model settings were activated without a receipt. Reuse existing recovery; no repeated backup diversion. Preserve production, independent products, auth/data/domains/billing; do not touch hosting, publish settings or another owner's release lane without appropriate authorization.

Gate A requires the five inspected inputs, full traceable definition and explicit protected surfaces. Safe independent work may continue around named blockers. After implementation automatically run product-acceptance, fix/retest and only then hand a checked candidate to the owner. Missing essential visual evidence remains a gate, even when builds succeed.

Canonical rules/templates: minyajing-rgb/GGC-AI-Spirituality-Research/.agents/skills and skills/product-delivery. Strict full evidence checking uses scripts/check-evidence-v2.mjs with actual bytes and tests, not legacy check-gates.mjs or a global visual boolean. Missing required checker/evidence is explicit. A validator cannot prove actual pixel inspection. Preserve existing AGENTS.md; record local version/hash/commit and POINTER/COPIED/ACTIVATION_TESTED/AUTOMATION_RUNNING separately. Files alone do not install global ChatGPT memory or run unattended automation.
