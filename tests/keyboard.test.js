/*
 * Getting around the site without a mouse or a touch screen.
 *
 * The November 10, 2026 audit (item 14) found three things wrong for someone
 * who uses the keyboard or a screen reader:
 *
 *  - No page offered a way past its header. On every page the Tab key had to
 *    go through the logo, the menu, the phone number and Client Login (nine
 *    stops on the homepage) before it reached the page itself, and again on
 *    the next page.
 *  - The homepage, the thank-you page and the not-found page had no
 *    main-content landmark, which is what a screen reader's "jump to the main
 *    content" key looks for. The other pages had one.
 *  - The contact form showed which field was chosen by turning its 1px
 *    underline pale gold: #c2a67a on white, 2.3:1, where a focus mark needs
 *    3:1 to be seen. The choice chips in the form and in the plan finder drew
 *    their keyboard ring in the same pale gold.
 *
 * So: every page has one <main id="main">, with the page's heading inside it.
 * Every page with a bar starts with a "Skip to main content" link that takes
 * no room until the Tab key reaches it, then shows as a button at the top
 * left, and sends the keyboard into the page. And a chosen field or chip is
 * marked in a colour that stands out from the page (the deeper gold, #866f4f).
 *
 * The focus marks are judged from a photograph of the page, not from the
 * stylesheet, so a mark that is there but too pale, or hidden under something,
 * still fails.
 *   node tests/keyboard.test.js
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const PLANS = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'plans.json'), 'utf8')).models.map((m) => `/plans/${m.slug}.html`);
const PAGES = ['/', '/custom-homes.html', '/semi-custom-homes.html', '/renovations.html', '/privacy.html', '/terms.html',
  '/success.html', '/404.html', '/plans/', ...PLANS];
// A phone and a laptop: the bar is laid out differently on each.
const WIDTHS = [390, 1280];

// WCAG relative luminance and contrast ratio, on [r, g, b].
const lum = ([r, g, b]) => {
  const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
const contrast = (a, b) => { const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x); return (hi + 0.05) / (lo + 0.05); };
const rgbOf = (css) => (css.match(/[\d.]+/g) || []).slice(0, 3).map(Number);

// The pixels of a rectangle of the page, as rows of [r, g, b].
async function pixels(page, clip) {
  const { data, info } = await sharp(await page.screenshot({ clip })).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const rows = [];
  for (let y = 0; y < info.height; y++) {
    const row = [];
    for (let x = 0; x < info.width; x++) { const i = (y * info.width + x) * 3; row.push([data[i], data[i + 1], data[i + 2]]); }
    rows.push(row);
  }
  return rows;
}

// What the page looks like to the keyboard: the landmark, and what comes before it.
const survey = () => {
  const shown = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const mains = [...document.querySelectorAll('main')];
  const main = mains[0];
  const h1 = document.querySelector('h1');
  const stops = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [tabindex]')]
    .filter((el) => el.tabIndex >= 0);
  const before = main ? stops.filter((el) => (main.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_PRECEDING) && !main.contains(el)) : stops;
  const skip = document.querySelector('a[href="#main"]');
  const sr = skip ? skip.getBoundingClientRect() : null;
  return {
    mains: mains.length,
    id: main ? main.id : null,
    h1Inside: !!(main && h1 && main.contains(h1)),
    nested: !!(main && main.parentElement.closest('header, nav, footer, aside, main')),
    stopsBefore: before.filter((el) => el !== skip && shown(el)).length,
    firstStop: stops[0] ? (stops[0].getAttribute('href') || stops[0].tagName) : null,
    skipText: skip ? skip.textContent.replace(/\s+/g, ' ').trim() : null,
    skipHidden: sr ? sr.width <= 1 && sr.height <= 1 : null,
  };
};

(async () => {
  const site = await serveRepo();
  const b = await launch();
  let barPages = 0;

  for (const url of PAGES) {
    console.log(`\n== ${url} ==`);
    for (const w of WIDTHS) {
      const p = await b.newPage({ viewport: { width: w, height: 800 } });
      await serveFonts(p);
      await p.goto(site.base + url, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      const s = await p.evaluate(survey);

      ok(s.mains === 1 && s.id === 'main' && s.h1Inside && !s.nested,
        `${w}px: one main-content landmark, with the page's heading inside it`
        + (s.mains !== 1 ? ` - ${s.mains} <main> elements` : !s.h1Inside ? ' - the heading is outside it' : s.nested ? ' - it sits inside another landmark' : s.id !== 'main' ? ' - it has no id="main"' : ''));

      // A page with a bar puts several stops before its content. One stop (the
      // logo on the thank-you and not-found pages) is nothing worth skipping.
      if (s.stopsBefore <= 1) {
        ok(s.stopsBefore <= 1, `${w}px: nothing to skip (${s.stopsBefore} link before the content)`);
        await p.close();
        continue;
      }
      if (w === WIDTHS[0]) barPages++;

      ok(s.firstStop === '#main' && /^skip to (the )?(main )?content$/i.test(s.skipText || '') && s.skipHidden === true,
        `${w}px: ${s.stopsBefore} stops sit before the content, and the first thing on the page is a "Skip to main content" link that takes no room`
        + (s.firstStop !== '#main' ? ` - the first stop is ${s.firstStop}` : s.skipHidden ? '' : ' - it shows before it is reached'));
      if (s.firstStop !== '#main') { await p.close(); continue; }

      // The Tab key reaches it first, and then it can be seen.
      await p.keyboard.press('Tab');
      const shown = await p.evaluate(() => {
        const el = document.activeElement;
        const r = el.getBoundingClientRect();
        const st = getComputedStyle(el);
        const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return {
          isSkip: el.getAttribute('href') === '#main',
          rect: { x: r.left, y: r.top, width: r.width, height: r.height },
          inView: r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight,
          onTop: top === el,
          color: st.color, background: st.backgroundColor,
        };
      });
      const ratio = contrast(rgbOf(shown.color), rgbOf(shown.background));
      ok(shown.isSkip && shown.inView && shown.onTop && shown.rect.height >= 24 && shown.rect.width >= 100 && ratio >= 4.5,
        `${w}px: the first press of Tab shows it, on top of the page (${Math.round(shown.rect.width)} by ${Math.round(shown.rect.height)}px, ${ratio.toFixed(1)}:1)`
        + (!shown.isSkip ? ' - Tab went somewhere else' : !shown.onTop ? ' - something covers it' : !shown.inView ? ' - it is off the screen' : ''));

      // Enter sends the keyboard into the page: the next Tab lands inside it.
      await p.keyboard.press('Enter');
      await p.waitForFunction(() => location.hash === '#main', null, { timeout: 3000 }).catch(() => {});
      await p.keyboard.press('Tab');
      const after = await p.evaluate(() => {
        const main = document.querySelector('main');
        const el = document.activeElement;
        return { inside: !!(main && el && el !== main && main.contains(el)), what: el ? (el.textContent || el.tagName).replace(/\s+/g, ' ').trim().slice(0, 40) : '' };
      });
      ok(after.inside, `${w}px: Enter moves into the page, and the next Tab lands inside the content ("${after.what}")`);
      await p.close();
    }
  }

  console.log('\n== what was covered ==');
  ok(barPages >= 6 + PLANS.length, `the skip link was tried on every page with a bar (${barPages})`);

  // --- the mark on a chosen field or chip ---
  // Photographed, then compared with the page around it: 3:1 is the least a
  // focus mark may differ from its surroundings (WCAG 1.4.11).
  console.log('\n== a chosen field in the contact form is clearly marked ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.goto(site.base + '/', { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    // Step 2 holds the text fields; it opens once a project and a budget are chosen.
    await p.click('label[for="contact-interest-custom"]');
    await p.click('label[for="contact-budget-250"]');
    await p.click('#contact-continue');
    await p.waitForSelector('#contact-name', { state: 'visible', timeout: 3000 });

    // How many rows of the field's bottom edge stand out from the white of the form.
    const underline = async (id) => {
      const r = await p.locator(id).evaluate((el) => {
        el.scrollIntoView({ block: 'center', behavior: 'instant' });
        const q = el.getBoundingClientRect();
        return { x: q.left, y: q.top, width: q.width, height: q.height };
      });
      const clip = { x: Math.round(r.x) + 4, y: Math.round(r.y + r.height) - 5, width: Math.round(r.width) - 8, height: 10 };
      const rows = await pixels(p, clip);
      const page = rows[0][0];
      return rows.filter((row) => row.filter((px) => contrast(px, page) >= 3).length > row.length * 0.9).length;
    };
    for (const id of ['#contact-name', '#contact-email', '#contact-phone', '#contact-details']) {
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      const resting = await underline(id);
      await p.focus(id);
      await p.waitForTimeout(350);   // the underline's colour eases in
      const chosen = await underline(id);
      ok(chosen >= 2 && chosen > resting, `${id}: when chosen its underline is ${chosen}px of a colour that stands out (${resting}px before)`);
    }
    await p.close();
  }

  console.log('\n== a chip reached with the keyboard is clearly ringed ==');
  for (const url of ['/', '/plans/']) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await serveFonts(p);
    await p.goto(site.base + url, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.keyboard.press('Tab');   // the keyboard is in use, so rings are drawn
    const radios = await p.locator('input[type="radio"]').count();
    const faint = [];
    let ringed = 0;
    for (let i = 0; i < radios; i++) {
      const radio = p.locator('input[type="radio"]').nth(i);
      const box = await radio.evaluate((el) => {
        const chip = el.nextElementSibling;
        if (!chip || chip.getBoundingClientRect().width <= 1) return null;
        el.focus();
        chip.scrollIntoView({ block: 'center', behavior: 'instant' });
        const q = chip.getBoundingClientRect();
        let node = chip.parentElement;
        let page = 'rgba(0, 0, 0, 0)';
        while (node && /rgba\(0, 0, 0, 0\)|transparent/.test(page)) { page = getComputedStyle(node).backgroundColor; node = node.parentElement; }
        return { x: q.left, y: q.top, width: q.width, height: q.height, page, visible: el.matches(':focus-visible'), name: chip.textContent.replace(/\s+/g, ' ').trim().slice(0, 28) };
      });
      if (!box) continue;
      // A strip from 6px outside the chip's left edge to the edge, at mid-height:
      // the ring, if there is one, crosses it.
      const strip = (await pixels(p, { x: Math.round(box.x) - 6, y: Math.round(box.y + box.height / 2), width: 6, height: 1 }))[0];
      const best = Math.max(...strip.map((px) => contrast(px, rgbOf(box.page))));
      if (box.visible && best >= 3) ringed++; else faint.push(`"${box.name}" ${best.toFixed(1)}:1`);
    }
    ok(ringed >= 8 && faint.length === 0, `${url}: all ${ringed} chips show a ring that stands out from the page`
      + (faint.length ? ` - too pale: ${faint.slice(0, 6).join(', ')}${faint.length > 6 ? ` and ${faint.length - 6} more` : ''}` : ''));
    await p.close();
  }

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
