"""faults_allowed.py <full-check file> <allowed-item regex or NONE>: prints every FAULT line that has anything NOT allowed.
22:0x 28 Oct: the gate's grep -v let through a whole line if the allowed text appeared anywhere in it, even beside other faults.
Here a line is allowed only if every item it names matches the regex and every count without a list is 0, the hero is ok and the menu has no faults."""
import sys,re,ast
A=None if sys.argv[2]=='NONE' else re.compile(sys.argv[2]); bad=0
for l in open(sys.argv[1],encoding='utf-8'):
    if not re.match(r'^ *\d+ FAULT',l): continue
    why=[]
    for name,n,lst in re.findall(r'\|?\s*([a-z][a-z ]+?) (\d+)\s*(\[[^\]]*\])?',l.split('FAULT',1)[1]):
        if int(n)==0: continue
        if name.strip()=='menu': continue
        items=ast.literal_eval(lst) if lst else []
        if not items or A is None or not all(A.search(i) for i in items): why.append('%s %s %s'%(name.strip(),n,lst or ''))
    if 'hero ok' not in l: why.append('hero')
    m=re.search(r"faults (\[.*?\]|none)",l)
    if m and m.group(1)!='none' and not all(x.startswith('not tested') for x in ast.literal_eval(m.group(1))): why.append('menu '+m.group(1))
    if why: bad+=1; print(l.split('|')[0].strip(),'NOT ALLOWED:',why)
txt=open(sys.argv[1],encoding='utf-8').read()
n=len(re.findall(r'(?m)^ *\d+ (?:ok|FAULT)',txt))
if n<122: bad+=1; print('only %d widths in the file, 122 needed'%n)
for m in re.findall(r'(?m)^1280 narrowed to 390: sideways (\d+)',txt):
    if int(m)!=0: bad+=1; print('narrowing 1280 -> 390: sideways',m)
if not re.search(r'(?m)^1280 narrowed to 390',txt): bad+=1; print('no narrowing result in the file')
sys.exit(1 if bad else 0)
