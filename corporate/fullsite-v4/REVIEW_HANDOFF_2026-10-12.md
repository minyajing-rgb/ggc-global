# GGC Full-site UI V4 — complete visual review and executable frontend

2026-10-12. Follows Joyce's latest request: complete every UI page using the selected company-first magenta/blue-violet, large-type, strategic-sheet template before further implementation by Codex or the assistant.

## Actual deliverables in the conversation

- `GGC_Fullsite_UI_16_Types_Overview.png`: 16-screen overview, drawn from actual HTML browser renders.
- `GGC_Fullsite_UI_Review_CN_EN.pdf`: 32 full-scroll review pages, one Chinese and one English desktop/mobile spread per UI type.
- `GGC_Fullsite_UI_and_Frontend_V4_2026-10-12.zip`: runnable site, all source, approved portrait/book crops, 64 representative desktop/mobile long screenshots, 4 additional state screenshots, page coverage and QA records, source-provenance notes and Codex handoff.

**These new frontend source files and visual assets are currently in the conversation ZIP, not checked into this GitHub directory and not installed over Base44's existing preview.** This GitHub document registers the scope and handoff accurately. The existing `corporate/implementation/src/` and existing `/ggc-next/` remain the prior Magenta Prism build until this design-review package is imported. Do not tell users that the 96-page build is already deployed or published.

## Screen scope

| UI type | Routes / instances | Key interaction |
|---|---|---|
| 01 Home | index | Strategic memo scenarios, four business routes, founder proof |
| 02 Expertise | expertise | 16 services, category/search and empty state |
| 03 Service detail | service-s01 ... service-s16 | Scope, delivery, process, FAQ and service-prefilled inquiry |
| 04 Research library | research | Games/AI theme filters |
| 05 Research brief | research-casino / arcade / sims / consumer-ai / agent | Reading layout, table of contents, method/source/contact routes |
| 06 Decision OS | decision-os | Evidence/Benchmark/Decision/Agent diagram and selectable illustrative scenarios |
| 07 Joyce Method | method | Three capabilities, seven modules and seven-step operating process |
| 08 Product portfolio | lab | Category filters and actual individual detail routes |
| 09 Product detail | product-01 ... product-14 | Positioning, audience, three-panel information gallery and official/external or partnership action |
| 10 Co-build / Ventures | ventures | Collaboration modes and engagement flow |
| 11 Why GGC | about | Provided founder image, scoped historical roles, method/book, vision and evolution |
| 12 Book | book | Provided book cover and source-poster eight-topic overview |
| 13 Updates / interest | updates | Topic/email interest draft; explicitly marked future-state design previews |
| 14 Contact | contact | Required/invalid inputs, consent, service/track referral and local mail draft |
| 15 Components | buttons | Selected 01/04/06/08/09/10; default/hover/pressed/focus/disabled/loading and tabs |
| 16 Not found | 404 | Home/contact recovery |

There are **48 paths per locale, 96 localized HTML pages total**, plus a root entry and an all-screen review hub. This is 16 distinct UI types with directory instances, not 96 distinct designs or products.

## Exact source and content boundaries

The new builder reuses the reviewed PR11 source at `64bbb83f9b12f39bb055fd98fdf055bb0587678a`. Existing company copy and corrected career-role wording are retained. Service detail scope comes from `joyce/content/services.json`, including its numerical scope caps, rather than an older promotional rate poster.

The method page uses the supplied `Joyce_Method_Plot_Style_Deck_4pages_副本.pdf` p2: Decide / Build / Compound; seven modules; Diagnose / Prioritize / Build / Operate / Review / Scale-Stop / Codify. Book assets and eight thematic labels come from pp3–4; they are not asserted to be a newly verified formal table of contents. Portfolio framing also draws on the supplied nine-poster deck pp7–8, without converting product tracks into legal subsidiaries.

Portrait is a resize of the user's previously supplied Joyce poster crop, not a newly generated person or an independently verified camera-original photograph. Book cover is cropped from the supplied book poster. No font files are included.

Research detail pages are clearly marked **theme / method briefs**, not newly produced research findings or market forecasts. Product information gallery panels are clearly marked **not actual app screenshots**. Personal/spiritual source material is not silently recharacterized as a scientific corporate-diagnosis methodology.

## Source package

Open `START_HERE.html` or `site/review.html` in the ZIP. Build with:

```sh
python source/build_fullsite.py --out site
```

The build uses only Python standard-library dependencies. Existing reviewed source modules are included for reproducibility; new modules are `build_fullsite.py`, `fullsite.css`, `fullsite.js`, plus approved asset crops. Only the QA harness requires Playwright/BeautifulSoup.

## Verified locally

`qa/review.json` records **3910 static and offline Chromium checks, 0 failed, 0 browser JavaScript errors**. All 96 pages have static local-resource/link checks. Sixteen representative UI types were rendered in both languages at 320/390/768/1440, with 64 long-page screenshots and 4 extra state screenshots. Tests exercise scenarios, keyboard tabs, service empty state, gallery, mobile navigation, contact draft and subscription-interest/design-state UI. No automatic business POST occurred.

These are local in-memory DOM/browser checks, not hosted production E2E. PDF rendering was additionally inspected with MuPDF; PDF has 32 pages. No changes to production domain, root index, CNAME, CRM, subscription backend or payments were made in this unit.

## Next integration gate

Import the conversation source bundle into an isolated review route, verify source hashes and run deployed HTTP/browser checks. Preserve selected visual identity and existing root. Attach authorized original research/case documents and actual product captures where available. Integrate real inquiry/CRM/notification and double-opt-in only after owner and privacy decisions. Do not relabel draft preparation or design-state previews as real sends/subscriptions.
