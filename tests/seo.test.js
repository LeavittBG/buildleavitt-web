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
}

console.log(fail === 0 ? '\nAll checks passed.' : `\n${fail} check(s) failed.`);
process.exit(fail ? 1 : 0);
