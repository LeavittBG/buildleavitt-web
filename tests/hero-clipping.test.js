/*
 * Does the hero headline clip any of its own glyphs?
 *
 * The masks exist to hide the words while they slide up, so they have to clip
 * vertically. The test is whether they also clip horizontally, which is always a
 * defect: switch overflow to visible and nothing about the painted pixels should
 * change. Any pixel that differs is ink the shipped page is cutting off.
 *
 */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const sharp = require('sharp');
const path = require('path');
const { serveFonts, assertLoaded } = require('./lib/fonts');

const SITE = FILE_ROOT + 'index.html';
const WIDTHS = [390, 768, 1024, 1280, 1440];

// The headline is Playfair Display italic and the whole question is how far its
// "A" overhangs, so ./fonts serves the real font rather than letting the page
// fall back to a system serif. See the note there.

// Freeze the reveal animation in its finished state and drop the hero photo and
// its overlays, so the only thing left in the frame is white text on black.
// Everything that moves has to be stopped, not just the headline words: the
// check below counts any pixel that differs between two screenshots as clipped
// ink, so anything still in motion between them reads as a failure. The
// strapline above the headline slides 30px into place, and once the preloader
// was cut to 1s its slide landed inside this test's screenshot window - which
// is how the test came to fail intermittently, reporting the strapline
// (x 24-270) as "clipped" while the headline itself was fine.
const SETTLE = `
  document.getElementById('preloader')?.remove();
  const still = document.createElement('style');
  still.textContent = '*, *::before, *::after { transition: none !important; animation: none !important; }';
  document.head.appendChild(still);
  document.querySelectorAll('.cinematic-text-word, .cinematic-fade-up').forEach(w => w.classList.add('revealed'));
  document.querySelectorAll('#home img, #home video, .animate-ken-burns').forEach(n => n.remove());
  document.body.style.background = '#000';
`;

const wordRects = () =>
  [...document.querySelectorAll('.cinematic-text-word')].map((w) => {
    const r = w.getBoundingClientRect();
    return { text: w.textContent.trim(), x: +r.x.toFixed(2), y: +r.y.toFixed(2), w: +r.width.toFixed(2) };
  });

async function diffPixels(a, b) {
  const [ra, rb] = await Promise.all(
    [a, b].map((buf) => sharp(buf).greyscale().raw().toBuffer({ resolveWithObject: true })),
  );
  if (ra.data.length !== rb.data.length) throw new Error('frame size changed between shots');
  const { width } = ra.info;
  let n = 0;
  let minX = Infinity;
  let maxX = -Infinity;
  for (let i = 0; i < ra.data.length; i++) {
    if (Math.abs(ra.data[i] - rb.data[i]) > 8) {
      n++;
      const x = i % width;
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
    }
  }
  return { n, minX, maxX };
}

(async () => {
  const browser = await launch();
  let failures = 0;

  for (const width of WIDTHS) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
    await serveFonts(page);
    await page.goto(SITE, { waitUntil: 'networkidle' });
    await assertLoaded(page, 'Playfair');
    await page.evaluate(SETTLE);
    await page.waitForTimeout(150);

    const h1 = page.locator('h1').first();
    const box = await h1.boundingBox();
    // Take a generous margin either side: a clipped glyph's missing ink lies
    // outside the element box, so a tight clip would hide the very thing we want.
    const clip = {
      x: Math.max(0, box.x - 30),
      y: Math.max(0, box.y - 20),
      width: Math.min(width - Math.max(0, box.x - 30), box.width + 60),
      height: box.height + 40,
    };

    const before = await wordRects_(page);
    const shipped = await page.screenshot({ clip });

    await page.addStyleTag({ content: '.overflow-hidden-mask { overflow: visible !important; }' });
    const unclipped = await page.screenshot({ clip });
    const after = await wordRects_(page);

    const { n, minX, maxX } = await diffPixels(shipped, unclipped);
    const moved = JSON.stringify(before) !== JSON.stringify(after);

    const where = n ? `  clipped ink at CSS x ${(minX / 2).toFixed(1)}-${(maxX / 2).toFixed(1)}` : '';
    console.log(`${n === 0 ? 'ok  ' : 'FAIL'} ${String(width).padStart(4)}px  ${n} clipped px${where}`);
    if (moved) console.log(`     note: word positions shifted when overflow changed`);
    if (n !== 0) failures++;

    await page.close();
  }

  // The words must sit exactly where they did before the left pad was added.
  // padding-left and margin-left cancel in the outer box, so they should.
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await serveFonts(page);
  await page.goto(SITE, { waitUntil: 'networkidle' });
  await assertLoaded(page, 'Playfair');
  await page.evaluate(SETTLE);
  const withPad = await wordRects_(page);
  await page.addStyleTag({
    content: '.overflow-hidden-mask { padding-left: 0 !important; margin-left: 0 !important; }',
  });
  const withoutPad = await wordRects_(page);
  const shifts = withPad
    .map((w, i) => ({ text: w.text, dx: +(w.x - withoutPad[i].x).toFixed(2) }))
    .filter((s) => Math.abs(s.dx) > 0.01);
  if (shifts.length) {
    console.log(`FAIL layout shifted by the left pad: ${shifts.map((s) => `${s.text} ${s.dx}px`).join(', ')}`);
    failures++;
  } else {
    console.log(`ok   layout unchanged by the left pad (all ${withPad.length} words)`);
  }
  await page.close();

  await browser.close();
  process.exit(failures ? 1 : 0);
})();

async function wordRects_(page) {
  return page.evaluate(`(${wordRects.toString()})()`);
}
