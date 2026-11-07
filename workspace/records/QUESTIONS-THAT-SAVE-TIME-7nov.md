# Review of list-v6.md (16 questions)

Checked from files only. Nothing run, nothing changed except this file.
Short names: LOG = /home/claude/mm/records/DECISIONS-LOG-3-nov.md (the "log" the list cites); B = /home/claude/mm/build-35; EV = /home/claude/mm/records/evidence-english.

## 1. Verdicts

| Q | Verdict | File:line | Correction |
|---|---|---|---|
| 1 | PARTLY | B/b28,b29,b30,b32,b34,b35,b38,b39/checks2/SUMMARY.txt; B/b37/checks/SUMMARY.txt:4,9; B/b40/checks/SUMMARY.txt:7; LOG:295, 300, 309, 315, 322-327, 331, 335-337, 355, 357 | 17 STOPPED lines: right. They are in 10 builds, not 11 (the list itself names 10). b28 static was a runner fault too, not just a stop that cleared: LOG:295 says "static vs unsaved template 07:30". So at least 5 stops were the check or the set-up. The re-run started 33 s later (07:30:38); the PASS is stamped 07:30:39 (34 s). The b40 speed cause is only "likely" (LOG:357), and the first re-run alone also failed with the "cause not known". Not counted: spacing stops that were partly the check. b28's first runner spacing run (BUILD-ORDER.md:57: "66 of 230 wrong"), and b29 08:18, judged before the 08:53 check change (LOG:300). Also b35's spacing stop, which an allowed list settled (LOG:322-323). b38 images needed a check change as well as a template fix (LOG:336-337). |
| 2 | TRUE | B/b41-b44/checks2/SUMMARY.txt; B/b41/REVIEW.md:205; b42:221; b43:206; b44:209 | (b41 fault 4 is the brief, not the page: LOG:361.) |
| 3 | TRUE | tools/REQUIRED-CHECKS.txt:54,236,500,583,658,661,662,788,793,812; tools/v8/place_check.py:30,54 | Note: D337 (line 788) is a nearby rule (an image after a section heading), not the same rule. D258 (line 729) is the Resources version. A059, C105 and E005 name "place_check.py" with no folder. |
| 4 | PARTLY | LOG:309, 315-318, 329-331; B/b32/checks2/SUMMARY.txt:7; EV/time-report.txt:8-9 | b32 format: the fast round was 1 min in (stop 11:01:04) and was re-run about 3 min later (LOG:309), so it was a restart, not a whole round. b34 style: the stop came from the check (LOG:315, 319), but the next build did change the page: the template 24720ba5 change for the b34 review's faults (LOG:316). Undoing the stop also needed a check change (12:15 agreement, LOG:317-318). b37 height: TRUE. Stop 15:21:44, repeated 3 times, restarted 15:45 (LOG:329-331), about 24 min. Same items as Q1: merge. |
| 5 | PARTLY | EV/git-log.txt:72 (06:40:28); B/b38/checks2/SUMMARY.txt:21 (17:26:18); B/b39/checks2/SUMMARY.txt:21 (19:04:56); LOG:288, 291, 294, 339-341, 362 | The faults were found 11 and 12 builds later (b27 to b38/b39), not about 10, and 10 h 46 min and 12 h 24 min later. "Tested with the tablet check only" is LOG:339's own words. But tablet_check.py was written only at 07:28 (LOG:294), and b27's checks were stopped by a restart (LOG:291). So b27 was built at 06:39 with no check finished on it, and b28 was the first build checked. b41 code-only: TRUE (LOG:362). |
| 6 | TRUE | B/b41/REVIEW.md:31-32; b42:38 (fault 1); b43:32; b44:30 | - |
| 7 | PARTLY | LOG:328, 332, 335-336; B/b41-b44/checks2/SUMMARY.txt; LOG:399 | b37/b38: TRUE. "b41-b44 the reverse" covers only the fast round. The long round never ran on b41-b43, and b44's run_checks was stopped with no result (B/b44/checks/SUMMARY.txt:1, LOG:399). The early gate on b41 and b42 printed "integrity faults: 3" with no PASSED line (B/b41/checks2/SUMMARY.txt:16; b42:16). |
| 8 | TRUE | B/b40/REVIEW-FULL.md:9; B/b40/REVIEW.md:8; B/b41/REVIEW.md:24; b42:28; b43:54; b44:57; B/b43/REVIEW-first-no-screenshots.md:33 | Her rule D019 already says "screenshots looked at for every width" (tools/REQUIRED-CHECKS.txt:526). |
| 9 | TRUE | B/b44/REVIEW.md:141 | - |
| 10 | TRUE | /home/claude/eng35/vt/m.py:4-15, 21; LOG:393, 397 item (5) | The thresholds are in LOG:397, not in m.py. The line-end measure ("short") first appears in m2.py (13:40, after b44). |
| 11 | TRUE (claims) | LOG:197, 200, 237 | The claims are right, but they do not show a gap between what was built and what she agreed. Better evidence: her 09:16 and 13:38 agreements were carried out only above 830 px, which was found 6 Nov 06:3x (LOG:288) and caused b25 review faults 9-10 (EV/git-log.txt:72). The ALLOWED-FAULTS file she agreed to at 05:48 was not made until 13:4x (LOG:229). |
| 12 | TRUE | LOG:361, 364-370 | - |
| 13 | TRUE | LOG:305, 380, 381, 395, 396 | - |
| 14 | PARTLY | LESSONS-LEARNED-27-29-oct.md:943; EV/BUILD-ORDER.md:24, 26, 106 | Line 943 and the two owner safeguards: TRUE. "Stopping after two failed fixes" is NOT IN ANY FILE. The files have two other rules: "after two failed checker rounds, redraft" (messages, BUILD-ORDER.md:24) and "20 minutes without the cause -> stop, read the code" (BUILD-ORDER.md:26). BUILD-ORDER.md:106 lists as not enforceable: the message checker, and figures only from files. |
| 15 | TRUE | (no file measures usage) | - |
| 16 | (no claim) | - | - |

## 2. The list as a whole

Redundant (merge):
- Q4 is part of Q1: the same three stops (b32, b34, b37).
- Q7 and Q9 are part of Q2: what checks and reviews each miss, and faults that appear once.
- Q10 and Q8 belong with Q6: the I Spy line failed four times because each fix was tested narrowly, at too few widths and on the wrong measure.
- Q5 and Q11 ask the same thing: was a template change, or her agreement, carried out and tested at every width it names?

Questions the assistant should have asked itself (asking the owner adds nothing new):
- Q8: her rule D019 (every width) already existed (REQUIRED-CHECKS.txt:526).
- Q12, "could it go on without me": the assistant had already promised "the work never waits for an answer" (LOG:250).
- Q13: disk space and restarts are technical (lesson 18, LOG:306).
- Q16: the separate message checker exists for this, and she already did it (LOG:401).
- Q10: it is BUILD-ORDER.md:11 (item 2) / lesson 6.

These still work as owner checks of whether rules are kept, but not as new questions.

Ranking: the list's ranking (1, 2, 3, 5, 4, ...) is judgement and the files only partly support it. Time per cause, where the files allow:
- I Spy line (Q6/Q10): b42 built 07:01 to b44's fault at 13:40 = 6 h 39 min over 3 builds (b42 also had faults 2-7). Plus b41 (22:43 build, 23:11 review).
- 847b6adb template change (Q5): b38 images stop 17:26 to b40 long pass 22:22 = about 4 h 56 min, 2 extra builds (b40 also lost about 30 min to the speed stop).
- Overnight faces wait (Q12): 23:11 to 07:01 = about 7 h 50 min with no build. The cause: the pixel check looked only at blurred images (LOG:362).
- Check or set-up stops (Q1/Q4): about 1 h 15 min measurable. b28 static and style about 1 min; b32 format about 3 min; b34 style to b35 8 min; b37 height about 24 min; b38 code refusal about 10 min (16:20:27 to the fast pass 16:31:55); b40 speed about 30 min.
- Disk and restarts (Q13): b44 about 20 min (LOG:397 item 7); b40 chain died about 20 min (LOG:352); b31 about 2 min. Records lost: not a time cost.
- Q3, Q9, Q11, Q14, Q15, Q16: not measured.

Q1 is ranked first but has one of the smaller measured costs. Q6/Q10 and Q5 have the largest measured costs among the questions.

## 3. Largest time costs no question covers

1. Long rounds run before the review looked at the page. b24's long checks ran 00:28:44 to 02:52:39 and b25's ran 02:55:38 to 05:26:59: 4 h 55 min in all (LOG:269, 271, 274, 280-284). Then the b25 review found 11 faults, so b26 was needed (LOG:286). The order changed only on 6 Nov 07:28 (LOG:294).
2. The spacing check: a Resources-page check used on an Essay page (LOG:179), and not proved before it could stop builds. It was the stopping check in b28, b29 (twice), b30, b31, b35 and b36 (summaries; LOG:303, 327). It was settled mostly by changing the check (LOG:299-300) and by allowed lists (LOG:322-327), not by changing the page. 66 of b28's 230 faults were wrong (BUILD-ORDER.md:57). The b28-b37 window, from the first fast round 07:29 to b37's fast pass 15:08:36, is 7 h 39 min. The share spacing alone cost is not measured.
3. Template decisions asked one at a time as faults turned up. There were 9 template agreements on 5 Nov (BUILD-ORDER.md:54) and many more on 6 Nov (LOG:290, 302, 313, 317). The standing agreement came only on 6 Nov 16:18 (LOG:334). Not measured in total.
4. Work stopped when a turn ended, until a reminder: about 50 min (LOG:254), 10 min (LOG:257), 15 min (LOG:260), 25 min (LOG:270), 23 min (LOG:392). About 2 h in all.
5. The 524-row gate. It was built and proven, then failed b40 with 177 (153 NOT CHECKED; LOG:358-359), took several agreements (LOG:275, 290, 353, 356, 377), and was then not required before her review (LOG:389). Time not measured.

## 4. Corrected list (merged; ranked by measured time where the files allow)

1. "Before you build a fix, did you test it on a copy at every width, measuring what the reviewer looks at (where each line ends, not only the gap)? If it has failed twice, what is the cause?" (old 6, 10, 8). I Spy line at 768 failed review in b41 (Second Stage) and b42-b44 (First stage). b42 to b44 cost 6 h 39 min. The b41 fix was built from the code only (LOG:362). The b44 test measured gap, indent and widest word gap, not the line end, with thresholds Claude set itself (vt/m.py; LOG:397). Reviews saw only 1440, 768 and 390, although D019 says every width.
2. "Has every image the page uses unblurred been looked at for children's faces, and what can go on while I answer?" (old 12, plus the cause). The pixel check covered only blurred images (LOG:362), so 098 and 110 were missed from build 1 to b41. Then there were 7 h 50 min with no build (LOG:361-370), although the I Spy fix had already been tested at 23:37 (LOG:363).
3. "Was this template change, or my agreement, carried out at every width it names and tested with every check before a page build used it?" (old 5, 11). 847b6adb (06:40) caused the faults found at b38 (17:26) and b39 (19:04), 11-12 builds later. Fixing them cost about 4 h 56 min. The 09:16 and 13:38 agreements were done only above 830 px until 6 Nov 06:3x (LOG:288).
4. "Why run the long checks before the review has looked at the page?" (new). b24 and b25 cost 4 h 55 min of long checks, then the review found 11 faults (LOG:269-286).
5. "Is the spacing check judging this page by rules that fit it, and should 1-2 px stop a build?" (new). It stopped 6 of the builds b28-b36, inside a 7 h 39 min window; it was settled by changing the check and by allowed lists (LOG:299-300, 322-327). Its own share is not measured.
6. "When a check stops a build, is it the page, the check or the set-up, and does the check say the same as my agreements?" (old 1, 4). 17 stops in 10 builds. At least 5 were the check or set-up (b28 static and style, b34 style, b38 code, b40 speed likely). 3 more were settled by allowances (b32 format, b35 spacing, b37 height). About 1 h 15 min measurable.
7. "Which kinds of fault do the checks miss and the reviews find, and the other way round, and why did a fault appear once and go?" (old 2, 7, 9). b37/b38: the reviews found 0, then the checks stopped the builds. b41-b44: the fast checks passed, the reviews found 6 page faults (12 with b42's 2-7), and the long round never finished. The cause of b42's faults 2-7 is still not shown by a test. Time not measured.
8. "Can you give me every template decision this page needs in one list, and keep working while I answer?" (new). There were 9 template agreements on 5 Nov alone, and the standing agreement came only on 6 Nov 16:18. About 2 h was lost when work stopped after a turn ended (LOG:254, 257, 260, 270, 392).
9. "Which gate rows must pass before I see the page?" (new). The 524-row gate failed b40 with 177 and was set aside on 7 Nov 10:53 (LOG:358, 389). Time not measured.
10. "Which line of code measures each rule, on the elements this page has?" (old 3). The side-image-top rule appears in 10 rows; tools/v8/place_check.py measures TOP only for floated .mm-float, never .mm-set, and only at 641 px and wider. Time not measured.
11. "What can stop work or lose records without a result?" (old 13; mostly for the assistant to ask itself). Measured about 45 min (b44 about 20 min, b40 chain about 20 min, b31 about 2 min). The b31/b33/b36 records were lost.
12. "Which safeguards hold without your promise?" (old 14). Line 943 of the lessons file says "What held were the scripts". Still only promises: the message checker, and figures only from files.
13. "Which statement in your last message is not from a file?" (old 16; the message checker's job).
14. "What does each way of working cost my allowance?" (old 15). Not measured in any file.

## Corrections after the review (main session, checked against records/DECISIONS-LOG-3-nov.md, 7 Nov 15:xx)
- Item 4: "4 h 55 min" is the window 6 Nov 00:28-05:27; the timed checks in it sum to about 3 h 57 min (b24 run_checks 28 min, quick 3, wrap 68; b25 run_checks 29, images 37 + 10, wrap 62; log 269, 274, 280, 282, 284).
- Item 2: 7 h 50 min (b41 review 23:11 to b42 07:01) holds, but a build that night could only have been a test of the I Spy fix: no image with children may be used before her answer (Project rule).
- Item 8: BUILD-ORDER.md line 54 says "9 template agreements since 5 Nov 04:37", not "on 5 Nov". The stops after a turn ended: 50 min (log 254), 15 (260), 25 (270), 23 (392) = about 1 h 53 min; log 257 is not a stop.
