# Handover, 4 Nov 2026 (written about 11:0x Asia/Shanghai)

## State of the five Resources pages
All five passed tools/v8 send gate (GATE PASSED) and the upload zips were sent to the owner. At 10:52 she wrote: "Ok. I'll upload them later." Upload rule: put each zip's index.html into the page's existing folder, replacing only index.html.

| Page | Build | Upload zip (fingerprint) | Preview |
|---|---|---|---|
| 8.0 Resources | build-res/resources/t11 | send/resources-UPLOAD.zip (84fb260e) | claude.ai/artifact/QJnYsWR7ox6FqVMYFdRVBi |
| 8.1 Books by Montessori | build-res/books-by-montessori/t14 | send/books-by-montessori-UPLOAD.zip (ce0c109e) | claude.ai/artifact/4Qaw3VAqVKCTt1sQNErk3r |
| 8.2 Books of Interest | build-82/b30 | send/books-of-interest-UPLOAD.zip (69894e01) | claude.ai/artifact/2YrAVRoViYXowe7EDuWFfv |
| 8.3 Picture Books | build-res/picture-books/t13 | send/picture-books-UPLOAD.zip (6bc9e638) | claude.ai/artifact/QFw6s4QrJboZtzcUDCMNNu |
| 8.4 Websites | build-res/websites/t10 | send/websites-UPLOAD.zip (33a1b368) | claude.ai/artifact/2nHfsR2g344BPcRvfykZPP |

Each build folder holds CHANGES.txt (the change list she confirmed), REVIEW.md (separate review), checks/, gate.txt, and EDIT-QUEUE.md one level up (her words).

## Next
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
