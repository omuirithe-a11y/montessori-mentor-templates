# Separate review - The English Curriculum (3.5.0), build 41, zip sha256 90e53864ac2f4650e0f4136a85595ecd55660501bc342b638e895952e167548f

- Time: started Fri 6 Nov 2026 22:57:47 CST (from `date`, after /home/claude/mm/build-35/b41/shots/READY appeared; chain41.log: "fast passed; screenshots 22:55:10", "screenshots ready 22:57:41"); report written 23:0x CST.
- Build folder: /home/claude/mm/build-35/b41. Zip: the-english-curriculum.zip, sha256 90e53864ac2f4650e0f4136a85595ecd55660501bc342b638e895952e167548f (sha256sum). Build 40 zip for comparison: 44d8c51b3d5f0b704fc2475e1cde811111634ce727906829bc3c387839c79d32.
- Briefs: /home/claude/mm/tools/briefs/REVIEW-BRIEF-STANDARD.md, with the owner's rules from /home/claude/mm/tools/briefs/ENG-REVIEW-BRIEF.md "The owner's rules" (where the two differ on layout, I followed the standard brief - see fault 4).
- No browser, no build, no check script run. Measurements made with PIL/numpy on the screenshots and image files. No file changed except this report.

## What was compared
- Build 41 against build 40, files: b41/preview has 328 files; all are byte-identical to b40's (sha256) except index.html (b40 14bb3c4d..., b41 28639316...). All 326 files in b41/images are byte-identical to b40/images. The template file used is unchanged: index.html differs from b40 at exactly three places, nothing else (diff of the two files):
  - Word paragraph 246 (First stage): b40 `sound:<em>  "I Spy` -> b41 `sound:<span class="mm-t">TAB TAB</span><em>"I Spy`
  - Word paragraph 251 (Second Stage): b40 `sound.<em>  "I Spy` -> b41 `sound.<span class="mm-t">TAB</span><em>"I Spy`
  - Word paragraph 254 (Third Stage): b40 `sound. <em>"I Spy` -> b41 `sound.<span class="mm-t">TAB</span><em>"I Spy`
  - span.mm-t is the template's tab style (Essay Code Template.html line 528: `white-space:pre; tab-size:48px`, "Word's tabs kept - stops every 48px (Word's half inch)"). Word (python-docx) has 2, 1 and 1 tabs at these places, so the counts match. Build log /home/claude/mm/build-35/b41.log line 362: "settings - Word's tabs before the mid-line 'I Spy' quotations put back (mm-t) - 3"; otherwise b41.log differs from b40.log only in its own folder names.
- Build 41 against build 40, screenshots: all 85 parts (1440: 21, 768: 26, 390: 38; same counts and sizes as b40) compared pixel by pixel. Only four parts differ, and only on the text rows of the three stage lines: w1440-part06 rows 185-203, 488-506, 675-693; w768-part07 rows 546-564, 575-593, 897-915, 1144-1162, 1173-1191; w390-part10 rows 1202-1218, 1230-1246; w390-part11 rows 206-222, 234-250, 558-574, 586-602. The page height and everything else is unchanged at all three widths.
- The changed parts at full size beside PDF p6 (First stage) and p7 (Second, Third Stage) (/home/claude/eng35/review31/pdf/p06.png, p07.png). Measured gaps between "sound:"/"sound." and the opening quotation mark:
  - 1440 (w1440-part06; text column starts x=151): First stage quotation at x=345 (194 px from the column edge = 4 tab stops of 48), Second x=297 and Third x=297 (146 px = 3 stops). The PDF p6/p7 has the quotations at about 1.98 in and 1.5 in from the margin, that is 4 and 3 of Word's half-inch stops. Same stops as Word; the quotation is pushed right with a wide gap, wider in the First stage, as in the PDF. Fixed at 1440.
  - 390 (w390-part10/11): gaps 82 px (First), 53 px (Second), 51 px (Third). Wide gap kept.
  - 768 (w768-part07): First stage 64 px, Third Stage 54 px; Second Stage 9 px only (fault 1).
- Faces: the records in /home/claude/mm/build-35/faces (pixel-check-after-answer.json/.md, sheet-check-final.json, review2.json, photos-final.json, photos-final-names.json, photos-final/), the round 1 sheet /home/claude/mm/blur2/m_eng/eng-sheet.html (text only), /home/claude/mm/blur2/m_eng/faces.json and faces/keep_unblurred.json, and every one of the page's 163 full-size images in b41/images. Each page image was matched to its Word image: 104 are the blurred photos-final images (102 matched directly; 042.jpg and 096.jpg are Word's own crops of image43.jpeg and image102.JPG, checked against the srcRect in the Word file); in each, the pixels where blur and original differ match the blurred file (mean difference 0.6-4.9 levels, 28 on the tiny 042.jpg) and not the original (51-90 levels). The other 59 are recorded "no face to blur - the original is used as it is"; I looked at all 59 (contact sheets, then full size where a child's face could show).
- Records: /home/claude/mm/records/DECISIONS-LOG-3-nov.md, /home/claude/mm/build-35/b41.log, /home/claude/mm/build-35/b40/changes.txt (b41/changes.txt does not exist).
- Not given new looks (identical to b40 by pixel compare, checked there by /home/claude/mm/build-35/b40/REVIEW-FULL.md): all other parts of the page, at all three widths. Word text: b41's only text change is the three tabs; b40's full word-by-word compare stands. One detail: Word has a space before the tabs in paragraphs 246 ("sound: \t\t") and 251 ("sound. \t"); the page has none. A space before a tab is not shown in the PDF and moves nothing at 1440 (the tab reaches the same stop); not counted.

## NOT checked (whole review)
- Widths other than 1440, 768, 390 (no screenshots). Tab stops depend on where "sound:"/"sound." ends on its line, so at other widths any of the three lines can show a narrow gap as at 768 (fault 1); not looked at.
- Anything needing a browser: menus, swiping, late-loading images, tab order; the published page (not published); the preview artifact.
- Check and gate outputs (not used in place of looking).
- Process rows that rest on the chat (marked in the table).

## Faults

### PDF p7 (Second Stage) - 768 only
1. At 768 the Second Stage quotation still runs straight on. w768-part07 rows 897-915: "... always identifying the *ending* sound. "I Spy with my little" - "sound." ends at x=582, the quotation mark starts at x=591 (9 px; build 40 had 10 px). PDF p7 shows a wide gap (tab) before ""I Spy with my little eye, something ending with ....". The tab span is in the code (b41 index.html), but at this width "sound." ends just before a 48 px tab stop, so the tab is only a few pixels wide and justification makes it look like a word space. First stage (64 px) and Third Stage (54 px) at 768, and all three at 1440 and 390, show the gap. No owner rule found that excuses it. It is Word's tab behaving as a tab (a Word tab also moves only to the next stop), so if she accepts it, it is one wording item.

### PDF p14 (Cutting) and p14-p15 (Metal Insets) - children's faces not blurred (all widths; the page links each image's full-size file, data-full)
2. images/098.jpg (Word image99.JPG; the Cutting row of five, under "On this shelf I prepare a range of different, increasingly complex cutting exercises..."; w1440-part12/13, same image in b40): a boy cutting paper, face in profile looking down. At full size his eye (lashes), nose, mouth and cheek are clear and unblurred. faces.json (blur2/m_eng/faces.json, "image99.JPG", no 98) has only 98-a, "a printed picture on the shelf at the back (8 px)"; the boy's face was not found by the detectors. The round 1 sheet showed this image whole ("Image 98 (image99.JPG)", only 98-a boxed); her round 1 answer (review2.json) does not name it. The separate pixel check after her answer looked for missed faces only in the 104 blurred images (pixel-check-after-answer.md part 5), so this image was not looked at there. Rule: B104 "All photos of children are blurred"; pixel check criterion "no child's face with an eye showing is unlettered and unblurred".
3. images/110.jpg (Word image112.jpg, faces data image110.jpg, no 109; the Metal Insets row of six, after "...it appears effortless and perfectly natural."; w1440-part13): a girl colouring a metal-inset drawing, face turned down. At full size her eyelid and lashes, nose, cheek and ear are clear and unblurred. faces.json has only 109-a, "a hand holding a pencil, not a face". The round 1 sheet showed the image whole with only the hand boxed; not named in her answer; not in the pixel check's missed-face search (only the 104 blurred images). Same rules as fault 2.
- Not counted, for her to see: images/109.jpg (Word image114.JPG, faces data image113.JPG, no 112; same Metal Insets row): a girl resting her cheek on her hand, looking down. At full size hair and hand hide most of the face; no eye, nose or mouth is readable. This image was never shown to her: the round 1 sheet lists image 112 among the "44 images with no face found ... not shown", and the pixel check did not look at it.
- The other unblurred children I looked at are left by her answer or by rule in faces.json: 085.jpg (87-a, 87-b "left unblurred by your answer"), 102.jpg (106-a, her answer), 105.jpg (103-b, her answer), 111.jpg (faces behind cards, 113-a her answer), 116.jpg (printed image), 046.jpg and 152.jpg (archive images); the rest show backs of heads or faces turned away (005, 006, 009, 015, 041, 086, 088, 089, 090, 108, 114, 129, 130).

### The brief (process)
4. Row C112 "The review brief must not tell the reviewer that layout comes from the template". The owner's-rules section I was told to use (tools/briefs/ENG-REVIEW-BRIEF.md line 12) says: "layout, spacing, font sizes, menu and footer come from the template, not from the PDF". REVIEW-BRIEF-STANDARD.md line 3 says the opposite (the earlier excuse "was wrong"). I followed the standard brief; the ENG brief's line 12 should be fixed.

### Not counted - template items awaiting her (from build 40's full review; those parts are pixel-identical in build 41)
- 390: Writing Stages list split by the writing-strip image (w390-part25); Symbol Box tab lists and Phoneme/Grapheme lines lose their columns (w390-part13, 34, 37); gaps where Word's columns join (w390-part30).
- 768: Word Study label lines justified with wide gaps (w768-part23); Article/Verb text in a narrow justified column (w768-part22); swipe dots centred on the text column (w768-part06 and others).

### Build log WARNING lines (b41.log, identical to b40.log)
- Lines 187, 276, 280, 289, 291, 293 (mostly white edge on image62.png, image149/147/157/158/159.jpg): these are cards, book pages and word lists (058, 145, 147, 154, 155, 156.jpg); their white is part of the card, as in the PDF; not a fault (as build 40).
- Lines 332-335 (heading not found in Word: "Letter Bingo: learning / teaching", "Art/Drawing/Colouring", "Series 1 / Series 2"): kept as built; pixel-identical to build 40, where they were checked as the PDF.
- Lines 34-36 still say "tab after long text shown as a space"; line 362 puts the tabs back afterwards, and the code shows the tab spans. The build log could be clearer, not a page fault.

## Eye rows (all 143 rows of /home/claude/eng35/b40-eye-rows-full.txt)

Rows marked FAULT rest on faults 1-4 (B055, B061, C110 on fault 1; A067, B104 on faults 2-3; C112 on fault 4); they are not extra faults. "checked" for process rows means verified in the file named.

| Row | Result | What I looked at / why not |
|---|---|---|
| A007 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; all 326 image files byte-identical to b40 (sha256); object images (grammar-symbols box 153.jpg, tray 163.jpg) on beige, no white box seen |
| A008 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; page images 042.jpg and 096.jpg checked against Word's own crops (srcRect l/b on image43.jpeg, r on image102.JPG): the page shows exactly Word's crop, nothing more cut |
| A009 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; the only crops found are Word's own (srcRect on image43, image45, image81, image101, image102 in the Word file) |
| A015 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (delivery message) |
| A025 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A026 | checked | this report: each claim names the file, screenshot part or measurement; the rest marked NOT checked |
| A029 | checked | all 326 image files in b41/images and b41/preview/images byte-identical to b40 (sha256); the only page change is text (three spots in index.html) |
| A039 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A040 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A055 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (owner's go) |
| A056 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (owner's go) |
| A067 | FAULT | faults 2 and 3: two images on the page show a child's face unblurred at full size (098.jpg, 110.jpg); the faces records themselves are present and passing |
| A068 | checked | faces: excluded kinds left unblurred: adults (man in 049.jpg, woman in 042.jpg, woman in 012.jpg), printed image clipped to the easel (116.jpg), archive images (046.jpg, 152.jpg); pixel-check-after-answer.md part 2: 18 left by rule |
| A069 | checked | faces: review2.json records round 1 words ("No blurring needed on the following: 4i. 14b. ...") and round 2 "approved" 5 Nov 10:04; the words come from the chat, recorded in that file |
| A071 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; alt="" on images in b41 index.html; her 28 Oct rule says not needed |
| A073 | checked | changed parts (w1440-part06, w768-part07, w390-part10/11) looked at full size beside PDF p6-p7; all other 81 parts pixel-identical to b40, identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| A080 | NOT checked | needs the published page in Chrome (no browser allowed; not published) |
| A082 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; images byte-identical; only text rows differ in the screenshots |
| A084 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A085 | checked | this report gives the file/part/measurement for each claim |
| A086 | checked | this is a separate agent's review of build 41 (I did not make the page) |
| A089 | NOT checked | needs the published page |
| A093 | checked | faces: pixel-check-after-answer.md part 4: every final file the size of its original; my compare: each of the 104 blurred page images (2900 px long side) matches its photos-final file (mean difference 0.6-4.9 levels in the blurred areas) and not the original (51-90 levels) |
| A095 | checked | faces: 116.jpg (printed image of a child clipped to the easel) left unblurred; faces.json 115-a "printed photo ... rule item 7" |
| A096 | NOT checked | faces: the round 1 sheet's header text (blur2/m_eng/eng-sheet.html) says each blurred area is outlined; the sheet's pictures were not opened |
| A099 | checked | faces: blurred faces opened at full size on 004.jpg, 054.jpg, 069.jpg, 117.jpg: face covered, soft edges, same strength; pixel-check-after-answer.md part 1 (267 faces) |
| A100 | checked | faces: records in order: round 1 sheet check 4 Nov 22:01 (eng-sheet.html banner), her round 1 answer 5 Nov 09:31 and round 2 sheet check 10:00:43 (sheet-check-final.json), round 2 answer 10:04 (review2.json), final images 10:05 (file times), separate pixel check PASS 10:33 (pixel-check-after-answer.json), build 41 22:43. The steps were done; faults 2 and 3 are faces the steps missed |
| A101 | NOT checked | no replacement image recorded for this page in the files given |
| A104 | checked | faces: the full-size crops above: each blurred face still reads as a blurred face, not a blank patch |
| A105 | NOT checked | faces: round 2 sheet (blur2/m_eng_r2/round2.html) not opened; only sheet-check-final.json's summary read |
| A106 | checked | faces: adults seen unblurred at full size: man 049.jpg, woman 042.jpg, woman 012.jpg; pixel-check-after-answer.md part 2 (64-c teacher 17% inside a child's feather, as the method allows) |
| A114 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A116 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A221 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A223 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A224 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A234 | NOT checked | about other pages' structure, not this page |
| B013 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md (w1440-part01: six entries in two columns) |
| B022 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B023 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (a check round was running on this machine during this review, by design) |
| B055 | FAULT | fault 1 (768, Second Stage: the tab before the quotation shows as a 9 px gap) |
| B061 | FAULT | this separate review at 1440, 768, 390 found fault 1 |
| B072 | checked | Word crops (srcRect) on image43.jpeg and image102.JPG measured: page images 042.jpg/096.jpg are those crops of the blurred finals; others identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| B085 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| B087 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| B095 | checked | faces: blur2/m_eng/eng-sheet.html carries the banner "Checked by a separate agent at 22:01 CST 4 Nov 2026 - PASS - check v3"; her round 1 answer is 5 Nov 09:31 (review2.json). When it was sent rests on the chat |
| B104 | FAULT | faults 2 and 3 (098.jpg boy, 110.jpg girl: faces unblurred) |
| B107 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| B108 | checked | faces: pixel-check-after-answer.json "pass": true, 10:33, after her 10:04 answer |
| B111 | checked | faces: pixel check after her answer had "faults": [] (pixel-check-after-answer.json), so no fix round was needed |
| B113 | checked | faces: all 104 photos-final files dated 5 Nov 10:05, before the 10:33 pixel check, none changed since; the page images are scaled from them (my compare, A093) |
| B114 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B120 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| B132 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B152 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (a check round was running beside this review, by design) |
| B166 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B180 | NOT checked | about build 1's process |
| B181 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B205 | NOT checked | about every check on build 1; check outputs not used in this review |
| B206 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (what was sent with the sheet) |
| B207 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (what was sent with the sheet) |
| B209 | checked | faces: blurred faces at full size unreadable (A099 crops; pixel-check-after-answer.md part 1). The unblurred faces of faults 2 and 3 are counted under B104 |
| C005 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| C006 | NOT checked | faces: sheet checks present (sheet-check-final.json pass; eng-sheet.html banner), faces data present (blur2/m_eng/faces.json); what was sent with the sheet rests on the chat |
| C008 | checked | faces: pixel-check-after-answer.json: pass true, 104 images, 267 blurred faces, faults [] |
| C088 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| C110 | FAULT | fault 1 is a difference from the PDF with no written owner rule |
| C112 | FAULT | fault 4: the owner's-rules section I was told to use (tools/briefs/ENG-REVIEW-BRIEF.md line 12) says "layout, spacing, font sizes, menu and footer come from the template, not from the PDF"; I followed REVIEW-BRIEF-STANDARD.md (line 3, layout not excused) where they differ |
| D004 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D005 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D006 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D011 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D012 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D013 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D019 | checked | all 85 screenshot parts at 1440 (21), 768 (26), 390 (38) pixel-compared with b40; the 4 changed parts looked at full size; the rest identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D020 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D022 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D030 | NOT checked | needs late-loading images in a browser |
| D041 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D044 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D045 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D056 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D060 | NOT checked | needs the lines check at 8 widths; by eye no beige line through text in the changed parts |
| D062 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D063 | checked | screenshots reviewed (D019); new checks for missed kinds are for the main session |
| D069 | NOT checked | my brief also named the intended change and gave build 40's review; whether that narrows it is for the owner |
| D070 | NOT checked | READY of the independent check is the main session's record |
| D075 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D077 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D093 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D094 | NOT checked | needs the check outputs |
| D098 | NOT checked | READY of the independent check is the main session's record |
| D099 | NOT checked | preview artifact not opened (decisions log line 360 says preview version 34 = build 41; not verified) |
| D107 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D109 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md (no table in Word or on the page) |
| D114 | NOT checked | browser action: swipe rows not swiped |
| D121 | NOT checked | browser action: menu not opened |
| D123 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; the three changed lines have no line round the quotation |
| D126 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D130 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; the new tabs are mid-line (after "sound:"/"sound."), not before a quotation's first line |
| D134 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D138 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D140 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; Word crops matched (B072) |
| D155 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D170 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D195 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D197 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D199 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md (footer parts w1440-part21, w768-part26, w390-part38 unchanged) |
| D206 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D219 | NOT checked | no pair of two upper images over one lower image on this page; nothing to compare |
| D294 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D295 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D297 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D298 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D300 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D301 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D312 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D313 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D314 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D315 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D317 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D320 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D322 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D325 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D326 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D329 | NOT checked | not measured |
| D330 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D331 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D334 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D340 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| D342 | NOT checked | side-image heights not measured against their text |
| D344 | NOT checked | not measured |
| E007 | checked | this report has the table |
| E009 | checked | records/DECISIONS-LOG-3-nov.md: HOURLY LESSONS REVIEW lines 301, 306, 312, 319, 324, 328, 333, 335, 339, 341, 352, 357, 359 (6 Nov 09:50 to 22:2x), none more than about 70 minutes apart |
| E010 | checked | records/DECISIONS-LOG-3-nov.md line 302 (09:55) and line 354 (20:4x for 103647a) name the change, "at every width" and the pages; build 41 changed no template code (b40/b41 index.html differ only at the three tab spots) |
| E011 | NOT checked | gate and check results not given to me |
| E013 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E020 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E021 | checked | faces: review2.json "final" and pixel-check-after-answer.json (pass) both present in build-35/faces |
| E033 | checked | this report says image throughout (the page's own word "photo" is hers) |
| E034 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E035 | checked | 390 changed parts (w390-part10/11) looked at; other 390 parts identical to build 40 (pixel compare), checked there by REVIEW-FULL.md |
| E052 | checked | identical to build 40 (pixel compare), checked there by REVIEW-FULL.md; the changed lines have no beige line near them |

Date at writing: Fri Nov  6 23:10:30 CST 2026

NOT CHECKED: 76
FAULTS: 4
