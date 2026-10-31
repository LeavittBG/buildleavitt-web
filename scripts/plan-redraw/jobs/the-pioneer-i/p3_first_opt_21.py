"""The Pioneer I - FIRST FLOOR OPTIONS, vignette 'OPTIONAL 2'-0" REAR EXTENSION AND 4'-0" FAMILY
ROOM EXTENSION' (page 3, xref 21). Source raster 2301x684 px, 438 dpi, ~37.8 px/ft.
Traced walls/windows/linework; lettering re-set. Follows the first-floor change (Kyle, October 31,
2026): the kitchen peninsula is gone and the top counter run carries on to its old outer face
(x 1891); wall cabinets continue over it."""
import sys
import blib as B
hairlines = B.hairlines

PAGE, XREF = 3, 21
IMG = None   # set by draw()
TEXT = [(660, 320, 920, 480), (100, 535, 375, 650), (1380, 585, 1645, 684), (1930, 580, 2230, 684)]
PENINSULA = [(1772, 489, 1900, 684)]


def kitchen(c):
    N = B.NAVY
    B.counter(c, [(1772, 487), (1891, 487), (1891, 562), (1772, 562)])
    c.line(1772, 489, 1772, 560, 0.9, color='#ffffff')               # join with the existing run
    c.line(1782, 523, 1884, 523, 0.6, color=N, dash=c.dash(3, 2))    # wall cabinets


def labels(c):
    L = B.label
    L(c, 790, 400, 'TWO-STORY\nFAMILY ROOM', '18\'-1" × 21\'-0"')
    L(c, 238, 592, 'LIBRARY', '10\'-10" × 15\'-2"')
    L(c, 1510, 632, 'KITCHEN', '19\'-8" × 15\'-2"')
    L(c, 2078, 632, 'BREAKFAST NOOK', '10\'-0" × 15\'-2"')


def _draw(c):
    walls, wins = B.trace(IMG)
    DROP = TEXT + PENINSULA
    nv, gr = B.lineart(IMG, walls, drop=DROP)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hairlines(IMG, walls, DROP), B.NAVY)
    kitchen(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
    return wins


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
