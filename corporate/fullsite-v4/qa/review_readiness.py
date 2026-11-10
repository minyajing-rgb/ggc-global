#!/usr/bin/env python3
"""PR11 P0 regression: default real HTTP Chromium; --offline is explicitly separate.
Tests only generated candidates. Never calls a production site or sends mail.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import argparse, base64, hashlib, json, mimetypes, re, shutil, subprocess, sys, traceback
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from product_explorer import check_product_explorer

BASE=Path(__file__).resolve().parents[1]; ROOT=BASE.parents[1]
P=argparse.ArgumentParser();P.add_argument('--offline',action='store_true');P.add_argument('--out',type=Path,default=ROOT/'p0-evidence');P.add_argument('--source-commit',default='working-tree');args=P.parse_args()
OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
report={'source_commit':args.source_commit,'checked_at':datetime.now(timezone.utc).isoformat(),'browser_mode':'offline in-memory Chromium' if args.offline else 'local HTTP Chromium (CI)','production_accessed':False,'checks':[],'errors':[],'business_posts':[],'pii_requests':[],'layout_cases':0}

def check(name,ok,detail=None):report['checks'].append({'name':name,'passed':bool(ok),'detail':detail})
def soup(path):return BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
def filehash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def build(name,mode,base,inquiry_endpoint=None):
    target=OUT/name
    if target.exists():shutil.rmtree(target)
    cmd=[sys.executable,str(BASE/'build_ready.py'),'--out',str(target),'--mode',mode,'--base-url',base]
    if inquiry_endpoint:cmd.extend(['--inquiry-endpoint',inquiry_endpoint])
    subprocess.run(cmd,check=True)
    return target

def local_references(site,file):
    for el in soup(file).select('[href],[src]'):
        u=el.get('href') or el.get('src')
        if not u or re.match(r'^(https?:|mailto:|data:|tel:)',u):continue
        parts=urlsplit(u);target=(site/parts.path.lstrip('/')).resolve() if parts.path.startswith('/') else (file.parent/unquote(parts.path)).resolve() if parts.path else file
        okay=target.is_file()
        if okay and parts.fragment and target.suffix=='.html':okay=soup(target).find(id=unquote(parts.fragment)) is not None
        check('resource:'+str(file.relative_to(site)),okay,u)

def static_checks(site,mode):
    manifest=json.loads((site/'readiness-manifest.json').read_text())
    check('locale_pages:'+mode,manifest['locale_pages']==98 and manifest['baseline_locale_pages']==96)
    for n,h in manifest['approved_asset_hashes'].items():check('asset_unchanged:'+mode+'/'+n,filehash(site/'assets'/n)==h)
    entries={i['route']:i for i in manifest['inventory']};descs=[]
    for path,item in entries.items():
        f=site/path;doc=soup(f);loc,key=path.split('/');key=key[:-5]
        robots=doc.select('meta[name=robots]');desc=doc.select('meta[name=description]');canonical=doc.select('link[rel=canonical]')
        check('one_description:'+mode+'/'+path,len(desc)==1 and bool(desc[0].get('content')));descs.append(desc[0]['content'])
        check('one_robots:'+mode+'/'+path,len(robots)==1 and ('noindex' in robots[0]['content'])==(not item['indexable']))
        check('canonical:'+mode+'/'+path,(not canonical if key=='404' else len(canonical)==1 and canonical[0]['href']==item['canonical']))
        alts={a['hreflang']:a['href'] for a in doc.select('link[hreflang]')}
        if key not in ['buttons','404']:
            check('hreflang:'+mode+'/'+path,set(alts)=={'zh-Hans','en','x-default'})
            for code,folder in [('zh-Hans','zh'),('en','en'),('x-default','zh')]:check('alternate:'+mode+'/'+path+'/'+code,alts.get(code)==manifest['canonical_base']+folder+'/'+key+'.html')
        check('social:'+mode+'/'+path,all(doc.select_one(sel) for sel in ['meta[property="og:title"]','meta[property="og:description"]','meta[property="og:locale"]','meta[name="twitter:card"]']))
        check('skip_target:'+mode+'/'+path,doc.select_one('main#main[tabindex="-1"]') is not None)
        for form in doc.select('form'):
            check('notice_inside_form:'+mode+'/'+path,form.select_one('.p0-note') is not None)
            check('noscript_no_PII_names:'+mode+'/'+path,not form.select('input[name],select[name],textarea[name]'))
            check('noscript_disabled_submit:'+mode+'/'+path,all(b.has_attr('disabled') for b in form.select('button[type=submit]')))
        if key in ['contact','updates']:check('privacy_link_and_actual_state:'+mode+'/'+path,bool(doc.select_one('a[href="privacy.html"]')) and bool(doc.select_one('.p0-note')))
        if mode=='release':check('no_public_state_demo:'+path,not doc.select_one('.state-demo') and not doc.select('a[href="../review.html"]'))
        if item['indexable']:
            ld=doc.select('script[type="application/ld+json"]')
            try:
                schemas=[json.loads(tag.string or tag.get_text()) for tag in ld]
                valid=(len(schemas)==(2 if key=='index' else 1)
                       and schemas[0].get('@type')=='WebPage'
                       and (key!='index' or bool(schemas[1].get('@graph'))))
            except Exception:valid=False
            check('structured_data:'+path,valid)
        local_references(site,f)
    check('unique_descriptions:'+mode,len(set(descs))==98)
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    urls=ET.parse(site/'sitemap.xml').findall('s:url',ns)
    actual={u.find('s:loc',ns).text for u in urls};expected={i['canonical'] for i in entries.values() if i['indexable']}
    check('sitemap_exact_set:'+mode,actual==expected and len(urls)==len(actual),len(actual))
    check('robots_allows_noindex_read:'+mode,'Disallow: /' not in (site/'robots.txt').read_text())
    check('robots_sitemap:'+mode,('Sitemap: ' in (site/'robots.txt').read_text())==(mode=='release'))
    root404=soup(site/'404.html');check('root404_no_redirect:'+mode,not root404.select('meta[http-equiv=refresh]'));check('root404_no_canonical:'+mode,not root404.select('link[rel=canonical]'))
    local_references(site,site/'404.html')
    for path in ['index.html','review.html']:check('utility_noindex:'+mode+'/'+path,'noindex' in soup(site/path).select_one('meta[name=robots]')['content'])
    if mode=='release':
        root=soup(site/'index.html')
        check('root_no_review_link',not root.select('a[href="review.html"]'))
        check('root_language_fallbacks',{a['href'] for a in root.select('a[href]')}=={'zh/index.html','en/index.html'})

def as_data(path):return 'data:'+(mimetypes.guess_type(path.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(path.read_bytes()).decode()
def inline(site,file):
    doc=soup(file);scripts=[]
    def resolve(u):
        path=unquote(urlsplit(u).path)
        return site/path.lstrip('/') if path.startswith('/') else file.parent/path
    for tag in doc.select('link[rel=stylesheet]'):
        source=resolve(tag['href']);css=source.read_text();css=re.sub(r'@import\s+url\(.*?\);','',css)
        def image(m):
            path=source.parent/m[1].strip('"\'');return 'url("'+as_data(path)+'")' if path.is_file() else m[0]
        css=re.sub(r'url\(([^)]+)\)',image,css);new=doc.new_tag('style');new.string=css;tag.replace_with(new)
    for tag in doc.select('img[src]'):
        path=resolve(tag['src'])
        if path.is_file():tag['src']=as_data(path)
    for tag in doc.select('script[src]'):scripts.append(resolve(tag['src']).read_text());tag.decompose()
    for js in scripts:
        el=doc.new_tag('script');el.string=js;doc.body.append(el)
    return str(doc)

class CandidateHandler(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
    def send_error(self,code,message=None,explain=None):
        # Local test fixture for Codex's host contract, not a host configuration.
        if code==404:
            loc='en' if urlsplit(self.path).path.startswith('/en/') else 'zh';data=(Path(self.directory)/loc/'404.html').read_bytes()
            self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
            if self.command!='HEAD':self.wfile.write(data)
        else:super().send_error(code,message,explain)

def browser_checks(preview,release):
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(CandidateHandler,directory=str(release)))
    Thread(target=server.serve_forever,daemon=True).start();origin='http://127.0.0.1:'+str(server.server_port)
    manifest=json.loads((release/'build-manifest.json').read_text());reps=manifest['representatives']+['privacy']
    try:
        with sync_playwright() as p:
            opts={'headless':True,'args':['--no-sandbox']}
            if shutil.which('chromium'):opts['executable_path']=shutil.which('chromium')
            browser=p.chromium.launch(**opts);ctx=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
            ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
            def req(r):
                if r.method=='POST':report['business_posts'].append(r.url)
                if any(v in r.url for v in ['qa-private-token','qa%40example.com','qa@example.com']):report['pii_requests'].append(r.url)
            ctx.on('request',req);page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)));cache={}
            def load(loc,key,width=1440,query=''):
                page.set_viewport_size({'width':width,'height':1000})
                if args.offline:
                    f=release/loc/(key+'.html');cache.setdefault(str(f),inline(release,f));page.set_content(cache[str(f)],wait_until='load')
                else:
                    r=page.goto(origin+'/'+loc+'/'+key+'.html'+query,wait_until='networkidle');check('HTTP200:'+loc+'/'+key,r.status==200)
                page.evaluate('document.fonts.ready');page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(15)
                # Verify the files behind below-fold lazy images, rather than
                # treating their intentionally deferred request as a broken image.
                page.locator('img').evaluate_all('es=>es.forEach(e=>e.loading="eager")')
                page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
            for loc in ['zh','en']:
                for key in reps:
                    for w in [320,390,768,1440]:
                        load(loc,key,w);bounds=page.evaluate('({c:document.documentElement.clientWidth,s:document.documentElement.scrollWidth})');report['layout_cases']+=1
                        check('layout:'+loc+'/'+key+'/'+str(w),bounds['s']<=bounds['c']+1,bounds)
                        check('images:'+loc+'/'+key+'/'+str(w),page.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)'))
                load(loc,'index',390);menu=page.locator('[data-menu]');menu.focus();page.keyboard.press('Enter');check('keyboard_open:'+loc,menu.get_attribute('aria-expanded')=='true')
                page.keyboard.press('Tab');check('keyboard_enters_nav:'+loc,page.locator('[data-nav] a').first.evaluate('e=>e===document.activeElement'))
                page.keyboard.press('Shift+Tab');check('keyboard_back_trigger:'+loc,menu.evaluate('e=>e===document.activeElement'))
                page.keyboard.press('Tab');page.keyboard.press('Escape');check('keyboard_escape:'+loc,menu.get_attribute('aria-expanded')=='false' and menu.evaluate('e=>e===document.activeElement'))
                for key in ['index','decision-os','buttons']:
                    load(loc,key)
                    for group in page.locator('[role=tablist]').all():
                        group.locator('[role=tab]').first.focus();page.keyboard.press('End');check('tab_end:'+loc+'/'+key,group.locator('[role=tab]').last.get_attribute('aria-selected')=='true')
                        page.keyboard.press('Home');check('tab_home:'+loc+'/'+key,group.locator('[role=tab]').first.get_attribute('aria-selected')=='true')
                load(loc,'expertise');page.locator('[data-filter="partner"]').focus();page.keyboard.press('Space');check('keyboard_filter:'+loc,all(e.get_attribute('data-type')=='partner' for e in page.locator('[data-type]:visible').all()))
                page.locator('[data-filter="all"]').click();page.locator('[data-search]').fill('ZZZ_NO_MATCH');check('search_empty:'+loc,page.locator('[data-empty]').is_visible())
                for i in range(1,15):
                    load(loc,f'product-{i:02}')
                    page.locator('img').evaluate_all('es=>es.forEach(e=>e.loading="eager")')
                    page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
                    check_product_explorer(page,check,loc+f'/product-{i:02}')
                for key in ['contact','updates']:
                    load(loc,key);form=page.locator('[data-inquiry]' if key=='contact' else '[data-interest]');form.locator('button[type=submit]').click()
                    result=page.locator('#draft-result' if key=='contact' else '[data-interest-result]');check('empty_no_success:'+loc+'/'+key,result.is_hidden())
                    if key=='contact':
                        for k,v in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'qa-private-token for a business decision.'}.items():page.locator('#'+k).fill(v)
                        form.locator('[name=consent]').check()
                    else:page.locator('#updates-email').fill('qa@example.com');form.locator('.consent input').check()
                    form.locator('button[type=submit]').focus();page.keyboard.press('Enter');check('local_draft:'+loc+'/'+key,result.is_visible())
                    link=page.locator('#open-email' if key=='contact' else '[data-interest-mail]');check('mailto_only:'+loc+'/'+key,link.get_attribute('href').startswith('mailto:'))
                    check('draft_focus:'+loc+'/'+key,result.evaluate('e=>e===document.activeElement'))
                    field=page.locator('#message' if key=='contact' else '#updates-email');field.fill('A different decision.' if key=='contact' else 'another@example.com')
                    check('stale_draft_invalidated:'+loc+'/'+key,result.is_hidden() and link.get_attribute('href') is None)
                if not args.offline:
                    load(loc,'contact',query='?service=S12');check('service_prefill:'+loc,'S12' in page.locator('#message').input_value());page.locator('[data-locale]').click();check('locale_referral:'+loc,'service=S12' in page.url)
                    load(loc,'index',query='?service=private-email&track=secrets&email=do-not-propagate');page.locator('[data-locale]').click();check('referral_allowlist:'+loc,'?' not in page.url)
                nc=browser.new_context(java_script_enabled=False,reduced_motion='reduce');np=nc.new_page();nc.on('request',req)
                nc.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
                if args.offline:np.set_content(inline(release,release/loc/'contact.html'))
                else:np.goto(origin+'/'+loc+'/contact.html',wait_until='networkidle')
                check('nojs_disabled:'+loc,np.locator('button[type=submit]').is_disabled());check('nojs_unnamed:'+loc,np.locator('form [name]').count()==0)
                if not args.offline:
                    for k,v in {'name':'qa-private-token','email':'qa@example.com','company':'qa-private-token','message':'qa-private-token business question'}.items():np.locator('#'+k).fill(v)
                    np.locator('[data-p0-name=consent]').focus();np.keyboard.press('Space');check('nojs_consent_keyboard:'+loc,np.locator('[data-p0-name=consent]').is_checked());before=np.url;np.locator('#email').press('Enter');np.wait_for_timeout(150);check('nojs_no_navigation:'+loc,np.url==before)
                nc.close()
            if not args.offline:
                for path in ['/en/deep/path/missing','/zh/deep/path/missing','/unknown']:
                    r=page.goto(origin+path,wait_until='networkidle');check('real_fixture_404:'+path,r.status==404)
                    check('styled_404_assets:'+path,page.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)'));check('404_no_redirect:'+path,page.url==origin+path)
                    links=page.locator('a[href]').evaluate_all("es=>es.map(e=>e.getAttribute('href')).filter(u=>u.includes('contact.html')||u.includes('index.html'))");check('404_root_safe_links:'+path,all(u.startswith('/') for u in links))
            for loc in ['zh','en']:
                baseline=OUT/'baseline'/loc/'index.html';bp=ctx.new_page();bp.set_viewport_size({'width':1440,'height':1000});bp.set_content(inline(OUT/'baseline',baseline),wait_until='load');bp.evaluate('document.fonts.ready')
                load(loc,'index');a=bp.locator('.hero-headline').evaluate('e=>({r:e.getBoundingClientRect().toJSON(),s:getComputedStyle(e).fontSize,w:getComputedStyle(e).fontWeight})');b=page.locator('.hero-headline').evaluate('e=>({r:e.getBoundingClientRect().toJSON(),s:getComputedStyle(e).fontSize,w:getComputedStyle(e).fontWeight})');check('approved_hero_geometry:'+loc,a==b,{'before':a,'after':b});bp.close()
            browser.close()
    finally:server.shutdown()
    check('no_business_POST',not report['business_posts']);check('no_PII_URL_requests',not report['pii_requests']);check('no_browser_errors',not report['errors'])

def live_inquiry_checks(site):
    endpoint='https://formsubmit.co/ajax/minyajing@gmail.com'
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(CandidateHandler,directory=str(site)))
    Thread(target=server.serve_forever,daemon=True).start();origin='http://127.0.0.1:'+str(server.server_port)
    try:
        with sync_playwright() as p:
            opts={'headless':True,'args':['--no-sandbox']}
            if shutil.which('chromium'):opts['executable_path']=shutil.which('chromium')
            browser=p.chromium.launch(**opts);page=browser.new_page();posts=[];state={'status':200,'body':'{"success":"true"}'}
            def intercept(route):
                request=route.request
                headers={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'POST, OPTIONS',
                         'Access-Control-Allow-Headers':'content-type, accept','Content-Type':'application/json'}
                if request.method=='OPTIONS':route.fulfill(status=204,headers=headers);return
                posts.append(json.loads(request.post_data))
                route.fulfill(status=state['status'],headers=headers,body=state['body'])
            page.route('https://fonts.googleapis.com/**',lambda route:route.fulfill(status=200,content_type='text/css',body=''))
            page.route(endpoint,intercept)
            for loc in ['zh','en']:
                page.goto(origin+'/'+loc+'/contact.html',wait_until='networkidle')
                form=page.locator('form[data-live-inquiry]');check('live_form:'+loc,form.count()==1)
                for key,value in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'A sample business question for the local QA test.'}.items():
                    page.locator('#'+key).fill(value)
                form.locator('[name=consent]').check();form.locator('button[type=submit]').click()
                page.locator('#draft-result:not([hidden])').wait_for()
                check('live_mock_success:'+loc,len(posts)==(1 if loc=='zh' else 3) and page.locator('#form-error').inner_text()=='')
                check('live_payload:'+loc,posts[-1]['email']=='qa@example.com' and posts[-1]['consent']=='accepted' and posts[-1]['locale']==loc)
                check('live_no_PII_in_URL:'+loc,'qa@example.com' not in page.url and 'QA%20Example' not in page.url)
                state.update(status=503,body='{"success":"false"}')
                for key,value in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'A second business question for the local QA test.'}.items():
                    page.locator('#'+key).fill(value)
                form.locator('[name=consent]').check();form.locator('button[type=submit]').click()
                page.wait_for_function("document.querySelector('#form-error').textContent.length>0")
                check('live_mock_error:'+loc,page.locator('#draft-result').is_hidden() and page.locator('#form-error').inner_text()!='')
                state.update(status=200,body='{"success":"true"}')
            browser.close()
    finally:server.shutdown()

def run():
    baseline=OUT/'baseline'
    if baseline.exists():shutil.rmtree(baseline)
    subprocess.run([sys.executable,str(BASE/'prepare_site.py'),'--out',str(baseline),'--stage',str(OUT/'baseline-source')],check=True)
    preview=build('preview','preview','https://ggcgames.com/');release=build('release','release','https://ggcgames.com/')
    static_checks(preview,'preview');static_checks(release,'release')
    sub=build('subpath','release','https://preview.example.invalid/ggc/');h=soup(sub/'404.html');check('subpath_404_assets',all(t['href'].startswith('/ggc/') for t in h.select('link[rel=stylesheet]')));check('subpath_sitemap','https://preview.example.invalid/ggc/en/index.html' in (sub/'sitemap.xml').read_text())
    browser_checks(preview,release)
    live=build('live-inquiry','release','https://ggcgames.com/','https://formsubmit.co/ajax/minyajing@gmail.com')
    for loc in ['zh','en']:
        contact=soup(live/loc/'contact.html');privacy=soup(live/loc/'privacy.html');updates=soup(live/loc/'updates.html')
        check('live_contact_copy:'+loc,bool(contact.select_one('[data-live-inquiry]')) and 'FormSubmit' in contact.get_text())
        check('live_privacy_copy:'+loc,'FormSubmit' in privacy.get_text())
        check('updates_still_draft:'+loc,not updates.select_one('[data-live-inquiry]') and bool(updates.select_one('[data-interest-mail]')))
    live_inquiry_checks(live)

try:run()
except Exception:report['errors'].append(traceback.format_exc())
finally:
    report['summary']={'checks':len(report['checks']),'failed':sum(not c['passed'] for c in report['checks']),'exceptions':len(report['errors']),'layout_cases':report['layout_cases']}
    (OUT/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report['summary']))
    failed=[c for c in report['checks'] if not c['passed']]
    if failed:print(json.dumps(failed[:30],ensure_ascii=False))
    if report['errors']:print('\n'.join(report['errors']))
sys.exit(1 if report['summary']['failed'] or report['errors'] else 0)
