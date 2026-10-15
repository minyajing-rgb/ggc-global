"""Overlay the expanded-book guide on the two existing book pages."""
from pathlib import Path
import html

BOOK='https://biz.ggcgames.com/book/'

def button(label,url,number='04'):
    return f'<a class="ggc-btn" data-button-id="{number}" href="{html.escape(url,quote=True)}"><span class="btn-label">{label}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg></a>'

def guide(loc):
    x=lambda zh,en:zh if loc=='zh' else en
    url=BOOK+f'?lang={loc}&utm_source=ggc_corporate&utm_medium=website&utm_campaign=ops101_launch'
    topics=[('看全产品经营','See the whole business','连接体验、产品、数据与经营贡献，明确判断依据和责任。','Connect experience, product systems, data and economics with evidence and ownership.'),('做对阶段判断','Match decisions to stages','原型、测试、发布与长线经营，各自有适合的投入条件。','Define suitable investment conditions for prototypes, tests, launches and ongoing operations.'),('推进AI交付','Bring AI work to delivery','从需求、来源与工具，到成品、人工验收和修订。','Connect requirements, sources and tools to artifacts, human acceptance and revision.')]
    cards=''.join(f'<article class="card"><h3>{x(a,b)}</h3><p>{x(c,d)}</p></article>' for a,b,c,d in topics)
    paths=x('运营、制作与发行负责人：第1–4章 → 第10–15章。<br>创始人、产品负责人及出海团队：第3–4章 → 第5–9章 → 第12–15章。<br>AI产品实践者：第1–4章 → 第16–19章 → 第20–22章。','Operations, production and publishing leads: Chapters 1–4 → 10–15.<br>Founders, product leads and global teams: Chapters 3–4 → 5–9 → 12–15.<br>AI product practitioners: Chapters 1–4 → 16–19 → 20–22.')
    return f'''<section class="section book-expanded" id="expanded-ebooks"><div class="shell">
<div class="section-head"><div><p class="eyebrow">{x('中英文完整电子书 · 导读与试读','COMPLETE ENGLISH & CHINESE EBOOKS · GUIDE & PREVIEW')}</p><h2>{x('经典重制 + AI Native<br>全球游戏经营实践版','A remastered operating playbook<br>for the AI-native era.')}</h2></div><p>{x('Joyce Mi / 艾小米从原始素材重新梳理完整经营结构，加入近期AI实践。英文版面向国际读者编辑表达与背景。','Joyce Mi rebuilds the operating structure from the original material and adds current AI practice. The English edition is edited for international readers.')}</p></div>
<div class="grid g3">{cards}</div>
<div class="book-reader-path"><h3>{x('适合谁读，从哪里开始','Who it is for—and where to start')}</h3><p>{paths}</p></div>
<div class="book-delivery"><p>{x('6部分 · 24章计划目录 · 144小节。开篇与前四章可免费试读；完整书稿正在完成。','Six parts · 24 planned chapters · 144 sections. Read the opening and first four chapters free; complete manuscripts are in development.')}</p><p>{x('拟定方案（待确认）：英文版 US$19.99 · 中文版 US$19.99 · 中英两本套装 US$29.99；拟于2027年1月31日交付完整EPUB。最终价格、交付及退款条款确认后再开放预售。','Proposed terms, pending confirmation: English US$19.99 · Chinese US$19.99 · English + Chinese bundle US$29.99; proposed complete EPUB delivery on 31 January 2027. Preorders will open after pricing, delivery and refund terms are confirmed.')}</p><p>{x('当前付费结账尚未启用。点击进入导读、完整目录、版本选择与试读。','Paid checkout is not enabled yet. Open the reading guide, complete outline, edition choices and previews.')}</p></div>
<div class="actions">{button(x('查看新版电子书导读与试读','Explore the expanded ebook editions'),url)}{button(x('阅读前四章试读','Read the four-chapter preview'),url+'#preview','06')}</div>
<div class="book-print-note"><h3>{x('中文纸书原版推荐','Original Chinese print recommendation')}</h3><p>《游戏运营与出海实战：策略、方法与技巧》 · {x('艾小米 著 · 机械工业出版社','By 艾小米 / Joyce Mi · China Machine Press')} · ISBN 978-7-111-75037-6</p><p>{x('适合纸上标注与团队共读原版体系。新版电子书由GGC销售，订单不含纸书，也不承诺原版读者自动免费升级。','For annotation and shared reading of the original framework. New ebooks are sold by GGC; ebook orders do not include print copies or automatic upgrades from the original edition.')}</p><a href="https://ebooks.cmpbook.com/detail?id=26372">{x('查看出版社原书介绍','View the publisher’s original-book listing')} →</a></div>
</div></section>'''

CSS='''.book-expanded .book-reader-path{padding:30px 0;margin-top:20px;border-top:1px solid rgba(80,55,90,.18)}.book-expanded .book-reader-path p,.book-expanded .book-delivery p,.book-expanded .book-print-note p{max-width:900px;line-height:1.8}.book-expanded .book-delivery{padding:24px 28px;border-left:1px solid #77509e;background:#f4eff7;margin-bottom:25px}.book-expanded .book-print-note{padding-top:30px;margin-top:32px;border-top:1px solid rgba(80,55,90,.18)}.book-expanded .book-print-note a{color:#6940aa;text-decoration:underline;text-underline-offset:4px}@media(max-width:600px){.book-expanded .book-delivery{padding:20px}.book-expanded h2{overflow-wrap:anywhere}}'''

def add_book_release(site):
    for loc in ('zh','en'):
        path=Path(site)/loc/'book.html';s=path.read_text(encoding='utf-8')
        if 'id="expanded-ebooks"' in s:raise ValueError('Book overlay already applied')
        p=s.index('</section>',s.index('<main'))+len('</section>')
        s=s[:p]+guide(loc)+s[p:]
        s=s.replace('</head>','<style>'+CSS+'</style></head>',1)
        path.write_text(s,encoding='utf-8')
