import sys
f=sys.argv[1]
s=open(f).read()
blk=open('/tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/blk400.txt').read()
assert s.count('</head>')==1
s=s.replace('</head>',blk+'</head>')
open(f,'w').write(s);print('b14 ok')
