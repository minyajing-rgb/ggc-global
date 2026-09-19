"""Verify deployed coastal site, not just a local preview. No email is sent."""
from pathlib import Path
import csv, datetime, hashlib, json, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'coastal-live-evidence'
OUT.mkdir(exist_ok=True)
BASE = 'https://biz.ggcgames.com'
VERSION = '2026-09-19-coastal-v3'
checks = {}
http_results = {}
errors = []
stamp = str(int(time.time()))
manifest = json.loads((ROOT/'joyce/content/coastal-v3-manifest.json').read_text())
paths = ['/', '/joyce/', '/joyce/rate-card.csv', '/joyce/assets/coastal-v3.css', '/joyce/assets/coastal-v3.js']
paths += ['/joyce/assets/' + name for name in manifest['assets']]
try:
    for path in paths:
        info = {'url': BASE + path, 'ok': False}
        for attempt in range(4):
            try:
                request = urllib.request.Request(BASE + path + '?release=' + stamp,
                    headers={'User-Agent': 'GGC-Release-Verification/3', 'Cache-Control': 'no-cache'})
                with urllib.request.urlopen(request, timeout=25) as response:
                    data = response.read()
                    info.update(status=response.status, bytes=len(data), final_url=response.url)
                local = ROOT / ('index.html' if path=='/' else 'joyce/index.html' if path=='/joyce/' else path.lstrip('/'))
                expected = hashlib.sha256(local.read_bytes()).hexdigest()
                actual = hashlib.sha256(data).hexdigest()
                info.update(sha256=actual, expected_sha256=expected, ok=info['status']==200 and actual==expected)
                if info['ok']:
                    break
            except Exception as exc:
                info['error'] = str(exc)
            if attempt < 3:
                time.sleep(8)
        http_results[path] = info
    checks['live_files_match_committed_release'] = all(item['ok'] for item in http_results.values())
    if not checks['live_files_match_committed_release']:
        raise RuntimeError('Some live files do not match the committed coastal release')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width':1440,'height':1000}, reduced_motion='reduce')
        page = context.new_page()
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto(BASE + '/joyce/?release=' + stamp, wait_until='networkidle', timeout=60000)
        page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
        page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)', timeout=20000)
        checks['live_release_marker'] = page.evaluate('window.__ggcRelease') == VERSION
        checks['service_count_16'] = page.locator('.service-card').count() == 16
        checks['capability_count_14'] = page.locator('.capability').count() == 14
        checks['scenario_count_12'] = page.locator('.scenario-grid article').count() == 12
        checks['desktop_no_overflow'] = page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        checks['no_pdf_links'] = page.locator('a[href$=".pdf"]').count() == 0
        checks['no_private_names'] = all(word not in page.inner_text('body').lower() for word in ['jordan','ryan','counterparty','reincarnation'])
        checks['images_loaded'] = page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        page.screenshot(path=str(OUT/'live-desktop.png'))
        page.screenshot(path=str(OUT/'live-desktop-full.png'), full_page=True)
        checks['prices_match_csv'] = all(int(row['CNY_base']) == int(page.locator('[data-price="'+row['ID']+'"]').inner_text().replace('CNY ','').replace(',','')) for row in csv.DictReader((ROOT/'joyce/rate-card.csv').open()) if row['ID'].startswith('S'))
        page.locator('[data-currency="usd"]').click()
        checks['usd_reference'] = '16,667' in page.locator('[data-price="S14"]').inner_text()
        page.locator('[data-filter="ai"]').click()
        checks['ai_filter'] = page.locator('.service-card:visible').count() == 2
        page.locator('[data-detail="S14"]').first.click()
        checks['service_details'] = page.locator('#service-dialog').is_visible()
        page.locator('#dialog-enquire').click()
        checks['service_selected'] = page.locator('#service-select').input_value() == 'S14'
        page.locator('[data-lang="zh"]').click()
        checks['language_switch'] = page.locator('html').get_attribute('lang') == 'zh' and 'AI工作流试点' in page.locator('[data-service-name="S14"]').inner_text()
        page.locator('[data-lang="en"]').click()
        page.locator('[data-filter="all"]').click()
        page.locator('[data-currency="cny"]').click()
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('scrollTo(0,0)')
        checks['mobile_no_overflow'] = page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(OUT/'live-mobile.png'), full_page=True)
        page.locator('.menu').click()
        checks['mobile_menu'] = page.locator('#navigation').is_visible()
        page.locator('#navigation a[href="#services"]').click()
        checks['mobile_navigation'] = not page.locator('#navigation').is_visible()
        page.goto(BASE+'/?release='+stamp, wait_until='networkidle', timeout=60000)
        checks['root_live_release'] = page.evaluate('window.__ggcRelease') == VERSION
        checks['no_js_errors'] = not errors
        browser.close()
except Exception as exc:
    errors.append(str(exc))
    checks['verification_finished'] = False
report = {'version':VERSION, 'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'base_url':BASE, 'checks':checks, 'http':http_results, 'errors':errors,
          'all_passed':bool(checks) and all(checks.values()) and not errors,
          'note':'Actual public-domain HTTP byte checks and desktop/mobile browser interaction. No email, booking or payment executed. No PDF produced.'}
(OUT/'live-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['all_passed']:
    raise SystemExit('Live coastal verification failed')
