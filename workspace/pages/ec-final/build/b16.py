import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# Q3 divider between "...adults in the room." and "In the environments I have prepared"
rep('independent of the adults in the room.</p><p>In the environments I have prepared','independent of the adults in the room.</p><p class="mm-gl"></p><p>In the environments I have prepared')
# Q8 Large / Small Moveable Alphabet: italic, text colour
rep('<span class="mm-hc-EE0000">Large Moveable Alphabet </span>','<em>Large Moveable Alphabet</em> ')
rep('<span class="mm-hc-EE0000">Small Moveable Alphabet </span>','<em>Small Moveable Alphabet</em> ')
# Q10 attributions on the quotation's line; stray space removed
rep('for writing.”</p><cite>- Maria Montessori, <em>Montessori’s Own Handbook</em>, p. 96. (1965)</cite></blockquote>','for writing.” <span class="mm-attr">- Maria Montessori, <em>Montessori’s Own Handbook</em>, p. 96. (1965)</span></p></blockquote>')
rep('for writing. <strong>”</strong></p><cite>- Maria Montessori, <em>The Formation of Man,</em> p. 91. (1949)</cite></blockquote>','for writing.<strong>”</strong> <span class="mm-attr">- Maria Montessori, <em>The Formation of Man,</em> p. 91. (1949)</span></p></blockquote>')
# Q11 the drawing section: one paragraph; "Children typically begin..." below the row of images
a='that’s the only time they’re allowed to colour?</p><p data-gap="29">I have to confess'
rep(a,'that’s the only time they’re allowed to colour? I have to confess')
c=' Children typically begin with crayons, and a huge advantage of this kind of activity is that many of them are likely to have used crayons at home, and this familiarity makes it stress-free and thus an ideal lesson on their first morning in the room. After a few weeks they progress to using chalk -which is a little more complex as it necessitates having a presentation on cleaning the chalkboard- and eventually they inevitably gravitate towards using pencils. I encourage the children to take a sharpener when they take the pencils, and this gets them into the habit of writing with pencils that are sharp.'
rep('colouring pencils and sharpeners.'+c+'</p>','colouring pencils and sharpeners.</p>')
rep('<p class="centred mm-hc-0432FF" data-mma="50">A sample of some useless','<p data-gap="29">'+c.strip()+'</p><p class="centred mm-hc-0432FF" data-mma="50">A sample of some useless')
# Q15 Supplemental Language Album in italics everywhere
rep('Kate Millie’s Supplemental Language Album - ','Kate Millie’s <em>Supplemental Language Album</em> - ')
assert s.count('Supplemental Language Album')==3 and s.count('<em>Supplemental Language Album</em>')==3
# Q16 the four captions blue (and centred - CSS)
for t in ['The Blue Series','The Green Series','Action Cards - Set 2']:
    pass
i=s.find('data-full="images/145.jpg"'); r0=s.rfind('<div class="mm-row"',0,i); r1=s.find('<div class="mm-row"',i)
row=s[r0:r1]; n=row.count('mm-hc-EE0000'); assert n>=4,n
s=s[:r0]+row.replace('mm-hc-EE0000','mm-hc-0432FF')+s[r1:]
# Q17 divider above Early Readers; Q18 divider above Reading Analysis (the heading in the page)
rep('<section class="section" id="early-readers"><h2 class="mm-hc-0432FF" data-gap="48">Early Readers</h2>','<p class="mm-gl"></p><section class="section" id="early-readers"><h2 class="mm-hc-0432FF" data-gap="48">Early Readers</h2>')
i=s.find('<h2 class="mm-hc-0432FF" data-gap="48">Reading Analysis</h2>'); j=s.rfind('<section',0,i); assert i-j<120, s[j:i]
s=s[:j]+'<p class="mm-gl"></p>'+s[j:]
# Q21 red/blue words in Reading Analysis: the text colour
i=s.find('<h2 class="mm-hc-0432FF" data-gap="48">Reading Analysis</h2>'); j=s.find('<h2 class="mm-hc-EE0000"',i)
seg=s[i:j]; seg2=seg.replace('<span class="mm-hc-EE0000">red</span>','red').replace('<span class="mm-hc-0432FF">blue</span>','blue')
assert seg.count('<span class="mm-hc-EE0000">red</span>')==2 and seg.count('<span class="mm-hc-0432FF">blue</span>')==2
s=s[:i]+seg2+s[j:]
# Q22 native speaker in italics
rep('a 6-year-old native speaker of English','a 6-year-old <em>native speaker</em> of English')
# Q20 Symbol Box items to the left margin; Q19 Series label gap
for sb in ['symbol-box-1','symbol-box-2']:
    i=s.find('<section class="section" id="%s">'%sb); j=s.find('</section>',i)
    seg=s[i:j]; seg2=re.sub(r'<p([^>]*)><span class="mm-t">\t</span>',r'<p\1 class="mm-sbl">',seg)
    s=s[:i]+seg2+s[j:]
s=re.sub(r'<p class="mm-hanglab" data-gap="29"><span class="mm-lab mm-hc-0432FF">Series (\d)',r'<p class="mm-hanglab mm-ser" data-gap="29"><span class="mm-lab mm-hc-0432FF">Series \1',s)
assert s.count('mm-hanglab mm-ser')==5, s.count('mm-hanglab mm-ser')
css='''<style id="mm-ec-12nov-b">
/* 12 Nov 2026 (owner: "and centred above the image"): the four captions over The Blue Series ... Puzzle Words */
@media (min-width:831px){html body main .mm-row .mm-imgs:has(img[data-full="images/145.jpg"]) figcaption.mm-cap{text-align:center !important;left:50% !important;transform:translateX(-50%) !important;width:max-content !important}}@media (min-width:641px) and (max-width:830px){html body main .mm-row .mm-imgs:has(img[data-full="images/145.jpg"]) figcaption.mm-cap{text-align:center !important}}
/* 12 Nov 2026 (owner: "fix this gap"): Pinning - the text runs up to the image */
@media (min-width:641px){html body main .mm-set.mm-col:has(img[data-full="images/100.jpg"]) > .mm-text{max-width:calc(100% - 186px - 30px) !important;flex:1 1 auto !important}}
/* 12 Nov 2026 (owner: "make it 80"): the Materials image */
@media (min-width:641px){html body main .mm-float[data-mmbot] .pim{height:80px !important;width:auto !important}}
/* 12 Nov 2026 (owner: "make it 50"): the gap in the row of images 040-042 */
@media (min-width:831px){html body main .mm-row:has(img[data-full="images/041.jpg"]){gap:50px !important;column-gap:50px !important}}
/* 12 Nov 2026 (owner: "Reduce this gap so the text is vertically aligned"): Series 1-5, the name after a shorter gap, in one column */
html body main p.mm-hanglab.mm-ser{padding-left:5em !important;text-indent:-5em !important}html body main p.mm-hanglab.mm-ser .mm-lab{min-width:5em !important;width:5em !important;display:inline-block}
/* 12 Nov 2026 (owner: "all of the items in these lists - align to the left margin"): Symbol Box lists */
@media (min-width:641px){html body main p.mm-sbl{padding-left:0 !important;margin-left:0 !important;text-indent:0 !important;tab-size:12em}}
@media (max-width:640px){html body main section[id^="symbol-box"] p.mm-sbl{padding-left:0 !important}html body main section[id^="symbol-box"] p.mm-sbl > .mm-t{display:inline-block !important;width:1.2em !important;overflow:hidden;vertical-align:baseline}}
</style>'''
rep('</body>',css+'</body>')
# Introduction: 50 above (all red headings 50)
rep('<h2 class="mm-hc-EE0000" data-gap="48" data-mma="40" data-mmb="30" id="introduction">','<h2 class="mm-hc-EE0000" data-gap="48" data-mma="50" data-mmb="30" id="introduction">')
open(f,'w').write(s);print('b16 ok')
