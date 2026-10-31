"""The Pioneer I - FIRST FLOOR OPTIONS, vignette 'OPTIONAL 3 CAR GARAGE' (page 3, xref 22).
Source raster 1434x916 px, 438 dpi, ~37.8 px/ft (33'-4" inside = 1265 px). Traced walls/windows/
linework; lettering re-set. Follows the first-floor change (Kyle, October 31, 2026): the bench by
the garage entry becomes lockers with a bench, same as /tmp/pw/jobs/p1_first.py lockers()."""
import sys
import blib as B
hairlines = B.hairlines

PAGE, XREF = 3, 22
IMG = None   # set by draw()
TEXT = [(555, 455, 895, 560), (1398, 645, 1440, 780)]
BENCH = [(98, 50, 258, 118)]


def lockers(c):
    N = B.NAVY
    x0, x1, y0, y1 = 102.0, 252.0, 55.0, 112.0
    B.box(c, x0, y0, x1, y1, sw=0.55)
    for i in (1, 2):
        x = x0 + (x1 - x0) * i / 3
        c.line(x, y0, x, y1, 0.45, color=N)
    c.line(x0, y1 - 15, x1, y1 - 15, 0.4, color=N, dash=c.dash(2.5, 1.6))   # bench seat edge
    B.small(c, (x0 + x1) / 2, y0 + 20, 'LOCKERS', size=3.8)


def labels(c):
    L, S = B.label, B.small
    L(c, 727, 508, 'THREE-CAR GARAGE', '33\'-4" × 21\'-0"')
    S(c, 1418, 712, 'OPT. DOOR', size=3.4, color=B.OPT, rotate=-90)


def _draw(c):
    walls, wins = B.trace(IMG, win_drop=[(410, 125, 580, 150)])
    DROP = TEXT + BENCH
    nv, gr = B.lineart(IMG, walls, drop=DROP)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hairlines(IMG, walls, DROP), B.NAVY)
    lockers(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
    return wins


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
