# Joyce / GGC — Coastal website, clarity refresh v4

Active release: `2026-09-21-credibility-v7`.

## Live website

- [Main website](https://biz.ggcgames.com/?v=refresh-v4)
- [Joyce website](https://biz.ggcgames.com/joyce/?v=refresh-v4)
- [Product review scope](https://biz.ggcgames.com/joyce/?service=S03&lang=en#services)
- [Bilingual master rate CSV](rate-card.csv)

Both root and `/joyce/` serve the same complete interactive website. The legacy rate-card page redirects to the services section. No new PDF is produced and there are no PDF links on the active website.

## What changed in v7

- Expanded public credibility from selected cards into a **2019–2026 Speaking & Industry Contributions timeline**.
- Added source-linked 2026 AI-driven user growth, 2025 AI + global product lifecycle, 2024 mini-game global growth, 2024 global game operating blueprint, 2023 AIGC, and 2019 global growth / monetization records.
- Kept LinkedIn as the current social source of truth and the website as the owned, structured credibility archive.

## What changed in v6

- Added a source-linked **News & Recognition** section instead of leaving credibility as generic labels.
- Added the confirmed Tencent-alumni Entrepreneurship Honor Roll record, the 2024 Hangzhou App-global-growth talk and book signing, the 2023 Huibuluo × Xiaguang summit talk, the China Machine Press book, KCHUHAI industry writing and a current LinkedIn activity entry.
- Added the book ISBN and direct publisher reference.
- Kept award applications / conference proposals out of the confirmed public record until accepted.
- Preserved the approved coastal lavender/gold visual system.

## What changed in v5

- Preserved the approved pale-lavender / gold coastal visual system and existing portraits; this release is a content and conversion-architecture update rather than a visual redesign.
- Added **Executive Profile** with career proof and explicit role ownership.
- Added a six-project **Portfolio Ecosystem** linking GGC Business, AI Bible for Kids, Dharma Atlas, Earth Healing, QuriAtlas and MEMO.
- Added a **LinkedIn / Publications / Speaking / Industry Roles** section using verified public references only.
- Added a prominent **Annual Partnership** layer: Executive Advisory, Fractional CMO/COO, and Strategic Growth Partner.
- Updated Annual Global Game Copilot floor to **CNY 1,280,000 / year** in the detailed rate card.
- Preserved the detailed 16-service catalog for paid diagnostics, scoped projects and qualification before annual work.

## What changed in v4

- Replaced the heavily compressed461×540 portrait crop with a538×910 native crop from the user-selected standalone artwork. Desktop width is capped at538px;360px responsive source, AVIF and JPEG fallback added.
- Preserved the pale-lavender/gold coastal direction, white-suit portrait, gold signature motif and translucent cards. No new face generated. About retains the real blueGGC-shirt photo.
- Added three clear starting points: expert decision, product review,90-day operating partnership.
- Selected enquiry now shows service, fee and billing period; language and currency changes stay synchronized.
- Scope dialogs have accessible labels, Escape/background behavior and a copyable direct service link.
- Improved mobile-menu controls, bilingual form placeholders and budget label.

This is a native-reference-detail improvement, not a recovered4K source. The signature-style wordmark remains decorative, not an authenticated legal signature.

## Content and commercial boundaries

Four sector paths, interactive operating stages,14capability domains,12anonymized business-service scenarios and16scoped offers remain. Prices are controlled by the existing CSV and were not changed. USD remains a disclosed planning conversion.

The enquiry builder generates a local mail draft. It does not send messages, confirm bookings, store form data or take payment. Private client names, disputes, health and relationship histories are not public site content. Former employers and project names do not imply endorsements. No outcome guarantee or retrospective receivable is implied.

## Implementation and evidence

- [Product review and implemented fixes](docs/PRODUCT-REVIEW-V4.md)
- [Public Business Master](docs/PUBLIC-BUSINESS-MASTER.md)
- [Capability data](content/capabilities.json)
- [Anonymized scenarios](content/advisory-scenarios.json)
- [Services](content/services.json)
- [Refresh asset manifest](content/refresh-v4-manifest.json)
- [Built-file QA](content/refresh-qa/report.json)
- [Actual HTTPS QA](content/refresh-qa/live-report.json)
- [Release workflow](https://github.com/minyajing-rgb/ggc-global/actions/runs/35448756888)

Build in order:

```sh
python scripts/build_coastal_v3.py
python scripts/refresh_coastal_v4.py
python scripts/qa_refresh_v4.py
GGC_LIVE_BASE=https://biz.ggcgames.com python scripts/qa_refresh_v4.py
```

Requires Pillow11.3.0, Playwright1.57.0 and its Chromium browser. The active coastal workflow runs the base build and then v4; do not publish the base builder alone. The oldV2 automatic PDF workflow stays disabled.

## Release record

2026-09-19v4: Image transfer checksum passed. Built desktop/mobile and actual public-domain tests passed. The live verification at2026-09-19T14:28:41Z confirms v4 on both root and personal entries, responsive hero, unchanged prices, language controls, service selection, form draft and mobile layout. Full reports and screenshots are committed and archived in the release artifact.

2026-09-19v3: Initial user-selected coastal website published; retained in Git history.
