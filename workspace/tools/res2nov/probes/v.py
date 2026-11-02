import sys,zipfile,tempfile,threading,http.server,functools
from playwright.sync_api import sync_playwright
d=tempfile.mkdtemp(); zipfile.ZipFile(sys.argv[1]).extractall(d)
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
JS=open('/home/claude/mm/tools/scratch-30oct/vslive.py').read().split('JS = "')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':768,'height':900}); pg.goto('http://127.0.0.1:%d/books-by-montessori/'%s.server_address[1],wait_until='load'); pg.evaluate(JS)
    pg.evaluate('window.scrollTo(0,600)'); pg.wait_for_timeout(800); pg.screenshot(path=sys.argv[2])
    pg.screenshot(path=sys.argv[2]+'.full.png',full_page=True)
