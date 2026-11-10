/*
 * Where things are, for every test.
 *
 * These tests began life outside the repository, with the site's location and
 * the browser's location written into each file. Everything that depends on the
 * machine now lives here instead, so the suite runs from any checkout.
 */
const fs = require('fs');
const http = require('http');
const path = require('path');
const { pathToFileURL } = require('url');

/** The repository root. */
const ROOT = path.resolve(__dirname, '..', '..');

/** The same, as a file:// URL with a trailing slash: FILE_ROOT + 'index.html'. */
const FILE_ROOT = pathToFileURL(ROOT).href + '/';

/** Screenshots the tests leave behind for a person to look at. Ignored by git. */
const OUT = path.join(ROOT, 'tests', '.output');
fs.mkdirSync(OUT, { recursive: true });

/*
 * Which Chromium to drive. Normally Playwright's own, installed once with
 * `npx playwright install chromium`. CHROMIUM_PATH overrides that. Claude Code's
 * cloud containers ship a Chromium at /opt/pw-browsers/chromium that does not
 * match the build this Playwright version expects, so it is used when present.
 */
function chromiumPath() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  if (fs.existsSync('/opt/pw-browsers/chromium')) return '/opt/pw-browsers/chromium';
  return undefined;
}

/*
 * Hosts no test may reach: Google Tag Manager and Analytics. Every page carries
 * the live container, and a test that lets it load sends page views to
 * Leavitt's real Analytics property. A page view of the thank-you page counts
 * there as a lead (generate_lead), and fonts.test.js opens that page, so until
 * November 2026 a pull request's test run could be recorded as a lead.
 */
const ANALYTICS = /^https?:\/\/([a-z0-9-]+\.)*(googletagmanager\.com|google-analytics\.com|analytics\.google\.com|doubleclick\.net|googleadservices\.com|googlesyndication\.com)\//i;

/*
 * Every test gets its browser here, and every page that browser opens refuses
 * the hosts above before the request leaves the machine. browser.newPage()
 * makes its context through newContext(), so wrapping that one method covers
 * both. 'blockedbyclient' is what analytics-off.test.js looks for: a refusal by
 * the tests, which is not the same as the network happening to be down. A test
 * that adds its own route still wins, as the newest route always does, but none
 * of them lets these hosts through.
 */
async function launch(options = {}) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ ...options, executablePath: chromiumPath() });
  const newContext = browser.newContext.bind(browser);
  browser.newContext = async (...args) => {
    const context = await newContext(...args);
    await context.route(ANALYTICS, (route) => route.abort('blockedbyclient'));
    return context;
  };
  return browser;
}

/*
 * Serve the repository over HTTP. The pages under /plans/ link
 * "/dist/styles.css" from the root - correct on Netlify, unresolvable under
 * file:// - so loading them from disk renders them with no stylesheet at all.
 * Anything that looks at how a plans page renders has to come through here.
 */
const TYPES = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.pdf': 'application/pdf', '.xml': 'application/xml', '.ico': 'image/x-icon',
};

function serveRepo(rewrite) {
  const server = http.createServer((req, res) => {
    let p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
    if (p.endsWith('/')) p += 'index.html';
    fs.readFile(p, (e, buf) => {
      // As Netlify does: any address with no file behind it gets 404.html, with
      // a 404 status, served at the address that was asked for.
      if (e) {
        const nf = path.join(ROOT, '404.html');
        if (!fs.existsSync(nf)) { res.writeHead(404); return res.end('not found'); }
        res.writeHead(404, { 'content-type': 'text/html' });
        return res.end(fs.readFileSync(nf));
      }
      if (rewrite) buf = rewrite(p, buf) || buf;
      res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
      res.end(buf);
    });
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve({
    base: `http://127.0.0.1:${server.address().port}`,
    close: () => new Promise((r) => server.close(r)),
  })));
}

module.exports = { ROOT, FILE_ROOT, OUT, launch, serveRepo };
