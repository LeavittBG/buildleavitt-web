/*
 * A phone is not sent the full-size picture of a house to fill a small card.
 *
 * The November 10, 2026 audit (item 6) found every plan rendering in one size:
 * 1468 pixels wide (the Modern Brick ones 1600), 190 to 315 KB each, whether it
 * filled a plan page on a desktop or a card 340 pixels wide on a phone. The
 * homepage shows six of them, /plans/ seventeen. WebP made no difference: for
 * these pictures it is no smaller than JPEG.
 *
 * Each rendering now also exists 640 and 960 pixels wide (about 45 and 95 KB),
 * and every place one is shown lists all three with the width it will be
 * drawn at, so the browser takes the smallest that still looks sharp.
 *
 * Browsers choose differently. Chrome takes the nearest size; Safari takes the
 * first one at least as sharp as the screen, which on an iPhone (three device
 * pixels to each CSS pixel) would be the full-size file again for a 340px
 * card. So on a phone with a screen that sharp the page asks for a little less
 * than the card's width, and both browsers settle on the 960 copy: 2.8 device
 * pixels per pixel on a 3x screen, which the eye cannot tell from 3.
 *
 * This checks the files and the markup, then opens the pages as an iPhone, an
 * older phone and a laptop and reads which file the browser really took. It
 * also works out what Safari would take, by Safari's rule, from the same
 * markup. A picture must never be the full-size file on a phone, and never so
 * small that it is drawn blurred.
 *   node tests/plan-pictures.test.js
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { JSDOM } = require('jsdom');
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const MODELS = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'plans.json'), 'utf8')).models;
const IMG = path.join(ROOT, 'plans', 'img');
// A rendering: the cover photo of a plan, or the same house in another exterior.
const RENDERING = /plans\/img\/([a-z0-9-]+-elevation(?:-[a-z-]+)?)\.jpg$/;
const kb = (n) => Math.round(n / 1024);

(async () => {
  // ---------------------------------------------------------------- the files
  console.log('\n== every rendering exists in three widths ==');
  const names = MODELS.flatMap((m) => m.pages.filter((p) => /^elevation/.test(p.id)).map((p) => `${m.slug}-${p.id}`))
    .filter((n) => fs.existsSync(path.join(IMG, n + '.jpg')));
  const missing = [];
  const heavy = [];
  let full = 0;
  let small = 0;
  for (const n of names) {
    full += fs.statSync(path.join(IMG, n + '.webp')).size;
    for (const [w, limit] of [[640, 75], [960, 150]]) {
      for (const ext of ['webp', 'jpg']) {
        const f = path.join(IMG, `${n}-${w}.${ext}`);
        if (!fs.existsSync(f)) { missing.push(`${n}-${w}.${ext}`); continue; }
        const meta = await sharp(f).metadata();
        if (meta.width !== w) missing.push(`${n}-${w}.${ext} is ${meta.width}px wide`);
        if (fs.statSync(f).size > limit * 1024) heavy.push(`${n}-${w}.${ext} ${kb(fs.statSync(f).size)} KB`);
        if (w === 640 && ext === 'webp') small += fs.statSync(f).size;
      }
    }
  }
  ok(names.length >= 34 && missing.length === 0, `${names.length} renderings, each with a 640 and a 960 copy as WebP and JPEG`
    + (missing.length ? ` - ${missing.length} missing or the wrong size: ${missing.slice(0, 4).join(', ')} ...` : ''));
  ok(missing.length === 0 && heavy.length === 0, `the 640 copies are under 75 KB and the 960 copies under 150 KB (640: ${kb(small / names.length)} KB on average; full size: ${kb(full / names.length)} KB)`
    + (heavy.length ? ' - ' + heavy.slice(0, 4).join(', ') : ''));

  // --------------------------------------------------------------- the markup
  console.log('\n== every place a rendering is shown offers the three widths ==');
  const pages = ['index.html', 'semi-custom-homes.html', 'plans/index.html', ...MODELS.map((m) => `plans/${m.slug}.html`)];
  const bad = [];
  let shown = 0;
  for (const f of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), 'utf8')).window.document;
    for (const img of doc.querySelectorAll('img')) {
      if (!RENDERING.test(img.getAttribute('src') || '')) continue;
      shown++;
      for (const el of [img, ...img.closest('picture').querySelectorAll('source')]) {
        const widths = (el.getAttribute('srcset') || '').split(',').map((c) => parseInt(c.trim().split(/\s+/)[1], 10));
        if (!(widths.length === 3 && widths[0] === 640 && widths[1] === 960 && widths[2] > 1200 && el.getAttribute('sizes'))) {
          bad.push(`${f}: ${img.getAttribute('src').split('/').pop()} <${el.tagName.toLowerCase()}>`);
        }
      }
    }
  }
  ok(shown >= 17 * 3 + 6 && bad.length === 0, `${shown} renderings on ${pages.length} pages, every one with 640, 960 and full size and a stated width`
    + (bad.length ? ` - ${bad.length} without: ${bad.slice(0, 4).join(', ')} ...` : ''));

  // ---------------------------------------------------------- in the browser
  const site = await serveRepo();
  const b = await launch();
  const SCREENS = [
    { name: 'an iPhone (390px, 3x)', width: 390, height: 844, scale: 3, phone: true },
    { name: 'an older phone (360px, 2x)', width: 360, height: 740, scale: 2, phone: true },
    { name: 'a laptop (1280px, 1x)', width: 1280, height: 800, scale: 1, phone: false },
  ];
  const URLS = ['/', '/plans/', '/semi-custom-homes.html', '/plans/the-poet.html', '/plans/the-storyteller.html'];

  // In the page: each rendering on show, the file the browser took, its place,
  // and the file Safari's rule would take from the same srcset and sizes.
  const read = async (rendering) => {
    const re = new RegExp(rendering);
    const imgs = [...document.querySelectorAll('img')].filter((i) => re.test(i.getAttribute('src') || '') && i.closest('picture'));
    const out = [];
    for (const img of imgs) {
      if (!img.offsetParent) continue;   // not on show: a finder card that is filtered out
      img.loading = 'eager';
      img.scrollIntoView({ block: 'center', behavior: 'instant' });
      await new Promise((r) => { if (img.complete && img.naturalWidth) r(); else { img.addEventListener('load', r, { once: true }); img.addEventListener('error', r, { once: true }); setTimeout(r, 5000); } });
      if (img.getBoundingClientRect().width < 2) continue;
      const source = img.closest('picture').querySelector('source[type="image/webp"]') || img;
      const candidates = (source.getAttribute('srcset') || '').split(',').map((c) => c.trim().split(/\s+/))
        .map(([file, w]) => ({ file: file.split('/').pop(), w: parseInt(w, 10) })).filter((c) => c.w > 0);
      // sizes: the first entry whose condition holds, as a length in pixels
      let slotStated = null;
      for (const entry of (source.getAttribute('sizes') || '').split(',').map((e) => e.trim()).filter(Boolean)) {
        const m = /^(\(.*\))\s+(\S.*)$/.exec(entry);
        const [cond, length] = m ? [m[1], m[2]] : [null, entry];
        if (cond && !matchMedia(cond).matches) continue;
        const probe = document.createElement('div');
        probe.style.cssText = `position:absolute;visibility:hidden;width:${length}`;
        document.body.appendChild(probe);
        slotStated = probe.getBoundingClientRect().width;
        probe.remove();
        break;
      }
      const safari = slotStated ? (candidates.find((c) => c.w / slotStated >= devicePixelRatio) || candidates[candidates.length - 1]) : null;
      // The file's own width, by its name in the list: with a srcset the
      // browser reports naturalWidth already divided by the screen's sharpness.
      const took = (img.currentSrc || '').split('/').pop();
      out.push({
        took,
        natural: (candidates.find((c) => c.file === took) || {}).w || 0,
        drawn: img.getBoundingClientRect().width,
        full: candidates.length ? candidates[candidates.length - 1].w : null,
        safari: safari ? safari.w : null,
      });
    }
    return out;
  };

  let bytesFull = 0;
  let bytesTaken = 0;
  for (const screen of SCREENS) {
    console.log(`\n== ${screen.name} ==`);
    for (const url of URLS) {
      const ctx = await b.newContext({ viewport: { width: screen.width, height: screen.height }, deviceScaleFactor: screen.scale });
      const p = await ctx.newPage();
      await serveFonts(p);
      await p.goto(site.base + url, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      const got = await p.evaluate(read, RENDERING.source);
      await ctx.close();

      const sharpEnough = (width, r) => width >= r.drawn * Math.min(screen.scale, 1.8) - 1;
      const tooBig = got.filter((r) => screen.phone && (r.natural >= r.full || r.safari >= r.full));
      const blurred = got.filter((r) => r.full && !(sharpEnough(r.natural, r) && sharpEnough(r.safari, r)) && r.natural < r.full);
      const taken = [...new Set(got.map((r) => r.natural))].sort((x, y) => x - y).join(', ');
      const bySafari = [...new Set(got.map((r) => r.safari))].sort((x, y) => x - y).join(', ');
      ok(got.length > 0 && got.every((r) => r.full) && tooBig.length === 0 && blurred.length === 0,
        `${url}: ${got.length} renderings; Chrome took ${taken}px wide, Safari would take ${bySafari}px`
        + (screen.phone ? ', never the full-size file' : '')
        + (tooBig.length ? ` - ${tooBig.length} are the full-size file` : '')
        + (blurred.length ? ` - ${blurred.length} too small for their place` : '')
        + (got.some((r) => !r.full) ? ' - no choice of widths offered' : ''));
      if (screen.name.startsWith('an iPhone') && (url === '/' || url === '/plans/')) {
        for (const r of got) {
          const stem = r.took.replace(/-(640|960)\.webp$/, '.webp');
          bytesFull += fs.statSync(path.join(IMG, stem)).size;
          bytesTaken += fs.existsSync(path.join(IMG, r.took)) ? fs.statSync(path.join(IMG, r.took)).size : 0;
        }
      }
    }
  }

  console.log('\n== what it saves ==');
  ok(bytesTaken > 0 && bytesTaken < bytesFull * 0.6,
    `on an iPhone the homepage's and the plans page's renderings come to ${kb(bytesTaken)} KB, where the full-size files are ${kb(bytesFull)} KB`);

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
