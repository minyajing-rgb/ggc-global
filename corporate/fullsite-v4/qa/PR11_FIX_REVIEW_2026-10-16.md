# PR #11: focused acceptance repair, 2026-10-16

Baseline: `25ff9280f3bbff1a7b20626779c46653743de6dd`, branch
`feature/ggc-corporate-rebuild-20261010`.

Failure evidence: [run 38712928716](https://github.com/minyajing-rgb/ggc-global/actions/runs/38712928716),
job `116348532757`, [artifact 11960694422](https://github.com/minyajing-rgb/ggc-global/actions/runs/38712928716/artifacts/11960694422).
Downloaded ZIP SHA-256 verified against the artifact digest:
`b81d51f2b4957c7ddbe923f2945754ed132d6fe4324cf17324b31e488f82097b`.
The recovered report confirms 6,460 checks, three failed assertions and one timeout;
the source build and evidence upload both succeeded.

## Findings and minimal fixes

| Finding | Classification | Evidence and repair |
| --- | --- | --- |
| `requests_6_css_to_1` sees 5 → 1 | Stale assertion **and real optimizer omission** | The HTML actually links seven local stylesheets. `local_file()` rejected every query string, excluding `fullsite.css?v=home-art-15` and `visual-refinement.css?v=20261015-typography`. The old optimized page therefore still had three local CSS links. Accept only local `v` cache queries, combine all seven in their original order, and verify every page's actual source links against the ordered bundle inputs and single output link. Unknown transformation queries, external resources, fragments and paths outside assets remain excluded. |
| Chinese homepage geometry at 390 / 1440 | Test-fixture origin mismatch, no reproduced visual regression | Both original screenshot pairs have equal dimensions and **zero differing pixels** (390×7006 and 1440×3296). Reproduction found exactly one unequal property at each width: `.hero`'s computed `backgroundImage` included each server's different localhost port. All coordinates, sizes, colors, fonts and image paths matched. Normalize only `location.origin` in that property; retain exact geometry/style equality and pixel comparisons, and attach differing values to future failures. |
| `[data-next]` timeout on `product-10.html` | Retired carousel contract | The current hash-verified `source/build_fullsite.py:gallery()` emits `.product-story`: approved artwork, a disclosure caption and three visible positioning/method/partnership facts. It emits no carousel controls. The existing JS has no gallery to initialize, so this is not a broken button or missing initialization. Preserve the static design. Replace the obsolete clicks in all three QA entry points with shared checks for the actual component: structure, visibility, ordered facts, loaded artwork/alt, disclosure, source CTA, keyboard focus and absence of dead carousel controls. Cover all 14 products in both languages, with 390 / 1440 performance cases. |

The complete CSS scope is 24,663 bytes gzip before and 19,177 after (**22.24% reduction**),
seven local CSS links → one. These are deterministic gzip-9 estimates, not field latency.
The old 18 KiB limit covered only five files. The full seven-file bundle now has an
explicit **20 KiB cap**; the separate minimum 15% reduction check remains required.
This scope correction is intentional and is not a claim that the complete bundle meets
the old incomplete 18 KiB measurement. JS remains 3 → 1 and retains its 6 KiB cap.

Added two offline regressions for versioned middle-layer CSS cascade order, unchanged
original assets, and exclusions. The performance workflow runs them before browser QA.
The P0 inline fixture also resolves versioned assets by URL path rather than treating
the query as part of a disk filename. Image inventories explicitly trigger lazy
images and wait for real decoding; a deferred below-fold request is not a broken file.
No homepage template, copy, artwork, palette, responsive design or protected input hash
is changed by this patch. Pixel checks now also cover product-10 in both languages.

## Verification

Local and GitHub Actions results are recorded in the completion update for this patch.
Before pushing, the two optimizer regressions and 504 product-explorer assertions
(14 products × two locales × two widths × nine checks) passed locally. The 20 exact
before/after screenshot pairs for home, About, book, contact and product-10 also
matched. Product 12 correctly discloses the dated OpsGo brand asset; the other 13
disclose concept artwork, rather than falsely labeling every image as the same type.
The supplemental P0 run also exposes two older baseline disagreements, which remain
failures rather than being waived: `approved_hero_geometry:zh` compares the raw builder's
69 px / weight 900 title with the current refinement layer's 56 px / weight 850 title;
the English comparison is 63 px versus 67.68 px. The homepage CSS is unchanged in this
repair. These comparisons are between the earlier raw-builder design and the existing
refined design, whereas the passing performance pixel checks compare the current
design before and after optimization. Confirm the intended visual baseline before
changing either those P0 expectations or the homepage. Keep both assertions active.
The local environment uses available Chromium 153 through an external test adapter;
GitHub Actions retains Playwright 1.57.0 / Chromium 143. Google Fonts CSS remains stubbed
for deterministic comparisons. Live font delivery, field Core Web Vitals and final
brand approval are not established by these fixture tests.

PR #11 must remain Draft. This repair authorizes source/QA updates only: no merge,
production deployment, DNS, hosting configuration or real inquiry submission.
