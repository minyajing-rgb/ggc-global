"""Review an isolated corporate build; never publish, send or write business data."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from datetime import datetime, timezone
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys, traceback
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'review-evidence'
OUT.mkdir(exist_ok=True)
BASE = 'fa48a4639bdfbf03fdf74f3640ac914ded15be9c'
SRC = ROOT / 'corporate/implementation/src'
ROUTES = ['index', 'expertise', 'research', 'decision-os', 'lab', 'ventures', 'about', 'contact', 'buttons']
report = {'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'baseline_commit': BASE, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'method': 'isolated real HTTP browser QA; fonts use the same fallback for before/after comparisons', 'checks': [], 'layouts': [], 'pages': [], 'errors': [], 'network_posts': [], 'production_deployed': False}

def check(name, result, detail=None):
    report['checks'].append({'name': name, 'passed': bool(result), 'detail': detail})

def build():
    before = OUT / 'baseline-source'
    before.mkdir(exist_ok=True)
    for p in SRC.iterdir():
        if p.suffix not in {'.py', '.js', '.css', '.svg'}:
            continue
        rel = str(p.relative_to(ROOT))
        raw = subprocess.check_output(['git', 'show', BASE + ':' + rel], cwd=ROOT)
        (before / p.name).write_bytes(raw)
        if p.suffix in {'.css', '.js', '.svg'}:
            check('design_asset_unchanged:' + p.name, raw == p.read_bytes())
    for source, target in [(before, OUT / 'before'), (SRC, OUT / 'after')]:
        subprocess.run([sys.executable, str(source / 'build_refined_site.py'), '--out', str(target)], check=True)
    for locale in ['zh', 'en']:
        for name in ROUTES:
            path = OUT / 'after' / locale / (name + '.html')
            soup = BeautifulSoup(path.read_text(), 'html.parser')
            report['pages'].append({'locale': locale, 'page': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            check('title_lang_h1:' + locale + '/' + name, bool(soup.title and soup.select_one('h1')) and soup.html.get('lang') == ('zh-CN' if locale == 'zh' else 'en'))
            for tag in soup.select('[href],[src]'):
                href = tag.get('href') or tag.get('src')
                if not href or re.match(r'^(https?:|mailto:|data:|tel:)', href):
                    continue
                split = urlsplit(href)
                dest = (path.parent / unquote(split.path)).resolve() if split.path else path
                okay = dest.exists()
                if okay and split.fragment and dest.suffix == '.html':
                    okay = bool(BeautifulSoup(dest.read_text(), 'html.parser').find(id=unquote(split.fragment)))
                check('local_reference:' + locale + '/' + name, okay, href)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

def browser_review():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(OUT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = 'http://127.0.0.1:' + str(server.server_port)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        context.route('https://fonts.googleapis.com/**', lambda route: route.fulfill(status=200, content_type='text/css', body=''))
        context.on('request', lambda req: report['network_posts'].append(req.url) if req.method == 'POST' else None)
        page = context.new_page()
        page.on('pageerror', lambda error: report['errors'].append(str(error)))
        def load(locale, route, query='', version='after'):
            response = page.goto(origin + '/' + version + '/' + locale + '/' + route + '.html' + query, wait_until='networkidle')
            check('HTTP200:' + version + '/' + locale + '/' + route, response.status == 200)
        for locale in ['zh', 'en']:
            for width in [320, 390, 768, 1024, 1280, 1440, 1920]:
                page.set_viewport_size({'width': width, 'height': 1000})
                for route in ROUTES:
                    load(locale, route)
                    bounds = page.evaluate('({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth})')
                    okay = bounds['scroll'] <= bounds['client'] + 1
                    report['layouts'].append({'locale': locale, 'route': route, 'width': width, 'passed': okay})
                    check('no_overflow:' + locale + '/' + route + '/' + str(width), okay, bounds)
                    check('no_internal_release_copy:' + locale + '/' + route, not any(x in page.locator('body').inner_text() for x in ['Implementation preview', 'not a production cutover', '预览实现', '尚未切换正式域名', '旧职业材料', 'written to CRM']))
                    if width in [390, 1440]:
                        page.screenshot(path=str(OUT / (locale + '_' + route + '_' + str(width) + '.png')), full_page=True)
            page.set_viewport_size({'width': 1440, 'height': 1000})
            for version in ['before', 'after']:
                load(locale, 'index', version=version)
                page.screenshot(path=str(OUT / (version + '_' + locale + '_home.png')))
                geometry = page.locator('.hero-headline').evaluate('(e)=>({size:getComputedStyle(e).fontSize,weight:getComputedStyle(e).fontWeight,box:e.getBoundingClientRect().toJSON()})')
                report.setdefault('hero_geometry', {})[version + '_' + locale] = geometry
                load(locale, 'about', version=version)
                page.screenshot(path=str(OUT / (version + '_' + locale + '_about.png')), full_page=True)
            before = report['hero_geometry']['before_' + locale]
            after = report['hero_geometry']['after_' + locale]
            check('hero_type_and_position_preserved:' + locale, before == after, {'before': before, 'after': after})
            for route in ['index', 'decision-os', 'buttons']:
                load(locale, route)
                for group in page.locator('[role=tablist]').all():
                    for tab in group.locator('[role=tab]').all():
                        tab.click()
                        check('tab_panel:' + locale + '/' + route, page.locator('#' + tab.get_attribute('aria-controls')).is_visible())
                    first = group.locator('[role=tab]').first
                    first.focus(); first.press('End')
                    check('tab_keyboard:' + locale + '/' + route, group.locator('[role=tab]').last.get_attribute('aria-selected') == 'true')
            for route in ['expertise', 'lab']:
                load(locale, route)
                for button in page.locator('[data-filter]').all():
                    key = button.get_attribute('data-filter'); button.click()
                    visible = page.locator('[data-type]:visible').all()
                    check('filter:' + locale + '/' + route + '/' + key, all(key == 'all' or key == item.get_attribute('data-type') for item in visible))
                page.locator('[data-filter="all"]').click()
                if route == 'expertise':
                    check('all16_services:' + locale, page.locator('#services>.card').count() == 16)
                    page.locator('[data-search]').fill('ZZZZZZZZ')
                    check('search_empty:' + locale, page.locator('[data-empty]').is_visible())
                    page.locator('[data-search]').fill('')
                    for detail in page.locator('details').all():
                        detail.locator('summary').click()
                        check('scope_expander:' + locale, detail.get_attribute('open') is not None)
                        detail.locator('summary').click()
            for number in range(1, 17):
                service = 'S' + str(number).zfill(2)
                load(locale, 'contact', '?service=' + service)
                check('service_referral:' + locale + '/' + service, service in page.locator('#message').input_value() and page.locator('#track').input_value() == 'principal')
            for track in ['principal', 'intelligence', 'ventures', 'products', 'media']:
                load(locale, 'contact', '?track=' + track)
                check('track_referral:' + locale + '/' + track, page.locator('#track').input_value() == track)
            load(locale, 'contact')
            page.locator('button[type=submit]').click()
            check('empty_form_no_success:' + locale, page.locator('#draft-result').is_hidden())
            for key, value in {'name': 'QA Visitor', 'email': 'invalid', 'company': 'Example Studio', 'message': 'A concrete product operating question.'}.items():
                page.locator('#' + key).fill(value)
            page.locator('[name=consent]').check(); page.locator('button[type=submit]').click()
            check('invalid_email_no_success:' + locale, page.locator('#draft-result').is_hidden())
            page.locator('#email').fill('qa@example.com'); page.locator('button[type=submit]').click()
            check('valid_local_draft:' + locale, page.locator('#draft-result').is_visible() and page.locator('#open-email').get_attribute('href').startswith('mailto:minyajing@gmail.com'))
            page.locator('button[type=submit]').click()
            check('repeated_submission_stays_draft:' + locale, page.locator('#draft-result').is_visible())
            page.set_viewport_size({'width': 390, 'height': 900}); load(locale, 'index')
            page.locator('[data-menu]').click(); check('mobile_navigation:' + locale, page.locator('[data-nav]').is_visible())
            page.keyboard.press('Escape'); check('mobile_escape_focus:' + locale, page.locator('[data-menu]').get_attribute('aria-expanded') == 'false' and page.locator('[data-menu]').evaluate('(e)=>e===document.activeElement'))
        check('no_automatic_business_POST', not report['network_posts'])
        check('no_browser_JS_errors', not report['errors'])
        browser.close()
    server.shutdown()

try:
    build()
    browser_review()
except Exception:
    report['errors'].append(traceback.format_exc())
finally:
    report['summary'] = {'pages': len(report['pages']), 'layout_cases': len(report['layouts']), 'checks': len(report['checks']), 'failed': sum(not x['passed'] for x in report['checks']), 'exceptions': len(report['errors'])}
    report['all_passed'] = not report['summary']['failed'] and not report['errors']
    (OUT / 'review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report['summary']))
    if not report['all_passed']:
        print(json.dumps([x for x in report['checks'] if not x['passed']][:20], ensure_ascii=False))
        print('\n'.join(report['errors']))
sys.exit(0 if report['all_passed'] else 1)
