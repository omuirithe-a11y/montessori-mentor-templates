# 8 Nov 2026: copy of the 24-26 Oct settings for the rebuild from the new Word file (owner "B", 8 Nov); image names renumbered to the new Word file.
# 2.2.0 The Prepared Environment - settings (24 Oct 2026)
# User 24 Oct 11:59: "Build 2.2.0 The Prepared Environment from the updated Essay Code Template" (GitHub d33a6f5).
# Hero: the 2.2 hero decided 18 Oct (Drive prepared-environment-hero.jpg, three children's faces already blurred), centred.
# Faces: round 1 sheet sent for the user's answer; the page is built from the blurred copies only after round 2.

# 24 Oct 2026: at phone width the wide image beside "Trillium Montessori" (image151, 2.14 times as wide as tall) stood
# 386px wide at 180 high and pushed the page 20px wider than a 390 screen - on phones an image beside text is never
# wider than the text column (its height follows)
CSS = ""   # 8 Nov 2026: the phone rule for side images dropped - b3 showed them 592 wide from 480 files at 640 (on-screen check fault); without it they are 180 high as on every page, widest 337 at 390

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
# 8 Nov 2026: the 25 Oct mm-float-clear script dropped - on b3 it pushed image 1 and image 153 24-35 down at some loads (placement and
# blocks checks); without it no side image overlaps the text above at 641-1280 (measured on b3)
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
# 8 Nov 2026: the two font-size blocks above (Oct) dropped - measured at 1280, 768 and 390 on b3, every size is the same without them (the template now has her 29 Oct figures)
# 24 Oct 2026: with the menu bar at 18 the menu did not fit between 961 and 1099px - there the header's side padding is 16, the gap between
# menu items 2px and each arrow 13px wide (8 Nov: still needed - without it the menu runs 52px past the screen at 961)
CSS += """
/* 24 Oct 2026 (you: "18 everywhere"): the menu bar at 18 fits between 961 and 1099 */
@media (min-width:961px) and (max-width:1099px){html body .site-head-in{padding-left:16px !important;padding-right:16px !important}html body .menu{gap:2px !important}html body .menu .sub-toggle{width:13px !important;min-width:13px !important;padding:0 !important;margin-left:1px !important}}
"""

# 24 Oct 2026: a description for every image (site rule of 21 Oct), written by looking at each image
ALT_TEXT = {}   # 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere


# 24 Oct 2026: objects standing on white - the white painted the page colour (the cupboard; the round Raphael painting). Room scenes with white walls keep their white.
MASK_WHITE = ['image190.jpg', 'image193.jpg']   # 8 Nov 2026: the same two images (cupboard, Raphael) under the new Word file's names (were image103, image195)


# 26 Oct 2026 (2.2.0 page check): an image row straight after an image set beside the text sat beside it and was pushed left (1280: 107px off the screen) - rows start below it
CSS += """
/* 26 Oct 2026: an image row after images beside the text starts below them, as in your PDF */
html body main .mm-row{clear:both}
"""

# 8 Nov 2026 (owner, word for word "yes" to: "Should the contents list show only your 10 entries, each linking to its section, with the
# 33 headings staying on the page as they are in Word?"): the contents list is her 10 entries (her screenshot), each to the first heading of its part
PAGE_CODE_REPLACE += [('<ul class="toc-groups"><li><a href="#preparing-environments">Preparing environments</a></li><li><a href="#furniture">Furniture</a></li><li><a href="#purchasing">Purchasing</a></li><li><a href="#rows-of-the-shelves">Rows of the Shelves</a></li><li><a href="#shelf-height">Shelf Height</a></li><li><a href="#shelf-length">Shelf Length</a></li><li><a href="#height-of-tables-and-chairs">Height of Tables and Chairs</a></li><li><a href="#layout-of-the-furniture">Layout of the Furniture</a></li><li><a href="#layout-of-the-shelves">Layout of the Shelves</a></li><li><a href="#layout-of-mathematics-area">Layout of Mathematics Area</a></li><li><a href="#layout-of-language-area">Layout of Language Area</a></li><li><a href="#book-corner">Book Corner</a></li><li><a href="#easel">Easel</a></li><li><a href="#layout-of-sensorial-area-bells">Layout of Sensorial Area - Bells</a></li><li><a href="#layout-of-the-practical-life-area">Layout of the Practical Life Area</a></li><li><a href="#brushes-etc">Brushes, etc.</a></li><li><a href="#display-of-polishing-objects-and-trays">Display of Polishing Objects and Trays</a></li></ul>',
 '<ul class="toc-groups"><li><a href="#purchasing">Furniture - Purchasing</a></li><li><a href="#rows-of-the-shelves">Furniture - Dimensions</a></li><li><a href="#layout-of-mathematics-area">Layout of Mathematics</a></li><li><a href="#layout-of-language-area">Layout of Language</a></li><li><a href="#layout-of-sensorial-area-bells">Layout of Sensorial</a></li><li><a href="#layout-of-the-practical-life-area">Layout of Practical Life</a></li><li><a href="#layout-of-the-tables">Layout of Tables</a></li><li><a href="#single-use-tables">Single-Use Tables</a></li><li><a href="#mats-quantity">Mats</a></li><li><a href="#storage-and-admin">Storage and Admin</a></li></ul>')]

# ---------------------------------------------------------------------------------------------------------------------------
# 8 Nov 2026: the owner's agreed edits of 7-8 Nov (records/PE-EDITS-2.md, records/TEMPLATE-CHANGES.md, the 7 Nov list) put into this
# rebuild; each is measured on the build at 1280 before the checks.
DIV = ['preparing-environments', 'furniture', 'layout-of-the-furniture', 'layout-of-mathematics-area', 'layout-of-language-area',
       'book-corner', 'layout-of-the-tables', 'sharing-nature-table', 'mats-quantity', 'bathroom', 'storage-and-admin', 'windows']
# 7 Nov (owner): "When I write 'divider' I always mean 40/40"; dividers above these headings (her 7 Nov dividers, matched to the new headings, 8 Nov)
for _sid in DIV:
    for _cls in ('mm-hc-0432FF', 'mm-hc-EE0000'):
        PAGE_CODE_REPLACE.append(('</section><section class="section" id="%s"><h2 class="%s">' % (_sid, _cls),
                                  '<p class="mm-gl" data-space="40"> </p></section><section class="section" id="%s"><h2 class="%s" data-space="40">' % (_sid, _cls)))
# 7 Nov (owner): "delete that rule and ignore that old rule" - the 20 Oct rule "no lines round quotations"; a divider after a quotation stands
# 40 below the quotation's last line, measured from the line its letters stand on
PAGE_CODE_REPLACE += [
 ("      if (!bqA && !bqB) return;\n      g.classList.add('mm-gl-bq');",
  "      if (!bqA && !bqB) return;\n      if (bqA) { var bl = (function(e){ var w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT), n, last = null; while ((n = w.nextNode())) if (n.nodeValue.trim()) last = n; if (!last) return null; var z = document.createElement('span'); z.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline'; last.parentNode.insertBefore(z, last.nextSibling); var y = z.getBoundingClientRect().top; z.parentNode.removeChild(z); return y; })(pv);\n        if (bl !== null) for (var k0 = 0; k0 < 4; k0++) { var d0 = 40 - (g.getBoundingClientRect().top - bl); if (Math.abs(d0) < 0.2) break; g.style.setProperty('margin-top', ((parseFloat(getComputedStyle(g).marginTop) || 0) + d0).toFixed(2) + 'px', 'important'); } }\n      return;   /* 7 Nov 2026 (owner): a divider after a quotation stands 40 below its last line (the line the letters stand on), at every width */\n      g.classList.add('mm-gl-bq');"),
 # 8 Nov (owner, PE-EDITS-2 item 4: "Photos. make 30/30 instead of 40/40"): rows of images 30 above and 30 below
 ('var TP0 = 40;', 'var TP0 = 30;   /* 8 Nov 2026 (owner: "Photos. make 30/30 instead of 40/40") */'),
 # image 168 (Word image166, the boy at the board) stood as a side image with no text beside it at the end of its section and lay over the next heading - shown as a row of one
 ('<div class="mm-float"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.43541"><img alt="" class="doc-img" data-full="images/168.jpg"',
  '<div class="mm-row" data-above="40" data-level="25"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:1.43541"><img alt="" class="doc-img" data-full="images/168.jpg"'),
]
CSS += """
/* 7 Nov 2026 (you: "this pho is an exception. make it 200 high"): the Madonna della Seggiola beside its quotation 200 high */
@media (min-width:831px){html body main .mm-float:has(img[data-full="images/193.jpg"]) .pim{height:200px !important;width:auto !important}}
"""
# 8 Nov 2026 (owner: "Photos. make 30/30"): the space above a row of images is measured from the line the letters above stand on
# (her letters-to-letters measure), so a last line with or without letters below the line gives the same 30
PAGE_CODE_REPLACE += [
 ("        var ib = glInkBottom(pv); if (ib === null) return;\n        t = Math.min.apply(null, q('.pim', rw).map(function(p){ return p.getBoundingClientRect().top; }));\n        var d = TP0 + 0.8 - (t - ib);",
  "        var ib = (function(e){ var w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT), n, last = null; while ((n = w.nextNode())) if (n.nodeValue.trim()) last = n; if (!last) return null; var z = document.createElement('span'); z.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline'; last.parentNode.insertBefore(z, last.nextSibling); var y = z.getBoundingClientRect().top; z.parentNode.removeChild(z); return y; })(pv); if (ib === null) return;   /* 8 Nov 2026: from the baseline */\n        t = Math.min.apply(null, q('.pim', rw).map(function(p){ return p.getBoundingClientRect().top; }));\n        var d = TP0 - (t - ib);"),
 ('<div class="mm-row" data-above=', '<div class="mm-row" data-space="25" data-above='),
]
PAGE_CODE_REPLACE += [
 # below a row: 30 to the top of the capitals (the ascenders stand about 1 px above them)
 ("        var it = glInkTop(nx); if (it === null) return;\n        var d = TP0 - (it - b);", "        var it = glInkTop(nx); if (it === null) return;\n        var d = TP0 - 1 - (it - b);   /* 8 Nov 2026: 30 to the capitals */"),
 # 7 Nov (owner): the stray full stop ("is that a stray dot above sensorial?" - "yes"), still a paragraph of its own in the new Word file
 ('<p>.</p>', ''),
]
# 8 Nov 2026 (owner "yes"): the 20 Oct no-lines rule deleted, quotation lines 24 and quotation to paragraph 29 moved into the Essay Code Template
# the 40 below a divider: the blue headings measured 41 with the heading's own 40 (the red ones 40)
PAGE_CODE_REPLACE = [(o, n.replace('<h2 class="mm-hc-0432FF" data-space="40">', '<h2 class="mm-hc-0432FF" data-space="39">')) for o, n in PAGE_CODE_REPLACE]
# 7 Nov (owner: "make this table less than full-width. maybe reduce the space between the comlumns by 50%") and 8 Nov ("centre
# 'Dimensions ...' above 'Height of legs'"): above 640 each gap between columns is half the gap the full-width table had at that width,
# and the title's middle stands over the middle of "Height of Legs"
PAGE_CODE_REPLACE += [('</body>', """<script id="mm-table-half-7nov">/* 7-8 Nov 2026 (owner): the chairs table - gaps between columns halved; title centred above "Height of Legs" */(function(){function run(){[].forEach.call(document.querySelectorAll('main table.mm-table'),function(t){var all=[].slice.call(t.querySelectorAll('td,th'));t.style.removeProperty('width');all.forEach(function(c){c.style.removeProperty('padding-right');c.style.removeProperty('padding-left');c.style.removeProperty('text-align');});var th=t.querySelector('thead th');if(window.innerWidth<=640)return;var rows=[].slice.call(t.querySelectorAll('tbody tr')),n=0;rows.forEach(function(r){n=Math.max(n,r.children.length);});var R=[],L=[],g=document.createRange();for(var i=0;i<n;i++){R.push(-1e9);L.push(1e9);}rows.forEach(function(r){[].forEach.call(r.children,function(c,i){if(!c.textContent.trim())return;g.selectNodeContents(c);[].forEach.call(g.getClientRects(),function(q){R[i]=Math.max(R[i],q.right);L[i]=Math.min(L[i],q.left);});});});var gaps=[];for(var j=1;j<n;j++)gaps.push(L[j]-R[j-1]);t.style.setProperty('width','auto','important');rows.forEach(function(r){[].forEach.call(r.children,function(c,i){if(i<n-1)c.style.setProperty('padding-right',Math.max(0,gaps[i]/2).toFixed(2)+'px','important');});});if(!th)return;var hl=[].filter.call(t.querySelectorAll('tbody td'),function(c){return /Height of Legs/.test(c.textContent);})[0];if(!hl)return;th.style.setProperty('text-align','left','important');th.style.setProperty('padding-left','0px','important');var gr=document.createRange();gr.selectNodeContents(hl);var hr=gr.getClientRects()[0];gr.selectNodeContents(th);var tr=gr.getClientRects()[0];if(!hr||!tr)return;var mid=(hr.left+hr.right)/2,tw=tr.right-tr.left,want=mid-tw/2-th.getBoundingClientRect().left;th.style.setProperty('padding-left',Math.max(0,want).toFixed(2)+'px','important');});}addEventListener('load',run);addEventListener('resize',function(){clearTimeout(run.t);run.t=setTimeout(run,300);});run();})();</script></body>""")]
# measured 39/41/39 below the line with the figures above - each set so the space below measures 40 at 1280
PAGE_CODE_REPLACE = [(o, n.replace('id="preparing-environments"><h2 class="mm-hc-0432FF" data-space="39">', 'id="preparing-environments"><h2 class="mm-hc-0432FF" data-space="40">')
                          .replace('id="mats-quantity"><h2 class="mm-hc-0432FF" data-space="39">', 'id="mats-quantity"><h2 class="mm-hc-0432FF" data-space="40">')
                          .replace('id="layout-of-the-furniture"><h2 class="mm-hc-EE0000" data-space="40">', 'id="layout-of-the-furniture"><h2 class="mm-hc-EE0000" data-space="39">')) for o, n in PAGE_CODE_REPLACE]
# 7 Nov (owner: "top of photo = top of line of text"): the Madonna stood 14 above its quotation's first line - placed by glTopline (the template's 21 Oct rule) like a side image
PAGE_CODE_REPLACE += [('<div class="mm-float"><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:0.97556"><img alt="" class="doc-img" data-full="images/193.jpg"',
                       '<div class="mm-float" data-topline=""><div class="mm-imgs"><figure class="ph" style="--h:180;--hp:180"><div class="pim" style="aspect-ratio:0.97556"><img alt="" class="doc-img" data-full="images/193.jpg"')]
# 8 Nov (owner: "Photos. make 30/30"): a quotation straight after a row of images, 30 below the images (32 by the table's 32)
PAGE_CODE_REPLACE += [('</div></div><blockquote class="pullquote">', '</div></div><blockquote class="pullquote" data-space="30">')]

# 8 Nov 2026 (owner "yes": the contents list shows only her 10 entries): b3 still listed the 16 old entries in the second column;
# the 10 entries now stand 5 and 5 in the two columns
PAGE_CODE_REPLACE += [('<div class="toc-grid"><ul class="toc-groups"><li><a href="#purchasing">Furniture - Purchasing</a></li><li><a href="#rows-of-the-shelves">Furniture - Dimensions</a></li><li><a href="#layout-of-mathematics-area">Layout of Mathematics</a></li><li><a href="#layout-of-language-area">Layout of Language</a></li><li><a href="#layout-of-sensorial-area-bells">Layout of Sensorial</a></li><li><a href="#layout-of-the-practical-life-area">Layout of Practical Life</a></li><li><a href="#layout-of-the-tables">Layout of Tables</a></li><li><a href="#single-use-tables">Single-Use Tables</a></li><li><a href="#mats-quantity">Mats</a></li><li><a href="#storage-and-admin">Storage and Admin</a></li></ul><ul class="toc-groups"><li><a href="#woodwork">Woodwork</a></li><li><a href="#the-peace-table">The Peace Table</a></li><li><a href="#layout-of-the-tables">Layout of the Tables</a></li><li><a href="#single-use-tables">Single-Use Tables</a></li><li><a href="#sharing-nature-table">Sharing/Nature Table</a></li><li><a href="#mats-quantity">Mats - Quantity</a></li><li><a href="#mats-dimensions">Mats - Dimensions</a></li><li><a href="#mats-colour">Mats - Colour</a></li><li><a href="#mats-material-and-storage">Mats - Material and Storage</a></li><li><a href="#mats-cleaning">Mats - Cleaning</a></li><li><a href="#boxes-of-materials-open-or-closed">Boxes of Materials: open or closed?</a></li><li><a href="#class-decoration">Class Decoration</a></li><li><a href="#raphael-s-madonna-della-seggiola-madonna-of-the-chair">Raphael’s Madonna della Seggiola (Madonna of the Chair)</a></li><li><a href="#bathroom">Bathroom</a></li><li><a href="#storage-and-admin">Storage and Admin</a></li><li><a href="#windows">Windows</a></li></ul></div>',
  '<div class="toc-grid"><ul class="toc-groups"><li><a href="#purchasing">Furniture - Purchasing</a></li><li><a href="#rows-of-the-shelves">Furniture - Dimensions</a></li><li><a href="#layout-of-mathematics-area">Layout of Mathematics</a></li><li><a href="#layout-of-language-area">Layout of Language</a></li><li><a href="#layout-of-sensorial-area-bells">Layout of Sensorial</a></li></ul><ul class="toc-groups"><li><a href="#layout-of-the-practical-life-area">Layout of Practical Life</a></li><li><a href="#layout-of-the-tables">Layout of Tables</a></li><li><a href="#single-use-tables">Single-Use Tables</a></li><li><a href="#mats-quantity">Mats</a></li><li><a href="#storage-and-admin">Storage and Admin</a></li></ul></div>')]
# 8 Nov 2026 (b3 format check against the Word file): "Source: AMI France", a Caption-style text box under the chairs table in Word
# (italic, centred, as in her PDF), was missing from the page - put back under the table
PAGE_CODE_REPLACE += [('</table></div>', '</table></div><p class="centred mm-cap"><em>Source: AMI France</em></p>')]
# 8 Nov 2026 (b3 check): in the Lili Peller quotation Word has the LAST full stop upright ("... improving her work."); the build had made
# the one after "valuable assistant" upright instead
PAGE_CODE_REPLACE += [('valuable assistant<span class="mm-wordrun" style="font-style:normal !important">.</span>', 'valuable assistant.'),
 ('dividends in improving her work.</p>', 'dividends in improving her work<span class="mm-wordrun" style="font-style:normal !important">.</span></p>')]
# 8 Nov 2026 (b3 text check, owner 26 Oct: "maths", never "math", in ordinary text on the site)
TEXT_EDITS += [('place the Math shelves', 'place the Maths shelves'), ('lay out the Math shelves', 'lay out the Maths shelves'),
               ('inset paper/math calculations', 'inset paper/maths calculations')]
# 8 Nov 2026 (b3 wrap check: Word has the attribution as a dash-list line under its quotation, the page had it as a plain paragraph
# below the images): the attribution goes back inside its quotation, as on the live page and as the Peller attribution above
PAGE_CODE_REPLACE += [('Normalisation has been achieved.”</p></blockquote>', 'Normalisation has been achieved.”</p><cite>- Maria Montessori,<em> The Secret of Childhood</em>, p.162.</cite></blockquote>'),
 ('<p>Maria Montessori,<em> The Secret of Childhood</em>, p.162.</p>', '')]
# 8 Nov 2026 (b3 images check: at 390 the page was 443 wide): "Before" and "After" above the two halves of the row of images were
# one line with eight Word tabs between them - now the template's two-caption line (.mm-twocap): each over its half of the row,
# each on its own line at 830 and narrower
PAGE_CODE_REPLACE += [('<p>Before <span class="mm-t">' + '\u2409' * 8 + '</span>After</p>', '<p class="mm-twocap"><span>Before</span><span>After</span></p>')]
# 8 Nov 2026 (b3 placement check; your rule "top of photo = top of line of text"): the Madonna stood 14 above the capitals of the quotation's
# first line at 641-830 (the topline script does not run there) and 1 above them from 831 (it lines up with the opening quotation mark)
CSS += """
/* 8 Nov 2026 (you: "top of photo = top of line of text"): the Madonna level with the first line of its quotation */
@media (min-width:641px) and (max-width:830px){html body main .mm-float:has(img[data-full="images/193.jpg"]){margin-top:24px !important}}
@media (min-width:831px){html body main .mm-float:has(img[data-full="images/193.jpg"]) .pim{position:relative;top:1px}}
"""
