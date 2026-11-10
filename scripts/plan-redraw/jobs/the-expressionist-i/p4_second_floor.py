"""The Expressionist I - SECOND FLOOR (brochure page 4, image xref 25), redrawn clean.

Source raster 2166x1984 px placed at 370.4 dpi; about 32.1 px/ft, the same scale as the first floor.
This image sits 240 px left and 2 px up of the first floor's (family-room walls and the front wall
line up), so the first floor's straight stair (x 1180-1305, y 830-1150 there) is x 940-1065,
y 828-1148 here. Walls, windows and linework traced; lettering re-set. Modernised (Kyle, October 31,
2026): the curved (radius) stair seen from above becomes the first floor's straight flight, arriving
on the hall at its south end; the floor opening's edge now runs straight to it, with rails along
both sides of the flight. The buddy bath keeps its tub and double vanity.
"""
import blib as B

PAGE, XREF = 4, 25
K, PXFT = 370.4, 32.1

TEXT = [(761, 309, 976, 335), (747, 343, 981, 481), (347, 628, 431, 660), (1204, 817, 1316, 851),
        (717, 866, 871, 974), (304, 921, 537, 1026), (1621, 954, 1853, 1059), (1087, 1050, 1197, 1084),
        (676, 1225, 786, 1259), (1228, 1207, 1311, 1239), (249, 1249, 386, 1283), (656, 1441, 856, 1475),
        (290, 1445, 471, 1529), (605, 1543, 688, 1569), (1018, 1505, 1204, 1588)]
STAIR = [(845, 818, 1072, 1224), (800, 1128, 852, 1225)]   # last: the old DN


def stair(c):
    N = B.NAVY
    x0, x1, y0, y1 = 940.0, 1065.0, 828.0, 1148.0
    n = 12
    T = (y1 - y0) / n
    B.box(c, x0, y0, x1, y1, sw=0.55)
    for i in range(1, n):
        c.line(x0, y0 + T * i, x1, y0 + T * i, 0.45, color=N)
    c.line(x0, y0, x0, y1, 1.0, color=N)                     # rail, opening side and hall side
    c.line(x1, 946, x1, y1, 1.0, color=N)                    # rail, hall side
    c.line(x1, 946, 1074, 944, 1.0, color=N)                 # joins the rail to the mech room
    c.line(845, 1111, x0, 1111, 1.0, color=N)                # edge of the floor opening
    k = 8.0
    for px, py in ((x0, y1), (x1, y1), (x0, 1111)):
        c.rect(px - k / 2, py - k / 2, k, k, sw=0.4, color=N, fill=N)
    B.arrow(c, [((x0 + x1) / 2, y1 - 12), ((x0 + x1) / 2, y0 + 70)])
    B.small(c, (x0 + x1) / 2, y1 + 20, 'DN', size=4.2)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    S(c, 868, 322, 'OPT. BEAMED CEILING', size=4.0, color=o)
    L(c, 868, 400, 'OPEN TO\nFAMILY ROOM\nBELOW', '(OPTIONAL BEDROOM 6)', name_pt=5.8)
    L(c, 796, 918, 'OPEN TO\nGALLERY\nBELOW', name_pt=5.6)
    L(c, 425, 965, 'LOFT', '15\'-2" × 15\'-11"', '(OPTIONAL BEDROOM 5)')
    L(c, 1767, 1007, 'STORAGE', '24\'-11" × 17\'-4"', '(OPTIONAL BEDROOM 4)')
    L(c, 397, 1484, 'BEDROOM 3', '13\'-1" × 15\'-4"')
    L(c, 1103, 1525, 'BEDROOM 2', '12\'-9" × 15\'-3"')
    L(c, 755, 1457, 'BUDDY BATH', name_pt=5.4)
    L(c, 1265, 830, 'MECH.', name_pt=5.0)
    S(c, 1140, 1067, 'HALL', size=4.6, weight=700)
    S(c, 730, 1242, 'HALL', size=4.6, weight=700)
    S(c, 389, 644, 'W.I.C.', size=4.4)
    S(c, 1270, 1223, 'W.I.C.', size=4.4)
    S(c, 317, 1266, 'CLOSET', size=4.0)
    S(c, 647, 1556, 'LINEN', size=3.6)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img)
    drop = TEXT + STAIR
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
