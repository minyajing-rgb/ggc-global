# GGC 全站设计 → 实施 / Fullsite V4

更新：2026-10-12。这里已包含实际前端源代码、PRD、用户流程和原始肖像/书封资源，不再只有一份交接说明。

## 快速入口
- [PRD / 页面需求与验收](PRD.md)
- [User flows / 主要用户路径及状态](USER_FLOWS.md)
- [源代码](source/)
- [原始素材](assets/)
- [构建与校验入口](prepare_site.py)
- [HTTP浏览器验收与UI导出](qa/review_http.py)
- [GitHub检查及UI产物：首次通过记录](https://github.com/minyajing-rgb/ggc-global/actions/runs/38272022771)
- 历史的 `REVIEW_HANDOFF_2026-10-12.md` 记录导入前状态；本页取代其中“新源码仅在对话ZIP”的状态说明。

## 已确认设计规范 / 不再另起设计方向

公司定位：战略前瞻、经营诊断、关键判断、资源配置与实际行动。四大业务和GGC公司品牌为主，Joyce职业经历、肖像、方法和著作是专业证据。

视觉：白底，玫红与蓝紫激光炫彩，轻薄半透明战略面板，粗黑体大字，清晰的信息层次。不是SAGA世界大厅、工程控制台或个人肖像海报。

组件：只用已批准的01 Blade、04 Outline、06 Primary Gradient、08 Tab、09 Elevated Luminous、10 Ghost。默认、悬停、按下、键盘焦点、禁用和加载必须实际可用；不能把图片中的按钮当成交互。

语言：两套独立EN/ZH页面，深层页面语言切换保持语义同页。尺寸检查至少320/390/768/1440，桌面和手机都要有可审阅长图。

素材：`joyce-approved.webp` 是用户所给海报裁切，`book-cover.webp` 为所给著作海报裁切；源文件均经SHA-256校验恢复，与已认可ZIP中的二进制一致。不得换成新生成人物。字体只有公开CSS引用和SVG轮廓，不分发字体文件。

## 页面覆盖
16类UI，48个路径/语言，共96个中英文页面：
首页、专业能力、16服务详情、研究目录、5研究主题详情、Decision OS、Joyce Method、产品目录、14产品详情、联合立项、Why GGC、著作、动态与订阅意向、联系、组件库、404。

UI中保留来源海报的Decide / Build / Compound、七个经营模块与七步流程。书页主题保留给定海报的组织。研究详情是方法/主题说明，产品画廊是说明图，不冒充未提供的真实报告或App截图。

## 构建 / 给Codex及后续开发

从仓库根目录运行：
```sh
python corporate/fullsite-v4/prepare_site.py --out /tmp/ggc-fullsite --stage /tmp/ggc-fullsite-source
python -m http.server 8080 --directory /tmp/ggc-fullsite
```

打开 `/review.html` 查看全部UI；`/zh/index.html` 和 `/en/index.html` 为双语首页。

`prepare_site.py` 从既有已审阅的 `corporate/implementation/src/` 复用基础内容和交互，再叠加新全站模板。它核对14份来源文件/素材哈希，不静默换掉旧素材。后续有意更改已批准内容时，必须在PR说明中记录并更新相应校验基线，而不是删除检查。

后续代码入口：
- `source/build_fullsite.py`：页面构建、深层实例、内容组织。
- `source/fullsite.css`：全站页面和各类详情布局。
- `source/fullsite.js`：画廊、动态意向草稿、评审状态。
- `corporate/implementation/src/`：已审阅职业/服务基础、六款按钮、主导航/表单交互。

## 当前真实实施状态

- GitHub源代码已入库；原始WebP已由通过的CI恢复为正常文件，base64传输分片已删除。
- GitHub Actions `38272022771` 成功：在真实HTTP服务上用Chromium检查页面、图片、导航、筛选、画廊、表单和响应式，并导出64张代表性长页、4张状态图、16类总览、32页评审PDF及可运行包。
- 已把同一份已校验前端激活到既有Base44 `ggc-global` 开发路径 `/ggc-next/`，总览为 `/ggc-next/review.html`。
- 激活后109个HTML/CSS/JS/SVG/WebP通过HTTP200和字节一致校验；旧根首页与 `CNAME=biz.ggcgames.com` 未变。
- Base44变更前恢复点：`6accfa8a1de1b2870eb4eb3e`；变更后：`6acd012dd6d374067c9932bf`。
- `/app/ggc-next-pre-fullsite-v4/` 保留上一个开发预览。

Base44 路径仍是开发预览。正式站已于 2026-10-13 切至独立的 [ggc-corporate-site](https://github.com/minyajing-rgb/ggc-corporate-site) GitHub Pages 发布仓库，通过阿里云 DNS 绑定 [ggcgames.com](https://ggcgames.com/) 并启用 HTTPS。发布工作流固定从本 PR 已检查的 commit 构建，不从开发预览复制文件。

## UI mockups与证据

首次CI产物名：`ggc-fullsite-v4-ui-and-implementation`，含UI评审PDF、全站源代码/网页/截图包、总览和review.json。Actions产物有保留期限，UI可以从同一版本源码重建；后续导出也由工作流统一完成。

PDF中的每张页面是实际HTML浏览器渲染而非再生成的概念图。离线字体回退和实际用户字体可能不同；视觉验收不等于正式站点的跨设备字体一致保证。

## 当前发布状态与后续工作

1. 正式站已上线，根目录、中英文页面、HTTPS、sitemap、404及公开资源已通过独立线上扫描。原 Netlify/Bolt 内容未删除；阿里云 DNS 全记录导出已保存，邮箱、`biz` 与 `opsgo` 记录未改。
2. 当前正式站的联系与动态入口仍只生成访客自行发送的邮件草稿。2026-10-13 新增可选的 FormSubmit 商务询单构建模式，必须待邮箱持有人激活并完成真实收件测试后，发布工作流才可启用 `--inquiry-endpoint`。这只处理商务询单；动态订阅、双重确认、退订和 CRM 仍未接通。
3. 真实产品截图、可公开原研究与案例证据，按授权补齐，不用虚构内容填空。
4. 隐私页已描述当前前端流程；正式运营主体、托管与邮件日志、保存和删除安排仍需运营方核实。启用新询单模式时，构建器同步切换联系页及隐私页说明。
5. 视觉最终验收仍由 Joyce 在正式域名上确认。代码检查和线上路由扫描不代替主观设计认可。

原资料里的愿景与产品组合仍是内容依据；其中个人灵性材料没有被换写成企业科学验证结论。
