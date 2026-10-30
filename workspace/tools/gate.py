#!/usr/bin/env python3
"""The gate (21 Oct 2026, the user chose "1": the build tools and a mod enforce the speed-ups).

  python3 tools/gate.py 5.4                 build the page, run every check at once, write <out>/gate.json
  python3 tools/gate.py prove <check> 5.4 <broken-preview-folder>
                                            record that <check> catches a fault: it must FAIL on the broken copy
                                            and PASS on the real build

gate.json says PASS only when, for the page file just built:
  - every check passes (fault_checks.py and check_page.py, run at the same time);
  - every check that looked at anything on this page has a proof recorded for its current code
    (a check whose code changed since its proof needs a new proof);
  - every setting in the page's settings file names its source in a comment (user, Word, PDF, template, live, site rule).
The mod (the "gate" plugin) refuses to publish a page file unless gate.json is PASS and was made for that exact file.
"""
import sys, os, re, ast, json, hashlib, subprocess, datetime, concurrent.futures as cf

MM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = '/home/claude/admin/src'; FACES = '/home/claude/admin/faces'
PROOFS = os.path.join(MM, 'tools', 'check-proofs.json')
COMMON = ['--template', 'resources', '--no-toc', '--hero', 'heroes/administration.jpg', '--section-href', '/administration/']
# 21 Oct 12:4x (user, the 5.3 chat): 5.3 is built on the Essay Code Template (its table of contents is its own setting,
# NO_TOC), and its page check uses the Essay template's figures, not the Resources template's (no --resources)
ESSAY = ['--template', 'essay', '--hero', 'heroes/administration.jpg', '--section-href', '/administration/']
# the same pages and arguments as build_admin.sh; 5.4 builds into build-next (its preview artifact is published from there)
PAGES = {
    '5.1': dict(docx='5.1.docx', pdf='5.1.pdf', title='Staff', folder='staff', menu='Staff', out='build/staff',
                photos='build/staff/faces/photos'),
    '5.2': dict(docx='5.2.docx', pdf='5.2.pdf', title='School Handbook', folder='school-handbook', menu='School Handbook',
                out='build/school-handbook'),
    '5.3': dict(docx='5.3.docx', pdf='5.3.pdf', title='Classroom Management', folder='classroom-management',
                menu='Classroom Management', out='build/classroom-management', photos=FACES + '/5.3/photos',
                common=ESSAY, page_args=[]),
    '5.4': dict(docx='5.4-work.docx', pdf='5.4.pdf', title='Beginning of the Year - Teachers',
                folder='beginning-of-the-year-for-teachers', menu='Beginning of the year for Teachers',
                out='build-next/beginning-of-the-year-for-teachers', photos=FACES + '/5.4/photos', build_pdf=True),
    '5.5': dict(docx='5.5.docx', pdf='5.5.pdf', title='Observations for Teachers', folder='observations-for-teachers',
                menu='Observations for Teachers', out='build/observations-for-teachers'),
}
SOURCE_WORDS = re.compile(r'\b(user|your|you|Word|PDF|template|live|site rule)\b', re.I)
EXEMPT = {'CSS'}

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def settings_path(p): return os.path.join(MM, 'pages', p['folder'] + '.py')

def phone_gaps(p):
    ns = {}
    try: exec(compile(open(settings_path(p)).read(), settings_path(p), 'exec'), {'__file__': settings_path(p)}, ns)
    except Exception: return None
    return ns.get('PHONE_GAPS')

def build(num):
    p = PAGES[num]
    cmd = ['python3', 'tools/build_page.py'] + p.get('common', COMMON) + ['--docx', os.path.join(SRC, p['docx']), '--title', p['title'],
           '--folder', p['folder'], '--menu', p['menu'], '--settings', settings_path(p), '--out', p['out']]
    if p.get('build_pdf'): cmd += ['--pdf', os.path.join(SRC, p['pdf'])]
    if p.get('photos'): cmd += ['--photos', p['photos']]
    r = subprocess.run(cmd, cwd=MM, capture_output=True, text=True, timeout=900)
    if r.returncode != 0: sys.exit('build failed:\n' + (r.stdout + r.stderr)[-3000:])
    return r.stdout

def run_fault_checks(num, preview):
    p = PAGES[num]
    r = subprocess.run(['python3', 'tools/fault_checks.py', os.path.join(SRC, p['docx']), os.path.join(SRC, p['pdf']), preview,
                        settings_path(p)], cwd=MM, capture_output=True, text=True, timeout=1500)
    res = {}
    for line in r.stdout.splitlines():
        m = re.match(r'^([A-Z]\d?) (.*?) (PASS|FAIL) \((\d+) checked\)', line)
        if m: res[m.group(1)] = {'name': m.group(1) + ' ' + m.group(2), 'ok': m.group(3) == 'PASS', 'checked': int(m.group(4)), 'faults': []}
        elif line.startswith('     - ') and res: list(res.values())[-1]['faults'].append(line[7:])
    if not res: res['fault_checks'] = {'name': 'fault_checks.py did not run', 'ok': False, 'checked': 0, 'faults': [(r.stdout + r.stderr)[-1500:]]}
    return res

def run_check_page(num, preview):
    pg = phone_gaps(PAGES[num])
    cmd = ['python3', 'tools/check_page.py', preview] + PAGES[num].get('page_args', ['--resources']) + (['--phone-gaps=%s,%s' % tuple(pg)] if pg else [])
    r = subprocess.run(cmd, cwd=MM, capture_output=True, text=True, timeout=900)
    faults = []; widths = 0
    for line in r.stdout.splitlines():
        if re.match(r'^\d+  errors:', line):
            widths += 1
            if 'errors:none' not in line: faults.append(line[:200])
            elif 'sideways:True' in line: faults.append(line.split('  ')[0] + ' scrolls sideways')
            elif '<<' in line: faults.append(re.sub(r'lines \[.*?\]', 'lines [...]', line))
            elif not re.search(r'not justified:0\b', line): faults.append(line.split('  ')[0] + ' has lines that are not justified')
            elif not line.rstrip().endswith('photos not loaded:0'): faults.append(line.split('  ')[0] + ' photos not loaded')
        elif 'menu panels' in line and 'FAULT' in line: faults.append(line.strip())
    if widths != 3: faults.append('check_page.py did not measure 3 widths: ' + (r.stdout + r.stderr)[-800:])
    return {'PAGE': {'name': 'PAGE check_page (errors, sideways, gaps, lines, footer, justified, photos, menu)',
                     'ok': not faults, 'checked': widths, 'faults': faults}}

def code_hashes():
    """The code each check runs: a fault_checks.py section (from its '# X ' heading to the next) and check_page.py whole."""
    out = {}; cur = None; buf = []
    for line in open(os.path.join(MM, 'tools', 'fault_checks.py')).read().splitlines():
        m = re.match(r'^# ([A-Z]\d?) ', line)
        if m and m.group(1) != cur:
            if cur: out[cur] = hashlib.sha256('\n'.join(buf).encode()).hexdigest()
            cur, buf = m.group(1), []
        if cur: buf.append(line)
    if cur: out[cur] = hashlib.sha256('\n'.join(buf).encode()).hexdigest()
    out['PAGE'] = sha(os.path.join(MM, 'tools', 'check_page.py'))
    return out

def settings_sources(num):
    path = settings_path(PAGES[num]); lines = open(path).read().splitlines(); faults = []
    for node in ast.parse('\n'.join(lines)).body:
        if not isinstance(node, ast.Assign): continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if not names or set(names) <= EXEMPT: continue
        own = ' '.join(lines[node.lineno - 1:node.end_lineno])
        above = lines[node.lineno - 2] if node.lineno >= 2 else ''
        has = ('#' in own and SOURCE_WORDS.search(own[own.index('#'):])) or (above.strip().startswith('#') and SOURCE_WORDS.search(above))
        if not has: faults.append('%s (line %d) names no source (user, Word, PDF, template, live)' % (names[0], node.lineno))
    return {'SET': {'name': 'SET every setting names its source', 'ok': not faults, 'checked': len(lines), 'faults': faults}}

def all_checks(num, preview):
    with cf.ThreadPoolExecutor(2) as ex:   # speed-up 4: both check tools at the same time
        a = ex.submit(run_fault_checks, num, preview); b = ex.submit(run_check_page, num, preview)
        res = a.result(); res.update(b.result())
    return res

def gate(num):
    p = PAGES[num]
    if not os.path.exists(os.path.join(SRC, p['docx'])): sys.exit('%s: the Word file %s is not in %s' % (num, p['docx'], SRC))
    t0 = datetime.datetime.now()
    build(num)
    preview = os.path.join(MM, p['out'], 'preview'); page = os.path.join(preview, 'index.html')
    res = all_checks(num, preview); res.update(settings_sources(num))
    proofs = json.load(open(PROOFS)) if os.path.exists(PROOFS) else {}
    hashes = code_hashes(); missing = []
    for k, v in res.items():
        if k == 'SET' or not v['checked']: continue
        pr = proofs.get(k)
        if not pr or pr['code'] != hashes.get(k): missing.append(k)
    ok = all(v['ok'] for v in res.values()) and not missing
    g = {'page': num, 'file': page, 'sha256': sha(page), 'made': t0.isoformat(timespec='seconds'),
         'finished': datetime.datetime.now().isoformat(timespec='seconds'), 'pass': ok,
         'unproved_checks': missing, 'checks': res}
    json.dump(g, open(os.path.join(MM, p['out'], 'gate.json'), 'w'), indent=1, ensure_ascii=False)
    for k, v in res.items():
        print('%-4s %s %s (%d)%s' % (k, 'PASS' if v['ok'] else 'FAIL', v['name'], v['checked'],
                                     ''.join('\n       - ' + f for f in v['faults'][:20])))
    if missing: print('UNPROVED (no proof for the current code): ' + ', '.join(missing))
    print('\nGATE %s  %s  %s' % ('PASS' if ok else 'FAIL', page, g['sha256'][:12]))
    return ok

def prove(key, num, broken):
    p = PAGES[num]; preview = os.path.join(MM, p['out'], 'preview')
    real = all_checks(num, preview); bad = all_checks(num, os.path.abspath(broken))
    if key not in real or key not in bad: sys.exit('no check called %s ran on %s' % (key, num))
    if not real[key]['ok']: sys.exit('%s fails on the real build, so this proves nothing: %s' % (key, real[key]['faults'][:3]))
    if bad[key]['ok']: sys.exit('%s PASSED on the broken copy: the check does not catch this fault' % key)
    proofs = json.load(open(PROOFS)) if os.path.exists(PROOFS) else {}
    proofs[key] = {'code': code_hashes()[key], 'page': num, 'broken_copy': os.path.abspath(broken),
                   'caught': bad[key]['faults'][:3], 'at': datetime.datetime.now().isoformat(timespec='seconds')}
    json.dump(proofs, open(PROOFS, 'w'), indent=1, ensure_ascii=False)
    print('PROVED %s: passes on the build, fails on the broken copy with: %s' % (key, bad[key]['faults'][:2]))

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'prove': prove(a[1], a[2], a[3])
    elif a and a[0] in PAGES: sys.exit(0 if gate(a[0]) else 1)
    else: sys.exit(__doc__)
