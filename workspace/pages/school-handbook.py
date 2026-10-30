# 5.2 School Handbook (20 Oct 2026)
# The six pictures are pages 4-9 of the Post Oak School's table of contents: page numbers at their foot, and each
# page's last entry continues on the next. Word's file names in that order:
ROW_ORDER = [['image2.png', 'image3.png', 'image1.png', 'image4.png', 'image5.png', 'image6.png']]
# the user's note to Claude in the Word file - not page text
DROP = ['claude: check those images']
# the second half is a list of schools: built straight from Word (red regions, blue names, PDF badges)
LIST_FROM = 'Resources'
import os
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-common.css')).read() + '''
main p.mm-region{color:#EE0000;margin-top:30px !important}
main p.mm-entry{text-align:left !important}
main .mm-blue{color:#0432FF}
main a.pdf{display:inline-block;vertical-align:.12em;font-family:var(--sans,sans-serif);font-size:11px;letter-spacing:.06em;line-height:1;padding:4px 6px;border:1.5px solid #0563C1;border-radius:2px;color:#0563C1 !important;text-decoration:none;margin-left:24px}
main a.pdf:hover{background:#0563C1;color:#fff !important}'''
# 21 Oct 12:21 (user): "Check the punctuation: commas in the right place, periods after each school"
ENTRY_PERIOD = True
TEXT_EDITS = [('Pijnacker-Nootdorp. Netherlands', 'Pijnacker-Nootdorp, Netherlands')]   # user 12:21: "commas in the right place"
# 21 Oct 12:2x (user): "One column, 24 px after longest" - the PDF badges one column, 24 px after the longest school line
PDF_COLUMN = 'longest'
# 21 Oct 12:3x (user): "Make all three plain" - the bold comma after Saint-Cloud and the blue commas after Elckerlyc ... and Chantilly Montessori
PLAIN_COMMAS = True
