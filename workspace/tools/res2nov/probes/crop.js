const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const jobs=JSON.parse(process.argv[2]);
(async()=>{const b=await chromium.launch();
for(const j of jobs){
 const root=j.root;const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);fs.readFile(f,(e,d)=>{if(e){r.statusCode=404;r.end();return;}r.setHeader('content-type',{'.html':'text/html','.jpg':'image/jpeg','.png':'image/png'}[path.extname(f)]||'application/octet-stream');r.end(d);});});
 await new Promise(r=>srv.listen(0,r));
 const p=await b.newPage({viewport:{width:j.w,height:900}});await p.goto(`http://127.0.0.1:${srv.address().port}/${j.page}/`,{waitUntil:'load'});await p.waitForTimeout(2500);
 const box=await p.evaluate(t=>{const w=document.createTreeWalker(document.querySelector(t.sel||'main'),NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){if(n.nodeValue.includes(t.text)){let e=n.parentElement.closest(t.up||'p,div,h3,li,ul,nav');e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return {x:r.left,y:r.top+window.scrollY,w:r.width,h:r.height};}}return null;},j);
 if(!box){console.log('NOTFOUND',j.out);srv.close();continue;}
 await p.waitForTimeout(500);
 const y=Math.max(0,box.y-(j.above||60)),h=box.h+(j.above||60)+(j.below||60);
 await p.screenshot({path:j.out,fullPage:true,clip:{x:0,y,width:j.w,height:h}});console.log('ok',j.out,Math.round(h));
 await p.close();srv.close();}
await b.close();})();
