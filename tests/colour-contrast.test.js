/*
 * The gold (#c2a67a) is a colour for navy, not for white. Small gold text on
 * the white and off-white sections ("View plan", "See it in the video", the
 * "all standard features" and Privacy Policy links, the social links, the
 * numbered steps on the service pages) measured 2.3:1 against its background,
 * half the 4.5:1 that small text needs, and read as faint rather than premium.
 * On light backgrounds, gold text is now the deeper #866f4f (4.8:1 on white,
 * 4.5:1 on the #f8f9fa sections); the original gold stays for buttons, rules,
 * marks and anything on navy (October 2026).
 *
 * Two more things the daylight hero photo broke, which this file also guards:
 * the gold line above the headline ("Custom Home Builder Serving ...") ran
 * across the cream siding of the house and its last words vanished, so from
 * lg up it is white and held to two lines over the dark trees; and "Client
 * Login" in the transparent menu bar was gold on pale sky, so it is white
 * until the page scrolls and the bar turns navy.
 *   node tests/colour-contrast.test.js
 */
const { ROOT, launch, serveRepo } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const PAGES = ['index.html', 'custom-homes.html', 'semi-custom-homes.html', 'renovations.html',
  'privacy.html', 'terms.html', 'plans/index.html', 'plans/the-visionary.html'];

// WCAG relative luminance and contrast ratio, on "r g b" or "r, g, b" strings.
const lum = (rgb) => {
  const [r, g, b] = rgb.map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (a, b) => { const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x); return (hi + 0.05) / (lo + 0.05); };

(async () => {
  const b = await launch();
  const site = await serveRepo();

  // Every piece of text coloured any gold, with the solid background behind it
  // (the nearest ancestor painted an opaque colour). Text over the hero photo
  // and the fixed menu bar is judged separately below.
  for (const file of PAGES) {
    console.log(`\n== ${file} ==`);
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await serveFonts(p);
    await p.goto(`${site.base}/${file}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const found = await p.evaluate(() => {
      const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const n = m[1].split(/[\s,\/]+/).map(Number); return n.length === 4 && n[3] === 0 ? null : n.slice(0, 3); };
      const out = [];
      for (const el of document.querySelectorAll('body *')) {
        if (el.closest('#hero, #main-nav, script, style, svg')) continue;
        const text = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ');
        if (!text || el.getAttribute('aria-hidden') === 'true') continue;
        if (!el.getClientRects().length) continue;
        const cs = getComputedStyle(el);
        const color = parse(cs.color);
        if (!color) continue;
        // The two golds, and nothing else: this is about where gold is used.
        const gold = color.join() === '194,166,122' ? 'light' : color.join() === '134,111,79' ? 'deep' : null;
        if (!gold) continue;
        let bg = null;
        for (let a = el; a && !bg; a = a.parentElement) bg = parse(getComputedStyle(a).backgroundColor);
        out.push({ text: text.slice(0, 40), gold, color, bg: bg || [255, 255, 255], size: parseFloat(cs.fontSize), weight: cs.fontWeight });
      }
      return out;
    });
    const faint = found.filter((f) => {
      const large = f.size >= 24 || (f.size >= 18.66 && Number(f.weight) >= 700);
      return !large && contrast(f.color, f.bg) < 4.5;
    });
    ok(found.length > 0, `${file}: has gold text to check (${found.length} pieces)`);
    ok(faint.length === 0, `${file}: no small gold text under 4.5:1 against its background` +
      (faint.length ? ` - ${faint.map((f) => `"${f.text}" ${f.gold} gold on rgb(${f.bg}) = ${contrast(f.color, f.bg).toFixed(2)}`).join('; ')}` : ''));
    // The deep gold belongs on light backgrounds only; on navy it would be the
    // faint one (4:1).
    const deepOnDark = found.filter((f) => f.gold === 'deep' && lum(f.bg) < 0.5);
    ok(deepOnDark.length === 0, `${file}: the deeper gold is not used on dark backgrounds` +
      (deepOnDark.length ? ` - ${deepOnDark.map((f) => `"${f.text}"`).join('; ')}` : ''));
    await p.close();
  }

  // The hero's eyebrow line and Client Login over the daylight photo.
  console.log('\n== index.html hero, over the photo ==');
  for (const width of [1280, 1440, 1920]) {
    const p = await b.newPage({ viewport: { width, height: Math.round(width * 9 / 16) } });
    await serveFonts(p);
    await p.goto(`${site.base}/index.html`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => {
      const eyebrow = document.querySelector('#hero h1').previousElementSibling;
      const range = document.createRange(); range.selectNodeContents(eyebrow);
      const rects = [...range.getClientRects()];
      const lines = new Set(rects.map((b) => Math.round(b.top))).size;
      const login = [...document.querySelectorAll('#main-nav a')].find((a) => /client login/i.test(a.textContent));
      return { color: getComputedStyle(eyebrow).color, right: Math.max(...rects.map((b) => b.right)), lines, login: getComputedStyle(login).color };
    });
    // Left of about 40% of the width is the dark tree line behind the copy on
    // every desktop size; the old single line reached past half the screen.
    ok(/255, 255, 255/.test(r.color) && r.lines <= 2 && r.right < width * 0.4,
      `${width}px: eyebrow is white, on at most two lines, ending over the trees (${r.lines} lines, right edge ${Math.round(r.right)}px, ${r.color})`);
    ok(/255, 255, 255/.test(r.login), `${width}px: Client Login is white while the bar is transparent (${r.login})`);
    await p.evaluate(() => window.scrollTo(0, 400));
    // The link's colour fades over 300ms, so wait for it to settle rather than
    // read it the moment the bar's classes change.
    const loginColor = () => getComputedStyle([...document.querySelectorAll('#main-nav a')].find((a) => /client login/i.test(a.textContent))).color;
    await p.waitForFunction((want) => getComputedStyle([...document.querySelectorAll('#main-nav a')].find((a) => /client login/i.test(a.textContent))).color === want,
      'rgb(194, 166, 122)', { timeout: 3000 }).catch(() => {});
    const scrolled = await p.evaluate(loginColor);
    ok(/194, 166, 122/.test(scrolled), `${width}px: Client Login is gold once the bar turns navy (${scrolled})`);
    await p.close();
  }

  await site.close();
  await b.close();
  console.log(fail === 0 ? '\nAll colour checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
