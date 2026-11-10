"""The Illustrator - FIRST FLOOR (brochure page 2, image xref 16), redrawn clean.

Source raster 2373x1966 px placed at 370.4 dpi, 32.3 px/ft (garage 22'-10" inside = 738 px).

Kept by tracing: walls, windows, doors, cabinets, appliances, both stair runs, dashed options.
Changed (Kyle, October 31, 2026):
  - powder room: pedestal sink -> 24" vanity
  - lettering re-set in Roboto Condensed, room names centred in their rooms
Left as is: the stairs are straight runs with square landings; the kitchen has one island and no
peninsula; no desk or garage-entry bench (the counter run on the garage wall is cabinetry); the
pantry is a reach-in closet with no room to walk in.
"""
import blib as B

PAGE, XREF = 2, 16
B.K, B.PXFT = 370.4, 32.3

TEXT = [(860, 103, 1030, 137), (1400, 103, 1615, 140), (830, 338, 1060, 487), (195, 408, 492, 447),
        (1840, 408, 2137, 447), (1365, 423, 1562, 460), (1365, 598, 1557, 697), (1640, 598, 1882, 697),
        (1668, 750, 1752, 781), (2086, 548, 2132, 693), (2178, 818, 2214, 908), (2188, 978, 2224, 1058),
        (2306, 853, 2344, 1147), (2290, 1757, 2328, 1888), (215, 658, 472, 762), (20, 648, 57, 768),
        (20, 1363, 57, 1482), (26, 933, 65, 1222), (120, 945, 212, 1037), (393, 1088, 484, 1124),
        (878, 843, 1032, 892), (703, 1033, 760, 1072), (1340, 985, 1390, 1027), (913, 1398, 957, 1462),
        (106, 1248, 172, 1342), (106, 1498, 172, 1592), (213, 1373, 457, 1527), (1128, 1308, 1402, 1462),
        (703, 1453, 912, 1552), (698, 1773, 917, 1822), (1758, 1473, 2062, 1572)]
PDR_SINK = [(205, 1058, 287, 1120)]
# stair stringer ends the window finder reads as windows
WIN_DROP = [(740, 980, 770, 1080), (900, 1080, 1000, 1105)]


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 945, 410, 'TWO-STORY\nFAMILY ROOM', '18\'-1" × 16\'-11"')
    L(c, 345, 705, 'LIBRARY', '12\'-10" × 11\'-10"')
    L(c, 1460, 645, 'BREAKFAST\nNOOK')
    L(c, 1760, 640, 'KITCHEN', '18\'-9" × 15\'-3"')
    L(c, 335, 1448, 'LIVING ROOM', '12\'-10" × 12\'-9"', 'OPT. TRAY CEILING')
    L(c, 1265, 1384, 'DINING ROOM', '12\'-10" × 14\'-10"', 'OPT. TRAY CEILING')
    L(c, 808, 1502, 'TWO-STORY\nFOYER')
    L(c, 955, 868, 'GALLERY', name_pt=5.6)
    L(c, 1900, 1520, 'TWO-CAR GARAGE', '22\'-10" × 27\'-2"')
    L(c, 808, 1798, 'CONC. PORCH', name_pt=5.2)
    L(c, 166, 990, 'PDR.\nROOM', name_pt=4.6)
    S(c, 2109, 620, 'LAUNDRY', size=4.4, rotate=-90, weight=700)
    S(c, 1710, 766, 'ISLAND', size=3.6)
    S(c, 438, 1106, 'CLOSET', size=3.8)
    S(c, 2196, 863, 'PANTRY', size=3.6, rotate=-90)
    S(c, 2206, 1018, 'CLOSET', size=3.6, rotate=-90)
    S(c, 945, 120, 'GAS FIREPLACE', size=3.6)
    S(c, 730, 1052, 'DN', size=4.2)
    S(c, 1365, 1006, 'UP', size=4.2)
    S(c, 935, 1430, 'UP', size=4.2, rotate=-90)
    S(c, 1508, 121, 'OPTIONAL SUNROOM', size=3.6, color=o)
    S(c, 343, 427, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 1988, 427, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 1463, 441, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 38, 708, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 38, 1422, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 45, 1077, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2325, 1000, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2309, 1822, 'OPT. DOOR', size=3.4, color=o, rotate=-90)
    for y in (1295, 1545):
        S(c, 124, y, 'OPT.', size=3.4, color=o, rotate=-90)
        S(c, 154, y, 'WINDOW', size=3.4, color=o, rotate=-90)


def draw(c, img):
    c.K = B.K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 245, 1122, 'up', 24, 18)                       # powder room vanity
    B.draw_plan_walls(c, walls, wins)
    labels(c)
