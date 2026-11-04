# Handover, 4 Nov 2026 (written about 11:0x Asia/Shanghai)

## State of the five Resources pages
Updated 13:1x: at 11:42 she said yes to re-sending 8.1, 8.2 and 8.3 with section headings 60 (template f14174ee). All three passed the gate (12:29, 12:59, 13:02) and all five zips were re-sent together (her 12:32 "send the five zips anyway"). The table below lists the only five zips to upload; the earlier 8.1/8.2/8.3 zips are superseded.
All five passed tools/v8 send gate (GATE PASSED) and the upload zips were sent to the owner. At 10:52 she wrote: "Ok. I'll upload them later." Upload rule: put each zip's index.html into the page's existing folder, replacing only index.html.

| Page | Build | Upload zip (fingerprint) | Preview |
|---|---|---|---|
| 8.0 Resources | build-res/resources/t11 | send/resources-UPLOAD.zip (84fb260e) | claude.ai/artifact/QJnYsWR7ox6FqVMYFdRVBi |
| 8.1 Books by Montessori | build-res/books-by-montessori/t16 | send/books-by-montessori-UPLOAD.zip (b5bebc3f) | claude.ai/artifact/GNBaJgb5YWRqoXnRzPKn9d |
| 8.2 Books of Interest | build-82/b31 | send/books-of-interest-UPLOAD.zip (2d374994) | claude.ai/artifact/B2YkhEKnZi2BbhQSm48wTw |
| 8.3 Picture Books | build-res/picture-books/t14 | send/picture-books-UPLOAD.zip (02c701dd) | claude.ai/artifact/4TWT4V2ysNf4yVbhz3A18Z |
| 8.4 Websites | build-res/websites/t10 | send/websites-UPLOAD.zip (33a1b368) | claude.ai/artifact/2nHfsR2g344BPcRvfykZPP |

Each build folder holds CHANGES.txt (the change list she confirmed), REVIEW.md (separate review), checks/, gate.txt, and EDIT-QUEUE.md one level up (her words).

## What remains for Claude (list given to the owner 14:5x; her 15:03: "Add your 'remains for me' list to the handover")
1. Save this afternoon's work to GitHub: the Picture Books setting for "ancestor" (pages/picture-books.py), the 13:47 decision (DECISIONS-LOG-3-nov.md), this handover and the menu check tools (scratchpad/menu/n1321: mcheck.js, hcheck3.js, ONLY-MENU-DIFFERS.txt, MENU-CHECK-FINAL.txt).
2. Check the live pages once the two zips are uploaded: Picture Books (t15, 004eebd8) and the menu on all 37 pages (montessori-mentor-menu-37-pages-UPLOAD.zip, b9a3e830). At 14:56 neither was live.
3. Bring the template menus into line with the live site - a template change, needs her words first. The Resources Code Template shows 9 menu entries as plain text that are links on every live page: Essential Elements Resources, The Role of The Adult, The Role of The Adult Resources, The Role of the Assistant, Staff, School Handbook, Classroom Management, Beginning of the year for Teachers, Observations for Teachers. The Essay Code Template shows the same entries as plain text except The Role of The Adult.
4. Correct a typo on The History of Education: its timeline has "Friedrich Froëbel"; her rule (23 Oct) is "Fröbel". Needs a rebuild of that page with every check. (No other live page has Froëbel in its body text; "Froebel" on 6 pages, several in published titles, not covered by the rule - not changed.)
5. Hourly lessons review: next at 15:22 (send_later, this chat only).

## Next
00. 14:2x: sent picture-books-UPLOAD.zip t15 (004eebd8; her 13:25 "ancestor", "children's" deleted; GATE PASSED) and montessori-mentor-menu-37-pages-UPLOAD.zip (b9a3e830; scratchpad/menu/n1321; 37 pages = live copies with the 5 Resources pages' menu; outside the menu byte-identical; menu links right; 7 height flags = live loading variance, hcheck3). After upload: check the 37 live pages and Picture Books. 13:47 decision in DECISIONS-LOG-3-nov.md. Open: template menus have 9 plain-text entries that are links live (ask her).
0. 13:2x check: all five live Resources pages are byte-identical to the five zips in the table (she has uploaded them). The other 37 live pages still have the OLD Resources menu (3 Nov 42-page menu zip never uploaded; that zip also has "Froëbel" on 27 pages, so do not use it). Template menus have 9 entries as plain text that are links live (Essential Elements Resources, The Role of The Adult, The Role of The Adult Resources, The Role of the Assistant, Staff, School Handbook, Classroom Management, Beginning of the year for Teachers, Observations for Teachers); Essay and Resources templates disagree on The Role of The Adult. Template change needs her words.
1. After she uploads: check each live page against its upload zip (index.html byte-identical, images unchanged, menu layout B).
2. Template rules (owner 11:15 and 11:16, "Yes change the template now and in GitHub"): all five of her 4 Nov spacing edits are now Resources template rules - years 52 / books in a year 40; red name lines 50; section headings 60; headings that link to a page 50. Template f14174ee (GitHub 6e01790, fingerprints 869c6a9). The matching page settings were removed.
3. Rebuilt on f14174ee, not yet full-checked or sent: 8.0 t12, 8.1 t16, 8.2 b31, 8.3 t14, 8.4 t11. Against the zips sent today, at 1440: 8.0 and 8.4 identical; 8.1, 8.2, 8.3 differ only in green section headings, now 60 (8.1 Bibliography; 8.2 Books on Teaching, Book Lists; 8.3 Hornbooks). Code check ALL CHECKS OK on all five. The zips she has (old template) are still valid; if she wants the section headings at 60 on those three pages, they need the full checks, review and gate, then new zips.
4. Hourly lessons review reminders are set by send_later in this chat only; a new chat sets its own.

## Changed tools
- tools/spacecheck.py (08:42): gaps named in SPACE_AGREED are left out of the sameness test (old copy: tools/spacecheck.py.before-0840). Tested both ways on 8.2 b30.
- build-82/space-agreed.txt: 68 -> 69 (her 07:54 "make it 50").

## Records
- Decisions: records/DECISIONS-LOG-3-nov.md (4 Nov entries at the end) -> Project claude/DECISIONS-LOG-3-nov.md.
- Lessons 66-72: Project claude/LESSONS-LEARNED-27-29-oct.md.
- Message checker brief: tools/briefs/MESSAGE-CHECK.md.
- GitHub: page settings, spacecheck, queues, change lists and these records are in commit 15e8d53 (workspace/).
- Previews of the f14174ee rebuilds (section headings 60): 8.1 t16 claude.ai/artifact/GNBaJgb5YWRqoXnRzPKn9d; 8.2 b31 claude.ai/artifact/B2YkhEKnZi2BbhQSm48wTw; 8.3 t14 claude.ai/artifact/4TWT4V2ysNf4yVbhz3A18Z. Open question to her (11:3x): check and re-send these three now, or upload the zips she has and leave it for the next rebuild.
