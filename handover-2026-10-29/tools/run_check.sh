#!/bin/bash
# Every browser check (visual_check or format_check, full or key widths) goes through this: at most 2 at once on 2 processors,
# first come, first served (27 Oct: the earlier version let a new run jump ahead, so some runs waited over an hour).
# Usage: run_check.sh <checks folder> <visual_check.py|format_check.py> <args...>
Q=/home/claude/reports/.check-queue; mkdir -p $Q
me=$Q/$(date +%s%N)-$$; echo $$ > $me; trap 'rm -f $me' EXIT
while true; do
  # drop entries whose process has gone
  for f in $Q/*; do [ -f "$f" ] || continue; kill -0 $(cat $f 2>/dev/null) 2>/dev/null || rm -f "$f"; done
  pos=$(ls $Q | sort | grep -n "^$(basename $me)$" | cut -d: -f1)
  if [ -n "$pos" ] && [ "$pos" -le 2 ]; then
    for k in 0 1; do
      exec 9>/home/claude/reports/.visual-slot-$k
      if flock -n 9; then python3 -u "$1/$2" "${@:3}"; exit $?; fi
    done
  fi
  sleep 2
done
