import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':1440,'height':900}); pg=c.new_page()
    pg.goto('https://montessorimentor.co.uk/aun-aprendo/',wait_until='load',timeout=120000); pg.wait_for_timeout(3000)
    for i in [3,14,26,38,50]:
        im=pg.locator('main img.doc-img').nth(i); im.scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
        full=pg.evaluate("e=>e.closest('[data-full]')?e.closest('[data-full]').dataset.full:(e.dataset.full||'')", im.element_handle())
        t=time.time(); im.click()
        try:
            pg.wait_for_function("()=>{const i=document.querySelector('.lightbox img, .lb-frame img');return i&&i.complete&&i.naturalWidth>0&&getComputedStyle(document.querySelector('.lightbox')).display!=='none'&&!/-960\\./.test(i.currentSrc)}",timeout=30000)
            r=pg.evaluate("()=>{const i=document.querySelector('.lightbox img, .lb-frame img');return [i.currentSrc.split('/').pop(),i.naturalWidth]}")
            print('image',i+1,'opened full size in',round(time.time()-t,2),'s',r)
        except Exception as e: print('image',i+1,'did not open within 30 s', str(e)[:80])
        pg.keyboard.press('Escape'); pg.wait_for_timeout(800)
    b.close()
