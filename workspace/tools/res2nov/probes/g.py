import sys,zipfile,tempfile,threading,http.server,functools
from playwright.sync_api import sync_playwright
Z=sys.argv[1]; W=int(sys.argv[2])
d=tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(d)
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
JS=open('/home/claude/mm/tools/scratch-30oct/vslive.py').read().split('JS = "')[1].split('"\n')[0]
M="""()=>{const y=t=>{const w=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){const i=n.nodeValue.indexOf(t);if(i>=0){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+t.length);const q=r.getBoundingClientRect();return Math.round(q.top+scrollY);}}return null};
const a=y('Sydney, Australia'),b=y('Required Readings'),c=y('Each student is required');return [b-a,c-b,y('Key Principles Summarised'),document.body.scrollHeight];}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for i in range(2):
        pg=b.new_page(viewport={'width':W,'height':900}); pg.goto('http://127.0.0.1:%d/books-by-montessori/'%s.server_address[1],wait_until='load'); pg.evaluate(JS)
        print('run',i,pg.evaluate(M)); pg.close()
