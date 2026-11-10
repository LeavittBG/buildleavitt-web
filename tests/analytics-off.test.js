/*
 * The tests must never talk to Leavitt's real Google Analytics.
 *
 * Every page carries the live Google Tag Manager container. Until November
 * 2026 most tests let it load, so each run of the suite sent page views to the
 * real Analytics property from http://127.0.0.1 and file:// addresses. Worse,
 * fonts.test.js opens success.html, the thank-you page, and Analytics turns a
 * page view whose address contains "/success" into the generate_lead key event:
 * a pull request's test run could be counted as a lead.
 *
 * launch() in lib/env.js now refuses every request to Google's tag and
 * analytics hosts, on every page any test opens. This file checks that it
 * does, however the page is opened. It asks for "refused by the tests", not
 * just "did not arrive", so it cannot pass merely because the network was down.
 */
const { FILE_ROOT, launch, serveRepo } = require('./lib/env');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

// Kept apart from the list in lib/env.js on purpose: if that list is ever
// thinned, this one still knows what must not get out.
const TAG_HOST = /(^|\.)(googletagmanager\.com|google-analytics\.com|analytics\.google\.com|doubleclick\.net)$/i;
const isTag = (url) => { try { return TAG_HOST.test(new URL(url).hostname); } catch (e) { return false; } };

(async () => {
  const site = await serveRepo();
  const b = await launch();

  // The ways the suite opens a page: straight from the browser, through a
  // context of its own, with script switched off (the <noscript> iframe is a
  // request to Tag Manager too), and from disk rather than the local server.
  const ways = [
    ['browser.newPage()', async () => b.newPage({ viewport: { width: 1280, height: 900 } }), site.base + '/'],
    ['browser.newContext().newPage()', async () => (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage(), site.base + '/'],
    ['a context with script switched off', async () => (await b.newContext({ javaScriptEnabled: false })).newPage(), site.base + '/'],
    ['a page opened from disk', async () => b.newPage(), FILE_ROOT],
  ];

  for (const [name, open, base] of ways) {
    console.log(`\n== ${name} ==`);
    // success.html first: its page view is the one Analytics counts as a lead.
    for (const file of ['success.html', 'index.html', 'plans/index.html']) {
      const p = await open();
      const asked = [];
      const answered = [];
      const refused = [];
      p.on('request', (r) => { if (isTag(r.url())) asked.push(r.url()); });
      p.on('response', (r) => { if (isTag(r.url())) answered.push(r.url()); });
      p.on('requestfailed', (r) => { if (isTag(r.url())) refused.push((r.failure() || {}).errorText || ''); });
      await p.goto(base + file, { waitUntil: 'load' });
      await p.waitForLoadState('networkidle');
      ok(asked.length > 0, `${file}: the page does ask for the Google tag, so there is something to refuse (${asked.length})`);
      ok(answered.length === 0, `${file}: no request to Google's tag or analytics hosts was answered (${answered.length})`);
      ok(refused.length === asked.length && refused.every((e) => /BLOCKED_BY_CLIENT/.test(e)),
        `${file}: every one was refused by the tests themselves` +
        (refused.every((e) => /BLOCKED_BY_CLIENT/.test(e)) ? '' : ` - got: ${[...new Set(refused)].join(', ') || 'no refusal at all'}`));
      await p.context().close();
    }
  }

  await b.close();
  await site.close();
  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
