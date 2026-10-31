"""The Novel - SECOND FLOOR (brochure page 4, image xref 25), redrawn clean.

Source raster 2226x2051 px placed at 412.4 dpi, about 37.95 px/ft (same scale as the first floor).

Changed (Kyle, October 31, 2026):
  - owner's bath: the oval soaker tub on its chamfered deck between the two vanities becomes one
    walk-in shower filling the deck (about 8'-5" x 4'-3"), glass front with an open entry, bench at
    the right end, linear drain along the window wall
  - the old corner shower stall, walled off from it, becomes a towel closet behind its door
  - the stair's flared, round-ended start (seen from above) is squared to match the first floor
  - lettering re-set, room names centred
Kept: the hall bath's tub; the cathedral-ceiling lines over the bath outside the shower.
"""
import blib as B

PAGE, XREF = 4, 25
B.K, B.PXFT = 412.4, 37.95

TEXT = [(28, 385, 96, 485), (165, 505, 412, 600), (720, 410, 960, 605), (70, 800, 195, 840),
        (598, 786, 892, 822), (668, 868, 822, 898), (338, 934, 410, 968), (200, 1040, 298, 1086),
        (637, 990, 731, 1035), (948, 915, 982, 975), (1016, 913, 1112, 958), (1442, 580, 1585, 680),
        (1355, 717, 1502, 810), (1905, 555, 2010, 605), (1637, 975, 1935, 1185), (70, 1210, 190, 1250),
        (803, 1104, 958, 1135), (165, 1433, 412, 1528), (600, 1436, 820, 1528), (995, 1527, 1248, 1620),
        (1428, 1478, 1535, 1520), (1630, 1640, 1765, 1840), (1788, 1550, 1825, 1830)]
OB_TUB = [(1270, 402, 1584, 572)]
OLD_STALL = [(1138, 700, 1262, 852), (1262, 800, 1290, 852)]
STAIR_START = [(690, 1150, 868, 1325)]
WIN_DROP = [(1170, 1240, 1200, 1290)]


def owners_shower(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    x0, y0, x1, y1 = 1268.0, 401.0, 1586.0, 564.0
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill='#ffffff')
    c.line(x0, y0, x0, y1, 0.45, color=N)
    c.line(x1, y0, x1, y1, 0.45, color=N)
    B.box(c, x1 - 15 * k, y0 + 2, x1, y1, sw=0.45)                      # bench, 15" deep
    B.small(c, x1 - 7.5 * k, (y0 + y1) / 2, 'BENCH', size=3.0, color=B.GREY, rotate=-90)
    c.rect(x0 + 12 * k, y0 + 5 * k, (x1 - x0) - 30 * k, 1.6 * k, sw=0.35, color=N)   # linear drain
    c.line(x0 + 30 * k, y1, x1, y1, 1.1, color=N)                          # glass, open entry left
    B.small(c, (x0 + x1 - 15 * k) / 2, (y0 + y1) / 2 + 6, 'SHOWER', size=3.8)


def towel_closet(c):
    c.line(1182, 712, 1182, 845, 0.45, color=B.NAVY, dash=c.dash(2.5, 1.6))
    B.small(c, 1212, 768, 'TOWEL', size=3.4)
    B.small(c, 1212, 790, 'CLOSET', size=3.4)


def stair_start(c):
    """Squared start: straight stringer along the hall edge, square-cut first step, square newel."""
    N = B.NAVY
    c.rect(700, 1270, 168, 14, sw=0, fill=N)
    c.line(712, 1277, 868, 1277, 0.35, color='#ffffff')
    for x in (706, 737, 768, 800, 831):
        c.line(x, 1150, x, 1270, 0.9, color=N)
    c.rect(697, 1266, 21, 21, sw=0.5, color=N, fill=N)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 288, 552, 'BEDROOM 4', '13\'-9" × 15\'-9"')
    L(c, 840, 505, 'OPEN TO\nFAMILY ROOM\nBELOW', None, 'OPT. BEAMED CEILING')
    L(c, 1430, 760, "OWNER'S\nBATH", name_pt=5.6)
    L(c, 1875, 1066, "OWNER'S BEDROOM", '21\'-9" × 21\'-9"', 'OPT. TRAY CEILING')
    L(c, 288, 1480, 'BEDROOM 3', '13\'-9" × 15\'-9"')
    L(c, 710, 1482, 'OPEN TO\nFOYER BELOW', name_pt=5.6)
    L(c, 1112, 1573, 'BEDROOM 2', '13\'-0" × 15\'-6"')
    L(c, 1697, 1740, 'SITTING\nROOM', '10\'-1" × 10\'-4"', name_pt=5.6)
    L(c, 249, 1063, 'BATH', name_pt=5.4)
    L(c, 684, 1012, 'HALL', name_pt=5.6)
    L(c, 1064, 935, 'MECH.', name_pt=5.0)
    S(c, 132, 820, 'W.I.C.', size=4.2)
    S(c, 130, 1230, 'W.I.C.', size=4.2)
    S(c, 1957, 580, 'W.I.C.', size=4.6)
    S(c, 1481, 1499, 'W.I.C.', size=4.2)
    S(c, 374, 951, 'LINEN', size=3.2)
    S(c, 965, 945, 'LINEN', size=3.0, rotate=-90)
    S(c, 745, 883, 'WOOD RAILING', size=3.2)
    S(c, 880, 1119, 'WOOD RAILING', size=3.2)
    S(c, 1513, 630, 'OPT. CATHEDRAL CEILING', size=3.2, color=o)
    S(c, 1875, 1172, 'OPT. CATHEDRAL CEILING', size=3.2, color=o)
    S(c, 1806, 1690, 'OPT. CATHEDRAL CEILING', size=3.0, color=o, rotate=-90)
    S(c, 745, 804, 'OPTIONAL JULIET BALCONY', size=3.2, color=o)
    S(c, 62, 435, 'OPT. WINDOW', size=3.0, color=o, rotate=-90)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + OB_TUB + OLD_STALL + STAIR_START
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_shower(c)
    towel_closet(c)
    stair_start(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
