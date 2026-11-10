"""The Pioneer II - FIRST FLOOR OPTIONS, vignette 'OPTIONAL 2'-0" REAR EXTENSION' (page 3, xref 23).
Source raster 2302x532 px, 438 dpi, ~37.8 px/ft. The Pioneer II has no 4'-0" family room
extension, so its family room here has no label; below the family room this picture is The
Pioneer I's matching vignette moved (+1, -151) px (measured). Same change as The Pioneer I's first
floor: the kitchen peninsula is gone and the top counter run carries on to its old outer face,
with wall cabinets over it."""
import blib as B

PAGE, XREF = 3, 23
DX, DY = 1, -151
TEXT = [(100 + DX, 535 + DY, 375 + DX, 650 + DY), (1380 + DX, 585 + DY, 1645 + DX, 532),
        (1930 + DX, 580 + DY, 2230 + DX, 532)]
PENINSULA = [(1772 + DX, 489 + DY, 1900 + DX, 532)]


def kitchen(c):
    x0, x1, y0, y1 = 1772 + DX, 1891 + DX, 487 + DY, 562 + DY
    B.counter(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    c.line(x0, y0 + 2, x0, y1 - 2, 0.9, color='#ffffff')            # join with the existing run
    c.line(x0 + 10, 523 + DY, x1 - 7, 523 + DY, 0.6, color=B.NAVY, dash=c.dash(3, 2))   # wall cabinets


def labels(c):
    L = B.label
    L(c, 238 + DX, 592 + DY, 'LIBRARY', '10\'-10" × 15\'-2"')
    L(c, 1510 + DX, 632 + DY, 'KITCHEN', '19\'-8" × 15\'-2"')
    L(c, 2078 + DX, 632 + DY, 'BREAKFAST NOOK', '10\'-0" × 15\'-2"')


def draw(c, img):
    walls, wins = B.trace(img)
    drop = TEXT + PENINSULA
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    kitchen(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
