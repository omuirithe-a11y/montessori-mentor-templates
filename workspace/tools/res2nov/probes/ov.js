const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const [root,page_]=process.argv.slice(2);
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);fs.readFile(f,(e,d)=>{if(e){r.statusCode=404;r.end();return;}r.setHeader('content-type',{'.html':'text/html','.jpg':'image/jpeg'}[path.extname(f)]||'application/octet-stream');r.end(d);});}).listen(0,async()=>{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:320,height:900}});await p.goto(`http://127.0.0.1:${srv.address().port}/${page_}/`,{waitUntil:'load'});
 const bad=[];for(let w=320;w<=1440;w+=10){await p.setViewportSize({width:w,height:900});await p.waitForTimeout(700);
  const r=await p.evaluate(()=>{const ps=[...document.querySelectorAll('main p')].filter(x=>/^(It’s Never|Wordless Picture)/.test(x.textContent.trim()));const t=document.querySelector('main .res-title');const items=[...document.querySelectorAll('main div.res-item')].filter(x=>x.textContent.includes('100 Brilliant'));const els=[...items,...ps];const out=[];for(let i=1;i<els.length;i++){const a=els[i-1].getBoundingClientRect(),c=els[i].getBoundingClientRect();out.push(Math.round(c.top-a.bottom));}return out;});
  if(r.some(x=>x<0))bad.push([w,r]);}
 console.log('overlaps:',JSON.stringify(bad));await b.close();srv.close();});
