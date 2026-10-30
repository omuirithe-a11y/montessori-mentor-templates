#!/bin/bash
# gate2.sh - the answer clock, stronger version (20 Oct 2026, user's items 9 and 10)
#   start <kind>         start the clock for a question of <kind> (design | status | rule); loads its source list
#   run <source> <cmd..> run a search command; the log line (time, source, command, size of result) is written here, not typed
#   skip <source> <why>  mark a listed source not relevant, with the reason
#   check                GATE OPEN only if: 180 s passed; a search logged in each of minutes 1, 2 and 3;
#                        the last search is no more than 60 s old; every listed source searched or skipped with a reason
#   show                 print the log
D=/tmp/claude-0/-home-claude/e5b6f0aa-31bf-5b44-a113-b60ab48a7e85/scratchpad/g2; mkdir -p $D
now(){ date +%s; }
case "$1" in
 start) now > $D/start; : > $D/log; echo "$2" > $D/kind
   case "$2" in
     design) printf 'chat\nparallel-chat\nMASTER-DECISIONS\nSETTLED\nmemory\nlive-pages\nSensorial-live\n' ;;
     status) printf 'chat\nparallel-chat\nhandovers\nSETTLED\nMASTER-DECISIONS\nproject-files\n' ;;
     rule)   printf 'chat\nparallel-chat\nSETTLED\nSTART-HERE\nmemory\nproject-instructions\n' ;;
     *) printf 'chat\nparallel-chat\n' ;;
   esac > $D/sources
   echo "START $(TZ=Asia/Shanghai date +%H:%M:%S) kind=$2 sources: $(paste -sd' ' $D/sources)";;
 run) src=$2; shift 2; out=$("$@" 2>&1); t=$(( $(now) - $(cat $D/start) ))
   echo "$t $(TZ=Asia/Shanghai date +%H:%M:%S) RUN $src | $* | ${#out} chars" >> $D/log; printf '%s\n' "$out";;
 tool) t=$(( $(now) - $(cat $D/start) )); echo "$t $(TZ=Asia/Shanghai date +%H:%M:%S) TOOL $2 | $3" >> $D/log; echo logged;;
 skip) t=$(( $(now) - $(cat $D/start) )); echo "$t $(TZ=Asia/Shanghai date +%H:%M:%S) SKIP $2 | $3" >> $D/log; echo skipped;;
 check) s=$(cat $D/start); n=$(( $(now) - s )); ok=1; why=""
   [ $n -ge 180 ] || { ok=0; why="$why time=${n}s<180;"; }
   for m in 0 1 2; do c=$(awk -v a=$((m*60)) -v b=$((m*60+60)) '$3!="SKIP" && $1>=a && $1<b' $D/log | wc -l); [ $c -ge 1 ] || { ok=0; why="$why no-search-in-minute-$((m+1));"; }; done
   last=$(awk '$3!="SKIP"{l=$1} END{print l+0}' $D/log); [ $(( n - last )) -le 60 ] || { ok=0; why="$why last-search-$(( n - last ))s-ago;"; }
   while read src; do grep -q " \(RUN\|TOOL\|SKIP\) $src |" $D/log || { ok=0; why="$why source-missing:$src;"; }; done < $D/sources
   [ $ok = 1 ] && echo "GATE OPEN elapsed=${n}s" || echo "GATE SHUT elapsed=${n}s:$why";;
 show) cat $D/log;;
esac
