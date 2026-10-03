/**
 * Prints a src/plans.json entry for every PDF in assets-src/plans/ that is not
 * in there yet, so a new brochure does not have to be typed out by hand.
 *
 *   node scripts/scaffold-plans.mjs
 *
 * Written for the brochure template Leavitt adopted in October 2026: page 1 is
 * the cover, with the front elevation and its caption ("ELEVATION C - MODERN
 * FARMHOUSE / with Stone, Board & Batten and Siding"), and every later page
 * prints its title in the header band ("FIRST FLOOR", "BASEMENT OPTIONS").
 * Those brochures have clean text, so pdftotext reads both reliably. (The
 * brochures before them carried hidden leftover text layers and had to be read
 * through their document outline instead; the new ones have no outline.)
 *
 * The result is a starting point, not the last word: specs are left empty -
 * they come from Leavitt's own figures and are never read off a brochure - and
 * every entry should be checked against the rendered pages before it is
 * committed. tests/plans.test.js checks each label against its page's title.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve, basename } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'assets-src', 'plans');

const { models } = JSON.parse(readFileSync(join(ROOT, 'src', 'plans.json'), 'utf8'));
const known = new Set(models.map((m) => m.slug));

const titleCase = (s) => s.toLowerCase().split(/([\s-]+)/)
  .map((w) => (/^(i|ii|iii|iv)$/.test(w) ? w.toUpperCase() : w.replace(/^\w/, (c) => c.toUpperCase())))
  .join('');

const pageText = (pdf, page) => execFileSync('pdftotext',
  ['-f', String(page), '-l', String(page), '-layout', pdf, '-'], { encoding: 'utf8' })
  .split('\n').map((l) => l.trim()).filter(Boolean);

const out = [];

for (const file of readdirSync(SRC).filter((f) => f.toLowerCase().endsWith('.pdf')).sort()) {
  const slug = basename(file, '.pdf');
  if (known.has(slug)) continue;
  const pdf = join(SRC, file);
  const pageCount = Number(/Pages:\s*(\d+)/.exec(execFileSync('pdfinfo', [pdf], { encoding: 'utf8' }))[1]);

  // The cover caption becomes the elevation's label, written the way the
  // existing labels are: "Elevation C – Modern Farmhouse w/ Stone, ...".
  const cover = pageText(pdf, 1);
  const at = cover.findIndex((l) => /^ELEVATION\b/i.test(l));
  const caption = at < 0 ? null
    : `${titleCase(cover[at]).replace(/\s+[—–-]\s+/, ' – ')}${/^with\s/i.test(cover[at + 1] || '') ? ' ' + cover[at + 1].replace(/^with\s/i, 'w/ ') : ''}`;
  const pages = [{ page: 1, id: 'elevation', label: caption ?? 'TODO read the caption off page 1' }];

  for (let page = 2; page <= pageCount; page++) {
    const title = (pageText(pdf, page)[0] || '').split(/\s{2,}/).pop();
    if (!title) { console.error(`  ! ${slug} p${page}: no title in the header band`); continue; }
    pages.push({
      page,
      id: title.toLowerCase().replace(/\s+/g, '-').replace(/^elevations$/, 'other-elevations'),
      label: titleCase(title),
    });
  }

  // A plan set with no second-floor sheet is a single-story house. That is
  // read off the set itself; nothing else about the house is guessed.
  const stories = pages.some((p) => /second-floor$/.test(p.id)) ? 2 : 1;

  out.push({
    slug,
    name: titleCase(slug.replace(/-/g, ' ')),
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
console.error(`\n${out.length} entry(ies) written to stdout. Fill in the specs from Leavitt's figures, check every label against the pages, then paste into src/plans.json.`);
