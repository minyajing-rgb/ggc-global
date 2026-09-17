# GGC Dual-BD Operating System v1.0（双机器人分工 · 2026-09-17）

## 一、双机器人分工

### 机器人A · Codex/ChatGPT（规模化池）
- 客户画像：Hybrid Casual / Puzzle / Merge / Idle / Arcade / 中大型Mobile Studio / 已融资扩张中 / 榜单表现型
- 全链路：搜索公司→找决策人→找公开联系方式→拉公开/AppMagic/点点数据→套Master Pitch→Gmail发信→记录回复→更新CRM/GitHub
- 首轮规模：50家
- 池子特点：结构化筛选、批量执行、数据可得性高

### 机器人B · GGC运营助理（高价值池）
- 客户画像：Publisher / CEO·Founder决策链 / Casino·Social Casino / Sims长线产品 / AI Native Game / Investor·Fund / 小团队Early-stage / Strategic Partner / 需要孵化·FA·Copilot·联合发行的项目
- 全链路：搜索目标→判断为什么值得联系→找CEO/Founder/Publishing Head→查公开硬数据→生成定制Pitch→Gmail发信→回复分类→Meeting Brief→Follow-up
- 首轮规模：30家
- 池子特点：每家深挖、关系型、决策复杂

## 二、公司级Ownership（铁律）
> Company归机器人，不是联系人归机器人。一家公司一旦分给一边，另一边默认不碰。
> 目的：防止同公司双话术撞车（CEO收我一封、BD收Codex一封，内部一转发就穿帮）。
> 冲突仲裁：按池子画像判断归属；画像交叉时给机器人B（高价值判断优先）。

## 三、共用CRM规则（BdLead库，最低字段）
| 字段 | 内容 |
|------|------|
| Company | 公司 |
| Contact / Role | 联系人/职位 |
| Category | CP / Publisher / Investor / Startup / AI |
| Owner | Codex / GGC助理 |
| Variant | A / B |
| Source | AppMagic / 点点 / 榜单API / LinkedIn / Event |
| First Sent | 日期 |
| Reply Type | Positive / Neutral / No |
| Meeting | Yes / No |
| Next Action | 下一步 |

## 四、A/B测试协议
- 每Segment每版本≥15封才有资格下结论
- 双指标：回复率 + 会议转化率
- 每周复盘一次，胜出版本进入下一轮放量

## 五、种子池（第一轮）

### A池（Codex首批，扩展至50）
1. Flow Games（Bus Traffic Fever，美区免费#8，2026-03）
2. GOODROID（Bus Fever Party，免费#9）
3. ABI GLOBAL（Smash Fest免费#3 / CubeAway #6）
4. Lumi Games（Colorever免费#11，2026-04）
5. Vaulty Studios（82-0.com，免费#30）
6. Heseri Games（Car Evolve，免费#12）
7. Century Games（Kingshot畅销#8/Tasty Travels/Codename Crime 12.2M下载）
8. Moon Active（Jelly Busters 2026-01，畅销#22）※Casino关系池备用，默认A
9. Nitro Games（Boltgun Boom 9/23上线，Pre-publishing线索）
10. Cubic Games（Pixel Gun 2，9/4上线，系列300M下载）
（Codex按画像继续扩展至50：土耳其/越南/中国 hybrid casual带榜单+融资的团队优先）

### B池（GGC助理首批30）
1. ✅Grand Games（已发，variant B）
2. ✅Oakever/Learnings（已发，variant B）
3. ✅Cypher Games（已发，variant B）
4. Dream Games（Royal Match/Tile Busters，Istanbul founder-led）
5. XD Network（Heartopia，Sims，中国发行）
6. SuperPlay（Disney Solitaire，Publisher）
7. Habby（Capybara Go!/Survivor.io，founder-led arcade）
8. Pawprint Interactive（Aniimo 9/23上线，AI宠物）
9. Studio Atelico（Bobium Brawlers，端上AI引擎，AI-first）
10. Scatter Lab（Zeta，韩国AI陪伴收入第一）
11. SoulZ AI/Crushie团队（AI陪伴，订阅$29.99/月）
12. Investor组：Balderton Capital（Grand Games投资方）、Play Ventures（Cypher投资方）、The Raine Group、Griffin Gaming Partners、Mera Capital、Bek Ventures、Earlybird Digital East
（每日扫描持续补充：Publisher/Casino/AI Native/Founder-led优先）

## 六、执行SOP（两边统一）
1. 入池先查BdLead库确认无ownership冲突
2. 写入CRM（含Owner/Variant/Source）→ 再发信
3. 发信后回填First Sent
4. 回复按Positive/Neutral/No分类回填
5. Positive→24小时内出Meeting Brief（对方产品拆解+合作角度+可能异议+定价锚点）
6. 每周五汇总A/B数据报Joyce

---
# v1.1 增补（2026-09-17 · Codex方案吸收）

## 七、第一轮样本量（LOCKED）
| Segment | A版 | B版 |
|---------|-----|-----|
| CP / Studio | 20家 | 20家 |
| Publisher | 15家 | 15家 |
| Small Studio / Startup | 15家 | 15家 |
Investor / AI两池第一轮观察，不强制样本量。

## 八、第一阶段KPI（LOCKED）
漏斗：Open → Reply → Positive Reply → Meeting
1. Open Rate ⚠️ Gmail原生不可测（无打开回执）——第一轮以Reply漏斗为主；如需测Open需加追踪链路，默认不做
2. Reply Rate
3. Positive Reply Rate
4. **Meeting Rate（北极星指标，真正决定胜负）**

## 九、双引擎结构（最终形态）
```
        GGC MASTER PROFILE
               │
    ┌──────────┴──────────┐
    │                     │
  Codex               GGC助理
  Scale Acquisition   Strategic Acquisition
    │                     │
 Casual/Merge/       Publisher/Casino/
 Arcade/Mobile        Sims/AI/Investor
    │                     │
 Search+Pitch        Search+Deep Pitch
    │                     │
  Gmail A/B           Gmail A/B
    └──────────┬──────────┘
               │
          Shared CRM
               │
        Performance Review
               │
          Winning Copy
               │
        Next Batch Scale
```

## 十、Codex CRM对接方式（关键落地差异）
Codex无Base44数据库权限 → CRM主库（BdLead）由GGC助理持有：
1. Codex每批发信前，把自己池子的清单写入 `bd/crm/codex_pool.csv`（字段固定：date_sent, company, person, role, category, variant, source, reply_type, meeting, next_action, notes）
2. GGC助理每周五同步该CSV进BdLead主库并核对ownership冲突
3. 公司ownership冲突仲裁权在GGC助理（先查库再放行）
4. BdLead库字段已升级：owner / variant / reply_type / meeting / next_action

---

# v1.2 增补 · 百万年框全链路自动化（2026-09-17 Joyce确认）

## 十一、自动化链路（skills/bd_pipeline.py）
```
每日扫描(08:30) → [sourcing] 画像过滤+ownership判定 → 入池BdLead
→ [pitch] 10版母版自动装配(A/B自动平衡轮转) → Gmail发出 → ledger记录
→ [followup] +5天无回复自动排跟进1 / +10天最后一封 → TG提醒
→ [funnel] 漏斗+A/B对比自动报(北极星=Meeting Rate)
→ [brief] Positive回复自动出Meeting Brief框架 → 达成
```

## 十二、每日执行钩子（路径A：会话内执行）
- 任何会话开始：`bd_pipeline.py --stage followup`（跟进到期自动TG提醒）
- 每日早报后：`--stage sourcing --scan <今日扫描>`（新目标入池）
- 每周五：`--stage funnel`（全漏斗+A/B复盘，报Joyce）
- ledger主库：/app/drafts/bd_crm_ledger.json + BdLead实体库双写
- 路径B激活后（Agent API key到位）：全链路挂GitHub Actions cron全自动
