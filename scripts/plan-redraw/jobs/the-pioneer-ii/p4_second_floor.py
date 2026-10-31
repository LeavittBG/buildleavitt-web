"""The Pioneer II - SECOND FLOOR (brochure page 4, image xref 25), redrawn clean.

Source: assets-src/plans/originals/the-pioneer-ii.pdf page 4, raster 2289x1988 px at 438 dpi,
about 37.8 px/ft; coordinates are this raster's pixels. The stair and its floor opening are The
Pioneer I's second floor moved up 75 px (measured: identical there), so The Pioneer I job's stair()
draws them through that shift. The rest of the floor is The Pioneer II's own (owner's suite over
the family room, exercise room).

Part of the owner's suite is drawn with a lighter wall fill; bhelp.light_walls() reads it.

Kept from the source by tracing: walls, windows, doors, closets, vanities, toilets, the steps up
to the owner's bedroom, dashed option outlines. Redrawn by hand (Kyle, October 31, 2026):
  - main stair: lower flight straightened as on The Pioneer I (straight 45-degree flight, square
    cut), upper flight and wood railings redrawn clean
  - owner's bath: the oval drop-in soaker tub on its platform between the two vanities becomes one
    large walk-in tiled shower (about 6'-5" x 3'-10": glass front with an open entry, bench at the
    left end, linear drain on the window wall); the old 3'-0" shower stall becomes a towel closet
    behind its existing door, as on The Pioneer I
  - hall bath and bedroom 4 bath keep their tub/shower, redrawn as plain rectangular tubs
  - all lettering in Roboto Condensed, room names centred in their rooms
"""
import importlib.util
import os
import blib as B
import bhelp

PAGE, XREF = 4, 25
DY = -75.0

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p4_second.py')
_s = importlib.util.spec_from_file_location('pioneer_i_second', _p)
P1 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(P1)

TEXT = [(55, 322, 408, 358), (1528, 322, 1882, 358), (640, 405, 940, 560), (100, 595, 335, 685),
        (395, 665, 475, 735), (1105, 665, 1185, 735), (1445, 578, 1605, 685), (1935, 530, 2195, 625),
        (695, 802, 805, 848), (1360, 802, 1462, 848), (1365, 905, 1495, 952), (1910, 850, 2035, 898),
        (1205, 1028, 1268, 1072), (218, 990, 308, 1032), (350, 982, 460, 1022), (1645, 1278, 1738, 1312),
        (1500, 1372, 1602, 1412), (1792, 1372, 1832, 1488), (942, 1502, 988, 1622), (125, 1330, 370, 1425),
        (620, 1470, 850, 1565), (1095, 1425, 1330, 1510), (1940, 1260, 2180, 1350), (652, 1343, 803, 1374),
        (695, 1278, 805, 1322), (1095, 1698, 1245, 1728), (1750, 1858, 1965, 1892), (1238, 668, 1302, 738)]
STAIR = [(528, 950 + DY, 1040, 1322 + DY)]
OB_TUB = [(1372, 404, 1617, 556)]
OB_SHOWER = [(1738, 443, 1855, 630)]
TUBS = [(30, 916, 130, 1098), (1638, 1334, 1739, 1515)]
# the old shower's left side was glass with a door; as a closet it is a wall either side of it
ADD_WALLS = [(1729, 470, 1739, 504), (1729, 594, 1739, 628)]


def owners_shower(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    x0, y0, x1, y1 = 1374.0, 406.0, 1615.0, 552.0
    B.box(c, x0, y0, x1, y1, sw=0.45)
    B.box(c, x0, y0, x0 + 15 * k, y1, sw=0.45)                                 # bench
    B.small(c, x0 + 7.5 * k, (y0 + y1) / 2, 'BENCH', size=3.0, color=B.GREY, rotate=-90)
    c.rect(x0 + 22 * k, y0 + 4 * k, (x1 - x0) - 30 * k, 1.6 * k, sw=0.35, color=N)   # linear drain
    c.line(x0, y1, x1 - 26 * k, y1, 1.1, color=N)                                # glass front, open entry
    B.small(c, (x0 + x1) / 2 + 20, (y0 + y1) / 2 + 6, 'SHOWER', size=3.8)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    S(c, 230, 340, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 1705, 340, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    L(c, 790, 417, "OWNER'S BEDROOM", '18\'-1" × 17\'-0"', 'OPT. TRAY CEILING')
    L(c, 215, 645, 'SITTING ROOM', '11\'-2" × 13\'-2"')
    S(c, 433, 700, 'UP', size=3.6, rotate=-45)
    S(c, 1147, 700, 'UP', size=3.6, rotate=45)
    L(c, 1490, 628, "OWNER'S\nBATH", name_pt=5.0)
    S(c, 1794, 525, 'TOWEL', size=3.4)
    S(c, 1794, 547, 'CLOSET', size=3.4)
    L(c, 2066, 585, 'EXERCISE ROOM', '10\'-5" × 9\'-6"')
    S(c, 1271, 703, 'LINEN', size=3.2, rotate=45)
    L(c, 750, 825, 'HALL', name_pt=5.0)
    L(c, 1410, 825, 'HALL', name_pt=5.0)
    S(c, 1430, 930, 'CLOSET', size=4.0)
    S(c, 1972, 875, 'W.I.C.', size=4.2)
    S(c, 1237, 1050, 'DN', size=4.0)
    S(c, 263, 1011, 'BATH', size=4.4, weight=700)
    S(c, 405, 1002, 'W.I.C.', size=4.2)
    L(c, 750, 1300, 'HALL', name_pt=5.0)
    S(c, 728, 1359, 'WOOD RAILING', size=3.4)
    L(c, 250, 1420, 'BEDROOM 3', '13\'-11" × 14\'-3"')
    L(c, 727, 1515, 'OPEN TO\nFOYER BELOW', name_pt=5.4)
    L(c, 1220, 1460, 'BEDROOM 2', '14\'-1" × 10\'-4"')
    S(c, 965, 1562, 'CLOSET', size=3.6, rotate=-90)
    S(c, 1691, 1295, 'LINEN', size=3.6)
    S(c, 1551, 1392, 'BATH', size=4.4, weight=700)
    S(c, 1812, 1430, 'CLOSET', size=3.6, rotate=-90)
    L(c, 2047, 1312, 'BEDROOM 4', '13\'-5" × 11\'-0"')
    S(c, 1170, 1713, 'ELEVATION D', size=3.4, color=o)
    S(c, 1857, 1876, 'OPT. SITTING ROOM', size=3.6, color=o)


def stair_shifted(c):
    c.add(f'<g transform="translate(0 {DY:g})">')
    P1.stair(c)
    c.add('</g>')


def draw(c, img):
    walls, wins = B.trace(img, add=ADD_WALLS + [bhelp.light_walls(img)])
    drop = TEXT + STAIR + OB_TUB + OB_SHOWER + TUBS
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, bhelp.thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.tub(c, 30, 916, 130, 1098)
    B.tub(c, 1638, 1334, 1739, 1515)
    owners_shower(c)
    stair_shifted(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
