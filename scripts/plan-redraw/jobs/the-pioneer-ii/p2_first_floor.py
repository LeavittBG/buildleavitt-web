"""The Pioneer II - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

The Pioneer II's first floor is The Pioneer I's plan with a one-story family room (optional
beamed ceiling, no 4'-0" extension) and slightly different front windows and tray outlines.
Its raster is The Pioneer I's moved up 76 px (measured: the two match to 1.6 grey levels on
average below the family room with y_II = y_I - 76). So every hand-drawn item is The Pioneer I
job's own drawing (straightened stair, vanity, large island, coffee bar, lockers, nook doors),
drawn through a 76 px shift; walls, windows and linework are traced from this image.
"""
import importlib.util
import os
import blib as B
from shapely.geometry import Polygon
from shapely import affinity

PAGE, XREF = 2, 15
DY = -76.0

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p2_first_floor.py')
_s = importlib.util.spec_from_file_location('pioneer_i_first', _p)
P1 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(P1)


def sh(r):
    x0, y0, x1, y1 = r
    return (x0, y0 + DY, x1, y1 + DY)


# Pioneer I's text rects, minus its family-room ones (replaced by FAMROOM below)
TEXT = [sh(r) for r in P1.TEXT if r not in [(1090, 95, 1560, 135), (1190, 530, 1460, 700)]]
FAMROOM = [(1100, 180, 1545, 826)]          # beamed-ceiling lines and the room's lettering
TRAYS = [(628, 1342, 976, 1670), (1548, 1342, 1902, 1670)]
DROP = (TEXT + [sh(r) for r in P1.STAIR + P1.KITCHEN + P1.DESK + P1.BENCH + P1.PDR_SINK + P1.NOOK_DOORS]
        + FAMROOM + TRAYS)
WIN_DROP = [sh(r) for r in P1.WIN_DROP]
STAIR_WALLS = [sh(P1.STAIR_WALLS[0]), affinity.translate(P1.STAIR_WALLS[1], 0, DY)]


def shifted(c, fn):
    c.add(f'<g transform="translate(0 {DY:g})">')
    fn(c)
    c.add('</g>')


def hand_items(c):
    B.vanity(c, 690, 1277, 'up', 24, 19)
    P1.kitchen(c)
    P1.coffee_bar(c)
    B.double_door(c, (2493, 559), (2735, 559), side=1)
    P1.lockers(c)
    P1.stair(c)


def beams(c):
    for x in (1111, 1130, 1247.5, 1266, 1383.5, 1402, 1519.5, 1538.5):
        c.line(x, 182, x, 823, 0.35, color=B.OPT, dash=c.dash(6.1, 2.8))


def labels(c):
    L, S = B.label, B.small
    # centred in each room (Kyle, Oct 31): Pioneer I's centres moved up 76 px
    c.rect(1205, 466, 240, 98, sw=0, fill='#ffffff')         # keep the beam lines off the lettering
    L(c, 1325, 515, 'FAMILY ROOM', '18\'-1" × 17\'-0"', 'OPT. BEAMED CEILING')
    L(c, 765, 734, 'LIBRARY', '10\'-10" × 13\'-2"')
    L(c, 2092, 626, 'KITCHEN', '19\'-8" × 13\'-2"')
    L(c, 2610, 731, 'BREAKFAST\nNOOK', '10\'-0" × 13\'-2"')
    L(c, 802, 1506, 'LIVING ROOM', '13\'-7" × 13\'-10"', 'OPT. TRAY CEILING')
    L(c, 1725, 1506, 'DINING ROOM', '13\'-9" × 13\'-10"', 'OPT. TRAY CEILING')
    L(c, 1262, 1592, 'TWO-STORY\nFOYER')
    L(c, 1455, 1234, 'GALLERY', name_pt=5.4)
    L(c, 2557, 1104, 'LAUNDRY', name_pt=5.4)
    L(c, 2395, 1674, 'TWO-CAR GARAGE', '21\'-4" × 19\'-10"')
    L(c, 1262, 1864, 'CONC. PORCH', name_pt=4.8)
    L(c, 618, 1052, 'PDR.\nROOM', name_pt=4.6)
    L(c, 1745, 1099, 'HALL', name_pt=4.8)
    c.line(1863.5, 1000, 1863.5, 1202, 0.6, color=B.NAVY)       # butler's pantry counter edge
    S(c, 1838, 1100, "BUTLER'S PANTRY", size=3.6, rotate=-90)
    S(c, 2040, 1046, 'PANTRY', size=3.8)
    S(c, 795, 1146, 'CLOSET', size=3.6)
    S(c, 2280, 1222, 'CLOSET', size=3.6, rotate=-90)
    S(c, 2228, 954, 'UP', size=3.8)
    o = B.OPT
    S(c, 2375, 39, 'OPTIONAL MORNING ROOM', size=3.6, color=o)
    S(c, 760, 419, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 2245, 419, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 285, 1572, 'OPT. CONSERVATORY', size=3.6, color=o)
    S(c, 285, 1600, 'OR IN-LAW SUITE', size=3.6, color=o)
    S(c, 1705, 1797, 'ELEVATION D', size=3.4, color=o)
    S(c, 810, 1969, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 1710, 1969, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 3045, 2024, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)
    S(c, 2845, 1072, 'OPT. DOOR', size=3.4, color=o, rotate=-90)
    S(c, 2845, 1932, 'OPT. DOOR', size=3.4, color=o, rotate=-90)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP, add=STAIR_WALLS)
    nv, gr = B.lineart(img, walls, drop=DROP)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, DROP), B.NAVY)
    beams(c)
    shifted(c, hand_items)
    B.draw_plan_walls(c, walls, wins)
    B.dashed_rect(c, 636, 1350, 968, 1662, w=0.45)
    B.dashed_rect(c, 1556, 1350, 1894, 1662, w=0.45)
    labels(c)
