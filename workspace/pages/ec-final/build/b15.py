import sys
f=sys.argv[1]
s=open(f).read()
# 12 Nov 2026 (owner: "divider", screenshot of "This is a photo of the Spoken Language shelf..."): the beige line back above this paragraph and its image, 30 above and 30 below
a='Consonant Blends Sound Card</p></div></div><div class="mm-float"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.33333"><img alt="" class="doc-img" data-full="images/002.jpg"'
assert s.count(a)==1
s=s.replace(a,'Consonant Blends Sound Card</p></div></div><p class="mm-gl"></p><div class="mm-float"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.33333"><img alt="" class="doc-img" data-full="images/002.jpg"')
open(f,'w').write(s);print('b15 ok')
