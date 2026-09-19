# Joyce / GGC — Website Product Review & Refresh V4

Date: 2026-09-19. Release: `2026-09-19-coastal-v4`.

## User request

Refresh the actual website, improve the blurry hero, preserve the selected pale-lavender/gold coastal art direction and improve the product experience. No PDF, no new mockup in place of a website, no new face.

## Findings and implemented changes

| Priority | Finding | Implementation | Validation |
|---|---|---|---|
| P0 | Previous portrait asset was a 461×540 crop compressed to12,344bytes and enlarged in the desktop layout. | Use a538×910 native crop from the user-selected standalone reference; AVIF46,393bytes, less aggressive compression, desktop image-width cap538px,360px mobile source and JPEG fallback. | Asset checksum, image loading, responsive sources and render-width checks. |
| P1 | Sixteen service options require a first-time buyer to understand the entire menu. | Add three entry paths: one expert decision(S01), one product review(S03), or a90-day operating partnership(S11). Each opens the actual scope, price and exclusions. | Three entry points plus full16-item catalogue; no price or scope changes. |
| P1 | Choosing a service could leave the enquiry screen without a visible fee reminder. | Show selected service, indicative fee and billing period above the form. Keep it synchronized across service, language and currency controls. | S03/S14 selection; CNY/USD summary; English/Chinese summary tests. |
| P1 | A prospect cannot easily share the exact service being discussed. | Add copy-service-link inside the scope dialog. A `?service=S03&lang=en#services` URL reopens the relevant service. | Direct URL loads S03; Escape closes dialog. |
| P1 | Inquiry and booking could be confused. | Explicit enquiry-only summary, optional budget label, useful stage/problem placeholders; continue to generate a local email draft only. | Form preview and mailto target; no mail sent, slot reserved or payment taken. |
| P2 | Modal and mobile interactions need more explicit affordances. | Named/described dialog, background scroll lock, larger language/menu controls and outside-click mobile-menu close. | Keyboard, mobile-menu and320/390/768/1024/1440px layout checks. |
| P2 | Some hero overlays reduce portrait/text clarity. | Remove portrait filters, lower decorative overlay strength and improve small-text contrast while keeping the approved palette. | Desktop and mobile screenshots. |

## Image provenance and limits

The replacement is cropped from the already user-selected standalone artwork `141bc04d-08b7-4e52-800a-67233a6ab8c4.png`, rectangle(30,85,568,995). It is the selected AI-styled white-suit brand image, not a new portrait or a claim of unedited photography. The real blue-GGC-shirt image remains in About. The existing decorative signature is unchanged.

This improves use of available native detail. It is not a recovered4K source, a promise of pixel-perfect retinal sharpness at any size, or newly invented facial detail. The sea backdrop remains atmospheric.

## Commercial and privacy invariants

- Existing `joyce/rate-card.csv` controls all16 prices; the release verifies its hash is unchanged.
-14capabilities and12generic business-service scenarios remain.
- No private client names, disputes, family, health or relationship histories are copied to public pages.
- No PDF generated or linked; no repository/database links in the customer-facing UI.
- USD remains a disclosed planning conversion, not a current FX quotation.
- No fabricated testimonials, revenue guarantees, rankings or AI productivity claims added.

## Build and acceptance

Run the canonical coastal builder, then `scripts/refresh_coastal_v4.py`. The release workflow tests the built files using `scripts/qa_refresh_v4.py`, commits them to the Pages branch, waits for the actual v4 marker at both public entry points and tests again with `GGC_LIVE_BASE=https://biz.ggcgames.com`.

Machine results: `joyce/content/refresh-qa/report.json` (built files), `live-report.json` (actual HTTPS). Test reports and screenshots are available in the corresponding Actions artifact. Do not infer conversion lift or Lighthouse results from these functional checks.

## Remaining measurements

Actual lead-conversion lift, paid bookings and buyer feedback need consent-based production measurement. No analytics tracker or payment integration has been silently enabled. Retain the approved visual style when extending the site.
