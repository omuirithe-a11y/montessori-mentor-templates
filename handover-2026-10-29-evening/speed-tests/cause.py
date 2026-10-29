import sys
from playwright.sync_api import sync_playwright
INIT=r"""
window.__ev=[];
const _ael=EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener=function(t,f,o){
  if(this instanceof HTMLImageElement && t==='load' && this.classList && this.classList.contains('doc-img')){
    const img=this;const g=function(e){window.__ev.push(['image load',performance.now(),img.getAttribute('data-full')]);return f.apply(this,arguments)};return _ael.call(this,t,g,o);}
  if(this===window && (t==='resize'||t==='load')){const g=function(e){window.__ev.push(['window '+t,performance.now()]);return f.apply(this,arguments)};return _ael.call(this,t,g,o);}
  return _ael.call(this,t,f,o);};
const RO=window.ResizeObserver;window.ResizeObserver=function(cb){return new RO(function(es,o){window.__ev.push(['size observer',performance.now()]);return cb(es,o)})};
(function reg(){if(!document.documentElement){return setTimeout(reg,0)}new MutationObserver(()=>window.__ev.push(['PASS',performance.now()])).observe(document.documentElement,{attributes:true,attributeFilter:['data-layout']});})();
"""
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':1440,'height':900});c.add_init_script(INIT);pg=c.new_page()
  pg.goto(sys.argv[1],wait_until='load',timeout=90000);pg.wait_for_timeout(5000)
  pg.evaluate("()=>{window.__start=performance.now()}")
  H=pg.evaluate("document.documentElement.scrollHeight")
  for y in range(0,H,700): pg.mouse.wheel(0,700);pg.wait_for_timeout(1200)
  pg.wait_for_timeout(3000)
  ev=pg.evaluate("window.__ev.filter(e=>e[1]>=window.__start)")
  # for each PASS, the last trigger before it
  last=None;cause={};passes=0
  for e in ev:
    if e[0]=='PASS':
      passes+=1;k=last[0] if last else 'none';cause[k]=cause.get(k,0)+1;last=None
    elif last is None: last=e
  print('events while scrolling:',{k:sum(1 for e in ev if e[0]==k) for k in set(e[0] for e in ev)})
  print('passes:',passes,'| first trigger before each pass:',cause)
  b.close()
