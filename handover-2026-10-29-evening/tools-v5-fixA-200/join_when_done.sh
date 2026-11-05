#!/bin/bash
# join_when_done.sh <forward runner pid> <parts dir> <checks dir> <zip> <out>   28 Oct 22:0x
# When all 9 parts are finished, stops the forward runner (which could otherwise run a part the reverse runner already did) and writes the joined file.
FP=$1; D=$2; C=$3; Z=$4; O=$5
until [ $(for i in 1 2 3 4 5 6 7 8 9; do grep -l "^RESULT:" "$D/part0$i.txt" 2>/dev/null; done | wc -l) -eq 9 ]; do sleep 20; done
echo "all 9 parts at $(TZ=Asia/Shanghai date +%H:%M:%S)"
kids(){ for c in $(pgrep -P $1); do kids $c; echo $c; done; }
if kill -0 $FP 2>/dev/null; then L="$(kids $FP) $FP"; kill $L 2>/dev/null; echo "stopped forward runner $FP"; fi
cd /home/claude/reports && bash run_visual_split.sh "$C" "$Z" "$O" && grep -E "FAULT" "$O" | cut -c1-250
