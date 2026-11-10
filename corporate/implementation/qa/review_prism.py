"""Validate the approved visual pass without requiring old colors to remain unchanged.
Runs real HTTP Chromium in CI. Does not publish or submit business information.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys, traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'corporate/implementation/src'
OUT=ROOT/'review-evidence'
BASE='8184a2ea9f1a67598ef78a50242fd59771145545'
ROUTES=['index','expertise','research','decision-os','lab','ventures','about','contact','buttons']
report={'method':'real HTTP Chromium in CI','baseline':BASE,'checks':[],'errors':[],'POSTs':[],'production':False}
OUT.mkdir(exist_ok=True)
def check(name,passed,detail=None):report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    # The user approved new materials, not rewritten business claims or new form behavior.
    for name in ['build_site.py','app.js','buttons.css']:
        baseline=subprocess.check_output(['git','show',BASE+':corporate/implementation/src/'+name],cwd=ROOT)
        check('preserved_source:'+name,baseline==(SRC/name).read_bytes())
    subprocess.run([sys.executable,str(SRC/'build_refined_site.py'),'--out',str(OUT/'site')],check=True)
    for locale in ['zh','en']:
        for name in ROUTES:
            f=OUT/'site'/locale/(name+'.html');doc=BeautifulSoup(f.read_text(),'html.parser')
            check('document:'+locale+'/'+name,bool(doc.title and doc.select_one('h1')))
            check('prism_skin:'+locale+'/'+name,doc.select_one('link[href="../assets/prism.css"]') is not None)
            for el in doc.select('[href],[src]'):
                u=el.get('href') or el.get('src')
                if not u or re.match(r'^(https?:|mailto:|data:|tel:)',u):continue
                parts=urlsplit(u);dest=(f.parent/unquote(parts.path)).resolve() if parts.path else f
                good=dest.exists()
                if good and parts.fragment and dest.suffix=='.html':good=BeautifulSoup(dest.read_text(),'html.parser').find(id=unquote(parts.fragment)) is not None
                check('local_reference:'+locale+'/'+name,good,u)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(OUT/'site')))
    Thread(target=server.serve_forever,daemon=True).start()
    origin='http://127.0.0.1:'+str(server.server_port)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
            context.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
            context.on('request',lambda r:report['POSTs'].append(r.url) if r.method=='POST' else None)
            page=context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
            def load(loc,name,query=''):
                response=page.goto(origin+'/'+loc+'/'+name+'.html'+query,wait_until='networkidle')
                check('http:'+loc+'/'+name,response.status==200)
            for loc in ['zh','en']:
                for width in [320,390,768,1024,1280,1440,1920]:
                    page.set_viewport_size({'width':width,'height':1000})
                    for name in ROUTES:
                        load(loc,name)
                        bounds=page.evaluate('({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth})')
                        check('layout:'+loc+'/'+name+'/'+str(width),bounds['scroll']<=bounds['client']+1,bounds)
                        if name=='index':
                            fits=page.locator('.hero-headline .headline-line').evaluate_all('es=>es.map(e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect().right<=e.getBoundingClientRect().right+2})')
                            check('headline_fit:'+loc+'/'+str(width),all(fits))
                        if width in [390,1440]:page.screenshot(path=str(OUT/(loc+'_'+name+'_'+str(width)+'.png')),full_page=True)
                page.set_viewport_size({'width':1440,'height':1000})
                for name in ['index','decision-os','buttons']:
                    load(loc,name)
                    for group in page.locator('[role=tablist]').all():
                        for tab in group.locator('[role=tab]').all():
                            tab.click();check('tab:'+loc+'/'+name,page.locator('#'+tab.get_attribute('aria-controls')).is_visible())
                        group.locator('[role=tab]').first.focus();page.keyboard.press('End')
                        check('tab_keyboard:'+loc+'/'+name,group.locator('[role=tab]').last.get_attribute('aria-selected')=='true')
                for name in ['expertise','lab']:
                    load(loc,name)
                    for b in page.locator('[data-filter]').all():
                        key=b.get_attribute('data-filter');b.click()
                        check('filter:'+loc+'/'+name+'/'+key,all(key=='all' or e.get_attribute('data-type')==key for e in page.locator('[data-type]:visible').all()))
                    if name=='expertise':
                        page.locator('[data-filter="all"]').click()
                        check('16_services:'+loc,page.locator('#services>.card').count()==16)
                        page.locator('[data-search]').fill('ZZZ_NO_RESULT');check('empty:'+loc,page.locator('[data-empty]').is_visible())
                load(loc,'contact','?service=S12')
                check('service_referral:'+loc,'S12' in page.locator('#message').input_value())
                page.locator('button[type=submit]').click();check('no_false_success:'+loc,page.locator('#draft-result').is_hidden())
                for k,v in {'name':'QA Example','email':'qa@example.com','company':'Example Studio','message':'A sample strategic operating question.'}.items():page.locator('#'+k).fill(v)
                page.locator('[name=consent]').check();page.locator('button[type=submit]').click()
                check('local_draft:'+loc,page.locator('#draft-result').is_visible() and page.locator('#open-email').get_attribute('href').startswith('mailto:'))
                page.set_viewport_size({'width':390,'height':900});load(loc,'index')
                page.locator('[data-menu]').click();check('mobile_menu:'+loc,page.locator('[data-nav]').is_visible())
                page.keyboard.press('Escape');check('mobile_escape:'+loc,page.locator('[data-menu]').get_attribute('aria-expanded')=='false')
            check('no_auto_POST',not report['POSTs']);check('no_JS_errors',not report['errors'])
            browser.close()
    finally:server.shutdown()

try:main()
except Exception:report['errors'].append(traceback.format_exc())
finally:
    report['summary']={'checks':len(report['checks']),'failures':sum(not c['passed'] for c in report['checks']),'errors':len(report['errors'])}
    (OUT/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report['summary']))
    if report['errors']:print('\n'.join(report['errors']))
sys.exit(1 if report['summary']['failures'] or report['errors'] else 0)
