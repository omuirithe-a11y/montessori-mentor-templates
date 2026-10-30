#!/usr/bin/env python3
"""place_check.py <package.zip> [--rows-one-width]   (30 Oct 2026, owner 13:53 "implement the items on that list immediately")
Three placement checks the 122-width check missed on 30 Oct (Aun Aprendo), measured on the page as a reader sees it:
  COLUMN  every image inside main stays within the text column (no image runs past its column's right or left edge);
          widths 320-1920 (Aun Aprendo build b3: the Beckett image ran 18 px past the text at 390).
  TOP     an image beside text (floated, 641 px and wider) has its top level with the top of the capitals of the first line
          of the paragraph beside it, within 1 px - the owner's rule of 20 Oct ("side photos always align with the first line
          of the text"); widths 641-1920.
  ROWS    (only with --rows-one-width: a page the owner made an exception, Aun Aprendo 30 Oct 12:50) every row of images
          starts and ends at the same edges; widths 831-1920 (at 830 and narrower rows swipe).
Prints one line per check and width with a fault, then PLACE OK or PLACE FAULT. Exit 0 only on PLACE OK."""
import sys, os, zipfile, tempfile, threading, http.server, functools, shutil, atexit
from playwright.sync_api import sync_playwright
Z = sys.argv[1]; ROWS = '--rows-one-width' in sys.argv
d = tempfile.mkdtemp(prefix='pc-'); atexit.register(shutil.rmtree, d, True); zipfile.ZipFile(Z).extractall(d)
slug = zipfile.ZipFile(Z).namelist()[0].split('/')[0]
H = functools.partial(type('Q', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=d)
s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=s.serve_forever, daemon=True).start()
URL = 'http://127.0.0.1:%d/%s/' % (s.server_address[1], slug)
READY = "async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.race([Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,15000))]);await document.fonts.ready;await new Promise(r=>setTimeout(r,3500))}"
JS = r"""(rows)=>{const m=document.querySelector('main');const out={col:[],top:[],rows:null};
const tp=[...m.querySelectorAll('p')].find(p=>p.textContent.trim().length>80&&!p.closest('blockquote,figure,li'));const T=tp?tp.getBoundingClientRect():m.getBoundingClientRect();
for(const i of m.querySelectorAll('img.doc-img')){const r=i.closest('.pim')?i.closest('.pim').getBoundingClientRect():i.getBoundingClientRect();if(!r.width||i.closest('.mm-row'))continue;
  if(r.right>T.right+1||r.left<T.left-1)out.col.push([(i.getAttribute('src')||'').split('/').pop(),Math.round(r.left),Math.round(r.right),Math.round(T.left),Math.round(T.right)])}
const cv=document.createElement('canvas').getContext('2d');
for(const f of m.querySelectorAll('.mm-float')){if(getComputedStyle(f).cssFloat==='none')continue;const pim=f.querySelector('.pim');if(!pim)continue;
  let n=f.nextElementSibling;while(n&&(n.classList.contains('mm-fspacer')||n.classList.contains('mm-float')))n=n.nextElementSibling;if(!n)continue;
  const rg=document.createRange(),w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let t,top=1e9;while(t=w.nextNode()){if(!t.nodeValue.trim())continue;rg.selectNodeContents(t);for(const q of rg.getClientRects())if(q.width)top=Math.min(top,q.top)}
  if(top>=1e9)continue;const st=getComputedStyle(n);cv.font=st.fontStyle+' '+st.fontWeight+' '+st.fontSize+' '+st.fontFamily;const mm=cv.measureText('H');
  const off=pim.getBoundingClientRect().top-(top+mm.fontBoundingBoxAscent-mm.actualBoundingBoxAscent);
  if(Math.abs(off)>1)out.top.push([(pim.querySelector('img').getAttribute('src')||'').split('/').pop(),Math.round(off*10)/10,n.textContent.trim().slice(0,30)])}
if(rows){const e=[...m.querySelectorAll('.mm-row')].map(r=>{const is=[...r.querySelectorAll('img')].map(i=>i.getBoundingClientRect()).filter(q=>q.width>0);return is.length?[Math.round(is[0].left),Math.round(is[is.length-1].right)]:null}).filter(x=>x);
  const L=e.map(x=>x[0]),R=e.map(x=>x[1]);out.rows=(Math.max(...L)-Math.min(...L)>1||Math.max(...R)-Math.min(...R)>1)?e:[]}
return out}"""
W = [320, 360, 390, 430, 480, 560, 640, 641, 700, 768, 830, 831, 900, 1024, 1100, 1280, 1440, 1920]
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.goto(URL, wait_until='load')
    for w in W:
        pg.set_viewport_size({'width': w, 'height': 900}); pg.reload(wait_until='load'); pg.evaluate(READY)
        r = pg.evaluate(JS, ROWS and w >= 831)
        if r['col']: bad += 1; print('%4d COLUMN fault: image past the text column [image, left, right, column left, column right]: %s' % (w, r['col']))
        if w >= 641 and r['top']: bad += 1; print('%4d TOP fault: image top not level with the first line capitals [image, px off, text]: %s' % (w, r['top']))
        if r['rows']: bad += 1; print('%4d ROWS fault: rows do not share their edges: %s' % (w, r['rows']))
    b.close()
print('widths %d, package %s' % (len(W), os.path.basename(Z)))
print('PLACE OK' if not bad else 'PLACE FAULT (%d)' % bad); sys.exit(1 if bad else 0)
