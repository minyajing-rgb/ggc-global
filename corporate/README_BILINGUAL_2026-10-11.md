# GGC Corporate Website — Full Bilingual Business & Product Portal
**Build:** 2026-10-11 · **Status:** staged in PR #11, not merged/deployed.

## What is implemented
Eight functional bilingual HTML pages under `/corporate/`. Every page has a Chinese/English toggle with `localStorage` language persistence across navigation:

| Page | Purpose |
|---|---|
| `index.html` | Corporate identity, four pillars, cross-capability operating system, key product visuals, founder and partnership |
| `services.html` | Complete GGC Principal 16-service catalogue with pricing authority routed to official rate card |
| `copilot.html` | Creative, Outbound, Growth, Steam, Intel and known reuse engines; maturity boundaries |
| `portfolio.html` | **12 visual product/business tracks**, filterable by game / consumer / software / knowledge / lifestyle |
| `ventures.html` | Joint greenlight, incubation, co-development, publishing and capital |
| `about.html` | Founder, book, past/present/future and mission/vision |
| `insights.html` | OpsGo research, product lab, verified public voice, book, newsletter intent |
| `contact.html` | Segmented contact routes for executive, product, capital and distribution partnerships |

### Business pillars
1. Services and Principal Operating Partner
2. AI Copilot Software
3. Co-Build, Joint Ventures and Capital
4. Owned Products and D2C

Horizontal ecosystem: Capital × Flow × Prosperity; games and consumer distribution, content, people, data and AI.

### Product-exposure rules
- Live game category artwork (Casino / Sims / Arcade) is reused from `/joyce/assets/sector-{category}.avif`.
- Visual colorboards for Bunny, Plot, MEMO, spiritual/knowledge atlas products, OpsGo and AI suite are **illustrative navigation**, not screenshots.
- Categories/research directions ≠ released products.
- Existing project websites ≠ proof of paid installs, commercial success or full feature deployment.
- Product projects ≠ 12 or ten registered companies. Build a separate verified legal-entity and ownership table before making group-company claims.
- Some project domains may be temporarily unreachable or not verifiable from the available public browsing source; re-check links during deployment review.
- GGC five AI products vary in maturity. Avoid claiming all have launched.
- Personal credentials and operating results stay scoped per `positioning/JOYCE_PERSONA.md` and `joyce/docs/PUBLIC-BUSINESS-MASTER.md`.

### Product information and current authoritative links
- Full GGC business description: `bd/GGC_Executive_Intro_Bilingual_v2.md`
- Five AI product names: `sme/README.md`
- Service fee authority: `joyce/content/services.json` and `joyce/rate-card.csv`
- Career, public profile, newsroom: `joyce/docs/*`
- Approved GGC posters: `assets/marketing/2026-09-14/`
- Corporate draft source: `corporate/*.html`

### Release gate
- [x] Bilingual copy and page-to-page language persistence (code inspection).
- [x] Four business pillars and 12 product/business visual listings.
- [x] Five AI product directory.
- [x] All 16 service scopes.
- [x] Local `.html` reference audit (8/8 pages, no missing targets).
- [ ] Browser QA: desktop/mobile 1440/768/390, cross-page i18n, image loading, screen reader.
- [ ] Verify all public outgoing links and detailed product stage labels with respective owners.
- [ ] Validate entity/group structure; legal company naming and use of group claims.
- [ ] Verify reception and deliverability of public business email.
- [ ] Implement production contact intake, spam protection, consent records, CRM integration and event tracking.
- [ ] Implement real newsletter email capture, double opt-in, privacy policy, welcome, preferences and unsubscribe. Current `mailto:` expresses interest only.
- [ ] Audit WeChat official accounts, Video, Douyin, Xiaohongshu, Weibo, Bilibili, X, YouTube and other official profile URLs before publication.
- [ ] Prepare polished product screenshots and verified customer/partner case studies for the visual second pass.
- [ ] Domain and DNS owner confirmation for `ggcgames.com`, staging URL and release/rollback approval.
- [ ] Production SEO: hreflang routes, canonical, OG images, schema, sitemap and redirects.

**No modification has been made to the current root GitHub Pages site, CNAME (`biz.ggcgames.com`), DNS, real payment flows, live external projects or newsletter production services.**
