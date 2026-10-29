import asyncio,zipfile,tempfile,os,threading,http.server,functools,shutil,json,sys
from playwright.async_api import async_playwright
S='/tmp/claude-0/-home-claude/457824cb-7342-52d8-8229-8cd580a6aa46/scratchpad'
JS="""()=>{const f=document.querySelector('.site-foot,footer');const ft=f.getBoundingClientRect().top+scrollY;const below=[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.height>0&&r.top+scrollY>ft}).length;
const big=[...document.querySelectorAll('main *')].map(e=>[e,parseFloat(getComputedStyle(e).marginTop)]).filter(x=>x[1]>150).map(([e,m])=>{const p=e.previousElementSibling;return Math.round(m)+'px on '+e.tagName+'.'+[...e.classList].join('.')+' "'+(e.textContent||'').trim().slice(0,35)+'" after '+(p?p.tagName+'.'+[...p.classList].join('.'):'nothing')});
return {pageHeight:document.documentElement.scrollHeight,footerTop:Math.round(ft),elementsBelowFooter:below,marginsOver150:big.slice(0,6)}}"""
def serve(d):
    H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for z in sys.argv[1:]:
            if z.endswith('.zip'): t=tempfile.mkdtemp(dir=S+'/elist');zipfile.ZipFile(z).extractall(t);slug=os.listdir(t)[0];root=t
            else: slug=os.path.basename(z);root=os.path.dirname(z);t=None
            s=serve(root);pg=await b.new_page(viewport={'width':1440,'height':900});await pg.goto('http://127.0.0.1:%d/%s/'%(s.server_address[1],slug),wait_until='load',timeout=60000);await pg.wait_for_timeout(4000)
            print(('live ' if not t else '')+slug,json.dumps(await pg.evaluate(JS))[:700],flush=True);await pg.close();s.shutdown()
            if t: shutil.rmtree(t,True)
        await b.close()
asyncio.run(main())
