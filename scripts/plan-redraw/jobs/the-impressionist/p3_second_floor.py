"""The Impressionist - SECOND FLOOR (brochure page 3, image xref 17), redrawn clean.

Source raster 2765x3083 px placed at 505.2 dpi; 46.15 px/ft (the same scale as the first floor).
Traced: walls, windows, linework. Nothing to modernise: the hall bath keeps its tub/shower and
its sinks are already in a vanity; the stair is straight. Lettering re-set as printed, room names
centred in their rooms.
"""
import blib as B

PAGE, XREF = 3, 17
K, PXFT = 505.2, 46.15

TEXT = [(318, 1298, 627, 1407), (797, 1048, 932, 1102), (1123, 1090, 1237, 1132),
        (1628, 1055, 1762, 1107), (1538, 1210, 1645, 1245), (2055, 1163, 2352, 1272),
        (1364, 1350, 1476, 1393), (1088, 1444, 1276, 1474), (1400, 1424, 1446, 1482),
        (874, 1494, 962, 1562), (945, 1680, 1330, 1792), (2013, 1730, 2302, 1842),
        (1598, 1905, 1732, 1955), (0, 1185, 45, 1477), (2662, 1405, 2706, 1702)]
WIN_DROP = [(1440, 1460, 1540, 1630), (1320, 1990, 1360, 2070)]      # stair stringers read as windows


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 500, 1330, 'BEDROOM 2', '14\'-10" × 15\'-0"')
    L(c, 2185, 1247, 'BEDROOM 3', '15\'-10" × 11\'-5"')
    L(c, 2163, 1787, 'BEDROOM 4', '16\'-11" × 11\'-3"')
    L(c, 1420, 1371, 'HALL', name_pt=5.4)
    L(c, 1137, 1736, 'OPEN TO\nFOYER/HALL BELOW', name_pt=5.2)
    L(c, 1180, 1111, 'BATH', name_pt=5.0)
    S(c, 865, 1075, 'W.I.C.', size=4.2)
    S(c, 1695, 1081, 'W.I.C.', size=4.2)
    S(c, 1665, 1930, 'W.I.C.', size=4.2)
    S(c, 1591, 1228, 'LINEN', size=3.6)
    S(c, 1182, 1459, 'WOOD RAILING', size=3.2)
    S(c, 1423, 1453, 'DN', size=4.0, rotate=-90)
    S(c, 918, 1512, 'PLANT', size=3.2)
    S(c, 918, 1548, 'SHELF', size=3.2)
    S(c, 22, 1331, 'OPT. 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2684, 1553, 'OPT. 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    c.K = K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    nv, gr = B.lineart(img, walls, drop=TEXT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
