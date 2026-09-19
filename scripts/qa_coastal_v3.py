"""Browser tests for the live-site build; screenshots are QA evidence, not posters."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import threading, json, csv, shutil, base64, mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'joyce/content/coastal-qa';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/joyce/'
checks={};errors=[]
# Some managed local browsers block loopback URLs. Render the same build inline
# without any network request; CI uses the normal HTTP-served build.
inline_mode=bool(shutil.which('chromium'))
inline_html=(ROOT/'joyce/index.html').read_text()
if inline_mode:
 css=(ROOT/'joyce/assets/coastal-v3.css').read_text()
 js=(ROOT/'joyce/assets/coastal-v3.js').read_text()
 inline_html=inline_html.replace('<link rel="stylesheet" href="/joyce/assets/coastal-v3.css?v=3">','<style>'+css+'</style>')
 inline_html=inline_html.replace('<script src="/joyce/assets/coastal-v3.js?v=3" defer></script>','<script>'+js+'</script>')
 for f in (ROOT/'joyce/assets').iterdir():
  if f.suffix not in ['.avif','.webp','.svg']:continue
  uri='data:'+(mimetypes.guess_type(f.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(f.read_bytes()).decode()
  inline_html=inline_html.replace('/joyce/assets/'+f.name,uri).replace("url('"+f.name+"')","url('"+uri+"')")
 inline_html=inline_html.replace('loading="lazy"','loading="eager"')
def load_site(page,root=False):
 if inline_mode:page.set_content(inline_html,wait_until='load')
 else:page.goto(url.replace('/joyce/','/') if root else url,wait_until='networkidle')
 page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
 page.wait_for_function('Array.from(document.images).every(i=>i.complete)',timeout=10000)

try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or p.chromium.executable_path,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
  page.on('pageerror',lambda e:errors.append(str(e)))
  load_site(page);page.evaluate('document.fonts.ready')
  checks['release']=page.evaluate('window.__ggcRelease')=='2026-09-19-coastal-v3'
  checks['16_services']=page.locator('.service-card').count()==16
  checks['14_capabilities']=page.locator('.capability').count()==14
  checks['12_scenarios']=page.locator('.scenario-grid article').count()==12
  checks['images']=page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  checks['desktop_no_overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  checks['no_pdf_links']=page.locator('a[href$=".pdf"]').count()==0
  checks['no_repository_links']=page.locator('a[href*="github.com"]').count()==0
  checks['no_private_client']=all(s not in page.inner_text('body').lower() for s in ['jordan','ryan','counterparty','past life','reincarnation'])
  checks['all_anchors']=page.evaluate('Array.from(document.querySelectorAll("a[href^=\\"#\\"]")).every(a=>document.getElementById(a.getAttribute("href").slice(1)))')
  checks['unique_ids']=page.evaluate('(()=>{const x=Array.from(document.querySelectorAll("[id]"),e=>e.id);return x.length===new Set(x).size})()')
  page.screenshot(path=str(OUT/'desktop-1440.png'),full_page=False)
  page.screenshot(path=str(OUT/'desktop-full.png'),full_page=True)
  page.locator('[data-currency="usd"]').click();checks['currency_conversion']='16,667' in page.locator('[data-price="S14"]').inner_text()
  page.locator('[data-filter="ai"]').click();checks['ai_filter']=page.locator('.service-card:visible').count()==2
  page.locator('[data-detail="S14"]').first.click();checks['scope_dialog']=page.locator('#service-dialog').is_visible() and page.locator('#dialog-name').inner_text()=='AI Workflow Pilot'
  page.locator('#dialog-enquire').click();checks['selected_service']=page.locator('#service-select').input_value()=='S14'
  for name,value in {'name':'QA Visitor','company':'Example Studio','email':'qa@example.com','stage':'US mobile soft launch','problem':'Check retention and monetization','budget':'CNY 120,000; next month'}.items():page.locator(f'[name="{name}"]').fill(value)
  page.locator('#intake button[type="submit"]').click();checks['brief_prepared']=page.locator('#brief-result').is_visible() and 'Example Studio' in page.locator('#brief').inner_text()
  checks['mailto_only']=page.locator('#email-draft').get_attribute('href').startswith('mailto:minyajing@gmail.com?')
  page.locator('[data-lang="zh"]').click();checks['language_switch']=page.locator('html').get_attribute('lang')=='zh' and 'AI工作流试点' in page.locator('[data-service-name="S14"]').inner_text()
  checks['chinese_form']= 'Example Studio' in page.locator('#brief').inner_text() and '合作服务' in page.locator('#brief').inner_text()
  page.locator('[data-filter="all"]').click();page.locator('[data-currency="cny"]').click();page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/'desktop-zh.png'))
  page.locator('[data-lang="en"]').click();page.locator('[data-stage="2"]').click();checks['stage_interaction']=page.locator('#stage-number').inner_text()=='03'
  page.locator('#stage-2').press('ArrowRight');checks['keyboard_tabs']=page.locator('#stage-number').inner_text()=='04'
  page.locator('[data-sector="3"]').click();checks['sector_interaction']='Body, Mind' in page.locator('#sector-title').inner_text()
  checks['canonical_prices']=all(int(r['CNY_base'])==int(page.locator(f'[data-price="{r["ID"]}"]').inner_text().replace('CNY ','').replace(',','')) for r in csv.DictReader((ROOT/'joyce/rate-card.csv').open()) if r['ID'].startswith('S'))
  load_site(page);page.locator('[data-lang="en"]').click();page.set_viewport_size({'width':390,'height':844});page.evaluate('scrollTo(0,0)')
  checks['mobile_no_overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  page.screenshot(path=str(OUT/'mobile-390.png'),full_page=True)
  page.locator('.menu').click();checks['mobile_menu']=page.locator('#navigation').is_visible();page.locator('#navigation a[href="#services"]').click();checks['mobile_menu_closes']=not page.locator('#navigation').is_visible()
  page.locator('[data-lang="zh"]').click();checks['mobile_zh_no_overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/'mobile-zh.png'),full_page=False)
  page.set_viewport_size({'width':320,'height':740});checks['small_mobile_no_overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  load_site(page,root=True);checks['root_matches']=page.evaluate('window.__ggcRelease')=='2026-09-19-coastal-v3'
  checks['no_js_errors']=not errors
  browser.close()
finally:server.shutdown()
report={'version':'2026-09-19-coastal-v3','checks':checks,'browser_errors':errors,'all_passed':all(checks.values()),'note':'Local browser checks. No email sent or booking made. No PDF generated.'}
(OUT/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['all_passed']:raise SystemExit('QA failed')
