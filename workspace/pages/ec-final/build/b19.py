import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# A: the Taipei paragraph wraps under its two images (owner: "yes")
i=s.find('<div class="mm-set mm-col" data-h="120"><div class="mm-text"><p>These are photos of the Language area')
end=s.find('</figure></div></div>',i)+len('</figure></div></div>')
blk=s[i:end]
m=re.match(r'<div class="mm-set mm-col" data-h="120"><div class="mm-text">(.*?)</div>(<div class="mm-imgs">.*</div>)</div>$',blk,re.S)
assert m and m.group(2).count('<figure')==2 and '<p' not in m.group(2)
s=s[:i]+'<div class="mm-float mm-taipei">'+m.group(2)+'</div>'+m.group(1)+s[end:]
# B: the two Sound Game "I Spy" quotations take 30 (owner: "do not apply the 40/40 rule to the quotations in this section")
rep('<blockquote class="pullquote" data-gap="20"><p>“I Spy with my little eye, something in this room <u>containing</u>','<blockquote class="pullquote" data-gap="20" data-mma="30" data-mmb="30"><p>“I Spy with my little eye, something in this room <u>containing</u>')
i=s.find('something in this room containing the <u>sounds</u>');j=s.rfind('<blockquote class="pullquote"',0,i);assert i-j<120
s=s[:j]+'<blockquote class="pullquote" data-mma="30" data-mmb="30"'+s[j+len('<blockquote class="pullquote"'):]
# C: "graphemes." in the column of the two definitions
rep('<p data-gap="29">Phonemes <span class="mm-arw" aria-hidden="true"></span><span class="mm-vh"> to </span> graphemes.</p>','<p class="mm-hanglab" data-gap="29"><span class="mm-lab mm-arwlab">Phonemes <span class="mm-arw" aria-hidden="true"></span><span class="mm-vh"> to </span></span>graphemes.</p>')
# E, F, J, L: dividers
rep('<section class="section" id="the-moveable-alphabets">','<p class="mm-gl"></p><section class="section" id="the-moveable-alphabets">')
rep('<section class="section" id="reinforcement-of-letters">','<p class="mm-gl"></p><section class="section" id="reinforcement-of-letters">')
rep('</p></blockquote><p>However, on the language shelves','</p></blockquote><p class="mm-gl"></p><p>However, on the language shelves')
rep('<li data-gap="20">Glue</li></ul></div></div><blockquote class="pullquote" data-gap="29"><p><strong>“</strong>We thus began','<li data-gap="20">Glue</li></ul></div></div><p class="mm-gl"></p><blockquote class="pullquote" data-gap="29"><p><strong>“</strong>We thus began')
# G: the handwriting list in one column
rep('<div class="mm-wcols2" data-gap="29"><div><ul><li data-space="29">relax the arm, hand and fingers</li><li data-gap="20">control pressure on the pencil</li><li data-gap="20">work in a limited space</li><li data-gap="20">turn the wrist to guide the pencil</li></ul></div><div><ul><li data-space="20">make continuous strokes</li><li data-gap="20">make up and down strokes</li><li data-gap="20">move from left to right</li></ul></div></div>',
    '<ul data-gap="29" class="mm-onecol"><li data-space="29">relax the arm, hand and fingers</li><li data-gap="20">control pressure on the pencil</li><li data-gap="20">work in a limited space</li><li data-gap="20">turn the wrist to guide the pencil</li><li data-gap="20">make continuous strokes</li><li data-gap="20">make up and down strokes</li><li data-gap="20">move from left to right</li></ul>')
# H: Preparation lists - dashes under the headings
rep('<section class="section" id="preparation-of-the-mind"><div class="mm-wcols2" data-gap="48">','<section class="section" id="preparation-of-the-mind"><div class="mm-wcols2 mm-prep" data-gap="48">')
# I: attributions back on their own lines (the stray space stays removed)
rep('for writing.” <span class="mm-attr">- Maria Montessori, <em>Montessori’s Own Handbook</em>, p. 96. (1965)</span></p></blockquote>','for writing.”</p><cite>- Maria Montessori, <em>Montessori’s Own Handbook</em>, p. 96. (1965)</cite></blockquote>')
rep('for writing.<strong>”</strong> <span class="mm-attr">- Maria Montessori, <em>The Formation of Man,</em> p. 91. (1949)</span></p></blockquote>','for writing.<strong>”</strong></p><cite>- Maria Montessori, <em>The Formation of Man,</em> p. 91. (1949)</cite></blockquote>')
# K: drawing section order
i=s.find('colouring pencils and sharpeners.</p>')+len('colouring pencils and sharpeners.</p>'); j=s.find('</section>',i); seg=s[i:j]
rows=re.findall(r'<div class="mm-row" data-above="40" data-level="1[67]">.*?(?=<div class="mm-row"|<p |$)',seg,re.S)
assert len(rows)==3, len(rows)
crayon,e1,e2=rows
para=re.search(r'<p data-gap="29">Children typically begin.*?</p>',seg,re.S).group(0)
cap=re.search(r'<p class="centred mm-hc-0432FF" data-mma="50">A sample of.*?</p>',seg,re.S).group(0)
assert len(crayon)+len(para)+len(cap)+len(e1)+len(e2)==len(seg), (len(crayon)+len(para)+len(cap)+len(e1)+len(e2),len(seg))
s=s[:i]+cap+e1+e2+para+crayon+s[j:]
# M: 50 above the Kate Millie line
rep('<p data-gap="29">Kate Millie’s <em>Supplemental Language Album</em>','<p data-gap="29" data-mma="50">Kate Millie’s <em>Supplemental Language Album</em>')
# N: 24 between the three reading systems
rep('<ol><li data-gap="29">Follow the presentations in the AMI Language manual.</li>','<ol class="mm-ol24"><li data-gap="29">Follow the presentations in the AMI Language manual.</li>')
# P: the Perugia image 150 high, the text wrapping
i=s.find('<div class="mm-set mm-col" data-cap="1" data-h="120"><div class="mm-text"><p data-gap="24">I’ve been working')
end=s.find('</figcaption></figure></div></div>',i)+len('</figcaption></figure></div></div>')
blk=s[i:end]
m=re.match(r'<div class="mm-set mm-col" data-cap="1" data-h="120"><div class="mm-text">(.*?)</div>(<div class="mm-imgs">.*</div>)</div>$',blk,re.S)
assert m
s=s[:i]+'<div class="mm-float mm-perugia">'+m.group(2)+'</div>'+m.group(1)+s[end:]
# R: Series section gaps 24 / 24 / 30 / 30
open(f,'w').write(s);print('b19 html ok')
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# R (owner: "in this section: 1. blue heading and text = 24 2. between lines of text = 24 3. text and then blue heading = 30 4. between blue lines. = 30")
i=s.find('<p class="mm-hanglab mm-ser"');j=s.find('id="symbol-box-1"')
seg=s[i:j]
seg=seg.replace('<p class="mm-hanglab mm-ser" data-gap="29">','<p class="mm-hanglab mm-ser" data-gap="29" data-mma="30">').replace('<p class="mm-tab1" data-gap="20">','<p class="mm-tab1" data-gap="20" data-mma="24">')
s=s[:i]+seg+s[j:]
# N: 24 between the three reading systems
i=s.find('<ol class="mm-ol24">');j=s.find('</ol>',i)
seg=s[i:j].replace('<li data-gap="20">','<li data-gap="24">');assert seg.count('data-gap="24"')==2
s=s[:i]+seg+s[j:]
css='''<style id="mm-ec-12nov-d">
/* 12 Nov 2026 (owner: "yes" - the Taipei paragraph wraps under its two images): the two images side by side, 120 high */
@media (min-width:641px){html body main .mm-float.mm-taipei{width:max-content !important;max-width:none !important;height:auto !important}html body main .mm-float.mm-taipei .mm-imgs{height:auto !important}html body main .mm-float.mm-taipei>.mm-imgs{display:flex !important;gap:24px !important;width:max-content !important}html body main .mm-float.mm-taipei figure{flex:none !important;width:auto !important}html body main .mm-float.mm-taipei .pim{height:120px !important;width:auto !important}}
/* 12 Nov 2026 (owner: "make this photo 150 high and wrap the text"): Perugia */
@media (min-width:641px){html body main .mm-float.mm-perugia .pim{height:150px !important;width:auto !important}html body main .mm-float.mm-perugia figure{margin:0 !important}}
@media (max-width:640px){html body main .mm-float.mm-perugia .pim{max-width:480px !important;margin-left:auto !important;margin-right:auto !important}}/* on phones the Perugia image is not stretched beyond its file */
/* 12 Nov 2026 (owner: "make it 75"): the gap in the row of images 040-042 */
@media (min-width:831px){html body main .mm-row:has(img[data-full="images/041.jpg"]),html body main .mm-row:has(img[data-full="images/041.jpg"]) .mm-imgs{gap:75px !important;column-gap:75px !important}}
/* 12 Nov 2026 (owner: "Height can be flexible - make their widths 100"): the Word Study images */
@media (min-width:641px){html body main .mm-float.mm-wsf .pim{width:100px !important;height:auto !important}}
/* 12 Nov 2026 (owner: "have the dashes align with the blue headings. retain the current gap between the dashes and the words"): the Preparation lists */
@media (min-width:641px){html body main .mm-wcols2.mm-prep ul{margin-left:0 !important;padding-left:24px !important}}
/* "graphemes." in the column of the definitions (owner: "the text needs to align in these three rows") */
html body main p.mm-hanglab .mm-lab.mm-arwlab{white-space:nowrap}
</style>'''
rep('</body>',css+'</body>')
open(f,'w').write(s);print('b19 ok')
s=open(f).read()
a="if(s2.matches('.mm-float')&&getComputedStyle(s2).cssFloat!=='none'){var fr=s2.getBoundingClientRect(),fm=parseFloat(getComputedStyle(s2).marginBottom)||0;"
assert s.count(a)==1
s=s.replace(a,"if(s2.matches('.mm-float')&&!s2.matches('.mm-taipei,.mm-perugia')&&getComputedStyle(s2).cssFloat!=='none'){var fr=s2.getBoundingClientRect(),fm=parseFloat(getComputedStyle(s2).marginBottom)||0;")
open(f,'w').write(s);print('b19b ok')
