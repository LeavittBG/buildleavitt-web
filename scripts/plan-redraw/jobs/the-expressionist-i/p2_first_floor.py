"""The Expressionist I - FIRST FLOOR (brochure page 2, image xref 17), redrawn clean.

Source raster 2409x1989 px placed at 370.3 dpi; about 32.1 px/ft (three-car garage 25'-9" inside
= 829 px). Walls, windows and linework traced; lettering re-set. Modernised (Kyle, October 31, 2026):
  - the curved (radius) main stair in the gallery becomes a straight flight in its own footprint,
    square-cut first step and square newels; its curved outer wall is gone and the closet wall
    beside it bounds the stair
  - owner's bath: the angled corner soaker tub on its platform becomes one walk-in shower in the
    same corner; the old angled shower stall (walled off from it) becomes a towel closet
  - powder room: pedestal sink -> 24" vanity
The kitchen keeps its island and its cooktop peninsula: between the counters it is only about
9'-9" deep, too shallow for a larger island with proper aisles, and the peninsula carries the
cooktop. There is no desk or garage-entry bench; the pantry is already a closet with a door.
"""
import blib as B

PAGE, XREF = 2, 17
K, PXFT = 370.3, 32.1

TEXT = [(1040, 82, 1176, 108), (636, 210, 795, 239), (1703, 273, 1849, 302), (945, 348, 1278, 386),
        (1015, 386, 1202, 422), (1591, 351, 1766, 379), (1558, 386, 1798, 422), (1553, 422, 1774, 459),
        (488, 399, 612, 436), (455, 436, 645, 473), (2071, 466, 2192, 540), (1566, 503, 1790, 532),
        (2343, 556, 2376, 610), (514, 710, 628, 746), (470, 748, 668, 784), (553, 845, 619, 871),
        (1798, 806, 1893, 850), (2134, 803, 2229, 850), (1388, 825, 1465, 861), (1575, 811, 1652, 847),
        (976, 900, 1099, 936), (649, 1095, 728, 1124), (444, 1104, 502, 1217), (816, 1122, 846, 1188),
        (530, 1130, 607, 1166), (932, 1147, 1010, 1183), (1385, 1157, 1508, 1193), (1219, 1176, 1279, 1249),
        (924, 1251, 1052, 1280), (1122, 1257, 1199, 1293), (1861, 1343, 2125, 1380), (1888, 1378, 2100, 1418),
        (558, 1397, 729, 1432), (545, 1434, 740, 1469), (375, 1405, 408, 1496), (942, 1448, 1034, 1484),
        (556, 1484, 731, 1512), (1234, 1498, 1403, 1534), (1223, 1535, 1410, 1571), (1441, 1467, 1474, 1610),
        (133, 1514, 317, 1568), (1231, 1586, 1406, 1614), (891, 1764, 1066, 1800), (1047, 1157, 1098, 1197), (1350, 960, 1381, 1026)]
STAIR = [(1150, 820, 1303, 1150), (1176, 1096, 1250, 1170), (1176, 1170, 1204, 1198),
         (1074, 1075, 1150, 1215), (1150, 1080, 1190, 1150)]          # last: the basement stair below, redrawn
# the curved outer wall (cuts are applied after the added walls, so they stay clear of them)
STAIR_CUT = [(1176, 820, 1303, 1149), (1150, 1149, 1190, 1205), (1204, 1168, 1252, 1200)]
# powder-room top and left walls, which the curved wall used to form
STAIR_WALLS = [(1190, 1150, 1306, 1168), (1190, 1150, 1204, 1205)]
TUB = [(2200, 262, 2378, 438)]
SHOWER_OLD = [(2208, 636, 2372, 733)]
PDR_SINK = [(1298, 1250, 1352, 1322)]
WIN_DROP = [(1170, 1140, 1215, 1215), (2140, 600, 2215, 760), (2280, 600, 2312, 640), (1530, 900, 1570, 1050), (1270, 925, 1310, 960), (1080, 1100, 1110, 1220), (1330, 1265, 1360, 1300)]

# tray-ceiling outlines are kept from the trace; the text erasures above stay clear of them


def stair(c):
    """Straight flight in the radius stair's place: first step at the gallery (north), 13 treads
    south to the top at the powder-room wall, closet wall on the right, railing on the open left side."""
    N = B.NAVY
    x0, x1, y0, y1 = 1180.0, 1305.0, 830.0, 1150.0
    n = 12
    T = (y1 - y0) / n
    B.box(c, x0, y0, x1, y1, sw=0.55)
    for i in range(1, n):
        c.line(x0, y0 + T * i, x1, y0 + T * i, 0.45, color=N)
    c.line(x0, y0, x0, 1096, 1.0, color=N)                       # rail, open side
    c.line(x1, y0, x1, 950, 1.0, color=N)                        # rail above the closet wall
    k = 8.0
    for px in (x0, x1):
        c.rect(px - k / 2, y0 - k / 2, k, k, sw=0.4, color=N, fill=N)
    B.break_line(c, x0 - 10, 1040, x1 + 6, 1088)
    B.arrow(c, [((x0 + x1) / 2, y0 + 10), ((x0 + x1) / 2, 1030)])
    B.small(c, (x0 + x1) / 2 + 22, y0 + 26, 'UP', size=4.2)
    # basement stair below, going down east under the main flight from its door
    bx0, bx1, by0, by1 = 1076.0, 1178.0, 1110.0, 1202.0
    for i in range(1, 4):
        c.line(bx0 + 25.5 * i, by0, bx0 + 25.5 * i, by1, 0.45, color=N)
    c.line(bx0, by0, bx0, by1, 0.45, color=N)
    B.arrow(c, [(1052, 1186), (1160, 1186)])
    B.small(c, 1062, 1166, 'DN', size=4.2)


def owners_bath(c):
    N = B.NAVY
    k = PXFT / 12.0
    # walk-in shower in the old tub corner: tiled floor, linear drain on the back wall, bench on
    # the outside wall, glass on the two open sides with the entry at the vanity end
    x0, y0, x1, y1 = 2203.0, 260.0, 2379.0, 436.0
    B.box(c, x0, y0, x1, y1, sw=0.45)
    c.rect(x0 + 8 * k, y0 + 4 * k, (x1 - x0) - 30 * k, 1.6 * k, sw=0.3, color=N)          # drain
    B.box(c, x1 - 15 * k, y0, x1, y1, sw=0.45)                                                  # bench
    c.line(x0, y0 + 12, x0, y1, 0.9, color=N)                                                  # glass
    c.line(x0, y1, x1 - 15 * k - 66, y1, 0.9, color=N)
    B.small(c, (x0 + x1 - 15 * k) / 2, (y0 + y1) / 2 + 6, 'SHOWER', size=4.2)
    B.small(c, x1 - 7.5 * k, (y0 + y1) / 2, 'BENCH', size=3.2, rotate=-90)
    # old shower stall, walled off: towel closet behind its door
    c.line(2215, 690, 2372, 690, 0.4, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, 2300, 720, 'TOWEL CLOSET', size=3.8)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 1109, 400, 'TWO-STORY\nFAMILY ROOM', '17\'-9" × 21\'-1"')
    L(c, 545, 430, 'SUNROOM', '18\'-11" × 12\'-3"')
    S(c, 1633, 366, 'OPT. TRAY CEILING', size=4.2, color=o)
    L(c, 1633, 425, "OWNER'S BEDROOM", '19\'-4" × 16\'-3"')
    S(c, 1677, 518, 'OPT. CATHEDRAL CEILING', size=4.2, color=o)
    L(c, 2120, 505, "OWNER'S\nBATH", name_pt=5.6)
    L(c, 582, 742, 'KITCHEN', '17\'-6" × 14\'-10"')
    S(c, 586, 858, 'ISLAND', size=3.8)
    L(c, 1037, 918, 'GALLERY', name_pt=5.6)
    L(c, 1446, 1175, 'LAUNDRY', name_pt=5.4)
    L(c, 1255, 1212, 'PDR.\nROOM', name_pt=5.0)
    L(c, 643, 1450, 'DINING ROOM', '13\'-6" × 15\'-4"', 'OPT. TRAY CEILING')
    L(c, 1331, 1539, 'LIVING ROOM', '13\'-5" × 13\'-5"', 'OPT. TRAY CEILING')
    L(c, 988, 1455, 'FOYER', None, 'TRAY CEILING', name_pt=5.6)
    L(c, 1963, 1440, 'THREE-CAR GARAGE', '25\'-9" × 34\'-8"')
    L(c, 978, 1782, 'CONC. PORCH', name_pt=4.8)
    for x, y in ((1426, 843), (1613, 829), (568, 1148), (971, 1165), (1160, 1275)):
        S(c, x, y, 'HALL', size=4.4, weight=700)
    S(c, 1845, 828, 'W.I.C.', size=4.2)
    S(c, 2181, 826, 'W.I.C.', size=4.2)
    S(c, 688, 1110, 'PANTRY', size=3.8)

    S(c, 1365, 993, 'CLOSET', size=3.6, rotate=-90)
    S(c, 831, 1155, 'CLOSET', size=3.6, rotate=-90)
    S(c, 462, 1160, "BUTLER'S", size=3.4, rotate=-90)
    S(c, 485, 1160, 'PANTRY', size=3.4, rotate=-90)
    S(c, 2360, 583, 'LINEN', size=3.4, rotate=-90)
    S(c, 1108, 95, 'GAS FIREPLACE', size=3.6)
    S(c, 715, 224, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 1776, 288, 'OPT. FIREPLACE', size=3.6, color=o)
    S(c, 392, 1450, 'OPT. BAY', size=3.6, color=o, rotate=-90)
    S(c, 1458, 1538, 'OPT. FIREPLACE', size=3.6, color=o, rotate=-90)
    S(c, 225, 1528, 'OPT. CONSERVATORY', size=3.6, color=o)
    S(c, 225, 1554, 'OR IN-LAW SUITE', size=3.6, color=o)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP, cut=STAIR_CUT, add=STAIR_WALLS)
    drop = TEXT + STAIR + TUB + SHOWER_OLD + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 1354, 1286, 'left', 24, 19)
    owners_bath(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
