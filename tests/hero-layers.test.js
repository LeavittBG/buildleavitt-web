/* The failure on the office PC was a compositor layer that never painted and,
   because will-change pinned it, never got another chance: the headline kept
   its space and showed no words. The slide-in that used those layers is gone,
   but the rule stands - nothing may pin itself to a layer - and the headline
   must paint whether or not script runs. */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');
const sharp = require('sharp');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };
const SITE = FILE_ROOT + 'index.html';

// Count light pixels in the headline: white text on the dark hero.
async function painted(page) {
  const shot = await page.locator('h1').screenshot();
  const { data } = await sharp(shot).greyscale().raw().toBuffer({ resolveWithObject: true });
  return data.filter((v) => v > 180).length;
}

(async () => {
  const b = await launch();

  console.log('\n== nothing is pinned to its own layer ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.goto(SITE, { waitUntil: 'networkidle' });
    const pinned = await p.evaluate(() =>
      [...document.querySelectorAll('body *')]
        .filter((n) => { const w = getComputedStyle(n).willChange; return w && w !== 'auto'; })
        .map((n) => n.tagName + '.' + n.className.toString().slice(0, 40)));
    ok(pinned.length === 0, `no element declares will-change (${pinned.length} found${pinned.length ? ': ' + pinned.slice(0, 3).join(', ') : ''})`);
    await p.close();
  }

  console.log('\n== the headline paints, with and without script ==');
  for (const js of [true, false]) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: js });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    await p.goto(SITE, { waitUntil: 'load' });
    const n = await painted(p);
    ok(n > 500, `headline is painted with scripts ${js ? 'on' : 'off'} (${n} light pixels)`);
    await ctx.close();
  }

  await b.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll layer and fallback checks passed.');
  process.exit(fail ? 1 : 0);
})();
