# Separate check v2 of the round 2 faces sheet, The English Curriculum (3.5.0), 5 Nov 2026

Checker: a separate agent. Method: BLUR-METHOD-26-oct.md version 22, items 20-23, adapted to round 2. No image, mask, tool, faces.json or sheet was changed. Check v1 (round2-check-report.md) failed the sheet on a missed boy on image 33 and on the left-over "could not decide" line; this check covers the fixes and runs the five parts again.

Her round 1 answer (5 Nov 09:31, word for word): "These are the edits to the blurring. No blurring needed on the following: 4i. 14b. 25g. 27e. 31fh. 33f. 38de. 105b. 108b. 110b. 123f. 128b." = 14 faces.

## 1. Statuses - PASS
m_eng/faces.json against m_eng-round1-0931/faces.json: the same 165 images, image numbers and "left_off" entries; no face removed; no box moved. Exactly 14 faces changed status, all from blurred to "left unblurred by your answer": 4-i, 14-b, 25-g, 27-e, 31-f, 31-h, 33-f, 38-d, 38-e, 105-b, 108-b, 110-b, 123-f, 128-b. One face added: 33-g, blurred, src "hand", box [709.0, 238.3, 734.4, 289.1] at scale 2.56 = full image x 1815-1880, y 610-740 (the spot check v1 named). It matches m_eng/faces/extra_faces.json key "33" (the only difference from extra_faces.json.before-33g), with the reason "hand fix after the check (round 2 check 5 Nov 09:48)". Totals: 270 blurred (269 + 33-g), 41 left by rule, 21 left by her words. The blur log m_eng/blur-round2b.log ends "blur done 121 images; refused (no points): []"; against blur-round2.log the only changed line is image34.jpg "faces 6 blurred 3" -> "faces 7 blurred 4". m_eng/changed-vR1.json = ["33-c", "33-g"].

## 2. Unchanged images - PASS
121 result images in m_eng/images and in the round 1 copy, same names. The 109 images not among 4, 14, 25, 27, 31, 33, 38, 105, 108, 110, 123, 128 are all byte-identical to round 1 (sha256). The 12 named all differ from round 1, as expected. Masks: the 14 kept faces' masks are gone, 33-g.png is new, all other 269 masks byte-identical to round 1.

## 3. Changed images (image 33 against the previous round 2 run) - PASS
The previous round 2 run's image files were overwritten, so the comparison was made two ways:
- Against round 1 at full size (v1 found the previous round 2 run differed from round 1 only at the kept face 33-f): every pixel on image 33 that changed by more than 6 levels lies within 16 px of the 10% line of 33-f or of 33-g; changes of any size reach no further than 40 px from them (92 px of 1-3 levels within 16-40 px, JPEG blocks). Near 33-g the changes span x 1807-1888, y 639-752 (more than 6 levels: x 1821-1871, y 656-736). 33-f's area is as the original (largest difference 12 levels, changed share 0.000), as v1 found. 33-a and 33-b: difference 0 inside their 50% areas.
- Against the v1 sheet (round2-v1-check-failed.html, which embedded the previous run's renders): the new whole render of image 33 differs from the v1 one only at full-image x 1743-1893, y 505-801 (33-g and its new box and letter). The whole renders and crops of the other 11 images are byte-identical to those in the v1 sheet, so those images are unchanged since the previous run.
- 33-c: outside the 3,386 px where its 50% area meets 33-g's area, it is identical to round 1 (max difference 0); changed share against the original 0.448 (0.433 in round 1; the rise is the overlap with 33-g). The 33-c crop changed only because 33-g lies inside it.
- 33-g by eye, original beside result, at full size, 3x, 4x and 8x: nose and mouth gone; the lowered eye's lash line is now a soft smudge (brightness dip across it cut from about 80 levels to about 15). A small dark mark just above the blur's top edge (about x 1851, y 654, the end of the eyebrow or upper lid crease) is untouched; it does not read as an eye. Soft edge, no spill onto 33-c's hair beyond the overlap already blurred, or onto the bottle.

## 4. By eye - PASS
All 12 result images looked at whole in two halves with every box drawn and lettered, and every doubtful spot enlarged on the full-size image:
- 4: boy in the pink and white shirt (cheek and ear, no eye); girl with the star clip (ear, back of head); the picture card the teacher holds (printed); child's arm at the right edge. 4-g is the adult teacher.
- 14: the figure in yellow behind the raised hand is a standing adult with glasses, hidden by the hand's motion blur; a printed face on the alphabet strip at top right; hair at the right edge.
- 25: boy in blue at the back and girl sitting (backs of heads); child behind 25-b's head (cheek and ear, turned away).
- 27: girl at the left (back of head); child behind the plant (cheek and ear, out of focus, turned away).
- 31: boy at the far left (back of head, writing); boy in grey (back of head).
- 33: 33-g now blurred; child under the adult at the back left (top of head behind the counter); child in purple (cheek, turned away); child in grey behind him (head hidden); 33-d and 33-e adults.
- 38: 38-d (reflection) and 38-e left by her answer; 38-f blonde girl, profile with the eye under her hair, left by rule as in round 1.
- 105: child in gingham (back of head); child behind the girl (top of head).
- 108: through the glass, a small child's head in front of the seated figure (back/top of head, no eye) and an adult's legs at the right.
- 110, 128: nothing else (128 child in pink: head hidden behind the adult's legs; children at the top edge cut off).
- 123: child behind the raised blue arm at top left, out of focus, no eye to be seen; grey sleeve of an adult at top right.
No other child's face with an eye showing is unlettered. All blurred faces on the 12 images still hide eyes, nose and mouth.

## 5. Sheet contents - PASS
round2.html: 5,486,773 bytes, sha256 e7ece314893b950afccdb48da8b25692d45f0e910e39c9b79abec3f354ccc40f, "Made 05 Nov 2026 09:52:30", NOT CHECKED banner on.
- Exactly the 12 images, 57 embedded images (12 whole renders + 45 face crops), each byte-identical to a file in m_eng/whole-sheet or m_eng/crops. Against the v1 sheet only 3 changed: the whole render of image 33, the 33-c crop and the new 33-g crop.
- 33-g is shown with its crop (original with white outline, and result) and marked "hand fix after the check: a boy behind 33-c the round 2 check found unblurred - not your answer"; the top box lists "Faces I adjusted by hand after a separate check found a fault (not your answers), 1: 33-g".
- The 14 are each listed as "left unblurred by your answer" (14 occurrences, no others); the 4 by-rule faces with their reasons.
- "Faces I could not decide (red unless you say otherwise): none."
- Count line "45 faces blurred on 12 images; 18 faces left" matches m_eng_r2/faces.json, which equals m_eng/faces.json for these 12 images except that 33-g's notes carry the hand-fix line first.
- Wording slip (not a fail): because the hand-fix line was put first in 33-g's notes, the sheet's area line for 33-g reads "... - not your answer outline (yellow) + skin labels + oval", and the red "mesh found but failed the position tests" label is lost. 33-g has no usable mesh and no yellow outline on its crop; its area is skin labels + oval. The "Faces without a mesh, 22" list also leaves 33-g out. The maker may want to tidy this line; it does not change anything she is asked to judge.

## For the owner (by the sheet's image numbers)
- 33-g: the boy behind the girl at the far table (behind 33-c) is now blurred. This was added by hand after the check, not from your answer. A small dark mark of his eyebrow shows just above the blur. It is not an eye.

## Could not check
I could not compare byte for byte with the previous round 2 run's image files, because that run's files were overwritten. I compared against round 1 and against the renders embedded in the v1 sheet instead (part 3). Images outside the 12 were checked for being unchanged, not looked at again by eye.

PASS
