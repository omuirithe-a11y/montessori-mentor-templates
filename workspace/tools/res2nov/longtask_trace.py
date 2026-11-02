# longtask_trace.py <folder holding <slug>/index.html> <slug> <width>: long tasks while scrolling, with images loaded, resizes and main size changes
import sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
d, slug, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
INIT="""(function reg(){if(!document.documentElement)return setTimeout(reg,0);window.__lt=[];try{new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push([Math.round(e.startTime),Math.round(e.duration)]))).observe({type:'longtask'})}catch(e){}
window.__ev=[];document.addEventListener('load',e=>{if(e.target.tagName==='IMG')window.__ev.push([Math.round(performance.now()),'img '+e.target.src.split('/').pop()])},true);
window.addEventListener('resize',()=>window.__ev.push([Math.round(performance.now()),'resize '+innerWidth+'x'+innerHeight]));})();"""
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':w,'height':900}); c.add_init_script(INIT)
    c.route('**/*', lambda r: (__import__('time').sleep(0.7) if '/images/' in r.request.url else None, r.continue_()))
    pg=c.new_page(); pg.goto('http://127.0.0.1:%d/%s/'%(s.server_address[1],slug),wait_until='load'); pg.wait_for_timeout(4000)
    pg.evaluate("()=>{window.__lt=[];window.__ev=[];const m=document.querySelector('main');window.__sz=[];new ResizeObserver(e=>window.__sz.push([Math.round(performance.now()),Math.round(m.getBoundingClientRect().width),Math.round(m.getBoundingClientRect().height)])).observe(m)}")
    for y in range(0,pg.evaluate("document.documentElement.scrollHeight"),700): pg.mouse.wheel(0,700); pg.wait_for_timeout(1200)
    pg.wait_for_timeout(3000)
    print('long tasks',pg.evaluate("window.__lt")); print('events',pg.evaluate("window.__ev")); print('main size',pg.evaluate("window.__sz"))
    b.close()
