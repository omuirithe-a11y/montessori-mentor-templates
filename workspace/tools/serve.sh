#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 5; lessons 21, 64): a local test server started and stopped by its own
# process number (kept in a file), never by a name pattern.  Usage: serve.sh start <dir> <port> | serve.sh stop <port>
set -u; F=/home/claude/eng35/serve-$2.pid
case $1 in
  start) ( cd "$2" && exec python3 -m http.server "$3" >/dev/null 2>&1 ) & echo $! > /home/claude/eng35/serve-$3.pid; sleep 1; echo "serving $2 on $3, process $(cat /home/claude/eng35/serve-$3.pid)";;
  stop) [ -s "$F" ] && kill "$(cat "$F")" 2>/dev/null && rm -f "$F" && echo "stopped process on $2" || echo "no server recorded on $2";;
esac
