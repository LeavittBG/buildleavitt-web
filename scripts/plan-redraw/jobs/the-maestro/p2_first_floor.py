"""The Maestro - FIRST FLOOR (brochure page 2, image xref 18), redrawn clean.

Source raster 2450x2728 px placed at 446.4 dpi; 46.1 px/ft (garage 19'-5" inside = 896 px,
20'-10" = 964 px; library 10'-1" = 462 px, 11'-10" = 544 px).
Traced: walls, windows, linework (doors, cabinets, stairs, dashed options). The kitchen bay's
windows have glazing lines inside them, so the tracer reads them as gaps; they are set by hand
(BAY_WINDOWS) with the wall filled behind them.
Modernised (Kyle, October 31, 2026): powder-room pedestal sink -> 24" vanity.
Left as drawn: the stairs are straight flights (no flare or bullnose); the kitchen has one island
and no peninsula; there is no desk or garage-entry bench, and the pantry is a small closet.
"""
import math

import blib as B
from shapely.geometry import Polygon

PAGE, XREF = 2, 18
K, PXFT = 446.4, 46.1

TEXT = [(1880, 46, 2214, 88), (1826, 606, 2066, 646), (2168, 740, 2272, 782), (1220, 868, 1518, 1042),
        (1804, 912, 2150, 970), (213, 976, 504, 1090), (24, 972, 68, 1120), (128, 1118, 202, 1242),
        (632, 1244, 677, 1298), (801, 1270, 844, 1322), (161, 1350, 277, 1467), (684, 1393, 864, 1448),
        (390, 1495, 540, 1550), (2028, 1188, 2072, 1287), (1866, 1381, 2158, 1494), (228, 1788, 490, 1968),
        (126, 1696, 205, 1806), (24, 1803, 68, 1942), (650, 1883, 888, 1998), (1042, 1738, 1300, 1916),
        (634, 2278, 897, 2334), (186, 2396, 496, 2438), (1020, 2396, 1332, 2438), (1704, 2196, 2068, 2312),
        (2353, 2472, 2396, 2632)]
PDR_SINK = [(262, 1512, 360, 1593)]
WIN_DROP = [(900, 940, 940, 1300), (740, 1220, 800, 1280), (1650, 1700, 1840, 1760), (895, 940, 925, 975)]

# the wall between the two stair flights is drawn hollow at its foot in the source
STAIR_WALL = (756, 955, 780, 1242)
STAIR_WALL_E = (925, 900, 944, 1280)      # the up flight's east wall, mostly navy in the source

# kitchen bay windows: (centre, length, wall thickness, angle)
BAY_T = 29.0
BAY_WINDOWS = [((2426.5, 1141.5), 93, BAY_T, 90.0), ((2426.5, 1250.0), 100, BAY_T, 90.0),
               ((2426.5, 1357.5), 95, BAY_T, 90.0), ((2377.0, 979.0), 94, BAY_T, 45.0),
               ((2377.0, 1501.0), 94, BAY_T, 135.0)]


def _rect(center, length, thick, ang):
    (cx, cy), a = center, math.radians(ang)
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    L, T = length / 2.0 + 2, thick / 2.0
    return Polygon([(cx + su * L * ux + sv * T * vx, cy + su * L * uy + sv * T * vy)
                    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))])


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # names centred in their rooms: open floor, inside the tray outlines, with the island in the kitchen
    L(c, 1347, 985, 'TWO-STORY\nFAMILY ROOM', '17\'-6" × 13\'-2"')
    L(c, 357, 1047, 'LIBRARY', '10\'-1" × 11\'-10"')
    L(c, 1992, 915, 'BREAKFAST NOOK')
    L(c, 2037, 1455, 'KITCHEN', '12\'-0" × 22\'-1"')
    L(c, 774, 1420, 'GALLERY', name_pt=5.8)
    L(c, 215, 1410, 'PDR.\nROOM', name_pt=5.2)
    L(c, 359, 1873, 'LIVING ROOM', '10\'-1" × 11\'-4"', 'OPT. TRAY CEILING')
    L(c, 1170, 1821, 'DINING ROOM', '9\'-11" × 13\'-8"', 'OPT. TRAY CEILING')
    L(c, 767, 1950, 'TWO-STORY\nFOYER')
    L(c, 765, 2302, 'CONC. PORCH', name_pt=5.2)
    L(c, 1874, 2211, 'TWO-CAR GARAGE', '19\'-5" × 20\'-10"')
    S(c, 465, 1522, 'CLOSET', size=4.0)
    S(c, 2220, 761, 'PANTRY', size=4.0)
    S(c, 2050, 1237, 'ISLAND', size=3.8, rotate=-90)
    S(c, 655, 1283, 'DN', size=4.2, rotate=-90)
    S(c, 825, 1296, 'UP', size=4.2, rotate=-90)
    S(c, 2046, 67, 'OPTIONAL MORNING ROOM', size=3.8, color=o)
    S(c, 1945, 626, 'OPT. PATIO DOOR', size=3.8, color=o)
    S(c, 46, 1046, 'OPT. BAY', size=3.8, color=o, rotate=-90)
    S(c, 46, 1872, 'OPT. BAY', size=3.8, color=o, rotate=-90)
    for y in (1180, 1751):
        S(c, 143, y, 'OPT.', size=3.6, color=o, rotate=-90)
        S(c, 181, y, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 341, 2417, 'PORCH W/ ELEVATION D', size=3.6, color=o)
    S(c, 1176, 2417, 'PORCH W/ ELEVATION C', size=3.6, color=o)
    S(c, 2374, 2552, 'OPT. DOOR', size=3.6, color=o, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP, add=[_rect(*w) for w in BAY_WINDOWS] + [STAIR_WALL, STAIR_WALL_E])
    wins = list(wins) + BAY_WINDOWS
    drop = TEXT + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 314, 1594, 'up', 24, 19)              # powder room vanity (was a pedestal sink)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
