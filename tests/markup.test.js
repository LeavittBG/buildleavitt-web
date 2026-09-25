const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const path = require('path');
const fs = require('fs');
const { JSDOM } = require('jsdom');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

for (const file of ['index.html', 'success.html']) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const dom = new JSDOM(html);
  const d = dom.window.document;
  console.log('\n== ' + file + ' ==');

  // JSON-LD parses
  d.querySelectorAll('script[type="application/ld+json"]').forEach((s, i) => {
    try { const j = JSON.parse(s.textContent); ok(true, `JSON-LD #${i} parses (@type=${j['@type']})`); }
    catch (e) { ok(false, `JSON-LD #${i} parse error: ${e.message}`); }
  });

  // every referenced local asset exists
  const refs = new Set();
  d.querySelectorAll('img[src], link[href]').forEach(el => {
    const v = el.getAttribute('src') || el.getAttribute('href');
    if (v && !/^(data:|https?:|mailto:|tel:|#|\/\/)/.test(v)) refs.add(v.replace(/^\//, ''));
  });
  for (const r of refs) ok(fs.existsSync(path.join(ROOT, r)), `asset exists: ${r}`);

  // images have dimensions
  const imgs = [...d.querySelectorAll('img')].filter(i => i.id !== 'lightbox-img');
  const noDim = imgs.filter(i => !i.getAttribute('width') || !i.getAttribute('height'));
  ok(noDim.length === 0, `all ${imgs.length} <img> have width+height` + (noDim.length ? ` (missing: ${noDim.map(i=>i.getAttribute('src')).join(', ')})` : ''));

  // alt present on every img
  ok(imgs.every(i => i.hasAttribute('alt')), 'every <img> has an alt attribute');
}

// index-specific checks
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const d = new JSDOM(html).window.document;
console.log('\n== index.html wiring ==');

// every id the script reaches for actually exists
const ids = [...html.matchAll(/getElementById\('([^']+)'\)/g)].map(m => m[1]);
for (const id of [...new Set(ids)]) ok(!!d.getElementById(id), `getElementById('${id}') resolves`);

// querySelectorAll selectors used by the script match something
for (const sel of ['.magnetic','.reveal-element','.counter','.service-card','.process-card',
                   '.testimonial-slide','#testimonial-dots button','.gallery-img','.mobile-link',
                   '.cinematic-text-word','.cinematic-fade-up']) {
  const n = d.querySelectorAll(sel).length;
  ok(n > 0, `selector ${sel} matches ${n} element(s)`);
}

// counts line up between slides and dots
ok(d.querySelectorAll('.testimonial-slide').length === d.querySelectorAll('#testimonial-dots button').length,
   'testimonial slide count === dot count');

// form labels all point at a real control
const labels = [...d.querySelectorAll('form label[for]')];
ok(labels.length > 0 && labels.every(l => d.getElementById(l.getAttribute('for'))),
   `all ${labels.length} form labels resolve to a control`);
const controls = [...d.querySelectorAll('form input:not([type=hidden]), form select, form textarea')]
  .filter(c => c.name !== 'bot-field');
ok(controls.every(c => c.id && d.querySelector(`label[for="${c.id}"]`)),
   `all ${controls.length} visible form controls have a label`);

// data-service / data-step keys exist in the JS data objects
const svc = JSON.parse('{' + html.match(/const serviceData = \{([\s\S]*?)\n        \};/)[1].replace(/(\w+):/g,'"$1":') + '}');
[...d.querySelectorAll('[data-service]')].forEach(c =>
  ok(!!svc[c.getAttribute('data-service')], `serviceData has key "${c.getAttribute('data-service')}"`));

// no leftover references to the removed image or old selectors
ok(!html.includes('w9259kw9259'), 'no reference to the deleted 9.3MB PNG');
ok(!html.includes('.testimonial-dots span'), 'stale .testimonial-dots span selector is gone');
ok(!/<script[^>]+src="[^"]*lucide/i.test(html), 'no icon library is loaded from a CDN - icons are inline SVG');
ok(!html.includes('data-lucide='), 'no icon is left for a library to draw');

// Netlify must publish the pages as written. With Pretty URLs on it rewrote
// every link to an address the canonical tags and sitemap did not name.
{
  const toml = fs.readFileSync(path.join(ROOT, 'netlify.toml'), 'utf8');
  ok(/\[build\.processing\.html\][^\[]*pretty_urls\s*=\s*false/.test(toml), 'netlify.toml keeps Pretty URLs off');
}

// --- every link and button can be named ---
// An <a> with no text, no aria-label and no described image is an empty link:
// search engines get no anchor text and a screen reader announces "link". The
// footer's Facebook and Instagram links were exactly that once their icons
// stopped drawing.
console.log("\n== every link and button has a name, on every page ==");
{
  const pages = ['index.html', 'privacy.html', 'terms.html', 'success.html', '404.html',
    ...fs.readdirSync(path.join(ROOT, 'plans')).filter((f) => f.endsWith('.html')).map((f) => 'plans/' + f)];
  const named = (el) => (el.textContent || '').trim() || el.getAttribute('aria-label') || el.getAttribute('title') ||
    [...el.querySelectorAll('img[alt]')].some((i) => i.getAttribute('alt').trim()) ||
    (el.getAttribute('aria-labelledby') || '').split(/\s+/).some((id) => id && (el.ownerDocument.getElementById(id)?.textContent || '').trim());
  let checked = 0;
  for (const f of pages) {
    if (!fs.existsSync(path.join(ROOT, f))) { ok(false, `${f} exists`); continue; }
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), 'utf8')).window.document;
    const nameless = [...doc.querySelectorAll('a[href], button')].filter((el) => !named(el));
    checked += doc.querySelectorAll('a[href], button').length;
    ok(nameless.length === 0, `${f}: every link and button has a name` +
      (nameless.length ? ` - nameless: ${nameless.map((e) => e.outerHTML.slice(0, 90)).join(' | ')}` : ''));
  }
  console.log(`  ....  ${checked} links and buttons checked`);
}


// --- heading outline ---
console.log("\n== index.html heading outline ==");
{
  const hs=[...d.querySelectorAll("h1,h2,h3,h4,h5,h6")].map(h=>+h.tagName[1]);
  ok(d.querySelectorAll("h1").length===1, "exactly one <h1>");
  ok(hs[0]===1, "the first heading on the page is the <h1>");
  let skips=0; for(let i=1;i<hs.length;i++) if(hs[i]>hs[i-1]+1) skips++;
  ok(skips===0, "no heading level is skipped (found "+skips+")");
  // Every section that has a heading should lead with an h2.
  let bad=[];
  for(const sec of d.querySelectorAll("section")){
    const h=sec.querySelector("h1,h2,h3,h4,h5,h6");
    if(h && h.tagName!=="H2" && !sec.querySelector("h1")) bad.push((sec.id||"(unnamed)")+":"+h.tagName);
  }
  ok(bad.length===0, "every section leads with an <h2> "+(bad.length?"- offenders: "+bad.join(", "):""));
}


// --- no placeholder/example contact details anywhere ---
console.log("\n== contact details are real ==");
{
  const all = ["index.html","success.html","privacy.html","terms.html"]
    .map(n => fs.readFileSync(path.join(ROOT, n), "utf8")).join("\n");
  // 555-01xx is the reserved fictional range; example.com/.org likewise.
  const fake = all.match(/\(?\d{3}\)?[ -]?555-01\d\d|example\.(com|org|net)/g) || [];
  ok(fake.length === 0, "no fictional 555 numbers or example.com addresses" + (fake.length ? ": " + [...new Set(fake)].join(", ") : ""));
  const nums = [...new Set(all.match(/\(\d{3}\)\s?\d{3}-\d{4}/g) || [])];
  ok(nums.every(x => x.replace(/\D/g, "") === "8668326524"),
     "every displayed phone number is the real one: " + nums.join(", "));
}

// --- opening hours ---
// The footer shows the hours to people; the homepage's structured data gives
// the same hours to Google for the map listing. They are written separately,
// so check they still agree, and that every page shows the same line. The line
// is read as a screen reader hears it: the dots are hidden from it and the
// hidden commas are not.
console.log("\n== opening hours agree, on every page ==");
{
  const HOURS = "Monday–Friday 8 a.m.–5 p.m., Saturday by appointment, Closed Sunday";
  const spec = [...d.querySelectorAll('script[type="application/ld+json"]')]
    .map((s) => JSON.parse(s.textContent)).find((j) => j.openingHoursSpecification)?.openingHoursSpecification || [];
  ok(spec.length === 1 && spec[0].dayOfWeek.join() === "Monday,Tuesday,Wednesday,Thursday,Friday" &&
     spec[0].opens === "08:00" && spec[0].closes === "17:00",
     "structured data gives Monday-Friday 08:00-17:00 and nothing else - Saturday is by appointment, not open");
  const pages = ["index.html", "privacy.html", "terms.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const wrong = [];
  for (const f of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), "utf8")).window.document;
    const line = [...doc.querySelectorAll("p")].find((p) => /Saturday by appointment/.test(p.textContent));
    if (!line) { wrong.push(`${f}: no hours`); continue; }
    const heard = line.cloneNode(true);
    heard.querySelectorAll('[aria-hidden="true"]').forEach((el) => el.remove());
    const text = heard.textContent.replace(/\s+/g, " ").trim();
    if (text !== HOURS) wrong.push(`${f}: "${text}"`);
  }
  ok(wrong.length === 0, `all ${pages.length} pages show "${HOURS}"` + (wrong.length ? " - " + wrong.join(" | ") : ""));
}

console.log(fail === 0 ? '\nAll checks passed.' : `\n${fail} check(s) failed.`);
process.exit(fail ? 1 : 0);
