"""The Expressionist II - SECOND FLOOR (brochure page 4, image xref 26), redrawn clean.

Source raster 2166x1984 px at 370.4 dpi, 29.6 px/ft; this image is the first floor's moved
240 px left (x_here = x_first - 240, y the same), measured on the family room's walls.

Modernised (Kyle, October 31, 2026):
  - stair: the curved stair becomes the straight flight drawn on the first floor (12 treads,
    top at the south end, arriving in the hall). The curved railing around it becomes straight
    railings on the flight's sides; the void inside the old curve stays open to the gallery.
  - owner's bath: the drop-in soaker tub on its deck between the vanities becomes one walk-in
    shower in the same alcove (glass front with an open entry, bench, linear drain). The old
    corner shower, which does not adjoin it, becomes a towel closet with a door.
Kept: the buddy bath's tub/shower and both vanities; everything else traced.
"""
import blib as B

PAGE, XREF = 4, 26
K, PXFT = 370.4, 29.6

TEXT = [(765, 298, 968, 482), (340, 625, 435, 665), (1580, 570, 1705, 643), (1220, 818, 1302, 852),
        (732, 865, 855, 977), (318, 923, 527, 1025), (1598, 890, 1885, 1042), (1104, 1052, 1178, 1085),
        (694, 1227, 768, 1260), (1224, 1207, 1318, 1243), (1507, 1223, 1655, 1248), (265, 1252, 368, 1282),
        (285, 1445, 477, 1515), (672, 1442, 835, 1473), (615, 1542, 677, 1568), (1015, 1507, 1207, 1578),
        (1790, 1427, 1885, 1463), (1790, 1752, 1885, 1790)]
STAIR = [(835, 815, 1074, 1226), (798, 1126, 840, 1172)]
TUB = [(1524, 364, 1772, 532)]
OLD_SHOWER = [(1374, 596, 1540, 732)]
X0, X1, Y0, Y1 = 958.0, 1066.0, 862.0, 1153.0


def stair(c):
    N = B.NAVY
    n = 12
    T = (Y1 - Y0) / n
    B.box(c, X0, Y0, X1, Y1, sw=0.55)
    for i in range(1, n):
        c.line(X0, Y0 + T * i, X1, Y0 + T * i, 0.45, color=N)
    c.line(X0, Y0, X0, 1109, 1.0, color=N)                 # rail along the void
    c.line(840, 1109, X0, 1109, 1.0, color=N)              # void's south rail carried on
    c.line(X1, Y0, X1, Y1, 1.0, color=N)                   # rail on the hall side
    c.line(X1, 949, 1078, 945, 1.0, color=N)               # joins the rail to the mech. room
    k = 7.0
    for px, py in ((X0, 1109), (X1, Y1), (X0, Y0), (X1, Y0)):
        c.rect(px - k / 2, py - k / 2, k, k, sw=0.4, color=N, fill=N)
    xm = (X0 + X1) / 2
    B.arrow(c, [(xm, Y1 - 14), (xm, Y0 + 12)])
    B.small(c, xm, Y1 + 14, 'DN', size=4.0)


def owners_bath(c):
    N = B.NAVY
    k = PXFT / 12.0
    x0, y0, x1, y1 = 1527.0, 368.0, 1768.0, 505.0
    B.shower(c, x0, y0, x1, y1, glass=((1612, y1), (x1, y1)))
    B.box(c, x1 - 15 * k, y0, x1, y1, sw=0.4)               # 15" bench
    B.small(c, x1 - 7.5 * k, (y0 + y1) / 2 + 16, 'BENCH', size=2.9, rotate=-90)
    B.small(c, (x0 + x1) / 2 - 20, (y0 + y1) / 2 + 12, 'SHOWER', size=4.0)
    # old shower -> towel closet: wall across its open side, 2'-2" door, shelves
    c.rect(1376, 603, 1430 - 1376, 12, sw=0.5, color=N, fill=B.FILL)
    B.door(c, (1495, 609), (1430, 609), side=1)
    c.line(1380, 640, 1380, 728, 0.4, color=N, dash=c.dash(2.5, 1.6))
    c.line(1410, 640, 1410, 728, 0.4, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, 1452, 665, 'TOWEL', size=3.4)
    B.small(c, 1452, 685, 'CLOSET', size=3.4)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 866, 395, 'OPEN TO\nFAMILY ROOM\nBELOW', '(OPTIONAL BEDROOM 5)', 'OPT. BEAMED CEILING')
    L(c, 794, 925, 'OPEN TO\nGALLERY\nBELOW', name_pt=5.6)
    L(c, 420, 1010, 'LOFT', '15\'-2" × 15\'-11"', '(OPTIONAL BEDROOM 4)')
    # the cathedral ridge (dashed, y 1010) crosses the middle: name and size above it, notes below
    B.dashed(c, [(1598, 1011.5), (1885, 1011.5)], w=0.4)       # ridge line under the old lettering
    L(c, 1765, 968, "OWNER'S BEDROOM", '24\'-11" × 17\'-4"')
    S(c, 1765, 1036, 'OPT. TRAY CEILING', size=3.6, color=o)
    S(c, 1765, 1060, 'OPT. CATHEDRAL CEILING', size=3.6, color=o)
    L(c, 1645, 560, "OWNER'S\nBATH", name_pt=5.6)
    L(c, 380, 1500, 'BEDROOM 3', '13\'-1" × 15\'-4"')
    L(c, 1110, 1545, 'BEDROOM 2', '12\'-9" × 15\'-3"')
    L(c, 752, 1458, 'BUDDY BATH', name_pt=5.0)
    L(c, 1261, 835, 'MECH.', name_pt=4.8)
    L(c, 387, 645, 'W.I.C.', name_pt=4.8)
    L(c, 1271, 1225, 'W.I.C.', name_pt=4.8)
    L(c, 1837, 1445, 'W.I.C.', name_pt=4.8)
    L(c, 1837, 1771, 'W.I.C.', name_pt=4.8)
    L(c, 1150, 1068, 'HALL', name_pt=4.8)
    L(c, 731, 1243, 'HALL', name_pt=4.8)
    S(c, 316, 1267, 'CLOSET', size=3.6)
    S(c, 646, 1555, 'LINEN', size=3.2)
    S(c, 1581, 1236, 'OPT. FIREPLACE', size=3.4, color=o)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, add=[(1495, 603, 1510, 740)])   # towel closet's side wall
    drop = TEXT + STAIR + TUB + OLD_SHOWER
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_bath(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
