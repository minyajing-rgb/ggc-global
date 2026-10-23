/* Release-only business inquiry. The updates-interest form remains a local draft. */
(()=>{'use strict';
const form=document.querySelector('form[data-live-inquiry]');
if(!form)return;
const endpoint=form.dataset.endpoint;
if(endpoint!=='https://formsubmit.co/ajax/minyajing@gmail.com')return;
const zh=document.documentElement.lang.startsWith('zh');
const button=form.querySelector('button[type="submit"]');
const error=form.querySelector('#form-error');
const result=form.querySelector('#draft-result');
let sending=false;
form.addEventListener('submit',async event=>{
 event.preventDefault();
 event.stopImmediatePropagation(); // Do not run the legacy mail-draft handler.
 if(sending||!form.reportValidity())return;
 const fields=new FormData(form);
 const name=String(fields.get('name')||'').trim();
 const email=String(fields.get('email')||'').trim();
 const company=String(fields.get('company')||'').trim();
 const message=String(fields.get('message')||'').trim();
 const track=String(fields.get('track')||'');
 if(!name||!company||message.length<10||!fields.get('consent'))return;
 if(!['principal','intelligence','ventures','products','media'].includes(track))return;
 const payload={name,email,company,track,message,consent:'accepted',locale:zh?'zh':'en',
  _subject:'GGC website business inquiry',_template:'table',_url:location.origin+location.pathname};
 sending=true;button.disabled=true;button.setAttribute('aria-busy','true');error.textContent='';result.hidden=true;
 const controller=new AbortController();
 const timeout=setTimeout(()=>controller.abort(),15000);
 try{
  const response=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
   body:JSON.stringify(payload),signal:controller.signal});
  const data=await response.json().catch(()=>null);
  if(!response.ok||!data||!(data.success===true||data.success==='true'))throw new Error('Unconfirmed submission');
  form.reset();result.hidden=false;result.focus();
 }catch(_){
  error.textContent=zh?'暂时无法确认是否收到询单。请不要立即重复提交；如需确认，请使用本页邮箱直接联系。':
   'We could not confirm receipt. Please avoid immediately resubmitting; use the email link on this page to check or contact GGC directly.';
  error.tabIndex=-1;error.focus();
 }finally{
  clearTimeout(timeout);sending=false;button.disabled=false;button.removeAttribute('aria-busy');
 }
},true);
})();
