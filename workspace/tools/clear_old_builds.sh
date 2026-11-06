#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 1; lesson 18, 28 Oct change "delete each test build after use"; lesson 39):
# once build <newest> has passed its fast round, the bulky files (images, hostinger, work, preview, shots, the zip) of builds
# older than the one before it are deleted; their records (txt, md, json, log) are kept. A build whose folder any running
# process names is skipped, so nothing a running check reads is deleted.  Usage: clear_old_builds.sh <builds dir> <newest, e.g. b32>
set -u; D=$1; N=${2#b}
for b in "$D"/b*; do k=${b##*/b}; [[ "$k" =~ ^[0-9]+$ ]] || continue; [ "$k" -lt $((N-1)) ] || continue
  if pgrep -f "$b" >/dev/null; then echo "kept $b (a running process uses it)"; continue; fi
  rm -rf "${b:?}/images" "${b:?}/hostinger" "${b:?}/work" "${b:?}/preview" "${b:?}/shots"; rm -f "${b:?}"/*.zip; echo "cleared $b (records kept)"
done
