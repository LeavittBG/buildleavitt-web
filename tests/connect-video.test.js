// The Leavitt Connect tour is hosted on the site itself rather than on YouTube,
// which can run ads on any video, a competitor's included (October 2026). The
// original file was 38MB. Hosting it here is only fine while the homepage stays
// as light as before, so this guards that:
//  - nothing of the video downloads until someone presses play;
//  - the file stays the small web copy, with its index at the front so it can
//    start playing before it has finished downloading;
//  - the captions fit the video and the transcript matches them, so a
//    replacement video cannot leave either one out of date;
//  - each "See it in the video" button starts the tour at its own moment.
// Headless Chromium has no H.264 decoder, so the jump check plays a blank
// 108-second WebM in its place, served with byte ranges as Netlify serves the
// real file. Without ranges a browser cannot skip ahead at all.
const { ROOT, launch, serveRepo } = require('./lib/env');
const path = require('path');
const fs = require('fs');
const { JSDOM } = require('jsdom');

let fail = 0;
const ok = (c, m) => { console.log((c ? '  PASS  ' : '  FAIL  ') + m); if (!c) fail++; };

// Top-level MP4 boxes, in file order: [{ type, start, size }].
function boxes(buf) {
  const out = [];
  for (let i = 0; i + 8 <= buf.length;) {
    let size = buf.readUInt32BE(i);
    const type = buf.toString('latin1', i + 4, i + 8);
    if (size === 1) size = Number(buf.readBigUInt64BE(i + 8));
    if (size < 8) break;
    out.push({ type, start: i, size });
    i += size;
  }
  return out;
}

// Length of an MP4 in seconds, from its movie header.
function mp4Seconds(buf) {
  const i = buf.indexOf('mvhd', 0, 'latin1');
  if (i < 0) return NaN;
  const v = buf[i + 4];
  return v === 1
    ? Number(buf.readBigUInt64BE(i + 4 + 4 + 16 + 4)) / buf.readUInt32BE(i + 4 + 4 + 16)
    : buf.readUInt32BE(i + 4 + 4 + 8 + 4) / buf.readUInt32BE(i + 4 + 4 + 8);
}

const secs = (t) => { const [h, m, s] = t.split(':'); return +h * 3600 + +m * 60 + parseFloat(s); };
const plain = (s) => s.replace(/[\u2018\u2019]/g, "'").replace(/\s+/g, ' ').trim();

(async () => {
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const d = new JSDOM(html).window.document;
  const video = d.querySelector('#leavitt-connect video');

  console.log('\n== the video and its files ==');
  ok(!!video, 'the Leavitt Connect section has a video');
  if (!video) process.exit(1);
  ok(video.getAttribute('preload') === 'none', 'preload="none", so it downloads nothing until played');
  ok(video.hasAttribute('controls') && video.hasAttribute('playsinline'), 'it has controls and plays inline on iPhones');
  const src = video.querySelector('source')?.getAttribute('src') || '';
  const poster = video.getAttribute('poster') || '';
  const track = video.querySelector('track[kind="captions"]')?.getAttribute('src') || '';
  for (const f of [src, poster, track]) ok(!!f && fs.existsSync(path.join(ROOT, f)), `file exists: ${f || '(none named)'}`);

  const mp4 = fs.readFileSync(path.join(ROOT, src));
  const mb = mp4.length / 1048576;
  ok(mb < 8, `the video is the small web copy (${mb.toFixed(1)}MB, limit 8MB)`);
  const order = boxes(mp4).map((b) => b.type);
  ok(order.indexOf('moov') > -1 && order.indexOf('moov') < order.indexOf('mdat'),
     `its index comes first, so it starts before it has fully downloaded (${order.join(', ')})`);
  const length = mp4Seconds(mp4);
  ok(Math.abs(length - 108) < 2, `it runs 1:48 (${length.toFixed(1)}s)`);

  console.log('\n== captions and transcript ==');
  const vtt = fs.readFileSync(path.join(ROOT, track), 'utf8');
  ok(vtt.startsWith('WEBVTT'), 'the captions file is WebVTT');
  const cues = [...vtt.matchAll(/(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})\n([\s\S]*?)(?:\n\n|\n?$)/g)]
    .map((m) => ({ start: secs(m[1]), end: secs(m[2]), text: plain(m[3]) }));
  ok(cues.length > 20, `${cues.length} captions read`);
  const late = cues.filter((c) => !(c.start < c.end && c.end <= length + 0.5));
  ok(late.length === 0, 'every caption falls within the video' + (late.length ? ' - ' + late.map((c) => c.text).join(' | ') : ''));
  const transcript = plain(d.querySelector('#leavitt-connect details')?.textContent || '');
  const missing = cues.filter((c) => !transcript.includes(c.text));
  ok(missing.length === 0, 'the transcript has every caption, word for word' + (missing.length ? ' - missing: ' + missing.map((c) => c.text).join(' | ') : ''));

  console.log('\n== in the browser ==');
  const blank = fs.readFileSync(path.join(__dirname, 'fixtures', 'blank-108s.webm'));
  const b = await launch();
  const site = await serveRepo();
  const page = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const fetched = [];
  page.on('request', (r) => { if (r.url().endsWith('.mp4')) fetched.push(r.url()); });
  await page.route('**/*.mp4', (route) => {
    const m = /bytes=(\d+)-(\d*)/.exec(route.request().headers().range || '');
    const s = m ? +m[1] : 0;
    const e = m && m[2] ? +m[2] : blank.length - 1;
    route.fulfill({
      status: m ? 206 : 200,
      headers: {
        'content-type': 'video/webm', 'accept-ranges': 'bytes', 'content-length': String(e - s + 1),
        ...(m ? { 'content-range': `bytes ${s}-${e}/${blank.length}` } : {}),
      },
      body: blank.subarray(s, e + 1),
    });
  });
  await page.goto(site.base + '/');
  await page.locator('#leavitt-connect').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1500);
  ok(fetched.length === 0, 'nothing of the video loads with the page, even scrolled into view' + (fetched.length ? ` (${fetched.length} requests)` : ''));

  const seeks = await page.$$eval('#leavitt-connect [data-seek]', (bs) => bs.map((x) => +x.getAttribute('data-seek')));
  ok(seeks.length === 6, `six "See it in the video" buttons (${seeks.length})`);
  for (const t of seeks) {
    ok(t < length && cues.some((c) => c.start >= t - 2 && c.start <= t + 2), `${t}s starts on a caption`);
    await page.click(`[data-seek="${t}"]`);
    await page.waitForFunction((t) => { const v = document.getElementById('connect-video'); return !v.paused && v.currentTime >= t; }, t, { timeout: 8000 }).catch(() => {});
    const now = await page.evaluate(() => { const v = document.getElementById('connect-video'); return { t: v.currentTime, playing: !v.paused }; });
    ok(now.playing && now.t >= t && now.t < t + 4, `the ${t}s button plays from ${t}s (at ${now.t.toFixed(1)}s, ${now.playing ? 'playing' : 'paused'})`);
  }
  await site.close();
  await b.close();

  console.log(fail === 0 ? '\nAll Leavitt Connect video checks passed.' : `\n${fail} failed.`);
  process.exit(fail ? 1 : 0);
})();
