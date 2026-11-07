# Separate check v1 of the round 3 faces sheet, The English Curriculum (3.5.0), 7 Nov 2026

Checker: a separate agent that had not seen this work. Method: BLUR-METHOD-26-oct.md version 22, items 20-23 (with section K items 29-39), adapted to this round. I did not have the Projects tool, so I read the method from the summary in /home/claude/mm/records/START-HERE-6nov.md ("## Faces") and the docstrings and code of method.py, method_sheet.py and method_check.py. I changed no image, mask, tool, faces.json or sheet.

Sheet: /home/claude/mm/blur2/m_eng_r3/round2.html, 522,130 bytes, sha256 95eb72ce8488a6876ccdcaa6128858fc4ad879ed50b9a1035f008ab7548790cf (as given), "Made 07 Nov 2026 06:36:40", NOT CHECKED banner on.

Her answer (7 Nov, word for word): "Blur all three" (page images 098, 110, 109).

## Which image is which - confirmed
I compared the page images in /home/claude/mm/build-35/b41/images/ with the full-size originals in /home/claude/mm/blur2/m_eng/media/, by correlation and by eye:
- page 098.jpg = image99.JPG (set 98). Correlation 1.00, same framing.
- page 110.jpg = image110.jpg (set 109). The page image is a tall crop of it: the girl drawing, with the adult at the left.
- page 109.jpg = image113.JPG (set 112). The page image is a crop of it: the girl leaning on her hands.

Names: m_eng/media uses the 4 Nov Word names. In the current 5 Nov Word file (/home/claude/eng35/src/new-to-old-media.json, checked by sha256) these three are image99.JPG, image112.jpg and image114.JPG. See "Before the swap" below.

## 1. Statuses - PASS
m_eng_r3/faces.json holds exactly the three images and five faces:
- 98-a: yunet, box [862.3, 44.5, 871.1, 55.7], left by rule, reason "a printed picture on the shelf at the back (8 px), not a person". This matches by_rule.json and keep_unblurred.json.
- 98-b: blurred, src "hand", box [470, 420, 730, 590] x 2.88 = full_box [1353.6, 1209.6, 2102.4, 1699.2]. This is the same box as extra_faces.json "98".
- 109-a: yunet, box [604.4, 531.7, 711.9, 689.2], left by rule, reason "a hand holding a pencil, not a face". This matches by_rule.json and keep_unblurred.json.
- 109-b: blurred, src "hand", box [755, 400, 925, 510] x 3.57 = full_box [2695.3, 1428.0, 3302.2, 1820.7]. This is the same box as extra_faces.json "109".
- 112-a: blurred, src "retinaface second pass (0.86)", box [858, 328, 1024, 440] x 2.88. This is the same box as rf.json image113.JPG (score 0.859) and as candidates_ok "112@858,328".
- detections.json has 98-a and 109-a only, and nothing on 112. Nothing else is listed and no face is undecided.

## 2. Unchanged images - PASS
- The owner's earlier final images in /home/claude/mm/build-35/faces/photos-final/ are not touched. photos-final.json lists no hashes, so I checked the file times. No file in /home/claude/mm/build-35/faces/ is newer than 5 Nov 10:34; the folder's 104 images date from 5 Nov 10:05. None of the three images has a file there yet: photos-final.json says "no face to blur - the original is used as it is" for all three.
- On the three result images, nothing changed beyond each area's reach. I re-ran `method_check.py sets/eng-r3.json m_eng_r3/round2.html` and got fails [] and reports []. It counts changed_pixels_beyond_reach 0 on images 98, 109 and 112, and the left faces 98-a and 109-a have a changed share of 0.000 in their boxes. The re-run rewrote check-measure.json with the same content (sha256 unchanged); only the file time changed, to 06:38.
- I also measured this my own way, comparing each result with a q92 recompression of its original, outside every saved mask (any channel above 0):
  - image 99: largest difference 7 levels on 1 pixel, 99.99th percentile 3;
  - image 110: largest difference 4 levels;
  - image 113: largest difference 4 levels, and at most 2 levels beyond a 16 px band.
  These are JPEG noise, not blur.

## 3. Changed images - PASS
Each blurred face changed inside its area (item 21, method_check). The saved masks, placed at their crop offsets, give these measured areas in full-image pixels:

| face | changed share inside area | feather reach | 50% line (x; y) | 10% line (x; y) |
|---|---|---|---|---|
| 98-b | 0.928 | 0.112 w | x 1471-2176; y 1128-1787 | x 1412-2238; y 1064-1849 |
| 109-b | 0.825 | 0.134 w | x 2589-3346; y 1347-1920 | x 2536-3397; y 1293-1969 |
| 112-a | 0.825 | 0.126 w | x 2436-2970; y 978-1336 | x 2393-3012; y 938-1375 |

All are at or under the 0.3 w reach limit.

## 4. By eye - PASS
I looked at each blurred face at full size, the original with the 50% line drawn beside the result, then at the result at 1:1:
- 98-b (boy cutting, looking down): the lash line, the nose tip, the open mouth and the cheek are all inside the area and smoothly blurred. The hair over the eyes is softened inside the area and sharp outside it. No sharp eye, lid, nostril or mouth line remains. The edge is soft. The collar and hand are untouched beyond the feather.
- 109-b (girl drawing, head bowed): the lowered lash line, the nose, the mouth and the chin are inside the area and blurred. The ear is outside and sharp, which is right because it is not a face feature. No sharp feature remains, and the edge is soft.
- 112-a (girl leaning on her hands): the face between the hands (eyes under the fringe, nose, mouth) is inside the area and blurred. The hands and the hair outside it are sharp. No sharp feature remains, and the edge is soft. The RetinaFace mouth points lie above its nose point (a bowed face), but the area still covers the whole visible face.

I also looked at each whole image for any other child's face:
- image99: no other person. The shelf at the back has printed pictures and figures (98-a), which are not people.
- image110: the adult at the left shows only her back. A child lies face down on the mat at the top right; I enlarged this at full size (x 4000-5712, y 400-1450): only the back of the head, the hair, the yellow top and the striped trousers show, with no face.
- image113: behind the chair at the top there is a seated person in a white top, cut off at the frame edge, with no head showing (enlarged at x 1100-2900, y 0-700).

No missed face.

## 5. Sheet contents - PASS
- Counts: 3 images, 3 faces blurred, 2 faces left, 0 images left off. These match faces.json. The "Faces without a mesh, 3" list (98-b, 109-b, 112-a) is right. "Adjusted by hand after a separate check, 0" and "could not decide: none" are both right.
- Embedded images: 6 (3 whole renders + 3 face crops), each byte-identical to m_eng_r3/whole-sheet/ or m_eng_r3/crops/ (item 20). As the tool intends, the whole renders show the originals with the red 50% lines (method.py draws on the original). Each crop shows the original with a white outline beside the result.
- Her words: the title says "your answer 7 Nov: Blur all three", which is her words exactly. No other words are given as hers. The other uses of "your" are the method's standing lines: "your answers are [kept]", "Faces where your 25 Oct answer was applied, 0: none" and "Faces I adjusted by hand ... (not your answers)". None of them gives words as hers.
- "photo" appears 0 times.

## Notes for the maker (not fails)
1. Numbering on the sheet: the title uses page numbers (images 098, 110, 109), but the body headings use set numbers. The body's "Image 109" is page image 110, and page image 109 appears as "Image 112". The owner could be confused. It would help to add the page number to each heading, for example "Image 109 (page image 110)".
2. File names in brackets are the 4 Nov Word names. In the current 5 Nov Word file, "image110.jpg" and "image113.JPG" are different images. The current names of these three are image99.JPG, image112.jpg and image114.JPG.
3. Small slip: 98-a is shown as "9 px wide" but its reason says "(8 px)" (8.8 px, rounded two ways).

## Before the swap (warning)
When the three results go into /home/claude/mm/build-35/faces/photos-final/:
- They must take the 5 Nov names: image99.jpg -> image99.JPG, image110.jpg -> image112.jpg, image113.jpg -> image114.JPG.
- photos-final/image110.jpg already exists and is a different, blurred image (old image109.jpg). It must not be overwritten.
- photos-final.json uses the 4 Nov names (image99.JPG, image110.jpg, image113.JPG) for these three entries.

## Could not check
- I could not read the method's full text from the Project, because I did not have the Projects tool. I used the START-HERE summary and the tool code.

PASS
