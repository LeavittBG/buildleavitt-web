const { ROOT, FILE_ROOT, OUT, launch, serveRepo } = require('./lib/env');
const { chromium } = require('playwright');
// Real Inter/Playfair, not a system fallback - text width decides these layouts.
const { serveFonts } = require('./lib/fonts');
let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };
(async () => {
  const b = await launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await serveFonts(p);
  await p.goto(FILE_ROOT + 'index.html');
  await p.waitForTimeout(4200);
  await p.evaluate(() => document.querySelectorAll('.reveal-element').forEach(e => e.classList.add('active')));
  await p.evaluate(async () => { for (let y=0; y<document.body.scrollHeight; y+=300){window.scrollTo(0,y); await new Promise(r=>setTimeout(r,60));} });
  await p.waitForTimeout(1500);

  const m = await p.evaluate(() => {
    // The strip's tiles are the grid's own links. Matching on the label alone
    // would also count the footer's Instagram icon, which now has a label too.
    const insta = [...document.querySelectorAll('.grid > a[href*="instagram.com"]')];
    const logo = document.querySelector('#main-nav img');
    const hero = document.querySelector('.animate-ken-burns');
    const kyle = document.querySelector('img[src="kyle.jpg"]');
    const ba = document.querySelector('#ba-slider');
    const baImg = document.querySelector('#ba-slider img');
    return {
      instaCols: [...new Set(insta.map(a => a.offsetLeft))].length,
      instaRows: [...new Set(insta.map(a => a.offsetTop))].length,
      instaCount: insta.length,
      logoW: logo.offsetWidth, logoH: logo.offsetHeight,
      heroW: hero.offsetWidth, heroH: hero.offsetHeight,
      kyleW: kyle.offsetWidth, kyleH: kyle.offsetHeight,
      baW: ba.offsetWidth, baH: ba.offsetHeight, baImgW: baImg.offsetWidth, baImgH: baImg.offsetHeight,
      sourcesRendered: [...document.querySelectorAll('source')].filter(s => s.offsetWidth || s.offsetHeight).length,
      totalSources: document.querySelectorAll('source').length,
    };
  });
  console.log(JSON.stringify(m, null, 1).replace(/[{}"]/g, '').trim());
  ok(m.sourcesRendered === 0, `none of the ${m.totalSources} <source> elements occupy layout space`);
  ok(m.instaCols === 6 && m.instaRows === 1, `Instagram strip is one row of 6 (${m.instaCols}x${m.instaRows})`);
  ok(m.logoH > 0 && m.logoW > 0, `nav logo sized ${m.logoW}x${m.logoH}`);
  ok(m.heroW === 1280, `hero image spans the viewport (${m.heroW}px)`);
  ok(Math.abs(m.kyleW - m.kyleH) <= 1, `kyle.jpg still square (${m.kyleW}x${m.kyleH})`);
  ok(m.baImgW === m.baW && m.baImgH === m.baH, `before/after images fill the slider (${m.baImgW}x${m.baImgH} in ${m.baW}x${m.baH})`);
  await b.close();
  console.log(fail === 0 ? '\nAll layout checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
