# GGC — Visual Fidelity V2 / 视觉精修实际执行

Date: 2026-10-12
User request: the real website differs too much from the approved mockups; strengthen typography, GGC logo and large headlines, then execute.
Status: implemented in PR #11 and the existing Base44 `ggc-global` development route. Not a production-domain release.

## What changed in executable code

No new flat concept image, company repositioning, giant founder portrait or fantasy scene was introduced. The current content and approved button variants 01 / 04 / 06 / 08 / 09 / 10 remain.

| Element at 1440px viewport | Prior implementation | V2 measured local rendering |
|---|---|---|
| Chinese hero display size | 61.2px | 77.76px |
| English hero display size | 61.2px | 69.92px |
| Hero declared weight | 760 | 900 |
| Header logo element width | 109px | 146px |
| Chinese title top position | 254.6px from viewport top | 195px |
| Hero illustration | Main card with empty decorative back cards | Three authored sheets: source categories, selectable diagnostic memo, company-fit dimensions |

- Larger blue/violet GGC wordmark with tighter optical bounds, foil reflection and a fine rim. SVG paths, no font file distribution.
- Stronger display typography, intentional line breaks and controlled word spacing. The heavy title does not depend only on increasing paragraph size.
- Bilingual brand headline on the home hero; full page locale still switches between independent EN/ZH routes.
- Shared inner-page titles, section labels, cards, navigation and footer hierarchy refined.
- Questions and four business pillars use a more compact editorial rhythm rather than large empty section blocks.
- Three-sheet hero remains selectable HTML/CSS. Its scenario/source graphics are explicitly illustrative, not live data or client findings.
- Existing search, filters, tab keyboard controls, mobile menu and local email draft flow remain functional.

## Current build entry point

Use the refined builder for subsequent development:

```sh
python corporate/implementation/src/build_refined_site.py --out /tmp/ggc-preview
python -m http.server 8080 --directory /tmp/ggc-preview
```

`build_refined_site.py` imports the existing `build_site.py` content and route functions instead of creating an independent site or duplicating its service catalogue. The earlier `build_site.py` is the content/base renderer; it no longer represents the latest visual build by itself.

New source:
- `src/build_refined_site.py`
- `src/fidelity.css`
- `src/ggc-logo-refined.svg`

Shared base source remains unchanged: `build_site.py`, `site.css`, `buttons.css`, `app.js`.

## Font delivery

The build emits an external Google Fonts CSS reference for Inter and Noto Sans SC at weights 400–900 with `display=swap`; installed fonts/system sans-serif provide a fallback. No OTF, TTF or WOFF files are copied into the repository or review package.

The font stylesheet returned HTTP 200 from the Base44 sandbox, contained both families and a 900 weight, and the first referenced remote font returned HTTP 200. This is a reachability check, NOT a complete cross-device browser font audit. Local screenshots use installed Inter Display / CJK fallbacks because the local rendering environment has no external network access; no claim of pixel-identical font rendering across all devices is made.

## Verification actually performed

Local Chromium DOM rendering:
- 9 page types × 2 locales × 7 viewport widths (320, 390, 768, 1024, 1280, 1440, 1920): 126 layout checks.
- Added actual headline scroll-width checks; corrected the English 1280/1920 and small-phone clipping cases before delivery.
- Corrected the English Decision OS 320px grid/min-content overflow.
- 524 local file/anchor references resolved.
- 8 interaction groups passed: approved variants, loading/focus/disabled, keyboard tabs, locale/scenario behavior, service search/empty state, product filters, mobile navigation and local email draft.
- Final recorded failures: 0.

Boundary: these are in-memory DOM/layout tests, not deployed browser HTTP E2E or full WCAG certification. The font import is excluded from offline test rendering; its external reachability is checked separately.

Base44 actual execution:
- Existing app: `ggc-global`, `6a96dac28be99e3ac4d6d525`.
- New source downloaded from immutable GitHub commits; SHA-256 equality checked against the locally tested files.
- Build tested under a candidate directory, then moved onto the existing `/app/ggc-next/` development route.
- Final source commit: `1ebf6667e7af6894c9459885f15add22d07e6364`.
- 24 generated HTML/CSS/JS/SVG resources returned HTTP 200 with bytes equal to the generated files; external-style Host header used.
- EN/ZH home, button library and Expertise routes rechecked in the active directory.
- Original `/app/index.html` remains SHA-256 `b7da8a6754c64029dac68164ffc6ab70498278d4a92cb3dbd7c40c342d3da085`.
- CNAME remains `biz.ggcgames.com`.
- Restore point before work: `6accb85f0a8512075fdaf111`.
- Restore point after work: `6accbae82904ef768360571b`.

Development entry paths in the existing app:
`/ggc-next/zh/index.html`, `/ggc-next/en/index.html`, `/ggc-next/zh/buttons.html`, `/ggc-next/en/buttons.html`.
No verified public preview hostname is supplied by the available connector; these paths are not claimed to be live on ggcgames.com.

## Scope that is still not complete

This pass improves real UI fidelity; it does not complete product-specific artwork/case evidence, backend CRM persistence, newsletter double opt-in, production privacy/legal review, root-domain deployment or browser E2E. Existing local-draft contact behavior stays explicit; no fabricated sent/success state was added.

## Evidence / artifact delivery

The conversation package contains the actual generated site, editable source, real before/after screenshots in EN/ZH, mobile captures and the test script/results. No user-private astrology material or unverified mockup figures/testimonials were brought into the website.
