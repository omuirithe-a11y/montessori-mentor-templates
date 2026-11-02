# shots.py <zip> <out dir> : full-page screenshots of the page in the zip at 1440, 768, 390, cut into parts (for a no-live page)
import sys, os, io, zipfile, tempfile, threading, http.server, functools
from playwright.sync_api import sync_playwright
from PIL import Image
Z, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
d = tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(d); slug = zipfile.ZipFile(Z).namelist()[0].split('/')[0]
H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=d)
s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=s.serve_forever, daemon=True).start()
url = 'http://127.0.0.1:%d/%s/' % (s.server_address[1], slug); print('address', url)
JS = "async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}window.scrollTo(0,0);await Promise.race([Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,15000))]);await new Promise(r=>setTimeout(r,1500))}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 768, 390):
        pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto(url, wait_until='load'); pg.evaluate(JS)
        im = Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert('RGB'); pg.close()
        seg = 1400 if w > 500 else 1600; n = 0
        for y in range(0, im.height, seg):
            n += 1; im.crop((0, y, w, min(im.height, y + seg))).save(os.path.join(OUT, 'w%d-part%02d.png' % (w, n)))
        print(w, 'height', im.height, 'parts', n, flush=True)
    b.close()
import shutil; shutil.rmtree(d, True)
