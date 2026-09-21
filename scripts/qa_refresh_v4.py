"""Test built files or the actual HTTPS site. No messages or payments are sent."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import csv, json, os, mimetypes, shutil, sys, traceback
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'joyce/content/refresh-qa';OUT.mkdir(parents=True,exist_ok=True)
VERSION='2026-09-21-credibility-v7'
LIVE=os.environ.get('GGC_LIVE_BASE','').rstrip('/')
BASE=LIVE or 'https://ggc.test'
checks={};errors=[]
def error_report(kind,error,tb):
 report={'version':VERSION,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'mode':'actual live HTTPS' if LIVE else 'built files','base':BASE,'checks':checks,'errors':errors,'exception':''.join(traceback.format_exception(kind,error,tb)),'all_passed':False}
 (OUT/('live-report.json' if LIVE else 'report.json')).write_text(json.dumps(report,indent=2))
 sys.__excepthook__(kind,error,tb)
sys.excepthook=error_report
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
 if not LIVE:
  def route_request(route):
   rel=unquote(urlparse(route.request.url).path).lstrip('/')
   target=(ROOT/rel).resolve()
   if target.is_dir():target=target/'index.html'
   if ROOT.resolve() not in target.parents or not target.is_file():route.fulfill(status=404,body='Not found');return
   route.fulfill(status=200,body=target.read_bytes(),content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
  context.route(BASE+'/**',route_request)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 def load(path='/joyce/?lang=en&v=refresh-v4'):
  response=page.goto(BASE+path,wait_until='networkidle',timeout=60000)
  assert response and response.status==200
  page.evaluate("document.querySelectorAll('img').forEach(x=>x.loading='eager')")
  page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)',timeout=20000)
  page.evaluate('async()=>{await Promise.all(Array.from(document.images,i=>i.decode().catch(()=>{})));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}')
  return response
 load()
 checks['release_marker']=page.evaluate('window.__ggcRelease===window.__ggcRefresh') and page.evaluate('window.__ggcRelease')==VERSION
 checks['16_services']=page.locator('.service-card').count()==16
 checks['executive_profile']=page.locator('#executive-profile').count()==1 and page.locator('.executive-proof article').count()==6
 checks['portfolio_ecosystem']=page.locator('#portfolio .portfolio-card').count()==6
 checks['public_voice']=page.locator('#public-voice .voice-card').count()==4
 checks['annual_partnership']=page.locator('#annual-partnership .annual-card').count()==3
 checks['newsroom']=page.locator('#newsroom .news-card').count()==6
 checks['newsroom_award']='Tencent-alumni' in page.locator('#newsroom').inner_text()
 checks['newsroom_book']='978-7-111-75037-6' in page.locator('#newsroom').inner_text()
 checks['speaking_timeline']=page.locator('#newsroom .timeline-row').count()==6
 checks['speaking_2026']='AI-driven user growth' in page.locator('#newsroom .news-timeline').inner_text()
 checks['news_nav']=page.locator('nav a[href="#newsroom"]').count()==1
 checks['annual_primary_price']='1,280,000' in page.locator('#annual-partnership .annual-card.featured').inner_text()
 checks['14_capabilities']=page.locator('.capability').count()==14
 checks['12_scenarios']=page.locator('.scenario-grid article').count()==12
 checks['three_starting_points']=page.locator('.start-card').count()==3
 checks['hero_current_asset']='coastal-portrait-v4' in page.locator('.hero-art img').evaluate('e=>e.currentSrc')
 checks['hero_render_not_upscaled']=page.locator('.hero-art').evaluate('e=>e.getBoundingClientRect().width<=538')
 checks['responsive_sources']=page.locator('picture.portrait-picture source').get_attribute('srcset').count('w')==2
 checks['jpeg_fallback']=page.locator('.hero-art img').get_attribute('src').endswith('-v4.jpg')
 checks['images_loaded']=page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
 checks['desktop_no_overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 checks['no_pdf_links']=page.locator('a[href$=".pdf"]').count()==0
 checks['no_repository_links']=page.locator('a[href*="github.com"]').count()==0
 checks['public_business_only']=all(s not in page.inner_text('body').lower() for s in ['jordan','ryan','counterparty','past life','reincarnation'])
 checks['anchors']=page.evaluate("Array.from(document.links).filter(a=>a.getAttribute('href').startsWith('#')).every(a=>document.getElementById(a.getAttribute('href').slice(1)))")
 checks['unique_ids']=page.evaluate('(()=>{const x=Array.from(document.querySelectorAll("[id]"),e=>e.id);return x.length===new Set(x).size})()')
 page.screenshot(path=str(OUT/'desktop-1440.png'))
 page.screenshot(path=str(OUT/'desktop-full.png'),full_page=True)
 page.locator('.start-card[data-detail="S03"]').click()
 checks['product_review_path']=page.locator('#service-dialog').is_visible() and 'Monetization Audit' in page.locator('#dialog-name').inner_text()
 checks['named_dialog']=page.locator('#service-dialog').get_attribute('aria-labelledby')=='dialog-name'
 checks['modal_scroll_lock']=page.evaluate('getComputedStyle(document.body).overflow==="hidden"')
 page.locator('#dialog-enquire').click();page.wait_for_timeout(150)
 checks['selected_product_review']=page.locator('#service-select').input_value()=='S03' and 'Monetization Audit' in page.locator('#selection-name').inner_text()
 checks['selected_fee']='50,000' in page.locator('#selection-fee').inner_text()
 page.locator('[data-currency="usd"]').click();page.wait_for_timeout(150)
 checks['currency_conversion']='16,667' in page.locator('[data-price="S14"]').inner_text()
 checks['summary_currency']='6,944' in page.locator('#selection-fee').inner_text()
 page.locator('[data-filter="ai"]').click();checks['ai_filter']=page.locator('.service-card:visible').count()==2
 page.locator('.service-card [data-detail="S14"]').first.click();page.locator('#dialog-enquire').click();page.wait_for_timeout(150)
 checks['ai_selection']=page.locator('#service-select').input_value()=='S14' and 'Workflow Pilot' in page.locator('#selection-name').inner_text()
 for name,value in {'name':'QA Visitor','company':'Example Studio','email':'qa@example.com','stage':'US mobile soft launch','problem':'Review retention','budget':'CNY 120,000; next month'}.items():page.locator('[name="'+name+'"]').fill(value)
 page.locator('#intake button[type="submit"]').click()
 checks['draft_builder']=page.locator('#brief-result').is_visible() and 'Example Studio' in page.locator('#brief').inner_text()
 checks['no_automatic_send']=page.locator('#email-draft').get_attribute('href').startswith('mailto:')
 page.locator('[data-lang="zh"]').click();page.wait_for_timeout(150)
 checks['chinese_interface']='我需要评审产品' in page.locator('.start-card[data-detail="S03"]').inner_text()
 checks['chinese_summary']='AI工作流试点' in page.locator('#selection-name').inner_text()
 checks['chinese_draft']='合作服务' in page.locator('#brief').inner_text()
 page.locator('[data-filter="all"]').click();page.locator('[data-currency="cny"]').click();page.locator('[data-lang="en"]').click()
 checks['canonical_prices']=all(int(r['CNY_base'])==int(page.locator('[data-price="'+r['ID']+'"]').inner_text().replace('CNY ','').replace(',','')) for r in csv.DictReader((ROOT/'joyce/rate-card.csv').open()) if r['ID'].startswith('S'))
 page.locator('[data-stage="2"]').click();checks['operating_stage']=page.locator('#stage-number').inner_text()=='03'
 page.locator('#stage-2').press('ArrowRight');checks['keyboard_stage']=page.locator('#stage-number').inner_text()=='04'
 page.locator('[data-sector="3"]').click();checks['sector_selection']='Body, Mind' in page.locator('#sector-title').inner_text()
 load('/joyce/?lang=en&service=S03&v=refresh-v4#services');checks['shareable_service_url']=page.locator('#service-dialog').is_visible() and 'Monetization Audit' in page.locator('#dialog-name').inner_text()
 page.locator('#service-dialog').press('Escape');checks['escape_closes_dialog']=not page.locator('#service-dialog').is_visible()
 load('/?lang=en&v=refresh-v4');checks['root_release']=page.evaluate('window.__ggcRelease')==VERSION
 for width in [390,320,768,1024]:
  page.set_viewport_size({'width':width,'height':844});page.evaluate('scrollTo(0,0)')
  checks[f'layout_{width}']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  if width==390:
   page.screenshot(path=str(OUT/'mobile-390.png'))
   page.locator('.menu').click();checks['mobile_menu']=page.locator('#navigation').is_visible()
   page.locator('#navigation a[href="#services"]').click();checks['mobile_menu_closes']=not page.locator('#navigation').is_visible()
   page.locator('[data-lang="zh"]').click();checks['mobile_chinese_layout']=page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/'mobile-zh.png'));page.locator('[data-lang="en"]').click()
 checks['no_js_errors']=not errors
 browser.close()
report={'version':VERSION,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'mode':'actual live HTTPS' if LIVE else 'local built files served through browser routes','base':BASE,'checks':checks,'errors':errors,'all_passed':all(checks.values()),'note':'No PDF generated. No email sent. Native-source image optimization, not invented 4K detail.'}
(OUT/('live-report.json' if LIVE else 'report.json')).write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['all_passed']:raise SystemExit('QA failed')
