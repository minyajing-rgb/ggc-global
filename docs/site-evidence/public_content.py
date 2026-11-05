"""Public, bilingual case library. Evidence-scoped content, shared by both GGC sites."""
from html import escape as e
from pathlib import Path
import re,shutil
VERSION='2026-11-05-bp-kpi-v2'
# Each pair is Chinese / English. No client identities or private operating data.
CASES=[
('zynga-social','ZYNGA · SOCIAL / SIMS','2010–2012',
 ('CityVille 腾讯版与 FarmVille 中文版','CityVille Tencent edition & FarmVille Chinese edition'),
 ('把全球社交游戏模型，落到中国平台的用户行为。','Adapt global social-game models to player behavior on Chinese platforms.'),
 ('产品经理（PM）；带领、统筹多位PM与制作人，主责相应版本的产品经营与商业化。','Product Manager; led and coordinated PMs and producers, owning product and commercial operations for these editions.'),
 ('平台用户、新手体验、社交传播与付费需要共同建模。','Platform behavior, onboarding, social distribution and monetization needed a connected model.'),
 ('建立DAU / Revenue Model、K-factor与行为分群，结合用户研究和AB实验，把数据问题转成产品及运营优先级。','Built DAU/revenue models, K-factor and behavioral segments; connected player research and A/B experiments to product and operating priorities.'),
 ('CityVille中国项目职业记录：D1留存提升700 bps，即7个百分点；只对应该项目。','Career-reported CityVille China result: D1 retention increased by 700 bps, or 7 percentage points, on that scoped project.'),
 ('留下DAU / 收入模型、实验规则与社交循环评审框架；留存、商业化和传播一起看。','Reusable DAU/revenue models, experiment rules and social-loop reviews: assess retention, monetization and distribution together.')),
('zynga-arcade','ZYNGA · GLOBAL ARCADE','2010–2012',
 ('Bubble · Ruby · Slingo 全球产品','Bubble · Ruby · Slingo global products'),
 ('从玩法与数据，到可持续的全球产品经营。','Connect gameplay and data to sustainable global product operations.'),
 ('产品经理（PM），带领多个PM与制作人，主责全球主产品的经营、数据与商业化。','Product Manager leading multiple PMs and producers, with ownership of global product operations, data and monetization.'),
 ('多个产品组需要统一产品假设、数据定义、上线节奏与经营判断。','Multiple product teams needed shared hypotheses, metric definitions, launch cadence and operating decisions.'),
 ('把玩法、Spec、DAU与收入模型、用户研究、实验和发布流程连成一套跨组工作方式。','Connected gameplay, specifications, DAU/revenue models, player research, experiments and release processes across teams.'),
 ('历史主责履历记录了这些产品的上线与商业化经营，并沉淀可跨产品复用的数据和工作规范。','The career record documents product launches and commercial ownership, with data and operating practices reused across titles.'),
 ('Arcade先验证核心动作与回访理由，再评估内容供给和长期用户价值。','For Arcade, validate the core action and return reason before assessing content supply and long-term player value.')),
('huogu-wuxia','HUOGU · 0 → 1','2012–2013',
 ('《武侠Q传》：从立项到商业化','Wuxia Q Zhuan: from greenlight to commercialization'),
 ('把产品规划、经济模型和发行里程碑放进同一张图。','Put product planning, economics and launch milestones into one operating plan.'),
 ('火谷网络产品总监；负责产品规划、DAU / Revenue Model、定价、上线及跨职能推进。','Product Director at Huogu, responsible for planning, DAU/revenue models, pricing, launch and cross-functional execution.'),
 ('新品需要同时建立玩法与经济假设、数据验证和团队交付机制。','A new title needed gameplay and economic hypotheses, evidence and a delivery organization together.'),
 ('把商业化、数值、数据实验、招聘与KR、渠道及上线计划前置，按里程碑推进产品。','Brought monetization, economy, experiments, hiring, key results, channels and release planning into the development milestones.'),
 ('本人原始职业资料记载：历史海内外月流水约人民币6,000万元，峰值过1亿元。流水为项目规模，非净利润或个人收入。','First-party career record: historical monthly gross bookings of approximately CNY60m across markets, with a peak above CNY100m. These are project gross bookings.'),
 ('0→1交付同时包含产品、经济与证据；把上线条件写进立项。','A zero-to-one launch needs product, economics and evidence together; define launch gates at greenlight.')),
('gameloft','GAMELOFT · GLOBAL LIVEOPS','2013–2014',
 ('全球 MMO / MOBA，与中国区 Minion Rush','Global MMO / MOBA & Minion Rush China'),
 ('全球经营内核，配合不同地区的运营节奏。','A shared operating core, adapted to regional execution.'),
 ('亚洲区运营负责人；主责全球Order & Chaos、Heroes of Order & Chaos，以及Minion Rush中国区业务。','Head of Asian Operations; owned global operating work on Order & Chaos and Heroes of Order & Chaos, and Minion Rush China.'),
 ('跨工作室、地区和平台的版本、经济、活动与数据需要统一协作。','Releases, economies, events and data required coordination across studios, regions and platforms.'),
 ('统筹选型与竞品、经济与活动、数据、商店及版本准备，建立研发文档模板与跨区经营接口。','Coordinated benchmarking, economies, events, analytics, store and release readiness; established documentation templates and regional operating interfaces.'),
 ('协同10+工作室、500+跨职能网络，形成跨产品的发布与经营机制；500+为协作网络规模。','Worked across 10+ studios and a 500+ cross-functional collaboration network, establishing release and operating mechanisms across products.'),
 ('全球化从产品与组织开始：统一指标语言，保留区域内容、平台和商业差异。','Globalization starts with product and organization: shared metric definitions, with regional content, platform and commercial adaptations.')),
('founder-build','FOUNDER / CEO · BUILD','2014–2017',
 ('从零组建研发公司与产品团队','Building a development company and product teams'),
 ('在有限资金与时间里，把产品真正推向上线。','Ship products within real capital and time constraints.'),
 ('北京桃源西谷创始人 / CEO，承担公司经营、团队与研发交付责任。','Founder and CEO of Beijing Taoyuan Xigu, responsible for the company, team and development delivery.'),
 ('公司初创同时面临产品选择、核心人才、研发预算与发行准备。','The new company needed product selection, core talent, development budgets and publishing readiness at once.'),
 ('组建工作室，建立预算、Roadmap、招聘和绩效机制，协调市场、法务及外部资源，按产品阶段安排投入。','Built the studio, budgets, roadmaps, hiring and performance systems; coordinated market, legal and external resources with stage-based allocation.'),
 ('原始履历包括单机产品两周上线、棋牌大厅三个月上线；公司经历北京区域性股权市场挂牌。','The career record includes a single-player product shipped in two weeks and a card-game lobby in three months, plus a regional equity-market listing.'),
 ('把公司现金、产品组合与继续 / 停项条件一起管理，留下可复用的研发与发布机制。','Manage cash, portfolio and continue/stop gates together; preserve reusable development and release systems.')),
('publishing-os','FOUNDER / CMO · PUBLISHING','2017–2020',
 ('发行体系搭建与收购后业务协同','Publishing systems & post-acquisition operations'),
 ('把产品、渠道、条款、团队和运营交接串起来。','Connect products, channels, terms, teams and operating handoffs.'),
 ('发行公司创始人；业务被收购后担任海外集团CMO。','Publishing-company founder; later CMO of the overseas group after the business was acquired.'),
 ('发行能力需要从关系和临时处理，转成稳定的产品引入、上线和经营流程。','Publishing needed repeatable product intake, launch and operating processes alongside partner relationships.'),
 ('建立CP引入标准、渠道与商务条款、海外市场计划、发行SOP及团队交接，推进跨集团组织协同。','Established developer intake criteria, channels and commercial terms, overseas plans, publishing SOPs and team handoffs across the group.'),
 ('原始履历记载三天诊断、一周处理积压问题、两周形成稳定发行体系；另一独立广告 / 发行平台建设案例记录收入十倍增长。','The career record describes a three-day diagnosis, one week resolving a backlog and two weeks establishing a stable publishing system. A separate advertising/publishing platform case records 10x revenue growth.'),
 ('发行是一套阶段门与责任体系。平台10倍收入案例独立计量，不归因给单一游戏。','Publishing needs decision gates and ownership. The platform revenue case is measured separately from individual game outcomes.')),
('turnaround','ANONYMIZED · TURNAROUND','历史经营案例 / Historical case',
 ('复杂项目重整：恢复产品与组织连续性','Complex turnaround: restoring product and organizational continuity'),
 ('先恢复经营事实，再决定重建、放大或停止。','Recover operating truth, then decide whether to rebuild, scale or stop.'),
 ('经营重整与跨职能协同；客户和项目名称脱敏。','Operating turnaround and cross-functional coordination; client and title anonymized.'),
 ('接手记录包括收入停滞、存量用户流失、人员更替、历史资料与数据断层。','The case describes stalled revenue, existing-player loss, personnel changes and gaps in documentation and data.'),
 ('先盘点用户与产品资产，恢复指标基线；按P0/P1/P2重排版本、商业化和团队职责，建立周经营复盘。','Reviewed player and product assets, restored metric baselines, reprioritized releases, monetization and ownership, and established weekly operating reviews.'),
 ('沉淀了先恢复数据与组织连续性、再验证经营修复的接管方法。','Produced a takeover method that restores data and organizational continuity before evaluating operating recovery.'),
 ('接管清单、指标词典、责任表、修复顺序和阶段评审；对外不沿用币种与周期未确认的收入速记。','Reusable takeover checklist, metric dictionary, ownership map, recovery sequence and stage reviews.')),
('ai-validation','GGC · AI-ASSISTED VALIDATION','历史案例 / Historical case',
 ('AI辅助验证：同时看速度与用户价值','AI-assisted validation: speed and player value'),
 ('更早获得能够改变投入决策的证据。','Obtain evidence early enough to change investment decisions.'),
 ('产品验证、创意实验与经营模型设计；沿用脱敏历史项目记录。','Product validation, creative experiments and operating-model design, from an anonymized historical case.'),
 ('验证周期长，研发试错与素材测试尚未连接长期用户价值。','Long validation cycles and disconnected development trials, creative testing and player-value measurement.'),
 ('用AI辅助研究和创意供给，把Demo、素材实验、回访和LTV放进同一阶段评审；逐轮决定继续、调整或停止。','Used AI-assisted research and creative production, connecting prototypes, creative tests, return behavior and LTV to continue/adjust/stop reviews.'),
 ('同组历史Before / After：验证10周→4周；素材测试50→160；CTR 1.2%→1.62%；LTV US$12.5→US$16。','One historical before/after set: validation 10→4 weeks; creative tests 50→160; CTR 1.2%→1.62%; LTV US$12.5→US$16.'),
 ('保留实验定义和样本边界。以上为原稿历史自述，未独立审计，不代表未来项目效果。','Preserve experiment definitions and sample boundaries. These are first-party historical figures, not independently audited or forecasts.')),
]
AI_CASES=[
('office',('AI文明 → 七人办公室','AI civilization → Seven-Person Office'),('从宏大世界缩成可以观察、干预和验证的小组织。','Reduce a large world to a small organization that can be observed and tested.'),('最初范围过大，变量过多，行为与结果难以验证。','The initial scope had too many variables to verify behavior and outcomes.'),('缩到七个角色、一个办公室，观察分工、交接、关系与权力；把角色动作和真实执行分开。','Reduced scope to seven roles and one office; explored allocation, handoffs, relationships and power, separating simulation from real execution.'),('留下可交互流程模拟和组织验证问题；浏览器模拟不执行真实外部任务。','Produced an interactive workflow simulation and organizational questions. The browser simulation does not execute external tasks.'),'https://ai.ggcgames.com/'),
('demo',('20+ Demo → 产品验收','20+ demos → product acceptance'),('把生成、交互、产品与经营分成四层证据。','Separate generation, interaction, product and commercial evidence.'),('快速生成多个Demo后，代码可运行仍不能证明用户能完成任务或愿意付费。','After rapid prototype generation, runnable code still did not establish task completion or willingness to pay.'),('逐项检查完整路径、错误分支、移动端、上线状态和数据；增加留存、付费意愿与ROI门槛。','Added complete-path, failure-state, mobile, release and data checks, followed by retention, willingness-to-pay and ROI gates.'),('沉淀Product Review与分阶段验收；Demo数量作为探索记录单列。','Established product reviews and staged acceptance; prototype counts remain an exploration record.'),None),
('bunny',('Bunny：原创卡牌与AI消费体验','Bunny: original cards & AI consumer experience'),('从卡牌、对话与Web / App雏形，进入持续使用和付费验证。','Move from cards, conversation and Web/App prototypes toward repeated use and paid validation.'),('需要同时对齐需求、支付、权益、数据归因和留存。','Requirements, payment, entitlement, attribution and retention needed to work together.'),('按生产可用、留存与回收分阶段验收，检查购买后的真实权益及使用闭环。','Applied separate production, retention and payback gates, including post-purchase entitlement and use.'),('形成消费AI产品验收路径；产品发布与商业验证分别记录。','Produced a consumer-AI acceptance path; release and commercial validation are tracked separately.'),None),
('studio',('AI Content / Studio：内容到分发','AI Content / Studio: creation to distribution'),('将图文、视频、多语内容与渠道能力接起来。','Connect images, copy, video and multilingual content to channel capability.'),('平台接口和UI各有差异，内容生成之后仍需人工审核和发布核验。','Platform APIs and interfaces differed; generation still required review and publication verification.'),('按每个渠道的真实能力分发，保留人审、素材版本、发布回执与日志，再比较内容效果。','Distributed within each channel’s actual capabilities; retained human review, asset versions, publication receipts and logs before evaluating performance.'),('留下渠道适配、内容质检、回执与复盘SOP；按渠道记录接通状态。','Produced channel-adaptation, content-review, receipt and retrospective SOPs, with connection state recorded per channel.'),None),
('bd',('AI BD Agent：从名单到真人需求','AI BD Agent: from lists to real buyer needs'),('把找人、触达、回复、需求与成交逐级拆开。','Track discovery, contact, reply, validated need and sale as distinct stages.'),('发出消息后，送达、真人回复和成交仍需要各自验证。','A sent message still needed separate evidence for delivery, a human reply and a sale.'),('建立公司与联系人去重、资格门槛、抑制规则和Reply Desk，把真人回复放在流程前面。','Established account/contact deduplication, eligibility gates, suppression rules and a reply desk, prioritizing real replies.'),('沉淀可追溯的商务流程与漏斗口径；名单规模与真实客户分别计量。','Produced a traceable commercial workflow and funnel definitions; list size and real customers are counted separately.'),None),
]
CATEGORIES=[('AI Game & Simulation','游戏与模拟','范围与行为可验证','Verifiable scope and behavior'),('AI Creative Factory','创意工厂','创意质量与渠道适配','Creative quality and channel fit'),('AI Research & Intelligence','研究与情报','来源、口径与时效','Sources, definitions and freshness'),('AI Coding & Prototyping','编码与原型','完整路径与产品可用','Complete flows and usability'),('AI Consumer Products','消费产品','留存、付费与权益','Retention, payment and entitlement'),('Agent Automation','Agent自动化','权限、恢复与人审','Permissions, recovery and review'),('AI Distribution & BD','分发与商务','送达、回复与需求','Delivery, reply and need'),('AI Commerce & Infrastructure','交易与基础设施','交易、部署与归因','Transactions, deployment and attribution'),('AI Knowledge & OS','知识与操作系统','经验复用与资产沉淀','Reuse and compounding assets')]
MODULES=[('战略判断与组合','Strategy & portfolio','赛道、市场顺序、投入、立项与停项条件。','Category thesis, market sequence, allocation and greenlight/stop gates.','Category Thesis · Decision Memo'),('产品与商业化','Product & commercialization','核心循环、新手、成长、经济、付费分层与定价。','Core loop, onboarding, progression, economy, payer segments and pricing.','Economy Model · Product Roadmap'),('数据、实验与阶段门','Data, experiments & gates','DAU / Revenue、KPI树、分群、基线与实验。','DAU/revenue models, KPI trees, cohorts, baselines and experiments.','KPI Tree · Experiment Plan'),('LiveOps与生命周期','LiveOps & lifecycle','回访理由、内容供给、活动增量、召回和付费节奏。','Return reasons, content supply, event lift, reactivation and monetization cadence.','LiveOps Calendar · Lifecycle Plan'),('全球发行与分发','Global publishing & distribution','地区、平台、素材、渠道、回本与扩量条件。','Markets, platforms, creatives, channels, payback and scaling gates.','Global Launch System · GTM'),('组织、制作与治理','Organization, production & governance','岗位、决策权、WBS、版本、预算与损益复盘。','Roles, decision rights, WBS, releases, budgets and P&L reviews.','Org Blueprint · RACI · P&L Review'),('资本、生态与复利','Capital, ecosystem & compounding','共建、伙伴、权益、项目组合与可复用IP。','Co-builds, partners, rights, portfolios and reusable IP.','Partner Plan · Playbook · AI Workflow')]
PRINCIPLES=[('阶段先于战略','Stage before strategy'),('模型先于放大','Model before scale'),('基线先于目标','Baseline before target'),('行为先于观点','Behavior before opinion'),('实验先于争论','Experiment before argument'),('系统先于症状','System before symptom'),('商业化内置于产品','Commercialization inside product'),('全球化是经营重构','Globalization as operating redesign'),('统一经营语言','One operating language'),('决策权重于会议','Decision rights over meetings'),('停止也是有效决策','Stop is a valid decision'),('每个项目留下IP','Every project leaves IP')]
GATES=[('G0','机会','Opportunity','真实问题与适配','Real problem and fit'),('G1','可行性','Feasibility','能力、成本与实现','Capability, cost and implementation'),('G2','可用性','Usability','用户能完成任务','Users can complete the task'),('G3','吸引力','Desirability','愿意回来、推荐','Users return and recommend'),('G4','商业化','Monetization','真实付费与权益','Real payment and entitlement'),('G5','经济性','Economics','成本、回本与规模','Cost, payback and scale'),('G6','复用性','Reusability','能留下长期资产','Creates a lasting asset')]
TIMELINE=[('2025.01–02','创意探索','Creative exploration'),('2025.02–04','工具与效率实验','Tools and productivity'),('2025.04–12','商业模式筛选','Business-model screening'),('2026.06–07','Agent工作流实验','Agent workflow experiments'),('2026.08–09','多产品并行孵化','Portfolio incubation'),('2026.09–10','验收与经营决策','Acceptance and operating decisions')]

def text(pair,loc):
    if loc:return e(pair[0 if loc=='zh' else 1])
    return '<span class="proof-zh" lang="zh">'+e(pair[0])+'</span><span class="proof-en" lang="en">'+e(pair[1])+'</span>'

def section(id,kicker,title,intro,body,loc):
    t=lambda z,en:text((z,en),loc)
    return f'<section class="ggc-proof section" id="{id}" data-proof-version="{VERSION}"><div class="proof-wrap"><header class="proof-heading"><p class="proof-kicker">{e(kicker)}</p><h2>{text(title,loc)}</h2><p>{text(intro,loc)}</p></header>{body}</div></section>'

def career_cases(loc=None,compact=False):
    t=lambda z,en:text((z,en),loc)
    cards=''
    chosen=CASES[:4] if compact else CASES
    for n,c in enumerate(chosen):
        id,tag,date,title,lead,role,problem,action,result,reuse=c
        rows=''.join('<div><dt>'+text(label,loc)+'</dt><dd>'+text(val,loc)+'</dd></div>' for label,val in [(('我的职责','My role'),role),(('经营问题','Operating problem'),problem),(('关键动作','Critical actions'),action),(('结果与证据','Result & evidence'),result),(('沉淀与迁移','Reusable system'),reuse)])
        cards+=f'<article class="proof-case" id="case-{id}"><p class="proof-tag">{e(tag)}</p><h3>{text(title,loc)}</h3><p class="proof-lead">{text(lead,loc)}</p><details><summary>{t("展开案例 · 职责 / 动作 / 结果","Read case · role / action / result")}</summary><dl>{rows}</dl></details></article>'
    body=('<p class="proof-next"><a href="#ai-practice">'+t('AI实践复盘','AI practice')+'</a> · <a href="#joyce-method">Joyce Method</a></p>' if loc is None else '')+'<div class="proof-grid">'+cards+'</div>'
    if compact:body+='<p class="proof-next"><a href="about.html#case-library">'+t('查看全部8组案例与经营方法 →','Explore all 8 operating cases →')+'</a></p>'
    body+='<p class="proof-note">'+t('案例依据Joyce本人职业记录与已整理项目资料。历史成果按项目分别计量；客户案例已脱敏，过往雇主不代表现有合作或背书。','Based on Joyce’s first-party career and project records. Historical results are scoped by project; client cases are anonymized, and former employers do not imply current endorsement.')+'</p>'
    return section('career-library','SELECTED OPERATING CASES',('救产品、造旗舰，把经验变成体系。','Turn products into flagships. Turn experience into systems.'),('从全球旗舰产品，到研发公司、发行体系与AI验证：看清每次经营判断如何落地。','From global titles to company-building, publishing systems and AI validation: how operating decisions became action.'),body,loc)

def ai(loc=None,compact=False):
    t=lambda z,en:text((z,en),loc)
    body=ai_results(loc)+'<div class="proof-timeline">'+''.join('<div><b>'+d+'</b><span>'+t(z,en)+'</span></div>' for d,z,en in TIMELINE)+'</div>'
    if compact:
        body+='<div class="proof-grid">'+''.join('<article class="proof-case"><p class="proof-tag">AI PRACTICE / '+str(i+1).zfill(2)+'</p><h3>'+text(c[1],loc)+'</h3><p>'+text(c[2],loc)+'</p></article>' for i,c in enumerate(AI_CASES[:3]))+'</div><p class="proof-next"><a href="research-agent.html#ai-practice">'+t('阅读5个实践复盘、9类尝试与7大决策门槛 →','Read 5 case reviews, 9 experiment categories and 7 decision gates →')+'</a></p>'
    else:
        body+='<h3 class="proof-subhead">'+t('五个实践复盘','Five practice reviews')+'</h3><div class="proof-grid">'
        for id,title,lead,problem,action,output,url in AI_CASES:
            rows=''.join('<div><dt>'+text(label,loc)+'</dt><dd>'+text(val,loc)+'</dd></div>' for label,val in [(('遇到的问题','The problem'),problem),(('调整与验证','Adjustment & validation'),action),(('留下的能力','Capability retained'),output)])
            link=('<p><a href="'+url+'" target="_blank" rel="noopener noreferrer">'+t('体验流程模拟 ↗','Explore the workflow simulation ↗')+'</a></p>') if url else ''
            body+='<article class="proof-case" id="practice-'+id+'"><p class="proof-tag">EXPERIMENT → LEARNING → SYSTEM</p><h3>'+text(title,loc)+'</h3><p class="proof-lead">'+text(lead,loc)+'</p><details><summary>'+t('展开实践 · 问题 / 调整 / 沉淀','Read review · problem / adjustment / learning')+'</summary><dl>'+rows+'</dl>'+link+'</details></article>'
        body+='</div><h3 class="proof-subhead">'+t('九类AI探索，共用一套判断系统。','Nine experiment categories. A shared decision system.')+'</h3><div class="proof-categories">'+''.join('<article><b>'+str(i+1).zfill(2)+'</b><h4>'+t(z,en)+'</h4><p>'+t(qz,qe)+'</p></article>' for i,(en,z,qz,qe) in enumerate(CATEGORIES))+'</div>'
        body+='<h3 class="proof-subhead">'+t('七大决策门槛：每一关留下证据。','Seven decision gates. Evidence at every stage.')+'</h3><div class="proof-gates">'+''.join('<div><b>'+id+'</b><h4>'+t(z,en)+'</h4><p>'+t(qz,qe)+'</p></div>' for id,z,en,qz,qe in GATES)+'</div>'
        body+='<div class="proof-callout"><h3>'+t('执行、商业与组织，三层一起学习。','Learn at execution, business and organization levels.')+'</h3><p>'+t('执行层修功能、补接口、回归与发布；商业层重看用户价值、假设和实验；组合层决定加码、停损、复用或迁移。探索 → 筛选 → 构建验证 → 调整回摆 → 资产沉淀，反馈可以返回前一阶段。','At execution level, fix, integrate, test and release. At business level, revisit user value, hypotheses and experiments. At portfolio level, scale, stop, reuse or transfer. Explore → select → build/test → adjust → compound, with feedback returning to earlier stages.')+'</p></div>'
    body+='<p class="proof-note">'+t('依据《AI实践复盘》2026年10月21日八页版与《全球运营与发行实践》10月22日v10。以上记录实验、调整和方法沉淀；各产品的生产可用、留存与付费验证分别验收。','Based on the 21 October 2026 eight-page AI practice review and the 22 October v10 global-operations deck. These describe experiments and learning; production readiness, retention and paid validation are assessed separately per product.')+'</p>'
    return section('ai-practice','AI PRACTICE / 2025–2026',('从真实试错，到可复用的决策系统。','From real experiments to reusable decision systems.'),('把问题暴露、假设修正与经验复用的速度，变成下一次产品和经营判断的优势。','Surface problems, revise hypotheses and preserve learning to improve the next product and operating decision.'),body,loc)

def method(loc=None,compact=False):
    t=lambda z,en:text((z,en),loc)
    body='<div class="proof-three">'+''.join('<article><b>'+en+'</b><h3>'+t(z,ez)+'</h3><p>'+t(c,ec)+'</p></article>' for en,z,ez,c,ec in [('DECIDE','看方向、定阶段','Direction and stage','判断赛道、市场、产品、瓶颈与资源，明确下一项决策。','Assess category, market, product, bottlenecks and resources; define the next decision.'),('BUILD','把判断接进系统','Put judgment into systems','将产品、经济、数据、发行与组织转成有负责人的交付。','Turn product, economy, data, publishing and organization into owned deliverables.'),('COMPOUND','让项目留下资产','Preserve reusable assets','把结果沉淀为模型、案例、SOP、知识与AI工作流。','Codify results as models, cases, SOPs, knowledge and AI workflows.')])+'</div>'
    if compact:
        body+='<p class="proof-next"><a href="method.html#joyce-method">'+t('查看七模块、十二原则与落地流程 →','Explore 7 modules, 12 principles and the operating process →')+'</a></p>'
    else:
        body+='<h3 class="proof-subhead">'+t('七个模块，每一项都有交付物。','Seven modules, with concrete outputs.')+'</h3><div class="proof-modules">'+''.join('<article><b>'+str(i+1).zfill(2)+'</b><h3>'+t(z,en)+'</h3><p>'+t(c,ec)+'</p><small>'+e(out)+'</small></article>' for i,(z,en,c,ec,out) in enumerate(MODULES))+'</div>'
        body+='<h3 class="proof-subhead">'+t('十二条经营原则','Twelve operating principles')+'</h3><ol class="proof-principles">'+''.join('<li>'+text(p,loc)+'</li>' for p in PRINCIPLES)+'</ol>'
        body+='<div class="proof-callout"><h3>'+t('七步执行，把判断接到下一轮数据。','Seven operating steps, closing the evidence loop.')+'</h3><p>'+t('诊断 → 优先级 → 构建系统 → 运营 → 复盘 → 放大 / 重建 / 停止 → 沉淀。','Diagnose → prioritize → build the system → operate → review → scale / rebuild / stop → codify.')+'</p><p>'+t('首30天：W1全面Review；W2建立KPI基线和P0/P1/P2；W3把需求送进版本；W4回收数据，决定下一周期。具体节奏随项目范围与资料条件约定。','First 30 days: W1 review; W2 KPI baselines and priorities; W3 put requirements into releases; W4 recover evidence and decide the next cycle. Timing depends on scope and available inputs.')+'</p></div>'
        body+='<div class="proof-callout"><h3>'+t('GGC Intelligence：让方法进入工作流。','GGC Intelligence: putting the method into workflows.')+'</h3><p>'+t('Evidence Engine结构化来源；Benchmark Engine统一可比口径；Decision Engine形成选项与取舍；Agent Architecture承接任务、审核、回执与反馈。按模块和项目逐步建设与验证。','Evidence Engine structures sources; Benchmark Engine aligns comparable definitions; Decision Engine develops options and trade-offs; Agent Architecture handles tasks, review, receipts and feedback. Built and validated module by module.')+'</p></div>'
    body+='<p class="proof-note">'+t('依据Joyce Method 35页母稿、10月12日职业与经营体系更新、10月23日四页视觉版。三步为管理框架，七模块为能力结构，七步为执行流程。','Based on the 35-page Joyce Method master, the 12 October operating-system update and the 23 October four-page visual edition. Three capabilities frame management; seven modules organize capabilities; seven steps guide execution.')+'</p>'
    return section('joyce-method','JOYCE METHOD / DECIDE · BUILD · COMPOUND',('可验证的判断，可执行的系统，可复利的能力。','Evidence-based decisions. Executable systems. Compounding capability.'),('把15年以上的产品、商业化、发行与组织经验，变成团队可以理解、使用和交接的工作方法。','Translate 15+ years of product, commercialization, publishing and organizational experience into methods teams can use and transfer.'),body,loc)

CSS='''
/* Scoped editorial evidence components; existing site branding is preserved. */
.ggc-proof.section{--proof-accent:#77508b;--proof-line:#e5dce9;--proof-bg:#f9f6fc;scroll-margin-top:100px;color:#262038;padding:72px 24px;background:linear-gradient(140deg,#fff 45%,var(--proof-bg));font-family:inherit}
.ggc-proof *{box-sizing:border-box;min-width:0}.proof-wrap{max-width:1200px;margin:auto}.proof-heading{max-width:900px;margin-bottom:32px}.proof-kicker,.proof-tag{font-size:11px;line-height:1.6;letter-spacing:.12em;font-weight:700;color:var(--proof-accent);margin:0 0 14px}.proof-heading h2{font-size:clamp(28px,3.6vw,43px);line-height:1.3;letter-spacing:-.025em;margin:0 0 18px;font-family:inherit;font-weight:800}.proof-heading>p:last-child{max-width:760px;font-size:16px;line-height:1.85;color:#62546e}.proof-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;align-items:start}.proof-case{padding:30px;border:1px solid var(--proof-line);border-radius:18px;background:#ffffffed;box-shadow:0 8px 32px #61407407}.proof-case h3{font-weight:700;font-size:24px;line-height:1.4;font-family:inherit;margin:0 0 14px}.proof-lead{font-size:15px;line-height:1.85;color:#62546e;margin:0 0 18px}.proof-case details{border-top:1px solid var(--proof-line);padding-top:16px}.proof-case summary{cursor:pointer;color:var(--proof-accent);font-size:14px;font-weight:700;line-height:1.7;padding:6px 0}.ggc-proof a{color:var(--proof-accent);text-decoration:underline;text-underline-offset:4px}.proof-case summary:focus-visible,.ggc-proof a:focus-visible{outline:3px solid var(--proof-accent);outline-offset:5px;border-radius:2px}.proof-case dl{margin:20px 0 0}.proof-case dl>div{margin:0 0 18px}.proof-case dt{font-size:12px;font-weight:800;color:var(--proof-accent);margin:0 0 6px}.proof-case dd{font-size:14px;line-height:1.9;margin:0;color:#51465a}.proof-note{max-width:1000px;font-size:12px;line-height:1.8;color:#73667a;margin:25px 0 0}.proof-next{margin-top:24px;font-size:15px;font-weight:700}.proof-timeline{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:0 0 34px}.proof-timeline>div{border-left:3px solid var(--proof-accent);padding:10px 15px}.proof-timeline b{display:block;font-size:16px;margin-bottom:8px}.proof-timeline span{font-size:14px;line-height:1.7}.proof-subhead{font-size:25px;font-family:inherit;line-height:1.5;margin:42px 0 22px}.proof-categories,.proof-modules{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.proof-categories article,.proof-modules article{padding:23px;background:#fff;border:1px solid var(--proof-line);border-radius:14px}.proof-categories b,.proof-modules b{font-size:12px;color:var(--proof-accent)}.proof-categories h4,.proof-gates h4{font-size:17px;line-height:1.5;margin:10px 0}.proof-categories p,.proof-gates p,.proof-modules p{font-size:14px;line-height:1.8;margin:8px 0 0}.proof-gates{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.proof-gates>div{padding:19px;background:var(--proof-bg);border-radius:12px;border:1px solid var(--proof-line)}.proof-gates b{font-size:20px;color:var(--proof-accent)}.proof-callout{border-left:3px solid var(--proof-accent);padding:22px 26px;margin-top:30px;background:var(--proof-bg);border-radius:0 14px 14px 0}.proof-callout h3{font-size:22px;line-height:1.5;font-family:inherit;margin:0 0 14px}.proof-callout p{font-size:15px;line-height:1.9;margin:10px 0 0}.proof-three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.proof-three article{padding:28px;background:var(--proof-bg);border:1px solid var(--proof-line);border-radius:16px}.proof-three b{color:var(--proof-accent);font-size:13px;letter-spacing:.1em}.proof-three h3,.proof-modules h3{font-size:22px;line-height:1.5;font-family:inherit;margin:12px 0}.proof-three p{font-size:15px;line-height:1.85;margin:0}.proof-modules small{display:block;font-size:12px;line-height:1.6;color:var(--proof-accent);margin-top:17px}.proof-principles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 36px;padding-left:23px}.proof-principles li{font-size:15px;line-height:1.8;padding:8px 2px}.proof-principles li::marker{color:var(--proof-accent);font-weight:800}.proof-en{display:inline}.proof-zh{display:none}html[lang^=zh] .proof-en{display:none}html[lang^=zh] .proof-zh{display:inline}
@media(max-width:800px){.proof-categories,.proof-modules,.proof-gates,.proof-principles{grid-template-columns:repeat(2,minmax(0,1fr))}.proof-three{grid-template-columns:1fr}.proof-grid{gap:16px}.proof-case{padding:23px}.ggc-proof.section{padding:50px 22px}}
@media(max-width:540px){.proof-grid,.proof-categories,.proof-modules,.proof-gates,.proof-principles{grid-template-columns:1fr}.proof-timeline{grid-template-columns:repeat(2,minmax(0,1fr))}.proof-case h3{font-size:22px}.ggc-proof.section{padding:44px 20px}.proof-callout{padding:20px}.proof-heading h2{font-size:28px}.proof-heading>p:last-child{font-size:15px}.proof-principles{gap:0}}
'''

def inject(html,body,css_href,anchor=None):
    if 'data-proof-version=' in html:raise ValueError('Already patched: rebuild from source before reinjecting')
    if anchor:
        if html.count(anchor)!=1:raise ValueError('Expected unique insertion anchor '+anchor)
        html=html.replace(anchor,body+anchor,1)
    else:
        if html.count('</main>')!=1:raise ValueError('Expected one main')
        html=html.replace('</main>',body+'</main>',1)
    return html.replace('</head>','<link rel="stylesheet" href="'+css_href+'?v='+VERSION+'"></head>',1)

def apply_biz(root):
    root=Path(root)
    shutil.copytree(Path(__file__).parent/'logos',root/'joyce/assets/bp-logos',dirs_exist_ok=True)
    for rel in ['index.html','joyce/index.html']:
        p=root/rel;h=p.read_text();h=inject(h,cases()+ai()+method(),'/joyce/assets/operating-proof.css','<section class="section sectors" id="sectors">')
        anchor='<a href="#about">'
        if anchor not in h:raise ValueError('Missing About navigation anchor')
        h=h.replace(anchor,'<a href="#case-library">'+text(('案例与实践','Cases & practice'),None)+'</a>'+anchor,1)
        p.write_text(h)
    (root/'joyce/assets/operating-proof.css').write_text(CSS)

def apply_corporate(site):
    site=Path(site);shutil.copytree(Path(__file__).parent/'logos',site/'assets/bp-logos',dirs_exist_ok=True)
    (site/'assets/operating-proof.css').write_text(CSS.replace('--proof-accent:#77508b','--proof-accent:#6940ae'))
    for loc in ['zh','en']:
        routes={'index':cases(loc,True)+ai(loc,True)+method(loc,True),'about':cases(loc),'research-agent':ai(loc),'method':method(loc),'decision-os':ai(loc,True),'lab':ai(loc,True)}
        for route,content in routes.items():
            p=site/loc/(route+'.html');h=p.read_text()
            if route=='method':
                # Replace the older abbreviated method explanation, retaining its hero and contact CTA.
                main=re.search(r'<main\b[^>]*>([\s\S]*?)</main>',h)[1]
                hero=re.search(r'<section class="pagehero">[\s\S]*?</section>',main)[0]
                closing=re.search(r'<div class="shell"><section class="closing">[\s\S]*?</section></div>',main)
                h=h.replace(main,hero+content+(closing[0] if closing else ''))
                h=h.replace('</head>','<link rel="stylesheet" href="../assets/operating-proof.css?v='+VERSION+'"></head>',1)
            else:
                closing_anchor='<div class="shell"><section class="closing">'
                h=inject(h,content,'../assets/operating-proof.css',closing_anchor if h.count(closing_anchor)==1 else None)
            p.write_text(h)
        # Visible contextual wayfinding from the homepage without crowding global nav.
        p=site/loc/'index.html';h=p.read_text();nav='<nav class="proof-entry" aria-label="'+('案例与方法' if loc=='zh' else 'Cases and methods')+'"><a href="#case-library">'+text(('经营案例','Operating cases'),loc)+'</a><a href="#ai-practice">'+text(('AI实践复盘','AI practice'),loc)+'</a><a href="method.html#joyce-method">Joyce Method</a></nav>'
        h=re.sub(r'(<main\b[^>]*>)',lambda m:m[1]+nav,h,count=1);p.write_text(h)
    with (site/'assets/operating-proof.css').open('a') as f:f.write('.proof-entry{display:flex;justify-content:center;flex-wrap:wrap;gap:12px 26px;padding:16px 20px;background:#fff;border-bottom:1px solid #eee7f5;font-size:14px;font-weight:700}.proof-entry a{color:#6940ae;text-decoration:underline;text-underline-offset:4px}')

from kpi_content import result_cases, ai_results, logos, CSS as KPI_CSS
CSS+=KPI_CSS
def cases(loc=None,compact=False):
    return result_cases(loc,compact,section)+career_cases(loc,compact)+logos(loc,section)
