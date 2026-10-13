"""Add the playable Ops Cat showcase without changing approved V4 inputs."""
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
GAME_URL = 'https://mow.ggcgames.com/'
PRODUCT_GRID = '<div class="grid g3" id="products">'

COPY = {
    'zh': {
        'title': '运营猫 · 后院割草',
        'subtitle': '轻松割草 · 发现故事 · 布置小院',
        'body': '和运营猫一起，把一片草地变成喜欢的小院。随玩随停，慢慢收集生活里的小惊喜。',
        'status': 'H5 免费试玩',
        'button': '立即试玩',
        'new_tab': '在新标签页打开',
    },
    'en': {
        'title': 'OPS CAT<br>Mow &amp; Makeover',
        'subtitle': 'Mow a little. Discover stories. Make it yours.',
        'body': 'Turn a patch of grass into your own cozy yard with Ops Cat. Play at your pace and find little surprises along the way.',
        'status': 'Free H5 demo',
        'button': 'Play now',
        'new_tab': 'Opens in a new tab',
    },
}


def banner(locale):
    copy = COPY[locale]
    return f'''<article class="ops-mow-banner" data-type="games" aria-labelledby="ops-mow-title">
<div class="ops-mow-copy"><p class="eyebrow">GGC GAMES / OPS CAT BRIGHT LIFE</p>
<h3 id="ops-mow-title">{copy['title']}</h3>
<p class="ops-mow-subtitle">{copy['subtitle']}</p><p class="ops-mow-description">{copy['body']}</p>
<div class="ops-mow-actions"><a class="ggc-btn" data-button-id="06" href="{GAME_URL}" target="_blank" rel="noopener noreferrer" aria-describedby="ops-mow-new-tab"><span class="btn-label">{copy['button']}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg></a><span class="ops-mow-status">{copy['status']}</span></div>
<span class="ops-mow-sr-only" id="ops-mow-new-tab">{copy['new_tab']}</span></div>
<div class="ops-mow-art" aria-hidden="true"><img class="ops-mow-yard" src="../assets/ops-cat-backyard.png" alt="" loading="lazy" decoding="async" width="1536" height="1024"><img class="ops-mow-cat" src="../assets/ops-cat-mower.png" alt="" loading="lazy" decoding="async" width="1238" height="1271"><span class="ops-mow-art-label">A LITTLE YARD, A BRIGHTER DAY</span></div>
</article>'''


def add_mow_showcase(site):
    """Patch the two product directories; fail if the approved anchor changed."""
    site = Path(site)
    for locale in COPY:
        page = site / locale / 'lab.html'
        html = page.read_text(encoding='utf-8')
        if html.count(PRODUCT_GRID) != 1 or 'id="ops-mow-title"' in html:
            raise ValueError(f'Expected one unmodified product directory: {page}')
        html = html.replace(PRODUCT_GRID, PRODUCT_GRID + banner(locale), 1)
        html = html.replace('</head>', '<link rel="stylesheet" href="../assets/ops-cat-showcase.css"></head>', 1)
        page.write_text(html, encoding='utf-8')
    for source, destination in [('mow_banner.css', 'ops-cat-showcase.css'), ('assets/backyard.png', 'ops-cat-backyard.png'), ('assets/mower-cat.png', 'ops-cat-mower.png')]:
        shutil.copyfile(HERE / source, site / 'assets' / destination)
