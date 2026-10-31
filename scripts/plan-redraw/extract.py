"""Pull the raster floor-plan drawings out of a brochure PDF, on white, for redrawing.

  python3 scripts/plan-redraw/extract.py assets-src/plans/originals/the-pioneer-i.pdf WORKDIR

Writes WORKDIR/p<page>_x<xref>.png for every drawing image (the navy header band and the logos
are skipped by size) and prints each image's page, xref, pixel size and rectangle on the page.
The images carry a soft mask; it is composited over white here, or the whole drawing reads navy.
"""
import os
import sys

import pymupdf
from PIL import Image

SKIP_WIDTHS = {480, 2984}      # Leavitt logo and the header band, on every brochure page


def extract(pdf, work):
    os.makedirs(work, exist_ok=True)
    d = pymupdf.open(pdf)
    out = []
    for pno in range(1, len(d)):                         # page 1 is the cover rendering
        page = d[pno]
        for im in page.get_images(full=True):
            xref, smask, w, h = im[0], im[1], im[2], im[3]
            if w in SKIP_WIDTHS:
                continue
            base = pymupdf.Pixmap(d, xref)
            mode = 'RGB' if base.n - base.alpha >= 3 else 'L'
            rgb = Image.frombytes(mode, (base.width, base.height), base.samples).convert('RGB')
            if smask:
                m = pymupdf.Pixmap(d, smask)
                alpha = Image.frombytes('L', (m.width, m.height), m.samples)
                bg = Image.new('RGB', rgb.size, 'white')
                bg.paste(rgb, (0, 0), alpha)
                rgb = bg
            fn = os.path.join(work, f'p{pno + 1}_x{xref}.png')
            rgb.save(fn)
            r = page.get_image_rects(xref)[0]
            out.append((pno + 1, xref, w, h, (round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1))))
            print(f'page {pno + 1}  xref {xref}  {w}x{h}  rect {out[-1][4]}  -> {fn}')
    return out


if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2])
