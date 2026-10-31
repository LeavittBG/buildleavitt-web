"""The Daydreamer - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2844x2378 px placed at 389.4 dpi, 37.8 px/ft like The Pioneer I (garage 22'-10"
wide inside = 863 px).

Kept by tracing: walls, windows, doors, cabinets, appliances, the upper flight, dashed options.
Changed (Kyle, October 31, 2026):
  - main stair: the lower flight's rounded (bullnose) first step becomes a square-cut step with
    square newels, in place; treads redrawn clean
  - powder room: pedestal sink -> 24" vanity
  - lettering re-set in Roboto Condensed, room names centred in their rooms
Left as is: the kitchen has one island and no peninsula; no desk, no garage-entry bench, and no
room for a walk-in pantry inside the existing walls.
"""
import blib as B
from shapely.geometry import Polygon, LineString

PAGE, XREF = 2, 15
B.K = 389.4

TEXT = [(1580, 18, 1797, 56), (2058, 168, 2542, 210), (743, 322, 914, 360), (1583, 341, 1787, 382),
        (1222, 503, 1472, 602), (1323, 646, 1404, 682), (1576, 561, 1770, 657), (2203, 623, 2462, 777),
        (2703, 573, 2740, 742), (688, 593, 922, 744), (476, 603, 514, 724), (476, 1183, 514, 1302),
        (668, 1178, 907, 1332), (168, 1336, 397, 1407), (1108, 913, 1207, 952), (1396, 977, 1443, 1016),
        (1543, 1005, 1640, 1100), (1768, 958, 1817, 1107), (1173, 1358, 1367, 1454),
        (1518, 1373, 1754, 1464), (2148, 1406, 2452, 1502), (736, 1561, 890, 1600), (1123, 1653, 1344, 1704),
        (1498, 1736, 1759, 1774), (658, 1811, 922, 1850), (2163, 2316, 2447, 2354)]
# "CLOSET" is lettered at 45 degrees across the angled closet: erase it with a slanted band
DIAG_TEXT = LineString([(1418, 1290), (1522, 1186)]).buffer(21, cap_style=2)
STAIR = [(1025, 1096, 1252, 1412)]
PDR_SINK = [(1546, 955, 1634, 1014)]
WIN_DROP = [(1860, 925, 2015, 960), (1050, 1080, 1100, 1120), (1370, 960, 1400, 1080)]

# lower flight of the main stair (image px)
SX0, SX1 = 1062.0, 1182.0          # inside the left wall to the open-side rail
SY0, SY1 = 1098.0, 1350.0          # landing edge to the front of the first step
TREADS = 8


def stair(c):
    N = B.NAVY
    B.box(c, SX0, SY0, SX1, SY1, sw=0.55)
    for i in range(1, TREADS):
        y = SY0 + (SY1 - SY0) * i / TREADS
        c.line(SX0, y, SX1, y, 0.45, color=N)
    # rails: wall-side rail below the end of the wall, open-side rail full length; square newels
    c.line(1050, 1205, 1050, SY1 - 4, 1.0, color=N)
    c.line(SX1 + 3, 1090, SX1 + 3, SY1 - 4, 1.0, color=N)
    for x in (1050, SX1 + 3):
        B.box(c, x - 6, SY1 - 12, x + 6, SY1, sw=0.4, fill=N)
    B.arrow(c, [(1122, SY1 - 10), (1122, SY1 - 70)], w=0.45)
    B.small(c, 1104, 1380, 'UP', size=4.0, rotate=-90)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    # names centred in their rooms (inside the tray outlines in the dining and living rooms,
    # over the island in the kitchen)
    L(c, 806, 663, 'DINING ROOM', '13\'-0" × 13\'-8"', 'OPT. TRAY CEILING')
    L(c, 806, 1245, 'LIVING ROOM', '13\'-0" × 14\'-8"', 'OPT. TRAY CEILING')
    L(c, 1359, 552, 'KITCHEN', '21\'-1" × 14\'-4"')
    L(c, 1662, 640, 'BREAKFAST\nNOOK')
    L(c, 2297, 665, 'FAMILY ROOM', '23\'-0" × 13\'-7"', 'OPT. BEAMED CEILING')
    L(c, 1630, 1400, 'LIBRARY', '12\'-0" × 10\'-8"')
    L(c, 2305, 1459, 'TWO-CAR GARAGE', '22\'-10" × 27\'-2"')
    L(c, 1282, 1402, 'TWO-STORY\nFOYER')
    L(c, 1223, 1656, 'CONC. PORCH', name_pt=5.2)
    L(c, 1589, 1055, 'PDR.\nROOM', name_pt=4.6)
    S(c, 1793, 1032, 'LAUNDRY', size=4.4, rotate=-90, weight=700)
    S(c, 1363, 664, 'ISLAND', size=3.6)
    S(c, 1157, 932, 'PANTRY', size=3.8)
    S(c, 1419, 997, 'DN', size=4.0)
    S(c, 1470, 1238, 'CLOSET', size=3.6, rotate=-45)
    S(c, 2722, 657, 'GAS FIREPLACE', size=3.4, rotate=-90)
    S(c, 1688, 37, 'OPTIONAL SUNROOM', size=3.6, color=o)
    S(c, 2300, 189, 'OPTIONAL KITCHEN/FAMILY ROOM EXTENSION', size=3.6, color=o)
    S(c, 828, 341, 'OPT. BAY', size=3.6, color=o)
    S(c, 1685, 361, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 495, 663, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 495, 1242, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 282, 1355, 'OPT. CONSERVATORY', size=3.4, color=o)
    S(c, 282, 1388, 'OR IN-LAW SUITE', size=3.4, color=o)
    S(c, 813, 1580, 'ELEVATION D', size=3.4, color=o)
    S(c, 1628, 1755, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 790, 1830, 'PORCH W/ ELEVATION D', size=3.4, color=o)
    S(c, 2305, 2335, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    nv = nv.difference(DIAG_TEXT)
    hl = B.hairlines(img, walls, drop).difference(DIAG_TEXT)
    B.draw_geom(c, gr.difference(DIAG_TEXT), B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hl, B.NAVY)
    B.vanity(c, 1588, 953, 'down', 24, 18)                     # powder room vanity
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
