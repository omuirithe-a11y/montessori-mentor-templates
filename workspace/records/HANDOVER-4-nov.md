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
2. Open questions to her, one at a time: should these 4 Nov page edits become Resources template rules - 50 above red name lines (Picture Books 07:46, Websites 07:48), 60 above section headings (Websites 07:51), 50 above the headings on Resources (07:33)? Until she answers, they live only in the page settings (pages/*.py).
3. Template: Resources Code Template ea36d904 (GitHub 0c56930), 4 Nov 11:15 - years 52 / books in a year 40 (owner "Yes"). The zips sent today were built on c6e5bee0 (8.1 t14 had the same gaps as a page setting); each page takes ea36d904 at its next rebuild.
4. Hourly lessons review reminders are set by send_later in this chat only; a new chat sets its own.

## Changed tools
- tools/spacecheck.py (08:42): gaps named in SPACE_AGREED are left out of the sameness test (old copy: tools/spacecheck.py.before-0840). Tested both ways on 8.2 b30.
- build-82/space-agreed.txt: 68 -> 69 (her 07:54 "make it 50").

## Records
- Decisions: records/DECISIONS-LOG-3-nov.md (4 Nov entries at the end) -> Project claude/DECISIONS-LOG-3-nov.md.
- Lessons 66-72: Project claude/LESSONS-LEARNED-27-29-oct.md.
- Message checker brief: tools/briefs/MESSAGE-CHECK.md.
- GitHub: page settings, spacecheck, queues, change lists and these records are in commit 15e8d53 (workspace/).
