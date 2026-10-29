import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for rnd in [1,2]:
    c=b.new_context(viewport={'width':1440,'height':900});pg=c.new_page()
    info={}
    def onresp(r):
      if '/images/' in r.url and r.url.split('/')[-1][:3].isdigit() and '-' not in r.url.split('/')[-1]:
        h=r.headers;info[r.url.split('/')[-1]]=(h.get('content-type'),h.get('x-hcdn-cache-status'),h.get('content-length'),h.get('x-hcdn-upstream-rt'))
    pg.on('response',onresp)
    pg.goto('https://montessorimentor.co.uk/the-role-of-the-adult/',wait_until='load',timeout=90000);pg.wait_for_timeout(3000)
    for n in ['002','006','020','034','010','012']:
      im=pg.locator('img[data-full="images/%s.jpg"]'%n).first;im.scroll_into_view_if_needed();pg.wait_for_timeout(800)
      t0=time.time();im.click()
      pg.wait_for_function("()=>{const i=document.getElementById('lightbox-img');return i.src.includes('/%s.jpg')&&i.complete&&i.naturalWidth>0}"%n,timeout=30000)
      print('round',rnd,n,'%.2f s'%(time.time()-t0),info.get(n+'.jpg'),flush=True)
      pg.evaluate("()=>document.getElementById('lightbox').classList.remove('open')");pg.wait_for_timeout(400)
    c.close()
  b.close()
