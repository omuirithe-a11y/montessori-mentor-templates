# HANDOVER 29 Oct 2026 (07:5x Asia/Shanghai) - for the next chat, which decides the order of work

The owner's instruction (29 Oct 07:48): "I want a new chat to decide on the order of work." Nothing below is a decided order. This file gives the state and where every piece of evidence is. Read it with the files the project instructions list.

## Where the evidence is
1. **Project files** (claude.ai project "Montessori Mentor"; it is nearly full - 1.95 of 2.0 MB on 29 Oct): this file; claude/LESSONS-LEARNED-27-29-oct.md; claude/WHAT-THE-CHECKS-COVER-v5.md; claude/ELEMENTS-TO-CHECK-v11-additions.md; claude/REVIEW-28-oct.md (an independent review of 28 Oct, every point cited); claude/START-HERE.md; claude/SETTLED.md; claude/MASTER-DECISIONS.md; claude/DECISIONS-27-oct.md; claude/FAULT-LIST-27-oct.md; HANDOVER-16-oct-evening.md (owner answers on swipe rows, 1C/2A/7A).
2. **GitHub** omuirithe-a11y/montessori-mentor-templates (the only source of the templates). Folder `handover-2026-10-29/` holds everything the project has no room for:
   - `HANDOVER-29-oct.md` (this file)
   - `live-27oct/<page>.html` - the 9 live pages as they were on 27 Oct, BEFORE the owner uploaded the rebuilt pages. They are the "live copy" every comparison used. The live site no longer has them. For Culture and Sensorial the code check found no image file differing from these live copies; for the other pages see check-results/code-and-format.
   - `tools/` - send_gate.sh, vfast.py, faults_allowed.py, strip_protect.py, watch.sh, join_when_done.sh, stable.py (height), lines.py (lines through text), lines3.py (line comparison with live), foot.py, who.py (which script writes a margin), integrate.sh, run_visual_split.sh, run_parts_reverse.sh, run_check.sh. Paths inside them point to the 28 Oct session folders (/home/claude/reports, the scratchpad): adjust them.
   - `checks-v25/` - strip_compare.py (code check; its template fingerprint must be set to the template used), format_check.py, visual_check.py (sha256 68026417, unchanged since 27 Oct), live_match.py.
   - `check-results/` - every full-check file (`*-visual-full.txt`), height results, code-and-format outputs, and the independent checkers' outputs (chk-cul2, chk-sen2, chk-sen3, chk-sen4).
   - `patches/` - the OLD/NEW patches of 28-29 Oct (patchA-J, JSON) and edits.py (template items 0-41).
   - `docs/` - full ELEMENTS-TO-CHECK-v11.md (80,000 words; too big for the project), AGENT-BRIEF-STANDARD.md (brief for every agent and checker), the lessons, WHAT-THE-CHECKS-COVER v5, the review.
3. **The packages (zips)** are not stored anywhere outside the 28 Oct session (74-143 MB each). The live site serves what the owner uploaded; a package can be re-made by downloading the live page and its files (live_match.py shows the URL pattern), or rebuilt from the template.

## State of every page (facts; package = the zip handed over)
| Page | Template | Package sent (sha256, first 8) | Uploaded | Known faults, not corrected (owner 28 Oct 14:26: "do not correct the pages until I tell you to") |
|---|---|---|---|---|
| The Sensorial Curriculum | Essay b1ec2db | 07581fd2 (no copy protection), from 5cd0c693; sent 29 Oct 03:23 | yes (owner 29 Oct 07:46); not yet proved by live_match.py | none known. Gate PASSED; full check 122 widths ok; height steady 1440/390; lines through text 0 at 390/641/700/1024/1440; checker READY 03:08 |
| The Culture Curriculum | Essay b766638 (dc9bd79 + item 42) | bc59d517 (no copy protection), from c8659f36; sent 28 Oct 18:56 (the commit message's "19:13" is wrong) | yes (owner 29 Oct 07:46); not yet proved by live_match.py | squeezed text at 1020-1050 px ("Also introduced to small group"), the same on the 27 Oct live page. Never checked for lines through text or by screenshots. Sent before its template was committed and before its full check ended (the check later passed) |
| The Mathematics Curriculum | Essay 02f147a (items 29-30) | 8e4b6497 (no copy protection), from 8bae404f; sent 28 Oct 13:21 | yes (28 Oct) | tab gaps (mm-tabs) lost; a staircase of columns (fixed in the template later, page not rebuilt); 23 name lines removed by a template rule |
| A Montessori Journey | Essay ae040de | 9892d2bd (no copy protection), from 38225171 | yes (28 Oct) | 15 beige lines became grey (27 Oct "fixC" script); passed every check then |
| Biography | Essay 575b25b | 21096e7c, from 43051826 | yes | 2 lines removed (same 27 Oct script) |
| Aun Aprendo | Essay 575b25b | 3e510b8d, from 97b8de20 | yes | 2 images (016.jpg, 002.jpg) not served as images. Images with children: the "Faces" rounds in START-HERE apply before any image change |
| The Practical Life Curriculum (slug the-practical-life-curriculum-2) | Essay 575b25b | bab13be5, from 4c59a98b | yes | "390 px height unsettled" (as recorded on 28 Oct; not re-measured since) |
| Sensorial Resources | Resources ddce8cb | ef1820f3, from 80a8b076 | yes | none known; the Resources template got none of the 28-29 Oct fixes |
| The Role of the Adult - Resources | Resources ddce8cb | 6325f972, from f5e6ea1e | yes | none known; as above |

"Uploaded: yes" for the 7 earlier pages is from the 28 Oct record ("live == these"); it was proved then with live_match.py for those pages only as the record states - re-run it to be sure.

None of the 7 earlier pages has been checked for: height after scrolling, lines through text, or screenshots against live. Each has had only the 27-28 Oct checks (code, format, full width check).

## The template (Essay, GitHub main, b1ec2db)
- Items 42-50 (28-29 Oct) were tested only on Culture and Sensorial. The other 7 Essay pages are on older commits (table above), so none of them is on the current template.
- Items 47 and 50 are patches over the spacing scripts (a later script undoing what the spacing did), not a repair. The cause underneath - two scripts setting one element's margin, each measuring the other's result - is still in the template (lesson 32). A repair would change every page: it is the owner's decision.
- Items 42-50 are recorded only in the commit messages and in patches/patchA-J.json, not in edits.py or claude/TEMPLATE-EDITS-QUEUE.md.
- The Resources template (ddce8cb) has none of these fixes; whether it has the same spacing faults is not established.

## Checks and tools (details: WHAT-THE-CHECKS-COVER-v5)
- send_gate.sh: code check, full check of that exact zip (122 widths, faults item by item, narrowing test), height at 1440 and 390 (also after albums); only then makes the no-copy-protection zip. Prints GATE PASSED / GATE FAILED. Tested on known-good and known-bad results.
- Gap: the gate does NOT run lines-through-text or screenshots. Sensorial's lines through text (14 places at 700, 20 at 1440) passed the full check and the gate; only the checker's screenshots found them.
- vfast.py runs visual_check.py's own code faster (one browser per worker, shared queue, band edges first, narrowing once, resumes from saved results). Its results matched the old runner line for line on Culture.
- Background jobs are stopped after 2 hours; long checks must resume (vfast --skip-done).

## Machine facts (28-29 Oct session; a new session may differ - measure)
- 2 processors. 9 browsers at once gave a load of 13 and slowed every check about 2x.
- Full check timings (Sensorial): 82 widths in 54 min with 2 runners (28 Oct 23:2x-00:17); all 122 in 2 h 05 min with the checker and height checks alongside (29 Oct 01:17-03:22).
- An owner's rejected command stopped running agents silently twice (20:23, 21:54 on 28 Oct). Watch every agent (tools/watch.sh) and check all of them after any interruption.

## Settled rules (do not put to the owner as decisions)
Headings smaller than live; quotations without side margins and without lines beside them; spacing set by the template scripts; images beside text 150 px high or smaller; photos in a row under text that would be squeezed (owner's option C, 16 Oct); swipe rows below 831 px: each photo stops mid-screen, space added at both ends (owner 16 Oct, 1C); black/orange text shown as ink rgb(43,43,43); links rgb(4,50,255); typo and UK-spelling fixes; Sensorial only (28-29 Oct): images at most 200 px high at 641-830 px, the touch table's description on its own line at 641-665 px, a reference table's top line 6 px above its first row. Sources: claude/SETTLED.md, MASTER-DECISIONS.md, DECISIONS-27-oct.md, the 28 Oct record. Search the project before asking the owner (owner 28 Oct 18:02).

## Open questions for the owner (known)
1. Which pages to correct, and in what order (standing: do not correct until told).
2. Whether to repair the spacing scripts' root cause (changes every page).
3. Whether the next work also covers the Resources template.

## Owner's standing rules from 28 Oct (in addition to START-HERE)
Times read from the clock; answers only from evidence; plain English; "image", not "photo", in messages; the owner uploads, never the assistant; originals never edited; restart stopped agents at once; stop ineffective work; never search the Internet Archive; the templates on GitHub are the only source; "save this" means a download; the separate checker checks each package before it is sent; copies for the owner are sent without copy protection, named <slug>-NO-COPY-PROTECTION.zip.
