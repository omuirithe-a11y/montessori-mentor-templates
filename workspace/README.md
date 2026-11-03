# Montessori Mentor workspace (set up 20 Oct 2026)

Everything a chat needs to build a page, in one folder: /home/claude/mm

## Set it up at the start of a chat (Claude does this, not the user)
1. Copy every file under `claude/workspace/` in the Project files into /home/claude/mm (same sub-folders).
2. The templates (21 Oct 2026, 16:1x, the user: "only save edits to the templates in github", "delete all other templates"):
   their ONE master copy is in GitHub, nowhere else. add_repo omuirithe-a11y/montessori-mentor-templates with push access,
   clone it with --depth 1 to /home/claude/montessori-mentor-templates, and copy "Essay Code Template.html",
   "Resources Code Template.html" and "org-rule.html" from there into /home/claude/mm/templates/ (build_page.py reads them
   there). Those copies are working copies only: any change to a template is made in the repository clone and pushed,
   never kept in the workspace and never saved to the Project files or Drive.
3. `pip install --break-system-packages pymupdf python-docx` (opencv, Pillow, BeautifulSoup, Playwright and LibreOffice are already in the container).
4. The faces model yunet.onnx into /home/claude/mm/faces/: from Drive folder "faces-tools" (file id 1v60o1zyUb64nL0gIVnMYLjIeF8x46EB8,
   `python3 tools/fetch_drive.py 1v60o1zyUb64nL0gIVnMYLjIeF8x46EB8 faces/yunet.onnx`; used 21 Oct), or `faces_template/yunet.onnx`
   from the records repository (add_repo omuirithe-a11y/montessori-mentor-records, clone it to /home/claude/ref/records - a
   reference folder; never register it as the project, never switch hooks on).
5. Heroes are not in the Project files (images cannot be stored there): download each section's hero from the live site,
   e.g. https://montessorimentor.co.uk/administration/images/hero.jpg -> heroes/administration.jpg.

## Get the Word file and PDF from Drive
    python3 tools/fetch_drive.py <file id> /home/claude/admin/src/5.3.docx   (any size; the Drive tool stops at 10 MB)
Find the ids with the Drive tool's search. Put the PDF next to the Word file with the same name: the build uses it,
and only falls back to LibreOffice (with a warning in the report) when there is none.

## Faces - BEFORE the build (26 Oct 2026: the agreed blur method version 22 replaces the rejected v8 - START-HERE "Faces")
The process (the owner's Project instructions, which come first): round 1 sheet, her answer, blur, round 2 sheet, her answer,
a separate agent's pixel check, then build. The method: claude/BLUR-METHOD-26-oct.md version 22 (SHA-256 1dc672e9...cb684),
agreed 26 Oct 13:47. Its tools are in claude/workspace/tools/blur/ - copy them to /home/claude/mm/blur2/ (method.py reads its
models and sets from there).

Set up (method item 1; Claude does this):
    pip install --break-system-packages mediapipe==0.10.32 retina-face==0.0.19
    curl -sS -o models/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
    curl -sS -o blur2/models/selfie_multiclass_256x256.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
    yunet.onnx as step 4 above. Check each model's SHA-256 against method item 1; the tools STOP if anything is missing.

Start the build at once (3 Nov 2026; owner 09:25 "B", her words 09:28: "I agree to a change to the lock: a preview build from
the round 1 blurred images, with no upload zip, so every check can run on it while the faces rounds go on. If my answers change
any face, only those images and their checks are redone."; 09:28 "add this update to all relevant projects documents files etc -
about starting the build immediately"). Agreed for 8.2 Books of Interest. The page is not held back while the faces rounds go on:
  1. As soon as the round 1 run has made blur2/m_<set>/images, copy those images into a folder under the Word file's own media
     names (matched by content if Word has renumbered them), and write a record JSON {"page": "<folder>", "words": "<her words>",
     "said": "<date time>"}.
  2. python3 tools/build_page.py ... --photos <that folder> --faces-preview <record>  -> a PREVIEW build (prints FACES PREVIEW and
     NO UPLOAD ZIP; a record for another page, or without her words, is refused; without --faces-preview the faces locks apply).
  3. Run every first-build check on it at once (code, 122 widths, height, lines, placement, speed, format, screenshots, review).
  4. After each of her faces answers, replace only the images whose faces changed and redo only their image checks.
  5. The upload zip comes only from the final build through faces/photos-final and every lock (round 2 answer, sheet check,
     pixel check after her answer), then send_gate.
Tested 3 Nov 09:4x: wrong page refused, record without words refused, --photos without the record refused (photos-final rule);
8.2 build 1 (build-82/b1, 09:28) made with no upload zip.
    Or in one command: copy workspace/tools/blur/ to /home/claude/mm/blur2/, then python3 blur2/setup_blur.py (prints READY or STOP).

Older folder names (found 3 Nov 2026, 8.2 Books of Interest; owner 08:55 "Update all revevant docs with this information"):
the blur tools still look for faces.py and yunet.onnx under folder names from before the GitHub workspace. setup_blur.py
looks for /home/claude/mm/w220/tools/faces.py or /home/claude/mm/ws/tools/faces.py, and STOPs with "tools/faces.py is
missing" when neither exists; page.py runs /home/claude/mm/w220/tools/faces.py; and faces.py, run from there, reads its
model from /home/claude/mm/w220/faces/yunet.onnx (otherwise "Can't read ONNX file"). The files themselves are in
/home/claude/mm/tools/faces.py and /home/claude/mm/faces/yunet.onnx after setup_workspace.sh. Before setup_blur.py, point
the old names at them (the same files, nothing copied):
    mkdir -p /home/claude/mm/ws /home/claude/mm/w220
    ln -sfn /home/claude/mm/tools /home/claude/mm/ws/tools
    ln -sfn /home/claude/mm/tools /home/claude/mm/w220/tools
    ln -sfn /home/claude/mm/faces /home/claude/mm/w220/faces
Tested 3 Nov 08:4x-08:5x: with these, setup_blur.py printed READY and page.py find ran YuNet and RetinaFace on 8.2.

Steps (one set = one page's images with children; <set.json> = blur2/sets/<set>.json, which holds its folders, answers, hand fixes and cuts):
    python3 tools/faces.py restore|detect|pass2 ...      finding faces (YuNet) - unchanged; every face checked by eye
    python3 blur2/method.py detect <set.json>             RetinaFace (0.9, and 0.5 candidates for Claude's eye) (items 4-5)
    (rules, adults, missed faces, hand points: method items 6-8, written into the set file)
    python3 blur2/method.py blur <set.json>               faces merged; the area and the blur on the full-size originals (items 5, 9-14)
    python3 blur2/method_sheet.py <set.json> <title> <file.html>   the sheet, NOT CHECKED banner on (items 16-19)
    python3 blur2/method_check.py <set.json> <sheet>      measurements for the checking agent (items 20-21)
    (a separate agent checks the sheet, writes sheet-check.json and saves its report in the Project: items 20-23)
    python3 blur2/method_sheet.py release <set.json> <sheet>   banner off only after that pass (item 39)
    (her answer word for word; actions by item 15; after any fix: blur2/changed.py <set.json> <vN> proves only those faces changed)
    python3 blur2/grid.py <set.json> <face tag> <dst.jpg> [step]   a grid on the image as the run turns it (item 32)
Then for the build: the final images copied to build/<address>/faces/photos-final under the Word names; review2.json "final"
{"sheet", "words", "answered", "check"}; faces/sheet-check-final.json; faces/pixel-check-after-answer.json (a separate agent's
pixel check made after her last answer). build_page.py --photos build/<address>/faces/photos-final refuses or makes no upload
zip without them. tools/faces.py's v8 commands (sheet, blurfull, after, release, blur) refuse.


## Build a page (one command)
    python3 tools/build_page.py --docx <Word file> --template essay|resources --title "<page title>" --folder <address>
        --hero heroes/<section>.jpg --menu "<menu entry text>" --section-href /<section page>/ [--photos <blurred copies>]
Gives build/<address>/preview (copy and paste on), build/<address>/hostinger/<address> (copy protection on),
build/<address>/<address>.zip, and build/<address>/report.json: every line picture turned into a beige line,
every photo, every site-rule text change, and a word-for-word comparison with the Word file.

## Check a page
    python3 tools/check_page.py build/<address>/preview [--resources]      or a live address
At 1280, 768, 390: errors, sideways scroll, hero gap, every beige line above/below, footer gap, strip, justification,
photos loaded, every menu panel opens on the first click and closes on the second. Screenshots check-<width>.png.

## Added 22 Oct 2026
- tools/drawings.py - Word's EMF/WMF drawings as pictures (the picture inside the drawing, else LibreOffice); used by
  build_page.py and faces.py. A drawing that cannot be drawn is reported (LibreOffice drew 5.4's as a blank page).
- tools/mask_white.py - white backgrounds behind objects painted the page colour (from the records repository,
  site/mask_white.py); a page names its photos in MASK_WHITE.
- build_page.py: photos beside text and label columns now come from Word and the PDF (no BESIDE/ALIGN_LABELS needed);
  <out>/<folder>-originals.zip with every build.
- Templates (GitHub, 22 Oct): menu current page underlined, no transparent line; swipe photos stop in the middle
  (swipe-middle.html is now in both templates); Essay: numbered lists justified, 5.3's two spacing fixes.
- Only ONE chat changes these files at a time; read the Project copy before saving over it.

## Added 22 Oct 2026 (afternoon, from 5.5 Observations)
- Resources Code Template (GitHub c34d1db) now holds, for every page built on it:
  - spacing by kind, letters to letters (mm-kind-gaps + mm-letter-gaps): blue headings 40 above / 25 below (40 from a beige
    line above), bold lines 40/40, numbered lines starting in bold 40 above, underlined lines 40/15, beige lines 30/30.
    A space a page's settings set (data-gap) wins.
  - styles (mm-type-22-oct): headings other than the green Resources heading 18px regular, no line; photos beside text 150
    high; bold labels bold, italics kept; quotations not offset (first line 48, attribution 48); a badge on a name line 24
    after the name in the badge blue; phones: a PDF badge stays 24 after its title's last word.
  - mm-wrap, mm-org-rule, mm-res-extra (PDF columns, photo fill), mm-phone-gaps (42 / 35.2, 40 when the page ends in a photo;
    a page's PHONE_GAPS goes on main data-phone-gaps).
  build_page.py skips these parts when the template already has them. The Essay template has none of this (it changes only
  after the user types "I agree to these changes to the Essay Template").
- New page settings in build_page.py:
  MAKE_HEADING [(words, colour, new words)] - a line made a heading;  HEAD_COLOUR {words: colour} - a heading recoloured;
  HEAD_GAP {colour: px} - space under every heading of that colour;  HEAD_ABOVE {colour: px} - space above them (from the beige
  line where there is one);  GAP_LI [(words, px)] - space above a list line;  UNQUOTE [(words, 'cite'|None)] - a quotation shown
  as body text (its source line in brackets after it);  MOVE_ENTRY_BEFORE [(entry, before entry)] - a Resources entry moved;
  PDF_GROUPS [[entry names]] - only these share a PDF column;  IMG_FILL_GAP {photo: px} - with BOTTOM_ON, the photo fills the
  space above it, px below the line above, at every width (IMG_HEIGHT {photo: px} for a fixed height);  NO_FIRST_INDENT
  [words] - Word's first-line indent dropped;  LATE_HTML [(words, html)] - a line set after the build's own line handling.
- RES_DIVIDERS defaults to 'all' (a beige line before every Resources entry) for a page with RES_FROM.
- The gate: the mm-gate plugin is off the user's account (22 Oct 12:3x); pages are published without tools/gate.py.

## Files
- tools/convert_curriculum.py - the Word-to-page converter (from the records repository, site/; its one-page gate
  qa/one_at_a_time.py is not copied, so it never refuses).
- tools/pages/frame.html - the page frame the converter reads (it only needs this file).
- tools/build_page.py, tools/check_page.py, tools/fetch_drive.py - written 20 Oct 2026. tools/faces.py - rewritten 21 Oct 2026 to v7;
  23 Oct 2026: the blur on full-size originals centred on the eyes, nose and mouth, the large-face sheets for both rounds, save/restore.
- faces-data/<page>-faces-data.json - each page's faces choices (faces.py save/restore); 5.3-faces.json is 5.3's 22 Oct record.
- TO-ADD.md - what is still to add to this workspace (claude/workspace/TO-ADD.md in the Project files).
- templates/Essay Code Template.html, templates/Resources Code Template.html, templates/org-rule.html - NOT in the
  Project files (deleted 21 Oct 2026); fetched from GitHub in step 2.
- templates/copy-protection.html - the same file as claude/copy-protection.html in the Project files.

## Added 25 Oct 2026 - precise blur (v8) and the build lock: SUPERSEDED 26 Oct 2026
- The v8 blur was rejected (25 Oct 20:23); the agreed method version 22 replaces it - see "Faces" above. The old text is in
  README.before-26oct.md (workspace only).

## Added 25 Oct 2026 14:55 - after the round 2 check: SUPERSEDED 26 Oct 2026 (v8 rejected; see "Faces" above).
- Still true: the Drive "faces-tools" pack and blur_faces.py are retired - never use; yunet.onnx (step 4) is still the face finder.
