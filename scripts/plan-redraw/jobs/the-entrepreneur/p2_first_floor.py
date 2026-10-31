"""The Entrepreneur - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 3418x3253 px placed at 532 dpi; 46.2 px/ft (garage 21'-9" x 27'-10" inside =
1005 x 1286 px). Traced: walls, windows, linework (doors, cabinets, stair, dashed options).
Modernised (Kyle, October 31, 2026):
  - owner's bath: the corner soaker tub on its angled deck -> a 5'-5" square walk-in shower in
    the same corner (glass on the room side, bench, linear drain); the old shower stall below it
    (a wall between them) -> towel closet behind its existing door
  - kitchen: the peninsula (sink, dishwasher, raised bar) and the small prep-sink island -> one
    8'-0" x 3'-6" island with the sink, dishwasher and three stools; the range run is closed
    off where the peninsula met it
  - powder room: pedestal sink -> 24" vanity
Left as drawn: the basement stair is straight; there is no desk or garage-entry bench; the
pantry and butler's pantry are reach-in counters with no room to walk in.
"""
import blib as B

PAGE, XREF = 2, 15
K, PXFT = 532.0, 46.2

TEXT = [(2230, 0, 2500, 40), (2455, 171, 2749, 207), (2437, 327, 2760, 433), (1744, 264, 1971, 296),
        (1131, 513, 1358, 618), (1682, 629, 2016, 802), (269, 856, 680, 1029), (3122, 802, 3322, 847),
        (2567, 873, 2789, 951), (3016, 1087, 3196, 1133), (1207, 1122, 1333, 1178),
        (2249, 1129, 2569, 1238), (1669, 1249, 1902, 1298), (3262, 1178, 3307, 1311), (410, 1293, 545, 1336),
        (2068, 1366, 2111, 1418), (893, 1398, 1053, 1440), (224, 1433, 389, 1480), (1744, 1529, 1902, 1633),
        (96, 1582, 222, 1649), (1167, 1582, 1304, 1649), (2355, 1490, 2440, 1620), (1447, 1604, 1633, 1682),
        (1716, 1671, 1778, 1811), (1447, 1816, 1629, 1864), (31, 1867, 107, 2160), (189, 1907, 502, 2016),
        (858, 1907, 1171, 2016), (2660, 2056, 3073, 2171), (1884, 2118, 2182, 2293), (1364, 2422, 1678, 2471),
        (871, 2616, 1138, 2656), (2684, 3213, 3060, 3249)]
TUB = [(925, 255, 1182, 511)]
STALL = [(936, 532, 1062, 804)]
PENINSULA = [(2415, 622, 2945, 860)]
ISLAND = [(2545, 975, 2750, 1112)]
PDR_SINK = [(1950, 1435, 2036, 1545)]


def bath(c):
    N = B.NAVY
    k = PXFT / 12.0
    # walk-in shower in the tub corner: walls left and top, the bath partition below; glass on the
    # room side (x 1181) with an open entry at the bottom
    x0, y0, x1, y1 = 931.0, 262.0, 1181.0, 511.0
    B.box(c, x0, y0, x1, y1, sw=0.45)
    c.rect(x0 + 4 * k, y0 + 3 * k, 1.6 * k, (y1 - y0) - 6 * k, sw=0.3, color=N)          # linear drain
    B.box(c, x0, y0, x1, y0 + 15 * k, sw=0.45)                                             # bench
    B.small(c, (x0 + x1) / 2, y0 + 7.5 * k, 'BENCH', size=3.2, color=B.GREY)
    c.line(x1, y0, x1, y1 - 30 * k, 0.9, color=N)                                          # glass
    B.small(c, (x0 + x1) / 2 + 6, (y0 + y1) / 2 + 22, 'SHOWER', size=4.0)
    # towel closet in the old stall: shelves along the back wall
    c.line(931, 545, 1062, 545, 0.45, color=N)
    c.line(931 + 14 * k, 545, 931 + 14 * k, 790, 0.45, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, 1010, 668, 'TOWEL', size=3.6, rotate=-90)
    B.small(c, 1034, 668, 'CLOSET', size=3.6, rotate=-90)


def kitchen(c):
    N = B.NAVY
    k = PXFT / 12.0
    # range run, closed at the top where the peninsula met it
    B.box(c, 2892, 700, 2983, 866, sw=0.45)
    c.line(2893.5, 866, 2981.5, 866, 1.2, color='#ffffff')
    c.line(2900, 712, 2975, 712, 0.5, color=N, dash=c.dash(3, 2))      # wall cabinets
    # one island, 8'-0" x 3'-6": sink and dishwasher on the range side, stools on the gallery side
    x0, x1, y0, y1 = 2569.0, 2731.0, 758.0, 1128.0
    B.box(c, x0, y0, x1, y1, sw=0.6)
    c.line(x0 + 12 * k, y0, x0 + 12 * k, y1, 0.35, color=N, dash=c.dash(2.5, 1.6))   # seating overhang
    B.kitchen_sink(c, x1 - 11 * k, 900, horizontal=False, w_in=33, d_in=19, bowls=2)
    c.circle(x1 - 2.4 * k, 900, 1.1 * k, sw=0.3, color=N)
    B.box(c, x1 - 24 * k, 990, x1, 990 + 24 * k, sw=0.4)
    B.small(c, x1 - 12 * k, 990 + 12 * k, 'DW', size=3.2)
    for cy in (830, 943, 1056):
        c.circle(x0 - 27, cy, 22, sw=0.45, color=B.GREY)
    B.small(c, x0 + 20 * k, 1060, 'ISLAND', size=3.8, rotate=-90)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 474, 909, "OWNER'S BEDROOM", '19\'-0" × 16\'-7"', 'OPT. TRAY CEILING')
    L(c, 1852, 690, 'FAMILY ROOM', '14\'-10" × 18\'-6"', 'OPT. BEAMED CEILING')
    L(c, 2602, 379, 'SUNROOM', '16\'-7" × 13\'-2"', 'OPT. TRAY CEILING')
    L(c, 2650, 680, 'KITCHEN', '13\'-3" × 15\'-4"')
    S(c, 2678, 1172, 'OPT. BOX TRAY CEILING', size=4.2, color=o)
    L(c, 2035, 2201, 'DINING ROOM', '13\'-6" × 16\'-0"', 'OPT. TRAY CEILING')
    L(c, 360, 1889, 'BEDROOM 2', '14\'-1" × 15\'-9"')
    L(c, 1030, 1889, 'BEDROOM 3', '14\'-1" × 15\'-9"')
    L(c, 2875, 2078, 'TWO-CAR GARAGE', '21\'-9" × 27\'-10"')
    L(c, 1539, 1830, 'FOYER')
    S(c, 1539, 1885, 'OPT. TRAY', size=4.2, color=o)
    S(c, 1539, 1912, 'CEILING', size=4.2, color=o)
    L(c, 1539, 2440, 'CONC. PORCH', name_pt=5.2)
    L(c, 1270, 566, "OWNER'S\nBATH", name_pt=5.4)
    L(c, 1830, 1580, 'PDR.\nROOM', name_pt=5.2)
    L(c, 973, 1419, 'HALL', name_pt=5.4)
    L(c, 306, 1456, 'BATH', name_pt=5.4)
    L(c, 1785, 1273, 'GALLERY', name_pt=5.6)
    L(c, 3222, 825, 'LAUNDRY', name_pt=5.4)
    L(c, 3106, 1110, 'ENTRY', name_pt=5.4)
    S(c, 1270, 1150, 'W.I.C.', size=4.2)
    S(c, 159, 1615, 'W.I.C.', size=4.2)
    S(c, 1235, 1615, 'W.I.C.', size=4.2)
    S(c, 478, 1314, 'LINEN', size=3.8)
    S(c, 1747, 1741, 'CLOSET', size=3.8, rotate=-90)
    S(c, 3285, 1245, 'PANTRY', size=3.8, rotate=-90)
    S(c, 2376, 1555, "BUTLER'S", size=3.4, rotate=-90)
    S(c, 2420, 1555, 'PANTRY', size=3.4, rotate=-90)
    S(c, 2090, 1392, "DN", size=4.0, rotate=-90)
    S(c, 1857, 280, 'GAS FIREPLACE', size=3.8)
    S(c, 2365, 20, 'OPT. PATIO DOOR', size=3.8, color=o)
    S(c, 52, 1940, 'OPT.', size=3.6, color=o, rotate=-90)
    S(c, 88, 1940, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 52, 2090, 'OPT.', size=3.6, color=o, rotate=-90)
    S(c, 88, 2090, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 1004, 2636, 'PORCH W/ ELEV. B', size=3.6, color=o)
    S(c, 2872, 3231, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)


def draw(c, img):
    B.PXFT = PXFT
    B.K = c.K = K
    walls, wins = B.trace(img)
    drop = TEXT + TUB + STALL + PENINSULA + ISLAND + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    bath(c)
    kitchen(c)
    B.vanity(c, 2034, 1480, 'left', 24, 19)            # powder room vanity (was a pedestal sink)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
