#!/bin/bash
# spacing122.sh <page file url> <out.txt> : the spacing check at all 122 widths, one browser per processor (2), same measurements as onecheck2430.js
W=$(sed -n 2p /tmp/claude-0/-home-claude/2beee614-a0c2-5261-87c0-d8de1f9128b0/scratchpad/t1/widths.txt)
A=$(echo $W | tr , '\n' | awk 'NR%2==1' | paste -sd,); B=$(echo $W | tr , '\n' | awk 'NR%2==0' | paste -sd,)
D=$(dirname "$2"); node ${CHK:-/home/claude/ec/chk/onecheck2430.js} "$1" $A > "$D/.s1" 2>&1 & node ${CHK:-/home/claude/ec/chk/onecheck2430.js} "$1" $B > "$D/.s2" 2>&1; wait
grep -h '^[0-9]' "$D/.s1" "$D/.s2" | sort -n > "$2"; rm -f "$D/.s1" "$D/.s2"
echo "widths $(wc -l < "$2") of $(echo $W | tr , '\n' | wc -l)"; grep -vc ' ok ' "$2" | sed 's/^/not ok: /'
