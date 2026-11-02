# profile_scroll.py <zip> <width> : CPU profile while scrolling as speed_check.py does; prints the functions with the most self time
import sys, os, zipfile, tempfile, threading, http.server, functools, json, collections
from playwright.sync_api import sync_playwright
Z, W = sys.argv[1], int(sys.argv[2])
d=tempfile.mkdtemp(); zipfile.ZipFile(Z).extractall(d); slug=zipfile.ZipFile(Z).namelist()[0].split('/')[0]
H=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=d)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
url='http://127.0.0.1:%d/%s/'%(s.server_address[1],slug)
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':W,'height':900}); pg=c.new_page()
    pg.goto(url,wait_until='load'); pg.wait_for_timeout(4000)
    cdp=c.new_cdp_session(pg); cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval',{'interval':200}); cdp.send('Profiler.start')
    for y in range(0,pg.evaluate("document.documentElement.scrollHeight"),700): pg.mouse.wheel(0,700); pg.wait_for_timeout(1200)
    pg.wait_for_timeout(3000); prof=cdp.send('Profiler.stop')['profile']; b.close()
nodes={n['id']:n for n in prof['nodes']}; dt=collections.Counter()
ts=prof['timeDeltas']
for sid,delta in zip(prof['samples'],ts): dt[sid]+=delta
agg=collections.Counter()
for nid,t in dt.items():
    cf=nodes[nid]['callFrame']; key='%s line %d col %d'%(cf['functionName'] or '(anon)',cf['lineNumber']+1,cf['columnNumber']+1)
    if cf['functionName'] in ('(idle)','(program)','(root)'): continue
    agg[key]+=t
for k,v in agg.most_common(8): print('%7.0f ms  self  %s'%(v/1000,k))
par={}
for n in prof['nodes']:
    for ch in n.get('children',[]): par[ch]=n['id']
inc=collections.Counter()
for nid,t in dt.items():
    seen=set(); x=nid
    while x in nodes:
        cf=nodes[x]['callFrame']
        if cf['lineNumber']>=0 and cf['url']:
            key='%s line %d'%(cf['functionName'] or '(anon)',cf['lineNumber']+1)
            if key not in seen: inc[key]+=t; seen.add(key)
        x=par.get(x)
print('-- inclusive (page scripts):')
for k,v in inc.most_common(15): print('%7.0f ms  %s'%(v/1000,k))
