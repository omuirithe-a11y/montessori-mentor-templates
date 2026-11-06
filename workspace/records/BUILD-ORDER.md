# Build order for every page (owner 6 Nov 2026 07:16 "implement all 6 immediately", 07:33 "saved for all future builds")

This is the order. The scripts enforce steps 3, 4 (refusal without the review) and 6; steps 5 and the gate's check of the order (part of 7) are not yet enforced by code; the rest are rules. Earlier agreements this repeats (they were in
START-HERE or agent instructions and were not followed on 3.5.0): 27 Oct agent instruction E1 "cheapest first" and E3 "13 key widths while fixing, the full set once" (restated 30 Oct); START-HERE Quick start item 5 "on the first build ... screenshots looked at
by a separate agent"; the order START-HERE records as agreed 2 Nov 17:52 (screenshots and the review on the first build, every template question
asked together before any full check).

1. Before build 1: one decisions sheet - every place where Word/PDF and the template need her decision (colours, allowed
   differences, captions, indents, template changes) - sent as ONE question. Template faults found later: one list, one
   question per round.
2. Template changes: tested at every width the agreement names, straight after installing (tools/tablet_check.py for
   641-830), before any page build uses them.
3. Each build, fast round: `tools/check_round.sh <build> <settings> <docx> <pdf> <template> <menu ref> <122-width dir> <slug> fast`
   - code check, static code, Word format, columns, text, style, tablet (641-830), spacing - STOPS at the first fault
   (tools/round_judge.py; allowed faults AF001/AF002 judged as the gate does); then the gate's early run; stops on a fault in
   a fast result.
4. Each build: the separate review (an agent that has not seen the work) of that package, writing <build>/REVIEW.md naming
   the package sha256, last line "FAULTS: N".
5. All faults from 3 and 4 fixed together; ONE new build; back to 3.
6. Only when the fast round passes and REVIEW.md ends "FAULTS: 0": `check_round.sh ... long` - run_checks.sh (122 widths,
   height, lines, placement, speed) and more_checks.sh long (images, wrap). Both REFUSE without the fast pass and the review;
   both stop at the first fault; passed steps are kept after a restart.
7. The gate's full run, then send_gate.
8. Messages: at milestones only; every figure read from a file before the draft goes to the checker; after two failed
   checker rounds, redraft from the files.
9. Any investigation: 20 minutes without the cause -> stop, read the code that sets the thing, say what is known.
10. Every promise made to her: a line in the page's EDIT-QUEUE naming the file that carries it out; the hourly review
    reads the decisions log and lists promises not in code.

## Effectiveness (6 Nov 08:0x, owner 08:01 "Analyse the effectiveness ... then adjust")
Evidence from 3.5.0: rules kept only in documents were not followed (E1 27 Oct, START-HERE item 5, 2 Nov 17:52); what the
scripts enforce was followed. So each item is marked ENFORCED (a script refuses or stops) or RULE (relies on Claude).
- ENFORCED: fast checks first, stop at first fault (more_checks.sh fast) - on b28 the first fault (spacing) was found 07:49,
  19 min after the round began, instead of after the 2.5-hour round.
- ENFORCED: long checks refuse without the fast pass and a review ending FAULTS: 0 (more_checks.sh long, run_checks.sh) -
  tested 07:29 and 07:50.
- ENFORCED: review on every build (via the refusal above, and build_guard.sh below).
- ENFORCED: tablet check 641-830 every round - it also covers "test every agreement at all widths" for tablet widths.
- ENFORCED: restart-safe steps - at 07:37 five passed steps were kept, not re-run.
- ENFORCED (new 08:0x): tools/build_guard.sh, called by the page's build command - a new build is refused while the newest
  build's round is unfinished, or passed without a review report; so all faults of a round go into ONE new build.
  Tested: b29 allowed after b28's round stopped at a fault; a build with no round refused.
- ENFORCED already: checks proved on planted faults - the gate reads tools/check-proofs.json (row A083).
- RULE (weak): one decisions sheet before build 1; messages from files only, redraft after two failed checker rounds
  (drafts still failed 1-3 checker rounds on 6 Nov); promise lines in the edit queue (the hourly review reads them).
- NOT DONE, needs the owner: the gate's own check of the order; the template test page (would find template faults once
  per template change instead of page by page - the largest saving on 3.5.0, where 5 of the build 25 review's 11 faults
  needed the template).
- Weakness found: the fast round is only as good as its checks - the spacing check judged 39 of its 230 b28 faults on a
  median "not in PDF"; such a check must be proved before it can stop a round.

## Effectiveness review 2 (6 Nov 08:1x, owner 08:15 "Analyse the effectiveness ... then adjust accordingly")
The time sinks on 3.5.0, largest first, and whether a solution removes each:
1. Template faults found on the page (9 template agreements since 5 Nov 04:37; 5 of the b25 review's 11 faults; 142 of
   b28's 230 spacing lines) - NOT removed by any enforced item. Only the template test page removes it: first job after
   this page is published, with her yes.
2. Checks not proved before they stop work (the gate: 181 of its own faulty rows on b25; the spacing check: 66 of 230
   wrong on b28; two runner faults stopped b28's round) - PARTLY: proof recorded for the tablet check (check-proofs.json
   eng-6nov-tablet_check, b25 caught / b28 clean); the spacing check still unproved (her answer pending: A, B or C).
3. Faults found late - REMOVED: the fast round found b28's first page fault 19 minutes in.
4. One build per fix - REMOVED: build_guard.sh (b30 refused while b29's round runs - tested 08:1x).
5. Decisions asked one by one - NOW ENFORCED for new pages: build_guard.sh refuses build 1 without an answered decisions
   sheet (DECISIONS_SHEET file with "OWNER ANSWER:"), tested both ways 08:1x.
6. Message rounds - RULE only; not removed (drafts failed 1-3 checker rounds today).

## Added 6 Nov 09:3x (owner 09:25 "#3 to #16 find a solution and/or implement all of them immediately")
- #2 (agreed 09:25): the gate checks the order - INTEGRITY FAULT "order: ..." when the fast round has not passed, the review
  was written before it, or a long check started before the review. Tested: ok order -> no order fault; long stage started
  before the review -> fault (eng35/ordertest).
- #3/#11: the fast round runs the on-screen check at the 13 key widths (band edges) - every agreement's widths are tested on
  every build; the 122 widths run once in the long stage.
- #4: run_checks.sh runs first the widths that failed on the previous build.
- #5: run_checks.sh keeps widths already finished on this package after a restart (vfast --skip-done from its own worker output).
- #6: an early wrap pass every 40 px in the fast round; the 1 px sweep in the long stage.
- #7: gate rows that never fail - analysed; merging them changes the list, so it is put to her with the analysis.
- #8: re-checking only changed sections is covered by #3/#4 (fast faults found in minutes) without leaving any section unchecked
  on the final build.
- #9: spacing check C4-C6 (text on images left out; Word's style/default spacing read; zero-height beige lines not counted).
- #10: START-HERE gets the check order and the pointer to this file.
- #12/#14: the message checker's brief now refuses a second open question, figures not from the listed files, and a third
  round (redraft).
- #13: decisions sheet for this page: pages/the-english-curriculum.decisions.md.
- #15: any investigation: a 20-minute reminder (send_later) is set when it starts; at the reminder, stop and read the code.
- #16: queued in records/TO-DO-next-chat.md (after publishing).

## Added 6 Nov 13:1x (owner 13:07 "will i have the same problems in a new chat?")
- The build guard now runs inside tools/build_page.py itself: any build into a folder named b<N> is refused unless the build
  before it finished its round and has its review (build 1: her answered decisions sheet; low disk refused). A new chat or a new
  page's build command cannot build round it. Tested: a direct build after a build with no round - REFUSED; after b35 - allowed.
- Every rule in this file that a script enforces is in the GitHub workspace (fingerprinted), copied into every new chat by
  tools/setup_workspace.sh; START-HERE (Quick start) points here.

- 6 Nov 16:2x: every template change re-pins the code checks; the re-pinned check needs its proof (new build ALL CHECKS OK, previous build NOT ACCEPTABLE) recorded in tools/check-proofs.json BEFORE the round, or the round refuses it.
