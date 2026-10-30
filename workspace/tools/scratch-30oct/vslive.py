import sys, os, io, zipfile, tempfile, threading, http.server, functools
from playwright.sync_api import sync_playwright
from PIL import Image
Z, LIVE, OUT = sys.argv[1:4]
def serve(d):
    H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=d)
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=s.serve_forever, daemon=True).start(); return s.server_address[1]
d = tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(d); pb = serve(d); pl = serve(os.path.dirname(LIVE.rstrip('/')))
urls = {'live': 'http://127.0.0.1:%d/%s/' % (pl, os.path.basename(LIVE.rstrip('/'))), 'new': 'http://127.0.0.1:%d/aun-aprendo/' % pb}
JS = "async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}window.scrollTo(0,0);await Promise.race([Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,15000))]);await new Promise(r=>setTimeout(r,1500))}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 768, 390):
        im = {}
        for k, u in urls.items():
            pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto(u, wait_until='load'); pg.evaluate(JS)
            im[k] = Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert('RGB'); pg.close()
        seg = 1400 if w > 500 else 1600; H = max(im['live'].height, im['new'].height); n = 0
        for y in range(0, H, seg):
            c = Image.new('RGB', (w * 2 + 20, seg), 'red')
            for i, k in enumerate(('live', 'new')): c.paste(im[k].crop((0, y, w, y + seg)), (i * (w + 20), 0))
            n += 1; c.save(os.path.join(OUT, 'w%d-part%02d.png' % (w, n)))
        print(w, 'live height', im['live'].height, 'new height', im['new'].height, 'parts', n, flush=True)
    b.close()
