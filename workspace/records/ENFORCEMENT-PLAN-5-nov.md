# Enforcement plan agreed 5 Nov 05:48 (first agreement; owner's sentence in DECISIONS-LOG-3-nov.md)

Version sent 05:4x, after nine correction rounds. Four unknowns tested first: whether the gate mod can read a reply's text, sees agents' actions, can be on in every chat, and whether its record can be written by hand while it is off.

**The corrected list:**

1. **One list, with a source for every row.** A new file, tools/REQUIRED-CHECKS.txt. Each row gives:
   - the item and its source, quoted word for word;
   - which pages it applies to;
   - whether a script checks it, or an agent by eye;
   - the script with its fingerprint, the widths, and the line that counts as a pass.

   Every rule about a page in your preferences, MASTER-DECISIONS, START-HERE, the decisions logs, Lessons Learned and the templates' notes becomes a row, or is named as covered by one. A separate agent checks every quote, and that nothing is left out. You get the list as a page to read, grouped and in plain words. It takes effect only with your second agreement (item 14).
2. **New rules.** When you state a new rule about a page, I propose its row in the same reply, with its agreement sentence. Any change to the list needs your written agreement.
3. **Allowed faults in one fixed file.** A new file, tools/ALLOWED-FAULTS.txt, where each allowance quotes its rule. The gates refuse allowances typed in when they are run.
4. **Your confirmation.** The gates already print your confirmation file. New: the message checker compares it word for word with your message and its time.
5. **The gates run the list themselves.** gate.py, send_gate.sh and send_gate_nolive.sh do this on the exact package being sent:
   - Each gate first compares itself and the list with GitHub. It fails if either is out of date, or if GitHub cannot be reached.
   - It finds out for itself whether the page has a live version.
   - For each row a script checks, the gate confirms the script matches its listed fingerprint and runs it on the package itself. The row passes only if that run's output ends in the row's pass line.
   - The gate keeps its results under the package's fingerprint, in a locked folder only it writes to. It resumes from them if stopped, and never accepts a result it did not write.
   - Each row needs a recorded proof that its script failed on a real past fault, or on a planted one where no real fault exists.
   - A row checked by eye needs the agent's report on that package. It is marked in the printout as resting on that report.
   - The gate refuses a package that contains a preview band.
   - Any row that fails, or has no check yet, gives GATE FAILED. The printout lists every row. The upload zip's name carries the same 8 characters as the printout's first line.
6. **Every build runs the whole list.** build_page.py calls run_checks.sh and stamps each build with a mark. It refuses to build unless the mod's record was written within the last few seconds, for that command. run_checks.sh keeps its results in a locked folder only it writes to. Between builds, a result is reused only for a file that is byte for byte the same. The older gates are retired: send_gate_v7.sh, gate2.sh and the v7 folder.
7. **Test copies kept.** Build 7 and every other build with a real fault are kept for the proofs in the private templates repository, with only the released blurred images.
8. **The gate mod.**
   - **Previews and pages.** It reads the list. It refuses to publish anything that carries a build's mark, or that its existing tests (folder, hero, title) show to be a site page, until run_checks.sh has run every row with a check on that exact file. It accepts no result run_checks.sh did not write. The page carries a band at the top naming each row that failed, each row with no check yet, and each eye-checked row with no report on that exact file.
   - **Replies.** It refuses to end a reply, or to send a message during work, unless the message checker passed that exact text. The checker's pass rests on that agent's report, and the reply says so. UNCHECKED is allowed only when the checker's own record shows it could not run, not that it failed the message. Every UNCHECKED reply is counted.
   - **Its record.** At the moment it allows a command, it writes the record that build_page.py looks for.
   - **What the lock covers:**
     - the list, the allowed faults, the gates, gate.py, run_checks.sh and build_page.py;
     - every check script a row names, both briefs, the proofs, and the mod's own folder (at its real path);
     - setup_workspace.sh, FINGERPRINTS.txt and the start-chat skill;
     - the gate's results folder, run_checks.sh's results, each build's stamp, the mod's record, gate.json, the gate printouts, the eye-check reports and the message checker's passes.
   - **How it locks.** Joined commands that touch a locked file are refused. Each locked file opens only when your message has "unlock gate" and that file's short name, which I give you when I ask.
   - **Tested first.** Whether it can read a reply's text, whether it sees what agents do, and whether it can be on in every chat. I test these before anything else is built, and tell you the results. Each chat's set-up table shows whether the mod is on.
9. **One fixed review brief.** A new file, tools/briefs/REVIEW-BRIEF-STANDARD.md, replaces the per-page briefs. The gate checks that the review is of the package being sent, and that it lists every row as checked or not checked.
10. **The message checker.** It fails any message that says a page passed unless the message quotes the gate printout. It also fails any message that names a preview without either quoting that build's run_checks.sh summary or saying it has not passed. A summary counts only if it shows every eye-checked row as reported on.
11. **Every change made visible.** At the start of every chat, setup_workspace.sh prints every change to the locked files since the last handover, with its commit and your agreement sentence. It also prints the number of UNCHECKED replies. A change without your sentence is a fault, and I tell you about it first.
12. **Every chat.** All of these files are in GitHub, so every new chat gets them. A chat already running is stopped by the gate's GitHub check until it updates. Until the new checks are proven, no chat can send a page, the Resources chat included.
13. **Project files.**
    - claude/START-HERE.md points to the list and the gates.
    - claude/WHAT-THE-CHECKS-COVER v6 is printed from the list.
    - claude/ELEMENTS-TO-CHECK v12 adds the new elements.
    - claude/MASTER-DECISIONS.md, the decisions log and Lessons Learned record the decision.
14. **The order of work.** Your first agreement (below), then the mod test (item 8), then the list, then your second agreement to the list, then the checks written and proven, then The English Curriculum. Until then, no page can pass. I time the first check, then give an estimate from it and call it an estimate. Lesson 16 shows such estimates have been missed by 8 to 40 minutes.
15. **What only you can do.**
    - Change the Project instructions:

      [claude.ai/project/01a0ec78-fb6e-7351-8ff0-4a763339a1b0](https://claude.ai/project/01a0ec78-fb6e-7351-8ff0-4a763339a1b0)

      Open the link, find the Project's instructions and edit them: replace the old text with the new, then save.
      - Old: "Before fixing any page: run every check on its first build (full 122 widths, height, format, lines through text, screenshots against live). Send a page only through send_gate.sh, with its printout ending GATE PASSED."
      - New: "Run every row of tools/REQUIRED-CHECKS.txt that applies to the page on every build, starting with the first. Send a page only through the gate, with a printout that lists every row and ends GATE PASSED. Any change to the list, the allowed faults, the gates or the check scripts needs my written agreement."
    - When I ask to change a locked file, copy the words I give you ("unlock gate" and its short name) into your message.
    - Save the start-chat skill and the gate mod from the cards I send.
    - At the start of each chat, read the list of changes in the set-up table. Before each upload, check that the printout lists every row and ends GATE PASSED, and that the 8 characters on its first line are in the zip's name.

To agree to the system, the sentence is: "I agree to put the checks in tools/REQUIRED-CHECKS.txt and the allowed faults in tools/ALLOWED-FAULTS.txt, each row with its source quoted, and to make gate.py, send_gate.sh, send_gate_nolive.sh, run_checks.sh, build_page.py and the gate mod require every row that applies, for every page built from now on, with any change needing my written agreement; the list itself takes effect only after I agree to it separately."

The English Curriculum preview (build 7, not passed, has known faults):

[claude.ai/artifact/1HAzuhZq743dq8qeTJCa8n](https://claude.ai/artifact/1HAzuhZq743dq8qeTJCa8n)
