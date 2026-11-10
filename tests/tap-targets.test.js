/*
 * Every link and button is tall enough for a fingertip, on every page.
 *
 * The November 10, 2026 audit measured the small text links on a phone and
 * found them 16 to 20px tall: the breadcrumbs, "All plans", "Open full size"
 * and the phone number on all seventeen plan pages, the Leavitt Standard
 * download on /plans/, "Read the transcript" and the links inside the answers
 * on the homepage, the phone number on the 404 page, and the email, phone and
 * policy links on the two legal pages. A thumb lands on a neighbour of a target
 * that small, or misses it. 24px is the least a touch target may be (WCAG 2.2,
 * 2.5.8), and until now only the three service pages were held to it
 * (service-pages.test.js), so nothing stopped a 16px link on any other page.
 *
 * This measures every link, button and <summary> a visitor can see, on every
 * page, at two phone widths, a tablet upright and on its side, and a laptop,
 * in three states: as the page loads, with every closed <details> opened (the
 * homepage's answers and the video transcript hide links until they are
 * tapped), and with the phone menu open. The two wide sizes are there because
 * a tablet on its side and a touch-screen laptop get the homepage's desktop
 * menu, whose four links (Services, Plans, About, Process) were 20px tall.
 * The first version of this check stopped at 768px and left them, the menu
 * being Kyle's call; he approved raising them the same day. They gained
 * height and nothing else: the bar looks exactly as it did.
 *
 * A link inside a sentence gets its height from padding on the inline box,
 * which makes the target taller without moving the lines around it. Text is
 * drawn a pixel differently from one machine to the next, so each fix leaves
 * at least 3px to spare over the 24 this asks for.
 *   node tests/tap-targets.test.js
 */
const fs = require('fs');
const path = require('path');
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const MIN = 24;
// Two phones, a tablet upright (768) and on its side (1024), and a laptop:
// 1024 and up is where the homepage shows its desktop menu.
const WIDTHS = [360, 390, 768, 1024, 1280];
const PLANS = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'plans.json'), 'utf8')).models.map((m) => `/plans/${m.slug}.html`);
const PAGES = ['/', '/custom-homes.html', '/semi-custom-homes.html', '/renovations.html', '/privacy.html', '/terms.html',
  '/success.html', '/404.html', '/plans/', ...PLANS];

// Every link, button and <summary> on show, and the ones under the minimum.
const measure = (min) => {
  const small = new Set();
  let count = 0;
  let least = Infinity;
  for (const el of document.querySelectorAll('a, button, summary')) {
    const r = el.getBoundingClientRect();
    // Not drawn at all, or 1px by 1px for screen readers only: nothing to tap.
    if (r.width <= 1 || r.height <= 1 || getComputedStyle(el).visibility === 'hidden') continue;
    count++;
    least = Math.min(least, r.height);
    if (r.height < min) {
      const name = (el.textContent.replace(/\s+/g, ' ').trim() || el.getAttribute('aria-label') || el.tagName).slice(0, 32);
      small.add(`"${name}" ${Math.round(r.height * 10) / 10}px`);
    }
  }
  return { count, least: Math.round(least * 10) / 10, small: [...small] };
};

(async () => {
  const site = await serveRepo();
  const b = await launch();
  let pagesWithDetails = 0;
  let menusOpened = 0;

  for (const url of PAGES) {
    console.log(`\n== ${url} ==`);
    const p = await b.newPage({ viewport: { width: 390, height: 800 } });
    await serveFonts(p);
    await p.goto(site.base + url, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);

    for (const w of WIDTHS) {
      await p.setViewportSize({ width: w, height: 800 });
      const report = (state, r) => ok(r.count > 0 && r.small.length === 0,
        `${w}px, ${state}: all ${r.count} links and buttons are at least ${MIN}px tall (the shortest is ${r.least}px)`
        + (r.small.length ? ' - too small: ' + r.small.slice(0, 12).join(', ') : ''));

      report('as loaded', await p.evaluate(measure, MIN));

      // The answers and the transcript: closed until tapped, with links inside.
      const details = await p.evaluate(() => {
        const all = [...document.querySelectorAll('details')];
        all.forEach((d) => { d.open = true; });
        return all.length;
      });
      if (details) {
        if (w === WIDTHS[0]) pagesWithDetails++;
        report(`with all ${details} closed sections opened`, await p.evaluate(measure, MIN));
        await p.evaluate(() => document.querySelectorAll('details').forEach((d) => { d.open = false; }));
      }

      // The phone menu, where the page has one and this width shows its button.
      const menu = p.locator('#mobile-menu-btn');
      if (await menu.count() && await menu.isVisible()) {
        await menu.click();
        await p.waitForFunction(() => document.getElementById('mobile-menu-btn').getAttribute('aria-expanded') === 'true', null, { timeout: 3000 });
        menusOpened++;
        report('with the phone menu open', await p.evaluate(measure, MIN));
        await menu.click();
        await p.waitForFunction(() => document.getElementById('mobile-menu-btn').getAttribute('aria-expanded') === 'false', null, { timeout: 3000 });
      }
    }
    await p.close();
  }

  // The check is only worth something if it really looked where the small links
  // were hiding: every plan page, the opened answers, the open menu.
  console.log('\n== what was covered ==');
  ok(PLANS.length >= 17, `every plan page was measured (${PLANS.length})`);
  ok(pagesWithDetails >= 1, `the closed sections were opened and measured (${pagesWithDetails} page)`);
  ok(menusOpened >= 3, `the phone menu was opened and measured (${menusOpened} times)`);

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
