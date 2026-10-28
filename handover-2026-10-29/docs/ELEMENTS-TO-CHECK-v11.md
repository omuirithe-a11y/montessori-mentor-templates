# Elements the checks should look for — version 11 (29 Oct 2026)

## Added in version 11 (29 Oct 2026 07:3x): elements and behaviours the 28-29 Oct faults showed must be checked

Version 10 (below, unchanged) lists the elements and values in the templates. Version 11 adds the template elements and behaviours whose faults on Culture and Sensorial were not caught by any check, with the check each needs. Template: Essay commit b1ec2db (29 Oct).

| Element / behaviour | Template rule (item) | Fault seen | Check it needs |
|---|---|---|---|
| h3.material-name::before (2 px beige line above the name) | mm-sensorial-live-css; mm-matname-gap-js (item 50: margin-top at least 20px) | line ran through the text above in 14 places at 700, 20 at 1440 | lines-through-text at every band; screenshot |
| .ref-table .ref-row:first-child::before (top line of a reference table) | mm-refline-css (item 50: 6px above the first row; was 17px) | line through "Key Areas and Examples" | lines-through-text |
| .touch-table .ref-row grid (Material / Area / How to touch) | item 49: 641-665 px description on its own line | description squeezed to 235-254 px at 641-660 | full check (squeezed text) at 641-670 |
| .mm-imgs .pim in swipe rows, 641-830 px | item 48: at most 200px high (--hp 210, intro 240 kept at 640 and below) | 109 images too tall | full check (oversized) at 641-830 |
| .mm-row swipe rows below 831 px, padding-left/right | mm-swipe-middle-js (owner 16 Oct 1C: each photo stops mid-screen) | none - settled; checker queried it | screenshot only; allowed |
| A data-gap label opening a set's text (.mm-set .mm-text first child) | item 47: placed by the set, not by mm-letter-gaps-js | margin crept 6-12px per pass to 526-698px; page grew after scrolling | height check: 4 s = after scrolling; largest margin under 150px |
| .mm-set.mm-formula .mm-imgs .ph at phone width | item 46: width min(225px,100%) | 111.jpg 0x0 at 390 | format check images seen at 390 |
| Block after a set beside photos (negative margin, e.g. "Examples of Extensions") | item 45: moves with the set's text | text ran over the label | full check (text over text) |
| stackNarrow / .mm-set.mm-stack | item 44 (live option C) | squeezed text at 831-960 | full check (squeezed) |
| .mm-float.ext-float (Sensorial Extensions photos) | item 43: not centred by wrapFloats | photos 003/004/005 overlapping | full check (image over image) |
| micro-label.lbl-bold with data-gap | item 42: spaced only by mm-letter-gaps-js | +11px after an album toggle (Culture) | height check: closed again = load |
| Every margin the spacing scripts set | - | two scripts writing one margin (Culture headings) | record setProperty writes; one writer per element |



Built from both templates on GitHub (Essay 50e0cd0, Resources ddce8cb). Changes from version 5:
- a rule that **excludes** an element (`:not(...)`, nested ones included) is no longer counted as a rule for it. Version 5 listed, for example, the 17, 18 and 20 px paragraph sizes against the beige divider, which those rules exclude;
- how specific a selector is now counts the parts inside `:not(...)`, as browsers do;
- selectors are split on commas only outside brackets, so `:is(a, b)` is no longer cut in two;
- every value shows its condition and its width; a property is labelled **by width**, **by condition**, **by width and condition**, or **repeated** (the same value set more than once);
- "competing" is limited to values for the same element, at the same width, under the same condition; the winner is worked out from importance, then how specific the selector is, then order.

Changes in version 7: a property whose values differ under one condition at one width is always labelled competing, even when only their importance differs (version 6 called some of these "repeated"); and the section "Measured on every element" at the end compares every element of each page with its live copy.


## Essay template: 216 elements, 49 used on none of the nine pages, 116 competing values

| Element | Used on, whole page (count) | Property: value, with condition and width |
|---|---|---|
| `.article` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | margin: 0 auto<br>margin-top (by width): 33px ; 36px at (max-width:640px)<br>max-width (competing): **competing**: var(--page) wins over 1220px<br>padding (by width): **competing**: 0 var(--gutter) 72px wins over 8px 40px 96px ; **competing** at (max-width:640px): 0 24px 56px wins over 8px 24px 72px |
| `.beige-rule` | Jour 1, Aun 1, Bio 1, Cult 1, Math 1, PL 1, RoA 23, Sens 1 | background (by condition): #D9C9AB ; #D9C9AB where `.toc-rule-wrap .beige-rule`<br>height (by condition): 2px ; 2px where `.toc-rule-wrap .beige-rule`<br>margin (by condition): 0 auto 20px ; 0 where `.toc-rule-wrap .beige-rule`<br>max-width (by condition): 100% ; 100% where `.toc-rule-wrap .beige-rule`<br>visibility: hidden where `.toc-rule-wrap .beige-rule` |
| `.beside-photo` | Math 2, PL 1 | clear: none where `blockquote.pullquote.beside-photo` |
| `.blindfold-label` | Sens 2 | color: var(--head)<br>margin: 26px 0 6px<br>text-align: center |
| `.c1` | **none of the nine** | grid-template-columns: minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) where `.panel-in.c1` |
| `.c4` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | gap: 26px 40px where `.panel-in.c4`<br>grid-template-columns: repeat(4,minmax(0,1fr)) where `.panel-in.c4` |
| `.callout` | **none of the nine** | background: var(--tint)<br>border-radius: 3px<br>clear: both<br>margin: 24px 0<br>max-width: 800px<br>padding: 24px |
| `.callout-label` | **none of the nine** | color: var(--ink)<br>font-family: 'Cormorant Garamond',serif<br>font-size: 18px<br>font-style: italic<br>font-weight: 500<br>margin-bottom: 8px |
| `.centred` | PL 1 | text-align: center |
| `.colophon` | **none of the nine** | border-top: 1px solid var(--rule)<br>clear: both<br>color: var(--ink)<br>font-family: 'EB Garamond',serif<br>font-size: 14px<br>margin: 0 auto<br>max-width: 1220px<br>padding: 40px 40px 80px |
| `.cw-white` | Cult 1, Math 5, Sens 1 | border-bottom: 0 !<br>color: var(--ink) !<br>padding-bottom: 0 ! |
| `.doc-img` | Jour 152, Aun 58, Bio 23, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | background (by condition): #EDE6D8 ; transparent where `.ph img.doc-img`<br>border-radius (by condition): 2px ; 0 where `.ph img.doc-img`<br>cursor (by condition): zoom-in ; zoom-in where `.ph img.doc-img`<br>display (by condition): block where `.ph img.doc-img` ; block where `.pim>img.doc-img`<br>height (by condition): auto where `.ph img.doc-img` ; 100% ! where `.pim>img.doc-img`<br>max-height (by condition): none where `.ph img.doc-img` ; none ! where `.pim>img.doc-img`<br>max-width (by condition): 100% ; none where `.ph img.doc-img` ; none ! where `.pim>img.doc-img`<br>object-fit: fill ! where `.pim>img.doc-img`<br>width (by condition): auto ; 100% where `.ph img.doc-img` ; 100% ! where `.pim>img.doc-img` |
| `.formula-divider` | Jour 15, Sens 1 | border: 0<br>border-top: 1px solid var(--rule)<br>margin: 40px 0 24px |
| `.formula-head` | Sens 1 | margin-bottom: 10px |
| `.formula-table` | Sens 1 | border-collapse: collapse<br>font-size (by width): 17px ; 15px at (max-width:640px)<br>font-variant-numeric: tabular-nums |
| `.formula-wrap` | Sens 1 | max-width: 100%<br>overflow-x: auto |
| `.grp` | Jour 33, Aun 33, Bio 33, SRes 33, Cult 33, Math 33, PL 33, RoA 33, Sens 33 | font-weight: 400<br>list-style: none<br>margin: 0<br>margin-bottom: 6px at (max-width:960px)<br>margin-top: 24px where `.panel-in .grp + .grp` at (max-width:960px)<br>padding: 0 |
| `.grp-first` | Sens 42 | margin-bottom: 4px |
| `.grp-last` | Sens 42 | margin-top: 4px |
| `.grp-mid` | Sens 38 | margin-bottom: 4px<br>margin-top: 4px |
| `.hero` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: flex-end<br>background-color: #2A2420<br>background-position: center<br>background-size: cover<br>display: flex<br>margin (by width): 10px 10px 0 ; 0 at (max-width:640px)<br>min-height (by width): 400px ; 240px at (max-width:640px)<br>overflow: hidden<br>padding (by width): 0 8% 40px ; 0 24px 24px at (max-width:640px)<br>position: relative |
| `.hero-sub` | **none of the nine** | color: var(--ink)<br>font-family: 'Cormorant Garamond',serif<br>font-size: 19px<br>font-style: italic<br>font-weight: 400<br>margin-top: 8px |
| `.hero::after` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: linear-gradient(105deg,rgba(15,12,9,.72) 0%,rgba(15,12,9,.55) 34%,rgba(15,12,9,.12) 62%,rgba(15,12,9,0) 80%)<br>content: ""<br>inset: 0<br>pointer-events: none<br>position: absolute |
| `.icon-btn` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>background (by condition): none ; rgba(255,255,255,.1) where `.icon-btn:hover`<br>border: 0<br>border-radius: 22px<br>color: #fff<br>cursor: pointer<br>display: inline-flex<br>height: 44px<br>justify-content: center<br>width: 44px |
| `.lb-counter` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | bottom: 28px<br>color: rgba(255,255,255,.75)<br>display: none<br>font-family: 'EB Garamond',serif<br>font-size: 15px<br>left: 50%<br>position: fixed<br>transform: translateX(-50%) |
| `.lb-frame` | **none of the nine** | box-shadow: 0 20px 60px rgba(0,0,0,.5)<br>overflow: hidden<br>position: relative |
| `.lb-nav` | Jour 2, Aun 2, Bio 2, SRes 2, Cult 2, Math 2, PL 2, RoA 2, Sens 2 | align-items: center<br>background (by condition): rgba(255,255,255,.12) ; rgba(255,255,255,.24) where `.lb-nav:hover`<br>border: none<br>border-radius: 50%<br>color: #fff<br>cursor: pointer<br>display: none<br>font-size: 32px<br>height: 56px<br>justify-content: center<br>line-height: 1<br>position: fixed<br>top: 50%<br>transform: translateY(-50%)<br>transition: background .15s<br>width: 56px |
| `.lb-next` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | right: 24px |
| `.lb-prev` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | left: 24px |
| `.lbl-blue` | Jour 17, Cult 14, Sens 15 | color (by condition): **competing** where `.micro-label.lbl-blue`: var(--head,#0432FF) ! wins over var(--head) ! ; var(--head) ! where `.sub-label.lbl-blue`<br>font-weight (by condition): 400 ! where `.micro-label.lbl-blue` ; 400 ! where `.sub-label.lbl-blue` |
| `.lbl-bold` | Cult 31, Math 57, PL 46, Sens 69 | font-weight (by condition): 700 ! where `.micro-label.lbl-bold` ; 700 ! where `.sub-label.lbl-bold` |
| `.lead-rule` | **none of the nine** | background: #D9C9AB<br>height: 2px<br>margin: 20px auto 20px<br>max-width: 100% |
| `.lightbox` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>background: rgba(20,16,12,.94)<br>cursor: zoom-out<br>display (by condition): none ; flex where `.lightbox.open`<br>inset: 0<br>justify-content: center<br>padding: 5vw<br>position: fixed<br>z-index: 999 |
| `.material-name` | SRes 13, RoA 21, Sens 30 | border-top (competing): **competing**: 1px solid var(--line) wins over 1px solid var(--rule)<br>color (competing): **competing**: var(--head) wins over var(--material)<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',Georgia,serif<br>font-size (by width): 21px ; 19px at (max-width:640px)<br>font-weight (competing): **competing**: 500 wins over 700<br>margin: 0<br>margin-bottom: 8px<br>margin-top (competing): **competing**: 36px wins over 40px<br>padding-top (competing): **competing**: 22px wins over 24px |
| `.materials-table` | Sens 1 | clear: both<br>column-count: 2<br>column-gap: 48px<br>margin: 16px 0 24px<br>max-width: 640px |
| `.mc-1-1` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-1`<br>grid-row: 1 where `#p-curriculum .panel-in > .mc-1-1` |
| `.mc-1-2` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-2`<br>grid-row: 2 where `#p-curriculum .panel-in > .mc-1-2` |
| `.mc-1-3` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-3`<br>grid-row: 3 where `#p-curriculum .panel-in > .mc-1-3` |
| `.mc-2-1` | **none of the nine** | grid-column: 2 where `#p-curriculum .panel-in > .mc-2-1`<br>grid-row: 1 where `#p-curriculum .panel-in > .mc-2-1` |
| `.mc-2-2` | **none of the nine** | grid-column: 2 where `#p-curriculum .panel-in > .mc-2-2`<br>grid-row: 2 where `#p-curriculum .panel-in > .mc-2-2` |
| `.mc-3-1` | **none of the nine** | grid-column: 3 where `#p-curriculum .panel-in > .mc-3-1`<br>grid-row: 1 / span 3 where `#p-curriculum .panel-in > .mc-3-1` |
| `.mc-band` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background (competing): **competing**: #1E4D7B ! wins over <br>color: #fff<br>margin-top (competing): **competing**: 40px ! wins over 60px<br>padding (by width): **competing**: 40px 40px 30px ! wins over 92px 40px 96px ; 60px 24px 64px at (max-width:640px) ; 40px 24px 30px ! at (max-width:830px)<br>text-align: center |
| `.mc-by` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color (competing): **competing** where `.mc-band p.mc-by`: #DCE6F0 ! wins over <br>font-size (by width): **competing** where `.mc-band p.mc-by`: 18px ! wins over  ; **competing** where `.mc-band p.mc-by` at (max-width:640px): 17px ! wins over  ; 17px ! where `.mc-band p.mc-by` at (max-width:830px) ; 18px ! where `.mc-band p.mc-by` at (min-width:641px)<br>font-style (competing): **competing** where `.mc-band p.mc-by`: normal ! wins over <br>letter-spacing: .04em where `.mc-band p.mc-by`<br>line-height (by width): 40px ! where `.mc-band p.mc-by` ; 38px ! where `.mc-band p.mc-by` at (max-width:830px)<br>margin-top (competing): **competing** where `.mc-band p.mc-by`: 0 ! wins over 22px |
| `.menu` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display (by width): flex ; block at (max-width:960px)<br>font-weight: 400<br>gap (by width): 22px ; 15px at (max-width:1180px) ; 10px at (min-width:961px) and (max-width:1279px) ; 7px at (min-width:961px) and (max-width:1023px) ; 2px ! at (min-width:961px) and (max-width:1099px)<br>list-style: none<br>margin: 0<br>padding: 0 |
| `.menu-btn` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | display (by width): none ; inline-flex at (max-width:960px) |
| `.meta` | SRes 10, RoA 17 | display: inline ! where `.res-item:has(> .meta:last-child > a.pdf:last-child) > .meta` at (max-width:640px) |
| `.micro-label` | Cult 45, Math 57, PL 46, Sens 84 | border-top: 2px solid #D9C9AB where `.micro-label.mm-lineabove`<br>break-after: avoid where `.mm-albums-c .mm-cbody>.micro-label`<br>color (by condition): var(--ink) ; **competing** where `.micro-label.lbl-blue`: var(--head,#0432FF) ! wins over var(--head) ! ; #EE0000 ! where `.micro-label.mm-red`<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',serif<br>font-size (by width and condition): **competing**: 18px ! wins over 19px, 21px ! ; **competing** at (max-width:640px): 17px ! wins over 19px ! ; 20px ! where `.micro-label.mm-red`<br>font-weight (by condition): **competing**: 400 ! wins over 700 ; 700 ! where `.micro-label.lbl-bold` ; 400 ! where `.micro-label.lbl-blue` ; 400 ! where `.micro-label.mm-wc` ; 400 ! where `.micro-label.mm-red`<br>line-height (by width): **competing**: 29.7px ! wins over 37.2px ! ; **competing** at (max-width:640px): 28.05px ! wins over 36px !<br>margin: 6px 0 11px ! where `.mm-albums-c .mm-cbody>.micro-label`<br>margin-bottom: 0<br>margin-top (by condition): 15px ; 0 ! where `.lead-rule + .micro-label` ; 0 ! where `.mm-albums-c .mm-cbody>.micro-label:first-child`<br>padding-top: 28px where `.micro-label.mm-lineabove` |
| `.mm-albums-c` | Cult 7 | margin: 0<br>margin-left (by width): 24px ! ; 0 ! at (max-width:640px) |
| `.mm-area` | Cult 7, Math 12 | border-bottom (by condition): 0 ! ; 2px solid currentColor ! where `h2.mm-area:not([data-notred])`<br>padding-bottom (by condition): 0 ! ; 8px ! where `h2.mm-area:not([data-notred])` |
| `.mm-arrow` | **none of the nine** | display: none ! at (max-width:640px) |
| `.mm-attr` | PL 1 | font-size (by width and condition): 18px ! where `blockquote span.mm-attr` ; 18px ! where `blockquote.pullquote span.mm-attr` ; 17px ! where `blockquote span.mm-attr` at (max-width:830px) ; 17px ! where `blockquote.pullquote span.mm-attr` at (max-width:830px)<br>font-style: normal where `blockquote.pullquote p .mm-attr`<br>line-height (by width and condition): 40px ! where `blockquote span.mm-attr` ; 40px ! where `blockquote.pullquote span.mm-attr` ; 38px ! where `blockquote span.mm-attr` at (max-width:830px) ; 38px ! where `blockquote.pullquote span.mm-attr` at (max-width:830px) |
| `.mm-bda` | **none of the nine** | align-items: baseline<br>display: flex<br>line-height: 1.65 !<br>margin: 0 0 6px<br>text-align: left |
| `.mm-cabar` | Math 1 | align-items: stretch at (max-width:640px)<br>column-gap: 12px at (max-width:640px)<br>display: grid at (max-width:640px)<br>grid-template-columns: auto 6px 1fr at (max-width:640px)<br>margin: 0<br>position: relative |
| `.mm-cabar-bar` | Math 1 | background (by width): linear-gradient(90deg,#1E4D7B,#D9E2EA) ; linear-gradient(180deg,#1E4D7B,#D9E2EA) at (max-width:640px)<br>border-radius: 3px<br>grid-column: 2 at (max-width:640px)<br>height (by width): 6px ; auto at (max-width:640px)<br>min-height: 120px at (max-width:640px)<br>width: 6px at (max-width:640px) |
| `.mm-cabar-ends` | Math 1 | display: flex<br>flex-direction: column at (max-width:640px)<br>font-size: 14px<br>font-variant: small-caps<br>grid-column: 1 at (max-width:640px)<br>justify-content: space-between<br>letter-spacing: .06em<br>line-height: 1.2<br>margin: 0 at (max-width:640px)<br>margin-bottom: 5px |
| `.mm-cabar-tick` | **none of the nine** | font-size: 13px<br>line-height: 1.25<br>position (by width): absolute ; static at (max-width:640px)<br>text-align (by width): center ; left at (max-width:640px)<br>top: -9px<br>transform (by width): translateX(-50%) ; none at (max-width:640px)<br>white-space (by width): nowrap ; normal at (max-width:640px) |
| `.mm-cabar-tick::before` | **none of the nine** | background: #1E4D7B<br>content: ""<br>display (by width): block ; none at (max-width:640px)<br>height: 12px<br>margin: 0 auto 4px<br>width: 2px |
| `.mm-cabar-ticks` | Math 1 | display (by width and condition): none where `.mm-cabar-plain .mm-cabar-ticks` ; flex at (max-width:640px)<br>flex-direction: column at (max-width:640px)<br>grid-column: 3 at (max-width:640px)<br>height (by width): 40px ; auto at (max-width:640px)<br>justify-content: space-between at (max-width:640px)<br>position: relative |
| `.mm-cap` | Bio 9, Math 22 | bottom: 100% where `figure.mm-cf>.mm-cap:not(.mm-cap-below)`<br>font-size (by width): 16px ; 16px ! at (min-width:641px) ; 16px ! at (max-width:640px)<br>font-style: italic<br>left (by width): 50% where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; auto ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px)<br>line-height: 1.3<br>margin (by width and condition): 0 0 6px ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; 0 0 6px ! where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; 0 0 6px ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px) ; 0 0 6px<br>min-width: 100% where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)`<br>padding-top (by condition): 30px where `.mm-pdf-r:has(.mm-cap:not(.mm-cap-below))` ; 30px where `.mm-pdf-l:has(.mm-cap:not(.mm-cap-below))` ; 2px<br>position (by width and condition): absolute where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; static where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; static ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px)<br>text-align (by width and condition): center where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px) ; center<br>transform (by width and condition): translateX(-50%) where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; none where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; none ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px)<br>white-space (by width and condition): nowrap where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; normal where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; normal ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px)<br>width (by width and condition): 0 where `.mm-set[data-cap] figure.mm-cf>.mm-cap:not(.mm-cap-below)` ; auto ! where `figure.mm-cf>.mm-cap:not(.mm-cap-below)` at (max-width:640px) |
| `.mm-cap-below` | Math 2 | margin: 6px 0 0 where `figure .mm-cap-below` |
| `.mm-caprow` | **none of the nine** | display: grid<br>grid-template-columns: repeat(var(--n),1fr)<br>margin: 0 0 6px |
| `.mm-cbody` | Cult 23 | column-count (by width): 3 where `.mm-albums-c .mm-cbody` ; 1 where `.mm-albums-c .mm-cbody` at (max-width:640px)<br>column-gap: 40px where `.mm-albums-c .mm-cbody`<br>padding: 14px 0 6px where `.mm-albums-c .mm-cbody` |
| `.mm-centre` | Cult 23 | border-bottom: 1px solid #D9C9AB where `.mm-albums-c details.mm-centre`<br>padding: 10px 0 where `.mm-albums-c details.mm-centre` |
| `.mm-cf` | Math 12 | display: flex at (max-width:640px)<br>flex-direction: column at (max-width:640px)<br>position: relative |
| `.mm-cols2` | Math 1 | column-count: 1 ! at (max-width:640px)<br>column-gap: 40px<br>columns: 2<br>padding-left: 62px ! |
| `.mm-cols3` | Cult 1, Math 2 | column-gap: 40px<br>display: grid<br>grid-template-columns (by width): repeat(3,1fr) ; 1fr at (max-width:640px)<br>margin: 0 0 12px |
| `.mm-contain` | **none of the nine** | background: #fff where `.pim.mm-contain` |
| `.mm-cset` | **none of the nine** | align-items: start<br>column-gap: 24px<br>display: grid<br>grid-template-columns (by width): calc(50% - var(--hw) - 24px) 1fr ; 1fr at (max-width:640px)<br>margin: 0 0 12px |
| `.mm-ctr` | **none of the nine** | margin-left: 0 !<br>margin-right: 0 !<br>text-align: center |
| `.mm-dots` | **none of the nine** | display (by width): none ; flex at (max-width:830px)<br>gap: 6px at (max-width:830px)<br>justify-content: center at (max-width:830px)<br>margin: 8px 0 4px at (max-width:830px) |
| `.mm-float` | Aun 2, Bio 7, SRes 6, Cult 2, RoA 3, Sens 5 | clear (by condition): right ; left where `.mm-float.mm-left` ; right where `blockquote.pullquote .mm-float`<br>float (by width and condition): right ; left where `.mm-float.mm-left` ; none at (max-width:830px) ; none where `.mm-float.mm-left` at (max-width:830px) ; right where `blockquote.pullquote .mm-float`<br>margin (by width and condition): 4px 0 12px 32px ; 4px 32px 12px 0 where `.mm-float.mm-left` ; 12px 0 at (max-width:830px) ; 12px 0 where `.mm-float.mm-left` at (max-width:830px) ; 4px 0 12px 32px where `blockquote.pullquote .mm-float`<br>margin-top: 0 ! where `blockquote.pullquote + p.mm-gl + .mm-float` at (max-width:830px) |
| `.mm-flow` | Math 147, PL 163 | flex: 0 0 auto where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin-bottom: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin-left (by width and condition): var(--gl,0px) ! where `.mm-pdf figure.mm-pdff.mm-flow` ; 0 ! where `.mm-pdf-row .mm-pdfin>figure.mm-pdff.mm-flow` at (max-width:640px)<br>margin-right: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin-top: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>position: relative where `.mm-pdf figure.mm-pdff.mm-flow` |
| `.mm-formula` | Sens 1 | align-items: flex-start where `.mm-set.mm-formula` |
| `.mm-g2` | Math 1 | column-gap: 40px<br>display: grid<br>grid-template-columns (by width): 1fr 1fr ; 1fr ! at (max-width:640px)<br>margin: 0 0 12px<br>row-gap: 28px |
| `.mm-g2c` | Math 4 | align-items: start<br>column-gap: 20px<br>display: grid<br>grid-template-columns (by width): minmax(0,280px) auto ; 1fr ! at (max-width:640px)<br>justify-content: start<br>margin-top: var(--g2gap) where `.mm-g2col>.mm-g2c+.mm-g2c` |
| `.mm-g2col` | **none of the nine** | display: flex<br>flex-direction: column<br>row-gap: 0 |
| `.mm-gl` | Aun 9, Cult 1, PL 39, Sens 6 | background (by condition): #D9C9AB ; none ! where `p.mm-gl.mm-gl-bq` ; none ! where `blockquote.pullquote + p.mm-gl`<br>background-clip: content-box<br>box-sizing: content-box<br>display: flow-root<br>font-size (by condition): 2px ! ; 0 ! where `p.mm-gl.mm-gl-bq` ; 0 ! where `blockquote.pullquote + p.mm-gl`<br>height (by condition): 2px ; 0 ! where `p.mm-gl.mm-gl-bq` ; 0 ! where `blockquote.pullquote + p.mm-gl`<br>line-height (by condition): 2px ! ; 0 ! where `p.mm-gl.mm-gl-bq` ; 0 ! where `blockquote.pullquote + p.mm-gl`<br>min-height (by condition): 0 ! where `p.mm-gl.mm-gl-bq` ; 0 ! where `blockquote.pullquote + p.mm-gl`<br>overflow: hidden<br>text-align: start !<br>text-indent: 0 ! |
| `.mm-gl-bq` | **none of the nine** | background: none ! where `p.mm-gl.mm-gl-bq`<br>font-size: 0 ! where `p.mm-gl.mm-gl-bq`<br>height: 0 ! where `p.mm-gl.mm-gl-bq`<br>line-height: 0 ! where `p.mm-gl.mm-gl-bq`<br>min-height: 0 ! where `p.mm-gl.mm-gl-bq` |
| `.mm-hang` | **none of the nine** | padding-left (by width and condition): 0 ! where `p.mm-hang.mm-hang` at (max-width:640px) ; var(--hang) !<br>text-indent (by width and condition): 0 ! where `p.mm-hang.mm-hang` at (max-width:640px) ; calc(var(--ind, 0px) - var(--hang)) ! |
| `.mm-hc-0000FF` | Math 1 | color: #0000FF ! where `.mm-hc-0000FF:not(h2)` |
| `.mm-hc-008F00` | Sens 2 | color: #008F00 ! where `.mm-hc-008F00:not(h2)` |
| `.mm-hc-00B050` | SRes 4, Cult 9, Math 8 | border-bottom: 0 !<br>color (by condition): #00B050 ! where `.mm-hc-00B050:not(h2)` ; #00B050 !<br>font-size (by width): 20px ! ; 19px ! at (max-width:640px)<br>font-weight: 400 !<br>padding-bottom: 0 ! |
| `.mm-hc-0432FF` | Cult 27, Math 8, PL 22, Sens 3 | border-bottom: 0 !<br>color (by condition): #0432FF ! ; #0432FF ! where `.mm-hc-0432FF:not(h2)`<br>font-size: 18px !<br>font-weight: 400 !<br>padding-bottom: 0 ! |
| `.mm-hc-2CC171` | Math 1 | color: #2CC171 ! where `.mm-hc-2CC171:not(h2)` |
| `.mm-hc-521B93` | Sens 2 | color: #521B93 ! where `.mm-hc-521B93:not(h2)` |
| `.mm-hc-66CCFF` | Math 1 | color: #66CCFF ! where `.mm-hc-66CCFF:not(h2)` |
| `.mm-hc-7030A0` | Math 2 | color: #7030A0 ! where `.mm-hc-7030A0:not(h2)` |
| `.mm-hc-797979` | Sens 2 | color: #797979 ! where `.mm-hc-797979:not(h2)` |
| `.mm-hc-945200` | Sens 2 | color: #945200 ! where `.mm-hc-945200:not(h2)` |
| `.mm-hc-996633` | Math 1 | color: #996633 ! where `.mm-hc-996633:not(h2)` |
| `.mm-hc-CC66FF` | Math 1 | color: #CC66FF ! where `.mm-hc-CC66FF:not(h2)` |
| `.mm-hc-ED2AFB` | Math 1 | color: #ED2AFB ! where `.mm-hc-ED2AFB:not(h2)` |
| `.mm-hc-EE0000` | Cult 32, Math 7, RoA 1, Sens 34 | border-bottom: 0 !<br>color (by condition): #EE0000 ! ; #EE0000 ! where `.mm-hc-EE0000:not(h2)`<br>font-size: 18px !<br>font-weight: 400 !<br>padding-bottom: 0 ! |
| `.mm-hc-FB0207` | Math 4 | color: #FB0207 ! where `.mm-hc-FB0207:not(h2)` |
| `.mm-hc-FBEF32` | Math 1 | color: #FBEF32 ! where `.mm-hc-FBEF32:not(h2)` |
| `.mm-hc-FF0000` | Sens 3 | border-bottom: 0 !<br>color (by condition): #FF0000 ! ; #FF0000 ! where `.mm-hc-FF0000:not(h2)`<br>font-size: 18px !<br>font-weight: 400 !<br>padding-bottom: 0 ! |
| `.mm-hc-FF3FFF` | Sens 2 | color: #FF3FFF ! where `.mm-hc-FF3FFF:not(h2)` |
| `.mm-hc-FF9300` | Sens 2 | color: #FF9300 ! where `.mm-hc-FF9300:not(h2)` |
| `.mm-hc-FFDD60` | Sens 3 | color: #FFDD60 ! where `.mm-hc-FFDD60:not(h2)` |
| `.mm-hc-FFFFFF` | Math 1 | color: #FFFFFF ! where `.mm-hc-FFFFFF:not(h2)` |
| `.mm-hs` | **none of the nine** | background-position: center where `.hero>.mm-hs`<br>background-size: cover where `.hero>.mm-hs`<br>inset: 0 where `.hero>.mm-hs`<br>opacity (by condition): 0 where `.hero>.mm-hs` ; 1 where `.hero>.mm-hs.on`<br>position: absolute where `.hero>.mm-hs`<br>transition: opacity 1.2s ease where `.hero>.mm-hs`<br>z-index: 0 where `.hero>.mm-hs` |
| `.mm-imgs` | Jour 34, Aun 15, Bio 11, SRes 8, Cult 58, Math 61, PL 44, RoA 3, Sens 72 | align-items: flex-start where `.mm-set .mm-imgs`<br>display (by width and condition): contents where `.mm-row .mm-imgs` ; flex where `.mm-set .mm-imgs` ; flex where `.mm-cset>.mm-imgs` ; flex where `.mm-set .mm-imgs` at (max-width:830px) ; none where `.mm-set .mm-imgs::-webkit-scrollbar` at (max-width:830px) ; contents where `.mm-row .mm-imgs` at (max-width:830px)<br>flex (by condition): 1 1 auto where `.mm-set .mm-imgs` ; none where `.mm-set.mm-intro .mm-imgs` ; none where `.mm-set.mm-formula .mm-imgs`<br>gap (by width and condition): 24px where `.mm-set .mm-imgs` ; 16.8px ! where `.mm-set[data-grid] .mm-imgs` ; 10px where `.mm-set .mm-imgs` at (max-width:830px)<br>justify-content (by width and condition): center where `.mm-set .mm-imgs` ; flex-end where `.mm-set.mm-col .mm-imgs` ; flex-end where `.mm-set.mm-intro .mm-imgs` ; flex-end where `.mm-set[data-align=right] .mm-imgs` ; flex-end where `.mm-set[data-at=right] .mm-imgs` ; flex-start where `.mm-set.mm-formula .mm-imgs` ; flex-start ! where `.mm-row[data-left] .mm-imgs` ; flex-start where `.mm-cset>.mm-imgs` ; center where `.mm-cset>.mm-imgs` at (max-width:640px) ; center where `.mm-g2c>.mm-imgs` at (max-width:640px) ; flex-start ! where `.mm-set .mm-imgs` at (max-width:830px)<br>margin: 12px 0 0 ! where `.mm-set .mm-imgs` at (max-width:830px)<br>margin-left (by width and condition): 32px where `.mm-set.mm-intro .mm-imgs` ; 48px where `.mm-set.mm-formula .mm-imgs` ; 0 where `.mm-set.mm-intro .mm-imgs` at (max-width:830px) ; 0 where `.mm-set.mm-formula .mm-imgs` at (max-width:830px)<br>min-width: 0 where `.mm-set .mm-imgs`<br>overflow-x: auto where `.mm-set .mm-imgs` at (max-width:830px)<br>scroll-snap-type: x mandatory where `.mm-set .mm-imgs` at (max-width:830px)<br>scrollbar-width: none where `.mm-set .mm-imgs` at (max-width:830px) |
| `.mm-inner` | Math 2 | padding-left: 93px ! |
| `.mm-left` | **none of the nine** | clear: left where `.mm-float.mm-left`<br>float (by width): left where `.mm-float.mm-left` ; none where `.mm-float.mm-left` at (max-width:830px)<br>margin (by width): 4px 32px 12px 0 where `.mm-float.mm-left` ; 12px 0 where `.mm-float.mm-left` at (max-width:830px) |
| `.mm-lineabove` | Math 4 | background: linear-gradient(#D9C9AB,#D9C9AB) no-repeat 0 var(--ly,0px)/100% 2px<br>border-top (by condition): 2px solid #D9C9AB where `.micro-label.mm-lineabove` ; 0 !<br>padding-top (by condition): 28px where `.micro-label.mm-lineabove` ; 28px ! |
| `.mm-name` | Aun 9, Math 47, PL 17 | border-top (by condition): **competing**: 0 ! wins over 2px solid #D9C9AB ; 0 ! where `p.mm-name.mm-noline`<br>color: #0432FF !<br>font-size (by condition): 20px ! ; 20px ! where `p.mm-name:not(.mm-gl):not(.mm-cap)`<br>font-weight (competing): **competing**: 400 ! wins over <br>margin-top: 24px<br>padding-top (competing): **competing**: 0 ! wins over 28px |
| `.mm-noline` | Math 24, PL 1 | border-top: 0 ! where `p.mm-name.mm-noline` |
| `.mm-notes` | **none of the nine** | margin-bottom: 8px ! where `blockquote.pullquote.mm-notes`<br>margin-top: 8px ! where `blockquote.pullquote.mm-notes` |
| `.mm-pcap` | Math 8 | bottom: 100%<br>left: 0<br>margin (by width): 0 0 6px ! ; 0 0 6px ! at (max-width:640px)<br>position (by width): absolute ; static ! at (max-width:640px)<br>text-align: center at (max-width:640px)<br>white-space (by width): nowrap ; normal ! at (max-width:640px)<br>width: auto ! at (max-width:640px) |
| `.mm-pdf` | Math 57, PL 44 | align-items: flex-end at (max-width:640px)<br>display: flex at (max-width:640px)<br>flex-wrap: wrap at (max-width:640px)<br>float: none ! at (max-width:640px)<br>gap: 10px at (max-width:640px)<br>height: auto ! at (max-width:640px)<br>justify-content: center at (max-width:640px)<br>margin: 14px 0 ! at (max-width:640px)<br>position: relative<br>width: auto ! at (max-width:640px) |
| `.mm-pdf-l` | **none of the nine** | clear (by width): left ; both ! at (min-width:641px) and (max-width:830px)<br>float (by width): left ; none ! at (min-width:641px) and (max-width:830px)<br>margin-bottom: 0<br>margin-left: 0 ! at (min-width:641px) and (max-width:830px)<br>margin-right (by width): 24px ; auto ! at (min-width:641px) and (max-width:830px)<br>padding-top: 30px where `.mm-pdf-l:has(.mm-cap:not(.mm-cap-below))`<br>z-index: 1 |
| `.mm-pdf-r` | Math 32, PL 21 | clear (by width): right ; both ! at (min-width:641px) and (max-width:830px)<br>float (by width): right ; none ! at (min-width:641px) and (max-width:830px)<br>margin-bottom: 0<br>margin-left (by width): 24px ; auto ! at (min-width:641px) and (max-width:830px)<br>margin-right (by width): 0 ! at (min-width:641px) ; 0 ! at (min-width:641px) and (max-width:830px)<br>padding-top: 30px where `.mm-pdf-r:has(.mm-cap:not(.mm-cap-below))`<br>z-index: 1 |
| `.mm-pdf-row` | Math 25, PL 23 | clear: both |
| `.mm-pdfbr` | **none of the nine** | display: none at (max-width:640px) |
| `.mm-pdff` | Math 149, PL 163 | flex: 0 0 auto where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin: 0 ! where `.mm-pdf figure.mm-pdff`<br>margin-bottom: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin-left (by width and condition): var(--gl,0px) ! where `.mm-pdf figure.mm-pdff.mm-flow` ; 0 ! where `.mm-pdf-row .mm-pdfin>figure.mm-pdff.mm-flow` at (max-width:640px)<br>margin-right: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>margin-top: 0 ! where `.mm-pdf figure.mm-pdff.mm-flow`<br>padding: 0 where `.mm-pdf figure.mm-pdff`<br>position (by width and condition): absolute where `.mm-pdf figure.mm-pdff` ; relative where `.mm-pdf figure.mm-pdff.mm-flow` ; static ! where `.mm-pdf figure.mm-pdff` at (max-width:640px)<br>width: auto ! where `.mm-pdf figure.mm-pdff` at (max-width:640px) |
| `.mm-pdfflow` | Math 55, PL 44 | align-items: flex-start<br>display: flex<br>width: max-content |
| `.mm-pdfin` | Math 57, PL 44 | align-items (by condition): flex-end where `.mm-pdf-row .mm-pdfin` at (max-width:640px) ; flex-end where `.mm-pdf .mm-pdfin` at (max-width:640px)<br>display (by condition): contents at (max-width:640px) ; flex where `.mm-pdf-row .mm-pdfin` at (max-width:640px)<br>flex-wrap: wrap where `.mm-pdf-row .mm-pdfin` at (max-width:640px)<br>gap: 10px where `.mm-pdf-row .mm-pdfin` at (max-width:640px)<br>justify-content: center where `.mm-pdf-row .mm-pdfin` at (max-width:640px)<br>margin-left: 0 ! where `.mm-pdf-row .mm-pdfin` at (max-width:640px)<br>position: relative |
| `.mm-pdfsp` | **none of the nine** | display (by width): none ! at (max-width:640px) ; none ! at (min-width:641px) and (max-width:830px) |
| `.mm-pf` | Math 8 | display: flex at (max-width:640px)<br>flex-direction: column at (max-width:640px)<br>position: relative |
| `.mm-pfig` | **none of the nine** | clear: right where `.mm-pwrap .mm-pfig`<br>display: flex where `.mm-pwrap .mm-pfig`<br>float (by width): right where `.mm-pwrap .mm-pfig` ; none where `.mm-pwrap .mm-pfig` at (max-width:640px)<br>gap: 24px where `.mm-pwrap .mm-pfig`<br>justify-content: flex-start where `.mm-pwrap .mm-pfig` at (max-width:640px)<br>margin (by width): 0 0 0 24px where `.mm-pwrap .mm-pfig` ; 12px 0 0 where `.mm-pwrap .mm-pfig` at (max-width:640px) |
| `.mm-ph1` | PL 14 | margin-top: 1px ! at (max-width:640px) |
| `.mm-ph11` | PL 5 | margin-top: 11px ! at (max-width:640px) |
| `.mm-ph26` | **none of the nine** | margin-top: 26px ! at (max-width:640px) |
| `.mm-pspacer` | **none of the nine** | display: none where `.mm-pwrap .mm-pspacer` at (max-width:640px)<br>float: right where `.mm-pwrap .mm-pspacer`<br>height: 0 where `.mm-pwrap .mm-pspacer`<br>width: 0 where `.mm-pwrap .mm-pspacer` |
| `.mm-pwrap` | **none of the nine** | display: flow-root |
| `.mm-red` | Math 1 | color: #EE0000 ! where `.micro-label.mm-red`<br>font-size: 20px ! where `.micro-label.mm-red`<br>font-weight: 400 ! where `.micro-label.mm-red` |
| `.mm-row` | Jour 34, Aun 13, Bio 4, SRes 2, Cult 51, Sens 30 | align-items: flex-start<br>display (by width): flex ; **competing** at (max-width:830px): none wins over flex<br>flex-wrap: nowrap<br>gap (by width and condition): min(38.4px, calc((100vw - 80px) * 38.4 / 1140)) ; 10px at (max-width:830px) ; 19.2px ! where `.mm-row[data-level="10"]`<br>justify-content (by width and condition): center ; flex-start ! where `.mm-row[data-left]` ; flex-start ! at (max-width:830px)<br>margin (by width): 20px 0 ; 12px 0 0 ! at (max-width:830px)<br>margin-top: 24px where `.mm-row + .mm-row`<br>overflow-x: auto at (max-width:830px)<br>scroll-snap-type: x mandatory at (max-width:830px)<br>scrollbar-width: none at (max-width:830px) |
| `.mm-set` | Cult 5, Sens 37 | align-items (by condition): center ; flex-start where `.mm-set.mm-formula` ; flex-start where `main[data-spacing=table] .mm-set`<br>display (by width): flex ; block at (max-width:830px)<br>margin: 16px 0 |
| `.mm-sub` | Cult 30 | font-size (by width): 20px ! ; **competing** at (max-width:640px): 18px ! wins over 17px ! ; 18px ! at (min-width:641px) |
| `.mm-t` | Cult 53, Math 9, PL 2 | -moz-tab-size: 48px<br>display (by condition): none ! where `blockquote.pullquote p > .mm-t:first-child` ; none ! where `blockquote.pullquote p > span:first-child > .mm-t:first-child`<br>tab-size: 48px<br>white-space: pre |
| `.mm-tab1` | **none of the nine** | margin-left (by width): 48px ! ; 0 ! at (max-width:640px) |
| `.mm-tabcol` | Math 44 | display: block ! at (max-width:640px)<br>grid-template-columns: none ! at (max-width:640px)<br>white-space: normal ! at (max-width:640px) |
| `.mm-table` | PL 1 | border-collapse: collapse<br>border-top: 1px solid var(--rule) !<br>font-size: inherit<br>width: 100% |
| `.mm-table-wrap` | PL 1 | clear: both<br>margin: 24px 0<br>overflow-x: auto |
| `.mm-tabtail` | **none of the nine** | display: block ! at (max-width:640px)<br>grid-template-columns: none ! at (max-width:640px)<br>white-space: normal ! at (max-width:640px) |
| `.mm-text` | Cult 5, Math 4, Sens 37 | flex (by condition): 0 1 auto where `.mm-set .mm-text` ; 1 1 0 where `.mm-set.mm-intro .mm-text`<br>max-width: none ! where `.mm-set .mm-text` at (max-width:830px)<br>min-width: 0 where `.mm-set .mm-text`<br>text-align: left ! where `.mm-cset>.mm-text`<br>width: auto ! where `.mm-set .mm-text` at (max-width:830px) |
| `.mm-toc3` | SRes 1, RoA 1 | column-gap: 40px where `.toc .toc-grid.mm-toc3`<br>display: grid ! where `.toc .toc-grid.mm-toc3`<br>grid-template-columns (by width): repeat(2,1fr) ! where `.toc .toc-grid.mm-toc3` at (min-width:641px) ; repeat(3,1fr) where `.toc .toc-grid.mm-toc3` ; 1fr where `.toc .toc-grid.mm-toc3` at (max-width:640px) |
| `.mm-tocline` | PL 1 | background: #D9C9AB<br>border: 0<br>height: 2px<br>margin: 0<br>padding: 0 |
| `.mm-trio` | **none of the nine** | align-items: flex-start<br>clear: both<br>display: flex<br>flex-wrap: wrap at (max-width:640px)<br>gap (by width): 0 ; 12px at (max-width:640px)<br>justify-content: center at (max-width:640px) |
| `.mm-wc` | Cult 14, Math 10 | font-weight: 400 ! where `.micro-label.mm-wc` |
| `.mm-wcols2` | Math 1 | align-items: start<br>column-gap: 40px<br>display: grid<br>grid-template-columns (by width): 1fr 1fr ; 1fr at (max-width:640px) |
| `.mq` | **none of the nine** | font-family: var(--display)<br>font-size: 17px<br>font-style: italic<br>font-weight: 400<br>line-height: 1.65<br>margin (by width): 24px 38px ; 20px 0 at (max-width:640px)<br>margin-left (by width): 20px ! ; 0 ! at (max-width:640px)<br>margin-right (by width): 20px ! ; 0 ! at (max-width:640px)<br>padding: 0 |
| `.np` | Jour 74, Aun 74, Bio 74, SRes 74, Cult 74, Math 74, PL 74, RoA 74, Sens 74 | color (by width and condition): var(--ink) where `.grp .np` ; var(--ink) where `.grp li.lead .np` ; #0432FF where `.panel.cat .grp li.lead .np` ; #E7EEF5 where `.grp .np` at (max-width:960px) ; #fff where `.grp li.lead .np` at (max-width:960px) ; #8FC6FF where `.panel.cat .grp li.lead .np` at (max-width:960px) ; #0432FF ! where `.panel .grp li.lead > .np` at (min-width:831px) ; #2B2B2B ! where `.panel .grp li:not(.lead):not(.hd) > .np` at (min-width:831px)<br>cursor: default where `.grp .np`<br>display: block where `.grp .np`<br>font-family: var(--serif) where `.grp .np`<br>font-size (by width): 17px where `.grp .np` ; 17px where `.grp .np` at (max-width:960px) ; 18px ! where `.grp .np` at (min-width:641px) ; 17px ! where `.grp .np` at (max-width:640px)<br>font-weight (by width and condition): 400 where `.grp li.lead .np` ; 400 ! where `.panel .grp li.lead > .np` at (min-width:831px) ; 400 ! where `.panel .grp li:not(.lead):not(.hd) > .np` at (min-width:831px)<br>line-height: 1.3 where `.grp .np`<br>padding (by width): 8px 0 where `.grp .np` ; 7px 0 where `.grp .np` at (max-width:960px) |
| `.np-top` | **none of the nine** | color: #fff where `.menu .top.np-top:hover`<br>cursor (by width): default where `.menu .top.np-top` ; pointer where `.menu .top.np-top` at (max-width:960px) |
| `.on` | **none of the nine** | background: var(--ink) where `.mm-dots span.on` at (max-width:830px)<br>opacity: 1 where `.hero>.mm-hs.on` |
| `.op` | Sens 11 | border-top: 0 where `.formula-table tr.rule td.op`<br>padding-right: 12px where `.formula-table td.op`<br>width: 1.2em where `.formula-table td.op` |
| `.open` | **none of the nine** | display (by width and condition): block where `.site-nav.open` at (max-width:960px) ; flex where `.lightbox.open` |
| `.over` | **none of the nine** | grid-column: 1 / -1 where `.panel-in > .pcol.over`<br>margin-bottom (by width): -12px where `.panel-in > .pcol.over` ; 0 where `.panel-in > .pcol.over` at (max-width:960px) |
| `.page-h2` | **none of the nine** | border-bottom: 2px solid var(--head)<br>color: var(--head)<br>font-family: var(--serif)<br>font-size: 24px<br>font-weight: 500<br>line-height: 1.2<br>margin: 40px 0 16px<br>padding-bottom: 8px |
| `.panel` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | background (by width): #fff ; transparent at (max-width:960px) ; #F5EEE3 ! at (min-width:831px)<br>border: 0 at (max-width:960px)<br>border-bottom (competing): **competing**: 0 ! wins over 1px solid var(--line)<br>box-shadow (by width): 0 14px 28px rgba(20,30,40,.14) ; none at (max-width:960px)<br>display (by width and condition): none ; **competing** where `.has-panel:focus-within > .panel`: none wins over block ; block where `.has-panel.open > .panel` ; none where `.has-panel:focus-within > .panel` at (max-width:960px) ; block where `.has-panel.open > .panel` at (max-width:960px)<br>flex: 0 0 100% at (max-width:960px)<br>left: 0<br>position (by width): absolute ; static at (max-width:960px)<br>right: 0<br>top: 100% |
| `.panel-in` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | display (by width): grid ; block at (max-width:960px)<br>gap (by condition): 26px 48px ; 26px 40px where `.panel-in.c4`<br>grid-template-columns (by condition): repeat(3,minmax(0,1fr)) ; minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) where `.panel-in.c1` ; repeat(4,minmax(0,1fr)) where `.panel-in.c4`<br>margin: 0 auto<br>max-width: 1280px<br>padding (by width): 26px 40px 30px ; 0 0 10px 14px at (max-width:960px) |
| `.pcol` | Jour 25, Aun 25, Bio 25, SRes 25, Cult 25, Math 25, PL 25, RoA 25, Sens 25 | display (by width): flex where `.panel-in > .pcol` ; block where `.panel-in > .pcol` at (max-width:960px)<br>flex-direction: column where `.panel-in > .pcol`<br>gap: 22px where `.panel-in > .pcol`<br>grid-column: 1 / -1 where `.panel-in > .pcol.over`<br>margin-bottom (by width): -12px where `.panel-in > .pcol.over` ; 0 where `.panel-in > .pcol.over` at (max-width:960px)<br>margin-top (by condition): 24px where `.panel-in > .pcol + .pcol` at (max-width:960px) ; 0 where `#p-resources .panel-in > .pcol + .pcol` at (max-width:960px)<br>min-width: 0 where `.panel-in > .pcol` |
| `.pdf` | SRes 8, RoA 17 | display (by condition): block ! where `.res-item:has(> .meta:last-child > a.pdf:last-child)` at (max-width:640px) ; block ! where `.res-item:has(> a.pdf:last-child)` at (max-width:640px) ; inline ! where `.res-item > .meta:last-child > a.pdf:last-child` at (max-width:640px) ; inline ! where `.res-item > a.pdf:last-child` at (max-width:640px)<br>margin-left (by condition): 24px ! where `.res-item > .meta:last-child > a.pdf:last-child` at (max-width:640px) ; 24px ! where `.res-item > a.pdf:last-child` at (max-width:640px) |
| `.ph` | Jour 152, Aun 58, Bio 21, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | flex (by width and condition): none ; none where `.mm-trio>figure.ph` ; none where `.mm-trio>figure.ph` at (max-width:640px)<br>margin (by condition): 0 ; 0 where `.mm-trio>figure.ph` ; 0 where `.mm-pwrap .mm-pfig figure.ph`<br>min-width: 0<br>scroll-snap-align: center where `.mm-imgs .ph` at (max-width:830px) |
| `.pim` | Jour 152, Aun 58, Bio 22, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | --mh (by condition): none where `.mm-pdf .pim` ; none where `.mm-g2c .pim`<br>align-items: flex-start where `figure.ph > div:not(.pim):has(> .pim + .pim)`<br>background (by condition): transparent where `.ph .pim` ; #fff where `.pim.mm-contain`<br>border-radius (competing): **competing** where `.ph .pim`: 6px wins over 2px<br>display: flex where `figure.ph > div:not(.pim):has(> .pim + .pim)`<br>flex: none where `figure.ph > div:not(.pim) > .pim`<br>height (by width and condition): calc(var(--mh,153) * 1px) where `.mm-imgs .pim` ; auto where `.mm-float .pim` ; var(--mh,168px) where `.mm-trio .pim` ; 110px where `.mm-trio .pim` at (max-width:640px) ; calc(var(--mh,140) * 1px) where `.mm-pwrap .mm-pfig .pim` ; auto ! where `.mm-pdf .pim` at (max-width:640px) ; 168px where `.mm-cset>.mm-imgs .pim` ; 168px where `.mm-g2c .pim` ; auto ! where `.mm-g2c .pim` at (max-width:640px) ; calc(var(--hp,180) * 1px) ! where `.mm-imgs .pim` at (max-width:830px) ; 70px ! where `.mm-set.mm-col .mm-imgs .pim` at (max-width:830px) ; 240px ! where `.mm-set.mm-intro .mm-imgs .pim` at (max-width:830px) ; auto ! where `.mm-set.mm-formula .mm-imgs .pim` at (max-width:830px) ; 150px ! where `.mm-float .pim` at (min-width:831px)<br>margin-left (by width and condition): auto ! where `.mm-g2c .pim` at (max-width:640px) ; calc(var(--mh,153) * 24px / 170) where `figure.ph > div:not(.pim) > .pim + .pim`<br>margin-right: auto ! where `.mm-g2c .pim` at (max-width:640px)<br>max-height (by condition): none ! where `.mm-pdf .pim` ; none ! where `.mm-g2c .pim`<br>max-width (by width and condition): none ! where `.mm-pdf .pim` ; none ! where `.mm-g2c .pim` ; min(100%,400px) ! where `.mm-g2c .pim` at (max-width:640px)<br>overflow (by condition): hidden where `.ph .pim` ; hidden where `.pim[data-trim]`<br>position (by condition): relative where `.ph .pim` ; relative<br>width (by width and condition): auto where `.mm-imgs .pim` ; auto where `.mm-trio .pim` ; auto where `.mm-trio .pim` at (max-width:640px) ; auto where `.mm-pwrap .mm-pfig .pim` ; 44vw ! where `.mm-pdf .pim` at (max-width:640px) ; auto where `.mm-cset>.mm-imgs .pim` ; auto where `.mm-g2c .pim` ; min(300px, 100%) ! where `.mm-set.mm-formula .mm-imgs .pim` at (max-width:830px) ; auto ! where `.mm-float .pim` at (min-width:831px) |
| `.preview-grid` | Sens 1 | column-gap: 24px<br>display: grid<br>grid-auto-flow (by width): column ; row at (max-width:640px)<br>grid-template-columns (by width): 1fr 1fr ; 1fr at (max-width:640px)<br>grid-template-rows (by width): repeat(7,auto) ; none at (max-width:640px) |
| `.preview-line` | Sens 15 | color: var(--ink)<br>font-size: 17px<br>font-style: italic<br>margin: 8px 0 |
| `.pullquote` | SRes 2, Cult 1, Math 6, PL 15, Sens 2 | background: none ! where `p.mm-gl:has(+ blockquote.pullquote)`<br>border: none<br>clear (by condition): both ; none where `blockquote.pullquote.beside-photo`<br>font-family: var(--display)<br>font-size (by width and condition): **competing**: 18px ! wins over  ; 17px ! at (max-width:830px) ; 0 ! where `p.mm-gl:has(+ blockquote.pullquote)`<br>height: 0 ! where `p.mm-gl:has(+ blockquote.pullquote)`<br>line-height (by width and condition): **competing**: 40px ! wins over 43.2px, 43.2px ! ; **competing** at (max-width:640px): 42px ! wins over  ; 38px ! at (max-width:830px) ; 0 ! where `p.mm-gl:has(+ blockquote.pullquote)`<br>margin (by width): **competing**: 24px 38px ! wins over 24px 0 !, 32px auto ; 20px 0 ! at (max-width:640px)<br>margin-bottom: 8px ! where `blockquote.pullquote.mm-notes`<br>margin-left (by width): **competing**: 0 ! wins over 20px !, 38px ! ; 0 ! at (max-width:640px)<br>margin-right (by width): **competing**: 0 ! wins over 20px !, 38px ! ; 0 ! at (max-width:640px)<br>margin-top: 8px ! where `blockquote.pullquote.mm-notes`<br>max-width (by width): **competing**: none ! wins over 90% ; 100% at (max-width:640px)<br>min-height: 0 ! where `p.mm-gl:has(+ blockquote.pullquote)`<br>padding: 0<br>position: relative<br>text-align: left |
| `.ref-desc` | Sens 16 | color: var(--ink)<br>flex: 1 |
| `.ref-label` | Sens 16 | font-weight: 400 ! where `.touch-table .ref-row:not(.touch-head) .ref-label` |
| `.ref-row` | Sens 16 | border-bottom (by condition): 1px solid var(--rule) ; 0 where `.ref-table:not(.touch-table) .ref-row:not(:last-child)`<br>display: flex<br>flex-direction: column at (max-width:640px)<br>gap (by width): 24px ; 4px at (max-width:640px)<br>padding: 16px 0 |
| `.ref-table` | Sens 2 | border-top: 1px solid var(--rule)<br>clear: both<br>margin-top: 8px |
| `.res-title` | SRes 21, RoA 25 | display (by condition): inline ! where `.res-item:has(> .meta:last-child > a.pdf:last-child) > .res-title` at (max-width:640px) ; inline ! where `.res-item:has(> a.pdf:last-child) > .res-title` at (max-width:640px) |
| `.section` | Jour 1, Aun 1, Bio 1, SRes 4, Cult 36, Math 28, PL 2, RoA 1, Sens 15 | border-top (competing): **competing**: 0 wins over 1px solid var(--ink)<br>clear: both<br>container-type: inline-size<br>margin-top (by width and condition): **competing**: 48px wins over 64px ; **competing** where `.section:first-of-type`: 32px wins over 40px ; 72px where `section.section.sense` ; 56px where `section.section.sense` at (max-width:640px)<br>padding-top (competing): **competing**: 0 wins over 24px |
| `.sense` | Sens 4 | margin-top (by width): 72px where `section.section.sense` ; 56px where `section.section.sense` at (max-width:640px) |
| `.seq-line` | Sens 2 | padding-left (by width): 48px ; 24px at (max-width:640px) |
| `.site-foot` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: transparent !<br>border-top (by condition): **competing**: 0 ! wins over 1px solid var(--line) ; 0 where `.mc-band + .site-foot`<br>margin-top (by condition): **competing**: 0 ! wins over 24px ; 0 where `.mc-band + .site-foot` |
| `.site-foot-in` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items (by width): center ; flex-start at (max-width:640px)<br>color (by condition): var(--quiet) ; #6B6B6B ! where `.site-foot .site-foot-in`<br>display: flex<br>flex-direction: column at (max-width:640px)<br>font-size (by width): 15px ; 15px ! at (min-width:641px) ; 15px ! at (max-width:640px)<br>gap: 16px<br>justify-content: space-between<br>margin: 0 auto<br>max-width: var(--page)<br>padding (by width): 32px var(--gutter) 48px ; 28px 24px 40px at (max-width:640px)<br>padding-bottom (by width and condition): **competing**: 14px ! wins over 28px ! ; 17.625px ! where `.site-foot .site-foot-in` at (min-width:641px)<br>padding-top (by width and condition): **competing**: 14px ! wins over 0 ! ; 17.625px ! where `.site-foot .site-foot-in` at (min-width:641px) |
| `.site-head` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: var(--navy)<br>position: sticky<br>top: env(safe-area-inset-top,0px)<br>z-index: 40 |
| `.site-head-in` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display: flex<br>gap (by width): 24px ; 14px at (min-width:961px) and (max-width:1279px) ; 12px at (min-width:961px) and (max-width:1023px)<br>height (by width): 76px ; 60px at (max-width:960px)<br>justify-content: space-between<br>margin: 0 auto<br>max-width: 1280px<br>padding (by width): 0 40px ; 0 24px at (max-width:1180px) ; 0 8px 0 18px at (max-width:960px) ; 0 24px at (min-width:961px) and (max-width:1279px) ; 0 18px at (min-width:961px) and (max-width:1023px)<br>padding-left: 16px ! at (min-width:961px) and (max-width:1099px)<br>padding-right: 16px ! at (min-width:961px) and (max-width:1099px) |
| `.site-name` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color: #fff<br>font-family: var(--display)<br>font-size (by width): 25px ; 21px at (max-width:960px) ; 25px ! at (min-width:641px) ; 21px ! at (max-width:640px)<br>font-weight: 500<br>text-decoration: none<br>white-space: nowrap |
| `.site-nav` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: var(--navy) at (max-width:960px)<br>box-shadow: 0 12px 24px rgba(0,0,0,.18) at (max-width:960px)<br>display (by condition): none at (max-width:960px) ; block where `.site-nav.open` at (max-width:960px)<br>left: 0 at (max-width:960px)<br>max-height: calc(100vh - 60px) at (max-width:960px)<br>overflow-y: auto at (max-width:960px)<br>padding: 4px 18px 16px at (max-width:960px)<br>position: absolute at (max-width:960px)<br>right: 0 at (max-width:960px)<br>top: 60px at (max-width:960px) |
| `.site-tools` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display: flex<br>gap: 2px |
| `.skip` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: #fff where `.skip:focus`<br>left (by condition): -9999px ; 12px where `.skip:focus`<br>padding: 8px 12px where `.skip:focus`<br>position: absolute<br>top (by condition): 0 ; 12px where `.skip:focus`<br>z-index: 50 where `.skip:focus` |
| `.sub` | **none of the nine** | font-size (by width): 26px where `.hero h1 .sub` ; 19px where `.hero h1 .sub` at (max-width:640px)<br>margin-top: 6px where `.hero h1 .sub` |
| `.sub-label` | Jour 17, Sens 53 | color: var(--head) ! where `.sub-label.lbl-blue`<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',serif<br>font-size (by width): **competing**: 18px wins over 21px ; **competing** at (max-width:640px): 17px wins over 19px<br>font-weight (by condition): 400 ! ; 700 ! where `.sub-label.lbl-bold` ; 400 ! where `.sub-label.lbl-blue`<br>margin-bottom: 0<br>margin-top: 15px |
| `.sub-toggle` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | align-items: center<br>background: none<br>border: 0<br>color: #fff<br>cursor: pointer<br>display: inline-flex<br>height (by width): 30px ; 44px at (max-width:960px)<br>justify-content: center<br>margin-left (by width and condition): 1px ; 1px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>min-width: 13px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>opacity: .85<br>padding (by width and condition): 0 ; 0 ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>width (by width and condition): 22px ; 44px at (max-width:960px) ; 16px at (min-width:961px) and (max-width:1279px) ; 13px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px) |
| `.swatch` | Sens 1 | background: #fff<br>border: 1px solid #8F8F8F<br>border-radius: 50%<br>display: inline-block<br>height: .6em<br>margin-left: .28em<br>vertical-align: .04em<br>width: .6em |
| `.tight-bottom` | Sens 111 | margin-bottom: 5px |
| `.tight-top` | Sens 133 | margin-top: 5px |
| `.title-block` | **none of the nine** | padding: 56px 0 8px<br>text-align: center |
| `.toc-grid` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | column-gap: 40px where `.toc .toc-grid.mm-toc3`<br>display (by condition): grid ; grid ! where `.toc .toc-grid.mm-toc3`<br>gap: 6px 40px<br>grid-template-columns (by width and condition): 1fr 1fr ; 1fr at (max-width:640px) ; repeat(2,1fr) ! where `.toc .toc-grid.mm-toc3` at (min-width:641px) ; repeat(3,1fr) where `.toc .toc-grid.mm-toc3` ; 1fr where `.toc .toc-grid.mm-toc3` at (max-width:640px) |
| `.toc-label` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color: var(--head)<br>font-family: var(--serif)<br>font-size (by width and condition): **competing**: 22px ! wins over 24px ; **competing** at (max-width:640px): 19px ! wins over 20px !, 22px ; 22px ! where `.toc-wrap .toc-label` ; **competing** where `.toc-wrap .toc-label` at (max-width:640px): 19px ! wins over 20px ! ; 20px ! where `.toc-wrap .toc-label` at (min-width:641px) ; 20px ! where `.toc .toc-label` at (min-width:641px) ; 20px ! at (min-width:641px) ; 19px ! where `.toc .toc-label` at (max-width:640px)<br>font-weight: 500<br>line-height: 26px ! where `.toc .toc-col1 .toc-label`<br>margin (by condition): 0 0 14px ; 2px 0 0 ! where `.toc .toc-col1 .toc-label`<br>padding-bottom: 12px where `.toc .toc-col1 .toc-label` |
| `.toc-num` | **none of the nine** | color: var(--ink)<br>flex: 0 0 22px<br>font-size: 17px<br>font-variant-numeric: tabular-nums<br>font-weight: 600 |
| `.toc-rule-wrap` | Jour 1, Aun 1, Bio 1, Cult 1, Math 1, PL 1, Sens 1 | margin: 0 auto -2px<br>max-width: var(--page)<br>padding: 0 var(--gutter) |
| `.toc-wrap` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | display: none where `.toc-wrap:not(:has(li))`<br>margin: 0 auto<br>max-width: 1100px<br>padding (by width): 26px 0 36px ; 22px 24px 26px at (max-width:640px)<br>padding-bottom: 0 ! |
| `.top` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | border-bottom (by width): 0 where `.menu .top` ; 0 where `.menu .top` at (max-width:960px)<br>color (by condition): #fff where `.menu .top` ; #DCE6F0 where `.menu .top:hover` ; #fff where `.menu .top.np-top:hover`<br>cursor (by width): default where `.menu .top.np-top` ; pointer where `.menu .top.np-top` at (max-width:960px)<br>flex: 1 1 auto where `.menu .top` at (max-width:960px)<br>font-family: var(--serif) where `.menu .top`<br>font-size (by width): 17px where `.menu .top` ; 16px where `.menu .top` at (max-width:1180px) ; 18px where `.menu .top` at (max-width:960px) ; 16px where `.menu .top` at (min-width:961px) and (max-width:1023px) ; 18px ! where `.menu .top` at (min-width:641px) ; 17px ! where `.menu .top` at (max-width:640px)<br>font-weight: 400 where `.menu .top`<br>padding (by width): 6px 0 7.5px where `.menu .top` ; 13px 0 where `.menu .top` at (max-width:960px)<br>text-decoration (by width and condition): none where `.menu .top` ; underline where `.menu .top[aria-current="page"]` ; underline where `.menu .top[aria-current="page"]` at (max-width:960px)<br>text-underline-offset (by width): 4px where `.menu .top[aria-current="page"]` ; 4px where `.menu .top[aria-current="page"]` at (max-width:960px)<br>white-space: nowrap where `.menu .top` |
| `a` | Jour 44, Aun 44, Bio 48, SRes 74, Cult 83, Math 99, PL 60, RoA 79, Sens 52 | align-items: baseline where `.toc-groups a`<br>border-bottom: 1px solid transparent where `.toc a`<br>border-bottom-color: var(--head) where `.toc a:hover`<br>color (by width and condition): **competing**: var(--material) wins over var(--head) ; var(--ink) where `.grp a` ; var(--head) where `.grp a:hover` ; **competing** where `.grp li.lead a`: var(--ink) wins over var(--head) ; **competing** where `.grp a[aria-current="page"]`: var(--ink) wins over var(--head) ; var(--link) where `.toc a` ; var(--head) where `.toc a:hover` ; **competing** where `.site-foot a`: #6B6B6B ! wins over var(--quiet) ; #E7EEF5 where `.grp a` at (max-width:960px) ; #fff where `.grp li.lead a` at (max-width:960px) ; #fff where `.grp a[aria-current="page"]` at (max-width:960px) ; #0432FF ! where `a:not(.pdf)` ; #0432FF where `.panel.cat .grp li.lead a` ; #8FC6FF where `.panel.cat .grp li.lead a` at (max-width:960px) ; #E7EEF5 ! where `.panel .grp a[aria-current="page"]` at (max-width:960px) ; #8FC6FF ! where `#p-essentialelements .grp a[aria-current="page"]` at (max-width:960px) ; #8FC6FF ! where `#p-curriculum .grp a[aria-current="page"]` at (max-width:960px) ; #0432FF ! where `.panel .grp li.lead > a` at (min-width:831px) ; #2B2B2B ! where `.panel .grp li:not(.lead):not(.hd) > a` at (min-width:831px) ; #2B2B2B ! where `.panel .grp a[aria-current="page"]` at (min-width:831px)<br>display (by condition): block where `.grp a` ; flex where `.toc-groups a`<br>font-family: var(--serif) where `.grp a`<br>font-size (by width and condition): 17px where `.grp a` ; 19px where `.toc a` ; 17px where `.grp a` at (max-width:960px) ; **competing** where `.toc a` at (max-width:640px): 17px ! wins over 18px ; 18px ! where `.grp a` at (min-width:641px) ; 18px ! where `.toc a` at (min-width:641px) ; 15px ! where `.site-foot-in a` at (min-width:641px) ; 17px ! where `.grp a` at (max-width:640px) ; 15px ! where `.site-foot-in a` at (max-width:640px)<br>font-weight (by width and condition): **competing** where `.grp li.lead a`: 400 wins over 600 ; 400 where `.toc li.toc-area a` ; 400 where `.menu a` ; 400 ! where `.panel .grp li.lead > a` at (min-width:831px) ; 400 ! where `.panel .grp li:not(.lead):not(.hd) > a` at (min-width:831px)<br>gap: 8px where `.toc-groups a`<br>line-height (by condition): 1.3 where `.grp a` ; 1.35 where `.toc a`<br>outline (by condition): 2px solid var(--active) where `a:focus-visible` ; 2px solid #fff where `.site-head a:focus-visible`<br>outline-offset (by condition): 3px where `a:focus-visible` ; 3px where `.site-head a:focus-visible`<br>padding (by width): 8px 0 where `.grp a` ; 7px 0 where `.grp a` at (max-width:960px)<br>text-decoration (by condition): none where `.grp a` ; underline where `.grp a[aria-current="page"]` ; none where `.toc a` ; underline where `.grp a:hover`<br>text-underline-offset (by condition): 3px where `.grp a[aria-current="page"]` ; 3px where `.grp a:hover` |
| `b` | **none of the nine** | font-weight (by condition): 400 ! where `.mm-wcol b` ; 400 ! where `.mm-wc b` |
| `blockquote` | SRes 2, Cult 1, Math 6, PL 15, Sens 2 | flex: 1 1 auto where `.mm-trio>blockquote`<br>flex-basis: 100% where `.mm-trio>blockquote` at (max-width:640px)<br>font-size (by width and condition): 18px ! ; 17px ! at (max-width:830px) ; 18px ! where `blockquote:not(#mmz)` at (min-width:641px) ; 17px ! where `blockquote:not(#mmz)` at (max-width:640px)<br>line-height (by width): 40px ! ; 38px ! at (max-width:830px)<br>min-width: 0 where `.mm-trio>blockquote`<br>order: -1 where `.mm-trio>blockquote` at (max-width:640px) |
| `body` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background (competing): **competing**: #F5EEE3 ! wins over var(--bg), var(--paper)<br>color: var(--ink)<br>font-family (competing): **competing**: var(--serif) wins over 'EB Garamond',Georgia,serif<br>font-size (by width): **competing**: 18px wins over 19px ; 17px at (max-width:640px)<br>line-height (competing): **competing**: 1.65 wins over 1.7<br>margin: 0<br>padding-bottom: env(safe-area-inset-bottom,0px)<br>padding-top: env(safe-area-inset-top,0px) |
| `button` | Jour 11, Aun 11, Bio 11, SRes 11, Cult 11, Math 11, PL 11, RoA 11, Sens 11 | outline (by condition): 2px solid var(--active) where `button:focus-visible` ; 2px solid #fff where `.site-head button:focus-visible`<br>outline-offset (by condition): 3px where `button:focus-visible` ; 3px where `.site-head button:focus-visible` |
| `cite` | SRes 1, Math 3, PL 14, Sens 2 | color: var(--ink) where `blockquote.pullquote cite`<br>display (by condition): block where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: block ! wins over  ; block ! where `blockquote cite`<br>font-family (competing): **competing** where `blockquote.pullquote cite`: var(--serif) ! wins over inherit, var(--display)<br>font-size (by width and condition): **competing** where `blockquote.pullquote cite`: 18px ! wins over 17px, 1em ; 18px ! where `blockquote cite` ; 17px ! where `blockquote cite` at (max-width:830px) ; 17px ! where `blockquote.pullquote cite` at (max-width:830px) ; 18px ! where `blockquote:not(#mmz) cite` at (min-width:641px) ; 17px ! where `blockquote:not(#mmz) cite` at (max-width:640px)<br>font-style (by condition): normal where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: normal ! wins over  ; normal ! where `blockquote cite`<br>font-weight: 400 ! where `blockquote.pullquote cite`<br>line-height (by width and condition): **competing** where `blockquote.pullquote cite`: 40px ! wins over 43.2px, 43.2px ! ; **competing** where `blockquote.pullquote cite` at (max-width:640px): 42px ! wins over  ; 40px ! where `blockquote cite` ; 38px ! where `blockquote cite` at (max-width:830px) ; 38px ! where `blockquote.pullquote cite` at (max-width:830px)<br>margin-top (by condition): 6px where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: 0 ! wins over 8px ; 0 ! where `blockquote cite`<br>padding-left (by condition): 48px where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: 48px ! wins over 0 !, 11px !<br>text-indent: 0 ! where `blockquote.pullquote cite` |
| `div` | Jour 287, Aun 138, Bio 99, SRes 112, Cult 500, Math 402, PL 349, RoA 126, Sens 649 | break-inside: avoid where `.materials-table div`<br>color: var(--ink) where `.preview-grid > div`<br>font-size: 17px where `.preview-grid > div`<br>font-style: italic where `.preview-grid > div`<br>margin: 8px 0 where `.preview-grid > div`<br>padding: 4px 0 where `.materials-table div` |
| `figcaption` | Bio 9, Sens 3 | color: var(--ink) where `.ph figcaption`<br>font-family: 'EB Garamond',serif where `.ph figcaption`<br>font-size (by width and condition): 15px where `.ph figcaption` ; 16px ! at (min-width:641px) ; 16px ! at (max-width:640px)<br>line-height: 1.3 where `.ph figcaption`<br>margin-top: 6px where `.ph figcaption`<br>min-width: 100% where `.ph figcaption`<br>text-align: center where `.ph figcaption`<br>width: 0 where `.ph figcaption` |
| `figure` | Jour 152, Aun 58, Bio 21, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | margin-left: 0 ! where `.mm-pdf-row .mm-pdfin>figure` at (max-width:640px) |
| `footer` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | border-top: 0 where `.mc-band ~ footer`<br>margin-top: 0 where `.mc-band ~ footer` |
| `h1` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color (by condition): #fff where `.hero h1` ; var(--title)<br>font-family (by condition): var(--display) where `.hero h1` ; 'Cormorant Garamond',Georgia,serif<br>font-size (by width and condition): 40px where `.hero h1` ; **competing** where `.hero h1` at (max-width:640px): 28px ! wins over  ; 30px ; 26px at (max-width:640px) ; 40px ! where `.hero h1` at (min-width:641px)<br>font-weight (by condition): 500 where `.hero h1` ; 700<br>line-height (by condition): 1.2 where `.hero h1` ; 1.15<br>margin (by condition): 0 where `.hero h1` ; 0<br>max-width (by width): 760px where `.hero h1` ; 760px ! where `.hero h1` at (min-width:641px)<br>position: relative where `.hero h1`<br>text-shadow: 0 1px 12px rgba(0,0,0,.4) where `.hero h1`<br>z-index: 1 where `.hero h1` |
| `h2` | SRes 4, Cult 37, Math 12, Sens 15 | border-bottom (competing): **competing**: 2px solid #0432FF ! wins over 0 !, 2px solid var(--head)<br>color (competing): **competing**: var(--head) wins over var(--heading)<br>display: flow-root<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',Georgia,serif<br>font-size (by width and condition): **competing**: 22px ! wins over 24px !, 25px ; **competing** at (max-width:640px): 20px ! wins over 22px, 22px ! ; 23px ! at (min-width:641px) ; 20px ! where `h2[data-notred]` ; 18px ! where `h2:not(.mm-hc-00B050)` at (min-width:641px) ; 18px ! where `h2[class*="mm-hc-"]:not(.mm-hc-00B050)` at (min-width:641px) ; 17px ! where `h2:not(.mm-hc-00B050)` at (max-width:640px) ; 17px ! where `h2[class*="mm-hc-"]:not(.mm-hc-00B050)` at (max-width:640px) ; 17px ! where `h2[class*="mm-hc-"]:not(.mm-hc-00B050)[class]` at (max-width:640px)<br>font-weight (by condition): **competing**: 500 ! wins over 400 !, 700 ; 700 ! where `h2[data-notred]`<br>line-height (competing): **competing**: 1.2 ! wins over 1.25<br>margin: 0<br>margin-bottom: 16px<br>padding-bottom (competing): **competing**: 8px ! wins over 0 ! |
| `h3` | SRes 13, RoA 21, Sens 30 | font-size (by width): 18px ! at (min-width:641px) ; 17px ! at (max-width:640px) |
| `html` | **none of the nine** | -webkit-text-size-adjust: 100%<br>background: #F5EEE3 !<br>scroll-behavior: smooth at (prefers-reduced-motion:no-preference)<br>scroll-padding-top (by width): calc(76px + env(safe-area-inset-top,0px)) ; calc(64px + env(safe-area-inset-top,0px)) at (max-width:960px) |
| `img` | Jour 153, Aun 59, Bio 24, SRes 15, Cult 251, Math 154, PL 164, RoA 4, Sens 209 | box-shadow: 0 20px 60px rgba(0,0,0,.5) where `.lightbox img`<br>display (by condition): block ; block where `.lb-frame img` ; block where `.pim[data-trim] img`<br>height: 100% where `.pim[data-trim] img`<br>max-height: 100% where `.lightbox img`<br>max-width (by condition): 100% ; 100% where `.lightbox img`<br>object-fit (by condition): contain where `.lightbox img` ; cover where `.pim[data-trim] img` ; contain ! where `.pim.mm-contain img`<br>width: 100% where `.pim[data-trim] img` |
| `li` | Jour 122, Aun 122, Bio 122, SRes 128, Cult 209, Math 260, PL 153, RoA 133, Sens 141 | align-items (by width): center where `.menu > li` ; center where `.menu > li` at (max-width:960px)<br>border-bottom (by width and condition): 1px solid var(--line) where `.grp li` ; 0 where `.grp li:last-child` ; 1px solid rgba(255,255,255,.2) where `.menu > li` at (max-width:960px) ; 0 where `.grp li` at (max-width:960px) ; 0 ! where `.panel .grp li` ; 0 ! where `#site-nav li` ; 0 ! where `.menu .panel li`<br>break-inside: avoid where `ul.mm-cols2>li`<br>counter-increment (competing): **competing** where `ol>li`: mmn ! wins over none !<br>display (by width): flex where `.menu > li` ; flex where `.menu > li` at (max-width:960px)<br>flex-wrap: wrap where `.menu > li` at (max-width:960px)<br>font-size (by width): 18px ! at (min-width:641px) ; 17px ! at (max-width:640px)<br>font-weight: 400 where `.grp li`<br>height (by width): 76px where `.menu > li` ; auto where `.menu > li` at (max-width:960px)<br>line-height (by width): **competing**: 29.7px ! wins over 37.2px ; **competing** at (max-width:640px): 28.05px ! wins over 36px ; 37.2px ! at (min-width:641px)<br>margin (by condition): 0 0 10px where `.toc li` ; 8px 0 ; 0 where `.site-head li`<br>margin-bottom (by condition): 8px ! where `ul li` ; 0 ! where `nav.toc-wrap ul:last-child li:last-child`<br>margin-top (by condition): 0 ! where `ul.mm-cols2>li` ; 4.3px ! where `ul.mm-cols2>li+li` ; 8px ! where `ul li`<br>padding-left (competing): **competing** where `ol>li`: calc(0.71em + 24px) ! wins over 0 !, 30px, 31px !<br>position (by condition): static where `.menu > li` ; relative where `ul li` ; static ! where `.site-head li` ; **competing** where `ol>li`: relative ! wins over static !<br>text-align (by width and condition): **competing**: left wins over justify ; left where `.site-head li` ; left where `.toc .mm-toc3 li` ; left ! where `ul.mm-cols2 li` at (max-width:640px) ; left ! where `:root body main li` at (max-width:640px) ; left ! where `:root body main ul>li` at (max-width:640px) ; left ! where `:root body main ol>li` at (max-width:640px) ; justify ! where `ul>li` ; justify ! where `ol>li` |
| `li::before` | Jour 122, Aun 122, Bio 122, SRes 128, Cult 209, Math 260, PL 153, RoA 133, Sens 141 | color: var(--ink) where `ul li::before`<br>content (by condition): "\2010" where `ul li::before` ; none ! where `.site-head li::before` ; none ! where `.toc li::before` ; **competing** where `ol>li::before`: counter(mmn) "." ! wins over none !<br>left (by condition): **competing** where `ul li::before`: -24px ! wins over -20px, -30px ! ; **competing** where `ol>li::before`: 0 ! wins over auto ! ; -31px ! where `ul>li::before` ; -39px ! where `ul.mm-inner>li::before`<br>position (by condition): absolute where `ul li::before` ; **competing** where `ol>li::before`: absolute ! wins over static !<br>top: 0 where `ol>li::before` |
| `ol` | SRes 1, Cult 3, Math 11, PL 3, RoA 2, Sens 1 | column-gap: 48px where `ol[data-cols]`<br>counter-reset (competing): **competing**: mmn ! wins over none !<br>display: grid where `ol[data-cols]`<br>grid-auto-flow: column where `ol[data-cols]`<br>justify-content: start where `ol[data-cols]`<br>list-style (competing): **competing**: none ! wins over decimal inside !<br>margin: 16px 0<br>margin-left (by width): **competing**: 0 ! wins over 48px ! ; 0 ! at (max-width:640px)<br>padding-left (competing): **competing**: 0 ! wins over 24px, 48px ! |
| `p` | Jour 25, Aun 32, Bio 39, SRes 27, Cult 479, Math 362, PL 223, RoA 39, Sens 251 | -webkit-hyphens: manual where `p:not(blockquote p):not(.mm-pdf p):not([data-tabs]):not(.mm-name)` at (min-width:641px)<br>color (by condition): inherit where `blockquote.pullquote p` ; **competing** where `.mc-band p`: #fff ! wins over <br>font-family (competing): **competing** where `blockquote.pullquote p`: var(--serif) ! wins over inherit, var(--display)<br>font-size (by width and condition): **competing** where `blockquote.pullquote p`: 18px ! wins over 17px, 1em ; **competing** where `.mc-band p`: 18px ! wins over  ; **competing** where `.mc-band p` at (max-width:640px): 17px ! wins over  ; 18px ! where `blockquote p` ; 17px ! where `blockquote p` at (max-width:830px) ; 17px ! where `blockquote.pullquote p` at (max-width:830px) ; 17px ! where `.mc-band p` at (max-width:830px) ; 18px ! where `p:not(.mm-gl):not(.mm-cap)` at (min-width:641px) ; 18px ! where `blockquote:not(#mmz) p` at (min-width:641px) ; 18px ! where `.mc-band p` at (min-width:641px) ; 17px ! where `p:not(.mm-gl):not(.mm-cap)` at (max-width:640px) ; 17px ! where `blockquote:not(#mmz) p` at (max-width:640px)<br>font-style (by condition): **competing** where `blockquote.pullquote p`: italic ! wins over  ; **competing** where `.mc-band p`: italic ! wins over  ; italic ! where `blockquote p`<br>font-weight (competing): **competing** where `blockquote.pullquote p`: 400 ! wins over <br>hyphens: manual where `p:not(blockquote p):not(.mm-pdf p):not([data-tabs]):not(.mm-name)` at (min-width:641px)<br>line-height (by width and condition): **competing** where `blockquote.pullquote p`: 40px ! wins over 1.7, 43.2px, 43.2px ! ; **competing**: 29.7px ! wins over 37.2px ; **competing** at (max-width:640px): 28.05px ! wins over 36px ; **competing** where `blockquote.pullquote p` at (max-width:640px): 42px ! wins over  ; **competing** where `.mc-band p`: 40px ! wins over 1.6 ; 40px ! where `blockquote p` ; 38px ! where `blockquote p` at (max-width:830px) ; 38px ! where `blockquote.pullquote p` at (max-width:830px) ; 38px ! where `.mc-band p` at (max-width:830px)<br>margin (by condition): 0 0 8px where `blockquote.mq p` ; **competing**: 14px 0 wins over 16px 0 ; 0 where `blockquote.pullquote p` ; 8px 0 where `aside.callout p` ; **competing** where `.mc-band p`: 0 auto ! wins over <br>margin-left: 0 ! where `blockquote.mm-ctr p`<br>margin-top: 0 ! where `blockquote.pullquote p + p`<br>max-width (competing): **competing** where `.mc-band p`: none ! wins over 860px<br>padding-left (by condition): **competing** where `blockquote.pullquote p`: 0 ! wins over 11px ! ; 0 ! where `blockquote.mm-ctr p`<br>text-align (by width and condition): justify where `p:not(blockquote p):not(.mm-pdf p):not([data-tabs]):not(.mm-name)` at (min-width:641px) ; justify where `main.article p:not(.centred):not(.mm-poem-ctr):not(.mm-cap):not(.mc-by)` ; inherit ! where `main.article blockquote p` ; center ! where `.mc-band p` ; left ! where `:root body main.article p:not(.centred):not(.mm-poem-ctr):not(.mm-cap):not(.mc-by):not(blockquote p)` at (max-width:640px) ; left ! where `:root body main blockquote.pullquote.mm-just>p` at (max-width:640px) ; justify ! where `blockquote.pullquote.mm-just>p`<br>text-indent (by condition): 48px where `blockquote.mq p` ; **competing** where `blockquote.pullquote p`: 48px ! wins over 0 ! ; 0 ! where `blockquote.mm-ctr p` ; 0 ! where `.mc-band p` ; 0 ! where `blockquote.pullquote.mm-one>p` ; 0 ! where `blockquote.pullquote.mm-noind>p` ; 0 ! where `blockquote.pullquote.mm-notes>p` ; 48px ! where `:root body main blockquote.pullquote:not(.mm-one) p`<br>text-wrap (competing): **competing** where `.mc-band p`: wrap ! wins over balance |
| `span` | Jour 114, Aun 84, Bio 84, SRes 117, Cult 354, Math 222, PL 87, RoA 130, Sens 107 | background: var(--rule) where `.mm-dots span` at (max-width:830px)<br>border-radius: 50% where `.mm-dots span` at (max-width:830px)<br>color (by width and condition): var(--ink) where `.grp .hd span` ; var(--ink) where `.grp li.hd span` ; #0432FF where `.panel.cat .grp li.hd span` ; #fff where `.grp li.hd span` at (max-width:960px) ; #8FC6FF where `.panel.cat .grp li.hd span` at (max-width:960px) ; #0432FF ! where `.panel .grp li.hd span` at (min-width:831px)<br>cursor: default where `.grp .hd span`<br>display (by width and condition): block where `.hero h1 span` ; inline where `p.mm-tabcol>span` at (max-width:640px) ; inline where `span.mm-tabtail>span` at (max-width:640px) ; block where `.grp .hd span`<br>flex: 1 1 auto where `.mm-bda span`<br>font-family: var(--serif) where `.grp .hd span`<br>font-size (by width and condition): 17px where `.grp .hd span` ; 17px where `.grp .hd span` at (max-width:960px) ; 18px ! where `.grp .hd span` at (min-width:641px) ; 15px ! where `.site-foot-in span` at (min-width:641px) ; 17px ! where `.grp .hd span` at (max-width:640px) ; 15px ! where `.site-foot-in span` at (max-width:640px)<br>font-weight (by width and condition): 400 where `.menu span` ; 400 where `.grp li.hd span` ; 400 ! where `.panel .grp li.hd span` at (min-width:831px)<br>height: 6px where `.mm-dots span` at (max-width:830px)<br>line-height: 1.3 where `.grp .hd span`<br>min-width: 0 where `.mm-bda span`<br>padding (by width): 8px 0 where `.grp .hd span` ; 7px 0 where `.grp .hd span` at (max-width:960px)<br>text-align (by width and condition): justify where `.mm-bda span` ; left ! where `:root body main .mm-bda span` at (max-width:640px)<br>width: 6px where `.mm-dots span` at (max-width:830px) |
| `strong` | SRes 4, Cult 1, Math 30, PL 4, Sens 63 | color: var(--ink) where `.sub-label strong`<br>flex: 0 0 72px where `.mm-bda strong`<br>font-family: var(--serif) ! where `blockquote.pullquote strong`<br>font-weight (by condition): 400 where `blockquote.mq strong` ; 700 where `.sub-label strong` ; 400 ! where `blockquote.pullquote strong` ; 400 ! where `.mm-wcol strong` ; 400 ! where `.mm-wc strong` ; 700 where `.mm-bda strong` |
| `summary` | Cult 23 | color (by condition): #EE0000 where `.mm-albums-c summary` ; #2B2B2B where `.mm-albums-c details.mm-megd summary`<br>cursor: pointer where `.mm-albums-c summary`<br>display: none where `.mm-albums-c summary::-webkit-details-marker`<br>font-size: 18px where `.mm-albums-c summary`<br>list-style: none where `.mm-albums-c summary`<br>margin-left: 0 where `.mm-albums-c summary` |
| `summary::before` | Cult 23 | color: #EE0000 where `.mm-albums-c summary::before`<br>content (by condition): "+" where `.mm-albums-c summary::before` ; "\2212" where `.mm-albums-c details[open]>summary::before`<br>display: inline-block where `.mm-albums-c summary::before`<br>font-weight: 400 where `.mm-albums-c summary::before`<br>width: 22px where `.mm-albums-c summary::before` |
| `summary::marker` | Cult 23 | color: #EE0000 where `.mm-albums-c summary::marker` |
| `sup` | Math 2, Sens 37 | font-size (by condition): .68em where `.formula-table sup` ; .68em where `.article sup`<br>line-height (by condition): 0 where `.formula-table sup` ; 0 where `.article sup`<br>vertical-align (by condition): .45em where `.formula-table sup` ; .45em where `.article sup` |
| `svg` | Jour 9, Aun 9, Bio 9, SRes 9, Cult 9, Math 9, PL 9, RoA 9, Sens 9 | transform (by width): rotate(180deg) where `.has-panel.open > .sub-toggle svg` ; rotate(180deg) where `.has-panel.open > .sub-toggle svg` at (max-width:960px) |
| `td` | PL 32, Sens 121 | border: 0 where `.mm-table td`<br>border-bottom (by condition): 1px solid var(--rule) ! where `table.mm-table td` ; 0 ! where `.mm-table-wrap:has(+ p.mm-gl) tr:last-child>td`<br>border-top: 1px solid var(--ink) where `.formula-table tr.rule td`<br>font-weight: 600 where `.formula-table tr.total td`<br>padding (by condition): 3px 10px 3px 0 where `.formula-table td` ; 16px 24px 16px 0 ! where `table.mm-table td` ; 8px 16px 8px 0 where `.mm-table td`<br>padding-right: 0 ! where `table.mm-table td:last-child`<br>padding-top: 6px where `.formula-table tr.rule td`<br>text-align: left where `.mm-table td`<br>vertical-align (by condition): baseline where `.formula-table td` ; top where `.mm-table td`<br>white-space: nowrap where `.formula-table td` |
| `th` | PL 4 | border: 0 where `.mm-table th`<br>border-bottom (by condition): 1px solid var(--rule) ! where `table.mm-table th` ; 0 ! where `.mm-table-wrap:has(+ p.mm-gl) tr:last-child>th`<br>font-weight: 700 where `.mm-table th`<br>padding (by condition): 16px 24px 16px 0 ! where `table.mm-table th` ; 8px 16px 8px 0 where `.mm-table th`<br>padding-right: 0 ! where `table.mm-table th:last-child`<br>text-align: left where `.mm-table th`<br>vertical-align: top where `.mm-table th` |
| `ul` | Jour 36, Aun 36, Bio 36, SRes 37, Cult 44, Math 41, PL 37, RoA 37, Sens 38 | list-style (by condition): none where `.toc ul` ; none<br>margin (by condition): 0 where `.toc ul` ; 16px 0 ; 0 where `.site-head ul`<br>margin-left (by width): **competing**: 0 ! wins over 48px ! ; 0 ! at (max-width:640px)<br>padding: 0 where `.toc ul`<br>padding-left (by condition): **competing**: 48px ! wins over 24px, 30px !, 31px ! ; 0 ! where `.site-head ul` |

**Essay elements used on none of the nine pages (49)**: `.c1` `.callout` `.callout-label` `.colophon` `.hero-sub` `.lb-frame` `.lead-rule` `.mc-1-1` `.mc-1-2` `.mc-1-3` `.mc-2-1` `.mc-2-2` `.mc-3-1` `.mm-arrow` `.mm-bda` `.mm-cabar-tick` `.mm-cabar-tick::before` `.mm-caprow` `.mm-contain` `.mm-cset` `.mm-ctr` `.mm-dots` `.mm-g2col` `.mm-gl-bq` `.mm-hang` `.mm-hs` `.mm-left` `.mm-notes` `.mm-pdf-l` `.mm-pdfbr` `.mm-pdfsp` `.mm-pfig` `.mm-ph26` `.mm-pspacer` `.mm-pwrap` `.mm-tab1` `.mm-tabtail` `.mm-trio` `.mq` `.np-top` `.on` `.open` `.over` `.page-h2` `.sub` `.title-block` `.toc-num` `b` `html`

## Resources template: 170 elements, 56 used on none of the nine pages, 83 competing values

| Element | Used on, whole page (count) | Property: value, with condition and width |
|---|---|---|
| `.article` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | margin: 0 auto<br>max-width (competing): **competing**: var(--page) wins over 1220px<br>padding (by width): **competing**: 0 var(--gutter) 72px wins over 8px 40px 96px ; **competing** at (max-width:640px): 0 24px 56px wins over 8px 24px 72px |
| `.beige-rule` | Jour 1, Aun 1, Bio 1, Cult 1, Math 1, PL 1, RoA 23, Sens 1 | background: #D9C9AB<br>clear: none ! where `.res-entry:has(> .mm-fitlines) + .beige-rule`<br>height: 2px<br>margin: 0 auto 20px<br>max-width: 100% |
| `.blindfold-label` | Sens 2 | color: var(--head)<br>margin: 26px 0 6px<br>text-align: center |
| `.c1` | **none of the nine** | grid-template-columns: minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) where `.panel-in.c1` |
| `.c4` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | gap: 26px 40px where `.panel-in.c4`<br>grid-template-columns: repeat(4,minmax(0,1fr)) where `.panel-in.c4` |
| `.callout` | **none of the nine** | background: var(--tint)<br>border-radius: 3px<br>clear: both<br>margin: 24px 0<br>max-width: 800px<br>padding: 24px |
| `.callout-label` | **none of the nine** | color: var(--ink)<br>font-family: 'Cormorant Garamond',serif<br>font-size: 18px<br>font-style: italic<br>font-weight: 500<br>margin-bottom: 8px |
| `.colophon` | **none of the nine** | border-top: 1px solid var(--rule)<br>clear: both<br>color: var(--ink)<br>font-family: 'EB Garamond',serif<br>font-size: 14px<br>margin: 0 auto<br>max-width: 1220px<br>padding: 40px 40px 80px |
| `.cw-white` | Cult 1, Math 5, Sens 1 | color: var(--ink) ! |
| `.doc-img` | Jour 152, Aun 58, Bio 23, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | background (by condition): #EDE6D8 ; transparent where `.ph img.doc-img`<br>border-radius (by condition): 2px ; 0 where `.ph img.doc-img`<br>cursor (by condition): zoom-in ; zoom-in where `.ph img.doc-img`<br>display: block where `.ph img.doc-img`<br>height: auto where `.ph img.doc-img`<br>max-height: none where `.ph img.doc-img`<br>max-width (by condition): 100% ; none where `.ph img.doc-img`<br>width (by condition): auto ; 100% where `.ph img.doc-img` |
| `.formula-divider` | Jour 15, Sens 1 | border: 0<br>border-top: 1px solid var(--rule)<br>margin: 40px 0 24px |
| `.formula-head` | Sens 1 | margin-bottom: 10px |
| `.formula-table` | Sens 1 | border-collapse: collapse<br>font-size (by width): 17px ; 15px at (max-width:640px)<br>font-variant-numeric: tabular-nums |
| `.formula-wrap` | Sens 1 | max-width: 100%<br>overflow-x: auto |
| `.grp` | Jour 33, Aun 33, Bio 33, SRes 33, Cult 33, Math 33, PL 33, RoA 33, Sens 33 | font-weight: 400<br>list-style: none<br>margin: 0<br>margin-bottom: 6px at (max-width:960px)<br>margin-top: 24px where `.panel-in .grp + .grp` at (max-width:960px)<br>padding: 0 |
| `.grp-first` | Sens 42 | margin-bottom: 4px |
| `.grp-last` | Sens 42 | margin-top: 4px |
| `.grp-mid` | Sens 38 | margin-bottom: 4px<br>margin-top: 4px |
| `.hero` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: flex-end<br>background-color: #2A2420<br>background-position: center<br>background-size: cover<br>display: flex<br>margin (by width): 10px 10px 0 ; 0 at (max-width:640px)<br>min-height (by width): 400px ; 240px at (max-width:640px)<br>padding (by width): 0 8% 40px ; 0 24px 24px at (max-width:640px)<br>position: relative |
| `.hero-sub` | **none of the nine** | color: var(--ink)<br>font-family: 'Cormorant Garamond',serif<br>font-size: 19px<br>font-style: italic<br>font-weight: 400<br>margin-top: 8px |
| `.hero::after` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: linear-gradient(105deg,rgba(15,12,9,.72) 0%,rgba(15,12,9,.55) 34%,rgba(15,12,9,.12) 62%,rgba(15,12,9,0) 80%)<br>content: ""<br>inset: 0<br>pointer-events: none<br>position: absolute |
| `.icon-btn` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>background (by condition): none ; rgba(255,255,255,.1) where `.icon-btn:hover`<br>border: 0<br>border-radius: 22px<br>color: #fff<br>cursor: pointer<br>display: inline-flex<br>height: 44px<br>justify-content: center<br>width: 44px |
| `.lb-counter` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | bottom: 28px<br>color: rgba(255,255,255,.75)<br>display: none<br>font-family: 'EB Garamond',serif<br>font-size: 15px<br>left: 50%<br>position: fixed<br>transform: translateX(-50%) |
| `.lb-frame` | **none of the nine** | box-shadow: 0 20px 60px rgba(0,0,0,.5)<br>overflow: hidden<br>position: relative |
| `.lb-nav` | Jour 2, Aun 2, Bio 2, SRes 2, Cult 2, Math 2, PL 2, RoA 2, Sens 2 | align-items: center<br>background (by condition): rgba(255,255,255,.12) ; rgba(255,255,255,.24) where `.lb-nav:hover`<br>border: none<br>border-radius: 50%<br>color: #fff<br>cursor: pointer<br>display: none<br>font-size: 32px<br>height: 56px<br>justify-content: center<br>line-height: 1<br>position: fixed<br>top: 50%<br>transform: translateY(-50%)<br>transition: background .15s<br>width: 56px |
| `.lb-next` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | right: 24px |
| `.lb-prev` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | left: 24px |
| `.lightbox` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>background: rgba(20,16,12,.94)<br>cursor: zoom-out<br>display (by condition): none ; flex where `.lightbox.open`<br>inset: 0<br>justify-content: center<br>padding: 5vw<br>position: fixed<br>z-index: 999 |
| `.material-name` | SRes 13, RoA 21, Sens 30 | border-top (by condition): **competing**: 1px solid var(--line) wins over 1px solid var(--rule) ; 0 where `.res-entry h3.material-name`<br>color (by condition): **competing**: var(--head) wins over var(--material) ; #EE0000 where `.res-entry h3.material-name`<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',Georgia,serif<br>font-size (by width and condition): 21px ; 19px at (max-width:640px) ; 18px ! where `.res-entry h3.material-name` ; 17px ! where `.res-entry h3.material-name` at (max-width:640px)<br>font-weight (by condition): **competing**: 500 wins over 700 ; 400 ! where `.res-entry h3.material-name`<br>margin: 0<br>margin-bottom (by condition): 8px ; 0 ! where `.res-entry > h3.material-name`<br>margin-top (by condition): **competing**: 36px wins over 40px ; 32px where `.res-entry h3.material-name` ; 37px ! where `.res-entry:has(> .mm-row:last-child) + .res-entry > h3.material-name` ; 33.3px ! where `.res-entry:has(> .res-item:last-child) + .res-entry > h3.material-name` ; **competing** where `.res-entry:has(> .res-desc:last-child) + .res-entry > h3.material-name`: 29.55px ! wins over 33.3px ! ; **competing** where `.res-entry:has(> p:last-child) + .res-entry > h3.material-name`: 29.55px ! wins over 33.3px ! ; 33.3px ! where `.res-entry:has(> p:last-child > a.pdf:last-child) + .res-entry > h3.material-name`<br>padding-top (by condition): **competing**: 22px wins over 24px ; 0 where `.res-entry h3.material-name` |
| `.materials-table` | Sens 1 | clear: both<br>column-count: 2<br>column-gap: 48px<br>margin: 16px 0 24px<br>max-width: 640px |
| `.mc-1-1` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-1`<br>grid-row: 1 where `#p-curriculum .panel-in > .mc-1-1` |
| `.mc-1-2` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-2`<br>grid-row: 2 where `#p-curriculum .panel-in > .mc-1-2` |
| `.mc-1-3` | **none of the nine** | grid-column: 1 where `#p-curriculum .panel-in > .mc-1-3`<br>grid-row: 3 where `#p-curriculum .panel-in > .mc-1-3` |
| `.mc-2-1` | **none of the nine** | grid-column: 2 where `#p-curriculum .panel-in > .mc-2-1`<br>grid-row: 1 where `#p-curriculum .panel-in > .mc-2-1` |
| `.mc-2-2` | **none of the nine** | grid-column: 2 where `#p-curriculum .panel-in > .mc-2-2`<br>grid-row: 2 where `#p-curriculum .panel-in > .mc-2-2` |
| `.mc-3-1` | **none of the nine** | grid-column: 3 where `#p-curriculum .panel-in > .mc-3-1`<br>grid-row: 1 / span 3 where `#p-curriculum .panel-in > .mc-3-1` |
| `.mc-band` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: #1E4D7B !<br>margin-top: 40px !<br>padding (by width): 40px 40px 30px ! ; 40px 24px 30px ! at (max-width:830px)<br>text-align: center |
| `.mc-by` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color: #DCE6F0 ! where `.mc-band p.mc-by`<br>font-size (by width): 18px ! where `.mc-band p.mc-by` ; 17px ! where `.mc-band p.mc-by` at (max-width:830px) ; 18px ! where `.mc-band p.mc-by` at (min-width:641px) ; 17px ! where `.mc-band p.mc-by` at (max-width:640px)<br>font-style: normal ! where `.mc-band p.mc-by`<br>letter-spacing: .04em where `.mc-band p.mc-by`<br>line-height (by width): 40px ! where `.mc-band p.mc-by` ; 38px ! where `.mc-band p.mc-by` at (max-width:830px)<br>margin-top: 0 ! where `.mc-band p.mc-by` |
| `.menu` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display (by width): flex ; block at (max-width:960px)<br>font-weight: 400<br>gap (by width): 22px ; 15px at (max-width:1180px) ; 10px at (min-width:961px) and (max-width:1279px) ; 7px at (min-width:961px) and (max-width:1023px) ; 2px ! at (min-width:961px) and (max-width:1099px)<br>list-style: none<br>margin: 0<br>padding: 0 |
| `.menu-btn` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | display (by width): none ; inline-flex at (max-width:960px) |
| `.meta` | SRes 10, RoA 17 | color: #000 where `.res-item .meta`<br>display: inline ! where `.res-item > .meta` at (max-width:640px)<br>font-size (by width): 18px ! where `.res-item .meta` ; 17px ! where `.res-item .meta` at (max-width:640px)<br>margin-left: 30px ! where `.pdf-date + .meta` |
| `.micro-label` | Cult 45, Math 57, PL 46, Sens 84 | color: var(--ink)<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',serif<br>font-size (by width): **competing**: 18px ! wins over 19px, 21px ! ; **competing** at (max-width:640px): 17px ! wins over 19px !<br>font-weight (by condition): **competing**: 400 ! wins over 700 ; 700 ! where `.micro-label[data-word-bold="1"]`<br>margin-bottom: 0<br>margin-top: 15px |
| `.mm-ami` | **none of the nine** | margin-top: 4px ! where `.res-entry .res-item.mm-ami` |
| `.mm-attr` | PL 1 | font-size (by width and condition): 18px ! where `blockquote span.mm-attr` ; 18px ! where `blockquote.pullquote span.mm-attr` ; 17px ! where `blockquote span.mm-attr` at (max-width:830px) ; 17px ! where `blockquote.pullquote span.mm-attr` at (max-width:830px)<br>line-height (by width and condition): 40px ! where `blockquote span.mm-attr` ; 40px ! where `blockquote.pullquote span.mm-attr` ; 38px ! where `blockquote span.mm-attr` at (max-width:830px) ; 38px ! where `blockquote.pullquote span.mm-attr` at (max-width:830px) |
| `.mm-besidepdf` | **none of the nine** | display: flow-root |
| `.mm-blue` | RoA 1 | color: #0432FF !<br>display: inline-block |
| `.mm-cap` | Bio 9, Math 22 | font-size (by width): 16px ! at (min-width:641px) ; 16px ! at (max-width:640px) |
| `.mm-dots` | **none of the nine** | display (by width): none ; flex at (max-width:640px)<br>gap: 6px at (max-width:640px)<br>justify-content: center at (max-width:640px)<br>margin: 8px 0 4px at (max-width:640px) |
| `.mm-figcap` | **none of the nine** | font-size: 15px<br>font-style: italic<br>line-height: 1.3<br>margin (by width and condition): 6px auto 0 ; 6px 0 0 calc(100% - 160px) at (min-width:641px) ; 6px auto 0 ! where `#mm-fit10 figcaption.mm-figcap`<br>text-align: center<br>width (by width and condition): 160px at (min-width:641px) ; auto ! where `#mm-fit10 figcaption.mm-figcap` |
| `.mm-float` | Aun 2, Bio 7, SRes 6, Cult 2, RoA 3, Sens 5 | clear (by condition): right ; left where `.mm-float.mm-left`<br>float (by width and condition): right ; left where `.mm-float.mm-left` ; none at (max-width:640px) ; none where `.mm-float.mm-left` at (max-width:640px)<br>margin (by width and condition): 4px 0 12px 32px ; 4px 32px 12px 0 where `.mm-float.mm-left` ; 12px 0 at (max-width:640px) ; 12px 0 where `.mm-float.mm-left` at (max-width:640px)<br>padding-top: 24px ! where `.mm-float.mm-left` at (min-width:641px) |
| `.mm-formula` | Sens 1 | align-items: flex-start where `.mm-set.mm-formula` |
| `.mm-hanglab` | **none of the nine** | padding-left (by width): 8em ! ; 0 ! at (max-width:640px)<br>text-indent (by width): -8em ! ; 0 ! at (max-width:640px) |
| `.mm-hc-EE0000` | Cult 32, Math 7, RoA 1, Sens 34 | color: #EE0000 ! |
| `.mm-hc-FF0000` | Sens 3 | color: #FF0000 ! |
| `.mm-imgs` | Jour 34, Aun 15, Bio 11, SRes 8, Cult 58, Math 61, PL 44, RoA 3, Sens 72 | align-items: flex-start where `.mm-set .mm-imgs`<br>display (by width and condition): contents where `.mm-row .mm-imgs` ; flex where `.mm-set .mm-imgs` ; flex ! where `.mm-msfloat .mm-imgs` ; block ! where `#mm-fitR .mm-imgs` ; block ! where `#mm-fit10 .mm-imgs` ; flex ! where `.mm-float.mm-left .mm-imgs` at (min-width:641px) ; flex where `.mm-set .mm-imgs` at (max-width:640px) ; none where `.mm-set .mm-imgs::-webkit-scrollbar` at (max-width:640px) ; contents where `.mm-row .mm-imgs` at (max-width:640px)<br>flex (by condition): 1 1 auto where `.mm-set .mm-imgs` ; none where `.mm-set.mm-intro .mm-imgs` ; none where `.mm-set.mm-formula .mm-imgs`<br>flex-direction: row ! where `.mm-float.mm-left .mm-imgs` at (min-width:641px)<br>gap (by width and condition): 24px where `.mm-set .mm-imgs` ; 16.8px ! where `.mm-set[data-grid] .mm-imgs` ; 16px where `.mm-msfloat .mm-imgs` ; 16px where `.mm-float.mm-left .mm-imgs` at (min-width:641px) ; 10px where `.mm-set .mm-imgs` at (max-width:640px)<br>height (by condition): auto ! where `#mm-ms .mm-msfloat .mm-imgs` ; auto ! where `#mm-fitR .mm-imgs` ; auto ! where `#mm-fit10 .mm-imgs`<br>justify-content (by width and condition): center where `.mm-set .mm-imgs` ; flex-end where `.mm-set.mm-col .mm-imgs` ; flex-end where `.mm-set.mm-intro .mm-imgs` ; flex-end where `.mm-set[data-align=right] .mm-imgs` ; flex-end where `.mm-set[data-at=right] .mm-imgs` ; flex-start where `.mm-set.mm-formula .mm-imgs` ; flex-start ! where `.mm-row.mm-rowleft .mm-imgs` ; center where `.mm-msfloat .mm-imgs` at (max-width:640px) ; flex-start ! where `.mm-set .mm-imgs` at (max-width:640px)<br>margin: 12px 0 0 ! where `.mm-set .mm-imgs` at (max-width:640px)<br>margin-left (by width and condition): 32px where `.mm-set.mm-intro .mm-imgs` ; 48px where `.mm-set.mm-formula .mm-imgs` ; 0 ! where `.mm-row.mm-rowleft .mm-imgs` ; 0 where `.mm-set.mm-intro .mm-imgs` at (max-width:640px) ; 0 where `.mm-set.mm-formula .mm-imgs` at (max-width:640px)<br>min-width: 0 where `.mm-set .mm-imgs`<br>overflow-x: auto where `.mm-set .mm-imgs` at (max-width:640px)<br>scroll-snap-type: x mandatory where `.mm-set .mm-imgs` at (max-width:640px)<br>scrollbar-width: none where `.mm-set .mm-imgs` at (max-width:640px) |
| `.mm-ink` | RoA 2 | color: #000 ! |
| `.mm-inner` | Math 2 | margin: 8px 0 0 !<br>padding-left: 24px ! |
| `.mm-lab` | **none of the nine** | display: inline-block<br>margin-right: .6em where `p.mm-hanglab .mm-lab` at (max-width:640px)<br>min-width (by width and condition): 8em ; 0 where `p.mm-hanglab .mm-lab` at (max-width:640px)<br>text-indent: 0 |
| `.mm-left` | **none of the nine** | clear: left where `.mm-float.mm-left`<br>float (by width): left where `.mm-float.mm-left` ; none where `.mm-float.mm-left` at (max-width:640px)<br>margin (by width): 4px 32px 12px 0 where `.mm-float.mm-left` ; 12px 0 where `.mm-float.mm-left` at (max-width:640px)<br>padding-top: 24px ! where `.mm-float.mm-left` at (min-width:641px) |
| `.mm-licont` | **none of the nine** | margin: 8px 0 0 ! where `li > p.mm-licont`<br>text-indent: 0 ! where `li > p.mm-licont` |
| `.mm-lsp` | **none of the nine** | display: inline-block<br>white-space: pre<br>width: 24px |
| `.mm-msfloat` | **none of the nine** | float (by width): right ; none at (max-width:640px)<br>margin (by width): 0 0 0 32px ; 12px 0 at (max-width:640px) |
| `.mm-msfloat::after` | **none of the nine** | clear: both where `.res-entry:has(> .mm-msfloat)::after`<br>content:  where `.res-entry:has(> .mm-msfloat)::after`<br>display: block where `.res-entry:has(> .mm-msfloat)::after` |
| `.mm-n` | **none of the nine** | left: 0 where `p.mm-numline .mm-n`<br>position: absolute where `p.mm-numline .mm-n` |
| `.mm-numline` | **none of the nine** | padding-left: 30px<br>position: relative |
| `.mm-org-rule` | RoA 23 | background: #D9C9AB<br>clear: both<br>height: 2px<br>margin: 0<br>max-width: 100% |
| `.mm-pairend` | **none of the nine** | margin-bottom: 30px ! |
| `.mm-row` | Jour 34, Aun 13, Bio 4, SRes 2, Cult 51, Sens 30 | align-items: flex-start<br>display (by width): flex ; **competing** at (max-width:640px): none wins over flex<br>flex-wrap: nowrap<br>gap (by width): min(38.4px, calc((100vw - 80px) * 38.4 / 1140)) ; 10px at (max-width:640px)<br>justify-content (by width and condition): center ; flex-start ! where `.mm-row.mm-rowleft` ; flex-start ! at (max-width:640px)<br>margin (by width): 20px 0 ; 12px 0 0 ! at (max-width:640px)<br>margin-left: 0 ! where `.mm-row.mm-rowleft`<br>margin-top: 24px where `.mm-row + .mm-row`<br>overflow-x: auto at (max-width:640px)<br>scroll-snap-type: x mandatory at (max-width:640px)<br>scrollbar-width: none at (max-width:640px) |
| `.mm-rowleft` | **none of the nine** | justify-content: flex-start ! where `.mm-row.mm-rowleft`<br>margin-left: 0 ! where `.mm-row.mm-rowleft` |
| `.mm-set` | Cult 5, Sens 37 | align-items (by condition): center ; flex-start where `.mm-set.mm-formula` ; flex-start where `main[data-spacing=table] .mm-set`<br>display (by width): flex ; block at (max-width:640px)<br>margin: 16px 0 |
| `.mm-sub` | Cult 30 | font-size (by width): 20px ! ; 18px ! at (max-width:640px) |
| `.mm-t` | Cult 53, Math 9, PL 2 | -moz-tab-size: 48px<br>tab-size: 48px<br>white-space: pre |
| `.mm-t1` | **none of the nine** | margin-left: min(55px,calc((100vw - 80px)*55/1140)) where `.mm-sugar .mm-t1` at (min-width:641px) |
| `.mm-t2` | **none of the nine** | margin-left: min(37px,calc((100vw - 80px)*37/1140)) where `.mm-sugar .mm-t2` at (min-width:641px) |
| `.mm-t3` | **none of the nine** | margin-left: min(35px,calc((100vw - 80px)*35/1140)) where `.mm-sugar .mm-t3` at (min-width:641px) |
| `.mm-tab` | **none of the nine** | display: inline-block where `.mm-sugar .mm-tab`<br>margin-left: 24px where `.mm-sugar .mm-tab` at (max-width:640px) |
| `.mm-tab1` | **none of the nine** | margin-left (by width): 48px ! ; 0 ! at (max-width:640px) |
| `.mm-table` | PL 1 | border-top: 1px solid var(--rule) ! |
| `.mm-table-wrap` | PL 1 | clear: both |
| `.mm-text` | Cult 5, Math 4, Sens 37 | flex (by condition): 0 1 auto where `.mm-set .mm-text` ; 1 1 0 where `.mm-set.mm-intro .mm-text`<br>max-width: none ! where `.mm-set .mm-text` at (max-width:640px)<br>min-width: 0 where `.mm-set .mm-text`<br>width: auto ! where `.mm-set .mm-text` at (max-width:640px) |
| `.mm-toc3` | SRes 1, RoA 1 | column-gap: 40px where `.toc .toc-grid.mm-toc3`<br>display: grid ! where `.toc .toc-grid.mm-toc3`<br>grid-template-columns (by width): repeat(3,1fr) where `.toc .toc-grid.mm-toc3` ; 1fr where `.toc .toc-grid.mm-toc3` at (max-width:640px) |
| `.mm-trio` | **none of the nine** | align-items: flex-start<br>clear: both<br>display: flex<br>flex-wrap: wrap at (max-width:640px)<br>gap (by width): 0 ; 12px at (max-width:640px)<br>justify-content: center at (max-width:640px) |
| `.mm-under` | **none of the nine** | padding-left: 30px |
| `.mm-w` | **none of the nine** | color: #0432FF where `.mm-sugar .mm-w` |
| `.mm-wi` | **none of the nine** | margin-left: 0 !<br>padding-left: 0 ! |
| `.mq` | **none of the nine** | font-family: var(--display)<br>font-size: 17px<br>font-style: italic<br>font-weight: 400<br>line-height: 1.65<br>margin (by width): 24px 38px ; 20px 0 at (max-width:640px)<br>margin-left (by width): 20px ! ; 0 ! at (max-width:640px)<br>margin-right (by width): 20px ! ; 0 ! at (max-width:640px)<br>padding: 0 |
| `.np` | Jour 74, Aun 74, Bio 74, SRes 74, Cult 74, Math 74, PL 74, RoA 74, Sens 74 | color (by width and condition): var(--ink) where `.grp .np` ; var(--ink) where `.grp li.lead .np` ; #0432FF where `.panel.cat .grp li.lead .np` ; #E7EEF5 where `.grp .np` at (max-width:960px) ; #fff where `.grp li.lead .np` at (max-width:960px) ; #8FC6FF where `.panel.cat .grp li.lead .np` at (max-width:960px) ; #0432FF ! where `.panel .grp li.lead > .np` at (min-width:831px) ; #2B2B2B ! where `.panel .grp li:not(.lead):not(.hd) > .np` at (min-width:831px)<br>cursor: default where `.grp .np`<br>display: block where `.grp .np`<br>font-family: var(--serif) where `.grp .np`<br>font-size (by width): 17px where `.grp .np` ; 17px where `.grp .np` at (max-width:960px) ; 18px ! where `.grp .np` at (min-width:641px) ; 17px ! where `.grp .np` at (max-width:640px)<br>font-weight (by width and condition): 400 where `.grp li.lead .np` ; 400 ! where `.panel .grp li.lead > .np` at (min-width:831px) ; 400 ! where `.panel .grp li:not(.lead):not(.hd) > .np` at (min-width:831px)<br>line-height: 1.3 where `.grp .np`<br>padding (by width): 8px 0 where `.grp .np` ; 7px 0 where `.grp .np` at (max-width:960px) |
| `.np-top` | **none of the nine** | color: #fff where `.menu .top.np-top:hover`<br>cursor (by width): default where `.menu .top.np-top` ; pointer where `.menu .top.np-top` at (max-width:960px) |
| `.on` | **none of the nine** | background: var(--ink) where `.mm-dots span.on` at (max-width:640px) |
| `.op` | Sens 11 | border-top: 0 where `.formula-table tr.rule td.op`<br>padding-right: 12px where `.formula-table td.op`<br>width: 1.2em where `.formula-table td.op` |
| `.open` | **none of the nine** | display (by width and condition): block where `.site-nav.open` at (max-width:960px) ; flex where `.lightbox.open` |
| `.over` | **none of the nine** | grid-column: 1 / -1 where `.panel-in > .pcol.over`<br>margin-bottom (by width): -12px where `.panel-in > .pcol.over` ; 0 where `.panel-in > .pcol.over` at (max-width:960px) |
| `.page-h2` | **none of the nine** | border-bottom: 2px solid var(--head)<br>color: var(--head)<br>font-family: var(--serif)<br>font-size: 24px<br>font-weight: 500<br>line-height: 1.2<br>margin: 40px 0 16px<br>padding-bottom: 8px |
| `.panel` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | background (by width): #fff ; transparent at (max-width:960px) ; #F5EEE3 ! at (min-width:831px)<br>border: 0 at (max-width:960px)<br>border-bottom (competing): **competing**: 0 ! wins over 1px solid var(--line)<br>box-shadow (by width): 0 14px 28px rgba(20,30,40,.14) ; none at (max-width:960px)<br>display (by width and condition): none ; **competing** where `.has-panel:focus-within > .panel`: none wins over block ; block where `.has-panel.open > .panel` ; none where `.has-panel:focus-within > .panel` at (max-width:960px) ; block where `.has-panel.open > .panel` at (max-width:960px)<br>flex: 0 0 100% at (max-width:960px)<br>left: 0<br>position (by width): absolute ; static at (max-width:960px)<br>right: 0<br>top: 100% |
| `.panel-in` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | display (by width): grid ; block at (max-width:960px)<br>gap (by condition): 26px 48px ; 26px 40px where `.panel-in.c4`<br>grid-template-columns (by condition): repeat(3,minmax(0,1fr)) ; minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) where `.panel-in.c1` ; repeat(4,minmax(0,1fr)) where `.panel-in.c4`<br>margin: 0 auto<br>max-width: 1280px<br>padding (by width): 26px 40px 30px ; 0 0 10px 14px at (max-width:960px) |
| `.pcol` | Jour 25, Aun 25, Bio 25, SRes 25, Cult 25, Math 25, PL 25, RoA 25, Sens 25 | display (by width): flex where `.panel-in > .pcol` ; block where `.panel-in > .pcol` at (max-width:960px)<br>flex-direction: column where `.panel-in > .pcol`<br>gap: 22px where `.panel-in > .pcol`<br>grid-column: 1 / -1 where `.panel-in > .pcol.over`<br>margin-bottom (by width): -12px where `.panel-in > .pcol.over` ; 0 where `.panel-in > .pcol.over` at (max-width:960px)<br>margin-top (by condition): 24px where `.panel-in > .pcol + .pcol` at (max-width:960px) ; 0 where `#p-resources .panel-in > .pcol + .pcol` at (max-width:960px)<br>min-width: 0 where `.panel-in > .pcol` |
| `.pdf` | SRes 8, RoA 17 | background: #0563C1 where `a.pdf:hover`<br>border: 1.5px solid #0563C1<br>border-color: #0563C1 ! where `h3.res-src a.pdf`<br>border-radius: 2px<br>color (by condition): #0563C1 ! ; #fff ! where `a.pdf:hover` ; #0563C1 ! where `h3.res-src a.pdf` ; #fff ! where `h3.res-src a.pdf:hover`<br>display (by width and condition): inline-block ; block ! where `.res-item:has(> .meta > a.pdf)` at (max-width:640px) ; block ! where `.res-item:has(> a.pdf)` at (max-width:640px) ; inline ! where `.res-item > .meta > a.pdf` at (max-width:640px) ; inline ! where `.res-item > a.pdf` at (max-width:640px)<br>font-family: var(--sans, sans-serif)<br>font-size: 11px<br>font-weight: 400<br>letter-spacing: .06em<br>line-height: 1<br>margin-left (by width and condition): 24px where `p a.pdf` ; 30px ! where `.pdf-date + a.pdf` ; 6px ! where `.res-item > .pdf-date + a.pdf` ; 24px where `h3.res-src a.pdf` ; 24px ! where `.res-item > .meta > a.pdf` at (max-width:640px) ; 24px ! where `.res-item > a.pdf` at (max-width:640px)<br>padding: 4px 6px<br>text-decoration: none<br>vertical-align: .12em |
| `.pdf-date` | **none of the nine** | margin-left (by condition): 10px ! where `a.pdf + .pdf-date` ; -14px ! where `.res-item > a.pdf + .pdf-date` |
| `.ph` | Jour 152, Aun 58, Bio 21, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | flex (by width and condition): none ; none where `.mm-trio>figure.ph` ; none where `.mm-trio>figure.ph` at (max-width:640px)<br>margin (by condition): 0 ; 0 where `.mm-trio>figure.ph`<br>min-width: 0<br>scroll-snap-align: center where `.mm-imgs .ph` at (max-width:640px) |
| `.pim` | Jour 152, Aun 58, Bio 22, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | aspect-ratio (by condition): **competing** where `#mm-fitR .pim`: 1 ! wins over var(--arR) ! ; 0.681 ! where `#mm-fit10 .pim`<br>background: transparent where `.ph .pim`<br>border-radius (by condition): **competing** where `.ph .pim`: 6px wins over 2px ; 50% ! where `#mm-fitR .pim`<br>height (by width and condition): calc(var(--mh,153) * 1px) where `.mm-imgs .pim` ; **competing** where `.mm-float .pim`: 150px ! wins over auto ; var(--mh,168px) where `.mm-trio .pim` ; 110px where `.mm-trio .pim` at (max-width:640px) ; auto ! where `#mm-fitR .pim` ; 180px ! where `#mm-fitR .pim` at (max-width:640px) ; 180px ! where `#mm-fit10 .pim` at (max-width:640px) ; auto ! where `#mm-fit10 .pim` ; calc(var(--hp,168) * 1px) ! where `.mm-imgs .pim` at (max-width:640px) ; 70px ! where `.mm-set.mm-col .mm-imgs .pim` at (max-width:640px) ; 240px ! where `.mm-set.mm-intro .mm-imgs .pim` at (max-width:640px) ; auto ! where `.mm-set.mm-formula .mm-imgs .pim` at (max-width:640px)<br>margin (by condition): 0 auto where `#mm-fitR .pim` at (max-width:640px) ; 0 auto where `#mm-fit10 .pim` at (max-width:640px)<br>max-width: none where `#mm-fit10 .pim`<br>overflow (by condition): hidden where `.ph .pim` ; hidden where `#mm-fitR .pim`<br>position: relative where `.ph .pim`<br>width (by width and condition): auto where `.mm-imgs .pim` ; auto where `.mm-trio .pim` ; auto where `.mm-trio .pim` at (max-width:640px) ; auto ! where `#mm-fitR .pim` at (max-width:640px) ; auto ! where `#mm-fit10 .pim` at (max-width:640px) ; min(300px, 100%) ! where `.mm-set.mm-formula .mm-imgs .pim` at (max-width:640px) ; auto ! where `.mm-float .pim` |
| `.preview-grid` | Sens 1 | column-gap: 24px<br>display: grid<br>grid-auto-flow (by width): column ; row at (max-width:640px)<br>grid-template-columns (by width): 1fr 1fr ; 1fr at (max-width:640px)<br>grid-template-rows (by width): repeat(7,auto) ; none at (max-width:640px) |
| `.preview-line` | Sens 15 | color: var(--ink)<br>font-size: 17px<br>font-style: italic<br>margin: 8px 0 |
| `.pullquote` | SRes 2, Cult 1, Math 6, PL 15, Sens 2 | border: none<br>clear: both<br>color: #000<br>font-family: var(--display)<br>font-size (by width): 18px ! ; 17px ! at (max-width:830px)<br>line-height (by width): 40px ! ; 38px ! at (max-width:830px)<br>margin (by width): **competing**: 24px 38px ! wins over 24px 0 !, 32px auto ; 20px 0 ! at (max-width:640px)<br>margin-left (by width and condition): 20px ! ; 0 ! where `#books-on-music-in-montessori blockquote.pullquote` ; 0 ! at (max-width:640px) ; 0 ! where `:root body main blockquote.pullquote`<br>margin-right (by width and condition): 20px ! ; 0 ! at (max-width:640px) ; 0 ! where `:root body main blockquote.pullquote`<br>max-width (by width): **competing**: none ! wins over 90% ; 100% at (max-width:640px)<br>padding: 0<br>padding-left: 0 ! where `#books-on-music-in-montessori blockquote.pullquote`<br>position: relative<br>text-align: left<br>text-indent: 0 ! where `#books-on-music-in-montessori blockquote.pullquote` |
| `.q-ref` | **none of the nine** | font-style: normal where `.pullquote .q-ref` |
| `.ref-desc` | Sens 16 | color: var(--ink)<br>flex: 1 |
| `.ref-row` | Sens 16 | border-bottom: 1px solid var(--rule)<br>display: flex<br>flex-direction: column at (max-width:640px)<br>gap (by width): 24px ; 4px at (max-width:640px)<br>padding: 16px 0 |
| `.ref-table` | Sens 2 | border-top: 1px solid var(--rule)<br>clear: both<br>margin-top: 8px |
| `.res-book` | SRes 6 | margin-bottom: 0 where `.res-item.res-book`<br>margin-top (by width and condition): 35px where `.res-item.res-book` ; 0 ! where `> h2 + .res-item.res-book` ; -0.8px ! where `> h2 + .res-item.res-book` at (max-width:640px) |
| `.res-desc` | SRes 12, RoA 35 | color: #000<br>font-size (by width): 18px ! ; 17px ! at (max-width:640px)<br>line-height (by width): 37.2px ; 36px at (max-width:640px)<br>margin: 4px 0 !<br>margin-top (by condition): **competing** where `.res-entry p.res-desc + p.res-desc`: 6.8px ! wins over 14.3px ! ; **competing** where `.res-entry p.res-desc.res-label`: 9.8px ! wins over 17.3px ! ; **competing** where `.res-entry p.res-desc + p.res-desc.res-label`: 9.8px ! wins over 17.3px ! ; **competing** where `.res-entry p.res-desc.res-label + p.res-desc`: -4px ! wins over 3.5px ! ; **competing** where `.res-entry > h3.material-name + .res-desc`: -0.45px ! wins over 3.3px ! |
| `.res-entry` | SRes 13, RoA 22 | margin: 0 0 8px |
| `.res-item` | SRes 21, RoA 24 | align-items: baseline<br>column-gap: 24px<br>display: flex<br>flex-wrap: wrap<br>font-size (by width): 18px ! ; 17px ! at (max-width:640px)<br>margin: 4px 0<br>margin-bottom: 0 where `.res-item.res-book`<br>margin-top (by width and condition): 35px where `.res-item.res-book` ; **competing** where `.res-entry .res-desc + .res-item`: 19.55px ! wins over 23.3px ! ; 0 ! where `> h2 + .res-item.res-book` ; -0.8px ! where `> h2 + .res-item.res-book` at (max-width:640px) ; 3.3px ! where `.res-entry > h3.material-name + .res-item` ; -3.4px ! where `.res-entry > h3.material-name + .res-item:not(:has(.res-title))` ; 7.3px ! where `.res-entry .res-item + .res-item` ; 4px ! where `.res-entry .res-item.mm-ami`<br>row-gap: 4px |
| `.res-item-line` | **none of the nine** | margin-bottom: 0<br>margin-top: 3.5px ! where `.res-book + .res-item-line` |
| `.res-label` | **none of the nine** | margin-top (by condition): **competing** where `.res-entry p.res-desc.res-label`: 9.8px ! wins over 17.3px ! ; **competing** where `.res-entry p.res-desc + p.res-desc.res-label`: 9.8px ! wins over 17.3px ! |
| `.res-link` | SRes 2 | margin-top: 4px where `.res-link + .res-link` |
| `.res-title` | SRes 21, RoA 25 | color: #0432FF where `.res-item .res-title`<br>display (by condition): inline ! where `.res-item:has(> .meta > a.pdf) > .res-title` at (max-width:640px) ; inline ! where `.res-item:has(> a.pdf) > .res-title` at (max-width:640px)<br>font-size (by width): 18px ! where `.res-item .res-title` ; 17px ! where `.res-item .res-title` at (max-width:640px)<br>font-style: italic where `.res-item .res-title` |
| `.section` | Jour 1, Aun 1, Bio 1, SRes 4, Cult 36, Math 28, PL 2, RoA 1, Sens 15 | border-top (competing): **competing**: 0 wins over 1px solid var(--ink)<br>clear: both<br>margin-top (by width and condition): **competing**: 32.3px ! wins over 48px, 64px ; **competing** where `.section:first-of-type`: 32px wins over 40px ; 72px where `section.section.sense` ; 56px where `section.section.sense` at (max-width:640px) ; 34px ! at (max-width:640px)<br>padding-top (competing): **competing**: 0 wins over 24px |
| `.sense` | Sens 4 | margin-top (by width): 72px where `section.section.sense` ; 56px where `section.section.sense` at (max-width:640px) |
| `.seq-line` | Sens 2 | padding-left (by width): 48px ; 24px at (max-width:640px) |
| `.site-foot` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: transparent !<br>border-top (competing): **competing**: 0 ! wins over 1px solid var(--line)<br>margin-top (competing): **competing**: 0 ! wins over 24px |
| `.site-foot-in` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items (by width): center ; flex-start at (max-width:640px)<br>color (by condition): var(--quiet) ; #6B6B6B ! where `.site-foot .site-foot-in`<br>display: flex<br>flex-direction: column at (max-width:640px)<br>font-size (by width): 15px ; 15px ! at (min-width:641px) ; 15px ! at (max-width:640px)<br>gap: 16px<br>justify-content: space-between<br>margin: 0 auto<br>max-width: var(--page)<br>padding (by width): 32px var(--gutter) 48px ; 28px 24px 40px at (max-width:640px)<br>padding-bottom: 17.625px ! where `.site-foot .site-foot-in` at (min-width:641px)<br>padding-top: 17.625px ! where `.site-foot .site-foot-in` at (min-width:641px) |
| `.site-head` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: var(--navy)<br>position: sticky<br>top: env(safe-area-inset-top,0px)<br>z-index: 40 |
| `.site-head-in` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display: flex<br>gap (by width): 24px ; 14px at (min-width:961px) and (max-width:1279px) ; 12px at (min-width:961px) and (max-width:1023px)<br>height (by width): 76px ; 60px at (max-width:960px)<br>justify-content: space-between<br>margin: 0 auto<br>max-width: 1280px<br>padding (by width): 0 40px ; 0 24px at (max-width:1180px) ; 0 8px 0 18px at (max-width:960px) ; 0 24px at (min-width:961px) and (max-width:1279px) ; 0 18px at (min-width:961px) and (max-width:1023px)<br>padding-left: 16px ! at (min-width:961px) and (max-width:1099px)<br>padding-right: 16px ! at (min-width:961px) and (max-width:1099px) |
| `.site-name` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color: #fff<br>font-family: var(--display)<br>font-size (by width): 25px ; 21px at (max-width:960px) ; 25px ! at (min-width:641px) ; 21px ! at (max-width:640px)<br>font-weight: 500<br>text-decoration: none<br>white-space: nowrap |
| `.site-nav` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: var(--navy) at (max-width:960px)<br>box-shadow: 0 12px 24px rgba(0,0,0,.18) at (max-width:960px)<br>display (by condition): none at (max-width:960px) ; block where `.site-nav.open` at (max-width:960px)<br>left: 0 at (max-width:960px)<br>max-height: calc(100vh - 60px) at (max-width:960px)<br>overflow-y: auto at (max-width:960px)<br>padding: 4px 18px 16px at (max-width:960px)<br>position: absolute at (max-width:960px)<br>right: 0 at (max-width:960px)<br>top: 60px at (max-width:960px) |
| `.site-tools` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | align-items: center<br>display: flex<br>gap: 2px |
| `.skip` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background: #fff where `.skip:focus`<br>left (by condition): -9999px ; 12px where `.skip:focus`<br>padding: 8px 12px where `.skip:focus`<br>position: absolute<br>top (by condition): 0 ; 12px where `.skip:focus`<br>z-index: 50 where `.skip:focus` |
| `.sub` | **none of the nine** | font-size (by width): 26px where `.hero h1 .sub` ; 19px where `.hero h1 .sub` at (max-width:640px)<br>margin-top: 6px where `.hero h1 .sub` |
| `.sub-label` | Jour 17, Sens 53 | font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',serif<br>font-size (by width): **competing**: 18px wins over 21px ; **competing** at (max-width:640px): 17px wins over 19px<br>font-weight: 400 !<br>margin-bottom: 0<br>margin-top: 15px |
| `.sub-toggle` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | align-items: center<br>background: none<br>border: 0<br>color: #fff<br>cursor: pointer<br>display: inline-flex<br>height (by width): 30px ; 44px at (max-width:960px)<br>justify-content: center<br>margin-left (by width and condition): 1px ; 1px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>min-width: 13px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>opacity: .85<br>padding (by width and condition): 0 ; 0 ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px)<br>width (by width and condition): 22px ; 44px at (max-width:960px) ; 16px at (min-width:961px) and (max-width:1279px) ; 13px ! where `.menu .sub-toggle` at (min-width:961px) and (max-width:1099px) |
| `.swatch` | Sens 1 | background: #fff<br>border: 1px solid #8F8F8F<br>border-radius: 50%<br>display: inline-block<br>height: .6em<br>margin-left: .28em<br>vertical-align: .04em<br>width: .6em |
| `.tight-bottom` | Sens 111 | margin-bottom: 5px |
| `.tight-top` | Sens 133 | margin-top: 5px |
| `.title-block` | **none of the nine** | padding: 56px 0 8px<br>text-align: center |
| `.toc-grid` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | column-gap: 40px where `.toc .toc-grid.mm-toc3`<br>display (by condition): grid ; grid ! where `.toc .toc-grid.mm-toc3`<br>gap: 6px 40px<br>grid-template-columns (by width and condition): 1fr 1fr ; 1fr at (max-width:640px) ; repeat(3,1fr) where `.toc .toc-grid.mm-toc3` ; 1fr where `.toc .toc-grid.mm-toc3` at (max-width:640px) |
| `.toc-label` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color (by condition): var(--head) ; #00B050 ! where `.toc .toc-label`<br>font-family: var(--serif)<br>font-size (by width and condition): **competing**: 22px ! wins over 24px ; **competing** at (max-width:640px): 19px ! wins over 20px !, 22px ; 20px ! where `.toc .toc-label` ; 20px ! where `.toc-wrap .toc-label` at (min-width:641px) ; 20px ! where `.toc .toc-label` at (min-width:641px) ; 20px ! at (min-width:641px) ; 19px ! where `.toc-wrap .toc-label` at (max-width:640px) ; 19px ! where `.toc .toc-label` at (max-width:640px)<br>font-style: normal ! where `.toc .toc-label`<br>font-weight (by condition): 500 ; 400 ! where `.toc .toc-label`<br>margin: 0 0 14px |
| `.toc-num` | **none of the nine** | color: var(--ink)<br>flex: 0 0 22px<br>font-size: 17px<br>font-variant-numeric: tabular-nums<br>font-weight: 600 |
| `.toc-wrap` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | display: none where `.toc-wrap:not(:has(li))`<br>margin: 0 auto<br>max-width: 1100px<br>padding (by width): 26px 0 36px ; 22px 24px 26px at (max-width:640px) |
| `.top` | Jour 8, Aun 8, Bio 8, SRes 8, Cult 8, Math 8, PL 8, RoA 8, Sens 8 | border-bottom (by width): 0 where `.menu .top` ; 0 where `.menu .top` at (max-width:960px)<br>color (by condition): #fff where `.menu .top` ; #DCE6F0 where `.menu .top:hover` ; #fff where `.menu .top.np-top:hover`<br>cursor (by width): default where `.menu .top.np-top` ; pointer where `.menu .top.np-top` at (max-width:960px)<br>flex: 1 1 auto where `.menu .top` at (max-width:960px)<br>font-family: var(--serif) where `.menu .top`<br>font-size (by width): 17px where `.menu .top` ; 16px where `.menu .top` at (max-width:1180px) ; 18px where `.menu .top` at (max-width:960px) ; 16px where `.menu .top` at (min-width:961px) and (max-width:1023px) ; 18px ! where `.menu .top` at (min-width:641px) ; 17px ! where `.menu .top` at (max-width:640px)<br>font-weight: 400 where `.menu .top`<br>padding (by width): 6px 0 7.5px where `.menu .top` ; 13px 0 where `.menu .top` at (max-width:960px)<br>text-decoration (by width and condition): none where `.menu .top` ; underline where `.menu .top[aria-current="page"]` ; underline where `.menu .top[aria-current="page"]` at (max-width:960px)<br>text-underline-offset (by width): 4px where `.menu .top[aria-current="page"]` ; 4px where `.menu .top[aria-current="page"]` at (max-width:960px)<br>white-space: nowrap where `.menu .top` |
| `#mm-fit10` | **none of the nine** | float (by width): right ; none at (max-width:640px)<br>margin (by width): 0 0 12px 32px ; 12px 0 at (max-width:640px) |
| `#mm-fitR` | **none of the nine** | float (by width): right ; none at (max-width:640px)<br>margin (by width): 0 0 12px 32px ; 12px 0 at (max-width:640px) |
| `#mm-ms` | **none of the nine** | margin-top: 0 ! where `.res-entry > h3.material-name + #mm-ms` |
| `a` | Jour 44, Aun 44, Bio 48, SRes 74, Cult 83, Math 99, PL 60, RoA 79, Sens 52 | align-items: baseline where `.toc-groups a`<br>border-bottom: 1px solid transparent where `.toc a`<br>border-bottom-color: var(--head) where `.toc a:hover`<br>color (by width and condition): **competing**: #0563C1 wins over var(--head), var(--material) ; var(--ink) where `.grp a` ; var(--head) where `.grp a:hover` ; **competing** where `.grp li.lead a`: var(--ink) wins over var(--head) ; **competing** where `.grp a[aria-current="page"]`: var(--ink) wins over var(--head) ; **competing** where `.toc a`: #000 ! wins over var(--link) ; var(--head) where `.toc a:hover` ; **competing** where `.site-foot a`: #6B6B6B ! wins over var(--quiet) ; #E7EEF5 where `.grp a` at (max-width:960px) ; #fff where `.grp li.lead a` at (max-width:960px) ; #fff where `.grp a[aria-current="page"]` at (max-width:960px) ; #EE0000 ! where `.res-entry h3.material-name a` ; #0563C1 where `.res-item .res-title a` ; inherit ! where `.res-src a[href*=biodiversitylibrary]` ; #0432FF ! where `a:not(.pdf)` ; #0432FF where `.panel.cat .grp li.lead a` ; #8FC6FF where `.panel.cat .grp li.lead a` at (max-width:960px) ; #E7EEF5 ! where `.panel .grp a[aria-current="page"]` at (max-width:960px) ; #8FC6FF ! where `#p-essentialelements .grp a[aria-current="page"]` at (max-width:960px) ; #8FC6FF ! where `#p-curriculum .grp a[aria-current="page"]` at (max-width:960px) ; #0432FF ! where `.panel .grp li.lead > a` at (min-width:831px) ; #2B2B2B ! where `.panel .grp li:not(.lead):not(.hd) > a` at (min-width:831px) ; #2B2B2B ! where `.panel .grp a[aria-current="page"]` at (min-width:831px)<br>display (by condition): block where `.grp a` ; flex where `.toc-groups a`<br>font-family: var(--serif) where `.grp a`<br>font-size (by width and condition): 17px where `.grp a` ; **competing** where `.toc a`: 18px ! wins over 19px ; 17px where `.grp a` at (max-width:960px) ; **competing** where `.toc a` at (max-width:640px): 17px ! wins over 18px ; 18px ! where `.grp a` at (min-width:641px) ; 18px ! where `.toc a` at (min-width:641px) ; 15px ! where `.site-foot-in a` at (min-width:641px) ; 17px ! where `.grp a` at (max-width:640px) ; 15px ! where `.site-foot-in a` at (max-width:640px)<br>font-style: normal ! where `.toc a`<br>font-weight (by width and condition): **competing** where `.grp li.lead a`: 400 wins over 600 ; 400 ! where `.toc a` ; 400 where `.menu a` ; 400 ! where `.panel .grp li.lead > a` at (min-width:831px) ; 400 ! where `.panel .grp li:not(.lead):not(.hd) > a` at (min-width:831px)<br>gap: 8px where `.toc-groups a`<br>line-height (by condition): 1.3 where `.grp a` ; 1.35 where `.toc a`<br>margin-left: 30px ! where `.pdf-date + a`<br>outline (by condition): 2px solid var(--active) where `a:focus-visible` ; 2px solid #fff where `.site-head a:focus-visible`<br>outline-offset (by condition): 3px where `a:focus-visible` ; 3px where `.site-head a:focus-visible`<br>overflow-wrap: anywhere<br>padding (by width): 8px 0 where `.grp a` ; 7px 0 where `.grp a` at (max-width:960px)<br>text-decoration (by condition): none where `.grp a` ; underline where `.grp a[aria-current="page"]` ; none where `.toc a` ; underline where `.res-src a[href*=biodiversitylibrary]` ; underline where `.grp a:hover`<br>text-underline-offset (by condition): 3px where `.grp a[aria-current="page"]` ; 3px where `.grp a:hover` |
| `b` | **none of the nine** | font-weight (by condition): 700 ! ; 400 ! where `.res-title b` ; 400 ! where `h3 b` |
| `blockquote` | SRes 2, Cult 1, Math 6, PL 15, Sens 2 | flex: 1 1 auto where `.mm-trio>blockquote`<br>flex-basis: 100% where `.mm-trio>blockquote` at (max-width:640px)<br>font-size (by width and condition): 18px ! ; 17px ! at (max-width:830px) ; 18px ! where `blockquote:not(#mmz)` at (min-width:641px) ; 17px ! where `blockquote:not(#mmz)` at (max-width:640px)<br>line-height (by width): 40px ! ; 38px ! at (max-width:830px)<br>min-width: 0 where `.mm-trio>blockquote`<br>order: -1 where `.mm-trio>blockquote` at (max-width:640px) |
| `body` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | background (competing): **competing**: #F5EEE3 ! wins over var(--bg), var(--paper)<br>color: var(--ink)<br>font-family (competing): **competing**: var(--serif) wins over 'EB Garamond',Georgia,serif<br>font-size (by width): **competing**: 18px wins over 19px ; 17px at (max-width:640px)<br>line-height (competing): **competing**: 1.65 wins over 1.7<br>margin: 0<br>padding-bottom: env(safe-area-inset-bottom,0px)<br>padding-top: env(safe-area-inset-top,0px) |
| `button` | Jour 11, Aun 11, Bio 11, SRes 11, Cult 11, Math 11, PL 11, RoA 11, Sens 11 | outline (by condition): 2px solid var(--active) where `button:focus-visible` ; 2px solid #fff where `.site-head button:focus-visible`<br>outline-offset (by condition): 3px where `button:focus-visible` ; 3px where `.site-head button:focus-visible` |
| `cite` | SRes 1, Math 3, PL 14, Sens 2 | color (by condition): var(--ink) where `blockquote.pullquote cite` ; #000 where `.pullquote cite`<br>display (by condition): block where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: block ! wins over  ; block ! where `blockquote cite`<br>font-family (competing): **competing** where `blockquote.pullquote cite`: var(--serif) ! wins over inherit, var(--display)<br>font-size (by width and condition): **competing** where `blockquote.pullquote cite`: 18px ! wins over 17px, 1em ; 18px ! where `blockquote cite` ; 17px ! where `blockquote cite` at (max-width:830px) ; 17px ! where `blockquote.pullquote cite` at (max-width:830px) ; 18px ! where `blockquote:not(#mmz) cite` at (min-width:641px) ; 17px ! where `blockquote:not(#mmz) cite` at (max-width:640px)<br>font-style (by condition): normal where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: normal ! wins over  ; normal ! where `blockquote cite`<br>font-weight: 400 ! where `blockquote.pullquote cite`<br>line-height (by width and condition): 40px ! where `blockquote cite` ; 40px ! where `blockquote.pullquote cite` ; 38px ! where `blockquote cite` at (max-width:830px) ; 38px ! where `blockquote.pullquote cite` at (max-width:830px)<br>margin-top (by condition): 6px where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: 0 ! wins over 8px ; 0 ! where `blockquote cite`<br>padding-left (by condition): 48px where `blockquote.mq cite` ; **competing** where `blockquote.pullquote cite`: 48px ! wins over 0 ! ; 48px ! where `:root body main blockquote.pullquote cite`<br>text-indent: 0 ! where `:root body main blockquote.pullquote cite` |
| `div` | Jour 287, Aun 138, Bio 99, SRes 112, Cult 500, Math 402, PL 349, RoA 126, Sens 649 | break-inside: avoid where `.materials-table div`<br>color: var(--ink) where `.preview-grid > div`<br>font-size: 17px where `.preview-grid > div`<br>font-style: italic where `.preview-grid > div`<br>margin: 8px 0 where `.preview-grid > div`<br>padding: 4px 0 where `.materials-table div` |
| `em` | Aun 1, Bio 9, SRes 29, Cult 7, Math 38, PL 23, RoA 29, Sens 5 | font-style (by condition): italic where `.res-item .res-title em` ; italic ! where `blockquote.pullquote em` ; italic ! where `p em` ; italic ! where `li em` ; italic ! where `.micro-label em` |
| `figcaption` | Bio 9, Sens 3 | color: var(--ink) where `.ph figcaption`<br>font-family: 'EB Garamond',serif where `.ph figcaption`<br>font-size (by width and condition): 15px where `.ph figcaption` ; 16px ! at (min-width:641px) ; 16px ! at (max-width:640px)<br>line-height: 1.3 where `.ph figcaption`<br>margin-top: 6px where `.ph figcaption`<br>min-width: 100% where `.ph figcaption`<br>text-align: center where `.ph figcaption`<br>width: 0 where `.ph figcaption` |
| `figure` | Jour 152, Aun 58, Bio 21, SRes 14, Cult 250, Math 153, PL 163, RoA 3, Sens 208 | display (by condition): block ! where `#mm-fitR figure` ; block ! where `#mm-fit10 figure`<br>height (by condition): auto ! where `#mm-ms .mm-msfloat figure` ; auto ! where `#mm-fitR figure` ; auto ! where `#mm-fit10 figure` |
| `h1` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | color (by condition): #fff where `.hero h1` ; var(--title)<br>font-family (by condition): var(--display) where `.hero h1` ; 'Cormorant Garamond',Georgia,serif<br>font-size (by width and condition): 40px where `.hero h1` ; **competing** where `.hero h1` at (max-width:640px): 28px ! wins over  ; 30px ; 26px at (max-width:640px) ; 40px ! where `.hero h1` at (min-width:641px)<br>font-weight (by condition): 500 where `.hero h1` ; 700<br>line-height (by condition): 1.2 where `.hero h1` ; 1.15<br>margin (by condition): 0 where `.hero h1` ; 0<br>max-width: 760px where `.hero h1`<br>position: relative where `.hero h1`<br>text-shadow: 0 1px 12px rgba(0,0,0,.4) where `.hero h1`<br>z-index: 1 where `.hero h1` |
| `h2` | SRes 4, Cult 37, Math 12, Sens 15 | border-bottom (by condition): 2px solid var(--head) ; 2px solid currentColor ! where `section>h2` ; 0 ! where `h2:not(.mm-hc-00B050)`<br>border-bottom-color: #00B050 !<br>color (by condition): **competing**: #00B050 ! wins over var(--head), var(--heading) ; #0432FF ! where `h2:not(.mm-hc-00B050)`<br>font-family (competing): **competing**: var(--serif) wins over 'Cormorant Garamond',Georgia,serif<br>font-size (by width and condition): **competing**: 20px ! wins over 22px !, 24px !, 25px ; **competing** at (max-width:640px): 19px ! wins over 20px !, 22px, 22px ! ; 23px ! at (min-width:641px) ; 18px ! where `h2:not(.mm-hc-00B050)` ; 18px ! where `h2:not(.mm-hc-00B050)` at (min-width:641px) ; 17px ! where `h2:not(.mm-hc-00B050)` at (max-width:640px)<br>font-style: normal !<br>font-weight (by condition): **competing**: 400 ! wins over 500, 700 ; 400 ! where `h2:not(.mm-hc-00B050)`<br>line-height (competing): **competing**: 1.2 wins over 1.25<br>margin: 0<br>margin-bottom (competing): **competing**: 8px ! wins over 16px<br>padding-bottom (by condition): 8px ; 8px ! where `section>h2` ; 0 ! where `h2:not(.mm-hc-00B050)` |
| `h3` | SRes 13, RoA 21, Sens 30 | font-size (by width): 18px ! at (min-width:641px) ; 17px ! at (max-width:640px)<br>font-weight: 400 ! |
| `h4` | **none of the nine** | font-weight: 400 ! |
| `html` | **none of the nine** | -webkit-text-size-adjust: 100%<br>background: #F5EEE3 !<br>scroll-behavior: smooth at (prefers-reduced-motion:no-preference)<br>scroll-padding-top (by width): calc(76px + env(safe-area-inset-top,0px)) ; calc(64px + env(safe-area-inset-top,0px)) at (max-width:960px) |
| `i` | **none of the nine** | font-style (by condition): italic ! where `p i` ; italic ! where `li i` ; italic ! where `.micro-label i` |
| `img` | Jour 153, Aun 59, Bio 24, SRes 15, Cult 251, Math 154, PL 164, RoA 4, Sens 209 | box-shadow: 0 20px 60px rgba(0,0,0,.5) where `.lightbox img`<br>display (by condition): block ; block where `.lb-frame img`<br>height (by condition): 100% ! where `#mm-fitR .pim img` ; 100% ! where `#mm-fit10 .pim img`<br>max-height: 100% where `.lightbox img`<br>max-width (by condition): 100% ; 100% where `.lightbox img`<br>object-fit (by condition): contain where `.lightbox img` ; cover where `#mm-fitR .pim img` ; cover where `#mm-fit10 .pim img`<br>width (by condition): 100% ! where `#mm-fitR .pim img` ; 100% ! where `#mm-fit10 .pim img` |
| `li` | Jour 122, Aun 122, Bio 122, SRes 128, Cult 209, Math 260, PL 153, RoA 133, Sens 141 | align-items (by width): center where `.menu > li` ; center where `.menu > li` at (max-width:960px)<br>border-bottom (by width and condition): 1px solid var(--line) where `.grp li` ; 0 where `.grp li:last-child` ; 1px solid rgba(255,255,255,.2) where `.menu > li` at (max-width:960px) ; 0 where `.grp li` at (max-width:960px) ; 0 ! where `.panel .grp li` ; 0 ! where `#site-nav li` ; 0 ! where `.menu .panel li`<br>color: #000<br>counter-increment: mmn where `ol>li`<br>display (by width): flex where `.menu > li` ; flex where `.menu > li` at (max-width:960px)<br>flex-wrap: wrap where `.menu > li` at (max-width:960px)<br>font-size (by width): 18px ! ; 17px ! at (max-width:640px) ; 18px ! at (min-width:641px)<br>font-weight: 400 where `.grp li`<br>height (by width): 76px where `.menu > li` ; auto where `.menu > li` at (max-width:960px)<br>margin (by condition): 0 0 10px where `.toc li` ; 8px 0 ; 0 where `.site-head li`<br>margin-bottom: 0 ! where `.res-entry li:not(:last-child)`<br>margin-top: 4.3px ! where `.res-entry li + li`<br>padding-left (by condition): 30px where `ol>li` ; var(--wt) ! where `.mm-wi>li`<br>position (by condition): static where `.menu > li` ; relative where `ul li` ; static ! where `.site-head li` ; relative where `ol>li` ; relative where `.mm-wi>li`<br>text-align (by width and condition): justify ; left where `.site-head li` ; left where `.toc .mm-toc3 li` ; left ! where `:root body main li` at (max-width:640px) ; left ! where `:root body main ul>li` at (max-width:640px) ; left ! where `:root body main ol>li` at (max-width:640px) |
| `li::before` | Jour 122, Aun 122, Bio 122, SRes 128, Cult 209, Math 260, PL 153, RoA 133, Sens 141 | color: var(--ink) where `ul li::before`<br>content (by condition): "\2010" where `ul li::before` ; none ! where `.site-head li::before` ; none ! where `.toc li::before` ; counter(mmn) "." where `ol>li::before` ; "o" ! where `ul.mm-inner > li::before` ; counter(mmn,lower-roman) "." where `ol.mm-lroman>li::before` ; counter(mmn,lower-alpha) ")" where `ol.mm-mk-alpha-paren>li::before` ; counter(mmn,upper-roman) "." where `ol.mm-uroman>li::before` ; counter(mmn,lower-alpha) "." where `ol.mm-lalpha>li::before` ; counter(mmn,upper-alpha) "." where `ol.mm-ualpha>li::before`<br>left (by condition): **competing** where `ul li::before`: -30px ! wins over -20px, -24px ! ; 0 where `ol>li::before` ; var(--wm) ! where `.mm-wi>li::before` ; auto ! where `.mm-wi.mm-wr>li::before` ; -30px ! where `ul>li::before`<br>position (by condition): absolute where `ul li::before` ; absolute where `ol>li::before` ; absolute where `.mm-wi>li::before`<br>right: calc(100% - var(--wm)) ! where `.mm-wi.mm-wr>li::before`<br>text-align: right where `.mm-wi.mm-wr>li::before` |
| `main` | Jour 1, Aun 1, Bio 1, SRes 1, Cult 1, Math 1, PL 1, RoA 1, Sens 1 | font-style: normal ! |
| `ol` | SRes 1, Cult 3, Math 11, PL 3, RoA 2, Sens 1 | column-gap: 48px where `ol[data-cols]`<br>counter-reset: mmn<br>display: grid where `ol[data-cols]`<br>grid-auto-flow: column where `ol[data-cols]`<br>justify-content: start where `ol[data-cols]`<br>list-style: none !<br>margin: 16px 0<br>margin-left (by width): **competing**: 0 ! wins over 48px ! ; 0 ! at (max-width:640px)<br>padding-left (competing): **competing**: 0 ! wins over 24px, 48px ! |
| `p` | Jour 25, Aun 32, Bio 39, SRes 27, Cult 479, Math 362, PL 223, RoA 39, Sens 251 | color (by condition): inherit where `blockquote.pullquote p` ; #000 ; #000 where `.pullquote p` ; #fff ! where `.mc-band p`<br>font-family (competing): **competing** where `blockquote.pullquote p`: var(--serif) ! wins over inherit, var(--display)<br>font-size (by width and condition): **competing** where `blockquote.pullquote p`: 18px ! wins over 17px, 1em ; 18px ! ; 17px ! at (max-width:640px) ; 18px ! where `blockquote p` ; 17px ! where `blockquote p` at (max-width:830px) ; 17px ! where `blockquote.pullquote p` at (max-width:830px) ; 18px ! where `.mc-band p` ; 17px ! where `.mc-band p` at (max-width:830px) ; 18px ! where `p:not(.mm-gl):not(.mm-cap)` at (min-width:641px) ; 18px ! where `blockquote:not(#mmz) p` at (min-width:641px) ; 18px ! where `.mc-band p` at (min-width:641px) ; 17px ! where `p:not(.mm-gl):not(.mm-cap)` at (max-width:640px) ; 17px ! where `blockquote:not(#mmz) p` at (max-width:640px) ; 17px ! where `.mc-band p` at (max-width:640px)<br>font-style (by condition): **competing** where `blockquote.pullquote p`: italic ! wins over  ; italic ! where `blockquote p` ; italic ! where `.mc-band p`<br>font-weight (competing): **competing** where `blockquote.pullquote p`: 400 ! wins over <br>line-height (by width and condition): **competing** where `blockquote.pullquote p`: 40px ! wins over 1.7 ; 40px ! where `blockquote p` ; 38px ! where `blockquote p` at (max-width:830px) ; 38px ! where `blockquote.pullquote p` at (max-width:830px) ; 40px ! where `.mc-band p` ; 38px ! where `.mc-band p` at (max-width:830px)<br>margin (by condition): 0 0 8px where `blockquote.mq p` ; **competing**: 14px 0 wins over 16px 0 ; 0 where `blockquote.pullquote p` ; 8px 0 where `aside.callout p` ; 0 auto ! where `.mc-band p`<br>margin-left: 0 ! where `#books-on-music-in-montessori blockquote.pullquote p`<br>margin-top (by width and condition): 3.5px ! where `.res-book + p` ; 3.5px ! where `.res-book + .res-item-line + p` ; 0 ! where `> h2 + p` ; 0 ! where `> h2 + .mm-fspacer + .mm-float + p` ; -0.8px ! where `> h2 + p` at (max-width:640px) ; **competing** where `.res-entry > h3.material-name + p`: -0.45px ! wins over 3.3px ! ; 0 where `.mm-besidepdf p`<br>max-width (competing): **competing** where `.mc-band p`: none ! wins over 860px<br>padding-left (by condition): 0 ! where `#books-on-music-in-montessori blockquote.pullquote p` ; 0 ! where `:root body main blockquote.pullquote p`<br>text-align (by width and condition): justify where `main.article p:not(.centred):not(.mm-poem-ctr):not(.mm-cap):not(.mc-by)` ; inherit ! where `main.article blockquote p` ; center ! where `.mc-band p` ; left ! where `:root body main.article p:not(.centred):not(.mm-poem-ctr):not(.mm-cap):not(.mc-by):not(blockquote p)` at (max-width:640px) ; left ! where `:root body main blockquote.pullquote.mm-just>p` at (max-width:640px)<br>text-indent (by condition): 48px where `blockquote.mq p` ; **competing** where `blockquote.pullquote p`: 48px ! wins over 0 ! ; 0 ! where `#books-on-music-in-montessori blockquote.pullquote p` ; 0 ! where `.mc-band p` ; 48px ! where `:root body main blockquote.pullquote p`<br>text-wrap (competing): **competing** where `.mc-band p`: wrap ! wins over balance |
| `span` | Jour 114, Aun 84, Bio 84, SRes 117, Cult 354, Math 222, PL 87, RoA 130, Sens 107 | background: var(--rule) where `.mm-dots span` at (max-width:640px)<br>border-radius: 50% where `.mm-dots span` at (max-width:640px)<br>color (by width and condition): var(--ink) where `.grp .hd span` ; var(--ink) where `.grp li.hd span` ; #0432FF where `.panel.cat .grp li.hd span` ; #fff where `.grp li.hd span` at (max-width:960px) ; #8FC6FF where `.panel.cat .grp li.hd span` at (max-width:960px) ; #0432FF ! where `.panel .grp li.hd span` at (min-width:831px)<br>cursor: default where `.grp .hd span`<br>display (by condition): block where `.hero h1 span` ; block where `.grp .hd span`<br>font-family: var(--serif) where `.grp .hd span`<br>font-size (by width and condition): 17px where `.grp .hd span` ; 17px where `.grp .hd span` at (max-width:960px) ; 18px ! where `.grp .hd span` at (min-width:641px) ; 15px ! where `.site-foot-in span` at (min-width:641px) ; 17px ! where `.grp .hd span` at (max-width:640px) ; 15px ! where `.site-foot-in span` at (max-width:640px)<br>font-weight (by width and condition): 400 where `.menu span` ; 400 where `.grp li.hd span` ; 400 ! where `.panel .grp li.hd span` at (min-width:831px)<br>height: 6px where `.mm-dots span` at (max-width:640px)<br>line-height: 1.3 where `.grp .hd span`<br>margin-left: 30px ! where `.pdf-date + span`<br>padding (by width): 8px 0 where `.grp .hd span` ; 7px 0 where `.grp .hd span` at (max-width:960px)<br>text-align: left ! where `:root body main .mm-bda span` at (max-width:640px)<br>width: 6px where `.mm-dots span` at (max-width:640px) |
| `strong` | SRes 4, Cult 1, Math 30, PL 4, Sens 63 | color: var(--ink) where `.sub-label strong`<br>font-family: var(--serif) ! where `blockquote.pullquote strong`<br>font-weight (by condition): 400 where `blockquote.mq strong` ; 700 where `.sub-label strong` ; 400 ! where `blockquote.pullquote strong` ; 700 ! ; 400 ! where `h2 strong` ; 400 ! where `h3 strong` ; 400 ! where `.res-title strong` ; 400 ! where `.res-src strong` ; 400 ! where `a strong` |
| `sup` | Math 2, Sens 37 | font-size (by condition): .68em where `.formula-table sup` ; .68em where `.article sup`<br>line-height (by condition): 0 where `.formula-table sup` ; 0 where `.article sup`<br>vertical-align (by condition): .45em where `.formula-table sup` ; .45em where `.article sup` |
| `svg` | Jour 9, Aun 9, Bio 9, SRes 9, Cult 9, Math 9, PL 9, RoA 9, Sens 9 | transform (by width): rotate(180deg) where `.has-panel.open > .sub-toggle svg` ; rotate(180deg) where `.has-panel.open > .sub-toggle svg` at (max-width:960px) |
| `td` | PL 32, Sens 121 | border-bottom: 1px solid var(--rule) ! where `table.mm-table td`<br>border-top: 1px solid var(--ink) where `.formula-table tr.rule td`<br>font-weight: 600 where `.formula-table tr.total td`<br>padding (by condition): 3px 10px 3px 0 where `.formula-table td` ; 16px 24px 16px 0 ! where `table.mm-table td`<br>padding-right: 0 ! where `table.mm-table td:last-child`<br>padding-top: 6px where `.formula-table tr.rule td`<br>vertical-align: baseline where `.formula-table td`<br>white-space: nowrap where `.formula-table td` |
| `th` | PL 4 | border-bottom: 1px solid var(--rule) ! where `table.mm-table th`<br>padding: 16px 24px 16px 0 ! where `table.mm-table th`<br>padding-right: 0 ! where `table.mm-table th:last-child` |
| `ul` | Jour 36, Aun 36, Bio 36, SRes 37, Cult 44, Math 41, PL 37, RoA 37, Sens 38 | list-style (by condition): none where `.toc ul` ; none<br>margin (by condition): 0 where `.toc ul` ; 16px 0 ; 0 where `.site-head ul`<br>margin-left (by width): **competing**: 24px ! wins over 0 !, 48px ! ; 0 ! at (max-width:640px)<br>padding: 0 where `.toc ul`<br>padding-left (by condition): **competing**: 30px ! wins over 24px, 48px ! ; 0 ! where `.site-head ul` |

**Resources elements used on none of the nine pages (56)**: `.c1` `.callout` `.callout-label` `.colophon` `.hero-sub` `.lb-frame` `.mc-1-1` `.mc-1-2` `.mc-1-3` `.mc-2-1` `.mc-2-2` `.mc-3-1` `.mm-ami` `.mm-besidepdf` `.mm-dots` `.mm-figcap` `.mm-hanglab` `.mm-lab` `.mm-left` `.mm-licont` `.mm-lsp` `.mm-msfloat` `.mm-msfloat::after` `.mm-n` `.mm-numline` `.mm-pairend` `.mm-rowleft` `.mm-t1` `.mm-t2` `.mm-t3` `.mm-tab` `.mm-tab1` `.mm-trio` `.mm-under` `.mm-w` `.mm-wi` `.mq` `.np-top` `.on` `.open` `.over` `.page-h2` `.pdf-date` `.q-ref` `.res-item-line` `.res-label` `.sub` `.title-block` `.toc-num` `#mm-fit10` `#mm-fitR` `#mm-ms` `b` `h4` `html` `i`

## Measured on every element: each page against its live copy of 27 Oct

Every element of each kind was measured (not only the first), on the nine pages and on the nine live copies of 27 Oct, at 390, 831 and 1440 px, one load each after 2.5 seconds. For each element and property, the values and how many elements show each are compared, page against live. The allowed colour rules (black and orange shown as #2B2B2B, links in #0432FF) are taken out. Sizes and positions that follow from the text (width, height, top, left) are left out.

**Limit of this comparison:** elements are matched by class name. Where the page uses a different class from live for the same thing (live `mm-line`, page `mm-gl`), the two are not compared here. Such elements show as "on the page only" or "on live only" in the counts. The line comparison of this afternoon covers that case for lines.

| Page | Element-property-width differences | Element kinds only on the page | Element kinds only on live |
|---|---|---|---|
| Journey | 184 | 24 | 3 |
| Aun Aprendo | 184 | 24 | 6 |
| Biography | 231 | 18 | 0 |
| Sensorial Resources | 212 | 6 | 0 |
| Culture | 299 | 18 | 3 |
| Mathematics | 323 | 48 | 9 |
| Practical Life | 314 | 15 | 3 |
| Role of the Adult | 175 | 18 | 0 |
| Sensorial Curriculum | 415 | 36 | 0 |

### Every difference

| Page | Element | Property | Width | Live (value ×elements) | Page (value ×elements) |
|---|---|---|---|---|---|
| Journey | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Journey | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Journey | `.article` | padding | 390 | 36px 24px 20px ×1 | 0px 24px 56px ×1 |
| Journey | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Journey | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Journey | `.mc-band` | margin-top | 390 | -0.07px ×1 | -22.08px ×1 |
| Journey | `.mm-row` | margin | 390 | 0px ×10 / 26.95px 0px 20px ×8 / 0px 0px 20px ×7 … | 34px 0px 0px ×15 / 12.95px 0px 0px ×14 / 8.2px 0px 0px ×2 … |
| Journey | `.mm-row` | margin-top | 390 | 0px ×19 / 26.95px ×13 / 22.95px ×2 | 34px ×15 / 12.95px ×14 / 8.2px ×2 … |
| Journey | `.site-foot-in` | padding | 390 | 0px 24px 28px ×1 | 14px 24px ×1 |
| Journey | `.site-foot-in` | padding-bottom | 390 | 28px ×1 | 14px ×1 |
| Journey | `.site-foot-in` | padding-top | 390 | 0px ×1 | 14px ×1 |
| Journey | `.sub-label` | color | 390 | rgb(43, 43, 43) ×17 | rgb(4, 50, 255) ×17 |
| Journey | `.sub-label` | margin-bottom | 390 | 13.95px ×6 / 9.95px ×4 / 10.95px ×3 … | 0px ×17 |
| Journey | `.sub-label` | margin-top | 390 | 50px ×15 / 6px ×1 / 38.95px ×1 | 19px ×10 / 18.25px ×4 / 0px ×1 … |
| Journey | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Journey | `a` | font-size | 390 | 17px ×34 / 18px ×8 / 21px ×1 … | 17px ×42 / 21px ×1 / 15px ×1 |
| Journey | `a` | line-height | 390 | 22.1px ×33 / 29.7px ×8 / 28.05px ×1 … | 22.1px ×33 / 28.05px ×9 / 34.65px ×1 … |
| Journey | `div` | break-inside | 390 | auto ×336 | auto ×322 |
| Journey | `div` | color | 390 | rgb(43, 43, 43) ×333 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×303 / rgb(4, 50, 255) ×17 / rgb(107, 107, 107) ×1 … |
| Journey | `div` | font-size | 390 | 17px ×334 / 15px ×2 | 17px ×320 / 15px ×2 |
| Journey | `div` | font-style | 390 | normal ×336 | normal ×322 |
| Journey | `div` | margin | 390 | 0px ×222 / 8px 0px 4px ×34 / 24px 0px 0px ×15 … | 0px ×214 / 8px 0px 4px ×34 / 24px 0px 0px ×15 … |
| Journey | `div` | padding | 390 | 0px ×289 / 0px 0px 10px 14px ×8 / 0px 51.01px ×2 … | 0px ×275 / 0px 0px 10px 14px ×8 / 0px 51px ×2 … |
| Journey | `p` | color | 390 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Journey | `p` | font-family | 390 | "EB Garamond", Georgia, serif ×24 | "EB Garamond", Georgia, serif ×25 |
| Journey | `p` | font-size | 390 | 17px ×24 | 17px ×24 / 19px ×1 |
| Journey | `p` | font-style | 390 | normal ×22 / italic ×2 | normal ×23 / italic ×2 |
| Journey | `p` | font-weight | 390 | 400 ×24 | 400 ×24 / 500 ×1 |
| Journey | `p` | line-height | 390 | 28.05px ×21 / 38px ×3 | 28.05px ×21 / 38px ×3 / 31.35px ×1 |
| Journey | `p` | margin | 390 | 0px 0px 14px ×12 / 14px 0px ×5 / 0px ×4 … | 42px 0px 0px ×7 / 0.95px 0px 0px ×5 / -2.8px 0px 0px ×3 … |
| Journey | `p` | margin-left | 390 | 0px ×24 | 0px ×25 |
| Journey | `p` | margin-top | 390 | 0px ×16 / 14px ×5 / 28px ×3 | 42px ×7 / 0.95px ×5 / 0px ×4 … |
| Journey | `p` | max-width | 390 | none ×21 / 860px ×3 | none ×25 |
| Journey | `p` | padding-left | 390 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-align | 390 | left ×21 / center ×3 | left ×21 / center ×3 / start ×1 |
| Journey | `p` | text-indent | 390 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-wrap | 390 | wrap ×21 / balance ×3 | wrap ×25 |
| Journey | `span` | background | 390 | rgb(230, 230, 228) none repeat scroll 0% ×118 / rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×113 / rgb(43, 43, 43) none repeat scroll 0% 0% ×34 | rgb(230, 230, 228) none repeat scroll 0% ×118 / rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×114 / rgb(43, 43, 43) none repeat scroll 0% 0% ×34 |
| Journey | `span` | border-radius | 390 | 50% ×152 / 0px ×113 | 50% ×152 / 0px ×114 |
| Journey | `span` | color | 390 | rgb(43, 43, 43) ×152 / rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×30 … | rgb(43, 43, 43) ×152 / rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×30 … |
| Journey | `span` | display | 390 | block ×235 / inline ×17 / inline-block ×13 | block ×235 / inline ×31 |
| Journey | `span` | flex | 390 | 0 1 auto ×265 | 0 1 auto ×266 |
| Journey | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×264 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×265 / Vollkorn, Georgia, serif ×1 |
| Journey | `span` | font-size | 390 | 17px ×263 / 28px ×1 / 15px ×1 | 17px ×264 / 28px ×1 / 15px ×1 |
| Journey | `span` | font-weight | 390 | 400 ×264 / 500 ×1 | 400 ×265 / 500 ×1 |
| Journey | `span` | line-height | 390 | 28.05px ×182 / 22.1px ×81 / 33.6px ×1 … | 28.05px ×182 / 22.1px ×81 / 33.6px ×1 … |
| Journey | `span` | margin-left | 390 | 0px ×265 | 0px ×266 |
| Journey | `span` | min-width | 390 | auto ×153 / 0px ×99 / 110px ×13 | auto ×153 / 0px ×113 |
| Journey | `span` | padding | 390 | 0px ×184 / 7px 0px ×81 | 0px ×185 / 7px 0px ×81 |
| Journey | `span` | text-align | 390 | start ×184 / left ×81 | start ×184 / left ×81 / center ×1 |
| Journey | `ul` | list-style | 390 | outside none none ×34 | outside none none ×36 |
| Journey | `ul` | margin | 390 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Journey | `ul` | margin-left | 390 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding | 390 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding-left | 390 | 0px ×34 | 0px ×36 |
| Journey | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Journey | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Journey | `.article` | padding | 831 | 36px 40px 30.67px ×1 | 18.5px 40px 72px ×1 |
| Journey | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Journey | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Journey | `.mc-band` | margin-top | 831 | -11.69px ×1 | -14.72px ×1 |
| Journey | `.mm-row` | gap | 831 | 24px ×34 | 47.82px ×1 / 18.06px ×1 / 33.61px ×1 … |
| Journey | `.mm-row` | justify-content | 831 | space-between ×34 | center ×34 |
| Journey | `.mm-row` | margin | 831 | 0px ×10 / 27.31px 0px 30px ×8 / 0px 0px 30px ×7 … | 48px 0px 0px ×15 / 37.35px 0px 0px ×14 / 32.63px 0px 0px ×2 … |
| Journey | `.mm-row` | margin-top | 831 | 0px ×19 / 27.31px ×14 / 22.31px ×1 | 48px ×15 / 37.35px ×14 / 32.63px ×2 … |
| Journey | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Journey | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Journey | `.ph` | flex | 831 | 0 1 240px ×12 / 0 1 135px ×10 / 0 1 240.64px ×3 … | 0 0 auto ×152 |
| Journey | `.site-foot-in` | padding | 831 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Journey | `.site-foot-in` | padding-bottom | 831 | 28px ×1 | 17.625px ×1 |
| Journey | `.site-foot-in` | padding-top | 831 | 0px ×1 | 17.625px ×1 |
| Journey | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Journey | `.sub-label` | color | 831 | rgb(43, 43, 43) ×17 | rgb(4, 50, 255) ×17 |
| Journey | `.sub-label` | margin-bottom | 831 | 14.31px ×6 / 9.31px ×4 / 10.31px ×3 … | 0px ×17 |
| Journey | `.sub-label` | margin-top | 831 | 50px ×15 / 6px ×1 / 38.31px ×1 | 18.75px ×10 / 18px ×4 / 0px ×1 … |
| Journey | `a` | font-size | 831 | 17px ×33 / 18px ×9 / 21px ×1 … | 18px ×42 / 25px ×1 / 15px ×1 |
| Journey | `a` | line-height | 831 | 22.1px ×33 / 29.7px ×9 / 34.65px ×1 … | 23.4px ×33 / 29.7px ×9 / 41.25px ×1 … |
| Journey | `div` | break-inside | 831 | auto ×302 | auto ×288 |
| Journey | `div` | color | 831 | rgb(43, 43, 43) ×299 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×269 / rgb(4, 50, 255) ×17 / rgb(107, 107, 107) ×1 … |
| Journey | `div` | font-size | 831 | 18px ×300 / 15px ×2 | 18px ×286 / 15px ×2 |
| Journey | `div` | font-style | 831 | normal ×302 | normal ×288 |
| Journey | `div` | margin | 831 | 0px ×221 / 24px 0px 0px ×15 / 0px auto ×8 … | 0px ×213 / 24px 0px 0px ×15 / 48px 0px 0px ×15 … |
| Journey | `div` | padding | 831 | 0px ×289 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×275 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Journey | `p` | color | 831 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Journey | `p` | font-family | 831 | "EB Garamond", Georgia, serif ×24 | "EB Garamond", Georgia, serif ×25 |
| Journey | `p` | font-size | 831 | 18px ×24 | 18px ×24 / 20px ×1 |
| Journey | `p` | font-style | 831 | normal ×22 / italic ×2 | normal ×23 / italic ×2 |
| Journey | `p` | font-weight | 831 | 400 ×24 | 400 ×24 / 500 ×1 |
| Journey | `p` | line-height | 831 | 29.7px ×21 / 40px ×3 | 29.7px ×21 / 40px ×3 / 33px ×1 |
| Journey | `p` | margin | 831 | 0px 0px 14px ×12 / 14px 0px ×5 / 0px ×4 … | 31.75px 0px 0px ×7 / 0.31px 0px 0px ×6 / -4.19px 0px 0px ×4 … |
| Journey | `p` | margin-left | 831 | 0px ×24 | 0px ×25 |
| Journey | `p` | margin-top | 831 | 0px ×16 / 14px ×5 / 42px ×3 | 31.75px ×7 / 0.31px ×6 / 0px ×4 … |
| Journey | `p` | max-width | 831 | none ×21 / 860px ×3 | none ×25 |
| Journey | `p` | padding-left | 831 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-align | 831 | justify ×21 / center ×3 | justify ×21 / center ×3 / start ×1 |
| Journey | `p` | text-indent | 831 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-wrap | 831 | wrap ×21 / balance ×3 | wrap ×25 |
| Journey | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×113 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×114 |
| Journey | `span` | border-radius | 831 | 0px ×113 | 0px ×114 |
| Journey | `span` | color | 831 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×41 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×41 / rgb(255, 255, 255) ×2 … |
| Journey | `span` | display | 831 | block ×83 / inline ×17 / inline-block ×13 | block ×83 / inline ×31 |
| Journey | `span` | flex | 831 | 0 1 auto ×113 | 0 1 auto ×114 |
| Journey | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×112 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×113 / Vollkorn, Georgia, serif ×1 |
| Journey | `span` | font-size | 831 | 17px ×81 / 18px ×30 / 40px ×1 … | 18px ×112 / 40px ×1 / 15px ×1 |
| Journey | `span` | font-weight | 831 | 400 ×112 / 500 ×1 | 400 ×113 / 500 ×1 |
| Journey | `span` | line-height | 831 | 22.1px ×81 / 29.7px ×30 / 48px ×1 … | 23.4px ×81 / 29.7px ×30 / 48px ×1 … |
| Journey | `span` | margin-left | 831 | 0px ×113 | 0px ×114 |
| Journey | `span` | min-width | 831 | 0px ×99 / 150px ×13 / auto ×1 | 0px ×113 / auto ×1 |
| Journey | `span` | padding | 831 | 7px 0px ×81 / 0px ×32 | 7px 0px ×81 / 0px ×33 |
| Journey | `span` | text-align | 831 | left ×81 / start ×32 | left ×81 / start ×32 / center ×1 |
| Journey | `ul` | list-style | 831 | outside none none ×34 | outside none none ×36 |
| Journey | `ul` | margin | 831 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Journey | `ul` | margin-left | 831 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding | 831 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding-left | 831 | 0px ×34 | 0px ×36 |
| Journey | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Journey | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Journey | `.article` | padding | 1440 | 36px 40px 30.67px ×1 | 18.5px 40px 72px ×1 |
| Journey | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Journey | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Journey | `.mc-band` | margin-top | 1440 | -11.69px ×1 | -14.72px ×1 |
| Journey | `.mm-row` | gap | 1440 | 24px ×34 | 115.35px ×1 / 57.72px ×1 / 71.13px ×1 … |
| Journey | `.mm-row` | justify-content | 1440 | space-between ×34 | center ×34 |
| Journey | `.mm-row` | margin | 1440 | 0px ×10 / 27.31px 0px 30px ×8 / 0px 0px 30px ×7 … | 48px 0px 0px ×15 / 37.35px 0px 0px ×13 / 32.63px 0px 0px ×2 … |
| Journey | `.mm-row` | margin-top | 1440 | 0px ×19 / 27.31px ×13 / 22.31px ×2 | 48px ×15 / 37.35px ×13 / 32.63px ×2 … |
| Journey | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Journey | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Journey | `.ph` | flex | 1440 | 0 1 240px ×12 / 0 1 135px ×10 / 0 1 240.64px ×3 … | 0 0 auto ×152 |
| Journey | `.site-foot-in` | padding | 1440 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Journey | `.site-foot-in` | padding-bottom | 1440 | 28px ×1 | 17.625px ×1 |
| Journey | `.site-foot-in` | padding-top | 1440 | 0px ×1 | 17.625px ×1 |
| Journey | `.sub-label` | color | 1440 | rgb(43, 43, 43) ×17 | rgb(4, 50, 255) ×17 |
| Journey | `.sub-label` | margin-bottom | 1440 | 14.31px ×6 / 9.31px ×4 / 10.31px ×3 … | 0px ×17 |
| Journey | `.sub-label` | margin-top | 1440 | 50px ×15 / 6px ×1 / 38.31px ×1 | 18.75px ×10 / 18px ×4 / 0px ×1 … |
| Journey | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Journey | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Journey | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Journey | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Journey | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Journey | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×8 / 1px solid rgba(0, 0, 0, 0) ×7 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×8 … |
| Journey | `a` | border-bottom-color | 1440 | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×8 / rgba(0, 0, 0, 0) ×7 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … |
| Journey | `a` | font-size | 1440 | 17px ×41 / 18px ×1 / 25px ×1 … | 18px ×42 / 25px ×1 / 15px ×1 |
| Journey | `a` | line-height | 1440 | 22.1px ×33 / 28.05px ×8 / 29.7px ×1 … | 23.4px ×33 / 29.7px ×9 / 41.25px ×1 … |
| Journey | `a` | padding | 1440 | 8px 0px ×33 / 6px 0px ×8 / 0px ×3 | 8px 0px ×33 / 6px 0px 7.5px ×8 / 0px ×3 |
| Journey | `a` | text-decoration | 1440 | none ×41 / underline ×3 | none ×40 / underline ×4 |
| Journey | `a` | text-underline-offset | 1440 | auto ×43 / 3px ×1 | auto ×42 / 4px ×1 / 3px ×1 |
| Journey | `div` | break-inside | 1440 | auto ×302 | auto ×288 |
| Journey | `div` | color | 1440 | rgb(43, 43, 43) ×299 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×269 / rgb(4, 50, 255) ×17 / rgb(107, 107, 107) ×1 … |
| Journey | `div` | font-size | 1440 | 18px ×300 / 15px ×2 | 18px ×286 / 15px ×2 |
| Journey | `div` | font-style | 1440 | normal ×302 | normal ×288 |
| Journey | `div` | margin | 1440 | 0px ×234 / 0px auto ×8 / 30px 0px -28px ×8 … | 0px ×226 / 48px 0px 0px ×15 / 37.35px 0px 0px ×13 … |
| Journey | `div` | padding | 1440 | 0px ×289 / 26px 40px 30px ×8 / 0px 40px ×1 … | 0px ×275 / 26px 40px 30px ×8 / 0px 40px ×2 … |
| Journey | `p` | color | 1440 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×21 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Journey | `p` | font-family | 1440 | "EB Garamond", Georgia, serif ×24 | "EB Garamond", Georgia, serif ×25 |
| Journey | `p` | font-size | 1440 | 18px ×24 | 18px ×24 / 20px ×1 |
| Journey | `p` | font-style | 1440 | normal ×22 / italic ×2 | normal ×23 / italic ×2 |
| Journey | `p` | font-weight | 1440 | 400 ×24 | 400 ×24 / 500 ×1 |
| Journey | `p` | line-height | 1440 | 29.7px ×21 / 40px ×3 | 29.7px ×21 / 40px ×3 / 33px ×1 |
| Journey | `p` | margin | 1440 | 0px 0px 14px ×12 / 14px 0px ×5 / 42px 0px 14px ×3 … | 31.75px 0px 0px ×7 / 0.31px 0px 0px ×6 / -4.19px 0px 0px ×4 … |
| Journey | `p` | margin-left | 1440 | 0px ×21 / 250px ×3 | 0px ×25 |
| Journey | `p` | margin-top | 1440 | 0px ×16 / 14px ×5 / 42px ×3 | 31.75px ×7 / 0.31px ×6 / 0px ×4 … |
| Journey | `p` | max-width | 1440 | none ×21 / 860px ×3 | none ×25 |
| Journey | `p` | padding-left | 1440 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-align | 1440 | justify ×21 / center ×3 | justify ×21 / center ×3 / start ×1 |
| Journey | `p` | text-indent | 1440 | 0px ×24 | 0px ×25 |
| Journey | `p` | text-wrap | 1440 | wrap ×21 / balance ×3 | wrap ×25 |
| Journey | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×113 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×114 |
| Journey | `span` | border-radius | 1440 | 0px ×113 | 0px ×114 |
| Journey | `span` | color | 1440 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×41 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×41 / rgb(255, 255, 255) ×2 … |
| Journey | `span` | display | 1440 | block ×83 / inline ×17 / inline-block ×13 | block ×83 / inline ×31 |
| Journey | `span` | flex | 1440 | 0 1 auto ×113 | 0 1 auto ×114 |
| Journey | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×112 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×113 / Vollkorn, Georgia, serif ×1 |
| Journey | `span` | font-size | 1440 | 17px ×81 / 18px ×30 / 40px ×1 … | 18px ×112 / 40px ×1 / 15px ×1 |
| Journey | `span` | font-weight | 1440 | 400 ×112 / 500 ×1 | 400 ×113 / 500 ×1 |
| Journey | `span` | line-height | 1440 | 22.1px ×81 / 29.7px ×30 / 48px ×1 … | 23.4px ×81 / 29.7px ×30 / 48px ×1 … |
| Journey | `span` | margin-left | 1440 | 0px ×113 | 0px ×114 |
| Journey | `span` | min-width | 1440 | 0px ×99 / 150px ×13 / auto ×1 | 0px ×113 / auto ×1 |
| Journey | `span` | padding | 1440 | 8px 0px ×81 / 0px ×32 | 8px 0px ×81 / 0px ×33 |
| Journey | `span` | text-align | 1440 | left ×81 / start ×32 | left ×81 / start ×32 / center ×1 |
| Journey | `ul` | list-style | 1440 | outside none none ×34 | outside none none ×36 |
| Journey | `ul` | margin | 1440 | 0px ×34 | 0px ×36 |
| Journey | `ul` | margin-left | 1440 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding | 1440 | 0px ×34 | 0px ×36 |
| Journey | `ul` | padding-left | 1440 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Aun Aprendo | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Aun Aprendo | `.article` | padding | 390 | 36px 24px 20px ×1 | 0px 24px 56px ×1 |
| Aun Aprendo | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Aun Aprendo | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Aun Aprendo | `.mc-band` | margin-top | 390 | -6.02px ×1 | -34px ×1 |
| Aun Aprendo | `.mm-float` | margin | 390 | 0px 0px 12px ×2 | 12px 0px 0px ×2 |
| Aun Aprendo | `.mm-float` | margin-top | 390 | 0px ×2 | 12px ×2 |
| Aun Aprendo | `.mm-float` | padding-top | 390 | 0px ×2 | 0.97px ×2 |
| Aun Aprendo | `.mm-row` | margin | 390 | 0px 0px 16px ×13 | 14.95px 0px 0px ×5 / 34px 0px 0px ×3 / 10.2px 0px 0px ×2 … |
| Aun Aprendo | `.mm-row` | margin-top | 390 | 0px ×13 | 14.95px ×5 / 34px ×3 / 10.2px ×2 … |
| Aun Aprendo | `.ph` | scroll-snap-align | 390 | center ×56 / start ×2 | center ×58 |
| Aun Aprendo | `.pim` | max-width | 390 | none ×56 / 100% ×2 | none ×58 |
| Aun Aprendo | `.site-foot-in` | padding | 390 | 0px 24px 28px ×1 | 14px 24px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-bottom | 390 | 28px ×1 | 14px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-top | 390 | 0px ×1 | 14px ×1 |
| Aun Aprendo | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Aun Aprendo | `a` | font-size | 390 | 17px ×34 / 18px ×8 / 21px ×1 … | 17px ×42 / 21px ×1 / 15px ×1 |
| Aun Aprendo | `a` | line-height | 390 | 22.1px ×33 / 29.7px ×8 / 28.05px ×1 … | 22.1px ×33 / 28.05px ×9 / 34.65px ×1 … |
| Aun Aprendo | `div` | break-inside | 390 | auto ×169 | auto ×152 |
| Aun Aprendo | `div` | color | 390 | rgb(43, 43, 43) ×166 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×150 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Aun Aprendo | `div` | font-size | 390 | 17px ×167 / 15px ×2 | 17px ×150 / 15px ×2 |
| Aun Aprendo | `div` | font-style | 390 | normal ×169 | normal ×152 |
| Aun Aprendo | `div` | margin | 390 | 0px ×99 / 24px 0px 0px ×15 / 0px 0px 16px ×13 … | 0px ×100 / 24px 0px 0px ×15 / 8px 0px 4px ×13 … |
| Aun Aprendo | `div` | padding | 390 | 0px ×143 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×124 / 0px 0px 10px 14px ×8 / 0.97px 0px 0px ×2 … |
| Aun Aprendo | `p` | color | 390 | rgb(43, 43, 43) ×10 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×19 / rgb(4, 50, 255) ×10 / rgb(255, 255, 255) ×2 … |
| Aun Aprendo | `p` | font-family | 390 | "EB Garamond", Georgia, serif ×13 | "EB Garamond", Georgia, serif ×32 |
| Aun Aprendo | `p` | font-size | 390 | 17px ×13 | 17px ×13 / 2px ×9 / 20px ×9 … |
| Aun Aprendo | `p` | font-style | 390 | normal ×11 / italic ×2 | normal ×30 / italic ×2 |
| Aun Aprendo | `p` | font-weight | 390 | 400 ×13 | 400 ×31 / 500 ×1 |
| Aun Aprendo | `p` | line-height | 390 | 28.05px ×10 / 38px ×3 | 28.05px ×19 / 2px ×9 / 38px ×3 … |
| Aun Aprendo | `p` | margin | 390 | 14px 0px ×8 / 0px ×3 / 0px 0px 14px ×2 | 29px 0px 0px ×9 / 50px 0px 0px ×8 / 11.95px 0px 0px ×5 … |
| Aun Aprendo | `p` | margin-left | 390 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | margin-top | 390 | 14px ×8 / 0px ×5 | 29px ×9 / 50px ×8 / 0px ×5 … |
| Aun Aprendo | `p` | max-width | 390 | none ×10 / 860px ×3 | none ×32 |
| Aun Aprendo | `p` | padding-left | 390 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-align | 390 | left ×10 / center ×3 | left ×28 / center ×3 / start ×1 |
| Aun Aprendo | `p` | text-indent | 390 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-wrap | 390 | wrap ×10 / balance ×3 | wrap ×32 |
| Aun Aprendo | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×92 / rgb(230, 230, 228) none repeat scroll 0% ×43 / rgb(43, 43, 43) none repeat scroll 0% 0% ×13 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 / rgb(230, 230, 228) none repeat scroll 0% ×43 / rgb(43, 43, 43) none repeat scroll 0% 0% ×13 |
| Aun Aprendo | `span` | border-radius | 390 | 0px ×92 / 50% ×56 | 0px ×84 / 50% ×56 |
| Aun Aprendo | `span` | color | 390 | rgb(231, 238, 245) ×70 / rgb(43, 43, 43) ×56 / rgb(4, 50, 255) ×9 … | rgb(231, 238, 245) ×70 / rgb(43, 43, 43) ×56 / rgb(143, 198, 255) ×8 … |
| Aun Aprendo | `span` | display | 390 | block ×139 / inline ×9 | block ×139 / inline ×1 |
| Aun Aprendo | `span` | flex | 390 | 0 1 auto ×148 | 0 1 auto ×140 |
| Aun Aprendo | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×147 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×139 / Vollkorn, Georgia, serif ×1 |
| Aun Aprendo | `span` | font-size | 390 | 17px ×146 / 28px ×1 / 15px ×1 | 17px ×138 / 28px ×1 / 15px ×1 |
| Aun Aprendo | `span` | font-weight | 390 | 400 ×147 / 500 ×1 | 400 ×139 / 500 ×1 |
| Aun Aprendo | `span` | line-height | 390 | 22.1px ×81 / 28.05px ×65 / 33.6px ×1 … | 22.1px ×81 / 28.05px ×56 / 33.6px ×1 … |
| Aun Aprendo | `span` | margin-left | 390 | 0px ×148 | 0px ×140 |
| Aun Aprendo | `span` | min-width | 390 | 0px ×91 / auto ×57 | 0px ×83 / auto ×57 |
| Aun Aprendo | `span` | padding | 390 | 7px 0px ×81 / 0px ×67 | 7px 0px ×81 / 0px ×59 |
| Aun Aprendo | `span` | text-align | 390 | left ×81 / start ×67 | left ×81 / start ×58 / center ×1 |
| Aun Aprendo | `ul` | list-style | 390 | outside none none ×34 | outside none none ×36 |
| Aun Aprendo | `ul` | margin | 390 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Aun Aprendo | `ul` | margin-left | 390 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding | 390 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding-left | 390 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Aun Aprendo | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Aun Aprendo | `.article` | padding | 831 | 36px 40px 30.67px ×1 | 19.5px 40px 72px ×1 |
| Aun Aprendo | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Aun Aprendo | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Aun Aprendo | `.mc-band` | margin-top | 831 | -14.66px ×1 | -12px ×1 |
| Aun Aprendo | `.mm-float` | margin | 831 | 0px 0px 12px 32px ×2 | 4px 0px 12px 32px ×2 |
| Aun Aprendo | `.mm-float` | margin-top | 831 | 0px ×2 | 4px ×2 |
| Aun Aprendo | `.mm-row` | gap | 831 | 24px ×13 | 12.09px ×1 / 30.07px ×1 / 10px ×1 … |
| Aun Aprendo | `.mm-row` | justify-content | 831 | center ×7 / space-between ×6 | center ×13 |
| Aun Aprendo | `.mm-row` | margin | 831 | 0px 0px 24px ×13 | 38.1px 0px 0px ×7 / 48px 0px 0px ×3 / 33.35px 0px 0px ×1 … |
| Aun Aprendo | `.mm-row` | margin-top | 831 | 0px ×13 | 38.1px ×7 / 48px ×3 / 33.35px ×1 … |
| Aun Aprendo | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Aun Aprendo | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Aun Aprendo | `.ph` | flex | 831 | 0 1 240px ×12 / 0 1 135px ×4 / 0 0 auto ×2 … | 0 0 auto ×58 |
| Aun Aprendo | `.site-foot-in` | padding | 831 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-bottom | 831 | 28px ×1 | 17.625px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-top | 831 | 0px ×1 | 17.625px ×1 |
| Aun Aprendo | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Aun Aprendo | `a` | font-size | 831 | 17px ×33 / 18px ×9 / 21px ×1 … | 18px ×42 / 25px ×1 / 15px ×1 |
| Aun Aprendo | `a` | line-height | 831 | 22.1px ×33 / 29.7px ×9 / 34.65px ×1 … | 23.4px ×33 / 29.7px ×9 / 41.25px ×1 … |
| Aun Aprendo | `div` | break-inside | 831 | auto ×156 | auto ×141 |
| Aun Aprendo | `div` | color | 831 | rgb(43, 43, 43) ×153 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×139 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Aun Aprendo | `div` | font-size | 831 | 18px ×154 / 15px ×2 | 18px ×139 / 15px ×2 |
| Aun Aprendo | `div` | font-style | 831 | normal ×156 | normal ×141 |
| Aun Aprendo | `div` | margin | 831 | 0px ×98 / 24px 0px 0px ×15 / 0px 0px 24px ×13 … | 0px ×101 / 24px 0px 0px ×15 / 0px auto ×8 … |
| Aun Aprendo | `div` | padding | 831 | 0px ×143 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×128 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Aun Aprendo | `p` | color | 831 | rgb(43, 43, 43) ×10 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×19 / rgb(4, 50, 255) ×10 / rgb(255, 255, 255) ×2 … |
| Aun Aprendo | `p` | font-family | 831 | "EB Garamond", Georgia, serif ×13 | "EB Garamond", Georgia, serif ×32 |
| Aun Aprendo | `p` | font-size | 831 | 18px ×13 | 18px ×13 / 20px ×10 / 2px ×9 |
| Aun Aprendo | `p` | font-style | 831 | normal ×11 / italic ×2 | normal ×30 / italic ×2 |
| Aun Aprendo | `p` | font-weight | 831 | 400 ×13 | 400 ×31 / 500 ×1 |
| Aun Aprendo | `p` | line-height | 831 | 29.7px ×10 / 40px ×3 | 29.7px ×19 / 2px ×9 / 40px ×3 … |
| Aun Aprendo | `p` | margin | 831 | 14px 0px ×8 / 0px ×3 / 0px 0px 14px ×2 | 23px 0px 0px ×9 / 64px 0px 0px ×8 / 11.3px 0px 0px ×7 … |
| Aun Aprendo | `p` | margin-left | 831 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | margin-top | 831 | 14px ×8 / 0px ×5 | 23px ×9 / 64px ×8 / 11.3px ×7 … |
| Aun Aprendo | `p` | max-width | 831 | none ×10 / 860px ×3 | none ×32 |
| Aun Aprendo | `p` | padding-left | 831 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-align | 831 | justify ×10 / center ×3 | justify ×19 / start ×10 / center ×3 |
| Aun Aprendo | `p` | text-indent | 831 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-wrap | 831 | wrap ×10 / balance ×3 | wrap ×32 |
| Aun Aprendo | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×92 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 |
| Aun Aprendo | `span` | border-radius | 831 | 0px ×92 | 0px ×84 |
| Aun Aprendo | `span` | color | 831 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×20 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Aun Aprendo | `span` | display | 831 | block ×83 / inline ×9 | block ×83 / inline ×1 |
| Aun Aprendo | `span` | flex | 831 | 0 1 auto ×92 | 0 1 auto ×84 |
| Aun Aprendo | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×91 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×83 / Vollkorn, Georgia, serif ×1 |
| Aun Aprendo | `span` | font-size | 831 | 17px ×81 / 18px ×9 / 40px ×1 … | 18px ×82 / 40px ×1 / 15px ×1 |
| Aun Aprendo | `span` | font-weight | 831 | 400 ×91 / 500 ×1 | 400 ×83 / 500 ×1 |
| Aun Aprendo | `span` | line-height | 831 | 22.1px ×81 / 29.7px ×9 / 48px ×1 … | 23.4px ×81 / 48px ×1 / 40px ×1 … |
| Aun Aprendo | `span` | margin-left | 831 | 0px ×92 | 0px ×84 |
| Aun Aprendo | `span` | min-width | 831 | 0px ×91 / auto ×1 | 0px ×83 / auto ×1 |
| Aun Aprendo | `span` | padding | 831 | 7px 0px ×81 / 0px ×11 | 7px 0px ×81 / 0px ×3 |
| Aun Aprendo | `span` | text-align | 831 | left ×81 / start ×11 | left ×81 / start ×2 / center ×1 |
| Aun Aprendo | `ul` | list-style | 831 | outside none none ×34 | outside none none ×36 |
| Aun Aprendo | `ul` | margin | 831 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Aun Aprendo | `ul` | margin-left | 831 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding | 831 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding-left | 831 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Aun Aprendo | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Aun Aprendo | `.article` | padding | 1440 | 36px 40px 30.67px ×1 | 19.5px 40px 72px ×1 |
| Aun Aprendo | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Aun Aprendo | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Aun Aprendo | `.mc-band` | margin-top | 1440 | -14.66px ×1 | -12px ×1 |
| Aun Aprendo | `.mm-float` | margin | 1440 | 0px 0px 12px 32px ×2 | 4px 0px 12px 32px ×2 |
| Aun Aprendo | `.mm-float` | margin-top | 1440 | 0px ×2 | 4px ×2 |
| Aun Aprendo | `.mm-row` | gap | 1440 | 24px ×13 | 38.4px ×1 / 70.39px ×1 / 42.79px ×1 … |
| Aun Aprendo | `.mm-row` | justify-content | 1440 | center ×7 / space-between ×6 | center ×13 |
| Aun Aprendo | `.mm-row` | margin | 1440 | 0px 0px 24px ×13 | 38.1px 0px 0px ×7 / 48px 0px 0px ×3 / 33.35px 0px 0px ×1 … |
| Aun Aprendo | `.mm-row` | margin-top | 1440 | 0px ×13 | 38.1px ×7 / 48px ×3 / 33.35px ×1 … |
| Aun Aprendo | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Aun Aprendo | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Aun Aprendo | `.ph` | flex | 1440 | 0 1 240px ×12 / 0 1 135px ×4 / 0 0 auto ×2 … | 0 0 auto ×58 |
| Aun Aprendo | `.site-foot-in` | padding | 1440 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-bottom | 1440 | 28px ×1 | 17.625px ×1 |
| Aun Aprendo | `.site-foot-in` | padding-top | 1440 | 0px ×1 | 17.625px ×1 |
| Aun Aprendo | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Aun Aprendo | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Aun Aprendo | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Aun Aprendo | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Aun Aprendo | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Aun Aprendo | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×8 / 1px solid rgba(0, 0, 0, 0) ×7 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×8 … |
| Aun Aprendo | `a` | border-bottom-color | 1440 | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×8 / rgba(0, 0, 0, 0) ×7 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … |
| Aun Aprendo | `a` | font-size | 1440 | 17px ×41 / 18px ×1 / 25px ×1 … | 18px ×42 / 25px ×1 / 15px ×1 |
| Aun Aprendo | `a` | line-height | 1440 | 22.1px ×33 / 28.05px ×8 / 29.7px ×1 … | 23.4px ×33 / 29.7px ×9 / 41.25px ×1 … |
| Aun Aprendo | `a` | padding | 1440 | 8px 0px ×33 / 6px 0px ×8 / 0px ×3 | 8px 0px ×33 / 6px 0px 7.5px ×8 / 0px ×3 |
| Aun Aprendo | `a` | text-decoration | 1440 | none ×41 / underline ×3 | none ×40 / underline ×4 |
| Aun Aprendo | `a` | text-underline-offset | 1440 | auto ×43 / 3px ×1 | auto ×42 / 4px ×1 / 3px ×1 |
| Aun Aprendo | `div` | break-inside | 1440 | auto ×156 | auto ×141 |
| Aun Aprendo | `div` | color | 1440 | rgb(43, 43, 43) ×153 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×139 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Aun Aprendo | `div` | font-size | 1440 | 18px ×154 / 15px ×2 | 18px ×139 / 15px ×2 |
| Aun Aprendo | `div` | font-style | 1440 | normal ×156 | normal ×141 |
| Aun Aprendo | `div` | margin | 1440 | 0px ×111 / 0px 0px 24px ×13 / 0px auto ×8 … | 0px ×114 / 0px auto ×8 / 38.1px 0px 0px ×7 … |
| Aun Aprendo | `div` | padding | 1440 | 0px ×143 / 26px 40px 30px ×8 / 0px 40px ×1 … | 0px ×128 / 26px 40px 30px ×8 / 0px 40px ×2 … |
| Aun Aprendo | `p` | color | 1440 | rgb(43, 43, 43) ×10 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×19 / rgb(4, 50, 255) ×10 / rgb(255, 255, 255) ×2 … |
| Aun Aprendo | `p` | font-family | 1440 | "EB Garamond", Georgia, serif ×13 | "EB Garamond", Georgia, serif ×32 |
| Aun Aprendo | `p` | font-size | 1440 | 18px ×13 | 18px ×13 / 20px ×10 / 2px ×9 |
| Aun Aprendo | `p` | font-style | 1440 | normal ×11 / italic ×2 | normal ×30 / italic ×2 |
| Aun Aprendo | `p` | font-weight | 1440 | 400 ×13 | 400 ×31 / 500 ×1 |
| Aun Aprendo | `p` | line-height | 1440 | 29.7px ×10 / 40px ×3 | 29.7px ×19 / 2px ×9 / 40px ×3 … |
| Aun Aprendo | `p` | margin | 1440 | 14px 0px ×8 / 0px 250px ×3 / 0px 0px 14px ×2 | 23px 0px 0px ×9 / 64px 0px 0px ×8 / 11.3px 0px 0px ×7 … |
| Aun Aprendo | `p` | margin-left | 1440 | 0px ×10 / 250px ×3 | 0px ×32 |
| Aun Aprendo | `p` | margin-top | 1440 | 14px ×8 / 0px ×5 | 23px ×9 / 64px ×8 / 11.3px ×7 … |
| Aun Aprendo | `p` | max-width | 1440 | none ×10 / 860px ×3 | none ×32 |
| Aun Aprendo | `p` | padding-left | 1440 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-align | 1440 | justify ×10 / center ×3 | justify ×19 / start ×10 / center ×3 |
| Aun Aprendo | `p` | text-indent | 1440 | 0px ×13 | 0px ×32 |
| Aun Aprendo | `p` | text-wrap | 1440 | wrap ×10 / balance ×3 | wrap ×32 |
| Aun Aprendo | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×92 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 |
| Aun Aprendo | `span` | border-radius | 1440 | 0px ×92 | 0px ×84 |
| Aun Aprendo | `span` | color | 1440 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×20 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Aun Aprendo | `span` | display | 1440 | block ×83 / inline ×9 | block ×83 / inline ×1 |
| Aun Aprendo | `span` | flex | 1440 | 0 1 auto ×92 | 0 1 auto ×84 |
| Aun Aprendo | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×91 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×83 / Vollkorn, Georgia, serif ×1 |
| Aun Aprendo | `span` | font-size | 1440 | 17px ×81 / 18px ×9 / 40px ×1 … | 18px ×82 / 40px ×1 / 15px ×1 |
| Aun Aprendo | `span` | font-weight | 1440 | 400 ×91 / 500 ×1 | 400 ×83 / 500 ×1 |
| Aun Aprendo | `span` | line-height | 1440 | 22.1px ×81 / 29.7px ×9 / 48px ×1 … | 23.4px ×81 / 48px ×1 / 40px ×1 … |
| Aun Aprendo | `span` | margin-left | 1440 | 0px ×92 | 0px ×84 |
| Aun Aprendo | `span` | min-width | 1440 | 0px ×91 / auto ×1 | 0px ×83 / auto ×1 |
| Aun Aprendo | `span` | padding | 1440 | 8px 0px ×81 / 0px ×11 | 8px 0px ×81 / 0px ×3 |
| Aun Aprendo | `span` | text-align | 1440 | left ×81 / start ×11 | left ×81 / start ×2 / center ×1 |
| Aun Aprendo | `ul` | list-style | 1440 | outside none none ×34 | outside none none ×36 |
| Aun Aprendo | `ul` | margin | 1440 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | margin-left | 1440 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding | 1440 | 0px ×34 | 0px ×36 |
| Aun Aprendo | `ul` | padding-left | 1440 | 0px ×34 | 0px ×36 |
| Biography | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Biography | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Biography | `.article` | padding | 390 | 36px 24px 20px ×1 | 0px 24px 56px ×1 |
| Biography | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Biography | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Biography | `.mc-band` | margin-top | 390 | -0.07px ×1 | -22.08px ×1 |
| Biography | `.mm-cap` | font-size | 390 | 15px ×9 | 16px ×9 |
| Biography | `.mm-cap` | font-style | 390 | normal ×9 | italic ×9 |
| Biography | `.mm-cap` | line-height | 390 | 19.5px ×9 | 20.8px ×9 |
| Biography | `.mm-cap` | margin | 390 | 6px 0px 0px ×9 | 0px 0px 6px ×9 |
| Biography | `.mm-cap` | padding-top | 390 | 0px ×9 | 2px ×9 |
| Biography | `.mm-float` | margin | 390 | 0px 0px 12px ×7 | 12px 0px 0px ×7 |
| Biography | `.mm-float` | margin-top | 390 | 0px ×7 | 12px ×7 |
| Biography | `.mm-float` | padding-top | 390 | 0px ×7 | 0px ×4 / 0.97px ×3 |
| Biography | `.mm-row` | margin | 390 | 26.95px 0px -5.5px ×1 / 26.95px 0px 14px ×1 / 22.95px 0px -6px ×1 … | 12.95px 0px 0px ×3 / 8.2px 0px 0px ×1 |
| Biography | `.mm-row` | margin-top | 390 | 26.95px ×3 / 22.95px ×1 | 12.95px ×3 / 8.2px ×1 |
| Biography | `.ph` | margin | 390 | 0px ×20 / 0px 0px 0px 10px ×1 | 0px ×21 |
| Biography | `.ph` | scroll-snap-align | 390 | center ×14 / start ×7 | center ×21 |
| Biography | `.pim` | flex | 390 | 0 1 auto ×20 / 0 0 46.0234% ×1 / 0 0 45.501% ×1 | 0 1 auto ×20 / 0 0 auto ×2 |
| Biography | `.pim` | margin | 390 | 0px ×22 | 0px ×21 / 0px 0px 0px 25.4118px ×1 |
| Biography | `.pim` | margin-left | 390 | 0px ×22 | 0px ×21 / 25.4118px ×1 |
| Biography | `.pim` | max-width | 390 | none ×15 / 100% ×7 | none ×22 |
| Biography | `.site-foot-in` | padding | 390 | 0px 24px 28px ×1 | 14px 24px ×1 |
| Biography | `.site-foot-in` | padding-bottom | 390 | 28px ×1 | 14px ×1 |
| Biography | `.site-foot-in` | padding-top | 390 | 0px ×1 | 14px ×1 |
| Biography | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Biography | `a` | border-bottom | 390 | 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(143, 198, 255) ×8 … | 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(143, 198, 255) ×8 … |
| Biography | `a` | border-bottom-color | 390 | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … |
| Biography | `a` | color | 390 | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … |
| Biography | `a` | font-size | 390 | 17px ×38 / 18px ×8 / 21px ×1 … | 17px ×46 / 21px ×1 / 15px ×1 |
| Biography | `a` | line-height | 390 | 22.1px ×33 / 29.7px ×8 / 28.05px ×5 … | 22.1px ×33 / 28.05px ×13 / 34.65px ×1 … |
| Biography | `a` | outline | 390 | rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(143, 198, 255) none 3px ×8 … | rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(143, 198, 255) none 3px ×8 … |
| Biography | `div` | break-inside | 390 | auto ×103 | auto ×104 |
| Biography | `div` | color | 390 | rgb(43, 43, 43) ×100 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×102 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Biography | `div` | font-size | 390 | 17px ×100 / 15px ×3 | 17px ×102 / 15px ×2 |
| Biography | `div` | font-style | 390 | normal ×103 | normal ×104 |
| Biography | `div` | margin | 390 | 0px ×60 / 24px 0px 0px ×15 / 0px auto ×8 … | 0px ×64 / 24px 0px 0px ×15 / 0px auto ×8 … |
| Biography | `div` | padding | 390 | 0px ×86 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×84 / 0px 0px 10px 14px ×8 / 0.97px 0px 0px ×3 … |
| Biography | `figcaption` | font-size | 390 | 15px ×9 | 16px ×9 |
| Biography | `figcaption` | line-height | 390 | 19.5px ×9 | 20.8px ×9 |
| Biography | `figcaption` | margin-top | 390 | 6px ×9 | 0px ×9 |
| Biography | `figure` | margin-left | 390 | 0px ×20 / 10px ×1 | 0px ×21 |
| Biography | `p` | color | 390 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Biography | `p` | font-family | 390 | "EB Garamond", Georgia, serif ×38 | "EB Garamond", Georgia, serif ×39 |
| Biography | `p` | font-size | 390 | 17px ×38 | 17px ×38 / 19px ×1 |
| Biography | `p` | font-style | 390 | normal ×36 / italic ×2 | normal ×37 / italic ×2 |
| Biography | `p` | font-weight | 390 | 400 ×38 | 400 ×38 / 500 ×1 |
| Biography | `p` | line-height | 390 | 28.05px ×35 / 38px ×3 | 28.05px ×35 / 38px ×3 / 31.35px ×1 |
| Biography | `p` | margin | 390 | 14px 0px ×28 / 0px 0px 14px ×7 / 0px ×3 | 11.95px 0px 0px ×15 / 7.45px 0px 0px ×8 / 8px 0px 0px ×7 … |
| Biography | `p` | margin-left | 390 | 0px ×38 | 0px ×39 |
| Biography | `p` | margin-top | 390 | 14px ×28 / 0px ×10 | 11.95px ×15 / 7.45px ×8 / 8px ×7 … |
| Biography | `p` | max-width | 390 | none ×35 / 860px ×3 | none ×39 |
| Biography | `p` | padding-left | 390 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-align | 390 | left ×35 / center ×3 | left ×35 / center ×3 / start ×1 |
| Biography | `p` | text-indent | 390 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-wrap | 390 | wrap ×35 / balance ×3 | wrap ×39 |
| Biography | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×83 / rgb(230, 230, 228) none repeat scroll 0% ×10 / rgb(43, 43, 43) none repeat scroll 0% 0% ×4 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 / rgb(230, 230, 228) none repeat scroll 0% ×10 / rgb(43, 43, 43) none repeat scroll 0% 0% ×4 |
| Biography | `span` | border-radius | 390 | 0px ×83 / 50% ×14 | 0px ×84 / 50% ×14 |
| Biography | `span` | color | 390 | rgb(231, 238, 245) ×70 / rgb(43, 43, 43) ×14 / rgb(143, 198, 255) ×8 … | rgb(231, 238, 245) ×70 / rgb(43, 43, 43) ×14 / rgb(143, 198, 255) ×8 … |
| Biography | `span` | display | 390 | block ×97 | block ×97 / inline ×1 |
| Biography | `span` | flex | 390 | 0 1 auto ×97 | 0 1 auto ×98 |
| Biography | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×96 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×97 / Vollkorn, Georgia, serif ×1 |
| Biography | `span` | font-size | 390 | 17px ×95 / 28px ×1 / 15px ×1 | 17px ×96 / 28px ×1 / 15px ×1 |
| Biography | `span` | font-weight | 390 | 400 ×96 / 500 ×1 | 400 ×97 / 500 ×1 |
| Biography | `span` | line-height | 390 | 22.1px ×81 / 28.05px ×14 / 33.6px ×1 … | 22.1px ×81 / 28.05px ×14 / 33.6px ×1 … |
| Biography | `span` | margin-left | 390 | 0px ×97 | 0px ×98 |
| Biography | `span` | min-width | 390 | 0px ×82 / auto ×15 | 0px ×83 / auto ×15 |
| Biography | `span` | padding | 390 | 7px 0px ×81 / 0px ×16 | 7px 0px ×81 / 0px ×17 |
| Biography | `span` | text-align | 390 | left ×81 / start ×16 | left ×81 / start ×16 / center ×1 |
| Biography | `ul` | list-style | 390 | outside none none ×34 | outside none none ×36 |
| Biography | `ul` | margin | 390 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Biography | `ul` | margin-left | 390 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding | 390 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding-left | 390 | 0px ×34 | 0px ×36 |
| Biography | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Biography | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Biography | `.article` | padding | 831 | 36px 40px 30.67px ×1 | 19.5px 40px 72px ×1 |
| Biography | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Biography | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Biography | `.mc-band` | margin-top | 831 | -11.69px ×1 | -19.72px ×1 |
| Biography | `.mm-cap` | font-size | 831 | 15px ×9 | 16px ×9 |
| Biography | `.mm-cap` | font-style | 831 | normal ×9 | italic ×9 |
| Biography | `.mm-cap` | line-height | 831 | 19.5px ×9 | 20.8px ×9 |
| Biography | `.mm-cap` | margin | 831 | 6px 0px 0px ×9 | 0px 0px 6px ×9 |
| Biography | `.mm-cap` | padding-top | 831 | 0px ×9 | 2px ×9 |
| Biography | `.mm-float` | margin | 831 | 0px 0px 12px 32px ×6 / 39.26px 0px 12px 32px ×1 | 4px 0px 12px 32px ×6 / -30.8px 0px 12px 32px ×1 |
| Biography | `.mm-float` | margin-top | 831 | 0px ×6 / 39.26px ×1 | 4px ×6 / -30.8px ×1 |
| Biography | `.mm-row` | gap | 831 | 24px ×4 | 164.8px ×1 / 33.87px ×1 / 308.3px ×1 … |
| Biography | `.mm-row` | margin | 831 | 27.31px 0px 22.5px ×1 / 22.31px 0px 24px ×1 / 27.31px 0px 22px ×1 … | 37.35px 0px 0px ×2 / 32.85px 0px 0px ×2 |
| Biography | `.mm-row` | margin-top | 831 | 27.31px ×2 / 22.31px ×2 | 37.35px ×2 / 32.85px ×2 |
| Biography | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Biography | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Biography | `.ph` | flex | 831 | 0 0 auto ×7 / 0 1 136.89px ×1 / 0 1 120.33px ×1 … | 0 0 auto ×21 |
| Biography | `.ph` | margin | 831 | 0px ×20 / 0px 0px 0px 24px ×1 | 0px ×21 |
| Biography | `.pim` | flex | 831 | 0 1 auto ×20 / 0 0 46.0234% ×1 / 0 0 45.501% ×1 | 0 1 auto ×20 / 0 0 auto ×2 |
| Biography | `.pim` | margin | 831 | 0px ×22 | 0px ×21 / 0px 0px 0px 19.7647px ×1 |
| Biography | `.pim` | margin-left | 831 | 0px ×22 | 0px ×21 / 19.7647px ×1 |
| Biography | `.site-foot-in` | padding | 831 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Biography | `.site-foot-in` | padding-bottom | 831 | 28px ×1 | 17.625px ×1 |
| Biography | `.site-foot-in` | padding-top | 831 | 0px ×1 | 17.625px ×1 |
| Biography | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Biography | `a` | border-bottom | 831 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×8 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×12 / 0px none rgb(255, 255, 255) ×9 … |
| Biography | `a` | border-bottom-color | 831 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×12 / rgb(255, 255, 255) ×9 … |
| Biography | `a` | color | 831 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×12 / rgb(255, 255, 255) ×9 … |
| Biography | `a` | font-size | 831 | 17px ×33 / 18px ×13 / 21px ×1 … | 18px ×46 / 25px ×1 / 15px ×1 |
| Biography | `a` | line-height | 831 | 22.1px ×33 / 29.7px ×13 / 34.65px ×1 … | 23.4px ×33 / 29.7px ×13 / 41.25px ×1 … |
| Biography | `a` | outline | 831 | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×8 … | rgb(43, 43, 43) none 3px ×25 / rgb(4, 50, 255) none 3px ×12 / rgb(255, 255, 255) none 3px ×9 … |
| Biography | `div` | break-inside | 831 | auto ×99 | auto ×107 |
| Biography | `div` | color | 831 | rgb(43, 43, 43) ×96 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×105 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Biography | `div` | font-size | 831 | 18px ×96 / 15px ×3 | 18px ×105 / 15px ×2 |
| Biography | `div` | font-style | 831 | normal ×99 | normal ×107 |
| Biography | `div` | margin | 831 | 0px ×59 / 24px 0px 0px ×15 / 0px auto ×8 … | 0px ×69 / 24px 0px 0px ×15 / 0px auto ×8 … |
| Biography | `div` | padding | 831 | 0px ×86 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×94 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Biography | `figcaption` | font-size | 831 | 15px ×9 | 16px ×9 |
| Biography | `figcaption` | line-height | 831 | 19.5px ×9 | 20.8px ×9 |
| Biography | `figcaption` | margin-top | 831 | 6px ×9 | 0px ×9 |
| Biography | `figure` | margin-left | 831 | 0px ×20 / 24px ×1 | 0px ×21 |
| Biography | `p` | color | 831 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Biography | `p` | font-family | 831 | "EB Garamond", Georgia, serif ×38 | "EB Garamond", Georgia, serif ×39 |
| Biography | `p` | font-size | 831 | 18px ×38 | 18px ×38 / 20px ×1 |
| Biography | `p` | font-style | 831 | normal ×36 / italic ×2 | normal ×37 / italic ×2 |
| Biography | `p` | font-weight | 831 | 400 ×38 | 400 ×38 / 500 ×1 |
| Biography | `p` | line-height | 831 | 29.7px ×35 / 40px ×3 | 29.7px ×35 / 40px ×3 / 33px ×1 |
| Biography | `p` | margin | 831 | 14px 0px ×28 / 0px 0px 14px ×7 / 0px ×3 | 11.3px 0px 0px ×25 / 6.55px 0px 0px ×5 / 0px ×4 … |
| Biography | `p` | margin-left | 831 | 0px ×38 | 0px ×39 |
| Biography | `p` | margin-top | 831 | 14px ×28 / 0px ×10 | 11.3px ×25 / 0px ×5 / 6.55px ×5 … |
| Biography | `p` | max-width | 831 | none ×35 / 860px ×3 | none ×39 |
| Biography | `p` | padding-left | 831 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-align | 831 | justify ×35 / center ×3 | justify ×35 / center ×3 / start ×1 |
| Biography | `p` | text-indent | 831 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-wrap | 831 | wrap ×35 / balance ×3 | wrap ×39 |
| Biography | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×83 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 |
| Biography | `span` | border-radius | 831 | 0px ×83 | 0px ×84 |
| Biography | `span` | color | 831 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Biography | `span` | display | 831 | block ×83 | block ×83 / inline ×1 |
| Biography | `span` | flex | 831 | 0 1 auto ×83 | 0 1 auto ×84 |
| Biography | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×82 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×83 / Vollkorn, Georgia, serif ×1 |
| Biography | `span` | font-size | 831 | 17px ×81 / 40px ×1 / 15px ×1 | 18px ×82 / 40px ×1 / 15px ×1 |
| Biography | `span` | font-weight | 831 | 400 ×82 / 500 ×1 | 400 ×83 / 500 ×1 |
| Biography | `span` | line-height | 831 | 22.1px ×81 / 48px ×1 / 24.75px ×1 | 23.4px ×81 / 48px ×1 / 40px ×1 … |
| Biography | `span` | margin-left | 831 | 0px ×83 | 0px ×84 |
| Biography | `span` | min-width | 831 | 0px ×82 / auto ×1 | 0px ×83 / auto ×1 |
| Biography | `span` | padding | 831 | 7px 0px ×81 / 0px ×2 | 7px 0px ×81 / 0px ×3 |
| Biography | `span` | text-align | 831 | left ×81 / start ×2 | left ×81 / start ×2 / center ×1 |
| Biography | `ul` | list-style | 831 | outside none none ×34 | outside none none ×36 |
| Biography | `ul` | margin | 831 | 0px ×26 / 24px 0px 0px ×8 | 0px ×28 / 24px 0px 0px ×8 |
| Biography | `ul` | margin-left | 831 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding | 831 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding-left | 831 | 0px ×34 | 0px ×36 |
| Biography | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Biography | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Biography | `.article` | padding | 1440 | 36px 40px 30.67px ×1 | 19.5px 40px 72px ×1 |
| Biography | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Biography | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Biography | `.mc-band` | margin-top | 1440 | -11.69px ×1 | -14.72px ×1 |
| Biography | `.mm-cap` | font-size | 1440 | 15px ×9 | 16px ×9 |
| Biography | `.mm-cap` | font-style | 1440 | normal ×9 | italic ×9 |
| Biography | `.mm-cap` | line-height | 1440 | 19.5px ×9 | 20.8px ×9 |
| Biography | `.mm-cap` | margin | 1440 | 6px 0px 0px ×9 | 0px 0px 6px ×9 |
| Biography | `.mm-cap` | padding-top | 1440 | 0px ×9 | 2px ×9 |
| Biography | `.mm-float` | margin | 1440 | 0px 0px 12px 32px ×6 / -20.51px 0px 12px 32px ×1 | 4px 0px 12px 32px ×6 / -45.65px 0px 12px 32px ×1 |
| Biography | `.mm-float` | margin-top | 1440 | 0px ×6 / -20.51px ×1 | 4px ×6 / -45.65px ×1 |
| Biography | `.mm-row` | gap | 1440 | 24px ×4 | 231.64px ×1 / 62.15px ×1 / 437.41px ×1 … |
| Biography | `.mm-row` | margin | 1440 | 27.31px 0px 22.5px ×1 / 27.31px 0px 24px ×1 / 22.31px 0px 22px ×1 … | 37.35px 0px 0px ×3 / 32.35px 0px 0px ×1 |
| Biography | `.mm-row` | margin-top | 1440 | 27.31px ×3 / 22.31px ×1 | 37.35px ×3 / 32.35px ×1 |
| Biography | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Biography | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Biography | `.ph` | flex | 1440 | 0 0 auto ×7 / 0 1 136.89px ×1 / 0 1 120.33px ×1 … | 0 0 auto ×21 |
| Biography | `.ph` | margin | 1440 | 0px ×20 / 0px 0px 0px 24px ×1 | 0px ×21 |
| Biography | `.pim` | flex | 1440 | 0 1 auto ×20 / 0 0 46.0234% ×1 / 0 0 45.501% ×1 | 0 1 auto ×20 / 0 0 auto ×2 |
| Biography | `.pim` | margin | 1440 | 0px ×22 | 0px ×21 / 0px 0px 0px 24px ×1 |
| Biography | `.pim` | margin-left | 1440 | 0px ×22 | 0px ×21 / 24px ×1 |
| Biography | `.site-foot-in` | padding | 1440 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Biography | `.site-foot-in` | padding-bottom | 1440 | 28px ×1 | 17.625px ×1 |
| Biography | `.site-foot-in` | padding-top | 1440 | 0px ×1 | 17.625px ×1 |
| Biography | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Biography | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Biography | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Biography | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Biography | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Biography | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×8 / 1px solid rgba(0, 0, 0, 0) ×7 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×12 / 0px none rgb(255, 255, 255) ×9 … |
| Biography | `a` | border-bottom-color | 1440 | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×8 / rgba(0, 0, 0, 0) ×7 … | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×12 / rgb(255, 255, 255) ×9 … |
| Biography | `a` | color | 1440 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … | rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×12 / rgb(255, 255, 255) ×9 … |
| Biography | `a` | font-size | 1440 | 17px ×41 / 18px ×5 / 25px ×1 … | 18px ×46 / 25px ×1 / 15px ×1 |
| Biography | `a` | line-height | 1440 | 22.1px ×33 / 28.05px ×8 / 29.7px ×5 … | 23.4px ×33 / 29.7px ×13 / 41.25px ×1 … |
| Biography | `a` | outline | 1440 | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×8 … | rgb(43, 43, 43) none 3px ×25 / rgb(4, 50, 255) none 3px ×12 / rgb(255, 255, 255) none 3px ×9 … |
| Biography | `a` | padding | 1440 | 8px 0px ×33 / 6px 0px ×8 / 0px ×7 | 8px 0px ×33 / 6px 0px 7.5px ×8 / 0px ×7 |
| Biography | `a` | text-decoration | 1440 | none ×41 / underline ×7 | none ×40 / underline ×8 |
| Biography | `a` | text-underline-offset | 1440 | auto ×47 / 3px ×1 | auto ×46 / 4px ×1 / 3px ×1 |
| Biography | `div` | break-inside | 1440 | auto ×99 | auto ×107 |
| Biography | `div` | color | 1440 | rgb(43, 43, 43) ×96 / rgb(255, 255, 255) ×1 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×105 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Biography | `div` | font-size | 1440 | 18px ×96 / 15px ×3 | 18px ×105 / 15px ×2 |
| Biography | `div` | font-style | 1440 | normal ×99 | normal ×107 |
| Biography | `div` | margin | 1440 | 0px ×72 / 0px auto ×8 / 0px 0px 12px 32px ×6 … | 0px ×82 / 0px auto ×8 / 4px 0px 12px 32px ×6 … |
| Biography | `div` | padding | 1440 | 0px ×86 / 26px 40px 30px ×8 / 0px 40px ×1 … | 0px ×94 / 26px 40px 30px ×8 / 0px 40px ×2 … |
| Biography | `figcaption` | font-size | 1440 | 15px ×9 | 16px ×9 |
| Biography | `figcaption` | line-height | 1440 | 19.5px ×9 | 20.8px ×9 |
| Biography | `figcaption` | margin-top | 1440 | 6px ×9 | 0px ×9 |
| Biography | `figure` | margin-left | 1440 | 0px ×20 / 24px ×1 | 0px ×21 |
| Biography | `p` | color | 1440 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(220, 230, 240) ×1 | rgb(43, 43, 43) ×35 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Biography | `p` | font-family | 1440 | "EB Garamond", Georgia, serif ×38 | "EB Garamond", Georgia, serif ×39 |
| Biography | `p` | font-size | 1440 | 18px ×38 | 18px ×38 / 20px ×1 |
| Biography | `p` | font-style | 1440 | normal ×36 / italic ×2 | normal ×37 / italic ×2 |
| Biography | `p` | font-weight | 1440 | 400 ×38 | 400 ×38 / 500 ×1 |
| Biography | `p` | line-height | 1440 | 29.7px ×35 / 40px ×3 | 29.7px ×35 / 40px ×3 / 33px ×1 |
| Biography | `p` | margin | 1440 | 14px 0px ×28 / 0px 0px 14px ×7 / 0px 250px ×3 | 11.3px 0px 0px ×26 / 0px ×4 / 6.55px 0px 0px ×3 … |
| Biography | `p` | margin-left | 1440 | 0px ×35 / 250px ×3 | 0px ×39 |
| Biography | `p` | margin-top | 1440 | 14px ×28 / 0px ×10 | 11.3px ×26 / 0px ×5 / 6.55px ×3 … |
| Biography | `p` | max-width | 1440 | none ×35 / 860px ×3 | none ×39 |
| Biography | `p` | padding-left | 1440 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-align | 1440 | justify ×35 / center ×3 | justify ×35 / center ×3 / start ×1 |
| Biography | `p` | text-indent | 1440 | 0px ×38 | 0px ×39 |
| Biography | `p` | text-wrap | 1440 | wrap ×35 / balance ×3 | wrap ×39 |
| Biography | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×83 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×84 |
| Biography | `span` | border-radius | 1440 | 0px ×83 | 0px ×84 |
| Biography | `span` | color | 1440 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Biography | `span` | display | 1440 | block ×83 | block ×83 / inline ×1 |
| Biography | `span` | flex | 1440 | 0 1 auto ×83 | 0 1 auto ×84 |
| Biography | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×82 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×83 / Vollkorn, Georgia, serif ×1 |
| Biography | `span` | font-size | 1440 | 17px ×81 / 40px ×1 / 15px ×1 | 18px ×82 / 40px ×1 / 15px ×1 |
| Biography | `span` | font-weight | 1440 | 400 ×82 / 500 ×1 | 400 ×83 / 500 ×1 |
| Biography | `span` | line-height | 1440 | 22.1px ×81 / 48px ×1 / 24.75px ×1 | 23.4px ×81 / 48px ×1 / 40px ×1 … |
| Biography | `span` | margin-left | 1440 | 0px ×83 | 0px ×84 |
| Biography | `span` | min-width | 1440 | 0px ×82 / auto ×1 | 0px ×83 / auto ×1 |
| Biography | `span` | padding | 1440 | 8px 0px ×81 / 0px ×2 | 8px 0px ×81 / 0px ×3 |
| Biography | `span` | text-align | 1440 | left ×81 / start ×2 | left ×81 / start ×2 / center ×1 |
| Biography | `ul` | list-style | 1440 | outside none none ×34 | outside none none ×36 |
| Biography | `ul` | margin | 1440 | 0px ×34 | 0px ×36 |
| Biography | `ul` | margin-left | 1440 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding | 1440 | 0px ×34 | 0px ×36 |
| Biography | `ul` | padding-left | 1440 | 0px ×34 | 0px ×36 |
| Sensorial Resources | `.material-name` | margin | 390 | 33.3px 0px 0px ×11 / 32px 0px 0px ×2 | 29.55px 0px 0px ×8 / 33.3px 0px 0px ×3 / 32px 0px 0px ×1 … |
| Sensorial Resources | `.material-name` | margin-top | 390 | 33.3px ×11 / 32px ×2 | 29.55px ×8 / 33.3px ×3 / 32px ×1 … |
| Sensorial Resources | `.meta` | display | 390 | block ×10 | block ×6 / inline ×4 |
| Sensorial Resources | `.mm-float` | margin | 390 | 12px 0px ×3 / 12px 0px 36px ×3 | 12px 0px ×6 |
| Sensorial Resources | `.pdf` | display | 390 | block ×4 / inline-block ×4 | inline ×4 / inline-block ×4 |
| Sensorial Resources | `.pdf` | margin-left | 390 | 0px ×6 / 24px ×2 | 24px ×8 |
| Sensorial Resources | `.ph` | scroll-snap-align | 390 | start ×14 | center ×14 |
| Sensorial Resources | `.res-desc` | line-height | 390 | 28.05px ×12 | 36px ×12 |
| Sensorial Resources | `.res-desc` | margin | 390 | 4px 0px ×11 / 3.3px 0px 4px ×1 | 4px 0px ×10 / -0.45px 0px 4px ×1 / 6.8px 0px 4px ×1 |
| Sensorial Resources | `.res-desc` | margin-top | 390 | 4px ×11 / 3.3px ×1 | 4px ×10 / -0.45px ×1 / 6.8px ×1 |
| Sensorial Resources | `.res-entry` | margin | 390 | 0px 0px 8px ×13 | 0px 0px 8px ×11 / -3px 0px 8px ×1 / 22px 0px 8px ×1 |
| Sensorial Resources | `.res-item` | display | 390 | flex ×21 | flex ×18 / block ×3 |
| Sensorial Resources | `.res-item` | margin | 390 | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 23.3px 0px 4px ×1 … | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 19.55px 0px 4px ×1 … |
| Sensorial Resources | `.res-item` | margin-top | 390 | 3.3px ×12 / 35px ×6 / 23.3px ×1 … | 3.3px ×12 / 35px ×6 / 19.55px ×1 … |
| Sensorial Resources | `.res-link` | margin-top | 390 | 4px ×1 / 31.5px ×1 | 22px ×1 / 4px ×1 |
| Sensorial Resources | `.res-title` | display | 390 | block ×21 | block ×18 / inline ×3 |
| Sensorial Resources | `.section` | margin-top | 390 | 48px ×3 / 32px ×1 | 43.97px ×2 / 34px ×1 / 33px ×1 |
| Sensorial Resources | `.toc-label` | font-size | 390 | 20px ×1 | 19px ×1 |
| Sensorial Resources | `.toc-label` | line-height | 390 | 33px ×1 | 31.35px ×1 |
| Sensorial Resources | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Sensorial Resources | `a` | border-bottom | 390 | 0px none rgb(231, 238, 245) ×24 / 0px none rgb(5, 99, 193) ×18 / 0px none rgb(255, 255, 255) ×9 … | 0px none rgb(231, 238, 245) ×24 / 0px none rgb(4, 50, 255) ×18 / 0px none rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | border-bottom-color | 390 | rgb(5, 99, 193) ×26 / rgb(231, 238, 245) ×24 / rgb(255, 255, 255) ×9 … | rgb(231, 238, 245) ×24 / rgb(4, 50, 255) ×18 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | color | 390 | rgb(5, 99, 193) ×26 / rgb(231, 238, 245) ×24 / rgb(255, 255, 255) ×9 … | rgb(231, 238, 245) ×24 / rgb(4, 50, 255) ×18 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | display | 390 | block ×48 / inline ×22 / inline-block ×4 | block ×44 / inline ×26 / inline-block ×4 |
| Sensorial Resources | `a` | font-size | 390 | 17px ×52 / 18px ×12 / 11px ×8 … | 17px ×64 / 11px ×8 / 21px ×1 … |
| Sensorial Resources | `a` | line-height | 390 | 22.1px ×33 / 28.05px ×19 / 29.7px ×8 … | 22.1px ×33 / 28.05px ×19 / 11px ×8 … |
| Sensorial Resources | `a` | margin-left | 390 | 0px ×72 / 24px ×2 | 0px ×66 / 24px ×8 |
| Sensorial Resources | `a` | outline | 390 | rgb(5, 99, 193) none 3px ×26 / rgb(231, 238, 245) none 3px ×24 / rgb(255, 255, 255) none 3px ×9 … | rgb(231, 238, 245) none 3px ×24 / rgb(4, 50, 255) none 3px ×18 / rgb(255, 255, 255) none 3px ×9 … |
| Sensorial Resources | `a` | overflow-wrap | 390 | normal ×74 | normal ×48 / anywhere ×26 |
| Sensorial Resources | `div` | margin | 390 | 0px ×48 / 24px 0px 0px ×15 / 0px 0px 8px ×13 … | 0px ×48 / 24px 0px 0px ×15 / 3.3px 0px 4px ×12 … |
| Sensorial Resources | `div` | padding | 390 | 0px ×103 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×99 / 0px 0px 10px 14px ×8 / 13px 0px 0px ×2 … |
| Sensorial Resources | `em` | font-style | 390 | normal ×26 / italic ×3 | normal ×21 / italic ×8 |
| Sensorial Resources | `h2` | margin | 390 | 0px 0px 16px ×4 | 0px 0px 8px ×4 |
| Sensorial Resources | `h2` | margin-bottom | 390 | 16px ×4 | 8px ×4 |
| Sensorial Resources | `html` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Sensorial Resources | `li` | margin | 390 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px ×2 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px 0px ×1 … |
| Sensorial Resources | `li` | margin-bottom | 390 | 0px ×122 / 10px ×4 / 8px ×2 | 0px ×123 / 10px ×4 / 8px ×1 |
| Sensorial Resources | `li` | margin-top | 390 | 0px ×126 / 8px ×2 | 0px ×126 / 8px ×1 / 4.3px ×1 |
| Sensorial Resources | `li` | text-align | 390 | left ×124 / justify ×4 | left ×128 |
| Sensorial Resources | `li::before` | text-align | 390 | left ×124 / justify ×4 | left ×128 |
| Sensorial Resources | `p` | font-size | 390 | 17px ×26 / 20px ×1 | 17px ×26 / 19px ×1 |
| Sensorial Resources | `p` | line-height | 390 | 28.05px ×21 / 38px ×5 / 33px ×1 | 36px ×12 / 28.05px ×9 / 38px ×5 … |
| Sensorial Resources | `p` | margin | 390 | 4px 0px ×11 / 3.5px 0px 14px ×6 / 0px ×5 … | 4px 0px ×10 / 3.5px 0px 14px ×6 / 0px ×5 … |
| Sensorial Resources | `p` | margin-top | 390 | 4px ×11 / 0px ×7 / 3.5px ×6 … | 4px ×10 / 0px ×6 / 3.5px ×6 … |
| Sensorial Resources | `p` | max-width | 390 | none ×24 / 860px ×3 | none ×27 |
| Sensorial Resources | `p` | text-wrap | 390 | wrap ×24 / balance ×3 | wrap ×27 |
| Sensorial Resources | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×116 / rgb(230, 230, 228) none repeat scroll 0% ×6 / rgb(43, 43, 43) none repeat scroll 0% 0% ×2 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×117 / rgb(230, 230, 228) none repeat scroll 0% ×6 / rgb(43, 43, 43) none repeat scroll 0% 0% ×2 |
| Sensorial Resources | `span` | border-radius | 390 | 0px ×116 / 50% ×8 | 0px ×117 / 50% ×8 |
| Sensorial Resources | `span` | color | 390 | rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×21 / rgb(0, 0, 0) ×12 … | rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×21 / rgb(0, 0, 0) ×12 … |
| Sensorial Resources | `span` | display | 390 | block ×124 | block ×115 / inline ×10 |
| Sensorial Resources | `span` | flex | 390 | 0 1 auto ×124 | 0 1 auto ×125 |
| Sensorial Resources | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×123 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×124 / Vollkorn, Georgia, serif ×1 |
| Sensorial Resources | `span` | font-size | 390 | 17px ×122 / 28px ×1 / 15px ×1 | 17px ×123 / 28px ×1 / 15px ×1 |
| Sensorial Resources | `span` | font-weight | 390 | 400 ×123 / 500 ×1 | 400 ×124 / 500 ×1 |
| Sensorial Resources | `span` | line-height | 390 | 22.1px ×81 / 28.05px ×41 / 33.6px ×1 … | 22.1px ×81 / 28.05px ×41 / 33.6px ×1 … |
| Sensorial Resources | `span` | margin-left | 390 | 0px ×124 | 0px ×125 |
| Sensorial Resources | `span` | min-width | 390 | 0px ×82 / auto ×42 | 0px ×92 / auto ×33 |
| Sensorial Resources | `span` | padding | 390 | 7px 0px ×81 / 0px ×43 | 7px 0px ×81 / 0px ×44 |
| Sensorial Resources | `span` | text-align | 390 | left ×83 / start ×41 | left ×83 / start ×41 / center ×1 |
| Sensorial Resources | `ul` | list-style | 390 | outside none none ×35 | outside none none ×37 |
| Sensorial Resources | `ul` | margin | 390 | 0px ×27 / 24px 0px 0px ×8 | 0px ×29 / 24px 0px 0px ×8 |
| Sensorial Resources | `ul` | margin-left | 390 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding | 390 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding-left | 390 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `.material-name` | margin | 831 | 33.3px 0px 0px ×11 / 32px 0px 0px ×2 | 29.55px 0px 0px ×8 / 33.3px 0px 0px ×3 / 0px ×2 |
| Sensorial Resources | `.material-name` | margin-top | 831 | 33.3px ×11 / 32px ×2 | 29.55px ×8 / 33.3px ×3 / 0px ×2 |
| Sensorial Resources | `.mc-band` | margin-top | 831 | -52.02px ×1 | -32px ×1 |
| Sensorial Resources | `.mm-float` | margin | 831 | 0px 0px 36px 32px ×2 / 24px 0px 12px 32px ×1 / 4px 0px 36px 32px ×1 … | 4px 0px 12px 32px ×4 / 0px 0px 12px 32px ×2 |
| Sensorial Resources | `.mm-float` | margin-top | 831 | 4px ×2 / 0px ×2 / 24px ×1 … | 4px ×4 / 0px ×2 |
| Sensorial Resources | `.mm-float` | padding-top | 831 | 0px ×6 | 0px ×4 / 18px ×1 / 58.19px ×1 |
| Sensorial Resources | `.mm-row` | margin | 831 | 60.33px 0px 20px ×2 | 56.8px 0px 20px ×1 / 60.33px 0px 20px ×1 |
| Sensorial Resources | `.mm-row` | margin-top | 831 | 60.33px ×2 | 56.8px ×1 / 60.33px ×1 |
| Sensorial Resources | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Sensorial Resources | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Sensorial Resources | `.pdf` | display | 831 | block ×4 / inline-block ×4 | inline-block ×6 / block ×2 |
| Sensorial Resources | `.pdf` | margin-left | 831 | 0px ×6 / 24px ×2 | 0px ×4 / 24px ×4 |
| Sensorial Resources | `.pullquote` | margin | 831 | 24px 20px ×2 | 24px 0px ×2 |
| Sensorial Resources | `.pullquote` | margin-left | 831 | 20px ×2 | 0px ×2 |
| Sensorial Resources | `.pullquote` | margin-right | 831 | 20px ×2 | 0px ×2 |
| Sensorial Resources | `.res-desc` | line-height | 831 | 29.7px ×12 | 37.2px ×12 |
| Sensorial Resources | `.res-desc` | margin | 831 | 4px 0px ×11 / 3.3px 0px 4px ×1 | 4px 0px ×10 / -0.45px 0px 4px ×1 / 6.8px 0px 4px ×1 |
| Sensorial Resources | `.res-desc` | margin-top | 831 | 4px ×11 / 3.3px ×1 | 4px ×10 / -0.45px ×1 / 6.8px ×1 |
| Sensorial Resources | `.res-entry` | margin | 831 | 0px 0px 8px ×13 | 0px 0px 8px ×11 / 22px 0px 8px ×2 |
| Sensorial Resources | `.res-item` | margin | 831 | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 23.3px 0px 4px ×1 … | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 19.55px 0px 4px ×1 … |
| Sensorial Resources | `.res-item` | margin-top | 831 | 3.3px ×12 / 35px ×6 / 23.3px ×1 … | 3.3px ×12 / 35px ×6 / 19.55px ×1 … |
| Sensorial Resources | `.res-link` | margin-top | 831 | 4px ×1 / 31.5px ×1 | 22px ×1 / 4px ×1 |
| Sensorial Resources | `.section` | margin-top | 831 | 48px ×3 / 32px ×1 | 42.32px ×2 / 32.3px ×1 / 46px ×1 |
| Sensorial Resources | `.site-foot-in` | padding | 831 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Sensorial Resources | `.site-foot-in` | padding-bottom | 831 | 48px ×1 | 17.625px ×1 |
| Sensorial Resources | `.site-foot-in` | padding-top | 831 | 32px ×1 | 17.625px ×1 |
| Sensorial Resources | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Sensorial Resources | `a` | border-bottom | 831 | 0px none rgb(43, 43, 43) ×24 / 0px none rgb(5, 99, 193) ×18 / 0px none rgb(255, 255, 255) ×9 … | 0px none rgb(4, 50, 255) ×26 / 0px none rgb(43, 43, 43) ×24 / 0px none rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | border-bottom-color | 831 | rgb(5, 99, 193) ×26 / rgb(43, 43, 43) ×24 / rgb(255, 255, 255) ×9 … | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×24 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | color | 831 | rgb(5, 99, 193) ×26 / rgb(43, 43, 43) ×24 / rgb(255, 255, 255) ×9 … | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×24 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | display | 831 | block ×48 / inline ×22 / inline-block ×4 | block ×46 / inline ×22 / inline-block ×6 |
| Sensorial Resources | `a` | font-size | 831 | 17px ×33 / 18px ×31 / 11px ×8 … | 18px ×64 / 11px ×8 / 25px ×1 … |
| Sensorial Resources | `a` | line-height | 831 | 22.1px ×33 / 29.7px ×27 / 11px ×8 … | 23.4px ×33 / 29.7px ×19 / 11px ×8 … |
| Sensorial Resources | `a` | margin-left | 831 | 0px ×72 / 24px ×2 | 0px ×70 / 24px ×4 |
| Sensorial Resources | `a` | outline | 831 | rgb(5, 99, 193) none 3px ×26 / rgb(43, 43, 43) none 3px ×24 / rgb(255, 255, 255) none 3px ×9 … | rgb(4, 50, 255) none 3px ×26 / rgb(43, 43, 43) none 3px ×24 / rgb(255, 255, 255) none 3px ×9 … |
| Sensorial Resources | `a` | overflow-wrap | 831 | normal ×74 | normal ×48 / anywhere ×26 |
| Sensorial Resources | `div` | margin | 831 | 0px ×47 / 24px 0px 0px ×15 / 0px 0px 8px ×13 … | 0px ×47 / 24px 0px 0px ×15 / 3.3px 0px 4px ×12 … |
| Sensorial Resources | `div` | padding | 831 | 0px ×101 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×99 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Sensorial Resources | `em` | font-style | 831 | normal ×26 / italic ×3 | normal ×21 / italic ×8 |
| Sensorial Resources | `h2` | margin | 831 | 0px 0px 16px ×4 | 0px 0px 8px ×4 |
| Sensorial Resources | `h2` | margin-bottom | 831 | 16px ×4 | 8px ×4 |
| Sensorial Resources | `html` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Sensorial Resources | `li` | margin | 831 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px ×2 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px 0px ×1 … |
| Sensorial Resources | `li` | margin-bottom | 831 | 0px ×122 / 10px ×4 / 8px ×2 | 0px ×123 / 10px ×4 / 8px ×1 |
| Sensorial Resources | `li` | margin-top | 831 | 0px ×126 / 8px ×2 | 0px ×126 / 8px ×1 / 4.3px ×1 |
| Sensorial Resources | `li` | text-align | 831 | left ×122 / justify ×6 | left ×126 / justify ×2 |
| Sensorial Resources | `li::before` | text-align | 831 | left ×122 / justify ×6 | left ×126 / justify ×2 |
| Sensorial Resources | `p` | line-height | 831 | 29.7px ×21 / 40px ×5 / 33px ×1 | 37.2px ×12 / 29.7px ×9 / 40px ×5 … |
| Sensorial Resources | `p` | margin | 831 | 4px 0px ×11 / 3.5px 0px 14px ×6 / 0px ×5 … | 4px 0px ×10 / 3.5px 0px 14px ×6 / 0px ×5 … |
| Sensorial Resources | `p` | margin-top | 831 | 4px ×11 / 0px ×7 / 3.5px ×6 … | 4px ×10 / 0px ×6 / 3.5px ×6 … |
| Sensorial Resources | `p` | max-width | 831 | none ×24 / 860px ×3 | none ×27 |
| Sensorial Resources | `p` | text-wrap | 831 | wrap ×24 / balance ×3 | wrap ×27 |
| Sensorial Resources | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×116 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×117 |
| Sensorial Resources | `span` | border-radius | 831 | 0px ×116 | 0px ×117 |
| Sensorial Resources | `span` | color | 831 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×32 / rgb(0, 0, 0) ×12 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×32 / rgb(0, 0, 0) ×12 … |
| Sensorial Resources | `span` | display | 831 | block ×116 | block ×114 / inline ×3 |
| Sensorial Resources | `span` | flex | 831 | 0 1 auto ×116 | 0 1 auto ×117 |
| Sensorial Resources | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×115 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×116 / Vollkorn, Georgia, serif ×1 |
| Sensorial Resources | `span` | font-size | 831 | 17px ×81 / 18px ×33 / 40px ×1 … | 18px ×115 / 40px ×1 / 15px ×1 |
| Sensorial Resources | `span` | font-weight | 831 | 400 ×115 / 500 ×1 | 400 ×116 / 500 ×1 |
| Sensorial Resources | `span` | line-height | 831 | 22.1px ×81 / 29.7px ×33 / 48px ×1 … | 23.4px ×81 / 29.7px ×33 / 48px ×1 … |
| Sensorial Resources | `span` | margin-left | 831 | 0px ×116 | 0px ×117 |
| Sensorial Resources | `span` | min-width | 831 | 0px ×82 / auto ×34 | 0px ×85 / auto ×32 |
| Sensorial Resources | `span` | padding | 831 | 7px 0px ×81 / 0px ×35 | 7px 0px ×81 / 0px ×36 |
| Sensorial Resources | `span` | text-align | 831 | left ×81 / start ×33 / justify ×2 | left ×81 / start ×33 / justify ×2 … |
| Sensorial Resources | `ul` | list-style | 831 | outside none none ×35 | outside none none ×37 |
| Sensorial Resources | `ul` | margin | 831 | 0px ×27 / 24px 0px 0px ×8 | 0px ×29 / 24px 0px 0px ×8 |
| Sensorial Resources | `ul` | margin-left | 831 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding | 831 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding-left | 831 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `.material-name` | margin | 1440 | 33.3px 0px 0px ×11 / 32px 0px 0px ×2 | 29.55px 0px 0px ×8 / 33.3px 0px 0px ×3 / 0px ×2 |
| Sensorial Resources | `.material-name` | margin-top | 1440 | 33.3px ×11 / 32px ×2 | 29.55px ×8 / 33.3px ×3 / 0px ×2 |
| Sensorial Resources | `.mc-band` | margin-top | 1440 | -52.02px ×1 | -32px ×1 |
| Sensorial Resources | `.mm-float` | margin | 1440 | 0px 0px 36px 32px ×2 / 24px 0px 12px 32px ×1 / 4px 0px 36px 32px ×1 … | 4px 0px 12px 32px ×4 / 0px 0px 12px 32px ×2 |
| Sensorial Resources | `.mm-float` | margin-top | 1440 | 4px ×2 / 0px ×2 / 24px ×1 … | 4px ×4 / 0px ×2 |
| Sensorial Resources | `.mm-float` | padding-top | 1440 | 0px ×6 | 0px ×4 / 18px ×1 / 58.19px ×1 |
| Sensorial Resources | `.mm-row` | margin | 1440 | 60.33px 0px 20px ×2 | 56.8px 0px 20px ×1 / 60.33px 0px 20px ×1 |
| Sensorial Resources | `.mm-row` | margin-top | 1440 | 60.33px ×2 | 56.8px ×1 / 60.33px ×1 |
| Sensorial Resources | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Sensorial Resources | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Sensorial Resources | `.pdf` | display | 1440 | block ×4 / inline-block ×4 | inline-block ×6 / block ×2 |
| Sensorial Resources | `.pdf` | margin-left | 1440 | 0px ×6 / 24px ×2 | 0px ×4 / 24px ×4 |
| Sensorial Resources | `.pullquote` | margin | 1440 | 24px 20px ×2 | 24px 0px ×2 |
| Sensorial Resources | `.pullquote` | margin-left | 1440 | 20px ×2 | 0px ×2 |
| Sensorial Resources | `.pullquote` | margin-right | 1440 | 20px ×2 | 0px ×2 |
| Sensorial Resources | `.res-desc` | line-height | 1440 | 29.7px ×12 | 37.2px ×12 |
| Sensorial Resources | `.res-desc` | margin | 1440 | 4px 0px ×11 / 3.3px 0px 4px ×1 | 4px 0px ×10 / -0.45px 0px 4px ×1 / 6.8px 0px 4px ×1 |
| Sensorial Resources | `.res-desc` | margin-top | 1440 | 4px ×11 / 3.3px ×1 | 4px ×10 / -0.45px ×1 / 6.8px ×1 |
| Sensorial Resources | `.res-entry` | margin | 1440 | 0px 0px 8px ×13 | 0px 0px 8px ×11 / 22px 0px 8px ×2 |
| Sensorial Resources | `.res-item` | margin | 1440 | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 23.3px 0px 4px ×1 … | 3.3px 0px 4px ×12 / 35px 0px 0px ×6 / 19.55px 0px 4px ×1 … |
| Sensorial Resources | `.res-item` | margin-top | 1440 | 3.3px ×12 / 35px ×6 / 23.3px ×1 … | 3.3px ×12 / 35px ×6 / 19.55px ×1 … |
| Sensorial Resources | `.res-link` | margin-top | 1440 | 4px ×1 / 31.5px ×1 | 22px ×1 / 4px ×1 |
| Sensorial Resources | `.section` | margin-top | 1440 | 48px ×3 / 32px ×1 | 42.32px ×2 / 32.3px ×1 / 46px ×1 |
| Sensorial Resources | `.site-foot-in` | padding | 1440 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Sensorial Resources | `.site-foot-in` | padding-bottom | 1440 | 48px ×1 | 17.625px ×1 |
| Sensorial Resources | `.site-foot-in` | padding-top | 1440 | 32px ×1 | 17.625px ×1 |
| Sensorial Resources | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Sensorial Resources | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Sensorial Resources | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Sensorial Resources | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Sensorial Resources | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Sensorial Resources | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(5, 99, 193) ×18 / 1px solid rgba(0, 0, 0, 0) ×11 … | 0px none rgb(4, 50, 255) ×26 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | border-bottom-color | 1440 | rgb(5, 99, 193) ×26 / rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×11 … | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | color | 1440 | rgb(5, 99, 193) ×26 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Sensorial Resources | `a` | display | 1440 | block ×48 / inline ×22 / inline-block ×4 | block ×46 / inline ×22 / inline-block ×6 |
| Sensorial Resources | `a` | font-size | 1440 | 17px ×41 / 18px ×23 / 11px ×8 … | 18px ×64 / 11px ×8 / 25px ×1 … |
| Sensorial Resources | `a` | line-height | 1440 | 22.1px ×33 / 29.7px ×19 / 28.05px ×8 … | 23.4px ×33 / 29.7px ×19 / 11px ×8 … |
| Sensorial Resources | `a` | margin-left | 1440 | 0px ×72 / 24px ×2 | 0px ×70 / 24px ×4 |
| Sensorial Resources | `a` | outline | 1440 | rgb(5, 99, 193) none 3px ×26 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … | rgb(4, 50, 255) none 3px ×26 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Sensorial Resources | `a` | overflow-wrap | 1440 | normal ×74 | normal ×48 / anywhere ×26 |
| Sensorial Resources | `a` | padding | 1440 | 8px 0px ×33 / 0px ×25 / 6px 0px ×8 … | 8px 0px ×33 / 0px ×25 / 6px 0px 7.5px ×8 … |
| Sensorial Resources | `a` | text-decoration | 1440 | none ×53 / underline ×21 | none ×52 / underline ×22 |
| Sensorial Resources | `a` | text-underline-offset | 1440 | auto ×73 / 3px ×1 | auto ×72 / 4px ×1 / 3px ×1 |
| Sensorial Resources | `div` | margin | 1440 | 0px ×60 / 0px 0px 8px ×13 / 3.3px 0px 4px ×12 … | 0px ×60 / 3.3px 0px 4px ×12 / 0px 0px 8px ×11 … |
| Sensorial Resources | `div` | padding | 1440 | 0px ×101 / 26px 40px 30px ×8 / 0px 40px ×1 … | 0px ×99 / 26px 40px 30px ×8 / 0px 40px ×1 … |
| Sensorial Resources | `em` | font-style | 1440 | normal ×26 / italic ×3 | normal ×21 / italic ×8 |
| Sensorial Resources | `h2` | margin | 1440 | 0px 0px 16px ×4 | 0px 0px 8px ×4 |
| Sensorial Resources | `h2` | margin-bottom | 1440 | 16px ×4 | 8px ×4 |
| Sensorial Resources | `html` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Sensorial Resources | `li` | margin | 1440 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px ×2 | 0px ×122 / 0px 0px 10px ×4 / 8px 0px 0px ×1 … |
| Sensorial Resources | `li` | margin-bottom | 1440 | 0px ×122 / 10px ×4 / 8px ×2 | 0px ×123 / 10px ×4 / 8px ×1 |
| Sensorial Resources | `li` | margin-top | 1440 | 0px ×126 / 8px ×2 | 0px ×126 / 8px ×1 / 4.3px ×1 |
| Sensorial Resources | `li` | text-align | 1440 | left ×122 / justify ×6 | left ×126 / justify ×2 |
| Sensorial Resources | `li::before` | text-align | 1440 | left ×122 / justify ×6 | left ×126 / justify ×2 |
| Sensorial Resources | `p` | line-height | 1440 | 29.7px ×21 / 40px ×5 / 33px ×1 | 37.2px ×12 / 29.7px ×9 / 40px ×5 … |
| Sensorial Resources | `p` | margin | 1440 | 4px 0px ×11 / 3.5px 0px 14px ×6 / 0px 250px ×3 … | 4px 0px ×10 / 3.5px 0px 14px ×6 / 0px ×5 … |
| Sensorial Resources | `p` | margin-left | 1440 | 0px ×24 / 250px ×3 | 0px ×27 |
| Sensorial Resources | `p` | margin-top | 1440 | 4px ×11 / 0px ×7 / 3.5px ×6 … | 4px ×10 / 0px ×6 / 3.5px ×6 … |
| Sensorial Resources | `p` | max-width | 1440 | none ×24 / 860px ×3 | none ×27 |
| Sensorial Resources | `p` | text-wrap | 1440 | wrap ×24 / balance ×3 | wrap ×27 |
| Sensorial Resources | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×116 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×117 |
| Sensorial Resources | `span` | border-radius | 1440 | 0px ×116 | 0px ×117 |
| Sensorial Resources | `span` | color | 1440 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×32 / rgb(0, 0, 0) ×12 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×32 / rgb(0, 0, 0) ×12 … |
| Sensorial Resources | `span` | display | 1440 | block ×116 | block ×114 / inline ×3 |
| Sensorial Resources | `span` | flex | 1440 | 0 1 auto ×116 | 0 1 auto ×117 |
| Sensorial Resources | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×115 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×116 / Vollkorn, Georgia, serif ×1 |
| Sensorial Resources | `span` | font-size | 1440 | 17px ×81 / 18px ×33 / 40px ×1 … | 18px ×115 / 40px ×1 / 15px ×1 |
| Sensorial Resources | `span` | font-weight | 1440 | 400 ×115 / 500 ×1 | 400 ×116 / 500 ×1 |
| Sensorial Resources | `span` | line-height | 1440 | 22.1px ×81 / 29.7px ×33 / 48px ×1 … | 23.4px ×81 / 29.7px ×33 / 48px ×1 … |
| Sensorial Resources | `span` | margin-left | 1440 | 0px ×116 | 0px ×117 |
| Sensorial Resources | `span` | min-width | 1440 | 0px ×82 / auto ×34 | 0px ×85 / auto ×32 |
| Sensorial Resources | `span` | padding | 1440 | 8px 0px ×81 / 0px ×35 | 8px 0px ×81 / 0px ×36 |
| Sensorial Resources | `span` | text-align | 1440 | left ×81 / start ×33 / justify ×2 | left ×81 / start ×33 / justify ×2 … |
| Sensorial Resources | `ul` | list-style | 1440 | outside none none ×35 | outside none none ×37 |
| Sensorial Resources | `ul` | margin | 1440 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | margin-left | 1440 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding | 1440 | 0px ×35 | 0px ×37 |
| Sensorial Resources | `ul` | padding-left | 1440 | 0px ×35 | 0px ×37 |
| Mathematics | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Mathematics | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Mathematics | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Mathematics | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Mathematics | `.mc-band` | color | 390 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Mathematics | `.mc-band` | margin-top | 390 | -30px ×1 | -22.07px ×1 |
| Mathematics | `.micro-label` | border-top | 390 | 0px none rgb(43, 43, 43) ×52 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … | 0px none rgb(43, 43, 43) ×53 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … |
| Mathematics | `.micro-label` | line-height | 390 | 28.05px ×56 / 33px ×1 | 28.05px ×57 |
| Mathematics | `.micro-label` | margin | 390 | 27.04px 0px 0px ×24 / 15.9px 0px 0px ×10 / 21px 0px 0px ×5 … | 23.96px 0px 0px ×32 / 23.95px 0px 0px ×7 / 24.95px 0px 0px ×5 … |
| Mathematics | `.micro-label` | margin-bottom | 390 | 0px ×57 | 0px ×55 / -3.05px ×1 / -1.05px ×1 |
| Mathematics | `.micro-label` | margin-top | 390 | 27.04px ×24 / 15.9px ×10 / 21px ×5 … | 23.96px ×32 / 23.95px ×7 / 24.95px ×5 … |
| Mathematics | `.mm-area` | border-bottom | 390 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `.mm-area` | padding-bottom | 390 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `.mm-cabar` | margin | 390 | 13px 0px 0px ×1 | 8.25px 0px 0px ×1 |
| Mathematics | `.mm-cap` | line-height | 390 | 20.8px ×22 | 28.05px ×22 |
| Mathematics | `.mm-cap` | padding-top | 390 | 0px ×22 | 2px ×22 |
| Mathematics | `.mm-cap-below` | padding-top | 390 | 0px ×2 | 2px ×2 |
| Mathematics | `.mm-cols3` | margin | 390 | 27.04px 0px 0px ×1 / 23.04px 0px 0px ×1 | 12.96px 0px 0px ×2 |
| Mathematics | `.mm-g2` | column-gap | 390 | 20px ×1 | 40px ×1 |
| Mathematics | `.mm-g2` | margin | 390 | 16.95px 0px 0px ×1 | 38.47px 0px 0px ×1 |
| Mathematics | `.mm-lineabove` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 |
| Mathematics | `.mm-lineabove` | padding-top | 390 | 39px ×2 / 28px ×2 | 28px ×2 / 29.72px ×1 / 30.22px ×1 |
| Mathematics | `.mm-name` | border-top | 390 | 0px none rgb(4, 50, 255) ×24 / 2px solid rgb(217, 201, 171) ×23 | 0px none rgb(4, 50, 255) ×47 |
| Mathematics | `.mm-name` | margin-top | 390 | 24.57px ×9 / 23px ×7 / 10px ×6 … | 37.21px ×7 / 51.25px ×6 / 0px ×6 … |
| Mathematics | `.mm-name` | padding-top | 390 | 28px ×47 | 0px ×47 |
| Mathematics | `.mm-pdf-r` | padding-top | 390 | 25px ×9 / 23px ×6 / 48px ×6 … | 12.97px ×7 / 25.38px ×7 / 48px ×6 … |
| Mathematics | `.ph` | scroll-snap-align | 390 | start ×153 | center ×153 |
| Mathematics | `.pim` | max-width | 390 | none ×153 | none ×149 / min(100%, 400px) ×4 |
| Mathematics | `.pullquote` | margin | 390 | 0px ×3 / 10.9px 0px 0px ×1 / 9.9px 0px 0px ×1 … | 0px 0px 24px ×2 / 19.95px 0px 0px ×1 / 14.49px 0px 24px ×1 … |
| Mathematics | `.pullquote` | margin-bottom | 390 | 0px ×6 | 0px ×3 / 24px ×3 |
| Mathematics | `.pullquote` | margin-left | 390 | 0px ×5 / 20px ×1 | 0px ×6 |
| Mathematics | `.pullquote` | margin-right | 390 | 0px ×5 / 20px ×1 | 0px ×6 |
| Mathematics | `.pullquote` | margin-top | 390 | 0px ×4 / 10.9px ×1 / 9.9px ×1 | 0px ×2 / 19.95px ×1 / 14.49px ×1 … |
| Mathematics | `.pullquote` | padding | 390 | 0px ×2 / 24px 0px 0px ×2 / 10.9px 0px 0px ×1 … | 0px ×4 / 19.25px 0px 0px ×1 / 19px 0px 0px ×1 |
| Mathematics | `.pullquote` | padding-left | 390 | 0px ×5 / 73px ×1 | 0px ×6 |
| Mathematics | `.section` | margin-top | 390 | 0px ×28 | 0px ×27 / -13.52px ×1 |
| Mathematics | `.site-foot-in` | padding | 390 | 28px 24px 40px ×1 | 14px 24px ×1 |
| Mathematics | `.site-foot-in` | padding-bottom | 390 | 40px ×1 | 14px ×1 |
| Mathematics | `.site-foot-in` | padding-top | 390 | 28px ×1 | 14px ×1 |
| Mathematics | `.toc-label` | font-size | 390 | 20px ×1 | 19px ×1 |
| Mathematics | `.toc-label` | line-height | 390 | 33px ×1 | 31.35px ×1 |
| Mathematics | `.toc-wrap` | padding | 390 | 22px 24px 26px ×1 | 22px 24px 0px ×1 |
| Mathematics | `.toc-wrap` | padding-bottom | 390 | 26px ×1 | 0px ×1 |
| Mathematics | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Mathematics | `a` | align-items | 390 | normal ×99 | baseline ×55 / normal ×44 |
| Mathematics | `a` | color | 390 | rgb(74, 85, 96) ×48 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … | rgb(74, 85, 96) ×55 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … |
| Mathematics | `a` | display | 390 | inline ×55 / block ×44 | flex ×55 / block ×44 |
| Mathematics | `a` | font-size | 390 | 18px ×63 / 17px ×34 / 21px ×1 … | 17px ×97 / 21px ×1 / 15px ×1 |
| Mathematics | `a` | gap | 390 | normal ×99 | 8px ×55 / normal ×44 |
| Mathematics | `a` | line-height | 390 | 24.3px ×55 / 22.1px ×33 / 29.7px ×8 … | 22.95px ×55 / 22.1px ×33 / 28.05px ×9 … |
| Mathematics | `a` | outline | 390 | rgb(74, 85, 96) none 3px ×48 / rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … | rgb(74, 85, 96) none 3px ×55 / rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Mathematics | `cite` | margin-top | 390 | -2px ×2 / 9.9px ×1 | 0px ×3 |
| Mathematics | `cite` | padding-left | 390 | 11px ×2 / 73px ×1 | 48px ×3 |
| Mathematics | `div` | break-inside | 390 | auto ×401 | auto ×403 |
| Mathematics | `div` | color | 390 | rgb(43, 43, 43) ×395 / rgb(0, 176, 80) ×1 / rgb(237, 125, 49) ×1 … | rgb(43, 43, 43) ×398 / rgb(0, 176, 80) ×1 / rgb(112, 48, 160) ×1 … |
| Mathematics | `div` | font-size | 390 | 17px ×397 / 15px ×2 / 14px ×1 … | 17px ×399 / 15px ×2 / 14px ×1 … |
| Mathematics | `div` | font-style | 390 | normal ×401 | normal ×403 |
| Mathematics | `div` | margin | 390 | 0px ×317 / 27.04px 0px 0px ×25 / 24px 0px 0px ×15 … | 0px ×318 / 23.96px 0px 0px ×32 / 24px 0px 0px ×15 … |
| Mathematics | `div` | padding | 390 | 0px ×330 / 23px 0px 0px ×18 / 25px 0px 0px ×11 … | 0px ×334 / 12.97px 0px 0px ×16 / 0px 0px 10px 14px ×8 … |
| Mathematics | `h2` | border-bottom | 390 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | border-bottom-color | 390 | rgb(238, 0, 0) ×7 / rgb(43, 43, 43) ×5 | rgb(238, 0, 0) ×7 / rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | font-size | 390 | 20px ×12 | 17px ×12 |
| Mathematics | `h2` | line-height | 390 | 24px ×12 | 20.4px ×12 |
| Mathematics | `h2` | margin | 390 | 0px ×12 | 0px 0px -9.39px ×11 / 0px ×1 |
| Mathematics | `h2` | margin-bottom | 390 | 0px ×12 | -9.39px ×11 / 0px ×1 |
| Mathematics | `h2` | padding-bottom | 390 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `li` | margin | 390 | 0px ×122 / 7.95px 0px 0px ×59 / 0px 0px 10px ×51 … | 0px ×123 / 0px 0px 10px ×54 / -5px 0px 0px ×35 … |
| Mathematics | `li` | margin-bottom | 390 | 0px ×196 / 10px ×55 / 8px ×9 | 0px ×197 / 10px ×54 / 8px ×9 |
| Mathematics | `li` | margin-top | 390 | 0px ×174 / 7.95px ×59 / 19.84px ×9 … | 0px ×178 / -5px ×35 / -5.05px ×28 … |
| Mathematics | `li` | padding-left | 390 | 0px ×199 / 31px ×61 | 0px ×199 / 36.07px ×61 |
| Mathematics | `li` | text-align | 390 | left ×260 | left ×205 / justify ×55 |
| Mathematics | `li::before` | text-align | 390 | left ×260 | left ×205 / justify ×55 |
| Mathematics | `ol` | margin | 390 | 0px ×11 | 29px 0px 0px ×6 / 0px ×4 / 28.95px 0px 0px ×1 |
| Mathematics | `p` | font-size | 390 | 17px ×292 / 20px ×48 / 16px ×22 | 17px ×292 / 20px ×47 / 16px ×22 … |
| Mathematics | `p` | line-height | 390 | 36px ×327 / 20.8px ×22 / 38px ×12 … | 28.05px ×349 / 38px ×12 / 31.35px ×1 |
| Mathematics | `p` | margin | 390 | 0px ×119 / 3.95px 0px 0px ×45 / 11.9px 0px 0px ×44 … | -5px 0px 0px ×51 / -5.05px 0px 0px ×47 / 23.95px 0px 0px ×45 … |
| Mathematics | `p` | margin-top | 390 | 0px ×144 / 3.95px ×45 / 11.9px ×44 … | -5px ×51 / -5.05px ×47 / 23.95px ×45 … |
| Mathematics | `p` | max-width | 390 | none ×359 / 860px ×3 | none ×362 |
| Mathematics | `p` | padding-left | 390 | 0px ×356 / 11px ×5 / 31px ×1 | 0px ×362 |
| Mathematics | `p` | text-indent | 390 | 0px ×362 | 0px ×353 / 48px ×9 |
| Mathematics | `p` | text-wrap | 390 | wrap ×359 / balance ×3 | wrap ×362 |
| Mathematics | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×224 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×222 |
| Mathematics | `span` | border-radius | 390 | 0px ×224 | 0px ×222 |
| Mathematics | `span` | color | 390 | rgb(43, 43, 43) ×122 / rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 … | rgb(43, 43, 43) ×127 / rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 … |
| Mathematics | `span` | display | 390 | inline ×116 / block ×104 / inline-block ×4 | inline ×133 / block ×85 / inline-block ×4 |
| Mathematics | `span` | flex | 390 | 0 1 auto ×224 | 0 1 auto ×222 |
| Mathematics | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×223 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×221 / Vollkorn, Georgia, serif ×1 |
| Mathematics | `span` | font-size | 390 | 17px ×217 / 13px ×3 / 14px ×2 … | 17px ×218 / 14px ×2 / 28px ×1 … |
| Mathematics | `span` | font-weight | 390 | 400 ×223 / 500 ×1 | 400 ×221 / 500 ×1 |
| Mathematics | `span` | line-height | 390 | 36px ×136 / 22.1px ×81 / 16.25px ×3 … | 28.05px ×136 / 22.1px ×81 / 16.8px ×2 … |
| Mathematics | `span` | margin-left | 390 | 0px ×220 / 66.0599px ×1 / 13.061px ×1 … | 0px ×218 / 19.0047px ×1 / 13.0527px ×1 … |
| Mathematics | `span` | min-width | 390 | 0px ×202 / auto ×22 | 0px ×219 / auto ×3 |
| Mathematics | `span` | padding | 390 | 0px ×143 / 7px 0px ×81 | 0px ×141 / 7px 0px ×81 |
| Mathematics | `span` | text-align | 390 | left ×220 / start ×4 | left ×217 / start ×4 / center ×1 |
| Mathematics | `ul` | list-style | 390 | outside none none ×42 | outside none none ×41 |
| Mathematics | `ul` | margin | 390 | 0px ×33 / 24px 0px 0px ×8 / 15.9px 0px 0px ×1 | 0px ×32 / 24px 0px 0px ×8 / 4.27px 0px 0px ×1 |
| Mathematics | `ul` | margin-left | 390 | 0px ×42 | 0px ×41 |
| Mathematics | `ul` | padding | 390 | 0px ×37 / 0px 0px 0px 62px ×2 / 0px 0px 0px 93px ×2 … | 0px ×36 / 0px 0px 0px 93px ×2 / 0px 0px 0px 48px ×2 … |
| Mathematics | `ul` | padding-left | 390 | 0px ×37 / 62px ×2 / 93px ×2 … | 0px ×36 / 93px ×2 / 48px ×2 … |
| Mathematics | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Mathematics | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Mathematics | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Mathematics | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Mathematics | `.mc-band` | color | 831 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Mathematics | `.mc-band` | margin-top | 831 | -46.3px ×1 | -14.7px ×1 |
| Mathematics | `.micro-label` | border-top | 831 | 0px none rgb(43, 43, 43) ×52 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … | 0px none rgb(43, 43, 43) ×53 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … |
| Mathematics | `.micro-label` | line-height | 831 | 29.7px ×56 / 33px ×1 | 29.7px ×57 |
| Mathematics | `.micro-label` | margin | 831 | 27.82px 0px 0px ×25 / 16.29px 0px 0px ×11 / 2px 0px 0px ×7 … | 22.3px 0px 0px ×30 / 32.8px 0px 0px ×3 / 32.55px 0px 0px ×3 … |
| Mathematics | `.micro-label` | margin-bottom | 831 | 0px ×57 | 0px ×55 / -3.7px ×1 / -2.7px ×1 |
| Mathematics | `.micro-label` | margin-top | 831 | 27.82px ×25 / 16.29px ×11 / 2px ×7 … | 22.3px ×30 / 32.8px ×3 / 32.55px ×3 … |
| Mathematics | `.mm-area` | border-bottom | 831 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `.mm-area` | padding-bottom | 831 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `.mm-cabar` | margin | 831 | 13px 0px 0px ×1 | 9px 0px 0px ×1 |
| Mathematics | `.mm-cap` | line-height | 831 | 20.8px ×22 | 29.7px ×22 |
| Mathematics | `.mm-cap` | padding-top | 831 | 0px ×22 | 2px ×22 |
| Mathematics | `.mm-cap-below` | padding-top | 831 | 0px ×2 | 2px ×2 |
| Mathematics | `.mm-cols3` | margin | 831 | 27.82px 0px 0px ×1 / 23.82px 0px 0px ×1 | 14px 0px 0px ×2 |
| Mathematics | `.mm-flow` | margin-left | 831 | 25px ×78 / 0px ×54 / 80px ×4 … | 25px ×80 / 0px ×55 / 80px ×4 … |
| Mathematics | `.mm-g2` | column-gap | 831 | 20px ×1 | 40px ×1 |
| Mathematics | `.mm-g2` | margin | 831 | -3.9px 0px 0px ×1 | 6.35px 0px 0px ×1 |
| Mathematics | `.mm-imgs` | margin | 831 | 0px ×49 / 0px 0px 0px 5.68434e-14px ×3 / 70.2px 0px 0px ×2 … | 0px ×49 / 0px 0px 0px 5.68434e-14px ×3 / 27.98px 0px 0px ×2 … |
| Mathematics | `.mm-lineabove` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 |
| Mathematics | `.mm-lineabove` | padding-top | 831 | 38.8px ×2 / 28px ×2 | 28px ×2 / 28.55px ×1 / 34.3px ×1 |
| Mathematics | `.mm-name` | border-top | 831 | 0px none rgb(4, 50, 255) ×24 / 2px solid rgb(217, 201, 171) ×23 | 0px none rgb(4, 50, 255) ×47 |
| Mathematics | `.mm-name` | margin-top | 831 | 26.32px ×11 / 23px ×7 / 0px ×6 … | 39.86px ×8 / 0px ×7 / 51.25px ×6 … |
| Mathematics | `.mm-name` | padding-top | 831 | 28px ×47 | 0px ×47 |
| Mathematics | `.mm-pdf` | margin | 831 | 0px ×25 / 0px 12.0611px 0px 24px ×5 / 0px 0px 0px 24px ×4 … | 0px 0px 0px 24px ×32 / 0px ×25 |
| Mathematics | `.mm-pdf-r` | margin-right | 831 | 12.0611px ×5 / 0px ×4 / 8.0357px ×2 … | 0px ×32 |
| Mathematics | `.mm-pdff` | margin | 831 | 0px 0px 0px 25px ×78 / 0px ×56 / 0px 0px 0px 80px ×4 … | 0px 0px 0px 25px ×80 / 0px ×57 / 0px 0px 0px 80px ×4 … |
| Mathematics | `.mm-pdff` | margin-left | 831 | 25px ×78 / 0px ×56 / 80px ×4 … | 25px ×80 / 0px ×57 / 80px ×4 … |
| Mathematics | `.mm-tabcol` | display | 831 | grid ×44 | block ×44 |
| Mathematics | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Mathematics | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Mathematics | `.ph` | margin | 831 | 0px 0px 0px 25px ×78 / 0px ×60 / 0px 0px 0px 80px ×4 … | 0px 0px 0px 25px ×80 / 0px ×61 / 0px 0px 0px 80px ×4 … |
| Mathematics | `.pullquote` | margin | 831 | 0px 20px ×4 / 11.29px 20px 0px ×1 / 9.48px 20px 0px ×1 | 23.3px 0px 0px ×2 / 18.54px 0px 0px ×1 / 18px 0px 23px ×1 … |
| Mathematics | `.pullquote` | margin-bottom | 831 | 0px ×6 | 0px ×3 / 23px ×2 / 24.5px ×1 |
| Mathematics | `.pullquote` | margin-left | 831 | 20px ×6 | 0px ×6 |
| Mathematics | `.pullquote` | margin-right | 831 | 20px ×6 | 0px ×6 |
| Mathematics | `.pullquote` | margin-top | 831 | 0px ×4 / 11.29px ×1 / 9.48px ×1 | 23.3px ×2 / 0px ×2 / 18.54px ×1 … |
| Mathematics | `.pullquote` | padding | 831 | 0px ×2 / 24px 0px 0px ×2 / 11.29px 0px 0px ×1 … | 0px ×4 / 18.75px 0px 0px ×2 |
| Mathematics | `.pullquote` | padding-left | 831 | 0px ×5 / 73px ×1 | 0px ×6 |
| Mathematics | `.section` | margin-top | 831 | 0px ×28 | 0px ×27 / 17.95px ×1 |
| Mathematics | `.site-foot-in` | padding | 831 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Mathematics | `.site-foot-in` | padding-bottom | 831 | 48px ×1 | 17.625px ×1 |
| Mathematics | `.site-foot-in` | padding-top | 831 | 32px ×1 | 17.625px ×1 |
| Mathematics | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Mathematics | `.toc-label` | font-size | 831 | 22px ×1 | 20px ×1 |
| Mathematics | `.toc-label` | line-height | 831 | 36.3px ×1 | 33px ×1 |
| Mathematics | `.toc-wrap` | padding | 831 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Mathematics | `.toc-wrap` | padding-bottom | 831 | 36px ×1 | 0px ×1 |
| Mathematics | `a` | align-items | 831 | normal ×99 | baseline ×55 / normal ×44 |
| Mathematics | `a` | color | 831 | rgb(74, 85, 96) ×48 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … | rgb(74, 85, 96) ×55 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Mathematics | `a` | display | 831 | inline ×55 / block ×44 | flex ×55 / block ×44 |
| Mathematics | `a` | font-size | 831 | 19px ×55 / 17px ×33 / 18px ×9 … | 18px ×97 / 25px ×1 / 15px ×1 |
| Mathematics | `a` | gap | 831 | normal ×99 | 8px ×55 / normal ×44 |
| Mathematics | `a` | line-height | 831 | 25.65px ×55 / 22.1px ×33 / 29.7px ×9 … | 24.3px ×55 / 23.4px ×33 / 29.7px ×9 … |
| Mathematics | `a` | outline | 831 | rgb(74, 85, 96) none 3px ×48 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … | rgb(74, 85, 96) none 3px ×55 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Mathematics | `cite` | margin-top | 831 | -2.8px ×2 / 9.48px ×1 | 0px ×3 |
| Mathematics | `cite` | padding-left | 831 | 11px ×2 / 73px ×1 | 48px ×3 |
| Mathematics | `div` | break-inside | 831 | auto ×433 | auto ×435 |
| Mathematics | `div` | color | 831 | rgb(43, 43, 43) ×427 / rgb(0, 176, 80) ×1 / rgb(237, 125, 49) ×1 … | rgb(43, 43, 43) ×430 / rgb(0, 176, 80) ×1 / rgb(112, 48, 160) ×1 … |
| Mathematics | `div` | font-size | 831 | 18px ×429 / 15px ×2 / 14px ×1 … | 18px ×431 / 15px ×2 / 14px ×1 … |
| Mathematics | `div` | font-style | 831 | normal ×433 | normal ×435 |
| Mathematics | `div` | margin | 831 | 0px ×301 / 27.82px 0px 0px ×26 / 24px 0px 0px ×15 … | 0px ×304 / 0px 0px 0px 24px ×32 / 22.3px 0px 0px ×30 … |
| Mathematics | `div` | padding | 831 | 0px ×393 / 22.8px 0px 0px ×11 / 0px 0px 10px 14px ×8 … | 0px ×395 / 44.55px 0px 0px ×10 / 0px 0px 10px 14px ×8 … |
| Mathematics | `figure` | margin-left | 831 | 25px ×78 / 0px ×60 / 80px ×4 … | 25px ×80 / 0px ×61 / 80px ×4 … |
| Mathematics | `h2` | border-bottom | 831 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | border-bottom-color | 831 | rgb(238, 0, 0) ×7 / rgb(43, 43, 43) ×5 | rgb(238, 0, 0) ×7 / rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | font-size | 831 | 22px ×7 / 20px ×5 | 18px ×12 |
| Mathematics | `h2` | line-height | 831 | 26.4px ×7 / 24px ×5 | 21.6px ×12 |
| Mathematics | `h2` | margin | 831 | 0px ×12 | 0px 0px -9.59px ×11 / 0px ×1 |
| Mathematics | `h2` | margin-bottom | 831 | 0px ×12 | -9.59px ×11 / 0px ×1 |
| Mathematics | `h2` | padding-bottom | 831 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `li` | margin | 831 | 0px ×122 / 7.52px 0px 0px ×59 / 0px 0px 10px ×51 … | 0px ×123 / 0px 0px 10px ×54 / -5px 0px 0px ×45 … |
| Mathematics | `li` | margin-bottom | 831 | 0px ×196 / 10px ×55 / 8px ×9 | 0px ×197 / 10px ×54 / 8px ×9 |
| Mathematics | `li` | margin-top | 831 | 0px ×174 / 7.52px ×59 / 19.79px ×9 … | 0px ×178 / -5px ×45 / -5.72px ×16 … |
| Mathematics | `li` | padding-left | 831 | 0px ×199 / 31px ×61 | 0px ×199 / 36.78px ×61 |
| Mathematics | `li` | text-align | 831 | left ×177 / justify ×83 | justify ×138 / left ×122 |
| Mathematics | `li::before` | text-align | 831 | left ×177 / justify ×83 | justify ×138 / left ×122 |
| Mathematics | `ol` | margin | 831 | 0px ×11 | 0px ×6 / 28.02px 0px 0px ×3 / 27.8px 0px 0px ×2 |
| Mathematics | `p` | font-size | 831 | 18px ×292 / 20px ×47 / 16px ×22 … | 18px ×292 / 20px ×48 / 16px ×22 |
| Mathematics | `p` | line-height | 831 | 37.2px ×327 / 20.8px ×22 / 40px ×12 … | 29.7px ×349 / 40px ×12 / 33px ×1 |
| Mathematics | `p` | margin | 831 | 0px ×121 / 3.52px 0px 0px ×47 / 12.29px 0px 0px ×43 … | -5.72px 0px 0px ×57 / -5px 0px 0px ×56 / 22.3px 0px 0px ×31 … |
| Mathematics | `p` | margin-top | 831 | 0px ×142 / 3.52px ×47 / 12.29px ×43 … | -5.72px ×57 / -5px ×56 / 0px ×45 … |
| Mathematics | `p` | max-width | 831 | none ×359 / 860px ×3 | none ×362 |
| Mathematics | `p` | padding-left | 831 | 0px ×356 / 11px ×5 / 31px ×1 | 0px ×362 |
| Mathematics | `p` | text-indent | 831 | 0px ×362 | 0px ×355 / 48px ×7 |
| Mathematics | `p` | text-wrap | 831 | wrap ×339 / nowrap ×20 / balance ×3 | wrap ×342 / nowrap ×20 |
| Mathematics | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×224 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×222 |
| Mathematics | `span` | border-radius | 831 | 0px ×224 | 0px ×222 |
| Mathematics | `span` | color | 831 | rgb(43, 43, 43) ×192 / rgb(4, 50, 255) ×17 / rgb(0, 176, 80) ×3 … | rgb(43, 43, 43) ×197 / rgb(4, 50, 255) ×16 / rgb(255, 255, 255) ×3 … |
| Mathematics | `span` | display | 831 | block ×192 / inline ×28 / inline-block ×4 | inline ×133 / block ×85 / inline-block ×4 |
| Mathematics | `span` | flex | 831 | 0 1 auto ×224 | 0 1 auto ×222 |
| Mathematics | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×223 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×221 / Vollkorn, Georgia, serif ×1 |
| Mathematics | `span` | font-size | 831 | 18px ×136 / 17px ×81 / 13px ×3 … | 18px ×218 / 14px ×2 / 40px ×1 … |
| Mathematics | `span` | font-weight | 831 | 400 ×223 / 500 ×1 | 400 ×221 / 500 ×1 |
| Mathematics | `span` | line-height | 831 | 37.2px ×136 / 22.1px ×81 / 16.25px ×3 … | 29.7px ×136 / 23.4px ×81 / 16.8px ×2 … |
| Mathematics | `span` | margin-left | 831 | 0px ×220 / 104.878px ×1 / 15.9807px ×1 … | 0px ×218 / 1.54912px ×1 / 17.503px ×1 … |
| Mathematics | `span` | min-width | 831 | 0px ×117 / auto ×107 | 0px ×219 / auto ×3 |
| Mathematics | `span` | padding | 831 | 0px ×143 / 7px 0px ×81 | 0px ×141 / 7px 0px ×81 |
| Mathematics | `span` | text-align | 831 | justify ×136 / left ×81 / start ×4 … | justify ×136 / left ×81 / start ×4 … |
| Mathematics | `ul` | list-style | 831 | outside none none ×42 | outside none none ×41 |
| Mathematics | `ul` | margin | 831 | 0px ×33 / 24px 0px 0px ×8 / 16.29px 0px 0px ×1 | 0px ×32 / 24px 0px 0px ×8 / 4.8px 0px 0px ×1 |
| Mathematics | `ul` | margin-left | 831 | 0px ×42 | 0px ×41 |
| Mathematics | `ul` | padding | 831 | 0px ×37 / 0px 0px 0px 62px ×2 / 0px 0px 0px 93px ×2 … | 0px ×36 / 0px 0px 0px 93px ×2 / 0px 0px 0px 48px ×2 … |
| Mathematics | `ul` | padding-left | 831 | 0px ×37 / 62px ×2 / 93px ×2 … | 0px ×36 / 93px ×2 / 48px ×2 … |
| Mathematics | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Mathematics | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Mathematics | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Mathematics | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Mathematics | `.mc-band` | color | 1440 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Mathematics | `.mc-band` | margin-top | 1440 | -43.05px ×1 | -14.7px ×1 |
| Mathematics | `.micro-label` | border-top | 1440 | 0px none rgb(43, 43, 43) ×52 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … | 0px none rgb(43, 43, 43) ×53 / 2px solid rgb(217, 201, 171) ×2 / 0px none rgb(0, 176, 80) ×1 … |
| Mathematics | `.micro-label` | line-height | 1440 | 29.7px ×56 / 33px ×1 | 29.7px ×57 |
| Mathematics | `.micro-label` | margin | 1440 | 27.82px 0px 0px ×25 / 16.29px 0px 0px ×11 / 2px 0px 0px ×7 … | 22.3px 0px 0px ×27 / 32.8px 0px 0px ×5 / 33.3px 0px 0px ×4 … |
| Mathematics | `.micro-label` | margin-bottom | 1440 | 0px ×57 | 0px ×55 / -3.7px ×1 / -2.7px ×1 |
| Mathematics | `.micro-label` | margin-top | 1440 | 27.82px ×25 / 16.29px ×11 / 2px ×7 … | 22.3px ×27 / 32.8px ×5 / 33.3px ×4 … |
| Mathematics | `.mm-area` | border-bottom | 1440 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `.mm-area` | padding-bottom | 1440 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `.mm-cabar` | margin | 1440 | 13px 0px 0px 121.4px ×1 | 9px 0px 0px ×1 |
| Mathematics | `.mm-cap` | line-height | 1440 | 20.8px ×22 | 29.7px ×22 |
| Mathematics | `.mm-cap` | padding-top | 1440 | 0px ×22 | 2px ×22 |
| Mathematics | `.mm-cap-below` | padding-top | 1440 | 0px ×2 | 2px ×2 |
| Mathematics | `.mm-cols3` | margin | 1440 | 27.82px 0px 0px ×1 / 23.82px 0px 0px ×1 | 14px 0px 0px ×2 |
| Mathematics | `.mm-flow` | margin-left | 1440 | 25px ×78 / 0px ×54 / 80px ×4 … | 25px ×80 / 0px ×55 / 80px ×4 … |
| Mathematics | `.mm-g2` | column-gap | 1440 | 20px ×1 | 40px ×1 |
| Mathematics | `.mm-g2` | margin | 1440 | -3.9px 0px 0px ×1 | 6.35px 0px 0px ×1 |
| Mathematics | `.mm-imgs` | margin | 1440 | 0px ×37 / 70.22px 0px 0px ×4 / 0px 0px 0px 118.985px ×2 … | 0px ×37 / 27.98px 0px 0px ×4 / 0px 0px 0px 118.985px ×2 … |
| Mathematics | `.mm-lineabove` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×2 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 / rgba(0, 0, 0, 0) linear-gradient(rgb(217 ×1 |
| Mathematics | `.mm-lineabove` | padding-top | 1440 | 38.8px ×2 / 28px ×2 | 28px ×2 / 28.55px ×1 / 34.3px ×1 |
| Mathematics | `.mm-name` | border-top | 1440 | 0px none rgb(4, 50, 255) ×24 / 2px solid rgb(217, 201, 171) ×23 | 0px none rgb(4, 50, 255) ×47 |
| Mathematics | `.mm-name` | margin-top | 1440 | 26.32px ×11 / 23px ×7 / 0px ×6 … | 39.86px ×8 / 0px ×7 / 51.25px ×6 … |
| Mathematics | `.mm-name` | padding-top | 1440 | 28px ×47 | 0px ×47 |
| Mathematics | `.mm-pdf` | margin | 1440 | 0px ×25 / 0px 18.3084px 0px 24px ×5 / 0px 0px 0px 24px ×4 … | 0px 0px 0px 24px ×32 / 0px ×25 |
| Mathematics | `.mm-pdf-r` | margin-right | 1440 | 18.3084px ×5 / 0px ×4 / 12.198px ×2 … | 0px ×32 |
| Mathematics | `.mm-pdff` | margin | 1440 | 0px 0px 0px 25px ×78 / 0px ×56 / 0px 0px 0px 80px ×4 … | 0px 0px 0px 25px ×80 / 0px ×57 / 0px 0px 0px 80px ×4 … |
| Mathematics | `.mm-pdff` | margin-left | 1440 | 25px ×78 / 0px ×56 / 80px ×4 … | 25px ×80 / 0px ×57 / 80px ×4 … |
| Mathematics | `.mm-tabcol` | display | 1440 | grid ×44 | block ×44 |
| Mathematics | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Mathematics | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Mathematics | `.ph` | margin | 1440 | 0px 0px 0px 25px ×78 / 0px ×60 / 0px 0px 0px 80px ×4 … | 0px 0px 0px 25px ×80 / 0px ×61 / 0px 0px 0px 80px ×4 … |
| Mathematics | `.pullquote` | margin | 1440 | 0px 20px ×4 / 11.29px 20px 0px ×1 / 9.48px 20px 0px ×1 | 23.3px 0px 0px ×2 / 20.79px 0px 0px ×1 / 18px 0px 23px ×1 … |
| Mathematics | `.pullquote` | margin-bottom | 1440 | 0px ×6 | 0px ×3 / 23px ×2 / 24.5px ×1 |
| Mathematics | `.pullquote` | margin-left | 1440 | 20px ×6 | 0px ×6 |
| Mathematics | `.pullquote` | margin-right | 1440 | 20px ×6 | 0px ×6 |
| Mathematics | `.pullquote` | margin-top | 1440 | 0px ×4 / 11.29px ×1 / 9.48px ×1 | 23.3px ×2 / 0px ×2 / 20.79px ×1 … |
| Mathematics | `.pullquote` | padding | 1440 | 0px ×2 / 24px 0px 0px ×2 / 11.29px 0px 0px ×1 … | 0px ×4 / 18.75px 0px 0px ×2 |
| Mathematics | `.pullquote` | padding-left | 1440 | 0px ×5 / 73px ×1 | 0px ×6 |
| Mathematics | `.section` | margin-top | 1440 | 0px ×28 | 0px ×27 / 17.95px ×1 |
| Mathematics | `.site-foot-in` | padding | 1440 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Mathematics | `.site-foot-in` | padding-bottom | 1440 | 48px ×1 | 17.625px ×1 |
| Mathematics | `.site-foot-in` | padding-top | 1440 | 32px ×1 | 17.625px ×1 |
| Mathematics | `.toc-label` | font-size | 1440 | 22px ×1 | 20px ×1 |
| Mathematics | `.toc-label` | line-height | 1440 | 36.3px ×1 | 33px ×1 |
| Mathematics | `.toc-wrap` | padding | 1440 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Mathematics | `.toc-wrap` | padding-bottom | 1440 | 36px ×1 | 0px ×1 |
| Mathematics | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Mathematics | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Mathematics | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Mathematics | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Mathematics | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Mathematics | `a` | align-items | 1440 | normal ×99 | baseline ×55 / normal ×44 |
| Mathematics | `a` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×62 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×8 … | 1px solid rgba(0, 0, 0, 0) ×55 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 … |
| Mathematics | `a` | border-bottom-color | 1440 | rgba(0, 0, 0, 0) ×62 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×8 … | rgba(0, 0, 0, 0) ×55 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Mathematics | `a` | color | 1440 | rgb(74, 85, 96) ×48 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … | rgb(74, 85, 96) ×55 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Mathematics | `a` | display | 1440 | inline ×55 / block ×44 | flex ×55 / block ×44 |
| Mathematics | `a` | font-size | 1440 | 19px ×55 / 17px ×41 / 18px ×1 … | 18px ×97 / 25px ×1 / 15px ×1 |
| Mathematics | `a` | gap | 1440 | normal ×99 | 8px ×55 / normal ×44 |
| Mathematics | `a` | line-height | 1440 | 25.65px ×55 / 22.1px ×33 / 28.05px ×8 … | 24.3px ×55 / 23.4px ×33 / 29.7px ×9 … |
| Mathematics | `a` | outline | 1440 | rgb(74, 85, 96) none 3px ×48 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … | rgb(74, 85, 96) none 3px ×55 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Mathematics | `a` | padding | 1440 | 0px ×58 / 8px 0px ×33 / 6px 0px ×8 | 0px ×58 / 8px 0px ×33 / 6px 0px 7.5px ×8 |
| Mathematics | `a` | text-decoration | 1440 | none ×96 / underline ×3 | none ×95 / underline ×4 |
| Mathematics | `a` | text-underline-offset | 1440 | auto ×98 / 3px ×1 | auto ×97 / 4px ×1 / 3px ×1 |
| Mathematics | `cite` | margin-top | 1440 | -2.8px ×2 / 9.48px ×1 | 0px ×3 |
| Mathematics | `cite` | padding-left | 1440 | 11px ×2 / 73px ×1 | 48px ×3 |
| Mathematics | `div` | break-inside | 1440 | auto ×433 | auto ×435 |
| Mathematics | `div` | color | 1440 | rgb(43, 43, 43) ×427 / rgb(0, 176, 80) ×1 / rgb(237, 125, 49) ×1 … | rgb(43, 43, 43) ×430 / rgb(0, 176, 80) ×1 / rgb(112, 48, 160) ×1 … |
| Mathematics | `div` | font-size | 1440 | 18px ×429 / 15px ×2 / 14px ×1 … | 18px ×431 / 15px ×2 / 14px ×1 … |
| Mathematics | `div` | font-style | 1440 | normal ×433 | normal ×435 |
| Mathematics | `div` | margin | 1440 | 0px ×302 / 27.82px 0px 0px ×26 / 16.29px 0px 0px ×11 … | 0px ×305 / 0px 0px 0px 24px ×32 / 22.3px 0px 0px ×27 … |
| Mathematics | `div` | padding | 1440 | 0px ×393 / 22.8px 0px 0px ×11 / 26px 40px 30px ×8 … | 0px ×395 / 44.55px 0px 0px ×12 / 26px 40px 30px ×8 … |
| Mathematics | `figure` | margin-left | 1440 | 25px ×78 / 0px ×60 / 80px ×4 … | 25px ×80 / 0px ×61 / 80px ×4 … |
| Mathematics | `h2` | border-bottom | 1440 | 2px solid rgb(238, 0, 0) ×7 / 0px none rgb(43, 43, 43) ×5 | 2px solid rgb(238, 0, 0) ×7 / 2px solid rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | border-bottom-color | 1440 | rgb(238, 0, 0) ×7 / rgb(43, 43, 43) ×5 | rgb(238, 0, 0) ×7 / rgb(4, 50, 255) ×5 |
| Mathematics | `h2` | font-size | 1440 | 22px ×7 / 20px ×5 | 18px ×12 |
| Mathematics | `h2` | line-height | 1440 | 26.4px ×7 / 24px ×5 | 21.6px ×12 |
| Mathematics | `h2` | margin | 1440 | 0px ×12 | 0px 0px -9.59px ×11 / 0px ×1 |
| Mathematics | `h2` | margin-bottom | 1440 | 0px ×12 | -9.59px ×11 / 0px ×1 |
| Mathematics | `h2` | padding-bottom | 1440 | 8px ×7 / 0px ×5 | 8px ×12 |
| Mathematics | `li` | margin | 1440 | 0px ×122 / 7.52px 0px 0px ×59 / 0px 0px 10px ×51 … | 0px ×123 / 0px 0px 10px ×54 / -5px 0px 0px ×51 … |
| Mathematics | `li` | margin-bottom | 1440 | 0px ×196 / 10px ×55 / 8px ×9 | 0px ×197 / 10px ×54 / 8px ×9 |
| Mathematics | `li` | margin-top | 1440 | 0px ×174 / 7.52px ×59 / 19.79px ×9 … | 0px ×178 / -5px ×51 / -5.72px ×10 … |
| Mathematics | `li` | padding-left | 1440 | 0px ×199 / 31px ×61 | 0px ×199 / 36.78px ×61 |
| Mathematics | `li` | text-align | 1440 | left ×177 / justify ×83 | justify ×138 / left ×122 |
| Mathematics | `li::before` | text-align | 1440 | left ×177 / justify ×83 | justify ×138 / left ×122 |
| Mathematics | `ol` | margin | 1440 | 0px ×11 | 0px ×6 / 28.02px 0px 0px ×3 / 27.8px 0px 0px ×2 |
| Mathematics | `p` | font-size | 1440 | 18px ×292 / 20px ×47 / 16px ×22 … | 18px ×292 / 20px ×48 / 16px ×22 |
| Mathematics | `p` | line-height | 1440 | 37.2px ×327 / 20.8px ×22 / 40px ×12 … | 29.7px ×349 / 40px ×12 / 33px ×1 |
| Mathematics | `p` | margin | 1440 | 0px ×118 / 3.52px 0px 0px ×48 / 12.29px 0px 0px ×45 … | -5px 0px 0px ×62 / -5.72px 0px 0px ×55 / 4.8px 0px 0px ×32 … |
| Mathematics | `p` | margin-left | 1440 | 0px ×359 / 250px ×3 | 0px ×362 |
| Mathematics | `p` | margin-top | 1440 | 0px ×142 / 3.52px ×48 / 12.29px ×45 … | -5px ×62 / -5.72px ×55 / 0px ×45 … |
| Mathematics | `p` | max-width | 1440 | none ×359 / 860px ×3 | none ×362 |
| Mathematics | `p` | padding-left | 1440 | 0px ×356 / 11px ×5 / 31px ×1 | 0px ×362 |
| Mathematics | `p` | text-indent | 1440 | 0px ×362 | 0px ×355 / 48px ×7 |
| Mathematics | `p` | text-wrap | 1440 | wrap ×339 / nowrap ×20 / balance ×3 | wrap ×342 / nowrap ×20 |
| Mathematics | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×224 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×222 |
| Mathematics | `span` | border-radius | 1440 | 0px ×224 | 0px ×222 |
| Mathematics | `span` | color | 1440 | rgb(43, 43, 43) ×192 / rgb(4, 50, 255) ×17 / rgb(0, 176, 80) ×3 … | rgb(43, 43, 43) ×197 / rgb(4, 50, 255) ×16 / rgb(255, 255, 255) ×3 … |
| Mathematics | `span` | display | 1440 | block ×192 / inline ×28 / inline-block ×4 | inline ×133 / block ×85 / inline-block ×4 |
| Mathematics | `span` | flex | 1440 | 0 1 auto ×224 | 0 1 auto ×222 |
| Mathematics | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×223 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×221 / Vollkorn, Georgia, serif ×1 |
| Mathematics | `span` | font-size | 1440 | 18px ×136 / 17px ×81 / 13px ×3 … | 18px ×218 / 14px ×2 / 40px ×1 … |
| Mathematics | `span` | font-weight | 1440 | 400 ×223 / 500 ×1 | 400 ×221 / 500 ×1 |
| Mathematics | `span` | line-height | 1440 | 37.2px ×136 / 22.1px ×81 / 16.25px ×3 … | 29.7px ×136 / 23.4px ×81 / 16.8px ×2 … |
| Mathematics | `span` | margin-left | 1440 | 0px ×220 / 78.4254px ×1 / 71.0261px ×1 … | 0px ×218 / 78.4254px ×1 / 71.0261px ×1 … |
| Mathematics | `span` | min-width | 1440 | 0px ×117 / auto ×107 | 0px ×219 / auto ×3 |
| Mathematics | `span` | padding | 1440 | 0px ×143 / 8px 0px ×81 | 0px ×141 / 8px 0px ×81 |
| Mathematics | `span` | text-align | 1440 | justify ×136 / left ×81 / start ×4 … | justify ×136 / left ×81 / start ×4 … |
| Mathematics | `ul` | list-style | 1440 | outside none none ×42 | outside none none ×41 |
| Mathematics | `ul` | margin | 1440 | 0px ×41 / 16.29px 0px 0px ×1 | 0px ×40 / 4.8px 0px 0px ×1 |
| Mathematics | `ul` | margin-left | 1440 | 0px ×42 | 0px ×41 |
| Mathematics | `ul` | padding | 1440 | 0px ×37 / 0px 0px 0px 62px ×2 / 0px 0px 0px 93px ×2 … | 0px ×36 / 0px 0px 0px 93px ×2 / 0px 0px 0px 48px ×2 … |
| Mathematics | `ul` | padding-left | 1440 | 0px ×37 / 62px ×2 / 93px ×2 … | 0px ×36 / 93px ×2 / 48px ×2 … |
| Practical Life | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Practical Life | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Practical Life | `.article` | padding | 390 | 0px 24px ×1 | 0px 24px 56px ×1 |
| Practical Life | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Practical Life | `.mc-band` | margin-top | 390 | 26px ×1 | -22.08px ×1 |
| Practical Life | `.micro-label` | line-height | 390 | 36px ×46 | 28.05px ×46 |
| Practical Life | `.micro-label` | margin | 390 | 16px 0px 0px ×22 / 33px 0px 0px ×11 / 13px 0px 0px ×8 … | 23.95px 0px 0px ×22 / 32px 0px 0px ×11 / 24.95px 0px 0px ×6 … |
| Practical Life | `.micro-label` | margin-top | 390 | 16px ×22 / 33px ×11 / 13px ×8 … | 23.95px ×22 / 32px ×11 / 24.95px ×6 … |
| Practical Life | `.mm-flow` | margin-left | 390 | 0px ×163 | 0px ×140 / 25px ×15 / 25.1197px ×2 … |
| Practical Life | `.mm-gl` | background | 390 | rgb(217, 201, 171) none repeat scroll 0% ×39 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×26 / rgb(217, 201, 171) none repeat scroll 0% ×13 |
| Practical Life | `.mm-gl` | background-clip | 390 | content-box ×39 | border-box ×26 / content-box ×13 |
| Practical Life | `.mm-gl` | display | 390 | block ×39 | flow-root ×39 |
| Practical Life | `.mm-gl` | font-size | 390 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-gl` | line-height | 390 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-name` | margin-top | 390 | 25px ×16 / 16px ×1 | 29px ×13 / 64.75px ×3 / 16.25px ×1 |
| Practical Life | `.mm-pdf-r` | padding-top | 390 | 25px ×11 / 9px ×7 / 27px ×3 | 12.97px ×11 / 12.47px ×4 / 14.72px ×2 … |
| Practical Life | `.mm-pdff` | margin | 390 | 0px ×163 | 0px ×140 / 0px 0px 0px 25px ×15 / 0px 0px 0px 25.1197px ×2 … |
| Practical Life | `.mm-pdff` | margin-left | 390 | 0px ×163 | 0px ×140 / 25px ×15 / 25.1197px ×2 … |
| Practical Life | `.mm-table-wrap` | margin | 390 | 0px 0px -33.05px ×1 | -16.22px 0px -19.05px ×1 |
| Practical Life | `.mm-tocline` | margin | 390 | -9.05px 0px 25px ×1 | -7.94px 0px 29px ×1 |
| Practical Life | `.ph` | margin | 390 | 0px ×163 | 0px ×140 / 0px 0px 0px 25px ×15 / 0px 0px 0px 25.1197px ×2 … |
| Practical Life | `.ph` | scroll-snap-align | 390 | start ×163 | center ×163 |
| Practical Life | `.pullquote` | margin | 390 | 0px 0px -8px ×14 / 10px 0px 0px ×1 | 0px 0px -8px ×12 / 19.45px 0px 0px ×1 / 18.95px 0px 24px ×1 … |
| Practical Life | `.pullquote` | margin-bottom | 390 | -8px ×14 / 0px ×1 | -8px ×12 / 0px ×2 / 24px ×1 |
| Practical Life | `.pullquote` | margin-top | 390 | 0px ×14 / 10px ×1 | 0px ×12 / 18.95px ×2 / 19.45px ×1 |
| Practical Life | `.pullquote` | padding | 390 | 22px 0px 0px ×12 / 10px 0px 0px ×2 / 0px ×1 | 17.25px 0px 0px ×10 / 0px ×3 / 17px 0px 0px ×2 |
| Practical Life | `.site-foot-in` | padding | 390 | 28px 24px 40px ×1 | 14px 24px ×1 |
| Practical Life | `.site-foot-in` | padding-bottom | 390 | 40px ×1 | 14px ×1 |
| Practical Life | `.site-foot-in` | padding-top | 390 | 28px ×1 | 14px ×1 |
| Practical Life | `.toc-label` | font-size | 390 | 20px ×1 | 19px ×1 |
| Practical Life | `.toc-label` | line-height | 390 | 33px ×1 | 31.35px ×1 |
| Practical Life | `.toc-wrap` | padding | 390 | 22px 24px 26px ×1 | 22px 24px 0px ×1 |
| Practical Life | `.toc-wrap` | padding-bottom | 390 | 26px ×1 | 0px ×1 |
| Practical Life | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Practical Life | `a` | align-items | 390 | normal ×61 | normal ×47 / baseline ×13 |
| Practical Life | `a` | border-bottom | 390 | 0px none rgb(231, 238, 245) ×25 / 1px solid rgba(0, 0, 0, 0) ×13 / 0px none rgb(255, 255, 255) ×9 … | 0px none rgb(231, 238, 245) ×25 / 1px solid rgba(0, 0, 0, 0) ×13 / 0px none rgb(255, 255, 255) ×9 … |
| Practical Life | `a` | border-bottom-color | 390 | rgb(231, 238, 245) ×25 / rgba(0, 0, 0, 0) ×13 / rgb(255, 255, 255) ×9 … | rgb(231, 238, 245) ×25 / rgba(0, 0, 0, 0) ×13 / rgb(255, 255, 255) ×9 … |
| Practical Life | `a` | color | 390 | rgb(231, 238, 245) ×25 / rgb(74, 85, 96) ×13 / rgb(255, 255, 255) ×9 … | rgb(231, 238, 245) ×25 / rgb(74, 85, 96) ×13 / rgb(255, 255, 255) ×9 … |
| Practical Life | `a` | display | 390 | block ×44 / inline ×17 | block ×44 / flex ×13 / inline ×3 |
| Practical Life | `a` | font-family | 390 | "EB Garamond", Georgia, serif ×60 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×59 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `a` | font-size | 390 | 17px ×38 / 18px ×21 / 21px ×1 … | 17px ×58 / 21px ×1 / 15px ×1 |
| Practical Life | `a` | font-style | 390 | normal ×60 / italic ×1 | normal ×60 |
| Practical Life | `a` | font-weight | 390 | 400 ×60 / 500 ×1 | 400 ×59 / 500 ×1 |
| Practical Life | `a` | gap | 390 | normal ×61 | normal ×47 / 8px ×13 |
| Practical Life | `a` | line-height | 390 | 22.1px ×33 / 24.3px ×13 / 29.7px ×8 … | 22.1px ×33 / 22.95px ×13 / 28.05px ×10 … |
| Practical Life | `a` | margin-left | 390 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | outline | 390 | rgb(231, 238, 245) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(255, 255, 255) none 3px ×9 … | rgb(231, 238, 245) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(255, 255, 255) none 3px ×9 … |
| Practical Life | `a` | outline-offset | 390 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | overflow-wrap | 390 | normal ×61 | normal ×60 |
| Practical Life | `a` | padding | 390 | 7px 0px ×33 / 0px ×20 / 13px 0px ×8 | 7px 0px ×33 / 0px ×19 / 13px 0px ×8 |
| Practical Life | `a` | text-decoration | 390 | none ×53 / underline ×8 | none ×53 / underline ×7 |
| Practical Life | `a` | text-underline-offset | 390 | auto ×59 / 4px ×1 / 3px ×1 | auto ×58 / 4px ×1 / 3px ×1 |
| Practical Life | `cite` | padding-left | 390 | 59px ×14 | 48px ×14 |
| Practical Life | `div` | break-inside | 390 | auto ×348 | auto ×350 |
| Practical Life | `div` | color | 390 | rgb(43, 43, 43) ×346 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 | rgb(43, 43, 43) ×348 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Practical Life | `div` | font-size | 390 | 17px ×346 / 15px ×2 | 17px ×348 / 15px ×2 |
| Practical Life | `div` | font-style | 390 | normal ×348 | normal ×350 |
| Practical Life | `div` | margin | 390 | 0px ×277 / 16px 0px 0px ×22 / 24px 0px 0px ×15 … | 0px ×278 / 23.95px 0px 0px ×22 / 24px 0px 0px ×15 … |
| Practical Life | `div` | padding | 390 | 0px ×291 / 33px 0px 0px ×16 / 25px 0px 0px ×13 … | 0px ×292 / 12.97px 0px 0px ×24 / 0px 0px 10px 14px ×8 … |
| Practical Life | `figure` | margin-left | 390 | 0px ×163 | 0px ×140 / 25px ×15 / 25.1197px ×2 … |
| Practical Life | `li` | line-height | 390 | 28.05px ×135 / 36px ×18 | 28.05px ×153 |
| Practical Life | `li` | margin | 390 | 0px ×129 / 0px 0px 10px ×13 / 6px 0px 0px ×9 … | 0px ×129 / 0px 0px 10px ×12 / 8px 0px 0px ×12 |
| Practical Life | `li` | margin-bottom | 390 | 0px ×140 / 10px ×13 | 0px ×141 / 10px ×12 |
| Practical Life | `li` | margin-top | 390 | 0px ×142 / 6px ×9 / 16px ×2 | 0px ×141 / 8px ×12 |
| Practical Life | `li` | padding-left | 390 | 0px ×142 / 31px ×11 | 0px ×142 / 36.07px ×11 |
| Practical Life | `li` | text-align | 390 | left ×153 | left ×140 / justify ×13 |
| Practical Life | `li::before` | text-align | 390 | left ×153 | left ×140 / justify ×13 |
| Practical Life | `ol` | margin | 390 | 0px ×2 / 2px 0px -7px ×1 | 0px ×2 / 11.95px 0px 0px ×1 |
| Practical Life | `p` | font-size | 390 | 17px ×166 / 2px ×39 / 20px ×18 | 17px ×166 / 0px ×26 / 20px ×17 … |
| Practical Life | `p` | line-height | 390 | 36px ×165 / 2px ×39 / 38px ×18 … | 28.05px ×165 / 0px ×26 / 38px ×18 … |
| Practical Life | `p` | margin | 390 | 0px ×143 / 23px 0px 0px ×20 / 30px 0px 0px ×20 … | 14px 0px 0px ×92 / 23.95px 0px 0px ×36 / 0px ×18 … |
| Practical Life | `p` | margin-top | 390 | 0px ×144 / 23px ×20 / 30px ×20 … | 14px ×92 / 23.95px ×36 / 0px ×19 … |
| Practical Life | `p` | max-width | 390 | none ×220 / 860px ×3 | none ×223 |
| Practical Life | `p` | padding-left | 390 | 0px ×208 / 11px ×15 | 0px ×223 |
| Practical Life | `p` | text-wrap | 390 | wrap ×220 / balance ×3 | wrap ×223 |
| Practical Life | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×86 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×87 |
| Practical Life | `span` | border-radius | 390 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | color | 390 | rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 / rgb(255, 255, 255) ×4 … | rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 / rgb(255, 255, 255) ×5 … |
| Practical Life | `span` | display | 390 | block ×83 / inline ×3 | block ×83 / inline ×4 |
| Practical Life | `span` | flex | 390 | 0 1 auto ×86 | 0 1 auto ×87 |
| Practical Life | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×85 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×86 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `span` | font-size | 390 | 17px ×84 / 28px ×1 / 15px ×1 | 17px ×85 / 28px ×1 / 15px ×1 |
| Practical Life | `span` | font-weight | 390 | 400 ×85 / 500 ×1 | 400 ×86 / 500 ×1 |
| Practical Life | `span` | line-height | 390 | 22.1px ×81 / 36px ×2 / 33.6px ×1 … | 22.1px ×81 / 28.05px ×2 / 38px ×2 … |
| Practical Life | `span` | margin-left | 390 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | min-width | 390 | 0px ×85 / auto ×1 | 0px ×86 / auto ×1 |
| Practical Life | `span` | padding | 390 | 7px 0px ×81 / 0px ×5 | 7px 0px ×81 / 0px ×6 |
| Practical Life | `span` | text-align | 390 | left ×84 / start ×2 | left ×84 / start ×2 / center ×1 |
| Practical Life | `td` | border | 390 | 0px none rgb(43, 43, 43) ×32 |  ×28 / 0px none rgb(43, 43, 43) ×4 |
| Practical Life | `td` | border-bottom | 390 | 0px none rgb(43, 43, 43) ×32 | 1px solid rgb(230, 230, 228) ×28 / 0px none rgb(43, 43, 43) ×4 |
| Practical Life | `td` | padding | 390 | 0px ×32 | 16px 24px 16px 0px ×24 / 16px 0px ×8 |
| Practical Life | `td` | padding-right | 390 | 0px ×32 | 24px ×24 / 0px ×8 |
| Practical Life | `td` | padding-top | 390 | 0px ×32 | 16px ×32 |
| Practical Life | `th` | font-weight | 390 | 400 ×4 | 700 ×4 |
| Practical Life | `th` | padding | 390 | 0px ×4 | 16px 24px 16px 0px ×3 / 16px 0px ×1 |
| Practical Life | `th` | padding-right | 390 | 0px ×4 | 24px ×3 / 0px ×1 |
| Practical Life | `ul` | padding | 390 | 0px ×36 / 0px 0px 0px 31px ×1 | 0px ×36 / 0px 0px 0px 48px ×1 |
| Practical Life | `ul` | padding-left | 390 | 0px ×36 / 31px ×1 | 0px ×36 / 48px ×1 |
| Practical Life | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Practical Life | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Practical Life | `.article` | padding | 831 | 0px 40px ×1 | 0px 40px 72px ×1 |
| Practical Life | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Practical Life | `.mc-band` | margin-top | 831 | 25.7px ×1 | -14.72px ×1 |
| Practical Life | `.micro-label` | line-height | 831 | 37.2px ×46 | 29.7px ×46 |
| Practical Life | `.micro-label` | margin | 831 | 15.8px 0px 0px ×22 / 33px 0px 0px ×11 / 11.8px 0px 0px ×8 … | 23.3px 0px 0px ×21 / 31.75px 0px 0px ×11 / 19.3px 0px 0px ×5 … |
| Practical Life | `.micro-label` | margin-top | 831 | 15.8px ×22 / 33px ×11 / 11.8px ×8 … | 23.3px ×21 / 31.75px ×11 / 19.3px ×5 … |
| Practical Life | `.mm-flow` | margin-left | 831 | 25px ×105 / 0px ×44 / 32.0982px ×4 … | 25px ×101 / 0px ×52 / 25.3453px ×2 … |
| Practical Life | `.mm-gl` | background | 831 | rgb(217, 201, 171) none repeat scroll 0% ×39 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×26 / rgb(217, 201, 171) none repeat scroll 0% ×13 |
| Practical Life | `.mm-gl` | background-clip | 831 | content-box ×39 | border-box ×26 / content-box ×13 |
| Practical Life | `.mm-gl` | display | 831 | block ×39 | flow-root ×39 |
| Practical Life | `.mm-gl` | font-size | 831 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-gl` | line-height | 831 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-gl` | text-align | 831 | justify ×39 | start ×39 |
| Practical Life | `.mm-name` | margin-top | 831 | 25px ×16 / 16px ×1 | 23px ×16 / 16.25px ×1 |
| Practical Life | `.mm-pdf` | margin | 831 | 0px ×23 / 0px 0px 0px 24px ×5 / 0px 84.4049px 0px 24px ×2 … | 0px ×23 / 0px 0px 0px 24px ×21 |
| Practical Life | `.mm-pdf-r` | margin-right | 831 | 0px ×5 / 84.4049px ×2 / 136.652px ×2 … | 0px ×21 |
| Practical Life | `.mm-pdff` | margin | 831 | 0px 0px 0px 25px ×105 / 0px ×44 / 0px 0px 0px 32.0982px ×4 … | 0px 0px 0px 25px ×101 / 0px ×52 / 0px 0px 0px 25.3453px ×2 … |
| Practical Life | `.mm-pdff` | margin-left | 831 | 25px ×105 / 0px ×44 / 32.0982px ×4 … | 25px ×101 / 0px ×52 / 25.3453px ×2 … |
| Practical Life | `.mm-ph1` | margin-top | 831 | 3px ×13 / 3.01px ×1 | 3px ×14 |
| Practical Life | `.mm-ph11` | margin-top | 831 | 10.8px ×5 | 18.3px ×5 |
| Practical Life | `.mm-table-wrap` | margin | 831 | 0px 0px -19.69px ×1 | -27.5px 0px -19.69px ×1 |
| Practical Life | `.mm-tocline` | margin | 831 | -18.69px 0px 25px ×1 | -15.3px 0px 29px ×1 |
| Practical Life | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Practical Life | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Practical Life | `.ph` | margin | 831 | 0px 0px 0px 25px ×105 / 0px ×44 / 0px 0px 0px 32.0982px ×4 … | 0px 0px 0px 25px ×101 / 0px ×52 / 0px 0px 0px 25.3453px ×2 … |
| Practical Life | `.pullquote` | margin | 831 | 0px 20px -9px ×12 / 0px 20px ×2 / -11.8px 20px 0px ×1 | 0px 0px -9px ×12 / -100.5px 0px 0px ×1 / 22.8px 0px 23px ×1 … |
| Practical Life | `.pullquote` | margin-bottom | 831 | -9px ×12 / 0px ×3 | -9px ×12 / 0px ×2 / 23px ×1 |
| Practical Life | `.pullquote` | margin-left | 831 | 20px ×15 | 0px ×15 |
| Practical Life | `.pullquote` | margin-right | 831 | 20px ×15 | 0px ×15 |
| Practical Life | `.pullquote` | margin-top | 831 | 0px ×14 / -11.8px ×1 | 0px ×12 / -100.5px ×1 / 22.8px ×1 … |
| Practical Life | `.pullquote` | padding | 831 | 22px 0px 0px ×12 / 0px ×3 | 16.75px 0px 0px ×12 / 0px ×3 |
| Practical Life | `.site-foot-in` | padding | 831 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Practical Life | `.site-foot-in` | padding-bottom | 831 | 48px ×1 | 17.625px ×1 |
| Practical Life | `.site-foot-in` | padding-top | 831 | 32px ×1 | 17.625px ×1 |
| Practical Life | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Practical Life | `.toc-label` | font-size | 831 | 22px ×1 | 20px ×1 |
| Practical Life | `.toc-label` | line-height | 831 | 36.3px ×1 | 33px ×1 |
| Practical Life | `.toc-wrap` | padding | 831 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Practical Life | `.toc-wrap` | padding-bottom | 831 | 36px ×1 | 0px ×1 |
| Practical Life | `a` | align-items | 831 | normal ×61 | normal ×47 / baseline ×13 |
| Practical Life | `a` | border-bottom | 831 | 0px none rgb(43, 43, 43) ×25 / 1px solid rgba(0, 0, 0, 0) ×13 / 0px none rgb(4, 50, 255) ×11 … | 0px none rgb(43, 43, 43) ×25 / 1px solid rgba(0, 0, 0, 0) ×13 / 0px none rgb(4, 50, 255) ×10 … |
| Practical Life | `a` | border-bottom-color | 831 | rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×13 / rgb(4, 50, 255) ×11 … | rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×13 / rgb(4, 50, 255) ×10 … |
| Practical Life | `a` | color | 831 | rgb(43, 43, 43) ×25 / rgb(74, 85, 96) ×13 / rgb(4, 50, 255) ×11 … | rgb(43, 43, 43) ×25 / rgb(74, 85, 96) ×13 / rgb(4, 50, 255) ×10 … |
| Practical Life | `a` | display | 831 | block ×44 / inline ×17 | block ×44 / flex ×13 / inline ×3 |
| Practical Life | `a` | font-family | 831 | "EB Garamond", Georgia, serif ×60 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×59 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `a` | font-size | 831 | 17px ×33 / 18px ×13 / 19px ×13 … | 18px ×58 / 25px ×1 / 15px ×1 |
| Practical Life | `a` | font-style | 831 | normal ×60 / italic ×1 | normal ×60 |
| Practical Life | `a` | font-weight | 831 | 400 ×60 / 500 ×1 | 400 ×59 / 500 ×1 |
| Practical Life | `a` | gap | 831 | normal ×61 | normal ×47 / 8px ×13 |
| Practical Life | `a` | line-height | 831 | 22.1px ×33 / 25.65px ×13 / 29.7px ×9 … | 23.4px ×33 / 24.3px ×13 / 29.7px ×10 … |
| Practical Life | `a` | margin-left | 831 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | outline | 831 | rgb(43, 43, 43) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(4, 50, 255) none 3px ×11 … | rgb(43, 43, 43) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(4, 50, 255) none 3px ×10 … |
| Practical Life | `a` | outline-offset | 831 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | overflow-wrap | 831 | normal ×61 | normal ×60 |
| Practical Life | `a` | padding | 831 | 7px 0px ×33 / 0px ×20 / 13px 0px ×8 | 7px 0px ×33 / 0px ×19 / 13px 0px ×8 |
| Practical Life | `a` | text-decoration | 831 | none ×53 / underline ×8 | none ×53 / underline ×7 |
| Practical Life | `a` | text-underline-offset | 831 | auto ×59 / 4px ×1 / 3px ×1 | auto ×58 / 4px ×1 / 3px ×1 |
| Practical Life | `cite` | margin-top | 831 | 3px ×13 / 3.01px ×1 | 3px ×14 |
| Practical Life | `cite` | padding-left | 831 | 59px ×14 | 48px ×14 |
| Practical Life | `div` | break-inside | 831 | auto ×369 | auto ×371 |
| Practical Life | `div` | color | 831 | rgb(43, 43, 43) ×367 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 | rgb(43, 43, 43) ×369 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Practical Life | `div` | font-size | 831 | 18px ×367 / 15px ×2 | 18px ×369 / 15px ×2 |
| Practical Life | `div` | font-style | 831 | normal ×369 | normal ×371 |
| Practical Life | `div` | margin | 831 | 0px ×267 / 15.8px 0px 0px ×22 / 24px 0px 0px ×15 … | 0px ×273 / 0px 0px 0px 24px ×21 / 23.3px 0px 0px ×21 … |
| Practical Life | `div` | padding | 831 | 0px ×333 / 32.8px 0px 0px ×14 / 0px 0px 10px 14px ×8 … | 0px ×334 / 44.55px 0px 0px ×14 / 0px 0px 10px 14px ×8 … |
| Practical Life | `figure` | margin-left | 831 | 25px ×105 / 0px ×44 / 32.0982px ×4 … | 25px ×101 / 0px ×52 / 25.3453px ×2 … |
| Practical Life | `h1` | font-size | 831 | 35px ×1 | 40px ×1 |
| Practical Life | `h1` | line-height | 831 | 42px ×1 | 48px ×1 |
| Practical Life | `h1` | max-width | 831 | 880px ×1 | 760px ×1 |
| Practical Life | `li` | line-height | 831 | 29.7px ×135 / 37.2px ×18 | 29.7px ×153 |
| Practical Life | `li` | margin | 831 | 0px ×128 / 0px 0px 10px ×13 / 5.8px 0px 0px ×9 … | 0px ×129 / 0px 0px 10px ×12 / 13.3px 0px 0px ×8 … |
| Practical Life | `li` | margin-bottom | 831 | 0px ×140 / 10px ×13 | 0px ×141 / 10px ×12 |
| Practical Life | `li` | margin-top | 831 | 0px ×141 / 5.8px ×9 / 15.8px ×2 … | 0px ×141 / 13.3px ×8 / 7.3px ×1 … |
| Practical Life | `li` | padding-left | 831 | 0px ×142 / 31px ×11 | 0px ×142 / 36.78px ×11 |
| Practical Life | `li` | text-align | 831 | left ×135 / justify ×18 | left ×122 / justify ×31 |
| Practical Life | `li::before` | text-align | 831 | left ×135 / justify ×18 | left ×122 / justify ×31 |
| Practical Life | `ol` | margin | 831 | 0px ×2 / 1.8px 0px -7.2px ×1 | 0px ×2 / 11.3px 0px 0px ×1 |
| Practical Life | `p` | font-size | 831 | 18px ×166 / 2px ×39 / 20px ×17 … | 18px ×166 / 0px ×26 / 20px ×18 … |
| Practical Life | `p` | line-height | 831 | 37.2px ×165 / 2px ×39 / 40px ×18 … | 29.7px ×165 / 0px ×26 / 40px ×18 … |
| Practical Life | `p` | margin | 831 | 0px ×140 / 30px 0px 0px ×18 / 22.8px 0px 0px ×17 … | 7.3px 0px 0px ×94 / 23px 0px 0px ×16 / 7.28px 0px 0px ×16 … |
| Practical Life | `p` | margin-top | 831 | 0px ×141 / 30px ×18 / 22.8px ×17 … | 7.3px ×94 / 0px ×16 / 23px ×16 … |
| Practical Life | `p` | max-width | 831 | none ×220 / 860px ×3 | none ×223 |
| Practical Life | `p` | padding-left | 831 | 0px ×208 / 11px ×15 | 0px ×223 |
| Practical Life | `p` | text-align | 831 | justify ×204 / left ×15 / center ×3 … | justify ×165 / start ×40 / left ×15 … |
| Practical Life | `p` | text-wrap | 831 | wrap ×220 / balance ×3 | wrap ×223 |
| Practical Life | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×86 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×87 |
| Practical Life | `span` | border-radius | 831 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | color | 831 | rgb(43, 43, 43) ×73 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×73 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Practical Life | `span` | display | 831 | block ×83 / inline ×3 | block ×83 / inline ×4 |
| Practical Life | `span` | flex | 831 | 0 1 auto ×86 | 0 1 auto ×87 |
| Practical Life | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×85 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×86 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `span` | font-size | 831 | 17px ×81 / 18px ×3 / 35px ×1 … | 18px ×85 / 40px ×1 / 15px ×1 |
| Practical Life | `span` | font-weight | 831 | 400 ×85 / 500 ×1 | 400 ×86 / 500 ×1 |
| Practical Life | `span` | line-height | 831 | 22.1px ×81 / 37.2px ×2 / 42px ×1 … | 23.4px ×81 / 29.7px ×2 / 40px ×2 … |
| Practical Life | `span` | margin-left | 831 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | min-width | 831 | 0px ×85 / auto ×1 | 0px ×86 / auto ×1 |
| Practical Life | `span` | padding | 831 | 7px 0px ×81 / 0px ×5 | 7px 0px ×81 / 0px ×6 |
| Practical Life | `span` | text-align | 831 | left ×82 / start ×2 / justify ×2 | left ×82 / start ×2 / justify ×2 … |
| Practical Life | `th` | font-weight | 831 | 400 ×4 | 700 ×4 |
| Practical Life | `ul` | margin | 831 | 0px ×28 / 24px 0px 0px ×8 / 0px 0px 0px 25px ×1 | 0px ×29 / 24px 0px 0px ×8 |
| Practical Life | `ul` | margin-left | 831 | 0px ×36 / 25px ×1 | 0px ×37 |
| Practical Life | `ul` | padding | 831 | 0px ×36 / 0px 0px 0px 31px ×1 | 0px ×36 / 0px 0px 0px 48px ×1 |
| Practical Life | `ul` | padding-left | 831 | 0px ×36 / 31px ×1 | 0px ×36 / 48px ×1 |
| Practical Life | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Practical Life | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Practical Life | `.article` | padding | 1440 | 0px 40px ×1 | 0px 40px 72px ×1 |
| Practical Life | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Practical Life | `.mc-band` | margin-top | 1440 | 25.7px ×1 | -14.7px ×1 |
| Practical Life | `.micro-label` | line-height | 1440 | 37.2px ×46 | 29.7px ×46 |
| Practical Life | `.micro-label` | margin | 1440 | 15.8px 0px 0px ×22 / 33px 0px 0px ×11 / 11.8px 0px 0px ×8 … | 23.3px 0px 0px ×22 / 31.75px 0px 0px ×11 / 19.3px 0px 0px ×5 … |
| Practical Life | `.micro-label` | margin-top | 1440 | 15.8px ×22 / 33px ×11 / 11.8px ×8 … | 23.3px ×22 / 31.75px ×11 / 19.3px ×5 … |
| Practical Life | `.mm-flow` | margin-left | 1440 | 25px ×105 / 0px ×44 / 35.9032px ×4 … | 25px ×101 / 0px ×52 / 25.444px ×2 … |
| Practical Life | `.mm-gl` | background | 1440 | rgb(217, 201, 171) none repeat scroll 0% ×39 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×26 / rgb(217, 201, 171) none repeat scroll 0% ×13 |
| Practical Life | `.mm-gl` | background-clip | 1440 | content-box ×39 | border-box ×26 / content-box ×13 |
| Practical Life | `.mm-gl` | display | 1440 | block ×39 | flow-root ×39 |
| Practical Life | `.mm-gl` | font-size | 1440 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-gl` | line-height | 1440 | 2px ×39 | 0px ×26 / 2px ×13 |
| Practical Life | `.mm-gl` | text-align | 1440 | justify ×39 | start ×39 |
| Practical Life | `.mm-name` | margin-top | 1440 | 25px ×16 / 16px ×1 | 23px ×16 / 16.25px ×1 |
| Practical Life | `.mm-pdf` | margin | 1440 | 0px ×23 / 0px 0px 0px 24px ×5 / 0px 128.125px 0px 24px ×2 … | 0px ×23 / 0px 0px 0px 24px ×21 |
| Practical Life | `.mm-pdf-r` | margin-right | 1440 | 0px ×5 / 128.125px ×2 / 207.434px ×2 … | 0px ×21 |
| Practical Life | `.mm-pdff` | margin | 1440 | 0px 0px 0px 25px ×105 / 0px ×44 / 0px 0px 0px 35.9032px ×4 … | 0px 0px 0px 25px ×101 / 0px ×52 / 0px 0px 0px 25.444px ×2 … |
| Practical Life | `.mm-pdff` | margin-left | 1440 | 25px ×105 / 0px ×44 / 35.9032px ×4 … | 25px ×101 / 0px ×52 / 25.444px ×2 … |
| Practical Life | `.mm-ph1` | margin-top | 1440 | 3px ×13 / 3.01px ×1 | 3px ×14 |
| Practical Life | `.mm-ph11` | margin-top | 1440 | 10.8px ×5 | 18.3px ×5 |
| Practical Life | `.mm-table-wrap` | margin | 1440 | 0px 0px -19.69px ×1 | -27.5px 0px -19.69px ×1 |
| Practical Life | `.mm-tocline` | margin | 1440 | -18.69px 0px 25px ×1 | -15.3px 0px 29px ×1 |
| Practical Life | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Practical Life | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Practical Life | `.ph` | margin | 1440 | 0px 0px 0px 25px ×105 / 0px ×44 / 0px 0px 0px 35.9032px ×4 … | 0px 0px 0px 25px ×101 / 0px ×52 / 0px 0px 0px 25.444px ×2 … |
| Practical Life | `.pullquote` | margin | 1440 | 0px 20px -9px ×12 / 0px 20px ×2 / -22.6px 20px 0px ×1 | 0px 0px -9px ×12 / -81.72px 0px 0px ×1 / 22.8px 0px 23px ×1 … |
| Practical Life | `.pullquote` | margin-bottom | 1440 | -9px ×12 / 0px ×3 | -9px ×12 / 0px ×2 / 23px ×1 |
| Practical Life | `.pullquote` | margin-left | 1440 | 20px ×15 | 0px ×15 |
| Practical Life | `.pullquote` | margin-right | 1440 | 20px ×15 | 0px ×15 |
| Practical Life | `.pullquote` | margin-top | 1440 | 0px ×14 / -22.6px ×1 | 0px ×12 / -81.72px ×1 / 22.8px ×1 … |
| Practical Life | `.pullquote` | padding | 1440 | 22px 0px 0px ×12 / 0px ×3 | 16.75px 0px 0px ×12 / 0px ×3 |
| Practical Life | `.site-foot-in` | padding | 1440 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Practical Life | `.site-foot-in` | padding-bottom | 1440 | 48px ×1 | 17.625px ×1 |
| Practical Life | `.site-foot-in` | padding-top | 1440 | 32px ×1 | 17.625px ×1 |
| Practical Life | `.toc-label` | font-size | 1440 | 22px ×1 | 20px ×1 |
| Practical Life | `.toc-label` | line-height | 1440 | 36.3px ×1 | 33px ×1 |
| Practical Life | `.toc-wrap` | padding | 1440 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Practical Life | `.toc-wrap` | padding-bottom | 1440 | 36px ×1 | 0px ×1 |
| Practical Life | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Practical Life | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Practical Life | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Practical Life | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Practical Life | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Practical Life | `a` | align-items | 1440 | normal ×61 | normal ×47 / baseline ×13 |
| Practical Life | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 1px solid rgba(0, 0, 0, 0) ×20 / 0px none rgb(4, 50, 255) ×12 … | 0px none rgb(43, 43, 43) ×25 / 1px solid rgba(0, 0, 0, 0) ×13 / 0px none rgb(4, 50, 255) ×11 … |
| Practical Life | `a` | border-bottom-color | 1440 | rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×20 / rgb(4, 50, 255) ×12 … | rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×13 / rgb(4, 50, 255) ×11 … |
| Practical Life | `a` | color | 1440 | rgb(43, 43, 43) ×25 / rgb(74, 85, 96) ×13 / rgb(4, 50, 255) ×12 … | rgb(43, 43, 43) ×25 / rgb(74, 85, 96) ×13 / rgb(4, 50, 255) ×11 … |
| Practical Life | `a` | display | 1440 | block ×44 / inline ×17 | block ×44 / flex ×13 / inline ×3 |
| Practical Life | `a` | font-family | 1440 | "EB Garamond", Georgia, serif ×60 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×59 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `a` | font-size | 1440 | 17px ×41 / 19px ×13 / 18px ×5 … | 18px ×58 / 25px ×1 / 15px ×1 |
| Practical Life | `a` | font-style | 1440 | normal ×60 / italic ×1 | normal ×60 |
| Practical Life | `a` | font-weight | 1440 | 400 ×60 / 500 ×1 | 400 ×59 / 500 ×1 |
| Practical Life | `a` | gap | 1440 | normal ×61 | normal ×47 / 8px ×13 |
| Practical Life | `a` | line-height | 1440 | 22.1px ×33 / 25.65px ×13 / 28.05px ×8 … | 23.4px ×33 / 24.3px ×13 / 29.7px ×10 … |
| Practical Life | `a` | margin-left | 1440 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | outline | 1440 | rgb(43, 43, 43) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(4, 50, 255) none 3px ×12 … | rgb(43, 43, 43) none 3px ×25 / rgb(74, 85, 96) none 3px ×13 / rgb(4, 50, 255) none 3px ×11 … |
| Practical Life | `a` | outline-offset | 1440 | 0px ×61 | 0px ×60 |
| Practical Life | `a` | overflow-wrap | 1440 | normal ×61 | normal ×60 |
| Practical Life | `a` | padding | 1440 | 8px 0px ×33 / 0px ×20 / 6px 0px ×8 | 8px 0px ×33 / 0px ×19 / 6px 0px 7.5px ×8 |
| Practical Life | `a` | text-decoration | 1440 | none ×54 / underline ×7 | none ×53 / underline ×7 |
| Practical Life | `a` | text-underline-offset | 1440 | auto ×60 / 3px ×1 | auto ×58 / 4px ×1 / 3px ×1 |
| Practical Life | `cite` | margin-top | 1440 | 3px ×13 / 3.01px ×1 | 3px ×14 |
| Practical Life | `cite` | padding-left | 1440 | 59px ×14 | 48px ×14 |
| Practical Life | `div` | break-inside | 1440 | auto ×369 | auto ×371 |
| Practical Life | `div` | color | 1440 | rgb(43, 43, 43) ×367 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 | rgb(43, 43, 43) ×369 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Practical Life | `div` | font-size | 1440 | 18px ×367 / 15px ×2 | 18px ×369 / 15px ×2 |
| Practical Life | `div` | font-style | 1440 | normal ×369 | normal ×371 |
| Practical Life | `div` | margin | 1440 | 0px ×273 / 15.8px 0px 0px ×22 / 33px 0px 0px ×11 … | 0px ×279 / 23.3px 0px 0px ×22 / 0px 0px 0px 24px ×21 … |
| Practical Life | `div` | padding | 1440 | 0px ×333 / 32.8px 0px 0px ×14 / 26px 40px 30px ×8 … | 0px ×335 / 44.55px 0px 0px ×14 / 26px 40px 30px ×8 … |
| Practical Life | `figure` | margin-left | 1440 | 25px ×105 / 0px ×44 / 35.9032px ×4 … | 25px ×101 / 0px ×52 / 25.444px ×2 … |
| Practical Life | `h1` | font-size | 1440 | 35px ×1 | 40px ×1 |
| Practical Life | `h1` | line-height | 1440 | 42px ×1 | 48px ×1 |
| Practical Life | `h1` | max-width | 1440 | 880px ×1 | 760px ×1 |
| Practical Life | `li` | line-height | 1440 | 29.7px ×135 / 37.2px ×18 | 29.7px ×153 |
| Practical Life | `li` | margin | 1440 | 0px ×128 / 0px 0px 10px ×13 / 5.8px 0px 0px ×9 … | 0px ×129 / 0px 0px 10px ×12 / 13.3px 0px 0px ×7 … |
| Practical Life | `li` | margin-bottom | 1440 | 0px ×140 / 10px ×13 | 0px ×141 / 10px ×12 |
| Practical Life | `li` | margin-top | 1440 | 0px ×141 / 5.8px ×9 / 15.8px ×2 … | 0px ×141 / 13.3px ×7 / 13.28px ×2 … |
| Practical Life | `li` | padding-left | 1440 | 0px ×142 / 31px ×11 | 0px ×142 / 36.78px ×11 |
| Practical Life | `li` | text-align | 1440 | left ×135 / justify ×18 | left ×122 / justify ×31 |
| Practical Life | `li::before` | text-align | 1440 | left ×135 / justify ×18 | left ×122 / justify ×31 |
| Practical Life | `ol` | margin | 1440 | 0px ×2 / 1.8px 0px -7.2px ×1 | 0px ×2 / 11.3px 0px 0px ×1 |
| Practical Life | `p` | font-size | 1440 | 18px ×166 / 2px ×39 / 20px ×17 … | 18px ×166 / 0px ×26 / 20px ×18 … |
| Practical Life | `p` | line-height | 1440 | 37.2px ×165 / 2px ×39 / 40px ×18 … | 29.7px ×165 / 0px ×26 / 40px ×18 … |
| Practical Life | `p` | margin | 1440 | 0px ×137 / 30px 0px 0px ×18 / 22.8px 0px 0px ×17 … | 7.3px 0px 0px ×97 / 23px 0px 0px ×16 / 0px ×15 … |
| Practical Life | `p` | margin-left | 1440 | 0px ×220 / 250px ×3 | 0px ×223 |
| Practical Life | `p` | margin-top | 1440 | 0px ×141 / 30px ×18 / 22.8px ×17 … | 7.3px ×97 / 0px ×16 / 23px ×16 … |
| Practical Life | `p` | max-width | 1440 | none ×220 / 860px ×3 | none ×223 |
| Practical Life | `p` | padding-left | 1440 | 0px ×208 / 11px ×15 | 0px ×223 |
| Practical Life | `p` | text-align | 1440 | justify ×204 / left ×15 / center ×3 … | justify ×165 / start ×40 / left ×15 … |
| Practical Life | `p` | text-indent | 1440 | 0px ×208 / 48px ×15 | 0px ×209 / 48px ×14 |
| Practical Life | `p` | text-wrap | 1440 | wrap ×220 / balance ×3 | wrap ×223 |
| Practical Life | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×86 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×87 |
| Practical Life | `span` | border-radius | 1440 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | color | 1440 | rgb(43, 43, 43) ×73 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×1 … | rgb(43, 43, 43) ×73 / rgb(4, 50, 255) ×11 / rgb(255, 255, 255) ×2 … |
| Practical Life | `span` | display | 1440 | block ×83 / inline ×3 | block ×83 / inline ×4 |
| Practical Life | `span` | flex | 1440 | 0 1 auto ×86 | 0 1 auto ×87 |
| Practical Life | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×85 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×86 / Vollkorn, Georgia, serif ×1 |
| Practical Life | `span` | font-size | 1440 | 17px ×81 / 18px ×3 / 35px ×1 … | 18px ×85 / 40px ×1 / 15px ×1 |
| Practical Life | `span` | font-weight | 1440 | 400 ×85 / 500 ×1 | 400 ×86 / 500 ×1 |
| Practical Life | `span` | line-height | 1440 | 22.1px ×81 / 37.2px ×2 / 42px ×1 … | 23.4px ×81 / 29.7px ×2 / 40px ×2 … |
| Practical Life | `span` | margin-left | 1440 | 0px ×86 | 0px ×87 |
| Practical Life | `span` | min-width | 1440 | 0px ×85 / auto ×1 | 0px ×86 / auto ×1 |
| Practical Life | `span` | padding | 1440 | 8px 0px ×81 / 0px ×5 | 8px 0px ×81 / 0px ×6 |
| Practical Life | `span` | text-align | 1440 | left ×82 / start ×2 / justify ×2 | left ×82 / start ×2 / justify ×2 … |
| Practical Life | `th` | font-weight | 1440 | 400 ×4 | 700 ×4 |
| Practical Life | `ul` | margin | 1440 | 0px ×36 / 0px 0px 0px 25px ×1 | 0px ×37 |
| Practical Life | `ul` | margin-left | 1440 | 0px ×36 / 25px ×1 | 0px ×37 |
| Practical Life | `ul` | padding | 1440 | 0px ×36 / 0px 0px 0px 31px ×1 | 0px ×36 / 0px 0px 0px 48px ×1 |
| Practical Life | `ul` | padding-left | 1440 | 0px ×36 / 31px ×1 | 0px ×36 / 48px ×1 |
| Role of the Adult | `.beige-rule` | clear | 390 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.beige-rule` | margin | 390 | 23px 0px 22px ×8 / 19px 0px 22px ×3 / 26.97px 0px 22.04px ×3 … | 18px 0px 22px ×12 / 21.97px 0px 21.98px ×3 / 21.97px 0px ×2 … |
| Role of the Adult | `.beige-rule` | max-width | 390 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.hero` | background-position | 390 | 50% 22% ×1 | 50% 50% ×1 |
| Role of the Adult | `.mc-band` | margin-top | 390 | -38px ×1 | -39.8px ×1 |
| Role of the Adult | `.meta` | display | 390 | block ×16 / inline ×1 | inline ×17 |
| Role of the Adult | `.meta` | margin-left | 390 | 0px ×16 / 24px ×1 | 0px ×17 |
| Role of the Adult | `.mm-org-rule` | clear | 390 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.mm-org-rule` | margin | 390 | 23px 0px 22px ×8 / 19px 0px 22px ×3 / 26.97px 0px 22.04px ×3 … | 18px 0px 22px ×12 / 21.97px 0px 21.98px ×3 / 21.97px 0px ×2 … |
| Role of the Adult | `.mm-org-rule` | max-width | 390 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.pdf` | display | 390 | inline-block ×17 | inline ×16 / inline-block ×1 |
| Role of the Adult | `.pdf` | margin-left | 390 | 0px ×17 | 24px ×17 |
| Role of the Adult | `.ph` | scroll-snap-align | 390 | start ×3 | center ×3 |
| Role of the Adult | `.res-desc` | margin | 390 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `.res-desc` | margin-top | 390 | 4px ×21 / 6.8px ×9 / -0.45px ×5 | 4px ×19 / 6.8px ×9 / -0.45px ×5 … |
| Role of the Adult | `.res-entry` | margin | 390 | 0px 0px 8px ×22 | 0px ×21 / 0px 0px 8px ×1 |
| Role of the Adult | `.res-item` | display | 390 | flex ×24 | block ×16 / flex ×8 |
| Role of the Adult | `.res-item` | margin | 390 | 3.3px 0px 4px ×11 / 3.3px 0px 0px ×5 / 19.55px 0px 4px ×5 … | 3.3px 0px 4px ×11 / 19.55px 0px 4px ×6 / 3.3px 0px 0px ×5 … |
| Role of the Adult | `.res-item` | margin-top | 390 | 3.3px ×16 / 19.55px ×6 / 24.55px ×1 … | 3.3px ×16 / 19.55px ×7 / 0px ×1 |
| Role of the Adult | `.res-title` | display | 390 | block ×25 | inline ×16 / block ×9 |
| Role of the Adult | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Role of the Adult | `a` | display | 390 | block ×44 / inline ×18 / inline-block ×17 | block ×44 / inline ×34 / inline-block ×1 |
| Role of the Adult | `a` | font-size | 390 | 17px ×52 / 11px ×17 / 18px ×8 … | 17px ×60 / 11px ×17 / 21px ×1 … |
| Role of the Adult | `a` | line-height | 390 | 22.1px ×33 / 11px ×17 / 36px ×12 … | 22.1px ×33 / 11px ×17 / 28.05px ×15 … |
| Role of the Adult | `a` | margin-left | 390 | 0px ×79 | 0px ×62 / 24px ×17 |
| Role of the Adult | `a` | overflow-wrap | 390 | normal ×79 | normal ×44 / anywhere ×35 |
| Role of the Adult | `div` | break-inside | 390 | auto ×126 | auto ×127 |
| Role of the Adult | `div` | color | 390 | rgb(43, 43, 43) ×124 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 | rgb(43, 43, 43) ×125 / rgb(107, 107, 107) ×1 / rgba(255, 255, 255, 0.75) ×1 |
| Role of the Adult | `div` | font-size | 390 | 17px ×124 / 15px ×2 | 17px ×125 / 15px ×2 |
| Role of the Adult | `div` | font-style | 390 | normal ×126 | normal ×127 |
| Role of the Adult | `div` | margin | 390 | 0px ×31 / 0px 0px 8px ×22 / 24px 0px 0px ×15 … | 0px ×53 / 24px 0px 0px ×15 / 18px 0px 22px ×12 … |
| Role of the Adult | `div` | padding | 390 | 0px ×114 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×115 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Role of the Adult | `em` | font-style | 390 | normal ×29 | normal ×25 / italic ×4 |
| Role of the Adult | `li` | margin | 390 | 0px ×122 / 4.3px 0px 0px ×7 / 8px 0px 0px ×2 … | 0px ×122 / 4.3px 0px 0px ×8 / 8px 0px 0px ×2 … |
| Role of the Adult | `li` | margin-bottom | 390 | 0px ×131 / 8px ×2 | 0px ×132 / 8px ×1 |
| Role of the Adult | `p` | color | 390 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×3 / rgb(220, 230, 240) ×1 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×2 / rgb(0, 176, 80) ×1 … |
| Role of the Adult | `p` | font-size | 390 | 17px ×39 | 17px ×38 / 19px ×1 |
| Role of the Adult | `p` | font-style | 390 | normal ×36 / italic ×3 | normal ×37 / italic ×2 |
| Role of the Adult | `p` | line-height | 390 | 36px ×35 / 38px ×4 | 36px ×35 / 38px ×3 / 31.35px ×1 |
| Role of the Adult | `p` | margin | 390 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `p` | margin-top | 390 | 4px ×21 / 6.8px ×9 / -0.45px ×5 … | 4px ×19 / 6.8px ×9 / 0px ×6 … |
| Role of the Adult | `p` | text-align | 390 | left ×35 / center ×4 | left ×35 / center ×3 / start ×1 |
| Role of the Adult | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×129 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×130 |
| Role of the Adult | `span` | border-radius | 390 | 0px ×129 | 0px ×130 |
| Role of the Adult | `span` | color | 390 | rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×26 / rgb(0, 0, 0) ×18 … | rgb(231, 238, 245) ×70 / rgb(4, 50, 255) ×26 / rgb(0, 0, 0) ×18 … |
| Role of the Adult | `span` | display | 390 | block ×124 / inline ×4 / inline-block ×1 | block ×92 / inline ×37 / inline-block ×1 |
| Role of the Adult | `span` | flex | 390 | 0 1 auto ×129 | 0 1 auto ×130 |
| Role of the Adult | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×128 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×129 / Vollkorn, Georgia, serif ×1 |
| Role of the Adult | `span` | font-size | 390 | 17px ×127 / 28px ×1 / 15px ×1 | 17px ×128 / 28px ×1 / 15px ×1 |
| Role of the Adult | `span` | font-weight | 390 | 400 ×128 / 500 ×1 | 400 ×129 / 500 ×1 |
| Role of the Adult | `span` | line-height | 390 | 22.1px ×81 / 28.05px ×45 / 33.6px ×1 … | 22.1px ×81 / 28.05px ×45 / 33.6px ×1 … |
| Role of the Adult | `span` | margin-left | 390 | 0px ×128 / 24px ×1 | 0px ×130 |
| Role of the Adult | `span` | min-width | 390 | 0px ×87 / auto ×42 | 0px ×120 / auto ×10 |
| Role of the Adult | `span` | padding | 390 | 7px 0px ×81 / 0px ×48 | 7px 0px ×81 / 0px ×49 |
| Role of the Adult | `span` | text-align | 390 | left ×82 / start ×47 | left ×82 / start ×47 / center ×1 |
| Role of the Adult | `ul` | list-style | 390 | outside none none ×34 | outside none none ×37 |
| Role of the Adult | `ul` | margin | 390 | 0px ×26 / 24px 0px 0px ×8 | 0px ×29 / 24px 0px 0px ×8 |
| Role of the Adult | `ul` | margin-left | 390 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding | 390 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding-left | 390 | 0px ×34 | 0px ×37 |
| Role of the Adult | `.beige-rule` | clear | 831 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.beige-rule` | margin | 831 | 23.8px 0px 22px ×8 / 27.33px 0px 22.04px ×4 / 27.33px 0px 21.04px ×2 … | 17.8px 0px 21px ×13 / 21.31px 0px 21.01px ×4 / 21.31px 0px 21.04px ×2 … |
| Role of the Adult | `.beige-rule` | max-width | 831 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.hero` | background-position | 831 | 50% 22% ×1 | 50% 50% ×1 |
| Role of the Adult | `.meta` | margin-left | 831 | 0px ×16 / 24px ×1 | 0px ×17 |
| Role of the Adult | `.mm-float` | padding-top | 831 | 1.5px ×1 / 27.16px ×1 / 41.69px ×1 | 8px ×1 / 27.14px ×1 / 41.69px ×1 |
| Role of the Adult | `.mm-org-rule` | clear | 831 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.mm-org-rule` | margin | 831 | 23.8px 0px 22px ×8 / 27.33px 0px 22.04px ×4 / 27.33px 0px 21.04px ×2 … | 17.8px 0px 21px ×13 / 21.31px 0px 21.01px ×4 / 21.31px 0px 21.04px ×2 … |
| Role of the Adult | `.mm-org-rule` | max-width | 831 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Role of the Adult | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Role of the Adult | `.pdf` | margin-left | 831 | 0px ×17 | 0px ×16 / 24px ×1 |
| Role of the Adult | `.res-desc` | margin | 831 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `.res-desc` | margin-top | 831 | 4px ×21 / 6.8px ×9 / -0.45px ×5 | 4px ×19 / 6.8px ×9 / -0.45px ×5 … |
| Role of the Adult | `.res-entry` | margin | 831 | 0px 0px 8px ×22 | 0px ×21 / 0px 0px 8px ×1 |
| Role of the Adult | `.res-item` | margin | 831 | 3.3px 0px 4px ×11 / 3.3px 0px 0px ×5 / 19.55px 0px 4px ×5 … | 3.3px 0px 4px ×11 / 19.55px 0px 4px ×6 / 3.3px 0px 0px ×5 … |
| Role of the Adult | `.res-item` | margin-top | 831 | 3.3px ×16 / 19.55px ×6 / 24.55px ×1 … | 3.3px ×16 / 19.55px ×7 / 0px ×1 |
| Role of the Adult | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Role of the Adult | `a` | font-size | 831 | 17px ×33 / 18px ×27 / 11px ×17 … | 18px ×60 / 11px ×17 / 25px ×1 … |
| Role of the Adult | `a` | line-height | 831 | 22.1px ×33 / 11px ×17 / 29.7px ×15 … | 23.4px ×33 / 11px ×17 / 29.7px ×15 … |
| Role of the Adult | `a` | margin-left | 831 | 0px ×79 | 0px ×78 / 24px ×1 |
| Role of the Adult | `a` | overflow-wrap | 831 | normal ×79 | normal ×44 / anywhere ×35 |
| Role of the Adult | `div` | margin | 831 | 0px ×31 / 0px 0px 8px ×22 / 24px 0px 0px ×15 … | 0px ×52 / 24px 0px 0px ×15 / 17.8px 0px 21px ×13 … |
| Role of the Adult | `div` | padding | 831 | 0px ×112 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … | 0px ×112 / 0px 0px 10px 14px ×8 / 0px 8px 0px 18px ×1 … |
| Role of the Adult | `em` | font-style | 831 | normal ×29 | normal ×25 / italic ×4 |
| Role of the Adult | `li` | margin | 831 | 0px ×122 / 4.3px 0px 0px ×7 / 8px 0px 0px ×2 … | 0px ×122 / 4.3px 0px 0px ×8 / 8px 0px 0px ×2 … |
| Role of the Adult | `li` | margin-bottom | 831 | 0px ×131 / 8px ×2 | 0px ×132 / 8px ×1 |
| Role of the Adult | `p` | color | 831 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×3 / rgb(220, 230, 240) ×1 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×2 / rgb(0, 176, 80) ×1 … |
| Role of the Adult | `p` | font-size | 831 | 18px ×39 | 18px ×38 / 20px ×1 |
| Role of the Adult | `p` | font-style | 831 | normal ×36 / italic ×3 | normal ×37 / italic ×2 |
| Role of the Adult | `p` | line-height | 831 | 37.2px ×35 / 40px ×4 | 37.2px ×35 / 40px ×3 / 33px ×1 |
| Role of the Adult | `p` | margin | 831 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `p` | margin-top | 831 | 4px ×21 / 6.8px ×9 / -0.45px ×5 … | 4px ×19 / 6.8px ×9 / 0px ×6 … |
| Role of the Adult | `p` | text-align | 831 | justify ×35 / center ×4 | justify ×35 / center ×3 / start ×1 |
| Role of the Adult | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×129 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×130 |
| Role of the Adult | `span` | border-radius | 831 | 0px ×129 | 0px ×130 |
| Role of the Adult | `span` | color | 831 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×37 / rgb(0, 0, 0) ×18 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×37 / rgb(0, 0, 0) ×18 … |
| Role of the Adult | `span` | display | 831 | block ×124 / inline ×4 / inline-block ×1 | block ×124 / inline ×5 / inline-block ×1 |
| Role of the Adult | `span` | flex | 831 | 0 1 auto ×129 | 0 1 auto ×130 |
| Role of the Adult | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×128 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×129 / Vollkorn, Georgia, serif ×1 |
| Role of the Adult | `span` | font-size | 831 | 17px ×81 / 18px ×46 / 40px ×1 … | 18px ×128 / 40px ×1 / 15px ×1 |
| Role of the Adult | `span` | font-weight | 831 | 400 ×128 / 500 ×1 | 400 ×129 / 500 ×1 |
| Role of the Adult | `span` | line-height | 831 | 22.1px ×81 / 29.7px ×45 / 48px ×1 … | 23.4px ×81 / 29.7px ×45 / 48px ×1 … |
| Role of the Adult | `span` | margin-left | 831 | 0px ×128 / 24px ×1 | 0px ×130 |
| Role of the Adult | `span` | min-width | 831 | 0px ×87 / auto ×42 | 0px ×88 / auto ×42 |
| Role of the Adult | `span` | padding | 831 | 7px 0px ×81 / 0px ×48 | 7px 0px ×81 / 0px ×49 |
| Role of the Adult | `span` | text-align | 831 | left ×81 / start ×47 / justify ×1 | left ×81 / start ×47 / justify ×1 … |
| Role of the Adult | `ul` | list-style | 831 | outside none none ×34 | outside none none ×37 |
| Role of the Adult | `ul` | margin | 831 | 0px ×26 / 24px 0px 0px ×8 | 0px ×29 / 24px 0px 0px ×8 |
| Role of the Adult | `ul` | margin-left | 831 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding | 831 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding-left | 831 | 0px ×34 | 0px ×37 |
| Role of the Adult | `.beige-rule` | clear | 1440 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.beige-rule` | margin | 1440 | 23.8px 0px 22px ×10 / 27.33px 0px 22.04px ×4 / 27.33px 0px 21.04px ×2 … | 17.8px 0px 21px ×13 / 21.31px 0px 21.01px ×4 / 21.31px 0px 21.04px ×2 … |
| Role of the Adult | `.beige-rule` | max-width | 1440 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.hero` | background-position | 1440 | 50% 22% ×1 | 50% 50% ×1 |
| Role of the Adult | `.meta` | margin-left | 1440 | 0px ×16 / 24px ×1 | 0px ×17 |
| Role of the Adult | `.mm-float` | margin | 1440 | -67.52px 0px 12px 32px ×1 / -3.56px 0px 0px 32px ×1 / 4px 0px 12px 32px ×1 | 4px 0px 12px 32px ×2 / -6.06px 0px 0px 32px ×1 |
| Role of the Adult | `.mm-float` | margin-top | 1440 | -67.52px ×1 / -3.56px ×1 / 4px ×1 | 4px ×2 / -6.06px ×1 |
| Role of the Adult | `.mm-float` | padding-top | 1440 | 0px ×2 / 41.69px ×1 | 8px ×1 / 0px ×1 / 41.69px ×1 |
| Role of the Adult | `.mm-org-rule` | clear | 1440 | both ×21 / none ×2 | both ×22 / none ×1 |
| Role of the Adult | `.mm-org-rule` | margin | 1440 | 23.8px 0px 22px ×10 / 27.33px 0px 22.04px ×4 / 27.33px 0px 21.04px ×2 … | 17.8px 0px 21px ×13 / 21.31px 0px 21.01px ×4 / 21.31px 0px 21.04px ×2 … |
| Role of the Adult | `.mm-org-rule` | max-width | 1440 | 100% ×22 / 100px ×1 | 100% ×23 |
| Role of the Adult | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Role of the Adult | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Role of the Adult | `.pdf` | margin-left | 1440 | 0px ×17 | 0px ×16 / 24px ×1 |
| Role of the Adult | `.res-desc` | margin | 1440 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `.res-desc` | margin-top | 1440 | 4px ×21 / 6.8px ×9 / -0.45px ×5 | 4px ×19 / 6.8px ×9 / -0.45px ×5 … |
| Role of the Adult | `.res-entry` | margin | 1440 | 0px 0px 8px ×22 | 0px ×21 / 0px 0px 8px ×1 |
| Role of the Adult | `.res-item` | margin | 1440 | 3.3px 0px 4px ×11 / 3.3px 0px 0px ×5 / 19.55px 0px 4px ×5 … | 3.3px 0px 4px ×11 / 19.55px 0px 4px ×6 / 3.3px 0px 0px ×5 … |
| Role of the Adult | `.res-item` | margin-top | 1440 | 3.3px ×16 / 19.55px ×6 / 24.55px ×1 … | 3.3px ×16 / 19.55px ×7 / 0px ×1 |
| Role of the Adult | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Role of the Adult | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Role of the Adult | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Role of the Adult | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Role of the Adult | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Role of the Adult | `a` | border-bottom | 1440 | 0px none rgb(4, 50, 255) ×26 / 0px none rgb(43, 43, 43) ×25 / 1px solid rgb(5, 99, 193) ×17 … | 0px none rgb(4, 50, 255) ×26 / 0px none rgb(43, 43, 43) ×25 / 1px solid rgb(5, 99, 193) ×17 … |
| Role of the Adult | `a` | border-bottom-color | 1440 | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×25 / rgb(5, 99, 193) ×17 … | rgb(4, 50, 255) ×26 / rgb(43, 43, 43) ×25 / rgb(5, 99, 193) ×17 … |
| Role of the Adult | `a` | font-size | 1440 | 17px ×41 / 18px ×19 / 11px ×17 … | 18px ×60 / 11px ×17 / 25px ×1 … |
| Role of the Adult | `a` | line-height | 1440 | 22.1px ×33 / 11px ×17 / 37.2px ×12 … | 23.4px ×33 / 11px ×17 / 29.7px ×15 … |
| Role of the Adult | `a` | margin-left | 1440 | 0px ×79 | 0px ×78 / 24px ×1 |
| Role of the Adult | `a` | overflow-wrap | 1440 | normal ×79 | normal ×44 / anywhere ×35 |
| Role of the Adult | `a` | padding | 1440 | 8px 0px ×33 / 0px ×21 / 4px 6px ×17 … | 8px 0px ×33 / 0px ×21 / 4px 6px ×17 … |
| Role of the Adult | `a` | text-decoration | 1440 | none ×58 / underline ×21 | none ×57 / underline ×22 |
| Role of the Adult | `a` | text-underline-offset | 1440 | auto ×78 / 3px ×1 | auto ×77 / 4px ×1 / 3px ×1 |
| Role of the Adult | `div` | margin | 1440 | 0px ×44 / 0px 0px 8px ×22 / 3.3px 0px 4px ×11 … | 0px ×65 / 17.8px 0px 21px ×13 / 3.3px 0px 4px ×11 … |
| Role of the Adult | `div` | padding | 1440 | 0px ×114 / 26px 40px 30px ×8 / 0px 40px ×1 … | 0px ×113 / 26px 40px 30px ×8 / 0px 40px ×1 … |
| Role of the Adult | `em` | font-style | 1440 | normal ×29 | normal ×25 / italic ×4 |
| Role of the Adult | `li` | margin | 1440 | 0px ×122 / 4.3px 0px 0px ×7 / 8px 0px 0px ×2 … | 0px ×122 / 4.3px 0px 0px ×8 / 8px 0px 0px ×2 … |
| Role of the Adult | `li` | margin-bottom | 1440 | 0px ×131 / 8px ×2 | 0px ×132 / 8px ×1 |
| Role of the Adult | `p` | color | 1440 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×3 / rgb(220, 230, 240) ×1 | rgb(0, 0, 0) ×35 / rgb(255, 255, 255) ×2 / rgb(0, 176, 80) ×1 … |
| Role of the Adult | `p` | font-size | 1440 | 18px ×39 | 18px ×38 / 20px ×1 |
| Role of the Adult | `p` | font-style | 1440 | normal ×36 / italic ×3 | normal ×37 / italic ×2 |
| Role of the Adult | `p` | line-height | 1440 | 37.2px ×35 / 40px ×4 | 37.2px ×35 / 40px ×3 / 33px ×1 |
| Role of the Adult | `p` | margin | 1440 | 4px 0px 0px ×12 / 4px 0px ×9 / 6.8px 0px 4px ×8 … | 4px 0px 0px ×13 / 6.8px 0px 4px ×7 / 4px 0px ×6 … |
| Role of the Adult | `p` | margin-top | 1440 | 4px ×21 / 6.8px ×9 / -0.45px ×5 … | 4px ×19 / 6.8px ×9 / 0px ×6 … |
| Role of the Adult | `p` | text-align | 1440 | justify ×35 / center ×4 | justify ×35 / center ×3 / start ×1 |
| Role of the Adult | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×129 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×130 |
| Role of the Adult | `span` | border-radius | 1440 | 0px ×129 | 0px ×130 |
| Role of the Adult | `span` | color | 1440 | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×37 / rgb(0, 0, 0) ×18 … | rgb(43, 43, 43) ×70 / rgb(4, 50, 255) ×37 / rgb(0, 0, 0) ×18 … |
| Role of the Adult | `span` | display | 1440 | block ×124 / inline ×4 / inline-block ×1 | block ×124 / inline ×5 / inline-block ×1 |
| Role of the Adult | `span` | flex | 1440 | 0 1 auto ×129 | 0 1 auto ×130 |
| Role of the Adult | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×128 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×129 / Vollkorn, Georgia, serif ×1 |
| Role of the Adult | `span` | font-size | 1440 | 17px ×81 / 18px ×46 / 40px ×1 … | 18px ×128 / 40px ×1 / 15px ×1 |
| Role of the Adult | `span` | font-weight | 1440 | 400 ×128 / 500 ×1 | 400 ×129 / 500 ×1 |
| Role of the Adult | `span` | line-height | 1440 | 22.1px ×81 / 29.7px ×45 / 48px ×1 … | 23.4px ×81 / 29.7px ×45 / 48px ×1 … |
| Role of the Adult | `span` | margin-left | 1440 | 0px ×128 / 24px ×1 | 0px ×130 |
| Role of the Adult | `span` | min-width | 1440 | 0px ×87 / auto ×42 | 0px ×88 / auto ×42 |
| Role of the Adult | `span` | padding | 1440 | 8px 0px ×81 / 0px ×48 | 8px 0px ×81 / 0px ×49 |
| Role of the Adult | `span` | text-align | 1440 | left ×81 / start ×47 / justify ×1 | left ×81 / start ×47 / justify ×1 … |
| Role of the Adult | `ul` | list-style | 1440 | outside none none ×34 | outside none none ×37 |
| Role of the Adult | `ul` | margin | 1440 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | margin-left | 1440 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding | 1440 | 0px ×34 | 0px ×37 |
| Role of the Adult | `ul` | padding-left | 1440 | 0px ×34 | 0px ×37 |
| Culture | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Culture | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Culture | `.beige-rule` | margin | 390 | 17.95px 0px 0px ×1 | 0px ×1 |
| Culture | `.beige-rule` | visibility | 390 | visible ×1 | hidden ×1 |
| Culture | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Culture | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Culture | `.mc-band` | color | 390 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Culture | `.micro-label` | margin | 390 | 6px 0px 11px ×30 / 0px 0px 11px ×7 / 17.95px 0px 0px ×4 … | 23.95px 0px 11px ×21 / 6px 0px 11px ×8 / 0px 0px 11px ×7 … |
| Culture | `.micro-label` | margin-top | 390 | 6px ×30 / 0px ×7 / 17.95px ×4 … | 23.95px ×25 / 6px ×8 / 0px ×7 … |
| Culture | `.mm-albums-c` | margin | 390 | 2.2px 0px 0px ×7 | -2.61px 0px 0px ×7 |
| Culture | `.mm-cols3` | column-gap | 390 | 72px ×1 | 40px ×1 |
| Culture | `.mm-cols3` | margin | 390 | 14.95px 0px 0px ×1 | 0px 0px 12px ×1 |
| Culture | `.mm-float` | padding-top | 390 | 11px ×2 | 4px ×1 / 13.39px ×1 |
| Culture | `.mm-row` | gap | 390 | 10px ×51 | 10px ×47 / 19.2px ×4 |
| Culture | `.mm-row` | margin | 390 | 28.95px 0px 0px ×35 / 34px 0px 0px ×14 / 24px 0px 0px ×1 … | 12.97px 0px 0px ×19 / 34px 0px 0px ×14 / 8.47px 0px 0px ×9 … |
| Culture | `.mm-row` | margin-top | 390 | 28.95px ×35 / 34px ×14 / 24px ×1 … | 12.97px ×19 / 34px ×14 / 8.47px ×9 … |
| Culture | `.mm-set` | margin | 390 | 14.95px 0px 0px ×1 / 12.2px 0px 0px ×1 / 5.95px 0px 0px ×1 … | 7.22px 0px 0px ×1 / 12.61px 0px 0px ×1 / 23.95px 0px 0px ×1 … |
| Culture | `.mm-sub` | font-size | 390 | 19px ×30 | 17px ×22 / 18px ×8 |
| Culture | `.mm-t` | display | 390 | inline ×53 | inline ×52 / none ×1 |
| Culture | `.ph` | scroll-snap-align | 390 | start ×250 | center ×250 |
| Culture | `.pullquote` | margin | 390 | 0px ×1 | 7.98px 0px -8px ×1 |
| Culture | `.pullquote` | margin-bottom | 390 | 0px ×1 | -8px ×1 |
| Culture | `.pullquote` | margin-top | 390 | 0px ×1 | 7.98px ×1 |
| Culture | `.pullquote` | padding | 390 | 20.95px 0px 0px ×1 | 16.22px 0px 0px ×1 |
| Culture | `.section` | container-type | 390 | normal ×36 | inline-size ×36 |
| Culture | `.section` | margin-top | 390 | 0px ×36 | 0px ×34 / 15.95px ×1 / 5px ×1 |
| Culture | `.site-foot-in` | padding | 390 | 28px 24px 40px ×1 | 14px 24px ×1 |
| Culture | `.site-foot-in` | padding-bottom | 390 | 40px ×1 | 14px ×1 |
| Culture | `.site-foot-in` | padding-top | 390 | 28px ×1 | 14px ×1 |
| Culture | `.toc-label` | color | 390 | rgb(0, 176, 80) ×1 | rgb(4, 50, 255) ×1 |
| Culture | `.toc-label` | font-size | 390 | 20px ×1 | 19px ×1 |
| Culture | `.toc-label` | line-height | 390 | 33px ×1 | 31.35px ×1 |
| Culture | `.toc-wrap` | padding | 390 | 22px 24px 26px ×1 | 22px 24px 0px ×1 |
| Culture | `.toc-wrap` | padding-bottom | 390 | 26px ×1 | 0px ×1 |
| Culture | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Culture | `a` | align-items | 390 | normal ×83 | normal ×46 / baseline ×37 |
| Culture | `a` | border-bottom | 390 | 1px solid rgba(0, 0, 0, 0) ×37 / 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 … | 1px solid rgba(0, 0, 0, 0) ×37 / 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 … |
| Culture | `a` | border-bottom-color | 390 | rgba(0, 0, 0, 0) ×37 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … | rgba(0, 0, 0, 0) ×37 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … |
| Culture | `a` | color | 390 | rgb(74, 85, 96) ×30 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … | rgb(74, 85, 96) ×37 / rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 … |
| Culture | `a` | display | 390 | block ×44 / inline ×39 | block ×44 / flex ×37 / inline ×2 |
| Culture | `a` | font-size | 390 | 18px ×45 / 17px ×36 / 21px ×1 … | 17px ×81 / 21px ×1 / 15px ×1 |
| Culture | `a` | gap | 390 | normal ×83 | normal ×46 / 8px ×37 |
| Culture | `a` | line-height | 390 | 24.3px ×37 / 22.1px ×33 / 29.7px ×8 … | 22.95px ×37 / 22.1px ×33 / 28.05px ×11 … |
| Culture | `a` | outline | 390 | rgb(74, 85, 96) none 3px ×30 / rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … | rgb(74, 85, 96) none 3px ×37 / rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Culture | `div` | break-inside | 390 | auto ×518 / avoid ×37 | auto ×519 / avoid ×37 |
| Culture | `div` | color | 390 | rgb(43, 43, 43) ×538 / rgb(4, 50, 255) ×15 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×540 / rgb(4, 50, 255) ×14 / rgb(107, 107, 107) ×1 … |
| Culture | `div` | font-size | 390 | 17px ×553 / 15px ×2 | 17px ×554 / 15px ×2 |
| Culture | `div` | font-style | 390 | normal ×555 | normal ×556 |
| Culture | `div` | margin | 390 | 0px ×359 / 8px 0px 4px ×55 / 28.95px 0px 0px ×35 … | 0px ×361 / 8px 0px 4px ×55 / 23.95px 0px 11px ×21 … |
| Culture | `div` | padding | 390 | 0px ×518 / 14px 0px 6px ×23 / 0px 0px 10px 14px ×8 … | 0px ×467 / 14px 0px 6px ×23 / 0px 0px 10px 14px ×8 … |
| Culture | `h2` | border-bottom | 390 | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … |
| Culture | `h2` | border-bottom-color | 390 | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … |
| Culture | `h2` | display | 390 | block ×37 | flow-root ×37 |
| Culture | `h2` | font-size | 390 | 19px ×30 / 20px ×7 | 17px ×28 / 18px ×8 / 19px ×1 |
| Culture | `h2` | font-weight | 390 | 400 ×36 / 600 ×1 | 400 ×36 / 700 ×1 |
| Culture | `h2` | line-height | 390 | 22.8px ×30 / 24px ×7 | 20.4px ×28 / 21.6px ×8 / 22.8px ×1 |
| Culture | `h2` | margin | 390 | 0px ×30 / 78px 0px 0px ×6 / 56.31px 0px 0px ×1 | 0px ×25 / 71.75px 0px 0px ×6 / 0px 0px -9.39px ×4 … |
| Culture | `h2` | margin-bottom | 390 | 0px ×37 | 0px ×32 / -9.39px ×4 / -9.8px ×1 |
| Culture | `html` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Culture | `li` | margin | 390 | 0px ×122 / 8px 0px ×39 / 0px 0px 10px ×37 … | 0px ×123 / 8px 0px ×39 / 0px 0px 10px ×36 … |
| Culture | `li` | margin-bottom | 390 | 0px ×133 / 8px ×39 / 10px ×37 | 0px ×134 / 8px ×39 / 10px ×36 |
| Culture | `li` | margin-top | 390 | 0px ×159 / 8px ×39 / 4.95px ×9 … | 0px ×159 / 8px ×39 / 3.97px ×6 … |
| Culture | `li` | padding-left | 390 | 0px ×193 / 30px ×16 | 0px ×193 / 36.07px ×16 |
| Culture | `li` | text-align | 390 | left ×209 | left ×172 / justify ×37 |
| Culture | `li::before` | text-align | 390 | left ×209 | left ×172 / justify ×37 |
| Culture | `p` | color | 390 | rgb(43, 43, 43) ×468 / rgb(0, 0, 0) ×7 / rgb(255, 255, 255) ×2 … | rgb(43, 43, 43) ×475 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Culture | `p` | font-size | 390 | 17px ×478 / 20px ×1 | 17px ×477 / 19px ×1 / 2px ×1 |
| Culture | `p` | line-height | 390 | 28.05px ×474 / 38px ×4 / 33px ×1 | 28.05px ×473 / 38px ×4 / 31.35px ×1 … |
| Culture | `p` | margin | 390 | 0px 0px 11px ×385 / 14.95px 0px 0px ×19 / 12.2px 0px 0px ×18 … | 0px 0px 11px ×358 / 23.97px 0px 11px ×22 / 42px 0px 0px ×15 … |
| Culture | `p` | margin-left | 390 | 0px ×472 / 30px ×5 / 60px ×2 | 0px ×479 |
| Culture | `p` | margin-top | 390 | 0px ×402 / 14.95px ×19 / 12.2px ×18 … | 0px ×369 / 23.97px ×22 / 42px ×15 … |
| Culture | `p` | max-width | 390 | none ×476 / 860px ×3 | none ×479 |
| Culture | `p` | text-wrap | 390 | wrap ×476 / balance ×3 | wrap ×479 |
| Culture | `span` | background | 390 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×353 / rgb(230, 230, 228) none repeat scroll 0% ×192 / rgb(43, 43, 43) none repeat scroll 0% 0% ×55 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×354 / rgb(230, 230, 228) none repeat scroll 0% ×192 / rgb(43, 43, 43) none repeat scroll 0% 0% ×55 |
| Culture | `span` | border-radius | 390 | 0px ×353 / 50% ×247 | 0px ×354 / 50% ×247 |
| Culture | `span` | color | 390 | rgb(43, 43, 43) ×472 / rgb(231, 238, 245) ×70 / rgb(238, 0, 0) ×23 … | rgb(43, 43, 43) ×479 / rgb(231, 238, 245) ×70 / rgb(238, 0, 0) ×23 … |
| Culture | `span` | display | 390 | block ×513 / inline ×85 / inline-block ×2 | block ×333 / inline ×267 / none ×1 |
| Culture | `span` | flex | 390 | 0 1 auto ×600 | 0 1 auto ×601 |
| Culture | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×599 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×600 / Vollkorn, Georgia, serif ×1 |
| Culture | `span` | font-size | 390 | 17px ×574 / 18px ×24 / 28px ×1 … | 17px ×575 / 18px ×24 / 28px ×1 … |
| Culture | `span` | font-weight | 390 | 400 ×575 / 700 ×24 / 500 ×1 | 400 ×576 / 700 ×24 / 500 ×1 |
| Culture | `span` | line-height | 390 | 28.05px ×492 / 22.1px ×81 / 29.7px ×24 … | 28.05px ×492 / 22.1px ×81 / 29.7px ×24 … |
| Culture | `span` | margin-left | 390 | 0px ×600 | 0px ×601 |
| Culture | `span` | min-width | 390 | auto ×431 / 0px ×169 | 0px ×350 / auto ×251 |
| Culture | `span` | padding | 390 | 0px ×519 / 7px 0px ×81 | 0px ×520 / 7px 0px ×81 |
| Culture | `span` | text-align | 390 | start ×309 / left ×289 / center ×2 | start ×311 / left ×289 / center ×1 |
| Culture | `ul` | list-style | 390 | outside none none ×45 | outside none none ×44 |
| Culture | `ul` | margin | 390 | 0px ×37 / 24px 0px 0px ×8 | 0px ×36 / 24px 0px 0px ×8 |
| Culture | `ul` | margin-left | 390 | 0px ×45 | 0px ×44 |
| Culture | `ul` | padding | 390 | 0px ×37 / 0px 0px 0px 30px ×8 | 0px ×36 / 0px 0px 0px 48px ×8 |
| Culture | `ul` | padding-left | 390 | 0px ×37 / 30px ×8 | 0px ×36 / 48px ×8 |
| Culture | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Culture | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Culture | `.beige-rule` | margin | 831 | 17.31px 0px 0px ×1 | 0px ×1 |
| Culture | `.beige-rule` | visibility | 831 | visible ×1 | hidden ×1 |
| Culture | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Culture | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Culture | `.mc-band` | color | 831 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Culture | `.mc-band` | margin-top | 831 | -39.04px ×1 | -14.7px ×1 |
| Culture | `.micro-label` | margin | 831 | 6px 0px 11px ×30 / 0px 0px 11px ×7 / 17.31px 0px 0px ×5 … | 22.3px 0px 11px ×19 / 6px 0px 11px ×8 / 0px 0px 11px ×7 … |
| Culture | `.micro-label` | margin-top | 831 | 6px ×30 / 0px ×7 / 17.31px ×5 … | 22.3px ×23 / 6px ×8 / 0px ×7 … |
| Culture | `.mm-albums-c` | margin | 831 | 2.81px 0px 0px 24px ×7 | -2.5px 0px 0px 24px ×5 / -2.25px 0px 0px 24px ×2 |
| Culture | `.mm-cols3` | column-gap | 831 | 72px ×1 | 40px ×1 |
| Culture | `.mm-cols3` | margin | 831 | 14.31px 0px 0px ×1 | 0px 0px 12px ×1 |
| Culture | `.mm-imgs` | justify-content | 831 | normal ×53 / flex-end ×3 / flex-start ×2 | normal ×53 / flex-end ×3 / center ×2 |
| Culture | `.mm-imgs` | margin | 831 | 0px ×58 | 0px ×57 / 24px 0px 0px ×1 |
| Culture | `.mm-row` | gap | 831 | 10.01px ×17 / 10px ×8 / 25.3px ×5 … | 10.01px ×17 / 10px ×7 / 25.3px ×5 … |
| Culture | `.mm-row` | margin | 831 | 28.31px 0px 0px ×35 / 48px 0px 0px ×14 / 23px 0px 0px ×1 … | 37.35px 0px 0px ×24 / 48px 0px 0px ×14 / 32.6px 0px 0px ×7 … |
| Culture | `.mm-row` | margin-top | 831 | 28.31px ×35 / 48px ×14 / 23px ×1 … | 37.35px ×24 / 48px ×14 / 32.6px ×7 … |
| Culture | `.mm-set` | display | 831 | flex ×5 | flex ×4 / block ×1 |
| Culture | `.mm-set` | margin | 831 | 14.31px 0px 0px ×1 / 12.81px 0px 0px ×1 / 5.31px 0px 0px ×1 … | 11.3px 0px 0px ×1 / 11.41px 0px 0px ×1 / 22.3px 0px 0px ×1 … |
| Culture | `.mm-sub` | font-size | 831 | 21px ×30 | 18px ×22 / 20px ×8 |
| Culture | `.mm-t` | display | 831 | inline ×53 | inline ×52 / none ×1 |
| Culture | `.mm-text` | max-width | 831 | 292.056px ×1 / 142.216px ×1 / 471.856px ×1 … | 292.056px ×1 / none ×1 / 471.856px ×1 … |
| Culture | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Culture | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Culture | `.pullquote` | margin | 831 | 0px 20px ×1 | 8px 0px 0px ×1 |
| Culture | `.pullquote` | margin-left | 831 | 20px ×1 | 0px ×1 |
| Culture | `.pullquote` | margin-right | 831 | 20px ×1 | 0px ×1 |
| Culture | `.pullquote` | margin-top | 831 | 0px ×1 | 8px ×1 |
| Culture | `.pullquote` | padding | 831 | 20.31px 0px 0px ×1 | 15.3px 0px 0px ×1 |
| Culture | `.section` | container-type | 831 | normal ×36 | inline-size ×36 |
| Culture | `.section` | margin-top | 831 | 0px ×36 | 0px ×33 / 14.3px ×1 / 8.73px ×1 … |
| Culture | `.site-foot-in` | padding | 831 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Culture | `.site-foot-in` | padding-bottom | 831 | 48px ×1 | 17.625px ×1 |
| Culture | `.site-foot-in` | padding-top | 831 | 32px ×1 | 17.625px ×1 |
| Culture | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Culture | `.toc-label` | color | 831 | rgb(0, 176, 80) ×1 | rgb(4, 50, 255) ×1 |
| Culture | `.toc-label` | font-size | 831 | 22px ×1 | 20px ×1 |
| Culture | `.toc-label` | line-height | 831 | 36.3px ×1 | 33px ×1 |
| Culture | `.toc-wrap` | padding | 831 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Culture | `.toc-wrap` | padding-bottom | 831 | 36px ×1 | 0px ×1 |
| Culture | `a` | align-items | 831 | normal ×83 | normal ×46 / baseline ×37 |
| Culture | `a` | border-bottom | 831 | 1px solid rgba(0, 0, 0, 0) ×37 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 … | 1px solid rgba(0, 0, 0, 0) ×37 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 … |
| Culture | `a` | border-bottom-color | 831 | rgba(0, 0, 0, 0) ×37 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … | rgba(0, 0, 0, 0) ×37 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Culture | `a` | color | 831 | rgb(74, 85, 96) ×30 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×14 … | rgb(74, 85, 96) ×37 / rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 … |
| Culture | `a` | display | 831 | block ×44 / inline ×39 | block ×44 / flex ×37 / inline ×2 |
| Culture | `a` | font-size | 831 | 19px ×37 / 17px ×33 / 18px ×11 … | 18px ×81 / 25px ×1 / 15px ×1 |
| Culture | `a` | gap | 831 | normal ×83 | normal ×46 / 8px ×37 |
| Culture | `a` | line-height | 831 | 25.65px ×37 / 22.1px ×33 / 29.7px ×11 … | 24.3px ×37 / 23.4px ×33 / 29.7px ×11 … |
| Culture | `a` | outline | 831 | rgb(74, 85, 96) none 3px ×30 / rgb(43, 43, 43) none 3px ×25 / rgb(4, 50, 255) none 3px ×14 … | rgb(74, 85, 96) none 3px ×37 / rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 … |
| Culture | `div` | break-inside | 831 | auto ×465 / avoid ×37 | auto ×466 / avoid ×37 |
| Culture | `div` | color | 831 | rgb(43, 43, 43) ×485 / rgb(4, 50, 255) ×15 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×487 / rgb(4, 50, 255) ×14 / rgb(107, 107, 107) ×1 … |
| Culture | `div` | font-size | 831 | 18px ×500 / 15px ×2 | 18px ×501 / 15px ×2 |
| Culture | `div` | font-style | 831 | normal ×502 | normal ×503 |
| Culture | `div` | margin | 831 | 0px ×365 / 28.31px 0px 0px ×35 / 6px 0px 11px ×30 … | 0px ×366 / 37.35px 0px 0px ×24 / 22.3px 0px 11px ×19 … |
| Culture | `div` | padding | 831 | 0px ×465 / 14px 0px 6px ×23 / 0px 0px 10px 14px ×8 … | 0px ×465 / 14px 0px 6px ×23 / 0px 0px 10px 14px ×8 … |
| Culture | `h2` | border-bottom | 831 | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … |
| Culture | `h2` | border-bottom-color | 831 | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … |
| Culture | `h2` | display | 831 | block ×37 | flow-root ×37 |
| Culture | `h2` | font-size | 831 | 21px ×30 / 22px ×7 | 18px ×28 / 20px ×9 |
| Culture | `h2` | font-weight | 831 | 400 ×36 / 600 ×1 | 400 ×36 / 700 ×1 |
| Culture | `h2` | line-height | 831 | 25.2px ×30 / 26.4px ×7 | 21.6px ×28 / 24px ×9 |
| Culture | `h2` | margin | 831 | 0px ×30 / 91px 0px 0px ×6 / 57.31px 0px 0px ×1 | 0px ×12 / -20px 0px 0px ×11 / 35.25px 0px 0px ×6 … |
| Culture | `h2` | margin-bottom | 831 | 0px ×37 | 0px ×32 / -9.59px ×4 / -9px ×1 |
| Culture | `html` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Culture | `li` | margin | 831 | 0px ×122 / 8px 0px ×39 / 0px 0px 10px ×37 … | 0px ×123 / 8px 0px ×39 / 0px 0px 10px ×36 … |
| Culture | `li` | margin-bottom | 831 | 0px ×133 / 8px ×39 / 10px ×37 | 0px ×134 / 8px ×39 / 10px ×36 |
| Culture | `li` | margin-top | 831 | 0px ×159 / 8px ×39 / 4.31px ×9 … | 0px ×159 / 8px ×39 / 3.3px ×6 … |
| Culture | `li` | padding-left | 831 | 0px ×193 / 30px ×16 | 0px ×193 / 36.78px ×16 |
| Culture | `li` | text-align | 831 | left ×165 / justify ×44 | left ×122 / justify ×87 |
| Culture | `li::before` | text-align | 831 | left ×165 / justify ×44 | left ×122 / justify ×87 |
| Culture | `ol` | margin | 831 | 0px ×2 / 0px 0px 0px 48px ×1 | 0px ×3 |
| Culture | `ol` | margin-left | 831 | 0px ×2 / 48px ×1 | 0px ×3 |
| Culture | `p` | color | 831 | rgb(43, 43, 43) ×468 / rgb(0, 0, 0) ×7 / rgb(255, 255, 255) ×2 … | rgb(43, 43, 43) ×475 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Culture | `p` | font-size | 831 | 18px ×478 / 22px ×1 | 18px ×477 / 20px ×1 / 2px ×1 |
| Culture | `p` | line-height | 831 | 29.7px ×474 / 40px ×4 / 36.3px ×1 | 29.7px ×473 / 40px ×4 / 33px ×1 … |
| Culture | `p` | margin | 831 | 0px 0px 11px ×385 / 14.31px 0px 0px ×18 / 12.81px 0px 0px ×18 … | 0px 0px 11px ×358 / 22.3px 0px 11px ×20 / 31.75px 0px 0px ×15 … |
| Culture | `p` | margin-left | 831 | 0px ×467 / 30px ×5 / 48px ×5 … | 0px ×479 |
| Culture | `p` | margin-top | 831 | 0px ×402 / 14.31px ×19 / 12.81px ×18 … | 0px ×369 / 22.3px ×28 / 31.75px ×15 … |
| Culture | `p` | max-width | 831 | none ×476 / 860px ×3 | none ×479 |
| Culture | `p` | text-align | 831 | justify ×473 / center ×3 / left ×2 … | justify ×473 / center ×3 / start ×2 … |
| Culture | `p` | text-indent | 831 | 0px ×478 / 48px ×1 | 0px ×479 |
| Culture | `p` | text-wrap | 831 | wrap ×475 / balance ×3 / nowrap ×1 | wrap ×479 |
| Culture | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×353 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×354 |
| Culture | `span` | border-radius | 831 | 0px ×353 | 0px ×354 |
| Culture | `span` | color | 831 | rgb(43, 43, 43) ×295 / rgb(4, 50, 255) ×33 / rgb(238, 0, 0) ×23 … | rgb(43, 43, 43) ×302 / rgb(4, 50, 255) ×26 / rgb(238, 0, 0) ×23 … |
| Culture | `span` | display | 831 | block ×264 / inline ×85 / inline-block ×4 | inline ×265 / block ×86 / inline-block ×2 … |
| Culture | `span` | flex | 831 | 0 1 auto ×353 | 0 1 auto ×354 |
| Culture | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×352 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×353 / Vollkorn, Georgia, serif ×1 |
| Culture | `span` | font-size | 831 | 18px ×270 / 17px ×81 / 40px ×1 … | 18px ×352 / 40px ×1 / 15px ×1 |
| Culture | `span` | font-weight | 831 | 400 ×328 / 700 ×24 / 500 ×1 | 400 ×329 / 700 ×24 / 500 ×1 |
| Culture | `span` | line-height | 831 | 29.7px ×269 / 22.1px ×81 / 48px ×1 … | 29.7px ×269 / 23.4px ×81 / 40px ×2 … |
| Culture | `span` | margin-left | 831 | 0px ×351 / -4.08px ×1 / 151.57px ×1 | 0px ×352 / -4.08px ×1 / 151.57px ×1 |
| Culture | `span` | min-width | 831 | auto ×182 / 0px ×171 | 0px ×350 / auto ×4 |
| Culture | `span` | padding | 831 | 0px ×272 / 7px 0px ×81 | 0px ×273 / 7px 0px ×81 |
| Culture | `span` | text-align | 831 | justify ×207 / left ×84 / start ×62 | justify ×207 / left ×84 / start ×62 … |
| Culture | `ul` | list-style | 831 | outside none none ×45 | outside none none ×44 |
| Culture | `ul` | margin | 831 | 0px ×37 / 24px 0px 0px ×8 | 0px ×36 / 24px 0px 0px ×8 |
| Culture | `ul` | margin-left | 831 | 0px ×45 | 0px ×44 |
| Culture | `ul` | padding | 831 | 0px ×37 / 0px 0px 0px 30px ×8 | 0px ×36 / 0px 0px 0px 48px ×8 |
| Culture | `ul` | padding-left | 831 | 0px ×37 / 30px ×8 | 0px ×36 / 48px ×8 |
| Culture | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Culture | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Culture | `.beige-rule` | margin | 1440 | 17.31px 0px 0px ×1 | 0px ×1 |
| Culture | `.beige-rule` | visibility | 1440 | visible ×1 | hidden ×1 |
| Culture | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Culture | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Culture | `.mc-band` | color | 1440 | rgb(43, 43, 43) ×1 | rgb(255, 255, 255) ×1 |
| Culture | `.mc-band` | margin-top | 1440 | -39.04px ×1 | -14.7px ×1 |
| Culture | `.micro-label` | margin | 1440 | 6px 0px 11px ×30 / 0px 0px 11px ×7 / 17.31px 0px 0px ×4 … | 22.3px 0px 11px ×11 / 6px 0px 11px ×8 / 33.3px 0px 11px ×8 … |
| Culture | `.micro-label` | margin-top | 1440 | 6px ×30 / 0px ×7 / 17.31px ×4 … | 22.3px ×15 / 6px ×8 / 33.3px ×8 … |
| Culture | `.mm-albums-c` | margin | 1440 | 2.81px 0px 0px 24px ×7 | -2.5px 0px 0px 24px ×5 / -2.25px 0px 0px 24px ×2 |
| Culture | `.mm-cols3` | column-gap | 1440 | 72px ×1 | 40px ×1 |
| Culture | `.mm-cols3` | margin | 1440 | 14.31px 0px 0px ×1 | 0px 0px 12px ×1 |
| Culture | `.mm-imgs` | gap | 1440 | normal ×53 / 24px ×4 / 17.47px ×1 | normal ×53 / 24px ×4 / 20.15px ×1 |
| Culture | `.mm-imgs` | justify-content | 1440 | normal ×53 / flex-end ×3 / flex-start ×2 | normal ×53 / flex-end ×4 / center ×1 |
| Culture | `.mm-row` | gap | 1440 | 38.4px ×34 / 0px ×3 / 87.65px ×1 … | 38.4px ×33 / 19.2px ×4 / 0px ×3 … |
| Culture | `.mm-row` | margin | 1440 | 28.31px 0px 0px ×35 / 48px 0px 0px ×14 / 23px 0px 0px ×1 … | 37.35px 0px 0px ×32 / 48px 0px 0px ×14 / 32.6px 0px 0px ×2 … |
| Culture | `.mm-row` | margin-top | 1440 | 28.31px ×35 / 48px ×14 / 23px ×1 … | 37.35px ×32 / 48px ×14 / 32.6px ×2 … |
| Culture | `.mm-set` | margin | 1440 | 14.31px 0px 0px ×1 / 12.81px 0px 0px ×1 / 5.31px 0px 0px ×1 … | 8.8px 0px 0px ×1 / 369.82px 0px 0px ×1 / 22.3px 0px 0px ×1 … |
| Culture | `.mm-sub` | font-size | 1440 | 21px ×30 | 18px ×22 / 20px ×8 |
| Culture | `.mm-t` | display | 1440 | inline ×53 | inline ×52 / none ×1 |
| Culture | `.mm-text` | max-width | 1440 | 681.056px ×1 / 531.216px ×1 / 860.856px ×1 … | 537.056px ×1 / 531.216px ×1 / 860.856px ×1 … |
| Culture | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Culture | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Culture | `.pullquote` | margin | 1440 | 0px 20px ×1 | 8px 0px 0px ×1 |
| Culture | `.pullquote` | margin-left | 1440 | 20px ×1 | 0px ×1 |
| Culture | `.pullquote` | margin-right | 1440 | 20px ×1 | 0px ×1 |
| Culture | `.pullquote` | margin-top | 1440 | 0px ×1 | 8px ×1 |
| Culture | `.pullquote` | padding | 1440 | 20.31px 0px 0px ×1 | 15.3px 0px 0px ×1 |
| Culture | `.section` | container-type | 1440 | normal ×36 | inline-size ×36 |
| Culture | `.section` | margin-top | 1440 | 0px ×36 | 0px ×33 / 14.3px ×1 / 8.75px ×1 … |
| Culture | `.site-foot-in` | padding | 1440 | 32px 40px 48px ×1 | 17.625px 40px ×1 |
| Culture | `.site-foot-in` | padding-bottom | 1440 | 48px ×1 | 17.625px ×1 |
| Culture | `.site-foot-in` | padding-top | 1440 | 32px ×1 | 17.625px ×1 |
| Culture | `.toc-label` | color | 1440 | rgb(0, 176, 80) ×1 | rgb(4, 50, 255) ×1 |
| Culture | `.toc-label` | font-size | 1440 | 22px ×1 | 20px ×1 |
| Culture | `.toc-label` | line-height | 1440 | 36.3px ×1 | 33px ×1 |
| Culture | `.toc-wrap` | padding | 1440 | 26px 0px 36px ×1 | 26px 0px 0px ×1 |
| Culture | `.toc-wrap` | padding-bottom | 1440 | 36px ×1 | 0px ×1 |
| Culture | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Culture | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Culture | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Culture | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Culture | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Culture | `a` | align-items | 1440 | normal ×83 | normal ×46 / baseline ×37 |
| Culture | `a` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×44 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×8 … | 1px solid rgba(0, 0, 0, 0) ×37 / 0px none rgb(43, 43, 43) ×25 / 0px none rgb(4, 50, 255) ×10 … |
| Culture | `a` | border-bottom-color | 1440 | rgba(0, 0, 0, 0) ×44 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×8 … | rgba(0, 0, 0, 0) ×37 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×10 … |
| Culture | `a` | color | 1440 | rgb(74, 85, 96) ×30 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×15 … | rgb(74, 85, 96) ×37 / rgb(43, 43, 43) ×25 / rgb(4, 50, 255) ×10 … |
| Culture | `a` | display | 1440 | block ×44 / inline ×39 | block ×44 / flex ×37 / inline ×2 |
| Culture | `a` | font-size | 1440 | 17px ×41 / 19px ×37 / 18px ×3 … | 18px ×81 / 25px ×1 / 15px ×1 |
| Culture | `a` | gap | 1440 | normal ×83 | normal ×46 / 8px ×37 |
| Culture | `a` | line-height | 1440 | 25.65px ×37 / 22.1px ×33 / 28.05px ×8 … | 24.3px ×37 / 23.4px ×33 / 29.7px ×11 … |
| Culture | `a` | outline | 1440 | rgb(74, 85, 96) none 3px ×30 / rgb(43, 43, 43) none 3px ×25 / rgb(4, 50, 255) none 3px ×15 … | rgb(74, 85, 96) none 3px ×37 / rgb(43, 43, 43) none 3px ×25 / rgb(4, 50, 255) none 3px ×10 … |
| Culture | `a` | padding | 1440 | 0px ×42 / 8px 0px ×33 / 6px 0px ×8 | 0px ×42 / 8px 0px ×33 / 6px 0px 7.5px ×8 |
| Culture | `a` | text-decoration | 1440 | none ×78 / underline ×5 | none ×77 / underline ×6 |
| Culture | `a` | text-underline-offset | 1440 | auto ×82 / 3px ×1 | auto ×81 / 4px ×1 / 3px ×1 |
| Culture | `div` | break-inside | 1440 | auto ×465 / avoid ×37 | auto ×466 / avoid ×37 |
| Culture | `div` | color | 1440 | rgb(43, 43, 43) ×485 / rgb(4, 50, 255) ×15 / rgb(107, 107, 107) ×1 … | rgb(43, 43, 43) ×487 / rgb(4, 50, 255) ×14 / rgb(107, 107, 107) ×1 … |
| Culture | `div` | font-size | 1440 | 18px ×500 / 15px ×2 | 18px ×501 / 15px ×2 |
| Culture | `div` | font-style | 1440 | normal ×502 | normal ×503 |
| Culture | `div` | margin | 1440 | 0px ×378 / 28.31px 0px 0px ×35 / 6px 0px 11px ×30 … | 0px ×380 / 37.35px 0px 0px ×32 / 48px 0px 0px ×14 … |
| Culture | `div` | padding | 1440 | 0px ×465 / 14px 0px 6px ×23 / 26px 40px 30px ×8 … | 0px ×465 / 14px 0px 6px ×23 / 26px 40px 30px ×8 … |
| Culture | `h2` | border-bottom | 1440 | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … | 0px none rgb(4, 50, 255) ×12 / 0px none rgb(238, 0, 0) ×9 / 0px none rgb(0, 176, 80) ×8 … |
| Culture | `h2` | border-bottom-color | 1440 | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … | rgb(4, 50, 255) ×18 / rgb(0, 176, 80) ×9 / rgb(238, 0, 0) ×9 … |
| Culture | `h2` | display | 1440 | block ×37 | flow-root ×37 |
| Culture | `h2` | font-size | 1440 | 21px ×30 / 22px ×7 | 18px ×28 / 20px ×9 |
| Culture | `h2` | font-weight | 1440 | 400 ×36 / 600 ×1 | 400 ×36 / 700 ×1 |
| Culture | `h2` | line-height | 1440 | 25.2px ×30 / 26.4px ×7 | 21.6px ×28 / 24px ×9 |
| Culture | `h2` | margin | 1440 | 0px ×30 / 91px 0px 0px ×6 / 57.31px 0px 0px ×1 | 0px ×12 / -20px 0px 0px ×11 / 35.25px 0px 0px ×6 … |
| Culture | `h2` | margin-bottom | 1440 | 0px ×37 | 0px ×32 / -9.59px ×4 / -9px ×1 |
| Culture | `html` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×1 | rgb(245, 238, 227) none repeat scroll 0% ×1 |
| Culture | `li` | margin | 1440 | 0px ×122 / 8px 0px ×39 / 0px 0px 10px ×37 … | 0px ×123 / 8px 0px ×39 / 0px 0px 10px ×36 … |
| Culture | `li` | margin-bottom | 1440 | 0px ×133 / 8px ×39 / 10px ×37 | 0px ×134 / 8px ×39 / 10px ×36 |
| Culture | `li` | margin-top | 1440 | 0px ×159 / 8px ×39 / 4.31px ×9 … | 0px ×159 / 8px ×39 / 3.3px ×7 … |
| Culture | `li` | padding-left | 1440 | 0px ×193 / 30px ×16 | 0px ×193 / 36.78px ×16 |
| Culture | `li` | text-align | 1440 | left ×165 / justify ×44 | left ×122 / justify ×87 |
| Culture | `li::before` | text-align | 1440 | left ×165 / justify ×44 | left ×122 / justify ×87 |
| Culture | `ol` | margin | 1440 | 0px ×2 / 0px 0px 0px 48px ×1 | 0px ×3 |
| Culture | `ol` | margin-left | 1440 | 0px ×2 / 48px ×1 | 0px ×3 |
| Culture | `p` | color | 1440 | rgb(43, 43, 43) ×468 / rgb(0, 0, 0) ×7 / rgb(255, 255, 255) ×2 … | rgb(43, 43, 43) ×475 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Culture | `p` | font-size | 1440 | 18px ×478 / 22px ×1 | 18px ×477 / 20px ×1 / 2px ×1 |
| Culture | `p` | line-height | 1440 | 29.7px ×474 / 40px ×4 / 36.3px ×1 | 29.7px ×473 / 40px ×4 / 33px ×1 … |
| Culture | `p` | margin | 1440 | 0px 0px 11px ×385 / 14.31px 0px 0px ×18 / 12.81px 0px 0px ×18 … | 0px 0px 11px ×365 / 11.3px 0px 0px ×17 / 31.75px 0px 0px ×15 … |
| Culture | `p` | margin-left | 1440 | 0px ×464 / 30px ×5 / 48px ×5 … | 0px ×479 |
| Culture | `p` | margin-top | 1440 | 0px ×402 / 14.31px ×19 / 12.81px ×18 … | 0px ×376 / 22.3px ×22 / 11.3px ×17 … |
| Culture | `p` | max-width | 1440 | none ×476 / 860px ×3 | none ×479 |
| Culture | `p` | text-align | 1440 | justify ×473 / center ×3 / left ×2 … | justify ×473 / center ×3 / start ×2 … |
| Culture | `p` | text-indent | 1440 | 0px ×478 / 48px ×1 | 0px ×479 |
| Culture | `p` | text-wrap | 1440 | wrap ×475 / balance ×3 / nowrap ×1 | wrap ×479 |
| Culture | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×353 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×354 |
| Culture | `span` | border-radius | 1440 | 0px ×353 | 0px ×354 |
| Culture | `span` | color | 1440 | rgb(43, 43, 43) ×295 / rgb(4, 50, 255) ×33 / rgb(238, 0, 0) ×23 … | rgb(43, 43, 43) ×302 / rgb(4, 50, 255) ×26 / rgb(238, 0, 0) ×23 … |
| Culture | `span` | display | 1440 | block ×264 / inline ×85 / inline-block ×4 | inline ×265 / block ×86 / inline-block ×2 … |
| Culture | `span` | flex | 1440 | 0 1 auto ×353 | 0 1 auto ×354 |
| Culture | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×352 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×353 / Vollkorn, Georgia, serif ×1 |
| Culture | `span` | font-size | 1440 | 18px ×270 / 17px ×81 / 40px ×1 … | 18px ×352 / 40px ×1 / 15px ×1 |
| Culture | `span` | font-weight | 1440 | 400 ×328 / 700 ×24 / 500 ×1 | 400 ×329 / 700 ×24 / 500 ×1 |
| Culture | `span` | line-height | 1440 | 29.7px ×269 / 22.1px ×81 / 48px ×1 … | 29.7px ×269 / 23.4px ×81 / 40px ×2 … |
| Culture | `span` | margin-left | 1440 | 0px ×351 / 167.95px ×1 / 196.01px ×1 | 0px ×352 / 165.35px ×1 / 200.15px ×1 |
| Culture | `span` | min-width | 1440 | auto ×182 / 0px ×171 | 0px ×350 / auto ×4 |
| Culture | `span` | padding | 1440 | 0px ×272 / 8px 0px ×81 | 0px ×273 / 8px 0px ×81 |
| Culture | `span` | text-align | 1440 | justify ×207 / left ×84 / start ×62 | justify ×207 / left ×84 / start ×62 … |
| Culture | `ul` | list-style | 1440 | outside none none ×45 | outside none none ×44 |
| Culture | `ul` | margin | 1440 | 0px ×45 | 0px ×44 |
| Culture | `ul` | margin-left | 1440 | 0px ×45 | 0px ×44 |
| Culture | `ul` | padding | 1440 | 0px ×37 / 0px 0px 0px 30px ×8 | 0px ×36 / 0px 0px 0px 48px ×8 |
| Culture | `ul` | padding-left | 1440 | 0px ×37 / 30px ×8 | 0px ×36 / 48px ×8 |
| Sensorial Curriculum | `.article` | margin | 390 | 0px ×1 | 36px 0px 0px ×1 |
| Sensorial Curriculum | `.article` | margin-top | 390 | 0px ×1 | 36px ×1 |
| Sensorial Curriculum | `.article` | padding | 390 | 0px 24px 20px ×1 | 0px 24px 56px ×1 |
| Sensorial Curriculum | `.beige-rule` | background | 390 | rgb(217, 201, 171) none repeat scroll 0% ×7 | rgb(217, 201, 171) none repeat scroll 0% ×1 |
| Sensorial Curriculum | `.beige-rule` | clear | 390 | none ×7 | none ×1 |
| Sensorial Curriculum | `.beige-rule` | margin | 390 | 20px 0px ×5 / 0px ×1 / 20px 0px -22px ×1 | 0px ×1 |
| Sensorial Curriculum | `.beige-rule` | max-width | 390 | 100% ×7 | 100% ×1 |
| Sensorial Curriculum | `.beige-rule` | visibility | 390 | visible ×5 / hidden ×2 | hidden ×1 |
| Sensorial Curriculum | `.blindfold-label` | margin | 390 | 26px 0px 6px ×2 | 42px 0px 0px ×2 |
| Sensorial Curriculum | `.doc-img` | object-fit | 390 | fill ×191 / cover ×17 | fill ×208 |
| Sensorial Curriculum | `.formula-divider` | border | 390 | 0px none rgb(128, 128, 128) ×1 |  ×1 |
| Sensorial Curriculum | `.formula-divider` | border-top | 390 | 0px none rgb(128, 128, 128) ×1 | 1px solid rgb(230, 230, 228) ×1 |
| Sensorial Curriculum | `.formula-divider` | margin | 390 | 0px ×1 | 50px 0px 0px ×1 |
| Sensorial Curriculum | `.formula-head` | margin-bottom | 390 | 10px ×1 | 0px ×1 |
| Sensorial Curriculum | `.grp-first` | margin-bottom | 390 | 4px ×42 | 0px ×42 |
| Sensorial Curriculum | `.grp-last` | margin-top | 390 | 4px ×42 | 2.97px ×26 / -1.55px ×7 / 11.97px ×4 … |
| Sensorial Curriculum | `.grp-mid` | margin-bottom | 390 | 4px ×38 | 0px ×38 |
| Sensorial Curriculum | `.grp-mid` | margin-top | 390 | 4px ×38 | 2.97px ×34 / -1.55px ×2 / 11.97px ×2 |
| Sensorial Curriculum | `.hero` | background-position | 390 | 50% 50% ×1 | 50% 22% ×1 |
| Sensorial Curriculum | `.hero` | overflow | 390 | visible ×1 | hidden ×1 |
| Sensorial Curriculum | `.lbl-blue` | color | 390 | rgb(4, 50, 255) ×13 | rgb(4, 50, 255) ×15 |
| Sensorial Curriculum | `.lbl-blue` | font-weight | 390 | 400 ×13 | 400 ×15 |
| Sensorial Curriculum | `.material-name` | border-top | 390 | 0px none rgb(238, 0, 0) ×29 / 0px none rgb(4, 50, 255) ×1 | 1px solid rgb(230, 230, 228) ×30 |
| Sensorial Curriculum | `.material-name` | font-size | 390 | 19px ×30 | 17px ×30 |
| Sensorial Curriculum | `.material-name` | margin | 390 | 20px 0px ×30 | 19px 0px -3.05px ×11 / -24.55px 0px -3.05px ×5 / -17px 0px -3.05px ×4 … |
| Sensorial Curriculum | `.material-name` | margin-bottom | 390 | 20px ×30 | -3.05px ×30 |
| Sensorial Curriculum | `.material-name` | margin-top | 390 | 20px ×30 | 19px ×11 / -24.55px ×5 / -17px ×4 … |
| Sensorial Curriculum | `.material-name` | padding-top | 390 | 0px ×30 | 22px ×30 |
| Sensorial Curriculum | `.materials-table` | margin | 390 | 0px 0px -8px ×1 | -22.03px 0px -15.05px ×1 |
| Sensorial Curriculum | `.mc-band` | margin-top | 390 | 1.98px ×1 | -34px ×1 |
| Sensorial Curriculum | `.micro-label` | margin | 390 | 20px 0px 5px ×66 / 0px 0px 5px ×16 / 0px 0px 10px ×1 … | 27.01px 0px 0px ×20 / 29.47px 0px 0px ×10 / 15.97px 0px 0px ×6 … |
| Sensorial Curriculum | `.micro-label` | margin-bottom | 390 | 5px ×82 / 10px ×2 | 0px ×84 |
| Sensorial Curriculum | `.micro-label` | margin-top | 390 | 20px ×66 / 0px ×17 / 30px ×1 | 27.01px ×20 / 29.47px ×10 / 15.97px ×6 … |
| Sensorial Curriculum | `.mm-float` | margin | 390 | 0px 0px 12px ×4 / 0px 0px 20px ×1 | 12px 0px 0px ×5 |
| Sensorial Curriculum | `.mm-float` | margin-top | 390 | 0px ×5 | 12px ×5 |
| Sensorial Curriculum | `.mm-float` | padding-top | 390 | 0px ×5 | 36px ×2 / 13.38px ×1 / 0.97px ×1 … |
| Sensorial Curriculum | `.mm-imgs` | display | 390 | flex ×36 / contents ×30 / block ×6 | flex ×37 / contents ×30 / block ×5 |
| Sensorial Curriculum | `.mm-imgs` | flex | 390 | 1 1 auto ×36 / 0 1 auto ×35 / 0 0 auto ×1 | 0 1 auto ×35 / 1 1 auto ×35 / 0 0 auto ×2 |
| Sensorial Curriculum | `.mm-imgs` | margin | 390 | 12px 0px 0px ×36 / 0px ×36 | 12px 0px 0px ×37 / 0px ×35 |
| Sensorial Curriculum | `.mm-imgs` | overflow-x | 390 | auto ×36 / visible ×36 | auto ×37 / visible ×35 |
| Sensorial Curriculum | `.mm-row` | gap | 390 | 10px ×30 | 10px ×29 / 19.2px ×1 |
| Sensorial Curriculum | `.mm-row` | margin | 390 | 12px 0px 0px ×29 / 0px ×1 | 12.97px 0px 0px ×20 / -2px 0px 0px ×3 / 8.47px 0px 0px ×2 … |
| Sensorial Curriculum | `.mm-row` | margin-top | 390 | 12px ×29 / 0px ×1 | 12.97px ×20 / -2px ×3 / 8.47px ×2 … |
| Sensorial Curriculum | `.mm-set` | margin | 390 | 30px 0px 0px ×17 / 20px 0px 16px ×8 / 20px 0px 0px ×8 … | 19px 0px 0px ×9 / 15.97px 0px 0px ×3 / -17px 0px 0px ×3 … |
| Sensorial Curriculum | `.ph` | scroll-snap-align | 390 | start ×208 | center ×208 |
| Sensorial Curriculum | `.preview-grid` | grid-template-rows | 390 | 44.0469px 52.0469px 52.0469px 52.0469px  ×1 | 52.0469px 52.0469px 52.0469px 52.0469px  ×1 |
| Sensorial Curriculum | `.preview-line` | margin | 390 | 8px 0px ×5 / 0px 0px 8px ×4 / 8px 0px 5px ×4 … | 11.99px 0px 0px ×6 / -1.3px 0px 0px ×2 / -1.55px 0px 0px ×2 … |
| Sensorial Curriculum | `.pullquote` | margin | 390 | 20px 38px ×2 | 0px 0px -8px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-bottom | 390 | 20px ×2 | -8px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-left | 390 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-right | 390 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-top | 390 | 20px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | padding | 390 | 0px ×2 | 19.25px 0px 0px ×2 |
| Sensorial Curriculum | `.ref-row` | border-bottom | 390 | 0px none rgb(43, 43, 43) ×16 | 0px none rgb(43, 43, 43) ×9 / 1px solid rgb(230, 230, 228) ×7 |
| Sensorial Curriculum | `.ref-row` | display | 390 | flex ×10 / grid ×6 | flex ×16 |
| Sensorial Curriculum | `.ref-row` | gap | 390 | 4px ×10 / 0px 18px ×6 | 4px ×16 |
| Sensorial Curriculum | `.ref-row` | padding | 390 | 0px ×16 | 16px 0px ×16 |
| Sensorial Curriculum | `.ref-table` | border-top | 390 | 0px none rgb(43, 43, 43) ×2 | 1px solid rgb(230, 230, 228) ×2 |
| Sensorial Curriculum | `.ref-table` | margin-top | 390 | 0px ×2 | -21.78px ×1 / 0px ×1 |
| Sensorial Curriculum | `.section` | container-type | 390 | normal ×15 | inline-size ×15 |
| Sensorial Curriculum | `.section` | margin-top | 390 | 20px ×15 | 0px ×12 / -2.27px ×1 / -7px ×1 … |
| Sensorial Curriculum | `.section` | padding-top | 390 | 20px ×15 | 0px ×15 |
| Sensorial Curriculum | `.sense` | margin-top | 390 | 20px ×7 | 0px ×4 |
| Sensorial Curriculum | `.site-foot-in` | padding | 390 | 0px 24px 28px ×1 | 14px 24px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-bottom | 390 | 28px ×1 | 14px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-top | 390 | 0px ×1 | 14px ×1 |
| Sensorial Curriculum | `.sub-label` | margin-bottom | 390 | 10px ×53 | 0px ×53 |
| Sensorial Curriculum | `.sub-label` | margin-top | 390 | 30px ×35 / 0px ×18 | 15.97px ×18 / 0px ×18 / 15.22px ×4 … |
| Sensorial Curriculum | `.tight-bottom` | margin-bottom | 390 | 0px ×81 / 5px ×26 / 4px ×4 | 0px ×111 |
| Sensorial Curriculum | `.tight-top` | margin-top | 390 | 0px ×132 / 5px ×1 | 23.95px ×66 / 0.97px ×40 / 0.47px ×9 … |
| Sensorial Curriculum | `.toc-label` | font-size | 390 | 22px ×1 | 19px ×1 |
| Sensorial Curriculum | `.toc-label` | line-height | 390 | 36.3px ×1 | 31.35px ×1 |
| Sensorial Curriculum | `.top` | font-size | 390 | 18px ×8 | 17px ×8 |
| Sensorial Curriculum | `a` | border-bottom | 390 | 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(143, 198, 255) ×8 … | 0px none rgb(231, 238, 245) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(143, 198, 255) ×8 … |
| Sensorial Curriculum | `a` | border-bottom-color | 390 | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … |
| Sensorial Curriculum | `a` | color | 390 | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … | rgb(231, 238, 245) ×25 / rgb(255, 255, 255) ×9 / rgb(143, 198, 255) ×8 … |
| Sensorial Curriculum | `a` | font-size | 390 | 17px ×35 / 18px ×15 / 21px ×1 … | 17px ×50 / 21px ×1 / 15px ×1 |
| Sensorial Curriculum | `a` | line-height | 390 | 22.1px ×33 / 29.7px ×8 / 24.3px ×7 … | 22.1px ×33 / 28.05px ×10 / 22.95px ×7 … |
| Sensorial Curriculum | `a` | outline | 390 | rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(143, 198, 255) none 3px ×8 … | rgb(231, 238, 245) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(143, 198, 255) none 3px ×8 … |
| Sensorial Curriculum | `div` | break-inside | 390 | auto ×691 / avoid ×13 | auto ×683 / avoid ×13 |
| Sensorial Curriculum | `div` | color | 390 | rgb(43, 43, 43) ×679 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … | rgb(43, 43, 43) ×672 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … |
| Sensorial Curriculum | `div` | font-size | 390 | 17px ×702 / 15px ×2 | 17px ×694 / 15px ×2 |
| Sensorial Curriculum | `div` | font-style | 390 | normal ×691 / italic ×13 | normal ×683 / italic ×13 |
| Sensorial Curriculum | `div` | margin | 390 | 0px ×351 / 20px 0px 5px ×66 / 12px 0px 0px ×65 … | 0px ×382 / 8px 0px 4px ×46 / 12px 0px 0px ×42 … |
| Sensorial Curriculum | `div` | padding | 390 | 0px ×677 / 4px 0px ×13 / 0px 0px 10px 14px ×8 … | 0px ×617 / 16px 0px ×16 / 4px 0px ×13 … |
| Sensorial Curriculum | `figcaption` | font-size | 390 | 15px ×3 | 16px ×3 |
| Sensorial Curriculum | `figcaption` | line-height | 390 | 19.5px ×3 | 20.8px ×3 |
| Sensorial Curriculum | `h2` | display | 390 | block ×15 | flow-root ×15 |
| Sensorial Curriculum | `h2` | font-size | 390 | 22px ×15 | 17px ×15 |
| Sensorial Curriculum | `h2` | line-height | 390 | 26.4px ×15 | 20.4px ×15 |
| Sensorial Curriculum | `h2` | margin | 390 | 0px 0px 20px ×15 | 0px 0px -9.39px ×14 / 0px ×1 |
| Sensorial Curriculum | `h2` | margin-bottom | 390 | 20px ×15 | -9.39px ×14 / 0px ×1 |
| Sensorial Curriculum | `h3` | font-size | 390 | 19px ×30 | 17px ×30 |
| Sensorial Curriculum | `img` | object-fit | 390 | fill ×191 / cover ×17 / contain ×1 | fill ×208 / contain ×1 |
| Sensorial Curriculum | `li` | counter-increment | 390 | none ×141 | none ×138 / mmn 1 ×3 |
| Sensorial Curriculum | `li` | margin | 390 | 0px ×123 / 8px 0px ×12 / 0px 0px 10px ×6 | 0px ×123 / 0px 0px 10px ×6 / 3.97px 0px 0px ×6 … |
| Sensorial Curriculum | `li` | margin-bottom | 390 | 0px ×123 / 8px ×12 / 10px ×6 | 0px ×135 / 10px ×6 |
| Sensorial Curriculum | `li` | margin-top | 390 | 0px ×129 / 8px ×12 | 0px ×129 / 3.97px ×6 / 11.97px ×2 … |
| Sensorial Curriculum | `li` | padding-left | 390 | 0px ×141 | 0px ×138 / 36.07px ×3 |
| Sensorial Curriculum | `li` | position | 390 | static ×125 / relative ×16 | static ×122 / relative ×19 |
| Sensorial Curriculum | `li::before` | position | 390 | absolute ×138 / static ×3 | absolute ×141 |
| Sensorial Curriculum | `ol` | counter-reset | 390 | none ×1 | mmn 0 ×1 |
| Sensorial Curriculum | `ol` | list-style | 390 | inside none decimal ×1 | outside none none ×1 |
| Sensorial Curriculum | `ol` | margin | 390 | 16px 0px 0px ×1 | 0px ×1 |
| Sensorial Curriculum | `p` | color | 390 | rgb(43, 43, 43) ×241 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … | rgb(43, 43, 43) ×247 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Sensorial Curriculum | `p` | font-family | 390 | "EB Garamond", Georgia, serif ×245 | "EB Garamond", Georgia, serif ×251 |
| Sensorial Curriculum | `p` | font-size | 390 | 17px ×244 / 22px ×1 | 17px ×244 / 0px ×4 / 2px ×2 … |
| Sensorial Curriculum | `p` | font-style | 390 | normal ×226 / italic ×19 | normal ×232 / italic ×19 |
| Sensorial Curriculum | `p` | font-weight | 390 | 400 ×244 / 500 ×1 | 400 ×250 / 500 ×1 |
| Sensorial Curriculum | `p` | line-height | 390 | 28.05px ×239 / 38px ×5 / 36.3px ×1 | 28.05px ×239 / 38px ×5 / 0px ×4 … |
| Sensorial Curriculum | `p` | margin | 390 | 0px ×81 / 0px 0px 4px ×42 / 4px 0px ×38 … | 23.95px 0px 0px ×66 / 2.97px 0px 0px ×60 / 0.97px 0px 0px ×40 … |
| Sensorial Curriculum | `p` | margin-left | 390 | 0px ×245 | 0px ×251 |
| Sensorial Curriculum | `p` | margin-top | 390 | 0px ×152 / 4px ×80 / 8px ×9 … | 23.95px ×66 / 2.97px ×60 / 0.97px ×40 … |
| Sensorial Curriculum | `p` | max-width | 390 | none ×242 / 860px ×3 | none ×251 |
| Sensorial Curriculum | `p` | padding-left | 390 | 0px ×243 / 24px ×2 | 0px ×249 / 24px ×2 |
| Sensorial Curriculum | `p` | text-align | 390 | left ×241 / center ×3 / start ×1 | left ×247 / center ×3 / start ×1 |
| Sensorial Curriculum | `p` | text-indent | 390 | 0px ×243 / 48px ×2 | 0px ×249 / 48px ×2 |
| Sensorial Curriculum | `p` | text-wrap | 390 | wrap ×242 / balance ×3 | wrap ×251 |
| Sensorial Curriculum | `span` | background | 390 | rgb(230, 230, 228) none repeat scroll 0% ×136 / rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×105 / rgb(43, 43, 43) none repeat scroll 0% 0% ×46 … | rgb(230, 230, 228) none repeat scroll 0% ×136 / rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×106 / rgb(43, 43, 43) none repeat scroll 0% 0% ×46 … |
| Sensorial Curriculum | `span` | border-radius | 390 | 50% ×183 / 0px ×105 | 50% ×183 / 0px ×106 |
| Sensorial Curriculum | `span` | color | 390 | rgb(43, 43, 43) ×184 / rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 … | rgb(43, 43, 43) ×184 / rgb(231, 238, 245) ×70 / rgb(143, 198, 255) ×8 … |
| Sensorial Curriculum | `span` | display | 390 | block ×265 / inline ×22 / inline-block ×1 | block ×265 / inline ×23 / inline-block ×1 |
| Sensorial Curriculum | `span` | flex | 390 | 0 1 auto ×288 | 0 1 auto ×289 |
| Sensorial Curriculum | `span` | font-family | 390 | "EB Garamond", Georgia, serif ×287 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×288 / Vollkorn, Georgia, serif ×1 |
| Sensorial Curriculum | `span` | font-size | 390 | 17px ×286 / 28px ×1 / 15px ×1 | 17px ×287 / 28px ×1 / 15px ×1 |
| Sensorial Curriculum | `span` | font-weight | 390 | 400 ×287 / 500 ×1 | 400 ×288 / 500 ×1 |
| Sensorial Curriculum | `span` | line-height | 390 | 28.05px ×205 / 22.1px ×81 / 33.6px ×1 … | 28.05px ×205 / 22.1px ×81 / 33.6px ×1 … |
| Sensorial Curriculum | `span` | margin-left | 390 | 0px ×287 / 4.76px ×1 | 0px ×288 / 4.76px ×1 |
| Sensorial Curriculum | `span` | min-width | 390 | auto ×183 / 0px ×105 | auto ×183 / 0px ×106 |
| Sensorial Curriculum | `span` | padding | 390 | 0px ×207 / 7px 0px ×81 | 0px ×208 / 7px 0px ×81 |
| Sensorial Curriculum | `span` | text-align | 390 | start ×184 / left ×104 | start ×184 / left ×104 / center ×1 |
| Sensorial Curriculum | `ul` | margin | 390 | 0px ×28 / 24px 0px 0px ×8 / 16px 0px ×2 | 0px ×30 / 24px 0px 0px ×8 |
| Sensorial Curriculum | `.article` | margin | 831 | 0px ×1 | 33px 0px 0px ×1 |
| Sensorial Curriculum | `.article` | margin-top | 831 | 0px ×1 | 33px ×1 |
| Sensorial Curriculum | `.article` | padding | 831 | 0px 40px 30.67px ×1 | 0px 40px 72px ×1 |
| Sensorial Curriculum | `.beige-rule` | background | 831 | rgb(217, 201, 171) none repeat scroll 0% ×7 | rgb(217, 201, 171) none repeat scroll 0% ×1 |
| Sensorial Curriculum | `.beige-rule` | clear | 831 | none ×7 | none ×1 |
| Sensorial Curriculum | `.beige-rule` | margin | 831 | 16.58px 0px -13.25px ×2 / -4.44px 0px 20px ×2 / 0px ×1 … | 0px ×1 |
| Sensorial Curriculum | `.beige-rule` | max-width | 831 | 100% ×7 | 100% ×1 |
| Sensorial Curriculum | `.beige-rule` | visibility | 831 | visible ×5 / hidden ×2 | hidden ×1 |
| Sensorial Curriculum | `.blindfold-label` | margin | 831 | 26px 0px 6px ×2 | 31.75px 0px 0px ×2 |
| Sensorial Curriculum | `.doc-img` | object-fit | 831 | fill ×191 / cover ×17 | fill ×208 |
| Sensorial Curriculum | `.formula-divider` | border | 831 | 0px none rgb(128, 128, 128) ×1 |  ×1 |
| Sensorial Curriculum | `.formula-divider` | border-top | 831 | 0px none rgb(128, 128, 128) ×1 | 1px solid rgb(230, 230, 228) ×1 |
| Sensorial Curriculum | `.formula-divider` | margin | 831 | 0px ×1 | 64px 0px 0px ×1 |
| Sensorial Curriculum | `.formula-head` | margin-bottom | 831 | 10px ×1 | 0px ×1 |
| Sensorial Curriculum | `.grp-first` | margin-bottom | 831 | 4px ×42 | 0px ×42 |
| Sensorial Curriculum | `.grp-last` | margin-top | 831 | 4px ×42 | 2.3px ×34 / 11.3px ×4 / -2.72px ×2 … |
| Sensorial Curriculum | `.grp-mid` | margin-bottom | 831 | 4px ×38 | 0px ×38 |
| Sensorial Curriculum | `.grp-mid` | margin-top | 831 | 4px ×38 | 2.3px ×34 / 11.3px ×2 / -2.72px ×1 … |
| Sensorial Curriculum | `.hero` | background-position | 831 | 50% 50% ×1 | 50% 22% ×1 |
| Sensorial Curriculum | `.hero` | overflow | 831 | visible ×1 | hidden ×1 |
| Sensorial Curriculum | `.lbl-blue` | color | 831 | rgb(4, 50, 255) ×13 | rgb(4, 50, 255) ×15 |
| Sensorial Curriculum | `.lbl-blue` | font-weight | 831 | 400 ×13 | 400 ×15 |
| Sensorial Curriculum | `.material-name` | border-top | 831 | 0px none rgb(238, 0, 0) ×29 / 0px none rgb(4, 50, 255) ×1 | 1px solid rgb(230, 230, 228) ×30 |
| Sensorial Curriculum | `.material-name` | font-size | 831 | 21px ×30 | 18px ×30 |
| Sensorial Curriculum | `.material-name` | margin | 831 | 30px 0px 20px ×17 / 26.58px 0px 20px ×5 / 22.47px 0px 20px ×3 … | 8.75px 0px -3.69px ×10 / -11.72px 0px -3.69px ×5 / -25.47px 0px -3.69px ×5 … |
| Sensorial Curriculum | `.material-name` | margin-bottom | 831 | 20px ×30 | -3.69px ×30 |
| Sensorial Curriculum | `.material-name` | margin-top | 831 | 30px ×17 / 26.58px ×5 / 22.47px ×3 … | 8.75px ×10 / -11.72px ×5 / -25.47px ×5 … |
| Sensorial Curriculum | `.material-name` | padding-top | 831 | 0px ×30 | 22px ×30 |
| Sensorial Curriculum | `.materials-table` | margin | 831 | 0px 0px -8px ×1 | -22.43px 0px -15.05px ×1 |
| Sensorial Curriculum | `.materials-table` | max-width | 831 | 820px ×1 | 640px ×1 |
| Sensorial Curriculum | `.mc-band` | margin-top | 831 | -10.67px ×1 | -12px ×1 |
| Sensorial Curriculum | `.micro-label` | margin | 831 | 20px 0px 5px ×66 / 0px 0px 5px ×16 / 0px 0px 10px ×1 … | 22.3px 0px 0px ×25 / 26.01px 0px 0px ×20 / 15.3px 0px 0px ×6 … |
| Sensorial Curriculum | `.micro-label` | margin-bottom | 831 | 5px ×82 / 10px ×2 | 0px ×84 |
| Sensorial Curriculum | `.micro-label` | margin-top | 831 | 20px ×66 / 0px ×17 / 30px ×1 | 22.3px ×25 / 26.01px ×20 / 15.3px ×6 … |
| Sensorial Curriculum | `.mm-float` | margin | 831 | 0px 0px 12px 32px ×4 / -45.39px 0px 20px 32px ×1 | 4px 0px 12px 32px ×2 / 0px 0px 12px 32px ×1 / -270.97px 0px 12px 32px ×1 … |
| Sensorial Curriculum | `.mm-float` | margin-top | 831 | 0px ×4 / -45.39px ×1 | 4px ×2 / 0px ×1 / -270.97px ×1 … |
| Sensorial Curriculum | `.mm-imgs` | flex | 831 | 1 1 auto ×36 / 0 1 auto ×35 / 0 0 auto ×1 | 0 1 auto ×35 / 1 1 auto ×35 / 0 0 auto ×2 |
| Sensorial Curriculum | `.mm-imgs` | justify-content | 831 | normal ×35 / center ×21 / flex-end ×16 | normal ×35 / center ×20 / flex-end ×16 … |
| Sensorial Curriculum | `.mm-imgs` | margin | 831 | 0px ×64 / 44.31px 0px 0px ×7 / 0px 0px 0px 32px ×1 | 0px ×69 / 0px 0px 0px 32px ×1 / 32px 0px 0px 48px ×1 … |
| Sensorial Curriculum | `.mm-imgs` | margin-left | 831 | 0px ×71 / 32px ×1 | 0px ×70 / 32px ×1 / 48px ×1 |
| Sensorial Curriculum | `.mm-row` | gap | 831 | 25.2968px ×30 | 10.01px ×13 / 10px ×4 / 14.18px ×1 … |
| Sensorial Curriculum | `.mm-row` | margin | 831 | 44.33px 0px 20px ×15 / 44.33px 0px 0px ×9 / 20px 0px ×2 … | 37.35px 0px 0px ×23 / 48px 0px 0px ×4 / 32.6px 0px 0px ×2 … |
| Sensorial Curriculum | `.mm-row` | margin-top | 831 | 44.33px ×24 / 20px ×2 / 32px ×2 … | 37.35px ×23 / 48px ×4 / 32.6px ×2 … |
| Sensorial Curriculum | `.mm-set` | display | 831 | flex ×30 / block ×7 | flex ×36 / block ×1 |
| Sensorial Curriculum | `.mm-set` | margin | 831 | 30px 0px 0px ×17 / 20px 0px 0px ×10 / 20px 0px 16px ×6 … | 15.3px 0px 0px ×3 / 10.8px 0px 0px ×3 / -1.22px 0px 0px ×3 … |
| Sensorial Curriculum | `.mm-text` | max-width | 831 | none ×9 / 599.578px ×6 / 466.168px ×4 … | none ×3 / 599.578px ×3 / 470.273px ×2 … |
| Sensorial Curriculum | `.np` | font-size | 831 | 17px ×74 | 18px ×74 |
| Sensorial Curriculum | `.np` | line-height | 831 | 22.1px ×74 | 23.4px ×74 |
| Sensorial Curriculum | `.preview-grid` | grid-template-rows | 831 | 44.0469px 52.0469px 52.0469px 52.0469px  ×1 | 52.0469px 52.0469px 52.0469px 52.0469px  ×1 |
| Sensorial Curriculum | `.preview-line` | font-size | 831 | 17px ×15 | 18px ×15 |
| Sensorial Curriculum | `.preview-line` | margin | 831 | 8px 0px ×5 / 0px 0px 8px ×4 / 8px 0px 5px ×4 … | 10.99px 0px 0px ×6 / -2.47px 0px 0px ×4 / 1.55px 0px 0px ×2 … |
| Sensorial Curriculum | `.pullquote` | margin | 831 | 20px 38px ×2 | 0px 0px -9px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-bottom | 831 | 20px ×2 | -9px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-left | 831 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-right | 831 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-top | 831 | 20px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | padding | 831 | 0px ×2 | 18.75px 0px 0px ×2 |
| Sensorial Curriculum | `.ref-row` | border-bottom | 831 | 0px none rgb(43, 43, 43) ×16 | 0px none rgb(43, 43, 43) ×9 / 1px solid rgb(230, 230, 228) ×7 |
| Sensorial Curriculum | `.ref-row` | display | 831 | flex ×10 / grid ×6 | flex ×16 |
| Sensorial Curriculum | `.ref-row` | gap | 831 | 24px ×10 / 0px 18px ×6 | 24px ×16 |
| Sensorial Curriculum | `.ref-row` | padding | 831 | 0px ×16 | 16px 0px ×16 |
| Sensorial Curriculum | `.ref-table` | border-top | 831 | 0px none rgb(43, 43, 43) ×2 | 1px solid rgb(230, 230, 228) ×2 |
| Sensorial Curriculum | `.ref-table` | margin-top | 831 | 0px ×2 | -22.93px ×1 / 0px ×1 |
| Sensorial Curriculum | `.section` | container-type | 831 | normal ×15 | inline-size ×15 |
| Sensorial Curriculum | `.section` | margin-top | 831 | 20px ×15 | 0px ×12 / -3.25px ×1 / -8px ×1 … |
| Sensorial Curriculum | `.section` | padding-top | 831 | 20px ×15 | 0px ×15 |
| Sensorial Curriculum | `.sense` | margin-top | 831 | 20px ×7 | 0px ×4 |
| Sensorial Curriculum | `.site-foot-in` | padding | 831 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-bottom | 831 | 28px ×1 | 17.625px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-top | 831 | 0px ×1 | 17.625px ×1 |
| Sensorial Curriculum | `.site-name` | font-size | 831 | 21px ×1 | 25px ×1 |
| Sensorial Curriculum | `.sub-label` | margin-bottom | 831 | 10px ×53 | 0px ×53 |
| Sensorial Curriculum | `.sub-label` | margin-top | 831 | 30px ×35 / 0px ×18 | 15.3px ×23 / 0px ×18 / 14.55px ×4 … |
| Sensorial Curriculum | `.tight-bottom` | margin-bottom | 831 | 0px ×92 / 5px ×15 / 4px ×4 | 0px ×111 |
| Sensorial Curriculum | `.tight-top` | margin-top | 831 | 0px ×132 / 5px ×1 | 22.3px ×66 / 0.33px ×29 / 0.3px ×13 … |
| Sensorial Curriculum | `.toc-label` | font-size | 831 | 24px ×1 | 20px ×1 |
| Sensorial Curriculum | `.toc-label` | line-height | 831 | 39.6px ×1 | 33px ×1 |
| Sensorial Curriculum | `a` | border-bottom | 831 | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×7 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×8 … |
| Sensorial Curriculum | `a` | border-bottom-color | 831 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×7 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … |
| Sensorial Curriculum | `a` | color | 831 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×7 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … |
| Sensorial Curriculum | `a` | font-size | 831 | 17px ×33 / 18px ×10 / 19px ×7 … | 18px ×50 / 25px ×1 / 15px ×1 |
| Sensorial Curriculum | `a` | line-height | 831 | 22.1px ×33 / 29.7px ×10 / 25.65px ×7 … | 23.4px ×33 / 29.7px ×10 / 24.3px ×7 … |
| Sensorial Curriculum | `a` | outline | 831 | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×7 … | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×8 … |
| Sensorial Curriculum | `div` | break-inside | 831 | auto ×645 / avoid ×13 | auto ×640 / avoid ×13 |
| Sensorial Curriculum | `div` | color | 831 | rgb(43, 43, 43) ×633 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … | rgb(43, 43, 43) ×629 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … |
| Sensorial Curriculum | `div` | font-size | 831 | 18px ×643 / 17px ×13 / 15px ×2 | 18px ×638 / 17px ×13 / 15px ×2 |
| Sensorial Curriculum | `div` | font-style | 831 | normal ×645 / italic ×13 | normal ×640 / italic ×13 |
| Sensorial Curriculum | `div` | margin | 831 | 0px ×378 / 20px 0px 5px ×66 / 30px 0px 10px ×46 … | 0px ×419 / 15.3px 0px 0px ×32 / 22.3px 0px 0px ×28 … |
| Sensorial Curriculum | `div` | padding | 831 | 0px ×631 / 4px 0px ×13 / 0px 0px 10px 14px ×8 … | 0px ×609 / 16px 0px ×16 / 4px 0px ×13 … |
| Sensorial Curriculum | `figcaption` | font-size | 831 | 15px ×3 | 16px ×3 |
| Sensorial Curriculum | `figcaption` | line-height | 831 | 19.5px ×3 | 20.8px ×3 |
| Sensorial Curriculum | `h2` | display | 831 | block ×15 | flow-root ×15 |
| Sensorial Curriculum | `h2` | font-size | 831 | 24px ×15 | 18px ×15 |
| Sensorial Curriculum | `h2` | line-height | 831 | 28.8px ×15 | 21.6px ×15 |
| Sensorial Curriculum | `h2` | margin | 831 | 0px 0px 20px ×15 | 0px 0px -9.59px ×10 / -2px 0px -9.59px ×3 / 0px ×2 |
| Sensorial Curriculum | `h2` | margin-bottom | 831 | 20px ×15 | -9.59px ×13 / 0px ×2 |
| Sensorial Curriculum | `h3` | font-size | 831 | 21px ×30 | 18px ×30 |
| Sensorial Curriculum | `img` | object-fit | 831 | fill ×191 / cover ×17 / contain ×1 | fill ×208 / contain ×1 |
| Sensorial Curriculum | `li` | counter-increment | 831 | none ×141 | none ×138 / mmn 1 ×3 |
| Sensorial Curriculum | `li` | margin | 831 | 0px ×123 / 8px 0px ×12 / 0px 0px 10px ×6 | 0px ×123 / 3.3px 0px 0px ×7 / 0px 0px 10px ×6 … |
| Sensorial Curriculum | `li` | margin-bottom | 831 | 0px ×123 / 8px ×12 / 10px ×6 | 0px ×135 / 10px ×6 |
| Sensorial Curriculum | `li` | margin-top | 831 | 0px ×129 / 8px ×12 | 0px ×129 / 3.3px ×7 / 2.55px ×2 … |
| Sensorial Curriculum | `li` | padding-left | 831 | 0px ×141 | 0px ×138 / 36.78px ×3 |
| Sensorial Curriculum | `li` | position | 831 | static ×125 / relative ×16 | static ×122 / relative ×19 |
| Sensorial Curriculum | `li` | text-align | 831 | left ×125 / justify ×16 | left ×122 / justify ×19 |
| Sensorial Curriculum | `li::before` | position | 831 | absolute ×138 / static ×3 | absolute ×141 |
| Sensorial Curriculum | `li::before` | text-align | 831 | left ×125 / justify ×16 | left ×122 / justify ×19 |
| Sensorial Curriculum | `ol` | counter-reset | 831 | none ×1 | mmn 0 ×1 |
| Sensorial Curriculum | `ol` | list-style | 831 | inside none decimal ×1 | outside none none ×1 |
| Sensorial Curriculum | `ol` | margin | 831 | 16px 0px 0px ×1 | 0px ×1 |
| Sensorial Curriculum | `p` | color | 831 | rgb(43, 43, 43) ×241 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … | rgb(43, 43, 43) ×247 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Sensorial Curriculum | `p` | font-family | 831 | "EB Garamond", Georgia, serif ×245 | "EB Garamond", Georgia, serif ×251 |
| Sensorial Curriculum | `p` | font-size | 831 | 18px ×229 / 17px ×15 / 24px ×1 | 18px ×244 / 0px ×4 / 2px ×2 … |
| Sensorial Curriculum | `p` | font-style | 831 | normal ×226 / italic ×19 | normal ×232 / italic ×19 |
| Sensorial Curriculum | `p` | font-weight | 831 | 400 ×244 / 500 ×1 | 400 ×250 / 500 ×1 |
| Sensorial Curriculum | `p` | line-height | 831 | 29.7px ×224 / 28.05px ×15 / 40px ×5 … | 29.7px ×239 / 40px ×5 / 0px ×4 … |
| Sensorial Curriculum | `p` | margin | 831 | 0px ×93 / 0px 0px 4px ×42 / 4px 0px 0px ×39 … | 2.3px 0px 0px ×69 / 22.3px 0px 0px ×66 / 0.33px 0px 0px ×29 … |
| Sensorial Curriculum | `p` | margin-left | 831 | 0px ×245 | 0px ×251 |
| Sensorial Curriculum | `p` | margin-top | 831 | 0px ×152 / 4px ×80 / 8px ×9 … | 2.3px ×69 / 22.3px ×66 / 0.33px ×29 … |
| Sensorial Curriculum | `p` | max-width | 831 | none ×242 / 860px ×3 | none ×251 |
| Sensorial Curriculum | `p` | padding-left | 831 | 0px ×243 / 48px ×2 | 0px ×249 / 48px ×2 |
| Sensorial Curriculum | `p` | text-align | 831 | justify ×239 / center ×3 / left ×2 … | justify ×239 / start ×7 / center ×3 … |
| Sensorial Curriculum | `p` | text-indent | 831 | 0px ×243 / 48px ×2 | 0px ×249 / 48px ×2 |
| Sensorial Curriculum | `p` | text-wrap | 831 | wrap ×242 / balance ×3 | wrap ×251 |
| Sensorial Curriculum | `span` | background | 831 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×105 / rgb(255, 255, 255) none repeat scroll 0% ×1 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×106 / rgb(255, 255, 255) none repeat scroll 0% ×1 |
| Sensorial Curriculum | `span` | border-radius | 831 | 0px ×105 / 50% ×1 | 0px ×106 / 50% ×1 |
| Sensorial Curriculum | `span` | color | 831 | rgb(43, 43, 43) ×72 / rgb(4, 50, 255) ×14 / rgb(255, 0, 0) ×3 … | rgb(43, 43, 43) ×72 / rgb(4, 50, 255) ×14 / rgb(255, 0, 0) ×3 … |
| Sensorial Curriculum | `span` | display | 831 | block ×83 / inline ×22 / inline-block ×1 | block ×83 / inline ×23 / inline-block ×1 |
| Sensorial Curriculum | `span` | flex | 831 | 0 1 auto ×106 | 0 1 auto ×107 |
| Sensorial Curriculum | `span` | font-family | 831 | "EB Garamond", Georgia, serif ×105 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×106 / Vollkorn, Georgia, serif ×1 |
| Sensorial Curriculum | `span` | font-size | 831 | 17px ×81 / 18px ×23 / 40px ×1 … | 18px ×105 / 40px ×1 / 15px ×1 |
| Sensorial Curriculum | `span` | font-weight | 831 | 400 ×105 / 500 ×1 | 400 ×106 / 500 ×1 |
| Sensorial Curriculum | `span` | line-height | 831 | 22.1px ×81 / 29.7px ×23 / 48px ×1 … | 23.4px ×81 / 29.7px ×23 / 48px ×1 … |
| Sensorial Curriculum | `span` | margin-left | 831 | 0px ×105 / 5.04px ×1 | 0px ×106 / 5.04px ×1 |
| Sensorial Curriculum | `span` | min-width | 831 | 0px ×105 / auto ×1 | 0px ×106 / auto ×1 |
| Sensorial Curriculum | `span` | padding | 831 | 7px 0px ×81 / 0px ×25 | 7px 0px ×81 / 0px ×26 |
| Sensorial Curriculum | `span` | text-align | 831 | left ×81 / justify ×23 / start ×2 | left ×81 / justify ×23 / start ×2 … |
| Sensorial Curriculum | `ul` | margin | 831 | 0px ×28 / 24px 0px 0px ×8 / 16px 0px ×2 | 0px ×30 / 24px 0px 0px ×8 |
| Sensorial Curriculum | `.article` | margin | 1440 | 0px 110px ×1 | 33px 110px 0px ×1 |
| Sensorial Curriculum | `.article` | margin-top | 1440 | 0px ×1 | 33px ×1 |
| Sensorial Curriculum | `.article` | padding | 1440 | 0px 40px 30.67px ×1 | 0px 40px 72px ×1 |
| Sensorial Curriculum | `.beige-rule` | background | 1440 | rgb(217, 201, 171) none repeat scroll 0% ×7 | rgb(217, 201, 171) none repeat scroll 0% ×1 |
| Sensorial Curriculum | `.beige-rule` | clear | 1440 | none ×7 | none ×1 |
| Sensorial Curriculum | `.beige-rule` | margin | 1440 | -4.44px 0px 20px ×2 / 0px ×1 / 19.97px 0px -13.25px ×1 … | 0px ×1 |
| Sensorial Curriculum | `.beige-rule` | max-width | 1440 | 100% ×7 | 100% ×1 |
| Sensorial Curriculum | `.beige-rule` | visibility | 1440 | visible ×5 / hidden ×2 | hidden ×1 |
| Sensorial Curriculum | `.blindfold-label` | margin | 1440 | 26px 0px 6px ×2 | 31.75px 0px 0px ×2 |
| Sensorial Curriculum | `.doc-img` | object-fit | 1440 | fill ×191 / cover ×17 | fill ×208 |
| Sensorial Curriculum | `.formula-divider` | border | 1440 | 0px none rgb(128, 128, 128) ×1 |  ×1 |
| Sensorial Curriculum | `.formula-divider` | border-top | 1440 | 0px none rgb(128, 128, 128) ×1 | 1px solid rgb(230, 230, 228) ×1 |
| Sensorial Curriculum | `.formula-divider` | margin | 1440 | 0px ×1 | 64px 0px 0px ×1 |
| Sensorial Curriculum | `.formula-head` | margin-bottom | 1440 | 10px ×1 | 0px ×1 |
| Sensorial Curriculum | `.grp-first` | margin-bottom | 1440 | 4px ×42 | 0px ×42 |
| Sensorial Curriculum | `.grp-last` | margin-top | 1440 | 4px ×42 | 2.3px ×34 / 11.3px ×4 / -2.47px ×2 … |
| Sensorial Curriculum | `.grp-mid` | margin-bottom | 1440 | 4px ×38 | 0px ×38 |
| Sensorial Curriculum | `.grp-mid` | margin-top | 1440 | 4px ×38 | 2.3px ×36 / 11.3px ×2 |
| Sensorial Curriculum | `.hero` | background-position | 1440 | 50% 50% ×1 | 50% 22% ×1 |
| Sensorial Curriculum | `.hero` | overflow | 1440 | visible ×1 | hidden ×1 |
| Sensorial Curriculum | `.lbl-blue` | color | 1440 | rgb(4, 50, 255) ×13 | rgb(4, 50, 255) ×15 |
| Sensorial Curriculum | `.lbl-blue` | font-weight | 1440 | 400 ×13 | 400 ×15 |
| Sensorial Curriculum | `.material-name` | border-top | 1440 | 0px none rgb(238, 0, 0) ×29 / 0px none rgb(4, 50, 255) ×1 | 1px solid rgb(230, 230, 228) ×30 |
| Sensorial Curriculum | `.material-name` | font-size | 1440 | 21px ×30 | 18px ×30 |
| Sensorial Curriculum | `.material-name` | margin | 1440 | 30px 0px 20px ×14 / 26.58px 0px 20px ×8 / 22.47px 0px 20px ×3 … | 8.75px 0px -3.69px ×10 / -11.72px 0px -3.69px ×6 / -25.47px 0px -3.69px ×5 … |
| Sensorial Curriculum | `.material-name` | margin-bottom | 1440 | 20px ×30 | -3.69px ×30 |
| Sensorial Curriculum | `.material-name` | margin-top | 1440 | 30px ×14 / 26.58px ×8 / 22.47px ×3 … | 8.75px ×10 / -11.72px ×6 / -25.47px ×5 … |
| Sensorial Curriculum | `.material-name` | padding-top | 1440 | 0px ×30 | 22px ×30 |
| Sensorial Curriculum | `.materials-table` | margin | 1440 | 0px 0px -8px ×1 | -22.43px 0px -15.05px ×1 |
| Sensorial Curriculum | `.materials-table` | max-width | 1440 | 820px ×1 | 640px ×1 |
| Sensorial Curriculum | `.mc-band` | margin-top | 1440 | -10.67px ×1 | -12px ×1 |
| Sensorial Curriculum | `.micro-label` | margin | 1440 | 20px 0px 5px ×66 / 0px 0px 5px ×16 / 0px 0px 10px ×1 … | 22.3px 0px 0px ×25 / 26.01px 0px 0px ×20 / 15.3px 0px 0px ×7 … |
| Sensorial Curriculum | `.micro-label` | margin-bottom | 1440 | 5px ×82 / 10px ×2 | 0px ×84 |
| Sensorial Curriculum | `.micro-label` | margin-top | 1440 | 20px ×66 / 0px ×17 / 30px ×1 | 22.3px ×25 / 26.01px ×20 / 15.3px ×7 … |
| Sensorial Curriculum | `.mm-float` | margin | 1440 | 0px 0px 12px 32px ×4 / -45.39px 0px 20px 32px ×1 | 4px 0px 12px 32px ×2 / 0px 0px 12px 32px ×1 / -319.62px 0px 12px 32px ×1 … |
| Sensorial Curriculum | `.mm-float` | margin-top | 1440 | 0px ×4 / -45.39px ×1 | 4px ×2 / 0px ×1 / -319.62px ×1 … |
| Sensorial Curriculum | `.mm-imgs` | flex | 1440 | 1 1 auto ×36 / 0 1 auto ×35 / 0 0 auto ×1 | 0 1 auto ×35 / 1 1 auto ×35 / 0 0 auto ×2 |
| Sensorial Curriculum | `.mm-imgs` | justify-content | 1440 | normal ×35 / center ×20 / flex-end ×17 | normal ×35 / center ×21 / flex-end ×15 … |
| Sensorial Curriculum | `.mm-imgs` | margin | 1440 | 0px ×71 / 0px 0px 0px 32px ×1 | 0px ×66 / 24px 0px 0px ×4 / 0px 0px 0px 32px ×1 … |
| Sensorial Curriculum | `.mm-imgs` | margin-left | 1440 | 0px ×71 / 32px ×1 | 0px ×70 / 32px ×1 / 48px ×1 |
| Sensorial Curriculum | `.mm-row` | gap | 1440 | 38.4px ×30 | 38.4px ×25 / 46.25px ×1 / 45.68px ×1 … |
| Sensorial Curriculum | `.mm-row` | margin | 1440 | 44.33px 0px 20px ×15 / 44.33px 0px 0px ×9 / 20px 0px ×2 … | 37.35px 0px 0px ×23 / 48px 0px 0px ×4 / 0px ×1 … |
| Sensorial Curriculum | `.mm-row` | margin-top | 1440 | 44.33px ×24 / 20px ×2 / 32px ×2 … | 37.35px ×23 / 48px ×4 / 0px ×1 … |
| Sensorial Curriculum | `.mm-set` | display | 1440 | flex ×37 | flex ×33 / block ×4 |
| Sensorial Curriculum | `.mm-set` | margin | 1440 | 30px 0px 0px ×17 / 20px 0px 0px ×10 / 20px 0px 16px ×6 … | 15.3px 0px 0px ×4 / 7.3px 0px 0px ×4 / 32px 0px 0px ×3 … |
| Sensorial Curriculum | `.mm-text` | max-width | 1440 | 988.578px ×6 / 855.168px ×4 / 918.567px ×3 … | none ×6 / 859.273px ×2 / 918.567px ×2 … |
| Sensorial Curriculum | `.np` | font-size | 1440 | 17px ×74 | 18px ×74 |
| Sensorial Curriculum | `.np` | line-height | 1440 | 22.1px ×74 | 23.4px ×74 |
| Sensorial Curriculum | `.preview-grid` | grid-template-rows | 1440 | 44.0469px 52.0469px 52.0469px 52.0469px  ×1 | 52.0469px 52.0469px 52.0469px 52.0469px  ×1 |
| Sensorial Curriculum | `.preview-line` | font-size | 1440 | 17px ×15 | 18px ×15 |
| Sensorial Curriculum | `.preview-line` | margin | 1440 | 8px 0px ×5 / 0px 0px 8px ×4 / 8px 0px 5px ×4 … | 10.99px 0px 0px ×6 / -2.47px 0px 0px ×4 / 1.55px 0px 0px ×2 … |
| Sensorial Curriculum | `.pullquote` | margin | 1440 | 20px 38px ×2 | 0px 0px -9px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-bottom | 1440 | 20px ×2 | -9px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-left | 1440 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-right | 1440 | 38px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | margin-top | 1440 | 20px ×2 | 0px ×2 |
| Sensorial Curriculum | `.pullquote` | padding | 1440 | 0px ×2 | 18.75px 0px 0px ×2 |
| Sensorial Curriculum | `.ref-row` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×16 | 0px none rgb(43, 43, 43) ×9 / 1px solid rgb(230, 230, 228) ×7 |
| Sensorial Curriculum | `.ref-row` | display | 1440 | flex ×10 / grid ×6 | flex ×16 |
| Sensorial Curriculum | `.ref-row` | gap | 1440 | 24px ×10 / 0px 18px ×6 | 24px ×16 |
| Sensorial Curriculum | `.ref-row` | padding | 1440 | 0px ×16 | 16px 0px ×16 |
| Sensorial Curriculum | `.ref-table` | border-top | 1440 | 0px none rgb(43, 43, 43) ×2 | 1px solid rgb(230, 230, 228) ×2 |
| Sensorial Curriculum | `.ref-table` | margin-top | 1440 | 0px ×2 | -22.93px ×1 / 0px ×1 |
| Sensorial Curriculum | `.section` | container-type | 1440 | normal ×15 | inline-size ×15 |
| Sensorial Curriculum | `.section` | margin-top | 1440 | 20px ×15 | 0px ×12 / -3.25px ×1 / -8px ×1 … |
| Sensorial Curriculum | `.section` | padding-top | 1440 | 20px ×15 | 0px ×15 |
| Sensorial Curriculum | `.sense` | margin-top | 1440 | 20px ×7 | 0px ×4 |
| Sensorial Curriculum | `.site-foot-in` | padding | 1440 | 0px 40px 28px ×1 | 17.625px 40px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-bottom | 1440 | 28px ×1 | 17.625px ×1 |
| Sensorial Curriculum | `.site-foot-in` | padding-top | 1440 | 0px ×1 | 17.625px ×1 |
| Sensorial Curriculum | `.sub-label` | margin-bottom | 1440 | 10px ×53 | 0px ×53 |
| Sensorial Curriculum | `.sub-label` | margin-top | 1440 | 30px ×35 / 0px ×18 | 15.3px ×23 / 0px ×18 / 14.55px ×3 … |
| Sensorial Curriculum | `.tight-bottom` | margin-bottom | 1440 | 0px ×92 / 5px ×15 / 4px ×4 | 0px ×111 |
| Sensorial Curriculum | `.tight-top` | margin-top | 1440 | 0px ×132 / 5px ×1 | 22.3px ×66 / 0.33px ×29 / 0.3px ×13 … |
| Sensorial Curriculum | `.toc-label` | font-size | 1440 | 24px ×1 | 20px ×1 |
| Sensorial Curriculum | `.toc-label` | line-height | 1440 | 39.6px ×1 | 33px ×1 |
| Sensorial Curriculum | `.top` | border-bottom | 1440 | 1px solid rgba(0, 0, 0, 0) ×7 / 1px solid rgb(255, 255, 255) ×1 | 0px none rgb(255, 255, 255) ×8 |
| Sensorial Curriculum | `.top` | font-size | 1440 | 17px ×8 | 18px ×8 |
| Sensorial Curriculum | `.top` | padding | 1440 | 6px 0px ×8 | 6px 0px 7.5px ×8 |
| Sensorial Curriculum | `.top` | text-decoration | 1440 | none ×8 | none ×7 / underline ×1 |
| Sensorial Curriculum | `.top` | text-underline-offset | 1440 | auto ×8 | auto ×7 / 4px ×1 |
| Sensorial Curriculum | `a` | border-bottom | 1440 | 0px none rgb(43, 43, 43) ×25 / 1px solid rgba(0, 0, 0, 0) ×14 / 0px none rgb(4, 50, 255) ×8 … | 0px none rgb(43, 43, 43) ×25 / 0px none rgb(255, 255, 255) ×9 / 0px none rgb(4, 50, 255) ×9 … |
| Sensorial Curriculum | `a` | border-bottom-color | 1440 | rgb(43, 43, 43) ×25 / rgba(0, 0, 0, 0) ×14 / rgb(4, 50, 255) ×8 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×9 … |
| Sensorial Curriculum | `a` | color | 1440 | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×8 … | rgb(43, 43, 43) ×25 / rgb(255, 255, 255) ×9 / rgb(4, 50, 255) ×9 … |
| Sensorial Curriculum | `a` | font-size | 1440 | 17px ×41 / 19px ×7 / 18px ×2 … | 18px ×50 / 25px ×1 / 15px ×1 |
| Sensorial Curriculum | `a` | line-height | 1440 | 22.1px ×33 / 28.05px ×8 / 25.65px ×7 … | 23.4px ×33 / 29.7px ×10 / 24.3px ×7 … |
| Sensorial Curriculum | `a` | outline | 1440 | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×8 … | rgb(43, 43, 43) none 3px ×25 / rgb(255, 255, 255) none 3px ×9 / rgb(4, 50, 255) none 3px ×9 … |
| Sensorial Curriculum | `a` | padding | 1440 | 8px 0px ×33 / 0px ×11 / 6px 0px ×8 | 8px 0px ×33 / 0px ×11 / 6px 0px 7.5px ×8 |
| Sensorial Curriculum | `a` | text-decoration | 1440 | none ×48 / underline ×4 | none ×47 / underline ×5 |
| Sensorial Curriculum | `a` | text-underline-offset | 1440 | auto ×51 / 3px ×1 | auto ×50 / 4px ×1 / 3px ×1 |
| Sensorial Curriculum | `div` | break-inside | 1440 | auto ×645 / avoid ×13 | auto ×640 / avoid ×13 |
| Sensorial Curriculum | `div` | color | 1440 | rgb(43, 43, 43) ×633 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … | rgb(43, 43, 43) ×629 / rgb(4, 50, 255) ×17 / rgb(238, 0, 0) ×5 … |
| Sensorial Curriculum | `div` | font-size | 1440 | 18px ×643 / 17px ×13 / 15px ×2 | 18px ×638 / 17px ×13 / 15px ×2 |
| Sensorial Curriculum | `div` | font-style | 1440 | normal ×645 / italic ×13 | normal ×640 / italic ×13 |
| Sensorial Curriculum | `div` | margin | 1440 | 0px ×398 / 20px 0px 5px ×66 / 30px 0px 10px ×46 … | 0px ×430 / 15.3px 0px 0px ×34 / 22.3px 0px 0px ×28 … |
| Sensorial Curriculum | `div` | padding | 1440 | 0px ×631 / 4px 0px ×13 / 26px 40px 30px ×8 … | 0px ×609 / 16px 0px ×16 / 4px 0px ×13 … |
| Sensorial Curriculum | `figcaption` | font-size | 1440 | 15px ×3 | 16px ×3 |
| Sensorial Curriculum | `figcaption` | line-height | 1440 | 19.5px ×3 | 20.8px ×3 |
| Sensorial Curriculum | `h2` | display | 1440 | block ×15 | flow-root ×15 |
| Sensorial Curriculum | `h2` | font-size | 1440 | 24px ×15 | 18px ×15 |
| Sensorial Curriculum | `h2` | line-height | 1440 | 28.8px ×15 | 21.6px ×15 |
| Sensorial Curriculum | `h2` | margin | 1440 | 0px 0px 20px ×15 | 0px 0px -9.59px ×10 / -2px 0px -9.59px ×3 / 0px ×2 |
| Sensorial Curriculum | `h2` | margin-bottom | 1440 | 20px ×15 | -9.59px ×13 / 0px ×2 |
| Sensorial Curriculum | `h3` | font-size | 1440 | 21px ×30 | 18px ×30 |
| Sensorial Curriculum | `img` | object-fit | 1440 | fill ×191 / cover ×17 / contain ×1 | fill ×208 / contain ×1 |
| Sensorial Curriculum | `li` | counter-increment | 1440 | none ×141 | none ×138 / mmn 1 ×3 |
| Sensorial Curriculum | `li` | margin | 1440 | 0px ×123 / 8px 0px ×12 / 0px 0px 10px ×6 | 0px ×123 / 3.3px 0px 0px ×7 / 0px 0px 10px ×6 … |
| Sensorial Curriculum | `li` | margin-bottom | 1440 | 0px ×123 / 8px ×12 / 10px ×6 | 0px ×135 / 10px ×6 |
| Sensorial Curriculum | `li` | margin-top | 1440 | 0px ×129 / 8px ×12 | 0px ×129 / 3.3px ×7 / 11.3px ×2 … |
| Sensorial Curriculum | `li` | padding-left | 1440 | 0px ×141 | 0px ×138 / 36.78px ×3 |
| Sensorial Curriculum | `li` | position | 1440 | static ×125 / relative ×16 | static ×122 / relative ×19 |
| Sensorial Curriculum | `li` | text-align | 1440 | left ×125 / justify ×16 | left ×122 / justify ×19 |
| Sensorial Curriculum | `li::before` | position | 1440 | absolute ×138 / static ×3 | absolute ×141 |
| Sensorial Curriculum | `li::before` | text-align | 1440 | left ×125 / justify ×16 | left ×122 / justify ×19 |
| Sensorial Curriculum | `ol` | counter-reset | 1440 | none ×1 | mmn 0 ×1 |
| Sensorial Curriculum | `ol` | list-style | 1440 | inside none decimal ×1 | outside none none ×1 |
| Sensorial Curriculum | `ol` | margin | 1440 | 16px 0px 0px ×1 | 0px ×1 |
| Sensorial Curriculum | `p` | color | 1440 | rgb(43, 43, 43) ×241 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … | rgb(43, 43, 43) ×247 / rgb(255, 255, 255) ×2 / rgb(4, 50, 255) ×1 … |
| Sensorial Curriculum | `p` | font-family | 1440 | "EB Garamond", Georgia, serif ×245 | "EB Garamond", Georgia, serif ×251 |
| Sensorial Curriculum | `p` | font-size | 1440 | 18px ×229 / 17px ×15 / 24px ×1 | 18px ×244 / 0px ×4 / 2px ×2 … |
| Sensorial Curriculum | `p` | font-style | 1440 | normal ×226 / italic ×19 | normal ×232 / italic ×19 |
| Sensorial Curriculum | `p` | font-weight | 1440 | 400 ×244 / 500 ×1 | 400 ×250 / 500 ×1 |
| Sensorial Curriculum | `p` | line-height | 1440 | 29.7px ×224 / 28.05px ×15 / 40px ×5 … | 29.7px ×239 / 40px ×5 / 0px ×4 … |
| Sensorial Curriculum | `p` | margin | 1440 | 0px ×90 / 0px 0px 4px ×42 / 4px 0px 0px ×39 … | 2.3px 0px 0px ×71 / 22.3px 0px 0px ×66 / 0.33px 0px 0px ×29 … |
| Sensorial Curriculum | `p` | margin-left | 1440 | 0px ×242 / 250px ×3 | 0px ×251 |
| Sensorial Curriculum | `p` | margin-top | 1440 | 0px ×152 / 4px ×80 / 8px ×9 … | 2.3px ×71 / 22.3px ×66 / 0.33px ×29 … |
| Sensorial Curriculum | `p` | max-width | 1440 | none ×242 / 860px ×3 | none ×251 |
| Sensorial Curriculum | `p` | padding-left | 1440 | 0px ×243 / 48px ×2 | 0px ×249 / 48px ×2 |
| Sensorial Curriculum | `p` | text-align | 1440 | justify ×239 / center ×3 / left ×2 … | justify ×239 / start ×7 / center ×3 … |
| Sensorial Curriculum | `p` | text-indent | 1440 | 0px ×243 / 48px ×2 | 0px ×249 / 48px ×2 |
| Sensorial Curriculum | `p` | text-wrap | 1440 | wrap ×242 / balance ×3 | wrap ×251 |
| Sensorial Curriculum | `span` | background | 1440 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×105 / rgb(255, 255, 255) none repeat scroll 0% ×1 | rgba(0, 0, 0, 0) none repeat scroll 0% 0 ×106 / rgb(255, 255, 255) none repeat scroll 0% ×1 |
| Sensorial Curriculum | `span` | border-radius | 1440 | 0px ×105 / 50% ×1 | 0px ×106 / 50% ×1 |
| Sensorial Curriculum | `span` | color | 1440 | rgb(43, 43, 43) ×72 / rgb(4, 50, 255) ×14 / rgb(255, 0, 0) ×3 … | rgb(43, 43, 43) ×72 / rgb(4, 50, 255) ×14 / rgb(255, 0, 0) ×3 … |
| Sensorial Curriculum | `span` | display | 1440 | block ×83 / inline ×22 / inline-block ×1 | block ×83 / inline ×23 / inline-block ×1 |
| Sensorial Curriculum | `span` | flex | 1440 | 0 1 auto ×106 | 0 1 auto ×107 |
| Sensorial Curriculum | `span` | font-family | 1440 | "EB Garamond", Georgia, serif ×105 / Vollkorn, Georgia, serif ×1 | "EB Garamond", Georgia, serif ×106 / Vollkorn, Georgia, serif ×1 |
| Sensorial Curriculum | `span` | font-size | 1440 | 17px ×81 / 18px ×23 / 40px ×1 … | 18px ×105 / 40px ×1 / 15px ×1 |
| Sensorial Curriculum | `span` | font-weight | 1440 | 400 ×105 / 500 ×1 | 400 ×106 / 500 ×1 |
| Sensorial Curriculum | `span` | line-height | 1440 | 22.1px ×81 / 29.7px ×23 / 48px ×1 … | 23.4px ×81 / 29.7px ×23 / 48px ×1 … |
| Sensorial Curriculum | `span` | margin-left | 1440 | 0px ×105 / 5.04px ×1 | 0px ×106 / 5.04px ×1 |
| Sensorial Curriculum | `span` | min-width | 1440 | 0px ×105 / auto ×1 | 0px ×106 / auto ×1 |
| Sensorial Curriculum | `span` | padding | 1440 | 8px 0px ×81 / 0px ×25 | 8px 0px ×81 / 0px ×26 |
| Sensorial Curriculum | `span` | text-align | 1440 | left ×81 / justify ×23 / start ×2 | left ×81 / justify ×23 / start ×2 … |
| Sensorial Curriculum | `ul` | margin | 1440 | 0px ×36 / 16px 0px ×2 | 0px ×38 |
## Added in version 8

### 1. What the template scripts change while the page runs

The styles above are not the whole template: its scripts set spacing and sizes on the page after it loads, and again on later events. The Culture audit (28 Oct, 15:35) found one of them, `mm-letter-gaps-js`, growing a margin on every run inside the album columns, up to 126 043 px. A check must therefore measure each of these after the page has settled, and again after each event that runs them.

| Template | Script | Sets | Runs again on | A check must measure |
|---|---|---|---|---|
| Essay | `mm-shape-js` | counter-reset, overflow | once | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (98997 characters)` | --mh, align-items, display, flex-direction, gap, grid-template-rows, height, justify-content, left, margin-bottom, margin-left, margin-top, max-height, max-width, min-height, overflow-anchor, padding-left, padding-top, position, row-gap, text-align, top, transform, visibility, white-space, width | click, element resize, keydown, load, resize, scroll, touchend, touchstart | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (550 characters)` | width | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (1605 characters)` | display, margin-left, width | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (1858 characters)` | --ly | load, resize | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (8913 characters)` | --h, clear, height, margin-top, width | once | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (3844 characters)` | margin-bottom, margin-top | DOMContentLoaded, load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `unnamed (1333 characters)` | margin-bottom, margin-top | load, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-foot-gap-js` | margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-band-js` | display | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-hero-gap-js` | padding-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-name-lines-js` | color, font-size, font-weight, margin-bottom, margin-top, padding-left | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-swipe-middle-js` | padding-left, padding-right | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-res-extra-js` | margin-left | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Essay | `mm-letter-gaps-js` | margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `unnamed (64561 characters)` | --mh, align-items, display, flex-direction, gap, grid-template-rows, height, justify-content, left, margin-bottom, margin-left, margin-top, max-height, max-width, min-height, overflow-anchor, padding-left, padding-top, position, row-gap, text-align, top, transform, visibility, white-space, width | click, element resize, keydown, load, resize, scroll, touchend, touchstart | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `unnamed (1677 characters)` | line-height, margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `unnamed (1587 characters)` | margin-top, width | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `unnamed (1457 characters)` | margin-top, width | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `unnamed (4259 characters)` | margin-top, padding-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-foot-gap-js` | margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-hero-gap-js` | padding-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-photo-align-js` | margin-bottom, margin-right, margin-top, padding-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-band-js` | display | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-pdf-column-js` | margin-left | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-ul-gap-js` | margin-bottom, margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-swipe-middle-js` | padding-left, padding-right | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-org-rule-js` | margin-bottom, margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-res-extra-js` | aspect-ratio, height, margin-left, margin-top, width | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-letter-gaps-js` | margin-bottom, margin-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |
| Resources | `mm-phone-gaps-js` | margin-top, padding-top | load, resize, timers | the same values after load, after 4 s, after scrolling to the end, after a resize, after opening and closing every album and contents entry; no value growing between runs |

### 2. Things live had that the package no longer has

The code check (line 111) only rejects names the template does not mention. The cleaning removes live classes the template does not use, and with them their look. Below, for each page, every class inside the content that live had and the package does not. "styled" means live's own page style gave it a look, which the package has lost unless the template does the same another way. A check must compare each of these with live.

| Page | Live classes gone, styled by live (count) | Live classes gone, not styled (count) | Settings fewer than live |
|---|---|---|---|
| A Montessori Journey | `mm-blue` ×30, `mm-hd` ×17, `mm-line` ×15, `mm-years` ×13 | `landscape` ×97, `portrait` ×55, `mm-place` ×13, `mm-space50` ×3 | — |
| Aun Aprendo | `mm-line` ×9, `sub-label` ×9, `mm-hd` ×9, `mm-blue` ×9, `mm-edges` ×6, `mm-craic` ×1 | `landscape` ×40, `portrait` ×18 | — |
| Biography | `mm-line` ×2, `pair` ×1, `gap2` ×1, `pimpair` ×1, `mm-rowcap` ×1, `mm-sign` ×1 | `portrait` ×14, `landscape` ×6, `eulogy-end` ×1 | — |
| Sensorial Resources | `mm-stack` ×3, `res-pdfline` ×1, `mm-italic` ×1 | `landscape` ×10, `portrait` ×4, `res-list` ×1 | `data-name` 13→0 |
| The Culture Curriculum | `mm-num` ×77, `mm-off` ×5, `mm-tabgap` ×2, `mm-lvl1` ×2, `beige-rule` ×1, `mm-introlist` ×1, `mm-nooff` ×1 | `landscape` ×157, `portrait` ×93, `mm-cname` ×23 | `inline style` 565→500, `data-name` 246→0, `data-word-colour` 14→0, `data-nowrap` 1→0 |
| The Mathematics Curriculum | `mm-cat` ×7, `mm-tabs` ×3, `mm-ind31` ×1, `mm-quote1` ×1 | `mm-stacked` ×4, `mm-qline` ×3 | `inline style` 475→332, `data-name` 153→0, `data-photos` 57→0, `data-g` 55→0, `data-n` 55→0, `data-pdf-centre` 55→0, `data-pdf-left` 55→0, `data-pdf-right` 55→0, `data-s` 55→0, `data-first` 32→0, `data-last` 32→0, `data-above-line` 20→0, `data-row-above` 20→0, `data-exception` 10→0, `data-top` 6→0, `data-gpx` 5→0, `data-ga-photos` 4→0, `data-after` 4→0, `data-word-colour` 4→0, `data-ntab` 4→0, `data-col` 4→0, `data-colw` 4→0, `data-photo` 4→0, `data-group` 3→0, `data-colour-exception` 3→0, `data-pdf-order` 3→0, `data-bottom` 2→0, `data-step-edit` 2→0, `data-added` 2→0, `data-moved` 1→0, `data-between` 1→0, `data-pdf-page` 1→0, `data-deftab` 1→0, `data-tabstops` 1→0, `data-fit-text` 1→0, `data-row` 1→0 |
| The Practical Life Curriculum | `mm-ph0` ×126, `mm-ph16` ×27, `mm-ph13` ×16, `mm-ph6` ×9, `mm-mlx` ×8, `mm-ph2` ×5, `mm-stack` ×1, `mm-off` ×1, `mm-ph18` ×1 | `mm-gl-q` ×23, `mm-thc` ×4, `mm-stacked` ×1, `mm-up` ×1 | `inline style` 348→326, `data-tpl` 234→0, `data-tpl-i` 206→0, `data-tpl-space` 206→0, `data-name` 163→0, `data-g` 44→0, `data-n` 44→0, `data-pdf-centre` 44→0, `data-pdf-left` 44→0, `data-pdf-right` 44→0, `data-photos` 44→0, `data-s` 44→0, `data-label` 24→0, `data-first` 21→0, `data-last` 21→0, `data-above-line` 20→0, `data-row-above` 20→0, `data-lastrev` 16→0, `data-fitmax` 6→0, `data-fitpara` 6→0, `data-back` 5→0, `data-hostmax` 5→0, `data-stack` 5→0, `data-after` 5→0, `data-group` 2→0, `data-ga-photos` 1→0, `data-gpx` 1→0 |
| The Role of the Adult – Resources | `mm-black` ×2, `mm-redname` ×1, `mm-short` ×1 | `landscape` ×2, `res-list` ×2, `mm-centretext` ×1, `mm-joosten` ×1, `portrait` ×1 | `inline style` 7→6, `data-name` 1→0 |
| The Sensorial Curriculum | `beige-rule` ×6, `bq-rule` ×4, `full` ×2, `no-line` ×1, `dm-blue` ×1 | `landscape` ×150, `portrait` ×50, `cw` ×22, `wide` ×8, `ref-area` ×6, `ext-float` ×3 | `inline style` 500→416, `data-name` 205→0, `data-vcentre` 8→0, `data-photo-bottom` 4→0, `data-w` 3→0, `data-centre-text` 3→0, `data-hcentre` 1→0 |

### 3. States a check must open

- every `<details>` section closed **and** open (the Culture albums looked right closed and broke open);
- every menu panel open (already in the on-screen check, 17 widths);
- the image viewer open on an image, with next and previous;
- the page scrolled slowly to the end, so images load one by one (the 831 px Aims overlap appeared only this way);
- the window narrowed and widened again.

## Added in version 9

### 4. The live look each lost class had (live's own style rules, verbatim)

A check needs the look it is checking for. These are the rules in each live page's own style that give the lost classes their look (27 Oct copies). Width conditions are shown.

**A Montessori Journey**

- `mm-blue` (×30 on live): `main .mm-blue{color:#0432FF}`
- `mm-hd` (×17 on live): `main .sub-label.mm-hd .mm-years{min-width:110px}` at (max-width:830px) ; `main .sub-label.mm-hd{margin-top:50px !important;margin-bottom:25px !important;clear:both}` ; `main .sub-label.mm-hd .mm-years{display:inline-block;min-width:150px}`
- `mm-line` (×15 on live): `main .mm-line{height:2px;background:#D9C9AB;clear:both}`
- `mm-years` (×13 on live): `main .sub-label.mm-hd .mm-years{min-width:110px}` at (max-width:830px) ; `main .sub-label.mm-hd .mm-years{display:inline-block;min-width:150px}`

**Aun Aprendo**

- `mm-line` (×9 on live): `main .mm-line{height:2px;background:#D9C9AB;clear:both}`
- `sub-label` (×9 on live): `.sub-label{font-size:19px}` at (max-width:640px) ; `.sub-label{font-size:17px}` at (max-width:640px) ; `.sub-label{font-family:'Cormorant Garamond',serif;margin-top:15px;margin-bottom:0;font-size:21px}` ; `.sub-label strong{color:var(--ink);font-weight:700}` ; `.sub-label{font-family:var(--serif);font-size:18px}` ; `.micro-label,.sub-label{font-weight:400 !important}` …+4 more
- `mm-hd` (×9 on live): `main .sub-label.mm-hd{margin-top:30px !important;margin-bottom:25px !important;clear:both}`
- `mm-blue` (×9 on live): `main .mm-blue{color:#0432FF}`
- `mm-edges` (×6 on live): `main .mm-row.mm-edges{justify-content:space-between}` at (min-width:831px)
- `mm-craic` (×1 on live): `main p.mm-craic{clear:both}`

**Biography**

- `mm-line` (×2 on live): `main .mm-line{height:2px;background:#D9C9AB;clear:both}`
- `pair` (×1 on live): `main .mm-row figure.ph:not(.pair) .pim{width:100% !important;height:auto !important}` at (min-width:831px) ; `main .ph.pair .pimpair{width:100%}` at (min-width:831px) ; `main .ph.pair .pim{width:100% !important;height:auto !important}` at (min-width:831px) ; `main .ph.pair .pimpair{display:flex;align-items:flex-start;gap:calc(var(--gp) * 1%)}` ; `main .ph.pair .pimpair .pim:first-child{flex:0 0 calc(var(--pa) * 1%)}` ; `main .ph.pair .pimpair .pim:last-child{flex:0 0 calc(var(--pb) * 1%)}`
- `gap2` (×1 on live): `main .mm-row figure.ph.gap2{margin-left:10px}` at (max-width:830px) ; `main .mm-row figure.ph.gap2{margin-left:24px}`
- `pimpair` (×1 on live): `main .ph.pair .pimpair{width:100%}` at (min-width:831px) ; `main .ph.pair .pimpair{display:flex;align-items:flex-start;gap:calc(var(--gp) * 1%)}` ; `main .ph.pair .pimpair .pim:first-child{flex:0 0 calc(var(--pa) * 1%)}` ; `main .ph.pair .pimpair .pim:last-child{flex:0 0 calc(var(--pb) * 1%)}`
- `mm-rowcap` (×1 on live): `main .mm-rowcap{font-family:'EB Garamond',serif;font-size:15px;line-height:1.3;text-align:center;margin:6px 0 0;clear:both}`
- `mm-sign` (×1 on live): `main .mm-sign{text-align:center;margin:30px 0 0;clear:both}` ; `main .mm-sign img{width:min(571px,100%);height:auto;display:block;margin:0 auto}`

**Sensorial Resources**

- `mm-stack` (×3 on live): `main .mm-float.mm-stack{margin-bottom:36px !important}`
- `res-pdfline` (×1 on live): `main p.res-pdfline{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:24px}` ; `main p.res-pdfline a.pdf{margin-left:0 !important;margin-right:0 !important}`
- `mm-italic` (×1 on live): `main blockquote.mm-italic p, main blockquote.mm-italic p *{font-style:italic !important}`

**The Culture Curriculum**

- `mm-num` (×77 on live): `main p.mm-num{display:grid;grid-template-columns:44px 1fr}` ; `main .micro-label.mm-num{display:grid;grid-template-columns:44px 1fr}`
- `mm-off` (×5 on live): `main p.mm-off{margin-left:0 !important}` at (max-width:640px) ; `main p.mm-off{margin-left:48px !important}`
- `mm-tabgap` (×2 on live): `main .mm-tabgap{display:inline-block;width:2em}`
- `mm-lvl1` (×2 on live): `main ul.mm-lvl1{margin-left:48px !important}`
- `beige-rule` (×1 on live): `.beige-rule{height:2px;background:#D9C9AB;margin:0 auto 20px;max-width:100%}`
- `mm-introlist` (×1 on live): `main .mm-introlist{grid-template-columns:1fr;margin-left:0}` at (max-width:640px) ; `main .mm-introlist{display:grid;grid-template-columns:1fr 1fr;column-gap:40px;margin:0 0 0 48px}` ; `main .mm-introlist p{margin:0 0 11px !important;display:grid;grid-template-columns:30px 1fr}`
- `mm-nooff` (×1 on live): `main .mm-set ol.mm-nooff{margin-left:0 !important;padding-left:0 !important;list-style-position:inside}`

**The Mathematics Curriculum**

- `mm-cat` (×7 on live): `main p.mm-cat{display:grid;grid-template-columns:157px 1fr}`
- `mm-tabs` (×3 on live): `main p.mm-tabs{grid-template-columns:auto auto;column-gap:12px}` at (max-width:640px) ; `main p.mm-tabs>span:last-child{grid-column:1/-1}` at (max-width:640px) ; `main p.mm-tabs{display:grid;grid-template-columns:115px 185px auto}` ; `main .mm-set p.mm-tabs{grid-template-columns:115px 185px minmax(0,170px)}`
- `mm-ind31` (×1 on live): `main ul.mm-ind31{padding-left:31px !important}` ; `main ul.mm-ind31>li::before{left:-31px !important}`
- `mm-quote1` (×1 on live): `main blockquote.mm-quote1{margin-left:20px !important;margin-right:20px !important;padding-left:73px !important;border-left:0 !important;font-style:italic}` ; `main blockquote.mm-quote1 p{text-indent:0 !important;padding-left:0 !important;margin-left:0 !important}`

**The Practical Life Curriculum**

- `mm-ph0` (×126 on live): `main .mm-ph0{margin-top:0px !important}` at (max-width:640px)
- `mm-ph16` (×27 on live): `main .mm-ph16{margin-top:16px !important}` at (max-width:640px)
- `mm-ph13` (×16 on live): `main .mm-ph13{margin-top:13px !important}` at (max-width:640px)
- `mm-ph6` (×9 on live): `main .mm-ph6{margin-top:6px !important}` at (max-width:640px)
- `mm-mlx` (×8 on live): `main .mm-pdf.mm-pdf-row .mm-pdfin>figure.mm-pdff.mm-flow.mm-mlx,main .mm-pdf .mm-pdfin>figure.mm-pdff.mm-flow.mm-mlx{margin-left:var(--mlx) !important}` at (min-width:641px)
- `mm-ph2` (×5 on live): `main .mm-ph2{margin-top:2px !important}` at (max-width:640px)
- `mm-stack` (×1 on live): `main table.mm-stack,main table.mm-stack tbody,main table.mm-stack tr,main table.mm-stack td,main table.mm-stack th{display:block !important;width:auto !important;max-width:100% !im` at (max-width:640px) ; `main table.mm-stack{border-collapse:collapse}` at (max-width:640px) ; `main table.mm-stack thead{display:none !important}` at (max-width:640px) ; `main table.mm-stack tr{margin:0 0 30px 0;padding:0}` at (max-width:640px) ; `main table.mm-stack td,main table.mm-stack th{padding:0 !important;border:0 !important}` at (max-width:640px) ; `main table.mm-stack td[data-label]{margin-top:10px}` at (max-width:640px) …+1 more
- `mm-off` (×1 on live): `main ul.mm-off{margin-left:25px !important}` at (min-width:641px)
- `mm-ph18` (×1 on live): `main .mm-ph18{margin-top:18px !important}` at (max-width:640px)

**The Role of the Adult – Resources**

- `mm-black` (×2 on live): `.mm-black{color:#000;font-style:normal}`
- `mm-redname` (×1 on live): `.mm-redname{color:#EE0000;font-style:normal}`
- `mm-short` (×1 on live): `main .mm-org-rule.mm-short{width:100px;max-width:100px;margin-left:auto !important;margin-right:auto !important;clear:none}`

**The Sensorial Curriculum**

- `beige-rule` (×6 on live): `.beige-rule{height:2px;background:#D9C9AB;margin:0 auto 20px;max-width:100%}` ; `.toc-rule-wrap .beige-rule{margin:0}` ; `.beige-rule.full{width:100% !important}` ; `.toc-rule-wrap .beige-rule{visibility:hidden}` ; `.beige-rule.no-line{visibility:hidden}` ; `.beige-rule{background:#D9C9AB}` …+2 more
- `bq-rule` (×4 on live): `.bq-rule{margin:0}` ; `.beige-rule.bq-rule:not(.no-line),.beige-rule.full{margin-top:20px !important;margin-bottom:20px !important}`
- `full` (×2 on live): `.beige-rule.full{width:100% !important}` ; `.beige-rule.bq-rule:not(.no-line),.beige-rule.full{margin-top:20px !important;margin-bottom:20px !important}`
- `no-line` (×1 on live): `.beige-rule.no-line{visibility:hidden}` ; `.beige-rule.bq-rule:not(.no-line),.beige-rule.full{margin-top:20px !important;margin-bottom:20px !important}` ; `.beige-rule.no-line{margin-top:20px !important;margin-bottom:-22px !important}`
- `dm-blue` (×1 on live): `h3.material-name.dm-blue{color:#0432FF !important}` ; `h3.material-name.dm-blue::before{background:transparent !important}`

### 5. Inline styles live had that the package dropped

Inline styles carried part of live's layout (for example the Culture photo rows' `--hg` and `--ar`). The code check bans most inline styles inside the content (line 127), so the cleaning removes them. Counted by property, live against package:

| Page | Inline style properties live had, with how many elements; package count after the arrow |
|---|---|
| A Montessori Journey | `--hg` 152→0, `--ar` 152→0, `--w` 152→0 |
| Aun Aprendo | `--hg` 58→0, `--ar` 58→0, `--w` 58→0, `width` 2→0 |
| Biography | `--hg` 21→0, `--ar` 21→0, `--w` 21→0, `width` 4→0, `--pa` 1→0, `--pb` 1→0, `--gp` 1→0 |
| Sensorial Resources | `--h` 14→0, `--hg` 14→0, `--ar` 14→0, `width` 5→0, `--w` 1→0 |
| The Culture Curriculum | `--hg` 250→0, `--ar` 250→0, `color` 53→0, `margin-left` 12→0, `--w` 4→0, `width` 2→0 |
| The Mathematics Curriculum | `width` 159→155, `height` 157→153, `color` 119→22, `grid-template-columns` 48→0, `display` 44→0, `--ar` 6→2, `border-color` 5→0, `--hg` 4→0, `counter-reset` 2→0, `padding-left` 2→0, `white-space` 1→0, `text-shadow` 1→0 |
| The Practical Life Curriculum | `color` 21→0, `font-weight` 4→0, `font-style` 1→0 |
| The Role of the Adult – Resources | `--h` 3→0, `--hg` 3→0, `--ar` 3→0, `--w` 2→0, `margin-top` 1→0, `width` 1→0 |
| The Sensorial Curriculum | `--hg` 208→0, `--ar` 208→0, `width` 59→0, `position` 54→0, `left` 54→0, `top` 54→0, `height` 54→0, `max-width` 54→0, `color` 28→0, `object-fit` 17→0, `transform` 5→0, `--w` 3→0, `font-weight` 2→0 |
## Added in version 10: does each page settle?

Measured 28 Oct 15:4x at 1440 px, one load per page: the height of the content area after 1 s, after 4 s, after scrolling slowly to the end and waiting 3.5 s, and (where the page has open-and-close sections) with all of them opened, then closed again; and the largest top margin on any element. Packages are the copies you were sent (seven), the Culture build cul3 and Sensorial Curriculum 425a822f; three live copies of 27 Oct for comparison.

| Page | After 1 s | After 4 s | After scrolling | All sections open | Closed again | Largest margin (element) | Live 27 Oct, after scrolling |
|---|---|---|---|---|---|---|---|
| a-montessori-journey | 10024 | 10024 | 10024 | — | — | 64 px (HR.formula-divider ) | |
| aun-aprendo | 5225 | 5225 | 5225 | — | — | 64 px (P.mm-gl ) | |
| biography | 4992 | 4992 | 4992 | — | — | 64 px (IMG.doc-img ) | |
| sensorial-resources | 4315 | 4315 | 4315 | — | — | 60 px (DIV.mm-row ) | |
| the-mathematics-curriculum | 25981 | 25981 | 25981 | — | — | 257 px (DIV.micro-label.lbl-bold.mm-hc-7030A0 Th) |30611 (largest margin 70) |
| the-practical-life-curriculum-2 | 21384 | 21872 | 21902 | — | — | 931 px (P. “In the 3-6 Montessori classro) | |
| the-role-of-the-adult-resources | 6766 | 6766 | 6766 | — | — | 32 px (SECTION.section The Froebel Trust
Nurser) | |
| the-culture-curriculum | 26872 | 26872 | 27997 | 1816087 | 25561 | 4275490 px (DIV.micro-label.lbl-bold Studying Specif) |21121 (largest margin 91) |
| the-sensorial-curriculum | 42601 | 42601 | 42632 | — | — | 547322 px (DIV.mm-set MaterialsFive pairs of tablet) |30460 (largest margin 44) |

**What this shows (facts from the table):**
- The Culture Curriculum (my build, not sent): the height grows after scrolling (26 872 → 27 997), reaches 1 816 087 px with the sections open, and one label has a 4 275 490 px margin. Live: 21 121 throughout, 28 373 open, largest margin 91.
- The Sensorial Curriculum (package, not sent): 42 601 px against live 30 460, and one block has a 547 322 px margin.
- **The Practical Life Curriculum, now live from your upload:** the height keeps growing after load (21 384 → 21 872 → 21 902), and one paragraph ("“In the 3-6 Montessori classro…") has a 931 px margin above it.
- The Mathematics Curriculum, live from your upload: steady; its largest margin is 257 px, on the label "Third Period - Recall / Output".
- A Montessori Journey, Aun Aprendo, Biography, Sensorial Resources, The Role of the Adult - Resources: steady, largest margin 32-64 px.

**What a check must therefore do, which none of the current checks does:** load each page, record the height and the largest margin after 1 s and 4 s, after a slow scroll, and with every section opened and closed; fail the page if the height changes after settling or any margin is larger than the largest live has.
