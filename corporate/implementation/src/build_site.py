#!/usr/bin/env python3
"""GGC corporate implementation. Pure stdlib; generates independent EN/ZH pages.
Preview only: never writes to a production root, sends mail, or stores submitted data.
"""
from pathlib import Path
from html import escape
import argparse, json, shutil
SRC=Path(__file__).resolve().parent
ROUTES=[('index','首页','Home'),('expertise','专业能力','Expertise'),('research','研究与前瞻','Research'),('decision-os','决策系统','Decision OS'),('lab','产品与实践','Lab Work'),('ventures','联合立项','Ventures'),('about','为什么 GGC','Why GGC'),('contact','联系合作','Contact'),('buttons','按钮组件库','Button Library')]
ARROW='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
ICONS={
 'compass':'<circle cx="12" cy="12" r="9"/><path d="m16 8-2.5 5.5L8 16l2.5-5.5Z"/>',
 'search':'<circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/>',
 'chart':'<path d="M4 20V12h3v8m4 0V7h3v13m4 0V3h3v17"/>',
 'cube':'<path d="m12 2 9 5v10l-9 5-9-5V7Zm-9 5 9 5 9-5M12 12v10"/>',
 'people':'<circle cx="9" cy="8" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M16 5a3 3 0 0 1 0 6m3 10v-4a5 5 0 0 0-2-4"/>',
 'arrow':'<path d="m3 10 18-7-7 18-3-8-8-3Zm8 3L21 3"/>',
 'lab':'<path d="M9 3h6m-5 0v7L4 20h16l-6-10V3M8 14h8"/>',
 'layers':'<path d="m12 3 10 5-10 5L2 8Zm-10 9 10 5 10-5M2 16l10 5 10-5"/>'}
APPROVED=[('01','Blade','轻量光刃','轻量次级行动','Light secondary actions'),('04','Outline','渐变轮廓','清晰次级层级','Clear secondary hierarchy'),('06','Primary Gradient','主渐变','首页与导航主行动','Hero and navigation CTA'),('08','Tab','标签切换','筛选、内容与场景切换','Filters and content selection'),('09','Elevated Luminous','微光强调','页尾重点合作入口','One closing emphasis'),('10','Ghost','轻量幽灵','卡片与安静阅读入口','Quiet in-card actions')]
SERVICES=[
 ('S01','advisory','专家决策咨询','Expert Decision Call','围绕一个明确问题，形成决策讨论与下一步。','One scoped question, a decision discussion and clear next steps.'),
 ('S02','advisory','高管诊断与决策备忘录','Executive Diagnostic & Decision Memo','识别结构性问题，形成可讨论的判断与优先级。','Structural diagnosis, defensible options and prioritized decisions.'),
 ('S03','advisory','产品留存与商业化评审','Product, Retention & Monetization Audit','新手体验、核心循环、经济系统与分群表现。','Onboarding, core loops, virtual economy and cohort performance.'),
 ('S04','advisory','全球发行与市场进入冲刺','Global Publishing & GTM Sprint','市场顺序、定位、渠道、预算与上线条件。','Market sequencing, positioning, channels, budget and launch gates.'),
 ('S05','advisory','买量与素材效能评审','UA & Creative Performance Review','渠道经济性、素材策略和测试学习。','Channel economics, creative strategy and testing.'),
 ('S06','advisory','经济系统与LiveOps蓝图','Economy & LiveOps Blueprint','产消、礼包、玩家分层与活动节奏。','Sources, sinks, offers, player segments and operating cadence.'),
 ('S07','advisory','组织与招聘需求校准','Organization & Hiring Calibration','岗位、职责、人才组合与决策权。','Roles, responsibilities, talent mix and decision rights.'),
 ('S08','advisory','伙伴筛选与引荐准备','Partner Sourcing & Introduction Readiness','伙伴画像、候选研究与经同意的引荐。','Partner criteria, research and permission-based introductions.'),
 ('S09','advisory','商业尽调与投资前产品评审','Commercial Due Diligence','市场假设、数据质量、商业逻辑与风险。','Market assumptions, data quality, commercial logic and risk.'),
 ('S10','partner','战略顾问月包','Strategic Advisory Retainer','持续的高管决策讨论和经营复盘。','Recurring executive decision support and operating reviews.'),
 ('S11','partner','90天经营合作','90-Day Operating Partner','把判断落实到KPI、WBS、产品与经营行动。','Translate decisions into KPI, WBS, product and operating action.'),
 ('S12','partner','全球游戏经营Copilot年框','Annual Global Game Copilot','战略、经营治理、季度复盘与能力沉淀。','Strategy, governance, quarterly reviews and reusable capabilities.'),
 ('S13','ai','高管AI业务工作坊','Executive AI Workshop','围绕团队真实业务，定义AI流程的价值。','Define practical AI workflows around a real business.'),
 ('S14','ai','AI工作流试点','AI Workflow Pilot','单场景试点、评测、审批和SOP交接。','A scoped workflow pilot, evaluation, approval and handoff.'),
 ('S15','advisory','Web3游戏产品与经济评审','Web3 Game Product & Economy Review','玩家路径、钱包摩擦与经济假设。','Player journey, wallet friction and economy assumptions.'),
 ('S16','advisory','游戏经营培训或主题分享','Game Operating Masterclass / Keynote','针对实际受众的实战方法与案例。','Operator methods and cases tailored to the audience.')]
PRODUCTS=[
 ('software','GGC Intelligence','Decision OS','证据 → 对标 → 判断 → 行动的共用决策架构。','A shared architecture connecting evidence, benchmarks, decisions and action.','decision-os.html'),
 ('software','Creative','Creative','创意策略、脚本、素材与测试工作流。','Creative strategy, briefs, production and testing workflows.','https://biz.ggcgames.com/sme/'),
 ('software','Outbound','Outbound','买方情报、企业筛选、触达与跟进。','Buyer intelligence, account qualification and outreach.','https://biz.ggcgames.com/sme/'),
 ('software','Game / App Copilot','Game / App','游戏与APP的留存、经济、运营诊断。原工作名 GGC Growth。','Game and app diagnostics. Existing working name: GGC Growth.','https://biz.ggcgames.com/sme/'),
 ('software','Steam','Steam','商店页、愿望单、Demo与发行准备。','Store pages, wishlists, demos and launch readiness.','https://biz.ggcgames.com/sme/'),
 ('software','Intel','Intel','垂直行业、竞品与商业信号研究。','Vertical-market, competitor and business signal research.','https://biz.ggcgames.com/sme/'),
 ('games','Social Casino / Slot+','Casino+','虚拟经济、内容循环与长线运营研究及共创方向。','Virtual economy, content loops and LiveOps research and co-building.','contact.html?track=ventures'),
 ('games','Simulation / Cozy','Sims','模拟经营、Cozy体验与产品立项。','Simulation, cozy experiences and product greenlights.','contact.html?track=ventures'),
 ('games','Arcade / Hybrid','Arcade','玩法循环、内容效率与商业化验证。','Gameplay loops, content efficiency and commercial validation.','contact.html?track=ventures'),
 ('consumer','Bunny Crystal Oracle','Bunny','原创神谕卡、AI内容体验与数字/实体产品方向。','Original cards, AI consumer experiences and digital/physical products.','https://bunny.saga1001.com/'),
 ('consumer','Plot / Relationship AI','Plot','语音优先的关系洞察与消费AI体验。','Voice-first relationship insights and consumer AI experiments.','contact.html?track=products'),
 ('knowledge','OpsGo','OpsGo','行业研究、专业内容与游戏运营知识。','Industry research, professional content and operating knowledge.','https://opsgo.ggcgames.com/'),
 ('knowledge','Dharma / QuriAtlas / Healing','Atlas','文化、科学与知识体验的项目集合。','A collection of cultural, science and knowledge experiences.','contact.html?track=products'),
 ('consumer','MEMO','MEMO','独立生活方式品牌方向。','An independent lifestyle brand direction.','contact.html?track=products')]
Q=[('chart','哪个赛道值得做？','Where should we compete?'),('compass','适合你的公司吗？','Does it fit your company?'),('search','真正的问题在哪？','What is the real constraint?'),('cube','商业模型成立吗？','Does the business model hold?'),('people','还缺什么能力？','What capability is missing?'),('arrow','下一步怎么执行？','What happens next?')]
SCENARIOS=[
 ('自研自发','Self-publishing','现在该自建海外发行吗？','Build international publishing now?',
 [('表面诉求','Apparent need','尽快扩大海外安装量。','Acquire more players overseas.'),('待验证约束','Constraint to verify','留存与经济性尚未验证；缺少发行负责人。','Unproven cohorts and unit economics; no accountable publishing owner.'),('在这些前提下','Under these premises','先验证产品循环，明确负责人，再小范围测试一个市场。','Validate the product loop, assign an owner, then test one market.')]),
 ('新品类','New category','热门赛道，就是你的机会吗？','Is a hot category right for you?',
 [('说明性前提','Illustrative premise','小团队希望进入内容消耗较重的新赛道。','A lean team is considering a content-heavy category.'),('待验证约束','Constraint to verify','品类机会与团队内容产能可能不匹配。','Category demand may exceed the team’s content capacity.'),('在这些前提下','Under these premises','先测试一个可持续循环；比较自建、合作与暂缓的成本。','Test a sustainable loop; compare building, partnering and deferring.')]),
 ('经营瓶颈','Operating constraint','该加投入，还是先找瓶颈？','More spend — or a clearer diagnosis?',
 [('说明性前提','Illustrative premise','活动增加，但团队没有一致的经营基线。','More events, but the team lacks an agreed operating baseline.'),('待验证约束','Constraint to verify','症状可能来自分群、经济或组织，不只是流量。','The issue may be segments, economy or ownership — not just traffic.'),('在这些前提下','Under these premises','建立基线，识别主要约束，安排有负责人和退出条件的实验。','Set a baseline, isolate the constraint and run an owned, bounded test.')])]

def x(zh,en):return zh if LANG=='zh' else en

def btn(label,href=None,style='01',extra='',arrow=True):
    inner=f'<span class="btn-label">{escape(label)}</span>'+(ARROW if arrow else '')
    if href:return f'<a class="ggc-btn" data-button-id="{style}" href="{escape(href,quote=True)}" {extra}>{inner}</a>'
    return f'<button type="button" class="ggc-btn" data-button-id="{style}" {extra}>{inner}</button>'

def icon(name):return f'<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'

def card(title,copy,index='',action='',attr=''):
    return f'<article class="card" {attr}><span class="index">{index}</span><h3>{escape(title)}</h3><p>{escape(copy)}</p>{action}</article>'

def section(eye,title,body,sub='',kind='',id=''):
    return f'<section class="section {kind}"'+(f' id="{id}"' if id else '')+f'><div class="shell"><div class="section-head"><div><p class="eyebrow">{eye}</p><h2>{title}</h2></div><p>{sub}</p></div>{body}</div></section>'

def pagehero(eye,title,copy):return f'<section class="pagehero"><div class="shell"><p class="eyebrow">{eye}</p><h1>{title}</h1><p>{copy}</p></div></section>'

def memo(prefix='hero'):
    tabs=[];panels=[]
    for i,s in enumerate(SCENARIOS):
        tid=f'{prefix}-tab-{i}';pid=f'{prefix}-panel-{i}';active=i==0
        tabs.append(btn(x(s[0],s[1]),style='08',extra=f'id="{tid}" role="tab" aria-controls="{pid}" aria-selected="{str(active).lower()}" tabindex="{0 if active else -1}"',arrow=False))
        rows=''.join(f'<div class="memo-line"><i>0{j+1}</i><div><b>{x(r[0],r[1])}</b><p>{x(r[2],r[3])}</p></div></div>' for j,r in enumerate(s[4]))
        panels.append(f'<div id="{pid}" role="tabpanel" aria-labelledby="{tid}" tabindex="0"'+(' hidden' if not active else '')+f'><h2>{x(s[2],s[3])}</h2>{rows}</div>')
    return f'<div class="memo-stage"><div class="memo-ghost"></div><div class="memo-ghost two"></div><article class="memo"><div class="memo-top"><strong>GGC</strong><span>DECISION MEMO</span><span>{x("说明性场景","ILLUSTRATIVE")}</span></div><div class="ggc-tabs" role="tablist" aria-label="{x("诊断示例","Sample diagnostics")}">{"".join(tabs)}</div>{"".join(panels)}<footer>{x("示例不是客户结论，也不是实时AI诊断。判断须经客户数据与实际条件验证。","Not a client result or live AI analysis. Decisions require client data and validation.")}</footer></article></div>'

def close():return f'<div class="shell"><section class="closing"><div><h2>{x("聊聊你的下一步。","Let’s discuss your next move.")}</h2><p>{x("更清楚的判断。更好的产品。更大的可能。","Clearer decisions. Better products. Greater possibilities.")}</p></div>{btn(x("讨论一个关键决策","Discuss a strategic decision"),'contact.html','09')}</section></div>'

def home():
    h=f'<section class="hero"><div class="shell hero-grid"><div><p class="eyebrow">STRATEGIC FORESIGHT × DECISION × REAL IMPACT</p><h1>{x("看清下一程。","See what’s next.")}<span class="inkgrad">{x("做对关键决策。","Know your next move.")}</span></h1><p class="intro">{x("GGC 将市场信号、一线行业交流、跨市场研究与头部经营经验，转化为适合你公司的判断、资源配置与行动。","GGC turns market signals, practitioner insight, cross-market research and operating experience into decisions, resources and action that fit your business.")}</p><p class="subline">{x("面向游戏、AI产品与数字业务的战略前瞻和经营决策实验室。","A strategic foresight and decision lab for games, AI products and digital businesses.")}</p><div class="actions">{btn(x("聊聊关键决策","Discuss a strategic decision"),'contact.html','06')}{btn(x("了解我们的方法","Explore our approach"),'decision-os.html','04')}</div><div class="hero-proof"><span>{x("全球视角","Global perspective")}</span><span>{x("头部产品实战","Top-tier operating experience")}</span><span>{x("研究 → 判断 → 行动","Research → Decision → Action")}</span></div></div>{memo()}</div></section>'
    qs=''.join(f'<article class="card question">{icon(q[0])}<h3>{x(q[1],q[2])}</h3>{btn(x("了解","Explore"),'expertise.html','10',arrow=True)}</article>' for q in Q)
    h+=section('THE DECISIONS THAT MATTER',x('先找到真正的问题。','Start with the real question.'),f'<div class="questions">{qs}</div>',x('不是只判断赛道好不好，而是看它是否适合你的公司。','An attractive market is only the start. We assess whether it fits your company.'),'white')
    pillars=[('01','战略咨询与经营诊断','Advisory & Diagnosis','从品类判断到具体经营选择。','From opportunity assessment to operating decisions.','expertise.html','principal'),('02','行业情报与决策系统','Intelligence & Decision OS','让研究、对标与方法成为可复用的能力。','Turn research, benchmarks and methods into reusable capability.','decision-os.html','intelligence'),('03','联合立项与共建','Co-Build & Ventures','连接研发、发行、资源与共同目标。','Connect development, publishing, resources and shared goals.','ventures.html','ventures'),('04','自研产品与实验','Owned Products & Lab Work','把方法做成产品，在实践中继续验证。','Build products from methods and keep validating in practice.','lab.html','products')]
    blocks=''.join(card(x(p[1],p[2]),x(p[3],p[4]),p[0],btn(x('探索详情','Explore'),'{}'.format(p[5]),'01')) for p in pillars)
    h+=section('OUR BUSINESS PILLARS',x('四大业务，一套经营能力。','Four businesses. One operating foundation.'),f'<div class="grid g4">{blocks}</div>',kind='alt')
    proof=f'<div class="evidence"><div><h2>{x("不只看过趋势。<br>也做过关键决定。","More than market observers.<br>Operators, builders and decision-makers.")}</h2><p>{x("从全球头部游戏产品，到研发、发行与公司经营。把行业认知放进实际约束，才形成对你有用的判断。","From globally leading game products to development, publishing and company operations. Insight becomes useful when tested against real constraints.")}</p><div class="actions">{btn(x("为什么是 GGC","Why GGC"),'about.html','04')}</div></div><div><div class="proof"><b>{x("全球头部游戏项目经验","Global flagship product experience")}</b><small>CityVille · FarmVille · Order & Chaos · Minion Rush</small></div><div class="proof"><b>{x("数据、产品、商业化与组织","Data, product, commercialization and organization")}</b><small>{x("过往职业经历：Microsoft、Tencent、Zynga、Gameloft。","Career experience: Microsoft, Tencent, Zynga and Gameloft.")}</small></div><div class="proof"><b>Joyce · {x("GGC 创始人","Founder of GGC")}</b><small>{x("《游戏运营与出海实战》作者 · 经营系统与方法构建者","Published author · Operating system and framework builder")}</small></div></div></div>'
    h+=section('BUILT FROM REAL OPERATING EXPERIENCE','',proof,kind='white')
    briefs=[('CASINO / ARCADE','产品经济与长线运营','Product economics & LiveOps','research.html'),('SIMULATION / COZY','赛道与团队适配','Category and team fit','research.html'),('AI WORKFLOWS','从工具到经营行动','From tooling to operating action','decision-os.html')]
    h+=section('RESEARCH & PRACTICE',x('研究，不停在报告里。','Research that informs a decision.'),'<div class="grid g3">'+''.join(card(x(a,b),x('查看研究方向、方法和资料入口。','Explore research scope, methods and source materials.'),k,btn(x('查看研究','View research'),u,'10')) for k,a,b,u in briefs)+'</div>',x('游戏赛道研究、跨市场实践与经营方法。','Game-category research, cross-market practice and operating methods.'),'alt')
    featured=[('GGC Intelligence',x('Evidence · Benchmark · Decision · Action','Evidence · Benchmark · Decision · Action'),'decision-os.html'),('Bunny',x('AI消费体验与原创卡牌产品方向。','AI consumer experiences and original card products.'),'lab.html'),('OpsGo',x('行业研究、方法和专业内容入口。','Industry research, methods and professional content.'),'https://opsgo.ggcgames.com/')]
    featured_html='<div class="grid g3">'+''.join(card(name,copy,x('产品 / 实践','PRODUCT / PRACTICE'),btn(x('查看产品','Explore product'),url,'01')) for name,copy,url in featured)+'</div>'
    h+=section('FEATURED LAB WORK',x('方法，也成为产品。','Methods become products.'),featured_html,x('产品与研发方向的完整状态见目录。','See the directory for product and R&D status.'))
    return h+close()

def filters(options,target,search=False):
    b=''.join(btn(x(a,c),style='08',extra=f'data-filter="{key}" aria-pressed="{str(i==0).lower()}"',arrow=False) for i,(key,a,c) in enumerate(options))
    inp=f'<label><span class="sr-only">{x("搜索服务","Search services")}</span><input class="search" data-search type="search" placeholder="{x("搜索服务 / 交付","Search services / scope")}"></label>' if search else ''
    return f'<div class="utility"><div class="ggc-tabs" data-filter-group data-target="{target}" role="group" aria-label="{x("筛选","Filters")}">{b}</div>{inp}</div><p class="sr-only" aria-live="polite" data-result-count></p>'

def expertise():
    cards=[]
    for sid,group,zh,en,cz,ce in SERVICES:
        details=f'<details><summary>{x("查看合作范围","Scope & engagement")}</summary><p>{x("交付、时间投入、数据权限、执行责任与第三方费用按具体SOW确认。参考价格以现有官方价目表为准。","Deliverables, time, access, execution responsibilities and third-party fees follow an agreed SOW. Consult the existing official rate card for reference fees.")}</p><a class="source-link" href="https://biz.ggcgames.com/joyce/rate-card.html">{x("官方价目表","Official rate card")} ↗</a></details>'
        cards.append(card(x(zh,en),x(cz,ce),sid,details+btn(x('讨论这项服务','Discuss this service'),'contact.html?service='+sid,'10'),f'data-type="{group}"'))
    return pagehero('EXPERTISE / GGC PRINCIPAL',x('从关键判断，到实际经营。','From a critical decision to real operations.'),x('16项服务，覆盖战略、产品、发行、经营与AI流程。选择适合问题和责任深度的合作方式。','16 scoped engagements across strategy, product, publishing, operations and AI workflows. Start with the decision and agree the right level of ownership.'))+section('SERVICES',x('完整服务目录','Complete service catalogue'),filters([('all','全部','All'),('advisory','诊断与评审','Diagnostics'),('partner','经营合作','Operating'),('ai','AI流程','AI Workflows')],'services',True)+f'<div class="grid g3" id="services">{"".join(cards)}</div><p class="empty" data-empty hidden>{x("没有匹配服务，请清空搜索或选择全部。","No matching services. Clear the search or choose All.")}</p>')+close()

def research():
    topics=[('01','Social Casino / Casino+','经济、付费、LiveOps与用户生命周期。','Economy, monetization, LiveOps and player lifecycle.'),('02','Arcade','核心循环、内容效率与商业化结构。','Core loops, content efficiency and monetization.'),('03','Simulation / Cozy','用户动机、产能、长线内容与品类适配。','Player motivations, production capacity and category fit.'),('04','AI Consumer','内容、记忆、留存与可持续产品价值。','Content, memory, retention and durable user value.'),('05','AI Operating Workflows','情报、创意、商务与多流程协作。','Intelligence, creative, outbound and workflow coordination.')]
    body='<div class="grid g3">'+''.join(card(n,x(z,e),i,btn(x('查看 OpsGo 资料','Explore OpsGo'),'https://opsgo.ggcgames.com/','01')) for i,n,z,e in topics)+'</div><div class="note">'+x('本页是既有研究方向目录。具体结论、数据、日期与证据以原始报告为准；交流观点不等于其所在公司的官方战略。','This is a directory of research themes. Findings, data, dates and evidence belong to the original reports. Practitioner views are not their employer’s official strategy.')+'</div>'
    return pagehero('RESEARCH / FORESIGHT',x('行业往哪里走，你的公司该怎么走。','Where the industry is going. What it means for you.'),x('研究全球产品与商业模型，结合一线经营者交流、公开证据和客户条件，形成有边界的判断。','We combine product and market research, practitioner dialogue, public evidence and client context to form bounded, useful judgments.'))+section('RESEARCH DESK',x('持续研究的核心方向','Core research themes'),body)+close()

def decision():
    stages=[('01','Evidence','证据引擎','从授权数据、公开资料和一线交流建立事实基础。','Build a factual base from authorized data, public sources and practitioner dialogue.'),('02','Benchmark','对标引擎','跨产品、市场和经营阶段识别差异与模式。','Compare products, markets and operating stages.'),('03','Decision','决策引擎','定义问题，比较路径，明确条件与风险。','Define the constraint, compare paths and make assumptions explicit.'),('04','Action','行动层','形成负责人、验证计划、资源安排与复盘。','Assign ownership, validation, resources and review gates.')]
    body='<div class="grid g4">'+''.join(card(x(z,en),x(cz,ce),i) for i,en,z,cz,ce in stages)+'</div>'
    samples=f'<div class="evidence"><div><p class="eyebrow">ILLUSTRATIVE SCENARIOS</p><h2>{x("看清约束，才知道下一步。","Understand the constraint.<br>Then choose the next move.")}</h2><p>{x("这里演示的是工作方法，不读取你的数据、不提供自动诊断。点击不同问题，查看示例前提、约束与行动。","These scenarios illustrate a method. They do not ingest your data or run automatic analysis. Select a question to inspect its premises, constraint and action.")}</p></div>{memo('detail')}</div>'
    return pagehero('GGC INTELLIGENCE / DECISION OS',x('从信号到判断，从判断到行动。','From signals to decisions. From decisions to action.'),x('Evidence → Benchmark → Decision → Action。让经营经验成为可复用的工作流。','Evidence → Benchmark → Decision → Action. Turn operating experience into a reusable workflow.'))+section('THE OPERATING METHOD',x('一套共用的决策能力','One connected decision system'),body)+section('','',samples,kind='alt')+close()

def lab():
    cards=[]
    for group,name,visual,zh,en,url in PRODUCTS:
        status=x('研究 / 产品方向','Research / product track') if group!='knowledge' else x('内容与知识入口','Knowledge resource')
        c=f'<article class="card product-card" data-type="{group}"><div class="product-visual" aria-label="{x("品牌文字示意，非产品截图","Illustrative wordmark, not a product screenshot")}"><span>{escape(visual)}</span></div><span class="status">{status}</span><h3>{escape(name)}</h3><p>{x(zh,en)}</p>{btn(x("查看资料 / 联系","Explore / contact"),url,"10")}</article>'
        cards.append(c)
    return pagehero('LAB WORK / PRODUCTS',x('我们持续研究，也亲自构建。','We study businesses. And build them, too.'),x('产品、工具和研发方向属于不同成熟阶段。项目不等于法律实体，网站入口不等于已验证收入。','Products, tools and R&D tracks have different maturity levels. A project is not a legal subsidiary, and a website is not proof of revenue.'))+section('PRODUCT DIRECTORY',x('产品与实践矩阵','Products and current practice'),filters([('all','全部','All'),('software','AI软件','AI Software'),('games','游戏','Games'),('consumer','消费产品','Consumer'),('knowledge','知识','Knowledge')],'products')+f'<div class="grid g3" id="products">{"".join(cards)}</div><p class="empty" data-empty hidden>{x("此分类暂无项目。","No projects in this category.")}</p>')+close()

def ventures():
    entries=[('01','联合立项','Joint Greenlight','定义赛道、用户、产品和可验证的机会。','Define the category, user, product and testable opportunity.'),('02','MVP与联合研发','MVP & Co-development','组织团队、资源、研发节奏与测试。','Align teams, resources, production and validation.'),('03','联合发行与经营','Publishing & Operations','市场进入、渠道、商业化与长期运营。','Market entry, distribution, monetization and long-term operations.'),('04','产业与资本合作','Strategic Partnerships','围绕具体项目、权限、投入和权益讨论。','Discuss a specific project, rights, contributions and economics.')]
    return pagehero('CO-BUILD / VENTURES',x('看见机会之后，一起把它做出来。','Find the opportunity. Build it together.'),x('GGC在品类判断、研发、发行和经营之间连接互补能力。不是每个合作都需要共同投资。','GGC connects complementary capabilities across category selection, development, publishing and operations. Not every partnership requires joint investment.'))+section('COLLABORATION',x('从具体产品与彼此优势开始','Start with a product and complementary strengths'),'<div class="grid g4">'+''.join(card(x(a,b),x(c,d),i,btn(x('讨论项目','Discuss a project'),'contact.html?track=ventures','01')) for i,a,b,c,d in entries)+'</div>')+close()

def about():
    proofs=[('GLOBAL OPERATIONS','全球头部产品实践','Global flagship product experience','Joyce在Zynga任产品经理，带领多位制作人，主责CityVille腾讯版、FarmVille中文版及全球Bubble／Ruby／Slingo的经营与商业化；任Gameloft亚洲区运营负责人，负责《混沌与秩序》系列全球经营及《小黄人快跑》中国业务。','At Zynga, Joyce was a PM leading multiple producers, with product and commercial responsibility for CityVille (Tencent), FarmVille (China), and global Bubble / Ruby / Slingo. As Gameloft’s Head of Asian Operations, she led global Order & Chaos / Heroes of Order & Chaos and Minion Rush in China.'),('BUILD / OPERATE','从项目到公司','From product to company','研发与发行、团队建设、数据、预算与跨市场经营。','Development, publishing, team-building, data, budgets and cross-market operations.'),('METHOD / KNOWLEDGE','把经验沉淀成方法','Codifying operating experience','《游戏运营与出海实战》作者；持续将经营判断整理为模型、方法和工作流。','Author of Game Operations & Global Expansion; codifying decisions as models, methods and workflows.')]
    body='<div class="grid g3">'+''.join(card(x(a,b),x(c,d),i) for i,a,b,c,d in proofs)+'</div><div class="note">'+x('从旗舰产品经营到研发发行与公司建设，GGC把实战经验转化为团队可复用的判断与行动。','From flagship operations to company building, GGC turns operating experience into practical decisions and action.')+'</div>'
    links='<div class="actions">'+btn(x('Why Joyce 完整资料','Joyce’s executive profile'),'https://biz.ggcgames.com/joyce/','01')+btn('LinkedIn','https://www.linkedin.com/in/minyajing/','04')+btn(x('查看著作','Published book'),'https://ebooks.cmpbook.com/detail?id=26372','10')+'</div>'
    return pagehero('WHY GGC / WHY JOYCE',x('更深的实战，更清楚的判断。','Operating depth. Clearer decisions.'),x('GGC由Joyce创立，以全球游戏与互动娱乐实践为基础，连接行业前瞻、经营诊断与行动。','Founded by Joyce, GGC connects industry foresight, diagnosis and action, grounded in global games and interactive entertainment.'))+section('WHY GGC',x('不只提供观点，更提供可执行的选择。','More than an opinion. A practical choice.'),body+links)+section('VISION',x('让好产品，拥有更大的可能。','Make room for products worth building.'),'<div class="evidence"><p>'+x('把头部经营经验与一线行业认知，转化为优秀团队可复用的决策能力；让资本、人才与技术投向真正值得做的产品。','Make high-calibre operating experience and practitioner insight reusable — so capital, talent and technology reach the products worth building.')+'</p><div><h3>Good Games. A Brighter World.</h3><p>Capital · Flow · Prosperity</p></div></div>',kind='alt')+close()

def contact():
    opts=[('principal','战略与经营','Strategy / operations'),('intelligence','AI与决策系统','AI / decision systems'),('ventures','联合立项','Co-build / ventures'),('products','产品合作','Product partnership'),('media','媒体与活动','Media / events')]
    select=''.join(f'<option value="{k}">{x(a,b)}</option>' for k,a,b in opts)
    fields=''.join(f'<div class="field"><label for="{key}">{x(a,b)}</label><input id="{key}" name="{key}" type="{typ}" autocomplete="{auto}" maxlength="{length}" required></div>' for key,a,b,typ,auto,length in [('name','姓名','Name','text','name',80),('email','回复邮箱','Reply email','email','email',160),('company','公司 / 团队','Company / team','text','organization',140)])
    form=f'<form class="form" data-inquiry><div class="fieldgrid">{fields}<div class="field"><label for="track">{x("合作方向","Partnership track")}</label><select id="track" name="track">{select}</select></div></div><div class="field"><label for="message">{x("你最希望解决的一个业务问题","The business question you most want to solve")}</label><textarea id="message" name="message" minlength="10" maxlength="1500" required></textarea></div><label class="consent"><input name="consent" type="checkbox" required><span>{x("我了解此页面只在本地生成邮件草稿。点击打开邮箱后，需由我自行发送；不会自动加入订阅。","I understand this page prepares a local draft. I must open my email app and send it myself. This does not subscribe me to updates.")}</span></label><p id="form-error" class="error" role="alert"></p><button class="ggc-btn" data-button-id="06" type="submit"><span class="btn-label">{x("生成商务邮件","Prepare business email")}</span>{ARROW}</button><div id="draft-result" class="result" tabindex="-1" hidden><p>{x("草稿已准备好。请打开邮箱核对并发送。","Your draft is ready. Open your email app to review and send it.")}</p><a id="open-email" class="ggc-btn" data-button-id="01">{x("打开邮箱草稿","Open email draft")}{ARROW}</a></div></form>'
    aside='<aside><p class="eyebrow">LET’S TALK</p><h2>'+x('从一个重要的问题开始。','Start with one important question.')+'</h2><p>'+x('告诉我们产品、市场、团队与当前约束。不需要一开始就确定合作形式。','Tell us about the product, market, team and constraint. We can discuss the right engagement model together.')+'</p><div class="proof"><b>WeChat</b><small>17701087579</small></div><div class="proof"><b>Telegram</b><a class="source-link" href="https://t.me/joyceggc">@joyceggc ↗</a></div><div class="proof"><b>'+x('邮件联系','Email')+'</b><a class="source-link" href="mailto:minyajing@gmail.com">minyajing@gmail.com</a></div><p>'+x('当前版本不调用后台，也不收集表单内容。正式CRM与订阅确认流程待接入。','This version does not call a backend or collect form contents. Production CRM and confirmed subscriptions are not connected yet.')+'</p></aside>'
    return pagehero('CONTACT / PARTNERSHIPS',x('你的下一步，值得认真讨论。','Your next move deserves a thoughtful conversation.'),x('战略、诊断、经营合作、产品共建与行业交流。','Strategy, diagnosis, operating partnerships, product building and practitioner exchange.'))+section('','',f'<div class="contact-grid">{aside}{form}</div>')

def buttons():
    blocks=[]
    for id,en,zh,uz,ue in APPROVED:
        label=x('聊聊关键决策','Discuss your next move')
        if id=='08':
            group='<div class="ggc-tabs" role="tablist" aria-label="'+x('组件示例标签','Component example tabs')+'">'
            for j,(a,b) in enumerate([('研究','Research'),('洞察','Insights'),('动态','News')]):group+=btn(x(a,b),style='08',extra=f'role="tab" id="lab-tab-{j}" aria-controls="lab-panel-{j}" aria-selected="{str(j==0).lower()}" tabindex="{0 if j==0 else -1}"',arrow=False)
            group+='</div>'+''.join(f'<p role="tabpanel" id="lab-panel-{j}" aria-labelledby="lab-tab-{j}"'+(' hidden' if j else '')+'>'+x(a,b)+'</p>' for j,(a,b) in enumerate([('研究内容示例。','Research panel example.'),('洞察内容示例。','Insights panel example.'),('动态内容示例。','News panel example.')]))
            states=f'<div class="sample-row"><span class="caption">{x("键盘左右键切换","Use left/right arrow keys")}</span>{group}</div>'
        else:
            states=''.join(f'<div class="sample-row"><span class="caption">{x(z,e)}</span>{btn(label,style=id,extra="data-demo "+attrs)}</div>' for z,e,attrs in [('默认 / 可点击','Default / interactive',''),('悬停','Hover','data-preview-state="hover"'),('键盘焦点','Keyboard focus','data-preview-state="focus"'),('按下','Pressed','data-preview-state="pressed"'),('不可用','Disabled','disabled')])
        blocks.append(f'<article class="card sample"><span class="index">{id} / APPROVED</span><h3>{en}</h3><p class="small">{zh} · {x(uz,ue)}</p>{states}</article>')
    return pagehero('GGC / APPROVED BUTTON SYSTEM',x('六种细节，一致的品牌手感。','Six expressions. One considered system.'),x('已选定：01 · 04 · 06 · 08 · 09 · 10。这里是实际HTML/CSS组件，不是平面图片。','Approved: 01 · 04 · 06 · 08 · 09 · 10. Real HTML/CSS components, not a flattened concept image.'))+section('INTERACTIVE COMPONENTS',x('轻盈、清晰、精细。','Light. Clear. Refined.'),f'<div class="utility">{btn(x("深 / 浅底切换","Toggle background"),style="04",extra="data-surface aria-pressed=\"false\"",arrow=False)}<p class="caption" data-demo-status role="status" aria-live="polite">{x("点击可演示加载状态，不提交业务信息。","Click to preview loading states. No information is submitted.")}</p></div><div class="grid g3">{"".join(blocks)}</div>')

RENDER={'index':home,'expertise':expertise,'research':research,'decision-os':decision,'lab':lab,'ventures':ventures,'about':about,'contact':contact,'buttons':buttons}

def document(key,body):
    names={r[0]:x(r[1],r[2]) for r in ROUTES}; title=names[key]+' · GGC — Global Game Copilot'
    nav=''.join(f'<a href="{k}.html"'+(' aria-current="page"' if key==k else '')+'>'+names[k]+'</a>' for k in ['expertise','research','decision-os','lab','about'])
    logo='<span class="brand"><img src="../assets/ggc-logo.svg" width="109" height="40" alt="GGC"><small>GLOBAL GAME<br>COPILOT</small></span>'
    footer='<footer class="footer"><div class="shell"><div class="footer-grid"><div><a class="brand" href="index.html">'+logo+'</a><p>'+x('战略前瞻、经营判断与真实行动。<br>让好游戏走向更大的世界。','Strategic foresight, operating decisions and real action.<br>Good Games. A Brighter World.')+'</p></div><div><h3>'+x('业务与产品','Business & products')+'</h3>'+''.join(f'<a href="{k}.html">{names[k]}</a>' for k in ['expertise','decision-os','ventures','lab'])+'</div><div><h3>'+x('保持连接','Stay connected')+'</h3><a href="https://www.linkedin.com/in/minyajing/">LinkedIn ↗</a><a href="https://t.me/joyceggc">Telegram ↗</a><a href="https://opsgo.ggcgames.com/">OpsGo ↗</a><a href="contact.html">'+x('合作 / 订阅意向','Partnership / updates interest')+'</a></div></div><div class="footer-bottom"><small>© 2026 GGC · Global Game Copilot</small><small>'+x('Good Games. A Brighter World.','Good Games. A Brighter World.')+'</small></div></div></footer>'
    return f'<!doctype html><html lang="{"zh-CN" if LANG=="zh" else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#f7f8ff"><meta name="description" content="{x("GGC战略前瞻与经营决策：行业研究、企业诊断、AI与产品实践。","GGC strategic foresight and operating decisions: research, diagnosis, AI and product practice.")}"><title>{title}</title><link rel="stylesheet" href="../assets/buttons.css"><link rel="stylesheet" href="../assets/site.css"><script defer src="../assets/app.js"></script></head><body><a class="skip" href="#main">{x("跳到内容","Skip to content")}</a><header class="top"><nav class="shell nav" aria-label="{x("主导航","Main navigation")}"><a href="index.html">{logo}</a><div class="navlinks" id="primary-nav" data-nav data-open="false">{nav}<a href="contact.html">{names["contact"]}</a></div><div class="nav-actions"><a class="lang" data-locale lang="{OTHER}" href="../{OTHER}/{key}.html">{x("EN","中文")}</a>{btn(x("聊聊关键决策","Discuss your next move"),"contact.html","06")}<button class="menu" data-menu type="button" aria-label="{x("打开导航","Open navigation")}" aria-controls="primary-nav" aria-expanded="false">☰</button></div></nav></header><div class="review-note"><div class="shell">{x("GGC 官网开发预览 · 按钮 01 / 04 / 06 / 08 / 09 / 10 已接入","GGC implementation preview · approved buttons 01 / 04 / 06 / 08 / 09 / 10")}</div></div><main id="main">{body}</main>{footer}</body></html>'

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=SRC.parent/'site');args=parser.parse_args();out=args.out.resolve()
    if out==SRC or str(out) in ['/',str(Path.home()),'/app']:raise SystemExit('Refusing unsafe output root')
    assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
    for filename in ['buttons.css','site.css','app.js','ggc-logo.svg']:shutil.copyfile(SRC/filename,assets/filename)
    for LANG in ['zh','en']:
        OTHER='en' if LANG=='zh' else 'zh';folder=out/LANG;folder.mkdir(parents=True,exist_ok=True)
        for key in RENDER:(folder/(key+'.html')).write_text(document(key,RENDER[key]()),encoding='utf-8')
    (out/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=zh/index.html"><title>GGC</title></head><body><a href="zh/index.html">中文</a> · <a href="en/index.html">English</a></body></html>',encoding='utf-8')
    (out/'build-manifest.json').write_text(json.dumps({'version':'2026-10-12','approvedButtons':[1,4,6,8,9,10],'pagesPerLanguage':len(RENDER),'locales':['zh','en'],'backend':'none — local mail draft only','production':False},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'pages':len(RENDER)*2,'approved':[1,4,6,8,9,10]}))
