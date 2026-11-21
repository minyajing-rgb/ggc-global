# GGC — Website Implementation / 官网实际实现

Version: 2026-10-12. Stage: isolated development preview, NOT a production cutover.
Approval: Joyce explicitly selected button variants **01, 04, 06, 08, 09, 10** and requested GitHub upload plus actual website implementation.

## What exists now

This is executable source, not another flat website mockup. The generator creates **8 corporate pages in each language + 1 component library in each language**: 18 independently rendered EN/ZH pages and a root entry point.

| Route in each locale | Implemented function |
|---|---|
| `index.html` | Company-first hero, glass-light strategic memo, three illustrative diagnostic scenarios, six decision questions, four businesses, research and featured product entry points |
| `expertise.html` | All 16 service names, service search, filters, scope expanders, canonical rate-card link, service-to-inquiry referral |
| `research.html` | Existing research directions and OpsGo source entry; not invented news or market findings |
| `decision-os.html` | Evidence / Benchmark / Decision / Action, three sample scenarios with real accessible tabs |
| `lab.html` | Five specialized Copilot directions plus Intelligence, game R&D and consumer/knowledge products; filters and maturity boundaries |
| `ventures.html` | Greenlight, MVP, co-development, publishing and strategic partnerships |
| `about.html` | Why GGC / Joyce, historical operating experience, author/book, vision and public profile |
| `contact.html` | Required-field validation, partnership/service preselection and explicit local email-draft preparation; no automatic sending or CRM claims |
| `buttons.html` | Six approved components, default/hover/focus/pressed/disabled states, loading demo, keyboard tabs and light/dark inspection |

## Selected button application

- 01 Blade: lightweight secondary actions and business/product cards.
- 04 Outline: secondary hero and approach actions.
- 06 Primary Gradient: hero and navigation primary actions.
- 08 Tab: diagnostic samples and categorical filters; correct tablist vs filter-button semantics.
- 09 Elevated Luminous: controlled closing CTA; no flashing.
- 10 Ghost: quiet research and product actions.

Unselected styles 02/03/05/07 are not included in the implementation set. The forward-leaning blue/violet GGC wordmark is outlined SVG; **no font file is distributed**.

## Build locally

Python 3.12+; no third-party package required for the website build.

```sh
python corporate/implementation/src/build_site.py --out /tmp/ggc-preview
python -m http.server 8080 --directory /tmp/ggc-preview
```

Open `/zh/index.html`, `/en/index.html`, `/zh/buttons.html` or `/en/buttons.html`.

Shared source: `src/buttons.css`, `src/site.css`, `src/app.js`, `src/ggc-logo.svg`, `src/build_site.py`.

## Base44 implementation — actual existing app

App: `ggc-global`, ID `6a96dac28be99e3ac4d6d525`.

The **same immutable GitHub source commit** `21372760bb2ddfb29484fe9585bf49d5b22c9c09` was retrieved and all five SHA-256 digests matched the locally tested files before execution. Source lives in `/app/ggc-next-source/`; generated site lives in **`/app/ggc-next/`**.

Important entry routes in that app's preview server:
- `/ggc-next/zh/index.html`
- `/ggc-next/en/index.html`
- `/ggc-next/zh/buttons.html`
- `/ggc-next/en/buttons.html`

These are sandbox preview paths, NOT a claim that `ggcgames.com/ggc-next/` is live. No public preview hostname has been verified through the available connector. Do not invent one.

An HTTP read with an external-style Host header verified **23 HTML/CSS/JS/SVG assets**, each status 200 and byte-equal to its generated file. Original root index SHA-256 remains `b7da8a6754c64029dac68164ffc6ab70498278d4a92cb3dbd7c40c342d3da085`; CNAME remains `biz.ggcgames.com`.

## Verification — precise scope

Local Chromium rendered the actual generated HTML/CSS/JS **in memory**, because its policy blocks `file://` and localhost navigation. We did not change browser policies. Therefore these checks are DOM/interaction/layout tests, **not a deployed HTTP end-to-end browser test**.

- 72 layout checks: 9 page types × 2 locales × widths 320/390/768/1440; no horizontal overflow after one 320px decorative-surface fix.
- 502 local file/anchor references resolved.
- 8 interaction check groups passed: selected styles, loading/focus/disabled, keyboard tabs, same-page locale link, scenarios, service search/empty state, product filter, mobile menu and local-draft behavior (some checks grouped).
- No automatic form POST was made.
- Screenshots and full generated site are delivered as conversation artifacts; screenshots are not committed here as binary media.
- Base44 separately passed 23 HTTP byte-match checks. Its sandbox has no Playwright/browser installed; no remote browser E2E result is claimed.

## Content and safety boundaries

The original approved posters and button board guide style; their generated figures, testimonial/partner logos, dates and prices are not treated as verified live-company claims. Public website content uses the latest strategic-lab positioning, existing service names and public profile sources. `joyce/content/services.json` and `joyce/rate-card.csv` remain fee authorities. Product text panels are illustrative, not fake app screenshots. Research categories, prototypes and products are not legal subsidiaries. Private client files and personal astrology records are not included.

The inquiry flow uses the existing Gmail route `minyajing@gmail.com` only to prepare a draft. No backend, CRM, analytics, subscriber database or payment connection has been added. Input stays in the page until the visitor chooses to open their mail client. Newsletter link is an expression-of-interest route, not an active subscription system.

## Next implementation gates

1. Replace eligible product text covers with each product's approved visual assets and reconcile exact maturity/ownership. Expand project-level case/Why GGC proof without fabricating metrics.
2. Complete dedicated detail pages and deeper research-library links after source/permission review. Keep the selected design and six button IDs stable.
3. Add real inquiry persistence, notification/retry, anti-spam and CRM routing; double opt-in, preferences and unsubscribe for newsletter. Do not change UI to “sent” before server acknowledgment.
4. Verify root-domain host, public staging URL, legal/privacy copy, indexable locale SEO metadata, full browser E2E and external destinations.
5. Only then perform a controlled production release with a rollback point. Existing `biz` and current Base44 root remain untouched in this unit.
