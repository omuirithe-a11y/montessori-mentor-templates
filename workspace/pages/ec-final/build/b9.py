import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# fault 18: on phones each Letter Bingo caption stands over its own images
for n,cap in [('064','Letter Bingo: learning'),('066','Letter Bingo: teaching')]:
    i=s.find('data-full="images/%s.jpg"'%n); j=s.rfind('<figure class="ph"',0,i)
    s=s[:j]+'<figure class="ph" data-capph="%s"'%cap+s[j+len('<figure class="ph"'):]
css='''<style id="mm-ec-11nov-ph">
@media (max-width:640px){
/* fault 18: Letter Bingo - on phones each caption over its own images, in the swipe row */
html body main p.mm-twocap:has(+ .mm-row figure[data-capph]){display:none !important}
html body main figure[data-capph]{position:relative}html body main .mm-row:has(figure[data-capph]){margin-top:40px !important}
html body main figure[data-capph]::before{content:attr(data-capph);display:block;color:#0432FF;text-align:center;margin:0 0 6px;font-size:18px;line-height:1.3}
/* fault 19: lettered lines (a. b. c.) wrap under their own text, not under the letter */
html body main p.mm-tab1{padding-left:2.4em !important;text-indent:-2.4em !important}html body main p.mm-tab1>.mm-t{display:inline-block;width:1.5em;white-space:normal;font-size:inherit}
/* fault 19: Symbol Box lines - on phones the whole line is indented (wrapped lines stay under their text) and the name of the part follows after a clear space */
html body main section[id^="symbol-box"] p:has(> .mm-t:first-child){padding-left:2.6em !important;text-indent:0 !important}html body main section[id^="symbol-box"] p > .mm-t:first-child{display:none !important}html body main section[id^="symbol-box"] p > .mm-t ~ .mm-t{display:inline-block !important;width:1.2em !important;overflow:hidden;vertical-align:baseline}
/* fault 17 / A: the Writing Stages strip on phones - in the middle, a size that can be read */
html body main .mm-float[data-mmstrip]{float:none !important;display:flex;justify-content:center}html body main .mm-float[data-mmstrip] .pim{height:220px !important;width:49.6px !important}
}
</style>'''
rep('</body>',css+'</body>')
open(f,'w').write(s);print('b9 ok')
