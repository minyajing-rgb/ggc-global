# GGC · AI-native small-studio games — real code / awards submission screening
**Checked:** 2026-10-23, Base44 connected user app inventory, actual sandbox source inspection, Vite build QA, official 2027 competition pages.

## 1. Scope and claim controls
- The connected Base44 account returned **50 named app records**. This is an **account inventory**, not 50 games or 50 shipped consumer products.
- Nine clearly game/interactive-experience candidates were source-inspected in app sandboxes. They contain distinct game-play components, not only pitch slides. No public app URLs, Apple/Google store identifiers, original release dates, third-party rights clearance or paid-active-user records were returned by app listing.
- **Four actual production build commands** were run on 2026-10-23 via connected Base44 sandboxes: Yarn Fever Mania, Neon Dots Connect, Prince Shroom, Soccer Tycoon 3D. All returned shell exit code 0; `dist/index.html` and JS/CSS build outputs were found, with respective dist sizes about 595 KB, 592 KB, 1.5 MB and 665 KB. Builds are not browser E2E, public-deployment or published-game evidence.
- Joyce's commercial story: founder/operator with historical Zynga/Gameloft global game experience, personally designing Skills, Agent workflows, AI-assisted coding and game/creative/intelligence tools. A small **human-led, AI-assisted studio** — do NOT claim 7 human employees, independently autonomous AI staff, 50 launched games, or verified revenue without dated proof. Older closed-door deck's `7 enabled tasks` should not be conflated with `7 production-running agents`.
- Public code evidence for the support tooling: [A+B Loop/Content Editor](../../research/casino/ab-editor/README.md) and [HTML/JS source](../../research/casino/ab-editor/index.html), [AI-native Game Build-to-Revenue Skill](../../skills/ggc-ai-native-game-build-to-revenue/SKILL.md), [Skill/Agent business system](../../skills/ggc-principal-ai-native-two-flow-os/SKILL.md).

## 2. Nine sourced game candidates — exact source classification

| Candidate (Base44 app name) | Actual inspected implementation clues | 23 Oct build result | Public release / Play URL | PR / award lane |
|---|---|---|---|---|
| Yarn Fever Mania | `src/pages/YarnGame.jsx`, `src/lib/yarnLevels.js`, `src/components/yarn/GameHUD.jsx`; level/entity models | **Vite BUILD PASS**, dist generated | **NOT VERIFIED** | Casual mobile-web puzzle; **first choice for AI Browser Game Jam**, conditional |
| Neon Dots Connect | `src/pages/Game.jsx`, `src/lib/gameLevels.js`, `src/lib/gameStore.js`, Home/Shop/game-state UI | **Vite BUILD PASS**, dist generated | **NOT VERIFIED** | Casual puzzle; **second AI Jam candidate**, conditional |
| Pixel Yarn Unravel | `src/pages/GamePage.jsx`, app/game UI | Source found; BUILD NOT CHECKED | **NOT VERIFIED** | Experimental casual/puzzle |
| Soccer Tycoon 3D | `src/components/game/{DraftScreen,TeamBuilder,MatchSimulation,Collection,RoadToGlory}.jsx` | **Vite BUILD PASS**, dist generated | **NOT VERIFIED** | Sports/simulation, playable product lane if authenticated QA/release proven |
| PartyIsland | `src/components/game/{IslandScene,SlotMachine,SpinWheel,AIChat,EventPanel,StarShardGame}.jsx` | Source found; BUILD NOT CHECKED | **NOT VERIFIED** | Multisystem interactive entertainment; copyright/compliance and casino mechanics deserve additional review |
| Prince Shroom (one of 3 copies) | `src/pages/GamePage.jsx`, admin CMS/analytics/config plus multiple `base44/functions/*` including economy/gameTick/analytics services | **Vite BUILD PASS**, dist generated | **NOT VERIFIED** | Technical innovation, simulation/interactive game; do not infer backend functions have live QA |
| Glamour Empire (Copy) | `src/pages/{Play,Chapters,StoryMap,Social,Store,Estate}.jsx`, chapter branches and Stripe function stubs | Source found; BUILD NOT CHECKED | **NOT VERIFIED** | Interactive narrative and Sims; do not infer production payments |
| 42楼吃西瓜 | `src/hooks/useGameLoop.js`, `src/components/GameRenderer.jsx`, Game/Leaderboard pages | Source found; BUILD NOT CHECKED | **NOT VERIFIED** | Browser arcade |
| Probability Garden | `src/components/garden/{useRound,PredictionControls,ProbabilityCharts,GardenHero}.jsx` | Source found; BUILD NOT CHECKED | **NOT VERIFIED** | Experimental interactive experience; not automatically standard mobile game |

## 3. Real award matching — eligibility is a gate

**BEST NEW MATCH: AI Browser Game Jam 5** — https://itch.io/jam/ai-jam-5  
- **Deadline:** 2026-10-31 03:00 (the itch.io page timestamp; validate displayed user-zone at submit).
- Entries MUST be **free, publicly playable in browser without download**, heavily AI-assisted, with majority of submitted work AI-generated. Existing projects accepted **only if >50% newly developed content in this jam**. Theme "TORCH" is optional. Team or solo okay.
- Yarn Fever Mania and Neon Dots Connect are the leading candidates **on code/build evidence**, but no hosted playable URL, majority-new-content proof or itch.io submission account found. **STATUS: NOT SUBMITTED**. Next: public H5 build QA + date/asset/license evidence, upload to itch.io, official jam join+submit and keep submission page receipt. No fake itch page.
- Itch.io's documented workflow requires a creator account and a public game page before jam submission: https://itch.io/docs/creators/game-jams

**Game Developers Choice Awards 2027** — https://gamechoiceawards.com/ and https://gdcawards.secure-platform.com/site/ ; **2026-11-01 23:59 PT**. Free direct developer/publisher submission, but release/platform requirements described by contemporary 2027 industry reports include 2026 PC/console games. **No current project passes a verified 2026 PC/console shipped-game test**. New **Best Gaming Tech** category officially covers innovations in game development software/hardware/tools, so GGC A+B editor and Skill-based production workflows are a **conditional exploratory fit**. Official source: https://gamechoiceawards.com/categories/. Portal requires sign-in and entrant representations. **No award submission performed**; an organizer eligibility question email was attempted on 23 Oct but the Gmail provider returned **FORBIDDEN**, do not count it as sent.

**Pocket Gamer Awards 2027** — https://www.pocketgamer.com/pocket-gamer-awards/2027/nominate/ ; **2026-11-15**, free public Google Form. Ordinary new-release titles must have launched between 2025-10-01 and 2026-09-30; category options Best Mobile Indie Developer, Developer, Publisher etc may consider catalogue. Official embedded form requires actual nominable game/developer name, category, first/last name/email, GDPR consent and newsletter choice. GGC games are presently **web app code**, no Google Play or App Store ID and mobile public launch proven. **Do NOT claim official nomination**, and do not submit an ineligible 2026-10 prototype as a 2026-09 mobile launch. A web-mobile playable game alone is not evidence of mobile store release.

**BAFTA Games 2027** — https://www.bafta.org/awards/games-rules/ ; some qualifying 2026 releases due **2026-11-06**; standard fee **£475 + VAT**, rights holder consent and eligible UK release required. Current evidence insufficient, payment not approved; **no submission**.

**IGF 2027** — https://igf.com/submission-info/ ; **closed 2026-09-13**. Accepts mobile/HTML5 games generally but cannot submit for 2027 now.

**IndieCade** — https://www.indiecade.com/submissions/ ; 2026 cycle closed; 2027 submissions expected February 2027. Good future fit for work-in-progress games; fees/rights as published then.

**Slapjam #2** — https://slapjam.ai/ ; 2026-10-29–31; free 48-hour **new** mobile portrait browser-game jam. Theme and jam start later; do not submit an old app as a game built during the jam.

## 4. International PR editorial outreach — actual Gmail proof

**Portfolio / small-studio pitch:** real 2026-10-23 Gmail `SENT`:
- Pocket Gamer consumer news `news@pocketgamer.co.uk` message **`1a168a12a7bcf774`**: small-team AI-native game studio with specifically named Base44 prototypes, source-level evidence, and offer to provide screenshots/access after verification; does not call them released.
- IndieDB `press@indiedb.com` message **`1a168a1369845767`**: founder-operated indie game prototypes and specialist AI workflows, editorial/devlog discussion, no unverified launches.

Both are **press/story pitches**, not competition nominations or published features. No delivery or human reply assumed from Gmail SENT. Prior 2026-10-23 seven-email batch for games/AI/women/business PR is listed at [earlier expansion ledger](../authority-engine/PR_AWARDS_EXPANSION_AND_OUTREACH_2026-10-23.md).

## 5. Story pitch and proof: small human team × specialized AI workflows

### English masthead
**A Game Industry Veteran Builds an AI-Native Game Studio: Small Human Team, Specialist Agents, and Real Browser-Game Prototypes**

### Editorial abstract
After leading global game product and commercial operations across Zynga and Gameloft, Joyce Mi is building a different kind of indie studio. She personally designs game loops, product-economy and release criteria, runs bespoke AI Skills and specialist Agent workflows, and uses AI-assisted coding to turn concepts into interactive browser projects. Her Base44 account holds source-backed implementations for games spanning puzzle (Yarn Fever Mania, Neon Dots Connect), sport (Soccer Tycoon 3D), narrative (Glamour Empire), and multisystem play (Prince Shroom, PartyIsland). Four sampled projects generated production Vite builds in an actual 23 October code check. She is also developing reusable game content and market intelligence software, including a public single-file A+B Game Loop & Content Editor.

The original angle is not that AI "replaces a game studio" or that dozens of apps prove success. It is a verifiable change in **production architecture**: one experienced operator can command bounded AI-assisted work across ideation, product research, game design, prototype coding, content, QA, global expansion and commercialization. The next proof gates are public playable demo, independent QA, launch/release record and real player feedback. We distinguish functioning code from a commercial launch, experimental prototypes from polished releases and AI task roles from staff headcount.

### Chinese headline
**资深全球游戏操盘手亲自打造 AI-Native 小团队工作室：从 Skills / Agents 到九款有源码的游戏原型**

**技术支撑角色示意**（不是声称恰有七个实时运行的 Agent）：market/competitive intelligence → product design / core-loop → AI coding/prototyping → creative/asset production → QA/acceptance → publishing/localization → player/revenue feedback. Joyce personally owns product priorities, integration and final go/no-go responsibility.

**Do not claim:** 7 human employees; 7 autonomous production bots; 9 shipped games; 50 released titles; 4 full E2E tested games; measured AI-driven profit; public store availability without proofs.

## 6. Next acceptance checks

- [x] Actual Base44 app inventory, source inspection, individual gameplay components.
- [x] Four Vite production builds successful, dist output verified.
- [x] Match AI browser jam and GDCA tech award using official evidence.
- [x] Two distinct editorial story pitches SENT in Gmail.
- [ ] **Public game URL / playable without login**, per candidate, and verified mobile/desktop UX.
- [ ] Legal art/code/IP provenance and 2026 creation/release dates; AI jam majority new-content check.
- [ ] Itch.io game page + entry for AI Browser Game Jam 5 by **31 Oct** (no itch.io authenticated app action presently available).
- [ ] Evaluate standalone tool eligibility in GDCA Best Gaming Tech, read 2027 full rules / official entrant portal, capture receipt if eligible.
- [ ] Obtain legitimate submitted nomination receipts for everywoman / other formal portals separately. **This markdown is an evidence packet, not a formal submission.**
