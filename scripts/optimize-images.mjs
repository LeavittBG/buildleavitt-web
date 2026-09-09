/**
 * Image pipeline:  assets-src/  ->  optimised web images in the repo root
 *
 *   npm run images
 *
 * assets-src/ holds the full-resolution originals. Everything the site serves
 * is derived from them here: a resized JPEG/PNG, a WebP companion, and the
 * favicon set. Nothing is generated during a Netlify build - the outputs are
 * committed, and this script is only re-run when source photos change.
 *
 * Why WebP is encoded from the originals rather than from the resized JPEGs:
 * re-compressing an already-lossy JPEG stacks a second generation of loss on
 * top of the first. Measured against the original as ground truth, WebP from
 * source came out both smaller AND closer to the original than WebP derived
 * from the shipping JPEG.
 *
 * Adding a photo: drop the full-size file in assets-src/, add an entry to
 * TARGETS below, run `npm run images`, then reference it from the HTML inside
 * a <picture> with a .webp <source> and the .jpg as the <img> fallback.
 *
 * sharp is deterministic, so re-running with unchanged sources rewrites
 * byte-identical files and git shows no diff.
 */
import sharp from 'sharp';
import { mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'assets-src');

const JPEG = { quality: 82, mozjpeg: true, progressive: true };
const WEBP = { quality: 80, effort: 6 };
const PNG = { compressionLevel: 9 };
const NAVY = { r: 15, g: 23, b: 42, alpha: 1 };

/** Max width each image is served at (roughly 2x its largest CSS display size). */
const TARGETS = {
  'Gemini_Generated_Image_ka316gka316gka31.jpg': 2000,
  'kyle.jpg': 928,
  'Before.jpg': 1800,
  'After.jpg': 1800,
  'project1.jpg': 1600,
  'project2.jpg': 1600,
  'project3.jpg': 1600,
  'project4.jpg': 1600,
  'project5.jpg': 1600,
  'project6.jpg': 1600,
  'Gold.png': 1200,
};

/** WebP is only worth a second file when it is meaningfully smaller. */
const MIN_WEBP_SAVING = 0.05;

const kb = (n) => (n / 1024).toFixed(1).padStart(8) + ' KB';

if (!existsSync(SRC)) {
  console.error(`Missing ${SRC}. The full-resolution originals live there.`);
  process.exit(1);
}

await mkdir(ROOT, { recursive: true });

let totalPrimary = 0;
let totalWebp = 0;
const skipped = [];

console.log('source'.padEnd(46) + 'primary'.padStart(11) + 'webp'.padStart(14) + '   saving');

for (const [name, width] of Object.entries(TARGETS)) {
  const src = join(SRC, name);
  if (!existsSync(src)) {
    console.error(`  ! ${name} not found in assets-src/ - skipping`);
    continue;
  }

  const isPng = name.toLowerCase().endsWith('.png');
  const base = sharp(src).rotate().resize({ width, withoutEnlargement: true });

  // Primary (the <img> fallback)
  const primary = await (isPng ? base.clone().png(PNG) : base.clone().jpeg(JPEG)).toBuffer();
  await writeFile(join(ROOT, name), primary);

  // WebP companion, encoded from the same original rather than from `primary`
  const webpName = name.replace(/\.(jpe?g|png)$/i, '.webp');
  const webp = await base.clone().webp(WEBP).toBuffer();

  const saving = 1 - webp.length / primary.length;
  const keep = saving >= MIN_WEBP_SAVING;

  if (keep) {
    await writeFile(join(ROOT, webpName), webp);
    totalWebp += webp.length;
  } else {
    skipped.push({ name, webpName, saving });
    totalWebp += primary.length; // no webp served for this one
  }
  totalPrimary += primary.length;

  console.log(
    name.padEnd(46) +
      kb(primary.length) +
      (keep ? kb(webp.length) : '        --   ') +
      (keep ? `  -${(saving * 100).toFixed(0)}%` : '   (skipped)')
  );
}

// --- Favicons, all derived from the one oversized source icon ---
const faviconSrc = join(SRC, 'favicon.png');
if (existsSync(faviconSrc)) {
  const square = await sharp(faviconSrc)
    .resize(512, 512, { fit: 'contain', background: NAVY })
    .png()
    .toBuffer();

  const icons = [
    ['favicon.png', 32, false],
    ['favicon-192.png', 192, false],
    ['apple-touch-icon.png', 180, true], // iOS has no transparency, so flatten
  ];

  for (const [outName, size, flatten] of icons) {
    let pipe = sharp(square).resize(size, size, flatten ? { fit: 'contain', background: NAVY } : {});
    if (flatten) pipe = pipe.flatten({ background: NAVY });
    const buf = await pipe.png(PNG).toBuffer();
    await writeFile(join(ROOT, outName), buf);
    console.log(outName.padEnd(46) + kb(buf.length));
  }
}

console.log(
  `\nServed weight: ${kb(totalPrimary)} as JPEG/PNG -> ${kb(totalWebp)} where WebP is supported ` +
    `(-${((1 - totalWebp / totalPrimary) * 100).toFixed(0)}%)`
);

if (skipped.length) {
  console.log(
    `\nNo WebP written for ${skipped.length} image(s) - under the ${MIN_WEBP_SAVING * 100}% threshold, ` +
      `so a second file is not worth it:`
  );
  for (const s of skipped) {
    console.log(`  ${s.name}  (webp would be ${(s.saving * 100).toFixed(0)}% smaller)`);
  }
  console.log('  Make sure the HTML has no <source> pointing at these.');
}
