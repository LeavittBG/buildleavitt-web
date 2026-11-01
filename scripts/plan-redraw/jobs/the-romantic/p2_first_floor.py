"""The Romantic - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2313x2224 px placed at 370.4 dpi; 46.2 px/ft (garage 19'-6" inside = 901 px, its
22'-10" depth = 1055 px). Walls, windows and linework traced; lettering re-set. Modernised (Kyle,
October 31, 2026):
  - main stair: the rounded (bullnose) starting step becomes a square-cut step with square
    newels, in place; the flight, landing and basement stair are unchanged
  - powder room: pedestal sink -> 24" vanity
Left as drawn: the kitchen is an L of counters with no island or peninsula; there is no desk or
garage-entry bench; the pantry is a reach-in with no room to walk in.
"""
import blib as B

PAGE, XREF = 2, 15
K, PXFT = 370.4, 46.2

TEXT = [(850, 0, 1090, 40), (800, 325, 1150, 436), (330, 405, 620, 520), (1570, 415, 1885, 605),
        (2140, 395, 2192, 625), (695, 718, 812, 762), (928, 700, 985, 846), (740, 852, 858, 970),
        (1122, 806, 1238, 864), (1110, 962, 1135, 1042), (1135, 962, 1148, 1064), (240, 1030, 522, 1210), (722, 1302, 792, 1346),
        (578, 1360, 712, 1410), (1548, 1368, 1912, 1482), (192, 1770, 462, 1826), (792, 1745, 1092, 1922),
        (2214, 1712, 2262, 1876), (848, 2180, 998, 2226)]
STAIR_START = [(772, 1254, 821, 1482), (722, 1340, 772, 1358)]
PDR_SINK = [(770, 786, 872, 866)]
WIN_DROP = [(1080, 1015, 1225, 1045), (1040, 1400, 1075, 1440)]


def stair_start(c):
    """Square-cut first step and square newels where the rounded starting step was."""
    N = B.NAVY
    B.box(c, 789, 1281, 822, 1455, sw=0.55)
    k = 14.0
    for y in (1289, 1446):
        c.rect(806 - k / 2, y - k / 2, k, k, sw=0.4, color=N, fill=N)
    c.line(806, 1289, 1060, 1289, 0.9, color=N)                 # rails along both sides
    c.line(806, 1446, 1060, 1446, 0.9, color=N)
    B.arrow(c, [(730, 1349), (812, 1349)])
    B.small(c, 752, 1326, 'UP', size=4.4)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # knock the beamed-ceiling lines out behind the family-room label
    c.rect(1570, 415, 315, 190, sw=0, fill='#ffffff')
    L(c, 1726, 505, 'FAMILY ROOM', '20\'-0" × 14\'-9"', 'OPT. BEAMED CEILING')
    L(c, 970, 450, 'BREAKFAST NOOK', '11\'-7" × 12\'-10"')
    L(c, 452, 470, 'KITCHEN', '12\'-2" × 13\'-1"')
    L(c, 375, 1110, 'DINING ROOM', '10\'-9" × 14\'-0"', 'OPT. TRAY CEILING')
    L(c, 924, 1765, 'LIVING ROOM', '14\'-5" × 13\'-4"', 'OPT. TRAY CEILING')
    L(c, 1733, 1405, 'TWO-CAR GARAGE', '19\'-6" × 22\'-10"')
    L(c, 335, 1792, 'CONC. PORCH', name_pt=5.0)
    L(c, 645, 1385, 'FOYER', name_pt=5.8)
    L(c, 790, 920, 'PDR.\nROOM', name_pt=5.0)
    L(c, 1180, 836, 'HALL', name_pt=5.4)
    S(c, 752, 741, 'PANTRY', size=4.0)
    S(c, 957, 773, 'CLOSET', size=3.8, rotate=-90)
    S(c, 1120, 1013, 'DN', size=4.2, rotate=-90)
    B.arrow(c, [(1141, 972), (1141, 1056)])
    S(c, 2166, 510, 'GAS FIREPLACE', size=3.8, rotate=-90)
    S(c, 970, 20, 'OPT. PATIO DOOR', size=3.8, color=o)
    S(c, 923, 2203, 'OPT. BAY', size=3.8, color=o)
    S(c, 2238, 1794, 'OPT. DOOR', size=3.8, color=o, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR_START + PDR_SINK
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.vanity(c, 821, 787, 'down', 24, 19)
    stair_start(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
