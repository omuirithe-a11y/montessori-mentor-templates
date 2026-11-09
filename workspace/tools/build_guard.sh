#!/bin/bash
# 6 Nov 2026 (owner 10:53 "yes", lessons list item 1; lesson 18): refuse a build when free disk space is under 4 GB (a build and
# its checks use about 1.5 GB; on 6 Nov 09:57 a full disk stopped build 31)
FREE=$(df -Pk /home/claude | awk 'NR==2{print int($4/1048576)}'); [ "${FREE:-0}" -ge 4 ] || { echo "BUILD REFUSED: only ${FREE} GB free on the disk (4 GB needed) - clear superseded builds' bulky files first (tools/clear_old_builds.sh)"; exit 3; }
# build_guard.sh <builds folder> <new build name>
# 6 Nov 2026 (owner 08:01 "analyse the effectiveness ... then adjust"; BUILD-ORDER item 5/6): a new build is refused while the
# newest build's check round is unfinished - the fast round must have STOPPED at a fault or PASSED, and if it passed, a
# separate review report (REVIEW.md, naming the package sha256) must exist. So every fault a round finds is fixed together in
# ONE new build, not one build per fix. Override only with the owner's words in <builds>/<new>.override.txt.
set -u; D=$1; N=$2
# 8 Nov 2026 (owner "built the three", item 3): the template and the check scripts may not change mid-page - their fingerprints are
# recorded at the page's first build (tools/fingerprints.py) and checked before EVERY build, overrides and trial builds included;
# a change needs her words in the decisions log ("FINGERPRINT <page> <combined>" with OWNER)
PG0=${PAGE_SLUG:-$(ls "$D"/b[0-9]*/*.zip 2>/dev/null | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1 | xargs -r basename | sed 's/\.zip$//')}
if [ -n "$PG0" ]; then
  if [ -f /home/claude/mm/records/fingerprints/$PG0.txt ]; then python3 /home/claude/mm/tools/fingerprints.py check "$PG0" || { echo "BUILD REFUSED: the template or the check scripts changed since this page's record (above)"; exit 3; }
  else echo "BUILD REFUSED: no fingerprint record for $PG0 (records/fingerprints/$PG0.txt) - made at the page's first build"; exit 3; fi
fi
# 8 Nov 2026 (owner "built the three"): a build into a folder not named b<N> (a trial build, e.g. <builds>/try) is not numbered and is
# not guarded further - only a trial whose fast round passed can become a numbered build (tools/promote.sh)
case "$N" in b[0-9]*) ;; *) echo "build guard: trial build $N (not numbered) - fingerprints unchanged; allowed"; exit 0;; esac
[ -s "$D/$N.override.txt" ] && { echo "build guard: override by the owner's words in $D/$N.override.txt"; exit 0; }
P=$(ls -d "$D"/b[0-9]* 2>/dev/null | sed 's/.*\/b//' | grep -E '^[0-9]+$' | sort -n | tail -1)
if [ -z "$P" ]; then   # 6 Nov 08:2x (owner 08:15 "adjust accordingly"): build 1 needs the decisions sheet answered first
  DS=${DECISIONS_SHEET:-}; { [ -n "$DS" ] && [ -s "$DS" ] && grep -q "^OWNER ANSWER:" "$DS"; } || { echo "BUILD REFUSED: first build - no answered decisions sheet (set DECISIONS_SHEET to a file holding a line 'OWNER ANSWER: <her words>')"; exit 3; }
  # 8 Nov 06:44 (owner "yes" to removing it): the 7 Nov S4b wait for the template test page is removed - the template test page was deleted from the to-do list (owner 8 Nov 06:43)
  [ -n "${PAGE_SLUG:-}" ] && python3 /home/claude/mm/tools/fingerprints.py record "$PAGE_SLUG"   # 8 Nov 2026 (item 3): the page's record, made at build 1
  touch "/home/claude/mm/records/.guard-ok-$(basename "$D")-$N"; echo "build guard: first build, decisions sheet answered ($DS)"; exit 0; fi
# 8 Nov 2026 (owner "yes" to the decisions audit, claude/DECISIONS-AUDIT-8nov.md): after build 1 a numbered build needs only that the
# previous build's checks have finished (stopped with their whole fault list, or passed) and a stated cause - no override question to the
# owner, no review of a stopped build, no trial-first rule, and the 524-item list's gate plan is no longer required
B="$D/b$P"; S="$B/checks2/SUMMARY.txt"
[ -f "$S" ] || { echo "BUILD REFUSED: build b$P has no check round (run tools/check_round.sh ... fast on it first)"; exit 3; }
grep -qE "^STOPPED at |^FAST CHECKS PASSED" "$S" || { echo "BUILD REFUSED: build b$P's checks have not finished"; exit 3; }
Z=$(ls "$B"/*.zip | grep -vE -- '-(originals|CHECK-ONLY|UPLOAD)\.zip$' | head -1); PG=$(basename "$Z" .zip)
[ -n "${BUILD_CAUSE:-}" ] || { echo "BUILD REFUSED: no cause given for build $N - set BUILD_CAUSE (review fault / check fault / template change / owner change: what) (S10)"; exit 3; }
echo "$(date '+%d %b %Y %H:%M:%S') | $N | cause: $BUILD_CAUSE" >> /home/claude/mm/records/build-causes-$PG.txt
touch "/home/claude/mm/records/.guard-ok-$(basename "$D")-$N"; echo "build guard: b$P checks finished - build $N"
