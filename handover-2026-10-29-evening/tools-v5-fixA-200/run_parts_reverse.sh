#!/bin/bash
# run_parts_reverse.sh <checks dir> <package.zip> <first part> <last part>
# A second run for a full check, on the second processor: does parts from <first> down to <last>, writing into the SAME parts folder
# that run_visual_split.sh uses, skipping any part already finished or being run there. Same frozen check, same widths.
C=$1; Z=$2; A=$3; B=$4
V=$C/visual_check.py; VS=$(sha256sum "$V" | cut -d' ' -f1); ZS=$(sha256sum "$Z" | cut -d' ' -f1)
D=$(dirname "$0")/final-checks/.parts-${ZS:0:16}-${VS:0:12}-full; mkdir -p "$D"
ALL=$(python3 -I -c "import re;s=open('$V').read();exec(re.search(r'^WIDTHS = .*$',s,re.M).group(0));print(','.join(map(str,WIDTHS)))")
PARTS=($(python3 -I -c "w='$ALL'.split(',');print(' '.join(','.join(w[i:i+15]) for i in range(0,len(w),15)))"))
for n in $(seq $A -1 $B); do f=$D/part$(printf %02d $n).txt
  [ -f "$f" ] && grep -q '^RESULT' "$f" && continue; [ -f "$f.tmp" ] && continue
  P=${PARTS[$((n-1))]}
  { echo "part $n widths $P start $(TZ=Asia/Shanghai date +%H:%M:%S)"; python3 -u "$V" "$Z" "$P"; echo "exit $?"; echo "end $(TZ=Asia/Shanghai date +%H:%M:%S)"; } > "$f.tmp2" 2>&1
  if ! { [ -f "$f" ] && grep -q '^RESULT' "$f"; }; then grep -q '^RESULT' "$f.tmp2" && mv "$f.tmp2" "$f"; fi
  echo "part $n done $(TZ=Asia/Shanghai date +%H:%M:%S)"
done
