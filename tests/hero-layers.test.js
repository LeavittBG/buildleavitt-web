/* The failure on the office PC was a compositor layer that never painted and,
   because will-change pinned it, never got another chance. These checks assert
   that nothing asks to be pinned, and that the hero copy cannot end up
   invisible by any route. */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };
const SITE = FILE_ROOT + 'index.html';

const visible = (sel) => {
  const n = document.querySelector(sel);
  if (!n) return null;
  const cs = getComputedStyle(n);
  return { opacity: parseFloat(cs.opacity), transform: cs.transform, willChange: cs.willChange };
};

(async () => {
  const b = await launch();

  console.log('\n== nothing is pinned to its own layer ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.goto(SITE, { waitUntil: 'networkidle' });
    await p.waitForTimeout(3500);
    const pinned = await p.evaluate(() =>
      [...document.querySelectorAll('body *')]
        .filter((n) => { const w = getComputedStyle(n).willChange; return w && w !== 'auto'; })
        .map((n) => n.tagName + '.' + n.className.toString().slice(0, 40)));
    ok(pinned.length === 0, `no element declares will-change (${pinned.length} found${pinned.length ? ': ' + pinned.slice(0, 3).join(', ') : ''})`);
    await p.close();
  }

  console.log('\n== the reveal still plays as intended ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.goto(SITE, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(700);
    const early = await p.evaluate(visible, '.cinematic-text-word');
    ok(early.opacity < 0.1, `hidden behind the curtain at 0.7s (opacity ${early.opacity})`);
    await p.waitForTimeout(2600);
    const late = await p.evaluate(visible, '.cinematic-text-word');
    ok(late.opacity > 0.9, `revealed by 3.3s (opacity ${late.opacity})`);
    const words = await p.evaluate(() => [...document.querySelectorAll('.cinematic-text-word')]
      .map((n) => parseFloat(getComputedStyle(n).opacity)));
    ok(words.every((o) => o > 0.9), `all ${words.length} headline words are visible, none left behind`);
    await p.close();
  }

  console.log('\n== script never runs at all ==');
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    await p.goto(SITE, { waitUntil: 'load' });
    await p.waitForTimeout(400);
    const w = await p.evaluate(visible, '.cinematic-text-word').catch(() => null);
    // javaScriptEnabled:false also blocks page.evaluate, so read it from the DOM text instead.
    const shot = await p.locator('h1').screenshot();
    const sharp = require('sharp');
    const { data } = await sharp(shot).greyscale().raw().toBuffer({ resolveWithObject: true });
    const bright = data.filter((v) => v > 180).length;
    ok(bright > 500, `headline is painted with scripts off (${bright} light pixels)`);
    await ctx.close();
  }

  console.log('\n== script runs but the reveal never fires ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.addInitScript(() => {
      const add = DOMTokenList.prototype.add;
      DOMTokenList.prototype.add = function (...c) {
        if (c.includes('revealed')) return;      // the reveal is dead
        return add.apply(this, c);               // .js-anim still gets set
      };
    });
    await p.goto(SITE, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(5500);
    const w = await p.evaluate(visible, '.cinematic-text-word');
    ok(w.opacity > 0.9, `headline appears anyway via the 4s net (opacity ${w.opacity})`);
    await p.close();
  }

  console.log('\n== script dies before it can take the curtain down ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.addInitScript(() => {
      // Kill the preloader logic specifically: no timers ever fire.
      window.setTimeout = function () { return 0; };
    });
    await p.goto(SITE, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(7000);
    const pre = await p.evaluate(() => {
      const n = document.getElementById('preloader');
      if (!n) return { gone: true };
      const cs = getComputedStyle(n);
      return { gone: false, visibility: cs.visibility, transform: cs.transform };
    });
    ok(pre.gone || pre.visibility === 'hidden' || pre.transform.includes('-'),
       `curtain does not trap the visitor (${JSON.stringify(pre)})`);
    await p.close();
  }

  await b.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll layer and fallback checks passed.');
  process.exit(fail ? 1 : 0);
})();
