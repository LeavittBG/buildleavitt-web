/**
 * Turns the model brochures in assets-src/plans/*.pdf into web images.
 *
 *   npm run plans:images
 *
 * Which PDF page is which sheet, and what each sheet is called, comes from
 * src/plans.json - not from the PDF. These brochures carry leftover content
 * layers that pdftoppm correctly does not render but pdftotext still returns,
 * so extracted text names the wrong sheet. See the _README in that file.
 *
 * Each page is furniture around one drawing: a title banner or box, the drawing,
 * a caption under it on the elevation sheets, then a logo block and a
 * disclaimer at the foot. We keep the drawing and drop the rest by measuring
 * where the ink actually is - see findDrawing.
 *
 * The drawings are rendered at 200dpi and downscaled, which keeps the linework
 * crisp on the floor plans and the rendering smooth on the elevations.
 *
 * Outputs to plans/img/ as WebP plus a PNG fallback, mirroring the site's
 * existing <picture> approach. Also copies the source PDF to plans/pdf/ for the
 * download link, and writes the measured pixel sizes to src/plan-images.json so
 * every generated <img> can carry real width/height and reserve its space.
 */
import sharp from 'sharp';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync, rmSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'assets-src', 'plans');
const IMG = join(ROOT, 'plans', 'img');
const PDF = join(ROOT, 'plans', 'pdf');
const TMP = join(ROOT, '.plan-render-tmp');

// A row counts as having ink if this fraction of its pixels are not paper-white.
const INK_LUMA = 245;
const INK_COVERAGE = 0.004;
// Blocks closer together than this (as a fraction of page height) are one block.
const BLOCK_GAP = 0.008;
// Breathing room kept around the drawing before trim() tightens it.
const PAD = 0.004;

/**
 * Finds the drawing on a page and returns its {top, height} in pixels.
 *
 * Every sheet is furniture around one drawing. Measuring the rows that carry
 * ink splits the page into blocks, and on all four page types the drawing is by
 * far the tallest one:
 *
 *   elevation sheet   banner .041-.130 | RENDERING .25-.63 | caption .649-.678 | logo .811-.958
 *   floor plan sheet  DRAWING .063-.845 | logo .857-.908 | disclaimer .918-.935
 *
 * So "keep the tallest block" drops the banner, the logo and the disclaimer on
 * every sheet, and on the elevation sheets it also drops the caption naming the
 * elevation and exterior style, which Leavitt asked to keep off the site.
 *
 * This replaced a pair of hand-tuned fractions. Those needed re-tuning whenever
 * the brochure template changed - and it changed completely when the plans were
 * re-rendered, moving the banner, the drawing and the foot of every page.
 * Measuring costs one pass over the pixels and needs no tuning at all.
 */
async function findDrawing(file) {
  const { data, info } = await sharp(file)
    .flatten({ background: '#ffffff' })
    .raw()
    .toBuffer({ resolveWithObject: true });
  const { width, height, channels } = info;

  const inked = [];
  for (let y = 0; y < height; y++) {
    let n = 0;
    for (let x = 0; x < width; x++) {
      const i = (y * width + x) * channels;
      const luma = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
      if (luma < INK_LUMA) n++;
    }
    inked.push(n / width > INK_COVERAGE);
  }

  const blocks = [];
  let start = null;
  for (let y = 0; y < height; y++) {
    if (inked[y] && start === null) start = y;
    else if (!inked[y] && start !== null) { blocks.push([start, y - 1]); start = null; }
  }
  if (start !== null) blocks.push([start, height - 1]);

  // A drawing has internal white gaps - between a callout and the main plan, or
  // between the roof and the landscaping. Join anything separated by a hairline.
  const gap = Math.round(height * BLOCK_GAP);
  const merged = [];
  for (const b of blocks) {
    const last = merged[merged.length - 1];
    if (last && b[0] - last[1] <= gap) last[1] = b[1];
    else merged.push([...b]);
  }
  if (!merged.length) return { top: 0, height };

  const [top, bottom] = merged.reduce((a, b) => (b[1] - b[0] > a[1] - a[0] ? b : a));
  const pad = Math.round(height * PAD);
  const t = Math.max(0, top - pad);
  return { top: t, height: Math.min(height, bottom + pad) - t };
}

const WEBP = { quality: 82, effort: 6 };
const PNG_TRUECOLOUR = { compressionLevel: 9 };
const PNG_PALETTE = { compressionLevel: 9, palette: true, colours: 64, dither: 0, effort: 10 };
// A palette is a big win on a line drawing and a bad trade on a photographic
// one. This set now has both: the floor plans are still black linework on white,
// but the elevations are full-colour renderings. So rather than assume, encode
// both ways and keep the palette only when it is genuinely smaller and the error
// against the truecolour version is imperceptible.
//
// The two kinds separate cleanly when measured: across the set the floor plans
// score 1.07-1.48 and the renderings 2.80-3.69, with nothing in between. The
// threshold sits in that gap. A floor plan at the top of its range was checked
// by eye at zoom against its truecolour version and is indistinguishable, while
// halving the file (230KB -> 105KB).
const PALETTE_MAX_RMSE = 2.0;   // out of 255
const MAX_WIDTH = 1600;

/** Root-mean-square difference between two encoded images, in levels of 255. */
async function rmse(a, b) {
  const [A, B] = await Promise.all([
    sharp(a).greyscale().raw().toBuffer(),
    sharp(b).greyscale().raw().toBuffer(),
  ]);
  let sum = 0;
  for (let i = 0; i < A.length; i++) { const d = A[i] - B[i]; sum += d * d; }
  return Math.sqrt(sum / A.length);
}

async function encodePng(source) {
  const full = await sharp(source).png(PNG_TRUECOLOUR).toBuffer();
  const pal = await sharp(source).png(PNG_PALETTE).toBuffer();
  if (pal.length >= full.length) return { buffer: full, note: 'truecolour (palette no smaller)' };
  const err = await rmse(full, pal);
  if (err > PALETTE_MAX_RMSE) return { buffer: full, note: `truecolour (palette RMSE ${err.toFixed(2)})` };
  return { buffer: pal, note: `palette -${(100 - (pal.length / full.length) * 100).toFixed(0)}%` };
}
const kb = (n) => (n / 1024).toFixed(0).padStart(5) + ' KB';

const { models } = JSON.parse(readFileSync(join(ROOT, 'src', 'plans.json'), 'utf8'));

for (const d of [IMG, PDF, TMP]) mkdirSync(d, { recursive: true });

const manifest = {};
let missing = 0;

for (const model of models) {
  const { slug } = model;
  const src = join(SRC, `${slug}.pdf`);
  if (!existsSync(src)) {
    console.error(`  ! ${slug}: no assets-src/plans/${slug}.pdf`);
    missing++;
    continue;
  }

  const info = execFileSync('pdfinfo', [src], { encoding: 'utf8' });
  const pageCount = Number(/^Pages:\s*(\d+)/m.exec(info)?.[1] || 0);

  console.log(`\n${model.name}  (${pageCount} pages in PDF, ${model.pages.length} used)`);
  manifest[slug] = {};

  execFileSync('pdftoppm', ['-r', '200', '-png', src, join(TMP, slug)]);

  for (const { page, id, label, band } of model.pages) {
    if (page > pageCount) {
      console.error(`  ! ${slug} page ${page}: PDF only has ${pageCount} pages`);
      missing++;
      continue;
    }

    // pdftoppm zero-pads the page number to the width of the page count
    const padded = String(page).padStart(String(pageCount).length, '0');
    const rendered = [join(TMP, `${slug}-${padded}.png`), join(TMP, `${slug}-${page}.png`)]
      .find((f) => existsSync(f));
    if (!rendered) {
      console.error(`  ! ${slug} page ${page}: render missing`);
      missing++;
      continue;
    }

    const meta = await sharp(rendered).metadata();

    // A page may override the measurement from plans.json, as [top, bottom]
    // fractions of page height, if a future brochure ever defeats findDrawing.
    const box = band
      ? { top: Math.round(meta.height * band[0]),
          height: Math.round(meta.height * (band[1] - band[0])) }
      : await findDrawing(rendered);

    const extract = { left: 0, width: meta.width, ...box };

    // Two passes on purpose: extract and trim in a single pipeline makes sharp
    // evaluate the crop against the trimmed dimensions, which throws
    // "bad extract area". Crop to a buffer first, then trim that.
    const cropped = await sharp(rendered).extract(extract).png().toBuffer();

    const base = sharp(cropped)
      .trim({ threshold: 12 })                 // tighten onto the linework
      .resize({ width: MAX_WIDTH, withoutEnlargement: true })
      .flatten({ background: '#ffffff' });

    const name = `${slug}-${id}`;
    const webp = await base.clone().webp(WEBP).toBuffer();
    const { buffer: png, note } = await encodePng(await base.clone().png().toBuffer());
    const dims = await sharp(webp).metadata();

    writeFileSync(join(IMG, `${name}.webp`), webp);
    writeFileSync(join(IMG, `${name}.png`), png);

    manifest[slug][id] = { file: name, width: dims.width, height: dims.height, label };

    console.log(`   p${page} -> ${name}  ${dims.width}x${dims.height}  ` +
      `webp ${kb(webp.length)} / png ${kb(png.length)}  ${note}`);
  }

  copyFileSync(src, join(PDF, `${slug}.pdf`));
  console.log(`   pdf -> plans/pdf/${slug}.pdf  ${kb(statSync(src).size)}`);
}

rmSync(TMP, { recursive: true, force: true });

// The Leavitt Standard sheet is not a plan, but it is offered for download from
// the same place, so it rides along out of assets-src/ into the published folder.
const STANDARD_PDF = join(ROOT, 'assets-src', 'leavitt-standard.pdf');
if (existsSync(STANDARD_PDF)) {
  copyFileSync(STANDARD_PDF, join(PDF, 'leavitt-standard.pdf'));
  console.log(`\npdf -> plans/pdf/leavitt-standard.pdf  ${kb(statSync(STANDARD_PDF).size)}`);
} else {
  console.error('\n  ! assets-src/leavitt-standard.pdf missing - the download link on /plans/ will 404');
  missing++;
}

writeFileSync(join(ROOT, 'src', 'plan-images.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`\nWrote src/plan-images.json for ${Object.keys(manifest).length} models.`);

if (missing) {
  console.error(`\n${missing} page(s) could not be produced.`);
  process.exit(1);
}
