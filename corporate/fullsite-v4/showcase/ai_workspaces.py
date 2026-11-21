"""Add public product entries using each product's own branding and UI capture.

This post-processing step preserves the hash-protected fullsite templates.
"""
from html import escape
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
PRODUCT_GRID = '<div class="grid g3" id="products">'
PRODUCTS = (
    {
        'id': 'agent-office',
        'url': 'https://ai.ggcgames.com/',
        'brand': 'agent-office-brand.webp',
        'brand_alt': 'JOYCE × GGC · AGENT OFFICE / V0.1',
        'screen': 'agent-office-screen.webp',
        'zh': {
            'title': '七人办公室',
            'type': '可交互的流程模拟',
            'body': '给七个角色分派任务，观察交接、阻塞、复盘与组织演化。支持手工干预和本地存档。',
            'scope': '浏览器本地模拟；不执行真实 AI 任务或对外操作。',
            'alt': '七人办公室实际界面：办公室角色、项目看板与手工任务控制台',
            'cta': '进入七人办公室',
        },
        'en': {
            'title': 'Seven Agent Office',
            'type': 'Interactive workflow simulation',
            'body': 'Assign tasks to seven roles and explore handoffs, blockers, reviews and organizational evolution. Includes manual controls and local saves.',
            'scope': 'A browser-local simulation; it does not execute real AI tasks or external actions.',
            'alt': 'Actual Seven Agent Office interface showing the office, project board and manual task controls',
            'cta': 'Open the agent office',
        },
    },
    {
        'id': 'cat-workspace',
        'url': 'https://agency.ggcgames.com/',
        'brand': 'cat-workspace-brand.webp',
        'brand_alt': 'GGC WORKSPACE · 小猫工作室',
        'screen': 'cat-workspace-screen.webp',
        'zh': {
            'title': '小猫工作室',
            'type': '公开脱敏的工作状态',
            'body': '在 GGC 工作室与 SAGA1001 庭院里，查看六位猫同事对应的 GPT / Codex 工作状态和记录。',
            'scope': '只展示脱敏状态；角色动作不代表任务完成或交付。',
            'alt': '小猫工作室实际界面：相连的工作室和庭院、六位猫同事与状态档案',
            'cta': '看看工作现场',
        },
        'en': {
            'title': 'GGC Cat Workspace',
            'type': 'Public, sanitized work status',
            'body': 'Explore the GGC studio and SAGA1001 garden, where six cat colleagues represent GPT / Codex work statuses and records.',
            'scope': 'Sanitized status only; character movement does not mean a task is complete or delivered.',
            'alt': 'Actual Cat Workspace interface showing the connected studio and garden, six cats and status details',
            'cta': 'Visit the workspace',
        },
    },
)


def card(product, locale):
    copy = product[locale]
    caption = '实际产品界面' if locale == 'zh' else 'Actual product interface'
    access = '公开体验 · 无需登录' if locale == 'zh' else 'Public access · No login required'
    new_tab = '在新标签页打开' if locale == 'zh' else 'Opens in a new tab'
    asset = '../assets/ai-workspaces/'
    return f'''<article class="card product-card ai-workspace-card {product['id']}" data-type="software" aria-labelledby="{product['id']}-title">
<a class="ai-workspace-visual" href="{product['url']}" target="_blank" rel="noopener noreferrer" aria-label="{escape(copy['cta'] + ' · ' + new_tab)}"><img src="{asset + product['screen']}" alt="{escape(copy['alt'])}" loading="lazy" decoding="async" width="1280" height="900"><span>{caption}</span></a>
<div class="ai-workspace-copy"><img class="ai-workspace-brand" src="{asset + product['brand']}" alt="{escape(product['brand_alt'])}" loading="lazy" decoding="async"><span class="status">{copy['type']}</span><h3 id="{product['id']}-title">{copy['title']}</h3><p>{copy['body']}</p><p class="ai-workspace-scope">{copy['scope']}</p><div class="ai-workspace-actions"><a class="ggc-btn" data-button-id="10" href="{product['url']}" target="_blank" rel="noopener noreferrer" aria-describedby="{product['id']}-access {product['id']}-new-tab"><span class="btn-label">{copy['cta']}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg></a><small id="{product['id']}-access">{access}</small><span class="ai-workspace-sr-only" id="{product['id']}-new-tab">{new_tab}</span></div></div>
</article>'''


def add_ai_workspaces(site):
    site = Path(site)
    for locale in ('zh', 'en'):
        page = site / locale / 'lab.html'
        html = page.read_text(encoding='utf-8')
        if html.count(PRODUCT_GRID) != 1 or 'id="agent-office-title"' in html:
            raise ValueError(f'Expected one unmodified AI product directory: {page}')
        utility_end = '</div></div><p class="sr-only" aria-live="polite" data-result-count>'
        if html.count(utility_end) != 1 or 'data-search' in html:
            raise ValueError(f'Expected one product filter toolbar without search: {page}')
        search_label = '搜索产品' if locale == 'zh' else 'Search products'
        search = f'<label><span class="sr-only">{search_label}</span><input class="search" data-search type="search" placeholder="{search_label}"></label>'
        html = html.replace(utility_end, '</div>' + search + '</div><p class="sr-only" aria-live="polite" data-result-count>', 1)
        cards = ''.join(card(product, locale) for product in PRODUCTS)
        html = html.replace(PRODUCT_GRID, PRODUCT_GRID + cards, 1)
        html = html.replace('</head>', '<link rel="stylesheet" href="../assets/ai-workspaces.css"></head>', 1)
        page.write_text(html, encoding='utf-8')
    shutil.copyfile(HERE / 'ai_workspaces.css', site / 'assets' / 'ai-workspaces.css')
    shutil.copytree(HERE / 'assets' / 'ai-workspaces', site / 'assets' / 'ai-workspaces', dirs_exist_ok=True)
