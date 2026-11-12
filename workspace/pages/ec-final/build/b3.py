import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
rep('<span class="mm-hc-0432FF">blue </span>(vowels)','<span class="mm-hc-0445B3">blue </span>(vowels)')
rep('<p data-gap="29"><span class="mm-hc-0432FF">The Blue Series </span>','<p data-gap="29"><span class="mm-hc-0445B3">The Blue Series </span>')
i=s.find('>Blue Language Materials</p>'); j=s.rfind('<p class="mm-hc-0432FF"',0,i); assert i-j<60
s=s[:j]+'<p class="mm-hc-0445B3"'+s[j+len('<p class="mm-hc-0432FF"'):]
css='''<style id="mm-ec-11nov">
/* 11 Nov 2026 (owner): the pink, blue and green of the sandpaper letters ("the green to be used here and wherever green is used on this page is the green of the green sandpaper letters ... same for pink and blue"), taken from the page's images of the letters */
html body main .mm-hc-FF40FF:not(h2){color:#C6304F !important}html body main .mm-hc-2AB116{color:#038F45 !important}html body main .mm-hc-0445B3{color:#0445B3 !important}
/* 11 Nov 2026 (owner: "make this arrow more stylish. the > is too big and ugly"): a thin line with a small open arrowhead */
main .mm-arw{display:inline-block;position:relative;width:2.4em;height:1px;background:currentColor;vertical-align:.32em;margin:0 .35em}
main .mm-arw::after{content:"";position:absolute;right:0;top:-3.5px;width:7px;height:7px;border-top:1px solid currentColor;border-right:1px solid currentColor;transform:rotate(45deg);transform-origin:center}
main .mm-vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* 11 Nov 2026 (owner: "Fix the spacing after the numbers - it's way too big. compared with the PDF"): Kate Millie's list 3.1-3.17, the number column as in the PDF */
@media (min-width:641px){main p.mm-hanglab.mm-knum{padding-left:4em !important;text-indent:-4em !important}main p.mm-hanglab.mm-knum .mm-lab{min-width:4em}}
</style>'''
rep('</body>',css+'</body>')
open(f,'w').write(s);print('b3 ok')
