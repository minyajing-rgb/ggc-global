"""Apply clarity and conversion improvements to the approved coastal website.
Run build_coastal_v3.py first. Preserve prices, identity, privacy and domain.
"""
from pathlib import Path
import base64, hashlib, json, re
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'joyce'
VERSION = '2026-09-19-coastal-v4'
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
start = '<div id="refresh-start" class="refresh-start"><p class="eyebrow">'+t('refresh.kicker')+'</p><h3>'+t('refresh.title')+'</h3><p class="start-intro">'+t('refresh.intro')+'</p><div class="start-grid">'
for key, sid in [('call','S01'), ('audit','S03'), ('partner','S11')]:
    s = next(s for s in data['services'] if s['ID'] == sid)
    fee = 'CNY '+format(s['fee'],',')+('+' if key!='call' else '')
    start += '<button type="button" class="start-card" data-detail="'+sid+'"><span class="start-title">'+t('refresh.'+key)+'</span><span class="start-description">'+t('refresh.'+key+'body')+'</span><span class="start-bottom"><b data-route-price="'+sid+'">'+fee+'</b><span>'+t('refresh.view')+' ↗</span></span></button>'
start += '</div></div>'
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
