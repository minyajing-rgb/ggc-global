# 2026-10-12 职业页面文案收敛与公司官网区分

本轮按Joyce要求只修介绍和多余内部说明，保留原设计。事实更正继续有效，不恢复错误Lead Producer职称，不重发历史商务邮件。

## 实际修订与发布

`f3ac23aed4bbae51d219032b3632bebef205df4d` 只改个人站两个HTML入口及两个生成脚本的文案：

- Zynga证明卡恢复CityVille / FarmVille / Arcade产品名，保留产品经理与带领多位制作人。
- 职业详情直接写CityVille腾讯版、FarmVille中文版和全球Bubble / Ruby / Slingo经营商业化主责；保留Gameloft亚洲区运营负责人及已确认项目范围。
- 去掉此前过长的dated-career / 独立Thor2核验说明，完整职业底稿不删。
- 没有改CSS、JS、SVG、肖像、Logo或布局。

[实际发布与复测run 38251963578](https://github.com/minyajing-rgb/ggc-global/actions/runs/38251963578) 对真实HTTPS执行56项检查，全部通过。实际抓取 `https://biz.ggcgames.com/` 与 `/joyce/` 均200，HTML字节相同，SHA-256 `11c1986748f508241f17bf52b602dbd76be34967df984e36eab36d636053f731`；实际浏览器展开中文职业正文，PM带队、五款Zynga产品及Gameloft职位/范围核对通过。GitHub提交之外，已经取得本轮窄修订的真实线上证据。

## 页面不是同一个产品

蓝紫色GGC公司官网在PR #11和已有Base44 `/ggc-next/` 开发路由。紫金色、Joyce肖像主视觉的页面是biz职业站；两套页面不可在交付说明中混为同一版。

公司站只改访客文字，原CSS/JS/SVG逐字节保持。最终测试源码 `7765e325`，18页面/126布局/1106检查全部通过；Base44 24个资源HTTP200且字节等于构建；公司站正式主域名没有切换。

完整公司站Product Review、状态矩阵、缺陷表、上线Checklist与发布边界保存在[PR #11](https://github.com/minyajing-rgb/ggc-global/pull/11) 的 `corporate/implementation/qa/COPY_PRODUCT_REVIEW_2026-10-12.md` 等五份证据文件。全生产目标仍NOT_READY，不把开发预览改好当作ggcgames.com上线。

## 仍未更新的线上内容

- `https://ggcgames.com/` 是独立旧站。本轮浏览器实际渲染页面仍见首页/关于/经验/页脚的“北交所上市”，与最新母稿不一致；500+、排名、收入等旧口径需逐项处理。本轮没有切换或重新设计它。SPA初始HTML没有命中某段文字并不等于渲染页面没有。
- `https://opsgo.ggcgames.com/joyce/` 返回200，但没有取得可验证的职业正文，不能宣称资料已同步。
- 历史4YFN等外部已提交资料保留原始发送记录及纠正提示，外部主办方页面未直接修改。
- 蓝紫色公司官网的ggcgames.com正式版本尚未部署，API/CRM/订阅/产品详情/素材与正式域名全流程验收仍有缺项。

事实依据仍为Joyce本人2026-10-12说明、v5逐项目母稿与同日新增v7母稿；不因文案缩短削弱旗舰主责，不补写未经确认的职级、排名和财务口径。
