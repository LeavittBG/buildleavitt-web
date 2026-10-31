"""The Impressionist - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2766x3087 px placed at 505.2 dpi; 46.15 px/ft (garage 20'-7" inside = 950 px).
Traced: walls, windows, linework (doors, cabinets, stair, dashed options).
Modernised (Kyle, October 31, 2026):
  - owner's bath: the oval drop-in tub on its deck becomes a walk-in shower (glass, bench, linear
    drain) in the same alcove; the old shower stall across the room, behind a wall, becomes a
    towel closet behind its existing door
  - powder room: pedestal sink -> 24" vanity
Left as drawn: one island and no peninsula in the kitchen; the stair is straight with a landing;
the pantry and butler's pantry are reach-in; no desk or garage-entry bench.
"""
import math
from shapely.geometry import Polygon
import blib as B

PAGE, XREF = 2, 15
K, PXFT = 505.2, 46.15

TEXT = [(1995, 50, 2245, 95), (168, 205, 242, 325), (168, 760, 242, 882), (400, 487, 775, 672),
        (1210, 457, 1512, 640), (1975, 487, 2275, 665), (2507, 450, 2547, 646), (0, 937, 40, 1232),
        (2665, 1410, 2705, 1700), (1268, 1105, 1446, 1155), (2035, 1200, 2382, 1252),
        (268, 1120, 397, 1170), (773, 1120, 905, 1170), (1082, 1243, 1132, 1382), (425, 1393, 597, 1507),
        (1703, 1405, 1812, 1446), (1402, 1435, 1442, 1500), (1113, 1610, 1222, 1660),
        (2200, 1600, 2235, 1690), (1638, 1757, 1817, 1805), (193, 1793, 297, 1900),
        (526, 1803, 656, 1850), (2048, 1790, 2345, 1897), (1112, 1935, 1170, 1978),
        (366, 2285, 626, 2337), (1080, 2280, 1365, 2457), (1873, 2510, 2235, 2615),
        (2575, 2832, 2620, 2980)]
TUB = [(166, 1299, 348, 1677)]                 # oval tub and its deck
OLD_SHOWER = [(724, 1459, 852, 1670)]          # the X and drain of the old stall
PDR_SINK = [(188, 1695, 292, 1772)]
WIN_DROP = [(1360, 1490, 1510, 1525), (1650, 2060, 1840, 2095)]   # stair-top and garage-step jambs

R2 = math.sqrt(2)


def band(cx, cy, length, height):
    """A rectangle along the 45-degree (rising to the right) text line, centred on (cx, cy)."""
    ux, uy = 1 / R2, -1 / R2
    vx, vy = 1 / R2, 1 / R2
    L, H = length / 2.0, height / 2.0
    return Polygon([(cx - ux * L - vx * H, cy - uy * L - vy * H), (cx + ux * L - vx * H, cy + uy * L - vy * H),
                    (cx + ux * L + vx * H, cy + uy * L + vy * H), (cx - ux * L + vx * H, cy - uy * L + vy * H)])


BUTLER_TEXT = [band(1621, 1272, 150, 44), band(1650, 1302, 124, 44)]


def owners_bath(c):
    # walk-in shower in the old tub alcove: glass along the bath side with the entry at the top
    x0, y0, x1, y1 = 165.0, 1298.0, 349.0, 1678.0
    B.shower(c, x0, y0, x1, y1, glass=((x1, 1405), (x1, 1567)), drain='linear')
    k = PXFT / 12.0
    B.box(c, x0, y1 - 15 * k, x1, y1, sw=0.4)                     # 15" bench at the far end
    B.small(c, (x0 + x1) / 2, y1 - 7.5 * k, 'BENCH', size=3.2, color=B.GREY)
    B.small(c, (x0 + x1) / 2, (y0 + y1) / 2 - 20, 'SHOWER', size=4.0)
    # old stall -> towel closet (its door stays)
    B.label(c, 788, 1565, 'TOWEL\nCLOSET', name_pt=4.2)


def butlers_pantry(c):
    # upper-cabinet dashes the lettering sat on, set again
    c.line(1579, 1340, 1632, 1286, 0.75, color=B.NAVY, cap='round')
    c.line(1659, 1260, 1703, 1217, 0.75, color=B.NAVY, cap='round')
    B.small(c, 1612, 1268, "BUTLER'S", size=3.8, rotate=-45)
    B.small(c, 1655, 1304, 'PANTRY', size=3.8, rotate=-45)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # names centred in their rooms: inside tray outlines, on the open floor, over the island
    L(c, 588, 548, "OWNER'S BEDROOM", '18\'-5" × 18\'-2"', 'OPT. TRAY CEILING')
    L(c, 1355, 540, 'DINING ROOM', '14\'-0" × 18\'-0"', 'OPT. TRAY CEILING')
    L(c, 2125, 565, 'FAMILY ROOM', '18\'-5" × 18\'-2"', 'OPT. BEAMED CEILING')
    L(c, 1357, 1130, 'GALLERY', name_pt=5.8)
    L(c, 2210, 1226, 'BREAKFAST NOOK', name_pt=5.8)
    L(c, 2205, 1845, 'KITCHEN', '15\'-1" × 22\'-6"')
    L(c, 525, 1432, "OWNER'S\nBATH", name_pt=5.2)
    L(c, 1168, 1635, 'HALL', name_pt=5.4)
    L(c, 1727, 1781, 'LAUNDRY', name_pt=5.0)
    L(c, 245, 1846, 'PDR.\nROOM', name_pt=4.6)
    L(c, 591, 1826, 'FOYER', name_pt=5.6)
    L(c, 496, 2311, 'CONC. PORCH', name_pt=5.2)
    L(c, 1222, 2368, 'LIVING ROOM', '15\'-0" × 11\'-8"', 'OPT. TRAY CEILING')
    L(c, 2072, 2565, 'TWO-CAR GARAGE', '20\'-7" × 21\'-2"')
    S(c, 332, 1145, 'W.I.C.', size=4.2)
    S(c, 839, 1145, 'W.I.C.', size=4.2)
    S(c, 1107, 1312, 'CLOSET', size=3.8, rotate=-90)
    S(c, 1757, 1426, 'PANTRY', size=3.8)
    S(c, 1422, 1467, 'DN', size=4.0, rotate=-90)
    S(c, 2218, 1645, 'ISLAND', size=3.6, rotate=-90)
    S(c, 1140, 1958, "UP", size=4.0)
    S(c, 2527, 548, 'GAS FIREPLACE', size=3.4, rotate=-90)
    S(c, 2120, 72, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 188, 265, 'OPT.', size=3.4, color=o, rotate=-90)
    S(c, 222, 265, 'WINDOW', size=3.4, color=o, rotate=-90)
    S(c, 188, 821, 'OPT.', size=3.4, color=o, rotate=-90)
    S(c, 222, 821, 'WINDOW', size=3.4, color=o, rotate=-90)
    S(c, 20, 1085, 'OPT. 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2685, 1555, 'OPT. 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2598, 2906, 'OPT. DOOR', size=3.4, color=o, rotate=-90)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    c.K = K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + TUB + OLD_SHOWER + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    hl = B.hairlines(img, walls, drop)
    for p in BUTLER_TEXT:                       # slanted lettering: erase with bands, not boxes
        nv, gr, hl = nv.difference(p), gr.difference(p), hl.difference(p)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, hl, B.NAVY)
    owners_bath(c)
    butlers_pantry(c)
    B.vanity(c, 240, 1697, 'down', 24, 19)          # powder room vanity (was a pedestal sink)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
