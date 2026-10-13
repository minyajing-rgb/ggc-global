# GGC Academy / 课程、著作与方法

2026-10-13. Requested by Joyce: add her Sanjieke courses and review GGC subdomains/material suitable for public exposure.

**This directory contains executable source, not a published subdomain.** Codex continues to own hosting, DNS, TLS and live acceptance. No current site, domain record, form configuration or subscription setting is modified here.

## What is ready in source

- Chinese and English course-directory pages, category filters, local search and an empty state.
- 13 identified public Sanjieke course pages across 12 topic groups. Two PR/brand listings are explicitly related; identical content, version or purchasing rights is NOT assumed.
- Exact Chinese course titles and official external course URLs. English text is editorial translation, not a claim of English video/audio delivery.
- Existing GGC portrait, logo, book cover and approved magenta-prism/button assets reused without modification.
- Book, Joyce Method, corporate contact, public instructor, OpsGo and Biz links.
- Independent preview/release modes, canonical language pairs and a small sitemap when a verified release base is explicitly supplied.
- No learner accounts, video hosting, paid downloads, onsite checkout, course purchase, tracking, CRM or newsletter enrollment.

### Reproduce from the original source branch

```sh
python corporate/fullsite-v4/prepare_site.py \
  --out /tmp/ggc-academy-baseline \
  --stage /tmp/ggc-academy-source

python corporate/academy/build_academy.py \
  --assets-from /tmp/ggc-academy-baseline/assets \
  --out /tmp/ggc-academy-preview
```

The original full-site builder verifies its 14 protected inputs. The Academy builder copies seven needed approved assets and records their hashes; it does not replace original pages. Output must be new/empty. For local viewing, serve the output directory, or open `zh/index.html` and `en/index.html`.

Only the release owner may supply `--mode release --base-url <verified HTTPS host/path>`. That command still only builds files, never deploys.

## Hosting / subdomain proposal — not a DNS instruction

1. **Prefer the existing `opsgo.ggcgames.com` knowledge surface** for courses, book, methods and permitted public research. A new `/academy/` route can host this isolated artifact if its current application/router supports the mount. Do not overwrite its app or assume an arbitrary route is already implemented.
2. `academy.ggcgames.com` is a possible separate learning entry, not an asserted existing host. Its status must be checked against public DNS and Codex's authoritative zone inventory before choosing it.
3. `biz.ggcgames.com` retains executive/business proof and service details; the apex remains the corporate brand. A path such as `/sme/` is not another subdomain.
4. Products on `saga1001.com` remain independent product sites. Do not move them or imply they are GGC subdomains.
5. Publishing the catalogue does not require mirroring Sanjieke videos or moving payments off Sanjieke.

The new `audit_public.py` checks only literal repository-mentioned GGC hosts plus known references and the explicit Academy proposal. It performs public DNS/HTTP GETs only, with a 50-host cap. **It is not a complete Alibaba DNS-zone export.** HTTP 200 is not proof of product readiness, ownership, authorization, enrollment, privacy acceptance or working payment.

## Public-exposure decision matrix

| Material | Safe initial website treatment | Additional gate |
|---|---|---|
| Sanjieke courses | Course name, concise description, Joyce attribution, official learning link | Full recordings/handouts need an explicit contractual-rights check before rehosting |
| Book | Existing approved cover, introduction, author and publisher/book page | No full ebook reproduction or independent resale claim |
| Joyce Method | Public overview of Decide / Build / Compound and operating modules | Original source terminology retained; private examples omitted |
| Public research | Title, theme, date and source-backed public abstract | Full reports require disclosure and licensing approval; no fabricated findings |
| Professional profile/services | Approved career wording, scoped services, contact | Old poster prices/metrics and employer logos do not create current customer endorsements |
| Community/knowledge products | Description; verified official public entry when available | No assertion of active membership, payment or auto-subscription until tested |
| AI tools/product experiments | Clearly labeled product state, approved demo or contact route | Not every prototype is a released paid SaaS product |
| Admin/earnings/internal plans | Do not expose in public discovery navigation | Access-control review is separate; a link alone does not prove unauthorized access |
| Client/BD data/private practitioner dialogue | Do not publish | Consent, confidentiality, anonymization and disclosure review |
| Personal/private astrology or family records | Excluded from corporate material | Never copy private client/personal records into a public course hub |

OpsGo's current public extraction surfaced routes named `AdminDashboard`, `ReferralEarnings` and `ProductRoadmap`. They were not opened or tested here. Exclude them from the outward-facing catalogue; do not misreport this navigation observation as a demonstrated security vulnerability.

## Course evidence / source trace

Primary instructor page: https://www.sanjieke.cn/teacher_info?id=23221919
Course detail pattern: https://www.sanjieke.cn/course/detail/sjk/{id}
All IDs and descriptions are in `catalog.json`. Sources were read from the official public instructor/course pages on 2026-10-13, supplemented by separately identified historical public listings. They are not paid course content.

- Main current instructor-page links include 8009627, 8009616, 8009615, 8006182, 8007244, 8006835, 8006834, 8006210, 8003817, 8003816, 8003815 and 8003814.
- AIGC 8003845 has a public detail page identifying Joyce; its January 2024 date is explicitly disclosed rather than marketed as a current 2026 tools course.
- Historical leadership 8003802 is held out: the latest detail extraction returned an empty course title. That is a verification limitation, not a claim of deletion.
- Exact prices, discounts, durations, access periods, refunds and delivery language stay with Sanjieke. Do not copy cached numbers or advertise the listings as permanently available.
- The instructor page can show a partial subset. This is not claimed to be a complete inventory of everything Joyce has taught.

Approved user source decks: `Joyce_GGC_9_Original_Posters_副本.pdf`, p7 (Knowledge / Community, courses and content), and `Joyce_Method_Plot_Style_Deck_4pages_副本.pdf`, p2 (Decide / Build / Compound), pp3–4 (book). Those materials establish the information architecture; they do not authorize publishing every internal/personal page.

## QA scope

`review_academy.py` defaults to HTTP Chromium and checks both locales at 320/390/768/1440, all course counts and local links, loaded images, keyboard filters, empty search/reset, language navigation, no embedded recordings/collection forms and no POST. `--offline` is a clearly labeled local DOM alternative where browser policy blocks localhost; it is not deployed acceptance.

The read-only GitHub Actions workflow preserves the built preview, desktop/mobile screenshots, QA and `public-inventory.json` for inspection. A request failure is a review flag, not proof that a course or subdomain was deleted.

## Codex next steps

Inspect the catalogue and audit output; choose one existing-compatible knowledge route or an explicitly approved new Academy host; publish the isolated files without overwriting other apps; use the exact verified canonical base; add the public entry to the main site only after its route is live. Verify both languages, official learning links and browser/server behavior. No changes to live inquiry providers or subscription configuration are part of this task.
