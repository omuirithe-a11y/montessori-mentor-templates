# 20 Oct 2026: Administration pages on the Resources template; headings 18, no line (user, 15:00), in their Word colour; Resources heading green as the template
import os
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-common.css')).read()
# the name cards: in Word they float on the right of the documentation list (wrapped tight), as in the PDF
# 22 Oct 2026: photos 2-5 are now placed beside their text by the build itself, from the PDF (the converter found them; the
# build had turned them into rows) - only the name-card drawing keeps a setting: beside the documentation list, centred on it
BESIDE = {'image1.emf': 'Contact details for parents'}

# the Resources part as the Resources template's entries (red source, blue italic title, PDF badges, description)
RES_FROM = 'Resources'

# 20 Oct 21:3x (your "fix them" and "center on the space you print"):
WORD_LIST_INDENT = 'numbered'   # numbered lists at Word's own indent; 21 Oct 14:37 (user): "fix the dash position to follow the template" - dash lists at the template's place
# 22 Oct 2026: the label column is now found from Word by the build (was ALIGN_LABELS = ['Classroom Flow', 'Order and Aesthetics', 'Materials Readiness'])
MIDDLE = ['image1.emf']   # the name-card drawing centred on the printed list beside it (user 21:15: "center on the space you print")
LABEL_COL = '9em'   # the label column (user 22:41: "Option 3 - 162 px (9em) - on the page now")
PHONE_GAPS = (41, 34)   # 20 Oct 22:0x (user): at phone width, 41 from the banner to the first letters, 34 from the last letters to the footer band
DIVIDERS_BEFORE = '0432FF'   # 20 Oct 22:1x (user): a beige line 30/30 before each blue heading, after the first (Introduction)
LIST_MARKERS = {'Guide the children': 'alpha-paren'}   # 20 Oct 23:27 (user): "change to a) b) c)" - the three lines under "How to manage the class?" (Word: i. ii. iii.)
CENTRE_ON = {'image2.JPG': 'others using the same steps'}   # 20 Oct 23:28 (user): the puzzles photo centred on this line, computer and tablet widths
TEXT_EDITS = [('How to sit; leg crossed, upright.', 'How to sit: leg crossed, upright.')]   # 20 Oct 23:34 (user): "Change: How to sit: leg crossed, upright."
RES_DIVIDERS = True   # 20 Oct 23:54 (user): "dividers between each elemnt in resources" - a beige line 30/30 between the Resources entries
LABEL_PHONE = 'own-line'   # 21 Oct 00:1x (user, phone widths): "Label on its own line" above its description
# 21 Oct (user, 5.4): "Left-align that line" - the line beside the name-card drawing at 768 (20 px word gaps); the drawing sits beside the list from 641 px, and at 1200+ the line had normal gaps
LEFT_ALIGN = {'Children’s name-cards for': '(min-width:641px) and (max-width:1199px)'}
DASH_SPACES = True   # 21 Oct 14:09 (user): "correct the dashes" - a dash Word writes against a word gets a space each side, as the page's other dashes
