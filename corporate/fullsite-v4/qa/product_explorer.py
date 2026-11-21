"""Acceptance for the current static product explorer, shared by all three reviews.

The builder's gallery() now renders product artwork and three visible facts.
Do not restore the retired carousel merely to satisfy its old test selectors.
"""
def check_product_explorer(page, check, label):
    story = page.locator('.product-story')
    check('product_explorer_structure:'+label, story.count() == 1)
    if story.count() != 1:
        return  # The structural failure is recorded; continue the other routes.
    check('product_explorer_visible:'+label, story.is_visible())
    facts = story.locator('.product-story-facts > article')
    check('product_explorer_three_facts:'+label, facts.count() == 3 and
          all(f.is_visible() and f.locator('h3').inner_text().strip() for f in facts.all()))
    check('product_explorer_fact_order:'+label,
          [f.locator('.eyebrow').inner_text().split(' / ')[0] for f in facts.all()] == ['01','02','03'])
    images = story.locator('figure img')
    check('product_explorer_artwork:'+label, images.count() == 1 and images.evaluate_all(
          'es=>es.every(e=>e.complete&&e.naturalWidth>0&&e.getBoundingClientRect().width>0&&e.alt.trim())'))
    caption = story.locator('figcaption')
    # Product 12 uses the actual dated OpsGo brand asset; other products use
    # concept illustrations. Their disclosures must describe the correct source.
    is_brand = images.count() == 1 and 'opsgo-os-2026-09.png' in (images.first.get_attribute('src') or '')
    disclosures = ('品牌物料','brand asset') if is_brand else ('非实际应用截图','not an app screenshot')
    check('product_explorer_disclosure:'+label, caption.count() == 1 and caption.is_visible() and
          any(text in caption.inner_text().lower() for text in disclosures))
    source = page.locator('[data-product-source]')
    check('product_explorer_source_link:'+label, source.count() == 1 and source.is_visible() and
          bool(source.get_attribute('href')) and source.get_attribute('href') != '#')
    if source.count() == 1:
        source.focus()
        check('product_explorer_keyboard_link:'+label, source.evaluate('e=>e===document.activeElement'))
    check('product_explorer_no_dead_controls:'+label,
          page.locator('[data-gallery],[data-next],[data-prev],[data-slide-to]').count() == 0)
