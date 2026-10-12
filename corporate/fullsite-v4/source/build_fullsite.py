#!/usr/bin/env python3
"""GGC full-site UI implementation. Reuses reviewed copy and six approved buttons.
New detail templates are authored website proposals, not invented client reports.
No application login, subscription, CRM, payment or automated diagnosis is claimed.
"""
from pathlib import Path
from html import escape as esc
import argparse, importlib.util, json, shutil, re, hashlib
S=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('refined',S/'build_refined_site.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
b=r.base
x=b.x
btn=b.btn
section=b.section
BASE_RENDER=dict(b.RENDER)
DETAILS={}
ASSETS=['joyce-approved.webp','book-cover.webp']
MODULES=[
('Strategic Thesis & Portfolio','战略判断与组合管理','找方向、定边界、做分合。','Choose direction, define boundaries and allocate across a portfolio.'),
('Product & Commercial Architecture','产品与商业化架构','把好游戏做成可持续的好生意。','Connect product value with a sustainable business.'),
('Data / Experiment / Stage-Gate OS','数据、实验与阶段评审','用数据验证假设，用阶段评审降低风险。','Validate assumptions with evidence and decision gates.'),
('LiveOps / Lifecycle','长线运营与生命周期','提升留存、扩展内容、延长游戏生命力。','Build retention, content and a durable product lifecycle.'),
('Global Publishing / UA / Distribution','全球发行与用户获取','打通全球市场，找到对应的用户。','Connect global markets with the right audiences.'),
('Organization / Production / Governance','组织、制作与治理','打造高效、可持续的团队与协作机制。','Build sustainable teams, production and decision rights.'),
('Capital / Ecosystem / Institutional Compounding','资本、生态与制度复利','整合资源、放大价值，构建长期生态。','Combine resources and build institutional value over time.')]
CYCLE=[('诊断','Diagnose'),('优先级','Prioritize'),('构建','Build'),('运营','Operate'),('复盘','Review'),('放大 / 停止','Scale / Stop'),('沉淀','Codify')]
RESEARCH=[
('casino','CASINO / SLOT+','产品经济与长期运营','Product economics & long-term operations','虚拟经济、付费结构、活动节奏与玩家生命周期。','Virtual economies, offer structure, LiveOps cadence and player lifecycle.','运营模型与经济系统','Operating models and economies'),
('arcade','ARCADE / HYBRID','玩法成立之后，生意怎样成立？','When the loop works, does the business work?','核心循环、内容效率与商业化结构。','Core loops, content efficiency and monetization structure.','核心循环与商业化','Core loops and monetization'),
('sims','SIMULATION / COZY','机会很大，适合你的团队吗？','An attractive market. The right fit for your team?','用户动机、内容产能、长线目标与品类适配。','Player motivations, content capacity and category fit.','品类与团队适配','Category and capability fit'),
('consumer-ai','AI CONSUMER','从新鲜感，到可持续的产品价值','From novelty to lasting product value','内容、记忆、留存与持续使用的理由。','Content, memory, retention and reasons to return.','用户体验与产品价值','Experience and product value'),
('agent','AI WORKFLOWS','把智能接进实际经营流程','Put intelligence inside the operating workflow','行业情报、创意、商务与工作流协作。','Industry intelligence, creative, outreach and workflow collaboration.','工作流与质量验证','Workflows and evaluation')]
SCOPE=[
('1个问题；60分钟交流；最多30分钟预读；简明行动要点。','One question; 60-minute call; up to 30-minute pre-read; concise next steps.'),
('1个游戏或经营决策；最多20页预读；2小时讨论；2–4页备忘录；1轮澄清。','One game or decision; up to 20 pages reviewed; 2-hour workshop; 2–4-page memo; one clarification round.'),
('1个游戏、1个市场、最多3个对标；KPI基线；新手与经济评审；90天路线图。','One game and market; up to three benchmarks; KPI baseline; onboarding/economy review; 90-day roadmap.'),
('1个产品、最多2个市场；定位与渠道；上线门槛；预算和伙伴需求书。','One title; up to two markets; positioning, channels, launch gates, budget and partner brief.'),
('1个产品、最多2个渠道、30份素材；Cohort/ROAS；测试与停投扩量规则。','One title; up to two channels / 30 creatives; cohort/ROAS; tests and stop/scale rules.'),
('1个核心经济；90天活动框架；产消、礼包、分层；测试工作簿。','One core economy; 90-day event framework; sources/sinks, offers, segments and testing workbook.'),
('最多3个岗位或JD；面试评分；决策权；招聘顺序；负责人讨论。','Up to three roles/JDs; interview rubric, decision rights, hiring sequence and manager workshop.'),
('1类伙伴；公开研究短名单最多10家；合作摘要；经同意的协调。','One partner category; up to ten public-source prospects; pitch brief and permission-based coordination.'),
('1个标的或产品；市场与KPI质量；商业模型；团队；假设、风险与评审问题。','One target/product; market and KPI quality, model, team, assumptions, risk and committee questions.'),
('1个项目；每月6小时含会议、预读与异步沟通；月度决策记录；首期3个月。','One project; six hours/month across calls, pre-read and async; monthly decision log; initial three-month scope.'),
('1个产品市场；每月最多4个主顾问日；周经营会；KPI/WBS；版本、活动、买量；月P&L。','One title/market; up to four principal days/month; weekly reviews; KPI/WBS, releases, LiveOps, UA and monthly P&L.'),
('12个月；每月最多4个主顾问日；季度重置；经营治理与改善。','12 months; up to four principal days/month; quarterly reset, governance and operating improvement.'),
('最多12人；3小时工作坊；课前需求；1条游戏业务AI流程；模板。','Up to 12 participants; three-hour workshop; intake, one game-business AI workflow and templates.'),
('4–6周；1条流程、最多2个授权源或工具；沙盒；最多30个评测；审批与SOP。','4–6 weeks; one workflow with up to two authorized sources/tools; sandbox, up to 30 evaluations, approvals and SOP.'),
('1个游戏；玩家路径、钱包摩擦；链上链下经济假设；留存与落地风险。','One game; player journey, wallet friction, on/off-chain economy assumptions, retention and rollout risk.'),
('最多90分钟；1个业务主题；针对受众的案例与实践清单。','Up to 90 minutes; one business theme, audience-specific examples and a practical checklist.')]


def portrait(kind='panel'):
    if kind=='peek':return '<div class="portrait-peek"><img src="../assets/joyce-approved.webp" alt="Joyce — GGC founder"></div><span class="portrait-sign">Joyce<small>Founder / GGC</small></span>'
    return '<figure class="portrait-panel"><img src="../assets/joyce-approved.webp" alt="Joyce — GGC founder" loading="lazy"><figcaption><strong>Joyce</strong>'+x('GGC创始人 · 全球游戏操盘者 · 作者','Founder · Global game operator · Author')+'</figcaption></figure>'


def sheet(title,rows,cap='GGC / DECISION SYSTEM'):
    return '<div class="glass-sheet"><div class="sheet-brow"><img src="../assets/ggc-logo.svg" alt="GGC"><span>'+cap+'</span></div><h2 class="sheet-head">'+title+'</h2>'+''.join('<div class="sheet-row"><b>'+str(i+1).zfill(2)+'</b><span>'+row+'</span></div>' for i,row in enumerate(rows))+'<p class="sheet-foot">BETTER DECISIONS. A BRIGHTER TOMORROW.</p></div>'


def hero(eye,title,copy,visual,actions=''):
    return '<section class="pagehero"><div class="shell hero-layout"><div class="hero-copy2"><p class="eyebrow">'+eye+'</p><h1>'+title+'</h1><p>'+copy+'</p>'+('<div class="actions">'+actions+'</div>' if actions else '')+'</div><div class="hero-visual">'+visual+'</div></div></section>'


def flow(steps):
    return '<div class="process-row">'+''.join('<article class="process-step"><strong>'+str(i+1).zfill(2)+'</strong><h3>'+x(a,c)+'</h3><p>'+x(z,e)+'</p></article>' for i,(a,c,z,e) in enumerate(steps))+'</div>'


def faq():
    items=[('从哪里开始？','Where do we start?','先说明你的产品、市场和最重要的经营问题。我们再确定问题范围、所需资料与合作深度。','Start with your product, market and critical business question. Then agree the scope, data and level of engagement.'),('需要提供什么资料？','What should we provide?','根据服务范围提供可授权使用的产品信息、现有指标、团队与资源情况；不要提交无权披露的第三方资料。','Provide authorized product information, current metrics and team/resource context appropriate to the agreed scope.'),('是否包含实际执行？','Is execution included?','诊断、顾问和经营合作是不同范围。交付、执行责任、时间及第三方成本在SOW中明确。','Diagnostics, advisory and operating partnerships have different scopes. Deliverables, ownership, time and external costs are agreed in the SOW.')]
    return '<div class="faq">'+''.join('<details><summary>'+x(a,c)+'</summary><p>'+x(z,e)+'</p></details>' for a,c,z,e in items)+'</div>'


def fullhome():
    h=r.refined_home()
    # Portrait appears in the full founder strip, not cropped behind the decision sheets.
    proof='<div class="shell"><div class="founder-strip"><img src="../assets/joyce-approved.webp" alt="Joyce"><div><strong>'+x('Joyce · GGC 创始人','Joyce · Founder of GGC')+'</strong><p>'+x('全球旗舰产品经营 · 数据与商业化 · 方法与著作','Global flagship operations · Data & commercialization · Methods & published work')+'</p></div>'+btn(x('为什么是我们','Why GGC'),'about.html','01')+'</div></div>'
    h=h.replace('<section class="section white"><div class="shell"><div class="section-head"><div><p class="eyebrow">BUILT FROM REAL OPERATING EXPERIENCE',proof+'<section class="section white"><div class="shell"><div class="section-head"><div><p class="eyebrow">BUILT FROM REAL OPERATING EXPERIENCE',1)
    return h


def expertise():
    old=BASE_RENDER['expertise'](); rest=old[old.index('<section class="section'):]
    for sid,*_ in b.SERVICES:rest=rest.replace('contact.html?service='+sid,'service-'+sid.lower()+'.html').replace('Discuss this service','View service').replace('讨论这项服务','查看服务详情')
    visual=sheet(x('先诊断。<br>再做关键决定。','Diagnose first.<br>Make the right call.'),[x('产品 / 市场 / 经营问题','Product / market / operating question'),x('现有证据与主要约束','Available evidence and key constraints'),x('判断、取舍与下一步','Decision, trade-offs and next actions')])
    return hero('GGC PRINCIPAL / EXPERTISE',x('把复杂问题，<br>变成清晰的行动。','Complex questions.<br>Clear operating action.'),x('从单次诊断到长期经营合作。先定义问题、交付与责任，再确定合作形式。','From a focused diagnostic to an operating partnership. Define the decision, deliverables and ownership first.'),visual,btn(x('选择合作方式','Explore engagements'),'#services','06')+btn(x('聊聊你的问题','Discuss your question'),'contact.html','04'))+rest


def service_detail(n):
    sid,group,zh,en,cz,ce=b.SERVICES[n];scope=SCOPE[n]
    visual=sheet(x('你会拿到什么','What you receive'),[x('明确的工作范围','A clearly scoped engagement'),x(scope[0],scope[1]),x('SOW确定责任、时间与验收','An SOW defining ownership, timing and acceptance')],sid+' / GGC PRINCIPAL')
    body=hero(sid+' / '+group.upper(),x(zh,en),x(cz,ce),visual,btn(x('讨论这项服务','Discuss this engagement'),'contact.html?service='+sid,'06')+btn(x('所有服务','All services'),'expertise.html','04'))
    intro='<div class="feature-split"><div class="paper-stack">'+sheet(x('从问题，到交付。','From the question<br>to the deliverable.'),[x('核心问题是什么？','What is the decision?'),x('现有证据支持什么？','What does the evidence support?'),x('该做什么，如何验证？','What should happen, and how is it tested?')])+'</div><div><p class="eyebrow">SCOPE / DELIVERY</p><h2>'+x('范围清楚，<br>合作才真正高效。','Clear scope.<br>Useful collaboration.')+'</h2><p>'+x(scope[0],scope[1])+'</p><ul class="deliverable-list"><li>'+x('资料和判断依据可追溯','Traceable inputs and decision rationale')+'</li><li>'+x('合作角色、交付与执行责任明确','Explicit roles, deliverables and execution ownership')+'</li><li>'+x('费用与具体范围以现行价目表及SOW为准','Current rate card and signed SOW govern fees and scope')+'</li></ul>'+btn(x('查看现行参考价目','View the current rate card'),'https://biz.ggcgames.com/joyce/rate-card.html','10')+'</div></div>'
    body+=section('ENGAGEMENT DETAIL','',intro)
    body+=section('WORKING TOGETHER',x('从一次清晰的讨论开始。','Begin with a well-defined question.'),flow([('定义问题','Define','目标、范围和约束。','Goal, scope and constraints.'),('梳理证据','Review','产品、数据和团队条件。','Product, data and team context.'),('形成判断','Decide','明确选择与行动。','Choices and operating actions.'),('交接复盘','Review','交付与后续验证。','Handoff and validation.')]),kind='alt')
    return body+section('FAQ',x('合作前，先说清楚。','Clarity before commitment.'),faq())+b.close()


def research():
    v=sheet(x('不只知道发生了什么。<br>更知道它意味着什么。','Beyond what happened.<br>Understand what it means.'),[x('信号：产品、市场与玩家','Signals: products, markets and players'),x('解释：模式、约束与差异','Interpretation: patterns, constraints, differences'),x('判断：与你公司的相关性','Decision: relevance to your company')],'RESEARCH / FORESIGHT')
    cards=[]
    for slug,cap,z,e,sz,se,kz,ke in RESEARCH:
        cards.append('<article class="card research-card" data-type="'+('ai' if 'AI' in cap else 'games')+'"><div class="report-art"><strong>'+cap.split(' / ')[0]+'</strong><small>GGC RESEARCH / METHOD BRIEF</small></div><div class="report-body"><span class="status">'+x('研究主题 / 方法说明','Research theme / method brief')+'</span><h3>'+x(z,e)+'</h3><p>'+x(sz,se)+'</p>'+btn(x('进入研究详情','Read the brief'),'research-'+slug+'.html','10')+'</div></article>')
    return hero('RESEARCH / FORESIGHT',x('看清行业，<br>也看清你的机会。','See the industry.<br>Find your opportunity.'),x('从全球产品、商业模式与经营实践中寻找有意义的信号。研究的终点，是更清晰的选择。','Identify meaningful signals in global products, commercial models and operating practice. Research should inform a decision.'),v,btn(x('浏览研究主题','Browse research themes'),'#research-grid','06')+btn('OpsGo','https://opsgo.ggcgames.com/','04'))+section('RESEARCH LIBRARY',x('研究与前瞻。','Research & foresight.'),b.filters([('all','全部','All'),('games','游戏品类','Games'),('ai','AI与工作流','AI / Workflows')],'research-grid')+'<div class="grid g3" id="research-grid">'+''.join(cards)+'</div><p class="empty" data-empty hidden>'+x('暂无匹配主题。','No matching topics.')+'</p>',x('此处展示研究主题与方法。市场数据和结论需查看对应原始报告。','These are themes and methods; consult the original reports for market data and findings.'))+b.close()


def research_detail(n):
    slug,cap,z,e,sz,se,kz,ke=RESEARCH[n]
    visual=sheet(x('问题 → 证据 → 判断','Question → Evidence → Decision'),[x(kz,ke),x('拆解产品与经营条件','Examine product and operating conditions'),x('形成可验证的下一步','Form a testable next step')],'METHOD BRIEF')
    content=hero('RESEARCH / '+cap,x(z,e),x(sz,se),visual,btn(x('回到研究目录','All research'),'research.html','04'))
    ids=[('question','研究的问题','The question'),('evidence','观察与资料','Evidence to review'),('method','如何形成判断','Decision method'),('action','用于你的业务','Apply to your business')]
    toc='<aside class="toc"><strong>IN THIS BRIEF</strong>'+''.join('<a href="#'+i+'">'+x(a,c)+'</a>' for i,a,c in ids)+'</aside>'
    article='<article class="article-body"><span class="status">'+x('方法说明 · 不是新发布的市场结论','Method brief · not new market findings')+'</span><section id="question"><h2>'+x('先把问题问对。','Start with the right question.')+'</h2><p>'+x(sz,se)+'</p><p>'+x('判断机会时，需要区分行业吸引力与具体公司的适配：产品、团队、预算、时间和资源条件必须一起看。','Distinguish category attractiveness from company fit. Product, team, budget, timing and resources have to be considered together.')+'</p></section><section id="evidence"><h2>'+x('从资料，到可讨论的证据。','From information to usable evidence.')+'</h2><ul class="deliverable-list"><li>'+x('产品、用户行为与经营指标','Product, player behaviour and operating metrics')+'</li><li>'+x('公开或授权的市场与竞品材料','Public or authorized market and competitor material')+'</li><li>'+x('团队能力、产能、预算与组织条件','Team capability, production capacity, budget and organization')+'</li></ul></section><section id="method"><h2>'+x('Decide · Build · Compound','Decide · Build · Compound')+'</h2><p>'+x('Joyce Method将判断、构建与复利作为三项核心能力，并用数据、实验与阶段评审连接策略和行动。','Joyce Method defines three core capabilities — Decide, Build and Compound — connecting strategy with action through data, experiments and stage gates.')+'</p>'+btn(x('查看完整方法','Explore the full method'),'method.html','01')+'</section><section id="action"><h2>'+x('最后，回答你下一步怎么走。','Finally, define your next move.')+'</h2><p>'+x('把研究转化为你公司的明确问题、资料缺口、优先级和验证动作。具体判断须建立在产品与数据之上。','Translate research into a company-specific question, evidence gaps, priorities and validation actions. A specific recommendation requires product and data review.')+'</p><p class="image-license">'+x('内容依据：GGC现有研究目录与《Joyce Method》海报的三项能力、七个模块。未添加新的行业统计或预测结果。','Basis: existing GGC research themes and the three capabilities / seven modules in the Joyce Method poster. No new industry statistics or forecast results are asserted.')+'</p></section></article>'
    rail='<aside class="article-rail"><p class="eyebrow">FOR YOUR COMPANY</p><h3>'+x('这与你当前的决策有关吗？','Relevant to a decision you face?')+'</h3><p>'+x('带着你的产品、阶段和问题来讨论。','Bring your product, stage and question.')+'</p>'+btn(x('讨论关键决策','Discuss a decision'),'contact.html?track=principal','06')+'<hr style="border:0;border-top:1px solid #eadcec;margin:23px 0"><a class="source-link" href="https://opsgo.ggcgames.com/">OpsGo ↗</a></aside>'
    return content+section('','',f'<div class="reading-grid">{toc}{article}{rail}</div>')+b.close()


def method():
    v=sheet(x('从复杂的游戏问题，<br>到可执行的经营系统。','From complex game problems<br>to an executable operating system.'),[x('Decide / 判断','Decide'),x('Build / 构建','Build'),x('Compound / 复利','Compound')],'JOYCE METHOD / GGC')
    modules='<div class="diagram-seven">'+''.join('<article class="module"><em>'+str(i+1).zfill(2)+'</em><h3>'+x(zh,en)+'</h3><p>'+x(z,e)+'</p></article>' for i,(en,zh,z,e) in enumerate(MODULES))+'</div>'
    cycle='<div class="method-cycle">'+('<i>→</i>'.join('<span>'+x(z,e)+'</span>' for z,e in CYCLE))+'</div>'
    return hero('JOYCE METHOD / GLOBAL GAME OPERATING SYSTEM',x('有判断。<br>有方法。有体系。','Better judgment.<br>A repeatable system.'),x('把复杂的游戏与商业问题，拆成可验证的判断、可执行的经营系统和可复利的组织能力。','Turn complex game-business problems into evidence-based decisions, executable operating systems and compounding organizational capability.'),v,btn(x('讨论如何应用','Apply the method'),'contact.html','06'))+section('SEVEN MODULES',x('完整的游戏经营系统。','A complete game operating system.'),modules)+section('FROM INSIGHT TO IMPACT',x('不是一次判断，而是持续的工作方法。','Not a one-off opinion. A way of operating.'),cycle,kind='alt')+section('PRINCIPLES',x('先看清，再做对。','Clarity before commitment.'),'<div class="grid g3">'+''.join(b.card(x(z,e),x(c,d),str(i+1).zfill(2)) for i,(z,e,c,d) in enumerate([('阶段先于战略','Stage before strategy','先分阶段，再谈战略。','Understand the stage before choosing the strategy.'),('模型先于放大','Model before scale','先跑通模型，再放大。','Prove the model before expanding.'),('行为先于观点','Behavior before opinion','用行为与数据说话。','Let behavior and evidence inform the decision.')]))+'</div>')+b.close()


def decision():
    old=BASE_RENDER['decision-os']();rest=old[old.index('<section class="section'):]
    spheres='<div class="glass-sheet"><div class="sheet-brow"><img src="../assets/ggc-logo.svg" alt="GGC"><span>INTELLIGENCE</span></div><h2 class="sheet-head">'+x('同一套底层能力。<br>不同的业务应用。','One core system.<br>Different applications.')+'</h2><div class="mini-spheres">'+''.join('<div class="sphere"><strong>'+a+'</strong><small>'+x(z,e)+'</small></div>' for a,z,e in [('Evidence','真实输入','Real inputs'),('Benchmark','更清晰的对标','Clearer perspective'),('Decision','更好的判断','Better decisions'),('Agent','可复用的工作流','Reusable workflows')])+'</div></div>'
    return hero('GGC INTELLIGENCE / OPERATOR DECISION OS',x('把洞察，<br>变成经营能力。','Turn insight<br>into operating capability.'),x('Evidence Engine、Benchmark Engine、Decision Engine与Agent Architecture，构成共用的证据与决策系统。','Evidence, Benchmark and Decision engines, connected with Agent Architecture: a shared evidence and decision system.'),spheres,btn(x('查看方法体系','Explore the method'),'method.html','06'))+rest


def lab():
    old=BASE_RENDER['lab']();rest=old[old.index('<section class="section'):]
    # Every existing project now has its own explorable detail route.
    for i,product in enumerate(b.PRODUCTS):
        old_link=btn(x('查看资料 / 联系','Explore / contact'),product[-1],'10')
        rest=rest.replace(old_link,btn(x('查看产品详情','Explore product'),'product-'+str(i+1).zfill(2)+'.html','10'),1)
    v='<div class="product-hero-art"><div class="wordtile back"></div><div class="wordtile">GGC<br>LAB</div><span class="status">'+x('产品 · 工具 · 研发','Products · Tools · R&D')+'</span></div>'
    return hero('LAB WORK / OUR PRODUCT ECOSYSTEM',x('从方法，到产品。<br>从想法，到真实体验。','Methods into products.<br>Ideas into experiences.'),x('GGC Build Together、研究、知识内容、消费AI与自研方向，共同构成产品组合。各项目成熟度分别标注。','Co-building, research, knowledge, consumer AI and R&D form the GGC product ecosystem. Each project has its own maturity and scope.'),v,btn(x('浏览产品','Browse products'),'#products','06'))+rest


def gallery(name,group):
    entries=[('定位','Positioning','用户与业务场景','Audience & use case'),('方法','Method','输入、判断与行动','Inputs, decisions and action'),('合作','Partnership','产品路径与下一步','Product path and next steps')]
    slides=[]
    for i,(z,e,cz,ce) in enumerate(entries):
        slides.append('<div class="gallery-slide" data-slide'+(' hidden' if i else '')+'><div class="gallery-grid"><div class="gallery-object"><strong>'+esc(name)+'</strong><small>'+x(z,e).upper()+' / GGC</small></div><div class="gallery-copy"><p class="eyebrow">'+str(i+1).zfill(2)+' / PRODUCT OVERVIEW</p><h3>'+x(cz,ce)+'</h3><p>'+x('这里呈现项目的说明结构与业务定位。进入官方产品站可查看实际功能和可用版本。','This panel presents the project’s explanation structure and business positioning. Refer to the official product site for actual features and available versions.')+'</p><p class="image-license">'+x('产品说明图 · 非实际App截图','Product information panel · not an app screenshot')+'</p></div></div></div>')
    return '<div class="gallery-frame" data-gallery>'+''.join(slides)+'<div class="gallery-controls">'+btn(x('上一张','Previous'),style='04',extra='data-prev aria-label="Previous"',arrow=False)+'<div class="gallery-dots">'+''.join('<button type="button" data-slide-to="'+str(i)+'" aria-pressed="'+str(i==0).lower()+'" aria-label="'+str(i+1)+'"></button>' for i in range(3))+'</div><span data-gallery-status aria-live="polite" style="font-size:11px;color:#8b7699"></span>'+btn(x('下一张','Next'),style='01',extra='data-next aria-label="Next"')+'</div></div>'


def product_detail(i):
    group,name,visual,cz,ce,url=b.PRODUCTS[i]
    ext=url if url.startswith('http') else 'contact.html?track='+('ventures' if group=='games' else 'products')
    visual='<div class="product-hero-art"><div class="wordtile back"></div><div class="wordtile">'+esc(visual)+'</div><span class="status">'+x('项目 / 产品方向','Project / product track')+'</span></div>'
    body=hero('GGC LAB / '+group.upper(),esc(name),x(cz,ce),visual,btn(x('打开项目入口','Explore project'),ext,'06',extra='data-product-source')+btn(x('讨论产品合作','Discuss partnership'),'contact.html?track=products','04'))
    audience={'software':('游戏与数字产品团队','Game and digital-product teams'),'games':('研发与发行伙伴','Development and publishing partners'),'consumer':('消费者、内容及品牌伙伴','Consumers, content and brand partners'),'knowledge':('行业读者与知识用户','Industry readers and knowledge users')}
    content='<div class="grid g3">'+b.card(x('面向谁','For whom'),x(*audience[group]),'01')+b.card(x('产品角色','Product role'),x(cz,ce),'02')+b.card(x('下一步','Next step'),x('查看项目当前信息，或围绕产品和合作方式发起讨论。','Review current project information or start a product and partnership conversation.'),'03')+'</div>'
    body+=section('PRODUCT OVERVIEW',x('定位、价值与合作。','Positioning, value and collaboration.'),content)
    body+=section('PRODUCT EXPLORER',x('进一步了解这个项目。','Explore the project.'),gallery(name,group),kind='alt')
    body+=section('RELATED WORK',x('同一生态，更多实践。','Connected practice across the ecosystem.'),'<div class="actions">'+btn(x('返回全部产品','All products'),'lab.html','01')+btn(x('了解Decision OS','Explore Decision OS'),'decision-os.html','04')+'</div>')
    return body+b.close()


def ventures():
    old=BASE_RENDER['ventures']();rest=old[old.index('<section class="section'):]
    v=sheet(x('共同做成一个项目。','Build something together.'),[x('好的方向与验证条件','A strong thesis and validation gates'),x('互补的团队与资源','Complementary teams and resources'),x('明确的投入、职责与权益','Explicit contributions, responsibilities and rights')],'CO-BUILD / GGC')
    return hero('CO-BUILD / VENTURES',x('有好的方向，<br>也要有做成的组合。','The right idea.<br>The right team to build it.'),x('从联合立项到MVP、研发、发行与产业协作。找到互补优势，共同推进下一步。','From joint greenlight to MVP, development, publishing and strategic collaboration. Bring complementary strengths to the next milestone.'),v,btn(x('提交项目讨论','Discuss a project'),'contact.html?track=ventures','06'))+rest.replace(b.close(),'')+section('PARTNERSHIP FLOW',x('合作不是一句话，而是一条路径。','A partnership needs a working path.'),flow([('洞察','Insight','发现真实需求与机会。','Identify the real need.'),('共创','Co-create','找到互补的人与资源。','Bring complementary strengths.'),('验证','Validate','用产品和数据验证价值。','Test value with product and data.'),('推进','Build','明确分工和后续里程碑。','Agree roles and milestones.')]),kind='alt')+b.close()


def about():
    body=hero('WHY GGC / WHY JOYCE',x('真实的经历。<br>清晰的判断。<br>可落地的结果。','Real experience.<br>Clearer judgment.<br>Practical action.'),x('从旗舰产品经营到研发发行与公司建设，GGC把实战经验转化为团队可复用的方法、体系与经营行动。','From flagship operations to development, publishing and company-building: reusable methods, systems and operating action.'),portrait(),btn(x('方法体系','Joyce Method'),'method.html','06')+btn(x('我的书','The book'),'book.html','04'))
    old=BASE_RENDER['about']();rest=old[old.index('<section class="section'):]
    body+=rest.replace(b.close(),'')
    timeline='<div class="process-row">'+''.join('<article class="process-step"><strong>'+i+'</strong><h3>'+x(z,e)+'</h3><p>'+x(c,d)+'</p></article>' for i,z,e,c,d in [('01','产品实战','Product practice','全球游戏、数据与商业化。','Global games, data and commercialization.'),('02','公司经营','Company operations','研发、发行、团队与组织。','Development, publishing and organizations.'),('03','方法沉淀','Codify methods','研究、著作、框架与SOP。','Research, books, frameworks and SOPs.'),('04','智能与共建','Intelligence & co-build','AI系统、联合项目与产品实践。','AI systems, joint projects and product practice.')])+'</div>'
    body+=section('PAST / PRESENT / NEXT',x('从经历到体系，从体系到更多可能。','From experience to systems. From systems to possibility.'),timeline,kind='alt')
    return body+b.close()


def book():
    v='<div class="book-stack"><img class="book-card" src="../assets/book-cover.webp" alt="游戏运营与出海实战 — supplied book cover"></div>'
    chapters=[('行业与职业','Industry & career'),('团队与协作','Team & organization'),('数据与指标','Data & KPIs'),('产品与变现','Product & monetization'),('全球化运营','Global operations'),('实战案例解析','Case studies'),('增长与用户体验','User experience'),('未来趋势与思维','Future trends & mindset')]
    body=hero('MY BOOK / PUBLISHED KNOWLEDGE',x('游戏运营与出海实战','Game Operations & Global Expansion'),x('策略、方法与技巧。从实战出发，将运营经验沉淀为更容易理解和应用的框架。','Strategies, methods and practical techniques. Operating experience translated into understandable, usable frameworks.'),v,btn(x('查看出版社书页','Publisher listing'),'https://ebooks.cmpbook.com/detail?id=26372','06')+btn(x('了解方法','Explore the method'),'method.html','04'))
    body+=section('TOPICS IN THE SUPPLIED BOOK POSTER',x('八个主题，一套完整视角。','Eight themes. A connected perspective.'),'<div class="chapter-grid">'+''.join('<article class="chapter"><b>'+str(i+1).zfill(2)+'</b><h3>'+x(z,e)+'</h3></article>' for i,(z,e) in enumerate(chapters))+'</div>',x('主题来自你提供的著作介绍海报；不是另行编写的正式目录。','Themes reproduced from the supplied book poster, not a newly asserted formal table of contents.'))
    body+=section('WHY IT MATTERS',x('不是理论合集，而是经验的系统化。','Not theory alone. Operating experience, systematized.'),'<div class="grid g3">'+b.card(x('完整的经营框架','A connected operating framework'),x('从本土运营到全球发行，连接角色、流程、数据与商业化。','Connect roles, workflows, data and commercialization, from local operation to global publishing.'),'01')+b.card(x('可以复用的方法','Reusable methods'),x('用真实工作的结构，帮助团队理解问题和建立工作方式。','Structure real operating work into understandable questions and working methods.'),'02')+b.card(x('不同角色都能使用','Across different roles'),x('面向运营、发行、产品、创业者与团队负责人。','For operators, publishers, product teams, founders and managers.'),'03')+'</div>',kind='alt')
    return body+b.close()


def updates():
    v=sheet(x('重要的变化，<br>值得持续关注。','Meaningful change.<br>Worth following.'),[x('行业研究与经营判断','Industry research and decisions'),x('GGC产品与AI工作流','GGC products and AI workflows'),x('著作、方法与公开分享','Books, methods and public talks')],'GGC UPDATES')
    form='<form class="interest-form" data-interest><h3>'+x('登记动态订阅意向','Register interest in updates')+'</h3><div class="field"><label for="updates-email">'+x('你的邮箱','Your email')+'</label><input type="email" id="updates-email" name="email" autocomplete="email" required></div><div class="topic-choices">'+''.join('<label><input type="checkbox" name="topic" value="'+e+'">'+x(z,e)+'</label>' for z,e in [('游戏与发行','Games & publishing'),('AI与决策系统','AI & Decision OS'),('产品与共建','Products & co-build'),('方法与公开分享','Methods & speaking')])+'</div><label class="consent"><input type="checkbox" required><span>'+x('我了解当前只生成意向邮件，由我确认发送；不等于已经订阅。','I understand this prepares an interest email for me to send; it does not activate a subscription.')+'</span></label><button type="submit" class="ggc-btn" data-button-id="06">'+x('生成意向邮件','Prepare interest email')+b.ARROW+'</button><div class="result" data-interest-result tabindex="-1" hidden><p>'+x('意向邮件已准备好。打开邮箱核对后发送。','Your interest email is ready. Open your mail app, review and send.')+'</p><a class="ggc-btn" data-button-id="01" data-interest-mail>'+x('打开邮件草稿','Open email draft')+'</a></div></form>'
    state_titles=[('pending','等待确认','Pending confirmation'),('confirmed','确认完成','Confirmed'),('unsubscribed','已退订','Unsubscribed')]
    demo='<details class="state-demo"><summary>'+x('设计评审：订阅状态样稿（不触发真实订阅）','Design review: subscription states (no real subscription)')+'</summary><p style="font-size:11px;margin:14px 0">'+x('以下为未来后台接入后的UI状态样式，仅供评审。','These are UI states for review of a future backend integration.')+'</p><div class="ggc-tabs" role="group" aria-label="State previews">'+''.join(btn(x(z,e),style='08',extra='data-show-state="'+key+'" aria-pressed="'+str(i==0).lower()+'"',arrow=False) for i,(key,z,e) in enumerate(state_titles))+'</div>'+''.join('<div class="demo-state" data-state="'+key+'"'+(' hidden' if i else '')+'><div class="status-icon">'+['✉','✓','−'][i]+'</div><strong>'+x(z,e)+'</strong><p>'+x('状态样稿 · 未发送邮件或改变订阅记录。','State preview only — no email sent and no subscription changed.')+'</p></div>' for i,(key,z,e) in enumerate(state_titles))+'</details>'
    left='<div><p class="eyebrow">STAY IN THE LOOP</p><h2>'+x('少一点噪声。<br>多一点有用的判断。','Less noise.<br>More useful perspective.')+'</h2><p style="margin-top:20px">'+x('关注真正影响产品、发行和经营的变化。当前可通过邮件登记意向，正式订阅服务尚未接入。','Follow changes that matter to product, publishing and operations. Interest can currently be registered by email; automated subscription delivery is not connected.')+'</p><div class="actions">'+btn('OpsGo','https://opsgo.ggcgames.com/','01')+btn('LinkedIn','https://www.linkedin.com/in/minyajing/','04')+'</div>'+demo+'</div>'
    return hero('GGC UPDATES / INSIGHTS',x('保持连接，<br>一起看向下一程。','Stay connected.<br>Look ahead with us.'),x('研究、实践、产品与公开分享，持续连接更好的判断。','Research, practice, products and public knowledge — connected with better decisions.'),v)+section('','',f'<div class="updates-grid">{left}{form}</div>')


def contact():
    old=BASE_RENDER['contact']();rest=old[old.index('<section class="section'):]
    intro='<div class="founder-strip"><img src="../assets/joyce-approved.webp" alt="Joyce"><div><strong>Joyce / GGC</strong><p>'+x('先讨论真正的问题，再确定合适的合作。','Define the real question, then the right engagement.')+'</p></div></div>'
    v=sheet(x('你在决定什么？','What are you deciding?'),[x('产品、市场与当前阶段','Product, market and current stage'),x('真正希望解决的一件事','The one issue you want to resolve'),x('已有数据、团队与资源','Your data, team and resources')],'LET’S TALK')
    return hero('CONTACT / PARTNERSHIPS',x('下一步，<br>我们认真聊聊。','Your next move.<br>Let’s talk it through.'),x('战略与诊断、长期经营、AI流程、联合产品和全球合作。','Strategy and diagnostics, operating partnerships, AI workflows, joint products and global collaboration.'),v)+section('','',intro)+rest


def notfound():
    return hero('404 / KEEP EXPLORING',x('这条路径，<br>还没有内容。','This path is<br>not available.'),x('回到首页，或者继续浏览我们的专业能力与产品实践。','Return home, or explore our expertise and product practice.'),sheet('404',[x('重新选择方向','Choose a direction'),x('回到关键问题','Return to the question')]),btn(x('回到首页','Return home'),'index.html','06')+btn(x('联系GGC','Contact GGC'),'contact.html','04'))


def layout(key,body,parent='index',title=None):
    h=r.refined_document(parent,body)
    h=h.replace('fidelity-v2 prism-v3 page-','fidelity-v2 prism-v3 fullsite page-')
    h=h.replace('</head>','<link rel="stylesheet" href="../assets/fullsite.css"><script defer src="../assets/fullsite.js"></script></head>')
    h=re.sub(r'<title>.*?</title>','<title>'+esc((title or key)+' · GGC Global Game Copilot')+'</title>',h)
    # Keep language switching on the same semantic deep page.
    h=h.replace('../'+b.OTHER+'/'+parent+'.html','../'+b.OTHER+'/'+key+'.html')
    parent_names={a:x(z,e) for a,z,e in b.ROUTES}
    breadcrumb='<div class="page-tools"><div class="shell"><div class="crumb"><a href="index.html">GGC</a><span>/</span><a href="'+parent+'.html">'+parent_names.get(parent,'GGC')+'</a>'+('<span>/</span><span>'+esc(title or key)+'</span>' if key!=parent else '')+'</div><a href="../review.html">'+x('整站UI总览 ↗','All-screen review ↗')+'</a></div></div>'
    if key!='index':h=h.replace('<main id="main">',breadcrumb+'<main id="main">')
    h=h.replace('<a href="contact.html">'+x('合作 / 订阅意向','Partnership / updates interest')+'</a>','<a href="contact.html">'+x('商务合作','Partnership')+'</a><a href="updates.html">'+x('动态与订阅','Updates')+'</a><a href="method.html">Joyce Method</a><a href="book.html">'+x('著作','Book')+'</a>')
    return h


def register():
    global DETAILS
    DETAILS={
    'index':('index',fullhome,'首页','Home'),
    'expertise':('expertise',expertise,'专业能力','Expertise'),
    'research':('research',research,'研究与前瞻','Research'),
    'decision-os':('decision-os',decision,'决策系统','Decision OS'),
    'lab':('lab',lab,'产品与实践','Lab Work'),
    'ventures':('ventures',ventures,'联合立项','Ventures'),
    'about':('about',about,'为什么 GGC','Why GGC'),
    'contact':('contact',contact,'联系合作','Contact'),
    'buttons':('buttons',BASE_RENDER['buttons'],'组件与状态','Components'),
    'method':('decision-os',method,'Joyce Method方法体系','Joyce Method'),
    'book':('about',book,'著作','Book'),
    'updates':('research',updates,'动态与订阅意向','Updates & interest'),
    '404':('index',notfound,'页面不存在','Page not found')}
    for i,s in enumerate(b.SERVICES):DETAILS['service-'+s[0].lower()]=('expertise',lambda i=i:service_detail(i),s[2],s[3])
    for i,s in enumerate(RESEARCH):DETAILS['research-'+s[0]]=('research',lambda i=i:research_detail(i),s[2],s[3])
    for i,s in enumerate(b.PRODUCTS):DETAILS['product-'+str(i+1).zfill(2)]=('lab',lambda i=i:product_detail(i),s[1],s[1])

REPRESENTATIVES=['index','expertise','service-s02','research','research-sims','decision-os','method','lab','product-10','ventures','about','book','updates','contact','buttons','404']

def reviewhub(out):
    cards=[]
    for key in REPRESENTATIVES:
        parent,fn,zh,en=DETAILS[key]
        cards.append('<article class="hub-card"><span class="eyebrow">'+str(len(cards)+1).zfill(2)+' / '+key.upper()+'</span><h2>'+esc(zh)+'<br><small>'+esc(en)+'</small></h2><div class="actions"><a class="ggc-btn" data-button-id="06" href="zh/'+key+'.html">中文 ↗</a><a class="ggc-btn" data-button-id="04" href="en/'+key+'.html">English ↗</a></div></article>')
    html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>GGC · Full-site UI Review</title><link rel="stylesheet" href="assets/buttons.css"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/fullsite.css"></head><body><main class="review-hub"><div class="shell"><img src="assets/ggc-logo.svg" width="145" alt="GGC"><p class="eyebrow">FULL-SITE UI / DESIGN-TO-CODE</p><h1>整站UI，一次看全。<br>One system. Every screen.</h1><p class="review-count">16类UI / '+str(len(DETAILS)*2)+'个双语页面 / 16项服务详情 / 5项研究主题 / 14项产品详情</p><p>这是可点击的前端与视觉评审包。商务联系与订阅意向只生成邮件草稿；状态样稿不代表后台已接入。</p><div class="hub-grid">'+''.join(cards)+'</div><h2 style="margin-top:40px">所有详情页面 / All instances</h2><div class="hub-grid">'+''.join('<article class="hub-card"><strong>'+esc(v[2])+'</strong><p>'+esc(v[3])+'</p><a href="zh/'+k+'.html">中文 ↗</a> · <a href="en/'+k+'.html">EN ↗</a></article>' for k,v in DETAILS.items() if k not in REPRESENTATIVES)+'</div></div></main></body></html>'
    (out/'review.html').write_text(html,encoding='utf-8')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=S.parent/'site-full');args=parser.parse_args();out=args.out.resolve()
    if out in [Path('/'),S,Path('/app'),Path.home()]:raise SystemExit('Unsafe output path')
    # Reuse the exact reviewed base sources; generated output is isolated.
    assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
    for name in ['buttons.css','site.css','app.js','fidelity.css','prism.css','prism-ribbon.svg','fullsite.css','fullsite.js']:shutil.copyfile(S/name,assets/name)
    shutil.copyfile(S/'ggc-logo-refined.svg',assets/'ggc-logo.svg')
    for name in ASSETS:
        src=S/name
        if not src.is_file():raise SystemExit('Missing approved asset: '+str(src))
        shutil.copyfile(src,assets/name)
    # Refer to browser-served font CSS, never distribute font files.
    font_url='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+SC:wght@400;500;600;700;800;900&display=swap'
    f=assets/'fidelity.css';f.write_text('@import url("'+font_url+'");\n'+f.read_text().replace("'Noto Sans CJK SC'","'Noto Sans SC','Noto Sans CJK SC'"),encoding='utf-8')
    b.memo=r.refined_memo
    register()
    for loc in ['zh','en']:
        b.LANG=loc;b.OTHER='en' if loc=='zh' else 'zh';folder=out/loc;folder.mkdir(exist_ok=True)
        for key,(parent,fn,zh,en) in DETAILS.items():(folder/(key+'.html')).write_text(layout(key,fn(),parent,x(zh,en)),encoding='utf-8')
    (out/'index.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=zh/index.html"><title>GGC</title></head><body><a href="review.html">UI review</a> · <a href="zh/index.html">中文</a> · <a href="en/index.html">English</a></body></html>')
    reviewhub(out)
    manifest={'version':'2026-10-12-full-site-ui-v4','screen_types':len(REPRESENTATIVES),'locale_pages':len(DETAILS)*2,'routes':list(DETAILS),'representatives':REPRESENTATIVES,'services':16,'research_themes':5,'product_details':14,'approved_buttons':[1,4,6,8,9,10],'production':False,'forms':'local email draft only','source_basis':['reviewed corporate copy @64bbb83','supplied Joyce Method poster pp1-4','supplied original posters pp2,6-8'],'new_content':'UI organization and explanation copy; not new market findings or live-product claims'}
    (out/'build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages':len(DETAILS)*2,'screen_types':len(REPRESENTATIVES),'out':str(out)}))
if __name__=='__main__':main()
