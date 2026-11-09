const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const EXP=["Essential Elements","Essential Elements Resources","Mixed-Age Groups","Mixed-Age Groups Resources","The Three-Hour Cycle","The Three-Hour Cycle Resources","The Role of The Adult","The Role of The Adult Resources","The Role of the Assistant","The Montessori Materials","The Montessori Materials Resources","The Montessori Materials Sourcing","The Prepared Environment","The Prepared Environment Resources","Essential Characteristics","The Outdoor Environment","Anji Play"].join('|');
const pages=fs.readdirSync('new').filter(f=>f.endsWith('.html')&&f!=='the-prepared-environment.html');let bad=0;
for(const f of pages)for(const w of [1440,390]){const c=await b.newContext({viewport:{width:w,height:900}});await c.route(/^https?:/,r=>r.abort());const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+__dirname+'/new/'+f,{waitUntil:'domcontentloaded'});await p.waitForTimeout(400);
if(w<900){const t=await p.$('button.menu-btn');if(t)await t.click().catch(()=>{});await p.waitForTimeout(300);}
await p.click('button[aria-controls="p-essentialelements"]',{timeout:5000}).catch(e=>errs.push('toggle '+e.message.slice(0,50)));await p.waitForTimeout(400);
const r=await p.evaluate(()=>{const P=document.getElementById('p-essentialelements');const items=[...P.querySelectorAll('li')].map(l=>l.textContent.trim());const vis=P.getBoundingClientRect().height>50;const cols=P.querySelectorAll('.pcol').length;return {items:items.join('|'),vis,cols}});
const ok=r.items===EXP&&r.vis&&r.cols===3&&!errs.length;if(!ok){bad++;console.log(f,w,'FAULT',JSON.stringify(r).slice(0,200),errs.join(';').slice(0,200));}
await c.close();}
console.log(bad?'RESULT: '+bad+' FAULTS':'RESULT: menu right on all '+pages.length+' pages at 1440 and 390');await b.close();})();
