import time,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':1440,'height':900});pg=c.new_page()
  pg.goto('https://montessorimentor.co.uk/the-role-of-the-adult/',wait_until='load',timeout=90000);pg.wait_for_timeout(3000)
  pg.evaluate("""()=>{const i=document.getElementById('lightbox-img');window.__t={};
    new MutationObserver(()=>{window.__t.src=performance.now()}).observe(i,{attributes:true,attributeFilter:['src']});
    i.addEventListener('load',()=>{window.__t.load=performance.now()});}""")
  for n in ['002','020','034','010','012']:
    im=pg.locator('img[data-full="images/%s.jpg"]'%n).first;im.scroll_into_view_if_needed();pg.wait_for_timeout(800)
    r=pg.evaluate("""(n)=>{const e=document.querySelector('img[data-full="images/'+n+'.jpg"]');const f=e.closest('.mm-imgs,.mm-pfig,.mm-trio,.mm-float,figure');
       return {cls:e.parentElement.className+' | '+(f?f.className:''),rot:e.getAttribute('data-rot'),crop:e.getAttribute('data-crop'),lbOpenBefore:document.getElementById('lightbox').className}}""",n)
    pg.evaluate("()=>{window.__t={click:performance.now()}}")
    im.click()
    pg.wait_for_function("()=>{const i=document.getElementById('lightbox-img');return i.src.includes('/%s.jpg')&&i.complete&&i.naturalWidth>0}"%n,timeout=30000)
    t=pg.evaluate("()=>window.__t");rt=pg.evaluate("(n)=>{const e=performance.getEntriesByType('resource').filter(x=>x.name.endsWith('/images/'+n+'.jpg')).pop();return e?[Math.round(e.startTime),Math.round(e.responseStart),Math.round(e.responseEnd)]:null}",n)
    print(n,{k:round(v-t['click']) for k,v in t.items()},'resource start/firstbyte/end rel click:',[x-round(t['click']) for x in rt] if rt else None,r,flush=True)
    pg.evaluate("()=>document.getElementById('lightbox').classList.remove('open')");pg.wait_for_timeout(400)
  b.close()
