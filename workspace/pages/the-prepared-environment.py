# 2.2.0 The Prepared Environment - settings (24 Oct 2026)
# User 24 Oct 11:59: "Build 2.2.0 The Prepared Environment from the updated Essay Code Template" (GitHub d33a6f5).
# Hero: the 2.2 hero decided 18 Oct (Drive prepared-environment-hero.jpg, three children's faces already blurred), centred.
# Faces: round 1 sheet sent for the user's answer; the page is built from the blurred copies only after round 2.

# 24 Oct 2026: at phone width the wide image beside "Trillium Montessori" (image151, 2.14 times as wide as tall) stood
# 386px wide at 180 high and pushed the page 20px wider than a 390 screen - on phones an image beside text is never
# wider than the text column (its height follows)
CSS = """
@media (max-width:640px){html body main .mm-float .pim{max-width:100% !important;height:auto !important}html body main .mm-float .pim img{width:100% !important;height:auto !important}}
"""

# 24 Oct 2026 13:47 (user, on the typo list): keep "Molère!"; "Nienhuis"; "25+"; edit 182 and 363 as given ("some string, a marker
# and two colleague or a pair of 5-year-olds." - 14:48: "change it to 'two colleagues'" and "... is that … it's only used for one activity"); "All other suggested edits are accurate"
TEXT_EDITS = [
 ('needs at children each stage', 'needs of children at each stage'),
 ('wonderfully simply to find', 'wonderfully simple to find'),
 ('which I confess cause this', 'which I confess caused this'),
 ('distinctly bigger than other (Japan', 'distinctly bigger than others (Japan'),
 ('if all the shelves are all the same length', 'if all the shelves are the same length'),
 ('arranged in a square, The larger tables', 'arranged in a square. The larger tables'),
 ('the long chains in a the hall', 'the long chains in the hall'),
 ('the line should in the shape', 'the line should be in the shape'),
 ('some string, a marker and some.', 'some string, a marker and two colleagues or a pair of 5-year-olds.'),
 ('fall of their head', 'fall on their head'),
 ('is that that it reinforces', 'is that it reinforces'),
 ('25+ plus children', '25+ children'),
 ('…’For me', '…’ For me'),
 ('by a centra wall', 'by a central wall'),
 ("so i’'s important", 'so it’s important'),
 ('which was idea for hanging', 'which was ideal for hanging'),
 ('they’re not much you can do', 'there’s not much you can do'),
 ('a sign form the universe', 'a sign from the universe'),
 ('a lot with a clam attached', 'a lot with a clamp attached'),
 ('about a matre high', 'about a metre high'),
 ('believed that that a child', 'believed that a child'),
 ('if there’s windows', 'if there are windows'),
 ('is that … it’s that’s only used', 'is that … it’s only used'),
 ('a left they found in the park', 'a leaf they found in the park'),
 ('what ppictures there are', 'what pictures there are'),
 ('Children’s Houses”represent', 'Children’s Houses” represent'),
 ('for the guides personal items', 'for the guide’s personal items'),
 ('there was jumble of odds', 'there was a jumble of odds'),
]
# The three edits below touch a link or a quotation's marks, so they are made on the page code (one match each)
PAGE_CODE_REPLACE = [
 ('target="_blank">nienhuis</a> mat', 'target="_blank">Nienhuis</a> mat'),
 ('<p>"\'The central and main room', '<p>"The central and main room'),
 ('<em>The Discovery of the Child</em>. P.46. (1909)', '<em>The Discovery of the Child</em>. p. 46. (1909)'),
 ('var a=lastBase(el),b=firstTop(el);if(a===null||b===null)return;', 'var a=lastBase(el),b=firstTop(el);if(a===null||b===null)return;if(imgBetween(el,a,b))return;'),   # 25 Oct 2026: a line with an image row between it and the text above keeps its own spacing (the measure from the text above the images pulled 22 sections up over the images)
 ('function tgt(el){', "function imgBetween(el,a,b){var r=false;[].forEach.call(document.querySelectorAll('main img'),function(i){if(r||el.contains(i)||!(el.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_PRECEDING))return;var q=(i.closest('.pim')||i).getBoundingClientRect();if(q.height>2&&q.top>=a-1)r=true;});return r;}\n  function tgt(el){"),
 ('<script id="mm-letter-gaps-js">', '<script id="mm-float-clear-js">/* 25 Oct 2026: a photo beside a short paragraph, centred on it, never climbs over a line of the text above it (at 900 the last line of the list above ran under the photo) */\n(function(){function run(){[].forEach.call(document.querySelectorAll(\'main .mm-float\'),function(f){if(getComputedStyle(f).float===\'none\')return;var pim=f.querySelector(\'.pim\');if(!pim)return;\n  for(var k=0;k<3;k++){var r=pim.getBoundingClientRect(),low=null,pv=f.previousElementSibling;\n    for(var j=0;pv&&j<3;j++,pv=pv.previousElementSibling){if(pv.classList.contains(\'mm-fspacer\'))continue;var w=document.createTreeWalker(pv,NodeFilter.SHOW_TEXT),n;while((n=w.nextNode())){if(!n.nodeValue.trim())continue;var g=document.createRange();g.selectNodeContents(n);[].forEach.call(g.getClientRects(),function(q){if(q.width>1&&q.right>r.left+1&&q.left<r.right-1&&q.bottom>r.top+3&&q.top<r.bottom-3)low=low===null?q.bottom:Math.max(low,q.bottom);});}}\n    if(low===null)break;var mt=parseFloat(getComputedStyle(f).marginTop)||0;f.style.setProperty(\'margin-top\',(mt+low-r.top+2).toFixed(2)+\'px\',\'important\');}});\n  if(window.__mmKeepSize)window.__mmKeepSize();}\n  var pl=window.__mmAfterLayout;window.__mmAfterLayout=function(){if(pl)pl();run();};})();\n</script>\n<script id="mm-letter-gaps-js">'),   # 25 Oct 2026: page check - a photo centred beside a short paragraph overlapped the last line of the list above it at 900
 ('<cite><span class="mm-t">\u2409</span>- Maria Montessori, <em>The Advanced', '<cite>- Maria Montessori, <em>The Advanced'),   # 25 Oct 2026: page check - attributions start alike (no tab before or after the dash); 26 Oct: the tab is U+2409 at this stage (it was written as \t and never matched)
 ('<cite><span class="mm-t">\u2409</span>- Maria Montessori, <em>The Absorbent Mind,</em> p. 89.', '<cite>- Maria Montessori, <em>The Absorbent Mind,</em> p. 89.'),   # 25 Oct 2026: page check - attributions start alike (no tab before or after the dash)
 ('<cite><span class="mm-t">\u2409</span>- Maria Montessori, <em>The 1946', '<cite>- Maria Montessori, <em>The 1946'),   # 25 Oct 2026: page check - attributions start alike (no tab before or after the dash)
 ('<cite>-<span class="mm-t">\xa0\xa0\xa0</span>Maria Montessori,<em> The Discovery', '<cite>- Maria Montessori,<em> The Discovery'),   # 25 Oct 2026: page check - attributions start alike (no tab before or after the dash)
 ('<th>Dimensions of Chairs', '<th colspan="4">Dimensions of Chairs'),   # 25 Oct 2026: page check - the title spans all 4 columns, as in Word (gridSpan=4)
# 26 Oct 2026: the mm-quote-tab-25oct style is now in the Essay template (GitHub change 6, 6acd357) - the page's own copy is dropped (it was on the page twice)
 # 26 Oct 2026 (2.2.0 page check): the Peller source line is a dash list item in Word, like the other attributions - shown as its quotation's attribution
 ('</p></blockquote><ul><li>Peller, Lili.', '</p><cite>- Peller, Lili.'),
 (' pg. 21</li></ul>', ' pg. 21</cite></blockquote>'),
 # 26 Oct 2026 (2.2.0 page check): level-10 rows fit the text column (see the script's note)
 ('</body>', '<script id="mm-row-fit-26oct">/* 26 Oct 2026 (2.2.0 page check): the template\'s 19.2px gap for level-10 image rows never pushes a row past the text - where it would (1024: 14px each side), the gap is what fits (set as --mm-fit, which the template\'s row script does not clear) */(function(){function fit(){document.querySelectorAll(\'main .mm-row[data-level="10"]\').forEach(function(r){var f=r.querySelectorAll(\'figure\');if(innerWidth<=830||f.length<2){r.style.removeProperty(\'--mm-fit\');return;}var s=0;f.forEach(function(x){s+=x.getBoundingClientRect().width;});r.style.setProperty(\'--mm-fit\',Math.max(0,Math.min(19.2,(r.clientWidth-s)/(f.length-1))).toFixed(2)+\'px\');});}addEventListener(\'load\',function(){[300,1500,4000].forEach(function(t){setTimeout(fit,t);});});addEventListener(\'resize\',function(){clearTimeout(fit.t);fit.t=setTimeout(fit,800);});})();</script><style id="mm-row-fit-26oct-css">html body main .mm-row[data-level="10"][style*="--mm-fit"]{gap:var(--mm-fit) !important}</style></body>'),
]

# 24 Oct 2026 16:15 (user): "correct the prepared environment so it uses following numbers" - hero 40, site name 25, menu bar 20,
# menu panels 18, "Table of contents" heading 20, contents entries 18, section / green / blue and red Word headings 18,
# sub-headings 18, body text 18, lists 18, quotations 18, quotation attribution 18, image captions 15, footer quotation 18,
# copyright line and "Back to top" 15. 16:2x (user, the menu bar did not fit at 20 between 961 and 1179): "18 everywhere".
# Phones (21 Oct rule: "transfer them across to phones but using numbers that work on phones and are consistent with how other
# pages on this site worked"): the site's own phone step - 18 -> 17, 20 -> 19, 25 -> 21, 40 -> 28; 15 stays 15.
CSS += """
@media (min-width:641px){
html body .hero h1{font-size:40px !important}
html body .site-name{font-size:25px !important}
html body .menu .top{font-size:18px !important}
html body .grp a,html body .grp .np,html body .grp .hd span{font-size:18px !important}
html body .toc-wrap .toc-label,html body .toc .toc-label,html body .toc-label{font-size:20px !important}
html body .toc a{font-size:18px !important}
html body main h2,html body main .section h2,html body main h2.mm-sub,html body main h2[class*="mm-hc-"],html body main h3{font-size:18px !important}
html body main p:not(.mm-gl),html body main li{font-size:18px !important}
html body main blockquote:not(#mmz),html body main blockquote:not(#mmz) p,html body main blockquote:not(#mmz) cite{font-size:18px !important}
html body main figcaption,html body main .mm-cap{font-size:15px !important}
html body .mc-band p,html body .mc-band p.mc-by{font-size:18px !important}
html body .site-foot-in,html body .site-foot-in a,html body .site-foot-in span{font-size:15px !important}
}
"""
CSS += """
@media (max-width:640px){
html body .hero h1{font-size:28px !important}
html body .site-name{font-size:21px !important}
html body .menu .top{font-size:17px !important}   /* 25 Oct 2026: your phone number for the menu bar (17); the template had 18 */
html body .grp a,html body .grp .np,html body .grp .hd span{font-size:17px !important}
html body .toc-wrap .toc-label,html body .toc .toc-label,html body .toc-label{font-size:19px !important}
html body .toc a{font-size:17px !important}
html body main h2,html body main .section h2,html body main h2.mm-sub,html body main h2[class*="mm-hc-"],html body main h3{font-size:17px !important}
html body main h2[class*="mm-hc-"][class]{font-size:17px !important}   /* 24 Oct: beats the Word-colour heading rules (18), which come later */
html body main p:not(.mm-gl),html body main li{font-size:17px !important}
html body main blockquote:not(#mmz),html body main blockquote:not(#mmz) p,html body main blockquote:not(#mmz) cite{font-size:17px !important}
html body main figcaption,html body main .mm-cap{font-size:15px !important}
html body .mc-band p,html body .mc-band p.mc-by{font-size:17px !important}
html body .site-foot-in,html body .site-foot-in a,html body .site-foot-in span{font-size:15px !important}
}
"""
# 24 Oct 2026: with the menu bar at 18 the eight menu words did not fit between 961 and 1099px (the page scrolled sideways by up to
# 52px) - there the header's side padding is 16 (was 24), the space between menu items 2px (was 7-10) and each arrow 13px wide (was 16)
CSS += """
@media (min-width:961px) and (max-width:1099px){html body .site-head-in{padding-left:16px !important;padding-right:16px !important}html body .menu{gap:2px !important}html body .menu .sub-toggle{width:13px !important;min-width:13px !important;padding:0 !important;margin-left:1px !important}}
"""

# 24 Oct 2026: a description for every image (site rule of 21 Oct), written by looking at each image
ALT_TEXT = {
    'image1.jpeg': "A yellow building with shuttered windows and the words 'Casa dei Bambini' and 'Maria Montessori' on its wall",
    'image2.JPG': 'Children working on mats and at tables in a bright, spacious classroom with a wooden floor',
    'image3.jpg': 'Children in aprons wiping a long wooden table in a classroom lined with low shelves',
    'image4.JPG': 'A small L-shaped wooden shelf with a mirror, jars, a plant and a dustpan against a pink wall',
    'image5.jpeg': 'Children in green smocks working on mats inside a blue line on the classroom floor',
    'image6.JPG': 'A long, bright classroom with low shelves, plants and a blue ellipse on the floor',
    'image7.JPG': "A row of low wooden language shelves beneath children's drawings and a print of The Starry Night",
    'image8.JPG': 'Children working on the floor and at small tables in a large classroom full of shelves',
    'image9.jpeg': 'A small hand-washing table with a wooden basin, a jug and towels',
    'image10.jpg': 'Adjustable wall shelves holding wooden boxes, cabinets, trays and jars of materials',
    'image11.JPG': 'A wooden shelf of metal insets and coloured pencils below a row of sandpaper letters',
    'image12.jpg': 'White adjustable shelves holding practical life trays, a green watering can and jugs',
    'image13.jpg': 'White shelves of language materials in boxes and baskets beside a small white table',
    'image14.JPG': 'A boy carrying the Red Rods in their wooden stand across a classroom',
    'image15.png': "A low view beneath a table of two children's legs and shoes on blue chairs",
    'image16.jpg': 'A small boy sitting on a blue chair in a classroom with a grey carpet',
    'image17.jpg': 'Boys sitting on small wooden chairs in a row in a classroom',
    'image18.JPG': 'A boy sitting at a small white table, working on a tray',
    'image19.png': 'A woman working on a laptop at a table while a girl sits on the floor underneath it',
    'image20.jpg': 'A row of children sitting along a brick wall, some of them underneath a small wooden table',
    'image21.png': 'A boy at a table placing red cylinders in a green Knobbed Cylinder Block',
    'image22.png': 'A man in a shirt and tie bending over a table where children build with pink and brown blocks',
    'image23.jpg': 'A long chart of numbers and a strip of coloured number labels lying on a table',
    'image24.png': 'A boy standing at a small table by a window, working with a chart and papers',
    'image25.png': 'Three children standing around a table holding four Knobbed Cylinder Blocks',
    'image26.png': 'Two girls on a mat laying out wooden number boards in a long line',
    'image27.png': 'A boy on a long mat working with image cards beside a two-hemisphere globe map',
    'image28.png': 'Three floor mats of different sizes with red and blue rods laid along their edges',
    'image29.png': 'A toddler sitting beside a mat covered with yellow and blue geometric inset trays',
    'image30.png': 'A girl on a rug laying out rows of coloured tablets in shades of blue, brown and grey',
    'image31.JPG': 'Children rolling up dark mats in a row on a classroom floor',
    'image32.JPG': 'Two boys kneeling behind colour tablets arranged in a sunburst around a wooden circle',
    'image33.jpg': 'A boy kneeling behind long bead chains laid out on a patterned rug',
    'image34.JPG': 'A girl and a boy rolling up striped cloth mats in front of wooden shelves',
    'image35.JPG': 'A girl arranging coloured triangles on a black mat',
    'image36.JPG': 'A child in a woolly hat and high-visibility vest standing inside a large wicker basket outdoors',
    'image37.png': 'A catalogue page showing rows of woven baskets in different shapes and sizes',
    'image38.jpg': 'Rolled cloth mats standing in a blue woven basket and against a wall',
    'image39.jpg': 'Rolled beige mats standing in a lined wicker basket in a classroom',
    'image40.JPG': 'Folded cream mats stacked inside a wooden box stand on a grey floor',
    'image41.jpg': 'A wooden stand holding rolled mats in slots beside a basket of dark mats',
    'image42.JPG': 'Laughing children holding up a blue mat while one beats it with a wicker carpet beater',
    'image43.jpg': 'Three girls shaking out a mat on a lawn, seen through a classroom window',
    'image44.JPG': 'Smiling girls holding up a black mat while one beats it with a carpet beater',
    'image45.JPG': 'Two girls holding up a blue mat while a younger girl beats it with a carpet beater',
    'image46.jpg': 'A sunlit classroom with low shelves where a teacher and children work on the floor',
    'image47.png': 'An empty classroom with tall windows, small tables and chairs and low shelves along the walls',
    'image48.JPG': 'An empty classroom with a dark wooden floor, small tables and rows of low shelves',
    'image49.jpg': 'Children working at tables in a sunny classroom with long windows and low shelves',
    'image50.png': 'An empty room with grey flooring, a few small tables and stacked cardboard boxes',
    'image51.png': 'An empty room with small tables, cardboard boxes and white flat-packed furniture',
    'image52.png': 'A bare corner of a room with blue and green walls and a grey wooden floor',
    'image53.png': 'An empty room with small wooden chairs and tables stacked together and boxes waiting to be unpacked',
    'image54.png': 'A newly arranged classroom with low wooden shelves, small tables and a plant against a blue wall',
    'image55.png': 'A prepared classroom with low wooden shelves, small tables and tall potted plants',
    'image56.png': 'A prepared classroom with globes and maps on a central shelf and plants on top',
    'image57.png': 'A prepared classroom with a blue ellipse on the floor and shelves around the walls',
    'image58.png': 'A large room with concrete walls and a wooden floor, its shelves still mostly empty',
    'image59.png': 'A woman standing in a large, nearly empty room with a red line taped on the floor',
    'image60.png': 'A large classroom with concrete walls, filled shelves and children at work',
    'image61.png': 'A spacious room with a wooden floor, tables, a green tape line and a colourful display board',
    'image62.jpg': 'Children laying out a long bead chain on a white mat running the length of a classroom',
    'image63.jpg': 'A long black mat with a bead chain stretched across a classroom while children work nearby',
    'image64.jpg': 'A long bead chain laid out on an orange mat along a brick-walled corridor',
    'image65.jpg': 'A smiling boy sitting beside a long bead chain on a grey mat in a corridor',
    'image66.jpg': 'A long black mat laid diagonally across an empty classroom floor',
    'image67.JPG': 'A long grey mat with a bead chain stretching down a classroom with a dark wooden floor',
    'image68.png': 'A teacher and children sitting around a blue ellipse on the floor with a tray of plants in the middle',
    'image69.JPG': 'Children working with image cards on red and blue mats inside a red ellipse',
    'image70.png': 'Children and teachers holding hands in a circle on a line on the classroom floor',
    'image71.png': 'Children walking around a yellow ellipse holding bells, with cards laid out on mats in the middle',
    'image72.png': 'A large classroom with white shelves, tables and a Pink Tower, seen from above',
    'image73.jpg': 'A bright classroom with white tables, wooden chairs and low shelves under large windows',
    'image74.png': 'A bright classroom with a cloth-covered round table, a painted cabinet and low shelves',
    'image75.png': 'A spacious classroom with small tables, white shelves and pink flowers in the foreground',
    'image76.jpg': "Rows of children's low beds with colourful bedding laid out between classroom shelves",
    'image77.jpg': 'Girls setting up green folding cots for nap time while a child lies under a blanket',
    'image78.jpg': 'A girl and a teacher carrying a low bed across a classroom while children watch',
    'image79.jpg': 'A classroom with low beds made up among the tables, shelves and a small animal cage',
    'image80.JPG': 'A boy and a girl sitting at a long wooden table beside a window with green curtains',
    'image81.JPG': 'Two children arranging flowers on a long line of wooden tables beside shelves',
    'image82.jpg': 'Two young children carrying a small wooden table across a classroom',
    'image83.JPG': 'Two children carrying a wooden table in a classroom with a bead cabinet by the window',
    'image84.JPG': 'A mathematics shelf with Golden Beads, number cards and bead materials laid out in order',
    'image85.jpeg': 'A mathematics shelf with red and blue Number Rods along the top and Spindle Boxes below',
    'image86.jpg': 'A cream metal trolley holding trays of golden bead hundreds and thousands',
    'image87.jpg': 'A girl taking letters from a Large Moveable Alphabet beside a table with words laid out on red tape lines',
    'image88.JPG': 'A stationery shelf with labelled wooden drawers, baskets and a blue glass vase',
    'image89.JPG': 'A language shelf with plastic stationery drawers, coloured paper and pencils',
    'image90.JPG': 'A long row of language shelves beneath a line of Sandpaper Letters on a narrow wall rim',
    'image91.jpg': 'A child sitting on the floor drawing at a wooden easel beside a window',
    'image92.png': 'A girl standing on a step stool to draw on paper at an easel',
    'image93.jpg': 'A girl in a red apron painting with blue paint at an easel',
    'image94.png': 'A kneeling girl drawing lines on a paper roll at a wooden easel',
    'image95.JPG': 'A girl in an apron drawing at a tall easel in front of a window',
    'image96.JPG': 'A small boy on a step stool drawing with chalk on an easel blackboard',
    'image97.jpg': 'A small boy reaching up to the top shelf where the Geometric Cabinet trays are kept',
    'image98.JPG': 'A boy sitting on the floor pulling out a drawer of blue Geometric Cabinet insets',
    'image99.jpeg': 'A low wooden shelf holding the Geometric Cabinet, cards and geometric solids',
    'image100.JPG': 'A sensorial shelf with the Geometric Cabinet, blue solids and the Pink Tower beside it',
    'image101.jpg': 'A wooden Geometric Cabinet beside a chart of blue geometric shapes with labels',
    'image102.jpg': 'A long row of low sensorial shelves holding Cylinder Blocks, Red Rods and other materials',
    'image103.jpg': 'A wooden cupboard of sensorial materials including the Brown Stair and Pink Tower cubes',
    'image104.png': "An early black and white image of a glass-fronted cupboard of materials, captioned 'Cupboard with Apparatus'",
    'image105.JPG': 'A sensorial shelf of Constructive Triangles boxes, Geometric Solids and coloured materials in open trays',
    'image106.JPG': 'A girl striking a row of metal Montessori Bells on a wooden table',
    'image107.png': 'A boy playing the Montessori Bells on a table beside a large window',
    'image108.JPG': 'A girl in a green coat holding a beater beside two rows of Montessori Bells',
    'image109.JPG': 'A shelf holding a row of Montessori Bells with music cards and instruments below',
    'image110.png': 'A boy playing the Montessori Bells on a long table while a teacher sits nearby',
    'image111.JPG': 'A boy and a girl pegging blue towels on a wooden drying rack outdoors',
    'image112.jpg': 'Three girls pegging cloths and towels on a washing line on a terrace',
    'image113.png': 'A girl taking a towel from a shelf of folded cloths and towels beside a green basin',
    'image114.png': 'Children washing their hands at a long steel sink in a classroom',
    'image115.png': 'Two girls washing plastic plates at a sink with a dish brush',
    'image116.png': 'A cloth, broom, dustpan, brush and mop hanging from hooks on a glass-block wall, each under an illustrated label',
    'image117.jpg': 'Feather dusters, a dustpan, a brush and a mop hanging on hooks along a white brick wall',
    'image118.JPG': 'Two boys at a counter in front of a wall of hanging dusters, brushes and dustpans',
    'image119.JPG': 'A girl standing on a chair to hang a dustpan on a wall hook',
    'image120.png': 'A wooden rail with child-sized brooms, a feather duster, a dustpan and a carpet beater hanging from it',
    'image121.jpg': 'A tiger figure, a large brass coin and small metal objects arranged on dark wooden display stands',
    'image122.jpg': 'A wooden display case with small compartments holding tiny ornaments and figures',
    'image123.jpg': 'Polishing trays holding a glass bottle, a wooden cup and a jar of polish on a shelf',
    'image124.jpeg': 'A polishing shelf with brightly coloured rolled mats, baskets and small brass objects on top',
    'image125.jpeg': 'A white polishing shelf with coloured mats, baskets and brass ornaments on top',
    'image126.jpeg': 'A polishing shelf with orange and yellow trays, coloured mats and small ornaments on top',
    'image127.jpeg': 'A white polishing shelf with rolled coloured mats, baskets and small ornaments on top',
    'image128.jpeg': 'A white polishing shelf with coloured mats, trays of glass and metal objects and a round framed panel above',
    'image129.JPG': 'A child-sized woodwork bench beside a pegboard of saws, hammers, pliers and screwdrivers',
    'image130.jpg': 'Three boys at a woodwork table, one wearing safety goggles and holding a piece of wood',
    'image131.JPG': "A wooden carpenter's bench with a vice beside shelves of woodwork tools and materials",
    'image132.png': 'Three children working at separate small tables in front of mathematics shelves',
    'image133.jpg': 'A bright classroom with small tables placed singly and in pairs among low shelves',
    'image134.jpg': 'A classroom with white tables pushed together in groups and shelves around the walls',
    'image135.jpg': 'Two views of a classroom with long tables pushed together in rows beneath nature charts',
    'image136.jpg': 'Two boys working at a pair of tables placed side by side in a sunny classroom',
    'image137.jpg': 'A girl and a boy sharing a table, writing in booklets beside a tray of beads',
    'image138.jpg': 'A boy working at a single table by a window, with other children at tables beyond',
    'image139.JPG': 'Two girls at a white table by a window, one matching cut-up images of children',
    'image140.JPG': 'Two boys working at tables facing each other with a Trinomial Cube and coloured beads',
    'image141.jpg': 'A smiling boy carrying a folding table with its legs tucked away on artificial grass',
    'image142.jpg': 'Children sitting on the floor drawing at low folding tables with coloured pencils',
    'image143.jpg': 'Children working outdoors on artificial grass at low portable tables and on mats',
    'image144.png': 'Boys writing on the floor at low folding tables in a classroom',
    'image145.jpg': 'Children eating lunch at low portable tables on a carpeted classroom floor',
    'image146.jpg': 'Two girls sitting on a rug at a low cloth-covered peace table',
    'image147.png': 'A boy and a girl sitting on floor cushions facing each other across a low white table',
    'image148.JPG': 'A small round wooden table on a pale rug beneath a framed image on the wall',
    'image149.png': 'Two children kneeling on cushions at a small table with a terrarium, in front of a poster of dancing figures',
    'image150.jpg': 'Two boys sitting on the floor beside a small round table with a flower and a small easel',
    'image151.jpeg': "A sign in Chinese with the English words 'Please keep quiet and keep quiet'",
    'image152.jpg': "A book corner with a small sofa, a round rug and a wooden display rack of children's books",
    'image153.jpg': 'A painted red book holder with flowers beside a small dark leather armchair',
    'image154.jpg': "A cosy reading corner with an armchair, a book rack and children's drawings by a window",
    'image155.jpeg': 'A reading nook under a pink canopy with cushions and a small bookshelf',
    'image156.jpg': "A child's armchair with a dinosaur-patterned cushion beside a small bookshelf by a window",
    'image157.JPG': 'A boy and a girl looking at a large open book on a wooden bookshelf',
    'image158.jpg': 'A painted blue book holder beside a small wicker chair on a patterned rug',
    'image159.jpg': 'Two small white armchairs on either side of a low wooden book rack',
    'image160.JPG': 'A wooden shelf of books, image cards and a glass bowl of small cacti',
    'image161.jpg': 'A basket of rolled mats beside a small wicker chair and a painted green book holder',
    'image162.jpg': 'Four girls brushing their teeth in front of a row of child-sized washbasins',
    'image163.JPG': 'Children brushing their teeth at a long steel sink with a mirror and a hand-washing chart',
    'image164.JPG': 'Two laughing children standing on step stools to brush their teeth at a washbasin',
    'image165.jpeg': 'Two urinals in a bathroom with a small blue step stool on a raised platform',
    'image166.JPG': 'Children washing their hands at a long trough sink with several taps',
    'image167.jpg': 'A small washing table with a blue and white bowl and jug beside a round table with a cloth',
    'image168.JPG': 'A girl at a table looking at her open mouth in a hand mirror',
    'image169.jpg': "Children brushing each other's hair at a table with a tray of combs",
    'image170.jpg': 'A boy with face cream on his cheeks sitting at a table in front of a wooden mirror',
    'image171.jpg': 'A wooden tray holding a mirror, hairbrushes, a comb and a red cloth on a classroom table',
    'image172.JPG': 'An older girl and a small girl looking into a wall mirror in a classroom',
    'image173.jpg': 'A low self-care table with a small mirror chest and folded cloths beneath Chinese posters',
    'image174.jpg': 'A small self-care table with a mirror, tissues and a hairbrush above a woven stool',
    'image175.jpg': 'A small round self-care table with a mirror and boxes, with a woven stool beneath',
    'image176.png': 'A small self-care table with a wall mirror, a hairbrush, tissues and a pink basin',
    'image177.png': 'A low dark wooden self-care table with a mirror, combs and creams beside a red floor cushion',
    'image178.jpg': 'A low carved wooden table with a red embroidered runner, a round mirror and a tissue box',
    'image179.jpg': 'A practical life area with shelves of cloths and small tables set for washing activities',
    'image180.jpg': 'A girl wearing headphones listening to a CD player on a board over a fish tank',
    'image181.jpg': 'A hand-washing table set with a blue jug, a large blue bowl and blue cloths',
    'image182.jpg': 'A washing table set with two red and white bowls, a jug, a soap dispenser and a dish rack',
    'image183.jpg': 'A cloth-washing table with two decorated bowls, a washboard, a yellow jug and a bar of soap',
    'image184.jpg': 'A table set for flower arranging with a wooden bowl, a jug, scissors and a small funnel',
    'image185.png': 'A low tea table with a tea tray and cups beside a cabinet of teapots and a floor cushion',
    'image186.jpg': 'A calligraphy table with a felt cloth, a brush rack and an ink stone beside a wicker chair',
    'image187.jpg': 'A low tea table with a blue cloth, a tea tray, small blue teapots and a sand timer',
    'image188.png': 'A calligraphy table with a grid-lined mat, a brush stand and an ink pot beneath Chinese characters on the wall',
    'image189.jpg': 'A sharing table with a blue patterned cloth holding pressed plants, an illustrated card and a small tray',
    'image190.png': 'Three children looking at family snapshots pinned above a sharing table',
    'image191.JPG': 'A group of girls looking at plants and pebbles in a glass tank on a sharing table',
    'image192.jpg': 'Three children looking at a board of family snapshots above a sharing table',
    'image193.png': 'Two girls kneeling at a sharing table beneath a board of family snapshots',
    'image194.png': 'A boy sitting at a sharing table beneath a corkboard covered with family snapshots',
    'image195.jpg': "Raphael's Madonna della Seggiola: a round painting of the Madonna holding the Christ Child, with the young St John beside them",
    'image196.jpg': 'A cluttered storage corner with a glass-fronted cabinet and a stack of plastic drawers',
    'image197.jpg': 'White storage shelves neatly filled with boxes, baskets, books and supplies',
    'image198.JPG': 'A storeroom with white shelves of materials and supplies and a stepladder in the middle',
    'image199.jpeg': 'A storage room with grey cabinets, a microwave and clear plastic boxes stacked on shelves',
    'image200.jpg': "Wooden drawer units labelled in English and Chinese, such as 'Glue', 'Scissors' and 'Crayons'",
    'image201.jpg': 'An empty wooden shelf unit with a red and blue Number Rod laid along its edge to measure it',
    'image202.jpg': 'Two girls beside a newly assembled wooden shelf unit next to a teal cabinet',
    'image203.jpg': 'A handwritten sheet of shelf measurements reading 30, 30, 50, 35 and 35',
    'image204.jpg': 'A boy and a girl carrying a wooden shelf board in a classroom',
    'image205.jpg': 'Two girls helping to assemble a wooden shelf unit on the classroom floor',
    'image206.jpg': "Stacks of plastic drawers labelled with children's names and filled with unfinished papers",
    'image207.jpeg': 'Two tall white plastic drawer units standing side by side on a wooden floor',
    'image208.jpg': 'A girl sitting on the floor sorting zipped plastic pouches beside a basket',
    'image209.jpg': 'Shelves of clear plastic storage boxes of different sizes in a shop',
    'image210.jpg': 'A cupboard of clear jars holding beans, lentils, rice and labelled spices',
    'image211.jpg': 'A small shelf unit holding a jar of pencils, a pencil sharpener and folders of papers',
    'image212.JPG': 'Children sitting on the classroom floor watching a window cleaner hanging outside the glass',
    'image213.jpg': 'Children crowding at tall classroom windows to watch the snow falling outside',
    'image214.JPG': 'Two girls kneeling on a window seat looking at a man outside the glass',
}


# 24 Oct 2026: objects standing on white - the white painted the page colour (the cupboard; the round Raphael painting). Room scenes with white walls keep their white.
MASK_WHITE = ['image103.jpg', 'image195.jpg']


# 26 Oct 2026 (2.2.0 page check): an image row straight after an image set beside the text sat beside it and was pushed left (1280: 107px off the screen) - rows start below it
CSS += """
html body main .mm-row{clear:both}
"""
