"""The Visionary - SECOND FLOOR (brochure page 4, image xref 27), redrawn clean.

Source raster 2226x2523 px placed at 478 dpi, same 37.85 px/ft as the first floor. This image sits
537 px left and 12 px up of the first-floor image (family-room walls and stair treads).
Modernised (Kyle, October 31, 2026):
  - main stair seen from above: the first floor's L-stair (north flight, landing, four steps west)
    in place of the radius stair; the curved floor edge and railing around it become a straight
    railing that turns the corner
  - owner's bath: the corner soaker tub becomes one large walk-in shower with glass, bench and a
    linear drain; the old separate shower becomes a towel closet behind its door
  - the hall bath keeps its tub/shower
"""
import blib as B

PAGE, XREF = 4, 27
K = 478.0
DX, DY = 537.0, 12.0                          # first-floor image = this image + (DX, DY)

TEXT = [(650, 433, 985, 620), (695, 785, 940, 824), (740, 870, 895, 900), (512, 876, 586, 911),
        (1047, 876, 1121, 911), (1744, 1136, 1818, 1172), (776, 992, 869, 1038), (1175, 840, 1271, 886),
        (805, 1090, 961, 1122), (1144, 1088, 1299, 1120), (729, 1129, 760, 1250), (362, 1113, 457, 1159),
        (26, 615, 92, 712), (70, 1045, 180, 1095), (70, 1250, 180, 1300), (140, 739, 370, 832),
        (140, 1538, 370, 1631), (1226, 640, 1497, 686), (1228, 580, 1262, 760), (1776, 655, 1992, 692),
        (1735, 696, 2033, 790), (1745, 836, 2023, 873), (2074, 615, 2197, 712), (2074, 960, 2197, 1056),
        (1815, 1317, 1962, 1410), (1878, 1536, 1958, 1573), (1395, 1395, 1500, 1445),
        (998, 1580, 1240, 1673), (995, 1160, 1050, 1200), (1085, 1160, 1140, 1200), (586, 1678, 808, 1772), (1735, 1775, 1840, 1822), (1735, 2192, 1840, 2240)]
STAIR = [(585, 1257, 882, 1475), (630, 1470, 887, 1722)]
TUB = [(1972, 1360, 2193, 1580)]
OLD_SHOWER = [(1585, 1435, 1680, 1572)]
WIN_DROP = [(1100, 1180, 1180, 1270), (960, 1180, 1020, 1270), (820, 1240, 900, 1270), (870, 1480, 895, 1505)]


def stair(c):
    """The first floor's L-stair, seen from above."""
    N = B.NAVY
    x0, x1, top, T = 1305.0 - DX, 1417.0 - DX, 1259.0, 33.0
    yl = 1271.0 - DY + 8 * T
    yb = yl + (x1 - x0)
    xw = x0 - 4 * T
    B.box(c, x0, top, x1, yl, sw=0.55)
    for i in range(1, 8):
        c.line(x0, top + T * i, x1, top + T * i, 0.45, color=N)
    B.box(c, x0, yl, x1, yb, sw=0.55)
    B.box(c, xw, yl, x0, yb, sw=0.55)
    for i in range(1, 4):
        c.line(x0 - T * i, yl, x0 - T * i, yb, 0.45, color=N)
    c.line(xw, yb, x1, yb, 1.0, color=N)
    c.line(xw, yl, x0, yl, 1.0, color=N)
    B.arrow(c, [((x0 + x1) / 2, top + 14), ((x0 + x1) / 2, (yl + yb) / 2), (xw + 12, (yl + yb) / 2)])
    B.small(c, (x0 + x1) / 2 + 22, top + 40, 'DN', size=4.0)
    # straight floor edge and wood railing where the curved one was
    c.line(764, 1262, 764, 1453, 1.4, color=N)
    c.line(591, 1453, 764, 1453, 1.4, color=N)
    k = 9.0
    for px, py in ((764, 1453), (591, 1453)):
        c.rect(px - k / 2, py - k / 2, k, k, sw=0.4, color=N, fill=N)


def owners_bath(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    x0, y0, x1, y1 = 1975.0, 1362.0, 2196.0, 1582.0          # where the corner tub was
    B.shower(c, x0, y0, x1, y1)
    c.line(x0, y0, x0, y1 - 32 * k, 1.0, color=N)             # glass, with a 32" opening
    B.box(c, x1 - 15 * k, y0 + 18 * k, x1, y1 - 6 * k, sw=0.45)  # bench along the far wall
    B.small(c, x1 - 7.5 * k, (y0 + y1) / 2 + 14, 'BENCH', size=3.0, rotate=-90)
    B.small(c, (x0 + x1) / 2 - 10, (y0 + y1) / 2 - 8, 'SHOWER', size=4.0)
    # old shower -> towel closet: shelves on three sides
    c.rect(1592, 1442, 1680 - 1592, 1568 - 1442, sw=0.4, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, 1632, 1492, 'TOWEL', size=3.4)
    B.small(c, 1632, 1515, 'CLOSET', size=3.4)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 817, 500, 'OPEN TO\nFAMILY ROOM BELOW', '(OPT. BEDROOM 5)', 'OPT. BEAMED CEILING', name_pt=5.8)
    L(c, 256, 752, 'BEDROOM 4', '12\'-0" × 13\'-9"')
    L(c, 260, 1597, 'BEDROOM 3', '12\'-5" × 14\'-0"')
    L(c, 1133, 1626, 'BEDROOM 2', '12\'-3" × 18\'-6"')
    L(c, 1881, 745, "OWNER'S BEDROOM", '23\'-4" × 15\'-2"')
    S(c, 1881, 673, 'OPT. TRAY CEILING', size=3.8, color=o)
    S(c, 1881, 855, 'OPT. CATHEDRAL CEILING', size=3.8, color=o)
    L(c, 1384, 663, 'SITTING ROOM', name_pt=5.6)
    L(c, 823, 1016, 'HALL', name_pt=5.6)
    L(c, 410, 1137, 'BATH', name_pt=5.0)
    L(c, 1855, 1350, "OWNER'S\nBATH", name_pt=5.2)
    L(c, 697, 1726, 'OPEN TO\nFOYER BELOW', name_pt=5.4)
    for x, y in ((124, 1069), (124, 1274), (1447, 1419), (1787, 1798), (1787, 2215)):
        L(c, x, y, 'W.I.C.', name_pt=4.8)
    L(c, 1223, 863, 'MECH.', name_pt=4.6)
    S(c, 1918, 1555, 'BENCH', size=3.6)
    for x, y in ((548, 893), (1084, 893), (1781, 1154)):
        S(c, x, y, 'LINEN', size=3.6)
    S(c, 1021, 1180, 'DN', size=4.0)
    S(c, 1111, 1180, 'DN', size=4.0)
    S(c, 818, 805, 'OPT. JULIET BALCONY', size=3.6, color=o)
    S(c, 818, 885, 'WOOD RAILING', size=3.2)
    S(c, 884, 1106, 'WOOD RAILING', size=3.2)
    S(c, 1221, 1106, 'WOOD RAILING', size=3.2)
    S(c, 745, 1190, 'WOOD RAILING', size=3.2, rotate=-90)
    S(c, 1245, 669, 'OPT. FIREPLACE', size=3.4, color=o, rotate=-90)
    S(c, 58, 661, 'OPT. WINDOW', size=3.4, color=o, rotate=-90)
    S(c, 2163, 661, 'OPT. WINDOW', size=3.4, color=o, rotate=-90)
    S(c, 2163, 1005, 'OPT. WINDOW', size=3.4, color=o, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR + TUB + OLD_SHOWER
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    stair(c)
    owners_bath(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
