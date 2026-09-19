# Joyce / GGC — Public business site v2

- [English website](https://biz.ggcgames.com/joyce/)
- [Signed rate card](https://biz.ggcgames.com/joyce/rate-card.html)
- [Rate card PNG](downloads/Joyce_GGC_Rate_Card_EN.png)
- [Rate card PDF](downloads/Joyce_GGC_Rate_Card_EN.pdf)
- [Bilingual master rate CSV](rate-card.csv)
- [Public Business Master](docs/PUBLIC-BUSINESS-MASTER.md)
- [Visual System](docs/VISUAL-SYSTEM.md)
- [Changes](docs/CHANGELOG.md)
- [Capability data](content/capabilities.json)
- [Anonymized service scenarios](content/advisory-scenarios.json)
- [Service data](content/services.json)
- [Asset manifest](content/asset-manifest.json)
- [Automated QA](content/release-qa.json)

Build: `python scripts/build_joyce_business.py`. Browser QA/render: `python scripts/qa_joyce_business.py` with Playwright Chromium installed. Build inputs are the existing capability records, the current rate-card.csv and approved visual assets. Generated output contains public business information only. Private valuation records are not copied here.

Prices are proposed scoped offers, not verified paid rates or retroactive receivables. The gold signature-style wordmark is decorative. The portrait is a resized real user-supplied photo, not an AI identity rendering.
