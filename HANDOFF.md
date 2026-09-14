# GGC 人设与年度客户开发交接

更新：2026-09-14；基线：main / dbb0faa。范围：本次定位与技能文档；没有改应用代码。

## 已完成

- 按 Joyce 最新要求明确游戏经营者、GGC创始人的定位及证据使用边界。
- 建立 sourcing、pitch、connect、展示、成交 skill，重点补齐买方分析、话题、案例、分工和采购推进。
- README 加入入口；人设归本公开库，新媒体平台执行归 `minyajing-rgb/newmedia`。

## 剩余问题

- 实际客户资格、预算、现任负责人、全渠道去重、提案、签约及回款需回到私有CRM核验。本次没有外发或成交。
- 部分历史履历数字口径不同，不能直接复用；/joyce和出版社页本轮抓取失败。
- 公开存档图片尚未逐图复核成发送包；网站、社交个人页、全局安装和定时执行均未在本次修改。
- 下一步按具体账户补证据和相关展示资料，再推进已获授权动作。

## 关键架构决策

公开定位与可复用流程分开于私人客户资料；不复制销售名单、合同、内部目标和敏感案例到本库。使用远端最新main作为提交基线，保留本地历史分叉。本地旧库有独立提交，未合并或强推。

## 变更文件

- `positioning/JOYCE_PERSONA.md`：人设、证据和使用边界。
- `skills/ggc-annual-client-development/SKILL.md`：客户开发入口。
- `skills/ggc-annual-client-development/references/connect-to-close.md`：需求、展示和采购推进。
- `skills/ggc-annual-client-development/agents/openai.yaml`：调用元数据。
- `README.md`、`HANDOFF.md`：入口与交接。

## 测试状态

校验通过：`quick_validate.py`（skill结构）、YAML解析、全部文档相对链接与交接长度检查；交接按每个汉字一单位保守计数仍少于1500。人工场景复核覆盖未知预算、已有关系、明确需求与私有材料边界，尚未实战验证成交效果。没有应用代码变更，未运行应用测试。提交与远端文件内容逐一核对后方可报告同步成功。
