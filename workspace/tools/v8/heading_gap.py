"""heading_gap.py <url> <widths comma> : for every image that stands straight after an H2/H3 (its block's previous
sibling is the heading), print the gap from the baseline of the heading's last line to the top of the image box (.pim), the same reference as the template's mm-image-gap-29oct."""
import sys, asyncio
from playwright.async_api import async_playwright
URL, WS = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]
JS = r"""() => {
  const cv=document.createElement('canvas').getContext('2d');
  function baseLast(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,q=null,s=null;while((n=w.nextNode())){if(!n.nodeValue.trim())continue;var r=document.createRange();r.selectNodeContents(n);var rs=r.getClientRects();for(var i=0;i<rs.length;i++){if(rs[i].width&&(!q||rs[i].bottom>=q.bottom)){q=rs[i];s=n.parentElement;}}}if(!q)return null;var st=getComputedStyle(s);cv.font=st.fontStyle+' '+st.fontWeight+' '+st.fontSize+' '+st.fontFamily;var m=cv.measureText('H');return q.top+(q.height-(m.fontBoundingBoxAscent+m.fontBoundingBoxDescent))/2+m.fontBoundingBoxAscent;}
  const out=[];
  document.querySelectorAll('main img').forEach(img=>{
    let b=img; while(b.parentElement && b.parentElement.tagName!=='MAIN' && !b.previousElementSibling) b=b.parentElement;
    let pv=b.previousElementSibling; while(pv && getComputedStyle(pv).display==='none') pv=pv.previousElementSibling;
    if(!pv || !/^H[23]$/.test(pv.tagName)) return;
    const last=baseLast(pv); if(last===null) return; const it=(img.closest('.pim')||img).getBoundingClientRect();
    if(it.height===0) return;
    out.push([ (img.getAttribute('src')||'').split('/').pop(), pv.textContent.trim().slice(0,40), Math.round((it.top-last)*10)/10 ]);
  }); return out; }"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in WS:
            pg = await b.new_page(viewport={'width': w, 'height': 900})
            await pg.goto(URL, wait_until='load', timeout=90000); await pg.wait_for_timeout(4000)
            for row in await pg.evaluate(JS): print(w, *row)
            await pg.close()
        await b.close()
asyncio.run(main())
