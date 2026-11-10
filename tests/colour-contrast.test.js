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
 *
 * And the licence numbers (November 2026). "MHBR 9796 | MHIC 161316 | PAHIC
 * 212160" closes every page, and it was the faintest text on the site: grey
 * #6b7280 on the navy footer, 3.7:1 where small text needs 4.5:1. The licence
 * line under the hero copy was 10px on phones and 11px on desktop. For a
 * builder these numbers are a reason to trust the company, so they have to be
 * readable: the footer line is now the footer's own grey (7:1), and the hero
 * line is 12px, a shade lighter where it lies over the photograph.
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

  // The licence numbers at the foot of every page, including the two pages
  // that have no footer proper (the thank-you page and the 404).
  console.log('\n== the licence numbers can be read ==');
  const LICENCES = 'MHBR 9796 | MHIC 161316 | PAHIC 212160';
  for (const file of [...PAGES, 'success.html', '404.html']) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await serveFonts(p);
    await p.goto(`${site.base}/${file}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const found = await p.evaluate((want) => {
      const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const n = m[1].split(/[\s,\/]+/).map(Number); return n.length === 4 && n[3] === 0 ? null : n.slice(0, 3); };
      return [...document.querySelectorAll('body *')]
        .filter((el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.replace(/\s+/g, ' ').includes(want)))
        .map((el) => {
          const cs = getComputedStyle(el);
          let bg = null;
          for (let a = el; a && !bg; a = a.parentElement) bg = parse(getComputedStyle(a).backgroundColor);
          return { color: parse(cs.color), bg: bg || [255, 255, 255], size: parseFloat(cs.fontSize) };
        });
    }, LICENCES);
    const line = found[0];
    const ratio = line ? contrast(line.color, line.bg) : 0;
    ok(found.length === 1 && ratio >= 4.5 && line.size >= 12,
      `${file}: the licence line is at least 4.5:1 and 12px` +
      (line ? ` (${ratio.toFixed(2)}:1, ${line.size}px, rgb(${line.color}) on rgb(${line.bg}))` : ` (found ${found.length})`));
    await p.close();
  }

  // The licence line under the hero copy: on phones it is on the navy below the
  // banner, on desktop it lies over the lawn of the photograph. Judged against
  // what is really behind it: the words are hidden, their box photographed, and
  // the text colour compared with the brightest hundredth of those pixels.
  console.log('\n== index.html hero, the licence line ==');
  const sharp = require('sharp');
  for (const [width, height] of [[390, 844], [768, 1024], [1024, 768], [1440, 900], [1920, 1080]]) {
    const p = await b.newPage({ viewport: { width, height } });
    await serveFonts(p);
    await p.goto(`${site.base}/index.html`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => { const i = document.querySelector('#hero img'); return i.complete && i.naturalWidth > 0; });
    const r = await p.evaluate(() => {
      const row = [...document.querySelectorAll('#hero span')].find((s) => /MHBR 9796/.test(s.textContent)).parentElement;
      const cs = getComputedStyle(row);
      const color = cs.color.match(/[\d.]+/g).slice(0, 3).map(Number);
      const size = parseFloat(cs.fontSize);
      const boxes = [...row.children].map((c) => c.getBoundingClientRect());
      row.style.color = 'transparent';
      const x = Math.min(...boxes.map((q) => q.left)), y = Math.min(...boxes.map((q) => q.top));
      return { color, size, words: row.textContent.replace(/\s+/g, ' ').trim(),
        clip: { x: Math.floor(x), y: Math.ceil(y), width: Math.ceil(Math.max(...boxes.map((q) => q.right)) - x), height: Math.floor(Math.max(...boxes.map((q) => q.bottom)) - y) } };
    });
    const { data } = await sharp(await p.screenshot({ clip: r.clip })).removeAlpha().raw().toBuffer({ resolveWithObject: true });
    const behind = [];
    for (let i = 0; i < data.length; i += 3) behind.push(lum([data[i], data[i + 1], data[i + 2]]));
    behind.sort((x, y) => x - y);
    const bright = behind[Math.floor(behind.length * 0.99)];
    const ratio = (Math.max(lum(r.color), bright) + 0.05) / (Math.min(lum(r.color), bright) + 0.05);
    ok(/Licensed in MD & PA/.test(r.words) && /MHBR 9796/.test(r.words) && r.size >= 12 && ratio >= 4.5,
      `${width}x${height}: the hero licence line is at least 12px and 4.5:1 against what is behind it (${r.size}px, ${ratio.toFixed(2)}:1)`);
    await p.close();
  }

  await site.close();
  await b.close();
  console.log(fail === 0 ? '\nAll colour checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
