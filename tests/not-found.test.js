/*
 * The page someone lands on when a link is wrong.
 *
 * Netlify serves 404.html for any address with no file behind it, and serves it
 * AT that address. So the page has to work from any depth - a relative
 * "dist/styles.css" asked for from /plans/old/page.html would resolve to
 * /plans/old/dist/styles.css and the visitor would get an unstyled page. This
 * requests addresses at several depths and checks the page arrives whole, and
 * that search engines are told not to index it.
 */
const { ROOT, launch, serveRepo } = require('./lib/env');
const { serveFonts } = require('./lib/fonts');
const fs = require('fs');
const path = require('path');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  console.log('\n== a missing address gets the real 404 page, fully styled ==');
  const server = await serveRepo();
  const b = await launch();
  for (const missing of ['/no-such-page', '/plans/the-old-name.html', '/plans/deeper/still/missing.html']) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    await ctx.route(/googletagmanager|google\.com/, (r) => r.abort());
    const p = await ctx.newPage();
    const broken = [];
    p.on('response', (r) => {
      const u = r.url();
      if (u.startsWith(server.base) && u !== server.base + missing && r.status() >= 400) broken.push(u.replace(server.base, ''));
    });
    const res = await p.goto(server.base + missing, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => {
      const logo = document.querySelector('img[alt="Leavitt Building Group"]');
      return {
        title: document.title,
        noindex: document.querySelector('meta[name="robots"]')?.content || '',
        styled: getComputedStyle(document.body).backgroundColor === 'rgb(15, 23, 42)',
        logo: !!logo && logo.naturalWidth > 0,
        links: [...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href')),
      };
    });
    ok(res.status() === 404, `${missing}: answers with a 404 status (${res.status()})`);
    ok(/Page Not Found/.test(r.title), `${missing}: serves the 404 page ("${r.title}")`);
    ok(r.styled && r.logo, `${missing}: stylesheet and logo load at this depth`);
    ok(broken.length === 0, `${missing}: nothing on the page itself fails to load${broken.length ? ' - ' + broken.join(', ') : ''}`);
    ok(r.noindex.includes('noindex'), `${missing}: tells search engines not to index it`);
    ok(['/', '/plans/', '/#contact'].every((h) => r.links.includes(h)), `${missing}: offers a way back - home, plans, contact`);
    await ctx.close();
  }
  await b.close();
  await server.close();

  console.log('\n== the 404 page stays out of the sitemap ==');
  const sitemap = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  ok(!/404/.test(sitemap), 'sitemap.xml does not list it');

  console.log(fail ? `\n${fail} FAILED` : '\nAll not-found checks passed.');
  process.exit(fail ? 1 : 0);
})();
