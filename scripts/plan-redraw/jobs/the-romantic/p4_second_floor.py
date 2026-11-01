"""The Romantic - SECOND FLOOR (brochure page 4, image xref 22), redrawn clean.

Source raster 2308x2063 px placed at 370.4 dpi; 46.2 px/ft like the first floor. Walls, windows
and linework traced; lettering re-set, room names centred. Modernised (Kyle, October 31, 2026):
  - owner's bath: the angled corner soaker tub on its deck becomes one walk-in shower in its
    corner (glass on the room side with the entry at the bottom, linear drain on the back wall,
    bench on the outside wall); a wall separates it from the old shower stall, which becomes a
    towel closet behind its existing door
  - main stair seen from above: the rounded starting step is squared to match the first floor
The hall baths keep their tubs; their sinks are already in vanities.
"""
import blib as B

PAGE, XREF = 4, 22
K, PXFT = 370.4, 46.2

TEXT = [(395, 232, 566, 340), (893, 168, 1042, 219), (715, 425, 830, 470), (715, 710, 830, 755),
        (900, 560, 1030, 610), (185, 635, 315, 685), (445, 685, 550, 730), (1035, 820, 1145, 870),
        (1095, 880, 1135, 945), (845, 895, 1025, 925), (800, 1015, 980, 1180), (1246, 1080, 1274, 1256),
        (260, 1030, 560, 1145), (1515, 965, 1690, 1010), (1925, 965, 2025, 1010), (1980, 1135, 2110, 1192),
        (1410, 1195, 1520, 1245), (1535, 405, 1890, 525), (1590, 550, 1840, 580), (1748, 1512, 2052, 1618),
        (755, 1665, 1050, 1775), (1330, 1695, 1460, 1745)]
TUB = [(128, 128, 392, 344), (386, 192, 399, 234)]                    # corner tub and its deck
OLD_SHOWER = [(130, 368, 258, 546)]             # interior of the old stall (its door is kept)
STAIR_START = [(742, 1205, 786, 1393)]
WIN_DROP = [(1000, 1350, 1050, 1410)]


def owners_bath(c):
    N = B.NAVY
    k = PXFT / 12.0
    x0, y0, x1, y1 = 126.0, 126.0, 350.0, 346.0
    B.box(c, x0, y0, x1, y1, sw=0.45)
    c.rect(x0 + 8 * k, y0 + 4 * k, (x1 - x0) - 16 * k, 1.6 * k, sw=0.3, color=N)        # linear drain
    B.box(c, x0, y0 + 10 * k, x0 + 15 * k, y1, sw=0.45)                                    # bench
    c.line(x1, y0, x1, y1 - 100, 0.9, color=N)                                             # glass, entry below
    B.small(c, (x0 + 15 * k + x1) / 2, (y0 + y1) / 2 + 4, 'SHOWER', size=4.2)
    B.small(c, x0 + 7.5 * k, (y0 + y1) / 2 + 20, 'BENCH', size=3.2, rotate=-90)
    # old stall: towel closet with shelves
    c.line(132, 400, 256, 400, 0.4, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, 194, 470, 'TOWEL', size=3.8)
    B.small(c, 194, 492, 'CLOSET', size=3.8)


def stair_start(c):
    N = B.NAVY
    B.box(c, 752, 1236, 787, 1393, sw=0.55)
    k = 14.0
    c.rect(772 - k / 2, 1244 - k / 2, k, k, sw=0.4, color=N, fill=N)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 1712, 460, "OWNER'S BEDROOM", '20\'-5" × 14\'-9"', 'OPT. TRAY CEILING')
    L(c, 520, 290, "OWNER'S\nBATH", name_pt=5.6)
    L(c, 412, 1100, 'BEDROOM 2', '12\'-4" × 12\'-7"')
    L(c, 929, 1725, 'BEDROOM 3', '14\'-5" × 13\'-4"')
    L(c, 1883, 1568, 'BEDROOM 4', '13\'-1" × 13\'-11"')
    L(c, 868, 1085, 'OPEN TO\nFOYER BELOW', name_pt=5.2)
    L(c, 1603, 990, 'LAUNDRY', name_pt=5.2)
    L(c, 1975, 990, 'BATH', name_pt=5.0)
    L(c, 497, 708, 'BATH', name_pt=5.0)
    L(c, 1090, 845, 'HALL', name_pt=5.2)
    L(c, 1465, 1220, 'HALL', name_pt=5.2)
    S(c, 965, 585, 'W.I.C.', size=4.4)
    S(c, 250, 660, 'W.I.C.', size=4.4)
    S(c, 2045, 1162, 'W.I.C.', size=4.4)
    S(c, 1395, 1720, 'W.I.C.', size=4.4)
    S(c, 967, 194, 'CLOSET', size=4.2)
    S(c, 772, 447, 'LINEN', size=4.0)
    S(c, 772, 732, 'LINEN', size=4.0)
    S(c, 1116, 912, 'DN', size=4.0, rotate=-90)
    S(c, 935, 911, 'WOOD RAILING', size=3.4)
    S(c, 1258, 1168, "WOOD RAILING", size=3.4, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + TUB + OLD_SHOWER + STAIR_START
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_bath(c)
    stair_start(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
