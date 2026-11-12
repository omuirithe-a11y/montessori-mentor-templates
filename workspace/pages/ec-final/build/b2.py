import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# E21/E10..: remove every beige line in the page, and the one under the contents
assert s.count('<p class="mm-gl"></p>')==10
s=s.replace('<p class="mm-gl"></p>','')
rep('<div class="toc-rule-wrap"><div class="beige-rule"></div></div>','')
# E31, E33: a beige line above these two
rep('<section class="section" id="phonetic-reading-and-the-pink-blue-and-green-series">','<p class="mm-gl"></p><section class="section" id="phonetic-reading-and-the-pink-blue-and-green-series">')
rep('<section class="section" id="montessori-reading-systems">','<p class="mm-gl"></p><section class="section" id="montessori-reading-systems">')
# E8/E9/E4/E5/E33: red only for the six contents headings and Introduction
keep=['toc-spoken','toc-wabs','toc-keys','toc-wcon','toc-reading','toc-grammar']
def col(m):
    t=m.group(0)
    if any('id="%s"'%k in t for k in keep): return t
    return t.replace('mm-hc-EE0000','mm-hc-0432FF')
s,n=re.subn(r'<h2 class="mm-hc-EE0000"[^>]*>',col,s)
print('red h2 tags seen',n, 'red left', len(re.findall(r'<h2 class="mm-hc-EE0000"',s)))
# E1: Introduction heading, 40 above it, 30 below its line (as The Prepared Environment)
i=s.index('<main'); j=s.index('<section class="section">',i)
k=j+len('<section class="section">')
s=s[:k]+'<h2 class="mm-hc-EE0000" data-gap="48" data-mma="40" data-mmb="30" id="introduction">Introduction</h2>'+s[k:]
# fault 24: duplicate section ids
for dup in ['spoken-language','enrichment-of-vocabulary']:
    c=[0]
    def r(m):
        c[0]+=1; return m.group(0) if c[0]==1 else 'id="%s-%d"'%(dup,c[0])
    s=re.sub(r'id="%s"'%dup,r,s)
open(f,'w').write(s);print('b2 ok')
