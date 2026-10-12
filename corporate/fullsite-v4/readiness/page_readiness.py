"""Add deployment-independent metadata and honest operating-state UI.

Do not rewrite approved business copy, styles, portrait or product structure.
HTML is patched narrowly rather than reserialized (preserves SVG/viewBox and CSS).
"""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin
import hashlib, json, re, shutil
import xml.etree.ElementTree as ET

VERSION = '2026-10-13-pr11-p0'
EXCLUDED = {'buttons', '404'}
LANG = {'zh': ('zh-Hans', 'zh_CN'), 'en': ('en', 'en_US')}
NOTICE = {
 'zh': {
  'title': '隐私与联系说明',
  'intro': '说明本网站当前如何处理页面访问、邮件草稿与订阅意向。',
  'form': '此表单只在你的浏览器中准备邮件草稿，不会向网站后台提交，也不会写入CRM。请在邮箱中核对并自行发送；不要填写密码、证件或无权披露的客户资料。',
  'interest': '这里只准备订阅意向邮件。生成草稿或发送意向，不等于已加入邮件列表；自动订阅、确认邮件和退订后台尚未接通。',
  'noscript': '此处需要 JavaScript 才能准备草稿。未启用时不会提交表单；请直接使用邮件联系入口。',
  'sections': [
   ('页面访问与外部资源', '本网站是静态页面。当前前端没有接入站内分析、广告追踪、账户登录或CRM接口，也不使用本地存储保存表单。页面会请求 Google Fonts 的字体样式和字体文件；网站托管及字体服务商可能按其服务规则处理IP地址、浏览器和请求信息。本说明不表示服务器没有访问日志。'),
   ('商务联系', '姓名、回复邮箱、公司、合作方向和业务问题用于在本页组织邮件草稿。你点击打开邮箱后，草稿会交给你选择的邮件客户端；只有你在邮箱中发送后，才会通过邮件渠道联系GGC。本网页不能核实发送或送达状态。收到的邮件由所用邮件服务处理，不代表已进入CRM。'),
   ('动态与订阅意向', '邮箱、主题偏好和语言用于准备意向邮件。当前没有自动加入订阅名单、双重确认或退订系统。设计评审中的“等待确认”“确认完成”“已退订”只表示界面样稿，不会改变任何订阅记录。商务询问不会自动订阅动态。'),
   ('你可以如何控制信息', '在发送前可编辑或放弃草稿。请不要提交密码、证件、付款资料或未经授权的第三方信息。若已发送邮件，需要查询、更正或请求删除邮件中的个人信息，可通过现有联系邮箱提出；处理范围需结合实际邮件记录及适用要求确认，不在此承诺未经核实的保存期限。'),
   ('外部产品与链接', '访问 LinkedIn、Telegram、OpsGo、出版社或产品独立站后，相关服务各自处理访问、账户或付款信息。本网站不会仅凭你打开这些链接，就声称已创建产品账户、完成付款或提交申请。'),
   ('说明的范围', '本说明对应当前静态前端和人工邮件联系流程。未来接入后台、分析或订阅服务时，应在启用前更新相应说明和选择方式。正式运营主体、托管日志及具体保存安排仍需由网站运营方核实；这不是已经完成法律合规审查的声明。')]
 },
 'en': {
  'title': 'Privacy & contact notice',
  'intro': 'How the current website handles page requests, email drafts and updates interest.',
  'form': 'This form prepares an email draft in your browser only. It does not submit to a website backend or CRM. Review and send it from your email app. Do not include passwords, identity documents or unauthorized client information.',
  'interest': 'This prepares an updates-interest email only. Preparing or sending it does not enroll you in a mailing list. Automated subscription, confirmation and unsubscribe services are not connected.',
  'noscript': 'JavaScript is required to prepare a draft here. With it disabled this form does not submit; use the direct email contact instead.',
  'sections': [
   ('Page requests and external resources', 'This is a static website. The current frontend has no on-site analytics, advertising trackers, account login or CRM integration, and does not save forms in browser storage. Pages request Google Fonts stylesheets and font files. Hosting and font providers may process IP addresses, browser details and request information under their own service rules. This notice does not claim that server access logs do not exist.'),
   ('Business contact', 'Your name, reply email, company, partnership track and question are used to compose a local draft. Opening your email app passes that draft to the client you choose; GGC is contacted through email only if you send it there. This website cannot verify sending or delivery. Received mail is handled by the email service used; it is not evidence of CRM integration.'),
   ('Updates interest', 'Your email, selected topics and language are used to prepare an interest email. Automatic list enrollment, double opt-in and unsubscribe services are not connected. The pending, confirmed and unsubscribed panels in design review are UI examples, not subscription records. Business inquiries do not automatically subscribe you.'),
   ('Your choices', 'You may edit or discard a draft before sending. Do not submit passwords, identity or payment documents, or third-party information you are not entitled to disclose. For information already emailed, contact the existing address to ask about access, correction or deletion; handling depends on the actual records and applicable requirements. No unverified retention period is promised here.'),
   ('External products and links', 'LinkedIn, Telegram, OpsGo, publishers and independent product sites operate their own access, account and payment processes. Opening an external link does not mean this website has created an account, completed payment or submitted an application for you.'),
   ('Scope of this notice', 'This notice describes the current static frontend and manual email workflow. It must be updated before introducing new backend, analytics or subscription processing. The legal operator, hosting logs and specific retention arrangements still require operator verification. This is not a claim of completed legal compliance review.')]
 }
}

class ReadCopy(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.title=[]; self.lead=[]; self.capture=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag,a))
        if tag=='p' and self.capture is None and not self.lead:
            classes=set(a.get('class','').split())
            inside=any(set(v.get('class','').split()) & {'hero-copy2','hero-copy'} for _,v in self.stack)
            if inside and not classes & {'eyebrow','hero-translation','subline'}:
                self.capture=len(self.stack)
    def handle_endtag(self, tag):
        if tag=='p' and self.capture is not None:self.capture=None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:]; break
    def handle_data(self,data):
        if any(t=='title' for t,_ in self.stack):self.title.append(data)
        if self.capture is not None:self.lead.append(data)


def validate_base_url(value):
    p=urlsplit(value)
    if p.scheme!='https' or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise ValueError('Use an explicit HTTPS canonical base without credentials, query or fragment.')
    if p.port not in (None,443) or not re.fullmatch(r'[A-Za-z0-9.-]+',p.hostname):
        raise ValueError('Invalid canonical host.')
    if not re.fullmatch(r'/[A-Za-z0-9/_-]*',p.path or '/') or '..' in p.path:
        raise ValueError('Canonical path must be a simple directory path.')
    return value.rstrip('/')+'/'


def clean_text(value):return re.sub(r'\s+',' ',unescape(value)).strip()

def hashfile(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_contact(html, loc):
    notice=NOTICE[loc]
    # Fail closed: no form names or enabled submission control until the prevention
    # guard is installed. This avoids a no-JS fallback leaking fields into a GET URL.
    def form_patch(match):
        form=match.group(0)
        form=re.sub(r'(<(?:input|select|textarea)\b[^>]*?)\sname="([^"]+)"',r'\1 data-p0-name="\2"',form)
        form=re.sub(r'(<button\b[^>]*\btype="submit"[^>]*)(>)',r'\1 disabled data-p0-submit\2',form)
        label='p0-contact-note' if 'data-inquiry' in form else 'p0-interest-note'
        form=re.sub(r'<form\b',f'<form aria-describedby="{label}"',form,count=1)
        info=notice['form'] if 'data-inquiry' in form else notice['interest']
        prefix=f'<p id="{label}" class="note p0-note">{escape(info)} <a class="source-link" href="privacy.html">{escape(notice["title"])}</a></p>'
        noscript=f'<noscript><p class="note">{escape(notice["noscript"])} <a href="mailto:minyajing@gmail.com">minyajing@gmail.com</a></p></noscript>'
        return prefix+noscript+form
    return re.sub(r'<form\b[^>]*data-(?:inquiry|interest)[\s\S]*?</form>',form_patch,html)


def privacy_page(template, loc):
    n=NOTICE[loc]
    content=(f'<section class="pagehero"><div class="shell"><p class="eyebrow">PRIVACY / CONTACT</p>'
             f'<h1>{escape(n["title"])}</h1><p>{escape(n["intro"])}</p></div></section>'
             '<section class="section"><div class="shell"><div class="grid g2">'+
             ''.join(f'<article class="card"><h2>{escape(h)}</h2><p>{escape(p)}</p></article>' for h,p in n['sections'])+
             '</div><div class="actions"><a class="ggc-btn" data-button-id="04" href="contact.html">'+
             ('联系GGC' if loc=='zh' else 'Contact GGC')+'</a><a class="source-link" href="mailto:minyajing@gmail.com">minyajing@gmail.com</a></div></div></section>')
    template=re.sub(r'<main id="main">[\s\S]*?</main>',lambda _:f'<main id="main">{content}</main>',template,count=1)
    template=re.sub(r'<title>[\s\S]*?</title>',lambda _:f'<title>{escape(n["title"])} · GGC Global Game Copilot</title>',template,count=1)
    other='en' if loc=='zh' else 'zh'
    template=template.replace(f'../{other}/index.html',f'../{other}/privacy.html')
    template=template.replace('page-index','page-privacy')
    return template


def add_metadata(html, loc, route, mode, base):
    parser=ReadCopy();parser.feed(html)
    title=clean_text(''.join(parser.title))
    lead=clean_text(''.join(parser.lead))
    if route=='privacy':lead=NOTICE[loc]['intro']
    if not lead:lead=title
    # Existing on-page wording is the source; no invented claims or dates.
    desc=clean_text(title.split(' · GGC')[0]+' — '+lead)
    limit=180 if loc=='en' else 120
    if len(desc)>limit:desc=desc[:limit-1].rsplit(' ',1)[0]+'…' if loc=='en' else desc[:limit-1]+'…'
    html=re.sub(r'<meta\b(?=[^>]*\bname="(?:description|robots)")[^>]*>','',html,flags=re.I)
    url=base+loc+'/'+route+'.html'
    indexed=mode=='release' and route not in EXCLUDED
    tags=[f'<meta name="description" content="{escape(desc,quote=True)}">',
          f'<meta name="robots" content="{"index,follow,max-image-preview:large" if indexed else "noindex,nofollow"}">',
          '<meta name="referrer" content="strict-origin-when-cross-origin">',
          '<link rel="icon" href="../assets/ggc-logo.svg" type="image/svg+xml">']
    if route!='404':
        tags.append(f'<link rel="canonical" href="{escape(url,quote=True)}">')
        if route not in EXCLUDED:
            for language,folder in [('zh-Hans','zh'),('en','en'),('x-default','zh')]:
                tags.append(f'<link rel="alternate" hreflang="{language}" href="{escape(base+folder+"/"+route+".html",quote=True)}">')
    properties={'og:title':title,'og:description':desc,'og:type':'website','og:site_name':'GGC — Global Game Copilot',
                'og:locale':LANG[loc][1],'og:locale:alternate':LANG['en' if loc=='zh' else 'zh'][1],
                'og:image':base+'assets/joyce-approved.webp','og:image:type':'image/webp',
                'og:image:width':'400','og:image:height':'421','og:image:alt':'Joyce — GGC founder'}
    if route!='404':properties['og:url']=url
    tags.extend(f'<meta property="{key}" content="{escape(value,quote=True)}">' for key,value in properties.items())
    tags.extend(f'<meta name="{key}" content="{escape(value,quote=True)}">' for key,value in {
        'twitter:card':'summary','twitter:title':title,'twitter:description':desc,
        'twitter:image':base+'assets/joyce-approved.webp','twitter:image:alt':'Joyce — GGC founder'}.items())
    if indexed:
        schema={'@context':'https://schema.org','@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,
                'inLanguage':LANG[loc][0],'isPartOf':{'@type':'WebSite','@id':base+'#website','name':'GGC — Global Game Copilot','url':base}}
        tags.append('<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    html=html.replace('</head>','\n'+'\n'.join(tags)+'\n</head>',1)
    return html,{'route':loc+'/'+route+'.html','title':title,'description':desc,'canonical':url if route!='404' else None,'indexable':indexed}


def absolute_404_paths(html, loc, base):
    # Site-root-relative assets and navigation survive /arbitrary/deep/missing paths.
    # No host rewrite, HTTP status or production configuration is changed here.
    prefix=urlsplit(base).path
    logical=prefix+loc+'/404.html'
    def rewrite(m):
        u=m.group(2)
        if not u or u.startswith(('http:','https:','mailto:','data:','tel:','#')):return m.group(0)
        return m.group(1)+urljoin(logical,u)+m.group(3)
    return re.sub(r'((?:href|src)=")([^"]*)(")',rewrite,html)


def patch_page(html, loc, route, mode):
    script='<script defer src="../assets/readiness.js"></script>'
    # Guard executes before legacy scripts; enhancement waits for DOMContentLoaded.
    html=html.replace('<script defer src="../assets/app.js">',script+'<script defer src="../assets/app.js">',1)
    html=html.replace('</head>','<link rel="stylesheet" href="../assets/readiness.css"></head>',1)
    html=html.replace('<main id="main">','<main id="main" tabindex="-1">',1)
    html=html.replace('<div class="footer-bottom">','<div class="footer-bottom"><a class="source-link" href="privacy.html">'+NOTICE[loc]['title']+'</a>',1)
    # Per-locale accessibility names, while visible artwork and labels stay intact.
    if loc=='zh':
        html=html.replace('data-prev aria-label="Previous"','data-prev aria-label="上一张"').replace('data-next aria-label="Next"','data-next aria-label="下一张"')
    html=re.sub(r'(data-slide-to="(\d+)"[^>]*aria-label=")(\d+)(")',lambda m:m[1]+('查看第'+str(int(m[2])+1)+'张说明图' if loc=='zh' else 'View information panel '+str(int(m[2])+1))+m[4],html)
    html=patch_contact(html,loc)
    if mode=='release':
        # Design-only review links and state simulations remain in preview, not the public flow.
        html=re.sub(r'<a href="\.\./review\.html">[^<]*</a>','',html)
        if route=='updates':html=re.sub(r'<details class="state-demo">[\s\S]*?</details>','',html)
    return html


def prepare_pages(site, assets, mode, base):
    base=validate_base_url(base)
    manifest=json.loads((site/'build-manifest.json').read_text())
    assert manifest['locale_pages']==96 and len(manifest['routes'])==48,'Unexpected baseline; reconcile before modifying.'
    before={f.relative_to(site/'assets').as_posix():hashfile(f) for f in (site/'assets').iterdir() if f.is_file()}
    baseline_bodies={f.relative_to(site).as_posix():hashfile(f) for f in site.glob('*/*.html')}
    for loc in LANG:
        original=(site/loc/'index.html').read_text()
        (site/loc/'privacy.html').write_text(privacy_page(original,loc),encoding='utf-8')
    for name in ['readiness.js','readiness.css']:shutil.copyfile(assets/name,site/'assets'/name)
    inventory=[]
    for loc in LANG:
        for route in manifest['routes']+['privacy']:
            f=site/loc/(route+'.html');html=f.read_text()
            html=patch_page(html,loc,route,mode)
            html,meta=add_metadata(html,loc,route,mode,base)
            if route=='404':html=absolute_404_paths(html,loc,base)
            f.write_text(html,encoding='utf-8');inventory.append(meta)
    # Unknown-path fallback is an actual page, not a redirect to Home (which would hide the error).
    (site/'404.html').write_bytes((site/'zh/404.html').read_bytes())
    for f in [site/'index.html',site/'review.html']:
        h=f.read_text()
        h=re.sub(r'<meta\b(?=[^>]*\bname="robots")[^>]*>','',h)
        h=h.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>',1)
        f.write_text(h,encoding='utf-8')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';xn='http://www.w3.org/1999/xhtml'
    ET.register_namespace('',ns);ET.register_namespace('xhtml',xn);root=ET.Element('{'+ns+'}urlset')
    for item in inventory:
        if not item['indexable']:continue
        u=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(u,'{'+ns+'}loc').text=item['canonical']
        route=item['route'].split('/',1)[1]
        for code,loc in [('zh-Hans','zh'),('en','en'),('x-default','zh')]:
            ET.SubElement(u,'{'+xn+'}link',{'rel':'alternate','hreflang':code,'href':base+loc+'/'+route})
    ET.ElementTree(root).write(site/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    robots='# Generated artifact only; release owner installs at its origin root.\nUser-agent: *\nAllow: /\n'
    if mode=='release':robots+='Sitemap: '+base+'sitemap.xml\n'
    else:robots+='# Preview HTML carries noindex. Allow crawling so that noindex can be read.\n# This is not access control; use hosting authentication for confidential previews.\n'
    (site/'robots.txt').write_text(robots,encoding='utf-8')
    assert all(hashfile(site/'assets'/n)==v for n,v in before.items()),'An approved asset changed.'
    result={'version':VERSION,'mode':mode,'canonical_base':base,'baseline_locale_pages':96,'added_privacy_pages':2,'locale_pages':98,
            'indexable_urls':sum(i['indexable'] for i in inventory),'root_404':'404.html','deployment_performed':False,
            'approved_assets_unchanged':True,'approved_asset_hashes':before,'baseline_page_hashes':baseline_bodies,
            'forms':'Local drafts only; no CRM or subscription activation','font_requests':'Existing Google Fonts CSS/files; see notice',
            'host_404_contract':{'status':404,'default_document':'404.html','zh_document':'zh/404.html','en_document':'en/404.html','must_not_redirect_or_return_200':True},
            'inventory':inventory}
    (site/'readiness-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    # Keep original route inventory for baseline acceptance; ready inventory is explicit above.
    manifest['readiness']={'version':VERSION,'mode':mode,'locale_pages':98,'manifest':'readiness-manifest.json'}
    (site/'build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
