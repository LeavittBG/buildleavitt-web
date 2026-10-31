"""The Poet - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2787x2577 px placed at 421.7 dpi (this brochure's plans print slightly smaller than
The Pioneer I's), about 38.0 px/ft (garage 23'-2" deep inside = 880 px).

Kept by tracing: walls, windows, doors, cabinets, appliances, stairs, dashed options.
Changed (Kyle, October 31, 2026): powder room pedestal sink -> 24" vanity; lettering re-set.
Left as is: the kitchen already has one island (with the sink) and no peninsula; the stairs are
straight; the pantry is already a walk-in; there is no desk or garage-entry bench.
"""
import blib as B
from shapely.geometry import Polygon

PAGE, XREF = 2, 15
B.K, B.PXFT = 421.7, 38.0

TEXT = [(1040, 8, 1218, 44), (1562, 8, 1838, 44), (1038, 296, 1236, 338), (1903, 350, 1941, 545),
        (965, 578, 1255, 684), (2110, 482, 2365, 584), (1738, 688, 1832, 738), (2508, 652, 2547, 783),
        (2618, 747, 2657, 868), (2207, 877, 2403, 918), (1752, 909, 1853, 945), (2003, 882, 2118, 933),
        (1703, 1112, 1808, 1165), (1303, 1222, 1337, 1303), (381, 1222, 412, 1388), (548, 1252, 808, 1408),
        (1186, 1457, 1434, 1553), (2131, 1385, 2434, 1488), (1810, 1427, 1844, 1513), (1713, 1667, 1750, 1718),
        (1040, 1712, 1072, 1801), (1040, 2067, 1072, 2158), (566, 1882, 789, 2033), (1252, 1952, 1363, 1998),
        (1727, 1912, 1888, 1961), (1982, 2019, 2078, 2118), (1440, 2152, 1493, 2195), (605, 2235, 751, 2273),
        (1240, 2340, 1460, 2391), (50, 2497, 310, 2535), (555, 2497, 813, 2535)]
PDR_SINK = [(2132, 1928, 2200, 2042)]
# the diagonal "OPT. PATIO DOOR" sits just above the door's own line: erase it with a slanted band
DIAG_TEXT = Polygon([(1462, 456), (1650, 644), (1690, 604), (1502, 416)])
WIN_DROP = [(1680, 1640, 1800, 1690), (1515, 2220, 1550, 2270)]


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    # names centred on each room's open floor (inside the tray outline in the dining room,
    # under the island in the kitchen, whose island runs the long way)
    L(c, 1105, 630, 'BREAKFAST NOOK', '17\'-8" × 14\'-6"')
    L(c, 2225, 655, 'OFFICE', '13\'-8" × 18\'-8"')
    L(c, 688, 1300, 'FAMILY ROOM', '16\'-6" × 19\'-8"', 'OPT. BEAMED CEILING')
    L(c, 1362, 1515, 'KITCHEN', '16\'-1" × 20\'-7"')
    L(c, 2304, 1464, 'TWO-CAR GARAGE', '23\'-7" × 23\'-2"')
    L(c, 678, 1952, 'DINING ROOM', '16\'-2" × 11\'-5"', 'OPT. TRAY CEILING')
    L(c, 1340, 1979, 'FOYER')
    L(c, 1800, 1935, 'MUDROOM', name_pt=5.6)
    L(c, 2030, 2085, 'PDR.\nROOM', name_pt=5.0)
    L(c, 1351, 2368, 'CONC. PORCH', name_pt=5.2)
    L(c, 1785, 713, 'HALL', name_pt=5.4)
    S(c, 1802, 927, 'PANTRY', size=3.8)
    S(c, 2060, 907, 'W.I.C.', size=4.2)
    S(c, 1755, 1138, 'W.I.C.', size=4.2)
    S(c, 1320, 1262, 'ISLAND', size=3.6, rotate=-90)
    S(c, 397, 1305, 'GAS FIREPLACE', size=3.4, rotate=-90)
    S(c, 1827, 1470, 'CLOSET', size=3.4, rotate=-90)
    S(c, 1056, 1757, 'CLOSET', size=3.4, rotate=-90)
    S(c, 1056, 2112, 'CLOSET', size=3.4, rotate=-90)
    S(c, 1731, 1692, 'DN', size=3.8)
    S(c, 1466, 2173, 'UP', size=3.8)
    S(c, 1128, 26, 'OPTIONAL DECK', size=3.6, color=o)
    S(c, 1700, 26, 'OPTIONAL SCREEN PORCH', size=3.6, color=o)
    S(c, 1137, 318, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 1556, 512, 'OPT. PATIO DOOR', size=3.6, color=o, rotate=45)
    S(c, 1922, 447, 'OPT. PATIO DOOR', size=3.6, color=o, rotate=-90)
    S(c, 2528, 717, 'OPT. DOOR', size=3.4, color=o, rotate=-90)
    S(c, 2638, 807, 'OPT. DECK', size=3.4, color=o, rotate=-90)
    S(c, 2305, 898, '(OPTIONAL BATH)', size=3.6, color=o)
    S(c, 678, 2254, 'ELEVATION C', size=3.4, color=o)
    S(c, 180, 2516, 'PORCH W/ ELEVATION C', size=3.4, color=o)
    S(c, 684, 2516, 'PORCH W/ ELEVATION B', size=3.4, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    nv = nv.difference(DIAG_TEXT)
    hl = B.hairlines(img, walls, drop).difference(DIAG_TEXT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hl, B.NAVY)
    B.vanity(c, 2198, 1985, 'left', 24, 19)                    # powder room vanity
    B.draw_plan_walls(c, walls, wins)
    labels(c)
