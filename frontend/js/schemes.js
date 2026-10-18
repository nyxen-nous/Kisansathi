/* Source text stays text: never inject upstream HTML into the DOM. */
const schemeForm = document.getElementById('schemeForm');
const schemeResults = document.getElementById('schemeResults');
const schemeStatus = document.getElementById('schemeStatus');
const searchButton = document.getElementById('searchButton');
let schemeData = null;
let schemeBusy = false;
let schemeError = null;
const SCHEME_STATES = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu and Kashmir','Ladakh','Chandigarh','Puducherry','Andaman and Nicobar Islands','Lakshadweep','Dadra and Nagar Haveli and Daman and Diu'];
function schemeStateOptions() {
  const select = document.getElementById('state');
  const selected = select.value || 'Punjab';
  select.replaceChildren(...SCHEME_STATES.map(s => el('option', {value:s, text:stateName(s)})));
  select.value = selected;
}
function safeSource(url) {
  try {
    const u = new URL(url);
    const host = u.hostname.toLowerCase();
    const approvedDomain = host.endsWith('.gov.in') || host.endsWith('.nic.in');
    return u.protocol === 'https:' && !u.username && !u.password && (!u.port || u.port === '443') && approvedDomain;
  } catch (_) { return false; }
}
function renderSchemes() {
  searchButton.disabled = schemeBusy;
  searchButton.textContent = t(schemeBusy ? 'sc_searching' : 'sc_search');
  schemeStatus.replaceChildren();
  schemeResults.replaceChildren();
  if (schemeBusy) { showNotice(schemeStatus,'info',t('sc_searching')); return; }
  if (schemeError) { showNotice(schemeStatus,'error',t(schemeError)); return; }
  if (!schemeData) return;
  if (!schemeData.results.length) { showNotice(schemeStatus,'info',t('sc_empty')); return; }
  showNotice(schemeStatus,schemeData.partial ? 'warn' : 'info',t(schemeData.partial ? 'sc_partial' : 'sc_provider'));
  for (const r of schemeData.results) {
    const card = el('article',{class:'panel scheme-card'},el('h2',{text:r.title}));
    card.append(el('p',{class:'scheme-meta',text:t(r.state_mentioned ? 'sc_state_mentioned':'sc_state_unknown')}));
    if (r.past_period) card.append(el('p',{class:'notice warn',text:t('sc_old')}));
    if (r.status !== 'extracted') card.append(el('p',{text:t('sc_unavailable')}));
    else {
      for (const key of ['benefits','eligibility','documents','application','period']) {
        card.append(el('details',{},el('summary',{text:t('sc_'+key)}),el('p',{class:'scheme-excerpt',text:r.sections[key] || t('sc_missing')})));
      }
      card.append(el('details',{},el('summary',{text:t('sc_excerpt')}),el('p',{class:'scheme-excerpt',text:r.excerpt})));
    }
    if (safeSource(r.url)) card.append(el('a',{class:'btn btn-ghost',href:r.url,target:'_blank',rel:'noopener noreferrer',text:t('sc_source')}));
    card.append(el('p',{class:'scheme-meta',text:t('sc_retrieved')+': '+new Date(r.retrieved_at).toLocaleString(getLang()==='hi'?'hi-IN':'en-IN')}));
    schemeResults.append(card);
  }
}
schemeForm.addEventListener('submit',async event => {
  event.preventDefault(); if (schemeBusy) return;
  schemeBusy=true; schemeError=null; schemeData=null; renderSchemes();
  const abort = new AbortController(); const timer=setTimeout(()=>abort.abort(),90000);
  try {
    const res=await fetch(API_BASE+'/api/schemes/search',{method:'POST',headers:{'Content-Type':'application/json'},signal:abort.signal,body:JSON.stringify({state:document.getElementById('state').value,category:document.getElementById('category').value})});
    const data=await res.json();
    if (!res.ok) { schemeError=['schemes_not_configured','schemes_busy','schemes_unavailable'].includes(data.detail)?data.detail:(res.status===429?'schemes_busy':'schemes_unavailable'); }
    else schemeData=data;
  } catch (_) { schemeError='schemes_unavailable'; }
  finally { clearTimeout(timer); schemeBusy=false; renderSchemes(); }
});
document.addEventListener('langchange',()=>{schemeStateOptions();renderSchemes();});
schemeStateOptions(); renderSchemes();
