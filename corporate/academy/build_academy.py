#!/usr/bin/env python3
"""Build an isolated bilingual GGC learning directory. Does not deploy or write DNS.
Reuses reviewed site assets; never hosts course video, takes payment or collects data.
"""
from pathlib import Path
from html import escape as e
from urllib.parse import urlsplit
import argparse, json, shutil, hashlib

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'catalog.json').read_text(encoding='utf-8'))
CATEGORIES=[('all','全部课程','All courses'),('publishing','发行与推广','Publishing'),('operations','留存与运营','LiveOps'),('data','数据与判断','Analytics'),('brand','PR与品牌','Brand / PR'),('organization','组织与招聘','Teams'),('ai','AI应用','AI'),('risk','法规与风险','Risk')]
ASSETS=['buttons.css','site.css','prism.css','ggc-logo.svg','prism-ribbon.svg','book-cover.webp','joyce-approved.webp']
ARROW='<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
CSS=(HERE/'academy.css').read_text(encoding='utf-8')
JS=(HERE/'academy.js').read_text(encoding='utf-8')

def build(out,asset_dir,mode,base_url):
    canonical=base_url.rstrip('/')+'/' if base_url else ''
    u=urlsplit(canonical)
    if mode=='release' and (u.scheme!='https' or not u.netloc or u.query or u.fragment or u.username or u.password):
        raise ValueError('Release requires a verified HTTPS canonical base URL, without query/fragment/credentials.')
    out=out.resolve();asset_dir=asset_dir.resolve()
    if out in (Path('/'),Path('/app'),Path.home(),HERE) or out in HERE.parents or HERE in out.parents:raise ValueError('Unsafe output directory')
    if out.exists() and any(out.iterdir()):raise ValueError('Output must be new or empty')
    missing=[name for name in ASSETS if not (asset_dir/name).is_file()]
    if missing:raise ValueError('Missing approved site assets: '+', '.join(missing))
    dest=out/'assets';dest.mkdir(parents=True)
    hashes={}
    for name in ASSETS:
        data=(asset_dir/name).read_bytes();(dest/name).write_bytes(data);hashes[name]=hashlib.sha256(data).hexdigest()
    (dest/'academy.css').write_text(CSS,encoding='utf-8');(dest/'academy.js').write_text(JS,encoding='utf-8')
    for lang in ['zh','en']:
        other='en' if lang=='zh' else 'zh';t=lambda z,en:z if lang=='zh' else en
        def link(label,url,style='01',external=False):
            return f'<a class="ggc-btn" data-button-id="{style}" href="{e(url,quote=True)}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'><span>{e(label)}</span>{ARROW}</a>'
        cards=[]
        for i,c in enumerate(DATA['courses'],1):
            title=c['title'] if lang=='zh' else c['en'];summary=c['summary'] if lang=='zh' else c['summary_en'];url='https://www.sanjieke.cn/course/detail/sjk/'+c['id']
            note=''
            if 'note' in c:note=f'<p class="edition-note">{e(c["note"] if lang=="zh" else c["note_en"])}</p>'
            translated=f'<p class="title-original" lang="zh-CN">{e(c["title"])}</p>' if lang=='en' else ''
            cards.append(f'<article class="card academy-card" data-course="{c["id"]}" data-category="{c["category"]}"><div class="course-index"><b>{i:02}</b><span>SANJIEKE · JOYCE</span></div><h3>{e(title)}</h3>{translated}<p>{e(summary)}</p>{note}<p class="course-meta">{t("课程及学习权益由三节课页面说明；价格以平台为准。","Sanjieke defines access and learning terms. See the platform for pricing.")}</p>{link(t("前往三节课查看","View on Sanjieke"),url,"01",True)}</article>')
        filters=''.join(f'<button type="button" class="academy-filter" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{e(t(z,en))}</button>' for i,(key,z,en) in enumerate(CATEGORIES))
        robots='index,follow' if mode=='release' else 'noindex,nofollow'
        meta=''
        if canonical:
            meta=f'<link rel="canonical" href="{e(canonical+lang+"/index.html",quote=True)}"><meta property="og:url" content="{e(canonical+lang+"/index.html",quote=True)}">'+''.join(f'<link rel="alternate" hreflang="{loc}" href="{e(canonical+route+"/index.html",quote=True)}">' for loc,route in [('zh-Hans','zh'),('en','en'),('x-default','zh')])
        title=t('GGC Academy · 课程、著作与方法','GGC Academy · Courses, Book & Methods')
        desc=t('Joyce的三节课公开课程入口，连接游戏运营、全球发行、数据、组织与AI实践。','A directory of Joyce’s public Sanjieke courses, published book and operating methods.')
        body=f'''<!doctype html><html lang="{'zh-CN' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="{robots}"><meta name="description" content="{e(desc,quote=True)}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(desc,quote=True)}"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{e(title)}</title>{meta}<link rel="icon" href="../assets/ggc-logo.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/buttons.css"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/prism.css"><link rel="stylesheet" href="../assets/academy.css"><script defer src="../assets/academy.js"></script></head><body class="prism-v3"><a class="skip" href="#main">{t('跳到内容','Skip to content')}</a><header class="academy-top"><nav class="shell academy-nav" aria-label="{t('主导航','Main navigation')}"><a class="academy-brand" href="index.html"><img src="../assets/ggc-logo.svg" width="138" height="50" alt="GGC"><span>ACADEMY<br>{t('课程 · 著作 · 方法','LEARN · APPLY · OPERATE')}</span></a><div class="academy-links"><a href="#courses">{t('课程目录','Courses')}</a><a class="optional" href="#knowledge">{t('著作与方法','Book & methods')}</a><a class="optional" href="https://ggcgames.com/">{t('GGC官网','GGC')}</a><a data-locale href="../{other}/index.html" lang="{other}">{t('EN','中文')}</a></div></nav></header><main id="main"><section class="academy-hero"><div class="shell academy-hero-grid"><div><p class="eyebrow">GGC ACADEMY / KNOWLEDGE INTO PRACTICE</p><h1>{t('把实战经验，','Operating experience.')}<span>{t('变成你的经营能力。','A capability you can use.')}</span></h1><p>{t('从全球发行、留存付费，到数据分析、团队建设与AI应用。集中找到Joyce的公开课程、著作和方法入口。','Find Joyce’s public courses, book and methods across global publishing, player operations, analytics, teams and AI.')}</p><div class="actions">{link(t('浏览三节课课程','Explore the courses'),'#courses','06')}{link(t('查看官方讲师主页','Official instructor profile'),DATA['teacher_url'],'04',True)}</div><p class="academy-mode">{t('中英文的是目录介绍；授课语言、价格及学习权益以三节课平台为准。','This directory is bilingual. English titles are editorial translations; check Sanjieke for teaching language, prices and access.')}</p></div><aside class="academy-proof"><img src="../assets/joyce-approved.webp" width="105" height="125" alt="Joyce Mi" loading="lazy" decoding="async"><h2>Joyce Mi</h2><p>{t('GGC创始人 · 《游戏运营与出海实战》作者','Founder of GGC · Author of Game Operations & Global Expansion')}</p>{link(t('Why GGC / Joyce','Why GGC / Joyce'),'https://ggcgames.com/'+lang+'/about.html','10')}</aside></div></section><section class="section white" id="courses"><div class="shell"><div class="academy-head"><div><p class="eyebrow">PUBLIC COURSE DIRECTORY</p><h2>{t('三节课 · 公开课程入口','Public Sanjieke course listings')}</h2></div><p>{t('按工作问题浏览。保留原课程名称与官方入口，不重新包装为本站售卖的课程。','Browse by work area. Original course names and official destinations are retained; this is not a new course storefront.')}</p></div><div class="academy-tools"><div class="academy-filters" role="group" aria-label="{t('课程分类','Course categories')}">{filters}</div><label><span class="sr-only">{t('搜索课程','Search courses')}</span><input type="search" class="academy-search" data-search placeholder="{t('搜索课程 / 主题','Search course / topic')}" maxlength="100"></label></div><p class="academy-result" data-count role="status" aria-live="polite"></p><div class="grid g3">{''.join(cards)}</div><p class="academy-empty" data-empty hidden>{t('没有匹配项。清空搜索或切换到全部课程。','No matches. Clear the search or select All courses.')}</p><aside class="academy-disclosure">{t('本次目录收录13个公开课程页，PR与品牌营销包含两个同主题页面，不推定为相同版本。课程价格、时长、优惠及学习权限由平台维护；本站不下载、托管或转售付费视频与讲义。','This directory includes 13 public listings, including two related PR/brand pages; identical content is not assumed. Sanjieke maintains pricing, duration, offers and access. GGC does not download, host or resell the paid recordings or handouts here.')}</aside></div></section><section class="section alt" id="knowledge"><div class="shell"><div class="academy-head"><div><p class="eyebrow">BOOK / METHODS / BUSINESS</p><h2>{t('课程之外，继续深入。','Continue beyond a course.')}</h2></div></div><div class="grid g2"><article class="card academy-reading"><img src="../assets/book-cover.webp" width="175" height="235" alt="游戏运营与出海实战" loading="lazy" decoding="async"><div><h3>{t('游戏运营与出海实战','Game Operations & Global Expansion')}</h3><p>{t('查看著作介绍与公开出版入口。本站不提供整本电子书下载。','Explore the published book and official listing. No full ebook is reproduced here.')}</p><div class="actions">{link(t('著作介绍','Book overview'),'https://ggcgames.com/'+lang+'/book.html','01')}</div></div></article><article class="card"><p class="eyebrow">JOYCE METHOD</p><h3>{t('判断 · 构建 · 复利','Decide · Build · Compound')}</h3><p>{t('从诊断、优先级、构建、运营和复盘，到放大／停止及方法沉淀。','From diagnosis, prioritization, building and operations to review, scale/stop and codification.')}</p>{link(t('查看GGC方法','Explore the method'),'https://ggcgames.com/'+lang+'/method.html','04')}<div class="actions">{link(t('讨论企业培训或经营问题','Discuss a team workshop or operating question'),'https://ggcgames.com/'+lang+'/contact.html?track=principal','10')}</div></article></div></div></section></main><footer class="academy-footer"><div class="shell"><div><p>© 2026 GGC · Global Game Copilot</p><p>{t('课程资料核对日期：2026-10-13。未宣称讲师全部课程已穷尽。','Directory reviewed: 13 October 2026. Not asserted to be an exhaustive catalogue.')}</p></div><div><a href="https://ggcgames.com/{lang}/privacy.html">{t('隐私与联系','Privacy & contact')}</a><a href="https://opsgo.ggcgames.com/">OpsGo ↗</a><a href="https://biz.ggcgames.com/">GGC Business ↗</a></div></div></footer></body></html>'''
        folder=out/lang;folder.mkdir();(folder/'index.html').write_text(body,encoding='utf-8')
    (out/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=zh/index.html"><title>GGC Academy</title></head><body><a href="zh/index.html">中文</a> · <a href="en/index.html">English</a></body></html>',encoding='utf-8')
    urls=[canonical+lang+'/index.html' for lang in ['zh','en']] if mode=='release' else []
    sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(url)+'</loc></url>' for url in urls)+'</urlset>'
    (out/'sitemap.xml').write_text(sitemap,encoding='utf-8')
    (out/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+canonical+'sitemap.xml\n' if mode=='release' else 'Disallow: /\n'),encoding='utf-8')
    (out/'build-manifest.json').write_text(json.dumps({'version':DATA['version'],'mode':mode,'canonical':canonical,'courses':len(DATA['courses']),'distinct_topic_groups':12,'video_files':0,'tracking':False,'payments':False,'backend':False,'deployed':False,'source_asset_sha256':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'courses':13,'locales':['zh','en'],'deployed':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--assets-from',type=Path,required=True);p.add_argument('--mode',choices=['preview','release'],default='preview');p.add_argument('--base-url',default='');a=p.parse_args();build(a.out,a.assets_from,a.mode,a.base_url)
