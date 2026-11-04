const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const pages=fs.readFileSync('pages.txt','utf8').trim().split('\n');const out=[];
for(const h of pages){const n=h.replace(/^\/|\/$/g,'')||'home';const file=n==='home'?'out/index.html':'out/'+n+'/index.html';
 for(const w of [1440,390]){const res={};for(const mode of ['live','new']){const ctx=await b.newContext({viewport:{width:w,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  if(mode==='new')await p.route('https://montessorimentor.co.uk'+h,r=>r.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync(file)}));
  try{await p.goto('https://montessorimentor.co.uk'+h,{waitUntil:'load',timeout:60000});}catch(e){errs.push('goto '+e.message.slice(0,60))}
  await p.waitForTimeout(2500);
  const r=await p.evaluate(async()=>{const H=document.documentElement.scrollHeight;const burger=document.querySelector('.nav-toggle,.menu-toggle,button[aria-controls="site-nav"]');if(burger&&getComputedStyle(burger).display!=='none')burger.click();await new Promise(r=>setTimeout(r,300));
   const t=document.querySelector('button[aria-controls="p-resources"]');if(t)t.click();await new Promise(r=>setTimeout(r,400));const pn=document.getElementById('p-resources');
   const links=[...pn.querySelectorAll('a,span')].filter(a=>a.getClientRects().length&&a.getBoundingClientRect().height>0).map(a=>(a.tagName==='A'?a.getAttribute('href'):'np:'+a.textContent)+(a.getAttribute('aria-current')?'*':''));return {H,links:links.join(' ')};});
  res[mode]={...r,errs:errs.length};await ctx.close();}
  const ok=res.new.links==='/books-by-montessori/'+(n==='books-by-montessori'?'*':'')+' /books-of-interest/'+(n==='books-of-interest'?'*':'')+' /picture-books/'+(n==='picture-books'?'*':'')+' /websites/'+(n==='websites'?'*':'')&&res.new.H===res.live.H&&res.new.errs<=res.live.errs;
  out.push([n,w,ok?'OK':'FAULT','height live/new '+res.live.H+'/'+res.new.H,'errors '+res.live.errs+'/'+res.new.errs,'menu: '+res.new.links].join(' | '));console.log(out[out.length-1]);}}
fs.writeFileSync('MENU-RENDER-CHECK.txt',out.join('\n')+'\nRESULT: '+(out.every(l=>l.includes('| OK |'))?'ALL OK':out.filter(l=>!l.includes('| OK |')).length+' FAULTS')+'\n');await b.close();})();
