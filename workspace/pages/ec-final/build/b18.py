import sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# Q6 (owner: "centre that photo"): image 052 beside the list "1. I-Spy ... 5. Reading"
i=s.find('data-full="images/052.jpg"'); j=s.rfind('<div class="mm-float">',0,i); assert i-j<300
s=s[:j]+'<div class="mm-float" data-mmctr="1">'+s[j+len('<div class="mm-float">'):]
js=r'''
/* 12 Nov 2026 (owner: "centre that photo"): image 052 in the middle of the space between the list beside it and the right margin */
var cf=document.querySelector('main .mm-float[data-mmctr]');if(cf&&W>640){var ol=cf.nextElementSibling,mx=0,rgc=document.createRange();if(ol){[].forEach.call(ol.querySelectorAll('li'),function(li){rgc.selectNodeContents(li);[].forEach.call(rgc.getClientRects(),function(q){if(q.width>1)mx=Math.max(mx,q.right);});});var rr=cf.parentElement.getBoundingClientRect().right,pw=cf.querySelector('.pim').getBoundingClientRect().width;if(mx){var mm=rr-((mx+rr)/2+pw/2);if(mm>0)S2(cf,'margin-right',mm.toFixed(1)+'px','important');}}}
/* 12 Nov 2026 (owner: "halve the gap between photos 1 + 2 and between 3+4, with the saved space going between photos 2 + 3"): Letter Bingo */
var bi=document.querySelector('main img[data-full="images/064.jpg"]'),brow=bi&&bi.closest('.mm-row');if(brow&&W>640){var bf=brow.querySelectorAll('figure.ph');if(bf.length===4){var bg=parseFloat(getComputedStyle(brow).columnGap)||parseFloat(getComputedStyle(bi.closest('.mm-imgs')).columnGap)||38;S2(bf[1],'margin-left',(-bg/2).toFixed(1)+'px','important');S2(bf[3],'margin-left',(-bg/2).toFixed(1)+'px','important');}}
'''
rep("\n};</script><script id=\"mm-one-spacing\">",js+"};</script><script id=\"mm-one-spacing\">")
css='''<style id="mm-ec-12nov-c">/* 12 Nov 2026 (owner: "the photos need to align on the right, as they do on the left"): the grid of 6 - left images on their left edges, right images on their right edges, middle ones centred */
@media (min-width:641px){html body main .mm-grid3 > .mm-imgs > figure:nth-child(3n+1){justify-self:start !important}html body main .mm-grid3 > .mm-imgs > figure:nth-child(3n){justify-self:end !important}html body main .mm-grid3 > .mm-imgs > figure:nth-child(3n+2){justify-self:center !important}}</style>'''
rep('</body>',css+'</body>')
open(f,'w').write(s);print('b18 ok')
