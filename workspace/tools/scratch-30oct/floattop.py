import sys
from playwright.sync_api import sync_playwright
JS="""()=>{const cv=document.createElement('canvas').getContext('2d');const out=[];
for(const f of document.querySelectorAll('main .mm-float')){if(getComputedStyle(f).cssFloat==='none')continue;const pim=f.querySelector('.pim');let n=f.nextElementSibling;while(n&&(n.classList.contains('mm-fspacer')||n.classList.contains('mm-float')))n=n.nextElementSibling;if(!n)continue;
const r=document.createRange();const w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let t,top=1e9;while(t=w.nextNode()){if(!t.nodeValue.trim())continue;r.selectNodeContents(t);for(const q of r.getClientRects()){if(q.width)top=Math.min(top,q.top)}}
const s=getComputedStyle(n);cv.font=s.fontStyle+' '+s.fontWeight+' '+s.fontSize+' '+s.fontFamily;const m=cv.measureText('H');const cap=top+m.fontBoundingBoxAscent-m.actualBoundingBoxAscent;
out.push([(pim.querySelector('img').getAttribute('src')||'').slice(-14),Math.round((pim.getBoundingClientRect().top-cap)*10)/10,n.textContent.trim().slice(0,24)])}return out}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in [int(x) for x in sys.argv[2].split(',')]:
        pg=b.new_page(viewport={'width':w,'height':900}); pg.goto('file://'+sys.argv[1]); pg.wait_for_timeout(3500); print(w, pg.evaluate(JS)); pg.close()
    b.close()
