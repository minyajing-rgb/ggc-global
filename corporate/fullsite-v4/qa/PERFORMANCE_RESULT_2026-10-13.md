# GGC PR11 — Product Review / Performance Result

2026-10-13. Source and build artifacts only; Codex retains production publishing, domain and live acceptance ownership.

## Exact changes and verification commits

- `afd2e850ff4beb27c2ca7747af7b96ed336c5b10`: adds `build_fast.py`, conservative asset optimizer, product review/checklist and read-only performance CI.
- `d6bcab7bc7db131ac124b2acce767457f6d4775f`: fixes the comparison HTTP fixture so each artifact has its own origin root; root-safe 404 URLs are not served under an artificial /baseline/ prefix.
- **`e7be44a9a92a89059f7357ae43f9e602cb06cbe8`**: final tested code. Fixes the synthetic response handler signature and additionally asserts the actual intercepted method/status; application inquiry behavior is unchanged.

Baseline: `bfcfc489463440afa44a2ee39b822de4545524ec`.
All application changes in this unit are additive build/QA files. No accepted business-copy builder, original styles, logo, portrait, book, metadata builder, inquiry endpoint, production pin, DNS, hosting setting or publishing workflow was modified. This result file is a documentation-only follow-up to the tested code.

## Final CI results — all at e7be44a…

| Workflow | Run | Result |
|---|---|---|
| Existing fullsite UI review | [38356608186](https://github.com/minyajing-rgb/ggc-global/actions/runs/38356608186) | success; unchanged original all-page build and UI checks |
| Existing P0 readiness | [38356608173](https://github.com/minyajing-rgb/ggc-global/actions/runs/38356608173) | success; unchanged metadata, 404, keyboard, privacy and inquiry-mode checks |
| New product / performance review | [38356608205](https://github.com/minyajing-rgb/ggc-global/actions/runs/38356608205) | **6,294 checks, 0 failed, 0 exceptions** |

New CI coverage: 98 localized pages; 136 responsive cases; 68 before/after geometry/style comparisons; **16 exact pixel comparisons passed** for Chinese/English home, About, book and contact at desktop/mobile widths. Pixel equivalence is under the same deterministic fallback-font setup, not a certification of production font behavior. All 13 existing built assets remain byte-identical. The original upstream 14 protected source/asset inputs remain unchanged and verified by the existing builders.

Keyboard tabs, category filters, product gallery, mobile menu, local email drafts, static metadata/link/form equivalence and four mocked live-inquiry cases pass. The mocked cases now separately verify that the intended POST response really was 500 or 200. No real inquiry or newsletter submission was made.

Local offline DOM check: 5,996 assertions, 0 failed, 0 exceptions. This complements, but does not replace, the real HTTP CI run.

Two earlier new-CI attempts were not passing runs: the first had a root-path test-fixture image timeout; the second had two failures because Playwright supplied Request to a defaulted second mock argument, causing intended failures to return a synthetic success. Both fixture defects were corrected; no failed assertion was simply disabled or counted as passed. Final source behavior and all retained checks were rerun.

## Payload result — reproducible bytes, not claimed user latency

| Resource | Before | After |
|---|---:|---:|
| Standard-page local CSS requests | 6 | 1 |
| Standard-page deferred JS requests | 3 | 1 |
| CSS raw bytes | 73,616 | 71,458 |
| CSS gzip-9 estimate | 21,734 | 17,096 |
| JS raw bytes | 11,276 | 11,283 |
| JS gzip-9 estimate | 4,757 | 3,879 |
| Combined CSS + JS gzip-9 estimate | **26,491** | **20,975** |

Combined compressed payload is approximately **20.8% smaller**. The seven extra raw JS bytes are statement delimiters protecting original execution order. These figures exclude HTML, images, fonts, headers and TLS; they do not mean the website is 20.8% faster. Actual hosting compression/cache behavior must be checked by Codex.

The same Google font families, weights and display=swap now have early HTML discovery and preconnect instead of a CSS @import dependency. No font binaries are included. Original WebP images are not re-encoded. Intrinsic dimensions/async decoding and explicit hero/below-fold priority are set; book sizing remains visually identical. Fifty-two empty layout headings are hidden from the accessibility tree without removing their layout boxes.

## Controlled lab observations — all four routes, not cherry-picked

Each cell is the median of three cold-cache runs. Mobile viewport 390×844; 4× CPU slowdown; 150 ms emulated latency; 200,000 B/s download; Python HTTP fixture with gzip-9. External Google Fonts CSS is stubbed, so real font downloads, geography and provider delay are excluded. These are not field measurements or Lighthouse scores.

| Route | FCP before → after | LCP before → after | Load-window shift sum before → after |
|---|---:|---:|---:|
| Chinese home | 712 → 688 ms | 872 → 832 ms | 0 → 0 |
| English home | 624 → 588 ms | 772 → 744 ms | 0 → 0 |
| Chinese About | 604 → 676 ms | 776 → 824 ms | 0 → 0 |
| English book | 548 → 624 ms | 716 → 780 ms | 0.05618 → 0 |

**The experiment does not show universal speed improvement.** About/book LCP medians increased slightly in this sample, while the book's observed loading shift disappeared. The source/request improvements are established; further priority/font tuning must use representative real-font and real-device runs rather than promising that every page got faster. INP, field p75, session-window CLS and production Core Web Vitals are not certified by this test.

## Product review and launch gates

Full Chinese-first checklist: [`PRODUCT_REVIEW_AND_LAUNCH_CHECKLIST_2026-10-13.md`](../PRODUCT_REVIEW_AND_LAUNCH_CHECKLIST_2026-10-13.md).

It now records **10 product findings and 18 release gates**, each with expected evidence and ownership. Most important unfinished work:

1. Activate the two language origins and verify actual mailbox receipt before publishing the optional live inquiry flow; confirm legal operator and processing/retention details.
2. Replace method-only research previews with authorized example deliverables; add scoped case evidence, not invented results or employer-as-client logos.
3. Complete true product screenshots/demo links and per-product stage/platform/ownership verification; current labeled information panels are not app UI.
4. Define inquiry triage, owner response targets and outcome tracking. CRM, real subscriptions, double opt-in and unsubscribe are still not connected.
5. Finish company/product/research social share cards and actual-device/font/region checks. Current shared founder image is not a complete social-preview design system.
6. After adopting the candidate, verify production cache/compression, true 404, canonical/hreflang/sitemap, external links and field performance. Keep the previously pinned good artifact available for rollback.

The existing main site has been published by Codex according to PR records. This performance candidate has **not** replaced it, and PR #11 has not been merged by this work.

## Build handoff — no publishing side effects

```sh
python corporate/fullsite-v4/build_fast.py \
  --out /tmp/ggc-fast-release \
  --mode release \
  --base-url https://ggcgames.com/
```

Use a new/empty output directory and the verified canonical base. Without release mode the artifact stays preview/noindex. `build_fast.py` calls the existing `build_ready.py`, retaining the P0 layer and the explicit, disabled-by-default inquiry option. **Running only build_ready.py does not apply the new bundling/image-scheduling layer.** Do not enable the optional endpoint merely because it is supported. Codex owns publication and activation decisions.

Performance artifact: [11793485108](https://github.com/minyajing-rgb/ggc-global/actions/runs/38356608205/artifacts/11793485108), `ggc-pr11-product-performance`, retention 14 days; report + optimized candidate + before/after images.
ZIP SHA-256: `6e07ae99787e1c955e18f8d7fcfa9670d9aff66455ede3d168b6b9a6dff7dd9b`.
Build/QA source and this evidence record persist in the original branch for regeneration.
