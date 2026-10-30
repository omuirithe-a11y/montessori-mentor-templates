import type { Register } from 'claude-code'

// Montessori Mentor gate (21 Oct 2026, the user chose "1": the build tools and a mod enforce the speed-ups).
//  1. A site page is published only when tools/gate.py made a PASS gate.json for that exact file.
//  2. The gate's results, the proofs and the gate itself cannot be edited, unless the user's latest message says "unlock gate".
//  3. The turn cannot end while QUEUE.md has open work, or while a gate failure is neither fixed nor put to the user.
//  4. No blocking question (AskUserQuestion) while QUEUE.md has open work: ask in a message and keep working.

const MM = '/home/claude/mm'
const QUEUE = `${MM}/QUEUE.md`
const PROTECTED = /(gate\.json|check-proofs\.json|tools\/gate\.py|tools\/prove_all\.py|dev-mods\/[^/]+\/mm-gate)/
const RUNS_GATE = /^\s*(cd \/home\/claude\/mm[^;&|]*(&&|;)\s*)?(\(?\s*time\s+)?python3 (\/home\/claude\/mm\/)?tools\/(gate|prove_all)\.py\b/

const sh = async ($: any, cmd: string) => {
  const r = await $.process.run(['bash', '-c', cmd])
  return String(r.stdout ?? '')
}

const unlocked = async ($: any) => /\bunlock gate\b/i.test(String((await $.store.get('lastUserPrompt')) ?? ''))

// open items: "- [ ] ..." lines; "- [x]" is done; "- [waiting: ...]" waits for the user
const openItems = async ($: any): Promise<string[]> => {
  const q = await sh($, `cat ${QUEUE} 2>/dev/null`)
  return q.split('\n').filter(l => /^\s*- \[ \]/.test(l)).map(l => l.replace(/^\s*- \[ \]\s*/, ''))
}
const waitingText = async ($: any) =>
  (await sh($, `cat ${QUEUE} 2>/dev/null`)).split('\n').filter(l => /^\s*- \[waiting/i.test(l)).join('\n')

// gate.json files whose checks failed (a fault, not only a missing proof)
const failedGates = async ($: any) => {
  const out = await sh($, `for f in ${MM}/build*/*/gate.json; do [ -f "$f" ] && python3 -c "import json,sys;g=json.load(open(sys.argv[1]));b=[k for k,v in g['checks'].items() if not v['ok']];print(g['page']+'|'+','.join(b)) if b else None" "$f"; done`)
  return out.split('\n').filter(Boolean).map(l => { const [page, checks] = l.split('|'); return { page, checks } })
}

export const register: Register = on => {
  on('prompt.submit', async ($, e, next) => {
    const kind = (e as any).origin?.kind
    if (kind === 'composer' || kind === 'bridge' || kind === 'sdk') await $.store.set('lastUserPrompt', e.text)
    return next(e)
  })

  // 1. publishing a site page
  on('tool.call', { tool: 'Artifact' }, async ($, e: any, next) => {
    const action = e.action ?? 'publish'
    if (action !== 'publish' || e.asset || !e.file_path) return next(e)
    const path: string = e.file_path.startsWith('/') ? e.file_path : `${MM}/${e.file_path}`
    const html = await sh($, `head -c 400000 ${JSON.stringify(path)} 2>/dev/null`)
    const isSitePage = path.startsWith(MM + '/') || /<div class="hero"/.test(html) || /Montessori Mentor<\/title>/.test(html)
    if (!isSitePage) return next(e)
    if (e.edits) return { deny: 'mm-gate: a site page cannot be published with edits; change the settings or tools, rebuild with tools/gate.py, then publish.' }
    const found = (await sh($, `d=$(dirname ${JSON.stringify(path)}); for i in 1 2 3; do [ -f "$d/gate.json" ] && { echo "$d/gate.json"; break; }; d=$(dirname "$d"); done`)).trim()
    if (!found) return { deny: `mm-gate: no gate.json for ${path}. Run: python3 tools/gate.py <page number>` }
    const fileSha = (await sh($, `sha256sum ${JSON.stringify(path)} | cut -c1-64`)).trim()
    const g = JSON.parse(await sh($, `cat ${JSON.stringify(found)}`))
    if (g.sha256 !== fileSha) return { deny: `mm-gate: ${path} is not the file the gate checked (gate ${String(g.sha256).slice(0, 12)}, file ${fileSha.slice(0, 12)}). Rebuild with tools/gate.py.` }
    if (!g.pass) {
      const bad = Object.entries(g.checks).filter(([, v]: any) => !v.ok).map(([k]) => k)
      return { deny: `mm-gate: the gate FAILED for ${g.page}: failing ${bad.join(', ') || 'none'}; unproved ${(g.unproved_checks || []).join(', ') || 'none'}. Fix, or prove the checks (tools/prove_all.py), then rerun the gate.` }
    }
    return next(e)
  })

  // 2. the gate's own files
  on('tool.call', { tool: 'Write' }, async ($, e: any, next) =>
    PROTECTED.test(e.file_path ?? '') && !(await unlocked($)) ? { deny: 'mm-gate: the gate, its results and proofs are locked. The user must say "unlock gate".' } : next(e))
  on('tool.call', { tool: 'Edit' }, async ($, e: any, next) =>
    PROTECTED.test(e.file_path ?? '') && !(await unlocked($)) ? { deny: 'mm-gate: the gate, its results and proofs are locked. The user must say "unlock gate".' } : next(e))
  on('tool.call', { tool: 'Bash' }, async ($, e: any, next) => {
    const c = String(e.command ?? '')
    if (PROTECTED.test(c) && !RUNS_GATE.test(c) && !(await unlocked($)))
      return { deny: 'mm-gate: commands that touch the gate, its results or proofs are locked (only running tools/gate.py or tools/prove_all.py is allowed). The user must say "unlock gate".' }
    return next(e)
  })

  // 4. no blocking question while work is open
  on('tool.call', { tool: 'AskUserQuestion' }, async ($, e, next) => {
    const open = await openItems($)
    return open.length
      ? { deny: `mm-gate: QUEUE.md has open work (${open[0]}). Ask with SendUserMessage instead, add a "- [waiting: ...]" line, and keep working.` }
      : next(e)
  })

  // 3. ending the turn
  on('classic.Stop', async ($, e: any, next) => {
    const r = await next(e)
    const open = await openItems($)
    const running = (e.background_tasks ?? []).length
    if (open.length)
      return { ...r, block: `mm-gate: QUEUE.md has open work${running ? ' while a background check runs' : ''}: "${open[0]}". Do it now, or mark it "- [waiting: <what the user must decide>]" if it needs the user.` }
    const waiting = await waitingText($)
    const unreported = (await failedGates($)).filter(f => !waiting.includes(f.page))
    if (unreported.length)
      return { ...r, block: `mm-gate: the gate shows faults on ${unreported.map(f => `${f.page} (${f.checks})`).join('; ')}. Fix them, or ask the user now and add a "- [waiting: ${unreported[0].page} ...]" line to QUEUE.md.` }
    return r
  })
}
