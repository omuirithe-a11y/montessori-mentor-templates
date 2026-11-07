# Pixel check after the owner's last answer - The English Curriculum (3.5.0)

Separate agent, final pixel check (BLUR-METHOD-26-oct.md version 22, skill step 7). I had not seen the work before. No image or tool was changed. Checked 5 Nov 2026, finished 10:33 (Asia/Shanghai).

**Result: PASS.** No faults. Four notes for the owner are at the end.

## Her answers, as recorded
- Round 1 (5 Nov 09:31): "These are the edits to the blurring. No blurring needed on the following: 4i. 14b. 25g. 27e. 31fh. 33f. 38de. 105b. 108b. 110b. 123f. 128b."
- Round 2 (5 Nov 10:04): "approved". Round 2 sheet: blur2/m_eng_r2/round2.html, which added 33-g, a hand fix after the check.

## What was checked
- Final images: build-35/faces/photos-final, 104 files.
- Name map: photos-final-names.json (104 pairs, no repeats).
- Originals: blur2/m_eng/media.
- Faces data: blur2/m_eng/faces.json.
- Masks: blur2/m_eng/masks/<tag>.png. Each mask is the size of the face's crop (faces.json "crop"). Its three channels are the feathered weight above 0.5, above 0.1 and above 0.01.

I wrote my own scripts for this check. They read the files only and are kept in my scratchpad.

### Counts
- photos-final.json lists 165 images. 105 are blurred and 60 have no face to blur.
- 104 of the blurred images are in the 5 Nov Word file. image74.jpeg (no 73) is not: the content map new-to-old-media.json does not use it. So it is not in photos-final, and its old-named copy is in photos-final-oldnames only (105 files there).
- Faces in the 104 images:
  - 267 blurred (270 in faces.json, less 73-c, d and e on image74.jpeg)
  - 32 left: 14 by her round 1 answer and 18 by rule
- The other 7 faces "left unblurred by your answer" (87-a, 87-b, 92-a, 103-b, 106-a, 113-a, 132-a) are on images that are not in photos-final (no face to blur there, so the original is used). They come from the earlier no-blur list (keep_unblurred.json), not from today's answer.
- All 14 faces she named are left, and none of them is blurred: 4-i, 14-b, 25-g, 27-e, 31-f, 31-h, 33-f, 38-d, 38-e, 105-b, 108-b, 110-b, 123-f, 128-b.

### 4. Right image, right turn
- Every final file is the same size as the original its map name points to.
- Every original stored under the new name in the 5 Nov Word media folder is byte-identical to blur2/m_eng/media/<old name>: 104 of 104.
- Every file in photos-final-oldnames is byte-identical to its new-named file: 104 of 104.
- No original carries an EXIF turn (all orientation 1), so page.py turned none back.
- The final files carry no EXIF orientation tag.
- image7.png and image66.png are RGBA originals with no transparent pixels, so saving them as RGB loses nothing.
- The difference test outside the faces (item 3) also matches each final file to its original, pixel for pixel, so no image is under the wrong name.

### 3. Nothing changed outside the faces
- **Area tested:** every pixel outside the union of all blurred faces' feather reach (mask weight above 0.01), grown a further 16 px to allow for JPEG blocks. That is 942.5 million pixels over the 104 images.
- **Measure:** the largest difference in any colour channel, final against original. As a reference for JPEG noise, I re-encoded the original the same way the pipeline did (JPEG 92, then JPEG 95, or PNG for .png) and measured that difference too.
- **Result:** the final files match that reference in every image.
  - Mean difference is equal to 0.01 levels in every image (largest mean 3.18, reference 3.18).
  - The 99.9th percentile is at most 24 levels, and the maximum is at most 61, the same as the reference.
  - Final against the re-encoded reference: no pixel differs by more than 40 levels anywhere outside the faces (0 pixels).
- **Verdict:** what changed outside the faces is JPEG noise only.

### 1. Every blurred face is blurred
Measured for all 267 blurred faces, on the full-size images, inside each face's full_box where the mask weight is above 0.5:

- **Fine detail:** measured as Laplacian energy, final against original.
  - Median 0.069.
  - Largest 0.383 (65-a, 33 px wide, a soft, low-detail original).
  - Every face lost at least 62% of its fine detail, and most lost over 90%.
- **Eye, nose and mouth points:** recovered for all 267 faces with method.py's own face-loading code.
  - Eyes and mouth corners fall inside the 0.5 line on nearly all faces.
  - On about 20 profiles (for example 120-a, 59-a, 95-c, 23-d, 116-a and b, 152-d, 26-a, 54-b), the nose-tip or mouth point sits on the outline of the profile, just outside the 0.5 line but inside the feather. That is where the method's area ends on a profile.
  - Every one of these 20 was looked at by eye (see below).

**By eye, at full size and enlarged, original beside final, with the area outline and points drawn:**
- every face under 40 px wide (11): 14-c, 28-f, 31-e, 35-d, 42-a, 65-a, 65-b, 65-c, 66-a, 66-b, 66-c
- 30 at random (Python random.seed(20261105), random.sample over the rest): 134-b, 74-d, 57-d, 74-a, 13-a, 79-a, 4-d, 128-a, 27-c, 4-h, 51-a, 144-a, 28-a, 81-b, 19-f, 84-d, 56-a, 67-b, 82-a, 68-b, 29-c, 93-a, 74-b, 20-a, 144-e, 83-a, 105-a, 19-h, 18-d, 22-b
- 33-g (the hand fix)
- the profiles whose points sit at the edge: 120-a, 116-a, 116-b, 152-d, 23-d, 26-a, 59-a, 95-c, 54-b, 64-b, 141-e, 41-d, 37-a
- the faces my eye-window measure flagged: 141-d, 63-c, 151-a, 53-a, 21-c, 74-e, 4-f, 22-b, 144-e, 152-f, 25-b, 58-c, 4-d, 110-a

Open mouths (79-a, 51-a, 56-a, 28-a, 74-a, 59-a, 120-a) and profiles (4-d, 4-f, 4-h, 57-d, 67-b, 84-d, 81-b, 93-a, 19-h, 22-b, 134-b, 128-a, 74-e, 152-f) are among them.

On every one, the eyes, nose and mouth cannot be read: no shape of an eye, nose or lips that would identify the child is left. 33-g: the lowered eye, nose and mouth are gone; the blur is soft-edged and the blue bottle is untouched.

### 2. Faces left match the original
All 32 left faces (14 by her answer, 18 by rule: adults, printed images, objects, heads turned away) were measured inside their boxes:
- The mean difference equals the JPEG-noise reference to 0.01 levels on every one.
- The largest single-pixel difference is at most 22 levels.
- Fine detail (Laplacian) is 0.99 to 1.26 of the original, so none of them is blurred.
- 64-c (the adult teacher): 17% of his box lies inside the feather of the blurred child 64-b next to him. That part is softened by 64-b's feather, as the method allows. The rest of his box matches the original (mean 1.50 against reference 1.49).

### 5. Missed faces
- **By eye:** every one of the 104 final images was looked at whole, at 760 px, with the left faces boxed.
- **Enlarged parts:** busy areas were enlarged on images 14, 15, 17, 19, 20, 22, 24, 26, 28, 29, 30, 31, 32, 34, 38, 39, 41, 42, 59, 63, 64, 65, 66, 72, 74, 75, 77, 80, 81, 84, 95, 96, 106, 110, 116, 122, 124, 125, 136, 142 and 145 (new names).
- **Second detector:** I also ran YuNet myself on every final image at 0.5 confidence, at full size and half size. It found 134 places not near a lettered face. Each was looked at enlarged: all are blurred hair, hands, backs of heads, printed cards, toys, or children too far back to show an eye.
- **Result:** no child's face with an eye showing is unlettered and unblurred.

The 5 Nov Word file has one image not in faces.json, image97.gif (and image3.gif): both are 623 x 2 px line strips, with no faces.

## Notes for the owner (not faults)
1. **59-a (image59.JPG, the girl in profile):** at 4x enlargement the eye shows as a soft dark smudge where the eye was. It is not readable as her eye at page size or at full size. The nose and mouth are gone. Say if you want this face blurred more.
2. **Profiles generally:** on the profiles listed above, the nose tip and lips at the very edge of the face are softened but not as fully as the middle of the face. This is the method's profile edge, as earlier checks noted for 67-c.
3. **image38.JPG (no 37):** two children at the top edge are cut off by the frame above the nose. Their mouths show, but no eye does. They are left by the "head cut off by the frame" rule, as in the round 1 checks.
4. **image74.jpeg (old no 73) is not in the 5 Nov Word file.** Its blurred copy is not in photos-final. Nothing is needed unless the image is put back.
