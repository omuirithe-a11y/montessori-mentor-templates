# Standard agent brief (28 Oct 2026, 20:3x). Paste into every agent's prompt; fill the FAULT part.

## Rules (all agents)
- Work only in your own scratchpad folder (named in the task). Never edit other files. Never upload anything.
- Facts only, each with the command output that shows it. No guesses; say "not established" if not measured.
- Times: `TZ=Asia/Shanghai date`.
- The machine has 2 processors: run ONE browser at a time. Never run the full visual_check during fault work.
- Test only at the width(s) where the fault shows. Confirm at 390, 831 and 1440 once, at the end, with
  `python3 -u /home/claude/reports/<checks dir>/visual_check.py <zip> 390,831,1440`.
- The base build's faults are listed below: do NOT re-measure the base.
- Do not investigate anything another agent has (listed below).
- Measure with a short targeted Playwright script. To find what sets a value, instrument
  CSSStyleDeclaration.prototype.setProperty in an init script and record the script line.
- Height check on every result: main height at 4 s, after scrolling the whole page, after opening and closing every
  <details>; largest margin-top in main. Tool: scratchpad/elist/stable.py <width> <zip>.
- Settled and allowed (never report as faults): headings smaller than live; quotations without side margins; spacing set
  by the template scripts; images beside text 150 px high; photos under text where text would be squeezed (option C);
  no lines next to quotations; black/orange shown as ink rgb(43,43,43); links rgb(4,50,255); typo and UK-spelling fixes.
- Never use change 39 (stackNarrow as in edits.py index 30).
- Report: OLD and NEW text verbatim (OLD must occur exactly once in index.html), the cause with line numbers,
  before/after measurements, check lines, file paths. Report as soon as the fix works.

## Fill in per task
- FAULT:
- BUILD (zip):
- LIVE COPY:
- CHECKS DIR:
- BASE BUILD'S KNOWN FAULTS:
- OTHER AGENTS' FAULTS (do not touch):
- YOUR FOLDER:

## Checker briefs (28 Oct 20:4x, from Anthropic's best practices: the reviewer "sees only the diff and the criteria")
- Give the checker ONLY: the build, the template, the live copy, the checks folder, the settled rules. No fix story, no known faults, no conclusions.
- Ask it to try to prove the page wrong, and to report only faults against the template or the settled rules.
- Its report must list what it did NOT check.
- Every check runs from its own fresh unzip, browser and server port (never a shared server).
- Read raw check output, never only the RESULT line. A READY is never passed on without what it covered.
- Sending: only through /home/claude/reports/tools/send_gate.sh (code check, full check on this exact zip, height check, then the no-copy-protection copy).

## Watching running work (28 Oct 21:5x, after the 20:23-21:42 silent stop)
- Every agent and check runs with tools/watch.sh 20 <its folder> in the background: it ends - and so alerts the coordinator - when a folder has no new file for 20 minutes.
- On an alert: read the agent's own notes in its folder first (the cause may already be written there), then restart it from those notes or finish the work directly.
- Any interruption by the owner (a rejected command) can stop agents silently: after one, check every agent's folder at once.
