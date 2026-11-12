import sys
f=sys.argv[1]
s=open(f).read()
a='</body>'
assert s.count(a)==1
s=s.replace(a,'<style id="mm-ec-12nov">/* 12 Nov 2026 (owner: "is this bold" - "if it is, make it regular"): "Table of contents" in regular weight (it was 500, medium) */html body .toc-label{font-weight:400 !important}</style></body>')
open(f,'w').write(s);print('b13 ok')
