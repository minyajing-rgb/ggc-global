# GGC 5 AI Growth Apps — SME Product Architecture

Public page: https://biz.ggcgames.com/sme/

## Canonical five products

1. GGC Creative — AI Performance Creative
2. GGC Outbound — B2B Outbound Engine
3. GGC Growth — Game / App Growth Copilot
4. GGC Steam — Steam Launch / Wishlist Copilot
5. GGC Intel — Vertical Intelligence

Do not replace these five with Offer/Pricing, generic Money Radar or Revenue Ops. Those may exist as features inside the five products, but they are not separate v1 products.

## Existing-system merge map

| Product | Reuse now | Rebuild / missing |
|---|---|---|
| GGC Creative | Base44 FlowMedia AI: Create Studio, Content Library, Analytics and publishing workflow. | Reframe around performance creative: creative audit, hook/angle, storyboard, test matrix and winner/loser learning. New mobile-first front end. |
| GGC Outbound | Base44 GGC DealGraph: accounts, opportunities, companies, relationships, outreach, signals, CRM and reports. | Simplify to daily leads → score → decision maker → outreach → follow-up. Remove deal/investment complexity from customer-facing UX. |
| GGC Growth | Base44 GamePulse AI: game reports, analytics, product review and QA. OmniCritique AI: analysis form, product review and analysis detail. | One Growth Health Score, FTUE/retention/monetization/UA/ASO diagnosis and Top 5 Actions. Mobile-first UX. |
| GGC Steam | No current Base44 app is a clean fit. Some research/benchmark components may be reused from GamePulse / GGC research. | New standalone Base44 app required. Store page, wishlist, trailer/demo, creators, festivals, launch calendar and weekly actions. |
| GGC Intel | Base44 TrendPulse: library, feeds, daily brief, analytics and brief pipeline. GGC research agents/category databases. | Refocus from generic content intelligence to vertical business intelligence: competitor moves, ads, hiring, funding, product changes, opportunity scoring and “what this means for you.” |

## Shared backend vs customer-facing products

The five products should look separate on mobile. The backend can reuse:
- ChatGPT reasoning / research / synthesis
- Codex code, data processing, QA and automation
- Telegram / agent notification and distribution workflows
- GGC research databases and category taxonomies
- shared company/account context
- subscription and entitlement model
- shared evaluation / logging layer

Do not market ChatGPT, Codex, Base44 or TG Agency as the product names. They are implementation layers.

## Product principle

Website can be rich. Mobile must be small and beautiful.

Each app should open directly into its primary job:
- Creative → What should I test?
- Outbound → Who should I contact today?
- Growth → What is blocking growth?
- Steam → What should I do before launch?
- Intel → What changed and what does it mean?

## Commercial ladder

Self-serve App / Audit → paid Sprint → GGC annual executive partnership.

Annual services remain on the Joyce/GGC executive page and should not clutter the five mobile apps.
