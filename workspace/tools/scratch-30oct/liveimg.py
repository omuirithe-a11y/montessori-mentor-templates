import time, json, sys
from playwright.sync_api import sync_playwright
W=int(sys.argv[1]); R=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':900}, device_scale_factor=2 if W<=640 else 1)
    t0=time.time()
    def done(r):
        if r.request.resource_type=='image':
            try: n=len(r.body())
            except Exception: n=-1
            R.append((round(time.time()-t0,2), r.status, n, r.url.split('/')[-1][:40], r.headers.get('content-type',''), r.headers.get('server',''), r.headers.get('x-hcdn-cache-status', r.headers.get('x-cache',''))))
    pg.on('response', done)
    pg.goto('https://montessorimentor.co.uk/aun-aprendo/', wait_until='load', timeout=120000); tl=time.time()-t0
    h=pg.evaluate('document.body.scrollHeight')
    for y in range(0,h,800): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(400)
    pg.wait_for_timeout(4000)
    info=pg.evaluate("""()=>[...document.querySelectorAll('main img.doc-img')].slice(0,3).map(i=>[i.currentSrc.split('/').pop(),i.naturalWidth,i.naturalHeight,Math.round(i.getBoundingClientRect().width)])""")
    b.close()
print('width',W,'page load event',round(tl,1),'s; image responses',len(R),'; total',round(sum(max(0,x[2]) for x in R)/1e6,1),'MB')
print('first images shown (file, natural w, h, shown w):',info)
R.sort(key=lambda x:-x[2]); print('largest 6:'); [print(' ',x) for x in R[:6]]
ts=[x[0] for x in R]; print('first image at',min(ts) if ts else None,'s, last at',max(ts) if ts else None,'s')
