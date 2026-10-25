# GGC 主站部署与域名切换 / Read-only baseline

2026-10-12。本记录来自当前公共DNS解析与HTTP读取。没有登录或改写阿里云，没有修改DNS、现有生产页面或邮箱。公共查询不是阿里云完整区域导出，切换前仍需授权导出。

## 实测现状

| 名称 | 记录/响应 | 意义 |
|---|---|---|
| ggcgames.com | NS dns31.hichina.com / dns32.hichina.com | 阿里云DNS管理体系 |
| ggcgames.com | A 75.2.60.5；TTL 600 | 当前主域名目的地址，先保留 |
| www.ggcgames.com | CNAME site-dns.bolt.host；TTL 600 | 现有Bolt关联的DNS入口 |
| biz.ggcgames.com | CNAME minyajing-rgb.github.io；TTL 600 | 独立GitHub Pages商务站，保留 |
| opsgo.ggcgames.com | A 216.24.57.1；TTL 600 | 独立内容站，保留 |

HTTP读取：
- `https://ggcgames.com/`：200；Server: Netlify；title: GGC Games - AI赋能全球化游戏化商业化战略。
- `https://www.ggcgames.com/`：最终跳转至 `https://ggcgames.com/`，200，Server: Netlify。
- `https://biz.ggcgames.com/`：200，Server: GitHub.com；title: Joyce Mi · Global Game Copilot。
- `https://opsgo.ggcgames.com/`：200，title: Game Ops Hub。

## 必须保留的邮件记录

当前公开MX返回：
```
1  mxw.mxhichina.com.
1  mxn.mxhichina.com.
5  mx1.qiye.aliyun.com.
10 mx2.qiye.aliyun.com.
15 mx3.qiye.aliyun.com.
```
SPF TXT：`v=spf1 include:spf.qiye.aliyun.com -all`

不得在官网切换时整理/删除这些记录；DKIM、DMARC和验证TXT需要在完整DNS导出中核对。禁止整区覆盖导入、Nameserver迁移、批量清理及修改无关子域。

## 建议部署路线

**先复用现有Netlify/Bolt托管项目。** 阿里云负责域名解析，不等于需要新增阿里云服务器。现有主域A记录与实际Netlify响应相符；若新版本发布到同一个受控Netlify站点，可能无需更换主域解析。必须先核实用户拥有的站点ID、现有域名绑定和发布权限，不能仅凭公共DNS猜站点配置。

工具分工：GitHub保存设计/PRD/源代码，GitHub Actions负责构建与浏览器检查，现有Base44负责开发预览，既有Netlify/Bolt负责正式托管，阿里云只做经核对的DNS记录管理。

已连接Vercel读取没有返回可用team scope，未建立新项目。插件目录没有返回Netlify专用插件，因此其授权访问需使用用户确认的浏览器会话，而非假称已连接。不会为此自动购买服务。

## 用户需要完成的事

1. 在已提供的可连接浏览器登录阿里云、完成验证码并保存profile。仅在用户窗口输入凭据，不在聊天发密码或验证码。
2. 原Netlify/Bolt站点需一次账号/项目发布授权。没有该权限，仅能检查DNS，不能声称已经接管旧站。
3. 产生额外费用、迁移现有服务或遇到非预期权限时停止，向用户确认。

私有登录handoff地址、cookies、验证码及API密钥绝不写入仓库。

## 上线执行顺序

A. 导出完整DNS与现有生产部署回滚信息；保留源值及TTL。
B. 关联已确认GitHub工程/明确构建目录；先建立独立部署预览，检查96页面、双语深链、图片、主CTA、404及HTTPS。
C. 从前端预览中单独处理正式SEO、隐私、表单交付边界。尚未接CRM/订阅时，保持“邮件草稿/订阅意向”，不伪装成功。
D. 在托管平台核实root/www绑定，读取其实际要求。只在确有需要时修改对应web记录；不猜CNAME目标，不动mail/biz/opsgo。
E. 验证root/www跳转、TLS、代表性深层页面、资源加载与旧子站；发现故障立即回滚到保存的部署/记录。

当前：全站前端已导入并激活Base44开发预览，CI浏览器检查通过；正式域名发布等待认证与目标项目核实。

## 官方操作参考
- Netlify external DNS: https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/
- Alibaba Cloud DNS record management: https://www.alibabacloud.com/help/en/dns/pubz-manage-resolution-records

官方通用文档是操作依据，不替代当前账号中的实际DNS记录和站点目标值。
