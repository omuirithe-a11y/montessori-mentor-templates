import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
rep('Birmingham%20conference%202018%20draft.pdf" rel="noopener" target="_blank">PDF</a>','Birmingham%20conference%202018%20draft.pdf" rel="noopener" target="_blank" class="mm-nou">PDF</a>')
css='''<style id="mm-ec-11nov-d">
/* 11 Nov 2026 (owner: "increase the gap between those four images to make clearer separation between them"); captions start at the left of their image, as the PDF (fault 10) */
@media (min-width:831px){html body main .mm-row .mm-imgs:has(img[data-full="images/145.jpg"]) figcaption.mm-cap{white-space:nowrap !important}}@media (min-width:641px){html body main .mm-row .mm-imgs:has(img[data-full="images/145.jpg"]) figcaption.mm-cap{text-align:left !important;width:auto !important;left:0 !important;transform:none !important}}@media (min-width:641px) and (max-width:830px){html body main .mm-row:has(img[data-full="images/145.jpg"]){gap:36px !important;column-gap:36px !important}html body main .mm-row figure.mm-cf>figcaption.mm-cap{white-space:nowrap !important;width:auto !important}}
/* 11 Nov 2026 (owner: "when I scroll over the contents that blue line shouldn't appear, but the word should turn blue") */
html body .toc a:hover,html body .toc-groups a:hover,html body .toc a:focus-visible{color:#0432FF !important;border-bottom-color:transparent !important;text-decoration:none !important;box-shadow:none !important}html body .toc li:hover{border-bottom-color:transparent !important;box-shadow:none !important}
/* the PDF link after Frierson is not underlined, as in the PDF (fault 11) */
html body main a.mm-nou{text-decoration:none !important;border-bottom:0 !important}
/* 11 Nov 2026 (owner: "centre that grid of 6 photos on the space, as they are approximately centred on the PDF"); the two rows line up (fault 20) */
@media (min-width:641px){html body main .mm-grid3 > .mm-imgs{display:grid !important;grid-template-columns:repeat(3,auto) !important;column-gap:24px !important;row-gap:24px !important;justify-content:center !important;justify-items:center !important;flex:none !important;width:auto !important}html body main .mm-grid3 > .mm-imgs > figure{margin:0 !important}}
</style>'''
rep('</body>',css+'</body>')
js=r'''
/* the four images (Blue Series ... Puzzle Words): wider gaps (owner), as wide as the line allows, up to 72 */
var f4=document.querySelector('main img[data-full="images/145.jpg"]'),r4=f4&&f4.closest('.mm-row');if(r4&&W>830){var fs4=[].slice.call(r4.querySelectorAll('figure.ph')),sw=0;fs4.forEach(function(x){sw+=x.getBoundingClientRect().width;});var av4=r4.getBoundingClientRect().width,g4=Math.min(72,Math.floor((av4-sw)/(fs4.length-1)));if(g4>0){S2(r4,'gap',g4+'px','important');S2(r4,'column-gap',g4+'px','important');}}
/* the grid of 6 reading images: centred in the space between the list and the right margin */
var g3=document.querySelector('main .mm-grid3');if(g3&&W>640){var ti=g3.querySelector('.mm-text'),gi=g3.querySelector('.mm-imgs');if(ti&&gi){var mlx=0,rg3=document.createRange();[].forEach.call(ti.querySelectorAll('p'),function(pp){rg3.selectNodeContents(pp);[].forEach.call(rg3.getClientRects(),function(q){if(q.width>1)mlx=Math.max(mlx,q.right);});});var mrx=g3.getBoundingClientRect().right,gr=gi.getBoundingClientRect(),cur=parseFloat(gi.style.marginRight)||0;if(mlx){var want=mrx-((mlx+mrx)/2+gr.width/2);S2(gi,'margin-right',Math.max(0,want).toFixed(1)+'px','important');S2(gi,'margin-left','auto','important');}}}
'''
rep("\n};</script><script id=\"mm-one-spacing\">",js+"};</script><script id=\"mm-one-spacing\">")
open(f,'w').write(s);print('b7 ok')
s=open(f).read()
a='<span class="mm-hc-EE0000">Action Cards </span>'
assert s.count(a)==1
s=s.replace(a,'<span class="mm-hc-0432FF">Action Cards </span>');open(f,'w').write(s);print('b7b ok')
