/*
 * The pages under /plans/ link "/dist/styles.css" - root-absolute, which is
 * right for Netlify and unresolvable under file://. Loading them from disk
 * therefore renders them with no stylesheet at all, so any visual assertion
 * made that way is about a page no visitor sees. This serves the repo over HTTP
 * and checks the plans pages as they actually render.
 */
const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');

const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.xml': 'application/xml' };

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const server = http.createServer((req, res) => {
    let p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (p.endsWith('/')) p += 'index.html';
    fs.readFile(p, (e, buf) => {
      if (e) { res.writeHead(404); return res.end('no'); }
      res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
      res.end(buf);
    });
  }).listen(0);
  const base = `http://127.0.0.1:${server.address().port}`;

  const models = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/plans.json'), 'utf8')).models;
  const urls = ['/plans/', ...models.map((m) => `/plans/${m.slug}.html`)];

  const browser = await launch();

  for (const width of [390, 768, 1280]) {
    console.log(`\n== /plans/ at ${width}px, styled ==`);
    const ctx = await browser.newContext({ viewport: { width, height: 900 } });
    await serveFonts(ctx);
    // Refuse everything that would leave the machine, except the fonts that
    // serveFonts answers from its cache. Tag Manager is the only such request
    // these pages make and nothing asserted here depends on it; left alone it
    // went out to the sandbox proxy, waited 150-260ms to be refused, and the
    // result and runtime of this test depended on how that proxy felt.
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)(?!fonts\.(googleapis|gstatic)\.com)/, (r) => r.abort());
    const page = await ctx.newPage();
    let stylesheetSeen = false;
    page.on('response', (r) => { if (r.url().endsWith('/dist/styles.css') && r.status() === 200) stylesheetSeen = true; });

    for (const u of urls) {
      stylesheetSeen = false;
      // Wait for exactly what the checks below depend on: the stylesheet and
      // images (both hold back 'load') and the web fonts, whose widths decide
      // whether text overflows. 'networkidle' was the old wait - a fixed 500ms
      // of quiet after the last request, 54 times over, which made this the
      // slowest suite at ~41s, and which never promised the fonts had applied.
      await page.goto(base + u, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      const r = await page.evaluate(() => {
        const de = document.documentElement;
        // Anything wider than the viewport, and any element whose own text is
        // being cut off by an ancestor that clips.
        const clipped = [...document.querySelectorAll('*')].filter((n) => {
          const cs = getComputedStyle(n);
          if (cs.overflow === 'visible' || !n.children.length) return false;
          return n.scrollWidth > n.clientWidth + 1 && n.clientWidth > 0;
        }).slice(0, 3).map((n) => n.tagName + '.' + (n.className || '').toString().slice(0, 30));
        return {
          overflow: Math.max(0, de.scrollWidth - de.clientWidth),
          // Tailwind is applied if the body carries its background, which only
          // the stylesheet sets. Typefaces are fontcheck.js's job, not this one's.
          styled: getComputedStyle(document.body).backgroundColor === 'rgb(252, 252, 252)',
          clipped,
        };
      });
      ok(r.styled && stylesheetSeen, `${u} loads its stylesheet`);
      ok(r.overflow === 0, `${u} no horizontal scroll (${r.overflow}px)`);
      ok(r.clipped.length === 0, `${u} nothing clipping its own content${r.clipped.length ? ': ' + r.clipped.join(', ') : ''}`);
    }
    await ctx.close();
  }

  await browser.close();
  server.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll styled plans-page checks passed.');
  process.exit(fail ? 1 : 0);
})();
