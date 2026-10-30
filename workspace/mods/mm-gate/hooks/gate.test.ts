import { expect, test } from 'claude-code/testing'

// Each process.run the mod makes is answered here from a small fake disk.
const fake = (files: Record<string, string>, sha: string) => (_: any, e: any) => {
  const cmd = String(e.argv?.[2] ?? '')
  if (cmd.startsWith('head -c')) return { value: { exitCode: 0, stdout: '<div class="hero">' } }
  if (cmd.startsWith('d=$(dirname')) return { value: { exitCode: 0, stdout: files.gatePath ? files.gatePath + '\n' : '' } }
  if (cmd.startsWith('sha256sum')) return { value: { exitCode: 0, stdout: sha + '\n' } }
  if (cmd.startsWith('cat /home/claude/mm/QUEUE.md')) return { value: { exitCode: 0, stdout: files.queue ?? '' } }
  if (cmd.startsWith('cat ')) return { value: { exitCode: 0, stdout: files.gate ?? '' } }
  if (cmd.startsWith('for f in')) return { value: { exitCode: 0, stdout: files.failed ?? '' } }
  return { value: { exitCode: 0, stdout: '' } }
}
const PAGE = '/home/claude/mm/build-next/x/preview/index.html'
const GOOD = JSON.stringify({ page: '5.4', sha256: 'a'.repeat(64), pass: true, checks: {}, unproved_checks: [] })

test('a page whose gate passed for this exact file is published', async ($, on) => {
  on('process.run', fake({ gatePath: '/home/claude/mm/build-next/x/gate.json', gate: GOOD }, 'a'.repeat(64)))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'Artifact', file_path: PAGE } as any)
  expect(r.deny).toBe(undefined)
})

test('a page changed after the gate is refused', async ($, on) => {
  on('process.run', fake({ gatePath: '/home/claude/mm/build-next/x/gate.json', gate: GOOD }, 'b'.repeat(64)))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'Artifact', file_path: PAGE } as any)
  expect(String(r.deny)).toMatch(/not the file the gate checked/)
})

test('a page with no gate is refused', async ($, on) => {
  on('process.run', fake({}, 'a'.repeat(64)))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'Artifact', file_path: PAGE } as any)
  expect(String(r.deny)).toMatch(/no gate.json/)
})

test('a failed gate is refused', async ($, on) => {
  const bad = JSON.stringify({ page: '5.4', sha256: 'a'.repeat(64), pass: false, checks: { F: { ok: false } }, unproved_checks: ['B'] })
  on('process.run', fake({ gatePath: '/g/gate.json', gate: bad }, 'a'.repeat(64)))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'Artifact', file_path: PAGE } as any)
  expect(String(r.deny)).toMatch(/FAILED for 5.4: failing F; unproved B/)
})

test('editing the gate results is refused', async ($, on) => {
  on('store.get', () => ({ value: undefined }))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'Edit', file_path: '/home/claude/mm/build-next/x/gate.json', old_string: 'a', new_string: 'b' } as any)
  expect(String(r.deny)).toMatch(/locked/)
  const b = await $.tool.call({ tool: 'Bash', command: 'echo {} > /home/claude/mm/build-next/x/gate.json' } as any)
  expect(String(b.deny)).toMatch(/locked/)
  const ok = await $.tool.call({ tool: 'Bash', command: 'python3 tools/gate.py 5.4' } as any)
  expect(ok.deny).toBe(undefined)
})

test('a blocking question is refused while the queue has open work', async ($, on) => {
  on('process.run', fake({ queue: '- [ ] 5.3 build\n' }, ''))
  on('tool.call', () => ({ result: {} }))
  const r = await $.tool.call({ tool: 'AskUserQuestion', questions: [] } as any)
  expect(String(r.deny)).toMatch(/open work/)
})

test('the turn cannot end with open work or unreported faults', async ($, on) => {
  on('process.run', fake({ queue: '- [ ] 5.3 build\n' }, ''))
  on('classic.Stop', () => ({}))
  const r: any = await ($ as any).classic.Stop({ hook_event_name: 'Stop', stop_hook_active: false, background_tasks: [] })
  expect(String(r.block)).toMatch(/open work/)
})

test('the turn cannot end while a gate failure is not put to the user', async ($, on) => {
  on('process.run', fake({ queue: '- [x] done\n', failed: '5.4|F\n' }, ''))
  on('classic.Stop', () => ({}))
  const r: any = await ($ as any).classic.Stop({ hook_event_name: 'Stop', stop_hook_active: false, background_tasks: [] })
  expect(String(r.block)).toMatch(/faults on 5.4 \(F\)/)
})

test('the turn can end when every item is done or waiting', async ($, on) => {
  on('process.run', fake({ queue: '- [x] done\n- [waiting: 5.4 F asked]\n', failed: '5.4|F\n' }, ''))
  on('classic.Stop', () => ({}))
  const r: any = await ($ as any).classic.Stop({ hook_event_name: 'Stop', stop_hook_active: false, background_tasks: [] })
  expect(r.block).toBe(undefined)
})
