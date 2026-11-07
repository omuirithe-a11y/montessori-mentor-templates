# Separate agent's critique of the solutions list (7 Nov 2026, about 07:5x-08:0x CST) - copied from its report to the main session

(The full report as the agent returned it; the list it reviewed is ../SOLUTIONS-7-nov.md.)

## Two findings that change the plan
1. The early gate stop is broken and nothing obeys it. check_round.sh lines 19-24 stop the round when the gate's early run shows integrity faults, or a FAULT row whose result is a fast result. That happens on every build: checks2/gate-early.txt shows "integrity faults: 3" on b37-b42; row D078 ("this gate + strip_compare.py", met only when every other row passes) matches the FAST pattern strip-nolive; eng35/round-b42-fast.log says "ROUND STOPPED at the gate's early run". chain.sh line 5 ignores the stop: it waits only for checks2/FAST-PASSED, which more_checks.sh line 73 writes before the gate's early run; the long runners also check only FAST-PASSED (run_checks.sh line 17, more_checks.sh line 76). So the gate stop never stopped anything: b37-b40 went on to review and the long round regardless.
2. Most of what S1 proposes already exists: gate_list.py already sorts every row by how it is met (lines 114-631); check_round.sh already runs it on every build; tools/allowed/the-english-curriculum-gate-rows.txt already exists and gate_list.py reads it.

## Verdicts
- S1 REFINE: fix the early gate (leave out the "this gate" rows and the order lines), make check_round.sh write checks2/GATE-EARLY-PASSED and the chain and long runners require it; the guard refuses build 2 while b1's early gate has NO CHECK YET or after-upload rows not in the page's row file. Gaming risk: the assistant writes the "decision" itself (precedents 6 Nov 07:16, 15:4x, 20:1x) - each decision line must carry her quoted words with a time. gate_list.py hard-codes this page's PLAN at eng35/checks-plan/PLAN.md (lines 35-50) - it must be made general before it can plan a new page.
- S2 KEEP the count (bind by sha256 of the source images, not names or counts; lesson 39: the assistant once edited a checker's json); DEMOTE the sheet part: of the three missed faces, sets 98 and 109 WERE on the round 1 sheet (their faces 98-a and 109-a "left by rule"); sheet checks v1-v3 and the owner missed 98-b and 109-b; only set 112 (page 109) was hidden as "no face found".
- S3 REFINE: as written it would not have caught M5 - b42's fault is inside the changed block. Add line boxes, line count, largest word gap on justified lines; run as a fast-round step comparing b(N) with b(N-1); measure after 4 s and after images load.
- S4 DISCARD (fold into S3): commit hashes do not exist at build time; it would not have stopped M4 (made under the 5 Nov agreements, later under the standing agreement).
- S4b REFINE: not "no yes needed" - TO-DO item 1 says to ask her agreement before building the template test page; her words say only "after this page is published".
- S5 REFINE: as written it goes round in a circle; b37, b38, b39 were each stopped by a long-only check (placement, images heights, images swipe) - move those into the fast round at the 13 key widths (needs her yes).
- S6 DISCARD: duplicates the proof refusal in more_checks.sh step() and her standing rule; the gap is that run_checks.sh has no proof refusal at all.
- S7 REFINE: the b40 overlap was gate_list.py (no browser), so a browser lock in serve.sh would not have stopped it; a round lock every tool checks, gate_list.py included; speed results void if anything else ran.
- S8 REFINE: the transcript does not hold the owner's messages before 6 Nov 20:21 - use the log's quoted words; the runners accept any review whose last line is "FAULTS: 0" however many rows it left NOT CHECKED (b42 left 74).
- S9 KEEP (only lines added; HH:Mx as HH:M0); it does not cover times typed in messages to her, which was most of M11.
- S10 KEEP (use file modification times; the cause argument is free text, can be gamed, costs almost nothing).
- S11 DISCARD: the real fault - the hourly review said "Not followed: none" from 7 Nov 00:3x to 05:3x while all work waited about 7 hours; the em-space fix tested at 23:37 could have been built and checked overnight.
- S12 KEEP as later. S13 DISCARD: the 45 allowed lines are template-rule causes (5-6 px), not 1-2 px jitter; the check already allows 1 px.

## Missing mistakes
1. The early gate stop always fires and the chain ignores it.
2. Drafts with unsourced figures and claims (lesson 42 in almost every hourly review; several reached her: 5 Nov 05:35; "6 placement faults" 18:0x, 18:53, 19:0x).
3. Work stopped while waiting for her answers (5 Nov 19:3x-20:2x, 21:18-21:28, 22:1x-22:2x; 6 Nov 01:0x-01:3x; 7 Nov 23:37-06:3x overnight).
4. Agreements carried out narrower than their words (two done only above 830 when they said "641 px and wider", 6 Nov 06:3x; the 11:59 one reached p but not li).
5. Runners used older script versions than the list names (lines.py and place_check.py v1, 5 Nov 16:1x, 19:1x).
6. Promises and agreed plan items not done (5 Nov 05:48 items 3, 5, 6 until 13:42; 16:16 promise kept at 17:1x; chains detached 6 Nov 20:2x - 7 Nov 03:3x; ENG-REVIEW-BRIEF fix said 23:1x, done 23:37).
7. Results that change from run to run, handled case by case (speed b25, b40; height font re-layout; quick looks; b42 review faults 2-7 at 768).
8. Faces round 3 skipped the method (round 1 was a plain images page, 7 Nov 06:40).
9. The owner had to ask about speed seven times (4 Nov 21:39; 5 Nov 13:01, 16:14, 17:49 x5, 18:58; 6 Nov 07:16, 09:25).
10. Two disk-full events, not one (5 Nov 10:3x b17, which also deleted a folder a running pixel check was reading; 6 Nov 09:57 b31).
11. Check scripts changed during runs (check_round.sh edited while the b32 round ran, 6 Nov 11:52; b28 round stopped twice on runner faults 07:30, 07:37).

## Inaccurate statements in the list
- M1: the long rounds were about 38 min (b37), 49 min (b38), 34 min (b39); only b40's about 2 h 20.
- M2: gate_list.py ran on b19 (5 Nov 16:0x: 139 eye rows NOT CHECKED, 8 NO CHECK YET), was sorted on b25, ran early on every build from b37 - the fault was reading only FAULT rows.
- M3: three faces in three images (98-b, 109-b, 112-a); "unblurred since build 1" holds only for that preview.
- M5: the 23:37 test measured gaps every 7 px from 320 to 1920; 6 of the 7 b42 faults are not from the fix.
- M6: one question at a time is her own rule (3 Nov 14:16).
- M8: the log says b40's long round died because the chain was left detached ("as b36's did", 6 Nov 20:23).
- M9: she ruled the spacing check applies to Essay pages (3 Nov 17:23; 5 Nov 04:36); the mistake was its misreadings.
- M13: most differences were 5-6 px from template rules.
