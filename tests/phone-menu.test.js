/*
 * Away from the homepage, a phone gets the same menu the homepage has.
 *
 * Until November 2026 the bar on the service pages, the plans page and the
 * seventeen plan pages showed a phone two things, "Plans" and "Get a Quote".
 * Services, About, Process and Client Login could be reached only by scrolling
 * to the footer or going back to the homepage (the November 10, 2026 audit,
 * item 12). The homepage had a menu button; these 21 pages had none.
 *
 * Kyle approved this on November 13, 2026, from a picture: on a phone a menu
 * button takes the place of the word "Plans"; "Get a Quote" and the "Call"
 * line stay where they were; the menu holds the homepage phone menu's six
 * entries, same words, same order. Tablets and desktops are unchanged, and so
 * are privacy.html and terms.html, by his choice.
 *
 * The menu is a <details>, like the questions on the homepage, so it opens
 * with no script at all. Script only adds the ways people expect to close one:
 * the Escape key, a tap anywhere else, and coming back to the page with the
 * Back button.
 *
 *   node tests/phone-menu.test.js
 */
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');
const fs = require('fs');
const path = require('path');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const MAIN = ['/custom-homes.html', '/semi-custom-homes.html', '/renovations.html', '/plans/'];
const PLANS = fs.readdirSync(path.join(ROOT, 'plans')).filter((f) => f.endsWith('.html') && f !== 'index.html').sort().map((f) => '/plans/' + f);
// Where each entry must lead from a page that is not the homepage.
const TARGETS = {
  Services: '/#services', Plans: '/plans/', About: '/#about', Process: '/#process',
  'Client Login': 'https://connect.buildleavitt.com', 'Get a Quote': '/#contact',
};

// Everything the checks need to know about the bar, read in the page.
const read = () => {
  const header = document.querySelector('header');
  const box = (el) => el.getBoundingClientRect();
  // checkVisibility, not size alone: a closed <details> keeps its contents laid
  // out but not drawn, so they still report a width and a height.
  const shown = (el) => !!el && box(el).width > 0 && box(el).height > 0 && el.checkVisibility({ checkVisibilityCSS: true });
  const menu = header.querySelector('details');
  const summary = menu && menu.querySelector('summary');
  const entries = menu ? [...menu.querySelectorAll('a')] : [];
  const bar = [...header.querySelectorAll('a')].filter((a) => !menu || !menu.contains(a));
  const text = (a) => a.textContent.replace(/\s+/g, ' ').trim();
  return {
    hasMenu: !!menu,
    button: shown(summary) ? { w: Math.round(box(summary).width), h: Math.round(box(summary).height), name: summary.getAttribute('aria-label') || text(summary) } : null,
    open: !!menu && menu.open,
    entries: entries.filter(shown).map((a) => ({
      text: text(a), href: a.getAttribute('href'), h: Math.round(box(a).height),
      inside: box(a).left >= 0 && box(a).right <= innerWidth + 1,
      belowBar: box(a).top >= box(summary).bottom,
    })),
    barLinks: bar.filter(shown).map(text),
    logo: Math.round(box(header.querySelector('a img')).width),
    sideways: document.documentElement.scrollWidth > innerWidth,
  };
};

(async () => {
  const site = await serveRepo();
  const b = await launch();
  const open = async (url, w, extra = {}) => {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, ...extra });
    const p = await ctx.newPage();
    await serveFonts(p);
    await p.goto(site.base + url, { waitUntil: 'load' });
    if (extra.javaScriptEnabled !== false) await p.evaluate(() => document.fonts.ready);
    return p;
  };
  const SUMMARY = 'header details > summary';

  // The words and their order come from the homepage's own phone menu, so the
  // two cannot drift apart: change one and this fails until the other matches.
  console.log('\n== the homepage phone menu, which the others must repeat ==');
  const home = await open('/', 390);
  const HOME = await home.evaluate(() => ({
    labels: [...document.querySelectorAll('#mobile-menu a')].map((a) => a.textContent.replace(/\s+/g, ' ').trim()),
    ids: ['services', 'about', 'process', 'contact'].filter((id) => document.getElementById(id)),
  }));
  ok(HOME.labels.length === 6, `the homepage phone menu has six entries (${HOME.labels.join(', ')})`);
  ok(HOME.ids.length === 4, `the homepage still has the sections the menu leads to (${HOME.ids.join(', ')})`);
  ok(HOME.labels.every((l) => l in TARGETS), 'every entry has a known destination from the other pages');
  await home.context().close();

  // The four main pages and one plan page at three phone widths; the other
  // sixteen plan pages, which share that page's generated header, at one.
  const runs = [
    ...[...MAIN, PLANS[0]].flatMap((u) => [320, 360, 390].map((w) => [u, w])),
    ...PLANS.slice(1).map((u) => [u, 390]),
  ];
  console.log(`\n== on a phone: a menu button, and behind it the homepage's six entries (${MAIN.length + PLANS.length} pages) ==`);
  for (const [url, w] of runs) {
    const p = await open(url, w);
    const closed = await p.evaluate(read);
    if (!closed.hasMenu || !closed.button) {
      ok(false, `${url} ${w}px: there is a menu button in the bar (${JSON.stringify(closed.barLinks)})`);
      await p.context().close();
      continue;
    }
    await p.click(SUMMARY);
    const opened = await p.evaluate(read);
    await p.click(SUMMARY);
    const again = await p.evaluate(read);

    const wrong = [];
    if (closed.button.w < 44 || closed.button.h < 44) wrong.push(`the button is ${closed.button.w}x${closed.button.h}, under 44x44`);
    if (!closed.button.name) wrong.push('the button has no name for a screen reader');
    if (closed.open || closed.entries.length) wrong.push('the menu is open before it is tapped');
    if (!closed.barLinks.includes('Get a Quote')) wrong.push('"Get a Quote" is not in the bar');
    if (!closed.barLinks.some((t) => /^Call \(443\) 613-9750$/.test(t))) wrong.push('the "Call" line is gone');
    if (closed.barLinks.includes('Plans')) wrong.push('"Plans" is still in the bar beside the menu button');
    if (!opened.open) wrong.push('a tap does not open it');
    if (opened.entries.map((e) => e.text).join('|') !== HOME.labels.join('|')) wrong.push(`entries are "${opened.entries.map((e) => e.text).join(', ')}"`);
    const badHref = opened.entries.filter((e) => TARGETS[e.text] !== e.href).map((e) => `${e.text} -> ${e.href}`);
    if (badHref.length) wrong.push(`wrong destinations: ${badHref.join(', ')}`);
    if (opened.entries.some((e) => !e.inside)) wrong.push('an entry runs off the side of the screen');
    if (opened.entries.some((e) => !e.belowBar)) wrong.push('the open menu covers the bar');
    if (opened.entries.some((e) => e.h < 27)) wrong.push(`an entry is under 27px tall (${opened.entries.map((e) => e.h).join(',')})`);
    if (closed.sideways || opened.sideways) wrong.push('the page scrolls sideways');
    if (again.open || again.entries.length) wrong.push('a second tap does not close it');
    ok(wrong.length === 0, `${url} ${w}px: menu button, six entries, opens and closes` + (wrong.length ? ' - ' + wrong.join('; ') : ''));
    await p.context().close();
  }

  // Script is only a convenience here. With it switched off the menu must
  // still open and show every entry.
  console.log('\n== with script switched off the menu still opens ==');
  for (const url of [MAIN[0], PLANS[0]]) {
    const p = await open(url, 390, { javaScriptEnabled: false });
    const has = await p.locator(SUMMARY).count();
    if (has) await p.click(SUMMARY);
    const shown = has ? await p.locator('header details a').evaluateAll((as) => as.filter((a) => a.getBoundingClientRect().height > 0 && a.checkVisibility({ checkVisibilityCSS: true })).length) : 0;
    ok(shown === 6, `${url}: all six entries show after a tap, without script (${shown})`);
    await p.context().close();
  }

  console.log('\n== with script: Escape, a tap elsewhere and the Back button close it ==');
  for (const url of [MAIN[0], PLANS[0]]) {
    const p = await open(url, 390);
    const isOpen = () => p.evaluate(() => { const d = document.querySelector('header details'); return !!d && d.open; });
    if (!(await p.locator(SUMMARY).count())) { ok(false, `${url}: there is a menu to close`); await p.context().close(); continue; }
    await p.click(SUMMARY);
    await p.keyboard.press('Escape');
    const afterEscape = await isOpen();
    const focusBack = await p.evaluate(() => document.activeElement && document.activeElement.tagName === 'SUMMARY');
    await p.click(SUMMARY);
    await p.mouse.click(195, 760); // well below the open menu
    const afterOutside = await isOpen();
    // Back button: a phone keeps the page as it was left and shows it again,
    // open menu and all. This test browser reloads the page instead, which
    // would pass with no script, so the page is told it is being shown again
    // from that cache, which is what a phone does.
    await p.click(SUMMARY);
    await p.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true })));
    const afterBack = await isOpen();
    ok(!afterEscape && focusBack, `${url}: Escape closes the menu and returns to the button`);
    ok(!afterOutside, `${url}: a tap outside the menu closes it`);
    ok(!afterBack, `${url}: it is closed when the page is shown again by the Back button`);
    await p.context().close();
  }

  // From tablet width up nothing changed: no menu button, "Plans" in the bar.
  console.log('\n== tablets and desktops keep the bar they had ==');
  for (const url of [MAIN[0], MAIN[3], PLANS[0]]) {
    for (const w of [768, 1280]) {
      const p = await open(url, w);
      const r = await p.evaluate(read);
      ok(!r.button && r.entries.length === 0 && r.barLinks.includes('Plans') && r.barLinks.includes('Get a Quote') && r.barLinks.includes('Client Login'),
        `${url} ${w}px: no menu button; Plans, Get a Quote and Client Login in the bar (${r.barLinks.join(', ')})`);
      await p.context().close();
    }
  }

  await b.close();
  await site.close();
  console.log(fail === 0 ? '\nAll phone-menu checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
