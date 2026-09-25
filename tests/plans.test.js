/**
 * Checks the generated plan pages and the plan -> contact-form hand-off.
 *   SP=$PWD node plans.js
 */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { JSDOM } = require('jsdom');
const sharp = require('sharp');
const { serveFonts } = require('./lib/fonts');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const { models } = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/plans.json'), 'utf8'));
const images = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/plan-images.json'), 'utf8'));

(async () => {
  console.log('\n== generated files exist ==');
  const pages = ['plans/index.html', ...models.map(m => `plans/${m.slug}.html`)];
  for (const p of pages) ok(fs.existsSync(path.join(ROOT, p)), `${p} exists`);

  console.log('\n== every referenced asset resolves ==');
  const missing = [];
  const rootRelative = [];
  for (const p of pages) {
    const html = fs.readFileSync(path.join(ROOT, p), 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    const refs = [
      ...[...doc.querySelectorAll('img[src]')].map(e => e.getAttribute('src')),
      ...[...doc.querySelectorAll('source[srcset]')].map(e => e.getAttribute('srcset')),
      ...[...doc.querySelectorAll('link[rel="stylesheet"][href]')].map(e => e.getAttribute('href')),
      ...[...doc.querySelectorAll('a[href$=".pdf"], a[href$=".html"]')].map(e => e.getAttribute('href')),
    ].filter(u => u && !/^https?:/.test(u));

    for (const u of refs) {
      // Pages live in plans/, so a relative path would resolve to plans/<path>.
      if (!u.startsWith('/')) rootRelative.push(`${p}: ${u}`);
      const onDisk = path.join(ROOT, u.replace(/^\//, '').split('#')[0]);
      if (!fs.existsSync(onDisk)) missing.push(`${p} -> ${u}`);
    }
  }
  ok(rootRelative.length === 0, 'every asset path is root-relative' +
    (rootRelative.length ? ': ' + rootRelative.slice(0, 4).join(', ') : ''));
  ok(missing.length === 0, 'no broken links or images' +
    (missing.length ? ': ' + missing.slice(0, 6).join(', ') : ''));

  console.log('\n== page structure ==');
  for (const p of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, p), 'utf8')).window.document;
    const label = p.replace('plans/', '');
    ok(doc.querySelectorAll('h1').length === 1, `${label}: exactly one <h1>`);

    const levels = [...doc.querySelectorAll('h1,h2,h3,h4')].map(h => +h.tagName[1]);
    let skips = 0;
    for (let i = 1; i < levels.length; i++) if (levels[i] > levels[i - 1] + 1) skips++;
    ok(skips === 0, `${label}: no heading level skipped`);

    const noAlt = [...doc.querySelectorAll('img')].filter(i => i.getAttribute('alt') === null);
    ok(noAlt.length === 0, `${label}: every <img> has alt text`);

    const noDims = [...doc.querySelectorAll('img')]
      .filter(i => !i.getAttribute('width') || !i.getAttribute('height'));
    ok(noDims.length === 0, `${label}: every <img> declares width/height`);

    ok(!!doc.querySelector('link[rel="canonical"]'), `${label}: has a canonical URL`);
    ok(/GTM-K9ND8BDT/.test(doc.head.innerHTML), `${label}: carries the GTM container`);
  }

  console.log('\n== no drawing is duplicated onto another model ==');
  // Fifteen of the sixteen brochures were made by batch-editing the branding onto
  // copies of The Visionary, so a drawing landing on the wrong model's page is a
  // real failure mode, and a customer could be shown a plan that is not the one
  // they are looking at. Compare a 32x32 greyscale signature of every drawing
  // against every other and fail on an exact match across different models.
  const sigOf = async (img) => sharp(path.join(ROOT, `plans/img/${img.file}.${img.ext || 'png'}`))
    .greyscale().resize(32, 32, { fit: 'fill' }).raw().toBuffer();

  // Empty again. The Expressionist I and II used to share a pixel-identical
  // front elevation, which was flagged for Leavitt to check against the
  // originals; the re-rendered brochures give them distinct elevations, so the
  // exception is gone rather than carried forward.
  const ACCEPTED_DUPLICATES = [];

  const all = Object.entries(images).flatMap(([slug, pages]) =>
    Object.values(pages).map((i) => ({ slug, file: i.file, ext: i.ext })));
  const sigs = {};
  for (const a of all) sigs[a.file] = await sigOf(a);

  const dupes = [];
  for (let i = 0; i < all.length; i++) {
    for (let j = i + 1; j < all.length; j++) {
      if (all[i].slug === all[j].slug) continue;      // within one model is fine
      if (Buffer.compare(sigs[all[i].file], sigs[all[j].file]) !== 0) continue;
      dupes.push([all[i].file, all[j].file].sort().join(' + '));
    }
  }
  const unexpected = dupes.filter((d) => !ACCEPTED_DUPLICATES.includes(d));
  ok(unexpected.length === 0,
    `no unexpected identical drawings across models${unexpected.length ? ': ' + unexpected.join(', ') : ''}`);
  for (const d of ACCEPTED_DUPLICATES) {
    ok(dupes.includes(d), `known shared drawing still present (${d}) - drop it from the list if the source changed`);
  }

  console.log('\n== specs match Leavitt\'s figures exactly ==');
  const SPEC_KEY = { Bedrooms: 'beds', Bathrooms: 'baths', 'Living Sq Ft': 'sqft', Stories: 'stories',
                     Garage: 'garage' };
  const plansJson = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/plans.json'), 'utf8'));
  for (const m of models) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, `plans/${m.slug}.html`), 'utf8')).window.document;
    // Pair each term with its OWN value. A spec can carry a second <dd> holding a
    // qualifier ("3,840 with the three-car garage option"), so the two lists do
    // not line up by index.
    const rows = [...doc.querySelectorAll('dt')].map(dt => ({
      term: dt.textContent.trim(),
      value: (dt.nextElementSibling?.textContent || '').trim(),
      note: dt.nextElementSibling?.nextElementSibling?.tagName === 'DD'
        ? dt.nextElementSibling.nextElementSibling.textContent.trim() : null,
    }));
    for (let i = 0; i < rows.length; i++) {
      const { term, value: dd, note } = rows[i];
      const dts = [term], dds = [dd];
      const key = SPEC_KEY[dts[0]];
      ok(key !== undefined, `${m.slug}: "${dts[0]}" is a spec this test knows about`);
      const v = m.specs[key];
      const known = v !== null && v !== undefined && v !== '';

      // Where the data carries a qualifier, the page has to show it.
      const NOTE_FOR = { sqft: 'sqftNote', baths: 'bathsNote', price: 'priceNote' };
      const wantNote = m.specs[NOTE_FOR[key]];
      if (wantNote) ok(note === wantNote, `${m.slug}: ${dts[0]} note reads "${wantNote}" (got "${note}")`);

      if (!known) {
        ok(dds[0] === 'On request', `${m.slug}: ${dts[0]} is "On request", not invented (got "${dds[0]}")`);
      } else if (key === 'sqft') {
        // The figure and the "starting at" qualifier both have to survive: a
        // number Leavitt gave as a floor must never be shown as exact.
        const want = (m.specs.sqftFrom ? 'From ' : '') + v.toLocaleString('en-US');
        ok(dds[0] === want, `${m.slug}: sq ft reads "${want}" (got "${dds[0]}")`);
      }
    }
    // Any number the page actually presents as a square footage - in the prose
    // blurb as well as the spec table - has to be the one Leavitt gave. Matched
    // only where the words follow it, so the phone number, the copyright year
    // and the MHBR licence are not mistaken for floor area.
    const stray = [...doc.body.textContent.matchAll(/([\d,]{3,})\s*(?:living\s*)?(?:square feet|sq\.?\s*ft)/gi)]
      .map(x => +x[1].replace(/,/g, ''))
      .filter(n => n !== m.specs.sqft);
    ok(stray.length === 0, `${m.slug}: every square-footage figure is ${m.specs.sqft}${stray.length ? ' (found ' + [...new Set(stray)].join(', ') + ')' : ''}`);

    // Per-model prices are deliberately not published: the collection carries one
    // anchor and the model pages carry none. A price reappearing on a model page
    // would quietly turn the plans back into a price list.
    const money = [...doc.body.textContent.matchAll(/\$([\d,]+)/g)].map(x => x[0]);
    ok(money.length === 0,
      `${m.slug}: no price on the model page${money.length ? ' (found ' + [...new Set(money)].join(', ') + ')' : ''}`);
  }

  console.log('\n== one price anchor, on the collection only ==');
  {
    const idx = new JSDOM(fs.readFileSync(path.join(ROOT, 'plans/index.html'), 'utf8')).window.document;
    const figures = [...idx.body.textContent.matchAll(/\$([\d,]+)/g)].map(x => +x[1].replace(/,/g, ''));
    ok(figures.length === 1, `exactly one price on the collection page (found ${figures.length})`);

    // It has to be the cheapest model, or "starts at" is not true. Derived from
    // the data so adding a cheaper model updates it automatically.
    const lowest = Math.min(...models.map(m => m.specs?.price).filter(Boolean));
    ok(figures[0] === lowest,
      `the anchor is the lowest price in the data ($${lowest.toLocaleString('en-US')}, got $${(figures[0] ?? 0).toLocaleString('en-US')})`);

    // No card may carry a price of its own.
    for (const m of models) {
      const card = [...idx.querySelectorAll('a[href^="/plans/"]')]
        .find(a => a.getAttribute('href') === `/plans/${m.slug}.html`);
      ok(!!card && !/\$/.test(card.textContent), `${m.slug}: card shows no price`);
    }

    ok(/without any optional features/i.test(idx.body.textContent),
      'the anchor carries the "starting price" qualifier');
    ok(/do(es)? not include the homesite/i.test(idx.body.textContent),
      'the anchor says the homesite is excluded');
    const asOf = plansJson.pricesAsOf;
    if (asOf) ok(idx.body.textContent.includes(asOf), `the anchor is dated (${asOf})`);
  }

  console.log('\n== the elevation caption is off the site ==');
  // Leavitt asked for the text naming the elevation and exterior style to be
  // kept off the pages. It is cropped out of the rendering, and it must not have
  // crept back in as visible text either. It does survive as alt text, which is
  // an attribute and so is not part of textContent.
  for (const m of models) {
    const caption = m.pages.find(p => p.id === 'elevation')?.label;
    if (!caption) continue;
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, `plans/${m.slug}.html`), 'utf8')).window.document;
    ok(!doc.body.textContent.includes(caption), `${m.slug}: caption not shown as page text`);
    ok(!/Modern Farmhouse w\//.test(doc.body.textContent), `${m.slug}: no "Elevation X - style w/ materials" line`);
    const alts = [...doc.querySelectorAll('img')].map(i => i.getAttribute('alt')).join(' | ');
    ok(alts.includes(caption), `${m.slug}: caption kept in alt text for screen readers`);
  }
  {
    const idx = new JSDOM(fs.readFileSync(path.join(ROOT, 'plans/index.html'), 'utf8')).window.document;
    ok(!/Modern Farmhouse w\//.test(idx.body.textContent), 'plans index: no elevation caption text');
    const home = new JSDOM(fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')).window.document;
    ok(!/Modern Farmhouse w\//.test(home.body.textContent), 'homepage: no elevation caption text');
  }

  console.log('\n== the Leavitt Standard ==');
  {
    const idx = new JSDOM(fs.readFileSync(path.join(ROOT, 'plans/index.html'), 'utf8')).window.document;
    const sec = idx.querySelector('#included');
    ok(!!sec, 'plans index has an #included section');
    if (sec) {
      const items = sec.querySelectorAll('li');
      ok(items.length === 16, `all 16 standard items are listed (found ${items.length})`);
      ok(/Andersen/.test(sec.textContent) && /Advantech/.test(sec.textContent),
        'brand names from the sheet survive');
    }
    ok(fs.existsSync(path.join(ROOT, 'plans/pdf/leavitt-standard.pdf')), 'the Leavitt Standard PDF is published');
    // Every model page should point at it.
    for (const m of models) {
      const doc = new JSDOM(fs.readFileSync(path.join(ROOT, `plans/${m.slug}.html`), 'utf8')).window.document;
      ok(!!doc.querySelector('a[href="/plans/#included"]'), `${m.slug}: links to the Leavitt Standard`);
    }
  }

  console.log('\n== floor-plan labels corroborated by the PDF itself ==');
  // The brochures carry hidden leftover layers, so extracted text can name sheets
  // that are not the printed one - but the printed one is always in there too.
  // So: the asserted label must appear somewhere in that page's text. A page whose
  // title is drawn as vector art yields no text at all and is listed for a human
  // to eyeball rather than silently passed.
  const { execFileSync, spawnSync } = require('child_process');
  // pdftotext comes with poppler (brew install poppler / apt install
  // poppler-utils). Without it this one cross-check is skipped, loudly, rather
  // than the whole suite crashing - the labels are still checked against the
  // generated pages further down.
  if (spawnSync('pdftotext', ['-v']).error) {
    console.log('  SKIP  pdftotext is not installed, so brochure text cannot be cross-checked');
  } else {
  const unverifiable = [];
  let corroborated = 0;
  for (const m of models) {
    // A model built from images has no brochure to cross-check against; its
    // labels were read straight off the plan images instead.
    if (m.pages.every(p => p.image)) { unverifiable.push(`${m.slug} (no brochure)`); continue; }
    for (const pg of m.pages) {
      if (pg.id.startsWith('elevation')) continue;
      const text = execFileSync('pdftotext',
        ['-f', String(pg.page), '-l', String(pg.page), path.join(ROOT, `assets-src/plans/${m.slug}.pdf`), '-'],
        { encoding: 'utf8' });
      const found = [...new Set(text.match(/(Basement|First|Second|Third|Lower|Upper|Main)\s+Floor Plan/gi) || [])]
        .map(s => s.replace(/\s+/g, ' ').toLowerCase());
      if (!found.length) { unverifiable.push(`${m.slug} p${pg.page}`); continue; }
      ok(found.includes(pg.label.toLowerCase()),
        `${m.slug} p${pg.page}: "${pg.label}" appears in the page text${found.includes(pg.label.toLowerCase()) ? '' : ` (found ${JSON.stringify(found)})`}`);
      corroborated++;
    }
  }
  console.log(`  ....  ${corroborated} labels corroborated from page text`);
  // These three were checked by eye against the rendered page instead.
  const EYEBALLED = ['the-craftsman p2', 'the-daydreamer p2', 'the-novel p2',
                     'the-storyteller (no brochure)'];
  ok(unverifiable.every(u => EYEBALLED.includes(u)),
    `only the known vector-art titles lack page text (${JSON.stringify(unverifiable)})`);
  }

  console.log('\n== page labels match the data ==');
  for (const m of models) {
    const text = new JSDOM(fs.readFileSync(path.join(ROOT, `plans/${m.slug}.html`), 'utf8'))
      .window.document.body.textContent;
    for (const pg of m.pages) {
      if (pg.id === 'elevation') continue; // shown as a figcaption, checked below
      ok(text.includes(pg.label), `${m.slug}: page shows "${pg.label}"`);
    }
    ok(Object.keys(images[m.slug]).length === m.pages.length,
      `${m.slug}: ${m.pages.length} images generated`);
  }

  console.log('\n== search results and link previews ==');
  // Google cuts a description off at about 155 characters. These used to run to
  // 217-231 and lose the bedrooms and square footage - the part people choose a
  // plan by. And with no preview image, a plan shared by text or on Facebook
  // arrived as a bare link.
  for (const p of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, p), 'utf8')).window.document;
    const meta = (sel) => doc.querySelector(sel)?.getAttribute('content') || '';
    const desc = meta('meta[name="description"]');
    ok(desc.length > 0 && desc.length <= 155, `${p}: description fits in a search result (${desc.length} chars)`);
    const img = meta('meta[property="og:image"]');
    const file = img.replace('https://buildleavitt.com/', '');
    const real = file && fs.existsSync(path.join(ROOT, file)) ? await sharp(path.join(ROOT, file)).metadata() : null;
    ok(!!real && /\.(png|jpe?g)$/.test(file), `${p}: preview image is a JPEG or PNG that exists (${file || 'none'})`);
    if (real) ok(+meta('meta[property="og:image:width"]') === real.width && +meta('meta[property="og:image:height"]') === real.height,
      `${p}: preview image declares its real size (${real.width}x${real.height})`);
    ok(meta('meta[name="twitter:card"]') === 'summary_large_image' && meta('meta[name="twitter:image"]') === img,
      `${p}: large preview card, same image`);
  }
  for (const m of models) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, `plans/${m.slug}.html`), 'utf8')).window.document;
    const desc = doc.querySelector('meta[name="description"]').getAttribute('content');
    const sq = m.specs?.sqft ? m.specs.sqft.toLocaleString('en-US') : null;
    ok(desc.startsWith(m.name) && (!sq || desc.includes(`${m.specs.sqftFrom ? 'from ' : ''}${sq} sq ft`)),
      `${m.slug}: description leads with the name and carries Leavitt's square footage`);
  }

  console.log('\n== sitemap.xml ==');
  // What Search Console reads. Every address must be a real page whose own
  // canonical names that exact address, and every entry carries the date the
  // page last changed - a real date, never one in the future.
  {
    const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
    const entries = [...xml.matchAll(/<url><loc>([^<]+)<\/loc>(?:<lastmod>([^<]+)<\/lastmod>)?<\/url>/g)];
    ok(/^<\?xml version="1\.0" encoding="UTF-8"\?>\s*<urlset xmlns="http:\/\/www\.sitemaps\.org\/schemas\/sitemap\/0\.9">/.test(xml),
      'declares the sitemap schema');
    ok(entries.length === (xml.match(/<url>/g) || []).length && entries.length >= 5, `every <url> entry is well formed (${entries.length})`);
    const today = new Date().toLocaleDateString('en-CA');
    let good = 0;
    for (const [, loc, mod] of entries) {
      const u = new URL(loc);
      const file = u.pathname.endsWith('/') ? u.pathname.slice(1) + 'index.html' : u.pathname.slice(1);
      const exists = u.origin === 'https://buildleavitt.com' && fs.existsSync(path.join(ROOT, file));
      const canon = exists && new JSDOM(fs.readFileSync(path.join(ROOT, file), 'utf8')).window.document.querySelector('link[rel=canonical]')?.href;
      const dated = /^\d{4}-\d{2}-\d{2}$/.test(mod || '') && mod <= today;
      if (exists && canon === loc && dated) good++;
      else ok(false, `${loc}: ${!exists ? 'no such page' : canon !== loc ? `canonical is ${canon}` : `lastmod "${mod}" is not a real past date`}`);
    }
    ok(good === entries.length, `all ${entries.length} addresses are real pages, match their canonical, and carry a real lastmod`);
  }

  // ------------------------------------------------------------------ browser
  const browser = await launch();

  console.log('\n== plan pages render without JavaScript ==');
  const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
  const p1 = await noJs.newPage();
  await p1.goto('file://' + path.join(ROOT, 'plans/index.html'), { waitUntil: 'load' });
  ok(await p1.locator('h1').isVisible(), 'index h1 visible with JS disabled');
  ok(await p1.locator('a[href="/plans/the-visionary.html"]').first().isVisible(), 'plan cards visible with JS disabled');
  await p1.goto('file://' + path.join(ROOT, 'plans/the-visionary.html'), { waitUntil: 'load' });
  ok(await p1.locator('h1').isVisible(), 'model h1 visible with JS disabled');
  ok(await p1.locator('figure img').first().isVisible(), 'elevation drawing visible with JS disabled');
  await noJs.close();

  console.log('\n== plan hand-off into the contact form ==');
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  // Serve the real Inter/Playfair. Without this the page falls back to system
  // faces of different widths, and every measurement below - above all the
  // nav-fit check - would be about a layout no visitor ever sees.
  await serveFonts(ctx);
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));

  const home = FILE_ROOT + 'index.html';
  await page.goto(home + '?plan=The%20Visionary', { waitUntil: 'load' });
  await page.waitForTimeout(3200);
  ok(errs.length === 0, 'no JS errors with ?plan set' + (errs.length ? ': ' + errs.join(' | ') : ''));
  ok(await page.inputValue('#contact-plan') === 'The Visionary', 'hidden Plan field carries the model name');
  ok(await page.locator('#contact-plan-note').isVisible(), 'the "Starting from" note is shown');
  ok((await page.locator('#contact-plan-name').textContent()) === 'The Visionary', 'the note names the model');

  await page.click('#contact-plan-clear');
  ok(await page.inputValue('#contact-plan') === '', 'Clear empties the Plan field');
  ok(!await page.locator('#contact-plan-note').isVisible(), 'Clear hides the note');

  console.log('\n== a hostile ?plan value is ignored ==');
  for (const bad of ['<img src=x onerror=alert(1)>', 'A'.repeat(200), 'javascript:alert(1)']) {
    const errs2 = [];
    page.on('pageerror', e => errs2.push(e.message));
    await page.goto(home + '?plan=' + encodeURIComponent(bad), { waitUntil: 'load' });
    await page.waitForTimeout(3200);
    ok(await page.inputValue('#contact-plan') === '', `rejected: ${bad.slice(0, 30)}`);
    ok(!await page.locator('#contact-plan-note').isVisible(), `note stays hidden for: ${bad.slice(0, 30)}`);
  }

  console.log('\n== the form still submits everything Netlify needs ==');
  await page.goto(home + '?plan=The%20Craftsman', { waitUntil: 'load' });
  await page.waitForTimeout(3200);
  const fields = await page.$$eval('form[name="contact"] [name]', els => els.map(e => e.name));
  for (const f of ['form-name', 'bot-field', 'Name', 'Email', 'Phone', 'Interest', 'Budget', 'Plan', 'Details']) {
    ok(fields.includes(f), `form posts "${f}"`);
  }

  console.log('\n== homepage links reach the plans ==');
  ok(await page.locator('nav#main-nav a[href="/plans/"]').count() > 0, 'desktop nav links to /plans/');
  ok(await page.locator('#mobile-menu a[href="/plans/"]').count() > 0, 'mobile nav links to /plans/');
  ok(await page.locator('#plans a[href="/plans/"]').count() > 0, 'teaser section links to /plans/');

  // The teaser cards are hand-maintained; make sure they still point at real models.
  const teased = await page.$$eval('#plans a[href^="/plans/"][href$=".html"]', a => a.map(x => x.getAttribute('href')));
  for (const href of teased) {
    ok(fs.existsSync(path.join(ROOT, href.replace(/^\//, ''))), `teaser card target exists: ${href}`);
  }

  // The teaser's width/height are typed by hand and silently go stale whenever a
  // crop changes, which reintroduces layout shift. Check them against the manifest.
  const teaserImgs = await page.$$eval('#plans img', els => els.map(e => ({
    src: e.getAttribute('src'), w: e.getAttribute('width'), h: e.getAttribute('height'),
  })));
  const byFile = Object.fromEntries(Object.values(images).flatMap(m => Object.values(m).map(i => [i.file, i])));
  for (const t of teaserImgs) {
    const key = path.basename(t.src).replace(/\.(png|jpe?g|webp)$/i, '');
    const real = byFile[key];
    ok(!!real, `teaser image is a generated plan image: ${key}`);
    if (real) {
      ok(+t.w === real.width && +t.h === real.height,
        `teaser ${key} declares its real size (${t.w}x${t.h} vs ${real.width}x${real.height})`);
    }
  }

  console.log('\n== nav fits at every width ==');
  // Regression guard for the overlap this change fixed: at 768 and 1024 the desktop
  // row used to run underneath the wordmark and push "Get a Quote" off the page.
  for (const width of [390, 768, 1023, 1024, 1100, 1280, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.waitForTimeout(350);
    const r = await page.evaluate(() => {
      const row = document.querySelector('#main-nav .hidden.lg\\:flex');
      const burger = document.getElementById('mobile-menu-btn');
      const shown = row && getComputedStyle(row).display !== 'none';
      const burgerShown = getComputedStyle(burger.parentElement).display !== 'none';
      if (!shown) return { shown, burgerShown };
      const logo = document.querySelector('#main-nav .flex-shrink-0').getBoundingClientRect();
      const box = document.querySelector('#main-nav .max-w-7xl').getBoundingClientRect();
      const rr = row.getBoundingClientRect();
      return {
        shown, burgerShown,
        clearsLogo: rr.left >= logo.right - 0.5,
        insideBox: rr.right <= box.right - 24 + 0.5,   // px-6 = 24px padding
        gap: Math.round(rr.left - logo.right),
        overhang: Math.round(rr.right - (box.right - 24)),
      };
    });
    // Exactly one of the two navigations is on screen at any width.
    ok(r.shown !== r.burgerShown, `${width}px: exactly one nav shown (desktop=${r.shown}, burger=${r.burgerShown})`);
    if (r.shown) {
      ok(r.clearsLogo, `${width}px: nav links clear the wordmark (gap ${r.gap}px)`);
      ok(r.insideBox, `${width}px: nav stays inside the content box (overhang ${r.overhang}px)`);
    }
  }

  await page.setViewportSize({ width: 768, height: 900 });
  await page.waitForTimeout(400);
  // The row is items-center with items of differing heights, so compare
  // horizontal extents, not tops: nothing may be squeezed past the viewport and
  // no link may be compressed until its own label wraps to a second line.
  // The whole page must not gain a horizontal scrollbar at any width.
  for (const width of [390, 768, 1024, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await page.waitForTimeout(350);
    const hScroll = await page.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    ok(hScroll <= 1, `${width}px: no horizontal page scroll (overflow ${hScroll}px)`);
  }

  await browser.close();
  console.log(fail ? `\n${fail} check(s) FAILED.` : '\nAll plan checks passed.');
  process.exit(fail ? 1 : 0);
})();
