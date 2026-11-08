# The three safeguards (owner 8 Nov 2026: "built the three") - what each does and the deliberately broken cases that proved it

1. The builder refuses an edit that does not land as written (tools/build_page.py, the PAGE_CODE_REPLACE step).
   - One-place edit found other than once, every-place edit found nowhere, or a group (PAGE_CODE_REPLACE_ONE_OF) where not exactly one lands -> BUILD REFUSED, exit 3; a refused numbered folder is renamed <bN>-refused-<time>.
   - Proof: proofs-8nov/settings-broken.py (planted: '<p>' -> found 85 times; 'THIS TEXT IS ON NO PAGE' -> 0; group NOWHERE-A/B -> 0 of 2) - all three caught (proofs-8nov/pt1.log). The same run also caught three real edits of the page settings that no longer landed with her new PDF (image 27 placement) - removed from the settings.
   - Clean case: the page settings as now - trial build /home/claude/pe2/build/try built with 12 expected group misses only (try.log).
2. The fast round runs every check to the end and stops with one list (tools/more_checks.sh, fast stage; checks2/FAULTS.txt); numbered builds only from a trial whose fast round passed (tools/promote.sh; tools/build_guard.sh refuses a numbered build after build 1 unless PROMOTING=1).
   - Proofs: guard on a test builds folder (proofs-8nov/gd): direct b3 -> REFUSED "build the fixes as a trial"; trial -> allowed; promote with no passed fast round -> PROMOTE REFUSED.
   - Fast round run on the trial: see /home/claude/pe2/build/try/checks2/SUMMARY.txt (first run 8 Nov).
   - Also: the allowed lists are now read by the page's name (more_checks.sh PAGE=$SLUG) - before, The Prepared Environment's format allowed list was never read.
3. Fingerprints of the templates and every check script and runner (tools/fingerprints.py), checked by the guard before every build, overrides and trials included; a change needs a decisions-log line "FINGERPRINT <page> <combined>" with OWNER.
   - Proofs (test page zz-test, proofs-8nov/gd): unchanged -> allowed; one file changed -> REFUSED on a trial and with an override; with the decisions-log line -> accepted. A first fault found in the proof: paths with spaces (the templates) were misread - fixed before the record.
   - The Prepared Environment's record: records/fingerprints/the-prepared-environment.txt, 71 files, combined cef0bb52e28886d8 (8 Nov, after these changes).
