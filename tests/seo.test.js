/*
 * What search engines are told about the site, beyond the homepage.
 *
 * Until November 2026 the three service pages and /plans/ carried no
 * structured data at all; the plan pages' breadcrumb was the only structured
 * data outside the homepage, and the business itself (name, address, phone)
 * was described to Google on the homepage alone. The homepage menu and footer
 * never linked to the service pages, renovations.html linked to no plan and no
 * other service, and not one town was named anywhere, so a search for a
 * builder in Bel Air or Fallston had nothing to match. The hero always sent
 * the 2560-pixel photograph, to phones included, and Netlify sent no cache or
 * security headers. Each check here guards one of those.
 *
 * Everything is read from the files with jsdom; nothing is rendered, so this
 * runs in a second or two.
 */
const { ROOT } = require('./lib/env');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

const SITE = 'https://buildleavitt.com';
const PAGES = ['index.html', 'custom-homes.html', 'semi-custom-homes.html', 'renovations.html', 'privacy.html', 'terms.html', 'success.html', '404.html',
  ...fs.readdirSync(path.join(ROOT, 'plans')).filter((f) => f.endsWith('.html')).map((f) => 'plans/' + f)];
const SERVICE_PAGES = ['custom-homes.html', 'semi-custom-homes.html', 'renovations.html'];

const docOf = (f) => new JSDOM(fs.readFileSync(path.join(ROOT, f), 'utf8')).window.document;
const urlOf = (f) => SITE + '/' + f.replace(/index\.html$/, '');
const ldOf = (doc) => [...doc.querySelectorAll('script[type="application/ld+json"]')].map((s) => JSON.parse(s.textContent));
const canonicalOf = (doc) => doc.querySelector('link[rel="canonical"]')?.getAttribute('href');
const docs = Object.fromEntries(PAGES.map((f) => [f, docOf(f)]));
const home = ldOf(docs['index.html']).find((j) => j['@type'] === 'GeneralContractor');

// --- every piece of structured data parses ---
console.log('\n== structured data parses on every page ==');
{
  const bad = [];
  let n = 0;
  for (const f of PAGES) {
    docs[f].querySelectorAll('script[type="application/ld+json"]').forEach((s, i) => {
      n++;
      try { JSON.parse(s.textContent); } catch (e) { bad.push(`${f} #${i}: ${e.message}`); }
    });
  }
  ok(bad.length === 0, `all ${n} JSON-LD blocks parse` + (bad.length ? ' - ' + bad.join(' | ') : ''));
  ok(!!home && home['@id'] === `${SITE}/#business`, 'the homepage describes the business with @id ' + SITE + '/#business');
}

// --- breadcrumbs: what the page shows is what the structured data says ---
// A BreadcrumbList is Google's hint for the "Home > Home Plans > The Poet"
// line under a result. It is only safe when it repeats the visible trail, so
// the two are compared item for item, names and addresses.
console.log('\n== every visible breadcrumb has matching BreadcrumbList data ==');
{
  const bad = [];
  let n = 0;
  for (const f of PAGES) {
    const doc = docs[f];
    const nav = doc.querySelector('nav[aria-label="Breadcrumb"]');
    if (!nav) continue;
    n++;
    const shown = [...nav.children].filter((el) => el.getAttribute('aria-hidden') !== 'true').map((el) => ({
      name: el.textContent.replace(/\s+/g, ' ').trim(),
      item: el.tagName === 'A' ? new URL(el.getAttribute('href'), urlOf(f)).href : SITE + canonicalOf(doc)?.replace(SITE, ''),
    }));
    const list = ldOf(doc).find((j) => j['@type'] === 'BreadcrumbList');
    if (!list) { bad.push(`${f}: no BreadcrumbList`); continue; }
    const said = (list.itemListElement || []).map((e) => ({ name: e.name, item: e.item, position: e.position }));
    const same = said.length === shown.length && said.every((e, i) => e.position === i + 1 && e.name === shown[i].name && e.item === shown[i].item);
    if (!same) bad.push(`${f}: page shows ${JSON.stringify(shown)} but data says ${JSON.stringify(said)}`);
  }
  ok(n >= 21 && bad.length === 0, `${n} pages show a breadcrumb and each matches its BreadcrumbList` + (bad.length ? ' - ' + bad.join(' | ') : ''));
}

// --- service pages: the service, and who provides it ---
// Google reads each page on its own, so a page that only pointed at the
// homepage's @id would describe an entity it never defines. Each service page
// carries a compact copy of the business node with the same @id; the copy and
// the homepage must never drift apart.
console.log('\n== each service page describes its service and the business ==');
{
  const bad = [];
  for (const f of SERVICE_PAGES) {
    const doc = docs[f];
    const ld = ldOf(doc);
    const canonical = canonicalOf(doc);
    const service = ld.find((j) => j['@type'] === 'Service');
    const biz = ld.find((j) => j['@type'] === 'GeneralContractor');
    if (!service) bad.push(`${f}: no Service`);
    else {
      if (service.url !== canonical) bad.push(`${f}: Service url ${service.url} is not the canonical ${canonical}`);
      if (service.provider?.['@id'] !== home?.['@id']) bad.push(`${f}: Service provider is ${JSON.stringify(service.provider)}`);
      if (!service.name || !service.serviceType || !service.description || !Array.isArray(service.areaServed)) bad.push(`${f}: Service is missing name, serviceType, description or areaServed`);
      if (service.description !== doc.querySelector('meta[name="description"]')?.getAttribute('content')) bad.push(`${f}: Service description differs from the meta description`);
    }
    if (!biz) bad.push(`${f}: no business node`);
    else {
      for (const k of ['@id', 'name', 'url', 'telephone', 'logo']) if (biz[k] !== home?.[k]) bad.push(`${f}: business ${k} is ${JSON.stringify(biz[k])}, homepage says ${JSON.stringify(home?.[k])}`);
      if (JSON.stringify(biz.address) !== JSON.stringify(home?.address)) bad.push(`${f}: business address differs from the homepage`);
      if (biz.openingHoursSpecification) bad.push(`${f}: the hours are checked on the homepage only; do not repeat them here`);
    }
    const catalog = (home?.hasOfferCatalog?.itemListElement || []).map((o) => o.itemOffered?.['@id']);
    if (service && !catalog.includes(service['@id'])) bad.push(`${f}: the homepage's offer catalog does not list ${service['@id']}`);
  }
  ok(bad.length === 0, 'the three service pages carry a Service (url = canonical, provider = the business) and a business node equal to the homepage\'s' + (bad.length ? ' - ' + bad.join(' | ') : ''));
}

// --- the towns: shown on the page, repeated to Google ---
// The service-area band names the towns in each county; the homepage's
// structured data lists the same towns as City entries. Two hand-written
// copies, so they are compared, like the questions and their FAQPage data.
console.log('\n== the towns on the homepage band are the Cities in areaServed ==');
{
  const items = [...docs['index.html'].querySelectorAll('[data-towns] li')];
  const shown = items.flatMap((li) => {
    const copy = li.cloneNode(true);
    copy.querySelectorAll('strong').forEach((s) => s.remove());
    return copy.textContent.replace(/\s+/g, ' ').trim().split(/,\s*|\s+and\s+/).map((t) => t.trim()).filter(Boolean);
  });
  const cities = (home?.areaServed || []).filter((a) => a['@type'] === 'City').map((a) => a.name);
  const counties = (home?.areaServed || []).filter((a) => a['@type'] === 'AdministrativeArea').map((a) => a.name);
  ok(items.length === 5 && shown.length >= 20, `the band lists ${shown.length} towns under ${items.length} counties`);
  const missing = shown.filter((t) => !cities.includes(`${t}, MD`));
  const extra = cities.filter((c) => !shown.includes(c.replace(/, MD$/, '')));
  ok(missing.length === 0 && extra.length === 0 && cities.length === shown.length,
    `every town on the band is a City in the structured data and nothing else is` + (missing.length ? ' - not in data: ' + missing.join(', ') : '') + (extra.length ? ' - not on page: ' + extra.join(', ') : ''));
  ok(counties.length === 6 && counties[0] === 'Harford County, MD', 'the six counties and regions are still listed as AdministrativeArea');
}

// --- /plans/: the list of plans ---
console.log('\n== /plans/ lists every plan as an ItemList ==');
{
  const { models } = JSON.parse(fs.readFileSync(path.join(ROOT, 'src', 'plans.json'), 'utf8'));
  const list = ldOf(docs['plans/index.html']).find((j) => j['@type'] === 'ItemList');
  const urls = (list?.itemListElement || []).map((e) => e.url);
  const want = models.map((m) => `${SITE}/plans/${m.slug}.html`);
  ok(!!list && list.numberOfItems === models.length && JSON.stringify(urls) === JSON.stringify(want),
    `the ItemList names all ${models.length} plans in order` + (list ? ` (found ${urls.length})` : ' (no ItemList)'));
  ok(urls.every((u) => fs.existsSync(path.join(ROOT, u.replace(SITE + '/', '')))), 'every listed plan page exists');
}

// --- footers link the services ---
// The menu is Kyle's and stays as it is, so the footer is where every page
// links the three service pages: once, the homepage reached them only through
// its three service cards, and no other page reached them at all.
console.log('\n== every footer links the three service pages ==');
{
  const bad = [];
  let n = 0;
  for (const f of PAGES) {
    const footer = docs[f].querySelector('footer');
    if (!footer || !footer.querySelector('a[href]')) continue;
    n++;
    const hrefs = [...footer.querySelectorAll('a[href]')].map((a) => new URL(a.getAttribute('href'), urlOf(f)).pathname);
    const missing = ['/custom-homes.html', '/semi-custom-homes.html', '/renovations.html', '/plans/'].filter((p) => !hrefs.includes(p));
    if (missing.length) bad.push(`${f}: ${missing.join(', ')}`);
    const label = footer.querySelector('nav[aria-label="Footer"]');
    if (!label) bad.push(`${f}: footer links are not in a nav labelled Footer`);
  }
  ok(n >= 23 && bad.length === 0, `all ${n} footers link Custom Homes, Semi-Custom Homes, Renovations and Plans` + (bad.length ? ' - missing on ' + bad.join(' | ') : ''));
}

// --- the hero photograph comes in more than one size ---
// Without srcset every visitor downloaded the 2560-pixel file, 424 KB of WebP,
// on a 390-pixel phone included. Each source now offers several widths, and
// every file it names must exist, or the browser falls back to the <img> src.
console.log('\n== the hero offers several image widths, and each file exists ==');
{
  const hero = docs['index.html'].getElementById('hero');
  const sources = hero ? [...hero.querySelectorAll('picture source, picture img')] : [];
  const bad = [];
  let candidates = 0;
  for (const el of sources) {
    const set = el.getAttribute('srcset');
    if (!set) { bad.push(`${el.tagName} has no srcset`); continue; }
    const parts = set.split(',').map((s) => s.trim().split(/\s+/));
    if (parts.length < 2 || parts.some((p) => !/^\d+w$/.test(p[1] || ''))) bad.push(`${el.tagName} srcset has no width descriptors: ${set}`);
    if (!el.getAttribute('sizes')) bad.push(`${el.tagName} with w descriptors has no sizes`);
    for (const [file] of parts) { candidates++; if (!fs.existsSync(path.join(ROOT, file))) bad.push(`missing file ${file}`); }
  }
  ok(sources.length >= 4 && bad.length === 0, `${sources.length} hero sources offer ${candidates} files, all present` + (bad.length ? ' - ' + bad.join(' | ') : ''));
}

// --- response headers ---
console.log('\n== netlify.toml sets cache and security headers ==');
{
  const toml = fs.readFileSync(path.join(ROOT, 'netlify.toml'), 'utf8');
  const blocks = toml.split('[[headers]]').slice(1).map((b) => ({
    for: b.match(/for\s*=\s*"([^"]+)"/)?.[1],
    values: Object.fromEntries([...b.matchAll(/^\s*([A-Za-z-]+)\s*=\s*"([^"]+)"/gm)].map((m) => [m[1], m[2]]).filter(([k]) => k !== 'for')),
  }));
  const site = blocks.find((b) => b.for === '/*');
  ok(!!site && site.values['X-Content-Type-Options'] === 'nosniff' && !!site.values['Referrer-Policy'] && !!site.values['Permissions-Policy'],
    'every response carries X-Content-Type-Options, Referrer-Policy and Permissions-Policy');
  for (const p of ['/plans/img/*', '/plans/pdf/*', '/media/*']) {
    const b = blocks.find((x) => x.for === p);
    ok(!!b && /^public, max-age=\d+$/.test(b.values['Cache-Control'] || '') && +b.values['Cache-Control'].match(/\d+/)[0] <= 30 * 86400,
      `${p} may be cached (public, max-age of a month or less; the files are replaced in place)`);
  }
  ok(!blocks.some((b) => b.for === '/*' && b.values['Cache-Control']), 'HTML and dist/styles.css keep Netlify\'s default must-revalidate (no site-wide Cache-Control)');

  // The pictures at the top of the site (November 2026, audit item 15). The
  // hero photograph, the logo, Kyle's portrait and the before/after pair sit in
  // the site's root, outside the three cached folders, so they were served
  // "max-age=0, must-revalidate": a returning visitor's browser asked Netlify
  // about each of them again on every page, the logo included, which is on
  // every page. They get the same week as the plan pictures. A week at most
  // and never `immutable`, because a retaken photograph keeps its file name.
  // Netlify's rule for a path (docs.netlify.com, "Custom headers"): `*` matches
  // any characters, anywhere in a path segment; `:name` matches one segment.
  const matcher = (pattern) => new RegExp('^' + pattern.split('*').map((part) =>
    part.split(/(:[A-Za-z_]+)/).map((bit, i) => (i % 2 ? '[^/]+' : bit.replace(/[.+?^${}()|[\]\\]/g, '\\$&'))).join('')).join('.*') + '$');
  const cached = blocks.filter((b) => b.for && b.values['Cache-Control']).map((b) => ({ ...b, re: matcher(b.for) }));
  const lifetime = (p) => cached.filter((b) => b.re.test(p)).map((b) => b.values['Cache-Control']);

  const pictures = new Set();
  for (const f of PAGES) {
    const base = new URL(urlOf(f));
    docs[f].querySelectorAll('img[src], img[srcset], source[srcset], video[poster]').forEach((el) => {
      const refs = [el.getAttribute('src'), el.getAttribute('poster'),
        ...(el.getAttribute('srcset') || '').split(',').map((s) => s.trim().split(/\s+/)[0])].filter(Boolean);
      for (const r of refs) {
        const u = new URL(r, base);
        if (u.origin === base.origin && /\.(jpe?g|png|webp|avif|gif|svg)$/i.test(u.pathname)) pictures.add(u.pathname);
      }
    });
  }
  const list = [...pictures].sort();
  const missing = list.filter((p) => !fs.existsSync(path.join(ROOT, p)));
  ok(list.length > 50 && missing.length === 0, `the pages show ${list.length} pictures, all present` + (missing.length ? ' - missing: ' + missing.join(', ') : ''));
  const uncached = list.filter((p) => lifetime(p).length === 0);
  const atRoot = list.filter((p) => !p.slice(1).includes('/'));
  ok(uncached.length === 0, `every picture the pages show may be kept by the browser (${atRoot.length} of them at the site's root)` +
    (uncached.length ? ' - no cache lifetime: ' + uncached.join(', ') : ''));

  const WEEK = 7 * 86400;
  const wrong = cached.filter((b) => {
    const v = b.values['Cache-Control'];
    const age = /^public, max-age=(\d+)$/.exec(v);
    return !age || +age[1] < 86400 || +age[1] > WEEK;
  }).map((b) => `${b.for}: ${b.values['Cache-Control']}`);
  ok(cached.length >= 4 && wrong.length === 0 && !/immutable/i.test(toml.replace(/^\s*#.*$/gm, '')),
    `all ${cached.length} cache rules are "public", a day to a week, never immutable` + (wrong.length ? ' - ' + wrong.join(' | ') : ''));

  // A pattern written too widely would freeze a page or the stylesheet for a
  // week: an edit merged today would not show to someone who visited yesterday.
  const mustStayFresh = ['/', '/dist/styles.css', '/sitemap.xml', '/robots.txt', '/favicon.png', ...PAGES.map((f) => '/' + f), '/plans/'];
  const frozen = mustStayFresh.filter((p) => lifetime(p).length > 0);
  ok(frozen.length === 0, `no page, stylesheet or sitemap is caught by a cache rule (${mustStayFresh.length} addresses tried)` +
    (frozen.length ? ' - cached: ' + frozen.join(', ') : ''));
}

// --- "build on your lot" is said where a search engine looks first ---
// Kyle wants the site found for "build on your lot" and "custom home builder
// Maryland" (November 10, 2026). The audit that day found the first phrase
// only inside a closed answer and on a form card on the homepage, and once,
// far down, on two service pages: never in a title, a main heading or a
// description, the three places a search engine weighs most. The custom homes
// page now says it in all three, in words Kyle approved. He asked that the
// description keep the other half of the offer too: no lot yet, and Leavitt
// helps find one. The homepage title keeps Harford County, so the county is
// not lost from the titles now that this page's title names Maryland instead.
console.log('\n== the custom homes page says "build on your lot" in its title, heading and description ==');
{
  const doc = docs['custom-homes.html'];
  const title = doc.querySelector('title')?.textContent || '';
  const h1 = (doc.querySelector('h1')?.textContent || '').replace(/\s+/g, ' ').trim();
  const desc = doc.querySelector('meta[name="description"]')?.getAttribute('content') || '';
  ok(/build on your lot/i.test(title) && /custom home builder/i.test(title) && /\bMaryland\b/.test(title),
    `the title says "build on your lot", "custom home builder" and Maryland ("${title}")`);
  ok(/\bon your lot\b/i.test(h1), `the main heading says "on your lot" ("${h1}")`);
  ok(/^build on your lot/i.test(desc) && /\bMaryland\b/.test(desc), `the description opens with "build on your lot" and names Maryland ("${desc}")`);
  ok(/help you find one/i.test(desc), 'the description keeps the other option: Leavitt helps find a lot');
  const homeTitle = docs['index.html'].querySelector('title')?.textContent || '';
  ok(/Harford County/.test(homeTitle), `the homepage title still names Harford County ("${homeTitle}")`);
}

// --- "Maryland" is written out, not left as "MD" ---
// The second phrase Kyle wants the site found for is "custom home builder
// Maryland". The November 2026 audit (item 8) found the state was rarely
// spelled out: four of the five main titles said "MD" or named no place at
// all, the plans page and the seventeen plan pages named no place anywhere
// above the footer's postal address, and the homepage band ended "Southern
// PA". A search engine does not reliably read "MD" as Maryland, and a visitor
// from outside the state may not either. Kyle approved the words on November
// 11, 2026. Harford County stays wherever it was: this adds the state to it.
// The footer's "Forest Hill, MD 21050" is the postal form and stays as it is,
// matching the business listings.
console.log('\n== Maryland is written out in titles, descriptions and on the page ==');
{
  const MAIN_PAGES = ['index.html', ...SERVICE_PAGES, 'plans/index.html'];
  const PLAN_PAGES = PAGES.filter((f) => f.startsWith('plans/') && f !== 'plans/index.html');
  const titleOf = (f) => docs[f].querySelector('title')?.textContent || '';
  const descOf = (f) => docs[f].querySelector('meta[name="description"]')?.getAttribute('content') || '';
  // What a visitor reads in the body of the page: <main> without its scripts.
  const mainText = (f) => {
    const m = docs[f].querySelector('main').cloneNode(true);
    m.querySelectorAll('script, style, noscript').forEach((e) => e.remove());
    return m.textContent.replace(/\s+/g, ' ');
  };

  const noState = MAIN_PAGES.filter((f) => !/\bMaryland\b/.test(titleOf(f)));
  ok(noState.length === 0, `the homepage, the three service pages and /plans/ each name Maryland in the title` +
    (noState.length ? ' - not: ' + noState.map((f) => `${f} ("${titleOf(f)}")`).join(' | ') : ''));
  const abbreviated = [...MAIN_PAGES, ...PLAN_PAGES].filter((f) => /\bMD\b/.test(titleOf(f)) || /\bMD\b/.test(descOf(f)));
  ok(abbreviated.length === 0, 'no title or description abbreviates the state to "MD"' +
    (abbreviated.length ? ' - ' + abbreviated.join(', ') : ''));
  ok(/Harford County/.test(titleOf('index.html')) && /custom home builder/i.test(titleOf('index.html')),
    `the homepage title keeps Harford County and "custom home builder" beside Maryland ("${titleOf('index.html')}")`);

  const descMissing = [...MAIN_PAGES, ...PLAN_PAGES].filter((f) => !/\bMaryland\b/.test(descOf(f)));
  ok(PLAN_PAGES.length >= 17 && descMissing.length === 0,
    `all ${MAIN_PAGES.length + PLAN_PAGES.length} descriptions (main pages and plan pages) name Maryland` +
    (descMissing.length ? ' - not: ' + descMissing.join(', ') : ''));

  const bodyMissing = [...MAIN_PAGES, ...PLAN_PAGES].filter((f) => !/\bMaryland\b/.test(mainText(f)));
  ok(bodyMissing.length === 0, 'every main page and plan page names Maryland in the text a visitor reads' +
    (bodyMissing.length ? ' - not: ' + bodyMissing.join(', ') : ''));

  const noTown = SERVICE_PAGES.filter((f) => !/based in Forest Hill, Maryland/.test(mainText(f)));
  ok(noTown.length === 0, 'each service page says "based in Forest Hill, Maryland"' + (noTown.length ? ' - not: ' + noTown.join(', ') : ''));

  const band = [...docs['index.html'].querySelectorAll('h2')].find((h) => /Greater Baltimore/.test(h.textContent))?.closest('section');
  const bandText = (band?.textContent || '').replace(/\s+/g, ' ');
  ok(!!band && /\bMaryland/.test(band.querySelector('h2').textContent), 'the homepage service-area band names Maryland in its heading');
  ok(/Southern Pennsylvania/.test(bandText) && !/Southern PA\b/.test(bandText), 'the band ends "Southern Pennsylvania", not "Southern PA"');
}

// --- pictures: from this site only, and no bigger than their place needs ---
// Housekeeping from the November 2026 audit (item 17).
//
// Four pictures on the homepage (the logo, Kyle's portrait, Before and After)
// carried an `onerror` left over from the template the site began as: if the
// picture failed to load, the visitor's browser fetched a grey stand-in from
// placehold.co, an outside company, which then learned of the visit and could
// show whatever it liked in the middle of the page. A picture that fails
// should simply show its description.
//
// The logo was one file, 1200 pixels wide, for a place at most 328 wide, on
// every page. It is now offered at 656 as well (twice its largest place), and
// the browser takes the big one only on a screen sharp enough to use it.
// Gold.png keeps its address: the business data names it as the logo.
//
// And for every picture offered in several widths, the width the page states
// must be the file's real width, or the browser chooses wrongly.
const widthChecks = [];
console.log('\n== pictures come from this site, and the logo fits its place ==');
{
  const handlers = [];
  const outside = [];
  const logos = [];
  for (const f of PAGES) {
    const base = new URL(urlOf(f));
    docs[f].querySelectorAll('img, source, video').forEach((el) => {
      if (el.hasAttribute('onerror')) handlers.push(`${f}: ${el.getAttribute('src') || el.tagName}`);
      const refs = [el.getAttribute('src'), el.getAttribute('poster'),
        ...(el.getAttribute('srcset') || '').split(',').map((c) => c.trim())].filter(Boolean);
      for (const ref of refs) {
        const [file, descriptor] = ref.split(/\s+/);
        const u = new URL(file, base);
        if (u.origin !== base.origin) { outside.push(`${f}: ${u.host}`); continue; }
        if (/^\d+w$/.test(descriptor || '')) widthChecks.push({ page: f, file: u.pathname, stated: parseInt(descriptor, 10) });
      }
    });
    const logo = docs[f].querySelector('img[src$="Gold.png"]');
    if (logo) {
      const parts = [...logo.closest('picture').querySelectorAll('source'), logo];
      const good = parts.every((el) => {
        const widths = (el.getAttribute('srcset') || '').split(',').map((c) => parseInt(c.trim().split(/\s+/)[1], 10));
        return widths.length >= 2 && widths.every((n) => n > 0) && Math.min(...widths) <= 700 && !!el.getAttribute('sizes');
      });
      logos.push({ f, good, src: logo.getAttribute('src') });
    }
  }
  ok(handlers.length === 0, 'no picture has an onerror stand-in' + (handlers.length ? ' - ' + handlers.join(', ') : ''));
  ok(outside.length === 0, 'no page shows a picture from another site' + (outside.length ? ' - ' + [...new Set(outside)].join(', ') : ''));
  const big = logos.filter((l) => !l.good).map((l) => l.f);
  ok(logos.length === PAGES.length && big.length === 0,
    `the logo is offered at about twice its place, with the full-size file for sharper screens, on all ${logos.length} pages`
    + (big.length ? ` - only the 1200px file on ${big.length}: ${big.slice(0, 5).join(', ')}${big.length > 5 ? ' ...' : ''}` : ''));
  ok(logos.every((l) => /(^|\/)Gold\.png$/.test(l.src)) && home.logo === `${SITE}/Gold.png` && fs.existsSync(path.join(ROOT, 'Gold.png')),
    'Gold.png keeps its address: every page falls back to it and the business data names it');
}

(async () => {
  console.log('\n== a picture offered in several widths states each file\'s real width ==');
  const sharp = require('sharp');
  const seen = new Map();
  const wrong = [];
  for (const c of widthChecks) {
    const file = path.join(ROOT, c.file);
    if (!fs.existsSync(file)) { wrong.push(`${c.file} is missing`); continue; }
    if (!seen.has(c.file)) seen.set(c.file, (await sharp(file).metadata()).width);
    if (seen.get(c.file) !== c.stated) wrong.push(`${c.file} is ${seen.get(c.file)}px, stated as ${c.stated}w on ${c.page}`);
  }
  ok(seen.size >= 12 && wrong.length === 0, `${seen.size} files, each as wide as its page says` + (wrong.length ? ' - ' + [...new Set(wrong)].slice(0, 6).join(' | ') : ''));

  console.log(fail === 0 ? '\nAll checks passed.' : `\n${fail} check(s) failed.`);
  process.exit(fail ? 1 : 0);
})();
