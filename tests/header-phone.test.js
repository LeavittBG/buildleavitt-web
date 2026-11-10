/*
 * The phone number is at the top of every page, and a tap on it calls.
 *
 * Until November 2026 no page's header carried the number. The homepage showed
 * it in the hero and lost it once the page scrolled; on the service pages, the
 * plans page and every plan page, the first number a visitor on a phone could
 * tap was at the very bottom, after everything else (the November 10, 2026
 * audit). A builder's site lives on calls, so the number now sits in the bar
 * at the top of every page that has one:
 *
 *   homepage, desktop      on the right, after the fine rule, above Client Login
 *   homepage, below lg     a call button beside the menu button (the bar is
 *                          fixed, so it stays as the page scrolls); the number
 *                          is written out beside the icon from tablet width
 *   every other page       beside Client Login from tablet width up; on phones
 *                          a line of its own under the bar, "Call (443) ..."
 *
 * At each width exactly one of those shows. It must name the number, be big
 * enough to tap, stay on one line, and never squeeze the logo or push the bar
 * off the screen. success.html and 404.html have no bar; their number is
 * already on the first screen.
 *   node tests/header-phone.test.js
 */
const { launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const TEL = 'tel:+14436139750';
const NUMBER = '(443) 613-9750';
const PAGES = ['/', '/custom-homes.html', '/semi-custom-homes.html', '/renovations.html',
  '/plans/', '/plans/the-poet.html', '/privacy.html', '/terms.html'];
// 320 is the narrowest phone still in use; 768 and 1024 are where the layouts change.
const WIDTHS = [320, 360, 390, 768, 1024, 1280, 1440];

const measure = (tel) => {
  const bar = document.querySelector('#main-nav') || document.querySelector('header');
  const shown = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
  const links = [...bar.querySelectorAll(`a[href="${tel}"]`)].filter(shown);
  const a = links[0];
  const logo = bar.querySelector('img').getBoundingClientRect();
  const out = { count: links.length, logoW: Math.round(logo.width), overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, fixed: getComputedStyle(bar).position === 'fixed' };
  if (!a) return out;
  const r = a.getBoundingClientRect();
  // The words a visitor reads, and the words a screen reader is given.
  const text = [...a.querySelectorAll('*')].filter((e) => !e.children.length && e.tagName !== 'svg' && !e.closest('svg') && shown(e)).map((e) => e.textContent).join(' ')
    + ' ' + [...a.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ');
  // Lines of text, from the text itself: the icon beside it is not a line.
  const tops = new Set();
  const walk = document.createTreeWalker(a, NodeFilter.SHOW_TEXT);
  for (let n = walk.nextNode(); n; n = walk.nextNode()) {
    if (!n.textContent.trim()) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    for (const b of range.getClientRects()) if (b.width > 0 && b.height > 0) tops.add(Math.round(b.top));
  }
  const lines = tops.size;
  return { ...out, left: Math.round(r.left), right: Math.round(r.right), top: Math.round(r.top), bottom: Math.round(r.bottom), w: Math.round(r.width), h: Math.round(r.height),
    text: text.replace(/\s+/g, ' ').trim(), name: (a.getAttribute('aria-label') || text).replace(/\s+/g, ' ').trim(), lines, color: getComputedStyle(a).color };
};

(async () => {
  const site = await serveRepo();
  const b = await launch();

  for (const path of PAGES) {
    console.log(`\n== ${path} ==`);
    const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
    await serveFonts(p);
    await p.goto(site.base + path, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    for (const w of WIDTHS) {
      await p.setViewportSize({ width: w, height: 800 });
      await p.evaluate(() => window.scrollTo(0, 0));
      const r = await p.evaluate(measure, TEL);
      const at = `${w}px`;
      ok(r.count === 1, `${at}: the bar at the top shows the phone number once (${r.count})`);
      if (r.count !== 1) continue;
      ok(r.name.includes(NUMBER), `${at}: the link names the number ("${r.name}")`);
      const iconOnly = !r.text.includes(NUMBER);
      ok(iconOnly ? r.w >= 44 && r.h >= 44 : r.h >= 24, `${at}: big enough to tap (${r.w}x${r.h}${iconOnly ? ', icon only' : ''})`);
      ok(iconOnly || r.lines === 1, `${at}: the number stays on one line (${r.lines})`);
      ok(r.left >= 0 && r.right <= w && r.overflow <= 0, `${at}: inside the screen, with no sideways scroll (${r.left}-${r.right}, overflow ${r.overflow}px)`);
      ok(r.top >= 0 && r.bottom <= 200, `${at}: at the top of the page (${r.top}-${r.bottom}px)`);
      // The wordmark is 4.1 times as wide as it is tall; under about 125px its
      // second line cannot be read. The number must not be paid for with the logo.
      // (Away from the homepage the logo was already down to 90px on a 320px
      // screen, beside Plans and Get a Quote, before the number arrived; there
      // the check is only that it has not lost any more.)
      const room = path !== '/' && w < 360 ? 90 : 125;
      ok(r.logoW >= room, `${at}: the logo keeps its room (${r.logoW}px wide, at least ${room})`);
      if (path === '/') {
        // The homepage bar is fixed: the number is still there, and still white
        // on the bar's navy, once the hero has scrolled away.
        ok(r.fixed && /255, 255, 255/.test(r.color), `${at}: white over the hero photo (${r.color})`);
        await p.evaluate(() => window.scrollTo(0, 1600));
        await p.waitForFunction(() => window.scrollY >= 1500, null, { timeout: 5000 }).catch(() => {});
        await p.waitForFunction(() => !document.getElementById('main-nav').classList.contains('bg-transparent'), null, { timeout: 3000 }).catch(() => {});
        const s = await p.evaluate(measure, TEL);
        ok(s.count === 1 && s.top >= 0 && s.bottom <= 120 && /255, 255, 255/.test(s.color),
          `${at}: still at the top, and white, after scrolling (${s.count} shown, ${s.top}-${s.bottom}px, ${s.color})`);
      } else if (w < 768) {
        // On a phone the number has a line to itself: a full-width target.
        ok(r.h >= 40 && r.w >= w * 0.9, `${at}: on phones it is a full-width line under the bar (${r.w}x${r.h})`);
      }
    }
    await p.close();
  }

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
