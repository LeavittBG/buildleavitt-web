"""The Pioneer I - FIRST FLOOR OPTIONS, vignette 'OPTIONAL CONSERVATORY' (page 3, xref 19).
Source raster 872x1011 px, 438 dpi, ~37.8 px/ft. Traced walls/windows/linework; lettering re-set.
Nothing dated in this vignette; no layout changes."""
import sys
import blib as B
hairlines = B.hairlines

PAGE, XREF = 3, 19
IMG = None   # set by draw()
TEXT = [(100, 365, 140, 645), (340, 470, 680, 502), (300, 640, 720, 740)]


def labels(c):
    L, S = B.label, B.small
    L(c, 510, 690, 'OPTIONAL\nCONSERVATORY', '13\'-6" × 21\'-1"')
    S(c, 510, 488, 'OPTIONAL CATHEDRAL CEILING', size=3.6, color=B.OPT)
    S(c, 121, 505, 'OPTIONAL GAS FIREPLACE', size=3.6, rotate=-90)


def _draw(c):
    walls, wins = B.trace(IMG)
    DROP = TEXT
    nv, gr = B.lineart(IMG, walls, drop=DROP)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hairlines(IMG, walls, DROP), B.NAVY)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
    return wins


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
