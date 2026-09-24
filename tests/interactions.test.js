const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const path = FILE_ROOT + 'index.html';
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const browser = await launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));

  // Block the CDNs to prove the page survives a third-party failure.
  if (process.env.OFFLINE) await page.route('**://{unpkg.com,cdn.tailwindcss.com,fonts.googleapis.com,fonts.gstatic.com}/**', r => r.abort());

  await page.goto(path, { waitUntil: 'load' });
  await page.waitForTimeout(4200); // let the 2.4s preloader finish

  ok(errors.length === 0, 'no uncaught JS errors' + (errors.length ? ': ' + errors.join(' | ') : ''));
  ok(await page.locator('#preloader').count() === 0, 'preloader removed after load');
  ok(await page.locator('h1 .cinematic-text-word.revealed').count() === 6, 'hero headline words revealed');

  // Service modal: open by keyboard, close with Escape, focus restored
  const card = page.locator('.service-card').first();
  await card.focus();
  await page.keyboard.press('Enter');
  await page.waitForTimeout(400);
  ok(await page.locator('#service-modal').isVisible(), 'service modal opens via keyboard Enter');
  ok((await page.locator('#service-modal-title').textContent()).includes('Custom Ground-Up'), 'service modal shows correct title');
  ok(await page.evaluate(() => getComputedStyle(document.body).overflow) === 'hidden', 'body scroll locked while modal open');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  ok(!(await page.locator('#service-modal').isVisible()), 'Escape closes the service modal');
  ok(await page.evaluate(() => getComputedStyle(document.body).overflow) !== 'hidden', 'body scroll restored');
  ok(await page.evaluate(() => document.activeElement?.classList.contains('service-card')), 'focus returned to the card');

  // Process modal via click
  await page.locator('.process-card').nth(2).click();
  await page.waitForTimeout(400);
  ok((await page.locator('#process-modal-step').textContent()).trim() === 'Step 03', 'process modal shows Step 03');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  // Lightbox carries alt text across
  await page.locator('.gallery-img').first().scrollIntoViewIfNeeded();
  const firstAlt = await page.locator('.gallery-img').first().getAttribute('alt');
  await page.locator('.gallery-img').first().click();
  await page.waitForTimeout(400);
  ok(await page.locator('#lightbox').isVisible(), 'lightbox opens');
  // Compare against the source image rather than a hard-coded string, so this
  // keeps working when the gallery photos change.
  ok((await page.locator('#lightbox-img').getAttribute('alt')) === firstAlt,
     `lightbox carries the source alt text ("${(firstAlt || '').slice(0, 40)}...")`);
  ok((firstAlt || '').length > 20, 'gallery alt text is descriptive, not a placeholder');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  ok(!(await page.locator('#lightbox').isVisible()), 'Escape closes the lightbox');

  // Testimonial dots (the selector that was broken)
  await page.locator('#testimonial-dots button').nth(2).scrollIntoViewIfNeeded();
  await page.locator('#testimonial-dots button').nth(2).click();
  await page.waitForTimeout(1200);
  ok(await page.locator('.testimonial-slide').nth(2).evaluate(el => el.classList.contains('opacity-100')), 'third dot activates third testimonial');
  ok(await page.locator('#testimonial-dots button').nth(2).evaluate(el => el.className.includes('bg-[#c2a67a]')), 'third dot marked active');

  // Before/After slider responds to a drag
  const slider = page.locator('#ba-slider');
  await slider.scrollIntoViewIfNeeded();
  const box = await slider.boundingBox();
  await page.mouse.move(box.x + box.width * 0.25, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.75, box.y + box.height / 2, { steps: 10 });
  await page.mouse.up();
  const clip = await page.locator('#ba-after-wrapper').evaluate(el => el.style.clipPath);
  ok(/7[0-9](\.\d+)?%/.test(clip), 'slider drag updates the clip path (' + clip.slice(0, 40) + ')');

  // Counters ran
  await page.locator('.counter').first().scrollIntoViewIfNeeded();
  await page.waitForTimeout(2500);
  ok(await page.locator('.counter').first().textContent() === '20', 'counter animated to its target');


  // --- Before/After slider regressions ---
  await page.locator("#ba-slider").scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  const sBox = await page.locator("#ba-slider").boundingBox();
  const knob = await page.locator(".ba-handle-button").boundingBox();
  await page.mouse.move(sBox.x + sBox.width / 2, sBox.y + sBox.height / 2);
  await page.waitForTimeout(600);
  const centred = await page.evaluate(() => {
    const bar = document.getElementById("ba-handle").getBoundingClientRect();
    const btn = document.querySelector(".ba-handle-button").getBoundingClientRect();
    return { dx: Math.abs((btn.left + btn.width/2) - (bar.left + bar.width/2)),
             dy: Math.abs((btn.top + btn.height/2) - (bar.top + bar.height/2)),
             scaled: getComputedStyle(document.querySelector(".ba-handle-button")).transform };
  });
  ok(centred.dx < 2 && centred.dy < 2,
     `slider knob stays centred on the divider while hovered (off by ${centred.dx.toFixed(0)},${centred.dy.toFixed(0)}px)`);
  ok(/matrix\(1\.1/.test(centred.scaled), "knob still grows on hover (" + centred.scaled + ")");

  await page.mouse.move(knob.x + knob.width/2, knob.y + knob.height/2);
  await page.mouse.down();
  for (let i = 1; i <= 15; i++) { await page.mouse.move(knob.x - i*30, knob.y - i*20); await page.waitForTimeout(12); }
  const dragSel = await page.evaluate(() => window.getSelection().toString().trim().length);
  await page.mouse.up();
  ok(dragSel === 0, `dragging the knob selects no page text (${dragSel} chars)`);

  // Mobile menu aria state
  const mob = await ctx.newPage();
  await mob.setViewportSize({ width: 390, height: 844 });
  await mob.goto(path); await mob.waitForTimeout(4200);
  await mob.locator('#mobile-menu-btn').click();
  await mob.waitForTimeout(200);
  ok(await mob.locator('#mobile-menu-btn').getAttribute('aria-expanded') === 'true', 'menu button reports aria-expanded=true');
  ok(await mob.locator('#mobile-menu').isVisible(), 'mobile menu opens');
  await mob.locator('#mobile-menu-btn').click();
  await mob.waitForTimeout(200);
  ok(await mob.locator('#mobile-menu-btn').getAttribute('aria-expanded') === 'false', 'menu button reports aria-expanded=false');
  ok(!(await mob.locator('#mobile-menu').isVisible()), 'mobile menu closes');
  await mob.locator('#mobile-menu-btn').click();
  await mob.waitForTimeout(200);
  ok(await mob.locator('#mobile-menu').isVisible(), 'mobile menu re-opens on a third toggle');

  await browser.close();
  console.log(fail === 0 ? '\nAll browser checks passed.' : `\n${fail} browser check(s) failed.`);
  process.exit(fail ? 1 : 0);
})();
