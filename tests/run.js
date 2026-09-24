/*
 * Run every *.test.js in this folder, one after another, and report.
 *
 *   npm test                   all of them
 *   npm test -- hero           only files whose name contains "hero"
 *
 * Each test is a plain script that exits non-zero when anything fails, so any
 * one of them can also be run on its own:  node tests/hero-wrap.test.js
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const filter = process.argv[2] || '';
const files = fs.readdirSync(__dirname)
  .filter((f) => f.endsWith('.test.js') && f.includes(filter))
  .sort();

if (!files.length) {
  console.error(`No test files match "${filter}".`);
  process.exit(1);
}

const results = [];
for (const f of files) {
  const t0 = Date.now();
  const r = spawnSync(process.execPath, [path.join(__dirname, f)], { encoding: 'utf8' });
  const secs = (Date.now() - t0) / 1000;
  const out = (r.stdout || '') + (r.stderr || '');
  const passes = (out.match(/^\s*(PASS|ok)\b/gm) || []).length;
  const failed = r.status !== 0;
  results.push({ f, secs, passes, failed });
  console.log(`${failed ? 'FAIL' : 'pass'}  ${f.padEnd(28)} ${secs.toFixed(1).padStart(5)}s  ${passes} checks`);
  // A failing file prints its failures, and the tail of its output in case it
  // died before it could print any.
  if (failed) {
    const lines = out.split('\n');
    const fails = lines.filter((l) => /FAIL|Error/.test(l));
    for (const l of (fails.length ? fails : lines.slice(-15)).slice(0, 25)) console.log('      ' + l);
  }
}

const bad = results.filter((r) => r.failed);
const total = results.reduce((a, r) => a + r.secs, 0);
const checks = results.reduce((a, r) => a + r.passes, 0);
console.log(`\n${results.length - bad.length}/${results.length} files passed, ${checks} checks, ${total.toFixed(0)}s`);
process.exit(bad.length ? 1 : 0);
