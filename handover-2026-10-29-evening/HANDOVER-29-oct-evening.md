# HANDOVER - 29 October 2026, evening (Asia/Shanghai) - newest handover

Read first, in this order, as the Project instructions say: claude/START-HERE.md, this file, claude/LESSONS-LEARNED-27-29-oct.md,
claude/WHAT-THE-CHECKS-COVER-v5.md, claude/ELEMENTS-TO-CHECK-v11-additions.md.

## 0. Questions for the owner, still open at 20:31 on 29 Oct - ask them first, one at a time (her rule)

1. The Role of the Adult: confirm the six-item changes list (sample-page/the-role-of-the-adult.changes.txt) in her own words.
   The v5 gate cannot pass that page without it. (The page is already live with the v4-gated zip, so this blocks only a
   future v5 run on it.)
2. ANSWERED 29 Oct 20:00 ("test now"): tools-v5 tested 20:00-20:22 - see section 4. Still untested: send_gate.sh (needs a
   template build).
3. Today's lessons into LESSONS-LEARNED-27-29-oct.md (a whole-file rewrite; the store is 98% full) - try it, or make room
   first (no file deleted without her agreement), or leave them in this handover?
4. A separate agent's check of the live The Role of the Adult with fix A - wanted?
5. ANSWERED 29 Oct 20:00 - the owner: "when i start work tomorrow they will be in google drive". So: at the start of the next
   chat, search Google Drive for them; ask her which folder only if the search does not find them. This was what blocked item 1
   of her order (section 2).
6. SETTLED - not a question. Her words of 29 Oct 10:25: "no blurring needed for any of the three pages in drive" - the PAGES
   (Biography, Aun Aprendo, A Montessori Journey), so no blurring for any of their images, originals included. Do not ask it
   again. The owner, 20:30 and 20:36: the question was "bullshit" - not neutral: the answer was already in her 10:25 words, so
   asking it was wrong. Lesson: before asking her anything, read her earlier words on it; if they answer it, do not ask.
7. Large copies up to 2400 or 2900 px (pros and cons sent 19:14:19)?
8. Is item 4 of her order building the next page from The Role of the Adult, and item 5 the templates? If so, which page first,
   and what are its extra elements?
9. ANSWERED 29 Oct 20:08 - the owner, word for word: "Fix A on the 15 pages: the one image-load line, nothing else – confirmed".
   Saved as fixA-15-pages.confirmed.txt in the GitHub folder. For each of the 15 pages: its <zip>.changes.txt says only
   "Fix A: the one image-load line, nothing else"; its <zip>.confirmed.txt is a copy of that file. It covers fix A only - any
   other change to any of these pages needs its own confirmation.

This replaces the morning's HANDOVER-29-oct.md as the newest handover. LESSONS-LEARNED-27-29-oct.md does NOT yet hold
today's lessons - they are in section 3 below only.
The Project's knowledge store is 98% full (knowledge_size 1,964,188 of max 2,000,000 - the unit is not stated by the tool;
project_info at 19:47 on 29 Oct): a new file or a larger rewrite may not fit. Today's full records are in GitHub. Adding
today's lessons to LESSONS-LEARNED: the tool has no append, so the whole file (size not measured - the tool gives none; it was read in full this chat) must be
written again with the addition - possible only if the store has room for the larger file; not tried, and what the tool does
when a write does not fit is not known. Room-making, if the
owner wants it (nothing deleted; each step needs her agreement, file by file):
- NOT candidates: the 27 Oct AGENT-INSTRUCTION files. LESSONS-LEARNED cites them as evidence by name (Lesson 1 cites
  /home/claude/reports/AGENT-INSTRUCTION-27oct-1240.md line 3; Lesson 2 the -1240, -1245, -1255, -1300 and -1325 files). Those
  /home/claude/reports paths do not exist on this machine (checked 19:52) and no AGENT-INSTRUCTION file is in the GitHub repository
  (its 199 files listed, 19:52), and a Google Drive search found none (19:53; one query: title contains "AGENT-INSTRUCTION" or text contains the
  -1240 file's opening words; one result, an unrelated PDF from 2018, GSA-LSYM_2018sc.pdf - other wordings not tried). The 27 Oct chat "Fixing 9 pages" (https://claude.ai/chat/6563fac0-7704-4194-9908-4b14e4d21ad0) shows the
  -1240 file being written (search 19:53 - the result showed only its first lines, steps 0-3, not the whole file); whether the
  chat holds the whole text of any of these files is not checked. The records repository
  was not searched: it was archived on 20 Oct, before these files existed (START-HERE). So the Project copies are the only
  complete copies found - keep them.
- HANDOVER-27-oct-morning.md (root) and claude/HANDOVER-27-oct-morning.md: compared in full at 19:48 - NOT identical. They
  differ in section 5: the root copy says three agents were running; the claude/ copy says they were stopped and nothing came
  back, so the claude/ copy holds the later state. Its earlier created_at (22:57 against 23:06 UTC) does not contradict this:
  created_at is the first save, not the last - this handover's created_at read 11:06:28 UTC in both full reads (19:46 and 19:47), after many rewrites.
- HANDOVER-29-oct.md (root) and claude/HANDOVER-29-oct.md: identical when both were read in full at the start of this chat
  (source: this chat's summary); not compared again.
- LESSONS-LEARNED-27-28-oct.md (root and claude/): not compared.
- How much room any delete frees is not known: the tool gives no size per file.
The full set of today's tools and records is in GitHub: omuirithe-a11y/montessori-mentor-templates, folder handover-2026-10-29-evening/.

## 1. What is done (each measured; evidence in the GitHub folder)

1. Both templates (Essay, Resources): menu back to its earlier sizes; table of contents lines up with the text at 641-1180.
   GitHub commit 20ec0ee. The 10 rebuilt pages then matched the 28 older pages at 19 widths (separate checker PASS - source:
   this chat's summary of the morning; the checker's report file was not saved to GitHub).
2. The Role of the Adult - LIVE, uploaded by the owner 18:58, checked 18:59 (live file fetched at 18:58:58 and compared with the zip):
   - live index.html byte-identical to the zip sent (fingerprint f9f4d428...); all 109 image files answer 200; copy protection ON.
   - changes from the 29 Oct 11:21 live download: contents alignment (mm-toc-align); font sizes (mm-type-29oct, 1440: contents label
     20, entries 18, headings 18, quotations 18/40); image 023 above its quotation under 440px (mm-quote-image-29oct); text over
     images fixed at 320-830 (quotation-line script edits); 30px above and 30px below images 020, 028, 034, 046 at 830px and
     narrower (mm-image-gap-29oct and the glTopline edit); fix A (below).
   - checks on the final page: full check 122 widths "every width ok", narrowing 1280->390 sideways 0, height steady (1440 21883,
     390 49493), lines through text 0 at 390/430/641/700/830/1024/1440, gate_live.sh GATE PASSED 17:39.
   - separate checker (on the page before fix A): READY, nothing outside the agreed list visibly changed. No separate agent has
     checked the page WITH fix A (the live page) - Claude's own checks only. Do one at the start of the next chat if wanted.
   - owner kept: contents entries left-aligned (live was justified; no visible difference on this page); image 023 gap ~25px.
3. Fix A - slow image opening (owner "yes" 17:19). Cause, measured on the live page: every image that finished loading made the
   page re-space itself from the top (line "q('img.doc-img').forEach(... addEventListener('load', schedule) ...)"); each pass
   1-2 s; 23 of 23 passes were set off by image loads; 0 of 49 passes moved anything by more than 0.5px; clicks waited 3.15-5.60 s.
   Fix A: an image load re-spaces only if the page's size changed (the same test the page's size watcher already uses).
   Six fixes were tested on copies before choosing (results table in the GitHub folder, speed-tests/results.txt): A and B and D
   removed all passes; C (wait 0.3 s) and E (fetch on hover) did not help. Live after upload: clicks 0.53-1.13 s (were 3.15-5.60).

## 2. Order of work - the owner's order of 29 Oct 19:14 (replaces the earlier plan). One page per chat.

1. Images: put the owner's larger originals on every page (owner 19:14: "yes. each page needs the larger originals").
   - Images with children go through the faces rounds first (Project instructions), except where the owner has said no blurring
     is needed: 10:25, for the files of Biography, Aun Aprendo and A Montessori Journey in Drive folder
     1xtrI7iS0_HAEtOvxueB5hXSy0cPoIaSr. Her words say "pages", so this covers every image on those three pages, originals included (settled; section 0, question 6).
   - Measured on The Role of the Adult (image_sizes.py, run 19:24-19:25): all 54 large images under 2900 px, 10 under 1600 px, smallest
     494 px (048.jpg). Whether these are smaller than her originals is not known until she supplies the originals.
   - Where the originals are: the owner, 29 Oct 20:00 - "when i start work tomorrow they will be in google drive". Search Drive
     first; ask her for the folder only if the search does not find them. Not estimated: the number of images is 54 to 250 per page; each image with children needs
     both faces rounds and her answers.
   - The 2400 limit is set in the Project's claude/workspace/tools/build_page.py: big.thumbnail((2400, 2400)), saved at JPEG
     quality 92 (found by a Project search at 19:44 - the line read, the file not run). Changing it to 2900 is one
     number there, plus every page built again from the originals.
   - OPEN: large copies up to 2400 (the build now) or 2900 (what Hostinger sends computers) - pros and cons sent at 19:14:19
     (chat record); not answered.
2. Fix the slow image opening (fix A) on the other live pages (owner's confirmation for all 15: section 0, question 9): 15 pages fetched live at 19:26 still have the line, all with
   10 or more images loading as the reader scrolls (the 15 pages, with image counts, in section 3b). Measure each first: tools-v5 speed_check.py now takes a live page address (https://...) as well as a zip
   (first run on a live address 29 Oct 20:06-20:15: the-culture-curriculum fails badly - see section 4).
3. Known faults, as soon as possible (owner 19:14: "fix all of these asap"; no cause yet measured for any of the three): menu panels that do not close on a second click
   at desktop width (20 older pages, found in the morning of 29 Oct - the list of the 20 is NOT saved in any file found in a search made before 19:36
   (menu_toc.json, before.json, after.json, tocalign.json checked); measure again to find them); The History of Education scrolls sideways at 641 (source: the morning's
   check, recorded only in this chat's summary - re-measure); contents alignment on the older pages.
4. NOT ANSWERED: whether 4 is building the next page from The Role of the Adult (Biography, Aun Aprendo or A Montessori Journey -
   ask which first, and ask for their extra element kinds: Biography mm-cap; Aun Aprendo mm-name; A Montessori Journey
   formula-divider, sub-label) and 5 adding today's changes to both templates (only with her agreement). Build from the live
   The Role of the Adult, not the templates: the templates lack fix A, the 30/30 gaps, the font sizes and the quotation edits.
5. Workspace set-up step 1 (copy claude/workspace from the Project) was deferred by the owner in this chat; steps 2-4 were done.

## 3. Advice for tomorrow - lessons from 29 Oct, each with its evidence and its limits (revised 20:31, checked statement by statement)

Times are Asia/Shanghai, from file times, commit times and the chat. Where a figure is worked out, not measured, it says so.

1. Check click speed before sending. The Role of the Adult passed the 13:28 gate with clicks of 3-5 s; the fault was found
   14:23, the fixed page sent 17:45 and uploaded 18:58. Of 14:23-17:19 (176 min), about 107 min was waiting for the owner (chat record: Claude's answers at
   14:43:55, 15:39:58 and 16:59:47; her next messages at 15:30, 16:22 and 17:19), so Claude's own work was about 69 min (her messages are known to the minute only: 46 + 42 + 19 min of waiting).
   NOW: gate v4/v5 speed_check.py (limits
   50 ms busy, 1.0 s per click, with a 0.7 s download delay; sources web.dev optimize-long-tasks and rail). Tests started 19:23 (tools-v4/TEST-RESULTS.txt): the
   unfixed page FAILS at 1440 (busy 2,379 ms at once, clicks 2.85-3.63 s) and at 390 (1,473 ms, 2.02-3.00 s); the fix-A page
   passes at 1440 (no busy stretch, clicks 0.78-0.80 s) and at 390 (no busy stretch, clicks 0.77-0.79 s). Full gate v4 test on
   the fix-A page (19:33:43 start): GATE PASSED; speed ok at both widths; copy protection present; the UPLOAD zip is
   byte-identical to the zip uploaded at 18:58. Limits not yet tried
   on any other page - they may be too strict for brief busy moments (for example a menu opening).
2. Find the cause in the code before changing it. Text over images: six probe scripts at 11:36-11:45 name image 023 and the
   quotation images (file times and contents); the cause found was that the quotation-line script skipped images that do not
   float - that these scripts found it is read from their names and times, not from a record of their output. The 30 px gaps:
   scripts from 11:59 to 12:23 (gap.py, gap2.py, gap3.py, probe7.py, probe8.py), with the owner's answers at 12:12 and 12:15 in
   between, before the causes were found (a stacked image cleared the text beside it; the image-spacing script removed the gap
   above); CSS margins tried first were undone by margin collapse and the page's scripts (this chat's summary of the earlier part of the day). Slow clicks: one code recording (prof.py)
   named the re-spacing script. Nothing enforces this; it is a working method.
3. The gate makes the upload zip. The review copy (no copy protection) went live 14:16. The 18:58 upload replaced it, but that
   upload was needed for fix A anyway, so the wrong zip cost no extra upload this time - only the risk of a page without copy
   protection staying live (it was live 14:16-18:58).
   NOW: gate v4/v5 make <slug>-UPLOAD.zip after checking copy protection is present. Tested: the v4 gate made the UPLOAD zip only after finding copy protection, and it is byte-identical to the 18:58 upload
   (tools-v4/TEST-RESULTS.txt).
4. Test several fixes on copies at once. Six fixes measured 16:31:53-16:59:15 (27 min); the one chosen passed every check it
   was put through (122 widths, height, lines, speed, gate). Not enforced. speed-tests/test.py does it but names this page's
   images; it must be made general before reuse.
5. Long runs must save as they go. This morning's first all-pages measurement hit its time limit with nothing saved and was
   rewritten (part of 08:07-10:28; that share not measured; source: this chat's summary of the morning - the morning's own
   record is not available to search). vfast.py resumes; any new long script must too. Not enforced.
6. The separate checker took 48 min (its own report: 2,905,416 ms; 12:38-13:26) after Claude's own checks. Whether starting it earlier saves time on this
   2-processor machine is NOT measured - try it once, timed.
7. Silence and misreading: a 7-minute run of measurements with no message (14:23, the owner's question, to 14:30:37, her
   interruption - chat record); 16:22-16:30 spent answering a question the owner had
   not asked. About 15 min. Cannot be enforced by a tool.

8. Times typed instead of read: twice in this chat a revision time was typed ahead of the clock ("19:4x" written at 19:36,
   "19:38" written at 19:37; commit times 19:36:22 and 19:37:17). A written rule (Lesson 26, START-HERE item 40) did not stop it.
   What worked: the command that saves the file sets the time itself (python reading the clock), used from 19:37:29 on.
9. Freeze every file a running check will read. The gate test's changes list was corrected at 19:24 while the test was
   running. Before the edit, the results file was read and showed only test 1's heading, so the gate step (which reads the
   list) had not started; it began at 19:33:43 and printed the corrected list. Checking first made it safe; not editing at all
   would have been safer.
10. Say a file "now says" something only after reading it back from the saved copy. At 19:44 Claude told the owner the
   handover gave the reason for lesson 9 when that line had not been changed (found 19:45; corrected in commit ca405f4). Done so
   far for lessons 9 and 10 only (read back from the saved GitHub copy with git show HEAD:<file>, 19:45 and 19:46) - a method,
   not yet a habit shown over time. Read back the Project copy too: it is the one the next chat reads.
   What each check proves: md5 of the local file = md5 of git show HEAD:<file> proves the GitHub copy is the same file. The
   Project copy cannot be fingerprinted (project_read returns text only); a full project_read proves its content, a
   project_search proves only what the search index holds. Use a full project_read for the Project copy.

Not lessons (not proven): that more images means slower clicks (one page measured); that the image-size report finds small
images before a build (it shows only the page's sizes - the owner's originals are not in the package).

## 3b. Tomorrow's biggest job and its cost (worked out, not measured on these pages)
The 15 pages (images on the page, all loading as the reader scrolls): the-culture-curriculum 250, the-prepared-environment 214, the-sensorial-curriculum 208, the-practical-life-curriculum-2 163, the-mathematics-curriculum 153, a-montessori-journey 152, aun-aprendo 58, the-montessori-curriculum 36, play-varieties-and-characteristics 33, culture-resources 28, biography 23, the-role-of-the-assistant 20, essential-elements 19, sensorial-resources 14, mathematics-resources 12.
Fix A on the 15 other live pages that still have the slow-click line (all 15 fetched live 19:26; every image on them loads as
the reader scrolls). Each page: the one-line change, live_diff, full check, height, speed check, gate, and the owner's confirmed
changes list. On The Role of the Adult (54 images) the full check took 7.5 min today (449 s). On 27-28 Oct full checks took: A Montessori
Journey (152 images) 8 min 54 s, Biography (23 images) 15 min 32 s, The Role of the Adult - Resources 25 min 25 s, The
Practical Life Curriculum (163 images) 1 h 28 min (LESSONS-LEARNED Lesson 16). Biography, with the fewest images, took longer
than Journey - so image count did not decide the time; what else ran on the machine did (Lesson 15). Those 27-28 Oct runs shared the 2 processors with other runs, which slowed them (LESSONS-LEARNED Lesson 15) and vfast.py is
faster, so these figures may overstate; the speed check's time on a 250-image page is not measured either. Measure the first
large page's gate time, then estimate the rest from it.
Not proven: that fix A behaves the same on the three Resources-template pages among the 15 (Culture Resources, Sensorial
Resources, Mathematics Resources) or on older builds - each is measured. "Every image loads as the reader scrolls" was counted
on the 08:09 copies; the 19:26 fetch showed each page's file unchanged since then.

## 4. Tools (GitHub folder handover-2026-10-29-evening/)

- tools-v5/ - USE THIS. gate_live.sh (pages corrected from their live copy) and send_gate.sh (pages built from a template).
  Both now: print <zip>.changes.txt (the changes in plain words) and <zip>.confirmed.txt (the owner's confirming words, copied
  word for word, with the time) and fail without them; run image_sizes.py (report only); run speed_check.py (fails above 50 ms
  busy or 1.0 s per click); require copy protection in the checked zip; make <slug>-UPLOAD.zip (the checked zip) and
  <slug>-NO-COPY-PROTECTION-REVIEW-ONLY.zip. Fingerprints in tools-v5/FINGERPRINTS.txt.
  To use in a new chat: copy tools-v5/ from GitHub to /home/claude/chk/v5 and run the gates from there. START-HERE does not yet
  say this (not updated in this chat).
  The Role of the Adult has its changes list (sample-page/the-role-of-the-adult.changes.txt) but NO confirmed.txt yet: the
  owner has not confirmed the list, so a v5 gate run on that page would fail until she does.
  Test times measured 29 Oct: v5 gate on The Role of the Adult about 6 min (A 20:00:39-20:06:46; C 20:15:51-20:21:56); speed
  check on the live 250-image Culture Curriculum 545 s.
  TESTED 29 Oct 20:00:39-20:21:56 (tools-v5/TEST-RESULTS.txt): (A) with the changes list but no confirmation - printed
  "owner's confirmation missing", every other step passed, GATE FAILED, no zip made; (B) speed check on the live
  the-culture-curriculum (250 images, real network, 545 s): SPEED FAULT - busy up to 2,244 ms at 1440 and 2,150 ms at 390;
  clicks 5.07 s and 21.25 s at 1440, 17.6 s at 390, and 5 of the 8 clicks "did not open" within the 20 s limit (whether the
  page or the click was at fault in those 5 is not established); (C) with no changes list and no confirmation - printed both
  missing, GATE FAILED, no zip made. In A the four 390 click times equalled the 1440 ones; in C they differed, so A's match
  looks like coincidence (not proven).
  Still untested in v5: send_gate.sh has never been run since its
  folder paths were changed (v4 file 19:22:53, v5 file 19:24:42). A run on The Role of the Adult can show only that every step
  runs - it would fail at the template code check, because that page is not template-built. Run it once on a template build
  before trusting it.
- tools-v4/ - TESTED 29 Oct 19:23-19:39 (TEST-RESULTS.txt): speed_check fails the unfixed page at 1440 and 390 and passes the
  fix-A page at both; the full gate passes the fix-A page and its UPLOAD zip equals the 18:58 upload. The missing-list case was
  run to the end in v5 (test C): GATE FAILED.
- tools-v3/ - superseded. visual_check.py fingerprint 68026417 is unchanged in every version.
- speed-tests/ - click2.py, busy.py, prof.py, relayout.py, cause.py, test.py (the six-fix comparison), results.txt.
