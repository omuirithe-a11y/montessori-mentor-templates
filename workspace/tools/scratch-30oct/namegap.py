import sys, zipfile, tempfile, threading, http.server, functools
from playwright.sync_api import sync_playwright
Z=sys.argv[1]; d=tempfile.mkdtemp(dir=sys.argv[2]); zipfile.ZipFile(Z).extractall(d)
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
URL='http://127.0.0.1:%d/aun-aprendo/'%s.server_address[1]
JS=r"""()=>{const cv=document.createElement('canvas').getContext('2d');
const m=(el)=>{const st=getComputedStyle(el);cv.font=st.fontStyle+' '+st.fontWeight+' '+st.fontSize+' '+st.fontFamily;return cv.measureText('H')};
const lines=(el)=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let t,R=[];while(t=w.nextNode()){if(!t.nodeValue.trim())continue;const r=document.createRange();r.selectNodeContents(t);for(const x of r.getClientRects())if(x.width)R.push([x,t.parentElement])}return R};
const cap=(el)=>{const L=lines(el);if(!L.length)return null;const top=Math.min(...L.map(a=>a[0].top));const a=L.find(a=>Math.abs(a[0].top-top)<1);const mm=m(a[1]);return a[0].top+(a[0].height-(mm.fontBoundingBoxAscent+mm.fontBoundingBoxDescent))/2+mm.fontBoundingBoxAscent-mm.actualBoundingBoxAscent};
const base=(el)=>{const L=lines(el);if(!L.length)return null;const b=Math.max(...L.map(a=>a[0].bottom));const a=L.find(a=>Math.abs(a[0].bottom-b)<1);const mm=m(a[1]);return a[0].top+(a[0].height-(mm.fontBoundingBoxAscent+mm.fontBoundingBoxDescent))/2+mm.fontBoundingBoxAscent};
const out=[];for(const n of document.querySelectorAll('main p.mm-name')){const g=n.previousElementSibling;let lineB=null;if(g&&g.classList.contains('mm-gl')){const r=g.getBoundingClientRect();const bs=getComputedStyle(g);lineB=r.bottom-parseFloat(bs.paddingBottom||0)-parseFloat(bs.borderBottomWidth||0);const bt=parseFloat(bs.borderTopWidth),bb=parseFloat(bs.borderBottomWidth);out.push({bt,bb,h:r.height})}
 let nx=n.nextElementSibling;while(nx&&(!nx.textContent.trim()||nx.classList.contains('mm-gl')))nx=nx.nextElementSibling;
 out.push({name:n.textContent.trim().slice(0,28),gl:!!(g&&g.classList.contains('mm-gl')),glBottomToCaps:lineB===null?null:Math.round((cap(n)-lineB)*10)/10,nameBaseToNextCaps:nx?Math.round((cap(nx)-base(n))*10)/10:null,next:nx?nx.tagName+'.'+nx.className:null})}
return out}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in (1440,390):
    pg=b.new_page(viewport={'width':w,'height':900}); pg.goto(URL,wait_until='load'); pg.evaluate("async()=>{await document.fonts.ready;await new Promise(r=>setTimeout(r,4000))}")
    print(w); [print(' ',x) for x in pg.evaluate(JS)]; pg.close()
  b.close()
