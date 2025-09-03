// shared.js - helper utilities used by pages
async function postJSON(url, data){ 
  const res = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)});
  return res.ok ? res.json() : Promise.reject(await res.text());
}
function formatINR(n){ return '₹' + Number(n).toLocaleString('en-IN'); }
function showError(el, msg){ el.textContent = msg; el.style.color='crimson'; }
function showOK(el, msg){ el.textContent = msg; el.style.color='green'; }
