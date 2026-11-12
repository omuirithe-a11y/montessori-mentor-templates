# Montessori Mentor website - start here

The only instructions file. Updated 9 Nov 2026 (sections 2, 6 and 7 updated 12 Nov evening). It replaces every earlier START-HERE, HANDOVER, DECISIONS-LOG, BUILD-ORDER, check list, lessons file and agent instruction (owner, 9 Nov: "Remove old outdated unhelpful commands orders etc from start-here. I want each new chat to open with this plan, this way of building a page"). Those files have been removed from the Project; copies are kept on GitHub (workspace/records/) for history only. Never follow them.

The website is montessorimentor.co.uk. The pages are built from the owner's Word essays and hosted on Hostinger.

## 1. Start of each chat
1. Set up the workspace. Attach the GitHub repository omuirithe-a11y/montessori-mentor-templates (add_repo, push access) and clone it to /home/claude/montessori-mentor-templates. Then run `bash /home/claude/montessori-mentor-templates/workspace/tools/setup_workspace.sh`. It ends with SET-UP SUCCEEDED or SET-UP FAILED. If it fails, tell the owner before doing anything else.
2. Read this file. The Project's saved preferences load on their own.
3. First reply: one line saying whether set-up succeeded, then the answer to her message. Don't send a list of files read, and don't send a report.

## 2. How a page is built
The owner, 8-9 Nov 2026: "this process is much quicker than 46 builds"; "The most important thing to do now is to preserve this way of building pages". First used for The Prepared Environment: it was finished in one evening of edits on a live preview, after 8 builds by the old way.

1. **Faces first**, for any image with children (section 4).
2. **Build once** from the Word file and the Essay or Resources Code Template: `python3 tools/build_page.py` (each page's command goes in workspace/pages/<page>.build.sh). Put the one spacing rule (workspace/pages/pe-final/mm-one-spacing.js) in the page. Take the copy protection out (handover-2026-10-29-evening/tools-v5-fixA/strip_protect.py) and publish the page as a preview artifact. That preview is the working copy. Don't build again for edits.
3. **She edits on the live preview.**
   - Queue each edit as she sends it (one line back: what is queued, for which page). Make them all together when she says (12 Nov: "no. i don't want to wait a few minutes between edits"; "make those changes now", "finished. go"). If she says an edit is also for the template, queue it for the template too; otherwise it is for the page only (12 Nov: "when I want them to be included as changes to the essay template I'll say so").
   - Every question about something visible comes with the preview open.
   - Answers are bare numbers: "The space between those two paragraphs is 29". One number only (12 Nov: "stop with thr two cunitn mesaurements"). A gap between lines of text is from the bottom of the letters to the top of the next line's capitals (lines 36 apart in 18 px text is a gap of 24). Don't explain measuring methods, and don't quote phone figures.
   - Write her words for each edit in workspace/records/<page>-EDITS.md.
4. **The one spacing rule** (mm-one-spacing.js) sets all vertical spacing:
   - 30 between blocks, measured from the bottom of the text (its baseline) or image above to the top of the capitals or image below;
   - 40 above and below quotations;
   - 40 from the hero to "Table of contents";
   - 40 from the last line to the blue footer;
   - a red heading's line 16 below its letters;
   - side images level with the top of the capitals of the first line beside them.

   (12 Nov figures in mm-one-spacing.js: red headings 50 above; 18 after a blue heading before text; quotations 40/40. See section 7.)

   The template's spacing scripts may not change those blocks: they rewrite margins about 29,000 times in the 9 seconds after the page opens, which is why the old spacing was never consistent. Never add spacing fixes to those scripts.
5. **"Finished" means the preview is the page.** There is no new build. Run `python3 workspace/pages/pe-final/make_final.py <last build zip> <approved preview index.html> <out zip>`. It puts copy protection back, keeps the full-size images, leaves out deleted images, and proves that the page equals the approved preview. If the last build zip is gone (new session) and the page is already live, make a base zip from the live page folder: its index.html and every image it uses, downloaded from montessorimentor.co.uk (these are the blurred copies; done for The Prepared Environment, 12 Nov). The Word file comes from Drive with `python3 tools/fetch_drive.py <file id> <out>` (any size).
6. **The checks, once, one at a time, with nothing else running.** The machine has two processors, and a second browser job made the speed check fail on 9 Nov. Put the results next to the zip.
   - Code check (tools/v8/strip_compare_nolive.py). Add the preview's new lines to tools/allowed/<page>-code.txt, with her words.
   - Format check against the Word file (tools/v8/format_check_word.py). Her edits should be the only new differences.
   - 122 widths (vfast.py), height (stable.py at 1440 and 390), placement (tools/v8/place_check.py) and speed (speed_check.py). The first three are in handover-2026-10-29-evening/tools-v5-fixA-200, speed_check.py in tools-v5-fixA.
   - The spacing check at all 122 widths (pages/pe-final/onecheck.js; for her 12 Nov figures, images 40/40 and 20 under Before/After, pages/pe-final/onecheck-pe12.js).
   - Lines through text (tools/lines_v2.py, 8 widths).
   - Screenshots of the final page compared with the approved preview at 1440, 1024, 768, 641 and 390 (a fixed pixel comparison; an agent judges only the differences, if agents are on).

   Fix any fault in the page, then run the checks again.
7. **Gate:** tools/v8/send_gate_pe12.sh (send_gate_pe.sh plus her 12 Nov "photos 40/40" in the placement check) must print GATE PASSED. Then send the UPLOAD zip with one line of context.

## 3. Menu changes on every page
This is a separate job with no page build:
1. Download every live page's index.html (the links in the home page's menu).
2. Replace only the panel that changed. Byte-compare each page with live outside that panel: 0 differences.
3. Check the panel on every page at 1440 and 390 (tools/menu-9-nov/mcheck.js; open the panel with a script click).
4. Zip index.html only, one folder per page, with the home page at the root.
5. Make the same change in both Code Templates on GitHub, and re-pin tools/v8/strip_compare_nolive.py to the new template sha256.

## 3b. Template work
Before changing either Code Template, read these, and nothing else:
1. This file: section 2, and the "Next job" list in section 7.
2. The Project's saved preferences, "Site style" part. It holds her figures: fonts, spacing, dividers, image heights, lists, menu, footer.
3. The template itself, in GitHub at the top of montessori-mentor-templates (Essay Code Template.html or Resources Code Template.html).
4. The approved look: workspace/pages/pe-final/approved-preview-index.html (The Prepared Environment, approved by her 8 Nov), workspace/pages/ec-final/approved-preview-index.html (The English Curriculum, approved 12 Nov), and workspace/pages/pe-final/mm-one-spacing.js (the spacing rule).

How:
1. Show the change on a live preview of a real page. Use The Prepared Environment's approved page unless the change is about something that page doesn't have.
2. She agrees in writing to one sentence stating the change itself: what changes, at which widths, on which pages. Never edit a template before that.
3. Change the template only on GitHub, one change at a time.
4. Check the test page before and after at every width (onecheck.js plus a position comparison): only the agreed change may differ.
5. Re-pin tools/v8/strip_compare_nolive.py to the new template sha256 and push, and update section 7.
6. Live pages change only when they are rebuilt.

## 4. Faces (images with children)
- Use the blur-faces skill.
- The method is claude/BLUR-METHOD-26-oct.md, version 22, agreed by her on 26 Oct. Read it in full before any faces work.
- The order: round 1 sheet, her answer, blur, round 2 sheet, her answer, a separate agent's pixel check.
- The preview can start from the round 1 blurred images while the rounds go on. The upload zip comes only after the last round.
- When a new Word file arrives, compare its images with the old one by sha256, because Word renames images (8 Nov).

## 5. Standing rules (the owner's own words; nothing else is a rule)
1. Nothing is uploaded without her "go". She uploads to Hostinger herself.
2. Her originals (Word files, PDFs, images) are never edited; work on copies.
3. Page text comes from her Word documents word for word. Typos are corrected without asking and listed ("correct all typos on every page. do not ask about this again").
4. Uploads replace, they never merge: a page folder sent is complete. For a change to a live page only, send index.html only.
5. Copy protection is added to every page just before it is published.
6. Say "image", never "photo".
7. Plain English. She never runs commands. When you send her somewhere, give the full link on its own line first, then the steps.
8. Questions: decide wherever the evidence settles it. Otherwise ask one simple question, with the live preview open.
9. Answers are short. Give bare numbers, no phone figures and no measuring methods. An independent agent checks and corrects every answer before it is sent (8 Nov; 9 Nov: "Agents look at and correct all answers"). The agent is given the exact final text. What it passes or corrects is sent word for word. If any word is changed after the check, the changed text goes back to an agent before it is sent. (11 Nov she said "stop all agents now". 12 Nov: "start the agents again", then "stop the agents"; at the end of 12 Nov agents are OFF. She sometimes asks for one answer to be agent-checked ("have an agent check that answer"); do that one. Ask her before turning checks back on for every reply.)
10. If a fault, mistake or typo is found, correct it at once.
11. One page per chat.
12. Don't refer to The English Curriculum build or its decisions (8 Nov: "Whatever was done with that build was wrong"). This means the old builds before 8 Nov; the page finished on 12 Nov by section 2 is a valid reference.
13. "save this" means a download link, never GitHub.

## 6. Where things are
- **Word files and PDFs:** Google Drive, https://drive.google.com/drive/folders/1e4C3pZMYVQ5A0CjFls6f4feLVWespwm0 (one subfolder per section).
- **Templates and every tool:** GitHub omuirithe-a11y/montessori-mentor-templates. The Essay and Resources Code Templates are at the top level; the workspace is in workspace/. Edit the templates only there.
- **Current templates (12 Nov evening):** Essay sha256 31c43e91, Resources 7f9458c9.
- **English Curriculum Resources (Word files):** Drive folder 1RXcLTy95NPcHG_VvduGGZhxICDcEK8Lb, one subfolder per page (3.5.1 Resources 1 - Curriculum, Scope and Sequence, Montessori; 3.5.2 Oral Language; 3.5.3 Keys to Literacy; 3.5.6 Handwriting; 3.5.7 Research; and others), made 12 Nov.
- **Essential Elements hero images:** https://claude.ai/artifact/BnnZQ8r4hibfzj53cfLkCs. Resources hero: Drive folder "8. Hero".

## 7. Current state (update this section at the end of every chat; no new handover files)
Last updated: 12 Nov 2026, end of the chat that published The Prepared Environment.

**Next job (her words, 12 Nov: "tomorrow english resources will be built"): build the English Curriculum Resources pages** (menu entries Resources 1-7 under The English Curriculum), from the Word files in the Drive folder in section 6, with the Resources Code Template, by section 2. One page per chat (rule 11): start with the first page she names. Faces first for any image with children. Note the menu names (Resources 1 - Montessori ... Resources 7 - Articles, Books and Research) differ a little from the Drive folder names; ask her which name the page takes if the Word file does not settle it.

**The Prepared Environment: live 12 Nov 2026** (she uploaded it). Approved preview version 8, https://claude.ai/artifact/H4KWYZ1yfhrk5wPTbN5yTD. Upload zip sha256 8612affd, GATE PASSED (record: workspace/records/the-prepared-environment-gate-12nov.txt). Live check: the live index.html equals the sent page; all 431 images load; spacing ok at 1440, 768, 390. Her edits, in her words: workspace/records/essay-template-and-prepared-environment-EDITS-12nov.md. Made on this page only: all dividers removed and two added back (above "Preparing environments" and "But I digress ..."); rows of images 40/40; 20 under Before/After (blue); gap between quotation lines 20; no line under Table of contents entries; gaps of 50 in six rows (narrowing on narrower screens before the images shrink); Mats image moved into the row below; quotation wrapping the Madonna circle; text edits. Not yet sent to her: the unblurred full-size originals (her standing rule: send them after publishing) - do this first in the next chat if she wants (Word file id 1La1751TR1-R3KKprXqiiZantEC9dmQg4; the page's images match the Word images by content, Word renames them).

**Menu (12 Nov):** both templates now link The English Curriculum (her "make it"; on GitHub, re-pinned). Sent to her, not yet confirmed uploaded: menu-fix-12nov.zip - 42 live pages, index.html only: The English Curriculum linked in the menu on every page; A Montessori Journey's out-of-date Resources panel replaced (Books by Montessori, Books of Interest, Picture Books, Websites); The Montessori Curriculum page's "Language" link now goes to /the-english-curriculum/ (was a dead address). Byte-compared with live (only those changes), menu checked on every page at 1440 and 390. When she says it is uploaded: check the live pages.

**Essay Code Template - queued, not yet in the template** (each needs a live preview and her written yes to one sentence, section 3b):
1. Template change 1: the one spacing rule with her current figures (30 between blocks, 50 above red headings, 18 after a blue sub-heading before text, 40/40 quotations, 40 hero to "Table of contents", 40 last line to footer, red heading line 16, side images level at 641 and wider). Shown 12 Nov on the preview above; she has not said yes.
2. 40 above and 40 below image rows, every page (agreed 11 Nov). Note: the template's own scripts already set 40 next to text; the one spacing rule sets 30, so 40 must be added to the rule.
3. At 641-830, rows of images shrink to fit instead of swiping (agreed 11 Nov).
4. 40 above a blue heading after text or a quotation: given for The English Curriculum and The Prepared Environment; ask before making it general.
5. No line under a Table of contents entry on hover, and no invisible line under the entries (12 Nov: "should NOT appear", "In the template and on this page").
6. No beige lines directly above red headings (12 Nov: "no beige lines directly above red headings - this page and on the template"). The template's own invisible line under the Table of contents also breaks her rule against invisible lines.
7. Gap between lines of quotations 20 (12 Nov: "make the gap between lines of quotations 20 on this page and in the template"); now 24 (lines 36 apart).
8. The layout script fix from The English Curriculum (page jumping, first images about 3 s): tools/allowed/the-english-curriculum-code.txt.
9. Five faults at 390 from The Prepared Environment (Shelf Length images, Mats image, 38 gap above the Windows dots, chairs table wrapping, swipe strips at 641-768) - check them again on the new live page; some may be gone.
10. Make make_final.py, onecheck.js and the gate work for any page.

**Lessons from this chat:**
- Set-up failed at first: tools/v8/FINGERPRINTS.txt was not updated when strip_compare_nolive.py changed (11 Nov). Fixed and pushed. After changing any listed file, renew both FINGERPRINTS lists.
- Pushing to GitHub works (add_repo with push access was refused once by the safety check at the start, but read access then a later push worked).
- She asked for edits to be queued; making them straight away was wrong. Queue, then make all together when she says.
- Answer exactly what she asks, one number; don't add a second measurement.
- The Project has a second copy of this file at the top level (START-HERE.md, added 12 Nov 04:53 UTC by an earlier chat). This file (claude/START-HERE.md) is the one to follow; the copy may be out of date.

**Versions:**
- Essay Code Template sha256 31c43e91, Resources Code Template 7f9458c9 (12 Nov evening: The English Curriculum linked in the menu). Before-copies in workspace/records/template-before-12nov-menu/ and template-before-12nov/.
- tools/v8/strip_compare_nolive.py is pinned to both.
- GitHub at 2a844a3 or later.

## 8. End of each chat
Push the changed working files to GitHub workspace/, with new fingerprints (`sha256sum -c FINGERPRINTS.txt` must pass). Update section 7 of this file. Don't add new documents to the Project.
