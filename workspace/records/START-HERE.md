# Montessori Mentor website - start here

The only instructions file. Updated 9 Nov 2026 (section 7 updated 12 Nov). It replaces every earlier START-HERE, HANDOVER, DECISIONS-LOG, BUILD-ORDER, check list, lessons file and agent instruction (owner, 9 Nov: "Remove old outdated unhelpful commands orders etc from start-here. I want each new chat to open with this plan, this way of building a page"). Those files have been removed from the Project; copies are kept on GitHub (workspace/records/) for history only. Never follow them.

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
   - Make each edit in the preview's index.html straight away, republish, and tell her in one line.
   - Every question about something visible comes with the preview open.
   - Answers are bare numbers: "The space between those two paragraphs is 29". Don't explain measuring methods, and don't quote phone figures.
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
5. **"Finished" means the preview is the page.** There is no new build. Run `python3 workspace/pages/pe-final/make_final.py <last build zip> <approved preview index.html> <out zip>`. It puts copy protection back, keeps the full-size images, leaves out deleted images, and proves that the page equals the approved preview.
6. **The checks, once, one at a time, with nothing else running.** The machine has two processors, and a second browser job made the speed check fail on 9 Nov. Put the results next to the zip.
   - Code check (tools/v8/strip_compare_nolive.py). Add the preview's new lines to tools/allowed/<page>-code.txt, with her words.
   - Format check against the Word file (tools/v8/format_check_word.py). Her edits should be the only new differences.
   - 122 widths (vfast.py), height (stable.py at 1440 and 390), placement (tools/v8/place_check.py) and speed (speed_check.py). The first three are in handover-2026-10-29-evening/tools-v5-fixA-200, speed_check.py in tools-v5-fixA.
   - The spacing check at all 122 widths (pages/pe-final/onecheck.js).
   - Lines through text (tools/lines_v2.py, 8 widths).
   - A separate agent compares screenshots of the final page with the approved preview at 1440, 1024, 768, 641 and 390.

   Fix any fault in the page, then run the checks again.
7. **Gate:** tools/v8/send_gate_pe.sh must print GATE PASSED. Then send the UPLOAD zip with one line of context.

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
9. Answers are short. Give bare numbers, no phone figures and no measuring methods. An independent agent checks and corrects every answer before it is sent (8 Nov; 9 Nov: "Agents look at and correct all answers"). The agent is given the exact final text. What it passes or corrects is sent word for word. If any word is changed after the check, the changed text goes back to an agent before it is sent. (11 Nov she said "stop all agents now"; replies since then were not agent-checked. Ask her before starting again.)
10. If a fault, mistake or typo is found, correct it at once.
11. One page per chat.
12. Don't refer to The English Curriculum build or its decisions (8 Nov: "Whatever was done with that build was wrong"). This means the old builds before 8 Nov; the page finished on 12 Nov by section 2 is a valid reference.
13. "save this" means a download link, never GitHub.

## 6. Where things are
- **Word files and PDFs:** Google Drive, https://drive.google.com/drive/folders/1e4C3pZMYVQ5A0CjFls6f4feLVWespwm0 (one subfolder per section).
- **Templates and every tool:** GitHub omuirithe-a11y/montessori-mentor-templates. The Essay and Resources Code Templates are at the top level; the workspace is in workspace/. Edit the templates only there.
- **Current templates (12 Nov):** Essay sha256 021aca08, Resources 21c3edf1.
- **Essential Elements hero images:** https://claude.ai/artifact/BnnZQ8r4hibfzj53cfLkCs. Resources hero: Drive folder "8. Hero".

## 7. Current state (update this section at the end of every chat; no new handover files)
Last updated: 12 Nov 2026, end of the chat that finished The English Curriculum.

**Next job (her words, 12 Nov: "in the handover, write that fixing the essay template is the next job"): fix the Essay Code Template.** Follow section 3b (one change at a time, shown on a live preview, her written yes before each change, re-pin tools/v8/strip_compare_nolive.py after each). What is known to need fixing:
1. Put the one spacing rule into the template, with her current figures (workspace/pages/pe-final/mm-one-spacing.js is already updated: red headings 50 above, 18 after a blue heading before text, quotations 40/40). Not yet in the template, agreed by her: 40/40 above and below images (11 Nov, "every page"); at 641-830 rows of images shrink to fit instead of swiping (11 Nov). Given for The English Curriculum only, so ask before making it general: 40 above a blue heading after text or a quotation.
2. The template's layout script set off the spacing rule on The English Curriculum: the page jumped upwards and the first images took about 3 s. Fixed on that page only (layout re-runs only when the width changes, inside one run; the foot-gap and letter-gaps load timers off; scroll anchoring). The page's changes are the "-" and "+" lines in tools/allowed/the-english-curriculum-code.txt; the page is workspace/pages/ec-final/approved-preview-index.html. These belong in the template.
3. Five faults at 390 found on The Prepared Environment (they affect other pages too): the Shelf Length images stacked and touching; the Mats image small and at the left; a 38 px gap above the dots under the Windows image; the chairs table wrapping "35 x 35 cm" onto four lines; at 641-768, swipe strips starting right of the text.
4. Make make_final.py, onecheck.js and send_gate_pe.sh work for any page (the gate names The Prepared Environment's Madonna image). The gate was not run for The English Curriculum for this reason; its other checks were.
Already in both templates (12 Nov, her yes): all text 400 except what is named bold; contents text 18 (style mm-weight-400-12nov).

**The English Curriculum: live 12 Nov 2026.** Her approved preview version 22 (https://claude.ai/artifact/Ui87BFGaw9BteZsADD5a3g), uploaded as the-english-curriculum.zip (sha256 99914940). Live check: the live index.html equals the sent page; all 327 images load; spacing ok at 1440, 768, 390. Hostinger re-saves every image, so live image files differ very slightly from the sent ones (not visible; faces stay blurred). Every edit in her words: workspace/records/the-english-curriculum-EDITS.md. Page, build scripts and check results: workspace/pages/ec-final/. The unblurred full-size originals were sent to her as a download.

**The Prepared Environment:** on hold (her words: "The Prepared Environment: leave it.").

**Lessons from this chat:**
- A screenshot-comparison agent ran for an hour without reporting; she had me stop it. Give such an agent a fixed script and a time limit, or run the fixed comparison and have the agent only judge the differences.
- Replies have not been agent-checked since she said "stop all agents now" (11 Nov).

**Versions:**
- Essay Code Template sha256 021aca08, Resources Code Template 21c3edf1. Before-copies in workspace/records/template-before-12nov/.
- tools/v8/strip_compare_nolive.py is pinned to both.
- GitHub workspace at 89fbab6 or later.

## 8. End of each chat
Push the changed working files to GitHub workspace/, with new fingerprints (`sha256sum -c FINGERPRINTS.txt` must pass). Update section 7 of this file. Don't add new documents to the Project.
