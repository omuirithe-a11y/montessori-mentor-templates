# the gate's settings_sources() logic, unchanged, run on its own (the gate file itself is locked)
import re, ast, sys
SOURCE_WORDS = re.compile(r'\b(user|your|you|Word|PDF|template|live|site rule)\b', re.I)
EXEMPT = {'CSS'}
path = sys.argv[1]; lines = open(path).read().splitlines(); faults = []
for node in ast.parse('\n'.join(lines)).body:
    if not isinstance(node, ast.Assign): continue
    names = [t.id for t in node.targets if isinstance(t, ast.Name)]
    if not names or set(names) <= EXEMPT: continue
    own = ' '.join(lines[node.lineno - 1:node.end_lineno])
    above = lines[node.lineno - 2] if node.lineno >= 2 else ''
    has = ('#' in own and SOURCE_WORDS.search(own[own.index('#'):])) or (above.strip().startswith('#') and SOURCE_WORDS.search(above))
    if not has: faults.append('%s (line %d) names no source (user, Word, PDF, template, live)' % (names[0], node.lineno))
print('SET', 'PASS' if not faults else 'FAIL', faults)
