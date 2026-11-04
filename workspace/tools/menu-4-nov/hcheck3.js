// 4 Nov 13:5x: as hcheck2, but images are blocked so image loading cannot change the height; live and new each twice
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const [n,w] of [['observations-for-teachers',1440],['the-mathematics-curriculum',390],['the-practical-life-curriculum-2',1440],['the-prepared-environment',390],['the-role-of-the-adult',1440],['the-sensorial-curriculum',1440],['the-sensorial-curriculum',390]]){const r=[];
 for(const mode of ['live','new','live','new']){const ctx=await b.newContext({viewport:{width:w,height:900}});const p=await ctx.newPage();const h='/'+n+'/';
  await p.route('**/*',x=>x.request().resourceType()==='image'?x.abort():x.continue());
  if(mode==='new')await p.route('https://montessorimentor.co.uk'+h,x=>x.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync('out/'+n+'/index.html')}));
  await p.goto('https://montessorimentor.co.uk'+h,{waitUntil:'load',timeout:90000});await p.waitForTimeout(3000);
  r.push(mode+' '+await p.evaluate(()=>document.documentElement.scrollHeight));await ctx.close();}
 console.log(n,w,r.join(', '));}
await b.close();})();
