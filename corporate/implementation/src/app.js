(()=>{
/* GGC shared interactions. No analytics, subscriptions or implicit data submission. */
'use strict';
const lang = document.documentElement.lang.startsWith('zh') ? 'zh' : 'en';
const t = (zh,en) => lang === 'zh' ? zh : en;
const menu=document.querySelector('[data-menu]'),nav=document.querySelector('[data-nav]');
if(menu && nav){
 const close=()=>{nav.dataset.open='false';menu.setAttribute('aria-expanded','false');};
 menu.addEventListener('click',()=>{const open=nav.dataset.open!=='true';nav.dataset.open=String(open);menu.setAttribute('aria-expanded',String(open));});
 nav.addEventListener('click',e=>{if(e.target.closest('a'))close();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.dataset.open==='true'){close();menu.focus();}});
 window.addEventListener('resize',()=>{if(window.innerWidth>880)close();});
}
// A locale switch keeps the same page and safe referral keys, not entered form data.
document.querySelectorAll('[data-locale]').forEach(a=>a.addEventListener('click',()=>{
 const u=new URL(a.href,location.href),q=new URLSearchParams(location.search);
 for(const key of ['service','track'])if(q.has(key))u.searchParams.set(key,q.get(key));
 a.href=u.toString();
}));
// Actual tab pattern: one tab stop, keyboard navigation, matching panel visibility.
document.querySelectorAll('[role=tablist]').forEach(list=>{
 const tabs=[...list.querySelectorAll('[role=tab]')];
 const activate=tab=>{tabs.forEach(x=>{const active=x===tab;x.setAttribute('aria-selected',String(active));x.tabIndex=active?0:-1;const p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!active;});};
 tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>activate(tab));tab.addEventListener('keydown',e=>{
 let j=i;if(e.key==='ArrowRight')j=(i+1)%tabs.length;else if(e.key==='ArrowLeft')j=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')j=0;else if(e.key==='End')j=tabs.length-1;else return;
 e.preventDefault();activate(tabs[j]);tabs[j].focus();
 });});
});
// Filters use a button group with aria-pressed; they are not pretending to be tabs.
document.querySelectorAll('[data-filter-group]').forEach(group=>{
 const target=document.getElementById(group.dataset.target);if(!target)return;
 const items=[...target.querySelectorAll('[data-type]')],search=document.querySelector('[data-search]'),empty=document.querySelector('[data-empty]');
 let selected='all';
 const filter=()=>{const term=(search?.value||'').trim().toLocaleLowerCase();let n=0;items.forEach(item=>{const visible=(selected==='all'||item.dataset.type===selected)&&(!term||item.textContent.toLocaleLowerCase().includes(term));item.hidden=!visible;if(visible)n++;});if(empty)empty.hidden=n!==0;const c=document.querySelector('[data-result-count]');if(c)c.textContent=t(`显示 ${n} 项`,`${n} items shown`);};
 group.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.filter;group.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));filter();}));
 if(search)search.addEventListener('input',filter);filter();
});
const form=document.querySelector('[data-inquiry]');
if(form){
 const params=new URLSearchParams(location.search),track=params.get('track'),service=params.get('service');
 const allowed=['principal','intelligence','ventures','products','media'];
 if(allowed.includes(track))form.elements.track.value=track;
 if(/^S(0[1-9]|1[0-6])$/.test(service||'')){form.elements.message.value=t(`希望讨论 ${service} 服务。\n`,`I'd like to discuss service ${service}.\n`);form.elements.track.value='principal';}
 form.addEventListener('submit',e=>{
  e.preventDefault();const err=document.getElementById('form-error'),result=document.getElementById('draft-result');
  result.hidden=true;err.textContent='';
  if(!form.reportValidity())return;
  const data=new FormData(form),name=String(data.get('name')||'').trim(),email=String(data.get('email')||'').trim(),company=String(data.get('company')||'').trim(),message=String(data.get('message')||'').trim();
  if(!name||!company||message.length<10){err.textContent=t('请填写姓名、公司和至少10个字符的业务问题。','Enter your name, company and a business question of at least 10 characters.');return;}
  const sel=allowed.includes(String(data.get('track')))?String(data.get('track')):'principal';
  const body=`Name: ${name}\nCompany: ${company}\nReply email: ${email}\nTrack: ${sel}\n\n${message}`;
  const anchor=document.getElementById('open-email');anchor.href=`mailto:minyajing@gmail.com?subject=${encodeURIComponent('GGC · '+sel+' · '+company)}&body=${encodeURIComponent(body)}`;
  // No send/storage has occurred. Only a user click can open the mail client.
  result.hidden=false;result.focus();
 });
}
document.querySelectorAll('[data-demo]').forEach(b=>b.addEventListener('click',()=>{
 if(b.getAttribute('aria-busy')==='true')return;b.setAttribute('aria-busy','true');
 const live=document.querySelector('[data-demo-status]');if(live)live.textContent=t('正在演示按钮状态；没有提交业务信息。','Previewing the button state; no business information is submitted.');
 setTimeout(()=>{b.removeAttribute('aria-busy');if(live)live.textContent=t('演示完成。','Preview complete.');},850);
}));
const surface=document.querySelector('[data-surface]');if(surface)surface.addEventListener('click',()=>{document.querySelectorAll('.sample').forEach(el=>el.classList.toggle('dark'));surface.setAttribute('aria-pressed',String(surface.getAttribute('aria-pressed')!=='true'));});

})();
