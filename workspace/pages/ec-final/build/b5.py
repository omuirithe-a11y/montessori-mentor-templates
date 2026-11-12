import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# E15: the Materials image: its bottom level with the last line of its text
i=s.index('<section class="section" id="materials">'); j=s.index('<div class="mm-float">',i); assert j-i<200
s=s[:j]+'<div class="mm-float" data-mmbot="1">'+s[j+len('<div class="mm-float">'):]
rep("for(var k=0;k<4;k++){var t=capTop(p);if(t===null)break;var d=t-pim.getBoundingClientRect().top;",
    "for(var k=0;k<4;k++){var t=capTop(p);if(t===null)break;var d=f.hasAttribute('data-mmbot')?(function(){var tl=txt(p),bb=-1e9;tl.forEach(function(x){bb=Math.max(bb,base(x));});return bb-pim.getBoundingClientRect().bottom;})():(t-pim.getBoundingClientRect().top);/* 11 Nov (owner: \"move the photo up so the bottom of photo = bottom of lowest line of text\") */")
# extra layout run before the spacing in every pass
rep("function run(){window.__mmOneRuns=(window.__mmOneRuns||0)+1;MW=new WeakMap();mine=true;try{",
    "function run(){window.__mmOneRuns=(window.__mmOneRuns||0)+1;MW=new WeakMap();mine=true;try{if(window.__mmEcExtra)window.__mmEcExtra();")
js=r'''<script id="mm-ec-11nov-js">/* 11 Nov 2026 (owner), The English Curriculum: layouts the template has no rule for */
function S2(e,k,v,p){var o=e.style.getPropertyValue(k);if(e.style.getPropertyPriority(k)===(p||'')){if(o===v)return;if(/px$/.test(o)&&/px$/.test(v)&&Math.abs(parseFloat(o)-parseFloat(v))<0.6)return;}e.style.setProperty(k,v,p);}/* only a real change is written, so the page's observers are not woken for nothing */
window.__mmEcExtra=function(){var W=innerWidth;
/* Letter Bingo (owner: "move photos 1 + 2 to the left margin, move photos 3 + 4 to the [right] margin, keep the existing gap between 1/2 and 3/4, allow the gap between 2 and 3 to grow"); each caption over its pair */
var im=document.querySelector('main img[data-full="images/064.jpg"]'),row=im&&im.closest('.mm-imgs'),cap=row&&row.closest('.mm-row').previousElementSibling;
if(row&&W>640){var fg=row.querySelectorAll(':scope > figure');if(fg.length===4){S2(row,'justify-content','flex-start','important');S2(row,'width','100%','important');S2(fg[0],'margin-left','0','important');S2(fg[3],'margin-right','0','important');S2(fg[1],'margin-right','auto','important');
 if(cap&&cap.matches('p.mm-twocap')){var sp=cap.querySelectorAll(':scope > span');if(sp.length===2){S2(cap,'display','block','important');var pl=cap.getBoundingClientRect().left;var c1=(fg[0].getBoundingClientRect().left+fg[1].getBoundingClientRect().right)/2,c2=(fg[2].getBoundingClientRect().left+fg[3].getBoundingClientRect().right)/2;
 [].forEach.call(sp,function(x){S2(x,'display','inline-block','important');S2(x,'text-align','left','important');});
 var w1=sp[0].getBoundingClientRect().width,w2=sp[1].getBoundingClientRect().width;var m1=c1-w1/2-pl,m2=c2-w2/2-(pl+m1+w1);S2(sp[0],'margin-left',m1.toFixed(1)+'px','important');S2(sp[1],'margin-left',m2.toFixed(1)+'px','important');}}}}
};</script>'''
rep('<script id="mm-one-spacing">',js+'<script id="mm-one-spacing">')
css='''<style id="mm-ec-11nov-b">
/* 11 Nov 2026 (owner: "fix this large spacing gap"): "Show and tell" beside the circle-time image, as in the PDF */
@media (min-width:641px){html body main section#show-and-tell{clear:none !important}}
/* 11 Nov 2026 (owner: "make this photo 80 high"): the pin tools image */
@media (min-width:641px){html body main .pim:has(> img[data-full="images/100.jpg"]){height:80px !important;width:186px !important}}
</style>'''
rep('</body>',css+'</body>')
open(f,'w').write(s);print('b5 ok')
s=open(f).read()
a="var mt=(parseFloat(getComputedStyle(f).marginTop)||0)+d;if(mt<0)break;"
assert s.count(a)==1
s=s.replace(a,"var mt=(parseFloat(getComputedStyle(f).marginTop)||0)+d;if(mt<0&&!f.hasAttribute('data-mmbot'))break;")
open(f,'w').write(s);print('b5b ok')

s=open(f).read()
a="if(Math.abs(d)<0.5)break;var sp=f.previousElementSibling;if(sp&&sp.classList.contains('mm-fspacer')){"
assert s.count(a)==1
s=s.replace(a,"if(Math.abs(d)<0.5)break;var sp=f.previousElementSibling;if(sp&&sp.classList.contains('mm-fspacer')&&f.hasAttribute('data-mmbot')&&sp.style.height!=='0px'){sp.style.height='0px';CH++;continue;}if(sp&&sp.classList.contains('mm-fspacer')&&!f.hasAttribute('data-mmbot')){")
open(f,'w').write(s);print('b5c ok')
s=open(f).read()
a="var ims=f.querySelectorAll('.pim');if(!ims.length)return;"
assert s.count(a)==2
s=s.replace(a,"if(f.hasAttribute('data-mmbot'))return;/* 11 Nov: placed by its bottom (owner) */"+a)
open(f,'w').write(s);print('b5d ok')
