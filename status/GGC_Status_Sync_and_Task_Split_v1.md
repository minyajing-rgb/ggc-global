# GGC增长引擎 · 状态同步与分工需求 v1.0
**日期：2026-09-17 ｜ 作者：GGC运营助理 ｜ 用途：状态同步GitHub + 把可外包部分规格化给ChatGPT/Codex承接**

---

## 一、当前状态总览

### 1. BD管道（百万年框获客）
| 目标 | 状态 | 关键数据 | 下一动作 |
|------|------|---------|---------|
| Grand Games（Istanbul） | ✅ Pitch已发（9/17 Gmail→bekir@grand.gs） | Block Out!美区免费#1+畅销#20；$103M总融资，$70M B轮刚到账 | 5-7天无回复→co-founders Mustafa/Mehmet第二波 |
| Oakever/Learnings | ✅ Pitch已发（yiwei@oakevergames.com） | Meowdoku $200K/天≈$6M/月，免费榜#1，三款进Top25 | 同上 |
| Cypher Games | ✅ Pitch已发（anil@cyphergames.com，地址有佐证） | Royal Smash 2026-06-30上线免费#14；$30M A轮 | 同上 |

- Pitch v3结构（已锁定）：现象钩子+过去成绩+「知道答案但不写邮件」+30分钟CTA，禁止给具体方法论
- 材料：GitHub `bd/` 目录（中英文one-pager+3家定制pitch+邮件模板）
- 代码库：BdLead数据库3条记录，含高管名单与发送状态
- 待解：Gmail无readonly权限→弹回与回复需人工盯；如要自动化需追加授权

### 2. 内容自动化（六档位）
- 每日：08:30早报/08:56 deepdive批次/09:00一三五公司主页/10:00 LinkedIn+首评/13:00午篇/20:00晚篇
- 双星球：GGC出海实战（深度1篇/天）+ Joyce游戏运营（标准2篇/天），节假日停发（中秋9/25、国庆10/1-8）
- 发布链路：当前走「会话内补发」路径A；路径B（GitHub Actions→Agent API全自动化）文件已备好（`/app/drafts/ggc_external_trigger.yml`），等Agent API key激活
- 新品队列已排到12月：DAVE THE DIVER（9/17当天已拆）、Pixel Gun 2（9/22）、Boltgun Boom（9/23）、Aniimo（9/26）、Pusheen's Place（10/1）、Transformers（10/15）、MH Outlanders（12/15）

### 3. 基础设施
- GitHub主库：minyajing-rgb/ggc-global（框架/BD材料/定位文档/deep dives 237篇）
- 发信：/app/email_send.py（Gmail，已测试通过）
- 通知：/app/tg_send.py（Telegram HTML）
- 扫描：intelligence_scan.py（13板块+实时榜单API+releaseDate核实铁律）

---

## 二、分工方案：ChatGPT/Codex 可承接的部分

> 评估结论：ChatGPT能做「文字生产+结构化研究+格式转换」类任务；不能做「需要工具权限」的事（发邮件、拉实时API、写数据库、推GitHub）。以下任务全部按无工具权限设计，Joyce把本节复制给ChatGPT即可开工。

### 任务C1 · BD跟进邮件序列（3家×2封）
- **输入**：GitHub `bd/GGC_Pitch_Email_{GrandGames,Oakever,Cypher}_Instance.md`（第一封已发）
- **输出**：每家2封跟进邮件（发送窗口：+5天第一封跟进、+10天最后一封），英文，每封<120词
- **规格**：跟进邮件不得重复第一封内容；第一封跟进=补一个新硬数字钩子（如榜单新变化）+重申30分钟CTA；最后一封=「窗口期快过了」式收尾，礼貌退场+留门
- **验收**：无方法论泄露（不解释怎么修）、无推销腔、每封开头是对方产品的具体数字

### 任务C2 · 第二波触达对象情报卡（每家1页）
- **输入**：BdLead库已知高管名单（Grand: Mustafa Fırtına/Mehmet Çalım；Cypher: Burak Taban/Batuhan Şakarcan；Oakever: 待补）
- **输出**：每人1张情报卡：LinkedIn URL、背景（前公司/擅长领域）、对外言论风格、与pitch的关联角度（技术线→AI-native内容供给角度；运营线→LiveOps节奏角度）
- **规格**：信息只来自公开来源（LinkedIn/媒体采访/播客），每条注明来源；查不到的写「未找到」，禁止推测
- **验收**：Joyce可直接照卡发LinkedIn连接请求，无需再查资料

### 任务C3 · 新目标流水线预热（每周5个）
- **输入**：GGC情报扫描框架 v3.0（GitHub `frameworks/GGC_Intel_Scan_Framework_v3.md`）+ 每日早报的目标候选
- **输出**：按百万年框画像（月流水$3M+/起飞期/没打过全球仗/近期融资）筛5个新目标/周，每个输出：公司名、产品+硬数据、画像匹配度（高中低）、建议切入点（一句现象钩子）
- **验收**：Joyce圈定后我方48小时内出定制pitch（按v3结构）

### 任务C4 · LinkedIn连接请求文案（批量）
- **输入**：任务C2/C3的目标名单
- **输出**：每人1条连接请求文案，英文，<300字符（LinkedIn上限），对方产品硬数字开头+一句身份+不推销
- **验收**：格式对照已验证有效的3条（见`bd/`目录TG记录）风格

### 任务C5 · 内容翻译与改写
- **输入**：星球中文深度稿
- **输出**：LinkedIn英文版（800词+，crisp-hook校验：硬数字开头/verdict行/store产品+价格CTA）
- **验收**：通过content_quality_gate英文规则

---

## 三、GGC运营助理保留的部分（需要工具权限）
1. Gmail实际发送（含发送后状态写回BdLead库）
2. GitHub推送与状态同步（本文件即首次同步）
3. 实时榜单拉取（Apple API）+ releaseDate核实
4. 星球/LinkedIn/企业微信/Telegram发布与档位执行
5. 数据库读写（BdLead/LinkedInPost/TopicStatus）

**协作接口**：ChatGPT产出物统一由Joyce丢回本会话，我做事实核查（数据口径/榜单排名）→ 通过则入库/发送。ChatGPT禁止直接产出对外数字，所有数字以我方核实为准。

---

*v1.0 · 2026-09-17 · 状态与分工以本文件为基准，每次重大变更更新本文件并升版本号*
