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
