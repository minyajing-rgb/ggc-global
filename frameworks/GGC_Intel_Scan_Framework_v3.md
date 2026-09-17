# GGC每日全球游戏×AI产品情报扫描框架 v3.0
> 版本：v3.0 · 2026-09-17 · Joyce确认版
> 定位：GGC全球情报系统的执行标准——榜单直拉、新品核实、全板块覆盖、内容与BD双输出

---

## 一、扫描目标

1. **新品/黑马优先**：只深挖上线≤6个月且经iTunes API核实releaseDate的新产品
2. **头部公司动态**：大厂新品、收购融资、人事战略
3. **AI产品榜**：AI陪伴/身心灵/社交赛道单独成榜（a16z + Appfigures）
4. **输出双通道**：内容素材（星球/LinkedIn/群）+ BD线索（付费能力信号）

---

## 二、13个板块（12大类+AI产品榜，不可删减）

| # | 板块 | 核心数据源 |
|---|------|-----------|
| 1 | SIMS模拟经营 | 美区游戏畅销/免费榜API、AppMagic |
| 2 | ARCADE/Merge | 同上 + sort/puzzle新品观察 |
| 3 | 休闲小游戏/H5/微信小游戏 | 抖音小游戏榜、微信小游戏畅销榜、行业新闻 |
| 4 | AI身心灵/陪伴/冥想/玄学 | 健康类目畅销榜API、Appfigures AI陪伴收入榜、AI社交新品 |
| 5 | Casino（Social Casino+Sweepstakes/iGaming） | 畅销榜、sweepstakes新平台动态、监管新闻 |
| 6 | AI（AI游戏/AI工具/AI提效） | a16z Top 100、App Store新品、发布会动态 |
| 7 | Steam平台 | SteamDB、周新品数据 |
| 8 | 手游平台 | 美区+多地区免费/付费/畅销三榜API |
| 9 | 各地区渠道 | 东南亚/中东/日韩/拉美市场报告 |
| 10 | H5/Web/云游戏 | 行业新闻 |
| 11 | 公司动态 | mobilegamer digest、36kr、白鲸 |
| 12 | 会议与热点 | TGS/GDC/Gamescom/ChinaJoy/Apple keynote |
| 13 | **AI产品榜（新增）** | a16z Top 100 Gen AI Apps、Appfigures AI陪伴收入榜、Sensor Tower AI子品类增速 |

---

## 三、扫描方法（v2 · 榜单直拉优先）

```
第一层：Apple RSS API直拉（实时，免key）
  畅销榜：itunes.apple.com/{us/jp/gb/kr}/rss/topgrossingapplications/limit=30/genre=6014/json
  免费榜：同路径 topfreeapplications
  付费榜：同路径 toppaidapplications
  身心灵：genre=6013（健康）/ 6015（Entertainment）
  交叉核实新品：itunes.apple.com/search?term={产品名}&country=us&entity=software → releaseDate字段

第二层：发布线新闻（mobilegamer新品digest每周五、Apple keynote、TGS/GDC动态）

第三层：AppMagic/Sensor Tower周报交叉验证（Google Play侧）
```

**Google Play说明**：沙盒环境连不上Play商店，Play侧数据用AppMagic/Sensor Tower周报补。

---

## 四、新品核实铁律

1. 新品 = 上线≤6个月 + iTunes API核实过releaseDate，未核实禁止标NEW
2. 黑马 = 核实为新品 + 快速冲进地区榜头部；老产品排名复涨不算黑马
3. Voodoo类换皮产品不拆
4. 三方老产品不进内容排期（Joyce亲历职业案例除外）
5. 大厂新品发布线（digest/keynote）每周固定收割一次

---

## 五、输出格式

**早报（08:30 → Joyce TG）**：每条信号=产品名+关键数字+一句话GGC判断，禁提来源与过程
**深度文章（每日1篇）**：星球中文深度版 + LinkedIn英文版，六维拆解（冷启动/创意来源/立项/团队/变现/上下游）
**群分发**：身心灵群精简版、Casino群对应品类版
**BD信号**：黑马团队 → BdLead入库（公司+产品+流水/下载+为什么疼+开场白）

---

## 六、BD联动：拆解即BD

- 每天深拆的新品 = 潜在百万年框客户的内容敲门砖
- 触达路径：星球/LinkedIn深度拆解 → "我拆了你家产品，三个结构性问题"私信/邮件 → Project Review ¥10,000 → 年框提案（base+增量分成）
- 客户画像：月流水$3M+出海团队 / 融资到账90天内 / 现金流充沛Casino/Web3团队
- 决策人：CEO/实控人

---

## 七、发布线数据源清单（每周固定收割）

| 来源 | 频率 | 内容 |
|------|------|------|
| mobilegamer.biz new game digest | 每周五 | 全球新品/软启动/上线日历 |
| Apple keynote | 季度 | 大厂合作新品首发 |
| TGS/GDC/Gamescom | 会期 | 展会新品与行业信号 |
| 36kr/白鲸/扬帆出海 | 每日 | 中国团队出海动态 |
| Appfigures AI陪伴收入榜 | 月度 | AI陪伴赛道收入Top |
| a16z Top 100 Gen AI Apps | 半年 | AI消费产品全景 |
