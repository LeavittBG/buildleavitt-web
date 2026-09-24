/*
 * Serve the site's real webfonts to a test page, from tests/fixtures/fonts/.
 *
 * Any test that measures text has to call this. Without the real fonts the page
 * falls back to a system face with different widths - Playfair Display's italic
 * "A" overhangs far more than a system serif's - so a measurement could pass
 * while the live site clipped. Serving them from a committed copy also keeps
 * the suite independent of the network: headless Chromium is refused by Google
 * Fonts outright (a 400 for its default user-agent) and cannot always reach it
 * through a corporate or sandbox proxy.
 *
 * If the font URL in the pages changes, refresh the copy with
 *   npm run test:fonts
 * or the tests will be measuring the old weights.
 */
const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname, '..', 'fixtures', 'fonts');

function loadMap() {
  const map = new Map();
  for (const line of fs.readFileSync(path.join(DIR, 'map.txt'), 'utf8').trim().split('\n')) {
    const [url, file] = line.split(' ');
    map.set(url, path.join(DIR, file));
  }
  return map;
}

/** Point `page` at the cached fonts. Call before page.goto(). */
async function serveFonts(page) {
  const css = fs.readFileSync(path.join(DIR, 'gf.css'));
  const files = loadMap();

  await page.route('https://fonts.googleapis.com/**', (route) =>
    route.fulfill({ status: 200, contentType: 'text/css', body: css }),
  );
  await page.route('https://fonts.gstatic.com/**', (route) => {
    const file = files.get(route.request().url());
    if (!file) return route.abort();
    return route.fulfill({
      status: 200,
      contentType: 'font/woff2',
      headers: { 'access-control-allow-origin': '*' },
      body: fs.readFileSync(file),
    });
  });
}

/*
 * document.fonts.check() answers true for any family the browser is willing to
 * substitute, so it cannot confirm a download. Only a loaded FontFace can.
 */
async function assertLoaded(page, family) {
  await page.evaluate(() => document.fonts.ready);
  const ok = await page.evaluate(
    (f) => [...document.fonts].some((ff) => ff.family.includes(f) && ff.status === 'loaded'),
    family,
  );
  if (!ok) throw new Error(`${family} did not load - any glyph measurement here would be against the wrong font`);
}

module.exports = { serveFonts, assertLoaded };
