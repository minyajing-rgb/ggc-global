#!/usr/bin/env python3
"""Fullsite V4 HTTP/browser acceptance. No publish, DNS or business POST.
Fonts intentionally use consistent fallbacks in screenshots. Font files excluded.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit,unquote
from datetime import datetime,timezone
import json,re,subprocess,sys,traceback,shutil,zipfile
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import fitz
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'corporate/fullsite-v4'
OUT=ROOT/'fullsite-evidence'
SITE=OUT/'site'
SHOT=OUT/'screens'
OUT.mkdir(exist_ok=True);SHOT.mkdir(exist_ok=True)
report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'checked_at':datetime.now(timezone.utc).isoformat(),'method':'CI-hosted real HTTP Chromium; deterministic fallback fonts','checks':[],'layouts':[],'browser_errors':[],'automatic_posts':[],'production_deployed':False}

def check(name,passed,detail=None):
    report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def run():
    subprocess.run([sys.executable,str(BASE/'prepare_site.py'),'--out',str(SITE),'--stage',str(OUT/'source'),'--normalize-source'],check=True)
    m=json.loads((SITE/'build-manifest.json').read_text())
    report['manifest']=m
    check('96_locale_pages',m['locale_pages']==96)
    check('16_ui_types',m['screen_types']==16)
    for loc in ['zh','en']:
        for route in m['routes']:
            f=SITE/loc/(route+'.html');soup=BeautifulSoup(f.read_text(),'html.parser')
            check('document:'+loc+'/'+route,bool(soup.title and soup.select_one('h1')) and soup.html.get('lang')==('zh-CN' if loc=='zh' else 'en'))
            lang=soup.select_one('[data-locale]')
            check('locale_route:'+loc+'/'+route,lang and lang.get('href')=='../'+('en' if loc=='zh' else 'zh')+'/'+route+'.html')
            for e in soup.select('[href],[src]'):
                u=e.get('href') or e.get('src')
                if not u or re.match(r'^(https?:|mailto:|data:|tel:)',u):continue
                split=urlsplit(u);dest=(f.parent/unquote(split.path)).resolve() if split.path else f
                okay=dest.exists()
                if okay and split.fragment and dest.suffix=='.html':okay=BeautifulSoup(dest.read_text(),'html.parser').find(id=unquote(split.fragment)) is not None
                check('local_reference:'+loc+'/'+route,okay,u)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(SITE)))
    Thread(target=server.serve_forever,daemon=True).start();origin='http://127.0.0.1:'+str(server.server_port)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            ctx=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
            ctx.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=''))
            ctx.on('request',lambda r:report['automatic_posts'].append(r.url) if r.method=='POST' else None)
            page=ctx.new_page();page.on('pageerror',lambda e:report['browser_errors'].append(str(e)))
            def load(loc,route,query=''):
                response=page.goto(origin+'/'+loc+'/'+route+'.html'+query,wait_until='networkidle')
                check('http200:'+loc+'/'+route,response and response.status==200)
            for loc in ['zh','en']:
                for route in m['routes']:
                    load(loc,route)
                    imgs=page.locator('img').evaluate_all('es=>es.map(e=>({src:e.getAttribute("src"),ok:e.complete&&e.naturalWidth>0}))')
                    check('images:'+loc+'/'+route,all(e['ok'] for e in imgs),imgs if not all(e['ok'] for e in imgs) else None)
                for width in [320,390,768,1440]:
                    page.set_viewport_size({'width':width,'height':1000})
                    for route in m['representatives']:
                        load(loc,route)
                        bounds=page.evaluate('({width:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth})')
                        good=bounds['scroll']<=bounds['width']+1
                        report['layouts'].append({'locale':loc,'route':route,'width':width,'passed':good})
                        check('layout:'+loc+'/'+route+'/'+str(width),good,bounds)
                        if width in [390,1440]:page.screenshot(path=str(SHOT/(loc+'_'+route+'_'+str(width)+'.png')),full_page=True)
                page.set_viewport_size({'width':1440,'height':1000})
                for route in ['index','decision-os','buttons']:
                    load(loc,route)
                    for group in page.locator('[role=tablist]').all():
                        for tab in group.locator('[role=tab]').all():
                            tab.click();check('tab_panel:'+loc+'/'+route,page.locator('#'+tab.get_attribute('aria-controls')).is_visible())
                        group.locator('[role=tab]').first.focus();page.keyboard.press('End')
                        check('tab_keyboard:'+loc+'/'+route,group.locator('[role=tab]').last.get_attribute('aria-selected')=='true')
                for route in ['expertise','research','lab']:
                    load(loc,route)
                    for button in page.locator('[data-filter]').all():
                        kind=button.get_attribute('data-filter');button.click();visible=page.locator('[data-type]:visible').all()
                        check('filter:'+loc+'/'+route+'/'+kind,all(kind=='all' or i.get_attribute('data-type')==kind for i in visible))
                    page.locator('[data-filter="all"]').click()
                    if route=='expertise':
                        check('16_services:'+loc,page.locator('#services>.card').count()==16)
                        page.locator('[data-search]').fill('ZZZ_NO_MATCH');check('service_empty:'+loc,page.locator('[data-empty]').is_visible())
                        page.screenshot(path=str(SHOT/(loc+'_state_search_empty.png')))
                load(loc,'product-10')
                page.locator('[data-next]').click();check('gallery_next:'+loc,page.locator('[data-gallery-status]').inner_text()=='2 / 3')
                page.locator('[data-slide-to="2"]').click();check('gallery_dot:'+loc,page.locator('[data-gallery-status]').inner_text()=='3 / 3')
                page.locator('[data-prev]').click();check('gallery_prev:'+loc,page.locator('[data-gallery-status]').inner_text()=='2 / 3')
                for i in range(1,17):
                    sid='S'+str(i).zfill(2);load(loc,'service-'+sid.lower())
                    check('service_cta:'+loc+'/'+sid,page.locator('a[href="contact.html?service='+sid+'"]').count()>0)
                load(loc,'contact','?service=S12');check('service_preselect:'+loc,'S12' in page.locator('#message').input_value())
                page.locator('button[type=submit]').click();check('empty_form_no_success:'+loc,page.locator('#draft-result').is_hidden())
                for k,v in {'name':'QA Example','email':'invalid','company':'Example Studio','message':'A clear operating decision question.'}.items():page.locator('#'+k).fill(v)
                page.locator('[name=consent]').check();page.locator('button[type=submit]').click();check('invalid_email_no_success:'+loc,page.locator('#draft-result').is_hidden())
                page.locator('#email').fill('qa@example.com');page.locator('button[type=submit]').click()
                check('local_mail_draft:'+loc,page.locator('#draft-result').is_visible() and page.locator('#open-email').get_attribute('href').startswith('mailto:minyajing@gmail.com'))
                load(loc,'updates');page.locator('#updates-email').fill('qa@example.com');page.locator('[data-interest] input[type=checkbox]').last.check();page.locator('[data-interest] button[type=submit]').click()
                check('interest_draft:'+loc,page.locator('[data-interest-result]').is_visible() and page.locator('[data-interest-mail]').get_attribute('href').startswith('mailto:'))
                page.locator('.state-demo summary').click();page.locator('[data-show-state="confirmed"]').click();check('state_demo:'+loc,page.locator('[data-state="confirmed"]').is_visible())
                page.screenshot(path=str(SHOT/(loc+'_state_subscription_demo.png')),full_page=True)
                page.set_viewport_size({'width':390,'height':900});load(loc,'index');page.locator('[data-menu]').click()
                check('mobile_menu:'+loc,page.locator('[data-nav]').is_visible());page.keyboard.press('Escape')
                check('mobile_escape:'+loc,page.locator('[data-menu]').get_attribute('aria-expanded')=='false')
            check('no_automatic_POST',not report['automatic_posts']);check('no_JS_errors',not report['browser_errors'])
            # Real HTTP 404 for an unknown URL; the styled 404.html is also reviewed.
            response=page.goto(origin+'/missing-route-test');check('http404_unknown',response.status==404)
            browser.close()
    finally:server.shutdown()
    export_visuals(m)

def export_visuals(m):
    # One full-scroll desktop/mobile spread for each UI type and locale, 32 pages.
    pdf=OUT/'GGC_Fullsite_UI_Review_CN_EN.pdf';c=canvas.Canvas(str(pdf),pagesize=(1440,1600))
    labels={k:k.replace('-',' ').title() for k in m['representatives']}
    first_preview=None
    for loc in ['zh','en']:
        for i,route in enumerate(m['representatives']):
            desktop=Image.open(SHOT/(loc+'_'+route+'_1440.png')).convert('RGB')
            mobile=Image.open(SHOT/(loc+'_'+route+'_390.png')).convert('RGB')
            dw,mw=1120,280;dh=desktop.height*dw/desktop.width;mh=mobile.height*mw/mobile.width
            w,h=1500,max(dh,mh)+122;c.setPageSize((w,h));c.setFillColorRGB(.98,.975,.995);c.rect(0,0,w,h,fill=1,stroke=0)
            c.setFillColorRGB(.16,.09,.23);c.setFont('Helvetica-Bold',24);c.drawString(32,h-40,f'GGC / {i+1:02d} / {labels[route]} / {loc.upper()}')
            c.setFont('Helvetica',10);c.drawString(32,h-63,'Accepted template -> executable HTML/CSS. UI review export; not a production deployment.')
            c.drawImage(ImageReader(desktop),32,h-88-dh,dw,dh);c.drawImage(ImageReader(mobile),1188,h-88-mh,mw,mh)
            c.setFillColorRGB(.49,.39,.55);c.setFont('Helvetica',9);c.drawString(32,16,'Research panels are method briefs; product information panels are not app screenshots.');c.showPage()
    c.save()
    doc=fitz.open(pdf);check('32_pdf_pages',len(doc)==32)
    for i in [0,15,16,31]:
        pg=doc[i];scale=min(1,1400/max(pg.rect.width,pg.rect.height));pix=pg.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False);pix.save(OUT/('pdf-check-'+str(i+1)+'.png'))
    doc.close()
    # Compact visual index, 16 types; full screenshots are also exported individually.
    board=Image.new('RGB',(1600,1540),'#fbf7fd');draw=ImageDraw.Draw(board)
    try:f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15);big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',27)
    except OSError:f=big=None
    draw.text((28,21),'GGC / COMPLETE UI / 16 SCREEN TYPES',fill='#25132f',font=big)
    for i,route in enumerate(m['representatives']):
        img=Image.open(SHOT/('zh_'+route+'_1440.png')).convert('RGB');img=img.crop((0,0,img.width,min(img.height,1100)));img.thumbnail((370,295))
        px=28+(i%4)*395;py=86+(i//4)*360;board.paste(img,(px,py));draw.text((px,py+303),f'{i+1:02d} / {labels[route]}',fill='#68306f',font=f)
    board.save(OUT/'GGC_Fullsite_UI_16_Types_Overview.png')

try:run()
except Exception:report['browser_errors'].append(traceback.format_exc())
finally:
    report['summary']={'checks':len(report['checks']),'layouts':len(report['layouts']),'failed':sum(not c['passed'] for c in report['checks']),'exceptions':len(report['browser_errors'])}
    (OUT/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report['summary']))
    if report['browser_errors']:print('\n'.join(report['browser_errors']))
    failed=[c for c in report['checks'] if not c['passed']]
    if failed:print(json.dumps(failed[:20],ensure_ascii=False))
    # Reproducible source + generated pages + visual evidence, never font binaries.
    with zipfile.ZipFile(OUT/'GGC_Fullsite_Implementation_and_UI.zip','w',zipfile.ZIP_DEFLATED) as z:
        for folder,prefix in [(SITE,'site'),(OUT/'source','source'),(SHOT,'screens')]:
            if folder.exists():
                for p in folder.rglob('*'):
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.ttf','.otf','.woff','.woff2']:z.write(p,prefix+'/'+p.relative_to(folder).as_posix())
        for p in [OUT/'review.json',OUT/'GGC_Fullsite_UI_Review_CN_EN.pdf',OUT/'GGC_Fullsite_UI_16_Types_Overview.png']:
            if p.exists():z.write(p,p.name)
        for p in BASE.glob('*.md'):z.write(p,'docs/'+p.name)
sys.exit(1 if report['summary']['failed'] or report['summary']['exceptions'] else 0)
