const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

(async () => {
  const b = await launch();

  console.log('\n== icons are part of the page, not fetched from anyone ==');
  // The icons used to be drawn by lucide@latest from unpkg. Lucide 1.0 dropped
  // its Facebook and Instagram icons and ten of them went blank on the live site
  // without anything noticing. They are inline SVG now; these checks keep it so.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    const offsite = [];
    p.on('request', (r) => {
      const u = new URL(r.url());
      if (/^https?:$/.test(u.protocol) && !/^(fonts\.(googleapis|gstatic)\.com|www\.googletagmanager\.com)$/.test(u.hostname) && r.resourceType() === 'script') offsite.push(u.hostname);
    });
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'load' });
    await p.waitForTimeout(3000);
    ok(offsite.length === 0, `no third-party script is fetched to draw the page (${[...new Set(offsite)].join(', ') || 'none'})`);
    const r = await p.evaluate(() => {
      const social = [...document.querySelectorAll('a[href*="facebook.com"], a[href*="instagram.com"]')];
      return {
        leftover: document.querySelectorAll('[data-lucide]').length,
        socialIcons: social.map((a) => { const s = a.querySelector('svg'); const b = s && s.getBoundingClientRect(); return b ? b.width * b.height : 0; }),
      };
    });
    ok(r.leftover === 0, `no icon is left waiting for a library to draw it (${r.leftover})`);
    // Four since the photo strip under Follow Our Builds, whose six tiles each
    // carried an Instagram icon, came off with The Storyteller's photographs:
    // the Facebook and Instagram links in that section and in the footer.
    ok(r.socialIcons.length >= 4 && r.socialIcons.every((a) => a > 0),
      `every Facebook and Instagram link draws its icon (${r.socialIcons.filter((a) => a > 0).length} of ${r.socialIcons.length})`);
    await ctx.close();
  }

  console.log('\n== the page is readable the moment it arrives ==');
  // There used to be a loading screen in front of every visit, then a headline
  // that slid in word by word, then sections that faded in as they were reached:
  // about two and a half seconds before the first words, and a page that stayed
  // hidden wherever script failed. It is all plain content now. Sample it as
  // soon as the document is parsed, before any timer could have run.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await serveFonts(ctx);
    const p = await ctx.newPage();
    await p.goto(FILE_ROOT + 'index.html', { waitUntil: 'domcontentloaded' });
    const r = await p.evaluate(() => {
      // Effective opacity: an element is only as visible as its faintest ancestor.
      const seen = (el) => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity); return o; };
      const hidden = [...document.querySelectorAll('section h1, section h2, section h3, section p, section a, section form')]
        .filter((el) => !el.closest('[role="dialog"], .group'))
        .filter((el) => seen(el) < 0.99)
        .map((el) => el.tagName + ' "' + el.textContent.trim().slice(0, 30) + '"');
      const cover = [...document.querySelectorAll('body > *')].filter((n) => {
        const cs = getComputedStyle(n), b = n.getBoundingClientRect();
        return cs.position === 'fixed' && b.width >= innerWidth && b.height >= innerHeight && cs.visibility !== 'hidden' && cs.display !== 'none';
      }).map((n) => n.id || n.tagName);
      return { hidden, cover, h1: seen(document.querySelector('h1')), cta: seen(document.querySelector('#hero a[href="#services"]')) };
    });
    ok(r.cover.length === 0, `nothing covers the page while it loads (${r.cover.join(', ') || 'none'})`);
    ok(r.h1 === 1 && r.cta === 1, `headline and "What We Build" are fully visible at first paint (${r.h1}, ${r.cta})`);
    ok(r.hidden.length === 0, `no heading, text, link or form anywhere starts hidden` + (r.hidden.length ? ' - ' + r.hidden.slice(0, 5).join(' | ') : ''));
    await ctx.close();
  }

  await b.close();
  console.log(fail ? `\n${fail} FAILED` : '\nAll robustness checks passed.');
  process.exit(fail ? 1 : 0);
})();
