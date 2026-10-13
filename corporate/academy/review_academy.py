#!/usr/bin/env python3
"""Review the isolated course directory. Default is real HTTP; --offline is explicit.
Does not submit personal information or retrieve paid course contents.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit, unquote
import argparse, base64, hashlib, json, mimetypes, re, shutil, traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def inline_document(path):
    """Offline DOM rendering, not deployed-browser acceptance."""
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    def uri(p):
        mime=mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
        return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
    for link in soup.select('link[rel=stylesheet]'):
        f=(path.parent/link['href']).resolve();css=f.read_text(encoding='utf-8')
        def rewrite(m):
            candidate=(f.parent/m.group(1).strip('"\'')).resolve()
            return 'url("'+uri(candidate)+'")' if candidate.is_file() else m.group(0)
        css=re.sub(r'url\(([^)]+)\)',rewrite,css)
        style=soup.new_tag('style');style.string=css;link.replace_with(style)
    for im in soup.select('img[src]'):im['src']=uri((path.parent/im['src']).resolve())
    for script in soup.select('script[src]'):
        js=(path.parent/script['src']).resolve().read_text(encoding='utf-8');script.decompose()
        node=soup.new_tag('script');node.string=js;soup.body.append(node)
    return str(soup)

def review(site,evidence,offline=False):
    evidence.mkdir(exist_ok=True,parents=True);checks=[];errors=[];requests=[];server=None
    def check(name,passed,detail=None):checks.append({'name':name,'passed':bool(passed),'detail':detail})
    try:
        for locale in ['zh','en']:
            f=site/locale/'index.html';s=BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser')
            check(locale+' courses',len(s.select('[data-course]'))==13)
            check(locale+' h1',len(s.select('h1'))==1)
            check(locale+' no embeds or collection forms',not s.select('video,audio,iframe,form'))
            check(locale+' paid content absent',not list(site.rglob('*.mp4')))
            for a in s.select('[href],[src]'):
                u=a.get('href') or a.get('src');url=urlsplit(u)
                if url.scheme or url.netloc:continue
                dest=(f.parent/unquote(url.path)).resolve() if url.path else f
                ok=dest.is_file()
                if ok and url.fragment:ok=BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser').find(id=url.fragment) is not None
                check(locale+' local link',ok,u)
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        if not offline:
            server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(site)))
            Thread(target=server.serve_forever,daemon=True).start()
            origin='http://127.0.0.1:'+str(server.server_port)
        with sync_playwright() as p:
            launch={'headless':True}
            if offline and shutil.which('chromium'):launch['executable_path']=shutil.which('chromium')
            browser=p.chromium.launch(**launch)
            context=browser.new_context(reduced_motion='reduce')
            context.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,body=''))
            context.on('request',lambda r:requests.append({'method':r.method,'url':r.url}))
            page=context.new_page();page.on('pageerror',lambda err:errors.append(str(err)))
            for locale in ['zh','en']:
                for width in [320,390,768,1440]:
                    page.set_viewport_size({'width':width,'height':1000})
                    if offline:page.set_content(inline_document(site/locale/'index.html'),wait_until='load')
                    else:
                        response=page.goto(origin+'/'+locale+'/index.html',wait_until='networkidle')
                        check(locale+' http',response.status==200)
                    bounds=page.evaluate('({w:document.documentElement.clientWidth,s:document.documentElement.scrollWidth})')
                    check(locale+' layout '+str(width),bounds['s']<=bounds['w']+1,bounds)
                    for im in page.locator('img').all():
                        if im.is_visible():im.scroll_into_view_if_needed();im.evaluate('e=>e.decode().catch(()=>{})')
                    page.evaluate('window.scrollTo(0,0)')
                    check(locale+' images',page.locator('img').evaluate_all('els=>els.every(e=>!e.getClientRects().length||(e.complete&&e.naturalWidth>0))'))
                    if width in [390,1440]:page.screenshot(path=str(evidence/(locale+'_'+str(width)+'.png')),full_page=True)
                for button in page.locator('[data-filter]').all():
                    key=button.get_attribute('data-filter');button.focus();page.keyboard.press('Enter')
                    visible=page.locator('[data-course]:visible').all()
                    check(locale+' filter '+key,bool(visible) and all(key=='all' or x.get_attribute('data-category')==key for x in visible))
                page.locator('[data-filter=all]').click();page.locator('[data-search]').fill('ZZ_NO_RESULT')
                check(locale+' empty',page.locator('[data-empty]').is_visible());page.locator('[data-search]').fill('')
                check(locale+' reset',page.locator('[data-course]:visible').count()==13)
                target=page.locator('[data-locale]').get_attribute('href')
                check(locale+' paired locale link',target=='../'+('en' if locale=='zh' else 'zh')+'/index.html')
                if not offline:
                    page.locator('[data-locale]').click()
                    check(locale+' locale navigation',('/'+('en' if locale=='zh' else 'zh')+'/index.html') in page.url)
            check('no personal POST',not any(r['method']=='POST' for r in requests));check('no js errors',not errors)
            browser.close()
    except Exception:errors.append(traceback.format_exc())
    finally:
        if server:server.shutdown()
        result={'checks':checks,'errors':errors,'summary':{'checks':len(checks),'failed':sum(not c['passed'] for c in checks),'errors':len(errors)},'scope':('Offline in-memory Chromium DOM' if offline else 'Real local HTTP Chromium')+'; not production-domain acceptance','deployed':False}
        (evidence/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result['summary']))
        if errors:print('\n'.join(errors))
    if result['summary']['failed'] or errors:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args();review(a.site.resolve(),a.out.resolve(),a.offline)
