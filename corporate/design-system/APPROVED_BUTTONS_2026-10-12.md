# GGC — Approved Button Set / 已选按钮

Decision date: 2026-10-12
Authority: Joyce's explicit selection in the current conversation: **1, 4, 6, 8, 9, 10**; upload to GitHub and proceed with the actual corporate website.
Reference: user-selected 10-style board `未来感按钮设计系统展板.png`.

| ID | Original reference name | 中文 | Implementation role |
|---|---|---|---|
| 01 | Blade Button | 轻量光刃 | Light secondary CTA, delicate gradient edge |
| 04 | Outline Button | 轮廓按钮 | Secondary CTA, clear background, chromatic border |
| 06 | Primary Gradient | 主按钮（渐变） | Main hero and navigation CTA |
| 08 | Tab Button | 标签式按钮 | Content tabs, filters; real selected/keyboard states |
| 09 | Elevated Luminous | 高级发光按钮 | One strong closing CTA; controlled glow, not flashing |
| 10 | Ghost Button | 轻量幽灵按钮 | In-card research/product actions and quiet navigation |

02 Jelly, 03 Glassmorphism, 05 Split and 07 Frosted are NOT selected for the initial implementation. Preserve the prior board as historical inspiration; do not implement all ten as approved.

## Visual direction
Keep the user-selected editorial strategic-memo homepage, company-first GGC identity, restrained white/lavender base, blue-violet iridescent details and slim surfaces. No redesign into an engineer dashboard, mystical world hall or giant-founder portrait. Refresh the GGC wordmark as a forward-leaning blue/violet laser-style vector treatment; do not represent it as an independently registered new logo.

## Behavior & quality
Default, hover, pressed, focus-visible, disabled and loading must be real CSS/HTML states. Tabs require keyboard support and visible selected state. Minimum interactive target 44px. Avoid oversized bloom; readable text before decorative shine. Chinese and English are equivalent separate views, not crowded bilingual sentences inside every button.

## Website implementation
Continue PR #11 and preserve production. First implementation unit: reusable button CSS, interactive component gallery, refined vector GGC wordmark, shared website navigation and company homepage, then services/Decision OS/research/portfolio/contact flows. Source and verification results will be added next to this approval record.

Existing Base44 app discovered: `ggc-global` (`6a96dac28be99e3ac4d6d525`). It is a static-site sandbox whose CNAME says `biz.ggcgames.com`; this does not prove root-domain production ownership. Any implementation there must use an isolated `ggc-next/` route and leave the existing root index and CNAME unchanged. No new Base44 app, paid builder call, DNS change or production overwrite is authorized by this approval record.

Original career/brand posters remain reference material. Their figures, prices, personal subjects and company logos are not automatically approved website claims; no private source images are to be published as corporate client evidence.
