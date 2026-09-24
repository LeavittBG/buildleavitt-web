/*
 * Re-download tests/fixtures/fonts/ from the font URL index.html actually uses.
 * Run after changing that URL:   npm run test:fonts
 *
 * Google Fonts tailors its stylesheet to the requesting browser, so this asks
 * as a desktop Chrome would - the same files a visitor gets.
 */
const fs = require('fs');
const path = require('path');
const { ROOT } = require('./env');

const DIR = path.join(__dirname, '..', 'fixtures', 'fonts');
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

(async () => {
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const href = (html.match(/https:\/\/fonts\.googleapis\.com\/css2[^"]*/) || [])[0];
  if (!href) throw new Error('No Google Fonts link found in index.html');
  const url = href.replace(/&amp;/g, '&');

  const res = await fetch(url, { headers: { 'user-agent': UA } });
  if (!res.ok) throw new Error(`Stylesheet request failed: ${res.status}`);
  const css = await res.text();
  const files = [...new Set(css.match(/https:\/\/fonts\.gstatic\.com\/[^)]+/g) || [])];

  for (const f of fs.readdirSync(DIR)) fs.unlinkSync(path.join(DIR, f));
  const map = [];
  for (const [i, u] of files.entries()) {
    const r = await fetch(u, { headers: { 'user-agent': UA } });
    if (!r.ok) throw new Error(`Font request failed: ${r.status} ${u}`);
    const name = `f${i + 1}.woff2`;
    fs.writeFileSync(path.join(DIR, name), Buffer.from(await r.arrayBuffer()));
    map.push(`${u} ${name}`);
  }
  fs.writeFileSync(path.join(DIR, 'gf.css'), css);
  fs.writeFileSync(path.join(DIR, 'map.txt'), map.join('\n') + '\n');
  console.log(`Saved the stylesheet and ${files.length} font files for:\n  ${url}`);
})().catch((e) => { console.error(e.message); process.exit(1); });
