#!/bin/bash
# run_visual_split.sh <checks dir> <package.zip> <out.txt> [quick]
# 27 Oct 21:1x, owner: "make this process faster ... without losing accuracy".
# The full on-screen check, run as parts of 15 widths, each part through run_check.sh (at most 2 browser checks at once).
# The check script is the frozen one, unchanged; the widths are its own list, all of them. The joined file holds every width line.
# A part that finished is kept (named by the package sha), so a run stopped by the 2-hour limit resumes where it stopped: start the same command again.
# A changed package has a new sha, so its old parts are never reused.
# "quick": 10 key widths only, for finding faults early. Its file says QUICK LOOK; it never replaces the full check.
set -u
C=$1; Z=$2; OUT=$3; MODE=${4:-full}
V=$C/visual_check.py
VS=$(sha256sum "$V" | cut -d' ' -f1); ZS=$(sha256sum "$Z" | cut -d' ' -f1)
if [ "$MODE" = quick ]; then
  PARTS=("320,390,640,641,768,830,831,1024,1280,1440")
else
  ALL=$(python3 -I -c "import re;s=open('$V').read();exec(re.search(r'^WIDTHS = .*$',s,re.M).group(0));print(','.join(map(str,WIDTHS)))")
  PARTS=($(python3 -I -c "w='$ALL'.split(',');print(' '.join(','.join(w[i:i+15]) for i in range(0,len(w),15)))"))
fi
D=$(dirname "$OUT")/.parts-${ZS:0:16}-${VS:0:12}-$MODE; mkdir -p "$D"
n=0
for P in "${PARTS[@]}"; do
  n=$((n+1)); f=$D/part$(printf %02d $n).txt
  if [ -f "$f" ] && grep -q '^RESULT:' "$f"; then continue; fi
  if [ -f "$f.tmp2" ]; then continue; fi   # 28 Oct 22:0x: the reverse runner is doing this part - Culture's part 5 ran twice (19:40-19:59 and 19:57-20:08), the join waited 9 min for the duplicate
  run=/home/claude/reports/run_check.sh
  { echo "part $n widths $P start $(TZ=Asia/Shanghai date +%H:%M:%S)"; "$run" "$C" visual_check.py "$Z" "$P"; echo "exit $?"; echo "end $(TZ=Asia/Shanghai date +%H:%M:%S)"; } > "$f.tmp" 2>&1
  if grep -q '^RESULT:' "$f.tmp"; then mv "$f.tmp" "$f"; else echo "part $n did not finish - see $f.tmp"; exit 1; fi
done
while ls "$D"/part*.txt.tmp2 >/dev/null 2>&1; do sleep 20; done   # wait for parts the reverse runner is still doing
for i in $(seq 1 ${#PARTS[@]}); do g=$D/part$(printf %02d $i).txt; grep -q "^RESULT:" "$g" 2>/dev/null || { echo "part $i missing"; exit 1; }; done
{
  echo "visual_check.py sha256: $VS"
  echo "package sha256: $ZS"
  [ "$MODE" = quick ] && echo "QUICK LOOK - 10 widths only - this is NOT the full check"
  echo "run in ${#PARTS[@]} part(s) by run_visual_split.sh; parts in $D"
  for f in "$D"/part*.txt; do grep -E '^part |^end ' "$f" | tr '\n' ' '; echo; done
  echo ----
  for f in "$D"/part*.txt; do grep -E '^ *[0-9]+ (ok|FAULT)' "$f"; done
  grep -h '^1280 narrowed' "$D"/part*.txt | sort -u
  if grep -h '^RESULT:' "$D"/part*.txt | grep -qv 'every width ok'; then echo 'RESULT: FAULTS - see the lines marked FAULT'; else echo 'RESULT: every width ok'; fi
} > "$OUT"
echo "written $OUT"; tail -1 "$OUT"
