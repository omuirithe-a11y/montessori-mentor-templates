#!/bin/bash
# watch.sh <minutes> <dir>...   28 Oct 2026, after an agent stopped silently at 20:23 and was not noticed until 21:42.
# Runs in the background; EXITS (which wakes the coordinator) as soon as any watched folder has had no file written
# for <minutes>, or every folder is finished (a file named DONE, or a RESULT line in a .txt). Prints which and why.
M=$1; shift
while true; do now=$(date +%s)
  for d in "$@"; do
    [ -d "$d" ] || { echo "$(TZ=Asia/Shanghai date +%H:%M) MISSING $d"; exit 1; }
    last=$(find "$d" -type f -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1); last=${last:-0}
    if [ $(( (now-last)/60 )) -ge $M ]; then echo "$(TZ=Asia/Shanghai date +%H:%M) STALLED $d: no file written for $(( (now-last)/60 )) min"; exit 2; fi
  done
  sleep 60
done
