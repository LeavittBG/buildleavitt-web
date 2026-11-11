/*
 * No text on the site is smaller than 12px.
 *
 * The November 10, 2026 audit (item 13) found text at 9, 10 and 11px in about
 * 150 places: the line under Kyle's name on his photograph (9px on a phone),
 * the Before and After labels on the slider (10px on a phone), "Building
 * Group" in the homepage footer (10px), and at 11px every "Read More", "View
 * plan" and "Start with this plan", the questions in the plan finder, the
 * labels over the contact form's fields, the small headings on the plan pages
 * and the "Services" label in every footer. Most of it is capital letters
 * spaced wide apart, which is the hardest kind of text to read small, and much
 * of it is what a visitor is meant to tap.
 *
 * 12px is the floor: the size the licence line was raised to the same week
 * (colour-contrast.test.js holds that line to it).
 *
 * This reads the size the browser actually gives every piece of text, on every
 * page, at a phone and a laptop width, whether or not it is showing: step 2 of
 * the form, the closed answers and the phone menu are all words someone will
 * read. The four process pop-ups are opened as well, because script writes
 * their words. A size set any other way than a class (a <small>, a <sup>, a
 * style attribute) is caught the same.
 *   node tests/text-size.test.js
 */
const fs = require('fs');
const path = require('path');
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const MIN = 12;
const WIDTHS = [390, 1280];
const PLANS = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'plans.json'), 'utf8')).models.map((m) => `/plans/${m.slug}.html`);
const PAGES = ['/', '/custom-homes.html', '/semi-custom-homes.html', '/renovations.html', '/privacy.html', '/terms.html',
  '/success.html', '/404.html', '/plans/', ...PLANS];

// Every run of words on the page with the size it is drawn at.
const measure = (min) => {
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE']);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const small = new Map();
  let count = 0;
  let least = Infinity;
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const words = node.nodeValue.replace(/\s+/g, ' ').trim();
    const el = node.parentElement;
    if (!words || !el || skip.has(el.tagName) || el.closest('noscript, script, style, template')) continue;
    const size = parseFloat(getComputedStyle(el).fontSize);
    count++;
    least = Math.min(least, size);
    if (size < min - 0.01) {
      const key = `${size}px "${words.slice(0, 28)}"`;
      small.set(key, (small.get(key) || 0) + 1);
    }
  }
  return { count, least, small: [...small].map(([k, n]) => (n > 1 ? `${k} x${n}` : k)) };
};

(async () => {
  const site = await serveRepo();
  const b = await launch();
  let popups = 0;
  let total = 0;

  for (const url of PAGES) {
    console.log(`\n== ${url} ==`);
    for (const w of WIDTHS) {
      const p = await b.newPage({ viewport: { width: w, height: 800 } });
      await serveFonts(p);
      await p.goto(site.base + url, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      const r = await p.evaluate(measure, MIN);
      total += r.count;
      ok(r.count > 3 && r.small.length === 0,
        `${w}px: all ${r.count} pieces of text are at least ${MIN}px (the smallest is ${r.least}px)`
        + (r.small.length ? ` - ${r.small.length} smaller: ${r.small.slice(0, 8).join(', ')}${r.small.length > 8 ? ' ...' : ''}` : ''));

      // The process steps open a pop-up whose words are written by script.
      const steps = await p.locator('.process-card[data-step]').count();
      for (let i = 0; i < steps; i++) {
        await p.locator('.process-card[data-step]').nth(i).click();
        await p.waitForFunction(() => !document.getElementById('process-modal').classList.contains('hidden'), null, { timeout: 3000 });
        const m = await p.evaluate((min) => {
          const out = [];
          let n = 0;
          document.querySelectorAll('#process-modal *').forEach((el) => {
            if (![...el.childNodes].some((c) => c.nodeType === 3 && c.nodeValue.trim())) return;
            n++;
            const size = parseFloat(getComputedStyle(el).fontSize);
            if (size < min - 0.01) out.push(`${size}px "${el.textContent.trim().slice(0, 24)}"`);
          });
          return { n, out };
        }, MIN);
        popups++;
        ok(m.n > 2 && m.out.length === 0, `${w}px: process pop-up ${i + 1} has no text under ${MIN}px (${m.n} pieces)` + (m.out.length ? ' - ' + m.out.join(', ') : ''));
        await p.click('#close-process-modal');
        await p.waitForFunction(() => document.getElementById('process-modal').classList.contains('hidden'), null, { timeout: 3000 });
      }
      await p.close();
    }
  }

  console.log('\n== what was covered ==');
  ok(PLANS.length >= 17 && total > 5000, `every page was read at both widths (${PAGES.length} pages, ${total} pieces of text)`);
  ok(popups === 8, `the four process pop-ups were opened at both widths (${popups})`);

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
