#!/usr/bin/env python3
"""gate_files.py <build dir> <out file> [--nolive] [--gate-proofs DIR]   (5 Nov 2026; plan of 5 Nov, item 8 of
/home/claude/eng35/checks-plan/PLAN.md; owner's agreement 5 Nov 05:48, word for word: "I agree to put the checks in
tools/REQUIRED-CHECKS.txt and the allowed faults in tools/ALLOWED-FAULTS.txt, each row with its source quoted, and to make
gate.py, send_gate.sh, send_gate_nolive.sh, run_checks.sh, build_page.py and the gate mod require every row that applies, for
every page built from now on, with any change needing my written agreement")

The file and record checks: rows of tools/REQUIRED-CHECKS.json that can be judged from files alone (the build folder, its
zips, the build log, the check results, the records, the templates clone, FINGERPRINTS.txt, check-proofs.json). No browser,
nothing is built or run except sha256 and git. Rows that cannot be judged from files are printed NOT SCRIPTABLE -> eye, with
the reason (gate_list.py then needs the review report for them). A row whose reason starts "-> gate_list" is met by
gate_list.py's own printout.

Prints one line per row: "<ID> PASS|FAULT|NOT SCRIPTABLE <detail>", then GATE-FILES PASS or GATE-FILES FAULT (n), then END.
The same lines go to <out file>. Nothing is cut short (row D021). Exit 0 only on GATE-FILES PASS.

RESULTS below is the one table of which check writes which result file in a build folder; gate_list.py reads it from here.
"""
import sys, os, re, json, glob, hashlib, zipfile, subprocess, datetime, time

MM = '/home/claude/mm'
REPO = '/home/claude/montessori-mentor-templates'
FIX = REPO + '/handover-2026-10-29-evening'
TOOLS = MM + '/tools'

# ---- the result files a build folder holds, and how each is read (shared with gate_list.py) ----
# key: path in the build folder. script: the file that writes it (as run by its runner). runner: who runs it.
# pass: regex of the line that counts as a pass. fault: regex of a fault line. sha: how the result names the package
# ('full' = the whole sha256 in the file, 'summary16' = the first 16 characters in SUMMARY.txt of the same run folder,
# None = the format does not carry it). source: what the script reads ('zip' = the package, 'preview' = preview/index.html,
# the package without copy protection). complete: regex the last non-blank line must match (a part-written result fails).
CFIX = None   # the check folder run_checks.sh used; found from the visual_check.py sha that full.txt names
RESULTS = {
    'checks/full.txt':   dict(script='{C}/visual_check.py', runner='run_checks.sh (vfast.py)', pass_re=r'^RESULT: every width ok\s*$',
                              fault_re=r'^\s*\d+\s+FAULT\b', sha='full', source='zip', complete=r'^(RESULT|\s*\d+ narrowed)'),
    'checks/height.txt': dict(script='{C}/stable.py', runner='run_checks.sh', pass_re=None, fault_re=None, sha='summary16',
                              source='zip', complete=r'^width 390:', custom='height'),
    # 6 Nov 2026 (gatefix2 C1): run_checks.sh runs $G/lines_v2.py and $G/v8/place_check.py (its 5 Nov 16:0x header), so these
    # are the writers - not {C}/lines.py and tools/place_check.py (v1)
    'checks/lines.txt':  dict(script=TOOLS + '/lines_v2.py', runner='run_checks.sh', pass_re=None, fault_re=None, sha='summary16',
                              source='zip (served unpacked)', complete=r'^width 1440:', custom='lines'),
    'checks/place.txt':  dict(script=TOOLS + '/v8/place_check.py', runner='run_checks.sh', pass_re=r'^PLACE OK\s*$',
                              fault_re=r'\bfault\b', sha='summary16', source='zip', complete=r'^PLACE (OK|FAULT)'),
    'checks/speed.txt':  dict(script='{C}/speed_check.py', runner='run_checks.sh', pass_re=r'^SPEED OK\s*$',
                              fault_re=r'^\s*\d+\s+FAULT\b', sha='summary16', source='zip', complete=r'^SPEED (OK|FAULT)'),
    'checks2/format-word.txt': dict(script=TOOLS + '/v8/format_check_word.py', runner='more_checks.sh', pass_re=r'^RESULT: 0 differences',
                              fault_re=r'^RESULT: [1-9]\d* differences', sha='summary16', source='zip', complete=r'^RESULT'),
    'checks2/col.txt':   dict(script=TOOLS + '/col_check.py', runner='more_checks.sh', pass_re=r'^COLUMNS OK\s*$',
                              fault_re=r'^(COLUMN FAULT|NOT FOUND)\b', sha='summary16', source='zip (unpacked)', complete=r'^COLUMNS (OK|FAULT)'),
    'checks2/text/text-result.txt': dict(script=TOOLS + '/text_rules.py', runner='more_checks.sh', pass_re=r'^TEXT PASS\s*$',
                              fault_re=r'^FAULT\b', sha='summary16', source='zip (unpacked)', complete=r'^END\s*$'),
    'checks2/static.txt': dict(script=TOOLS + '/static_code.py', runner='more_checks.sh', pass_re=r'^STATIC PASS\s*$',
                              fault_re=r'^FAULT\b', sha='summary16', source='zip', complete=r'^END\s*$'),
    'checks2/style.txt': dict(script=TOOLS + '/style_rules.py', runner='more_checks.sh', pass_re=r'^STYLE PASS\s*$',
                              fault_re=r'^FAULT\b', sha='summary16', source='zip (unpacked)', complete=r'^END\s*$'),
    'checks2/images.txt': dict(script=TOOLS + '/images_behaviour.py', runner='more_checks.sh', pass_re=r'^IMAGES PASS\s*$',
                              fault_re=r'^FAULT\b', sha='summary16', source='zip (unpacked)', complete=r'^END\s*$'),
    # 6 Nov 2026: the images check runs as two commands in more_checks.sh (images.txt = heights at the 122 widths;
    # images-2.txt = swipe, late images, behaviour); the gate needs both, and a missing images-2.txt is a FAULT
    'checks2/images-2.txt': dict(script=TOOLS + '/images_behaviour.py', runner='more_checks.sh', pass_re=r'^IMAGES PASS\s*$',
                              fault_re=r'^FAULT\b', sha='summary16', source='zip (unpacked)', complete=r'^END\s*$'),
    'checks2/wrap.txt':  dict(script=TOOLS + '/wrap_sweep.py', runner='more_checks.sh', pass_re=r'^WRAP PASS\s*$',
                              fault_re=r'^(?!(127\.0\.0\.1|WRAP |END|INFO|==|#|\s*$)).+', sha='summary16', source='zip (unpacked)', complete=r'^END\s*$'),
    # 6 Nov 2026 (gatefix2 C4): the code check against Word and the spacing check, written by more_checks.sh (they were
    # run only by hand or by send_gate_nolive.sh, to its own printout / <zip>.space.txt, never to the build folder)
    'checks2/strip-nolive.txt': dict(script=TOOLS + '/v8/strip_compare_nolive.py', runner='more_checks.sh',
                              pass_re=r'ALL CHECKS OK', fault_re=r'^.*\bFAULT\b', sha='summary16', source='zip', complete=r'RESULT'),
    'checks2/space.txt': dict(script=TOOLS + '/spacecheck.py', runner='more_checks.sh', pass_re=r'^RESULT: SPACING OK\s*$',
                              fault_re=r'^RESULT: \d+ FAULTS', sha='summary16', source='zip (unpacked)', complete=r'^RESULT'),
    # written by no runner yet (run_checks.sh and more_checks.sh do not run them): the rows that name them read as NOT CHECKED
    'checks2/heading-gap.txt': dict(script=TOOLS + '/v8/heading_gap.py', runner='(no runner writes this file yet)', pass_re=None,
                              fault_re=None, sha=None, source='?', complete=r'.', nopass='the script prints measurements only, no pass line'),
    'checks2/check-page.txt': dict(script=TOOLS + '/check_page.py', runner='(no runner writes this file yet)', pass_re=None,
                              fault_re=None, sha=None, source='?', complete=r'.', nopass='the script prints measurements only, no pass line'),
    'checks2/menu-style.txt': dict(script=MM + '/qa/menu_style_check.py', runner='(no runner writes this file yet)', pass_re=r'\bPASS\b|\bOK\b',
                              fault_re=r'\bFAULT\b', sha=None, source='?', complete=r'.'),
    'setup.log':         dict(script=TOOLS + '/setup_workspace.sh', runner='(setup_workspace.sh output is not kept in a file)',
                              pass_re=r'SET-UP SUCCEEDED', fault_re=r'SET-UP FAILED|\bFAILED\b', sha=None, source='-', complete=r'SET-UP'),
}
RUNNER_FILES = {'run_checks.sh': TOOLS + '/run_checks.sh', 'more_checks.sh': TOOLS + '/more_checks.sh'}
CHECK_DIRS = [FIX + '/tools-v5-fixA-200', FIX + '/tools-v5-fixA', FIX + '/tools-v5', TOOLS]


_SHA = {}


def sha256(p):
    k = (p, os.path.getmtime(p), os.path.getsize(p))
    if k in _SHA:
        return _SHA[k]
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    _SHA[k] = h.hexdigest()
    return _SHA[k]


def read(p):
    try:
        with open(p, encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return None


def mtime(p):
    try:
        return os.path.getmtime(p)
    except OSError:
        return None


def hm(t):
    return datetime.datetime.fromtimestamp(t).strftime('%d %b %H:%M:%S') if t else '-'


class Build:
    def __init__(s, bdir, nolive=None, gate_proofs=None):
        s.B = os.path.abspath(bdir.rstrip('/'))
        s.P = os.path.dirname(s.B)
        s.name = os.path.basename(s.B)
        s.nolive = nolive
        s.gate_proofs = gate_proofs
        s.report = {}
        try:
            s.report = json.load(open(os.path.join(s.B, 'report.json')))
        except Exception:
            pass
        z = s.report.get('zip')
        s.zip = os.path.join(MM, z) if z and not os.path.isabs(z) else z
        if not s.zip or not os.path.exists(s.zip):
            c = [p for p in glob.glob(os.path.join(s.B, '*.zip')) if not re.search(r'-(originals|CHECK-ONLY|UPLOAD)', p)]
            s.zip = c[0] if len(c) == 1 else None
        s.slug = None
        s.sha = None
        if s.zip:
            s.sha = sha256(s.zip)
            with zipfile.ZipFile(s.zip) as zf:
                s.names = zf.namelist()
            s.slug = s.names[0].split('/')[0]
        s.log = os.path.join(s.P, s.name + '.log')
        s.logtext = read(s.log) or ''
        s.cfix = None
        full = read(os.path.join(s.B, 'checks/full.txt')) or ''
        m = re.search(r'visual_check\.py sha256: ([0-9a-f]{64})', full)
        s.full_vc_sha = m.group(1) if m else None
        if s.full_vc_sha:
            for d in CHECK_DIRS:
                p = os.path.join(d, 'visual_check.py')
                if os.path.exists(p) and sha256(p) == s.full_vc_sha:
                    s.cfix = d
                    break

    def script(s, key):
        sc = RESULTS[key]['script']
        if '{C}' in sc:
            return sc.replace('{C}', s.cfix) if s.cfix else None
        return sc

    def results_present(s):
        return [k for k in RESULTS if os.path.exists(os.path.join(s.B, k))]

    def run_window(s, folder):
        """start and end of the run that wrote a check folder, from its SUMMARY.txt (times of day; date from the file)"""
        p = os.path.join(s.B, folder, 'SUMMARY.txt')
        t = read(p)
        if t is None:
            return None
        return window_of(p, t)


def window_of(p, t):
    d = datetime.datetime.fromtimestamp(os.path.getmtime(p)).date()
    m1 = re.search(r'^start (\d\d:\d\d:\d\d)', t, re.M)
    m2 = re.search(r'^end (\d\d:\d\d:\d\d)', t, re.M)
    if not m1:
        return None
    a = datetime.datetime.combine(d, datetime.time.fromisoformat(m1.group(1))).timestamp()
    b = datetime.datetime.combine(d, datetime.time.fromisoformat(m2.group(1))).timestamp() if m2 else os.path.getmtime(p)
    if a > b:
        a -= 86400
    return a, b, bool(m2)


def fingerprints():
    """every FINGERPRINTS.txt entry: absolute path -> sha"""
    fp = {}
    for f, base in ((MM + '/FINGERPRINTS.txt', MM), (TOOLS + '/v8/FINGERPRINTS.txt', TOOLS + '/v8'),
                    (REPO + '/workspace/FINGERPRINTS.txt', REPO + '/workspace'),
                    # 6 Nov 2026 (gatefix2 C3): the check folder run_checks.sh is given (tools-v5-fixA-200, owner 5 Nov 09:16)
                    (FIX + '/tools-v5-fixA-200/FINGERPRINTS.txt', FIX + '/tools-v5-fixA-200')):
        for line in (read(f) or '').splitlines():
            m = re.match(r'^([0-9a-f]{64})\s+\*?(.+)$', line.strip())
            if m:
                fp.setdefault(os.path.normpath(os.path.join(base, m.group(2))), set()).add(m.group(1))
    return fp


def scripts_used(b):
    """(script path, result key) for every result present, plus the runners"""
    out = []
    for k in b.results_present():
        p = b.script(k)
        out.append((p, k))
    for r, p in RUNNER_FILES.items():
        if any(RESULTS[k]['runner'].startswith(r) for k in b.results_present()):
            out.append((p, 'runner'))
    return out


# ----------------------------------------------------------------- the rows
ROWS = []


def row(*ids):
    def deco(f):
        ROWS.append((ids, f))
        return f
    return deco


def ns(reason):
    return ('NOT SCRIPTABLE', '-> eye: ' + reason)


@row('A014', 'A051')
def originals(b):
    p = os.path.join(b.B, (b.slug or '?') + '-originals.zip')
    if not os.path.exists(p):
        return 'FAULT', 'no originals zip %s' % p
    with zipfile.ZipFile(p) as zf:
        n = [x for x in zf.namelist() if not x.endswith('/')]
    bad = [x for x in n if not re.match(r'^(.*/)?\d{3}\.\w+$', x)]
    if not n or bad:
        return 'FAULT', 'originals zip %s: %d files, %d not numbered (e.g. %s)' % (p, len(n), len(bad), bad[:3])
    return 'PASS', 'originals zip %s: %d numbered files (sending it after publishing is a message act, not in files)' % (os.path.basename(p), len(n))


@row('A024', 'A214')
def drive(b):
    hits = []
    for f in [b.log, os.path.join(b.B, 'report.json')] + glob.glob(os.path.join(b.P, '*.build.sh')) + glob.glob(os.path.join(MM, 'pages', (b.slug or '?') + '.build.sh')):
        t = read(f) or ''
        for m in re.finditer(r'(drive\.google\.com/\S+|[Dd]rive (file )?id[: ]+[\w-]{20,})', t):
            hits.append('%s: %s' % (os.path.basename(f), m.group(0)[:120]))
    if not hits:
        return 'FAULT', 'no record of the Word file\'s Google Drive id: the build log %s, report.json and the build command file name none' % b.log
    return 'PASS', '; '.join(hits[:3])


def template_commits(b):
    """commits of the Essay/Resources template since this page's first build"""
    first = None
    # 6 Nov 2026 (gatefix2 C7): superseded builds are deleted (D310), so their run logs (run-bN.log) also date the first build
    for d in glob.glob(os.path.join(b.P, 'b*.log')) + glob.glob(os.path.join(b.P, 'b*')) + glob.glob(os.path.join(b.P, 'run-b*.log')):
        t = mtime(d)
        if t and (first is None or t < first):
            first = t
    if not first:
        return None, []
    since = datetime.datetime.fromtimestamp(first - 60).strftime('%Y-%m-%d %H:%M:%S')
    try:
        o = subprocess.run(['git', '-C', REPO, 'log', '--since=' + since, '--format=%h|%ci|%s', '--',
                            'Essay Code Template.html', 'Resources Code Template.html'], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return first, None
    return first, [l.split('|', 2) for l in o.splitlines() if l.strip()]


def agreement_for(commit_msg):
    """the decisions-log entry the commit message cites ('owner 5 Nov 09:16 agreement')"""
    m = re.search(r'(?:owner )?(\d{1,2} \w{3}) (\d\d:\d\d) (?:agreement|Yes)\b', commit_msg)   # gatefix2 C7: "6 Nov 00:19 agreement" too
    if not m:
        return None, 'the commit cites no owner agreement time'
    when = '%s %s' % (m.group(1), m.group(2))
    for f in sorted(glob.glob(MM + '/records/DECISIONS-LOG*.md')):
        for line in (read(f) or '').splitlines():
            if when in line and re.search(r'AGREEMENT', line):
                return line, when
    return None, when


@row('A046', 'A047', 'B040', 'A222', 'D292')
def template_agreements(b):
    first, cs = template_commits(b)
    if cs is None:
        return 'FAULT', 'git log of the templates clone could not be read'
    if not cs:
        return 'PASS', 'no template commit since this page\'s first build (%s)' % hm(first)
    bad, ok = [], []
    for h, when, msg in cs:
        line, w = agreement_for(msg)
        if not line:
            bad.append('%s (%s): no word-for-word AGREEMENT entry in records/DECISIONS-LOG*.md for "%s"' % (h, when[:16], w))
            continue
        q = re.search(r'"(I agree[^"]+)"', line)
        if not q:
            bad.append('%s: agreement for %s has no "I agree ..." sentence' % (h, w))
            continue
        s = q.group(1)
        miss = [n for n, r in (('which widths', r'\d+ ?px|every width|all widths'), ('which pages', r'\bon [A-Z]|every page|all pages'))
                if not re.search(r, s)]
        if miss:
            bad.append('%s: sentence of %s does not state %s' % (h, w, ' and '.join(miss)))
        else:
            ok.append('%s<-%s' % (h, w))
    d = 'template commits since %s: %d; agreed with what/widths/pages: %s' % (hm(first), len(cs), ', '.join(ok) or 'none')
    if bad:
        return 'FAULT', d + ' | ' + ' | '.join(bad) + ' (the before-check, size test, load test and agent after-check of D292 are not in files: eye)'
    return 'PASS', d + ' (the before-check, size test, load test and agent after-check of D292 are not in files: eye)'


@row('A055', 'A056', 'B166')
def go_rule(b):
    return ns('whether a build came only after her "go" is in her messages, not in files')


def proofs_for(b):
    rec = {}
    try:
        for k, v in json.load(open(TOOLS + '/check-proofs.json')).items():
            rec.setdefault(v.get('code'), []).append(k)
    except Exception:
        pass
    used, miss, ok = {}, [], []
    for p, k in scripts_used(b):
        if p and os.path.exists(p) and k != 'runner':
            used[p] = sha256(p)
    for p, s in sorted(used.items()):
        (ok if s in rec else miss).append('%s %s' % (os.path.relpath(p, '/home/claude'), s[:8]))
    return ok, miss


@row('A083', 'A090', 'D018', 'D064', 'D086')
def proofs(b):
    ok, miss = proofs_for(b)
    if not ok and not miss:
        return 'FAULT', 'no check result in the build folder, so no script to look up'
    d = 'tools/check-proofs.json holds a planted-fault proof for %d of %d scripts used' % (len(ok), len(ok) + len(miss))
    if miss:
        return 'FAULT', d + '; none recorded for: ' + ', '.join(miss)
    return 'PASS', d


@row('D089')
def gate_proof(b):
    g = b.gate_proofs or (TOOLS + '/gate-proofs')
    p = os.path.join(g, 'PROOFS.txt')
    t = read(p)
    if t is None:
        return 'FAULT', 'no proof record %s for gate_list.py reading the checks\' outputs' % p
    cur = sha256(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gate_list.py'))
    if cur not in t:
        return 'FAULT', '%s does not name the current gate_list.py sha256 %s' % (p, cur[:16])
    if not (re.search(r'PASS row turned FAULT', t) and re.search(r'allowed fault accepted', t)):
        return 'FAULT', '%s does not show both ways (a planted fault caught and an allowed fault accepted)' % p
    return 'PASS', '%s: gate_list.py %s proven both ways' % (p, cur[:16])


@row('A087', 'A204', 'E014')
def by_converter(b):
    f = []
    if not b.zip:
        return 'FAULT', 'no package zip in %s' % b.B
    if not re.search(r'^zip: \S+%s\.zip\s*$' % re.escape(b.slug), b.logtext, re.M):
        f.append('build log %s does not end with build_page.py\'s "zip:" line' % b.log)
    lt, zt = mtime(b.log), mtime(b.zip)
    if lt is None or zt is None or abs(lt - zt) > 30:
        f.append('zip written %s, build log %s (not the same build run)' % (hm(zt), hm(lt)))
    hz = os.path.join(b.B, 'hostinger', b.slug)
    with zipfile.ZipFile(b.zip) as zf:
        for n in zf.namelist():
            if n.endswith('/'):
                continue
            hp = os.path.join(b.B, 'hostinger', n)
            if not os.path.exists(hp):
                f.append('%s in the zip, not in hostinger/' % n)
            elif mtime(hp) > zt + 5:
                f.append('%s changed after the zip was made (%s)' % (hp, hm(mtime(hp))))
            if n.endswith('index.html') and os.path.exists(hp) and zf.read(n) != open(hp, 'rb').read():
                f.append('the zip\'s index.html differs from hostinger/%s' % n)
    pv = os.path.join(b.B, 'preview', 'index.html')
    if os.path.exists(pv) and mtime(pv) > zt + 5:
        f.append('preview/index.html changed after the zip was made')
    if f:
        return 'FAULT', '; '.join(f[:12]) + (' (+%d more)' % (len(f) - 12) if len(f) > 12 else '')
    return 'PASS', 'zip and hostinger/ files are build_page.py\'s output of one run (%s), nothing changed after; a rebuild-and-compare was not run (no rebuild while another check uses the processors)' % hm(zt)


EXPECTED = ['checks/full.txt', 'checks/height.txt', 'checks/lines.txt', 'checks/place.txt', 'checks/speed.txt',
            'checks2/format-word.txt', 'checks2/col.txt', 'checks2/text/text-result.txt', 'checks2/static.txt',
            'checks2/style.txt', 'checks2/images.txt', 'checks2/images-2.txt', 'checks2/wrap.txt']


@row('A088')
def all_rerun(b):
    miss = [k for k in EXPECTED if not os.path.exists(os.path.join(b.B, k))]
    old = [k for k in EXPECTED if k not in miss and mtime(os.path.join(b.B, k)) < mtime(b.zip)]
    st = os.path.join(MM, 'pages', (b.slug or '?') + '.py')
    later = mtime(st) > mtime(b.log) if os.path.exists(st) and mtime(b.log) else False
    if miss or old or later:
        return 'FAULT', 'results missing: %s; older than the zip: %s%s' % (', '.join(miss) or 'none', ', '.join(old) or 'none',
            '; page settings %s changed after this build (%s): this build is not of the current settings' % (st, hm(mtime(st))) if later else '')
    return 'PASS', 'all %d results of run_checks.sh and more_checks.sh present and newer than the zip' % len(EXPECTED)


@row('A110')
def doubts(b):
    p = os.path.join(b.B, 'checks2/text/doubts.txt')
    if not os.path.exists(p):
        return 'FAULT', 'no doubts list %s (text_rules.py writes it)' % p
    return 'PASS', '%s, %d lines (sending it to her is a message act)' % (p, len((read(p) or '').splitlines()))


def setup_log(b):
    c = [p for p in (os.path.join(b.B, 'setup.log'), os.path.join(b.P, 'setup.log')) if os.path.exists(p)]
    c += sorted(glob.glob(MM + '/records/setup-*.log'))
    return c[-1] if c else None


@row('A253', 'D003')
def setup_before(b):
    p = setup_log(b)
    if not p:
        return 'FAULT', 'no setup log kept (setup_workspace.sh prints its table to the reply only); looked for %s/setup.log, %s/setup.log, %s/records/setup-*.log' % (b.B, b.P, MM)
    t = read(p)
    if 'SET-UP SUCCEEDED' not in t:
        return 'FAULT', '%s does not end SET-UP SUCCEEDED' % p
    if mtime(p) > mtime(b.zip):
        return 'FAULT', 'set-up %s after the build %s' % (hm(mtime(p)), hm(mtime(b.zip)))
    return 'PASS', '%s SET-UP SUCCEEDED at %s, before the build' % (p, hm(mtime(p)))


@row('D299')
def disk(b):
    p = setup_log(b)
    if not p:
        return 'FAULT', 'no setup log, so no record of the free disk at chat start'
    m = re.search(r'Free disk\S*\s*\|?\s*(succeeded|FAILED)\s*\|?\s*([^\n|]*)', read(p))
    if not m:
        return 'FAULT', '%s has no free-disk row' % p
    return ('PASS' if m.group(1) == 'succeeded' else 'FAULT'), 'free disk: %s %s' % (m.group(1), m.group(2).strip())


@row('B010')
def no_blur(b):
    m = re.search(r'^faces - .*$', b.logtext, re.M)
    if not m:
        return 'FAULT', 'the build log names no faces line'
    l = m.group(0)
    if 'no-blur' in l or 'no blur' in l:
        j = re.search(r'(\S+noblur\S*\.json|\S+no-blur\S*\.json)', b.logtext)
        if not j or not os.path.exists(os.path.join(MM, j.group(1))):
            return 'FAULT', 'built with no blurring but no record of her words: %s' % l[:160]
        return 'PASS', 'no blurring, her words in %s' % j.group(1)
    return 'PASS', 'blurring used, not the no-blur option: %s' % l[:200]


@row('B016', 'C114')
def one_table(b):
    return 'NOT SCRIPTABLE', '-> gate_list: met by gate_list.py\'s printout (the one table of every row that applies)'


def overlap(b):
    mine = []
    for f in glob.glob(os.path.join(b.B, 'checks*', 'SUMMARY.txt')):
        w = window_of(f, read(f))
        if w:
            mine.append((os.path.relpath(f, b.P), w))
    others = []
    for f in glob.glob(os.path.join(b.P, '*', 'checks*', 'SUMMARY.txt')):
        if f.startswith(b.B + '/'):
            continue
        w = window_of(f, read(f))
        if w:
            others.append((os.path.relpath(f, b.P), w))
    clash = []
    allw = mine + others
    for i, (n1, w1) in enumerate(mine):
        for n2, w2 in allw:
            if n2 == n1:
                continue
            if w1[0] < w2[1] and w2[0] < w1[1]:
                clash.append('%s (%s-%s) overlaps %s (%s-%s)' % (n1, hm(w1[0])[-8:], hm(w1[1])[-8:], n2, hm(w2[0])[-8:], hm(w2[1])[-8:]))
    return mine, clash


@row('B023', 'B152', 'C088', 'D012')
def nothing_beside(b):
    mine, clash = overlap(b)
    if not mine:
        return 'FAULT', 'no run times recorded (no checks*/SUMMARY.txt with a start line)'
    if clash:
        return 'FAULT', 'check runs at the same time: ' + '; '.join(sorted(set(clash)))
    return ns('no other recorded check run overlaps this build\'s (%s); other processes (browsers, builds) are not recorded in files'
              % ', '.join('%s %s-%s' % (n, hm(w[0])[-8:], hm(w[1])[-8:]) for n, w in mine))


def faces_dir(b):
    return os.path.join(b.P, 'faces')


@row('B112', 'B204', 'C004')
def faces_changed(b):
    fd = faces_dir(b)
    pc = os.path.join(fd, 'pixel-check-after-answer.json')
    if not os.path.exists(pc):
        return 'FAULT', 'no pixel check after her last answer (%s)' % pc
    j = json.load(open(pc))
    n_final = len([x for x in os.listdir(os.path.join(fd, 'photos-final'))]) if os.path.isdir(os.path.join(fd, 'photos-final')) else -1
    f = []
    if not j.get('pass'):
        f.append('pixel check did not pass')
    if j.get('images') != n_final:
        f.append('pixel check names %s images, photos-final/ holds %d' % (j.get('images'), n_final))
    newest = max([mtime(os.path.join(fd, 'photos-final', x)) for x in os.listdir(os.path.join(fd, 'photos-final'))] or [0])
    if newest > mtime(b.zip):
        f.append('a final image is newer than the zip')
    if mtime(pc) < newest:
        f.append('pixel check older than the newest final image')
    for k in ('checks/full.txt', 'checks2/images.txt', 'checks2/images-2.txt'):
        p = os.path.join(b.B, k)
        if not os.path.exists(p):
            f.append('image result %s missing' % k)
        elif mtime(p) < mtime(b.zip):
            f.append('%s older than the images in the zip' % k)
    m = re.search(r'from blurred working copies', b.logtext)
    d = 'pixel check %s: pass %s, %s images; photos-final %d files; build log %s' % (os.path.basename(pc), j.get('pass'), j.get('images'), n_final,
                                                                                    'uses blurred working copies' if m else 'names no blurred copies')
    return ('FAULT', d + ' | ' + '; '.join(f)) if f else ('PASS', d)


@row('E021')
def faces_final(b):
    fd = faces_dir(b)
    r2 = os.path.join(fd, 'review2.json')
    pc = os.path.join(fd, 'pixel-check-after-answer.json')
    f = [p for p in (r2, pc) if not os.path.exists(p)]
    if f:
        return 'FAULT', 'missing: ' + ', '.join(f)
    r = json.load(open(r2))
    if 'final' not in r:
        return 'FAULT', '%s has no "final" answer' % r2
    return 'PASS', 'review2.json "final" and pixel-check-after-answer.json present (the faces look itself is eye)'


@row('E022')
def blur_method(b):
    m = re.search(r'method (v\d+)', b.logtext)
    fp = fingerprints()
    bad, n = [], 0
    for p in sorted(glob.glob(TOOLS + '/blur/*.py')):
        n += 1
        s = sha256(p)
        if s not in fp.get(os.path.normpath(p), set()):
            bad.append(os.path.basename(p))
    if not m:
        return 'FAULT', 'the build log names no blur method'
    if bad:
        return 'FAULT', 'build log: method %s; blur scripts not matching FINGERPRINTS.txt: %s' % (m.group(1), ', '.join(bad))
    return 'PASS', 'build log: method %s; %d blur scripts match FINGERPRINTS.txt' % (m.group(1), n)


@row('B149')
def build_cmd(b):
    c = glob.glob(os.path.join(b.P, '*.build.sh')) + glob.glob(os.path.join(b.P, 'build-command*')) + \
        glob.glob(os.path.join(MM, 'pages', (b.slug or '?') + '.build.sh'))
    if not c:
        return 'FAULT', 'no build command file: looked for %s/*.build.sh, %s/build-command*, %s/pages/%s.build.sh' % (b.P, b.P, MM, b.slug)
    return 'PASS', ', '.join(c)


@row('B151')
def changes(b):
    c = [p for p in (b.zip + '.changes.txt', os.path.join(b.B, 'changes.txt')) if os.path.exists(p) and os.path.getsize(p)]
    if not c:
        return 'FAULT', 'no change list for this build (%s.changes.txt or %s/changes.txt)' % (b.zip, b.B)
    return 'PASS', c[0]


@row('B203', 'C002', 'E023')
def preview_no_zip(b):
    prev = re.search(r'faces-preview|NO UPLOAD ZIP|round 1 blurred', b.logtext)
    if prev:
        ups = [p for p in glob.glob(os.path.join(b.B, '*.zip')) if '-originals' not in p and 'CHECK-ONLY' not in p]
        if ups:
            return 'FAULT', 'faces-preview build has an upload zip: %s' % ups
        return 'PASS', 'faces-preview build, no upload zip'
    return 'PASS', 'not a faces-preview build (build log: her last faces answer used), so an upload zip is allowed'


@row('B253', 'D024')
def fingerprinted(b):
    fp = fingerprints()
    ok, bad = [], []
    for p, k in scripts_used(b):
        if not p or not os.path.exists(p):
            bad.append('%s: script for %s not found' % (p, k))
            continue
        s = sha256(p)
        (ok if s in fp.get(os.path.normpath(p), set()) else bad).append('%s %s' % (os.path.relpath(p, '/home/claude'), s[:8]))
    if b.full_vc_sha and not b.cfix:
        bad.append('full.txt names visual_check.py %s, found in no check folder' % b.full_vc_sha[:8])
    if not ok and not bad:
        return 'FAULT', 'no check result, so no script to look up'
    d = '%d scripts match FINGERPRINTS.txt' % len(ok)
    return ('FAULT', d + '; not listed with this sha: ' + ', '.join(bad)) if bad else ('PASS', d + ': ' + ', '.join(ok))


@row('C113')
def quoted(b):
    rows = json.load(open(TOOLS + '/REQUIRED-CHECKS.json'))
    bad = [r['id'] for r in rows if not (r.get('quote') or '').strip() or not (r.get('source') or '').strip()]
    af = [l for l in (read(TOOLS + '/ALLOWED-FAULTS.txt') or '').splitlines() if re.match(r'^AF\d+', l)]
    afbad = [l.split('|')[0].strip() for l in af if 'word for word' not in l]
    if bad or afbad:
        return 'FAULT', 'rows with no quote or source: %s; allowances with no quoted agreement: %s' % (bad[:40], afbad)
    return 'PASS', '%d rows each with a quote and a source; %d allowances each quoting her agreement' % (len(rows), len(af))


@row('C115')
def list_agreed(b):
    f = []
    a, w = sha256(TOOLS + '/REQUIRED-CHECKS.json'), REPO + '/workspace/tools/REQUIRED-CHECKS.json'
    if not os.path.exists(w) or sha256(w) != a:
        f.append('tools/REQUIRED-CHECKS.json differs from the committed copy in the templates clone')
    w2 = REPO + '/workspace/tools/ALLOWED-FAULTS.txt'
    if not os.path.exists(w2) or sha256(w2) != sha256(TOOLS + '/ALLOWED-FAULTS.txt'):
        f.append('tools/ALLOWED-FAULTS.txt differs from the committed copy')
    try:
        o = subprocess.run(['git', '-C', REPO, 'log', '--format=%h|%s', '--', 'workspace/tools/REQUIRED-CHECKS.json',
                            'workspace/tools/REQUIRED-CHECKS.txt'], capture_output=True, text=True, timeout=60).stdout
        for l in o.splitlines():
            h, s = l.split('|', 1)
            if not re.search(r"owner'?s? .*agreement|owner \d+ \w+ \d\d:\d\d", s):
                f.append('list commit %s cites no agreement: %s' % (h, s[:100]))
    except Exception as e:
        f.append('git log failed: %s' % e)
    second = any(re.search(r'LIST AGREEMENT \(second of two\)', read(p) or '') for p in glob.glob(MM + '/records/DECISIONS-LOG*.md'))
    if not second:
        f.append('no second (list) agreement in records/DECISIONS-LOG*.md')
    if f:
        return 'FAULT', '; '.join(f)
    return 'PASS', 'list and allowances equal the committed copies; every list commit cites her agreement; second agreement (list) recorded'


@row('D014', 'D040')
def names_sha(b):
    f, carried, none = [], [], []
    zips = [p for p in glob.glob(os.path.join(b.B, '*.zip')) if '-originals' not in p]
    shas = {p: sha256(p) for p in zips}
    # 6 Nov 2026 (gatefix2 C5): one package = one sha256; a copy byte for byte the same as the zip is the same package (named)
    if len(set(shas.values())) != 1:
        f.append('%d different package zips in the build folder (%s), not one' % (len(set(shas.values())), ', '.join('%s %s' % (os.path.basename(p), s[:8]) for p, s in shas.items())))
    elif len(zips) > 1:
        carried.append('copies byte for byte the same as the zip: ' + ', '.join(os.path.basename(p) for p in zips if p != b.zip))
    for k in b.results_present():
        r = RESULTS[k]
        t = read(os.path.join(b.B, k)) or ''
        if r['sha'] == 'full':
            m = re.search(r'package sha256: ([0-9a-f]{64})', t)
            if not m or m.group(1) != b.sha:
                f.append('%s names %s, not this zip %s' % (k, m.group(1)[:16] if m else 'no sha', b.sha[:16]))
            else:
                carried.append(k)
        elif r['sha'] == 'summary16':
            s = read(os.path.join(b.B, k.split('/')[0], 'SUMMARY.txt')) or ''   # gatefix2: the run's folder (checks2/text/... -> checks2)
            m = re.search(r'package sha256 ([0-9a-f]{16})', s)
            if not m or m.group(1) != b.sha[:16]:
                f.append('%s: its run\'s SUMMARY.txt names %s, not %s' % (k, m.group(1) if m else 'no sha', b.sha[:16]))
            else:
                carried.append(k + ' (16 characters, in SUMMARY.txt)')
        else:
            if b.sha not in t and b.sha[:16] not in t:
                none.append(k)
    if none:
        f.append('results that do not name the zip\'s sha256: ' + ', '.join(none))
    d = 'zip %s %s; named in: %s' % (os.path.basename(b.zip), b.sha[:16], ', '.join(carried) or 'none')
    return ('FAULT', d + ' | ' + '; '.join(f)) if f else ('PASS', d)


@row('D020')
def self_compare(b):
    return ns('running every new check on all live pages (a page against itself shows nothing changed) needs a browser run on the live pages; no record of such a run is kept in files')


@row('D021')
def no_truncation(b):
    f = []
    for p in [TOOLS + '/run_checks.sh', TOOLS + '/more_checks.sh', TOOLS + '/v8/send_gate.sh', TOOLS + '/v8/send_gate_nolive.sh',
              TOOLS + '/gate.py']:
        for i, l in enumerate((read(p) or '').splitlines(), 1):
            if l.lstrip().startswith('#'):
                continue
            hit = re.search(r'\|\s*cut -c\s*\d|\bhead -c\s*\d|\[:\d{2,4}\]\s*\)?\s*$', l) and \
                not re.search(r'sha256sum[^|]*\|\s*cut -c\s*1-(8|16)\b', l)
            # 6 Nov 2026 (gatefix2 C8): any list or text slice ([:N], [-N:]) in a Python gate, anywhere on the line, unless it
            # slices a sha256 (an id, not output)
            sl = [m for m in re.finditer(r'\[(:\d+|-\d+:)\]', l) if 'sha' not in l[max(0, m.start() - 25):m.start()]]
            if hit or (p.endswith('.py') and sl):
                g = re.search(r'(cut -c\s*[\d-]+|head -c\s*\d+|\[:\d+\]|\[-\d+:\])', l)
                f.append('%s line %d: %s' % (os.path.relpath(p, MM), i, g.group(1) if g else sl[0].group(0)))
    if f:
        return 'FAULT', 'output cut short in: ' + '; '.join(f)
    return 'PASS', 'no cut -c / head -c in the runners and gates'


def inputs_changed(b):
    f = []
    for k in b.results_present():
        res = os.path.join(b.B, k)
        w = b.run_window(os.path.dirname(k)) if os.path.dirname(k) else None
        start = w[0] if w else None
        p = b.script(k)
        if p and os.path.exists(p) and mtime(p) > mtime(res):
            f.append('%s changed (%s) after %s was written (%s)' % (os.path.relpath(p, '/home/claude'), hm(mtime(p)), k, hm(mtime(res))))
        elif p and start and os.path.exists(p) and mtime(p) > start:
            f.append('%s changed during the run of %s' % (os.path.relpath(p, '/home/claude'), k))
        if start and mtime(b.zip) > start:
            f.append('zip changed after the run of %s started' % k)
        src = RESULTS[k]['source']
        if start and src == 'preview' and mtime(os.path.join(b.B, 'preview/index.html')) > start:
            f.append('preview/index.html changed during the run of %s' % k)
    return f


@row('D023', 'D071')
def unchanged(b):
    if not b.results_present():
        return 'FAULT', 'no check result in the build folder'
    f = inputs_changed(b)
    if f:
        return 'FAULT', '; '.join(f)
    return 'PASS', 'zip, preview and every check script unchanged since each run started (file times)'


def complete(b, k):
    t = read(os.path.join(b.B, k)) or ''
    ls = [l for l in t.splitlines() if l.strip()]
    if not ls:
        return False
    rx = RESULTS[k]['complete']
    tail = ls[-3:]
    return any(re.search(rx, l) for l in tail)


@row('D035', 'D036')
def finished(b):
    pres = b.results_present()
    if not pres:
        return 'FAULT', 'no check result in the build folder'
    part = [k for k in pres if not complete(b, k)]
    runs = []
    for f in glob.glob(os.path.join(b.B, 'checks*', 'SUMMARY.txt')):
        w = window_of(f, read(f))
        if w and not w[2]:
            runs.append(os.path.relpath(f, b.B))
    if part or runs:
        return 'FAULT', 'part-written results: %s; runs with no end line: %s' % (', '.join(part) or 'none', ', '.join(runs) or 'none')
    return 'PASS', '%d results each end with their final line; every run has its end line' % len(pres)


@row('D041')
def upload_list(b):
    return ns('the upload list is written at the moment of sending, after the gate')


@row('D073')
def template_committed(b):
    try:
        st = subprocess.run(['git', '-C', REPO, 'status', '--porcelain', '--', 'Essay Code Template.html', 'Resources Code Template.html'],
                            capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return 'FAULT', 'git status failed: %s' % e
    if st:
        return 'FAULT', 'template not committed: ' + st
    return 'PASS', 'templates committed in %s (no uncommitted change)' % REPO


@row('D055', 'D306')
def template_commit(b):
    try:
        st = subprocess.run(['git', '-C', REPO, 'status', '--porcelain', '--', 'Essay Code Template.html', 'Resources Code Template.html'],
                            capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return 'FAULT', 'git status failed: %s' % e
    first, cs = template_commits(b)
    f = []
    if st:
        f.append('template not committed: ' + st)
    if cs and len(cs) > 1:
        f.append('%d template commits during this page (one per page): %s' % (len(cs), ', '.join(h for h, _, _ in cs)))
    if f:
        return 'FAULT', '; '.join(f)
    return 'PASS', 'template committed; %d template commit(s) during this page' % len(cs or [])


@row('D087')
def only_index(b):
    if b.nolive:
        return 'PASS', 'page has no live version: the whole folder is new, so the zip holds every file'
    return ns('whether only index.html changed needs the live copy; run with --nolive for a page with no live version')


def code_only(p):
    """6 Nov 2026 (gatefix2 C9): the script's text without comments ('#' lines and the part of a line after ' #' or '//')
    and, for Python, without module/class/function docstrings - a page named in a note is not a page written into the code"""
    t = read(p) or ''
    skip = set()
    if p.endswith('.py'):
        import ast
        try:
            for n in ast.walk(ast.parse(t)):
                if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body and \
                        isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], 'value', None), ast.Constant) and \
                        isinstance(n.body[0].value.value, str):
                    skip.update(range(n.body[0].lineno, n.body[0].end_lineno + 1))
        except SyntaxError:
            pass
    out = []
    for i, l in enumerate(t.splitlines(), 1):
        if i in skip or l.lstrip().startswith('#'):
            continue
        l = re.split(r'\s#\s|//', l)[0]
        out.append(l)
    return '\n'.join(out)


@row('D090')
def no_page_name(b):
    f = []
    words = set()
    if b.slug:
        words.add(b.slug)
        words.add(b.slug.replace('-', ' ').title().replace('The ', 'The '))
    used = scripts_used(b) + [(p, 'runner') for p in RUNNER_FILES.values()]
    for p, k in used:
        if not p or not os.path.exists(p):
            continue
        t = code_only(p)   # 6 Nov 2026 (gatefix2 C9): comments and docstrings left out
        for w in words:
            if w and w.lower() in t.lower():
                f.append('%s names "%s"' % (os.path.relpath(p, MM), w))
    if f:
        return 'FAULT', 'page name written into: ' + '; '.join(sorted(set(f)))
    return 'PASS', 'no check script or runner used names the page'


@row('D100')
def edit_queue(b):
    c = [p for p in (os.path.join(MM, 'queues', '%s-EDIT-QUEUE.md' % b.slug), os.path.join(b.P, 'EDIT-QUEUE.md')) if os.path.exists(p)]
    if not c:
        return 'FAULT', 'no EDIT-QUEUE.md for the page (%s/queues/%s-EDIT-QUEUE.md or %s/EDIT-QUEUE.md)' % (MM, b.slug, b.P)
    return 'PASS', c[0] + ' (whether every edit of hers is in it is eye)'


@row('D297')
def line_by_line(b):
    return ns('whether a script writes each line as it is measured is in its code, not its output (lesson 17: "tried, not shown to work")')


@row('D298')
def version7(b):
    left = [d for d in glob.glob(os.path.join(b.B, 'checks*', '*')) if os.path.isdir(d) and not d.endswith('/text')]
    return ns('no version number is recorded in the scripts or results%s' % (
        '; unpacked/working folders left in the results: ' + ', '.join(os.path.relpath(d, b.B) for d in left) if left else ''))


@row('D310')
def old_builds(b):
    kept = set()
    for p in glob.glob('/home/claude/eng35/checks-plan/**/*', recursive=True) + [MM + '/records/ENFORCEMENT-PLAN-5-nov.md', TOOLS + '/check-proofs.json']:
        if os.path.isfile(p) and os.path.getsize(p) < 5_000_000:
            for m in re.finditer(r'(?:%s/|\bbuild )(b?\d+)\b' % re.escape(os.path.basename(b.P)), read(p) or ''):
                kept.add('b' + m.group(1).lstrip('b'))
    builds = sorted([os.path.basename(d) for d in glob.glob(os.path.join(b.P, 'b*')) if os.path.isdir(d) and re.match(r'^b\d+$', os.path.basename(d))],
                    key=lambda x: int(x[1:]))
    me = int(b.name[1:]) if re.match(r'^b\d+$', b.name) else None
    older = [x for x in builds if me is not None and int(x[1:]) < me and x not in kept]
    newer = [x for x in builds if me is not None and int(x[1:]) > me]
    d = 'kept for proofs: %s; newer builds: %s' % (', '.join(sorted(kept & set(builds), key=lambda x: int(x[1:]))) or 'none', ', '.join(newer) or 'none')
    if older:
        return 'FAULT', 'superseded test builds left in %s: %s | %s' % (b.P, ', '.join(older), d)
    return 'PASS', 'no superseded build left | ' + d


@row('D314')
def watched(b):
    return ns('watch.sh runs as a process beside each agent and keeps no record file')


@row('D316')
def no_dupes(b):
    f = []
    for k in RESULTS:
        base = os.path.basename(k)
        found = [os.path.relpath(p, b.B) for p in glob.glob(os.path.join(b.B, '**', base), recursive=True)
                 if not re.search(r'/(hostinger|preview|images|work)/', p)]
        if len(found) > 1:
            f.append('%s: %s' % (base, ', '.join(found)))
    dirs = [os.path.basename(d) for d in glob.glob(os.path.join(b.B, 'checks*')) if os.path.isdir(d)]
    if f:
        return 'FAULT', 'the same check\'s result more than once: ' + '; '.join(f)
    return 'PASS', 'one result per check (folders: %s)' % ', '.join(sorted(dirs))


@row('D317')
def real_case(b):
    return ns('whether a planted fault is one this page can really have is a judgement on each proof')


@row('E008')
def fresh_clone(b):
    f, n = [], 0
    for base in (REPO + '/workspace', MM):
        fp = os.path.join(base, 'FINGERPRINTS.txt')
        if not os.path.exists(fp):
            f.append('no %s' % fp)
            continue
        r = subprocess.run(['sha256sum', '-c', '--quiet', 'FINGERPRINTS.txt'], cwd=base, capture_output=True, text=True)
        bad = [l for l in (r.stdout + r.stderr).splitlines() if l.strip() and 'WARNING' not in l]
        n += len((read(fp) or '').splitlines())
        if bad:
            f.append('%s: %d entries fail sha256sum -c: %s' % (base, len(bad), '; '.join(bad)))
    try:
        sh = subprocess.run(['git', '-C', REPO, 'rev-parse', '--is-shallow-repository'], capture_output=True, text=True).stdout.strip()
        st = subprocess.run(['git', '-C', REPO, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip()
    except Exception:
        sh, st = '?', '?'
    if st:
        f.append('templates clone has uncommitted changes: %d files' % len(st.splitlines()))
    if f:
        return 'FAULT', '; '.join(f)
    return 'PASS', 'sha256sum -c OK on %d entries (the session\'s clone, not a fresh one: %s)' % (n, 'shallow' if sh == 'true' else 'full')


@row('E018')
def zip_complete(b):
    if not b.zip:
        return 'FAULT', 'no zip'
    with zipfile.ZipFile(b.zip) as zf:
        html = zf.read(b.slug + '/index.html').decode('utf-8', 'replace')
        names = set(zf.namelist())
    refs = set(re.findall(r'''(?:src|href|data-full|data-src)=["'](images/[^"'#?]+)''', html))
    miss = sorted(r for r in refs if b.slug + '/' + r not in names)
    if miss:
        return 'FAULT', '%d files the page uses are missing from the zip: %s' % (len(miss), ', '.join(miss))
    return 'PASS', '0 missing files (%d image files referenced, %d files in the zip)' % (len(refs), len(names))


@row('E019')
def protection(b):
    with zipfile.ZipFile(b.zip) as zf:
        html = zf.read(b.slug + '/index.html').decode('utf-8', 'replace')
    a, c = html.count('id="mm-protect"'), html.count('id="mm-protect-js"')
    if (a, c) != (1, 1):
        return 'FAULT', 'copy protection in the upload zip: mm-protect %d, mm-protect-js %d (each must be 1)' % (a, c)
    return 'PASS', 'copy protection present once in the upload zip'


@row('C025')
def reads_zip(b):
    pres = b.results_present()
    if not pres:
        return 'FAULT', 'no check result in the build folder'
    copy = [k for k in pres if RESULTS[k]['source'] == 'preview']
    chk = [k for k in pres if 'CHECK-ONLY' in RESULTS[k]['source']]
    f = []
    # 6 Nov 2026 (gatefix2 C6): the browser checks read a copy unpacked from the upload zip; the run's SUMMARY.txt must say so
    for k in pres:
        if RESULTS[k]['source'] == 'zip (unpacked)':
            s = read(os.path.join(b.B, k.split('/')[0], 'SUMMARY.txt')) or ''
            if not re.search(r'unpacked from \S*%s\.zip sha256 %s' % (re.escape(b.slug or '?'), b.sha[:16]), s):
                f.append('%s: its run\'s SUMMARY.txt does not say it read a copy unpacked from %s.zip sha256 %s' % (k, b.slug, b.sha[:16]))
    if copy:
        f.append('read preview/index.html (the page without copy protection), not the upload zip: ' + ', '.join(copy))
    for k in chk:
        c = glob.glob(os.path.join(b.B, '*CHECK-ONLY.zip'))
        if not c or sha256(c[0]) != b.sha:
            f.append('%s read a CHECK-ONLY zip that is not byte for byte the upload zip' % k)
    if f:
        return 'FAULT', '; '.join(f)
    return 'PASS', 'every result read the upload zip, a byte-identical copy, or a copy unpacked from the upload zip (named in its run\'s SUMMARY.txt)'


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        print('GATE-FILES FAULT (1)')
        print('END')
        sys.exit(2)
    nolive = '--nolive' in a
    gp = None
    if '--gate-proofs' in a:
        gp = a[a.index('--gate-proofs') + 1]
    b = Build(a[0], nolive, gp)
    out = open(a[1], 'w')

    def say(s):
        print(s, flush=True)
        out.write(s + '\n')
        out.flush()
    say('gate_files.py sha256 %s  build %s  zip %s  sha256 %s  at %s' % (sha256(os.path.abspath(__file__)), b.B, b.zip, b.sha,
                                                                     datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')))
    if not b.zip:
        say('NO ZIP FAULT no package zip found in %s' % b.B)
        say('GATE-FILES FAULT (1)')
        say('END')
        sys.exit(1)
    nf = 0
    for ids, fn in ROWS:
        try:
            o, d = fn(b)
        except Exception as e:
            o, d = 'FAULT', 'the check itself failed: %r' % e
        for i in ids:
            say('%s %s %s' % (i, o, d))
            nf += o == 'FAULT'
    say('GATE-FILES PASS' if nf == 0 else 'GATE-FILES FAULT (%d)' % nf)
    say('END')
    out.close()
    sys.exit(0 if nf == 0 else 1)


if __name__ == '__main__':
    main()
