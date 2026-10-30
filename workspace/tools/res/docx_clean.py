"""Clean a Word document before it is read (27 Sept, every Resources page):
- hidden text (Word's "vanish": e.g. "Top of Form / Bottom of Form") is removed, and a paragraph left empty goes too;
- a link held in a Word field (HYPERLINK "url"), even one whose visible text lies in a later paragraph, becomes an
  ordinary Word link around its visible text.
Writes a cleaned copy; the original is never altered."""
import re, shutil, sys, zipfile
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'
q = lambda t: '{%s}%s' % (W, t)

def clean(src, dst):
    z = zipfile.ZipFile(src); doc = etree.fromstring(z.read('word/document.xml')); rels = etree.fromstring(z.read('word/_rels/document.xml.rels'))
    ids = {int(x.get('Id')[3:]) for x in rels if x.get('Id', '').startswith('rId') and x.get('Id')[3:].isdigit()}
    nid = max(ids or {0}) + 1; made = 0; hidden = 0
    body = doc.find(q('body'))
    # fields: walk runs in document order
    runs = list(body.iter(q('r'))); state = None; url = None; result = []
    for r in runs:
        fc = r.find(q('fldChar')); it = r.find(q('instrText'))
        if fc is not None and fc.get(q('fldCharType')) == 'begin': state = 'instr'; url = None; result = []; continue
        if it is not None and state == 'instr':
            m = re.search(r'HYPERLINK\s+"([^"]+)"', it.text or ''); url = url or (m.group(1) if m else None); continue
        if fc is not None and fc.get(q('fldCharType')) == 'separate': state = 'result'; continue
        if fc is not None and fc.get(q('fldCharType')) == 'end':
            vis = [x for x in result if x.find(q('rPr')) is None or x.find(q('rPr')).find(q('vanish')) is None]
            vis = [x for x in vis if ''.join(t.text or '' for t in x.iter(q('t'))).strip()]
            if url and vis:
                rid = f'rId{nid}'; nid += 1
                e = etree.SubElement(rels, '{%s}Relationship' % PR); e.set('Id', rid); e.set('Target', url); e.set('TargetMode', 'External')
                e.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink')
                # wrap the visible result runs of each paragraph in a hyperlink
                by_par = {}
                for x in vis: by_par.setdefault(x.getparent(), []).append(x)
                for par, xs in by_par.items():
                    h = etree.Element(q('hyperlink')); h.set('{%s}id' % R, rid)
                    xs[0].addprevious(h)
                    for x in xs: h.append(x)
                made += 1
            state = None; continue
        if state == 'result': result.append(r)
    # remove field machinery runs and hidden runs
    for r in list(body.iter(q('r'))):
        if r.find(q('fldChar')) is not None or r.find(q('instrText')) is not None: r.getparent().remove(r); continue
        pr = r.find(q('rPr'))
        if pr is not None and pr.find(q('vanish')) is not None and pr.find(q('vanish')).get(q('val')) not in ('0', 'false'):
            r.getparent().remove(r); hidden += 1
    for p in list(body.iter(q('p'))):
        if not ''.join(t.text or '' for t in p.iter(q('t'))).strip() and p.find('.//' + q('drawing')) is None and p.find('.//' + q('pict')) is None:
            ppr = p.find(q('pPr')); rpr = ppr.find(q('rPr')) if ppr is not None else None
            if rpr is not None and rpr.find(q('vanish')) is not None: p.getparent().remove(p)
    shutil.copy(src, dst)
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            if item.filename == 'word/document.xml': zo.writestr(item, etree.tostring(doc, xml_declaration=True, encoding='UTF-8', standalone=True))
            elif item.filename == 'word/_rels/document.xml.rels': zo.writestr(item, etree.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True))
            else: zo.writestr(item, zi.read(item.filename))
    return made, hidden

if __name__ == '__main__': print(clean(sys.argv[1], sys.argv[2]))
