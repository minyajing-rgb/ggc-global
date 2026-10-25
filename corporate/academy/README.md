# GGC Academy / 课程、著作与方法

2026-10-13. Joyce requested her Sanjieke courses be surfaced and existing GGC subdomains/public materials reviewed.

**Executable source and isolated review artifact only.** Codex owns production hosting, DNS, HTTPS and publication. This change does not modify the live site, existing 98-page source, publishing settings, inquiry provider or subscriptions.

## Final publication set

**12 currently matched public course pages**, spanning 11 topic groups. Two PR/brand pages are related listings; do not assume identical content, version or purchase entitlement.

| Area | Public course IDs |
|---|---|
| Global publishing / AAA marketing | 8006182, 8003815 |
| Retention / events / community | 8006834, 8009615, 8009616 |
| Analytics foundations / advanced | 8003817, 8003816 |
| PR / brand — two related listings | 8007244, 8009627 |
| Cross-cultural teams / hiring | 8006210, 8003814 |
| Laws / policy educational course | 8006835 |

**Held out:** 8003845 AIGC and 8003802 female leadership. They have historical indexed references, but direct HTTP on 2026-10-13 returned the placeholder title `--体系课`, not a matching course title/lecturer. Do not call this proof of deletion. They are not shown as current public course links.

The initial candidate contained 13 links based on indexed material. Read-only live verification found 8003845 needed review; the final candidate removes it rather than allowing an obsolete-looking listing through.

### Source of truth

Teacher: https://www.sanjieke.cn/teacher_info?id=23221919
Detail pattern: https://www.sanjieke.cn/course/detail/sjk/{id}
`catalog.json` holds exact Chinese course titles, concise summaries, editorial English translations, topic groups and held records. Retain course title wording even where it differs from current GGC brand language.

Learning stays on Sanjieke. No paid videos, lecture downloads, onsite playback, enrolment, checkout or independent resale. Prices, discounts, course duration, access periods and teaching language are not copied into this directory. English navigation does not imply English-language delivery. This is not claimed as Joyce's exhaustive lifetime course catalogue.

## Existing domain inventory — public read, not full zone export

At 2026-10-13 09:08 UTC, the repository-referenced public-host audit returned:

| Host | Public response | Treatment |
|---|---|---|
| `ggcgames.com` | GitHub Pages A records, HTTPS 200; corporate entry | Keep company-level services, proof and product navigation |
| `www.ggcgames.com` | CNAME `minyajing-rgb.github.io`; redirects to apex, HTTPS 200 | Alias of company site, not another business |
| `biz.ggcgames.com` | CNAME `minyajing-rgb.github.io`; HTTPS 200, Joyce Mi / Global Game Copilot | Public business profile and scoped service evidence |
| `opsgo.ggcgames.com` | A `216.24.57.1`; HTTPS 200, Game Ops Hub | Existing knowledge/research surface; preferred host to assess for the course directory |
| `academy.ggcgames.com` | DNS status 3 / NXDOMAIN in this lookup | Proposal only; not an existing published Academy |

The audit scanned literal `*.ggcgames.com` mentions in repository text plus known hosts and the explicit Academy proposal; five candidates were found, within the 50-host cap. It did not read Aliyun's full zone or credentials. Public DNS does not exhaust all records, prove ownership, or constitute product/privacy/payment acceptance.

**Deployment suggestion:** first assess an isolated `/academy/` mount on the existing OpsGo app. Codex must verify router/static-host support before adding it. An independent Academy subdomain is optional after that owner review; do not automatically create DNS. Keep the existing Biz and product apps. `/sme/` is a path, not a subdomain. `*.saga1001.com` products are separate domains, not GGC subdomains.

## Public-exposure matrix

| Material | Initial public treatment | Gate |
|---|---|---|
| Sanjieke courses | Title, brief introduction, Joyce attribution and official learning link | Explicit contract/disclosure review before hosting full recordings or paid handouts |
| Published book | Approved cover, introduction and official book destination | No full ebook reproduction |
| Joyce Method | Public Decide / Build / Compound overview and operating modules | Retain source terminology, omit confidential examples |
| Industry research | Source-backed public summary, date and subject | Full reports need licensing/disclosure checks; no invented findings |
| Professional history / services | Approved scoped career and service copy | Old poster prices/figures and employer logos do not become current client endorsements |
| Community / knowledge products | Introduction and separately verified public link | Do not claim live paid membership or subscriptions until tested |
| Tools / experiments | Honest maturity label and approved demo/contact | A prototype is not a released paid SaaS |
| Admin / earnings / internal plans | Exclude from public catalogue navigation | Access-control review is separate |
| Client data / BD lists / private dialogue | Do not publish | Consent and confidentiality review |
| Private personal/astrology records | Excluded | Not corporate course or client evidence |

OpsGo's public page extraction surfaced `AdminDashboard`, `ReferralEarnings` and `ProductRoadmap` links; those routes were not opened or tested. This observation is not a demonstrated authorization vulnerability.

Approved content framing: supplied `Joyce_GGC_9_Original_Posters_副本.pdf` p7 supports Knowledge / Community, courses and content; `Joyce_Method_Plot_Style_Deck_4pages_副本.pdf` p2 supplies the method and pp3–4 the book. It is not blanket permission to publish every internal/personal source page.

## Build without touching the existing site

```sh
python corporate/fullsite-v4/prepare_site.py \
  --out /tmp/ggc-academy-baseline --stage /tmp/ggc-academy-source
python corporate/academy/build_academy.py \
  --assets-from /tmp/ggc-academy-baseline/assets \
  --out /tmp/ggc-academy-preview
```

The first step checks the original 14 protected inputs. The Academy builder copies seven needed approved assets, recording hashes, and creates two localized pages plus a root entry, filters, search/empty state, book/method links and external course navigation. No font files are distributed.

Preview is noindex by default. Only the release owner supplies `--mode release --base-url <verified HTTPS host/path>`; that still builds files only. Output must be new or empty. Do not build over the current OpsGo application.

## Verification and artifacts

`review_academy.py` tests both languages at 320/390/768/1440, course count, local links, images, keyboard filters, search/empty/reset, locale links/navigation, no collection forms or media embeds and no POST. Its `--offline` flag is a labeled in-memory DOM alternative, not hosted acceptance.

`audit_public.py` performs bounded public DNS/HTTP GETs and title/lecturer matching. The workflow additionally blocks the reviewed catalogue when any published listing fails current metadata matching; held historical listings are reported but excluded. No paid content, enrolment or checkout is accessed.

The GitHub Actions artifact `ggc-academy-directory-and-inventory` contains the built candidate, screenshots, browser review and `public-inventory.json`. A successful read-only workflow is not publication. Final run details are appended to PR #11 after completion.

## Codex handoff

Review this source and public inventory; choose the verified knowledge route; deploy the isolated directory without replacing existing applications; use the correct canonical host/path; add a main-site learning entry after the destination is live. Validate both languages, official learning destinations, 404/HTTPS behavior and actual device rendering. No changes to live inquiry, CRM or newsletter configuration belong to this task.
