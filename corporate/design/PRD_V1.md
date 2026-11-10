# GGC Corporate Site — Product Design Master / PRD v1.0
**2026-10-11 · Draft for Design & Engineering · Scope: bilingual corporate gateway + product exposure**  
**Implementation:** existing `corporate/*.html` in PR #11. These files are an earlier working draft. This PRD defines the next production-quality target; it is not a claim all functions are implemented.

## North-star & differentiation
Turn `ggcgames.com` from a Joyce-led consulting introduction into the GGC corporate identity, with **four complementary commercial pillars**:
1. **Services / Principal** — strategic decisions, publishing, monetization, fractional CMO/COO and annual operating partnerships.
2. **AI Copilot** — GGC Creative, Outbound, Growth (existing product name), Steam and Intel, with per-product release labels.
3. **Co-Build / Ventures** — greenlight, incubation, joint development, publishing and strategic capital.
4. **Owned Products / D2C** — global games, consumer AI, content IP, knowledge and lifestyle.
A shared layer connects **Capital × Flow × Prosperity**: founders, teams, global distribution, operational leadership, data and AI.

## Audience and user jobs
| Who | Entry | Wants | Conversion |
|---|---|---|---|
| Game Founder / CEO / GM | Home, Services | Understand GGC's principal expertise and concrete scope | Qualified enterprise inquiry |
| R&D Studio | Ventures | Joint greenlight, development, publishing | Verified project intro |
| Investor / CVC | Portfolio, Founder | Real product, proof and team scope | Strategic/industrial investor inquiry |
| Game team / SaaS evaluator | Copilot | Job-to-be-done, maturity and trial access | Product pilot request |
| Consumer / KOL | Portfolio | Find actual Bunny, MEMO or other project | Verified product site outbound click |
| Press / Conference | About, News | Founder record, publication, confirmed speaking | Media inquiry |
| Industry reader | Insights | Practical research updates | Double-opt-in newsletter |

## Information architecture / target international SEO
- `/zh/` + `/en/`: corporate homepage, same content identities, independently indexable
- `/{locale}/services/` and `/services/{service-slug}/`: full 16 services, deliverables, scope, commercial terms, authoritatively sourced rates
- `/{locale}/copilot/` + `/copilot/{creative|outbound|growth|steam|intel}/`: AI software job, workflow, maturity, real demo/trial
- `/{locale}/ventures/`: greenlight, incubation, co-publishing, capital and partner screening
- `/{locale}/portfolio/` + `/portfolio/{product-slug}/`: portfolio filter, maturity, project detail, gallery, primary CTA
- `/{locale}/about/`: vision, Joyce, book, past/present/future, method, approved evidence
- `/{locale}/insights/`: public news, research, speaking and subscription
- `/{locale}/contact/`: purpose-specific contact / lead form
- `/{locale}/privacy/`, terms, subscription policy.

**Role of legacy sites:** keep `biz.ggcgames.com` as Joyce executive proof and fee detail, `opsgo.ggcgames.com` as research/knowledge; keep product logins, payments and consumer profiles at their owned project sites.

## Functional requirements
| ID | Priority | Requirement | Definition of Done |
|---|---|---|---|
| FR01 | P0 | EN/ZH parity | Every page, nav, CTA, empty/error state, SEO title and description has a translated counterpart. Language switch stays on same semantic page. |
| FR02 | P0 | Corporate-first homepage | Business model comprehensible at first viewport, CTA visible on 390px mobile, product exposure above lower site sections |
| FR03 | P0 | Four business routes | Services, Copilot, Co-build and Owned Products have distinct purpose, who-it's-for and CTA |
| FR04 | P0 | Complete Service catalog | All 16 services sync with canonical `joyce/content/services.json` / rate card, no unlimited COO claims |
| FR05 | P0 | Five AI tool cards | Real jobs, examples, development maturity and valid CTA or explicit waitlist |
| FR06 | P0 | Products and ventures catalog | Categorization, filters, per-product badges, actual or clearly marked conceptual visuals |
| FR07 | P0 | Product detail | What it is, user/customer, platform, maturity, differentiator, 3–6 approved media, verified claim, external site or partner CTA |
| FR08 | P0 | Credibility / founder | Career and book with sources, client results only when individually approved |
| FR09 | P0 | Lead routing | Inquiry type/region/stage/role + consent; server acceptance, idempotent retry, honest failure/success UI |
| FR10 | P0 | SEO/accessibility | Independent localized routes, canonical/hreflang, structured data where justified, 390/768/1440 QA |
| FR11 | P1 | Newsletter | Double opt-in, topics, welcome, preferences, unsubscribe, suppression audit |
| FR12 | P1 | CRM integration | Owner routing, company dedupe, state history and consent; STOP respected |
| FR13 | P1 | Publish workflow | Content draft -> evidence review -> approved -> live; source attribution and rollback |
| FR14 | P1 | Analytics | Funnel events with locale/track/product but no personal contact data |
| FR15 | P2 | Search and booking | Only after product/content corpus and real bookings verified |

## Page anatomy
**Home:** Global Nav → company Hero/2 CTAs + real product visual → four pillars → Featured Products → shared operating system → Founder and project proof → Ventures/Partners → latest public insights → Newsletter → social/footer.  
**Services:** scoped categories, deliverables, client inputs, pricing boundaries, adjacent cases, qualified inquiry.  
**Copilot:** input → AI-assisted output → human approval/action → expected value, release state and real demo.  
**Portfolio:** filter by Games/AI Consumer/Software/Knowledge/Lifestyle, explicit development status, ownership type, product card and detail.  
**Ventures:** collaboration mode, qualifying criteria, project stage, economics/rights boundary, inquiry.  
**About:** organization past→present→future, founder record, book, evidence, Mission/Vision, strategy.  
**Insights:** editorial streams, verified public news, newsletter preference.  
**Contact:** purpose preselection, company + role + market + key challenge, consent, server-confirmed inquiry ID.

## Product claims: strict boundaries
- A published URL does not prove paying users, production-grade functionality or a customer outcome.
- Category tracks (Casino, Sims, Arcade) are not automatically released GGC games.
- Twelve project/track cards do **not** equal twelve registered subsidiaries. Reconcile the intended “ten companies” with verifiable legal entity/ownership documentation before publishing company-family claims.
- Status must be one of `concept, prototype, private-beta, public-beta, live, paused, discontinued`, supported by owner review and `verificationDate`.
- Separate `assetType=real-ui | authorized-product-art | illustrative-concept`. Never use unrelated competitor screens as GGC own screenshots.
- Career and benchmark claims follow `positioning/JOYCE_PERSONA.md`; book link and public talks follow `joyce/docs/PUBLIC-NEWSROOM.md`.

## Events / success definition
North-star: **qualified enterprise inquiry**, not raw contact form clicks. Separate lead funnel from consumer D2C clickout and newsletter confirmation. Track `page_view, language_switch, pillar_click, product_filter, product_card_open, external_product_click, service_view, contact_start, contact_validation_error, contact_success, newsletter_pending, newsletter_confirmed, book_click`. No user email, name, phone or inquiry text in analytics. Baseline target metrics only after real launch data.

## Quality bar
- 390 / 768 / 1440 QA, mobile CTA visible, drawer keyboard accessibility, contrast WCAG 2.2 AA target.
- Real indexed EN/ZH routes, not only DOM text switching; output sitemap/hreflang/canonical.
- Core Web Vitals objectives: p75 LCP ≤2.5s, CLS ≤0.1, INP ≤200ms where feasible and after observed measurement.
- Contact: server-side validation, consent logging, anti-spam, rate limits and verified recipient/CRM routing before claim of success.
- Newsletter: privacy notice, double opt-in, localized emails and one-click unsubscribe before public signup.
- Production remains gated on real asset/license audit, correct product stage, DNS ownership, visual browser acceptance and rollback.
