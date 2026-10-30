"""shotcmp.py <a.zip> <b.zip> <widths csv|all> <out.txt>: full-page screenshots of both packages at each width, compared pixel by pixel."""
import sys, os, re, zipfile, tempfile, threading, http.server, functools, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
A, B, W, OUT = sys.argv[1:5]
if W == 'all':
    src = open('/home/claude/chk/v5/visual_check.py', encoding='utf-8').read()
    W = eval(re.search(r'^WIDTHS = (.*?)\s*#', src, re.M).group(1))
else: W = [int(x) for x in W.split(',')]
def serve(z):
    d = tempfile.mkdtemp(); zipfile.ZipFile(z).extractall(d); slug = zipfile.ZipFile(z).namelist()[0].split('/')[0]
    H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=d)
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=s.serve_forever, daemon=True).start()
    return 'http://127.0.0.1:%d/%s/' % (s.server_address[1], slug)
UA, UB = serve(A), serve(B)
JS_READY = "async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}window.scrollTo(0,0);await Promise.race([Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,15000))]);await document.fonts.ready;await new Promise(r=>setTimeout(r,800));return document.documentElement.scrollHeight}"
out = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in W:
        shots = []
        for u in (UA, UB):
            pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto(u, wait_until='load'); h = pg.evaluate(JS_READY)
            shots.append((h, Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert('RGB'))); pg.close()
        (ha, ia), (hb, ib) = shots
        if ia.size != ib.size: out.append('%4d DIFFERENT SIZE %s vs %s' % (w, ia.size, ib.size)); continue
        bb = ImageChops.difference(ia, ib).getbbox()
        out.append('%4d %s' % (w, 'identical' if bb is None else 'differs in box %s' % (bb,)))
        print(out[-1], flush=True)
    b.close()
n = sum(1 for x in out if x.endswith('identical'))
open(OUT, 'w').write('\n'.join(out) + '\nRESULT: %d of %d widths identical\n' % (n, len(out)))
print('RESULT: %d of %d widths identical' % (n, len(out)))
