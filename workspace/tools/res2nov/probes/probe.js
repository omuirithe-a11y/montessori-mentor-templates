const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const [root,page_,mode]=process.argv.slice(2);
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);fs.readFile(f,(e,d)=>{if(e){r.statusCode=404;r.end();return;}r.setHeader('content-type',{'.html':'text/html','.jpg':'image/jpeg','.png':'image/png'}[path.extname(f)]||'application/octet-stream');r.end(d);});}).listen(0,async()=>{
 const b=await chromium.launch();const url=`http://127.0.0.1:${srv.address().port}/${page_}/`;
 for(const w of [360,389,390,430,640,641,768,830,831,1440]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(2000);
  const r=await p.evaluate(()=>{const o={};const f=document.querySelector('main .mm-initial');if(f){const fr=f.getBoundingClientRect(),t=f.nextElementSibling,tr=document.createRange();tr.selectNodeContents(t);const first=[...tr.getClientRects()][0];o.initial={float:getComputedStyle(f).float,w:Math.round(fr.width),textLeft:Math.round(first.left),textW:Math.round(t.getBoundingClientRect().right-first.left)};}
   const ps=[...document.querySelectorAll('main p.res-desc, main p')].slice(0,400);o.justified=ps.filter(x=>getComputedStyle(x).textAlign==='justify').length;
   const lis=[...document.querySelectorAll('.toc li')];if(lis.length){const ys=lis.map(l=>l.getBoundingClientRect().top);o.tocSteps=ys.slice(1).map((y,i)=>Math.round(y-ys[i]));}
   o.sw=document.documentElement.scrollWidth;return o;});
  console.log(w,JSON.stringify(r));await p.close();}
 await b.close();srv.close();});
