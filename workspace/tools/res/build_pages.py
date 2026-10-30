"""Category 2 and Category 3 templates, built straight from Word.

Both documents use the same colour grammar, so one converter reads both:
  green, centred   -> page title (hero)
  green            -> section heading, and an entry in the contents box
  blue, no link    -> section heading (the essays use blue instead of green)
  red              -> the source or author of a resource: starts a resource entry
  blue / any line with links, inside an entry -> the item, linked, with a PDF badge if Word says PDF
  plain text inside an entry                  -> the description, indented under it
  italic paragraph (essays)                   -> quotation; the plain line under it is its attribution
  bold short line (essays)                    -> sub-heading
  image-only paragraph                        -> photo row (200px)
Tabs inside a line become separate columns (title, date, PDF), as in Word.
"""
import base64, html as H, io, os, re, sys, json
import docx
from docx.oxml.ns import qn
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # 30 Sept, 13th chat: 3.1.3 has a 12000x18000 chart (Word pictures are the user's own files)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import shell

RED = {'FF0000', 'EE0000', 'C00000', 'D81F35'}
BLUE = {'0432FF', '1560D4', '1E4D9B', '0000FF'}
GREEN = {'00B050', '1F9E42', '008F00'}
GALLERY = 200

# ---------------------------------------------------------------- Word reading
def props(par):
    # every run with text, including runs inside links (27 Sept: a red source name that is also a link)
    for r in par._p.iter(qn('w:r')):
        if ''.join(t.text or '' for t in r.iter(qn('w:t'))).strip():
            pr = r.find(qn('w:rPr')); col = None; b = i = False
            if pr is not None:
                c = pr.find(qn('w:color'))
                if c is not None and c.get(qn('w:val')) not in (None, 'auto'): col = c.get(qn('w:val')).upper()
                b = pr.find(qn('w:b')) is not None; i = pr.find(qn('w:i')) is not None
            return dict(colour=col, bold=b, italic=i, centred=str(par.alignment or '').startswith('CENTER'))
    return dict(colour=None, bold=False, italic=False, centred=False)

def inline(par, rels, keep_tabs=False):
    out = []
    for node in par._p.iter():
        tag = node.tag.split('}')[1]
        if tag == 'hyperlink':
            rid = node.get(qn('r:id')); url = rels[rid].target_ref if rid in rels else '#'
            if node.get(qn('w:anchor')) and url != '#': url = url + '#' + node.get(qn('w:anchor'))   # 20 Oct 21:2x (5.4 Monticello): the part after # kept, as convert_curriculum.py
            txt = ''.join(t.text or '' for t in node.iter(qn('w:t')))
            if txt.strip():
                cls = ' class="pdf"' if txt.strip().upper() == 'PDF' else ''
                out.append(f'<a{cls} href="{H.escape(url)}" target="_blank" rel="noopener">{H.escape(txt.strip())}</a>')
        elif tag == 'r' and node.getparent().tag != qn('w:hyperlink'):
            pr = node.find(qn('w:rPr'))
            for ch in node:   # 30 Sept (13th chat): text, tabs and breaks in Word's order - a break inside a text run was dropped
                ct = ch.tag.split('}')[1]
                if ct == 'br' and ch.get(qn('w:type')) in (None, 'textWrapping'): out.append('<br>')
                elif ct == 'tab': out.append('\t')
                elif ct == 't' and ch.text:
                    s = H.escape(ch.text)
                    if pr is not None:
                        if pr.find(qn('w:i')) is not None: s = f'<em>{s}</em>'
                        if pr.find(qn('w:b')) is not None: s = f'<strong>{s}</strong>'
                    out.append(s)
    s = ''.join(out)
    s = re.sub(r'[ \t]*\t[ \t]*', '\t', s).strip()
    return s if keep_tabs else s.replace('\t', ' ')

def links_of(par, rels):
    out = []
    for h in par._p.iter(qn('w:hyperlink')):
        rid = h.get(qn('r:id'))
        if rid in rels: out.append(rels[rid].target_ref)
    return out

def images_of(par, doc):
    out = []
    for b in par._p.iter(qn('a:blip')):
        rid = b.get(qn('r:embed'))
        if rid and rid in doc.part.rels: out.append((doc.part.rels[rid].target_ref.split('/')[-1], doc.part.rels[rid].target_part.blob))
    return out

# ---------------------------------------------------------------- page pieces
def side_photo(name, blob, height=180):
    im = Image.open(io.BytesIO(blob)); ar = im.size[0] / im.size[1]
    mime = 'image/png' if name.lower().endswith('png') else ('image/gif' if name.lower().endswith('gif') else 'image/jpeg')
    uri = f'data:{mime};base64,' + base64.b64encode(blob).decode()
    return (f'<div class="photo-row side-photo"><figure class="ph" style="--h:{height};--ar:{ar:.5f}"><div class="pim">'
            f'<img class="doc-img" src="{uri}" alt="" width="{im.size[0]}" height="{im.size[1]}" loading="lazy" data-name="{name}"></div></figure></div>')

def link_share(par, rels):
    t = par.text.strip(); lt = ''.join(''.join(x.text or '' for x in h.iter(qn('w:t'))) for h in par._p.iter(qn('w:hyperlink')))
    return len(lt.strip()) / max(1, len(t))

def photo_row(imgs, height=GALLERY):
    figs = []
    for name, blob in imgs:
        im = Image.open(io.BytesIO(blob)); ar = im.size[0] / im.size[1]
        mime = 'image/png' if name.lower().endswith('png') else ('image/gif' if name.lower().endswith('gif') else 'image/jpeg')
        uri = f'data:{mime};base64,' + base64.b64encode(blob).decode()
        figs.append(f'<figure class="ph" style="--h:{height};--ar:{ar:.5f}"><div class="pim">'
                    f'<img class="doc-img" src="{uri}" alt="" width="{im.size[0]}" height="{im.size[1]}" loading="lazy" data-name="{name}"></div></figure>')
    return f'<div class="photo-row{" single" if len(figs) == 1 else ""}">{"".join(figs)}</div>'

def item_line(par, rels):
    """A title line: the title (italic, linked if Word links it), then any tab-separated extras
    (date, Part I, notes). Every link reading "PDF" is a badge in its own place; a plain "PDF" gets the line's last link."""
    parts = [p.strip() for p in inline(par, rels, keep_tabs=True).split('\t') if p.strip()]
    links = links_of(par, rels)
    out = []
    for k, p in enumerate(parts):
        txt = re.sub(r'<[^>]+>', '', p).strip()
        if k == 0:
            # 27 Sept: PDF badges Word keeps inside the title's part become their own parts (24px apart)
            # 30 Sept (13th chat): the text after a badge (\"PDF (0 to 12) PDF (3 to 6)\") stays after it, in Word's order
            bits = [b.strip() for b in re.split(r'(<a class="pdf"[^>]*>PDF</a>)', p)]
            p = bits[0]; badges = []
            for b in bits[1:]:
                if b.startswith('<a class="pdf"'): badges.append(b)
                elif re.sub(r'<[^>]+>', '', b).strip(): badges.append(f'<span class="meta">{b}</span>')
            txt = re.sub(r'<[^>]+>', '', p).strip()
            if not txt:                                   # a line of badges only: no title
                out += [b.strip() for b in badges]; continue
            d = re.search(r'\s+((?:1[5-9]|20)\d\d(?:[\u2013-]\d{2,4})?)\s*$', txt)
            year = None
            if d and txt[:d.start()].strip():
                year = d.group(1); p = re.sub(r'\s*' + re.escape(year) + r'\s*((?:</[a-z]+>)*)\s*$', r'\1', p)
            head = p if p.lstrip().startswith('<em>') else f'<em>{p}</em>'
            out.append(f'<span class="res-title">{head}</span>')
            if year: out.append(f'<span class="meta">{year}</span>')
            out += [b.strip() for b in badges]
            continue
        if txt.upper() == 'PDF' and 'class="pdf"' not in p:
            url = links[-1] if links else None
            out.append(f'<a class="pdf" href="{url}" target="_blank" rel="noopener">PDF</a>' if url else '<span class="pdf">PDF</span>'); continue
        out.append(f'<span class="meta">{p}</span>')
    return f'<div class="res-item">{"".join(out)}</div>'

def num_fmt(par, doc):
    """Word's number format of a list paragraph ('bullet', 'decimal', ...)."""
    try:
        n = par._p.pPr.numPr; nid = n.numId.val; lvl = n.ilvl.val if n.ilvl is not None else 0
        num = doc.part.numbering_part.element
        aid = [x for x in num.findall(qn('w:num')) if x.get(qn('w:numId')) == str(nid)][0].find(qn('w:abstractNumId')).get(qn('w:val'))
        an = [x for x in num.findall(qn('w:abstractNum')) if x.get(qn('w:abstractNumId')) == aid][0]
        return an.findall(qn('w:lvl'))[int(lvl)].find(qn('w:numFmt')).get(qn('w:val'))
    except Exception: return 'decimal'

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60]

# ---------------------------------------------------------------- converter
def convert(path, active_menu, out_path, hero_img=None, subtitle=None, title_override=None):
    doc = docx.Document(path); rels = doc.part.rels
    title, body, toc, pend = title_override, [], [], []
    uses_green = any(props(q)['colour'] in GREEN and not props(q)['centred'] for q in doc.paragraphs if q.text.strip())
    in_entry = quote = False
    def close_entry():
        nonlocal in_entry
        if in_entry: body.append('</div>'); in_entry = False
    def close_quote():
        nonlocal quote
        if quote: body.append('</blockquote>'); quote = False
    def flush():
        if pend: body.append(photo_row(pend)); pend.clear()

    for par in doc.paragraphs:
        text = par.text.strip(); imgs = images_of(par, doc)
        if imgs and not text:
            if len(imgs) == 1 and not pend: body.append(side_photo(*imgs[0])); continue   # a lone picture sits beside the text
            pend.extend(imgs); continue
        if not text: continue
        flush()
        p = props(par); links = links_of(par, rels)
        if title is None and p['centred'] and p['colour'] in RED | GREEN | BLUE:
            title = text; continue
        if title is None and not body and p['colour'] in GREEN:     # e.g. "Sensorial Resources" at the top, not centred
            title = text; continue
        if imgs:                                                     # picture anchored in a text paragraph: beside it
            for nm, bl in imgs: body.append(side_photo(nm, bl))
        if p['colour'] in GREEN or (p['colour'] in BLUE and not uses_green and not in_entry and not links and len(text) < 80):
            close_quote(); close_entry()
            i = slug(text); toc.append((i, H.escape(text)))
            body.append(f'<h2 class="page-h2" id="{i}">{inline(par, rels)}</h2>'); continue
        if p['colour'] in RED and len(text) < 120:
            close_quote(); close_entry()
            body.append(f'<div class="res-entry"><div class="res-src">{inline(par, rels)}</div>'); in_entry = True; continue
        if in_entry:
            if (p['colour'] in BLUE or (links and link_share(par, rels) >= 0.7)) and len(text) <= 160: body.append(item_line(par, rels))
            else:   # prose inside an entry: a trailing "PDF" link still becomes the badge
                h = inline(par, rels)
                h = re.sub(r'\s*<a href="([^"]+)"[^>]*>\s*PDF\s*</a>\s*$', lambda m: f' <a class="pdf" href="{m.group(1)}" target="_blank" rel="noopener">PDF</a>', h)
                if par._p.pPr is not None and par._p.pPr.numPr is not None:   # 29 Sept (seventh chat): a Word numbered list inside an entry stays a numbered list
                    tag = 'ul' if num_fmt(par, doc) == 'bullet' else 'ol'     # 30 Sept (13th chat): a bulleted (dash) list stays bulleted
                    body.append(f'<{tag} class="res-list"><li>{h}</li></{tag}>')
                else:
                    # 30 Sept (13th chat): lines after a break that are a title and its PDF badge (Word blue, e.g.
                    # "Reading  PDF") are title lines of their own, as if Word had them as separate paragraphs
                    segs = h.split('<br>'); tail = []
                    while len(segs) > 1 and re.fullmatch(r'\s*[^<]{1,60}?\s*(<a class="pdf"[^>]*>PDF</a>\s*)+', segs[-1]):
                        seg = segs.pop(); t = re.match(r'\s*([^<]*?)\s*<a', seg).group(1)
                        tail.insert(0, f'<div class="res-item"><span class="res-title"><em>{t}</em></span>'
                                       + ''.join(re.findall(r'<a class="pdf"[^>]*>PDF</a>', seg)) + '</div>')
                    body.append(f'<p class="res-desc">{"<br>".join(segs)}</p>'); body.extend(tail)
            continue
        if (uses_green and p['colour'] in BLUE) or (links and link_share(par, rels) >= 0.7 and len(text) <= 160):
            close_quote(); body.append(item_line(par, rels)); continue
        if p['italic'] and len(text) > 40:
            close_quote(); body.append(f'<blockquote class="mq"><p>{inline(par, rels)}</p>'); quote = True; continue
        if quote:
            body.append(f'<cite>{inline(par, rels)}</cite></blockquote>'); quote = False; continue
        if p['bold'] and len(text) < 90:
            body.append(f'<h3 class="sub-head">{inline(par, rels)}</h3>'); continue
        if par.style.name.startswith('List'):
            body.append(f'<ul><li>{inline(par, rels)}</li></ul>'); continue
        body.append(f'<p>{inline(par, rels)}</p>')
    close_quote(); close_entry(); flush()
    html = re.sub(r'</ul>\s*<ul>', '', '\n'.join(body))
    html = re.sub(r'</ol>\s*<ol class="res-list">', '', html)
    html = re.sub(r'</ul>\s*<ul class="res-list">', '', html)

    hero = (shell.hero(hero_img, [subtitle, title] if subtitle else [title]) if hero_img
            else f'<div class="hero hero-plain"><h1><span>{H.escape(title)}</span></h1></div>')
    page = (shell.head(title, PAGE_CSS) + '<body id="top">\n' + shell.header(active_menu, title) + hero
            + (shell.toc(toc, []) if len(toc) >= 3 else '') + f'<main class="essay" id="content">\n{html}\n</main>\n'
            + shell.footer() + LIGHTBOX + '\n<script>' + LIGHTBOX_JS + shell.MENU_JS + '</script>\n</body>\n</html>\n')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write(page)
    txt = re.sub(r'<[^>]+>', ' ', html)
    return dict(title=title, sections=len(toc), photos=html.count('<figure'), entries=html.count('res-entry'),
                pdfs=html.count('class="pdf"'), links=html.count('<a '), words=len(txt.split()), out=out_path)

PAGE_CSS = r"""
.essay{max-width:var(--page);margin:0 auto;padding:0 var(--gutter) 72px}
.essay p{margin:14px 0}
.essay .page-h2:first-of-type{margin-top:8px}
.sub-head{font-family:var(--serif);font-weight:700;font-size:18px;margin:26px 0 6px}
.essay ul{list-style:none;margin:14px 0;padding-left:48px}
.essay li{position:relative;margin:6px 0}
.essay li::before{content:"\2010";position:absolute;left:-24px}
.photo-row{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin:26px 0}
.photo-row .ph{margin:0}
.photo-row .pim{height:calc(var(--h) * 1px);width:auto;overflow:hidden;border-radius:6px}
.photo-row img{display:block;height:100%;width:auto;cursor:zoom-in}
.hero-plain{background:#2B2B2B;min-height:220px}
.photo-row.side-photo{float:right;clear:right;margin:6px 0 14px 28px}
.essay .page-h2{clear:both}
.essay::after{content:"";display:block;clear:both}
.res-item .meta + .meta{margin-left:0}
/* resource entries (Category 3, and the resource lists at the end of essays) */
.res-entry{padding:14px 0;border-top:1px solid var(--line)}
.res-entry:first-of-type{border-top:0}
.res-src{font-weight:700}
.res-item{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:16px;row-gap:4px;margin:2px 0}
.res-item .meta{color:var(--quiet);font-size:17px}
.res-desc{margin:4px 0 !important;color:var(--ink)}
a.pdf,span.pdf{display:inline-block;vertical-align:.12em;margin-left:4px;font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.06em;line-height:1;
  padding:4px 6px;border:1.5px solid var(--head);border-radius:2px;color:var(--head);text-decoration:none}
a.pdf:hover{background:var(--head);color:#fff}
.res-item a.pdf,.res-item span.pdf{margin-left:0}
@media (max-width:640px){
  .essay{padding:0 24px 56px}
  .photo-row{gap:12px;margin:18px 0}
  .photo-row .pim{height:auto;width:100%}
  .photo-row .ph{flex:1 1 140px}
  .photo-row img{width:100%;height:auto}
  .photo-row.side-photo{float:none;margin:10px 0;max-width:62%}
}
.lightbox[hidden]{display:none}
.lightbox{position:fixed;inset:0;background:rgba(20,16,12,.94);z-index:999;display:flex;align-items:center;justify-content:center;padding:5vw 80px}
.lightbox img{max-width:100%;max-height:100%;object-fit:contain;cursor:pointer}
.lb-btn{position:fixed;width:56px;height:56px;border-radius:50%;border:0;background:rgba(255,255,255,.14);color:#fff;font-size:34px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center}
.lb-btn[hidden]{display:none}
.lb-btn:hover{background:rgba(255,255,255,.26)}
.lb-prev{left:18px;top:50%;transform:translateY(-50%)}
.lb-next{right:18px;top:50%;transform:translateY(-50%)}
.lb-close{right:18px;top:calc(18px + env(safe-area-inset-top,0px));font-size:30px}
.lb-count{position:fixed;bottom:calc(22px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);color:rgba(255,255,255,.8);font-size:15px}
@media (max-width:640px){.lightbox{padding:60px 8px}.lb-prev,.lb-next{top:auto;bottom:calc(14px + env(safe-area-inset-bottom,0px));transform:none;width:48px;height:48px}}
"""
LIGHTBOX = ('<div class="lightbox" id="lightbox" hidden role="dialog" aria-label="Photo viewer">'
            '<img id="lightbox-img" alt="">'
            '<button class="lb-btn lb-prev" type="button" aria-label="Previous photo">\u2039</button>'
            '<button class="lb-btn lb-next" type="button" aria-label="Next photo">\u203a</button>'
            '<button class="lb-btn lb-close" type="button" aria-label="Close">\u00d7</button>'
            '<div class="lb-count" aria-live="polite"></div></div>')
LIGHTBOX_JS = r"""
(function(){var lb=document.getElementById('lightbox');if(!lb)return;var im=document.getElementById('lightbox-img'),cnt=lb.querySelector('.lb-count');
var set=[],i=0,last=null;
function show(){im.src=set[i].src;var many=set.length>1;lb.querySelector('.lb-prev').hidden=!many||i===0;lb.querySelector('.lb-next').hidden=!many||i===set.length-1;cnt.textContent=many?(i+1)+' / '+set.length:'';}
function open(img){var row=img.closest('.photo-row');set=row?[].slice.call(row.querySelectorAll('img.doc-img')):[img];i=set.indexOf(img);last=img;lb.hidden=false;show();lb.querySelector('.lb-close').focus();}
function close(){lb.hidden=true;im.src='';if(last)last.focus();}
function step(d){if(set.length<2)return;var j=i+d;if(j<0||j>=set.length)return;i=j;show();}   // a first and a last photo
document.addEventListener('click',function(e){var t=e.target;if(t.tagName==='IMG'&&t.classList.contains('doc-img')){open(t);return;}
 if(lb.hidden)return;if(t.closest('.lb-prev'))step(-1);else if(t.closest('.lb-next'))step(1);else if(t===im){if(i<set.length-1)step(1);else close();}else close();});
document.addEventListener('keydown',function(e){if(lb.hidden){if(e.key==='Enter'&&e.target.classList&&e.target.classList.contains('doc-img'))open(e.target);return;}
 if(e.key==='Escape')close();else if(e.key==='ArrowLeft')step(-1);else if(e.key==='ArrowRight')step(1);});
var x0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
lb.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)step(dx<0?1:-1);x0=null;});
document.querySelectorAll('img.doc-img').forEach(function(img){img.tabIndex=0;img.setAttribute('role','button');img.setAttribute('aria-label','Open photo');});})();
"""

if __name__ == '__main__':
    jobs = [('/mnt/user-data/uploads/7_9_E_douard_Se_guin.docx', 'Education', '/home/claude/site/out/edouard-seguin.html'),
            ('/mnt/user-data/uploads/2_3_1_The_Uninterrupted_Three-Hour_Cycle_Resources.docx', 'Essential Elements',
             '/home/claude/site/out/three-hour-cycle-resources.html')]
    for src, menu, out in jobs: print(json.dumps(convert(src, menu, out)))
