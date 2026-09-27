export function showToast(msg){ const el=document.getElementById('toast'); const body=document.getElementById('toastBody'); if(!el||!body) return; body.textContent=msg; new bootstrap.Toast(el,{delay:2000}).show(); }
let __bigToastTimer;
export function showBigToast(message,duration=3500){ const el=document.getElementById('bigToast'); const msgEl=document.getElementById('bigToastMsg'); if(!el||!msgEl) return; msgEl.textContent=message; el.style.display='flex'; clearTimeout(__bigToastTimer); __bigToastTimer=setTimeout(()=>hideBigToast(),duration); }
export function hideBigToast(){ const el=document.getElementById('bigToast'); if(el) el.style.display='none'; }
export function showLoading(msg='Loading…'){ const el=document.getElementById('loadingOverlay'); const m=document.getElementById('loadingMsg'); if(m) m.textContent=msg; if(el) el.style.display='flex'; }
export function hideLoading(){ const el=document.getElementById('loadingOverlay'); if(el) el.style.display='none'; }
