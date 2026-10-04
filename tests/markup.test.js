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
  const imgs = [...d.querySelectorAll('img')];
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
for (const sel of ['.service-card','.process-card','.mobile-link']) {
  const n = d.querySelectorAll(sel).length;
  ok(n > 0, `selector ${sel} matches ${n} element(s)`);
}

// The stock template effects were taken out: a loading screen in front of
// every visit, a gold scroll-progress bar, buttons that drifted toward the
// pointer, figures that counted up, a headline that slid in word by word, a
// parallax quote mark and 38 blocks that faded in as they were scrolled to.
// Each also meant content that started hidden and depended on script to
// appear. None of it may come back unnoticed.
{
  const leftovers = ['#preloader', '#scroll-progress', '#parallax-quote', '.magnetic', '.reveal-element',
    '.counter', '[data-target]', '.cinematic-text-word', '.cinematic-fade-up', '.overflow-hidden-mask']
    .filter((sel) => d.querySelector(sel));
  const styles = fs.readFileSync(path.join(ROOT, 'src', 'styles.css'), 'utf8');
  const cssLeft = ['::-webkit-scrollbar', 'scrollbar-color', '@keyframes'].filter((x) => styles.includes(x));
  ok(leftovers.length === 0 && !/js-anim/.test(html) && cssLeft.length === 0,
     'no template effects: no loading screen, scroll bar, drifting buttons, counters, reveals or custom scrollbar' +
     (leftovers.length || cssLeft.length ? ' - found: ' + [...leftovers, ...cssLeft].join(', ') : ''));
}

// counts line up between slides and dots
// All three reviews are on the page at once. A carousel showed one and hid
// the other two behind dots that most visitors never press.
{
  const figs = [...d.querySelectorAll('#testimonials figure')];
  const names = figs.map((f) => f.querySelector('figcaption')?.textContent.trim());
  ok(figs.length === 3 && figs.every((f) => f.querySelector('blockquote')?.textContent.trim().length > 50),
     `three full testimonials in #testimonials (${names.join(', ')})`);
  ok(!d.querySelector('.testimonial-slide, #testimonial-dots, #prev-testimonial, #next-testimonial') && !/setInterval/.test(html),
     'no carousel: no slides, dots, arrows or auto-advance timer');
}

// The service cards had stock icons (a house, a ruler, a hammer) in heavy navy
// tiles that turned tan under the pointer, so a screenshot taken mid-hover made
// the set look mismatched. They are line drawings made for the site now, set
// straight on the page: navy for the building, gold for the architect's marks.
{
  const icons = [...d.querySelectorAll('.service-card svg')];
  const tiles = [...d.querySelectorAll('.service-card > div:first-child')].filter((t) => /\bbg-|group-hover:/.test(t.className));
  const colors = [...new Set(icons.flatMap((s) => [s, ...s.querySelectorAll('[stroke]')].map((e) => e.getAttribute('stroke').toLowerCase())))];
  const stray = colors.filter((c) => !['currentcolor', '#c2a67a'].includes(c));
  ok(icons.length === 3 && tiles.length === 0 && stray.length === 0,
     'service icons sit straight on the page in navy and gold: no tiles, no hover colour flip' +
     (tiles.length || stray.length ? ` - found ${tiles.length} tile(s)${stray.length ? ', colours ' + stray.join(', ') : ''}` : ''));
}

// The four process steps had their numbers in large gold-bordered boxes that
// filled with gold under the pointer, the same stock effect. They are a
// timeline now: a fine rule over each step, a small gold mark where it starts,
// and the number as a label. The numbers stay, because the steps are in order.
{
  const steps = [...d.querySelectorAll('.process-card')];
  const boxes = steps.filter((s) => s.querySelector('[class*="group-hover:bg-"], [class*="border-2"]'));
  const nums = steps.map((s) => (s.textContent.match(/\b0\d\b/) || [])[0]).join(' ');
  ok(steps.length === 4 && boxes.length === 0 && nums === '01 02 03 04',
     `process steps are a timeline numbered 01-04, with no boxes and no hover colour flip (numbers: ${nums}` +
     (boxes.length ? `, ${boxes.length} boxed` : '') + ')');
}

// The email, phone and office links had their icons in white tiles that turned
// navy under the pointer. They are a plain directory now, each entry between
// fine rules like the form's fields beside it. With that, nothing on the
// homepage fills a tile or box with colour on hover; the text turning gold is
// the only hover cue left on these links.
{
  const contact = [...d.querySelectorAll('#contact a[href^="mailto:"], #contact a[href^="tel:"], #contact a[href*="maps.google"]')];
  const iconned = contact.filter((a) => a.querySelector('svg'));
  ok(contact.length === 3 && iconned.length === 0, `contact details are a plain directory: 3 links, no icon tiles (${iconned.length} with icons)`);
  const flips = (html.match(/group-hover:bg-[^\s"]+/g) || []);
  ok(flips.length === 0, 'nothing on the homepage fills with colour under the pointer' + (flips.length ? ' - found ' + [...new Set(flips)].join(', ') : ''));
}

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

  // publish = "." would otherwise serve the repository's working files as
  // public pages - buildleavitt.com/README.md, /package.json, /src/plans.json.
  const command = (toml.match(/^\s*command\s*=\s*"([^"]*)"/m) || [])[1] || '';
  const removed = (command.match(/rm -rf ([^&;]*)/) || [])[1]?.trim().split(/\s+/) || [];
  const mustGo = ['assets-src', 'tests', 'src', 'scripts', 'package.json', 'package-lock.json', 'tailwind.config.js', 'README.md', 'CLAUDE.md'];
  const kept = mustGo.filter((f) => !removed.includes(f));
  ok(/npm run build\s*&&\s*rm -rf/.test(command) && kept.length === 0,
     'Netlify deletes non-site files after building the CSS' + (kept.length ? ' - still published: ' + kept.join(', ') : ''));
  const needed = removed.filter((f) => /^(dist|plans|index\.html|404\.html)$/.test(f));
  ok(needed.length === 0, 'and never deletes anything the site serves' + (needed.length ? ': ' + needed.join(', ') : ''));
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

// --- no italic-serif flourishes ---
// Headings used to end in Playfair Display italic - "Building legacies, *not
// just homes.*" - on every section of every page, the most recognisable mark of
// a template site. They were set upright, and the italic font is no longer
// downloaded, so an italic span would now render as a browser-faked slant too.
console.log("\n== no italic text or italic font ==");
{
  const pages = ["index.html", "privacy.html", "terms.html", "success.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const found = [];
  for (const f of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), "utf8")).window.document;
    for (const el of doc.querySelectorAll('[class~="italic"], em, i')) found.push(`${f}: "${el.textContent.trim().slice(0, 40)}"`);
    const font = doc.querySelector('link[href*="fonts.googleapis.com"]')?.getAttribute("href") || "";
    if (/ital/.test(font)) found.push(`${f}: font URL still requests italics`);
  }
  ok(found.length === 0, `no italic text on any of ${pages.length} pages` + (found.length ? " - " + found.slice(0, 8).join(" | ") : ""));
}

// --- no gold label stacked over each heading ---
// Every section used to open with a small gold letter-spaced label over its
// heading ("OUR EXPERTISE" / "Built for your lifestyle."), the most repeated
// template pattern on the site. The headings stand on their own now. The
// service and process pop-ups keep their small label ("Step 01"), which says
// where you are rather than restating the heading.
console.log("\n== no eyebrow labels over headings ==");
{
  const pages = ["index.html", "privacy.html", "terms.html", "success.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const found = [];
  for (const f of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), "utf8")).window.document;
    for (const h of doc.querySelectorAll("h1, h2")) {
      const prev = h.previousElementSibling;
      if (prev && /\buppercase\b/.test(prev.className) && /tracking-/.test(prev.className) && prev.textContent.trim().length < 40
          && !prev.closest('#hero, [role="dialog"]')) found.push(`${f}: "${prev.textContent.trim()}"`);
    }
  }
  ok(found.length === 0, `no small caps label sits over a heading on ${pages.length} pages` + (found.length ? " - " + found.slice(0, 6).join(" | ") : ""));
}

// --- claims Leavitt has not made ---
// The Architectural Design pop-up promised "premier architects and designers"
// and "3D renderings". Leavitt asked for both to come out; don't put either
// back without checking with him. Anything on the site has to be true.
console.log("\n== no claims Leavitt has not made ==");
{
  const claims = [/premier architects/i, /3D render/i];
  const found = claims.filter((re) => re.test(html)).map(String);
  ok(found.length === 0, 'no "premier architects" or "3D renderings" on the homepage' + (found.length ? ' - found: ' + found.join(', ') : ''));
}

// --- Facebook ---
// The site pointed at facebook.com/LeavittBuildingGroup, which is not
// Leavitt's page. The address below is the page's permanent one, as the
// browser shows it once the page is open, minus Facebook's tracking
// parameters. Every Facebook link on every page - the footer icon, the
// "Follow Our Builds" link and the structured data Google reads - must be it.
console.log("\n== Facebook links go to Leavitt's page ==");
{
  const FACEBOOK = "https://www.facebook.com/profile.php?id=61591583276647";
  const pages = ["index.html", "privacy.html", "terms.html", "success.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const found = [];
  for (const f of pages) {
    const src = fs.readFileSync(path.join(ROOT, f), "utf8");
    for (const m of src.matchAll(/https?:\/\/(?:www\.|m\.)?facebook\.com[^"'\s<)]*/g)) found.push(`${f}: ${m[0]}`);
  }
  const wrong = found.filter((x) => !x.endsWith(": " + FACEBOOK));
  ok(found.length >= 3 && wrong.length === 0,
     `all ${found.length} Facebook links are ${FACEBOOK}` + (wrong.length ? " - wrong: " + wrong.join(" | ") : ""));
}

// When the photo gallery came off the homepage, the header of all eighteen plan
// pages still offered "Gallery", pointing at a #gallery that no longer existed.
// A link to a section of a page has to find that section: on every page, each
// same-site link with a #fragment must name an id that exists on its target.
console.log("\n== every link to a section of a page finds that section ==");
{
  const pages = ["index.html", "privacy.html", "terms.html", "success.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const ids = new Map();
  const idsOf = (f) => {
    if (!ids.has(f)) {
      const file = path.join(ROOT, f);
      ids.set(f, fs.existsSync(file)
        ? new Set([...new JSDOM(fs.readFileSync(file, "utf8")).window.document.querySelectorAll("[id]")].map((e) => e.id))
        : null);
    }
    return ids.get(f);
  };
  const broken = [];
  let checked = 0;
  for (const f of pages) {
    const doc = new JSDOM(fs.readFileSync(path.join(ROOT, f), "utf8")).window.document;
    for (const a of doc.querySelectorAll("a[href*='#']")) {
      const href = a.getAttribute("href");
      if (/^[a-z]+:/i.test(href) || href === "#") continue;
      const u = new URL(href, "https://buildleavitt.com/" + f);
      if (!u.hash || u.hash === "#") continue;
      const target = u.pathname.endsWith("/") ? u.pathname.slice(1) + "index.html" : u.pathname.slice(1);
      const found = idsOf(target);
      checked++;
      if (!found || !found.has(decodeURIComponent(u.hash.slice(1)))) broken.push(`${f}: ${href}`);
    }
  }
  ok(checked > 20 && broken.length === 0,
     `all ${checked} section links land on a section that exists` + (broken.length ? " - broken: " + [...new Set(broken)].slice(0, 6).join(" | ") + (broken.length > 6 ? ` (+${broken.length - 6} more)` : "") : ""));
}

// The first Tag Manager container, GTM-K9ND8BDT, was created under the
// marketing agency's Google login, so Leavitt could not see or change what it
// ran. GTM-PHGFM247 is Leavitt's own; the agency is a user on it. Every page
// must load that container, in both the <head> script and the <noscript>
// iframe, and no other.
console.log("\n== every page loads Leavitt's own Tag Manager container ==");
{
  const GTM = "GTM-PHGFM247";
  const pages = ["index.html", "privacy.html", "terms.html", "success.html", "404.html",
    ...fs.readdirSync(path.join(ROOT, "plans")).filter((f) => f.endsWith(".html")).map((f) => "plans/" + f)];
  const bad = [];
  for (const f of pages) {
    const src = fs.readFileSync(path.join(ROOT, f), "utf8");
    const ids = [...src.matchAll(/GTM-[A-Z0-9]+/g)].map((m) => m[0]);
    if (ids.length !== 2 || ids.some((id) => id !== GTM)) bad.push(`${f}: ${ids.join(", ") || "none"}`);
  }
  ok(bad.length === 0, `all ${pages.length} pages load ${GTM} and no other container` + (bad.length ? " - " + bad.join(" | ") : ""));
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
