# GGC Strategic BD — Batch 07 Quota Fill to 100

**Date:** 2026-09-19  
**Owner:** ChatGPT Strategic BD Pool (`ChatGPT B`, company-level ownership)  
**Mode:** China-first quota fill / production outbound  
**Canonical inputs read:**
- `status/GGC_BD_Dual_Agent_Execution_Plan_v1.md`
- `skills/GGC_BD_Target_ICP_China_v1.md`
- `bd/chatgpt_pool/2026-09-19_Batch06_Production_China_First_30.md`
- newest ChatGPT-pool seed / production files

## 1. Run result

This continuation started from the **30 SENT** already logged in Batch 06 and continued until the day reached **100 SENT**.

| Metric | Result |
|---|---:|
| Day SENT before this continuation | 30 |
| Additional SENT in this continuation | **70** |
| **2026-09-19 total SENT** | **100** |
| Hard / envelope delivery failures in today's 100-send cohort | **15** |
| No hard-bounce observed yet | **85** |
| Automated replies | **1** (Rayark support-ticket auto reply from Batch 06) |
| Human replies | **0** |
| Positive replies | **0** |
| Meetings | **0** |
| Quota target achieved | **YES — 100 SENT** |
| Hard blocker | None for send quota |

**Cohort hard-bounce rate: 15.0% (15 / 100).** This is above the preferred deliverability threshold and is treated as a routing-quality warning even though the 100-SENT production target was completed.

### Bounce hygiene / suppression

Suppress these exact routes until independently reverified; do not retry them in +5/+10 follow-up:

1. `abby.li@mechanist.co` — Mechanist — hard bounce / 554 RCPT.
2. `zhangnan@fotoable.com` — Betta Games — address not found.
3. `business@zenjoy.net` — Zenjoy — message blocked / failed delivery.
4. `chengbijuan@4399inc.com` — 4399 — address not found.
5. `bd@gzycgame.com` — 游畅 — 554 RCPT.
6. `npc@minggames.com` — 明娱 — address not found.
7. `business@swiftjava.com` — 十万伏特 — address not found.
8. `liuchan@zhangyou.com` — 掌游 — 550 verify.
9. `lyp@uu898.com` — UU898 — 554 RCPT.
10. `business@gzpanxi.cn` — 盼兮网络 — address not found.
11. `bd@4x.com` — 4X — 550 5.1.1 recipient not found.
12. `biz@boogie.games` — BoogieGames — 550 verify.
13. `info@cgland.top` — CGLand — domain not found.
14. `imengru@jwxwh.com` — 紫宸互娱 — 550 verify.
15. `contact@joyseed.com` — JoySeed — address not found / 554 RCPT.

Also retain the prior Batch 06 suppression on Rayark `service@rayark.com`: it is a customer-support route and produced an automated support ticket, so it must not be used for cold BD again.

A separate older Gala Sports bounce arrived during this date window, but its outbound was **not part of today's 100-send cohort**, so it is excluded from the 15 / 100 cohort metric.

### Deliverability rule for next production run

- Do not reuse any address above without fresh independent verification.
- Prefer current official corporate business / BD / partnership / publishing pages on live first-party domains.
- Avoid stale personal addresses, SEO/directories, mirrored contact pages, support routes, and newly discovered domains that cannot be corroborated.
- When a source pattern starts producing >10% hard bounce, stop that pattern and move sourcing to a different channel; do not treat quota pressure as permission to reuse weak routes.

## 2. Ownership / dedupe gate

- Gmail history was checked before touching the added targets.
- The explicit Base44 / Agency TG A-owned pool remained excluded.
- Recent ChatGPT-owned companies from Sep 18–19 production batches were not re-touched.
- Sep 18 fresh accounts are not yet due for the +5-day follow-up; their next normal window begins Sep 23.
- Today's fresh accounts below are eligible for +5-day follow-up on **Sep 24** only if there is no reply and the route has not bounced; +10-day follow-up is **Sep 29**.

## 3. Variant legend

- **A — Portfolio OS:** scaled R&D/publishing/operation team; pitch focuses on greenlight, LiveOps, monetization, UA, regional allocation and stop/scale standards.
- **B — R&D → Self-Publishing:** R&D / co-dev / service team moving toward own-IP, self-publishing or global GTM; pitch focuses on front-loading market, monetization, LiveOps and Go/No-Go.
- **E — Ecosystem / Joint Delivery:** platform, publisher, infrastructure or ecosystem partner; pitch focuses on joint delivery / referral / product-operating layer.

No retroactive A/B-test label is invented here: these are operational segment labels for the modular pitch actually used.

## 4. Additional 70-send ledger

| # | Company | Owner | Variant | Public route used | Verified signal / source | Missing-corner diagnosis | Send / Reply / Meeting / Bounce | Next action |
|---:|---|---|---|---|---|---|---|---|
| 31 | G-Bits / 雷霆游戏 | ChatGPT B | A | `npi@g-bits.com` | Public business route; mature publishing / product-introduction / investment stack | Cross-project greenlight, monetization, LiveOps and resource-stop standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 if no reply |
| 32 | Changyou / 畅游 | ChatGPT B | A | `qibao@cyou-inc.com` | Public business route; mature R&D, IP and long-term operations | Global GTM + monetization + LiveOps + portfolio allocation consistency | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 33 | 4399 | ChatGPT B | A | `chengbijuan@4399inc.com` | Public overseas-business route found during sourcing | Platform/distribution scale needs cross-title operating OS | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route; no follow-up |
| 34 | TOPJOY | ChatGPT B | B | `bd@topjoy.com` | Public BD route; self-developed mobile-game focus | Move global validation, monetization, LiveOps and UA upstream into product decisions | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 35 | Mooncake Games | ChatGPT B | A/E | `bd@mooncakegame.com` | Public BD route; global publishing/developer-service positioning | Portfolio DD + greenlight + post-launch operating standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 36 | Zencode Games | ChatGPT B | B | `business@zencodegame.com` | Public business route; global mobile/H5 publishing + original products | Lightweight self-publishing OS before organization gets heavy | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 37 | 游畅 | ChatGPT B | A | `bd@gzycgame.com` | Public BD route; global-publishing positioning | Selection, soft launch, monetization and LiveOps operating standards | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 38 | 明娱 | ChatGPT B | A | `npc@minggames.com` | Public company/business route found during sourcing | Cross-region product, monetization and growth standards | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 39 | Vortex Gravity / 蜂有引力 | ChatGPT B | E | `business@vortexgravity.com` | Public business route; content/IP + game cooperation | Connect content traffic to product selection, monetization, LiveOps and global growth | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 40 | Baioo / 百奥 | ChatGPT B | A | `chenpingfen@aobi.com` | Public business route; IP, studios, publishing and overseas business | Common operating language across studios / regions | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 41 | XForce Games | ChatGPT B | A/E | `business@xforce-games.com` | Public business route; traditional-Chinese Web-game platform | Turn platform traffic into selection, monetization and long-term operating system | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 42 | 十万伏特 / SwiftJava | ChatGPT B | B | `business@swiftjava.com` | Public business route; self-developed casual/management products | Overseas validation + ad/IAP monetization + LiveOps + UA loop | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 43 | 趣炫网络 | ChatGPT B | A/B | `csy@q-dazzle.com` | Public cooperation route; domestic + overseas product cooperation | Upgrade project-by-project overseas publishing into repeatable self-publishing capability | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 44 | EYOUGAME | ChatGPT B | A | `weiguang.hong@eyougame.com` | Public executive/business route; multi-market mobile publishing | Common greenlight, monetization, LiveOps and regional-budget standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 45 | 上海同娱 | ChatGPT B | B | `sivan.lv@91mgame.com` | Public business route; mobile R&D/operations background | Build overseas self-publishing loop without a heavy publishing org | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 46 | 武汉掌游 | ChatGPT B | B | `liuchan@zhangyou.com` | Public product/agency/co-op route found during sourcing | Channel/agency base needs own product + global operating layer | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 47 | 蓝飞互娱 / Kunpo | ChatGPT B | A/B | `market@kunpo.cc` | Public market route; self-development, publishing and operations | Global greenlight + monetization + LiveOps + UA standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 48 | 电魂网络 | ChatGPT B | A | `bd@dianhun.cn` | Public overseas BD route; R&D, long-tail operations, esports and overseas cooperation | Unified regional GTM / monetization / LiveOps / stop-scale rules | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 49 | 中娱游 | ChatGPT B | E | `hbd@zyykeji.com` | Public business route; PC/game-distribution and venue traffic resources | Move upstream from traffic/distribution to selection, monetization and global growth | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 50 | UU898 | ChatGPT B | E | `lyp@uu898.com` | Public game-industry cooperation route | Convert channel/guild/transaction ecosystem into higher-value publishing operating layer | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 51 | 91wan | ChatGPT B | A | `denglala@91wan.com` | Public cooperation route; joint/agency operation + product cooperation | Product greenlight, monetization, LiveOps and stop/scale discipline | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 52 | 东莞畅游科技 | ChatGPT B | A/B | `union@ichangyou.com` | Public union/business route; promotion, platform, self-developed products | Shift from traffic monetization toward product/LTV/LiveOps operating depth | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 53 | ZPLAY | ChatGPT B | A/E | `contact@zplay.com` | Public developer/publishing contact route | Portfolio selection, market validation and post-launch long-tail OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 54 | 星火游戏 | ChatGPT B | B | `m15323804507_1@163.com` | Public business contact found during sourcing | R&D team needs market, monetization, LiveOps and Go/No-Go before global launch | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 55 | 草花互动 | ChatGPT B | A | `durui@caohua.com` | Public business route; game publishing/product cooperation | DD, greenlight, monetization, LiveOps, UA and stop/scale standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 56 | Boom Games | ChatGPT B | B | `business@boomgames.cn` | Public business route; boutique game R&D | Global validation / monetization / LiveOps / UA before scaling | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 57 | Mujoy / 乐都 | ChatGPT B | A/E | `bd@mujoy.com` | Public BD route; product agency + overseas channels | Move channel advantage into portfolio selection and long-tail operating system | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 58 | 盼兮网络 | ChatGPT B | A/B | `business@gzpanxi.cn` | Public business route; game publishing + social/video traffic matrix | Convert traffic strength into selection, LTV and LiveOps depth | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 59 | Revijoy | ChatGPT B | B | `business@revijoy.com` | Public Business Cooperation route; global-product R&D | Front-load market, monetization, LiveOps and UA into R&D | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 60 | 广州心玩科技 | ChatGPT B | A/B | `3366233469@qq.com` | Public cooperation route; domestic joint operation + overseas agency | Move upstream into selection, monetization, LiveOps and lifecycle | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 61 | ZQGame / 中青宝 | ChatGPT B | A | `siyang.lu@zqgame.com` | Public mobile-product cooperation route | Common global operating OS across R&D/publishing portfolio | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 62 | Ourpalm / 掌趣科技 | ChatGPT B | A | `ib@ourpalm.com` | Public business route; global game business + AI initiatives | Portfolio OS + AI workflow embedded in operating decisions | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 63 | Spiral Up Games | ChatGPT B | A/E | `hello@spiralupgames.com` | Official publishing contact; China/global PC indie publishing + funding/marketing/community | Project greenlight + commercial model + post-launch standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 64 | IndieArk | ChatGPT B | A/E | `pitch@indieark.com` | Official pitch route; China/global indie publishing | DD + commercial model + launch / post-launch operating OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 65 | Yooreka Studio / 游力卡 | ChatGPT B | A/E | `ang@yoorekastudio.com` | Public business/pitch route; PC/console indie publishing | Selection + market validation + commercial + long-tail standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 66 | VaryGaming | ChatGPT B | A | `info@varygaming.com` | Public company route; China × SEA × India publishing / AI-assisted liveops positioning | Common cross-market product, monetization and LiveOps OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 67 | Babeltime / 巴别时代 | ChatGPT B | A | `shangwuhezuo@babeltime.com` | Public business-cooperation route; long-running game R&D/operation | Product greenlight, monetization, LiveOps and global resource allocation | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 68 | 4X | ChatGPT B | A | `bd@4x.com` | Public business/product-cooperation route found during sourcing | Publishing portfolio OS across DD, monetization, LiveOps and regions | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 69 | 畅梦游戏 | ChatGPT B | A | `br@changmeng.com` | Public business route; mobile publishing / IP products | Global greenlight, monetization, LiveOps and post-launch operating standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 70 | 紫玩游戏 | ChatGPT B | A | `zengxueqin@ziwanyouxi.com` | Public business route; mobile joint operation/promotion | Product selection, monetization, LiveOps and lifecycle standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 71 | 鲨漫游戏 / Sharpman | ChatGPT B | B | `1612660955@qq.com` | Public business route; art/production services | Service → own-IP / co-dev requires product, monetization and GTM layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 72 | GameStart Studio | ChatGPT B | B | `gaimusida@gmail.com` | Public cooperation route; source licensing, original games, publishing/co-dev | Custom/technical service → own product requires validation + self-publishing OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 73 | QuietFire | ChatGPT B | B | `contact@quietfire.fun` | Public contact route; casual/puzzle self-development | Global market validation + ad/IAP monetization + LiveOps + UA | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 74 | QuickSDK | ChatGPT B | E | `lizhen@quicksdk.com` | Public business route; developer/channel SDK, attribution and ops infrastructure | Add product diagnosis / publishing / global growth as ecosystem layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 75 | 雷神加速器 | ChatGPT B | E | `BD@leigod.com` | Public BD route; game infrastructure / large gamer traffic entry | Joint game-publisher offer spanning growth, recall, segmentation and LiveOps | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 76 | BoogieGames | ChatGPT B | B | `biz@boogie.games` | Public business route; original IP / boutique R&D | Early global market, monetization, LiveOps and Go/No-Go layer | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 77 | Original Force | ChatGPT B | B | `ofinfo@of3d.com` | Official public contact; global external-development footprint | Co-dev/service → own-IP / joint product needs product-operating layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 78 | 武汉地游科技 | ChatGPT B | B | `diyougames@qq.com` | Public business route; global game-art outsourcing | External production → co-dev / own product requires product + GTM system | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 79 | Linyun Studios | ChatGPT B | B | `info@linyungame.com` | Public company contact; art + light game development/custom launch | Production capability → own product needs market/monetization/LiveOps/UA | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 80 | CGLand | ChatGPT B | B | `info@cgland.top` | Public route found during sourcing; co-dev/art/game development positioning | Co-dev → own product/publishing needs greenlight, monetization, LiveOps and GTM | **Sent / 0 / 0 / HARD BOUNCE — domain not found** | Suppress domain/route |
| 81 | RIE | ChatGPT B | B | `info@rietco.com` | Public BIZ route; global game-art / production services | Service → co-dev / own product needs product-operating layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 82 | 上海璃音网络 | ChatGPT B | B | `s-cool@163.com` | Public business route; China/Japan art, animation, 3D and AI-assisted production | Production → joint development/own product requires product + publishing OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 83 | Exigent China | ChatGPT B | B | `info.china@exigent3d.com` | Public China contact; global external-development organization | External development → co-creation / own IP needs product decision + GTM layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 84 | Leenzee / 灵泽游戏 | ChatGPT B | A | `guoxinyi@leenzee.com` | Official public business route; original AAA/PC-console development signal | Convert single-title global experience into reusable portfolio OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 85 | Wildfire Games | ChatGPT B | A | `bd@wildfiregames.net` | Official public BD route; global mobile publishing | Portfolio greenlight, monetization, LiveOps, UA and regional allocation | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 86 | Nova Games | ChatGPT B | A | `bd@novagamesltd.com` | Official public BD route; IAA/IAP/hybrid global mobile publishing | Unify soft launch, monetization, LiveOps and UA stop/scale standards | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 87 | CIPHER Games | ChatGPT B | A | `bd@cipherweb.co` | Official public BD route; self-development + global publishing + ad-growth capability | Cross-project product/monetization/LiveOps/UA operating OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 88 | Micuu Game | ChatGPT B | A | `miccuk68@gmail.com` | Official/public business route; overseas mobile publishing + localization/growth | Greenlight, soft launch, LiveOps, LTV and stop/scale across portfolio | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 89 | 紫宸互娱 | ChatGPT B | B | `imengru@jwxwh.com` | Official/public business route; senior-game-team background, publishing + UE5 co-dev | Strong R&D needs self-publishing/GTM layer upstream | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 90 | 小马游戏 | ChatGPT B | A | `lichunxiong@xiaoma.com.tw` | Official/public business route; HK/TW/JP/KR and broader overseas publishing | Portfolio greenlight, monetization, LiveOps, UA and regional allocation | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 91 | 益玩游戏 | ChatGPT B | A | `liuf@ewan.cn` | Official/public business route; agency/joint-op/UA/product introduction | Move channel advantage into DD, LTV, LiveOps and global operating layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 92 | JoySeed | ChatGPT B | B | `contact@joyseed.com` | Official/public contact route; original R&D + overseas publishing | Common product greenlight, monetization, LiveOps and UA standards | **Sent / 0 / 0 / HARD BOUNCE** | Suppress route |
| 93 | 优路互娱 / Yolo | ChatGPT B | A/E | `bd@esigame.com` | Official/public BD route; overseas games into China, localization/channel/growth | Upgrade inbound publishing into reusable two-way publishing operating layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 94 | 宇酷 / 顺网 | ChatGPT B | A | `rz.qiu@shunwang.com` | Official/public executive route; R&D + operations + global publishing positioning | Portfolio OS for greenlight, monetization, LiveOps and global resource allocation | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 95 | Grateek / LeonaSoftware | ChatGPT B | A/E | `info@grateek.com` | Official/public contact; China/Japan development, localization, overseas publishing/consulting | Make cross-market product, monetization and LiveOps standards reusable | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 96 | Permafrost Echo / 冻土回声 | ChatGPT B | E | `contact@permafrost-echo.com` | Official/public contact; Northeast-Asia indie-game ecosystem positioning | Add selection, market-entry, monetization and post-launch operating layer | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 97 | 液态喵 | ChatGPT B | A/B | `1522586912@qq.com` | Official/public contact; original IP, multi-platform/self-developed projects | Product portfolio needs unified greenlight, monetization, LiveOps and platform cadence | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 98 | 成都心辰互娱 | ChatGPT B | B | `cdxchy@cdxchy.cn` | Official/public contact; development + global publishing positioning | Early team should front-load validation, monetization, LiveOps, UA and Go/No-Go | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 99 | Hong Kong Kiwi Games | ChatGPT B | A/B | `zjy@mihoutaogame.hk` | Official/public business route; new app/game publishing + developer cooperation | New publisher needs project selection, commercial model, LiveOps and UA operating loop | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |
| 100 | Manifestart | ChatGPT B | A/E | `manifestart@163.com` | Official/public contact; China/Japan/Korea indie-game publishing/localization/PR/community | Project DD + commercial model + launch/post-launch long-tail OS | Sent / 0 / 0 / no hard bounce yet | +5d Sep24 |

## 5. Current reply state

At the end of this continuation:
- **Human replies:** 0
- **Positive replies:** 0
- **Meetings:** 0
- **Automated replies:** 1 total today, the Rayark customer-support ticket from Batch 06; it is not counted as a human reply and that route is suppressed.

## 6. Next action

1. No additional sends are required for today's 100-SENT quota; production target is complete.
2. Treat the 15% bounce rate as the top operational issue before the next high-volume run.
3. Continue sourcing a large reserve pool, but tighten route quality before transmission.
4. On Sep 24, follow up only non-bounced Sep 19 accounts that remain unanswered and still match ICP; read the original thread first.
5. Do not follow up any suppressed address without new independent verification.
