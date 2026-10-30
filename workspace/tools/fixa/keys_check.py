import sys
from playwright.sync_api import sync_playwright
U=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':900}); pg.goto(U,wait_until='load'); pg.wait_for_timeout(2500)
    seq=[]
    for i in range(12):
        pg.keyboard.press('Tab'); pg.wait_for_timeout(120)
        seq.append(pg.evaluate("(()=>{const e=document.activeElement;const r=e.getBoundingClientRect();return [e.tagName,(e.className||'').toString().slice(0,20),(e.textContent||'').trim().slice(0,25),(e.getAttribute('href')||''),getComputedStyle(e).visibility!='hidden'&&r.width>0]})()"))
    first=seq[0]; print('Tab 1:',first)
    pg.goto(U,wait_until='load'); pg.wait_for_timeout(2000); pg.keyboard.press('Tab'); pg.keyboard.press('Enter'); pg.wait_for_timeout(800)
    print('after Enter on the first link: focus in/at main =',pg.evaluate("(()=>{const m=document.querySelector('main');return m===document.activeElement||m.contains(document.activeElement)||location.hash})()"),'| scrollY',pg.evaluate('scrollY'))
    print('Tabs 2-12:',[s[:3] for s in seq[1:]]); print('any focused element invisible:',[s for s in seq if not s[4]])
    b.close()
