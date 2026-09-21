"""Apply clarity and conversion improvements to the approved coastal website.
Run build_coastal_v3.py first. Preserve prices, identity, privacy and domain.
"""
from pathlib import Path
import base64, hashlib, json, re
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'joyce'
VERSION = '2026-09-21-executive-v5'
ASSETS = SITE / 'assets'
parts = sorted((ROOT/'scripts/refresh-transfer').glob('portrait.part*.b64'))
hero = ASSETS/'coastal-portrait-v4.avif'
expected = 'ca3e049635c95281f2192513ca3fe7257821c87a5dd2c7c8622c44096a97f9ef'
if parts:
    if len(parts) != 4:
        raise RuntimeError('Incomplete portrait transfer')
    raw = base64.b64decode(''.join(''.join(p.read_text().split()) for p in parts), validate=True)
    if hashlib.sha256(raw).hexdigest() != expected:
        raise RuntimeError('Portrait checksum mismatch')
    hero.write_bytes(raw)
assert hero.is_file() and hashlib.sha256(hero.read_bytes()).hexdigest() == expected
im = Image.open(hero).convert('RGB')
assert im.size == (538, 910)
im.save(ASSETS/'coastal-portrait-v4.jpg', quality=91, optimize=True)
small = im.resize((360, 609), Image.Resampling.LANCZOS)
small.save(ASSETS/'coastal-portrait-v4-small.avif', quality=65, speed=6)
small.save(ASSETS/'coastal-portrait-v4-small.jpg', quality=88, optimize=True)
body = (SITE/'index.html').read_text(encoding='utf-8')
assert 'id="refresh-start"' not in body, 'Run the base builder before this refresh'
m = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', body, re.S)
assert m, 'Site data missing'
data = json.loads(m.group(1))
T = data['translations']
T.update({
 'refresh.kicker':['A CLEAR PLACE TO START','找到适合的合作起点'],
 'refresh.title':['One question. A product. An operating business.','一个问题、一款产品，或持续经营合作。'],
 'refresh.intro':['Choose the scope that matches the work. Every option opens its deliverables and boundaries before you enquire.','按实际工作选择。先看清交付与边界，再提交咨询。'],
 'refresh.call':['I need an expert decision','我需要一次专业判断'],
 'refresh.callbody':['One business question · 60-minute discussion','一个业务问题 · 60分钟讨论'],
 'refresh.audit':['I need a product review','我需要评审产品'],
 'refresh.auditbody':['One game and market · Priorities and roadmap','一款游戏、一个市场 · 优先级与路线图'],
 'refresh.partner':['I need an operating partner','我需要经营合作伙伴'],
 'refresh.partnerbody':['90-day mandate · Reviews and operating cadence','90天合作 · 复盘与经营节奏'],
 'refresh.view':['Review scope','查看范围'],
 'refresh.selected':['YOUR SELECTED ENGAGEMENT','你选择的合作服务'],
 'refresh.summary':['An enquiry only. Scope, fee and availability are confirmed separately.','这里只生成咨询意向；合作范围、费用与时间另行确认。'],
 'refresh.share':['Copy a link to this service','复制此服务链接'],
 'refresh.copied':['Service link copied','服务链接已复制'],
 'refresh.fallback':['Copy this service link:','请复制此服务链接：'],
 'exec.kicker':['EXECUTIVE PROFILE','高管与战略合伙人档案'],
 'exec.title':['Global operator. Growth partner. Builder.','全球经营者、增长伙伴、业务搭建者。'],
 'exec.intro':['Senior game experience matters when the work is not a single task but a chain of product, growth, publishing and operating decisions.','当问题不是一个单点任务，而是一整条产品、增长、发行与经营决策链时，资深经验本身就是价值。'],
 'exec.role':['WHAT JOYCE CAN OWN','Joyce 可以直接负责什么'],
 'exec.role_title':['From category judgment to global operating results.','从赛道判断到全球经营结果。'],
 'exec.role_body':['Joyce connects category strategy, product and R&D interface, monetization, LiveOps, UA, global publishing, data and organization. The role can be advisory, fractional executive or a long-term strategic growth partnership.','Joyce 将赛道战略、产品与研发协同、商业化、LiveOps、UA、全球发行、数据体系与组织执行连成一套经营系统；可按顾问、高管外脑或长期战略增长合伙人方式合作。'],
 'exec.cta':['See annual partnership','查看年度合作'],
 'exec.linkedin':['LinkedIn profile','LinkedIn 档案'],
 'exec.proof1':['Years in games & product','游戏与产品经验'],
 'exec.proof2':['Product Manager / Lead Producer · CityVille · FarmVille · Arcade','产品经理 / Lead Producer · CityVille · FarmVille · Arcade'],
 'exec.proof3':['Studios · 500+ collaboration network','工作室 · 500+ 跨职能协作网络'],
 'exec.proof4':['Chinese CityVille D1 retention on that scoped project','Chinese CityVille 该项目 D1 留存提升'],
 'exec.proof5':['Career experience across four major game companies','四家头部游戏公司职业经历'],
 'exec.proof6':['Published author · Tencent entrepreneurship-community mentor','已出版作者 · 腾讯创业社区导师'],
 'portfolio.kicker':['PORTFOLIO ECOSYSTEM','产品与知识生态'],
 'portfolio.title':['One operator. Multiple worlds.','一个经营者，多种世界。'],
 'portfolio.intro':['AI-native products and knowledge systems across games, education, culture, wellness, science and lifestyle. Each project is a real operating surface — not a slide-deck concept.','覆盖游戏、教育、文化、疗愈、科学与生活方式的 AI-native 产品和知识系统。每个项目都是实际建设中的产品入口，而不是概念PPT。'],
 'portfolio.ggc':['Global game growth, publishing, monetization, LiveOps and executive partnership.','全球游戏增长、发行、商业化、LiveOps 与高管级合作。'],
 'portfolio.bible':['A child-friendly Bible learning product built around story, reflection, exploration and family connection.','以故事、反思、探索与家庭连接为核心的儿童 Bible 学习产品。'],
 'portfolio.dharma':['A bilingual Buddhist knowledge atlas connecting texts, concepts, versions, people, places, timelines and evidence.','连接经论、概念、版本、人物、地点、时间线与证据的双语佛典知识地图。'],
 'portfolio.healing':['A global map and timeline connecting healing traditions, nature-based practices, sensory modalities and modern evidence.','连接全球疗愈传统、自然疗法、感官实践与现代证据的地图和时间线。'],
 'portfolio.quri':['A bilingual quantum-learning atlas with interactive experiments, concepts, stories, evidence and learning journeys.','带互动实验、概念、故事、证据与学习路径的双语量子知识地图。'],
 'portfolio.memo':['A playful-premium lifestyle brand moving across home, work, travel, resort and after-hours.','横跨居家、工作、旅行、度假与夜间场景的高级俏皮生活方式品牌。'],
 'portfolio.visit':['Visit project','访问项目'],
 'voice.kicker':['PUBLIC VOICE & CREDENTIALS','公开内容与专业背书'],
 'voice.title':['Ideas are useful when they become public, testable and reusable.','观点只有被公开、被检验、可复用，才真正有价值。'],
 'voice.intro':['Follow the work through LinkedIn, published writing, public talks and verified industry roles.','通过 LinkedIn、出版作品、公开演讲与已核实行业角色持续了解 Joyce 的工作。'],
 'voice.linkedin_title':['LinkedIn · Joyce Mi','LinkedIn · Joyce Mi'],
 'voice.linkedin_body':['Global game growth, publishing, LiveOps, monetization, AI-native product building and operating-system thinking.','全球游戏增长、发行、LiveOps、商业化、AI-native 产品与经营系统方法论。'],
 'voice.linkedin_cta':['Follow Joyce on LinkedIn','在 LinkedIn 关注 Joyce'],
 'voice.pub_title':['Publications','出版与专业内容'],
 'voice.pub_body':['Author of Game Operations and Global Expansion: Strategies, Methods, and Skills, published by China Machine Press in 2024 under the byline Ai Xiaomi / 艾小米.','《游戏运营与出海实战：策略、方法与技巧》作者，机械工业出版社 2024 年出版，署名艾小米。'],
 'voice.pub_cta':['Publisher reference','出版社书页'],
 'voice.speaking_title':['Selected public speaking','公开分享'],
 'voice.speaking_body':['Public records include Baijing, Huibuluo × Xiaguang, and RongCloud × Everyone Is a Product Manager industry events.','公开记录包括白鲸、汇部落 × 霞光、融云 × 人人都是产品经理等行业活动。'],
 'voice.honor_title':['Honors & industry roles','行业角色与荣誉'],
 'voice.honor_body':['Tencent entrepreneurship-community mentor and industry educator. Award and conference applications are never presented as wins before formal acceptance.','腾讯创业社区导师、行业教育者。奖项和大会申请在正式确认前不会被包装成“已获奖/已受邀”。'],
 'voice.source':['View public reference','查看公开记录'],
 'annual.kicker':['ANNUAL PARTNERSHIP','百万年框 · 年度战略合作'],
 'annual.title':['Buy senior judgment once. Keep it inside the business all year.','不是买一次建议，而是把资深判断长期放进经营体系。'],
 'annual.intro':['For teams with a real product, funding and global ambition. Annual work is designed around executive judgment, operating cadence, measurable priorities and the client’s own execution team.','面向已有产品、资金与全球增长目标的团队。年度合作围绕高管判断、经营节奏、可量化优先级和甲方执行团队展开。'],
 'annual.a.title':['Executive Advisory','年度高管顾问'],
 'annual.a.price':['CNY 880,000+ / year','¥880,000+ / 年'],
 'annual.a.body':['Board-level and founder-level judgment: product, market, portfolio, quarterly reviews and major decisions.','老板/董事会级判断：产品、市场、项目组合、季度复盘与重大决策。'],
 'annual.b.title':['Fractional CMO / COO','外部 CMO / COO'],
 'annual.b.price':['CNY 1,280,000–1,680,000 / year','¥1,280,000–1,680,000 / 年'],
 'annual.b.body':['Embedded growth and operating leadership across publishing, monetization, UA, LiveOps, data and organization.','深度参与发行、商业化、UA、LiveOps、数据与组织的增长和经营管理。'],
 'annual.c.title':['Strategic Growth Partner','战略增长合伙人'],
 'annual.c.price':['CNY 1,980,000+ / year + performance participation','¥1,980,000+ / 年 + 结果分成'],
 'annual.c.body':['Long-term partnership for global scale, with success mechanics agreed against a written baseline and attribution rules.','面向全球 Scale 的长期合作；结果分成基于书面基线、归因规则和双方约定。'],
 'annual.cta':['Discuss annual partnership','沟通年度合作'],
 'annual.note':['Reference annual models. Final scope, capacity, decision rights, performance mechanics and billing are confirmed in the written SOW.','以上为年度合作参考模型；最终范围、投入容量、决策权限、结果机制与付款方式以书面 SOW 为准。'],
 'form.budget':['Budget & timing (optional)','预算与时间（选填）'],
 'contact.title':['Let’s discuss<br>your next decision.','聊聊你下一步<br>要做的决策。'],
})
data['version'] = VERSION
body = body[:m.start(1)] + json.dumps(data, ensure_ascii=False).replace('</','<\\/') + body[m.end(1):]
body = body.replace('content="2026-09-19-coastal-v3"','content="'+VERSION+'"')
body = body.replace('<link rel="preload" as="image" href="/joyce/assets/coastal-portrait.avif">', '<link rel="preload" as="image" href="/joyce/assets/coastal-portrait-v4.avif" imagesrcset="/joyce/assets/coastal-portrait-v4-small.avif 360w, /joyce/assets/coastal-portrait-v4.avif 538w" imagesizes="(max-width:580px) 100vw, (max-width:860px) 45vw, 538px" type="image/avif">')
image = '<picture class="portrait-picture"><source type="image/avif" srcset="/joyce/assets/coastal-portrait-v4-small.avif 360w, /joyce/assets/coastal-portrait-v4.avif 538w" sizes="(max-width:580px) 100vw, (max-width:860px) 45vw, 538px"><img class="portrait" src="/joyce/assets/coastal-portrait-v4.jpg" srcset="/joyce/assets/coastal-portrait-v4-small.jpg 360w, /joyce/assets/coastal-portrait-v4.jpg 538w" sizes="(max-width:580px) 100vw, (max-width:860px) 45vw, 538px" alt="Joyce in the selected lavender-and-gold brand portrait" width="538" height="910" fetchpriority="high" decoding="async"></picture>'
body, n = re.subn(r'<img class="portrait"[^>]+>', image, body)
assert n == 1
body = body.replace('</head>', '<link rel="stylesheet" href="/joyce/assets/refresh-v4.css?v=4">\n</head>')
body = body.replace('</body>', '<script src="/joyce/assets/refresh-v4.js?v=4" defer></script></body>')
def t(key):
    return '<span data-i18n="'+key+'">'+T[key][0]+'</span>'
executive = (
 '<section class="section executive-profile" id="executive-profile"><div class="wrap">'
 '<div class="heading"><div><p class="eyebrow">'+t('exec.kicker')+'</p><h2>'+t('exec.title')+'</h2></div><p>'+t('exec.intro')+'</p></div>'
 '<div class="executive-grid"><article class="glass executive-main"><p class="eyebrow">'+t('exec.role')+'</p><h3>'+t('exec.role_title')+'</h3><p>'+t('exec.role_body')+'</p>'
 '<div class="executive-actions"><a class="button" href="#annual-partnership">'+t('exec.cta')+' <span>↗</span></a><a class="button secondary" href="https://www.linkedin.com/in/minyajing/" target="_blank" rel="noopener noreferrer">'+t('exec.linkedin')+' <span>↗</span></a></div></article>'
 '<div class="executive-proof"><article><strong>15+</strong><span>'+t('exec.proof1')+'</span></article><article><strong>Zynga</strong><span>'+t('exec.proof2')+'</span></article><article><strong>10+ · 500+</strong><span>'+t('exec.proof3')+'</span></article><article><strong>+700 bps</strong><span>'+t('exec.proof4')+'</span></article><article><strong>Microsoft · Tencent<br>Zynga · Gameloft</strong><span>'+t('exec.proof5')+'</span></article><article><strong>Author · Mentor</strong><span>'+t('exec.proof6')+'</span></article></div></div></div></section>'
)
portfolio = '<section class="section portfolio" id="portfolio"><div class="wrap"><div class="heading"><div><p class="eyebrow">'+t('portfolio.kicker')+'</p><h2>'+t('portfolio.title')+'</h2></div><p>'+t('portfolio.intro')+'</p></div><div class="portfolio-grid">'
portfolio_items = [('GGC Business','Games · Growth · Publishing','https://biz.ggcgames.com/','portfolio.ggc'),('AI Bible for Kids','Education · Story · Family','https://bible.saga1001.com/','portfolio.bible'),('Dharma Atlas','Culture · Text · Evidence','https://dharma.saga1001.com/','portfolio.dharma'),('Earth Healing','Wellness · Nature · Evidence','https://healing.saga1001.com/','portfolio.healing'),('QuriAtlas','Science · Learning · Interaction','https://quriatlas.saga1001.com/','portfolio.quri'),('MEMO','Lifestyle · Fashion · Travel','https://memo.saga1001.com/','portfolio.memo')]
for name, tag, url, key in portfolio_items:
    portfolio += '<a class="portfolio-card glass" href="'+url+'" target="_blank" rel="noopener noreferrer"><span class="portfolio-tag">'+tag+'</span><h3>'+name+'</h3><p>'+t(key)+'</p><span class="portfolio-link">'+t('portfolio.visit')+' ↗</span></a>'
portfolio += '</div></div></section>'
voice = (
 '<section class="section public-voice" id="public-voice"><div class="wrap"><div class="heading"><div><p class="eyebrow">'+t('voice.kicker')+'</p><h2>'+t('voice.title')+'</h2></div><p>'+t('voice.intro')+'</p></div><div class="voice-grid">'
 '<article class="glass voice-card featured"><p class="eyebrow">LINKEDIN</p><h3>'+t('voice.linkedin_title')+'</h3><p>'+t('voice.linkedin_body')+'</p><a class="button" href="https://www.linkedin.com/in/minyajing/" target="_blank" rel="noopener noreferrer">'+t('voice.linkedin_cta')+' <span>↗</span></a></article>'
 '<article class="glass voice-card"><p class="eyebrow">BOOK</p><h3>'+t('voice.pub_title')+'</h3><p>'+t('voice.pub_body')+'</p><a class="text-button" href="https://ebooks.cmpbook.com/detail?id=26372" target="_blank" rel="noopener noreferrer">'+t('voice.pub_cta')+' ↗</a></article>'
 '<article class="glass voice-card"><p class="eyebrow">SPEAKING</p><h3>'+t('voice.speaking_title')+'</h3><p>'+t('voice.speaking_body')+'</p><div class="voice-links"><a href="https://www.baijing.cn/article/49426" target="_blank" rel="noopener noreferrer">Baijing ↗</a><a href="https://www.sohu.com/a/724348973_120157439" target="_blank" rel="noopener noreferrer">Huibuluo × Xiaguang ↗</a><a href="https://www.woshipm.com/event/6108334.html" target="_blank" rel="noopener noreferrer">RongCloud × Woshipm ↗</a></div></article>'
 '<article class="glass voice-card"><p class="eyebrow">ROLES</p><h3>'+t('voice.honor_title')+'</h3><p>'+t('voice.honor_body')+'</p><a class="text-button" href="https://www.sanjieke.cn/course/detail/sjk/8007244" target="_blank" rel="noopener noreferrer">'+t('voice.source')+' ↗</a></article></div></div></section>'
)
annual = (
 '<section class="section annual-partnership" id="annual-partnership"><div class="wrap"><div class="heading"><div><p class="eyebrow">'+t('annual.kicker')+'</p><h2>'+t('annual.title')+'</h2></div><p>'+t('annual.intro')+'</p></div><div class="annual-grid">'
 '<article class="annual-card"><span class="annual-index">01</span><h3>'+t('annual.a.title')+'</h3><strong>'+t('annual.a.price')+'</strong><p>'+t('annual.a.body')+'</p></article>'
 '<article class="annual-card featured"><span class="annual-index">02</span><h3>'+t('annual.b.title')+'</h3><strong>'+t('annual.b.price')+'</strong><p>'+t('annual.b.body')+'</p></article>'
 '<article class="annual-card"><span class="annual-index">03</span><h3>'+t('annual.c.title')+'</h3><strong>'+t('annual.c.price')+'</strong><p>'+t('annual.c.body')+'</p></article></div><div class="annual-cta"><a class="button" href="#contact">'+t('annual.cta')+' <span>↗</span></a><p class="fineprint">'+t('annual.note')+'</p></div></div></section>'
)

start = '<div id="refresh-start" class="refresh-start"><p class="eyebrow">'+t('refresh.kicker')+'</p><h3>'+t('refresh.title')+'</h3><p class="start-intro">'+t('refresh.intro')+'</p><div class="start-grid">'
for key, sid in [('call','S01'), ('audit','S03'), ('partner','S11')]:
    s = next(s for s in data['services'] if s['ID'] == sid)
    fee = 'CNY '+format(s['fee'],',')+('+' if key!='call' else '')
    start += '<button type="button" class="start-card" data-detail="'+sid+'"><span class="start-title">'+t('refresh.'+key)+'</span><span class="start-description">'+t('refresh.'+key+'body')+'</span><span class="start-bottom"><b data-route-price="'+sid+'">'+fee+'</b><span>'+t('refresh.view')+' ↗</span></span></button>'
start += '</div></div>'
assert body.count('<section class="section sectors" id="sectors">') == 1
body = body.replace('<section class="section sectors" id="sectors">', executive+portfolio+'<section class="section sectors" id="sectors">')
assert body.count('<section class="section process">') == 1
body = body.replace('<section class="section process">', voice+annual+'<section class="section process">')
assert body.count('<div class="service-toolbar">') == 1
body = body.replace('<div class="service-toolbar">', start+'<div class="service-toolbar">')
summary = '<div class="selected-engagement" aria-live="polite"><span class="eyebrow">'+t('refresh.selected')+'</span><strong id="selection-name">Expert Decision Call</strong><span id="selection-fee">CNY 5,000</span><p>'+t('refresh.summary')+'</p></div>'
body = body.replace('<form id="intake" class="glass form">','<form id="intake" class="glass form">'+summary)
body = body.replace('<dialog id="service-dialog" class="service-dialog">', '<dialog id="service-dialog" class="service-dialog" aria-labelledby="dialog-name" aria-describedby="dialog-scope">')
body = body.replace('<p class="fineprint">'+t('service.note')+'</p></dialog>', '<button class="text-button share-service" type="button" id="share-service">'+t('refresh.share')+'</button><p id="share-status" class="fineprint" aria-live="polite"></p><p class="fineprint">'+t('service.note')+'</p></dialog>')
assert 'id="share-service"' in body
(SITE/'index.html').write_text(body,encoding='utf-8')
(ROOT/'index.html').write_text(body,encoding='utf-8')
manifest = {
 'version':VERSION, 'scope':'Live website refresh; no PDF or new image generation.',
 'portrait_source':'Higher-resolution portrait crop from user-selected standalone reference 141bc04d-08b7-4e52-800a-67233a6ab8c4.png, native rectangle (30,85,568,995).',
 'identity':'Existing AI-styled reference selected by the user. No new face generated. Real GGC-shirt photograph remains in About.',
 'before':{'hero_crop':[461,540],'hero_bytes':12344},
 'after':{'hero_crop':[538,910],'hero_bytes':hero.stat().st_size,'native_detail_only':True,'responsive_sizes':[360,538],'jpeg_fallback':True,'desktop_render_width_cap':538},
 'limits':'Re-encoded native reference detail, not recovered 4K detail or a newly captured portrait. Decorative sea background remains atmospheric.',
 'pricing':'Canonical rate-card.csv unchanged. New starting-point cards refer to S01, S03 and S11.',
 'privacy':'Public business content only; no client names or personal conversations; enquiries are local drafts, not sent messages.',
 'assets':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ASSETS.glob('coastal-portrait-v4*')}
}
(SITE/'content/refresh-v4-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Built',VERSION,'with responsive reference portrait, service entry paths and accessible inquiry flow.')
