import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
rep('<ol><li data-gap="20">I-Spy</li>','<ol class="mm-boldnum"><li data-gap="20">I-Spy</li>')
rep('<figure class="ph mm-cf" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.35747"><img alt="" class="doc-img" data-full="images/152.jpg"','<figure class="ph mm-cf mm-capone" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.35747"><img alt="" class="doc-img" data-full="images/152.jpg"')
css='''<style id="mm-ec-11nov-g">
/* fault 6: the numbers of the list "1. I-Spy ... 5. Reading" are bold, as in the PDF */
html body main ol.mm-boldnum>li::marker{font-weight:700}html body main ol.mm-boldnum>li::before{font-weight:700 !important}
/* fault 22: the caption "Maria Montessori, 1950, Perugia." on one line, ending at the right edge of its image */
@media (min-width:641px){html body main figure.mm-capone{display:flex !important;flex-direction:column;align-items:flex-end}html body main figure.mm-capone>figcaption{white-space:nowrap !important;width:max-content !important;max-width:none !important;text-align:right !important}}
/* fault 14: images beside text are 120 high (her rule), also where two or three stand together (Object Box 1, Action Cards - Set 1) */
@media (min-width:641px){html body main section .mm-set.mm-col .mm-imgs .pim:not(:has(img[data-full="images/100.jpg"])){height:120px !important}}
</style>'''
rep('</body>',css+'</body>')
a="function align(){if(innerWidth<641)return;[].forEach.call(document.querySelectorAll('main .mm-float'),function(f){if(f.closest('blockquote')||getComputedStyle(f).cssFloat==='none')return;"
assert s.count(a)==1
s=s.replace(a,a+"if(f.classList.contains('mm-wsf'))return;/* Word Study: spread down the side as in the PDF (owner: yes) */")
a2="if(f.hasAttribute('data-mmbot'))return;/* 11 Nov: placed by its bottom (owner) */"
assert s.count(a2)==2
s=s.replace(a2,"if(f.hasAttribute('data-mmbot')||f.classList.contains('mm-wsf'))return;/* 11 Nov: placed by its bottom, or spread as the PDF (owner) */")
s=s.replace("@media (min-width:641px){html body main .mm-float.mm-wsf{clear:right !important}}","@media (min-width:641px){html body main .mm-float.mm-wsf{clear:right !important}html body main .mm-float.mm-wsf ~ .mm-float.mm-wsf{margin-top:30px !important}}")
open(f,'w').write(s);print('b10 ok')
