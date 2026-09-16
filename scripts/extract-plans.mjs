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
 * Each brochure follows the same template: a title banner, the drawing, then a
 * logo block at the foot of the page. We render the page, crop away the banner
 * and the logo, then trim the remaining whitespace so the drawing fills the
 * frame. The bands below are fractions of page height and were read off the
 * rendered pages - if a future brochure uses a different template, its images
 * will look off and the band will need adjusting for it.
 *
 * The drawings are vector art in the PDF, so they are rendered at 200dpi and
 * downscaled, which keeps the linework crisp.
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

// Vertical slice of each page to keep, as a fraction of page height.
const BAND = {
  elevation: [null, 0.71], // top is measured per page (see findBannerBottom), above the logo block
  floor: [0.09, 0.83],     // keeps the optional-feature callouts alongside the plan
};

// How far down the page to look for the title banner, and how much of a row has
// to be non-white before it counts as a solid rule rather than part of a drawing.
const BANNER_SEARCH = 0.20;
const RULE_COVERAGE = 0.9;
const RULE_LUMA = 225;

/**
 * Finds the bottom of the title banner, as a pixel row.
 *
 * An elevation is cropped to start just under the banner. This used to be the
 * fixed fraction 0.16, which worked but needed a per-model override: the navy
 * banner ends at 0.130 on fifteen of the brochures, but the-visionary has a gold
 * rule below it at 0.161, and a crop at 0.16 left that rule in the image.
 * Measuring the banner per page gets both cases right with no tuning, and it
 * will keep working on a brochure whose banner is a different height.
 *
 * Looks for rows that are almost entirely non-white across the full page width -
 * that is a printed rule. A drawing never covers a whole row that densely.
 *
 * The crop only sets an upper bound; trim() below is what decides the final top
 * edge, so a generous band costs nothing.
 */
async function findBannerBottom(file) {
  const { data, info } = await sharp(file)
    .flatten({ background: '#ffffff' })
    .raw()
    .toBuffer({ resolveWithObject: true });
  const { width, height, channels } = info;

  let last = -1;
  for (let y = 0; y < Math.round(height * BANNER_SEARCH); y++) {
    let ink = 0;
    for (let x = 0; x < width; x++) {
      const i = (y * width + x) * channels;
      const luma = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
      if (luma < RULE_LUMA) ink++;
    }
    if (ink / width > RULE_COVERAGE) last = y;
  }
  // +2 so the rule's own antialiasing does not survive into the image.
  return last < 0 ? 0 : last + 2;
}

const WEBP = { quality: 82, effort: 6 };
// These are line drawings - black linework, a little grey hatch, white paper -
// so a palette costs nothing and saves ~44% over truecolour (9.0MB -> 5.1MB
// across the set). Measured worst-case RMSE against the truecolour render is
// 0.13/255, i.e. invisible; dropping to 16 colours saves another 2.3MB but
// takes the worst case to 2.15, which is not worth it on a drawing someone may
// open full size and zoom into. Dithering is off: it only adds noise to flat
// paper and makes the file bigger.
const PNG = { compressionLevel: 9, palette: true, colours: 64, dither: 0, effort: 10 };
const MAX_WIDTH = 1600;
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

    // A page may override the band in plans.json when its sheet does not follow
    // the usual template - e.g. a title banner that sits lower than the rest.
    const [top, bottom] = band || (id.startsWith('elevation') ? BAND.elevation : BAND.floor);
    const meta = await sharp(rendered).metadata();

    // A null top means "measure it": used for elevations, where a fixed fraction
    // cut the roof off the taller houses.
    const topPx = top === null
      ? await findBannerBottom(rendered)
      : Math.round(meta.height * top);

    const extract = {
      left: 0,
      top: topPx,
      width: meta.width,
      height: Math.round(meta.height * bottom) - topPx,
    };

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
    const png = await base.clone().png(PNG).toBuffer();
    const dims = await sharp(webp).metadata();

    writeFileSync(join(IMG, `${name}.webp`), webp);
    writeFileSync(join(IMG, `${name}.png`), png);

    manifest[slug][id] = { file: name, width: dims.width, height: dims.height, label };

    console.log(`   p${page} -> ${name}  ${dims.width}x${dims.height}  ` +
      `webp ${kb(webp.length)} / png ${kb(png.length)}  "${label}"`);
  }

  copyFileSync(src, join(PDF, `${slug}.pdf`));
  console.log(`   pdf -> plans/pdf/${slug}.pdf  ${kb(statSync(src).size)}`);
}

rmSync(TMP, { recursive: true, force: true });

writeFileSync(join(ROOT, 'src', 'plan-images.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`\nWrote src/plan-images.json for ${Object.keys(manifest).length} models.`);

if (missing) {
  console.error(`\n${missing} page(s) could not be produced.`);
  process.exit(1);
}
