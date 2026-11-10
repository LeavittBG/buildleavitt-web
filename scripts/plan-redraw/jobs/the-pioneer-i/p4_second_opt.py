"""The Pioneer I - SECOND FLOOR, "Optional Extended W.I.C." vignette (page 4, image xref 26).

Source raster 940x555 px, placed on the page at 141 x 83.3 pt, i.e. 480 px per paper inch (the
main plans are 438). Its PIXEL scale is the main plan's (walls 22-23 px thick in both; owner's
bath 344 px wide inside here, 347 px there), about 37.8 px/ft; it is just printed smaller.
B.K is set to 480 so line weights and type print at the same paper sizes as on the main plan.

Mapping from the main second-floor raster (owner's bath right wall inner face 2259 -> 907,
bath floor edge 1590 -> 82): x_v = x - 1352, y_v = y - 1508.
The strip of owner's bath along the top showed the corner soaker tub; it now shows the bottom of
the walk-in shower drawn in p1_second.py (bench, glass panel, drain), to match.
"""
import sys
import blib as B

B.K = 480.0
B.PXFT = 37.8
PAGE, XREF = 4, 26
IMG = None   # set by draw()
def m(x, y):
    """main second-floor px -> this vignette's px"""
    return (x - 1352.0, y - 1508.0)


TEXT = [(436, 262, 600, 358)]
TUB = [(712, 0, 905, 80)]


def shower(c):
    N = B.NAVY
    x0, y0 = m(2062, 1400)
    x1, y1 = m(2259, 1590)
    y0 = -4.0                                           # crop edge
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill='#ffffff')
    c.line(x0, y0, x0, y1, 0.45, color=N)
    k = B.PXFT / 12.0
    bx0 = m(2062 + 40, 0)[0]
    B.box(c, bx0, y1 - 15 * k, x1, y1, sw=0.45)
    B.small(c, (bx0 + x1) / 2, y1 - 7.5 * k, 'BENCH', size=3.0, color=B.GREY)
    gy1 = m(0, 1588)[1]
    c.line(x0, gy1, x0, y0, 1.1, color=N)                # glass panel
    c.rect(x1 - 6 * k, y0, 1.6 * k, (y1 - 18 * k) - y0, sw=0.35, color=N)   # linear drain


def _draw(c):
    walls, wins = B.trace(IMG)
    drop = TEXT + TUB
    nv, gr = B.lineart(IMG, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    shower(c)
    B.draw_plan_walls(c, walls, wins)
    B.label(c, 515, 310, 'OPTIONAL\nW.I.C.', name_pt=5.0)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
