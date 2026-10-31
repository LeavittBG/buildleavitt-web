"""Rebuild a model's brochure with its floor plans redrawn as clean vector drawings.

  python3 scripts/plan-redraw/build.py the-pioneer-i [--keep WORKDIR]
  npm run plans            # then: site images, plans/pdf/ copy, plan pages

Why: the October 2026 brochures carry each floor plan as a picture traced from the architect's
drawings, in a hand-lettered CAD font, with features Leavitt no longer builds (soaker tubs,
pedestal sinks, flared and radius stairs). Kyle asked on October 31, 2026 for clean plans in the
style of his bid sheets, updated to what Leavitt builds now. See CLAUDE.md, "Plan redraws".

How: the untouched brochure is kept in assets-src/plans/originals/<slug>.pdf. Each drawing on it
is an image; extract.py pulls them out, and jobs/<slug>/<name>.py redraws one image in that
image's own pixel coordinates (PAGE and XREF name it; draw(c, img) draws it). Walls, windows and
the plan's own linework are traced from the picture (blib.trace / blib.lineart), so nothing moves;
lettering and the modernised items are drawn by hand. Each drawing is rendered to a one-page PDF
the size of the image, and blib.swap() puts it on the brochure page in exactly the rectangle the
image filled, so the header band, room dimensions, options text and disclaimer are untouched.
The result is written over assets-src/plans/<slug>.pdf.

Needs: python3 with pymupdf pikepdf shapely opencv-python-headless scipy pillow playwright,
poppler (pdftoppm), a Chromium (CHROMIUM_PATH, default /opt/pw-browsers/chromium), and the fonts:
  (cd scripts/plan-redraw && mkdir -p fonts && cd fonts && npm init -y >/dev/null && \\
   npm install @fontsource/roboto-condensed @fontsource/montserrat @fontsource/cinzel)
"""
import glob
import importlib.util
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'jobs'))   # shared job helpers (_bhelp.py)
import blib as B          # noqa: E402
import extract as X       # noqa: E402


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build(slug, work=None):
    src = os.path.join(ROOT, 'assets-src', 'plans', 'originals', f'{slug}.pdf')
    dst = os.path.join(ROOT, 'assets-src', 'plans', f'{slug}.pdf')
    jobs = sorted(glob.glob(os.path.join(HERE, 'jobs', slug, '*.py')))
    if not os.path.exists(src):
        sys.exit(f'no original brochure at {src}')
    if not jobs:
        sys.exit(f'no jobs in jobs/{slug}/')
    work = work or tempfile.mkdtemp(prefix=f'redraw-{slug}-')
    os.makedirs(os.path.join(work, 'out'), exist_ok=True)
    found = {(p, x) for p, x, *_ in X.extract(src, work)}
    reps = []
    defaults = (B.K, B.PXFT)
    for path in jobs:
        B.K, B.PXFT = defaults          # a job may change them for its own image (480 dpi vignettes)
        job = load(path)
        img = os.path.join(work, f'p{job.PAGE}_x{job.XREF}.png')
        assert (job.PAGE, job.XREF) in found, f'{path}: page {job.PAGE} has no image {job.XREF}'
        c = B.new(img)
        job.draw(c, img)
        out = os.path.join(work, 'out', os.path.basename(path)[:-3] + '.pdf')
        B.render(c, out)
        reps.append((job.PAGE, job.XREF, out))
        print('drew', os.path.relpath(path, ROOT), '->', out)
    B.K, B.PXFT = defaults
    missing = found - {(p, x) for p, x, _ in reps}
    if missing:
        print('NOTE: images left as they were (no job):', sorted(missing))
    B.swap(src, reps, dst)
    print('wrote', os.path.relpath(dst, ROOT), f'(renders and side-by-sides in {work})')
    for p, x, out in reps:
        B.side_by_side(os.path.join(work, f'p{p}_x{x}.png'), out, out[:-4] + '_vs_original.png',
                       None, 0.5)
    return dst


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    keep = a[a.index('--keep') + 1] if '--keep' in a else None
    build(a[0], keep)
