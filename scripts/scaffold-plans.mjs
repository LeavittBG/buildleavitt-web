/**
 * Prints a src/plans.json entry for every PDF in assets-src/plans/ that is not
 * in there yet, so a new brochure does not have to be typed out by hand.
 *
 *   node scripts/scaffold-plans.mjs
 *
 * Page roles come from the PDF's document outline ("The Poet-Foundation"),
 * which is the one machine-readable label in these files that can be trusted.
 * The printed sheet titles cannot: the brochures carry leftover hidden content
 * layers that pdftoppm does not render but pdftotext still returns, so extracted
 * text names the wrong sheet. See the _README in src/plans.json.
 *
 * The outline is a starting point, not the last word. The front elevation's
 * caption is not in the outline at all and is left as a TODO to read off the
 * rendered page, and every generated entry should be checked against the images
 * before it is committed.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve, basename } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'assets-src', 'plans');

// Outline page name -> the file id it becomes and the title printed on the sheet.
const ROLES = [
  [/-Front$/i, 'elevation', null],          // caption varies; must be read off the page
  [/-Foundation$/i, 'floor-1', 'Basement Floor Plan'],
  [/-First Floor$/i, 'floor-2', 'First Floor Plan'],
  [/-Second Floor$/i, 'floor-3', 'Second Floor Plan'],
  [/-Third Floor$/i, 'floor-4', 'Third Floor Plan'],
  [/-Back$/i, 'elevation-2', 'Additional Elevations'],
];

const { models } = JSON.parse(readFileSync(join(ROOT, 'src', 'plans.json'), 'utf8'));
const known = new Set(models.map((m) => m.slug));

const titleCase = (slug) => slug.split('-')
  .map((w) => (/^(i|ii|iii|iv)$/.test(w) ? w.toUpperCase() : w[0].toUpperCase() + w.slice(1)))
  .join(' ');

const out = [];

for (const file of readdirSync(SRC).filter((f) => f.toLowerCase().endsWith('.pdf')).sort()) {
  const slug = basename(file, '.pdf');
  if (known.has(slug)) continue;

  // -i: do not extract the page images. Without it pdftohtml writes every
  // embedded bitmap out as a PNG next to the PDF, which is pure litter here -
  // we only want the outline.
  const xml = execFileSync('pdftohtml', ['-i', '-xml', '-stdout', join(SRC, file)], {
    encoding: 'utf8', maxBuffer: 64 * 1024 * 1024,
  });

  const outline = [...xml.matchAll(/<item page="(\d+)">([^<]*)<\/item>/g)]
    .map((m) => ({ page: Number(m[1]), name: m[2].trim() }));

  if (!outline.length) {
    console.error(`  ! ${slug}: no document outline - this one has to be done by hand`);
    continue;
  }

  const pages = [];
  for (const { page, name } of outline) {
    const role = ROLES.find(([re]) => re.test(name));
    if (!role) {
      console.error(`  ! ${slug} p${page}: unrecognised outline name "${name}"`);
      continue;
    }
    const [, id, label] = role;
    pages.push({ page, id, label: label ?? `TODO read the caption off page ${page}` });
  }

  // A plan set with no second-floor sheet is a single-storey house. That is
  // read off the set itself; nothing else about the house is guessed.
  const stories = pages.some((p) => p.id === 'floor-3') ? 2 : 1;

  out.push({
    slug,
    name: titleCase(slug),
    summary: null,
    specs: { beds: null, baths: null, sqft: null, stories, garage: null },
    pages,
  });
}

if (!out.length) {
  console.error('Nothing new in assets-src/plans/.');
  process.exit(0);
}

console.log(JSON.stringify(out, null, 2)
  .split('\n').map((l) => '    ' + l).join('\n'));
console.error(`\n${out.length} entry(ies) written to stdout. Fill in every TODO, then paste into src/plans.json.`);
