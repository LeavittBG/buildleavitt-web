"""The Novel - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2772x2519 px placed at 412.4 dpi, about 37.95 px/ft (library 13'-9" x 12'-4" =
522 x 467 px; garage 27'-10" deep = 1056 px).

Kept by tracing: walls, windows, doors, cabinets, appliances, the basement stair, dashed options.
Changed (Kyle, October 31, 2026): the main stair's flared, round-ended first steps are squared off
(straight stringers, square-cut first step, square newels) in the same place; the powder-room
pedestal sink becomes a 24" vanity; lettering re-set, room names centred.
Left as is: the kitchen has one island and no peninsula; there is no desk or garage-entry bench;
the pantry is a reach-in.
"""
import blib as B

PAGE, XREF = 2, 15
B.K, B.PXFT = 412.4, 37.95

TEXT = [(1940, 20, 2155, 57), (760, 318, 877, 355), (475, 575, 512, 695), (475, 1460, 512, 1578),
        (1150, 520, 1575, 620), (705, 575, 955, 670), (1760, 670, 1952, 766), (2030, 585, 2275, 680),
        (2078, 730, 2160, 765), (2540, 603, 2694, 650), (2497, 850, 2633, 897), (570, 965, 668, 1062),
        (838, 920, 880, 1012), (667, 1117, 762, 1164), (1297, 1047, 1448, 1094), (1719, 1255, 1790, 1288),
        (695, 1462, 935, 1615), (168, 1582, 397, 1650), (1148, 1490, 1345, 1585), (1540, 1597, 1782, 1744),
        (2175, 1535, 2473, 1630), (1118, 1913, 1336, 1960), (674, 2022, 934, 2059), (2187, 2457, 2469, 2494)]
STAIR_START = [(1170, 1168, 1452, 1442)]          # flared stringers, bullnose cap, UP text and arrow
PDR_SINK = [(690, 875, 775, 960)]
WIN_DROP = [(2425, 1040, 2450, 1080), (1480, 1340, 1515, 1375), (1705, 1220, 1735, 1365)]
TREADS = [1270, 1301, 1333, 1365, 1396, 1428]


def stair_start(c):
    """Squared first steps: straight stringers continue to a square-cut first step at x 1238."""
    N = B.NAVY
    x0, x1 = 1238.0, 1452.0
    for y0, y1 in ((1208.0, 1225.0), (1360.0, 1378.0)):
        c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill=N)
        c.line(x0 + 10, (y0 + y1) / 2, x1, (y0 + y1) / 2, 0.35, color='#ffffff')
    c.line(x0, 1225, x0, 1360, 0.9, color=N)                 # first step, square-cut
    for x in TREADS:
        c.line(x, 1225, x, 1360, 0.9, color=N)
    k = 22.0
    for yc in (1216.5, 1369.0):                             # square newels
        c.rect(x0 - 4, yc - k / 2, k, k, sw=0.5, color=N, fill=N)
    B.arrow(c, [(1190, 1292), (1252, 1292)], w=0.45)
    B.small(c, 1205, 1270, 'UP', size=4.2)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 1372, 560, 'TWO-STORY\nFAMILY ROOM', '14\'-10" × 20\'-1"')
    L(c, 818, 633, 'LIBRARY', '13\'-9" × 12\'-4"')
    L(c, 1856, 718, 'BREAKFAST\nNOOK')
    L(c, 2113, 633, 'KITCHEN', '19\'-11" × 14\'-9"')
    L(c, 2617, 627, 'LAUNDRY', name_pt=5.6)
    L(c, 2565, 874, 'PANTRY', name_pt=5.6)
    L(c, 617, 1013, 'PDR.\nROOM', name_pt=5.0)
    L(c, 714, 1140, 'HALL', name_pt=5.4)
    L(c, 1372, 1070, 'GALLERY', name_pt=5.8)
    L(c, 817, 1518, 'LIVING ROOM', '13\'-9" × 15\'-3"', 'OPT. TRAY CEILING')
    L(c, 1246, 1537, 'TWO-STORY\nFOYER')
    L(c, 1653, 1664, 'DINING ROOM', '13\'-0" × 15\'-6"', 'OPT. TRAY CEILING')
    L(c, 2327, 1583, 'TWO-CAR GARAGE', '21\'-7" × 27\'-10"')
    L(c, 1227, 1936, 'CONC. PORCH', name_pt=5.2)
    S(c, 2119, 747, 'ISLAND', size=3.6)
    S(c, 855, 966, 'CLOSET', size=3.6, rotate=-90)
    S(c, 1752, 1271, 'DN', size=4.0)
    S(c, 2047, 38, 'OPTIONAL SUNROOM', size=3.6, color=o)
    S(c, 818, 336, 'OPT. BAY', size=3.4, color=o)
    S(c, 493, 635, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 493, 1519, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 282, 1598, 'OPT. CONSERVATORY', size=3.4, color=o)
    S(c, 282, 1630, 'OR IN-LAW SUITE', size=3.4, color=o)
    S(c, 804, 2040, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 2328, 2475, 'OPTIONAL 3-CAR GARAGE', size=3.4, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR_START + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 723, 880, 'down', 24, 19)                     # powder room vanity
    stair_start(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
