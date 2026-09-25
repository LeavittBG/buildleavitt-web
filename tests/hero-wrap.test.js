const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');
const probe = () => {
  const byY = new Map();
  // Measure the mask each word sits in, not the word. The words slide up into
  // place when the page loads, and a word caught mid-slide reports a different
  // height from its neighbours - which read as a line break that was not there
  // and failed this test at random widths once the intro got shorter. The masks
  // never move, so their position is the line the word is actually on.
  for (const w of document.querySelectorAll('.cinematic-text-word')) {
    const y = Math.round(w.closest('.overflow-hidden-mask').getBoundingClientRect().y);
    if (!byY.has(y)) byY.set(y, []);
    byY.get(y).push(w.textContent.trim());
  }
  const de = document.documentElement;
  const h1 = document.querySelector('h1').getBoundingClientRect();
  const widest = Math.max(...[...document.querySelectorAll('.hero-line')].map(n => n.scrollWidth));
  return {
    lines: [...byY.entries()].sort((a, b) => a[0] - b[0]).map(([, v]) => v.join(' ')),
    pageOverflow: Math.max(0, de.scrollWidth - de.clientWidth),
    lineFits: widest <= Math.ceil(h1.width),
    font: Math.round(parseFloat(getComputedStyle(document.querySelector('h1')).fontSize)),
  };
};
(async () => {
  const b = await launch();
  const WANT = 'Crafting Custom Homes | Across the Region.';
  let bad = 0;
  const widths = [320, 360, 375, 390, 414, 480, 540, 600, 640, 700, 768, 820, 900, 1000, 1024, 1100, 1180, 1280, 1366, 1440, 1536, 1600, 1728, 1920, 2200, 2560];
  for (const w of widths) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    const r = await p.evaluate(probe);
    const sig = r.lines.join(' | ');
    const good = sig === WANT && r.pageOverflow === 0 && r.lineFits;
    if (!good) { bad++; console.log(`  FAIL ${w}px  font ${r.font}px  overflow ${r.pageOverflow}  fits ${r.lineFits}  ${sig}`); }
    else console.log(`  ok   ${String(w).padStart(4)}px  font ${r.font}px  ${sig}`);
    await ctx.close();
  }
  await b.close();
  console.log(bad ? `\n${bad} of ${widths.length} widths FAILED` : `\nAll ${widths.length} widths: headline reads in two lines, no overflow, each line fits its box.`);
  process.exit(bad ? 1 : 0);
})();
