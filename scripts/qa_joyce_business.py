#!/usr/bin/env python3
"""Render and verify the public site. Local-only form test; no messages are sent."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import base64, csv, json, mimetypes, os, re, shutil, threading
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; J=ROOT/'joyce'; OUT=J/'downloads';OUT.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
checks={}; errors=[]
def load(page, relative):
    if not os.environ.get('INLINE_QA'):
        page.goto(base+'/'+relative,wait_until='networkidle'); return
    target=ROOT/relative
    if target.is_dir(): target=target/'index.html'
    raw=target.read_text()
    raw=re.sub(r'<link rel="stylesheet" href="([^"]+)">',lambda m:'<style>'+(target.parent/m[1]).read_text()+'</style>',raw)
    raw=re.sub(r'<script src="([^"]+)" defer></script>',lambda m:'<script>'+(target.parent/m[1]).read_text()+'</script>',raw)
    def image(m):
        f=(target.parent/m[1]).resolve(); mime=mimetypes.guess_type(f)[0]
        return 'src="data:'+mime+';base64,'+base64.b64encode(f.read_bytes()).decode()+'"'
    raw=re.sub(r'src="((?:assets/|../)[^"]+\.(?:webp|svg))"',image,raw)
    raw=re.sub(r'<link rel="icon"[^>]+>','',raw)
    page.set_content(raw,wait_until='networkidle')
with sync_playwright() as p:
    opts={'headless':True}
    override=os.environ.get('CHROMIUM_PATH')
    if override: opts['executable_path']=override
    browser=p.chromium.launch(**opts)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
    page.on('pageerror',lambda err: errors.append(str(err)))
    load(page,'joyce/')
    checks['services']=page.locator('tr[data-service-id]').count()==16
    checks['capabilities']=page.locator('#capabilities details').count()==14
    checks['scenarios']=page.locator('#work details').count()==12
    checks['images_loaded']=page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)')
    checks['desktop_overflow']=page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
    page.screenshot(path=str(OUT/'website-desktop.png'),full_page=False,animations='disabled')
    page.screenshot(path=str(OUT/'website-full.png'),full_page=True,animations='disabled')
    page.locator('[data-node="5"]').click();checks['system_map']='workflow' in page.locator('#system-title').inner_text().lower()
    page.locator('[data-currency="usd"]').click();checks['usd_reference']='694' in page.locator('[data-service-id="S01"] .price').inner_text()
    page.locator('[data-currency="cny"]').click()
    page.locator('[data-filter="ai"]').click();checks['ai_filter']=page.locator('tr[data-service-id]:visible').count()==2
    page.locator('[data-filter="all"]').click()
    page.locator('.choose[data-service="S12"]').click();checks['service_selection']=page.locator('#service').input_value()=='S12'
    for key,value in {'name':'QA Test','company':'Example Studio','email':'test@example.com','stage':'Mobile game / US / soft launch','problem':'A test request, not a client inquiry.','budget':'To be scoped'}.items():page.locator('#'+key).fill(value)
    page.locator('#intake button[type="submit"]').click()
    checks['brief_builder']=page.locator('#result').is_visible() and page.locator('#mail-link').get_attribute('href').startswith('mailto:')
    page.set_viewport_size({'width':390,'height':844});load(page,'joyce/')
    checks['mobile_overflow']=page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
    checks['mobile_images']=page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)')
    page.screenshot(path=str(OUT/'website-mobile.png'),full_page=True,animations='disabled')
    text=page.locator('body').inner_text()
    checks['english_visible_copy']=not bool(re.search('[\u4e00-\u9fff]',text))
    checks['public_scope_only']=('illustrative scope examples' in text and 'Counterparty A' not in text)
    page.set_viewport_size({'width':1100,'height':1600});load(page,'joyce/rate-card.html')
    checks['poster_rates']=page.locator('.rate').count()==9
    checks['poster_images']=page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)')
    page.locator('.poster').screenshot(path=str(OUT/'Joyce_GGC_Rate_Card_EN.png'))
    page.emulate_media(media='print')
    height=int(page.locator('.poster').bounding_box()['height'])+2
    page.pdf(path=str(OUT/'Joyce_GGC_Rate_Card_EN.pdf'),width='1000px',height=f'{height}px',print_background=True,prefer_css_page_size=False,margin={'top':'0','bottom':'0','left':'0','right':'0'})
    checks['poster_height_px']=height
    checks['no_js_errors']=not errors
    browser.close()
server.shutdown()
report={'version':'2026-09-19-v2','checks':checks,'browser_errors':errors,'note':'Local browser tests. No email sent. Live-domain validation and deployment are separate.'}
(J/'content/release-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
failed=[k for k,v in checks.items() if v is False]
if failed: raise RuntimeError('QA failed: '+', '.join(failed))
