# Separate review - The English Curriculum (3.5.0), build 42, zip sha256 ee6ba2247d286b7351a4521530365b142339225a51f43282c1313ab0e1a47ed7

- Time: started Sat 7 Nov 2026 07:16:28 CST (from `date`, after /home/claude/mm/build-35/b42/shots/READY appeared; /home/claude/eng35/chain-b42.log: "fast passed; screenshots 07:13:48", "screenshots ready 07:16:19"; it does not say "fast round stopped"). Report written 07:3x CST.
- Build folder: /home/claude/mm/build-35/b42. Zip the-english-curriculum.zip, sha256 ee6ba2247d286b7351a4521530365b142339225a51f43282c1313ab0e1a47ed7 (sha256sum). Build 41 zip: 90e53864ac2f4650e0f4136a85595ecd55660501bc342b638e895952e167548f.
- Briefs: /home/claude/mm/tools/briefs/REVIEW-BRIEF-STANDARD.md, with the owner's rules from /home/claude/mm/tools/briefs/ENG-REVIEW-BRIEF.md "The owner's rules".
- No browser, no build, no check script run. Measurements made with PIL/numpy on the screenshots and image files. No file changed except this report.

## What was compared
- Files, build 42 against build 41 (sha256): preview/ 328 files, images/ 326 files, hostinger/ 328 files. Only these differ: images 098.jpg, 098-480.jpg, 109.jpg, 109-480.jpg, 110.jpg, 110-480.jpg (in all three folders) and index.html (preview and hostinger). Nothing else changed.
- index.html: one line differs (line 808), at exactly three places, each an em space (U+2003) added at the start of the tab span: First stage `sound:<span class="mm-t">` + em space + TAB TAB; Second Stage `sound.<span class="mm-t">` + em space + TAB; Third Stage the same. This is change (a). The template code is otherwise the same as b41.
- Build logs: b42.log differs from b41.log only in folder names, the faces lines (round 3 sheet, "yes" 7 Nov 06:46; final sheet check 07 Nov 06:41:53) and "107 from blurred working copies" (was 104). b42/changes.txt names the em spaces and the three blurred images. (b42/fast.log is empty, 0 bytes; b41's had 1589 bytes. Not counted.)
- Change (c): tools/briefs/ENG-REVIEW-BRIEF.md line 12 (file time 6 Nov 23:28) now says "sizes, spacing figures, fonts, colours, menu and footer come from the template; what is on the page and where ... follows the Word file and the PDF". b41 fault 4 is fixed.
- Screenshots: all 85 parts (1440: 21, 768: 26, 390: 38; same counts and sizes as b41) compared pixel by pixel with b41.
  - 1440: only w1440-part12 (rows 1327-1399) and w1440-part13 (rows 0-76, 762-909), x 754-1140: the faces in images 098, 110, 109. Nothing else.
  - 390: all 38 parts pixel-identical to b41 (the em space does not move the tab stop at 390, and the three images are not in view in the swipe rows there).
  - 768: w768-part02 rows 838-957 differ, and from w768-part05 down every part differs; the parts were stitched and lined up: content in b42 sits 12 px higher from part06, 16-17 px from part07, 25 px from part17, 55 px from part23, 85 px from part23-24 to the end. The places where the layout itself differs are faults 1-7. The places where only the offset differs (and half-pixel smoothing of letters) were looked at and are the same as b41.
- The changed parts looked at full size beside PDF p3, p6, p7, p14, p15, p18, p19, p20, p21 (/home/claude/eng35/review31/pdf/).
- The three I Spy gaps, measured on the b42 screenshots (blank run between the last ink of "sound:"/"sound." and the opening quotation mark):
  - 1440 (w1440-part06 rows 185-203, 488-506, 675-693): First 78 px, Second 51 px, Third 49 px (the same pixels as b41).
  - 768 (w768-part07): First 101 px ("sound:" now starts line 3, row 566-584, and the quotation follows on that line; see fault 1), Second 55 px (row about 888; b41 had 9 px - b41 fault 1 fixed), Third 53 px (row about 1135).
  - 390 (w390-part10 row 1202, w390-part11 rows 206, 558): First 81 px, Second 52 px, Third 50 px.
  - PDF p6/p7 show a wide gap before each quotation. At all three widths the gap is now wide.
- Faces: records in /home/claude/mm/build-35/faces (review2.json "round3" and "final": round 1 words "Blur all three", round 2 "yes" 7 Nov 06:46; sheet-check-final.json pass 06:41:53; pixel-check-after-answer.json/.md pass 06:57, 107 images, faults []). Images 098, 109, 110 opened at full size in b42/images: the boy cutting (098), the girl resting her cheek on her hand (109) and the girl colouring (110) are blurred from brow to chin, soft edges, eye, lashes, nose and mouth not readable; the rest of each image matches b41. The page images match faces/photos-final image99.JPG, image114.JPG, image112.jpg (with Word's crops srcRect l=15697 and l=24948 r=16767; mean difference 0.5-0.7 levels in the blurred areas, against 21-22 levels from b41). In 110.jpg the adult at left shows no face and is not blurred. b41 faults 2 and 3 are fixed (and 109, noted in b41, is blurred too).
- The 7 children's faces left unblurred by her 5 Nov answer (pixel-check-after-answer.json notes: 87-a, 87-b, 92-a, 103-b, 106-a, 113-a, 132-a; images byte-identical to b41) are her choice, not a fault.
- Records: /home/claude/mm/records/DECISIONS-LOG-3-nov.md (to 7 Nov 07:16), /home/claude/mm/build-35/b42.log, /home/claude/mm/build-35/b42/changes.txt, /home/claude/mm/build-35/b40/changes.txt.

## NOT checked (whole review)
- Widths other than 1440, 768, 390 (no screenshots).
- Anything needing a browser: menus, swiping, late-loading images, tab order; the published page (not published); the preview artifact. In particular I could not load the page again at 768 to see whether faults 2-7 are on the page every time or only in this capture.
- Check and gate outputs (not used in place of looking).
- Process rows that rest on the chat (marked in the table).

## Faults

All seven are at 768 only (1440 and 390 are pixel-identical to b41 except the intended changes). Fault 1 comes from change (a). Faults 2-7 are in parts whose code is byte-identical to b41. Fault 2 is above the I Spy lines, and fault 1 adds no line (the paragraph has three lines in both builds), so the em spaces do not explain them: the same code was laid out differently in this capture. That looks like the page's layout being worked out before the images had their size (row D030, "including while images load late"). I could not find the cause without a browser. Each is a fault in what the build 42 screenshots show.

### PDF p6 (The Sound Game, First stage)
1. w768-part07 rows 536-584. PDF p6: "... always / identifying the *beginning* sound: [wide gap] "I Spy with my little eye, something *beginning* with ...."" with ordinary word spaces. Build 41 at 768: line 2 ended "... always identifying the *beginning* sound:" with word gaps of 5-7 px. Build 42: the em space makes "sound:" + gap too wide for line 2, so "sound:" goes down to start line 3. Line 2 ("increased by adding objects: 7, 9, 11, 13, 15 .... 35, always identifying the *beginning*") is justified with word gaps of 13-15 px (line 1 above: 8-9 px), so it shows wide, uneven gaps. Where a line breaks at the margin is not a fault, but the stretched line is new in b42 and the PDF does not have it. No owner rule found that excuses it. (The 6 Nov 23:37 test of the em space, in the decisions log, measured only the gaps, "768: 97/51/49".)

### PDF p3 (the Language area images beside "These are photos of the Language area in my classroom in Taipei ...")
2. w768-part02 rows 838-957. PDF p3 and b41: two images beside the text, about 160 x 120 and 208 x 120. b42: the same two images about 83 x 61 and 54 x 40, small in the middle of an empty area beside the text.

### PDF p14 (Punching: "It's impossible to overstate how popular this activity is ...")
3. w768-part16 rows about 545-665. PDF p14 and b41: the punch-pin image beside the text about 279 x 120. b42: about 71 x 29, a thin strip at the right edge.

### PDF p15 (Writing Stages) and PDF p20-p21 (Functions of Words, Word Study)
4. Layout changed from b41 with the same code:
   - w768-part17 rows about 770-1050: the writing-strip image beside the Writing Stages list sits a few px lower and the paragraph "Writing emerged independently ..." is 8 px closer to the list (gap 34 px; b41 42 px).
   - w768-part22 row about 1363 to w768-part23: Functions of Words, "Verb": b41 kept all three lines in the narrow column beside the grammar-symbols image; b42 has one line beside it and "that implies action and movement from a still centre." in the full-width column. PDF p20 has the Verb line beside the image.
   - w768-part23 row about 1082: Word Study, "Prefixes": b41 kept three lines beside the word-card image; b42 two, then "different colour along the word they precede." full width; the lines below move up 30 px.

### PDF p18 (Object Box 1 ----> The Pink Series)
5. w768-part21 rows about 205-310. PDF p18 and b41: two images beside the text, about 141 x 106 and 80 x 106. b42: about 64 x 48 and 64 x 86.

### PDF p19 (the image "Maria Montessori, 1950, Perugia.")
6. w768-part21 row about 1338 to w768-part22 row about 100. PDF p19 and b41: the image about 163 x 120 beside the text, with its caption "Maria Montessori, 1950, Perugia." in two lines under it. b42: the image is a dot about 20 x 14 at the right edge, and the caption is squeezed into four lines ("Maria / Montessori, / 1950, / Perugia.") that run past the right edge of the screen ("Montessori," is cut off).

### End of the page
7. w768-part26 rows about 713-798: the page ends about 85 px early (b41 footer line at row 767, b42 at row 683) and the screenshot shows an empty beige band about 85 px high under the footer. The screenshot is as tall as b41's (35798 px in all), so the page's height was taken from a different layout from the one drawn.

### Not counted - template items awaiting her (from earlier reviews; those parts unchanged in b42)
- 390: Writing Stages list split by the writing-strip image; Symbol Box tab lists and Phoneme/Grapheme lines lose their columns; gaps where Word's columns join.
- 768: Word Study label lines justified with wide gaps; Article/Verb text in a narrow justified column; swipe dots centred on the text column.

### Build log WARNING lines
- b42.log has the same WARNING lines as b41.log (only folder names differ in the log, apart from the faces lines); b41's review covers them.

## Eye rows (all 143 rows of /home/claude/eng35/b40-eye-rows-full.txt)

Rows marked FAULT rest on faults 1-7; they are not extra faults. "checked" for process rows means verified in the file named.

| Row | Result | What I looked at / why not |
|---|---|---|
| A007 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; 323 of 326 image files byte-identical to b41 (sha256); the 3 changed ones (098, 109, 110) are classroom images, not objects on white |
| A008 | checked | 098, 109, 110 at full size: 2900x2175, 2900x1935, 2486x2900, the same sizes as b41; the page images match the blurred finals with Word's own crops (srcRect l=24948 r=16767 on image112.jpg, l=15697 on image114.JPG, none on image99.JPG), mean difference 0.5-1.4 levels; nothing more cut. Other images byte-identical to b41 |
| A009 | checked | the only crops are Word's own (srcRect above); the rest byte-identical to b41, checked there |
| A015 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (delivery message) |
| A025 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A026 | checked | this report: each claim names the file, screenshot part or measurement; the rest marked NOT checked |
| A029 | checked | b41 to b42: only 098, 098-480, 109, 109-480, 110, 110-480 changed in images/, preview/images and hostinger/ (sha256), the three she answered on; every other image byte-identical |
| A039 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A040 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A055 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (owner's go) |
| A056 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (owner's go) |
| A067 | checked | faces: review2.json round3/final ("Blur all three", "yes" 7 Nov 06:46), sheet-check-final.json pass 06:41:53, pixel-check-after-answer.json pass 06:57, build 07:00; 098, 109, 110 opened at full size: faces blurred (b41 faults 2-3 fixed) |
| A068 | checked | 110.jpg: the adult at left (body only, head out of frame) unblurred; other excluded kinds byte-identical to b41, checked there |
| A069 | checked | review2.json: round 1 words "Blur all three", round 2 words "yes" 7 Nov 06:46; earlier rounds 5 Nov kept (final_r2). The words come from the chat, recorded in that file |
| A071 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; alt="" in b42 index.html; her 28 Oct rule says not needed |
| A073 | FAULT | w1440 and w390 parts looked at where changed and pixel-identical to b41 elsewhere; all 26 w768 parts compared with b41 and the changed places looked at beside PDF p3, p6, p7, p14, p15, p18-p21: faults 1-7 |
| A080 | NOT checked | needs the published page in Chrome (no browser allowed; not published) |
| A082 | checked | 098, 109, 110: content, order, shape, crop, turn the same as b41 (only the blurred face areas differ); the rest byte-identical. Sizes at 768: see faults 2, 3, 5, 6 |
| A084 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A085 | checked | this report gives the file/part/measurement for each claim |
| A086 | checked | this is a separate agent's review of build 42 (I did not make the page) |
| A089 | NOT checked | needs the published page |
| A093 | checked | faces/photos-final image99.JPG, image112.jpg, image114.JPG (06:36) are full-size (pixel-check-after-answer.md: 4608x3456, 5712x3883, 4608x2592, same as originals); the page images are scaled from them (mean difference 0.5-0.7 levels in the blurred areas, 21-22 against b41) |
| A095 | checked | identical to build 41 (sha256), checked there: 116.jpg printed image left |
| A096 | NOT checked | faces: the round 1 and round 2 sheets for the three images (artifacts, blur2/m_eng_r3/round2.html) not opened |
| A099 | checked | 098 (boy cutting), 109 (girl, cheek on hand), 110 (girl colouring) at full size: face covered from brow to chin, soft edges, the same look as the earlier blurs; eye, lashes, nose and mouth not readable |
| A100 | checked | records in order: her "Blur all three" 06:3x, sheet check pass 06:41:53, her "yes" 06:46 (review2.json), finals 06:36-06:46, separate pixel check pass 06:57 (pixel-check-after-answer.json), build 07:00 (b42 files). Decisions log lines 7 Nov 06:3x-07:02 agree |
| A101 | NOT checked | no replacement image recorded for this page in the files given |
| A104 | checked | the three new blurs at full size still read as blurred faces (skin tone kept), not blank patches |
| A105 | NOT checked | faces: round 2 sheet not opened; sheet-check-final.json says it held only 98-b, 109-b, 112-a |
| A106 | checked | 110.jpg: adult at left not blurred (no face in frame); earlier adults byte-identical to b41, checked there |
| A114 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A116 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A221 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A223 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A224 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| A234 | NOT checked | about other pages' structure, not this page |
| B013 | checked | contents box parts (w1440-part01, w768-part01, w390-part01) pixel-identical to b41, checked there |
| B022 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B023 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (a check round ran on this machine during this review, by design) |
| B055 | FAULT | faults 1-7 (768 screenshots differ from the PDF/b41) |
| B061 | FAULT | this separate review at 1440, 768, 390 found faults 1-7 |
| B072 | checked | Word crops (srcRect) on image112.jpg and image114.JPG measured: page images 110.jpg and 109.jpg are those crops of the blurred finals; the rest byte-identical to b41 |
| B085 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| B087 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| B095 | checked | faces: round 3 round 1 was the three images shown whole (review2.json round1_shown); sheet-check-final.json pass 06:41:53 before her "yes" 06:46. When the round 1 page was sent rests on the chat |
| B104 | checked | 098, 109, 110 now blurred (full size looked at); the 7 faces left unblurred are her 5 Nov no-blur answer (pixel-check-after-answer.json notes: 87-a, 87-b, 92-a, 103-b, 106-a, 113-a, 132-a) - her choice, not a fault |
| B107 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| B108 | checked | faces: pixel-check-after-answer.json pass true, 06:57, after her 06:46 answer, 107 images |
| B111 | checked | faces: pixel check after her answer had faults [], so no fix round was needed |
| B113 | checked | faces: the three new finals dated 06:36, before the 06:57 pixel check; page images scaled from them (A093); the other 104 byte-identical to the 5 Nov backup per the pixel check |
| B114 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B120 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; at 768 the title lines in the changed parts not affected |
| B132 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B152 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (a check round ran beside this review, by design) |
| B166 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B180 | NOT checked | about build 1's process |
| B181 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| B205 | NOT checked | about every check on build 1; check outputs not used in this review |
| B206 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (what was sent with the sheet) |
| B207 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given (what was sent with the sheet) |
| B209 | checked | the three new blurred faces at full size unreadable (A099); pixel-check-after-answer.md: fine detail 0.11, 0.11, 0.15 |
| C005 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| C006 | NOT checked | faces: sheet check present (sheet-check-final.json pass), faces data present (review2.json, photos-final.json); what was sent with the sheet rests on the chat |
| C008 | checked | faces: pixel-check-after-answer.json: pass true, 107 images, faults [] |
| C088 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| C110 | FAULT | faults 1-7 are differences from the PDF (or from the checked b41 layout) with no written owner rule |
| C112 | checked | tools/briefs/ENG-REVIEW-BRIEF.md line 12 (file time 6 Nov 23:28) now says sizes, spacing figures, fonts, colours, menu and footer come from the template and what is on the page and where follows the Word file and the PDF, as the standard brief (b41 fault 4 fixed) |
| D004 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D005 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D006 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D011 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D012 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D013 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D019 | checked | all 85 parts (1440: 21, 768: 26, 390: 38) pixel-compared with b41; every changed place looked at full size (faults 1-7 found at 768) |
| D020 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D022 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D030 | FAULT | faults 2-7: at 768 the same code as b41 (index.html differs only by three em spaces further down) shows images drawn small and moved text; cause not found (looks like layout done before the images were sized). Not checked in a browser |
| D041 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D044 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D045 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D056 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D060 | NOT checked | needs the lines check at 8 widths; by eye no beige line through text in the changed parts |
| D062 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D063 | checked | screenshots reviewed (D019); new checks for missed kinds are for the main session |
| D069 | NOT checked | my brief also named the intended changes and gave build 41's review; whether that narrows it is for the owner |
| D070 | NOT checked | READY of the independent check is the main session's record |
| D075 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D077 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D093 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| D094 | NOT checked | needs the check outputs |
| D098 | NOT checked | READY of the independent check is the main session's record |
| D099 | NOT checked | preview artifact not opened |
| D107 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D109 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md (no table in Word or on the page) |
| D114 | NOT checked | browser action: swipe rows not swiped |
| D121 | NOT checked | browser action: menu not opened |
| D123 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; the three I Spy lines have no line round the quotation at any width |
| D126 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D130 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; the em spaces and tabs are mid-line (after "sound:"/"sound."), not before a quotation's first line |
| D134 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D138 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; at 768 see fault 4 (Verb, Prefixes) |
| D140 | checked | turns and Word crops match (B072); the rest identical to build 41, checked there |
| D155 | FAULT | faults 2, 3, 5, 6 (images at 768 drawn at a fraction of their size) |
| D170 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D195 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D197 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D199 | checked | footer quotation in w1440-part21, w390-part38 identical to b41; w768-part26 same three lines, no word alone (but see fault 7) |
| D206 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
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
| D320 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D322 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D325 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D326 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D329 | NOT checked | not measured |
| D330 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D331 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D334 | FAULT | faults 2, 3, 5, 6: at 768 the text beside the shrunk images keeps its narrow column with an empty area where the image was; fault 6 caption squeezed |
| D340 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md |
| D342 | FAULT | faults 2, 3, 5, 6: at 768 the side images are far shorter than the text beside them (b41: about the text block, e.g. 120 high; b42: about 14-60 high) |
| D344 | NOT checked | not measured |
| E007 | checked | this report has the table |
| E009 | checked | records/DECISIONS-LOG-3-nov.md HOURLY LESSONS REVIEW lines 6 Nov 23:2x, 7 Nov 00:3x, 01:3x, 02:3x, 03:3x, 04:3x, 05:3x, 06:40, about an hour apart; the next is due about 07:40 (log read 07:3x) |
| E010 | checked | build 42 changed no template code (index.html differs from b41 only by three em spaces); the 7 Nov 07:16 agreement line names the change (gate_files.py, run_checks.sh) and the pages |
| E011 | NOT checked | gate and check results not given to me |
| E013 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E020 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E021 | checked | faces: review2.json "final" (7 Nov 06:46) and pixel-check-after-answer.json (pass 06:57) both present in build-35/faces |
| E033 | checked | this report says image throughout (the page's own word "photo" is hers) |
| E034 | NOT checked | process or record row: rests on the chat or on how the work was done; not in the files given |
| E035 | checked | 390: only the I Spy lines and images could change; all 38 w390 parts pixel-identical to b41 (gaps 81/52/50 measured), checked there |
| E052 | checked | identical to build 41 at 1440 and 390 (pixel compare), checked there by REVIEW.md (b41), and through it b40/REVIEW-FULL.md; at 768 no beige line near the changed places |

Date at writing: Sat Nov  7 07:36:27 CST 2026

NOT CHECKED: 74
FAULTS: 7
