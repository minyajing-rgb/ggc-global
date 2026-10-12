---
name: product-acceptance
description: Independently inspect every product page/state/feature/flow against full PRD, actual UI references and architecture; fix/retest before owner review and verify actual live versions after authorized release.
metadata:
  standard_version: 1.0.0
---
Read product-definition and complete approved inputs. Bind evidence to exact commit/build/environment/URL/browser/device/viewport/locale. ALL concrete pages, nested nodes, tabs/modals and required states are the denominator. PASS/FAIL/BLOCKED/NA_WITH_REASON; untested cannot pass.
Open actual desktop/mobile screenshots against mockups: inspect layout/hierarchy/spacing/type/color/contrast/owned images/controls/readability/clipping/overlap/zoom/focus/reduced motion. DOM-only checks and builder self-report are not visual acceptance. Exercise every CTA and actual success/error/empty/loading/timeout/permission/cancel/back/refresh/deeplink/storage-denied/repeated-action result. Safely verify applicable auth/RLS/data/API/model/forms/payment; no unauthorized charge/send/data exposure or weakened permissions.
Maintain defects with severity/reproduction/expected/actual/evidence/fixing commit and RETEST. Review real visitor value and architecture/privacy/language/SEO/performance. Fix and rerun regressions. No internally accepted verdict with incomplete coverage, uninspected UI, open P0/P1 or unaccepted P2.
Separate implemented, preview-tested, internally accepted, owner-reviewed, deployed and live-verified. After authorized release inspect actual live version/hash, all pages and critical flows; preview proof is not live proof. Preserve existing site where requested. No repeated backup diversion or asking owner repeatedly to request review. Deliver self-checked candidate only; unfinished remains NOT_READY.
Full standard/templates: minyajing-rgb/GGC-AI-Spirituality-Research @ b50cc78567641341419c45a5759811b70f9d0456, .agents/skills/product-acceptance/SKILL.md and skills/product-delivery/. Repository entry installation is not global runtime activation.
