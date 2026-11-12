import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# F (owner: "F Swipe rows - yes"): from 641 px up the page is laid out as on a computer - no swipe rows, rows 150 high (shrinking to fit, her answer B), images beside text 120

css='''<style id="mm-ec-11nov-f">
/* 11 Nov 2026 (owner, F: "Swipe rows - yes"): at 641-830 px no swipe rows or dots; rows as on a computer */
@media (min-width:641px) and (max-width:830px){html body main .mm-row{display:flex !important;justify-content:center !important;overflow-x:visible !important;scroll-snap-type:none !important}html body main .mm-row .mm-imgs{display:contents !important}html body main .mm-row .mm-imgs .pim{height:var(--mmrh,150px) !important;width:auto !important}html body main section .mm-set .mm-imgs .pim:not(:has(img[data-full="images/100.jpg"])),html body main .mm-float .pim{height:120px !important;width:auto !important}html body main .mm-dots{display:none !important}}
</style>'''
rep('</body>',css+'</body>')
# E12 done properly: "Show and tell" joins the Storytelling section, so its text wraps beside the circle-time image
a='</section><section class="section" id="show-and-tell"><h2 class="mm-hc-0432FF" data-gap="48">Show and tell</h2>'
rep(a,'<h2 class="mm-hc-0432FF" data-gap="48" id="show-and-tell">Show and tell</h2>')
rep('@media (min-width:641px){html body main section#show-and-tell{clear:none !important}}','')
js=r'''
/* F (owner: "Swipe rows - yes"): at 641-830 px rows of images are 150 high, shrinking together to fit the line (her answer B), as on a computer */
if(W>640&&W<=830){[].forEach.call(document.querySelectorAll('main .mm-row'),function(r){var fs=[].slice.call(r.querySelectorAll('figure.ph'));if(!fs.length)return;var it=fs.map(function(f){var p=f.querySelector('.pim'),c=f.querySelector('figcaption.mm-cap:not(.mm-cap-below)'),cw=0;if(c){var rg=document.createRange();rg.selectNodeContents(c);cw=rg.getBoundingClientRect().width*18/(parseFloat(getComputedStyle(c).fontSize)||18);}return {ar:p?(parseFloat(p.style.aspectRatio)||1):0,cw:cw};});var gap=parseFloat(getComputedStyle(r).columnGap)||10,av=r.getBoundingClientRect().width-gap*(fs.length-1)-1,h=150;var capsum=0;it.forEach(function(x){capsum+=x.cw;});if(capsum>av*0.85){var sc=Math.max(0.7,av*0.85/capsum);fs.forEach(function(f){var c=f.querySelector('figcaption.mm-cap:not(.mm-cap-below)');if(c)S2(c,'font-size',(18*sc).toFixed(1)+'px','important');});it.forEach(function(x){x.cw*=sc;});}/* 12 Nov 2026 (owner: "have the name on one line"): captions never wrap - where the line is short they are set a little smaller, and the images shrink around them */for(var k=0;k<6;k++){var fixed=0,vari=0;it.forEach(function(x){if(x.cw>x.ar*h)fixed+=x.cw;else vari+=x.ar*h;});if(fixed+vari<=av||vari<=0)break;h=h*Math.max(0.2,(av-fixed)/vari);}S2(r,'--mmrh',Math.floor(h)+'px');});}/* captions over images count in the width (they stay on one line) */
'''
rep("\n};</script><script id=\"mm-one-spacing\">",js+"};</script><script id=\"mm-one-spacing\">")
open(f,'w').write(s);print('b8 ok')
