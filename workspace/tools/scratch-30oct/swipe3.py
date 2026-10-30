import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=2); pg=c.new_page()
    pg.goto(URL,wait_until='load',timeout=120000); pg.wait_for_timeout(4000)
    n=pg.evaluate("document.querySelectorAll('main .mm-row').length"); bad=ok=0; print('rows',n)
    for i in range(n):
        st=pg.evaluate(f"""(()=>{{const r=document.querySelectorAll('main .mm-row')[{i}];r.scrollIntoView({{block:'center'}});
          let ta='',e=r;while(e){{const t=getComputedStyle(e).touchAction;if(t&&t!='auto'){{ta+=e.tagName+':'+t+' '}};e=e.parentElement}}
          const q=r.getBoundingClientRect();const d=r.nextElementSibling&&r.nextElementSibling.classList.contains('mm-dots')?r.nextElementSibling:null;
          return {{scroll:r.scrollWidth>r.clientWidth+5,ox:getComputedStyle(r).overflowX,ta,x:q.left+q.width/2,y:q.top+q.height/2,left:r.scrollLeft,dots:d?d.children.length:0,on:d?[...d.children].findIndex(s=>s.classList.contains('on')):null}}}})()""")
        if not st['scroll']: print(f"row {i+1}: fits the screen, nothing to swipe"); continue
        pg.mouse.move(st['x'],st['y']); pg.mouse.wheel(300,0); pg.wait_for_timeout(1500)
        af=pg.evaluate(f"""(()=>{{const r=document.querySelectorAll('main .mm-row')[{i}];const d=r.nextElementSibling&&r.nextElementSibling.classList.contains('mm-dots')?r.nextElementSibling:null;return {{left:r.scrollLeft,on:d?[...d.children].findIndex(s=>s.classList.contains('on')):null}}}})()""")
        good=af['left']>st['left']+20 and (st['dots']==0 or af['on']!=st['on']) and not st['ta'].count('none')
        ok+=good; bad+=not good
        print(f"row {i+1}: overflow {st['ox']}; touch-action {st['ta'] or 'auto'}; moved {round(st['left'])}->{round(af['left'])} px; dots {st['dots']}, active {st['on']}->{af['on']}  {'ok' if good else 'FAULT'}")
    print('SWIPE', 'OK' if bad==0 else f'FAULT ({bad})', f'- {ok} rows moved')
    b.close()
