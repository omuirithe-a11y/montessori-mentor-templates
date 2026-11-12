import re,sys,hashlib
def blocks(p):
    s=open(p,encoding='utf-8').read()
    return [(m.group(1).lower(),m.group(0)) for m in re.finditer(r'<(script|style)\b[^>]*>.*?</\1>',s,re.S|re.I)]
T=blocks(sys.argv[1]); A=blocks(sys.argv[2])
pat=re.compile(r'marginTop|marginBottom|paddingTop|paddingBottom|margin-top|margin-bottom|padding-top|padding-bottom')
ts=[b for k,b in T if k=='script']
print('template scripts',len(ts),'with vertical spacing',sum(1 for b in ts if pat.search(b)))
th=set(hashlib.sha1(b.encode()).hexdigest() for k,b in T)
ah=set(hashlib.sha1(b.encode()).hexdigest() for k,b in A)
print('template blocks',len(T),'approved',len(A))
for i,(k,b) in enumerate(A):
    if hashlib.sha1(b.encode()).hexdigest() not in th:
        print('---',i,k,len(b),repr(b[:300]))
print('=== template blocks missing from approved')
for i,(k,b) in enumerate(T):
    if hashlib.sha1(b.encode()).hexdigest() not in ah:
        print('---',i,k,len(b),repr(b[:200]))
