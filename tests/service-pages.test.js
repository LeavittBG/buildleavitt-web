/*
 * The three service pages: custom-homes.html, semi-custom-homes.html and
 * renovations.html (October 2026). Before them, each service was a two-
 * paragraph pop-up on the homepage, filled in by script, so a search for
 * "custom home builder Harford County" had only the homepage to land on and the
 * service cards did nothing without JavaScript. Each page must render on its
 * own, be reachable from its homepage card, and hand the visitor to the contact
 * form with "Project Interest" already chosen.
 *   node tests/service-pages.test.js
 */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const PAGES = [
  ['custom-homes.html', 'Custom Home Build'],
  ['semi-custom-homes.html', 'Semi-Custom Home'],
  ['renovations.html', 'Large-Scale Renovation'],
];

(async () => {
  console.log('\n== static checks ==');
  const home = new JSDOM(fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')).window.document;
  const sitemap = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  for (const [file, interest] of PAGES) {
    const d = new JSDOM(fs.readFileSync(path.join(ROOT, file), 'utf8')).window.document;
    ok(d.querySelectorAll('h1').length === 1, `${file}: exactly one <h1>`);
    ok(d.querySelector('link[rel=canonical]')?.href === `https://buildleavitt.com/${file}`, `${file}: canonical names itself`);
    ok(!d.querySelector('meta[name=robots]'), `${file}: is indexable`);
    ok(sitemap.includes(`<loc>https://buildleavitt.com/${file}</loc>`), `${file}: listed in sitemap.xml`);
    // The homepage card for this service links here, and the page's call to
    // action goes back to the contact form with the matching interest chosen.
    ok(!!home.querySelector(`.service-card[href="/${file}"]`), `${file}: a homepage service card links to it`);
    const cta = [...d.querySelectorAll('a[href^="/?interest="]')];
    const chosen = cta.map((a) => decodeURIComponent(new URL(a.href, 'https://buildleavitt.com').searchParams.get('interest')));
    ok(cta.length > 0 && chosen.every((c) => c === interest) && cta.every((a) => a.getAttribute('href').endsWith('#contact')),
       `${file}: its call to action opens the contact form with "${interest}" chosen (${[...new Set(chosen)].join(', ') || 'none'})`);
    const option = [...home.querySelectorAll('#contact-interest option')].some((o) => o.textContent.trim() === interest);
    ok(option, `${file}: "${interest}" is one of the form's Project Interest options`);
    // Every root-relative asset and page it points at exists.
    const refs = [...d.querySelectorAll('img[src], source[srcset], link[rel=stylesheet][href], a[href^="/"]')]
      .map((e) => (e.getAttribute('src') || e.getAttribute('srcset') || e.getAttribute('href')).split(/[?#]/)[0])
      .filter((u) => u && u.startsWith('/'));
    const missing = [...new Set(refs)].filter((u) => !fs.existsSync(path.join(ROOT, u.endsWith('/') ? u + 'index.html' : u.slice(1))));
    ok(missing.length === 0, `${file}: every local link and asset resolves` + (missing.length ? ' - missing: ' + missing.join(', ') : ''));
    // No claims Kyle has not confirmed (see CLAUDE.md "Removed claims").
    const text = d.body.textContent;
    ok(!/dedicated project manager|warranty package|premier architects|3D render/i.test(text), `${file}: none of the unconfirmed claims`);
  }

  // ------------------------------------------------------------------ browser
  const b = await launch();
  const site = await serveRepo();

  for (const [file] of PAGES) {
    console.log(`\n== ${file} in the browser ==`);
    for (const width of [390, 768, 1280]) {
      const p = await b.newPage({ viewport: { width, height: 900 } });
      await serveFonts(p);
      await p.route(/^https?:\/\/(?!127\.0\.0\.1)(?!localhost)(?!fonts\.(googleapis|gstatic)\.com)/, (r) => r.abort());
      const errs = []; p.on('pageerror', (e) => errs.push(e.message));
      await p.goto(`${site.base}/${file}`, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      const r = await p.evaluate(() => ({
        styled: getComputedStyle(document.body).backgroundColor === 'rgb(252, 252, 252)',
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        year: document.getElementById('year')?.textContent,
        logo: document.querySelector('header img')?.naturalWidth > 0,
        // Every link and button is at least 24px tall, the size a fingertip needs.
        small: [...document.querySelectorAll('a, button')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 24; }).map((e) => e.textContent.trim().slice(0, 30)),
      }));
      ok(errs.length === 0, `${width}px: no JS errors` + (errs.length ? ': ' + errs.join(' | ') : ''));
      ok(r.styled, `${width}px: stylesheet applied`);
      ok(r.overflow <= 0, `${width}px: no horizontal scroll (${r.overflow}px)`);
      ok(r.year === String(new Date().getFullYear()) && r.logo, `${width}px: footer year and logo render`);
      ok(r.small.length === 0, `${width}px: every link and button is at least 24px tall` + (r.small.length ? ' - small: ' + r.small.join(', ') : ''));
      if (width === 1280) await p.screenshot({ path: `${OUT}/shot-${file.replace('.html', '')}.png`, fullPage: true });
      await p.close();
    }
  }

  console.log('\n== the hand-off to the contact form ==');
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await p.route(/^https?:\/\/(?!127\.0\.0\.1)(?!localhost)/, (r) => r.abort());
    // From the homepage card, through the page, to the form.
    await p.goto(`${site.base}/`, { waitUntil: 'load' });
    await p.locator('.service-card').nth(2).click();
    await p.waitForURL(/renovations\.html$/);
    ok(p.url().endsWith('/renovations.html'), 'the third homepage card opens renovations.html');
    await p.locator('a[href^="/?interest="]').first().click();
    await p.waitForURL(/#contact$/);
    await p.waitForTimeout(300);
    const r = await p.evaluate(() => ({
      interest: document.getElementById('contact-interest').value,
      plan: document.getElementById('contact-plan').value,
      note: document.getElementById('contact-plan-note').classList.contains('hidden'),
    }));
    ok(r.interest === 'Large-Scale Renovation', `the form opens with "Large-Scale Renovation" chosen (got "${r.interest}")`);
    ok(r.plan === '' && r.note, 'and no plan is named, since none was chosen');
    // A value that is not one of the options is ignored, never written anywhere.
    await p.goto(`${site.base}/?interest=${encodeURIComponent('<script>alert(1)</script>')}#contact`, { waitUntil: 'load' });
    const bad = await p.evaluate(() => document.getElementById('contact-interest').value);
    ok(bad === '', `an interest that is not an option leaves the form untouched (got "${bad}")`);
    // Both parameters together, as a plan page could send them.
    await p.goto(`${site.base}/?plan=The%20Poet&interest=Semi-Custom%20Home#contact`, { waitUntil: 'load' });
    const both = await p.evaluate(() => ({ interest: document.getElementById('contact-interest').value, plan: document.getElementById('contact-plan').value }));
    ok(both.interest === 'Semi-Custom Home' && both.plan === 'The Poet', `plan and interest work together (${JSON.stringify(both)})`);
    await p.close();
  }

  await site.close();
  await b.close();
  console.log(fail === 0 ? '\nAll service-page checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
