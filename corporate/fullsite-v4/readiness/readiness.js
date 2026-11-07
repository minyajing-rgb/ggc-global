/* PR11 P0: fail-closed local drafts and keyboard navigation. No network/storage. */
(()=>{'use strict';
const zh=document.documentElement.lang.startsWith('zh');
// This deferred script intentionally runs before the existing app scripts.
// Prevent native GET submission before restoring named controls to the legacy handlers.
document.querySelectorAll('form[data-inquiry],form[data-interest]').forEach(form=>{
 form.addEventListener('submit',e=>e.preventDefault(),true);
 form.querySelectorAll('[data-p0-name]').forEach(el=>{el.name=el.dataset.p0Name;});
});
const enhance=()=>{
 document.querySelectorAll('[data-p0-submit]').forEach(el=>el.disabled=false);
 const service=new URLSearchParams(location.search).get('service')||'';
 const inquiry=document.querySelector('.google-inquiry');
 if(inquiry&&/^S(0[1-9]|1[0-6])$/.test(service)){
  const link=inquiry.querySelector('a.ggc-btn[href]');
  if(link){
   const url=new URL(link.href);
   url.searchParams.set('usp','pp_url');
   url.searchParams.set('entry.2092759400',service==='S01'?'S01 — 战略咨询与经营诊断 / Strategy & operations advisory':service);
   if(service==='S01')url.searchParams.set('entry.627383357','战略咨询与经营诊断 / Strategy & operations advisory');
   link.href=url.toString();
   const note=document.createElement('p');
   note.className='note';
   note.textContent=zh?'已带入服务编号：'+service:'Service code included: '+service;
   link.closest('.actions')?.after(note);
  }
 }
 const menu=document.querySelector('[data-menu]'),nav=document.querySelector('[data-nav]');
 if(menu&&nav){
  const links=()=>[...nav.querySelectorAll('a[href]')];
  menu.addEventListener('keydown',e=>{if(e.key==='Tab'&&!e.shiftKey&&menu.getAttribute('aria-expanded')==='true'){
   e.preventDefault();links()[0]?.focus();
  }});
  nav.addEventListener('keydown',e=>{if(e.key==='Tab'&&e.shiftKey&&e.target===links()[0]&&menu.getAttribute('aria-expanded')==='true'){
   e.preventDefault();menu.focus();
  }});
  nav.addEventListener('focusout',e=>{if(menu.getAttribute('aria-expanded')==='true'&&e.relatedTarget&&e.relatedTarget!==menu&&!nav.contains(e.relatedTarget)){
   nav.dataset.open='false';menu.setAttribute('aria-expanded','false');
  }});
 }
 // Keep non-modal navigation a disclosure, not an incorrectly trapped modal dialog.
 document.querySelectorAll('[data-gallery]').forEach((gallery,g)=>{
  gallery.setAttribute('role','region');gallery.setAttribute('aria-label',zh?'产品说明画廊':'Product information gallery');
  const slides=[...gallery.querySelectorAll('[data-slide]')];
  slides.forEach((slide,i)=>{slide.id=slide.id||`p0-gallery-${g}-${i}`;slide.setAttribute('role','group');slide.setAttribute('aria-label',`${i+1} / ${slides.length}`);});
  gallery.querySelectorAll('[data-slide-to]').forEach((dot,i)=>{dot.setAttribute('aria-controls',slides[i].id);});
  // Native buttons remain tab stops; optional arrows only act on gallery controls.
  gallery.addEventListener('keydown',e=>{
   if(!e.target.closest('.gallery-controls')||!['ArrowLeft','ArrowRight'].includes(e.key))return;
   e.preventDefault();gallery.querySelector(e.key==='ArrowLeft'?'[data-prev]':'[data-next]')?.click();
  });
 });
 document.querySelectorAll('#draft-result,[data-interest-result]').forEach(result=>{result.setAttribute('aria-live','polite');});
 // Invalidate a previously prepared mail link when the corresponding input changes.
 document.querySelectorAll('form[data-inquiry],form[data-interest]').forEach(form=>{
  const result=form.querySelector('#draft-result,[data-interest-result]');
  const link=form.querySelector('#open-email,[data-interest-mail]');
  form.addEventListener('input',()=>{if(result)result.hidden=true;if(link)link.removeAttribute('href');});
  form.addEventListener('change',()=>{if(result)result.hidden=true;if(link)link.removeAttribute('href');});
 });
 // The legacy handler keeps only service/track keys. Validate their values as well.
 document.querySelectorAll('[data-locale]').forEach(link=>link.addEventListener('click',()=>{
  const u=new URL(link.href,location.href);
  if(!/^S(0[1-9]|1[0-6])$/.test(u.searchParams.get('service')||''))u.searchParams.delete('service');
  if(!['principal','intelligence','ventures','products','media'].includes(u.searchParams.get('track')))u.searchParams.delete('track');
  link.href=u.toString();
 }));
};
if(document.readyState!=='complete')document.addEventListener('DOMContentLoaded',enhance,{once:true});else enhance();
})();
