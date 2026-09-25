const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const b = await launch();

  console.log('\n== icons are part of the page, not fetched from anyone ==');
  // The icons used to be drawn by lucide@latest from unpkg. Lucide 1.0 dropped
  // its Facebook and Instagram icons and ten of them went blank on the live site
  // without anything noticing. They are inline SVG now; these checks keep it so.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    const offsite = [];
    p.on('request', (r) => {
      const u = new URL(r.url());
      if (/^https?:$/.test(u.protocol) && !/^(fonts\.(googleapis|gstatic)\.com|www\.googletagmanager\.com)$/.test(u.hostname) && r.resourceType() === 'script') offsite.push(u.hostname);
    });
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'load' });
    await p.waitForTimeout(3000);
    ok(offsite.length === 0, `no third-party script is fetched to draw the page (${[...new Set(offsite)].join(', ') || 'none'})`);
    const r = await p.evaluate(() => {
      const social = [...document.querySelectorAll('a[href*="facebook.com"], a[href*="instagram.com"]')];
      return {
        leftover: document.querySelectorAll('[data-lucide]').length,
        socialIcons: social.map((a) => { const s = a.querySelector('svg'); const b = s && s.getBoundingClientRect(); return b ? b.width * b.height : 0; }),
      };
    });
    ok(r.leftover === 0, `no icon is left waiting for a library to draw it (${r.leftover})`);
    ok(r.socialIcons.length >= 10 && r.socialIcons.every((a) => a > 0),
      `every Facebook and Instagram link draws its icon (${r.socialIcons.filter((a) => a > 0).length} of ${r.socialIcons.length})`);
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
