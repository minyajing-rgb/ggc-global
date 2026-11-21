"""Emit factual, source-linked discovery text for *released* GGC pages only.

This is supplementary documentation for human and machine readers.
It is not a search-ranking signal, AI crawler directive or proof of conversion.
No release is performed here; canonical host is inherited from the reviewed build.
"""
from pathlib import Path
import json
from html import escape


PUBLIC_REFERENCES = (
    ('zh/index.html', '中文首页', 'GGC 全球游戏、AI 产品与经营决策介绍。'),
    ('en/index.html', 'English home', 'GGC global games, AI products and business decision-making.'),
    ('zh/expertise.html', '专业能力', '服务、能力和经营方法的公开范围。'),
    ('en/expertise.html', 'Expertise', 'Public scope of operating and strategic advisory.'),
    ('zh/products.html', '产品与实践', '自有项目、研发方向及实际公开状态。'),
    ('en/products.html', 'Lab work', 'Owned products and current publicly described status.'),
    ('zh/book.html', '作者与著作', 'GGC 创始人的已出版著作与公开资料。'),
    ('en/book.html', 'Book and author', 'Published book and public author information.'),
    ('zh/contact.html', '中文合作联系', 'GGC 商务咨询与联系入口。'),
    ('en/contact.html', 'English contact', 'Enquiries and partnership contact information.'),
)


def emit_public_facts(site: Path, mode: str) -> int:
    """Write reviewed-origin text assets; return number of verified public URLs."""
    if mode != 'release':
        return 0
    report = json.loads((site / 'readiness-manifest.json').read_text(encoding='utf-8'))
    base = report['canonical_base']
    approved = {item['canonical'] for item in report['inventory'] if item['indexable']}
    home_zh = base + 'zh/index.html'
    home_en = base + 'en/index.html'
    if home_zh not in approved or home_en not in approved:
        raise ValueError('GGC discovery facts require two indexable language homepages.')
    links = [(base + route, label, desc) for route, label, desc in PUBLIC_REFERENCES if base + route in approved]
    lines = [
        '# GGC — Global Game Copilot',
        '',
        '> Global game operations, commercialization, publishing and AI product advisory.',
        '',
        '## Official identity',
        'Name: GGC — Global Game Copilot',
        'Founder: Joyce Mi',
        'Focus: game portfolio decisions, commercial strategy, LiveOps, worldwide publishing, AI workflows and co-build partnerships.',
        'Official bilingual site: ' + base,
        'Source status: only published, indexable pages in this release are listed below.',
        '',
        '## Public sources',
    ]
    lines.extend(f'- [{label}]({url}) — {desc}' for url, label, desc in links)
    lines += [
        '',
        '## Verification limits',
        '- Client project numbers, campaign returns, awards, endorsements, sales, testimonials and case-study outcomes are not verified by this file.',
        '- Service pricing, deliverables and availability must be checked on the current public service page or in a signed agreement.',
        '- Product concepts are not representations of fully shipped or paid software unless a linked page explicitly documents that state.',
        '- Private research, client data, contact records, partner pipelines, passwords and internal dashboards are not public discovery sources.',
        '- This text is supplementary; inclusion in search engines or AI responses is not guaranteed.',
        '',
        'Last reviewed: 2026-10-20.',
        '',
    ]
    body = '\n'.join(lines)
    for filename in ('llms.txt', 'ai-discovery.txt'):
        (site / filename).write_text(body, encoding='utf-8')
    # Link the source material from public homepage HEADs only; preserve approved body
    # hashes, visible CTA flows, preview indexability, and the two-link root router.
    for route in ('zh/index.html', 'en/index.html'):
        p = site / route
        html = p.read_text(encoding='utf-8')
        if '</head>' not in html or 'rel="canonical"' not in html:
            raise ValueError(f'Missing reviewed metadata in {route}')
        ref = ('<link rel="alternate" type="text/plain" title="GGC official public facts" '
               f'href="{escape(base, quote=True)}ai-discovery.txt">')
        if ref not in html:
            p.write_text(html.replace('</head>', ref + '\n</head>', 1), encoding='utf-8')
    return len(links)
