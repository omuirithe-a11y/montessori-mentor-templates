import sys,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in [1440,390]:
    c=b.new_context(viewport={'width':w,'height':900});pg=c.new_page()
    pg.goto(sys.argv[1],wait_until='load',timeout=90000);pg.wait_for_timeout(5000)
    pg.evaluate("""()=>{
      const snap=()=>{const m=document.querySelector('main');const a=[];m.querySelectorAll('p,h2,h3,li,blockquote,figure,.mm-float,img,hr').forEach(e=>{const r=e.getBoundingClientRect();a.push(Math.round((r.top+scrollY)*10)/10,Math.round(r.left*10)/10,Math.round(r.height*10)/10)});return a;};
      window.__runs=[];let last=snap(),t0=null;
      new MutationObserver(()=>{const s=snap();let d=0,mx=0;for(let i=0;i<s.length;i++){const x=Math.abs(s[i]-(last[i]??0));if(x>0.5)d++;mx=Math.max(mx,x);}
        window.__runs.push({changed:d,maxMove:Math.round(mx*10)/10,sameCount:s.length===last.length});last=s;})
        .observe(document.documentElement,{attributes:true,attributeFilter:['data-layout']});
      window.__imgs=0;document.querySelectorAll('img.doc-img').forEach(i=>{if(!i.complete)i.addEventListener('load',()=>window.__imgs++)});}""")
    H=pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0,H,700): pg.mouse.wheel(0,700);pg.wait_for_timeout(1200)
    pg.wait_for_timeout(3000)
    r=pg.evaluate("[window.__runs,window.__imgs]")
    runs=r[0];moved=[x for x in runs if x['changed']]
    print(sys.argv[2],w,'images loaded while scrolling:',r[1],'| layout passes:',len(runs),'| passes that moved anything over 0.5px:',len(moved),'| largest move px:',max([x['maxMove'] for x in runs] or [0]),flush=True)
    if moved: print('   moved:',moved[:10])
    c.close()
  b.close()
