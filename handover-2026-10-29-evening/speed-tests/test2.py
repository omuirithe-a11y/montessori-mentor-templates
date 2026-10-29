import sys,time,json,threading,http.server,functools
from playwright.sync_api import sync_playwright
ROOT=sys.argv[1];VARS=sys.argv[2].split(',');WS=[int(x) for x in sys.argv[3].split(',')];DELAY=0.7
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=ROOT)
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=srv.serve_forever,daemon=True).start();PORT=srv.server_address[1]
SNAP="()=>{const a=[];document.querySelector('main').querySelectorAll('p,h2,h3,li,blockquote,figure,.mm-float,img,hr').forEach(e=>{const r=e.getBoundingClientRect();a.push([Math.round((r.top+scrollY)*10)/10,Math.round(r.left*10)/10,Math.round(r.height*10)/10,Math.round(r.width*10)/10])});return a}"
INIT="""(function reg(){if(!document.documentElement)return setTimeout(reg,0);window.__p=0;new MutationObserver(()=>window.__p++).observe(document.documentElement,{attributes:true,attributeFilter:['data-layout']});
 window.__lt=[];try{new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(e.duration))).observe({type:'longtask'})}catch(e){}})();"""
def route(r):
  if '/images/' in r.request.url: time.sleep(DELAY)
  r.continue_()
res={}
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in WS:
    for v in VARS:
      url='http://127.0.0.1:%d/the-role-of-the-adult/index-%s.html'%(PORT,v)
      # scroll test
      c=b.new_context(viewport={'width':w,'height':900});c.add_init_script(INIT);c.route('**/*',route);pg=c.new_page()
      pg.goto(url,wait_until='load',timeout=120000);pg.wait_for_timeout(4000)
      pg.evaluate("()=>{window.__p=0;window.__lt=[]}")
      Hh=pg.evaluate("document.documentElement.scrollHeight")
      for y in range(0,Hh,700): pg.mouse.wheel(0,700);pg.wait_for_timeout(1200)
      pg.wait_for_timeout(4000)
      passes,lt=pg.evaluate("[window.__p,window.__lt]")
      pg.evaluate("()=>scrollTo(0,0)");pg.wait_for_timeout(1500)
      snap=pg.evaluate(SNAP);hgt=pg.evaluate("Math.round(document.querySelector('main').getBoundingClientRect().height)")
      c.close()
      # click test (fresh window)
      clicks={}
      if True:
        c=b.new_context(viewport={'width':w,'height':900});c.route('**/*',route);pg=c.new_page()
        pg.goto(url,wait_until='load',timeout=120000);pg.wait_for_timeout(3000)
        for n in ['002','006','020','034']:
          im=pg.locator('img[data-full="images/%s.jpg"]'%n).first;im.scroll_into_view_if_needed();pg.wait_for_timeout(800)
          t0=time.time()
          try:
            im.click(timeout=20000)
            pg.wait_for_function("(n)=>{const i=document.getElementById('lightbox-img');return i.src.includes('/'+n+'.jpg')&&i.complete&&i.naturalWidth>0}",arg=n,timeout=20000)
            clicks[n]=round(time.time()-t0,2)
          except Exception as e: clicks[n]='failed'
          pg.evaluate("()=>document.getElementById('lightbox').classList.remove('open')");pg.wait_for_timeout(400)
        c.close()
      res[(w,v)]=snap
      base=res.get((w,'0'))
      if base is None: diff='baseline'
      elif len(base)!=len(snap): diff='element count differs'
      else:
        mv=[max(abs(a-b2) for a,b2 in zip(x,y)) for x,y in zip(base,snap)];diff='%d elements differ by >0.5px (largest %.1f)'%(sum(1 for m in mv if m>0.5),max(mv))
      print(json.dumps({'width':w,'variant':v,'passes':passes,'busy_total_ms':round(sum(lt)),'longest_ms':round(max(lt or [0])),'main_height':hgt,'vs_unchanged_page':diff,'click_s':clicks}),flush=True)
  b.close()
