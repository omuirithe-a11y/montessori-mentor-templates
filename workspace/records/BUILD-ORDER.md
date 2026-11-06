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
