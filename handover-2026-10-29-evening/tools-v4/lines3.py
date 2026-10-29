import sys,asyncio,zipfile,tempfile,os,threading,http.server,functools,collections,shutil
from playwright.async_api import async_playwright
JS=r"""()=>{const m=document.querySelector("main#content")||document.querySelector("main");const out=[];
for(const e of m.querySelectorAll('*')){const s=getComputedStyle(e),r=e.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||r.width<20)continue;
 for(const side of ['Top','Bottom']){const w=parseFloat(s['border'+side+'Width']);if(w>=1&&s['border'+side+'Style']!=='none'&&s['border'+side+'Color']!=='rgba(0, 0, 0, 0)'&&!e.closest('table'))out.push('border-'+side.toLowerCase()+' '+w+'px '+s['border'+side+'Color']+' on '+e.tagName.toLowerCase()+'.'+[...e.classList].slice(0,2).join('.'))}
 const bg=s.backgroundColor;if(r.height>0&&r.height<=4&&bg!=='rgba(0, 0, 0, 0)')out.push('filled '+Math.round(r.height)+'px '+bg+' on '+e.tagName.toLowerCase()+'.'+[...e.classList].slice(0,2).join('.'));
 for(const ps of ['::before','::after']){const q=getComputedStyle(e,ps);if(!q.content||q.content==='none'||q.content==='normal'||q.display==='none')continue;const hh=parseFloat(q.height),bw=parseFloat(q.borderTopWidth)+parseFloat(q.borderBottomWidth);if((hh>0&&hh<=4&&q.backgroundColor!=='rgba(0, 0, 0, 0)'))out.push('filled '+Math.round(hh)+'px '+q.backgroundColor+' on '+e.tagName.toLowerCase()+'.'+[...e.classList].slice(0,2).join('.')+ps);else if(bw>=1&&q.borderTopStyle!=='none')out.push('border '+q.borderTopWidth+' '+q.borderTopColor+' on '+e.tagName.toLowerCase()+'.'+[...e.classList].slice(0,2).join('.')+ps)}
 const bi=s.backgroundImage;if(bi&&bi.startsWith('linear-gradient')&&r.width>100)out.push('drawn line '+bi.slice(0,60))}
return out}"""
def serve(d):
    H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();return s
async def grab(b,d,slug):
    s=serve(d);pg=await b.new_page(viewport={'width':1440,'height':900});await pg.goto('http://127.0.0.1:%d/%s/'%(s.server_address[1],slug),wait_until='load',timeout=60000)
    await pg.wait_for_timeout(2500);r=await pg.evaluate(JS);await pg.close();s.shutdown();return collections.Counter(r)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for item in sys.argv[1:]:
            slug,z,live=item.split('|');t=tempfile.mkdtemp(dir=os.path.dirname(__file__));zipfile.ZipFile(z).extractall(t)
            L=await grab(b,os.path.dirname(os.path.dirname(live)),slug);P=await grab(b,t,slug);shutil.rmtree(t,True)
            keys=sorted(set(L)|set(P));print('==',slug,'same' if L==P else 'DIFFERENT')
            for k in keys:
                if L[k]!=P[k]:print('   %-70s live %3d  page %3d'%(k,L[k],P[k]))
        await b.close()
asyncio.run(main())
