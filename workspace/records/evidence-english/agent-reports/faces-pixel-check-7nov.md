# Pixel check after the owner's last answer - The English Curriculum (3.5.0)

Separate agent, final pixel check after the 7 Nov answer. I had not seen this work before. No image or record was changed, except this report and pixel-check-after-answer.json. The 5 Nov check is kept as pixel-check-after-answer-5nov.md and .json. Checked 7 Nov 2026, finished 06:57 (Asia/Shanghai).

**Result: PASS.** No faults. Notes for the owner are at the end. Note 1 needs her attention: seven children's faces are left unblurred on the page because of her earlier no-blur list.

## Her answers, as recorded (review2.json)
- Round 1 (images shown whole, unblurred): "Blur all three"
- Round 2 sheet blur2/m_eng_r3/round2.html: "yes", 7 Nov 2026 06:46 (Asia/Shanghai). The sheet check (sheet-check.json) passed at 06:41:53.

## 1. The 104 earlier images are unchanged
- photos-final now holds 107 files. The backup eng35/photos-final-before-r3 holds 104.
- All 104 backup files are byte-identical (sha256) to their files in photos-final.
- No file is missing. The only new files are image99.JPG, image112.jpg and image114.JPG.
- Each new file is byte-identical to its source in blur2/m_eng_r3/images (image99.jpg, image110.jpg, image113.jpg).
- Each original in blur2/m_eng/media (image99.JPG, image110.jpg, image113.JPG) is byte-identical to the 5 Nov Word file's image99.JPG, image112.jpg and image114.JPG.
- The three files were copied in at 06:46:03, in the same minute as her answer (06:46).

## 2. The three new images
| Final image (5 Nov name) | Original | Size, final = original | EXIF turn |
|---|---|---|---|
| image99.JPG | image99.JPG | 4608 x 3456 | original 1 (none), final has no tag |
| image112.jpg | image110.jpg | 5712 x 3883 | original 1, final has no tag |
| image114.JPG | image113.JPG | 4608 x 2592 | original 1, final has no tag |

**How the masks are read.** method.py writes each mask with cv2 as [weight above 0.5, above 0.1, above 0.01] in BGR order. So in RGB order (PIL), channel 0 is the feather reach (above 0.01) and channel 2 is the core (above 0.5). Each mask is the size of its face's crop, and the crop is placed on the full image. I checked this: the channel 2 area lies inside channel 1, and channel 1 inside channel 0. For 98-b, 109-b and 112-a the mask size equals the crop size.

**Nothing changed outside the faces.**
- Area tested: every pixel outside the feather reach, grown a further 16 px for JPEG blocks. That is 15.4, 21.7 and 11.7 million pixels.
- Measure: final against the original saved again at JPEG quality 92.
  - image99.JPG: largest difference 7 levels, 99.9th percentile 1, mean 0.002
  - image112.jpg: largest 4, 99.9th percentile 0, mean 0.001
  - image114.JPG: largest 4, 99.9th percentile 0, mean 0.000
- Every pixel that differs by more than 40 levels lies inside the feather reach.
- Against the original itself, the mean difference outside the faces (1.19, 0.36, 0.21) is below the reference (the original re-encoded at 92 then 95: 1.34, 0.51, 0.30).
- Verdict: outside the blurred faces, the images are only re-encoded.

**Blurred faces.** Fine detail (Laplacian energy) inside the core, final against original:
- 98-b: 0.108
- 109-b: 0.105
- 112-a: 0.145

All three are within the 5 Nov range for blurred faces (median 0.069, largest 0.383).

**By eye at full size, original beside final:**
- **98-b** (boy cutting, looking down): the lash line, nose, nostril, mouth and the small mark on the cheek are gone. Only soft skin tone is left under the hair.
- **109-b** (girl colouring, face turned down): the eyelid, lashes, nose and lip line are gone. The ear and hair outside the face stay sharp.
- **112-a** (girl with her chin on her hand): the eye, nose and mouth area is soft skin with no lines.

No sharp eye, lash line, nostril or mouth line is left in any of the three.

**Faces left.** 98-a (the 8 px printed picture on the shelf) and 109-a (the hand holding a pencil) both lie wholly outside any feather. Both match the q92 re-encode exactly (largest difference 0), with fine detail 1.07 and 1.05 of the original. They are unchanged.

**Rest of the three images.** In image112.jpg, the child lying on the floor at the back shows only the back of the head. In image99.JPG and image114.JPG there are no other children. The adult's head in image112.jpg is out of frame.

## 3. Images the page uses without blurring (the new part)
The 5 Nov Word media folder holds 169 files and photos-final holds 107, which leaves 62:
- **3 .wdp files.** hdphoto1, 2 and 3 are Word's unedited layers under a brightness change on image7.png, image62.png and image66.png (document.xml a14:imgLayer). The page uses the rendered image, not these layers. They are JPEG XR, which I cannot open here, so I did not look at them (see note 4).
- **59 images.** I looked at every one whole on viewing sheets (about 750 px each), then at full size wherever a child's head shows.

| Image (5 Nov name) | What it shows | Result |
|---|---|---|
| image1.JPG, image2.JPG, image4.JPG, image48.JPG | classroom shelves, sandpaper letters | no person |
| image3.gif, image97.gif, image6.png | line strips (623 x 2, 1091 x 8) | no picture |
| image9.JPG | girl reading, book over her face | face covered (looked at full size) |
| image11.jpg | boy in a bean bag, book over his face | only forehead and fringe above the book (full size) |
| image12.JPG | child reading, book over the face | only the top of the head (full size) |
| image13.jpg, image46.jpg, image47.jpg, image56.jpeg, image86.jpg, image98.jpg, image103.jpg, image115.jpg, image128.JPG, image138.jpg, image139.jpg, image140.jpeg, image141.jpeg, image144.png, image147.jpg, image148.jpg, image149.jpg, image156.jpg, image157.jpg, image158.jpg, image159.jpg, image166.png | objects, cards, word lists, materials, shelves, a child's writing | no person |
| image160.jpg - image165.jpg | pictograms (drawings) | drawings only |
| image18.jpg | girl at a table, seen from behind | back of head, ear (full size) |
| image44.jpeg | boy pointing at the wall, from behind | back of head (enlarged) |
| image49.jpg | man (adult) and a girl from behind | girl: back of head and ear (full size). Man: adult |
| image53.jpg, image155.jpg | historical images (Montessori) | left by rule |
| image62.png | picture cards on a mat | printed pictures |
| image87.JPG | boy at an easel from behind, two children behind | **two children's faces show: 87-a (boy at left, eyes and mouth, smiling) and 87-b (child behind the easel)**. Both are left by her earlier no-blur list (note 1) |
| image88.JPG, image89.jpg, image118.JPG | girls at easels from behind | back of head, ear, mask strap (full size) |
| image90.JPG | girl at an easel, turned away to the window | back and side of head. The cheek line shows, but no eye, nose or mouth (full size, note 2) |
| image92.JPG | boy at an easel, side-on from behind | **lashes and nose tip show (92-a)**, left by her earlier no-blur list (note 1) |
| image104.jpg | boy pinning at a board | **profile (103-b)**, left by her earlier no-blur list. The printed photo on the board (103-a) is left by rule |
| image107.JPG | girl tracing, looking down | **face looking down (106-a)**, left by her earlier no-blur list |
| image111.jpg | two children holding drawings over their faces | **left child: one eye and mouth show (113-a)**, left by her earlier no-blur list. Right girl: face covered by the paper (full size) |
| image113.JPG | two girls from straight above | tops of heads only (full size) |
| image121.JPG | child's writing with a name card | small printed photo of a child (115-a), left by rule |
| image133.jpeg | boy writing, from behind | back of head (enlarged) |
| image134.jpeg | girl at a shelf | **small profile (132-a, 23 px)**, left by her earlier no-blur list |
| image150.jpg | picture cards on a table | printed pictures (one shows children) |
| image151.jpg | small books, printed photos pinned behind | printed images (150-a to f), left by rule |

**Result:** no child's face is unblurred unless it is lettered in faces.json and left by her earlier no-blur list. No face was found that the face finders and the records missed.

## 4. The 104 earlier blurred images
- I looked at all 104 whole on viewing sheets (6 to a sheet).
- I enlarged the places where a face could be missed beside the blurred ones: image131.jpeg (girl with glasses, looking down: blurred, hair over), image93.jpg (boy at an easel: blurred profile), image79.JPG (boy bending: blurred), image64.JPG (girl looking down: hair and blurred profile), image153.jpg (girl in front: only a soft cheek edge, no eye, nose or mouth) and image43.jpeg (small, both children blurred).
- Result: no missed child's face. This agrees with the 5 Nov check, which also ran a second face finder on these 104. They are byte-identical to what it checked.

## Notes for the owner (not faults by her recorded answers)
1. **Seven children's faces stay unblurred on the page because of the earlier no-blur list** (blur2/m_eng/faces/keep_unblurred.json, recorded as "left unblurred by your answer"). They are:
   - image87.JPG: 87-a and 87-b, two children behind the easel; the boy at left shows his eyes and smile
   - image92.JPG: 92-a, boy side-on, lashes and nose
   - image104.jpg: 103-b, boy in profile
   - image107.JPG: 106-a, girl looking down
   - image111.jpg: 113-a, child with one eye and mouth showing
   - image134.jpeg: 132-a, small profile

   The 5 Nov check and the 6 Nov review both named these. They go against the rule "all photos of children are blurred", so please say if any should now be blurred.
2. **image90.JPG:** the girl is turned away. Only the line of her cheek shows, with no eye, nose or mouth, so she is left like a back of head.
3. **Reading the masks:** the 5 Nov report's order (0.5, 0.1, 0.01) is cv2's BGR order. Read in RGB the order is reversed. Later checkers should read channel 0 in PIL as the feather reach.
4. **Word file layers:** the Word file still holds hdphoto1.wdp and hdphoto3.wdp, which are Word's unbrightened copies under image7.png and image66.png. Those two are blurred on the page, but these copies probably are not. The page does not use these files. If the Word file itself is ever shared, those layers may hold unblurred faces.

## 5. Added 7 Nov 2026 08:03 (Asia/Shanghai): images used unblurred, listed by sha256
A separate agent, new to this work, checked again for the builder's new rule (the json must list, by sha256, every image the page uses unblurred).

- **The set, confirmed.** The build log b42.log names 163 Word media files used by the page. 107 have a file in photos-final. That leaves **56 images used unblurred**. The earlier 59 included the three line strips image3.gif, image97.gif and image6.png; b42 does not use them as images, so they are not in the list. The .wdp files are not used.
- **The bytes.** The sha256 of each of the 56 was taken from word/media in /home/claude/eng35/src/3.5.0 The English Curriculum.docx. They are the same bytes as in b42/work/source.docx and in eng35/newmedia.
- **Looked at again.** I looked at all 56 whole on new viewing sheets, turned as EXIF says. I then looked at full size (or enlarged, for the small ones) every image where a child's head shows: image9, 11, 12, 18, 44, 49, 87, 88, 89, 90, 92, 104, 107, 111, 113, 118, 121, 133, 134, 150 and 151.
- **Result: PASS. No new fault.** No child's face shows unblurred except the seven left by her own 5 Nov answer (keep_unblurred.json), which are her choice:
  - image87.JPG: 87-a and 87-b
  - image92.JPG: 92-a
  - image104.jpg: 103-b
  - image107.JPG: 106-a
  - image111.jpg: 113-a
  - image134.jpeg: 132-a

  Everything else is one of these: a back of head, a face covered by a book or paper, the top of a head seen from above, an adult (image49), a historical image (image53, image155), printed pictures (image121, image150, image151, image62) or drawings.
- **The json.** The old json is kept as pixel-check-after-answer-0657.json. pixel-check-after-answer.json is the same, plus "unblurred_looked_at" (56 entries: name, sha256, what was seen) and "unblurred_time". "pass" stays true.
