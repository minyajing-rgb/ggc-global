#!/usr/bin/env python3
"""Source-only product/performance review. HTTP Chromium in CI; --offline locally.
External font CSS is stubbed for repeatability: timings are NOT field Core Web Vitals.
No deployment, analytics activation, real inquiry or subscription POST.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit, unquote
import argparse, base64, gzip, hashlib, json, re, shutil, statistics, subprocess, sys, traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'corporate/fullsite-v4'
parser=argparse.ArgumentParser();parser.add_argument('--before',type=Path);parser.add_argument('--out',type=Path,default=ROOT/'performance-evidence');parser.add_argument('--offline',action='store_true');args=parser.parse_args()
OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
BEFORE=args.before.resolve() if args.before else OUT/'baseline';AFTER=OUT/'candidate'
sys.path.insert(0,str(BASE/'performance'))
from optimize_site import optimize_site, attrs
report={'mode':'offline DOM' if args.offline else 'CI HTTP Chromium','font_policy':'external Google font CSS stubbed; selected fonts and weights preserved in artifact','checks':[],'exceptions':[],'post_requests':[],'timings':[], 'published':False}
def check(name,passed,detail=None):report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})

class Server(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
    def send_head(self):
        path=Path(self.translate_path(self.path))
        if path.is_file() and path.suffix in ['.html','.css','.js','.svg'] and 'gzip' in self.headers.get('Accept-Encoding',''):
            from io import BytesIO
            raw=path.read_bytes();encoded=gzip.compress(raw,compresslevel=9,mtime=0)
            self.send_response(200);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Content-Encoding','gzip');self.send_header('Vary','Accept-Encoding');self.send_header('Content-Length',str(len(encoded)));self.end_headers();return BytesIO(encoded)
        return super().send_head()

def inline(site,rel):
    text=(site/rel).read_text();scripts=[]
    def script(m):scripts.append((site/'assets'/m[1].split('/')[-1]).read_text());return ''
    text=re.sub(r'<script\b[^>]*src="([^"]+)"[^>]*>\s*</script>',script,text)
    def css(m):
        typ,a=attrs(m[0]);u=a.get('href','')
        if a.get('rel')!='stylesheet' or u.startswith('https:'):return ''
        data=(site/'assets'/u.split('/')[-1]).read_text();data=re.sub(r'@import\s+url\([^)]*\)\s*;','',data)
        def image(mm):
            path=site/'assets'/mm[2]
            if not path.is_file():return mm[0]
            return 'url("data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode()+'")'
        data=re.sub(r'url\(([\"\']?)([^\"\')]+)\1\)',image,data)
        return '<style>'+data+'</style>'
    text=re.sub(r'<link\b[^>]*>',css,text)
    def image(m):
        tag=m[0];p=site/'assets'/m[1].split('/')[-1];mime='image/svg+xml' if p.suffix=='.svg' else 'image/webp'
        return tag.replace(m[1],'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()).replace('loading="lazy"','loading="eager"')
    text=re.sub(r'<img\b[^>]*src="([^"]+)"[^>]*>',image,text)
    return text.replace('</body>',''.join('<script>'+s+'</script>' for s in scripts)+'</body>')

def run():
    if not args.before:
        subprocess.run([sys.executable,str(BASE/'build_ready.py'),'--out',str(BEFORE),'--mode','release','--base-url','https://ggcgames.com/'],check=True)
    if AFTER.exists():raise ValueError('Use a fresh evidence directory')
    shutil.copytree(BEFORE,AFTER);perf=optimize_site(AFTER);report['performance']=perf
    m=json.loads((BEFORE/'build-manifest.json').read_text());reps=m['representatives']+['privacy']
    check('98_localized_pages',perf['locale_pages']==98)
    home=next(x for x in perf['pages'] if x['path']=='zh/index.html');report['home_resource_budget']=home
    check('css_gzip_budget_18KiB',home['css']['gzip_after']<=18*1024)
    check('js_gzip_budget_6KiB',home['js']['gzip_after']<=6*1024)
    check('css_reduction_at_least_15_percent',home['css']['gzip_after']<=.85*home['css']['gzip_before'])
    check('requests_6_css_to_1',home['css']['requests_before']==6 and home['css']['requests_after']==1)
    check('requests_3_js_to_1',home['js']['requests_before']==3 and home['js']['requests_after']==1)
    for rel,digest in perf['original_assets_sha256'].items():check('preserved_asset:'+rel,hashlib.sha256((AFTER/rel).read_bytes()).hexdigest()==digest)
    for rel in [x.relative_to(BEFORE) for x in BEFORE.rglob('*.html')]:
        a=BeautifulSoup((BEFORE/rel).read_text(),'html.parser');b=BeautifulSoup((AFTER/rel).read_text(),'html.parser')
        check('text:'+str(rel),a.get_text()==b.get_text())
        for selector in ['meta','title','a','form','button','input','select','textarea','script[type="application/ld+json"]']:
            check('preserved_'+selector+':'+str(rel),[str(e) for e in a.select(selector)]==[str(e) for e in b.select(selector)])
        for h in b.select('h1,h2,h3,h4,h5,h6'):
            check('nonempty_accessible_heading:'+str(rel),bool(h.get_text(strip=True)) or h.get('aria-hidden')=='true')
        for el in b.select('[src],[href]'):
            u=el.get('src') or el.get('href');part=urlsplit(u)
            if part.scheme or part.netloc:continue
            path=unquote(part.path)
            dest=(AFTER/path.lstrip('/')) if path.startswith('/') else (AFTER/rel).parent/path if path else AFTER/rel
            okay=dest.is_file()
            if okay and part.fragment and dest.suffix=='.html':okay=BeautifulSoup(dest.read_text(),'html.parser').find(id=unquote(part.fragment)) is not None
            check('local_target:'+str(rel),okay,u)
        for image in b.select('img[src$=".webp"]'):
            check('image_dimensions:'+str(rel),image.has_attr('width') and image.has_attr('height'))
            check('priority_not_lazy:'+str(rel),not(image.get('loading')=='lazy' and image.get('fetchpriority')=='high'))
    for f in ['sitemap.xml','robots.txt','readiness-manifest.json']:
        check('unchanged_'+f,(BEFORE/f).read_bytes()==(AFTER/f).read_bytes())
    server=None
    if not args.offline:
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Server,directory=str(OUT)));Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            options={'headless':True,'args':['--no-sandbox']}
            if args.offline:options['executable_path']='/usr/bin/chromium'
            browser=p.chromium.launch(**options);ctx=browser.new_context(reduced_motion='reduce')
            ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
            ctx.on('request',lambda r:report['post_requests'].append(r.url) if r.method=='POST' else None)
            page=ctx.new_page();page.on('pageerror',lambda e:report['exceptions'].append(str(e)))
            def load(site,rel):
                nonlocal page
                if args.offline:
                    viewport=page.viewport_size;page.close();page=ctx.new_page();page.set_viewport_size(viewport or {'width':1440,'height':1000});page.on('pageerror',lambda e:report['exceptions'].append(str(e)))
                    page.set_content(inline(site,rel),wait_until='load')
                else:
                    r=page.goto(f'http://127.0.0.1:{server.server_port}/'+site.name+'/'+str(rel),wait_until='networkidle');check('HTTP200:'+str(rel),r.status==200)
                page.wait_for_timeout(60)
            for loc in ['zh','en']:
                for width in [320,390,768,1440]:
                    page.set_viewport_size({'width':width,'height':1000})
                    for name in reps:
                        rel=Path(loc)/(name+'.html');load(AFTER,rel)
                        check('layout:'+str(rel)+':'+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                        if width not in [390,1440]:continue
                        geom=[];shots=[]
                        for label,site in [('before',BEFORE),('after',AFTER)]:
                            load(site,rel)
                            # Compare fully loaded layout/paint, not a lazy image's temporary placeholder.
                            page.locator('img').evaluate_all('es=>es.forEach(e=>e.loading="eager")')
                            page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
                            geom.append(page.locator('h1,h2,.ggc-btn,.hero,.portrait-panel img,.book-card').evaluate_all('es=>es.map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return [r.x,r.y,r.width,r.height,s.color,s.backgroundImage,s.fontFamily,s.fontWeight]})'))
                            if name in ['index','about','book','contact']:
                                fp=OUT/(label+'_'+loc+'_'+name+'_'+str(width)+'.png');page.screenshot(path=str(fp),full_page=True);shots.append(fp)
                        check('geometry:'+str(rel)+':'+str(width),geom[0]==geom[1])
                        if shots:
                            a,b=[Image.open(f).convert('RGB') for f in shots]
                            check('pixels:'+str(rel)+':'+str(width),a.size==b.size and ImageChops.difference(a,b).getbbox() is None)
                page.set_viewport_size({'width':1440,'height':1000})
                for name in ['index','decision-os','buttons']:
                    load(AFTER,Path(loc)/(name+'.html'))
                    for group in page.locator('[role=tablist]').all():
                        group.locator('[role=tab]').first.focus();page.keyboard.press('End');tab=group.locator('[role=tab]').last
                        check('keyboard_tab:'+loc+name,tab.get_attribute('aria-selected')=='true' and page.locator('#'+tab.get_attribute('aria-controls')).is_visible())
                for name in ['expertise','lab','research']:
                    load(AFTER,Path(loc)/(name+'.html'))
                    for button in page.locator('[data-filter]').all():
                        button.click();key=button.get_attribute('data-filter');check('filter:'+loc+name,all(key=='all' or e.get_attribute('data-type')==key for e in page.locator('[data-type]:visible').all()))
                load(AFTER,Path(loc)/'product-10.html');page.locator('[data-next]').click();check('gallery:'+loc,page.locator('[data-gallery-status]').inner_text()=='2 / 3')
                load(AFTER,Path(loc)/'contact.html');page.locator('button[type=submit]').click();check('no_fake_success:'+loc,page.locator('#draft-result').is_hidden())
                for k,v in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'A bounded operating question for testing.'}.items():page.locator('#'+k).fill(v)
                page.locator('[name=consent]').check();page.locator('button[type=submit]').click();check('local_draft:'+loc,page.locator('#open-email').get_attribute('href').startswith('mailto:') and page.locator('#draft-result').is_visible())
                page.set_viewport_size({'width':390,'height':900});load(AFTER,Path(loc)/'index.html');page.locator('[data-menu]').click();page.keyboard.press('Escape');check('mobile_escape:'+loc,page.locator('[data-menu]').get_attribute('aria-expanded')=='false')
            check('no_POST',not report['post_requests'])
            # Enabled inquiries remain a separate, explicitly requested build. Responses
            # below are mocked locally; this does not activate a provider or send mail.
            if not args.offline:
                live=OUT/'live-mock-candidate'
                subprocess.run([sys.executable,str(BASE/'build_fast.py'),'--out',str(live),'--mode','release','--base-url','https://ggcgames.com/','--inquiry-endpoint','https://formsubmit.co/ajax/minyajing@gmail.com'],check=True)
                live_ctx=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
                live_ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
                for loc in ['zh','en']:
                    for okay in [False,True]:
                        live_ctx.route('https://formsubmit.co/ajax/minyajing@gmail.com',lambda r,ok=okay:r.fulfill(status=200 if ok else 500,content_type='application/json',body=json.dumps({'success': 'true' if ok else 'false','message':'mocked'})))
                        lp=live_ctx.new_page();lp.goto(f'http://127.0.0.1:{server.server_port}/'+live.name+'/'+loc+'/contact.html',wait_until='networkidle')
                        for k,v in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'A mocked business inquiry, never delivered.'}.items():lp.locator('#'+k).fill(v)
                        lp.locator('[name=consent]').check();lp.locator('button[type=submit]').click();lp.wait_for_timeout(500)
                        check('live_mock:'+loc+':'+str(okay),lp.locator('#draft-result').is_visible()==okay)
                        lp.close();live_ctx.unroute('https://formsubmit.co/ajax/minyajing@gmail.com')
                live_ctx.close();report['live_inquiry_tests']='4 mocked success/failure cases; no real provider submission or email'
            # Resource bytes are reproducible; these lab times are observations, not acceptance scores.
            if not args.offline:
                observe="""window.__lab={lcp:0,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lab.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__lab.cls+=e.value}).observe({type:'layout-shift',buffered:true});"""
                for rel in ['zh/index.html','en/index.html','zh/about.html','en/book.html']:
                    for iteration in range(3):
                        for label,site in [('before',BEFORE),('after',AFTER)]:
                            c=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,reduced_motion='reduce');c.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
                            pp=c.new_page();pp.add_init_script(observe);cdp=c.new_cdp_session(pp);cdp.send('Network.enable');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True});cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':100000,'connectionType':'cellular4g'});cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
                            pp.goto(f'http://127.0.0.1:{server.server_port}/'+site.name+'/'+rel,wait_until='networkidle');pp.wait_for_timeout(1000)
                            metrics=pp.evaluate('({lcp_ms:window.__lab.lcp,load_window_layout_shift:window.__lab.cls,fcp_ms:performance.getEntriesByName("first-contentful-paint")[0]?.startTime,resources:performance.getEntriesByType("resource").map(e=>({name:e.name.split("/").pop(),bytes:e.encodedBodySize}))})')
                            report['timings'].append({'version':label,'route':rel,'run':iteration+1,**metrics});c.close()
                report['lab_environment']={'CPU_slowdown':4,'RTT_ms':150,'download_bytes_per_second':200000,'cold_cache':True,'compression':'QA fixture gzip-9','external_fonts':'stubbed; no provider latency included','INP':'not measured; no field traffic or RUM','CLS':'load-window shift sum, not field p75 or session-window certification'}
            browser.close()
    finally:
        if server:server.shutdown()
    check('no_JS_exceptions',not report['exceptions'])

try:run()
except Exception:report['exceptions'].append(traceback.format_exc())
finally:
    report['summary']={'checks':len(report['checks']),'failed':sum(not x['passed'] for x in report['checks']),'exceptions':len(report['exceptions'])}
    (OUT/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report['summary']));print(json.dumps(report.get('home_resource_budget',{})))
    print(json.dumps([x for x in report['checks'] if not x['passed']][:15]))
    if report['exceptions']:print('\n'.join(report['exceptions']))
sys.exit(1 if report['summary']['failed'] or report['summary']['exceptions'] else 0)
