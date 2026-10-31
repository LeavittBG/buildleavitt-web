"""The Visionary - FIRST FLOOR (brochure page 2, image xref 16), redrawn clean.

Source raster 2773x2920 px placed at 478 dpi; about 37.85 px/ft (garage 21'-8" inside = 820 px).
Walls, windows and linework traced; lettering re-set. Modernised (Kyle, October 31, 2026):
  - the curved (radius) main stair in the foyer becomes an L-stair in its own footprint: a straight
    flight running north to the top, a square landing, and four square-cut steps down to the foyer
  - powder room: pedestal sink -> 24" vanity
The kitchen already has an island and no peninsula; there is no desk or garage-entry bench.
"""
import blib as B

PAGE, XREF = 2, 16
K = 478.0

TEXT = [(1265, 100, 1436, 138), (1850, 135, 2022, 176), (1140, 352, 1560, 450), (725, 470, 846, 511),
        (1775, 493, 1976, 534), (2262, 614, 2492, 712), (664, 743, 895, 842), (676, 591, 897, 632), (476, 740, 512, 860),
        (1750, 743, 2038, 842), (2345, 795, 2429, 831), (1265, 971, 1420, 1022), (2098, 1016, 2145, 1072),
        (2594, 1064, 2693, 1105), (600, 1066, 700, 1164), (1486, 1145, 1515, 1256), (1521, 1165, 1552, 1250),
        (851, 1172, 984, 1222), (1680, 1155, 1722, 1196), (1958, 1290, 2091, 1340), (2500, 1304, 2656, 1354),
        (1548, 1367, 1776, 1465), (1554, 1478, 1774, 1519), (668, 1481, 898, 1579), (674, 1593, 895, 1633),
        (476, 1487, 512, 1608), (166, 1635, 399, 1709), (1075, 1647, 1274, 1746), (2182, 1883, 2484, 1980),
        (679, 1959, 942, 2000), (2391, 2856, 2678, 2897)]
# tray-ceiling outlines: erased along their own lines only, then redrawn (the library's has a
# chamfered corner at its angled door)
TRAY_LIB = [(595, 592), (978, 592), (978, 887), (860, 1006), (595, 1006)]
TRAY_LIV = [(635, 1350), (950, 1350), (950, 1746), (635, 1746)]
TRAY_DIN = [(1508, 1350), (1818, 1350), (1818, 1898), (1508, 1898)]


def _strips(pts, w=7):
    out = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
        if xa == xb or ya == yb:
            out.append((min(xa, xb) - w, min(ya, yb) - w, max(xa, xb) + w, max(ya, yb) + w))
    return out


TRAYS = _strips(TRAY_LIB) + _strips(TRAY_LIV) + _strips(TRAY_DIN)
STAIR = [(1278, 1262, 1422, 1668), (1230, 1380, 1300, 1668), (1418, 1384, 1444, 1668)]
PDR_SINK = [(686, 1195, 772, 1262)]
WIN_DROP = [(1300, 1250, 1420, 1280), (1440, 1130, 1480, 1260), (1720, 1130, 1760, 1260),
            (2070, 1120, 2190, 1160)]


def stair(c):
    """L-stair in the old radius stair's place: 8 treads north to the top (y 1271), a landing,
    then 4 treads west to the foyer."""
    N = B.NAVY
    x0, x1, top = 1305.0, 1417.0, 1271.0
    T = 33.0
    yl = top + 8 * T                         # top of landing
    yb = yl + (x1 - x0)                      # bottom of landing (square)
    xw = x0 - 4 * T                          # first step, toward the foyer
    B.box(c, x0, top, x1, yl, sw=0.55)
    for i in range(1, 8):
        c.line(x0, top + T * i, x1, top + T * i, 0.45, color=N)
    B.box(c, x0, yl, x1, yb, sw=0.55)                       # landing
    B.box(c, xw, yl, x0, yb, sw=0.55)
    for i in range(1, 4):
        c.line(x0 - T * i, yl, x0 - T * i, yb, 0.45, color=N)
    # rails on the open sides, square newels
    c.line(x0, top, x0, yl, 1.0, color=N)
    c.line(xw, yl, x0, yl, 1.0, color=N)
    c.line(xw, yb, x1, yb, 1.0, color=N)
    c.line(x1, yl - 40, x1, yb, 1.0, color=N)
    k = 8.0
    for px, py in ((xw + k / 2, yl + k / 2), (xw + k / 2, yb - k / 2), (x1 - k / 2, yb - k / 2)):
        c.rect(px - k / 2, py - k / 2, k, k, sw=0.4, color=N, fill=N)
    B.arrow(c, [(xw + 12, (yl + yb) / 2), ((x0 + x1) / 2, (yl + yb) / 2), ((x0 + x1) / 2, top + 14)])
    B.small(c, xw - 24, (yl + yb) / 2, 'UP', size=4.0)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # room names centred in each room (tray-ceiling outline where there is one)
    L(c, 1350, 487, 'TWO-STORY\nFAMILY ROOM', '17\'-1" × 21\'-1"')
    L(c, 786, 799, 'LIBRARY', '12\'-0" × 12\'-11"', 'OPT. TRAY CEILING')
    L(c, 793, 1548, 'LIVING ROOM', '12\'-5" × 14\'-6"', 'OPT. TRAY CEILING')
    L(c, 1663, 1624, 'DINING ROOM', '12\'-3" × 18\'-6"', 'OPT. TRAY CEILING')
    L(c, 1877, 712, 'BREAKFAST\nNOOK', '9\'-10" × 15\'-2"')
    L(c, 2385, 697, 'KITCHEN', '17\'-9" × 16\'-1"')
    L(c, 1342, 996, 'GALLERY', name_pt=5.6)
    L(c, 1100, 1712, 'TWO-STORY\nFOYER', name_pt=5.2)
    L(c, 2560, 1330, 'LAUNDRY', name_pt=5.6)
    L(c, 2326, 1925, 'TWO-CAR GARAGE', '21\'-8" × 28\'-8"')
    L(c, 640, 1112, 'PDR.\nROOM', name_pt=5.0)
    S(c, 2385, 813, 'ISLAND', size=4.0)
    S(c, 918, 1197, 'CLOSET', size=4.0)
    S(c, 2024, 1316, 'CLOSET', size=4.0)
    S(c, 2643, 1085, 'PANTRY', size=3.8)
    S(c, 1501, 1200, "BUTLER'S", size=3.4, rotate=-90)
    S(c, 1536, 1207, 'PANTRY', size=3.4, rotate=-90)
    S(c, 1700, 1177, 'DN', size=4.0)
    S(c, 2120, 1044, 'UP', size=4.0, rotate=-90)
    S(c, 1350, 120, 'GAS FIREPLACE', size=3.6)
    S(c, 1936, 156, 'OPT. SUNROOM', size=3.8, color=o)
    S(c, 1876, 514, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 786, 491, 'OPT. BAY', size=3.6, color=o)
    S(c, 494, 800, 'OPT. BAY', size=3.6, color=o, rotate=-90)
    S(c, 494, 1547, 'OPT. BAY', size=3.6, color=o, rotate=-90)
    S(c, 282, 1656, 'OPT. CONSERVATORY', size=3.6, color=o)
    S(c, 282, 1689, 'OR IN-LAW SUITE', size=3.6, color=o)
    S(c, 810, 1980, 'PORCH W/ ELEVATION B', size=3.6, color=o)
    S(c, 2534, 2877, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)


def draw(c, img):
    B.K = c.K = K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + TRAYS + STAIR + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    for t in (TRAY_LIB, TRAY_LIV, TRAY_DIN):
        B.dashed(c, t, close=True, w=0.45)
    B.vanity(c, 729, 1258, 'up', 24, 19)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
