"""The Draftsman - SECOND FLOOR (brochure page 4, image xref 27), redrawn clean.

Source raster 2475x2146 px placed at 420.9 dpi, 38.0 px/ft (bedroom 3 12'-10" wide = 487 px).

Kept by tracing: walls, windows, doors, closets, bath fixtures (the hall bath keeps its tub),
stair, dashed beam and option lines.
Changed (Kyle, October 31, 2026): the stair's rounded starting step, seen from above at the
left end, is square-cut to match the first floor; lettering re-set, room names centred.
"""
import blib as B
from shapely.geometry import Polygon

PAGE, XREF = 4, 27
B.K, B.PXFT = 420.9, 38.0

TEXT = [(994, 534, 1239, 733), (1576, 703, 1824, 833), (2081, 912, 2342, 1015), (1085, 1430, 1342, 1533),
        (1509, 1060, 1564, 1104), (1649, 1076, 1742, 1124), (1458, 1221, 1551, 1273), (918, 1219, 1046, 1270),
        (1672, 1276, 1770, 1328), (1912, 1243, 2019, 1293), (2212, 1241, 2334, 1290)]
LINEN_TEXT = Polygon([(1512, 1384), (1566, 1438), (1586, 1418), (1532, 1364)])
STAIR_CAP = [(1010, 975, 1057, 1168)]
WIN_DROP = [(1120, 1000, 1180, 1050), (1490, 1030, 1520, 1175)]


def stair_cap(c):
    N = B.NAVY
    c.polyline([(1022, 1168), (1022, 990), (1060, 990)], w=0.6, color=N)    # square-cut first step
    c.rect(1037, 1010, 12, 12, sw=0.4, color=N, fill=N)                     # square newel
    c.line(1049, 1016, 1060, 1016, 0.9, color=N)


def labels(c):
    L, S = B.label, B.small
    L(c, 1117, 600, 'OPEN TO\nFAMILY ROOM\nBELOW', note='OPT. BEAMED CEILING')
    L(c, 1696, 750, 'LOFT', '13\'-4" × 14\'-1"', 'OPT. BEDROOM 4')
    L(c, 2202, 972, 'BEDROOM 3', '12\'-10" × 14\'-5"')
    L(c, 1212, 1480, 'BEDROOM 2', '21\'-5" × 16\'-0"')
    L(c, 1720, 1302, 'BATH', name_pt=5.4)
    L(c, 1695, 1100, 'HALL', name_pt=5.4)
    L(c, 1504, 1247, 'HALL', name_pt=5.0)
    L(c, 1966, 1268, 'MECH.', name_pt=5.0)
    S(c, 982, 1244, 'CLOSET', size=4.0)
    S(c, 2266, 1265, 'CLOSET', size=4.0)
    S(c, 1548, 1401, 'LINEN', size=3.4, rotate=45)
    S(c, 1537, 1082, 'DN', size=4.0)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR_CAP
    nv, gr = B.lineart(img, walls, drop=drop)
    hl = B.hairlines(img, walls, drop)
    B.draw_geom(c, gr.difference(LINEN_TEXT), B.OPT)
    B.draw_geom(c, nv.difference(LINEN_TEXT), B.NAVY)
    B.draw_geom(c, hl.difference(LINEN_TEXT), B.NAVY)
    stair_cap(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
