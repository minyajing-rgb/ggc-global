#!/usr/bin/env python3
"""Refine the existing GGC implementation; source-of-truth content is not duplicated.
Use this entry point for the visual-fidelity pass. No dependencies, font binaries,
production changes, form submission or analytics are introduced.
"""
from pathlib import Path
from html import escape
import argparse, importlib.util, json, shutil, hashlib

SRC=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ggc_core',SRC/'build_site.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base_home=base.home
base_document=base.document


def refined_memo(prefix='hero'):
    x=base.x
    tabs=[];panels=[]
    for i,s in enumerate(base.SCENARIOS):
        tid=f'{prefix}-tab-{i}';pid=f'{prefix}-panel-{i}'
        tabs.append(base.btn(x(s[0],s[1]),style='08',extra=f'id="{tid}" role="tab" aria-controls="{pid}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}"',arrow=False))
        lines=''.join(f'<div class="memo-line"><i>0{j+1}</i><div><b>{x(r[0],r[1])}</b><p>{x(r[2],r[3])}</p></div></div>' for j,r in enumerate(s[4]))
        panels.append(f'<div id="{pid}" role="tabpanel" aria-labelledby="{tid}" tabindex="0"'+(' hidden' if i else '')+f'><h3 class="memo-question">{x(s[2],s[3])}</h3>{lines}</div>')
    signals=[('市场变化','Market shifts'),('玩家需求','Player needs'),('竞争动态','Competitive moves'),('技术与平台','Technology / platforms')]
    signal_rows=''.join(f'<li><span class="source-dot"></span><span>{x(z,e)}</span></li>' for z,e in signals)
    signal=f'''<aside class="signal-sheet" aria-label="{x('信号来源示意，不是实时数据','Illustrative source categories, not live data')}"><p class="sheet-cap">MARKET SIGNALS</p><h3>{x('从信号开始','Start with evidence')}</h3><div class="signal-lines" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div><ul>{signal_rows}</ul><small>{x('研究 · 交流 · 公开证据','Research · Dialogue · Evidence')}</small></aside>'''
    fit=f'''<aside class="fit-sheet" aria-label="{x('战略适配维度示意','Illustrative strategic fit dimensions')}"><p class="sheet-cap">STRATEGIC FIT</p><h3>{x('放进你的公司条件','Fit your company')}</h3><div class="fit-map"><span class="fit-ring"></span><span class="fit-ring inner"></span><span class="fit-core">GGC<small>CLARITY</small></span><span class="fit-node a">{x('产品','PRODUCT')}</span><span class="fit-node b">{x('团队','PEOPLE')}</span><span class="fit-node c">{x('商业模式','BUSINESS')}</span><span class="fit-node d">{x('能力与资源','CAPABILITY')}</span></div><small>{x('不是漂亮赛道，是合适路径。','Not just an attractive market. The right path.')}</small></aside>'''
    front=f'''<article class="memo"><div class="memo-top"><img src="../assets/ggc-logo.svg" alt="GGC" width="70" height="27"><span>STRATEGIC MEMO</span><span>{x('示例','SAMPLE')}</span></div><p class="memo-overline">FROM SIGNAL TO NEXT MOVE</p><h2 class="memo-title">{x('看清问题。<br>找到下一步。','See the constraint.<br>Find the next move.')}</h2><div class="ggc-tabs" role="tablist" aria-label="{x('诊断示例','Sample diagnostics')}">{''.join(tabs)}</div>{''.join(panels)}<footer>{x('战略决策示例','Strategic decision examples')}</footer></article>'''
    return f'<div class="memo-stage fidelity-memo">{signal}{fit}{front}</div>'


def refined_home():
    x=base.x
    html=base_home()
    # The accepted message is retained; typography and bilingual brand line are refined.
    h1=f'<h1 class="hero-headline"><span class="headline-line">{x("看清下一程。","See what’s next.")}</span><span class="inkgrad headline-line">{x("做对关键决策。","Know your next move.")}</span></h1>'
    start=html.index('<h1>');end=html.index('</h1>',start)+5
    html=html[:start]+h1+f'<p class="hero-translation" lang="{base.OTHER}">{x("See what’s next. Know your next move.","看清下一程，做对关键决策。")}</p>'+html[end:]
    html=html.replace('<div class="shell hero-grid"><div>','<div class="shell hero-grid"><div class="hero-copy">',1)
    # Better visual cadence below the hero: question + pillar groups share the compact editorial grid.
    html=html.replace('<section class="section white"><div class="shell"><div class="section-head"><div><p class="eyebrow">THE DECISIONS THAT MATTER', '<section class="section white section-questions"><div class="shell"><div class="section-head"><div><p class="eyebrow">THE DECISIONS THAT MATTER',1)
    html=html.replace('<section class="section alt"><div class="shell"><div class="section-head"><div><p class="eyebrow">OUR BUSINESS PILLARS','<section class="section alt section-pillars"><div class="shell"><div class="section-head"><div><p class="eyebrow">OUR BUSINESS PILLARS',1)
    if base.LANG == 'zh':
        html=html.replace('先找到真正的问题。','先找到<br>真正的问题。',1).replace('四大业务，一套经营能力。','四大业务。<br>一套经营能力。',1)
    return html


def refined_document(key,body):
    html=base_document(key,body)
    html=html.replace('<link rel="stylesheet" href="../assets/site.css">','<link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/fidelity.css">')
    html=html.replace('<body>','<body class="fidelity-v2 page-'+key+'">',1)
    html=html.replace('width="109" height="40"','width="146" height="54"')
    # Keep the development-state disclosure readable, but out of the company masthead.
    start=html.index('<div class="review-note">');end=html.index('<main id="main">',start)
    html=html[:start]+html[end:]
    html=html.replace('<small>© 2026 GGC · Global Game Copilot</small>','<small>© 2026 GGC · Global Game Copilot</small>')
    html=html.replace('GGC implementation preview · approved buttons 01 / 04 / 06 / 08 / 09 / 10','GGC implementation preview')
    return html


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=SRC.parent/'site');args=parser.parse_args();out=args.out.resolve()
    if out in [SRC,Path('/'),Path.home(),Path('/app')]:raise SystemExit('Refusing unsafe output root')
    assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
    for name in ['buttons.css','site.css','app.js','fidelity.css']:shutil.copyfile(SRC/name,assets/name)
    shutil.copyfile(SRC/'ggc-logo-refined.svg',assets/'ggc-logo.svg')
    # Load real requested weights on devices without local design fonts.
    # Only the external CSS reference is emitted; no font binaries are distributed.
    font_url='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+SC:wght@400;500;600;700;800;900&display=swap'
    style=assets/'fidelity.css'
    css=style.read_text(encoding='utf-8').replace("'Noto Sans CJK SC'","'Noto Sans SC','Noto Sans CJK SC'")
    style.write_text('@import url("'+font_url+'");\n'+css,encoding='utf-8')
    base.memo=refined_memo
    base.RENDER['index']=refined_home
    for locale in ['zh','en']:
        base.LANG=locale;base.OTHER='en' if locale=='zh' else 'zh'
        directory=out/locale;directory.mkdir(parents=True,exist_ok=True)
        for key,render in base.RENDER.items():
            (directory/(key+'.html')).write_text(refined_document(key,render()),encoding='utf-8')
    (out/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=zh/index.html"><title>GGC</title></head><body><a href="zh/index.html">中文</a> · <a href="en/index.html">English</a></body></html>',encoding='utf-8')
    names=['build_site.py','build_refined_site.py','buttons.css','site.css','app.js','fidelity.css','ggc-logo-refined.svg']
    manifest={'version':'2026-10-12-visual-fidelity-v2','approvedButtons':[1,4,6,8,9,10],'pagesPerLocale':len(base.RENDER),'locales':['zh','en'],'production':False,'backend':'local mail draft only','sourceSHA256':{n:hashlib.sha256((SRC/n).read_bytes()).hexdigest() for n in names}}
    (out/'build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'pages':len(base.RENDER)*2,'version':manifest['version']}))
if __name__=='__main__':main()
