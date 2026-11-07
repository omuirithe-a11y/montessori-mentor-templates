#!/bin/bash
# roundlock.sh take|release|check   (7 Nov 2026, owner "implement all of these changes", S7 refined): while a check round runs,
# /home/claude/mm/.round-lock holds its process number; tools started outside the round (gate_list.py, serve.sh, the
# screenshot and block scripts) refuse to start. A tool inside the round carries MM_ROUND_LOCK=<that number>.
L=/home/claude/mm/.round-lock
case "$1" in
  take) echo "$2" > "$L";;
  release) [ -f "$L" ] && [ "$(cat "$L")" = "$2" ] && rm -f "$L";;
  check) [ -f "$L" ] || exit 0; P=$(cat "$L"); kill -0 "$P" 2>/dev/null || { rm -f "$L"; exit 0; }
         [ "${MM_ROUND_LOCK:-}" = "$P" ] && exit 0
         echo "REFUSED: a check round is running (process $P, $L) - wait for it, so nothing runs beside its checks"; exit 3;;
esac
