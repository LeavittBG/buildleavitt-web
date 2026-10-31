"""The Pioneer I - FIRST FLOOR OPTIONS, vignette 'OPTIONAL MORNING ROOM' (page 3, xref 23).
Source raster 1252x585 px, 438 dpi, ~37.8 px/ft. Traced walls/windows/linework; lettering re-set.
Follows the first-floor change (Kyle, October 31, 2026): the kitchen peninsula is gone and the
counter run carries on to its old outer face (x 840) under the raised bar; wall cabinets continue."""
import sys
import blib as B
hairlines = B.hairlines

PAGE, XREF = 3, 23
IMG = None   # set by draw()
TEXT = [(515, 195, 930, 295)]
PENINSULA = [(718, 489, 848, 585)]


def kitchen(c):
    N = B.NAVY
    B.counter(c, [(718, 484), (840, 484), (840, 561), (718, 561)])
    c.line(718, 487, 718, 558, 0.9, color='#ffffff')                 # join with the existing run
    c.line(728, 521, 834, 521, 0.6, color=N, dash=c.dash(3, 2))      # wall cabinets


def labels(c):
    L = B.label
    L(c, 722, 245, 'OPTIONAL MORNING ROOM', '29\'-4" × 11\'-6"')


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
