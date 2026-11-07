# Proposed changes so the next Montessori Mentor page does not repeat this page's mistakes (draft, 7 Nov 2026)

Mistakes found on The English Curriculum (42 builds, about three days), ranked by time lost (judgement, not measured):
M1 the 2-hour long round re-run on builds 37, 38, 39, each ending in another build
M2 the gate's full list (524 rows; 143 eye rows, 16 rows without a check, after-upload rows) not checked until build 40
M3 the faces pixel check covered only blurred images; two children's faces unblurred since build 1, found at build 41; the round 1 sheet listed "no face found" images without showing them
M4 17 template commits during the page; one change (6 Nov 06:3x) tested with the tablet check only caused faults costing builds 39 and 40
M5 the "I Spy" fixes tested too narrowly (b41 from code only: 9 px at 768; b42 gap size only: "sound:" pushed to the next line at 768)
M6 questions to the owner one at a time as they came up
M7 checks changed mid-page (spacing, style, height, images, gate), each needing her agreement and a proof
M8 runs lost: disk full (b31), b36 run ended (cause unknown), b40 long checks died in a workspace restart, b40 speed fault most likely from gate proofs run beside it
M9 a spacing check made for the Resources template used on an Essay page
M10 reviewers given too little (b40 full review: no faces records, 97 eye rows not checked; b41: 76)
M11 reports with times typed before reading the clock; replies sent without the separate message check
M12 never measuring where the time went or what caused each rebuild
M13 many rounds on 1-2 px spacing differences (45 ended on an allowed list)

Solutions:
S1 tools/gate_plan.sh: runs the gate on build 1, sorts each row by HOW it is met (a check's result / a review / a file record / no check yet / after upload). The build guard refuses build 2 until every "no check yet" and "after upload" row has the owner's decision recorded (accepting "decided after publishing"); refuses a build if tools/REQUIRED-CHECKS.json changed since the plan. The plan writes the page's gate row file (tools/allowed/<page>-gate-rows.txt). [no yes needed]
S2 build_page.py refuses the final images unless the faces pixel check records it looked at every image the build puts on the page unblurred (counted against the build's own images, not the Word file, which holds unused hdphoto files). [no yes] + the round 1 faces sheet shows every image, not only those with faces found [blur method change: needs her yes]
S3 tools/test_fix.sh: on a copy with the fix, measures every block's size and its position from the block before it at the 13 widths, twice (only changes seen both times count); the blocks whose HTML changed are found by the script; for a page-settings change, any other changed block stops the build; for a template change, every moved block is listed with sizes before/after and goes with the agreement line. The build guard refuses a new build unless test_fix.sh ran after the last settings/template change. [no yes]
S4 the build guard refuses a build on a changed template unless the decisions log has that change's "TEMPLATE COMMIT <hash> AGREEMENT" line (now checked only by the gate at the end); with a standing agreement it checks only that test_fix.sh ran. [no yes - her existing rule, enforced earlier]
S4b the build guard refuses build 1 of a new Essay page until the template test page to-do (claude/TO-DO-next-chat.md) is marked done, so the queued template items are settled before a page depends on them. [no yes]
S5 check_round.sh fix mode: fault-fixing builds get the fast checks, the 122-width check and the S3 block comparison; wrap and images only on widths where blocks changed; the full long round once, on the build sent to the gate. [check rule: needs yes]
S6 more_checks.sh / run_checks.sh refuse a check script changed after build 1 unless the decisions log names its new version with her words. [needs yes]
S7 run lock in tools/serve.sh and the screenshot script: refuse to start a browser while a round runs; the hourly review lists any browser process outside a round. [no yes]
S8 tools/review_brief.sh writes every review brief from one input list (PDF, Word, screenshots, faces records, decisions log, build log, the owner's messages extracted with times from the chat transcript, the eye-row list). [no yes]
S9 commit_push.sh refuses a decisions-log line whose time is later than the clock. [no yes]
S10 tools/time_report.py: hours per stage per build from the check summaries and the log; the build script requires a cause for each build (review fault / check fault / template change / owner change); the report goes in the handover and to her on request. [no yes]
S11 the hourly review writes to the log every hour but messages her only when something was not followed. [changes her instruction: needs yes]
S12 a spacing mode for the Essay template, with its own spacing rules agreed at the start - on the template test page to-do. [later]
S13 the build 1 decisions sheet asks once for a spacing tolerance (e.g. within 2 px of the template's figure counts as the same), read by the spacing check. [check rule: needs yes]
Not enforceable, left out: routing every reply through the separate message checker.
Order of building (by value): S1, S3, S2 count, S4, S4b, then S7, S8, S9, S10.
