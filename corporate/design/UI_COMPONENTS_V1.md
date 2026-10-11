# GGC Corporate UI / Design Specification v1.0
**2026-10-11 · Design handoff, not production release**

## Creative direction
**Strategic Systems × Playful Product Energy.** The site must feel like an international high-trust operating company while visibly demonstrating that it builds games and AI products. Large Gen-Z editorial headlines, 30–50% breathing room, creamy white/pale lavender base, black-ink titles, violet/magenta accents, subtle gold signal details and Aurora-like gradients. Avoid generic consulting stock photos, overly ornate mysticism or Disney-like caricatures. Illustrative color/shape compositions are mockups, not verified product UI.

### Color, spacing and type
See [DESIGN_TOKENS_V1.json](DESIGN_TOKENS_V1.json). Recommended headline H1 desktop 72–86px/mobile 44–48px; H2 desktop 42–50px/mobile 30–34px; regular text 16–18px. Container 1216px, mobile gutter 20px, section vertical spacing 90px/64px. Click/touch targets ≥44px. English/Chinese copy must fit naturally without clipping.

## Screen inventory / visual priorities
| Screen ID | Page | Visual hierarchy / layout | Interactive behavior / states |
|---|---|---|---|
| S01 | Corporate Home | Bold bilingual headline, triple product collage (game / Bunny / Copilot), two CTAs, four business cards, featured products, Founder, newsroom | Hero CTAs; business card links; language parity; mobile nav |
| S02 | Portfolio | Business heading, filter chips, project art tiles and honest maturity badges; three desktop columns, one mobile | All/Games/Consumer AI/Software/Knowledge/Lifestyle, URL-shareable filter planned |
| S03 | Product Detail | Product title/status, 2 CTAs (official product / business partner), narrative, authentic screenshot gallery, capabilities/markets | Gallery next-prev/swipe; external link tracking; partner preselect |
| S04 | AI Copilot | 5 tool cards with operator job, input/output, reuse engine, status/next-action | Demo only where verified, otherwise trial request |
| S05 | Services | 16 services grouped decision/product/publishing/operating/AI; detail reveals deliverables, capacity, fees authority | Filter/search; service-to-inquiry with preselected service ID |
| S06 | Contact | Two-column desktop / one-column mobile; trust/process left, 5 essential fields plus consent right | Client/server errors, sending, no duplicate, honest confirmation |
| S07 | Co-Build | collaboration modes, deal fit, founder/partner trust, project intake | Stage/type selector, route to lead form |
| S08 | About/News | history narrative, Joyce portrait/book, verified evidence and current product development | Filter confirmed vs pending awards; public source links |
| S09 | Newsletter | editorial value, cadence, topic preferences and email | pending, confirmation, subscribed, error, unsubscribed |

## Components and design rules
### Global Navigation
Desktop uses logo left, 7 primary routes middle and EN/中文 + partner CTA right; mobile hamburger with focus management and the language control always reachable. Sticky bar respects safe-area and doesn't hide anchored headings. Focus outlines clearly visible; no touch interaction requires hover.

### Home Hero
H1 answers “What is GGC?”; one primary business CTA and one product-discovery CTA. Product collage should use **approved game/category art or actual GGC product UI**, never competitor footage represented as owned work. Three-second message: four business pillars, real build work and global ambition.

### Pillar Card
Each card contains `01/02/03/04`, business title, one-sentence value, 1 CTA. Don’t reuse “consulting” language for Copilot or self-owned product cards. Card stays keyboard accessible.

### Product Card
`name`, `category`, `ownershipType`, `maturity`, hero art+alt, one-sentence use case, official URL/trial/inquiry. Use literal status text with color as secondary cue; status evidence and publication date in content registry. Entire cover/CTA navigation should be consistent, no nested anchor collisions.

### Product Detail
Hero: breadcrumb > maturity label > product title > differentiator > platform > primary CTA > secondary partner CTA. Content modules: `What it does`, `Product & UX screenshots`, `Audience & markets`, `Business model`, `Next milestone`, `Team/ownership disclosure`, `Proof/Links`. Use `Concept UI` label on mockups. Real app captures or promo posters should be attributed to their approved product sources.

### Service Detail
Include who this is for, typical inputs, scope, deliverables, estimated involvement, exclusions, reference fee source, CTA. Small review ≠ full fractional COO. Client numbers and case outputs require explicit approval.

### Contact Lead Form
Default steps: partnership track → essential fields + problem → privacy consent → submit → real receipt. Browser demo deliberately blocks actual sending. Production states: idle, required-field, invalid-email, bot-gate, sending, accepted + inquiry ID, retryable failure. Source/referrer safe-list; no PII in analytics. Investor requests separated from actual B2B buyers, consumer clickouts excluded.

### Newsletter
Inputs: email, category preferences, locale, consent. States pending opt-in, verified, unsubscribed. No fake success, no automatic subscription from a BD form.

### Footer
Company identity, major product/service links, verified social links and legal/privacy. WeChat official account, Xiaohongshu, Bilibili, Douyin, Weibo, X, YouTube etc are **not** linked until official ownership and exact destinations are confirmed.

## Responsive acceptance
- 1440 desktop: 55/45 Hero with visual to right; pillars four columns; product three columns; contact two-column.
- 768 tablet: columns collapse 2 → 1 as content requires; no overflowing navbar.
- 390 mobile: big title 44–48px, nav drawer, cards one column, form single column, details may use sticky contact CTA.
- 320 extreme mobile: no horizontal scroll, headings fit; avoid text badges as sole semantic indicators.
- Reduced-motion honors media preference; minimum WCAG 2.2 AA contrast and keyboard traversal.

## Image sourcing / legal gate
Repository sources: `joyce/assets/sector-{casino,sims,arcade}.avif`, `assets/marketing/2026-09-14/`, latest approved Joyce photos/book, Bunny and MEMO original project sources. Keep legal entity/portfolio status separate from visual claims. For anything unavailable, use clearly labeled editorial illustration; do not invent store screenshots, testimonials or already-live commerce.

## Local design package
A downloadable conversation artifact called **GGC_Corporate_UX_PRD_Mockups_Architecture_2026-10-11.zip** includes:
- Interactive HTML samples: home, portfolio, Bunny detail, AI copilot, services and contact
- 4 full documents: PRD, UX Flow, Architecture and Design System
- 390/1440 screenshots, bilingual and filter QA outputs and a single UX overview sheet
These assets are available in the conversation, **not committed to this public repository as PNG files**, and they are prototypes, not actual product imagery or deployed infrastructure.

## Ship gates
Production requires real content/asset owner review, valid company/domain, English/Chinese SEO routes, approved product states, valid forms/CRM/newsletter/consent, full 390/768/1440 browser QA, and explicit release authorization. The current site root / CNAME must remain untouched until verified.
