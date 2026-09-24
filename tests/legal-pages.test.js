const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
// Real Inter/Playfair, not a system fallback - text width decides these layouts.
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };
(async () => {
  const b = await launch();

  for (const page of ['privacy', 'terms']) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(`${FILE_ROOT}${page}.html`);
    await p.waitForTimeout(800);
    ok(errs.length === 0, `[${page}] no JS errors`);
    ok((await p.title()).length > 0, `[${page}] title: "${await p.title()}"`);
    ok(await p.locator('h1').count() === 1, `[${page}] exactly one <h1>`);
    const year = await p.locator('#year').textContent();
    ok(year === String(new Date().getFullYear()), `[${page}] footer year renders (${year})`);
    ok(await p.locator('header img').evaluate(i => i.naturalWidth > 0), `[${page}] logo loads`);
    const served = await p.locator('header img').evaluate(i => i.currentSrc.split('/').pop());
    ok(served === 'Gold.webp', `[${page}] logo served as WebP (${served})`);
    // no horizontal overflow at mobile width
    await p.setViewportSize({ width: 390, height: 844 });
    await p.waitForTimeout(400);
    const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    ok(overflow <= 0, `[${page}] no horizontal overflow at 390px (${overflow}px)`);
    await p.screenshot({ path: `${OUT}/shot-${page}.png` });
    await p.close();
  }

  // Footer links from the homepage actually navigate
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await serveFonts(p);
  await p.goto(FILE_ROOT + 'index.html');
  await p.waitForTimeout(4200);
  await p.locator('footer a[href="privacy.html"]').click();
  await p.waitForTimeout(600);
  ok(p.url().endsWith('privacy.html'), `homepage footer -> privacy (${p.url().split('/').pop()})`);
  await p.goBack(); await p.waitForTimeout(4200);
  await p.locator('footer a[href="terms.html"]').click();
  await p.waitForTimeout(600);
  ok(p.url().endsWith('terms.html'), `homepage footer -> terms (${p.url().split('/').pop()})`);
  // and back home from a legal page
  await p.locator('footer a[href="/"]').first().click();
  await p.waitForTimeout(600);
  ok(p.url().endsWith('index.html') || p.url().endsWith('/'), 'legal page -> home');

  await b.close();
  console.log(fail === 0 ? '\nAll legal-page checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
