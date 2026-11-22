import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  LayoutDashboard, Table2, Columns3, CalendarDays, GanttChart, AlertTriangle,
  MessageSquare, Plus, Search, ChevronDown, ChevronRight, X, Check, ExternalLink,
  Mic, Download, Upload, RefreshCw, Target, Clock3, FolderOpen, Archive,
  Menu, ArrowUpRight, ShieldCheck, Settings2, CalendarCheck2, GripVertical,
  ArrowLeft, ArrowRight, Layers, BriefcaseBusiness, BookOpen, Sparkles,
  CheckCircle2, ListFilter, LockKeyhole, CircleHelp, Trash2, CircleDot,
} from 'lucide-react';
import { useAuth } from '@/lib/AuthContext';
import { base44 } from '@/api/base44Client';
import './PMWorkbench.css';

const STATUS = ['待执行', '进行中', '待外部', '阻塞', '已完成'];
const PRIORITY = ['P0', 'P1', 'P2'];
const AREAS = [
  { name: 'Bunny / AI身心灵', color: '#f21b91', icon: Sparkles },
  { name: '游戏项目推荐', color: '#3578f6', icon: Layers },
  { name: 'GGC商务与BD', color: '#754ade', icon: BriefcaseBusiness },
  { name: '国际PR与合作', color: '#29b2cb', icon: Target },
  { name: '出版与内容', color: '#be68dc', icon: BookOpen },
  { name: '签证与申报', color: '#e29a27', icon: CalendarCheck2 },
  { name: '其他自有事项', color: '#8190a8', icon: FolderOpen },
];
const DEFAULT_AREA = AREAS[0].name;
const NAV = [
  ['overview', '总览', LayoutDashboard],
  ['table', '主表', Table2],
  ['kanban', '看板', Columns3],
  ['timeline', '时间线', GanttChart],
  ['calendar', '日历', CalendarDays],
  ['blocked', '阻塞中心', AlertTriangle],
  ['activity', '反馈记录', MessageSquare],
];
const todayISO = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
const iso = (d) => { const x = new Date(d); return Number.isNaN(x.getTime()) ? '' : new Date(x.getTime() - x.getTimezoneOffset() * 60000).toISOString().slice(0, 10); };
const plusDays = (base, days) => { const d = new Date(`${base}T12:00:00`); d.setDate(d.getDate() + days); return iso(d); };
const dateLabel = (x) => x ? `${x.slice(5, 7)}/${x.slice(8, 10)}` : '未设日期';
const formatTime = (v) => { if (!v) return '无日期'; const d = new Date(v); return Number.isNaN(d.getTime()) ? v : d.toLocaleString('zh-CN', {month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit'}); };
const colorFor = (name) => AREAS.find(a => a.name === name)?.color || '#8190a8';
const cleanText = (v) => String(v ?? '').trim();
const safeUrl = (u) => { try { const v = new URL(u); return ['https:', 'http:'].includes(v.protocol) ? v.href : ''; } catch { return ''; } };
const isExcluded = (text) => /spark\s*pro|fortune\s*isle|neon\s*dots|yarn\s*fever|pixel\s*yarn/i.test(text);
const normalizeStatus = (s) => {
  const v = cleanText(s).toLowerCase();
  if (['done','complete','completed','已完成','finished','完成'].includes(v)) return '已完成';
  if (['blocked','stuck','阻塞','卡住'].includes(v)) return '阻塞';
  if (['waiting','待外部','pending response','awaiting reply','待回复','等待'].includes(v)) return '待外部';
  if (['in progress','working on it','进行中','active','doing','处理中'].includes(v)) return '进行中';
  return '待执行';
};
const areaFor = (s) => {
  const v = cleanText(s).toLowerCase();
  if (/bunny|saga|oracle|身心灵|抽卡|ai灵性/.test(v)) return AREAS[0].name;
  if (/游戏项目|游戏推荐|sourcing|game project|cp推荐|发行项目推荐/.test(v)) return AREAS[1].name;
  if (/bd|business|咨询|客户|成交|tob|商务|年框|合作伙伴/.test(v)) return AREAS[2].name;
  if (/pr|奖项|会议|演讲|高校|协会|4yfn|gdc|gamescom|w icx/.test(v)) return AREAS[3].name;
  if (/书|kdp|出版|文章|内容/.test(v)) return AREAS[4].name;
  if (/签证|申报|visa|cyberport/.test(v)) return AREAS[5].name;
  return AREAS[6].name;
};
const fromRecord = (r, n = 0) => {
  const title = cleanText(r.title || r.Task || r.task || r.name || r['事项'] || r['任务'] || r['工作事项']);
  const key = cleanText(r.external_id || r.ID || r.task_id || r.key || r.no || r['任务编号'] || r['原编号'] || r.id || '');
  const source = cleanText(r.source_url || r['Evidence / Source'] || r['入口'] || r['来源链接'] || r['来源'] || '');
  const projectRaw = cleanText(r.project || r.Workstream || r.workstream || r['业务线'] || r['项目'] || '');
  const project = AREAS.some(a => a.name === projectRaw) ? projectRaw : areaFor(`${title} ${projectRaw}`);
  return {
    external_id: key, title, project,
    group_name: cleanText(r.group_name || r.group || r['分组'] || '本周重点'),
    status: normalizeStatus(r.status || r.Status || r['当前状态'] || r['状态']),
    priority: PRIORITY.includes(cleanText(r.priority || r.Priority || r['优先级']).toUpperCase()) ? cleanText(r.priority || r.Priority || r['优先级']).toUpperCase() : 'P1',
    owner: cleanText(r.owner || r['Owner role'] || r['负责人'] || r.assignee || ''),
    start_date: cleanText(r.start_date || r.Start || r['开始日期']).slice(0, 10),
    due_date: cleanText(r.due_date || r.Due || r['计划日期'] || r['截止日期']).slice(0, 10),
    acceptance: cleanText(r.acceptance || r['Acceptance criteria'] || r['完成条件'] || r['下一步／完成条件']),
    blocker: cleanText(r.blocker || r['Blocker / Dependency'] || r['阻塞'] || r['阻塞点']),
    evidence_url: safeUrl(r.evidence_url || source),
    source_url: safeUrl(source),
    note: cleanText(r.note || r['备注'] || ''),
    dependency: cleanText(r.dependency || ''),
    tags: Array.isArray(r.tags) ? r.tags : [],
    progress: Number(r.progress || 0),
    archived: Boolean(r.archived),
    origin: cleanText(r.origin || 'import'),
    position: Number(r.position || n),
  };
};
const parseCSV = (raw) => {
  const rows = []; let row = []; let value = ''; let quoted = false;
  for (let i = 0; i < raw.length; i++) {
    const ch = raw[i];
    if (quoted) { if (ch === '"' && raw[i+1] === '"') {value += '"'; i++;} else if (ch === '"') quoted = false; else value += ch; }
    else if (ch === '"') quoted = true;
    else if (ch === ',') { row.push(value); value = ''; }
    else if (ch === '\n' || ch === '\r') { if (ch === '\r' && raw[i+1] === '\n') i++; row.push(value); if (row.some(Boolean)) rows.push(row); row = []; value = ''; }
    else value += ch;
  }
  row.push(value); if (row.some(Boolean)) rows.push(row);
  const header = rows.shift()?.map(v => v.replace(/^\uFEFF/, '').trim()) || [];
  return rows.map(r => Object.fromEntries(header.map((key, i) => [key, r[i] ?? ''])));
};
const CSV_COLS = ['ID','Priority','Workstream','Task','Owner role','Start','Due','Status','Acceptance criteria','Blocker / Dependency','Evidence / Source'];
const quoteCSV = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const csvExport = (records) => [CSV_COLS.join(','), ...records.map(r => [r.external_id,r.priority,r.project,r.title,r.owner,r.start_date,r.due_date,r.status,r.acceptance,r.blocker,r.evidence_url || r.source_url].map(quoteCSV).join(','))].join('\n') + '\n';
const download = (name, contents, mime) => { const blob = new Blob([contents], {type: mime}); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = name; document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 500); };
const iconSize = 18;
const Badge = ({type, children, compact = false}) => <span className={`pm-badge pm-badge-${(type||'default').replace(/\W/g,'')} ${compact?'pm-badge-compact':''}`}>{children}</span>;
const Avatar = ({name}) => <span className="pm-avatar" title={name || '待指定'}>{(name || '?').slice(0, 2).toUpperCase()}</span>;
const emptyTask = () => ({external_id:'',title:'',project:DEFAULT_AREA,group_name:'本周重点',priority:'P1',status:'待执行',owner:'',start_date:todayISO(),due_date:'',blocker:'',acceptance:'',evidence_url:'',source_url:'',note:'',dependency:'',tags:[],origin:'manual',archived:false,position:0});

export default function PMWorkbench() {
  const {user,isAuthenticated,isLoadingAuth,authError,navigateToLogin,logout} = useAuth();
  const [tasks,setTasks] = useState([]), [events,setEvents] = useState([]);
  const [loading,setLoading] = useState(false), [error,setError] = useState('');
  const [view,setView] = useState('overview'), [mobileMenu,setMobileMenu] = useState(false);
  const [project,setProject] = useState('全部项目'), [search,setSearch] = useState(''), [statusFilter,setStatusFilter] = useState('全部'), [priorityFilter,setPriorityFilter] = useState('全部');
  const [selected,setSelected] = useState(null), [draft,setDraft] = useState(emptyTask()), [editing,setEditing] = useState(false), [saving,setSaving] = useState(false);
  const [message,setMessage] = useState(''), [comment,setComment] = useState(''), [dragId,setDragId] = useState(null);
  const [expandedGroups,setExpandedGroups] = useState({}), [calendarCursor,setCalendarCursor] = useState(new Date());
  const [importRows,setImportRows] = useState([]), [importName,setImportName] = useState(''), [importProgress,setImportProgress] = useState(''), [importModal,setImportModal] = useState(false);
  const [showFilters,setShowFilters] = useState(false), [includeArchived,setIncludeArchived] = useState(false);
  const fileInput = useRef(null);
  const [speechAvailable,setSpeechAvailable] = useState(false);
  useEffect(() => {setSpeechAvailable(typeof window !== 'undefined' && Boolean(window.SpeechRecognition || window.webkitSpeechRecognition));}, []);
  const announce = (msg) => { setMessage(msg); setTimeout(() => setMessage(''), 4200); };

  const refresh = useCallback(async () => {
    if (!isAuthenticated || user?.role !== 'admin') return;
    setLoading(true);setError('');
    try {
      const [rawTasks,rawEvents] = await Promise.all([
        base44.entities.PMTask.list('-updated_date', 1000),
        base44.entities.PMEvent.list('-created_date', 500),
      ]);
      setTasks(Array.isArray(rawTasks) ? rawTasks : rawTasks?.data || []);
      setEvents(Array.isArray(rawEvents) ? rawEvents : rawEvents?.data || []);
    } catch (e) {setError(`云端读取未成功：${e?.message || '请检查登录/权限'}`);}
    finally {setLoading(false);}
  },[isAuthenticated,user?.role]);
  useEffect(()=>{refresh();},[refresh]);

  const visible = useMemo(()=>tasks.filter(t => {
    if (!includeArchived && t.archived) return false;
    if (isExcluded(`${t.project} ${t.title}`)) return false;
    if (project !== '全部项目' && (t.project || DEFAULT_AREA) !== project) return false;
    if (statusFilter !== '全部' && t.status !== statusFilter) return false;
    if (priorityFilter !== '全部' && t.priority !== priorityFilter) return false;
    if (search && !`${t.external_id} ${t.title} ${t.owner} ${t.project} ${t.blocker} ${t.acceptance}`.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  }),[tasks,project,statusFilter,priorityFilter,search,includeArchived]);
  const active = useMemo(()=>tasks.filter(t => !t.archived && !isExcluded(`${t.project} ${t.title}`)),[tasks]);
  const metrics = useMemo(()=>{
    const due = todayISO(); const x = active;
    return {
      total:x.length, p0:x.filter(t=>t.priority==='P0' && t.status!=='已完成').length,
      blocked:x.filter(t=>t.status==='阻塞').length,
      waiting:x.filter(t=>t.status==='待外部').length,
      done:x.filter(t=>t.status==='已完成').length,
      overdue:x.filter(t=>t.due_date && t.due_date<due && t.status!=='已完成').length,
      thisWeek:x.filter(t=>t.due_date && t.due_date>=due && t.due_date<=plusDays(due,7) && t.status!=='已完成').length,
    };
  },[active]);
  const groups = useMemo(()=>{
    const keyed = new Map();
    for(const task of visible){const key = task.project || DEFAULT_AREA; if(!keyed.has(key))keyed.set(key,[]);keyed.get(key).push(task);}
    return [...keyed.entries()].sort((a,b)=>AREAS.findIndex(x=>x.name===a[0])-AREAS.findIndex(x=>x.name===b[0]));
  },[visible]);

  const log = async (task, kind, body, from = '', to = '') => {
    try {const a = await base44.entities.PMEvent.create({task_key:task.external_id,kind,body,actor:user?.full_name||user?.name||'Joyce',from_value:String(from||''),to_value:String(to||''),created_at:new Date().toISOString()});setEvents(prev=>[a,...prev]);} catch(e){announce(`任务已保存，记录写入失败：${e?.message || '未知错误'}`);}
  };
  const update = async (task, changes, kind='edit') => {
    if (!task?.id) return;
    const updated = {...changes,last_action_at:new Date().toISOString()};
    const before = task; setTasks(t=>t.map(x=>x.id===task.id?{...x,...updated}:x));
    try {
      const next=await base44.entities.PMTask.update(task.id,updated);
      setTasks(t=>t.map(x=>x.id===task.id?{...x,...next}:x));
      if(changes.status && changes.status!==before.status)await log(task,'status',`状态：${before.status} → ${changes.status}`,before.status,changes.status);
      else if(changes.blocker!==undefined && changes.blocker!==before.blocker)await log(task,'blocker',changes.blocker||'阻塞已清除',before.blocker,changes.blocker);
      else if(kind==='edit' && changes.priority && changes.priority!==before.priority)await log(task,'edit',`优先级：${before.priority} → ${changes.priority}`,before.priority,changes.priority);
    }catch(e){setTasks(t=>t.map(x=>x.id===task.id?before:x));announce(`未保存：${e?.message || '请重试'}`);}
  };
  const openTask = (task=null) => {setSelected(task);setDraft(task?{...task}:emptyTask());setEditing(true);setComment('');};
  const closeTask = () => {setEditing(false);setSelected(null);setComment('');};
  const saveDraft = async (e) => {
    e?.preventDefault?.(); if(!draft.title.trim()) return announce('请填写任务名称');
    setSaving(true);
    const fields=['external_id','title','project','group_name','status','priority','owner','start_date','due_date','acceptance','blocker','dependency','evidence_url','source_url','note','tags','progress','origin','archived','position'];
    const data=Object.fromEntries(fields.map(f=>[f,draft[f]]).filter(([_,v])=>v!==undefined));
    if(!data.external_id)data.external_id=`JPM-${new Date().toISOString().slice(0,10).replaceAll('-','')}-${Math.random().toString(36).slice(2,7).toUpperCase()}`;
    if(tasks.some(t=>t.external_id===data.external_id && t.id!==selected?.id)){setSaving(false);return announce('该原任务编号已存在，不能重复创建');}
    try {
      if(selected?.id){const result=await base44.entities.PMTask.update(selected.id,{...data,last_action_at:new Date().toISOString()});setTasks(t=>t.map(x=>x.id===selected.id?{...x,...result}:x));if(selected.status!==data.status)await log(selected,'status',`状态：${selected.status} → ${data.status}`,selected.status,data.status);else await log(selected,'edit','更新任务字段');}
      else {const result=await base44.entities.PMTask.create({...data,last_action_at:new Date().toISOString()});setTasks(t=>[result,...t]);await log(result,'edit','新增到工作台');}
      closeTask(); announce('已保存到云端');
    }catch(err){announce(`保存失败：${err?.message||'请检查权限'}`);}finally{setSaving(false);}
  };
  const appendComment = async () => {
    if(!selected?.id||!comment.trim())return;
    setSaving(true);await log(selected,'comment',comment.trim());setComment('');setSaving(false);announce('反馈已追加，不改变任务状态');
  };
  const archive = async (task) => {if(!window.confirm(`归档「${task.title}」？任务编号和历史记录会保留。`))return;await update(task,{archived:true});closeTask();announce('已归档，可在设置中显示');};
  const startVoice = () => {
    const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!SR)return announce('当前浏览器不支持语音识别，请使用文本输入');
    try {const rec=new SR();rec.lang='zh-CN';rec.interimResults=false;rec.maxAlternatives=1;rec.onresult=(e)=>{const words=e.results?.[0]?.[0]?.transcript||'';setDraft(v=>({...v,note:[v.note,words].filter(Boolean).join('\n')}));announce('语音转写已追加到备注，保存任务后持久化');};rec.onerror=(e)=>announce(`麦克风未启动：${e.error}`);rec.start();}catch(e){announce(`语音输入未启动：${e.message}`);}
  };
  const handleFile=async(file)=>{
    if(!file)return;setImportName(file.name);setImportProgress('正在解析文件…');
    try {
      const raw=await file.text();let rows;
      if(file.name.toLowerCase().endsWith('.json')){const p=JSON.parse(raw);rows=Array.isArray(p)?p:Array.isArray(p.tasks)?p.tasks:Array.isArray(p.items)?p.items:Array.isArray(p.records)?p.records:[];}
      else rows=parseCSV(raw);
      const normalized=rows.map((r,i)=>fromRecord(r,i)).filter(x=>x.title&&x.external_id&&!isExcluded(`${x.title} ${x.project}`));
      const ids=new Set();const unique=normalized.filter(r=>{if(ids.has(r.external_id))return false;ids.add(r.external_id);return true;});
      setImportRows(unique);setImportProgress(`已解析 ${rows.length} 行，符合范围且有编号 ${unique.length} 行；正式确认前不会改动云端。`);
    }catch(e){setImportProgress(`无法解析：${e?.message||'请用UTF-8 CSV或JSON'}`);setImportRows([]);}
  };
  const importSummary=useMemo(()=>{
    const currentIds=new Set(active.map(t=>t.external_id));const titles=new Set(active.map(t=>`${t.project}__${t.title.toLowerCase().trim()}`));
    return {new:importRows.filter(t=>!currentIds.has(t.external_id)&&!titles.has(`${t.project}__${t.title.toLowerCase().trim()}`)).length,update:importRows.filter(t=>currentIds.has(t.external_id)).length,similar:importRows.filter(t=>!currentIds.has(t.external_id)&&titles.has(`${t.project}__${t.title.toLowerCase().trim()}`)).length};
  },[importRows,active]);
  const importConfirm=async()=>{
    if(!importRows.length)return;setSaving(true);
    let made=0,modified=0,skipped=0,fail=0;
    const byId=new Map(tasks.map(t=>[t.external_id,t]));const byTitle=new Map(tasks.map(t=>[`${t.project}__${t.title.toLowerCase().trim()}`,t]));
    for(const input of importRows){
      const same=byId.get(input.external_id),near=byTitle.get(`${input.project}__${input.title.toLowerCase().trim()}`);
      if(near&&!same){skipped++;continue;}
      try {
        if(same){const data={...input,origin:same.origin||'import'};delete data.external_id;await base44.entities.PMTask.update(same.id,data);modified++;}
        else {const created=await base44.entities.PMTask.create(input);byId.set(input.external_id,created);made++;}
      }catch(e){fail++;}
      setImportProgress(`云端写入：新增 ${made} · 更新 ${modified} · 跳过 ${skipped} · 失败 ${fail}`);
    }
    setSaving(false);setImportRows([]);await refresh();announce(`已提交：新增${made}、更新${modified}、跳过${skipped}、失败${fail}`);
    if(!fail)setImportModal(false);
  };
  const exportData=(format)=>{
    const records=active;
    if(format==='csv')download(`JOYCE_PM_${todayISO()}.csv`,csvExport(records),'text/csv;charset=utf-8');
    else download(`JOYCE_PM_BACKUP_${todayISO()}.json`,JSON.stringify({schema:'joyce-pm-v2',exported_at:new Date().toISOString(),tasks:records,events},null,2),'application/json;charset=utf-8');
  };
  const navTo=(v)=>{setView(v);setMobileMenu(false);};
  if(isLoadingAuth)return <div className="pm-auth-page"><span className="pm-spinner"/><h2>正在核验私人工作区访问权限</h2><p>PRIVATE WORKSPACE · JOYCE PM</p></div>;
  if(!isAuthenticated)return <div className="pm-auth-page"><div className="pm-auth-logo">J<span>✳</span></div><h1>Joyce PM</h1><p>你的独立任务工作台 · 对标 monday 的实用交互</p><p className="pm-auth-note">云端任务仅授权管理员可读取。旧版数据没有被覆盖。</p><button className="pm-primary" onClick={navigateToLogin}><LockKeyhole size={18}/> 登录私人工作台</button>{authError&&<small>{authError.message}</small>}</div>;
  if(user?.role!=='admin')return <div className="pm-auth-page"><LockKeyhole size={38}/><h2>仅管理员可访问</h2><p>当前账号没有任务数据读写权限。请使用该应用的所有者账号登录。</p><button className="pm-primary" onClick={logout}>切换账号</button></div>;
  return <div className="pm-app">
    {mobileMenu&&<button className="pm-scrim" aria-label="关闭菜单" onClick={()=>setMobileMenu(false)}/>}
    <aside className={`pm-sidebar ${mobileMenu?'pm-sidebar-open':''}`}>
      <div className="pm-brand"><span className="pm-brand-mark">J✳</span><span><strong>JOYCE <em>PM</em></strong><small>THE WORK OPERATING SYSTEM</small></span></div>
      <div className="pm-workspace"><span className="pm-workspace-badge">J</span><span><b>Joyce 私人工作区</b><small>OWNER ONLY · 云端持久化</small></span><ChevronDown size={16}/></div>
      <div className="pm-nav-label">WORKSPACE / 工作区</div>
      <nav className="pm-nav">{NAV.map(([key,label,Icon])=><button key={key} className={view===key?'active':''} onClick={()=>navTo(key)}><Icon size={19}/><span>{label}</span>{key==='blocked'&&metrics.blocked>0&&<i>{metrics.blocked}</i>}</button>)}</nav>
      <div className="pm-nav-label pm-nav-label-projects">BOARDS / 业务板块</div>
      <nav className="pm-nav pm-project-nav"><button className={project==='全部项目'?'active':''} onClick={()=>{setProject('全部项目');navTo('table');}}><Layers size={17}/><span>全部项目</span><i>{active.length}</i></button>{AREAS.map(a=>{const Icon=a.icon;const count=active.filter(t=>t.project===a.name).length;return <button key={a.name} className={project===a.name?'active':''} onClick={()=>{setProject(a.name);navTo('table');}}><span className="pm-project-dot" style={{background:a.color}}/><span>{a.name}</span><i>{count}</i></button>})}</nav>
      <div className="pm-side-bottom"><button onClick={()=>setImportModal(true)}><Upload size={17}/> 导入原任务</button><button onClick={()=>exportData('json')}><Download size={17}/> 完整备份</button><span className="pm-server-state"><span/> 云端任务 · 用户私有</span></div>
    </aside>

    <div className="pm-shell">
      <header className="pm-topbar"><button className="pm-icon-btn pm-menu" onClick={()=>setMobileMenu(true)} aria-label="展开菜单"><Menu size={21}/></button><span className="pm-breadcrumb">Joyce Workspace <ChevronRight size={14}/> <strong>{NAV.find(x=>x[0]===view)?.[1]||'工作台'}</strong></span><div className="pm-top-actions"><button className="pm-icon-btn" aria-label="刷新云端数据" title="刷新云端数据" onClick={refresh}><RefreshCw size={19} className={loading?'pm-spin':''}/></button><span className="pm-user"><Avatar name={user?.full_name||user?.name||'JY'}/><span>{user?.full_name||user?.name||'Joyce'}</span></span></div></header>
      <div className="pm-content">
        <div className="pm-heading"><div><div className="pm-eyebrow">PRIVATE COMMAND CENTER <span>·</span> GGC × SAGA</div><h1>{view==='overview'?'我的工作台':NAV.find(x=>x[0]===view)?.[1]||'我的工作台'} <span className="pm-heading-star">✳</span></h1><p>从目标到行动，从行动到真实回执。<b>一张任务主表 · 多视图共享</b>。</p></div><button className="pm-primary pm-add" onClick={()=>openTask()}><Plus size={19}/> 新建任务</button></div>
        {error&&<div className="pm-alert"><AlertTriangle size={18}/>{error}<button onClick={refresh}>重试</button></div>}
        <div className="pm-metrics"><button onClick={()=>{setStatusFilter('全部');setView('table');}}><span className="pm-metric-icon violet"><Layers size={21}/></span><small>有效任务</small><strong>{metrics.total}</strong><span>仅按云端记录</span></button><button onClick={()=>{setPriorityFilter('P0');setView('table');}}><span className="pm-metric-icon pink"><Target size={21}/></span><small>当前 P0</small><strong>{metrics.p0}</strong><span>未完成高优先级</span></button><button onClick={()=>setView('blocked')}><span className="pm-metric-icon red"><AlertTriangle size={21}/></span><small>实际阻塞</small><strong>{metrics.blocked}</strong><span>需要解除条件</span></button><button onClick={()=>{setStatusFilter('已完成');setView('table');}}><span className="pm-metric-icon cyan"><CheckCircle2 size={21}/></span><small>已完成</small><strong>{metrics.done}</strong><span>以任务状态为准</span></button></div>
        <section className="pm-board"><div className="pm-board-head"><div><h2>{project==='全部项目'?'全部业务':'业务视图 · '+project}</h2><p>{visible.length} 个匹配事项 · 数据来源于同一云端主表</p></div><div className="pm-tools"><div className="pm-search"><Search size={17}/><input aria-label="搜索任务" placeholder="搜索任务、编号、联系人、阻塞…" value={search} onChange={e=>setSearch(e.target.value)}/>{search&&<button onClick={()=>setSearch('')} aria-label="清除搜索"><X size={14}/></button>}</div><button className={`pm-tool-btn ${showFilters?'selected':''}`} onClick={()=>setShowFilters(x=>!x)}><ListFilter size={17}/> 筛选</button><button className="pm-tool-btn" onClick={()=>setImportModal(true)}><Upload size={17}/> 导入</button><button className="pm-tool-btn" onClick={()=>exportData('csv')}><Download size={17}/> 导出</button></div></div>
          {showFilters&&<div className="pm-filters"><label>板块 <select value={project} onChange={e=>setProject(e.target.value)}><option>全部项目</option>{AREAS.map(a=><option key={a.name}>{a.name}</option>)}</select></label><label>状态 <select value={statusFilter} onChange={e=>setStatusFilter(e.target.value)}><option>全部</option>{STATUS.map(s=><option key={s}>{s}</option>)}</select></label><label>优先级 <select value={priorityFilter} onChange={e=>setPriorityFilter(e.target.value)}><option>全部</option>{PRIORITY.map(s=><option key={s}>{s}</option>)}</select></label><button onClick={()=>{setStatusFilter('全部');setPriorityFilter('全部');setProject('全部项目');setSearch('');}}>重置筛选</button></div>}
          <div className="pm-tabs">{NAV.filter(x=>!['activity'].includes(x[0])).map(([key,label,Icon])=><button key={key} className={view===key?'selected':''} onClick={()=>setView(key)}><Icon size={17}/>{label}</button>)}</div>
          {loading&&!tasks.length?<div className="pm-loading"><span className="pm-spinner"/>正在载入你的任务…</div> : <>
            {view==='overview'&&<Overview tasks={active} onOpen={openTask} onGo={setView} metrics={metrics}/>}
            {view==='table'&&<TaskTable groups={groups} expandedGroups={expandedGroups} setExpandedGroups={setExpandedGroups} onOpen={openTask} onUpdate={update} onAdd={openTask}/>}
            {view==='kanban'&&<Kanban tasks={visible} onOpen={openTask} onUpdate={update} dragId={dragId} setDragId={setDragId}/>}
            {view==='timeline'&&<Timeline tasks={visible} onOpen={openTask}/>}
            {view==='calendar'&&<Calendar tasks={visible} cursor={calendarCursor} setCursor={setCalendarCursor} onOpen={openTask}/>}
            {view==='blocked'&&<Blocked tasks={visible.filter(x=>x.status==='阻塞'||(x.blocker&&x.status!=='已完成'))} onOpen={openTask} onUpdate={update}/>}
            {view==='activity'&&<Activities events={events} tasks={active} onOpen={openTask}/>}
          </>}
        </section>
        <footer className="pm-footer"><span>JOYCE PM · PRIVATE WORK OS</span><span>不连接 monday.com / Jira · 编辑结果写入当前工作台云端数据库</span><button onClick={()=>setIncludeArchived(x=>!x)}>{includeArchived?'隐藏归档':'显示归档'}</button></footer>
      </div>
    </div>

    {editing&&<div className="pm-drawer-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)closeTask();}}><section className="pm-drawer" role="dialog" aria-modal="true" aria-label="任务详情"><div className="pm-drawer-head"><span className="pm-drawer-kicker">{selected?.external_id||'NEW TASK'} · 任务工作台</span><div><button className="pm-icon-btn" title="关闭" onClick={closeTask}><X size={22}/></button></div></div><form onSubmit={saveDraft}><div className="pm-drawer-body"><input className="pm-task-title" value={draft.title} maxLength={255} onChange={e=>setDraft(d=>({...d,title:e.target.value}))} placeholder="输入要交付的工作结果" required/><div className="pm-form-grid"><label>业务板块<select value={draft.project||DEFAULT_AREA} onChange={e=>setDraft(d=>({...d,project:e.target.value}))}>{AREAS.map(a=><option key={a.name}>{a.name}</option>)}</select></label><label>任务分组<input value={draft.group_name||''} onChange={e=>setDraft(d=>({...d,group_name:e.target.value}))}/></label><label>优先级<select value={draft.priority||'P1'} onChange={e=>setDraft(d=>({...d,priority:e.target.value}))}>{PRIORITY.map(s=><option key={s}>{s}</option>)}</select></label><label>状态<select value={draft.status||'待执行'} onChange={e=>setDraft(d=>({...d,status:e.target.value}))}>{STATUS.map(s=><option key={s}>{s}</option>)}</select></label><label>负责人<input value={draft.owner||''} onChange={e=>setDraft(d=>({...d,owner:e.target.value}))} placeholder="角色或姓名"/></label><label>任务编号<input value={draft.external_id||''} disabled={Boolean(selected)} onChange={e=>setDraft(d=>({...d,external_id:e.target.value}))} placeholder="留空自动生成"/></label><label>开始日期<input type="date" value={draft.start_date||''} onChange={e=>setDraft(d=>({...d,start_date:e.target.value}))}/></label><label>截止日期<input type="date" value={draft.due_date||''} onChange={e=>setDraft(d=>({...d,due_date:e.target.value}))}/></label></div><label className="pm-fullfield">验收标准 / Expected Outcome<textarea rows={3} value={draft.acceptance||''} onChange={e=>setDraft(d=>({...d,acceptance:e.target.value}))} placeholder="什么证据说明任务真的做完了？"/></label><label className="pm-fullfield">阻塞项 / Blocker<textarea rows={2} value={draft.blocker||''} onChange={e=>setDraft(d=>({...d,blocker:e.target.value}))} placeholder="缺什么权限、回复、资源或决策？"/></label><label className="pm-fullfield">依赖关系<input value={draft.dependency||''} onChange={e=>setDraft(d=>({...d,dependency:e.target.value}))} placeholder="关联原编号 / 前置事项"/></label><label className="pm-fullfield">证据链接 / GitHub Source<input type="url" value={draft.evidence_url||''} onChange={e=>setDraft(d=>({...d,evidence_url:e.target.value}))} placeholder="https://..."/></label><label className="pm-fullfield">工作备注 <button type="button" onClick={startVoice} className="pm-voice" title="使用浏览器语音输入（需允许麦克风）"><Mic size={14}/> {speechAvailable?'语音输入':'文本输入'}</button><textarea rows={3} value={draft.note||''} onChange={e=>setDraft(d=>({...d,note:e.target.value}))} placeholder="直接记录下一步，或点击语音按钮转写"/></label>
          {selected&&<div className="pm-discussion"><h3><MessageSquare size={18}/> 任务反馈与操作记录</h3><p>反馈追加至该任务，**不会**自动把任务标为完成或向外发送通知。</p><div className="pm-comment-input"><textarea placeholder="给这项工作写反馈 / 复盘 / 需要修改的内容" value={comment} rows={2} onChange={e=>setComment(e.target.value)}/><button type="button" className="pm-primary" onClick={appendComment} disabled={saving||!comment.trim()}><Plus size={16}/> 追加反馈</button></div><div className="pm-event-list">{events.filter(e=>e.task_key===selected.external_id).map(e=><article key={e.id}><Avatar name={e.actor}/><div><b>{e.actor||'Joyce'} <small>· {e.kind==='comment'?'反馈':e.kind==='status'?'状态变更':'操作'}</small></b><p>{e.body}</p><time>{formatTime(e.created_at||e.created_date)}</time></div></article>)}{!events.some(e=>e.task_key===selected.external_id)&&<div className="pm-empty-small">暂无历史评论</div>}</div></div>}
        </div><div className="pm-drawer-footer">{selected&&<button type="button" className="pm-archive" onClick={()=>archive(selected)}><Archive size={16}/> 归档</button>}<button type="button" className="pm-secondary" onClick={closeTask}>取消</button><button type="submit" className="pm-primary" disabled={saving}>{saving?'保存中…':'保存到云端'} <Check size={17}/></button></div></form></section></div>}
    {importModal&&<div className="pm-drawer-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)setImportModal(false)}}><section className="pm-import-modal" role="dialog" aria-modal="true"><div className="pm-import-top"><div><h2>导入原任务 · 不重复编号</h2><p>先预览，再确认，保持原 Task ID 与历史来源。</p></div><button className="pm-icon-btn" onClick={()=>setImportModal(false)}><X size={22}/></button></div><div className="pm-import-guide"><ShieldCheck size={23}/><span>只接受 <b>CSV / JSON</b>。按原编号更新，不重复造任务；同名不同编号将跳过待核。非本工作台范围内的研发项目自动忽略。所有数据默认仅管理员可读写。</span></div><input ref={fileInput} type="file" accept=".csv,.json,text/csv,application/json" hidden onChange={e=>handleFile(e.target.files?.[0])}/><button className="pm-dropzone" onClick={()=>fileInput.current?.click()}><Upload size={31}/><b>{importName||'选择旧站导出的 JSON 或排期 CSV'}</b><span>点击读取文件 · 不会立即保存</span></button>{importProgress&&<p className="pm-import-progress">{importProgress}</p>}{importRows.length>0&&<div className="pm-import-preview"><div className="pm-import-stats"><b>新增 {importSummary.new}</b><b>按编号更新 {importSummary.update}</b><b>同名跳过 {importSummary.similar}</b></div>{importRows.slice(0,8).map(r=><div key={r.external_id}><span>{r.external_id}</span><strong>{r.title}</strong><Badge type={r.priority}>{r.priority}</Badge></div>)}{importRows.length>8&&<small>另有 {importRows.length-8} 条，确认后逐条写入云端。</small>}</div>}<div className="pm-import-footer"><button className="pm-secondary" onClick={()=>exportData('json')}>先备份当前任务</button><button className="pm-primary" disabled={!importRows.length||saving} onClick={importConfirm}>{saving?'正在写入云端…':'确认导入 / 更新'} <ArrowUpRight size={17}/></button></div></section></div>}
    {message&&<div className="pm-toast" role="status"><CircleDot size={17}/>{message}<button onClick={()=>setMessage('')}><X size={15}/></button></div>}
  </div>;
}

function TaskTable({groups,expandedGroups,setExpandedGroups,onOpen,onUpdate,onAdd}) {
  if(!groups.length)return <Empty title="没有匹配的任务" desc="取消筛选，或建立首条任务。" onAdd={onAdd}/>;
  return <div className="pm-table-view">{groups.map(([group,records])=>{const collapsed=expandedGroups[group]===false;return <section className="pm-task-group" key={group}><button className="pm-group-title" onClick={()=>setExpandedGroups(v=>({...v,[group]:collapsed}))} style={{'--group':colorFor(group)}}>{collapsed?<ChevronRight size={21}/>:<ChevronDown size={21}/>}<strong>{group}</strong><span>{records.length} 个任务</span></button>{!collapsed&&<div className="pm-table-scroll"><table className="pm-data-table"><thead><tr><th className="pm-col-task">任务 / Task</th><th>状态</th><th>优先级</th><th>负责人</th><th>计划日期</th><th className="pm-col-blocker">阻塞 / 下一步</th><th>证据</th></tr></thead><tbody>{records.sort((a,b)=>(PRIORITY.indexOf(a.priority)-PRIORITY.indexOf(b.priority))||((a.position||0)-(b.position||0))).map(t=><tr key={t.id} onClick={()=>onOpen(t)}><td className="pm-cell-title"><span className="pm-task-key">{t.external_id}</span><b>{t.title}</b></td><td><select className={`pm-cell-status pm-status-${STATUS.indexOf(t.status)}`} value={t.status||'待执行'} onClick={e=>e.stopPropagation()} onChange={e=>{e.stopPropagation();onUpdate(t,{status:e.target.value},'status')}}>{STATUS.map(s=><option key={s}>{s}</option>)}</select></td><td><select className={`pm-cell-priority pm-priority-${t.priority||'P1'}`} value={t.priority||'P1'} onClick={e=>e.stopPropagation()} onChange={e=>{e.stopPropagation();onUpdate(t,{priority:e.target.value})}}>{PRIORITY.map(p=><option key={p}>{p}</option>)}</select></td><td><div className="pm-owner-cell"><Avatar name={t.owner}/><span>{t.owner||'待指定'}</span></div></td><td><span className={t.due_date&&t.due_date<todayISO()&&t.status!=='已完成'?'pm-overdue':''}>{dateLabel(t.due_date)}</span></td><td><p className="pm-blocker-text">{t.blocker||t.acceptance||'—'}</p></td><td>{safeUrl(t.evidence_url||t.source_url)?<a href={safeUrl(t.evidence_url||t.source_url)} target="_blank" rel="noopener noreferrer" onClick={e=>e.stopPropagation()} aria-label="打开证据"><ExternalLink size={17}/></a>:<span className="pm-muted">待补</span>}</td></tr>)}</tbody></table></div>}</section>})}<button className="pm-add-row" onClick={()=>onAdd()}><Plus size={18}/> 添加任务</button></div>;
}
function Kanban({tasks,onOpen,onUpdate,dragId,setDragId}){
  return <div className="pm-kanban-scroll"><div className="pm-kanban">{STATUS.map((status,i)=>{const list=tasks.filter(t=>t.status===status);return <section className={`pm-kanban-column pm-kanban-${i}`} key={status} onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault();const t=tasks.find(x=>x.id===dragId);if(t&&t.status!==status)onUpdate(t,{status},'status');setDragId(null);}}><header><span className="pm-kanban-dot"/><b>{status}</b><small>{list.length}</small></header><div className="pm-kanban-cards">{list.map(t=><article key={t.id} draggable onDragStart={e=>{setDragId(t.id);e.dataTransfer.effectAllowed='move'}} onDragEnd={()=>setDragId(null)} onClick={()=>onOpen(t)} className="pm-kanban-card"><div className="pm-card-top"><span className="pm-task-key">{t.external_id}</span><Badge type={t.priority}>{t.priority}</Badge></div><h3>{t.title}</h3><span className="pm-card-project"><span style={{background:colorFor(t.project)}}/>{t.project}</span><div className="pm-card-foot"><span><CalendarDays size={14}/>{dateLabel(t.due_date)}</span><Avatar name={t.owner}/></div>{t.blocker&&<p className="pm-card-blocker"><AlertTriangle size={14}/>{t.blocker}</p>}</article>)}{!list.length&&<div className="pm-kanban-empty">拖动任务到此处</div>}</div></section>})}</div></div>;
}
function Timeline({tasks,onOpen}) {
  const start=plusDays(todayISO(),-7);const days=35;const dates=Array.from({length:days},(_,i)=>plusDays(start,i));
  return <div className="pm-timeline-scroll"><div className="pm-timeline" style={{minWidth:1040}}><div className="pm-timeline-heading"><div>任务名称 · 计划周期</div><div className="pm-timeline-days">{dates.map((d,i)=><span key={d} className={d===todayISO()?'today':''}>{i%7===0?d.slice(5):d.slice(8)}</span>)}</div></div>{tasks.filter(t=>t.start_date||t.due_date).slice(0,100).map(t=>{let first=t.start_date||t.due_date;let last=t.due_date||first;let n1=Math.round((new Date(`${first}T12:00:00`)-new Date(`${start}T12:00:00`))/864e5);let n2=Math.round((new Date(`${last}T12:00:00`)-new Date(`${start}T12:00:00`))/864e5);let left=Math.max(0,n1),right=Math.min(days,n2+1);return <button className="pm-timeline-row" key={t.id} onClick={()=>onOpen(t)}><div><span className="pm-task-key">{t.external_id}</span><b>{t.title}</b></div><div className="pm-timeline-track">{dates.map((d,i)=><span key={i} className={d===todayISO()?'today':''}/>)}{right>left&&<div className="pm-timeline-bar" style={{left:`${left/days*100}%`,width:`${Math.max((right-left)/days*100,2.8)}%`,background:colorFor(t.project)}} title={`${first} — ${last}`}/>}</div></button>})}{!tasks.some(t=>t.start_date||t.due_date)&&<div className="pm-empty-small">请在任务详情中设置开始/截止日期。</div>}</div></div>;
}
function Calendar({tasks,cursor,setCursor,onOpen}){
  const year=cursor.getFullYear(),month=cursor.getMonth(),first=new Date(year,month,1),offset=(first.getDay()+6)%7;
  const days=Array.from({length:42},(_,i)=>new Date(year,month,1-offset+i));
  return <div className="pm-calendar"><div className="pm-calendar-top"><h3>{year} 年 {month+1} 月</h3><div><button onClick={()=>setCursor(new Date(year,month-1,1))}><ArrowLeft size={18}/></button><button onClick={()=>setCursor(new Date())}>今天</button><button onClick={()=>setCursor(new Date(year,month+1,1))}><ArrowRight size={18}/></button></div></div><div className="pm-calendar-grid">{['一','二','三','四','五','六','日'].map(w=><div className="pm-calendar-week" key={w}>周{w}</div>)}{days.map((date,i)=>{const d=iso(date),matching=tasks.filter(t=>t.due_date===d);return <div key={i} className={`pm-calendar-day ${date.getMonth()!==month?'other':''} ${d===todayISO()?'today':''}`}><span>{date.getDate()}</span>{matching.slice(0,3).map(t=><button key={t.id} onClick={()=>onOpen(t)} title={t.title} style={{borderLeftColor:colorFor(t.project)}}>{t.title}</button>)}{matching.length>3&&<small>+{matching.length-3} 项</small>}</div>})}</div></div>;
}
function Overview({tasks,onOpen,onGo,metrics}){
 const focus=[...tasks].filter(t=>t.status!=='已完成').sort((a,b)=>PRIORITY.indexOf(a.priority)-PRIORITY.indexOf(b.priority)||String(a.due_date||'9999').localeCompare(String(b.due_date||'9999'))).slice(0,6);
 const areas=AREAS.map(a=>({...a,count:tasks.filter(t=>t.project===a.name).length,blocked:tasks.filter(t=>t.project===a.name&&t.status==='阻塞').length})).filter(a=>a.count>0);
 return <div className="pm-overview"><div className="pm-overview-left"><div className="pm-section-head"><div><h3>🎯 今天最值得推进的任务</h3><p>按照优先级与截止日自动排序，不使用虚构进度百分比。</p></div><button onClick={()=>onGo('table')}>查看全部 <ArrowUpRight size={16}/></button></div>{focus.length?focus.map(t=><button className="pm-focus-row" key={t.id} onClick={()=>onOpen(t)}><span className="pm-focus-dot" style={{background:colorFor(t.project)}}/><div><b>{t.title}</b><span>{t.external_id} · {t.project}</span></div><Badge type={t.priority}>{t.priority}</Badge><span className="pm-focus-due">{dateLabel(t.due_date)}</span><ChevronRight size={17}/></button>):<div className="pm-empty-small">暂无待推进事项。可新建任务或导入已有主表。</div>}</div><div className="pm-overview-right"><div className="pm-mini-panel"><h3>任务分布 <span>BY WORKSTREAM</span></h3>{areas.map(a=><div className="pm-area-row" key={a.name}><span className="pm-area-dot" style={{background:a.color}}/><span>{a.name}</span><b>{a.count}</b><div><i style={{width:`${a.count/Math.max(tasks.length,1)*100}%`,background:a.color}}/></div></div>)}{!areas.length&&<p>暂无云端任务</p>}</div><div className="pm-mini-panel pm-quality-panel"><h3>交付口径</h3><p><CheckCircle2 size={17}/> 只有真实数据与证据才算结果</p><p><AlertTriangle size={17}/> 阻塞必须写明下一步和依赖</p><p><ShieldCheck size={17}/> 私人数据不进入公开分享页</p></div></div></div>;
}
function Blocked({tasks,onOpen,onUpdate}){
 return <div className="pm-blocked-view"><div className="pm-subhead"><AlertTriangle size={19}/><div><b>阻塞中心</b><span>真正需要外部资源、决策或操作才能解开的任务。</span></div></div>{tasks.length?tasks.map(t=><article key={t.id}><div className="pm-blocked-top"><Badge type={t.priority}>{t.priority}</Badge><button onClick={()=>onOpen(t)}>{t.title}</button><span>{t.external_id}</span></div><p>{t.blocker||'尚未写明具体阻塞条件，请补充详情。'}</p><div><span>负责人：{t.owner||'待指定'}</span><span>截止：{dateLabel(t.due_date)}</span><button onClick={()=>onOpen(t)}>补充证据/解决动作 <ArrowUpRight size={16}/></button></div></article>):<div className="pm-empty-small">当前筛选下没有阻塞事项。</div>}</div>;
}
function Activities({events,tasks,onOpen}){
 return <div className="pm-activity-view"><div className="pm-subhead"><MessageSquare size={19}/><div><b>任务反馈日志</b><span>来自实际保存的追加记录，不将讨论自动记为完成。</span></div></div>{events.length?events.map(e=>{const t=tasks.find(x=>x.external_id===e.task_key);return <article key={e.id}><span className="pm-event-icon"><MessageSquare size={17}/></span><div><div><b>{e.actor||'Joyce'}</b><small>{formatTime(e.created_at||e.created_date)}</small></div><button onClick={()=>t&&onOpen(t)}>{e.task_key}{t?` · ${t.title}`:''}</button><p>{e.body}</p></div></article>}):<div className="pm-empty-small">暂无操作记录，编辑任务或留言后在此查看。</div>}</div>;
}
function Empty({title,desc,onAdd}){return <div className="pm-empty"><span>✳</span><h3>{title}</h3><p>{desc}</p><button className="pm-secondary" onClick={()=>onAdd()}>+ 创建首项任务</button></div>}