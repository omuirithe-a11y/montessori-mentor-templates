set -e
D=/tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad
cd /home/claude/ec
O=${1:-t/N22.html}; cp t/N21.html $O
for b in b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20; do if [ -f $D/$b.py ]; then python3 $D/$b.py $O; fi; done
