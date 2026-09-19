'use strict';
(() => {
 const data=JSON.parse(document.getElementById('site-data').textContent);
 const $=s=>document.querySelector(s);
 const find=id=>data.services.find(s=>s.ID===id);
 const cn=()=>document.documentElement.lang==='zh';
 const text=key=>data.translations[key][cn()?1:0];
 const usd=()=> $('[data-currency="usd"]').getAttribute('aria-pressed')==='true';
 const money=s=>(usd()?'≈ US$ '+Math.round(s.fee/7.2).toLocaleString('en-US'):'CNY '+s.fee.toLocaleString('en-US'));
 const shareStatus=$('#share-status');
 const period=s=>{
  const u=s.Unit;
  for(const [key,en,zh] of [['90 days','90 days','90天'],['half day','half day','半天'],['month','month','月'],['year','year','年'],['pilot','pilot','试点'],['project','project','项目'],['session','session','次']])if(u.includes(key))return cn()?zh:en;
  return cn()?'项':'engagement';
 };
 function refresh(){
  const s=find($('#service-select').value);
  if(s){$('#selection-name').textContent=s[cn()?'中文服务':'English service'];$('#selection-fee').textContent=money(s)+(s.Unit.includes('from')?'+':'')+' / '+period(s);}
  document.querySelectorAll('[data-route-price]').forEach(e=>{const s=find(e.dataset.routePrice);e.textContent=money(s)+(s.Unit.includes('from')?'+':'');});
  const hints=cn()?{stage:'例如：美国 · 手机游戏 · Soft Launch',problem:'描述需要判断的产品问题或经营指标，请勿输入机密资料。',budget:'例如：5–8万元；下月启动'}:{stage:'Example: US · Mobile game · Soft launch',problem:'Describe the product decision or KPI without confidential data.',budget:'Example: CNY 50,000–80,000; next month'};
  for(const [name,value] of Object.entries(hints))$('[name="'+name+'"]').placeholder=value;
 }
 $('#service-select').addEventListener('change',refresh);
 document.addEventListener('click',e=>{if(e.target.closest('[data-currency], [data-lang], #dialog-enquire'))requestAnimationFrame(refresh);});
 new MutationObserver(refresh).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 $('#share-service').addEventListener('click',async()=>{
  const id=$('#dialog-id').textContent.split(' / ')[0];if(!find(id))return;
  const u=new URL('/joyce/',location.href);u.searchParams.set('service',id);u.searchParams.set('lang',cn()?'zh':'en');u.hash='services';
  try{await navigator.clipboard.writeText(u.href);shareStatus.textContent=text('refresh.copied');}
  catch(e){shareStatus.textContent=text('refresh.fallback')+' '+u.href;}
 });
 $('#service-dialog').addEventListener('close',()=>{shareStatus.textContent='';refresh();});
 const next=document.getElementById('navigation');
 document.addEventListener('click',e=>{if(next.classList.contains('open')&&!e.target.closest('.header'))$('.menu').click();});
 const requested=new URLSearchParams(location.search).get('service');
 if(find(requested)){
  $('#service-select').value=requested;
  const card=document.querySelector('.service-card [data-detail="'+requested+'"]');
  if(card)card.click();
 }
 refresh();window.__ggcRefresh= data.version;
})();
