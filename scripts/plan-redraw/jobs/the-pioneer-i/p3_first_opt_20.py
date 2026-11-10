"""The Pioneer I - FIRST FLOOR OPTIONS, vignette 'OPTIONAL IN-LAW SUITE' (page 3, xref 20).
Source raster 649x1010 px, 438 dpi, ~37.8 px/ft. Traced walls/windows/linework; lettering re-set.
The optional bath keeps its tub/shower and vanity (secondary bath). The powder-room toilet at the
right edge belongs to the main house; its sink is outside this vignette."""
import sys
import blib as B
hairlines = B.hairlines

PAGE, XREF = 3, 20
IMG = None   # set by draw()
TEXT = [(135, 195, 230, 290), (365, 145, 480, 240), (85, 540, 480, 640)]


def labels(c):
    L = B.label
    L(c, 280, 590, 'OPTIONAL\nIN-LAW SUITE', '13\'-6" × 15\'-5"')
    L(c, 183, 240, 'OPT.\nBATH', name_pt=4.6)
    L(c, 422, 192, 'OPT.\nW.I.C.', name_pt=4.6)


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
