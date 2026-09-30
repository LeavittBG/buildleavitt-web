const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
// Real Inter/Playfair, not a system fallback - text width decides these layouts.
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const b = await launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await serveFonts(p);
  await p.goto(FILE_ROOT + 'index.html');
  await p.waitForTimeout(4200);

  // Scroll through so lazy images load; without this currentSrc is empty.
  await p.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 300) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 90));
    }
  });
  // Bounded wait: a lazy image that never intersected stays !complete forever.
  await p.evaluate(() => Promise.all([...document.images].filter((i) => !i.complete).map((i) =>
    Promise.race([
      new Promise((r) => { i.addEventListener('load', r, { once: true }); i.addEventListener('error', r, { once: true }); }),
      new Promise((r) => setTimeout(r, 3000)),
    ]))));
  await p.waitForTimeout(1000);

  const loaded = await p.evaluate(() => [...document.querySelectorAll('img')]
    .map((i) => ({ fallback: i.getAttribute('src'), actual: (i.currentSrc || '').split('/').pop(),
                   w: i.naturalWidth, h: i.naturalHeight })));

  // Every photo on the page now has a WebP worth serving. This used to allow two
  // exceptions for project5, whose WebP came out larger than its JPEG; that photo
  // was retired with the rest of the old portfolio.
  const webpCount = loaded.filter((i) => i.actual.endsWith('.webp')).length;
  const notWebp = loaded.filter((i) => !i.actual.endsWith('.webp'));
  ok(webpCount === loaded.length,
     `${webpCount}/${loaded.length} images served as WebP` +
     (notWebp.length ? ' - not: ' + [...new Set(notWebp.map((i) => i.fallback))].join(', ') : ''));
  ok(loaded.every((i) => i.w > 0 && i.h > 0), 'every image decoded (no broken images)');

  // This file also used to check the photo gallery's grid and its lightbox:
  // that <source> took no grid cell under display:contents, and that every tile
  // opened the WebP. The gallery and lightbox came off the site with The
  // Storyteller's photographs in September 2026; the WebP checks above still
  // cover every image that remains.

  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(600);
  await p.screenshot({ path: OUT + '/shot-webp-hero.png' });
  await p.locator('#plans').scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
  await p.screenshot({ path: OUT + '/shot-webp-plans.png' });

  await b.close();
  console.log(fail === 0 ? '\nAll WebP checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
