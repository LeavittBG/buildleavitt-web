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

  // Scroll through so lazy images load and reveal animations settle; without this
  // currentSrc is empty and unrevealed .reveal-elements are still offset 30px.
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
    .filter((i) => i.id !== 'lightbox-img')
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

  // display:contents must leave the gallery grid untouched
  const geom = await p.evaluate(() => {
    const imgs = [...document.querySelectorAll('#gallery .gallery-img')];
    // offsetLeft/offsetTop are layout positions and ignore the reveal transform,
    // unlike getBoundingClientRect which would report translateY(30px) offsets.
    return imgs.map((i) => ({ w: i.offsetWidth, h: i.offsetHeight, left: i.offsetLeft, top: i.offsetTop }));
  });
  ok(new Set(geom.map((g) => g.w)).size === 1 && geom[0].w > 200,
     `gallery tiles all ${geom[0].w}px wide - grid intact under display:contents`);
  ok(new Set(geom.map((g) => g.h)).size === 1, 'gallery tiles all equal height');
  ok(new Set(geom.map((g) => g.left)).size === 3,
     `gallery still in 3 columns (found ${new Set(geom.map((g) => g.left)).size})`);
  // Regression guard: <source> must not claim its own grid cell under display:contents.
  const rowTops = new Set(geom.map((g) => g.top));
  ok(rowTops.size === 2,
     `gallery is 2 rows of 3, i.e. <source> takes no grid cell (found ${rowTops.size} rows)`);

  // Lightbox resolution
  await p.locator('.gallery-img').first().scrollIntoViewIfNeeded();
  await p.locator('.gallery-img').first().click();
  await p.waitForTimeout(500);
  const lb = await p.locator('#lightbox-img').evaluate((el) => el.currentSrc.split('/').pop());
  ok(lb.endsWith('.webp'), `lightbox opens the WebP (${lb})`);
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);

  // Every tile, not just the first: the lightbox takes currentSrc, so a tile
  // whose WebP was missing would quietly open the heavier fallback.
  const count = await p.locator('.gallery-img').count();
  const opened = [];
  for (let i = 0; i < count; i++) {
    await p.locator('.gallery-img').nth(i).scrollIntoViewIfNeeded();
    await p.locator('.gallery-img').nth(i).click();
    await p.waitForTimeout(350);
    opened.push(await p.locator('#lightbox-img').evaluate((el) => el.currentSrc.split('/').pop()));
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
  }
  ok(opened.every((f) => f.endsWith('.webp')),
     `all ${count} gallery tiles open as WebP` +
     (opened.some((f) => !f.endsWith('.webp')) ? ': ' + opened.filter(f => !f.endsWith('.webp')).join(', ') : ''));

  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(600);
  await p.screenshot({ path: OUT + '/shot-webp-hero.png' });
  await p.locator('#gallery').scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
  await p.screenshot({ path: OUT + '/shot-webp-gallery.png' });

  await b.close();
  console.log(fail === 0 ? '\nAll WebP checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
