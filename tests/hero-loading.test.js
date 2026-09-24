const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const LUCIDE = `window.lucide={createIcons(){document.querySelectorAll('[data-lucide]').forEach(n=>{const s=document.createElementNS('http://www.w3.org/2000/svg','svg');s.setAttribute('data-rendered','1');n.replaceWith(s);});}};`;

(async () => {
  const b = await launch();

  console.log('\n== icons render however the library arrives ==');
  for (const [label, stall, block] of [['immediately', 0, false], ['after 2s', 2000, false], ['never (blocked)', 0, true]]) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    await ctx.route(/unpkg\.com/, async (r) => {
      if (block) return r.abort();
      if (stall) await new Promise((s) => setTimeout(s, stall));
      r.fulfill({ status: 200, contentType: 'text/javascript', body: LUCIDE });
    });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', (e) => errs.push(e.message.split('\n')[0]));
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(stall + 1500);
    const n = await p.evaluate(() => document.querySelectorAll('svg[data-rendered]').length);
    if (block) ok(errs.length === 0, `library ${label}: page still runs clean (${errs.length} JS errors)`);
    else ok(n > 0, `library ${label}: icons drawn (${n})`);
    await ctx.close();
  }

  console.log('\n== hero copy appears even if the reveal never runs ==');
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    // Neutralise the reveal entirely: whatever adds .revealed, it will not stick.
    await p.addInitScript(() => {
      const add = DOMTokenList.prototype.add;
      DOMTokenList.prototype.add = function (...c) {
        if (c.includes('revealed')) return;
        return add.apply(this, c);
      };
    });
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(2500);
    const early = await p.evaluate(() => parseFloat(getComputedStyle(document.querySelector('.cinematic-text-word')).opacity));
    ok(early < 0.1, `at 2.5s the reveal genuinely has not run (opacity ${early}) - the test is valid`);
    await p.waitForTimeout(3000);
    const late = await p.evaluate(() => {
      const w = document.querySelector('.cinematic-text-word');
      const btn = document.querySelector('a[href="#services"]').parentElement;
      return { word: parseFloat(getComputedStyle(w).opacity), btn: parseFloat(getComputedStyle(btn).opacity),
               revealed: w.classList.contains('revealed') };
    });
    ok(!late.revealed, 'the reveal class never arrived, as staged');
    ok(late.word > 0.9, `headline is visible anyway (opacity ${late.word})`);
    ok(late.btn > 0.9, `call-to-action is visible anyway (opacity ${late.btn})`);
    await ctx.close();
  }

  console.log('\n== the safety net stays out of the way of the real reveal ==');
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'domcontentloaded' });
    // Curtain rises at 1.0s, headline starts 0.2s later, last element settles
    // about 2.6s. Sample either side of that.
    await p.waitForTimeout(800);
    const mid = await p.evaluate(() => parseFloat(getComputedStyle(document.querySelector('.cinematic-text-word')).opacity));
    ok(mid < 0.1, `still behind the preloader at 0.8s (opacity ${mid}) - choreography intact`);
    await p.waitForTimeout(2200);
    const done = await p.evaluate(() => {
      const w = document.querySelector('.cinematic-text-word');
      const btn = document.querySelector('a[href="#services"]').parentElement;
      return { w: parseFloat(getComputedStyle(w).opacity), b: parseFloat(getComputedStyle(btn).opacity) };
    });
    ok(done.w > 0.9, `headline revealed by 3s (opacity ${done.w})`);
    ok(done.b > 0.9, `call-to-action revealed by 3s (opacity ${done.b})`);
    await ctx.close();
  }

  await b.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll robustness checks passed.');
  process.exit(fail ? 1 : 0);
})();
