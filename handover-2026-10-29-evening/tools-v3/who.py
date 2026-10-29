import asyncio,zipfile,tempfile,os,threading,http.server,functools,shutil,sys,json,collections
from playwright.async_api import async_playwright
S='/tmp/claude-0/-home-claude/457824cb-7342-52d8-8229-8cd580a6aa46/scratchpad'
INJ=r"""(()=>{const o=CSSStyleDeclaration.prototype.setProperty;window.__who=[];CSSStyleDeclaration.prototype.setProperty=function(k,v,pr){try{if(k==='margin-top'&&parseFloat(v)>%d){const st=(new Error).stack.split('\n').slice(2,4).map(x=>x.trim().replace(/\(?http:\/\/[^)]*\/:/,'line ')).join(' < ');window.__who.push(Math.round(parseFloat(v))+' | '+st)}}catch(e){}return o.call(this,k,v,pr)}})()"""
def serve(d):
    H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
async def main():
    W=int(sys.argv[1]);thr=int(sys.argv[2]);openall=sys.argv[3]=='open'
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for z in sys.argv[4:]:
            t=tempfile.mkdtemp(dir=S+'/elist');zipfile.ZipFile(z).extractall(t);slug=os.listdir(t)[0];s=serve(t)
            ctx=await b.new_context(viewport={'width':W,'height':900});await ctx.add_init_script(INJ%thr);pg=await ctx.new_page()
            await pg.goto('http://127.0.0.1:%d/%s/'%(s.server_address[1],slug),wait_until='load');await pg.wait_for_timeout(4000)
            if openall: await pg.evaluate("()=>document.querySelectorAll('main details').forEach(x=>x.open=true)");await pg.wait_for_timeout(4000)
            w=await pg.evaluate('window.__who');c=collections.Counter(x.split(' | ',1)[1] for x in w)
            print(slug,len(w),'big margin-top writes');[print('  ',n,'x',k[:230]) for k,n in c.most_common(5)]
            await ctx.close();s.shutdown();shutil.rmtree(t,True)
        await b.close()
asyncio.run(main())
