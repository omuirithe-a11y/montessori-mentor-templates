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
ALT_TEXT = {}   # 28 Oct 2026, owner: image descriptions (alt text) "are not necessary anymore"; 30 Oct 12:26 "yes" to removing the rule everywhere


# 24 Oct 2026: objects standing on white - the white painted the page colour (the cupboard; the round Raphael painting). Room scenes with white walls keep their white.
MASK_WHITE = ['image103.jpg', 'image195.jpg']


# 26 Oct 2026 (2.2.0 page check): an image row straight after an image set beside the text sat beside it and was pushed left (1280: 107px off the screen) - rows start below it
CSS += """
html body main .mm-row{clear:both}
"""
