import sys,collections
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':1440,'height':900});pg=c.new_page()
  cdp=c.new_cdp_session(pg);cdp.send('Profiler.enable');cdp.send('Profiler.setSamplingInterval',{'interval':500})
  pg.goto(sys.argv[1],wait_until='load',timeout=90000);pg.wait_for_timeout(4000)
  cdp.send('Profiler.start')
  H=pg.evaluate("document.documentElement.scrollHeight")
  for y in range(0,H,700): pg.mouse.wheel(0,700);pg.wait_for_timeout(1200)
  prof=cdp.send('Profiler.stop')['profile']
  nodes={n['id']:n for n in prof['nodes']};dt=collections.Counter();cnt=collections.Counter()
  for sid,d in zip(prof['samples'],prof['timeDeltas']): dt[sid]+=d
  self_=collections.Counter()
  for i,us in dt.items():
    cf=nodes[i]['callFrame'];k='%s line %d (%s)'%(cf['functionName'] or '(anon)',cf['lineNumber']+1,cf['url'].split('/')[-2] or cf['url'][-20:]) if cf['url'] else cf['functionName']
    self_[k]+=us
  # inclusive time per function: walk parents
  parent={}
  for n in prof['nodes']:
    for ch in n.get('children',[]): parent[ch]=n['id']
  inc=collections.Counter()
  for i,us in dt.items():
    seen=set();j=i
    while j in nodes:
      cf=nodes[j]['callFrame']
      if cf['url']:
        k='%s line %d'%(cf['functionName'] or '(anon)',cf['lineNumber']+1)
        if k not in seen: inc[k]+=us;seen.add(k)
      j=parent.get(j)
  print('SELF (ms):');[print('  %7.0f'%(v/1000),k) for k,v in self_.most_common(12)]
  print('INCLUDING CALLS (ms), page scripts only:');[print('  %7.0f'%(v/1000),k) for k,v in inc.most_common(15)]
  b.close()
