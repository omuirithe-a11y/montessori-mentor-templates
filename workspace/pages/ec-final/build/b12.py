import re,sys
f=sys.argv[1]
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(a[:90],n); s=s.replace(a,b)
# images loading slowly (owner, 11 Nov): the template's layout ran three times on opening (about 2.5 s each), because later scripts changed the page's HEIGHT; it re-lays the page only when its WIDTH changes - the scripts that change the height place their own blocks
rep("if (m && Math.abs(r.width - m[0]) <= 1 && Math.abs(r.height - m[1]) <= 1) return;","if (m && Math.abs(r.width - m[0]) <= 1) return;   /* 11 Nov 2026 (owner: \"the photos are loading very slowly. why?\"): only a change of width re-lays the page */",3)
s,n=re.subn(r"if\s*\(m && Math\.abs\(r\.width - m\[0\]\) <= 1 && Math\.abs\(r\.height - m\[1\]\) <= 1\) return; schedule\(\);","if (m && Math.abs(r.width - m[0]) <= 1) return; schedule();",s)
# the first images start downloading at once (they are on the first screens)
k=[0]
def eag(m):
    k[0]+=1
    return m.group(0).replace('loading="lazy"','loading="eager" fetchpriority="high"') if k[0]<=4 else m.group(0)
i=s.index('<main')
s=s[:i]+re.sub(r'<img [^>]*loading="lazy"[^>]*>',eag,s[i:])
rep('</head>','<link rel="preload" as="image" href="images/hero.jpg"></head>')
# bold words in quotations stay bold (owner: "yes")
rep('<strong>motor</strong>','<strong class="mm-qb">motor</strong>')
rep('<strong>intellect</strong>','<strong class="mm-qb">intellect</strong>')
rep('</body>','<style id="mm-ec-11nov-h">/* 11 Nov 2026 (owner: "yes" - words bold in the PDF stay bold inside quotations) */html body main blockquote.pullquote strong.mm-qb{font-weight:700 !important}</style></body>')
open(f,'w').write(s);print('b12 ok',k[0])
