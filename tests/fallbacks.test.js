const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const path = FILE_ROOT + 'index.html';
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const b = await launch();

  // --- prefers-reduced-motion: reduce ---
  const rm = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
  const p1 = await rm.newPage();
  await p1.goto(path); await p1.waitForTimeout(700);
  ok(await p1.locator('#preloader').count() === 0, '[reduced-motion] preloader removed immediately, no intro wait');
  ok(await p1.locator('h1 .cinematic-text-word.revealed').count() === 6, '[reduced-motion] headline shown at once');
  await p1.screenshot({ path: OUT + '/shot-reduced.png' });

  // --- JavaScript disabled (no addStyleTag: that itself needs JS) ---
  const nojs = await b.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false });
  const p2 = await nojs.newPage();
  await p2.goto(path); await p2.waitForTimeout(400);
  const disp = await p2.locator('#preloader').evaluate(el => getComputedStyle(el).display);
  ok(disp === 'none', `[no-JS] preloader hidden by the noscript fallback (display=${disp})`);
  const heroOpacity = await p2.locator('h1 .cinematic-text-word').first().evaluate(el => getComputedStyle(el).opacity);
  ok(heroOpacity === '1', `[no-JS] hero words visible (opacity=${heroOpacity})`);
  const svcOpacity = await p2.locator('#services .reveal-element').first().evaluate(el => getComputedStyle(el).opacity);
  ok(svcOpacity === '1', `[no-JS] section content visible (opacity=${svcOpacity})`);
  ok(await p2.locator('#contact form').count() === 1, '[no-JS] contact form still present');

  // --- desktop: the visitor keeps their own mouse pointer ---
  // The site used to swap it for a gold dot and trailing ring - a stock
  // template effect that was taken out. Nothing may hide the real pointer.
  const std = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p3 = await std.newPage();
  await p3.goto(path); await p3.waitForTimeout(4200);
  await p3.mouse.move(640, 450);
  const pointer = await p3.evaluate(() => ({
    replaced: !!document.querySelector('#cursor-dot, #cursor-outline, .cursor-dot, .cursor-outline'),
    hidden: [document.body, ...document.querySelectorAll('a, button, input, select, textarea')]
      .filter((el) => getComputedStyle(el).cursor === 'none').length,
  }));
  ok(!pointer.replaced && pointer.hidden === 0, `[desktop] no custom cursor, native pointer never hidden (hidden on ${pointer.hidden} elements)`);
  await p3.screenshot({ path: OUT + '/shot-desktop.png' });
  await p3.locator('#contact').scrollIntoViewIfNeeded(); await p3.waitForTimeout(1500);
  await p3.screenshot({ path: OUT + '/shot-contact.png' });

  await b.close();
  console.log(fail === 0 ? '\nAll checks passed.' : `\n${fail} check(s) failed.`);
  process.exit(fail ? 1 : 0);
})();
