"""The Craftsman - FIRST FLOOR (brochure page 2, image xref 18), redrawn clean.

Source raster 2497x2263 px at 387 dpi; 46.2 px/ft (garage 20'-3" inside = 934 px, 22'-5" = 1037 px).
Traced: walls, windows, linework (doors, cabinets, stair, dashed options).
Modernised (Kyle, October 31, 2026): powder-room pedestal sink -> 24" vanity.
Left as drawn: the kitchen has an island and no peninsula; the U-stair turns on winders (not a
flared or curved start), so it is only re-traced.
"""
import blib as B

PAGE, XREF = 2, 18
K, PXFT = 387.1, 46.2

TEXT = [(1100, 22, 1300, 64), (1250, 355, 1490, 397), (322, 395, 460, 437), (1275, 545, 1508, 663),
        (880, 610, 1207, 720), (1018, 776, 1122, 815), (243, 730, 540, 904), (1826, 750, 2137, 928),
        (2328, 713, 2367, 912), (26, 746, 67, 879), (26, 1463, 67, 1595), (121, 938, 200, 1045),
        (121, 1246, 200, 1354), (705, 1085, 815, 1123), (255, 1158, 529, 1237), (712, 1222, 824, 1329),
        (1110, 1305, 1287, 1357), (730, 1485, 879, 1537), (1005, 1493, 1067, 1540), (255, 1495, 529, 1675),
        (788, 1653, 1020, 1767), (1001, 1801, 1062, 1845), (1713, 1605, 2070, 1720), (766, 2038, 1030, 2095),
        (293, 2166, 540, 2207), (1110, 2166, 1362, 2207), (2396, 1978, 2442, 2130)]
PDR_SINK = [(710, 1153, 820, 1232)]
WIN_DROP = [(1050, 1100, 1700, 1900), (1560, 1140, 1620, 1190)]


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # names centred in their rooms: tray outlines, open floor, over the island in the kitchen
    L(c, 392, 815, 'DINING ROOM', '11\'-7" × 13\'-10"', 'OPT. TRAY CEILING')
    L(c, 392, 1532, 'LIVING ROOM', '13\'-1" × 16\'-1"', 'OPT. TRAY CEILING')
    L(c, 1070, 668, 'KITCHEN', '19\'-10" × 13\'-10"')
    L(c, 1372, 600, 'BREAKFAST\nNOOK')
    L(c, 1985, 816, 'FAMILY ROOM', '16\'-8" × 13\'-10"', 'OPT. BEAMED CEILING')
    L(c, 1901, 1680, 'TWO-CAR GARAGE', '20\'-3" × 22\'-5"')
    L(c, 765, 1275, 'PDR.\nROOM', name_pt=5.2)
    L(c, 1182, 1300, 'LAUNDRY', name_pt=5.6)
    L(c, 893, 1700, 'TWO-STORY\nFOYER')
    L(c, 898, 2066, 'CONC. PORCH', name_pt=5.2)
    S(c, 1070, 806, 'ISLAND', size=4.0)
    S(c, 760, 1104, 'PANTRY', size=4.0)
    S(c, 805, 1511, 'CLOSET', size=4.0)
    S(c, 1036, 1516, 'DN', size=4.2)
    S(c, 1031, 1823, 'UP', size=4.2)
    S(c, 2348, 812, 'GAS FIREPLACE', size=3.6, rotate=-90)
    S(c, 392, 1180, 'OPT. KNEEWALLS W/', size=3.8, color=o)
    S(c, 392, 1214, '8" COLUMNS', size=3.8, color=o)
    S(c, 1200, 43, 'OPT. SUNROOM', size=3.8, color=o)
    S(c, 1370, 376, 'OPT. PATIO DOOR', size=3.8, color=o)
    S(c, 391, 416, 'OPT. BAY', size=3.8, color=o)
    S(c, 46, 812, 'OPT. BAY', size=3.8, color=o, rotate=-90)
    S(c, 46, 1529, 'OPT. BAY', size=3.8, color=o, rotate=-90)
    S(c, 140, 991, 'OPT.', size=3.6, color=o, rotate=-90)
    S(c, 180, 991, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 140, 1300, 'OPT.', size=3.6, color=o, rotate=-90)
    S(c, 180, 1300, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 416, 2186, 'PORCH W/ ELEV. D', size=3.6, color=o)
    S(c, 1236, 2186, 'PORCH W/ ELEV. C', size=3.6, color=o)
    S(c, 2419, 2054, 'OPT. DOOR', size=3.6, color=o, rotate=-90)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 765.5, 1151, 'down', 24, 19)          # powder room vanity (was a pedestal sink)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
