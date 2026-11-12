import sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# 12 Nov (owner: "These are photos of the Language area in my classroom in Taipei - spacing 50 above")
rep('<p>These are photos of the Language area','<p data-mma="50">These are photos of the Language area')
# 12 Nov (owner: "lowest image = with the bottom of the line A single card with a list of compound words. then make the space between the three images the same")
rep('A single card with a list of compound words.</p>','A single card with a list of compound words.</p>'.replace('<','<',1)) if False else None
i=s.find('A single card with a list of compound words.</p>'); j=s.rfind('<p class="mm-hanglab"',0,i)
s=s[:j]+'<p class="mm-hanglab mm-wslast"'+s[j+len('<p class="mm-hanglab"'):]
js=r'''
/* 12 Nov 2026 (owner): Word Study - the top image level with the first line, the lowest image's bottom level with the last line ("A single card with a list of compound words."), equal gaps between the three */
var wf=[].slice.call(document.querySelectorAll('main .mm-float.mm-wsf'));if(wf.length===3&&W>640){var lastp=document.querySelector('main p.mm-wslast'),firstp=wf[0].nextElementSibling;while(firstp&&!firstp.matches('p'))firstp=firstp.nextElementSibling;if(lastp&&firstp){var rq=document.createRange();rq.selectNodeContents(firstp);var r1=[].slice.call(rq.getClientRects()).filter(function(q){return q.width>1;})[0];rq.selectNodeContents(lastp);var rl=[].slice.call(rq.getClientRects()).filter(function(q){return q.width>1;});var lb=rl[rl.length-1];if(r1&&lb){var cvx=document.createElement('canvas').getContext('2d'),st1=getComputedStyle(firstp),stl=getComputedStyle(lastp);cvx.font=st1.fontStyle+' '+st1.fontWeight+' '+st1.fontSize+' '+st1.fontFamily;var mm1=cvx.measureText('H');var T=r1.top+(r1.height-(mm1.fontBoundingBoxAscent+mm1.fontBoundingBoxDescent))/2+mm1.fontBoundingBoxAscent-mm1.actualBoundingBoxAscent;cvx.font=stl.fontStyle+' '+stl.fontWeight+' '+stl.fontSize+' '+stl.fontFamily;var mm2=cvx.measureText('H');var B=lb.top+(lb.height-(mm2.fontBoundingBoxAscent+mm2.fontBoundingBoxDescent))/2+mm2.fontBoundingBoxAscent;
 var hs=wf.map(function(x){return x.querySelector('.pim').getBoundingClientRect().height;}),g=Math.max(10,(B-T-hs[0]-hs[1]-hs[2])/2);
 var p0=wf[0].querySelector('.pim').getBoundingClientRect().top,m0=parseFloat(getComputedStyle(wf[0]).marginTop)||0;wf.forEach(function(x){S2(x,'margin-bottom','0px','important');});S2(wf[0],'margin-top',(m0+T-p0).toFixed(1)+'px','important');S2(wf[1],'margin-top',g.toFixed(1)+'px','important');S2(wf[2],'margin-top',g.toFixed(1)+'px','important');}}}
'''
rep("\n};</script><script id=\"mm-one-spacing\">",js+"};</script><script id=\"mm-one-spacing\">")
a="if(s2.matches('.mm-float')&&!s2.matches('.mm-taipei,.mm-perugia')&&"
assert s.count(a)==1
s=s.replace(a,"if(s2.matches('.mm-float')&&!s2.matches('.mm-taipei,.mm-perugia,.mm-wsf')&&")
s=s.replace('</body>','<style id="mm-ec-12nov-e">@media (min-width:641px){html body main#content section .mm-float.mm-wsf,html body main section .mm-float.mm-wsf{float:right !important;clear:right !important}}</style></body>',1)
open(f,'w').write(s);print('b20 ok')
s=open(f).read()
# the first Word Study image goes before the "Word Study" heading, so it reaches the first line with a positive margin (a negative one let the first line run under it at 831-980)
i=s.find('<h2 class="mm-hc-0432FF" data-gap="48">Word Study</h2><div class="mm-float mm-wsf">')
assert i>0
j=i+len('<h2 class="mm-hc-0432FF" data-gap="48">Word Study</h2>')
k=s.find('</div></div>',j)+len('</div></div>')
fl=s[j:k]; assert fl.startswith('<div class="mm-float mm-wsf">') and fl.count('<figure')==1
s=s[:i]+fl+'<h2 class="mm-hc-0432FF" data-gap="48">Word Study</h2>'+s[k:]
open(f,'w').write(s);print('b20c ok')
