# HANDOVER - 29 October 2026, evening (Asia/Shanghai) - newest handover

Read first, in this order, as the Project instructions say: claude/START-HERE.md, this file, claude/LESSONS-LEARNED-27-29-oct.md,
claude/WHAT-THE-CHECKS-COVER-v5.md, claude/ELEMENTS-TO-CHECK-v11-additions.md.
The full set of today's tools and records is in GitHub: omuirithe-a11y/montessori-mentor-templates, folder handover-2026-10-29-evening/.

## 1. What is done (each measured; evidence in the GitHub folder)

1. Both templates (Essay, Resources): menu back to its earlier sizes; table of contents lines up with the text at 641-1180.
   GitHub commit 20ec0ee. The 10 rebuilt pages then matched the 28 older pages at 19 widths (separate checker PASS).
2. The Role of the Adult - LIVE, uploaded by the owner 18:58, checked 19:0x:
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

## 2. Plan for the next chats (one page per chat)

Owner's decisions stand: The Role of the Adult is now the SAMPLE the other pages are built from; the next stage starts in a new chat.

1. Next page from the sample: Biography, Aun Aprendo or A Montessori Journey - ASK THE OWNER WHICH FIRST.
   - Before building, ASK THE OWNER for the extra element kinds each needs (counted on the live pages 29 Oct 11:13: Biography
     mm-cap; Aun Aprendo mm-name; A Montessori Journey formula-divider, sub-label). Do not guess them from the Word file.
   - Owner 10:25: no blurring needed for any of the three. New Word files and PDFs: Drive folder 1xtrI7iS0_HAEtOvxueB5hXSy0cPoIaSr.
   - Build from the live The Role of the Adult (download it fresh), not from the templates: the templates do not yet have fix A,
     the 30/30 image gaps, the font sizes or the quotation-line edits.
2. Fix A on the other live pages. The same line is in both templates, so pages built from them very likely have the slow
   clicks. NOT MEASURED on any page but The Role of the Adult. First measure which pages have the line and their click times;
   then ask the owner the order. Each page: one-line change, live_diff, full check, gate.
3. Templates: add today's The Role of the Adult changes (fix A, 30/30 gaps, font sizes, quotation-line edits) to both templates -
   only with the owner's agreement; it is recorded as "to do later".
4. Images: the owner's originals are well beyond 1600px; the page's large copies are 1208-1600 (images 002, 004, 006, 008 checked;
   probably from the Word file - not checked). Hostinger sends up to 2900 to computers, 1600 to phones (measured 25 Oct, owner
   confirmed 29 Oct). OPEN QUESTIONS FOR THE OWNER: put the originals on The Role of the Adult (faces rounds needed - images with
   children), and large copies up to 2400 (now) or 2900.
5. Known faults, not fixed: 20 older pages have menu panels that do not close on a second click at desktop width; The History of
   Education scrolls sideways at 641; contents alignment on the older pages.
6. Workspace set-up step 1 (copy claude/workspace from the Project) was deferred this chat by the owner; steps 2-4 done.

## 3. What today taught - evidence, and whether anything enforces it (corrected 19:2x after the owner said the first list made claims it could not back)

Time, 29 Oct: 11:21-13:33 page corrected and sent (separate checker 12:38-13:26 = 48 min); 13:33-14:16 the review copy (copy
protection OFF) was uploaded; 14:23-17:19 slow image opening found and six fixes tested; 17:19-17:45 fix A checked, gated, sent.

1. Only agreed changes go out - ENFORCED: gate_live.sh runs live_diff.py (it passed the fix-A page and failed the 13:28 page).
2. Click speed was not checked - the page passed the gate at 13:28 with clicks of 3-5 s, found only after upload. NOT ENFORCED.
3. The review copy was uploaded (14:16) - the gate names only the review copy. NOT ENFORCED.
4. The separate checker started after my checks and added 48 min. NOT ENFORCED.
5. Testing several fixes on copies at once found the answer in one round (six fixes in about 25 min; fix A then passed every
   check). A working method, NOT ENFORCED.
6. Silence (7 min of runs with no message) and answering the wrong question (16:22-16:30) cost time. Cannot be enforced.

Proposed to the owner, NOT DONE, each needs her go: (A) put the click-speed and busy-time test in the gate; (B) the gate also
makes the upload zip (copy protection on) named UPLOAD; (C) start the separate checker as soon as the page is frozen, alongside
the full check.

## 2b. Order of work - the owner's order (19:14)
1. Images: put the larger originals on every page (owner: "yes. each page needs the larger originals"), faces rounds for every
   image with children; large copies 2400 or 2900 - waiting for her choice (pros and cons sent 19:1x).
2. Fix the slow image opening on the other live pages.
3. Known faults, as soon as possible: menu panels not closing (20 older pages); The History of Education sideways at 641;
   contents alignment on the older pages.
4. (her message ended at "4." - asked whether 4 is building the next page from The Role of the Adult, 5 the templates; not answered.)
This order replaces section 2's order.

## 4. Tools

- chk/v3 (GitHub folder tools-v3/): v2 plus fix A in live_diff.py's list. gate_live.sh <zip> <live folder> <full-check file> <out>.
  visual_check.py fingerprint 68026417 (unchanged).
- speed-tests/: click2.py, busy.py, prof.py, relayout.py, cause.py, test.py (the six-fix comparison), results.txt.
