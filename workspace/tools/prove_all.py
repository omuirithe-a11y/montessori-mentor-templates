#!/usr/bin/env python3
"""Prove every check on a deliberately broken copy (21 Oct 2026): python3 tools/prove_all.py 5.4 [CHECK ...]

For each check, one copy of the built page with one fault put in. The check must FAIL on its copy and PASS on the real
build; only then is the proof recorded in tools/check-proofs.json for the check's current code (gate.py reads it).
The copies run four at a time."""
import sys, os, re, json, shutil, tempfile, datetime, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate

def css(rule): return lambda h: h.replace('</head>', '<style>%s</style></head>' % rule, 1)
def first(pat, rep, flags=0):
    def f(h):
        n = re.subn(pat, rep, h, count=1, flags=flags)
        assert n[1] == 1, 'breaker found nothing to break: ' + pat
        return n[0]
    return f

def swap_photos(d):   # A: two photo files swapped
    im = os.path.join(d, 'preview', 'images'); fs = sorted(f for f in os.listdir(im) if re.match(r'00[2-5](-480)?\.jpg$', f))
    a, b = [f for f in fs if f.startswith('002')], [f for f in fs if f.startswith('003')]
    for x, y in zip(a, b):
        os.rename(os.path.join(im, x), os.path.join(im, 'tmp')); os.rename(os.path.join(im, y), os.path.join(im, x)); os.rename(os.path.join(im, 'tmp'), os.path.join(im, y))

def report_word(d):   # H: the build's report shows a word changed that no site rule allows
    p = os.path.join(d, 'report.json'); r = json.load(open(p))
    r['text_differences_word_vs_page'].append(['replace', 'consumables', 'consumabels']); json.dump(r, open(p, 'w'))

BREAK = {   # check -> (what is broken, html change or folder change)
    'A': ('two photo files swapped', swap_photos),
    'B': ('the first heading recoloured red', first(r'<h2 ', '<h2 style="color:#ff0000 !important" ')),
    'C': ('the first italic word made upright', first(r'<em>(.*?)</em>', r'\1', re.S)),
    'D': ('the first beige line before a blue heading removed', first(r'<[a-z]+ [^>]*class="[^"]*beige-rule[^"]*"[^>]*data-setting="1"[^>]*>(</[a-z]+>)?', '')),
    'E': ('photos pushed 300 px left, over the text', css('main .pim{transform:translateX(-300px)}')),
    'F': ('the a) b) c) list drawn as 1. 2. 3.', first(r'(<ol[^>]*class="[^"]*)mm-mk-alpha-paren', r'\1mm-mk-none')),
    'G': ('a 154 px gap put in the middle of a line', first(r'consumables \(paper,', 'consumables <span class="mm-t" style="display:inline-block;width:154px"></span>(paper,')),
    'H': ('the report shows a misspelt word', report_word),
    'H2': ('a word misspelt on the page', first(r'consumables', 'consumabels')),
    'K': ('list text moved off Word\'s indent', css('main .mm-wi>li{padding-left:60px !important}')),
    'P': ('photos moved 25 px down', css('main .mm-float,main .mm-co{transform:translateY(25px)}')),
    'S': ('the breaks after slashes removed', lambda h: h.replace('<wbr/>', '')),
    'T': ('the space after the labels made an ordinary trailing space', lambda h: re.sub(r'(<span class="mm-(?:lab|n)">[^<]*?) </span>', r'\1 </span>', h)),
    'PAGE': ('every paragraph left-aligned', css('main p,main li{text-align:left !important}')),
}

def make(num, key, root):
    p = gate.PAGES[num]; src = os.path.join(gate.MM, p['out']); d = os.path.join(root, key)
    shutil.copytree(os.path.join(src, 'preview'), os.path.join(d, 'preview')); shutil.copy(os.path.join(src, 'report.json'), d)
    what, f = BREAK[key]; page = os.path.join(d, 'preview', 'index.html')
    if f.__code__.co_argcount == 1 and f in (swap_photos, report_word): f(d)
    else:
        h = open(page, encoding='utf-8').read(); h2 = f(h); assert h2 != h, key + ': nothing changed'
        open(page, 'w', encoding='utf-8').write(h2)
    return os.path.join(d, 'preview')

def main(num, keys):
    root = tempfile.mkdtemp(prefix='proofs-', dir='/tmp/claude-0/-home-claude/f3d9d4de-dc3d-58c5-9b06-af678c61a8b2/scratchpad')
    preview = os.path.join(gate.MM, gate.PAGES[num]['out'], 'preview')
    with cf.ThreadPoolExecutor(2) as ex:   # 4 at once timed out the page check's screenshots
        real_f = ex.submit(gate.all_checks, num, preview)
        broken = {k: ex.submit(gate.all_checks, num, make(num, k, root)) for k in keys}
        real = real_f.result(); bad = {k: v.result() for k, v in broken.items()}
    proofs = json.load(open(gate.PROOFS)) if os.path.exists(gate.PROOFS) else {}
    hashes = gate.code_hashes(); ok = True
    for k in keys:
        what = BREAK[k][0]
        if k not in real: print('%-4s NOT RUN on %s' % (k, num)); ok = False; continue
        if not real[k]['ok']: print('%-4s fails on the real build, nothing proved: %s' % (k, real[k]['faults'][:2])); ok = False; continue
        if bad[k][k]['ok']: print('%-4s NOT PROVED: passed with "%s"' % (k, what)); ok = False; continue
        proofs[k] = {'code': hashes[k], 'page': num, 'fault_put_in': what, 'broken_copy': os.path.join(root, k),
                     'caught': bad[k][k]['faults'][:3], 'at': datetime.datetime.now().isoformat(timespec='seconds')}
        print('%-4s PROVED: "%s" -> %s' % (k, what, bad[k][k]['faults'][0][:110] if bad[k][k]['faults'] else 'FAIL'))
    json.dump(proofs, open(gate.PROOFS, 'w'), indent=1, ensure_ascii=False)
    return ok

if __name__ == '__main__':
    num = sys.argv[1]; keys = sys.argv[2:] or list(BREAK)
    sys.exit(0 if main(num, keys) else 1)
