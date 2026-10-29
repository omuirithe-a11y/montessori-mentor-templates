import sys,json,asyncio,zipfile,tempfile,os,threading,http.server,functools,shutil
from playwright.async_api import async_playwright
import tempfile; S=tempfile.mkdtemp(prefix='stable-'); os.makedirs(S+'/elist', exist_ok=True)
def serve(d):
    H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
H="()=>Math.round(document.querySelector('main').getBoundingClientRect().height)"
G="()=>{let m=0,w='';for(const e of document.querySelectorAll('main *')){const v=parseFloat(getComputedStyle(e).marginTop);if(v>m){m=v;w=e.tagName+'.'+[...e.classList].join('.')+' '+(e.textContent||'').trim().slice(0,30)}}return [Math.round(m),w]}"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for z in sys.argv[2:]:
            if z.endswith('.zip'): t=tempfile.mkdtemp(dir=S+'/elist');zipfile.ZipFile(z).extractall(t);slug=os.listdir(t)[0];root=t
            else: slug=os.path.basename(z);root=os.path.dirname(z);t=None
            s=serve(root);r={}
            pg=await b.new_page(viewport={'width':int(sys.argv[1]),'height':900});await pg.goto('http://127.0.0.1:%d/%s/'%(s.server_address[1],slug),wait_until='load',timeout=60000)
            await pg.wait_for_timeout(1000);r['1s']=await pg.evaluate(H)
            await pg.wait_for_timeout(3000);r['4s']=await pg.evaluate(H)
            for y in range(0,60000,800):
                await pg.evaluate('scrollTo(0,%d)'%y);await pg.wait_for_timeout(60)
            await pg.wait_for_timeout(3500);r['scrolled']=await pg.evaluate(H)
            n=await pg.evaluate("()=>{const d=[...document.querySelectorAll('main details')];d.forEach(x=>x.open=true);return d.length}")
            if n: await pg.wait_for_timeout(3500);r['all %d open'%n]=await pg.evaluate(H);r['largest margin, open']=await pg.evaluate(G);await pg.evaluate("()=>document.querySelectorAll('main details').forEach(x=>x.open=false)");await pg.wait_for_timeout(3500);r['closed again']=await pg.evaluate(H)
            r['largest margin']=await pg.evaluate(G)
            print(slug,json.dumps(r),flush=True);await pg.close();s.shutdown()
            if t: shutil.rmtree(t,True)
        await b.close()
asyncio.run(main())
