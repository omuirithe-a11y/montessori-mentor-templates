# Montessori Mentor website - start here

Fresh start: 12-13 Oct 2026. The old rule layers (skills, plugin, hooks, project rules) are retired. This file is the only current record.

## Quick start (30 Oct 2026, 11:54 - the owner's words: "implement all 8")
Do these first, in this order. Everything further down stays in force; this section only changes where the working files come from.
1. Workspace: from GitHub, not the Project. Attach omuirithe-a11y/montessori-mentor-templates (add_repo, push access), clone it, copy its workspace/ folder to /home/claude/mm and its Essay and Resources Code Templates and org-rule.html to /home/claude/mm/templates/. Then, in workspace/, run `sha256sum -c FINGERPRINTS.txt`: every line must say OK, otherwise stop and tell the owner. workspace/PROVENANCE.md says where each file came from. This replaces step 1 of "Set up the workspace first" below (steps 3 and 4 still apply; yunet.onnx is in workspace/faces/). The Project's claude/workspace/ is the older copy: reference only, never copied in again.
2. Read the Project's saved preferences (the memory file preferences.md for this Project) before any work. The 28 Oct note "image descriptions are not necessary anymore" is there; it was missed on 30 Oct.
3. Read claude/DECISIONS-LOG.md: every decision the owner makes, one line each, her words and the time. Add a line the moment she decides something.
4. Current versions: Essay Code Template sha256 3ebaef3a0922e9ea... (commit 13175ad, 30 Oct); check tools: handover-2026-10-29-evening/tools-v5 in the same repository.
5. First-build checks: workspace/tools/run_checks.sh runs the 122 widths, the height and lines through text side by side, then the speed check alone (other checks running at the same time would distort its timings). Every check still runs.
6. Reporting what was checked: one table, every item marked "checked (how)" or "not checked".
7. Questions to the owner: all open ones together, in one message.
8. End of each chat: changed working files go to GitHub workspace/ with new fingerprints (sha256sum -c must pass on a fresh clone); the Project holds the rules and notes.

## At the start of each chat
Read this file, then read the newest HANDOVER file in the Project files (added 18 Oct 2026). Then read claude/MASTER-DECISIONS.md (added 20 Oct 2026).
**Set up the workspace first, every chat, no exceptions** (27 Oct 2026, 10:20, the owner's "yes"). It is the first work done in every chat, before anything else, whatever the first message asks: before building, checking, fixing, measuring, searching, packaging, answering a question about a page, or launching any agent. Nothing counts as too small or too urgent to skip it. The steps (claude/workspace/README.md), all of them, in this order: 1. copy every file under claude/workspace/ in the Project into /home/claude/mm; 2. attach the GitHub repository omuirithe-a11y/montessori-mentor-templates, clone it, and copy the Essay and Resources Code Templates and org-rule.html into /home/claude/mm/templates/; 3. install the libraries; 4. fetch the faces models. When it is done, tell the owner in one line which steps succeeded. If any step fails or is refused, stop and tell the owner before doing anything else. Never decide that a step does not apply; if one seems not to, say so and wait.
Pages are built with tools/build_page.py, never typed by hand (added 20 Oct 2026).

## What this is
The Montessori Mentor website, montessorimentor.co.uk, built from your Word essays and hosted on Hostinger.

## Where things are
- Word files, PDFs and original photos: Google Drive, one folder per document.
- Live pages: on Hostinger. The full list will be confirmed when needed.
- Archive: the old repository montessori-mentor-hooks is retired and you are deleting it yourself. Its cleaned history (no photos) is in the private repository omuirithe-a11y/montessori-mentor-records, read-only reference only. Never clone it as the project folder and never switch any hooks on. To read it: add_repo (read access), clone with --depth 1 to /home/claude/ref/records, and do NOT call register_repo_root (that would load its old settings). Its hooks file is switched off (.claude/settings.json.DISABLED-hooks-off); leave it so. (added 20 Oct 2026)
- The workspace (added 20 Oct 2026): claude/workspace/ in the Project files - the Word-to-page converter (from the records repository), the build script, the faces script and the check script, with README.md. Everything else a page needs comes from Drive (Word file), the live site (section hero) and GitHub (the templates).
- The faces pack (added 21 Oct 2026): Google Drive folder "faces-tools" (https://drive.google.com/drive/folders/1qSEdp1Au7UibjfbJ9BULcw9-WoHavgOl) - only its face-finder model yunet.onnx is still used (workspace README step 4). Its blur_faces.py (v7 whole-face blur), README.md, find_faces.py, detect_lm.py and pass2.py are RETIRED since 25 Oct 2026: tools/faces.py does all of it., run_faces.py, review_sheet.py, round2_sheet.py and the face model yunet.onnx. The workspace's tools/faces.py does the same steps (rewritten 21 Oct 2026; see Faces below).
- The Essay Code Template (from the live The Role of the Adult page) has ONE master copy (21 Oct 2026, 10:04, your words: "delete all copies of the essay code template except the one in github ... one master copy is best"): "Essay Code Template.html" in the private GitHub repository omuirithe-a11y/montessori-mentor-templates (add_repo with push access). The Project-file copies and the Word sheet "Essay page template 18 October.docx" in Drive (moved to the Drive bin) were deleted that day. Never save a copy of it anywhere else; edit it only in the repository and push.
- The Resources Code Template (added 20 Oct 2026, from the live Culture Resources page) and org-rule.html (the beige lines between organisations, used by the build script) have ONE master copy each, in the same GitHub repository (21 Oct 2026, 16:1x, your words: "only save edits to the templates in github", "delete all other templates"; org-rule: "Move it to GitHub"). The Project-file copies (claude/Resources Code Template.html, claude/workspace/templates/Resources Code Template.html, claude/workspace/templates/org-rule.html) were deleted that day. Never save a copy anywhere else; edit only in the repository and push. Copy protection kept apart in claude/copy-protection.html and added only for the Hostinger build. Preview: https://claude.ai/artifact/CprtkdiwSyWMpHf4YJY4ME (resources, an older copy). The essay preview https://claude.ai/artifact/EzsNwEikT9beqau56MNKHu is an older copy of the Essay template.
- The six Essential Elements hero pictures (2.0 to 2.5), web copies, originals and the settings decided 18 Oct 2026: published page https://claude.ai/artifact/BnnZQ8r4hibfzj53cfLkCs (fetch a picture with the Artifact tool's read action and the path shown on the page, e.g. originals/role-of-the-adult-hero-original.jpg); also the zip montessori-mentor-essential-elements-heroes.zip (sent to the user 18 Oct 23:20). In Google Drive folder "2. Essential Elements" (id 14cTW-ZUqRQWwVZ7OvnUDtPvfRSvCWGBu) there are 300px-wide reference copies only, named 2.0-essential-elements-300px.jpg to 2.5-montessori-materials-300px.jpg (uploaded 18 Oct; file ids in claude/HANDOVER-18-oct-night.md) - good for finding the right photo, not for the site. Full size is not in Drive and not in the Project files (images cannot be stored there). (added 18 Oct 2026, Drive line 19 Oct)
- The master (one source for every page) and its content-type decisions: claude/MASTER-DECISIONS.md; the one preview page for its questions: https://claude.ai/artifact/CFTL6tKj5PtRicfHVwKkYR (added 20 Oct 2026).

Resources pages have their own template.

## Numbers
RETIRED 20 Oct 2026, 15:17 (your words: "Yes, retire both" - this section and SETTLED item 1). The Word sheet "Essay page template - the sheet new 16 Oct 2026 23-12 Beijing.docx" is no longer the source of numbers.
Now: pages start from the Essay Code Template and the Resources Code Template (both in GitHub, see above), made from the live The Role of the Adult and Culture Resources pages. Each content type's figures are measured against The Role of the Adult (your choice, 15:17) and recorded in claude/MASTER-DECISIONS.md. Both templates live only in the private GitHub repository montessori-mentor-templates (Essay 21 Oct 2026 10:04, Resources 21 Oct 2026 16:1x), brought up to date there at the end of each chat. Page text still comes from your Word documents (rule 7). No numbers are copied into this file.
Phones (21 Oct 2026, 10:01, your words): "no questions about phones. whatever edits we made or choices we make on this and all pages, transfer them across to phones but using numbers that work on phones and are consistent with how other pages on this site worked".
Text alignment (23 Oct 2026): justified on computers (641px and wider), left-aligned on phones (640px and narrower) - your 13 Oct decision, confirmed 16 Oct; agreed for both templates 23 Oct 09:47 ("I agree to these changes to the Essay Template and the Resources Template"): the block <style id="mm-phone-left"> before </head>, GitHub commit 61a14e3. Any new rule that justifies text must also be added to that block. This replaces the 18 Oct "justify the text on this and all pages" at phone widths, and the 22 Oct "numbered lists justified" and 21 Oct 5.4 "Label on its own line" apply at 641px and wider.

## Rules
1. Nothing goes live or gets uploaded without your "go".
2. Your originals (Word files, PDFs, photos) are never edited; I work on copies.
3. One page at a time.
4. I build what you asked, send a preview, and stop.
5. If an instruction is unclear, I ask one short question that names what is missing and gives options. (20 Oct 14:51, your words: "stop asking questions" - I decide from the evidence instead, say what I decided and on what evidence, and list what is still yours to settle without asking.) (23 Oct 2026, 09:47, your words: "do not ask questions until I write the words 'ask your questions now'" - until then I decide from the evidence.)
6. I don't re-ask anything you have already settled.
7. Page text comes from your Word documents word for word; I never write wording for your pages. Typos (27 Oct 2026, 10:05, your words: "correct all typos on every page. do not ask about this again"): every typo is corrected, without asking, and listed in the report. This replaces the 23 Oct rule (every typo reported to you to decide, never corrected).
8. I only say something is checked or done if I tell you what I looked at.
9. Everything is in plain English. I never ask you to run commands, and links go on their own line.
10. Uploads replace, they never merge (your words, 27 Oct 2026, 06:51 - "I know this. I've known it for months"). A folder
    uploaded to Hostinger REPLACES the folder there; any file left out of the zip is DELETED from the server. So every page
    folder I send is COMPLETE - index.html and every image the page uses, hero.jpg included. On 26 Oct hero.jpg was left out
    of nine folders on an assumption that uploads merge, and the hero was deleted from all nine pages.
10a. Where a thing cannot be established by measuring or reading, I say I do not know, or I ask. I never fill the gap with an
    assumption and report it as fact. (27 Oct 2026, 06:51, your words: "you prefer assuming even though your assumptions are
    always wrong".) Before quoting any record, I read the WHOLE file - on 27 Oct the 24 Oct image-size line was quoted as
    current when the same file corrected it four paragraphs later.
11. If something is blocked or refused, I stop and tell you; I don't find another way.
12. If you ask a question, I answer it and change nothing.
13. Copy protection is added to every page just before it is published (added 15 Oct 2026). Do not ask again.
14. The clock: OFF (23 Oct 2026; your words "stop the clock", 22 Oct 23:05, and "switch off the clock", 23 Oct 08:06): no clock times at the top of answers and no timed searches. The rule as it was: The clock (20 Oct 2026, 12:07, your words: "start the clock again. 3 minutes each answer"; replaces the morning's "stop using the clock"; 13:38: "Run every answer under the 3-minute clock, with the places searched not listed, and the places you haven't searched listed"; 14:51: the stronger timer). Every answer runs under gate2.sh (workspace scratchpad; rebuild it from the description if missing): start it with the kind of question (design, status, rule), which loads that kind's source list - your messages in this chat and the parallel chat always first. Shell searches run through it, so the log line (time, source, command, size of result) is written by the command, not typed; other tools are logged at the moment of the call. It opens only when: 180 seconds have passed; a search was logged in each of minutes 1, 2 and 3; the last search is no more than 60 seconds old; every listed source was searched or skipped with a reason. At the top of the answer: the start and end times, and the places NOT searched (most likely first). (Exception: in a chat where you say "stop the clock in this chat", it stays off in that chat.)
15. Options (20 Oct 2026; corrected 17:30 from your 16:24-16:26 answers): 5 options per question (per kind where a type covers two kinds of element) - the most-used live style; The Role of the Adult's (the model) most-used style, or the third most-used where it has none or it equals the first; the next most-used; none (or "not possible"); your own figures. An option is a whole style (all figures together as they occur live, counted). Every other style and value is listed as text with its count, values used once included. Drawn at 1440 on a named live page; phones are the mean of the live pages. One question at a time. (Replaces: "every option - Sensorial's figures ... every mix one figure at a time".)
16. Working (20 Oct 2026): before any step that takes more than a minute, send one line saying what it is. Say only what was looked at; never call a check unnecessary, a list complete, or a promise kept without having checked it.
17. Preview links (20 Oct 2026): every message that names a page - progress lines, "held" or "not updated yet" states, questions - ends with that page's preview URL on its own line, unasked. Never "open in the app" alone; never "shall I publish?" in place of a link.
18. Checking (20 Oct 2026, 14:51): every figure and fact in an answer carries its source, or is marked "not checked". A separate agent, which has not seen the work, checks each draft before it is sent, and its findings are shown to you. Extended web search is used for facts that are hard to find.

## Faces (26 Oct 2026, 13:49 - the agreed blur method version 22 replaces the rejected v8; the owner's words 13:47: "I agree to BLUR-METHOD-26-oct.md version 22 (attached)", and 13:48: "update all immediately, replacing v8 with the attached file")
Every page's images with children go through these steps BEFORE the page is built.

**The process** (the owner's Project instructions - they come first wherever the method says otherwise): round 1 sheet, her answer, blur, round 2 sheet, her answer, a separate agent's pixel check, then build. So images not yet answered always get both rounds; method item 17's single sheet applies only when the method changes and the faces were already answered.

**The method**: claude/BLUR-METHOD-26-oct.md version 22, SHA-256 1dc672e9f65e077e5e290ecf57cc30154848ce52501e8faba7c501a4405cb684, agreed 26 Oct 13:47 (record: claude/BLUR-METHOD-AGREEMENT-26-oct.md - its header line "FOR AGREEMENT, not yet agreed" is superseded by that record; the file is not edited, so its fingerprint stays as agreed). Its text is in that file, not copied here (see "The method itself" at the end of this section).

**The tools**: claude/workspace/tools/blur/ in the Project (method.py detect | blur | sheet, method_sheet.py incl. release, method_check.py, changed.py, grid.py, sets/<set>.json for every answer, hand fix and cut). tools/faces.py is used only for detect, pass2, pageorder, save and restore; its v8 commands (sheet, blurfull, after, release, blur) refuse. Never the Drive "faces-tools" pack or blur_faces.py (yunet.onnx excepted); never InsightFace.

**What enforces it in code**: method_sheet.py release refuses without a separate agent's pass newer than the sheet; build_page.py builds from faces/photos-final only when review2.json holds her last answer word for word ("final": sheet, words, check), and makes no upload zip without faces/sheet-check-final.json (the agent's passed check of the sheet she last answered) and faces/pixel-check-after-answer.json (a separate agent's pixel check made after her answer). Not enforced by code: that the words are hers, and the Project save of the faces data after each round (method item 25).

**Out of date in version 22, held for a later version** (each needs her agreement): item 1's yunet.onnx licence line (read 26 Oct 01:5x, in the HANDOVER); item 27's build lock (now the stricter locks above); item 3 assumes images from a Word file (bigger images she uploads are numbered by their place on the page).

**The method itself** is in claude/BLUR-METHOD-26-oct.md, version 22, unchanged (SHA-256 above). Until 30 Oct 2026 its full text was also copied into this section, word for word; on 30 Oct (the owner's "implement all 8", 11:54, item 3: a short START-HERE) the copy was replaced by this pointer. The file is the method; read it in full before any faces work.

## Before a page is finished (added 16 Oct 2026)
1. Open the live page as uploaded and check it at phone, tablet and computer widths.
2. Swiping: pose as a phone and swipe each photo row to check it moves and the dots follow (simulated touch).
3. The menu on phones and tablets: open and close every panel.
4. Spacing between 641 and 830 px.
5. Text alignment at every width.
6. The hero picture, table of contents and footer at tablet widths.
7. The page's code: errors the browser reports, the keyboard skip link and tab order. (Photo descriptions removed 30 Oct 2026: image descriptions "are not necessary anymore", the owner, 28 Oct; no image has a description.)
8. The other live pages: the 3 px menu fault and text alignment on each.
tools/check_page.py runs checks 1, 3, 5, 6 (footer and hero) and 7 (errors) at 1280, 768 and 390 on a preview or a live address (added 20 Oct 2026); the rest are still done by hand.

## Queued edits: how they are done (added 22 Oct 2026, 12:51, your words: "save all of those to the project and start here")
1. Prepare while you queue. Each queued edit is written into the page's settings at once, with any new build-tool code and its measurement, without building or publishing. Your "go" then starts one build, one measurement and screenshot pass, and one publish. (This is your OK for preparing early under the queue rule.)
2. Settings CSS before new code. Where one line of CSS in the page's settings does the edit, that is used, tested in the browser before the build.
3. One script for everything after the build: it measures every edit at 1280 and takes the 1280 and 390 screenshots in one run.
4. No re-reading the Project's copies while only one chat works on a page; save once, after the publish.
5. No questions about anything already settled: check the page's settings, claude/workspace/QUEUE.md and the preferences first.
The gate (22 Oct 2026, 12:3x): the mm-gate plugin is off your account and pages publish without tools/gate.py; you check the page yourself. mm-gate-0.2.0 (the gate without its publish block) was made but not installed.

## Order of work (added 24 Oct 2026, 11:59 - your words, unchanged)
Me: Images-to-replace list – locate and upload all replacement files

You – the following may be done in parallel, where possible, but 2.2.0 is most important and must be started immediately
1.	Build 2.2.0 The Prepared Environment from the updated Essay Code Template 
2.	The Mathematics Curriculum: the label fix, plus the unsolved images over the Exercise lines and text over text.
3.	Few-pixel touches: Mathematics Resources image 3 at tablet widths (641 to 768 pixels), and The Role of the Adult Resources at 641.
4.	Leftovers after resizing on about 18 pages.
5.	PDF badges alone on their own line on 6 resources pages. Fix them.
6.	Re-measure the width Hostinger serves images at. 

After I’ve uploaded the hi-res images:
7.	Prepare faces sheets for each page
8.	Send them to me one-by-one, for checks 1 and 2
9.	Download zips with the newest package after all changes on this list have been made, so I can add to Hostinger
10.	After I upload: you re-check the live pages.

11.	Template change: the narrow-column limit goes from 200 to 260 pixels. Before this is agreed to, explain exactly what it fixes and what other consequences the change might have, positive and negative

Also standing from 24 Oct 2026 (your words): say "image", never "photo" (10:55); "when you find files that are of sufficient quality, add them automatically. do not wait for permission. have an agent check your answer" (11:35) - images with children still go through the faces sheets and your answer first.
Also standing from 24 Oct 2026, 15:54 (your words): "If there's a fault error mistake typo etc correct it immediately".

## Replaced: image descriptions (30 Oct 2026)
The owner, 28 Oct: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere. No image on any page has a description, and live pages lose theirs when rebuilt. These older files still say otherwise and are replaced on this point (they are records and were not rewritten): claude/FAULT-LIST-27-oct.md item 17; claude/DECISIONS-27-oct.md item 5; claude/AGENT-INSTRUCTION-rev12.md to rev15.md step 6; claude/LESSONS-LEARNED-27-29-oct.md lesson 14 and its summary item 13 ("have a second agent compare every description with its image"); the 21 Oct rule quoted in tools/rules.json, extra_checks.py and page settings (changed in the GitHub workspace on 30 Oct).
