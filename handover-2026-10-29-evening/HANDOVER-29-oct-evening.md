# HANDOVER - 29 October 2026, evening (Asia/Shanghai) - newest handover

Read first, in this order, as the Project instructions say: claude/START-HERE.md, this file, claude/LESSONS-LEARNED-27-29-oct.md,
claude/WHAT-THE-CHECKS-COVER-v5.md, claude/ELEMENTS-TO-CHECK-v11-additions.md.
The full set of today's tools and records is in GitHub: omuirithe-a11y/montessori-mentor-templates, folder handover-2026-10-29-evening/.

## 1. What is done (each measured; evidence in the GitHub folder)

1. Both templates (Essay, Resources): menu back to its earlier sizes; table of contents lines up with the text at 641-1180.
   GitHub commit 20ec0ee. The 10 rebuilt pages then matched the 28 older pages at 19 widths (separate checker PASS).
2. The Role of the Adult - LIVE, uploaded by the owner 18:58, checked 18:59 (live file fetched at 18:58:58 and compared with the zip):
   - live index.html byte-identical to the zip sent (fingerprint f9f4d428...); all 109 image files answer 200; copy protection ON.
   - changes from the 29 Oct 11:21 live download: contents alignment (mm-toc-align); font sizes (mm-type-29oct, 1440: contents label
     20, entries 18, headings 18, quotations 18/40); image 023 above its quotation under 440px (mm-quote-image-29oct); text over
     images fixed at 320-830 (quotation-line script edits); 30px above and 30px below images 020, 028, 034, 046 at 830px and
     narrower (mm-image-gap-29oct and the glTopline edit); fix A (below).
   - checks on the final page: full check 122 widths "every width ok", narrowing 1280->390 sideways 0, height steady (1440 21883,
     390 49493), lines through text 0 at 390/430/641/700/830/1024/1440, gate_live.sh GATE PASSED 17:39.
   - separate checker (on the page before fix A): READY, nothing outside the agreed list visibly changed.
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
     is needed: 10:25, for Biography, Aun Aprendo and A Montessori Journey (their files in Drive folder 1xtrI7iS0_HAEtOvxueB5hXSy0cPoIaSr).
   - Measured on The Role of the Adult (image_sizes.py, 19:2x): all 54 large images under 2900 px, 10 under 1600 px, smallest
     494 px (048.jpg). Whether these are smaller than her originals is not known until she supplies the originals.
   - OPEN: large copies up to 2400 (the build now) or 2900 (what Hostinger sends computers) - pros and cons sent at about 19:16;
     not answered.
2. Fix the slow image opening (fix A) on the other live pages: 15 pages fetched live at 19:26 still have the line, all with
   10 or more images loading as the reader scrolls (list and figures in section 3b). Measure each with speed_check.py first.
3. Known faults, as soon as possible (owner 19:14: "fix all of these asap"): menu panels that do not close on a second click
   (20 older pages, found 29 Oct morning); The History of Education scrolls sideways at 641; contents alignment on the older pages.
4. NOT ANSWERED: whether 4 is building the next page from The Role of the Adult (Biography, Aun Aprendo or A Montessori Journey -
   ask which first, and ask for their extra element kinds: Biography mm-cap; Aun Aprendo mm-name; A Montessori Journey
   formula-divider, sub-label) and 5 adding today's changes to both templates (only with her agreement). Build from the live
   The Role of the Adult, not the templates: the templates lack fix A, the 30/30 gaps, the font sizes and the quotation edits.
5. Workspace set-up step 1 (copy claude/workspace from the Project) was deferred by the owner in this chat; steps 2-4 were done.

## 3. Advice for tomorrow - lessons from 29 Oct, each with its evidence and its limits (revised 19:35, checked statement by statement)

Times are Asia/Shanghai, from file times, commit times and the chat. Where a figure is worked out, not measured, it says so.

1. Check click speed before sending. The Role of the Adult passed the 13:28 gate with clicks of 3-5 s; the fault was found
   14:23 and fixed 17:45. Of 14:23-17:19 (176 min), about 107 min was waiting for the owner (chat record: Claude's answers at
   14:43:55, 15:39:58 and 16:59:47; her next messages at 15:30, 16:22 and 17:19), so Claude's own work was about 69 min. NOW: gate v4/v5 speed_check.py (limits
   50 ms busy, 1.0 s per click, with a 0.7 s download delay; sources web.dev optimize-long-tasks and rail). Tested at 19:3x (tools-v4/TEST-RESULTS.txt): the
   unfixed page FAILS at 1440 (busy 2,379 ms at once, clicks 2.85-3.63 s) and at 390 (1,473 ms, 2.02-3.00 s); the fix-A page
   passes at 1440 (no busy stretch, clicks 0.78-0.80 s); its 390 result and the full gate test are in that file. Limits not yet tried
   on any other page - they may be too strict for brief busy moments (for example a menu opening).
2. Find the cause in the code before changing it. Text over images: six probe scripts at 11:36-11:45 name image 023 and the
   quotation images (file times and contents); the cause found was that the quotation-line script skipped images that do not
   float - that these scripts found it is read from their names and times, not from a record of their output. The 30 px gaps:
   scripts from 11:59 to 12:23 (gap.py, gap2.py, gap3.py, probe7.py, probe8.py), with the owner's answers at 12:12 and 12:15 in
   between, before the causes were found (a stacked image cleared the text beside it; the image-spacing script removed the gap
   above); CSS margins tried first were undone by margin collapse and the page's scripts (this chat's record). Slow clicks: one code recording (prof.py)
   named the re-spacing script. Nothing enforces this; it is a working method.
3. The gate makes the upload zip. The review copy (no copy protection) went live 14:16. The 18:58 upload replaced it, but that
   upload was needed for fix A anyway, so the wrong zip cost no extra upload this time - only the risk of a page without copy
   protection staying live (it was live 14:16-18:58).
   NOW: gate v4/v5 make <slug>-UPLOAD.zip after checking copy protection is present. Being tested.
4. Test several fixes on copies at once. Six fixes measured 16:31:53-16:59:15 (27 min); the one chosen passed every check it
   was put through (122 widths, height, lines, speed, gate). Not enforced. speed-tests/test.py does it but names this page's
   images; it must be made general before reuse.
5. Long runs must save as they go. This morning's first all-pages measurement hit its time limit with nothing saved and was
   rewritten (part of 08:07-10:28; that share not measured; source: this chat's summary of the morning - the morning's own
   record is not available to search). vfast.py resumes; any new long script must too. Not enforced.
6. The separate checker took 48 min (its own report: 2,905,416 ms; 12:38-13:26) after Claude's own checks. Whether starting it earlier saves time on this
   2-processor machine is NOT measured - try it once, timed.
7. Silence and misreading: a 7-minute run of measurements with no message; 16:22-16:30 spent answering a question the owner had
   not asked. About 15 min. Cannot be enforced by a tool.

Not lessons (not proven): that more images means slower clicks (one page measured); that the image-size report finds small
images before a build (it shows only the page's sizes - the owner's originals are not in the package).

## 3b. Tomorrow's biggest job and its cost (worked out, not measured on these pages)
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
  NOT YET TESTED as a whole: v5 = v4 plus the confirmation file and image_sizes.py. send_gate.sh has never been run since its
  folder paths were changed (19:2x) - run it once on a template build before trusting it.
- tools-v4/ - the version tested on 29 Oct (TEST-RESULTS.txt): speed_check fails the unfixed page at 1440 and 390 and passes
  the fix-A page at both; the full gate test result is in that file.
- tools-v3/ - superseded. visual_check.py fingerprint 68026417 is unchanged in every version.
- speed-tests/ - click2.py, busy.py, prof.py, relayout.py, cause.py, test.py (the six-fix comparison), results.txt.
