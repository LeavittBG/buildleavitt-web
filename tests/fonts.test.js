/* Every page must actually render in the two typefaces the site pays to load,
   and every weight it asks for must be one that was downloaded rather than one
   the browser had to approximate. Served over HTTP because the /plans/ pages
   reference /dist/styles.css from the root. */
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

const audit = () => {
  // What each element is asked to render in, and what is actually available.
  const loaded = [...document.fonts].filter((f) => f.status === 'loaded');
  const has = (fam, weight, style) =>
    loaded.some((f) => f.family.replace(/["']/g, '') === fam &&
                       String(f.weight) === String(weight) &&
                       f.style === (style || 'normal'));
  const missing = new Map();
  let sans = 0, serif = 0, other = 0;
  for (const el of document.querySelectorAll('body, body *')) {
    if (!el.textContent.trim() || el.children.length && !el.childNodes.length) continue;
    const cs = getComputedStyle(el);
    const first = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    if (first === 'Inter') sans++;
    else if (first === 'Playfair Display') serif++;
    else { other++; continue; }
    if (!has(first, cs.fontWeight, cs.fontStyle)) {
      const k = `${first} ${cs.fontWeight}${cs.fontStyle === 'italic' ? ' italic' : ''}`;
      missing.set(k, (missing.get(k) || 0) + 1);
    }
  }
  return { sans, serif, other, missing: [...missing.entries()], bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0].replace(/["']/g, '') };
};

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
  const pages = ['/index.html', '/privacy.html', '/terms.html', '/success.html', '/404.html', '/plans/',
                 ...models.map((m) => `/plans/${m.slug}.html`)];

  const b = await launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  await serveFonts(ctx);
  const page = await ctx.newPage();

  const allMissing = new Map();
  for (const u of pages) {
    await page.goto(base + u, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(audit);
    ok(r.bodyFont === 'Inter', `${u} body renders in Inter (got ${r.bodyFont})`);
    ok(r.other === 0, `${u} every text element is Inter or Playfair (${r.sans} + ${r.serif}, ${r.other} neither)`);
    for (const [k, n] of r.missing) allMissing.set(k, (allMissing.get(k) || 0) + n);
  }

  console.log('\n== every weight in use was actually downloaded ==');
  if (allMissing.size === 0) ok(true, 'no element asks for a weight the browser did not have');
  else for (const [k, n] of allMissing) ok(false, `${n} elements ask for "${k}", which was never downloaded`);

  await b.close();
  server.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll font checks passed.');
  process.exit(fail ? 1 : 0);
})();
