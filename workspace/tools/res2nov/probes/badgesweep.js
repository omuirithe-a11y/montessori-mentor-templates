const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pages=JSON.parse(process.argv[2]);
for(const [f,slug] of pages){let bad=[];const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('file://'+f);await p.waitForTimeout(2000);
 for(let w=320;w<=1440;w+=(w<760?3:40)){await p.setViewportSize({width:w,height:900});await p.waitForTimeout(350);
  const r=await p.evaluate(()=>{const out=[];document.querySelectorAll('main a.pdf').forEach(a=>{const q=a.getBoundingClientRect();if(!q.width)return;if(q.height>28||q.width<28)out.push('squeezed '+Math.round(q.width)+'x'+Math.round(q.height));
   const it=a.closest('.res-item,h3,p');if(!it)return;const rg=document.createRange();rg.selectNodeContents(it);const rs=[...rg.getClientRects()].filter(x=>x.width>2&&!(x.left>=q.left-1&&x.right<=q.right+1&&x.top>=q.top-1&&x.bottom<=q.bottom+1));
   const same=rs.some(x=>Math.abs((x.top+x.bottom)/2-(q.top+q.bottom)/2)<12);if(!same)out.push('alone: '+(it.textContent.trim().slice(0,30)));});return out;});
  if(r.length)bad.push(w+': '+[...new Set(r)].join('; '));}
 console.log(slug, bad.length?'\n  '+bad.join('\n  '):'OK');await p.close();}await b.close();})();
