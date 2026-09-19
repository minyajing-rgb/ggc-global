'use strict';
(() => {
 const data=JSON.parse(document.getElementById('site-data').textContent);
 const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let lang='en',currency='cny',sector=0,stage=0,selected='S01',lastFocus=null;
 const tr=key=>data.translations[key][lang==='en'?0:1];
 const service=id=>data.services.find(s=>s.ID===id);
 const fee=s=>currency==='cny'?'CNY '+s.fee.toLocaleString('en-US'):'≈ US$ '+Math.round(s.fee/7.2).toLocaleString('en-US');
 const name=s=>s[lang==='en'?'English service':'中文服务'];
 const scope=s=>s[lang==='en'?'Included_scope':'包含范围'];
 const unit=s=>{
   if(lang==='en') return s.Unit.replace('from per project','from / project').replace('from per year','from / year').replace('from per 90 days','from / 90 days').replace('from per half day','from / half day').replace('from per pilot','from / pilot').replace('from per session','from / session');
   const a=s.Unit; if(a.includes('month'))return '每月';if(a.includes('year'))return '起／年';if(a.includes('90 days'))return '起／90天';if(a.includes('half day'))return '起／半天';if(a.includes('pilot'))return '起／试点';if(a.includes('project'))return '起／项目';return (a.includes('from')?'起／':'每')+(a.includes('session')?'次':'项');
 };
 function updateRates(){
  $$('[data-price]').forEach(el=>el.textContent=fee(service(el.dataset.price)));
  $$('[data-unit]').forEach(el=>el.textContent=unit(service(el.dataset.unit)));
  if($('#service-dialog').open)fillDialog(selected);
 }
 function updateSector(i){
  sector=i;const s=data.sectors[i],cn=lang==='zh';
  $('#sector-title').textContent=s[cn?1:0];$('#sector-description').textContent=s[cn?6:5];$('#sector-enquire').dataset.detail=s[7];
  $$('.sector-card').forEach((el,n)=>el.setAttribute('aria-pressed',String(n===i)));
 }
 function updateStage(i){
  stage=i;const s=data.steps[i],cn=lang==='zh';
  $('#stage-number').textContent=String(i+1).padStart(2,'0');$('#stage-heading').textContent=s[cn?3:2];$('#stage-output').textContent=s[cn?5:4];
  $('#stage-panel').setAttribute('aria-labelledby','stage-'+i);
  $$('[data-stage]').forEach((el,n)=>{el.setAttribute('aria-selected',String(n===i));el.tabIndex=n===i?0:-1});
 }
 function renderLanguage(next){
  lang=next==='zh'?'zh':'en';document.documentElement.lang=lang==='zh'?'zh':'en';
  $$('.lang').forEach(el=>{el.classList.toggle('active',el.dataset.lang===lang);el.setAttribute('aria-pressed',String(el.dataset.lang===lang))});
  $$('[data-i18n]').forEach(el=>el.innerHTML=tr(el.dataset.i18n));
  $$('[data-service-name]').forEach(el=>el.textContent=name(service(el.dataset.serviceName)));
  $$('[data-scope]').forEach(el=>el.textContent=scope(service(el.dataset.scope)));
  $$('[data-sector-name]').forEach(el=>el.textContent=data.sectors[+el.dataset.sectorName][lang==='zh'?1:0]);
  $$('[data-sector-tag]').forEach(el=>el.textContent=data.sectors[+el.dataset.sectorTag][lang==='zh'?4:3]);
  $$('[data-stage-name]').forEach(el=>el.textContent=data.steps[+el.dataset.stageName][lang==='zh'?1:0]);
  $$('[data-cap-name]').forEach(el=>{const i=+el.dataset.capName;el.textContent=lang==='zh'?data.caps_cn[i][0]:data.caps[i][0]});
  $$('[data-cap-body]').forEach(el=>{const i=+el.dataset.capBody,c=data.caps[i],cn=data.caps_cn[i];const a=lang==='zh'?cn.slice(1):c.slice(2,5);el.innerHTML=['cap.problem','cap.output','cap.measure'].map((k,j)=>'<p><strong>'+esc(tr(k))+'.</strong> '+esc(a[j])+'</p>').join('')+'<a href="#services">'+esc(c[5])+' →</a>'});
  $$('[data-scenario-name]').forEach(el=>{const i=+el.dataset.scenarioName;el.textContent=lang==='zh'?data.scenarios_cn[i][0]:data.scenarios[i][1]});
  $$('[data-scenario-copy]').forEach(el=>{const i=+el.dataset.scenarioCopy;el.textContent=lang==='zh'?data.scenarios_cn[i][1]:data.scenarios[i][2]});
  $$('[data-scenario-work]').forEach(el=>{const i=+el.dataset.scenarioWork;el.textContent=lang==='zh'?data.scenarios_cn[i][2]:data.scenarios[i][3]});
  [...$('#service-select').options].forEach(o=>o.textContent=o.value+' · '+name(service(o.value)));
  $('.dialog-close').setAttribute('aria-label',tr('modal.close'));
  $('.menu').setAttribute('aria-label',tr($('.menu').getAttribute('aria-expanded')==='true'?'menu.close':'menu.open'));
  document.title=lang==='zh'?'Joyce Mi · GGC全球游戏经营伙伴':'Joyce Mi · Global Game Copilot';
  updateSector(sector);updateStage(stage);updateRates();
  if(!$('#brief-result').hidden)buildBrief();
  try{localStorage.setItem('ggc-language',lang)}catch(e){}
 }
 function fillDialog(id){
  const s=service(id);if(!s)return;selected=id;
  $('#dialog-id').textContent=id+' / GGC';$('#dialog-name').textContent=name(s);$('#dialog-price').textContent=fee(s);$('#dialog-unit').textContent=unit(s);$('#dialog-scope').textContent=scope(s);$('#dialog-capacity').textContent=s.Principal_hours_cap+' '+tr('service.hours');$('#dialog-excluded').textContent=s[lang==='zh'?'excluded_cn':'Exclusions'];
 }
 function closeDialog(){ $('#service-dialog').close();if(lastFocus)lastFocus.focus({preventScroll:true}); }
 document.addEventListener('click',e=>{
  const b=e.target.closest('[data-detail]');if(!b)return;lastFocus=b;fillDialog(b.dataset.detail);$('#service-dialog').showModal();
 });
 $('.dialog-close').addEventListener('click',closeDialog);
 $('#service-dialog').addEventListener('click',e=>{if(e.target!==e.currentTarget)return;const r=e.currentTarget.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog()});
 $('#dialog-enquire').addEventListener('click',()=>{const id=selected;$('#service-dialog').close();$('#service-select').value=id;$('#contact').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});$('#service-select').focus({preventScroll:true})});
 $$('.lang').forEach(el=>el.addEventListener('click',()=>renderLanguage(el.dataset.lang)));
 $$('[data-currency]').forEach(el=>el.addEventListener('click',()=>{currency=el.dataset.currency;$$('[data-currency]').forEach(x=>{x.classList.toggle('active',x===el);x.setAttribute('aria-pressed',String(x===el))});updateRates()}));
 $$('[data-filter]').forEach(el=>el.addEventListener('click',()=>{const f=el.dataset.filter;$$('[data-filter]').forEach(x=>{x.classList.toggle('active',x===el);x.setAttribute('aria-pressed',String(x===el))});$$('.service-card').forEach(x=>x.hidden=f!=='all'&&x.dataset.group!==f);$('#service-count').textContent=$$('.service-card').filter(x=>!x.hidden).length}));
 $$('[data-sector]').forEach(el=>el.addEventListener('click',()=>updateSector(+el.dataset.sector)));
 $$('[data-stage]').forEach(el=>{el.addEventListener('click',()=>updateStage(+el.dataset.stage));el.addEventListener('keydown',e=>{const n=+el.dataset.stage;let target=n;if(e.key==='ArrowRight')target=(n+1)%4;else if(e.key==='ArrowLeft')target=(n+3)%4;else if(e.key==='Home')target=0;else if(e.key==='End')target=3;else return;e.preventDefault();updateStage(target);$('#stage-'+target).focus()})});
 function closeMenu(){ $('#navigation').classList.remove('open');$('.menu').setAttribute('aria-expanded','false');$('.menu').setAttribute('aria-label',tr('menu.open')); }
 $('.menu').addEventListener('click',()=>{const open=$('#navigation').classList.toggle('open');$('.menu').setAttribute('aria-expanded',String(open));$('.menu').setAttribute('aria-label',tr(open?'menu.close':'menu.open'))});
 $$('#navigation a').forEach(el=>el.addEventListener('click',closeMenu));
 document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
 function buildBrief(){
  const v=new FormData($('#intake')),s=service(v.get('service'));
  const en=lang==='en';const lines=en?['Hello Joyce,','','Engagement: '+name(s),'Name: '+v.get('name'),'Company / product: '+v.get('company'),'Email: '+v.get('email'),'Market, platform & stage: '+v.get('stage'),'Decision / KPI: '+v.get('problem'),'Budget / timing: '+v.get('budget'),'','Please confirm scope, fees and availability. No work or booking is confirmed by this enquiry.']:['Joyce您好：','','合作服务：'+name(s),'姓名：'+v.get('name'),'公司／产品：'+v.get('company'),'邮箱：'+v.get('email'),'市场、平台与阶段：'+v.get('stage'),'决策／指标：'+v.get('problem'),'预算与时间：'+v.get('budget'),'','请确认合作范围、费用和时间。本次咨询不代表工作或预约已确认。'];
  const text=lines.join('\n');$('#brief').textContent=text;$('#email-draft').href='mailto:minyajing@gmail.com?subject='+encodeURIComponent((en?'GGC enquiry — ':'GGC合作咨询 — ')+v.get('company'))+'&body='+encodeURIComponent(text);
 }
 $('#intake').addEventListener('submit',e=>{e.preventDefault();if(!e.currentTarget.reportValidity())return;buildBrief();$('#brief-result').hidden=false;$('#brief-result').scrollIntoView({behavior:'smooth',block:'nearest'})});
 $('#copy-brief').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#brief').textContent);$('#copy-brief').textContent=tr('form.copied')}catch(e){$('#copy-brief').textContent=tr('form.fallback');const r=document.createRange();r.selectNodeContents($('#brief'));const s=window.getSelection();s.removeAllRanges();s.addRange(r)}});
 // Evidence link expands its target rather than landing on a closed disclosure.
 $$('a[href="#evidence"]').forEach(a=>a.addEventListener('click',()=>$('#evidence details').open=true));
 let saved='en';try{saved=localStorage.getItem('ggc-language')||'en'}catch(e){}
 const requested=new URLSearchParams(location.search).get('lang');renderLanguage(requested||saved);
 window.__ggcRelease=data.version;
})();
