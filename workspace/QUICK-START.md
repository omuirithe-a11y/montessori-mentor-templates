## Quick start (30 Oct 2026, 11:54 - the owner's words: "implement all 8")
(Prepared 30 Oct for the top of claude/START-HERE.md; not yet in START-HERE - see the 30 Oct handover.)
Do these first, in this order. Everything further down stays in force; this section only changes where the working files come from.
1. Workspace: from GitHub, not the Project. Attach omuirithe-a11y/montessori-mentor-templates (add_repo, push access), clone it, copy its workspace/ folder to /home/claude/mm and its Essay and Resources Code Templates and org-rule.html to /home/claude/mm/templates/. Then, in workspace/, run `sha256sum -c FINGERPRINTS.txt`: every line must say OK, otherwise stop and tell the owner. workspace/PROVENANCE.md says where each file came from. This replaces step 1 of "Set up the workspace first" below (steps 3 and 4 still apply; yunet.onnx is in workspace/faces/). The Project's claude/workspace/ is the older copy: reference only, never copied in again.
2. Read the Project's saved preferences (the memory file preferences.md for this Project) before any work. The 28 Oct note "image descriptions are not necessary anymore" is there; it was missed on 30 Oct.
3. Read claude/DECISIONS-LOG.md: every decision the owner makes, one line each, her words and the time. Add a line the moment she decides something.
4. Current versions: Essay Code Template sha256 3ebaef3a0922e9ea... (commit 13175ad, 30 Oct); check tools: handover-2026-10-29-evening/tools-v5 in the same repository.
5. First-build checks: workspace/tools/run_checks.sh runs the 122 widths, the height and lines through text side by side, then the speed check alone (other checks running at the same time would distort its timings). Every check still runs.
6. Reporting what was checked: one table, every item marked "checked (how)" or "not checked".
7. Questions to the owner: all open ones together, in one message.
8. End of each chat: changed working files go to GitHub workspace/ with new fingerprints (sha256sum -c must pass on a fresh clone); the Project holds the rules and notes.

