"""The Pioneer I - FIRST FLOOR (brochure page 2, image xref 17), redrawn clean.

Source: assets-src/plans/originals/the-pioneer-i.pdf page 2, raster 3284x2154 px at 438 dpi, about 37.8 px/ft
(garage 21'-4" inside = 806 px). Coordinates below are that raster's pixels.

Kept from the source by tracing: walls, windows, door leaves and swings, cabinets, appliances,
dashed option outlines. Redrawn by hand (Kyle, October 31, 2026):
  - main stair: lower flight straightened in place (no flare, no rounded starting step)
  - powder room: pedestal sink -> 24" vanity
  - kitchen: small island + peninsula -> one large island with seating; top run extended
  - breakfast nook: built-in desk -> coffee bar
  - mud area: bench -> lockers with bench
  - all lettering in Roboto Condensed
"""
import math
import blib as B
from shapely.geometry import box as sbox, Polygon

PAGE, XREF = 2, 17
R2 = math.sqrt(2)

# --- text in the source (erased; set again below) ---
TEXT = [(1090, 95, 1560, 135), (2220, 95, 2530, 135), (1190, 530, 1460, 700), (570, 475, 950, 515),
        (2050, 475, 2440, 515), (1900, 650, 2170, 770), (1985, 785, 2090, 825), (2460, 730, 2780, 840),
        (620, 735, 910, 845), (2630, 975, 2710, 1020), (565, 1080, 675, 1185), (745, 1195, 845, 1245),
        (1680, 1140, 1800, 1210), (1815, 1100, 1885, 1240), (1985, 1100, 2095, 1145),
        (2205, 1000, 2250, 1065), (2460, 1160, 2620, 1215), (2820, 1080, 2870, 1215),
        (1375, 1280, 1535, 1340), (2258, 1250, 2300, 1345), (2015, 1300, 2115, 1345),
        (650, 1535, 990, 1700), (1595, 1525, 1930, 1690), (1150, 1600, 1370, 1710), (1620, 1850, 1790, 1895),
        (1140, 1940, 1370, 2000), (670, 2025, 950, 2065), (1570, 2025, 1850, 2065), (160, 1620, 410, 1700),
        (2220, 1690, 2540, 1800), (2820, 1945, 2870, 2070), (2890, 2080, 3200, 2120),
        (1519, 1126, 1576, 1166)]
# --- items redrawn by hand ---
STAIR = [(1068, 1074, 1499, 1199), (1068, 1199, 1180, 1262), (1066, 1199, 1360, 1440), (1090, 1262, 1200, 1440)]
KITCHEN = [(1940, 755, 2125, 880), (2286, 552, 2440, 885)]
NOOK_DOORS = [(2486, 545, 2742, 700)]
TRAYS = [(628, 1434, 972, 1744), (1548, 1418, 1901, 1744)]
DESK = [(2486, 970, 2806, 1062)]
BENCH = [(1984, 1288, 2146, 1352)]
PDR_SINK = [(640, 1205, 732, 1282)]
# stairwell walls kept explicit: basement-stair wall under the upper flight, angled wall carried
# down to the top of the straightened lower flight
STAIR_WALLS = [(1180, 1199, 1500, 1219),
               Polygon([(1048, 1262), (1068, 1262), (1133, 1327), (1119, 1341), (1048, 1270)])]
WIN_DROP = [(1490, 1060, 1525, 1215), (2180, 1110, 2310, 1150)]


def stair(c):
    """Main stair: upper flight east over the basement stair; landing at the west end; lower
    flight straight at 45 degrees along the angled stairwell wall, square-cut first step."""
    N = B.NAVY
    # landing + lower flight in the stairwell's 45-degree frame
    O = (1068.0, 1262.0)                     # inner corner of left wall and angled wall
    du = (1 / R2, 1 / R2)                     # down the flight (toward the gallery)
    dv = (1 / R2, -1 / R2)                    # across the flight
    W = 151.0                                 # 4'-0" flight
    u0, T, n = 92.0, 34.0, 4                  # top of lower flight, tread, number of treads
    def P(u, v):
        return (O[0] + du[0] * u + dv[0] * v, O[1] + du[1] * u + dv[1] * v)
    u1 = u0 + T * n
    # treads
    flight = [P(u0, 0), P(u0, W), P(u1, W), P(u1, 0)]
    c.polyline(flight, w=0.55, color=N, close=True, fill='#ffffff')
    for i in range(1, n):
        c.line(*P(u0 + T * i, 0), *P(u0 + T * i, W), 0.45, color=N)
    # rails both sides, square newels at the bottom
    for v in (0, W):
        a, b = P(u0 - 4, v), P(u1, v)
        c.line(*a, *b, 1.0, color=N)
    k = 7.0
    for v in (k / 2, W - k / 2):
        x, y = P(u1 - k / 2, v)
        c.polyline([(x, y - k / R2), (x + k / R2, y), (x, y + k / R2), (x - k / R2, y)], w=0.5, color=N,
                   close=True, fill=N)
    B.arrow(c, [P(u1 - 10, W / 2), P(u0 + 12, W / 2)], w=0.45)
    ax, ay = P(u1 - 34, W / 2 - 24)
    B.small(c, ax, ay, 'UP', size=4.0, rotate=45)
    # upper flight (main stair going up east) and the basement stair below it
    X0, X1, Y0, Y1 = 1180.0, 1499.0, 1074.0, 1199.0
    nt = 9
    tw = (X1 - X0) / nt
    xb = X0 + tw * 4                          # break line between the two
    B.box(c, X0, Y0, X1, Y1, sw=0.55)
    for i in range(1, nt):
        x = X0 + tw * i
        c.line(x, Y0, x, Y1, 0.45, color=N)
    B.break_line(c, xb - 18, Y0 - 14, xb + 12, Y1 + 18)
    B.arrow(c, [(X1 - 14, 1170), (xb + 26, 1170)], w=0.45)
    B.small(c, 1535, 1150, 'DN', size=4.2)
    B.small(c, X0 + tw * 2, 1150, 'UP', size=4.0)
    B.arrow(c, [(X0 + 8, 1170), (X0 + tw * 3.5, 1170)], w=0.45)


def kitchen(c):
    N = B.NAVY
    # top run now runs on to the nook (peninsula removed)
    B.counter(c, [(2286, 559), (2420, 559), (2420, 636), (2286, 636)])
    c.line(2286, 559, 2286, 636, 0.9, color='#ffffff')       # join with the existing run
    c.line(2300, 600, 2410, 600, 0.6, color=N, dash=c.dash(3, 2))   # wall cabinets
    # large island 9'-0" x 4'-0" with seating on the gallery side
    x0, x1, y0, y1 = 1922.0, 2262.0, 768.0, 919.0
    B.box(c, x0, y0, x1, y1, sw=0.6)
    c.line(x0, y1 - 38, x1, y1 - 38, 0.35, color=N, dash=c.dash(2.5, 1.6))   # seating overhang
    for i in range(4):
        cx = x0 + (x1 - x0) * (i + 0.5) / 4
        c.circle(cx, y1 + 30, 22, sw=0.45, color=B.GREY)
    B.small(c, (x0 + x1) / 2, y0 + 42, 'ISLAND', size=4.2)


def coffee_bar(c):
    N = B.NAVY
    B.box(c, 2492, 980, 2800, 1060, sw=0.55)
    c.line(2492, 1022, 2800, 1022, 0.45, color=N, dash=c.dash(3, 2))     # open shelves above
    B.box(c, 2716, 984, 2796, 1056, sw=0.4)                             # beverage fridge
    B.small(c, 2756, 1020, 'BEV.', size=3.4)
    B.small(c, 2600, 1001, 'COFFEE BAR', size=4.0)


def lockers(c):
    N = B.NAVY
    x0, x1, y0, y1 = 1990.0, 2140.0, 1292.0, 1347.0
    B.box(c, x0, y0, x1, y1, sw=0.55)
    for i in (1, 2):
        x = x0 + (x1 - x0) * i / 3
        c.line(x, y0, x, y1, 0.45, color=N)
    c.line(x0, y1 - 15, x1, y1 - 15, 0.4, color=N, dash=c.dash(2.5, 1.6))   # bench seat edge
    B.small(c, (x0 + x1) / 2, (y0 + y1) / 2 - 6, 'LOCKERS', size=3.6, bg='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 1325, 610, 'TWO-STORY\nFAMILY ROOM', '18\'-1" × 17\'-0"')
    L(c, 763, 790, 'LIBRARY', '10\'-10" × 13\'-2"')
    L(c, 2035, 705, 'KITCHEN', '19\'-8" × 13\'-2"')
    L(c, 2620, 785, 'BREAKFAST\nNOOK', '10\'-0" × 13\'-2"')
    L(c, 815, 1615, 'LIVING ROOM', '13\'-7" × 13\'-10"', 'OPT. TRAY CEILING')
    L(c, 1760, 1605, 'DINING ROOM', '13\'-9" × 13\'-10"', 'OPT. TRAY CEILING')
    L(c, 1262, 1655, 'TWO-STORY\nFOYER')
    L(c, 1455, 1310, 'GALLERY', name_pt=5.4)
    L(c, 2540, 1190, 'LAUNDRY', name_pt=5.4)
    L(c, 2380, 1745, 'TWO-CAR GARAGE', '21\'-4" × 19\'-10"')
    L(c, 1255, 1970, 'CONC. PORCH', name_pt=4.8)
    L(c, 618, 1128, 'PDR.\nROOM', name_pt=4.6)
    L(c, 1745, 1175, 'HALL', name_pt=4.8)
    c.line(1863.5, 1076, 1863.5, 1278, 0.6, color=B.NAVY)          # butler's pantry counter edge
    S(c, 1838, 1176, "BUTLER'S PANTRY", size=3.6, rotate=-90)
    B.dashed_rect(c, 636, 1442, 964, 1736, w=0.45)                  # optional tray ceilings
    B.dashed_rect(c, 1556, 1426, 1893, 1736, w=0.45)
    S(c, 2040, 1122, 'PANTRY', size=3.8)
    S(c, 795, 1222, 'CLOSET', size=3.6)
    S(c, 2280, 1298, 'CLOSET', size=3.6, rotate=-90)
    S(c, 2228, 1030, 'UP', size=3.8)
    o = B.OPT
    S(c, 1325, 115, 'OPTIONAL 4\'-0" FAMILY ROOM EXTENSION', size=3.6, color=o)
    S(c, 2375, 115, 'OPTIONAL MORNING ROOM', size=3.6, color=o)
    S(c, 760, 495, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 2245, 495, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 285, 1648, 'OPT. CONSERVATORY', size=3.6, color=o)
    S(c, 285, 1676, 'OR IN-LAW SUITE', size=3.6, color=o)
    S(c, 1705, 1873, 'ELEVATION D', size=3.4, color=o)
    S(c, 810, 2045, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 1710, 2045, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 3045, 2100, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)
    S(c, 2845, 1148, 'OPT. DOOR', size=3.4, color=o, rotate=-90)
    S(c, 2845, 2008, 'OPT. DOOR', size=3.4, color=o, rotate=-90)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP, add=STAIR_WALLS)
    drop = TEXT + STAIR + KITCHEN + DESK + BENCH + PDR_SINK + NOOK_DOORS + TRAYS
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 690, 1277, 'up', 24, 19)                      # powder room vanity
    kitchen(c)
    coffee_bar(c)
    B.double_door(c, (2493, 559), (2735, 559), side=1)        # french doors to the rear
    lockers(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
