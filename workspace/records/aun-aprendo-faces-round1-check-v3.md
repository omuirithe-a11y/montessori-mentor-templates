# Separate check v3 of the round 1 faces sheet, Aun Aprendo (1.2)

When: Sat Nov  7 05:57:09 UTC 2026 (from `date`)
Sheet: /home/claude/aun/aun-round1.html, sha256 59e02ffe95c699bf9793c895dd2cf46df6983bfcfbff7df8fde9d7d996b32302
I changed no file except this report and /home/claude/mm/blur2/m_aun7/sheet-check.json. My work files are in /home/claude/aun/check/work/v3/.

Summary: PASS. Both v2 faults are fixed, and nothing else on the sheet changed. Image 40 is now shown upright on the sheet: 40-a is on the girl and 40-b is on the teacher. The line about hand fixes now names all six faces that changed.

Faults by part: counts and byte-identity 0; item 21 measures 0; item 22 by eye 0; whole images 0.

## Part 1 - Counts and byte-identity: PASS
- **Embedded images:** the sheet holds 287 images, and all 287 are byte-identical to a file. None fails to match.
- **Counts:** faces.json, the sheet's own line and check-measure.json all give 226 blurred, 137 left, 59 images with faces and 2 left off (images 2 and 55).
- **Faces left:** the 137 faces left are exactly the entries in faces/by_rule.json.
- **Undecided faces:** 16-b, 16-f, 18-d, 20-b, 29-i and 15-k. All six are blurred faces in faces.json.
- **Sizes:** every result image is the same size as its original as stored. Image 40 is 4000x3000.
- **Image 40's working copy:** media/image40.JPG and before-fix1/image40-media-with-tag.JPG are the same length (5,019,136 bytes). They differ in exactly 2 bytes, at offsets 54 and 13238, where 6 became 1. The turn tag now reads 1, where it was 6. The decoded pixels are identical.
- **Word file:** image 40 is the only picture that Word turns on the page (`a:xfrm rot="5400000"`).
- **Hand fixes:** the sheet line now reads "Faces I adjusted by hand after a separate check found a fault (not your answers), 6: 15-k, 16-g, 16-h, 16-i, 40-a, 42-f".
  - 15-k, 16-g, 40-a and 42-f each carry a note saying what was fixed.
  - 16-h notes "was 16-g" and 16-i notes "was 16-h".

## Part 2 - Item 21: PASS
- **Measured fails:** check-measure.json lists the same 24 fails as v2, which I judged by eye in v1 and v2. My grids of them are pixel-identical to v2 (difference 0).
- **40-a:** changed on 0.91 of its area, feather reach 0.107 w. Image 40 has 0 changed pixels beyond reach.
- **My own measure of image 40:** I compared the working copy with the result, outside the 40-a crop. 233 pixels differ by more than 10 levels, none by more than 20, and the largest difference is 16. That is JPEG noise.

## Part 3 - Item 22 by eye: PASS
- **Same set as v2:** every fail, the 12 accepted candidates, the 6 undecided faces, the 10 smallest blurred faces and the 30 random faces (seed 20261108). I rebuilt these grids, and they are pixel-identical to v2 except for 40-a.
- **40-a:** I looked at it enlarged, the working copy next to the result. The girl's eyes, nose and mouth are hidden, with a soft edge.
- **Faces left:** these are unchanged from v2. 40-b is a box on the teacher's face, and she is an adult.
- **Notes from earlier checks:** 18-d still looks like an adult woman to me (blurred as undecided). 15-i is too dark to tell.

## Part 4 - Whole images: PASS
- **What changed:** I compared all 61 whole images with v2 pixel by pixel. Only image 40 changed.
- **Image 40, whole:** whole-sheet/image40.jpg is 900x1200 and upright. It matches the result images/image40.jpg turned a quarter clockwise, as Word turns it (mean difference 2.3 levels).
- **What the whole image shows:** the red outline 40-a is on the girl's face, and the grey box b is on the teacher's face.
- **Large crop and result:** crops/40-a.jpg shows the same girl and the same blurred area as the result, with the outline on her face.
- **Missed faces:** no child with an eye showing lacks a letter.

Note, not a fault: the large crop of 40-a is shown as the file is stored, so the girl appears on her side there, while the whole image above it is upright. The sheet does not claim the crops are turned as on the page, and the blur can be judged either way. Turning that crop to match would be easier for the owner to read.

## For the owner (by the sheet's image numbers)
- **Image 40:** the girl's face is blurred, and the teacher (b) is left. The large picture of 40-a appears on its side.
- **Image 16:** the letters moved. The child in goggles is g, the girl with the ponytail is i, and the boy at the front is h.
- **Image 42:** the blonde girl is f.
- **Image 15:** k is blurred and listed as could not decide.
- **Image 29:** i is listed as could not decide.
- **Image 18:** 18-d looks like an adult woman to me. Whether to leave her unblurred is your choice.
- **Image 15:** I could not tell about i.

Could not check: 15-i and the tiny background faces in images 23 and 53, which are too small or dark to decide.

PASS
