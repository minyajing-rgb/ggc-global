---
name: product-acceptance
description: Automatically inspect all product pages/functions/states/flows and actual UI; independently fix/retest before owner review and verify the actual live version after authorized release.
metadata:
  standard_version: 1.2.0
  canonical_acceptance_blob: 6e5ef36852f09862d175ba74047005e7e99cd1ea
  distribution: complete-local-rules
---
# Independent product acceptance

Read product-definition and the complete approved PRD, actual mockups, all flows, architecture, INPUT_LEDGER and page matrix. Trigger automatically after product implementation and authorized release; the owner does not need to request review again. Builder completion labels and send receipts are evidence to examine, not verdicts.

## Exact target and scope
Freeze repo/app/commit/build/URL/environment/time/browser/device/locale/width. Use a temporary fixture only when needed to isolate a moving writer; reuse recovery instead of repeatedly making backups. Compare all concrete pages/dynamic instances/nested branches/tabs/modals/controls/states against actual router and visible links. The denominator is every required page × state × locale × viewport, including default. Record covered/required, not a headline count alone. PASS/FAIL/BLOCKED/NA_WITH_REASON; untested is BLOCKED. A narrower matrix or nonapplicable condition needs explicit design justification, not retroactive removal of failures.

## One PAGE_REVIEW_CARD per page
Record requirement/flow/mockup IDs, tested version, exact actions, expected/actual, method, evidence and defect IDs. Open actual desktop/mobile pixels beside approved references: hierarchy, spacing, white space, typography, contrast, original images and crops/readability, clipping/overlap, long copy, sticky bars, unique accessible names, keyboard order, modal focus trap/return, zoom, touch and reduced motion. Inspect full truthful copy, sources, product status, professional facts, contacts and translated body/errors/legal/accessibility labels. Press every control and observe real destination, state change and side effect. Check visitor value, architecture, console/network/private access, privacy, metadata and measured performance.

Capturing screenshots, DOM assertions, HTTP 200 and Builder claims are not visual acceptance. Each page/locale/viewport needs actual screenshot plus corresponding approved or clearly proposed reference, reviewer comparison and findings. Missing essential visuals or reference inspection remains BLOCKED. Native originals, Canva exports, previews, optimized derivatives, app import and live rendering are separate facts; do not call a thumbnail an original or a located file an imported asset. Browser emulation is not physical-device QA. External review agents can establish only the pages/origin/viewports they actually inspected.

## Function and flow checks
Exercise happy/alternative/failure paths: empty/invalid/long input, loading/success/no-results/errors/timeouts/offline/retry, storage/permission denial, guest/auth, cancel/back/refresh/deep-link/repeated actions, filters, dialogs and timer cleanup. Observe actual state/network, not a success toast. Test in-scope auth/RLS/persistence/deletion/model grounding/forms/receipts/payments/webhooks/cancel/restore with explicitly authorized safe sandbox data. No unauthorized charges, messages, private writes, weakened permissions or credential exposure. Keep private research, customer data and personal records out of public bundles and evidence. Missing required service/credential behavior stays BLOCKED.

## Defect closure and gates
DEFECTS.json records severity/page/state/requirement, reproduction, expected/actual, evidence, owner, fixing commit and identical-case RETEST plus affected-neighbour regression. P0: security/data loss/catastrophic failure. P1: missing/broken required feature/path/page, misleading success or missing essential visual evidence. P2: nonblocking quality issue. Untested fixes remain open; lower-priority exceptions need explicit owner disposition.
Gate A: definition inputs inspected and complete contract.
Gate B IMPLEMENTED: required implementation exists and builds; unavailable services are not complete.
Gate C INTERNALLY_ACCEPTED: full required coverage, actual independent pixel inspection, zero open P0/P1, approved P2 disposition and evidence tied to the exact target.
Gate D LIVE_VERIFIED: authorized release and actual live verification.
Otherwise report NOT_READY with exact gaps; no silent waiver or unreviewed finished handoff.

## Fail-closed evidence
Use canonical skills/product-delivery/scripts/check-evidence-v2.mjs and tests when installed. Validate required inputs, target/build, complete matrix cases, page-level visual/reference records, flows, source/evidence byte hashes and defect retests. Missing checker/evidence stays explicit. Legacy check-gates.mjs and a global visual-reviewed flag cannot substitute. Evidence-complete still requires reviewer signoff; validators cannot prove a human/agent actually examined pixels. Never manufacture PASS/signoff entries to satisfy a schema.
Reuse evidence only when a recorded diff proves the page AND affected shared data/styles/translations unchanged; unknown mappings fail closed. Label logic/browser/server-render/visual methods separately. For assertions contradicted by a separately authorized new feature or proper name, preserve initial failures, inspect scope evidence, narrowly correct the assertion and rerun; report test-contract reconciliation, not imaginary product fixes.

## Actual release review
Read actual domain in a browser, final redirects/rendered body/title/robots/canonical/lang/OG and script/asset hashes, compared with reviewed build. SPA HTTP 200 or raw old HTML can misrepresent the rendered page. A preview and rebuilt production artifact need separate checks. Missing candidate is NOT_DEPLOYED; a different live version is a mismatch, not assumed approval. After authorized release, verify required live routes/locales/critical flows, console/network, auth boundaries and recovery context.
Do not publish/revert/change DNS or another operator's hosting lane just to satisfy a test. Preserve confirmed business content and professional facts. Do not claim CRM/subscription/payment integrations exist without real evidence.

Deliver only an internally checked candidate as accepted, with actual preview, changes, coverage, defect disposition, exact build/commit and release proof where verified. Intermediate updates may report real work and blockers. Preserve existing AGENTS.md and project-specific constraints. Read back paired local skill versions/hashes; COPIED, ACTIVATION_TESTED and AUTOMATION_RUNNING are different states. Repository files alone do not configure models, activate global ChatGPT memory or start unattended execution.
