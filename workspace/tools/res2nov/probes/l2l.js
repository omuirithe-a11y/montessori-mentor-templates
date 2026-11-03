// letters-to-letters gaps between consecutive text blocks in main, at one width (default 1440)
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const [root,slug,W]=process.argv.slice(2);const width=+(W||1440);
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);fs.readFile(f,(e,d)=>{if(e){r.statusCode=404;r.end();return;}r.setHeader('content-type',{'.html':'text/html','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp'}[path.extname(f)]||'application/octet-stream');r.end(d);});}).listen(0,async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width,height:900}});
 await p.goto(`http://127.0.0.1:${srv.address().port}/${slug}/`,{waitUntil:'load'});
 await p.evaluate(()=>document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'));await p.waitForTimeout(3000);
 const r=await p.evaluate(()=>{const cv=document.createElement('canvas').getContext('2d');const Y=scrollY;
  const blocks=[...document.querySelectorAll('main p, main h1, main h2, main h3, main li, main div.res-item, main img, main .beige-rule, main hr')].filter(e=>{const q=e.getBoundingClientRect();return q.height>0&&q.width>0&&!e.closest('nav')&&!(e.matches('p,h1,h2,h3,li')&&!e.textContent.trim())&&!(e.matches('p,li,div')&&e.querySelector('p,li,div.res-item,h2,h3'));});
  function lines(el){if(el.matches('img,hr,.beige-rule')){const q=el.getBoundingClientRect();return [{base:q.bottom+Y,cap:q.top+Y}];}
   const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n,out=[];while((n=w.nextNode())){if(!n.nodeValue.trim())continue;const s=getComputedStyle(n.parentElement);cv.font=s.fontStyle+' '+s.fontWeight+' '+s.fontSize+' '+s.fontFamily;const m=cv.measureText('H');const rg=document.createRange();rg.selectNodeContents(n);[...rg.getClientRects()].forEach(q=>{if(q.width<1)return;const mid=(q.top+q.bottom)/2+Y;const base=mid+(m.fontBoundingBoxAscent-m.fontBoundingBoxDescent)/2;out.push({base,cap:base-m.actualBoundingBoxAscent});});}return out;}
  const L=blocks.map(e=>({e,l:lines(e)})).filter(x=>x.l.length);const out=[];
  for(let i=1;i<L.length;i++){const a=L[i-1],c=L[i];if(c.e.contains(a.e)||a.e.contains(c.e))continue;const base=Math.max(...a.l.map(x=>x.base)),cap=Math.min(...c.l.map(x=>x.cap));
   const nm=x=>x.e.matches('img')?'[image]':x.e.matches('hr,.beige-rule')?'[divider]':x.e.textContent.trim().replace(/\s+/g,' ').slice(0,40);
   out.push(Math.round((cap-base)*10)/10+' | '+nm(a)+' -> '+nm(c));}return out.join('\n');});
 console.log(r);await b.close();srv.close();});
