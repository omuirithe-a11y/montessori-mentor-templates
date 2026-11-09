# Montessori Mentor website - start here

The only instructions file. Updated 9 Nov 2026. It replaces every earlier START-HERE, HANDOVER, DECISIONS-LOG, BUILD-ORDER, check list, lessons file and agent instruction (owner, 9 Nov: "Remove old outdated unhelpful commands orders etc from start-here. I want each new chat to open with this plan, this way of building a page"). Those files have been removed from the Project; copies are kept on GitHub (workspace/records/) for history only. Never follow them.

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
1. This file: section 2, and the "Recommended" list in section 7.
2. The Project's saved preferences, "Site style" part. It holds her figures: fonts, spacing, dividers, image heights, lists, menu, footer.
3. The template itself, in GitHub at the top of montessori-mentor-templates (Essay Code Template.html or Resources Code Template.html).
4. The approved look: workspace/pages/pe-final/approved-preview-index.html (The Prepared Environment, approved by her 8 Nov), and workspace/pages/pe-final/mm-one-spacing.js (the spacing rule that page uses).

How:
- One change at a time. Show it on a live preview of a real page, then offer her a sentence that states the change itself: what changes, at which widths, on which pages. Change the template only after her written yes.
- Then re-pin tools/v8/strip_compare_nolive.py to the new sha256 and push.
- Live pages change only when they are rebuilt.

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
9. Answers are short. Give bare numbers, no phone figures and no measuring methods. An independent agent checks each answer before it is sent (8 Nov).
10. If a fault, mistake or typo is found, correct it at once.
11. One page per chat.
12. Don't refer to The English Curriculum build or its decisions (8 Nov: "Whatever was done with that build was wrong").

## 6. Where things are
- **Word files and PDFs:** Google Drive, https://drive.google.com/drive/folders/1e4C3pZMYVQ5A0CjFls6f4feLVWespwm0 (one subfolder per section).
- **Templates and every tool:** GitHub omuirithe-a11y/montessori-mentor-templates. The Essay and Resources Code Templates are at the top level; the workspace is in workspace/. Edit the templates only there.
- **Current templates (9 Nov):** Essay sha256 2bd98f70, Resources 942a0587.
- **Essential Elements hero images:** https://claude.ai/artifact/BnnZQ8r4hibfzj53cfLkCs. Resources hero: Drive folder "8. Hero".

## 7. Current state (update this section at the end of every chat; no new handover files)
Last updated: 9 Nov 2026, end of the chat that built The Prepared Environment.

**Waiting for her upload (she will upload "later this morning", 9 Nov):**
- the-prepared-environment-UPLOAD.zip: The Prepared Environment, GATE PASSED, package c431a226. It is the whole folder the-prepared-environment, replacing the live one. The page source is in GitHub workspace/pages/pe-final/approved-preview-index.html (her approved preview v10, plus the menu change).
- essential-elements-menu-41-pages.zip: index.html only, for the other 41 live pages, with the new Essential Elements menu (her 9 Nov screenshot). The home page's index.html goes in public_html itself; each other page goes in its own folder. Outside that menu panel each page is identical to the live page.
- Both zips were sent to her in the chat. They are not in GitHub.

**First job of the next chat, after she says they are uploaded - the live check (about 10 minutes):**
1. Download the live the-prepared-environment/index.html and check it equals the sent page.
2. Run the spacing check (onecheck.js) on the live page at 1440, 768 and 390.
3. Open the Essential Elements menu on all 42 live pages at 1440 and 390 (tools/menu-9-nov/mcheck.js against the live addresses).
4. Report in a few lines.

**Recommended, waiting for her agreement (ask one at a time, with a preview):**
1. Put the one spacing rule into both Code Templates, so new pages start with it.
2. Make make_final.py, onecheck.js and send_gate_pe.sh work for any page. The gate's placement exception names the Madonna image (192-480.jpg); make it general: an image followed by a quotation at 40.
3. Five template faults the reviewer found at 390 on The Prepared Environment. All five are also in the approved preview, and they affect other pages too:
   - the Shelf Length images stacked and touching;
   - the Mats image small and at the left;
   - a 38 px gap above the dots under the Windows image;
   - the chairs table wrapping "35 x 35 cm" onto four lines;
   - at 641-768, swipe strips starting right of the text.

**Next page:** not chosen yet. Ask her which page is next, then follow section 2.

**Versions:**
- Essay Code Template sha256 2bd98f70, Resources Code Template 942a0587 (GitHub d122be5).
- tools/v8/strip_compare_nolive.py is pinned to both.
- GitHub workspace at ee9dd73 or later. The old instructions (START-HERE before 9 Nov, the memory notes before the trim) are archived in workspace/records/project-archive-9nov/.

## 8. End of each chat
Push the changed working files to GitHub workspace/, with new fingerprints (`sha256sum -c FINGERPRINTS.txt` must pass). Update section 7 of this file. Don't add new documents to the Project.
