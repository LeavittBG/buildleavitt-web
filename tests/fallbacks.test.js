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
  ok(!(await p1.evaluate(() => document.documentElement.classList.contains('custom-cursor'))), '[reduced-motion] native cursor kept');
  ok(await p1.evaluate(() => getComputedStyle(document.querySelector('.animate-ken-burns')).animationName) === 'none', '[reduced-motion] ken burns disabled');
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
  const cursorAllowed = await p2.evaluate(() => document.documentElement.classList.contains('custom-cursor'));
  ok(!cursorAllowed, '[no-JS] native cursor kept (cursor:none never applied)');
  ok(await p2.locator('#contact form').count() === 1, '[no-JS] contact form still present');

  // --- desktop: custom cursor engages, and the ring no longer piles up animations ---
  const std = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p3 = await std.newPage();
  await p3.goto(path); await p3.waitForTimeout(4200);
  ok(await p3.evaluate(() => document.documentElement.classList.contains('custom-cursor')), '[desktop] custom-cursor class applied once JS is live');
  for (let i = 0; i < 40; i++) await p3.mouse.move(400 + i * 5, 300 + i * 3);
  await p3.waitForTimeout(800);
  const anims = await p3.evaluate(() => document.getElementById('cursor-outline').getAnimations().length);
  ok(anims === 0, `[desktop] cursor ring uses rAF, no piled-up Web Animations (found ${anims})`);
  await p3.screenshot({ path: OUT + '/shot-desktop.png' });
  await p3.locator('#contact').scrollIntoViewIfNeeded(); await p3.waitForTimeout(1500);
  await p3.screenshot({ path: OUT + '/shot-contact.png' });

  await b.close();
  console.log(fail === 0 ? '\nAll checks passed.' : `\n${fail} check(s) failed.`);
  process.exit(fail ? 1 : 0);
})();
