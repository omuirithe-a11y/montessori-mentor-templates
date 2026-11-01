#!/usr/bin/env bash
# setup_workspace.sh - the workspace set-up in one run (owner 1 Nov 2026 09:24: "you do 2 and 3").
# START-HERE Quick start item 1 + "Set up the workspace first" steps 3 and 4.
# Before running: the repository must be attached (add_repo omuirithe-a11y/montessori-mentor-templates, push)
# and cloned with --depth 1 to /home/claude/montessori-mentor-templates. That part is a tool call, not a command.
# Run:  bash /home/claude/montessori-mentor-templates/workspace/tools/setup_workspace.sh
# It prints one table, one row per step, each "succeeded" or "FAILED", and ends with
# "SET-UP SUCCEEDED" (exit 0) or "SET-UP FAILED" (exit 1). That printout goes in the first reply.
# REPO and MM can be set to other folders for testing.

REPO="${REPO:-/home/claude/montessori-mentor-templates}"
MM="${MM:-/home/claude/mm}"
rows=()
fail=0
row() { rows+=("$1|$2|$3"); [ "$2" = "succeeded" ] || fail=1; }

# 1. The clone
if head=$(git -C "$REPO" log -1 --format='%h %ci' 2>/dev/null); then
  row "1. GitHub clone" succeeded "$REPO at commit $head"
else
  row "1. GitHub clone" FAILED "no working clone at $REPO (attach and clone first)"
fi

# 2. Fingerprints on the clone, before anything is copied
fp_ok=1
for list in "$REPO/workspace/FINGERPRINTS.txt" "$REPO/workspace/tools/v8/FINGERPRINTS.txt"; do
  dir=$(dirname "$list")
  if [ ! -f "$list" ]; then fp_ok=0; fpmsg+="missing $list; "; continue; fi
  out=$(cd "$dir" && sha256sum -c FINGERPRINTS.txt 2>&1)
  ok=$(grep -c ': OK$' <<<"$out"); bad=$(grep -c ': FAILED' <<<"$out")
  miss=$(grep -c 'No such file' <<<"$out")
  rel=${list#$REPO/}
  fpmsg+="$rel: $ok OK, $bad failed, $miss missing; "
  if [ "$bad" != 0 ] || [ "$miss" != 0 ] || [ "$ok" = 0 ]; then
    fp_ok=0; fpmsg+="($(grep -v ': OK$' <<<"$out" | grep -v WARNING | cut -d: -f1 | head -5 | paste -sd, -)) "
  fi
done
if [ $fp_ok = 1 ]; then row "2. Fingerprints" succeeded "$fpmsg"; else row "2. Fingerprints" FAILED "$fpmsg"; fi

# 3. Copy the workspace and the templates (only if the fingerprints passed)
if [ $fp_ok = 1 ]; then
  mkdir -p "$MM/templates" &&
  cp -a "$REPO/workspace/." "$MM/" &&
  cp "$REPO/Essay Code Template.html" "$REPO/Resources Code Template.html" "$REPO/org-rule.html" "$MM/templates/" &&
  copied=$(cd "$MM" && sha256sum -c FINGERPRINTS.txt 2>&1 | grep -vc ': OK$')
  if [ "${copied:-1}" = 0 ]; then
    e=$(sha256sum "$MM/templates/Essay Code Template.html" | cut -c1-8)
    r=$(sha256sum "$MM/templates/Resources Code Template.html" | cut -c1-8)
    row "3. Workspace and templates copied" succeeded "$MM; Essay template $e, Resources template $r"
  else
    row "3. Workspace and templates copied" FAILED "copy does not match the fingerprints"
  fi
else
  row "3. Workspace and templates copied" FAILED "not copied, because the fingerprints failed"
fi

# 4. Libraries
pip install --break-system-packages -q pymupdf python-docx >/dev/null 2>&1
if libs=$(python3 -W ignore -c "import fitz, docx, cv2, PIL, bs4, playwright; print('fitz docx cv2 PIL bs4 playwright')" 2>&1); then
  row "4. Libraries" succeeded "$libs import"
else
  row "4. Libraries" FAILED "$(tail -1 <<<"$libs")"
fi

# 5. Faces model
want=$(grep ' faces/yunet.onnx$' "$MM/FINGERPRINTS.txt" 2>/dev/null | cut -d' ' -f1)
have=$(sha256sum "$MM/faces/yunet.onnx" 2>/dev/null | cut -d' ' -f1)
if [ -n "$want" ] && [ "$want" = "$have" ]; then
  row "5. Faces model yunet.onnx" succeeded "fingerprint ${have:0:8} matches"
else
  row "5. Faces model yunet.onnx" FAILED "missing or fingerprint differs (want ${want:0:8}, have ${have:0:8})"
fi

# 6. Disk space (lesson 18)
free=$(df -BG --output=avail /home/claude 2>/dev/null | tail -1 | tr -dc 0-9)
if [ "${free:-0}" -ge 5 ]; then row "6. Free disk" succeeded "${free} GB"; else row "6. Free disk" FAILED "${free} GB (under 5 GB)"; fi

echo "Set-up run $(date '+%Y-%m-%d %H:%M') (machine started $(uptime -s))"
echo "| Step | Result | Detail |"
echo "|---|---|---|"
for r in "${rows[@]}"; do IFS='|' read -r a b c <<<"$r"; echo "| $a | $b | $c |"; done
if [ $fail = 0 ]; then echo "SET-UP SUCCEEDED"; exit 0; else echo "SET-UP FAILED"; exit 1; fi
