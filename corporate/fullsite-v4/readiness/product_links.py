"""Keep the company catalog linked to each product's public destination."""

from html import escape
from pathlib import Path


PRODUCTS = (
    ("dreamplot", "DreamPlot", "https://dreamplot.saga1001.com/book", "consumer",
     "梦频日记与中文电子书预售", "Dream diary and Chinese ebook preorder"),
    ("breath", "Chromatic Breathing", "https://apps.apple.com/us/app/chromatic-breathing/id6742974213", "consumer",
     "呼吸与色彩体验 · App Store", "Breathing and color experience · App Store"),
    ("dharma", "Dharma", "https://dharma.saga1001.com/", "knowledge",
     "佛学与内在探索", "Buddhist learning and inner exploration"),
    ("bible", "Bible", "https://bible.saga1001.com/", "knowledge",
     "圣经与信仰探索", "Bible and faith exploration"),
    ("healing", "Healing", "https://healing.saga1001.com/", "knowledge",
     "疗愈与自我关怀", "Healing and self care"),
    ("quri", "QuriAtlas", "https://quriatlas.saga1001.com/", "knowledge",
     "科学与知识地图", "Science and knowledge atlas"),
)


def _card(product, locale):
    key, name, url, kind, zh, en = product
    description = zh if locale == "zh" else en
    label = "访问产品" if locale == "zh" else "Visit product"
    status = "产品入口" if locale == "zh" else "Product site"
    return (f'<article class="card product-card" data-type="{kind}">'
            f'<div class="product-visual"><img src="../assets/product-previews/{key}-site-20261014.jpg" '
            f'alt="{escape(name)} {escape(description)}" loading="lazy"></div>'
            f'<span class="status">{status}</span><h3>{escape(name)}</h3>'
            f'<p>{escape(description)}</p><a class="ggc-btn" href="{escape(url)}" '
            f'target="_blank" rel="noopener noreferrer"><span class="btn-label">{label}</span>'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
            '</a></article>')


def _first_project_link(html, url):
    needle = 'href="contact.html?track=products" data-product-source'
    if needle not in html:
        needle = 'href="lab.html" data-product-source'
    if html.count(needle) != 1:
        raise ValueError("Expected exactly one product entry CTA")
    return html.replace(needle, f'href="{url}" target="_blank" rel="noopener noreferrer" data-product-source', 1)


def align_product_links(site: Path):
    for locale in ("zh", "en"):
        folder = site / locale
        lab = folder / "lab.html"
        html = lab.read_text(encoding="utf-8")
        marker = '</div><p class="empty" data-empty hidden>'
        if html.count(marker) != 1:
            raise ValueError("Product grid insertion point changed")
        html = html.replace(marker, ''.join(_card(p, locale) for p in PRODUCTS) + marker, 1)
        lab.write_text(html, encoding="utf-8")
        for number, url in ((11, "https://plot.saga1001.com/"),
                            (12, "https://opsgo.ggcgames.com/"),
                            (13, "https://dharma.saga1001.com/")):
            page = folder / f"product-{number:02d}.html"
            detail = _first_project_link(page.read_text(encoding="utf-8"), url)
            if number == 13:
                target = '</div></div><div class="hero-visual">'
                more = ('<p class="product-related-links">'
                        '<a href="https://healing.saga1001.com/">Healing ↗</a> · '
                        '<a href="https://quriatlas.saga1001.com/">QuriAtlas ↗</a> · '
                        '<a href="https://bible.saga1001.com/">Bible ↗</a>'
                        '</p>')
                if detail.count(target) != 1:
                    raise ValueError("Expected one grouped product hero")
                detail = detail.replace(target, '</div>' + more + '</div><div class="hero-visual">', 1)
            page.write_text(detail, encoding="utf-8")
