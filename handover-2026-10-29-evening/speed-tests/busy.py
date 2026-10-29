import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in [1440,390]:
    c=b.new_context(viewport={'width':w,'height':900});pg=c.new_page()
    pg.goto('https://montessorimentor.co.uk/the-role-of-the-adult/',wait_until='load',timeout=90000);pg.wait_for_timeout(5000)
    pg.evaluate("""()=>{window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)]))).observe({type:'longtask'});
      window.__runs=0;const o=window.__mmAfterLayout;}""")
    H=pg.evaluate("document.documentElement.scrollHeight");tot=0;worst=0;n=0;steps=0
    for y in range(0,H,700):
      pg.evaluate("()=>{window.__lt=[]}");pg.mouse.wheel(0,700);pg.wait_for_timeout(1200)
      lt=pg.evaluate("window.__lt");s=sum(d for _,d in lt);tot+=s;steps+=1
      if lt: n+=1;worst=max(worst,max(d for _,d in lt))
    print(w,'scroll steps',steps,'steps with busy periods',n,'total busy ms',tot,'longest single busy period ms',worst,flush=True)
    c.close()
  b.close()
