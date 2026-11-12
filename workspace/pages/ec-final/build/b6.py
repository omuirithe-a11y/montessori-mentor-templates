import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# E16: the same gap before every "I Spy"
rep('sound:<span class="mm-t mm-t-mid"> \t\t</span><em>“I Spy','sound:<span class="mm-ispy"></span><em>“I Spy')
rep('sound.<span class="mm-t mm-t-mid"> \t</span><em>“I Spy','sound.<span class="mm-ispy"></span><em>“I Spy',2)
# typos (fault 21)
rep('Puzzle Words（Sight Words）','Puzzle Words (Sight Words)')
rep('easily confused.“','easily confused.”')
# A: the Writing Stages image becomes a tall strip beside the list and the paragraph below it (as the PDF)
FL_open='<div class="mm-float"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:0.22556"><img alt="" class="doc-img" data-full="images/112.jpg" loading="lazy" src="images/112-480.jpg"/></div></figure></div></div>'
rep(FL_open,'')
rep('<h2 class="mm-hc-0432FF" data-gap="48">Writing Stages</h2>','<h2 class="mm-hc-0432FF" data-gap="48">Writing Stages</h2>'+FL_open.replace('<div class="mm-float">','<div class="mm-float" data-mmstrip="1">').replace('src="images/112-480.jpg"','src="images/112-1000.jpg"'))
# E37: Word Study - each card image beside its own rows (as the PDF)
i=s.find('id="word-study"');j=s.find('<div class="mm-float">',i);k=s.find('<p class="mm-hanglab"',j)
blk=s[j:k]
figs=re.findall(r'<figure class="ph".*?</figure>',blk)
assert len(figs)==3
mk=lambda fg:'<div class="mm-float mm-wsf"><div class="mm-imgs">'+fg+'</div></div>'
s=s[:j]+mk(figs[0])+s[k:]
g=s.find('<span class="mm-hc-0432FF">Gender</span>',i); gp=s.rfind('<p class="mm-hanglab"',0,g)
s=s[:gp]+mk(figs[1])+s[gp:]
a=s.find('<span class="mm-hc-0432FF">Antonyms</span>',i); ap=s.rfind('<p class="mm-hanglab"',0,a)
s=s[:ap]+mk(figs[2])+s[ap:]
# E38: grammar symbols image beside Series 1
i=s.find('<span class="mm-hc-0432FF">Subject and Verb</span>');j=s.find('<div class="mm-float">',i);assert j-i<100
s=s[:j]+'<div class="mm-float" data-mmgram="1">'+s[j+len('<div class="mm-float">'):]
css='''<style id="mm-ec-11nov-c">
/* 11 Nov 2026 (owner: "The gap before I Spy needs to be consistent. match the smaller gap used in the second two examples") */
main .mm-ispy{display:inline-block;width:2.6em}
/* Word Study images: each beside its own rows, spread down the right with clear gaps (owner, with the PDF: "yes") */
@media (min-width:641px){html body main .mm-float.mm-wsf{clear:right !important}}
</style>'''
rep('</body>',css+'</body>')
# JS: strip height, grammar image size and place
js_add=r'''
/* A (owner: "make it larger"; PDF: a tall strip beside the list and the paragraph below it): the strip runs from the top of the first list line to the last line of the paragraph */
var st=document.querySelector('main .mm-float[data-mmstrip] .pim');if(st&&W>640){var sec=st.closest('section'),wc=sec.querySelector('.mm-wcols2'),pa=wc&&wc.nextElementSibling;if(pa){var rg=document.createRange();rg.selectNodeContents(pa);var rs=rg.getClientRects(),lb=rs.length?rs[rs.length-1].bottom:null;var top=st.getBoundingClientRect().top;if(lb){var h=Math.max(120,lb-8-top);S2(st,'height',h.toFixed(1)+'px','important');S2(st,'width',(h*0.22556).toFixed(1)+'px','important');S2(st,'max-height','none','important');}}}
/* E38 (owner, with the PDF: "yes"): the grammar symbols image larger, in the middle of the space right of the Series 1 lines */
var gm=document.querySelector('main .mm-float[data-mmgram]');if(gm&&W>640){var gp=gm.querySelector('.pim'),ar=parseFloat(gp.style.aspectRatio)||1.34,gh=150;S2(gp,'height',gh+'px','important');S2(gp,'width',(gh*ar).toFixed(1)+'px','important');S2(gp,'max-height','none','important');
 var mr=gm.parentElement.getBoundingClientRect().right,ml=0,n=gm.nextElementSibling;while(n&&!(n.matches('p.mm-hanglab'))){var r3=document.createRange();r3.selectNodeContents(n);[].forEach.call(r3.getClientRects(),function(q){if(q.width>1)ml=Math.max(ml,q.right);});n=n.nextElementSibling;}
 if(ml){var c=(ml+mr)/2,wd=gh*ar,m=mr-(c+wd/2);if(m>0)S2(gm,'margin-right',m.toFixed(1)+'px','important');}}
'''
rep("\n};</script><script id=\"mm-one-spacing\">",js_add+"};</script><script id=\"mm-one-spacing\">")
open(f,'w').write(s);print('b6 ok')
