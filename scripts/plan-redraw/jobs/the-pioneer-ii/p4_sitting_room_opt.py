"""The Pioneer II - SECOND FLOOR, "Optional Sitting Room" vignette (page 4, image xref 26).

Source raster 941x555 px placed at 141 x 83.3 pt, i.e. 480 px per paper inch; its pixel scale is
the main plan's (about 37.8 px/ft), so B.K is 480 and line weights and type print at the main
plan's paper sizes (as The Pioneer I's vignette on this page). Mapping from the main second-floor
raster: x_v = x - 1349, y_v = y - 1433 (bedroom 4 bath tub, 101 px wide in both). The bath's tub
is redrawn as the plain rectangular tub of the main plan; traced walls and linework otherwise.
"""
import blib as B

B.K = 480.0
B.PXFT = 37.8
PAGE, XREF = 4, 26
TEXT = [(395, 245, 620, 385)]
TUB = [(292, 0, 388, 82)]


def draw(c, img):
    walls, wins = B.trace(img)
    drop = TEXT + TUB
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.tub(c, 1638 - 1349, 1334 - 1433, 1739 - 1349, 1515 - 1433)
    B.draw_plan_walls(c, walls, wins)
    B.label(c, 508, 278, 'OPTIONAL\nSITTING ROOM', '9\'-1" × 9\'-6"')
