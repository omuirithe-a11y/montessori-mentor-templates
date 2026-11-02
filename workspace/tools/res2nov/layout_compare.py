# layout_compare.py <old.zip> <new.zip> : positions of every block in main and every line, at 8 widths, old vs new; prints differences
import sys, os, zipfile, tempfile, threading, http.server, functools, json
from playwright.sync_api import sync_playwright
def serve(z):
    d=tempfile.mkdtemp(); zipfile.ZipFile(z).extractall(d); slug=zipfile.ZipFile(z).namelist()[0].split('/')[0]
    H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
    return 'http://127.0.0.1:%d/%s/'%(s.server_address[1],slug)
U=[serve(sys.argv[1]),serve(sys.argv[2])]; print('old',U[0],'new',U[1])
JS="""async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}window.scrollTo(0,0);await new Promise(r=>setTimeout(r,2500));
return [...document.querySelectorAll('main *')].filter(e=>e.matches('p,h2,h3,li,.pim,.beige-rule,.res-item,a.pdf')).map(e=>{const q=e.getBoundingClientRect();return [e.tagName+'.'+e.className,(e.textContent||'').trim().slice(0,30),Math.round((q.top+scrollY)*10)/10,Math.round(q.left*10)/10,Math.round(q.height*10)/10]})}"""
bad=0; TOL=float(sys.argv[3]) if len(sys.argv)>3 else 0.0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,640,641,768,1024,1280,1440):
        R=[]
        for u in U:
            pg=b.new_page(viewport={'width':w,'height':900}); pg.goto(u,wait_until='load'); R.append(pg.evaluate(JS)); pg.close()
        d=[(a,c) for a,c in zip(R[0],R[1]) if a[:2]!=c[:2] or any(abs(x-y)>TOL for x,y in zip(a[2:],c[2:]))]; mx=max([abs(x-y) for a,c in zip(R[0],R[1]) for x,y in zip(a[2:],c[2:])] or [0])
        if len(R[0])!=len(R[1]): d.append(('count',len(R[0]),len(R[1])))
        print(w,'elements',len(R[0]),'differences over %.1f px'%TOL,len(d),'largest shift %.1f px'%mx); bad+=len(d)
        for x in d[:5]: print('   ',x)
    b.close()
print('LAYOUT IDENTICAL' if not bad else 'LAYOUT DIFFERS')
