# Joyce / GGC — Coastal website v3

Active release: `2026-09-19-coastal-v3`.

## Live website

- [Main website](https://biz.ggcgames.com/)
- [Joyce website](https://biz.ggcgames.com/joyce/)
- [Interactive services and fees](https://biz.ggcgames.com/joyce/#services)
- [Bilingual master rate CSV](rate-card.csv)

Both the root and `/joyce/` now serve the same complete interactive website. The legacy rate-card page redirects to the services section. No new PDF is produced and there are no PDF links on the active website.

## Selected visual direction

The user-selected pale-lavender and gold coastal artwork is implemented with separate image assets and selectable HTML: sea panorama, white-suit portrait, gold signature motif, translucent cards and clear service controls. The hero portrait is cropped from the user's selected AI-styled reference; the about section retains the existing real blue GGC-shirt photo. No new face has been generated. The signature-style wordmark is decorative, not an authenticated legal signature.

## Working content and features

- English/Chinese language switch and mobile navigation.
- Four sector entry paths and interactive operating-system stages.
- 14 capability domains and 12 anonymized business-service scenarios.
- 16 scoped offers; category filter, CNY/USD planning reference, scope dialog and service selection.
- Inquiry brief builder opens a mail draft; it does not send email, confirm a booking or process payment.
- Public business content only; private customer names, disputes, health and relationship history are not published.
- Service prices remain controlled by the existing CSV, not by the old text embedded in concept artwork.

## Sources and implementation

- [Public Business Master](docs/PUBLIC-BUSINESS-MASTER.md)
- [Capability data](content/capabilities.json)
- [Anonymized service scenarios](content/advisory-scenarios.json)
- [Service data](content/services.json)
- [Coastal visual-asset manifest](content/coastal-v3-manifest.json)
- [Build/browser QA](content/coastal-qa/report.json)
- [Build source](../scripts/build_coastal_v3.py)
- [Local browser tests](../scripts/qa_coastal_v3.py)
- [Public-domain verification](../scripts/qa_coastal_live.py)

Build: `python scripts/build_coastal_v3.py`.
Local checks: `python scripts/qa_coastal_v3.py` with Playwright Chromium installed.
Actual-domain checks: `python scripts/qa_coastal_live.py`.

The old V2 builder is retained for history only; its automatic workflow is disabled so it cannot overwrite this design or generate new PDF deliverables.

## Release record

2026-09-19: All six source-transfer parts restored and checksum-verified. The complete website and media were built and committed at `f4e6b452d71a73ff7a7780733ca1668713edb0c9`. The corresponding GitHub Pages deployment completed successfully. Local browser QA passed all 30 checks. Public-domain verification runs separately and records the actual remote file hashes and browser behavior.

Prices are proposed scoped offers, not verified historical paid rates or retrospective receivables. USD uses the disclosed planning rate, not a live foreign-exchange quote. Former employers and historical projects are not client endorsements. No outcome guarantee is implied.
