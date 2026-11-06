#!/usr/bin/env python3
"""gate_list.py <package.zip> <build dir> <review report.md or NONE> <out file> [--page <slug>] [--kind essay|resources]
                [--gate-proofs DIR]
(5 Nov 2026; plan of 5 Nov, item 5, for a page with NO live version; owner's agreement 5 Nov 05:48, word for word: "I agree to
put the checks in tools/REQUIRED-CHECKS.txt and the allowed faults in tools/ALLOWED-FAULTS.txt, each row with its source quoted,
and to make gate.py, send_gate.sh, send_gate_nolive.sh, run_checks.sh, build_page.py and the gate mod require every row that
applies, for every page built from now on, with any change needing my written agreement")

Loads every current row of tools/REQUIRED-CHECKS.json that applies to the page (applies_to all, <kind>, nolive, page:<slug>)
and decides for each how it is met:
  - a script row: the result file that script writes in the build folder (the table RESULTS in gate_files.py). The row
    passes only if that result exists, is complete, is newer than the zip, names this package's sha256 where the result's
    format carries it (the printout says which formats do not), was written by the script the row names (same sha256), and
    its pass line holds - or every fault line it prints is matched by a row of tools/ALLOWED-FAULTS.txt for this page.
  - a "new" row: the script /home/claude/eng35/checks-plan/PLAN.md gives it (items 1-7), gate_files.py (item 8) or the eye
    (item 9). A plan item with no script written yet gives NO CHECK YET.
  - an eye row: passes only if the review report names the package's sha256 and names the row ID marked "checked" with no
    FAULT against it. The printout marks each as resting on that report.
  - a row met by the gate itself (send_gate rows, the one table): passes only when every other row passes.
Allowances come only from tools/ALLOWED-FAULTS.txt; any other argument is refused. A missing file is never a pass.
Prints every row (ID, how checked, PASS / FAULT / NOT CHECKED / NO CHECK YET, the evidence), the scripts' sha256, the counts,
and last line GATE PASSED, or GATE FAILED (n) with n the rows that do not pass. The same lines go to <out file>.
"""
import sys, os, re, json, hashlib, subprocess, datetime, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('gate_files', os.path.join(HERE, 'gate_files.py'))
GF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GF)
RESULTS, MM, FIX, TOOLS, REPO = GF.RESULTS, GF.MM, GF.FIX, GF.TOOLS, GF.REPO

# ---- PLAN.md (5 Nov) for the 157 "new" rows: which plan item checks each (copied from the plan, ids as written there)
PLAN_ITEMS = {
    1: 'A077 A119 A120 A121 A122 A123 A124 A125 A126 A127 D066 D122 D128 D136 D194 E015 E039 E041 E047 E051 E054 E036 E043',
    2: 'A005 A006 A023 A062 A091 A102 A107 A108 A109 A111 A112 A113 D139 E017',
    3: 'A013 A034 A035 D142 D143 D205 D213 E025 E049 E050',
    4: 'C050 E027 E042 E036',
    5: 'D101 E044 E043',
    6: 'A017 A044 A201 A210 A252 B005 D027 D088 E045',
    7: 'C111 E031 E046 E048 E056',
    8: ('A014 A024 A046 A047 A051 A055 A056 A083 A087 A088 A090 A110 A204 A214 A222 A253 B010 B016 B023 B040 B112 B149 B151 '
        'B152 B166 B203 B204 B253 C004 C088 C113 C114 C115 D003 D012 D014 D018 D020 D021 D023 D024 D035 D036 D040 D041 D055 '
        'D064 D071 D073 D086 D087 D089 D090 D100 D292 D297 D298 D299 D306 D310 D314 D316 D317 E008 E014'),
    9: ('A015 A026 A039 A040 A071 A085 A114 A116 A221 A223 A224 B022 B042 B132 B181 C005 D004 D005 D056 D093 D294 D295 D300 '
        'D301 D312 D313'),
}
ITEM_OF = {}
for n, s in PLAN_ITEMS.items():
    for i in s.split():
        ITEM_OF.setdefault(i, []).append(n)
ITEM_RESULT = {1: 'checks2/style.txt', 2: 'checks2/text/text-result.txt', 3: 'checks2/images.txt', 5: 'checks2/wrap.txt',
               6: 'checks2/static.txt'}
ITEM7 = {'C111': 'checks2/col.txt', 'E056': 'checks2/col.txt',
         'E046': None, 'E048': None, 'E031': None}
ITEM7_WHY = {'E046': 'place_check.py extension (caption above/below against the PDF) not written',
             'E048': 'format_check_word.py at the 11 band-edge widths not written',
             'E031': 'checked on the live site after her upload; nothing can check it before'}
NO_SCRIPT_WHY = {4: 'spacecheck.py template-rule mode (plan item 4) not written'}

# ---- send_gate rows: the parts gate_files.py checks, the rest rest on the gate itself
GATE_ROW_TO_FILES = {'E018': 'E018', 'E019': 'E019', 'C025': 'C025', 'B007': 'D089', 'E001': 'A253', 'C002': 'C002',
                     'E023': 'E023', 'C003': 'A088', 'E021': 'E021', 'E022': 'E022'}
AFTER_UPLOAD = {'B026': 'the after-upload checks run on the live page after her upload'}

SHA_CACHE = {}
MISSING_IS_FAULT = {'checks2/images-2.txt': 'the second images command of more_checks.sh (swipe, late, behaviour) wrote no result'}   # 6 Nov 2026


def sha256(p):
    k = (p, os.path.getmtime(p), os.path.getsize(p))
    if k not in SHA_CACHE:
        SHA_CACHE[k] = GF.sha256(p)
    return SHA_CACHE[k]


def applies(a, page, kind):
    return any(x.strip() in ('all', kind, 'nolive', 'page:' + page) for x in (a or '').split(';'))


def resolve_script(name):
    """the file a row's check text names"""
    n = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
    n = n.split()[0] if n else n
    if n.startswith('/'):
        return n
    m = re.match(r'^(tools-v5[\w-]*)/(.+)$', n)
    if m:
        return os.path.join(FIX, m.group(1), m.group(2))
    if n.startswith('tools/'):
        p = os.path.join(MM, n)
        return p if os.path.exists(p) else os.path.join(TOOLS, 'v8', os.path.basename(n))
    if n.startswith('qa/'):
        return os.path.join(MM, n)
    for p in (os.path.join(TOOLS, n), os.path.join(TOOLS, 'v8', n)):
        if os.path.exists(p):
            return p
    return os.path.join(TOOLS, n)


BASENAME_RESULT = {'visual_check.py': ['checks/full.txt'], 'vfast.py': ['checks/full.txt'], 'stable.py': ['checks/height.txt'],
                   'lines_v2.py': ['checks/lines.txt'], 'lines.py': ['checks/lines.txt'], 'place_check.py': ['checks/place.txt'],
                   'speed_check.py': ['checks/speed.txt'], 'format_check_word.py': ['checks2/format-word.txt'],
                   'strip_compare.py': ['checks2/strip-nolive.txt'], 'strip_compare_nolive.py': ['checks2/strip-nolive.txt'],
                   'spacecheck.py': ['checks2/space.txt'], 'heading_gap.py': ['checks2/heading-gap.txt'],
                   'check_page.py': ['checks2/check-page.txt'], 'menu_style_check.py': ['checks2/menu-style.txt'],
                   'col_check.py': ['checks2/col.txt'], 'text_rules.py': ['checks2/text/text-result.txt'],
                   'static_code.py': ['checks2/static.txt'], 'style_rules.py': ['checks2/style.txt'],
                   'images_behaviour.py': ['checks2/images.txt', 'checks2/images-2.txt'], 'wrap_sweep.py': ['checks2/wrap.txt'],
                   'run_checks.sh': ['checks/full.txt', 'checks/height.txt', 'checks/lines.txt', 'checks/place.txt', 'checks/speed.txt']}


def split_check(c):
    """the parts of a row's check text: ('eye',), ('new',), ('script', name), ('gate',), ('files', gate_files id) ..."""
    parts = []
    for p in re.split(r';|,| \+ ', c):
        p = p.strip()
        if not p:
            continue
        p = re.sub(r'^existing:', '', p).strip()
        if p == 'eye':
            parts.append(('eye',))
        elif p == 'new':
            parts.append(('new',))
        elif 'send_gate' in p:
            parts.append(('gate', p))
        elif p.startswith('setup_workspace.sh') or p.startswith('build_page.py') or p.startswith('blur tools'):
            parts.append(('files', p))
        elif re.search(r'faces locks', p):
            parts.append(('files', p))
        else:
            parts.append(('script', p))
    return parts


# ---------------------------------------------------------------- allowances
def load_allowances(page):
    out = []
    t = GF.read(os.path.join(TOOLS, 'ALLOWED-FAULTS.txt')) or ''
    for line in t.splitlines():
        if not re.match(r'^AF\d+\s*\|', line):
            continue
        f = [x.strip() for x in line.split('|')]
        if len(f) < 5:
            continue
        aid, pages, chk = f[0], f[1], f[2]
        pg = [x.strip() for x in pages.split(';')]
        ml = re.match(r'^(\S+?):\s*lines listed in (\S+)', chk)
        if ml:   # 6 Nov 2026: a file of exact lines, "kind | exact line", one width block, counted per width
            lf = ml.group(2)
            lf = lf if lf.startswith('/') else os.path.join(MM, lf)
            d = dict(id=aid, script=os.path.basename(ml.group(1)), rx=None, listfile=lf, text='lines listed in ' + lf, rows=[],
                     pages=pg, widths=f[3], applies=('page:' + page) in pg or 'all' in pg, until=(f[5] if len(f) > 5 else ''),
                     listed=Counter(), listbad=[])
            lt = GF.read(lf)
            if lt is None:
                d['listbad'].append('the allowed-lines file %s does not exist' % lf)
            else:
                d['listsha'] = sha256(lf)
                for i, x in enumerate(lt.splitlines(), 1):
                    if not x.strip() or x.startswith('#'):
                        continue
                    if ' | ' not in x:
                        d['listbad'].append('%s line %d is not "kind | exact line": %s' % (lf, i, x))
                        continue
                    d['listed'][x.split(' | ', 1)[1]] += 1
            out.append(d)
            continue
        m = re.match(r'^(\S+?):\s*lines\s*"(.+?)"\s*(\(rows ([^)]*)\))?', chk)
        if not m:
            out.append(dict(id=aid, bad='its check/fault text cannot be read: ' + chk))
            continue
        script = os.path.basename(m.group(1))
        pat = re.escape(m.group(2)).replace(r'\.\.\.', '.*?').replace(r'\ N\ ', r'\ \d+\ ')
        pat = '^' + pat.replace(r'\ ', ' ') + r'(?=:|\s*$)'
        rows = [x.strip() for x in (m.group(4) or '').split(',') if x.strip()]
        out.append(dict(id=aid, script=script, rx=re.compile(pat), text=m.group(2), rows=rows, pages=pg, widths=f[3],
                        applies=('page:' + page) in pg or 'all' in pg, until=(f[5] if len(f) > 5 else '')))
    return out


# ---------------------------------------------------------------- reading one result file
class Result:
    def __init__(s, b, key, allow):
        s.key = key
        s.info = RESULTS[key]
        s.path = os.path.join(b.B, key)
        s.exists = os.path.exists(s.path)
        s.problems = []        # make the result unusable (missing, part-written, old, other package, other script)
        s.faults = []          # fault lines not allowed
        s.allowed = []         # (line, AF id)
        s.passline = False
        s.notes = []
        s.writer = b.script(key)
        s.writer_sha = None
        if not s.exists:
            s.problems.append('result missing (%s; runner: %s)' % (key, s.info['runner']))
            return
        t = GF.read(s.path) or ''
        lines = t.splitlines()
        if not GF.complete(b, key):
            s.problems.append('part-written (no final line)')
        if os.path.getmtime(s.path) < os.path.getmtime(b.zip):
            s.problems.append('older than the zip')
        # the package sha
        if s.info['sha'] == 'full':
            m = re.search(r'package sha256: ([0-9a-f]{64})', t)
            if not m or m.group(1) != b.sha:
                s.problems.append('names package %s, not %s' % (m.group(1)[:16] if m else 'none', b.sha[:16]))
            else:
                s.notes.append('names the package sha256')
        elif s.info['sha'] == 'summary16':
            st = GF.read(os.path.join(b.B, key.split('/')[0], 'SUMMARY.txt')) or ''   # gatefix2: the run's folder (checks2/text/... -> checks2)
            m = re.search(r'package sha256 ([0-9a-f]{16})', st)
            if not m or m.group(1) != b.sha[:16]:
                s.problems.append('its run\'s SUMMARY.txt names %s, not %s' % (m.group(1) if m else 'no package', b.sha[:16]))
            else:
                s.notes.append('package sha256 (16 characters) in its run\'s SUMMARY.txt')
        else:
            s.notes.append('format carries no package sha256')
            if s.info['source'] == 'preview':
                s.notes.append('read preview/index.html (the package without copy protection)')
        # the writer and its sha
        if key == 'checks/full.txt':
            m = re.search(r'visual_check\.py sha256: ([0-9a-f]{64})', t)
            s.writer_sha = m.group(1) if m else None
        elif s.writer and os.path.exists(s.writer):
            s.writer_sha = sha256(s.writer)
            if os.path.getmtime(s.writer) > os.path.getmtime(s.path):
                s.problems.append('its script %s changed after the result was written' % os.path.relpath(s.writer, '/home/claude'))
        if not s.writer_sha:
            s.problems.append('the script that wrote it is not known')
        # pass line / faults
        if s.info.get('nopass'):
            s.problems.append(s.info['nopass'])
            return
        custom = s.info.get('custom')
        if custom == 'height':
            ok = True
            for w in ('1440', '390'):
                m = re.search(r'^width %s: \S+ (\{.*\})\s*$' % w, t, re.M)
                if not m:
                    s.faults.append('width %s: no reading' % w)
                    continue
                r = json.loads(m.group(1))
                if not (r.get('1s') == r.get('4s') == r.get('scrolled')) or r.get('largest margin', [999])[0] > 150:
                    s.faults.append('width %s: %s' % (w, m.group(1)))
            s.passline = not s.faults
            return
        if custom == 'lines':
            got = re.findall(r'^width (\d+): .*line-through-text (\d+)\s*$', t, re.M)
            for w, n in got:
                if n != '0':
                    s.faults.append('width %s: line-through-text %s' % (w, n))
            if len(got) < 8:
                s.faults.append('%d widths read, 8 needed' % len(got))
            s.passline = not s.faults
            return
        if key == 'checks2/format-word.txt':
            fw = [x for x in allow if x.get('listfile') and x['applies'] and x['script'] == os.path.basename(s.info['script'])]
            if fw:
                s.read_format_word(lines, fw)
                return
        s.passline = any(re.search(s.info['pass_re'], l) for l in lines) if s.info['pass_re'] else False
        fr = s.info['fault_re']
        summary_re = re.compile(r'^(PLACE|SPEED|STYLE|TEXT|STATIC|IMAGES|WRAP|COLUMNS) (OK|PASS|FAULT)|^RESULT|^END\s*$')
        fl = [l for l in lines if fr and re.search(fr, l) and not summary_re.search(l)] if key != 'checks2/format-word.txt' else \
            [l for l in lines if re.search(fr, l)]
        script_base = os.path.basename(s.info['script'])
        for l in fl:
            a = next((x for x in allow if x.get('rx') and x['applies'] and x['script'] == script_base and x['rx'].search(l)), None)
            if a:
                s.allowed.append((l, a['id']))
            else:
                s.faults.append(l)
        if not s.passline and not s.faults and not s.allowed:
            s.faults.append('no pass line and no fault line read (last line: %s)' % (lines[-1][:120] if lines else 'empty'))

    def read_format_word(s, lines, fw):
        """6 Nov 2026: every difference line of each width block of format_check_word.py (the lines between "-- width N" and
        "colour pairs") is matched against the allowed-lines file of the ALLOWED-FAULTS row that applies; a line is allowed
        only as many times per width as the file lists it. The check's own "ALLOWED BY A QUOTED OWNER RULE" section (after
        "colour pairs") is not a difference and stays as the check prints it. Any other line is a fault."""
        if len(fw) > 1:
            s.faults.append('more than one allowed-lines row applies to the Word-format check (%s): refused' % ', '.join(x['id'] for x in fw))
            return
        a = fw[0]
        if a['listbad']:
            s.faults.extend('allowance %s: %s' % (a['id'], x) for x in a['listbad'])
            return
        blocks, cur = [], None
        for l in lines:
            m = re.match(r'^-- width (\d+)\b', l)
            if m:
                cur = [m.group(1), [], False]
                blocks.append(cur)
                continue
            if cur is None or cur[2]:
                continue
            if l.startswith('colour pairs'):
                cur[2] = True
                continue
            if l.strip():
                cur[1].append(l)
        m = re.search(r'^RESULT: (\d+) differences', '\n'.join(lines), re.M)
        if not m:
            s.faults.append('no "RESULT: N differences" line')
        n = int(m.group(1)) if m else -1
        total = sum(len(d) for _, d, _ in blocks)
        if m and n != total:
            s.faults.append('RESULT names %d differences but the width blocks hold %d lines' % (n, total))
        for w, diffs, closed in blocks:
            if not closed:
                s.faults.append('width %s: block has no "colour pairs" line (not read to its end)' % w)
            left = Counter(a['listed'])
            for l in diffs:
                if left[l] > 0:
                    left[l] -= 1
                    s.allowed.append(('width %s: %s' % (w, l), a['id']))
                else:
                    s.faults.append('width %s: %s  [not in %s, or more times than it lists]' % (w, l, os.path.basename(a['listfile'])))
            unused = sum(left.values())
            if unused:
                s.notes.append('width %s: %d listed lines not printed (no longer differ)' % (w, unused))
        s.notes.append('Word-format lines read per width against %s (%s): widths %s' % (
            a['id'], os.path.basename(a['listfile']), ','.join(w for w, _, _ in blocks) or 'none'))
        s.passline = bool(m) and n == 0 and total == 0 and not s.faults

    def ok(s):
        """no fault line that is not allowed, and the pass line holds or every fault line printed is allowed"""
        return not s.problems and not s.faults and (s.passline or bool(s.allowed))

    def tagged(s, rid):
        return [l for l in s.faults if re.search(r'\b%s\b' % rid, l)]


# ---------------------------------------------------------------- the gate
def main():
    a = sys.argv[1:]
    known = {'--page': 1, '--kind': 1, '--gate-proofs': 1}
    pos, opt = [], {}
    i = 0
    while i < len(a):
        if a[i] in known:
            opt[a[i]] = a[i + 1]
            i += 2
        elif a[i].startswith('--'):
            print('refused: unknown option %s (allowances come only from tools/ALLOWED-FAULTS.txt)' % a[i])
            print('GATE FAILED (1)')
            sys.exit(2)
        else:
            pos.append(a[i])
            i += 1
    if len(pos) != 4:
        print(__doc__)
        print('GATE FAILED (1)')
        sys.exit(2)
    zpath, bdir, review, outp = pos
    zpath = os.path.abspath(zpath)
    b = GF.Build(bdir, True, opt.get('--gate-proofs'))
    zsha = sha256(zpath)
    page = opt.get('--page') or b.slug
    kind = opt.get('--kind', 'essay')
    out = open(outp, 'w')

    def say(x=''):
        print(x, flush=True)
        out.write(x + '\n')
        out.flush()

    integrity = []
    me = sha256(os.path.abspath(__file__))
    say('gate %s %s %s' % (datetime.datetime.now().strftime('%H:%M:%S'), page, zsha[:8]))
    say('gate_list.py sha256 %s | gate_files.py sha256 %s' % (me, sha256(os.path.join(HERE, 'gate_files.py'))))
    say('package %s sha256 %s' % (zpath, zsha))
    say('build folder %s | review report %s | page %s (%s, no live version)' % (b.B, review, page, kind))
    lst, af = os.path.join(TOOLS, 'REQUIRED-CHECKS.json'), os.path.join(TOOLS, 'ALLOWED-FAULTS.txt')
    say('list %s sha256 %s | allowances %s sha256 %s' % (lst, sha256(lst), af, sha256(af)))
    # the package must be the build's package
    if not b.zip or sha256(b.zip) != zsha:
        integrity.append('the package is not the build folder\'s zip (%s)' % b.zip)
    # self and list against the committed copies (local clone; the GitHub server itself is not fetched here)
    for p in ('gate_list.py', 'gate_files.py', 'REQUIRED-CHECKS.json', 'ALLOWED-FAULTS.txt'):
        c = os.path.join(REPO, 'workspace', 'tools', p)
        if not os.path.exists(c) or sha256(c) != sha256(os.path.join(TOOLS, p)):
            integrity.append('tools/%s is not the committed copy in %s/workspace/tools (%s)' % (p, REPO, 'absent there' if not os.path.exists(c) else 'differs'))
    # a preview band in the package
    import zipfile
    with zipfile.ZipFile(zpath) as zf:
        html = zf.read(b.slug + '/index.html').decode('utf-8', 'replace') if b.slug else ''
    if re.search(r'(id|class)="[^"]*(preview-band|check-band|mm-preview|not-passed)[^"]*"|NOT PASSED|NOT CHECKED', html):
        integrity.append('the package contains a preview band')
    # 6 Nov 2026 (owner 09:25 "#2 - agreed": the gate checks the order of the checks): the fast round must have passed
    # (checks2/FAST-PASSED for this package), the separate review report (REVIEW.md) must be written after it, and the long
    # checks (checks/SUMMARY.txt "start", checks2/SUMMARY.txt "stage long start") must have started after the review
    def _hms(path, rx):
        t = GF.read(path) or ''
        m_ = re.findall(rx, t)
        if not m_ or not os.path.exists(path): return None
        d0 = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        h, mi, se = [int(x) for x in m_[-1].split(':')]
        t_ = d0.replace(hour=h, minute=mi, second=se, microsecond=0)
        return t_ - datetime.timedelta(days=1) if t_ > d0 + datetime.timedelta(minutes=5) else t_
    fp = os.path.join(b.B, 'checks2', 'FAST-PASSED'); rvp = os.path.join(b.B, 'REVIEW.md')
    if not os.path.exists(fp) or zsha[:16] not in (GF.read(fp) or ''):
        integrity.append('order: the fast round has not passed for this package (checks2/FAST-PASSED)')
    else:
        tfast = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
        trev = datetime.datetime.fromtimestamp(os.path.getmtime(rvp)) if os.path.exists(rvp) else None
        if trev is None or trev < tfast:
            integrity.append('order: no separate review report written after the fast round passed (REVIEW.md)')
        for lp, rx, lab in ((os.path.join(b.B, 'checks', 'SUMMARY.txt'), r'^start (\d\d:\d\d:\d\d)', 'run_checks.sh'),
                            (os.path.join(b.B, 'checks2', 'SUMMARY.txt'), r'stage long start (\d\d:\d\d:\d\d)', 'more_checks.sh long')):
            tl = _hms(lp, rx)
            if tl is None: integrity.append('order: %s has not run (no start time in %s)' % (lab, lp)); continue
            if tl < tfast or (trev is not None and tl < trev - datetime.timedelta(seconds=1)):
                integrity.append('order: %s started %s, before the fast round passed (%s) or the review (%s)' % (lab, tl.strftime('%H:%M:%S'), tfast.strftime('%H:%M:%S'), trev.strftime('%H:%M:%S') if trev else 'none'))
    for x in integrity:
        say('INTEGRITY FAULT ' + x)

    allow = load_allowances(page)
    for x in allow:
        if x.get('bad'):
            say('ALLOWANCE %s REFUSED %s' % (x['id'], x['bad']))
        elif x.get('listfile'):
            say('allowance %s | script %s | lines listed in %s (sha256 %s, %d lines, counted per width)%s | pages %s | %s | %s' % (
                x['id'], x['script'], x['listfile'], x.get('listsha', 'none'), sum(x['listed'].values()),
                (' | FILE FAULT: ' + '; '.join(x['listbad'])) if x['listbad'] else '', ';'.join(x['pages']),
                'applies' if x['applies'] else 'not this page', x['until']))
        else:
            say('allowance %s | script %s | lines "%s" | rows %s | pages %s | %s | %s' % (
                x['id'], x['script'], x['text'], ','.join(x['rows']), ';'.join(x['pages']), 'applies' if x['applies'] else 'not this page', x['until']))

    # gate_files.py, run now (files only)
    gfo = outp + '.gate-files.txt'
    cmd = [sys.executable, os.path.join(HERE, 'gate_files.py'), b.B, gfo, '--nolive']
    if opt.get('--gate-proofs'):
        cmd += ['--gate-proofs', opt['--gate-proofs']]
    subprocess.run(cmd, capture_output=True, text=True)
    gfrows = {}
    gt = GF.read(gfo) or ''
    for l in gt.splitlines():
        m = re.match(r'^([A-E]\d{3}) (PASS|FAULT|NOT SCRIPTABLE) ?(.*)$', l)
        if m:
            gfrows[m.group(1)] = (m.group(2), m.group(3))
    gf_done = gt.rstrip().endswith('END')
    say('gate_files.py printout: %s (%s rows%s)' % (gfo, len(gfrows), '' if gf_done else ', NOT COMPLETE'))

    # every result file
    res = {k: Result(b, k, allow) for k in RESULTS}

    # the review report
    rep_lines, rep_ok, rep_why = [], False, ''
    if review != 'NONE':
        t = GF.read(review)
        if t is None:
            rep_why = 'review report %s not found' % review
        elif zsha[:16] not in t:
            rep_why = 'review report %s does not name this package\'s sha256 (%s)' % (review, zsha[:16])
        else:
            rep_ok, rep_lines = True, t.splitlines()
    else:
        rep_why = 'no review report given (NONE)'

    def eye(rid):
        if not rep_ok:
            return 'NOT CHECKED', rep_why
        ls = [l for l in rep_lines if re.search(r'\b%s\b' % rid, l)]
        if not ls:
            return 'NOT CHECKED', 'not in the review report (a row missing from its table counts as not checked)'
        if any(re.search(r'\bnot checked\b', l, re.I) for l in ls):
            return 'NOT CHECKED', 'the review report marks it NOT checked'
        if any(re.search(r'\bFAULTS?\b', l) and not re.search(r'\bno FAULTS?\b|FAULTS?: 0\b', l, re.I) for l in ls):
            return 'FAULT', 'the review report names a fault: ' + ' / '.join(l.strip()[:160] for l in ls)
        if any(re.search(r'\bchecked\b', l, re.I) for l in ls):
            return 'PASS', 'checked in the review report (rests on that report)'
        return 'NOT CHECKED', 'the review report names the row but not as checked'

    def script_part(rid, name):
        p = resolve_script(name)
        keys = BASENAME_RESULT.get(os.path.basename(p))
        if not keys:
            return 'NO CHECK YET', '%s: no result file is known for this script' % name, []
        outs, ev = [], []
        for k in keys:
            r = res[k]
            ev.append(r.path)
            how = os.path.relpath(r.path, b.B)
            if r.problems:
                miss = not r.exists
                if miss and k in MISSING_IS_FAULT:
                    outs.append(('FAULT', '%s: %s; %s' % (how, '; '.join(r.problems), MISSING_IS_FAULT[k])))
                    continue
                outs.append(('NOT CHECKED' if miss else 'FAULT', '%s: %s' % (how, '; '.join(r.problems))))
                continue
            # the row's script against the writer
            named_sha = sha256(p) if os.path.exists(p) else None
            sub = os.path.basename(p) == 'strip_compare.py'
            bare = '/' not in re.sub(r'\s*\(.*?\)\s*', '', name).strip()
            if bare:
                r.notes.append('the row names no folder for %s: the runner\'s copy is taken (its version is judged by rows D024/B253)' % os.path.basename(p)) \
                    if not any('names no folder' in n for n in r.notes) else None
            if sub:
                pass   # no live page: strip_compare_nolive.py stands in (send_gate_nolive.sh header, owner 31 Oct 21:08)
            elif bare:
                pass
            elif named_sha is None:
                outs.append(('FAULT', '%s: the script the row names (%s) does not exist' % (how, p)))
                continue
            elif os.path.basename(p) == 'run_checks.sh':
                pass
            elif named_sha != r.writer_sha:
                outs.append(('FAULT', '%s written by %s %s; the row names %s %s' % (
                    how, os.path.relpath(r.writer, '/home/claude') if r.writer else '?', (r.writer_sha or '?')[:8],
                    os.path.relpath(p, '/home/claude'), named_sha[:8])))
                continue
            if r.ok():
                d = 'pass line holds' if r.passline else 'every fault line allowed (%s)' % ', '.join(sorted(set(x[1] for x in r.allowed)))
                outs.append(('PASS', '%s: %s; %s%s' % (how, d, '; '.join(r.notes), ' (no-live stand-in for strip_compare.py)' if sub else '')))
            else:
                own = r.tagged(rid)
                outs.append(('FAULT', '%s: %d fault lines not allowed (%d naming %s)%s; e.g. %s' % (
                    how, len(r.faults), len(own), rid, (', %d allowed' % len(r.allowed)) if r.allowed else '',
                    (own or r.faults)[0][:200])))
        return worst(outs), ' | '.join(d for _, d in outs), ev

    rows = [r for r in json.load(open(lst)) if r.get('status') == 'current' and applies(r.get('applies_to'), page, kind)]
    table = []
    for r in rows:
        rid = r['id']
        parts = split_check(r['check'])
        outs = []   # (outcome, how, detail, evidence)
        for pt in parts:
            if pt[0] == 'eye':
                o, d = eye(rid)
                outs.append((o, 'eye', d, review if rep_ok else '-'))
            elif pt[0] == 'new':
                its = ITEM_OF.get(rid)
                if not its:
                    outs.append(('NO CHECK YET', 'new', 'not in PLAN.md', '-'))
                for it in its or []:
                    if it == 9:
                        if rid == 'B042':
                            outs.append(('NO CHECK YET', 'plan 9', 'excluded in the plan, to be decided', '-'))
                        else:
                            o, d = eye(rid)
                            outs.append((o, 'plan 9 eye', d, review if rep_ok else '-'))
                    elif it == 8:
                        g = gfrows.get(rid)
                        if not g:
                            outs.append(('NOT CHECKED', 'plan 8 gate_files.py', 'no line for this row in the gate_files.py printout', gfo))
                        elif g[0] == 'NOT SCRIPTABLE' and g[1].startswith('-> gate_list'):
                            outs.append(('SELF', 'plan 8 this gate', g[1], outp))
                        elif g[0] == 'NOT SCRIPTABLE':
                            o, d = eye(rid)
                            outs.append((o, 'plan 8 -> eye', '%s [gate_files: %s]' % (d, g[1][len('-> eye: '):]), review if rep_ok else '-'))
                        else:
                            outs.append((g[0], 'plan 8 gate_files.py', g[1], gfo))
                    elif it == 7:
                        k = ITEM7.get(rid)
                        if k:
                            o, d, ev = script_part(rid, os.path.basename(RESULTS[k]['script']))
                            outs.append((o, 'plan 7 ' + os.path.basename(RESULTS[k]['script']), d, ', '.join(ev)))
                        else:
                            outs.append(('NO CHECK YET', 'plan 7', ITEM7_WHY.get(rid, 'no script'), '-'))
                    elif it in ITEM_RESULT:
                        k = ITEM_RESULT[it]
                        o, d, ev = script_part(rid, os.path.basename(RESULTS[k]['script']))
                        outs.append((o, 'plan %d %s' % (it, os.path.basename(RESULTS[k]['script'])), d, ', '.join(ev)))
                    else:
                        outs.append(('NO CHECK YET', 'plan %d' % it, NO_SCRIPT_WHY.get(it, 'no script written'), '-'))
            elif pt[0] == 'gate':
                if rid in AFTER_UPLOAD:
                    outs.append(('NOT CHECKED', 'after upload', AFTER_UPLOAD[rid] + ' (cannot be met before upload)', '-'))
                elif rid in GATE_ROW_TO_FILES:
                    g = gfrows.get(GATE_ROW_TO_FILES[rid])
                    outs.append(((g[0] if g and g[0] != 'NOT SCRIPTABLE' else 'NOT CHECKED'), 'gate_files.py ' + GATE_ROW_TO_FILES[rid],
                                 g[1] if g else 'no line in gate_files.py', gfo))
                else:
                    outs.append(('SELF', 'this gate', 'met only when every other row passes', outp))
            elif pt[0] == 'files':
                gid = GATE_ROW_TO_FILES.get(rid)
                g = gfrows.get(gid) if gid else None
                if not g:
                    outs.append(('NO CHECK YET', pt[1], 'no file check for this row', '-'))
                elif g[0] == 'NOT SCRIPTABLE':
                    o, d = eye(rid)
                    outs.append((o, pt[1] + ' -> eye', d, review if rep_ok else '-'))
                else:
                    outs.append((g[0], 'gate_files.py ' + gid, g[1], gfo))
            else:
                o, d, ev = script_part(rid, pt[1])
                outs.append((o, os.path.basename(resolve_script(pt[1])), d, ', '.join(ev) or '-'))
        table.append([rid, outs])

    # rows that rest on the gate itself
    def row_outcome(outs, gate_ok):
        o = [x[0] if x[0] != 'SELF' else ('PASS' if gate_ok else 'FAULT') for x in outs]
        return worst([(x, '') for x in o])

    pre = [row_outcome(o, True) for _, o in table]
    others_ok = all(x == 'PASS' for x, (_, o) in zip(pre, table) if not any(y[0] == 'SELF' for y in o)) and not integrity
    counts = {}
    say('')
    say('ROW | HOW CHECKED | OUTCOME | EVIDENCE')
    nbad = 0
    for rid, outs in table:
        o = row_outcome(outs, others_ok)
        counts[o] = counts.get(o, 0) + 1
        nbad += o != 'PASS'
        how = ' + '.join(x[1] for x in outs)
        det = ' || '.join(('%s: %s' % (x[0], x[2])) if len(outs) > 1 else x[2] for x in outs)
        if any(x[0] == 'SELF' for x in outs) and not others_ok:
            det += ' || rests on the gate: other rows or the integrity checks do not pass'
        ev = ', '.join(sorted(set(x[3] for x in outs if x[3] and x[3] != '-'))) or '-'
        rest = ' [rests on the review report]' if any('eye' in x[1] for x in outs) else ''
        say('%s | %s | %s | %s | %s%s' % (rid, how, o, ev, det, rest))

    say('')
    say('SCRIPTS (sha256 of each script whose result was read):')
    fp = GF.fingerprints()
    seen = set()
    for k, r in res.items():
        if r.exists and r.writer and r.writer not in seen:
            seen.add(r.writer)
            s = r.writer_sha or '?'
            say('  %s %s | writes %s | FINGERPRINTS.txt: %s' % (s, r.writer, k, 'listed' if s in fp.get(os.path.normpath(r.writer), set()) else 'NOT listed with this sha'))
    say('  %s %s (this gate)' % (me, os.path.abspath(__file__)))
    say('  %s %s' % (sha256(os.path.join(HERE, 'gate_files.py')), os.path.join(HERE, 'gate_files.py')))
    say('RESULT FILES:')
    for k, r in res.items():
        say('  %s | %s | %s' % (k, 'present' if r.exists else 'MISSING', ('pass' if r.ok() else ('; '.join(r.problems) or '%d fault lines not allowed, %d allowed' % (len(r.faults), len(r.allowed))))
                                if r.exists else r.info['runner']))
    say('')
    say('rows that apply: %d | %s' % (len(table), ' | '.join('%s %d' % (k, counts[k]) for k in ('PASS', 'FAULT', 'NOT CHECKED', 'NO CHECK YET') if k in counts)))
    if integrity:
        say('integrity faults: %d' % len(integrity))
    n = nbad + len(integrity)
    say('GATE PASSED' if n == 0 else 'GATE FAILED (%d)' % n)
    out.close()
    sys.exit(0 if n == 0 else 1)


ORDER = {'FAULT': 0, 'NO CHECK YET': 1, 'NOT CHECKED': 2, 'SELF': 3, 'PASS': 4}


def worst(outs):
    if not outs:
        return 'NO CHECK YET'
    return min((o for o, _ in outs), key=lambda x: ORDER[x])


if __name__ == '__main__':
    main()
