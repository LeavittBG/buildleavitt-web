"""The Expressionist II - FIRST FLOOR (brochure page 2, image xref 16), redrawn clean.

Source raster 2409x1989 px placed at 370.4 dpi; about 29.6 px/ft (two-story family room
17'-9" inside = 526 px, study 13'-2" = 390 px). Every drawing in this brochure is at that dpi.

Kept by tracing: walls, windows, doors, cabinets, appliances, dashed outlines. Modernised (Kyle,
October 31, 2026):
  - the curved (radius) main stair in the gallery becomes one straight flight in its own place:
    12 treads from the gallery (north) up to the south, against the straight wall that stood
    behind the curved one. The curved wall is gone (it only enclosed a dead space between itself
    and that straight wall); the powder room's top wall is carried across where it met it.
  - kitchen: the peninsula with its raised bar (between kitchen and sunroom) and the small prep
    island become one 7'-0" x 4'-0" island with the prep sink and three stools facing the sunroom.
    (An 8'-0" island would leave aisles under 36".)
  - powder room: pedestal sink -> 24" vanity
Left as is: no desk, no garage-entry bench; the pantry and butler's pantry are reach-ins.
"""
import blib as B
from shapely.geometry import box as sbox

PAGE, XREF = 2, 16
K, PXFT = 370.4, 29.6

TEXT = [(1040, 80, 1175, 108), (638, 208, 795, 238), (455, 395, 645, 475), (945, 345, 1280, 425),
        (1495, 530, 1690, 612), (1850, 450, 1930, 487), (2080, 595, 2290, 670), (1845, 720, 1935, 758),
        (470, 708, 670, 785), (553, 843, 620, 870), (1388, 825, 1465, 862), (1633, 825, 1710, 862),
        (975, 900, 1098, 937), (1350, 955, 1380, 1025), (530, 1128, 605, 1165), (446, 1100, 503, 1212),
        (650, 1095, 727, 1123), (815, 1112, 845, 1186), (933, 1147, 1008, 1183), (1218, 1175, 1292, 1250),
        (1386, 1157, 1506, 1192), (1124, 1257, 1197, 1292), (925, 1251, 1050, 1280), (1862, 1342, 2122, 1418),
        (548, 1396, 738, 1513), (378, 1400, 405, 1490), (944, 1450, 1032, 1483), (1222, 1497, 1405, 1615),
        (1444, 1468, 1469, 1608), (135, 1513, 318, 1570), (893, 1764, 1063, 1800), (1046, 1152, 1094, 1194)]
STAIR = [(1100, 820, 1305, 1152), (1060, 1123, 1205, 1201), (1150, 1150, 1205, 1225),
         (985, 1100, 1062, 1225)]
KITCHEN = [(318, 570, 672, 704), (485, 788, 682, 920)]
PDR_SINK = [(1300, 1245, 1350, 1322)]
TRAYS = [(495, 1276, 792, 1290), (495, 1611, 792, 1625), (497, 1276, 511, 1625), (776, 1276, 791, 1625),
         (1185, 1393, 1479, 1407), (1185, 1672, 1479, 1686), (1185, 1393, 1199, 1686), (1465, 1393, 1479, 1686)]
WIN_DROP = [(1530, 900, 1570, 1060), (1280, 920, 1310, 970), (1080, 1100, 1110, 1230), (1330, 1260, 1360, 1310)]
# the curved stair wall goes; the powder room's top wall runs on to the straight wall
CUT = [(1125, 820, 1305, 1152), (1155, 1152, 1190, 1225)]
ADD = [sbox(1191, 1153, 1312, 1167), sbox(1306, 955, 1320, 1160),
       sbox(1100, 1108, 1198, 1124), sbox(1140, 1201, 1191, 1222)]

X0, X1, Y0, Y1 = 1198.0, 1306.0, 862.0, 1153.0     # the straight flight


def stair(c):
    N = B.NAVY
    n = 12
    T = (Y1 - Y0) / n
    B.box(c, X0, Y0, X1, Y1, sw=0.55)
    for i in range(1, n):
        c.line(X0, Y0 + T * i, X1, Y0 + T * i, 0.45, color=N)
    c.line(X0, Y0, X0, Y1, 1.0, color=N)                  # rail, open side to the gallery
    c.line(X1, Y0, X1, 960, 1.0, color=N)                 # rail until the wall starts
    k = 7.0
    for px in (X0 + k / 2, X1 - k / 2):                    # square newels at the first step
        c.rect(px - k / 2, Y0, k, k, sw=0.4, color=N, fill=N)
    xm = (X0 + X1) / 2
    B.arrow(c, [(xm, Y0 + 14), (xm, Y1 - 12)])
    B.small(c, xm, Y0 - 12, 'UP', size=4.0)
    # basement stair under the top of the flight, going down east from its door
    bx0, bx1, by0, by1 = 1062.0, 1198.0, 1124.0, 1201.0
    B.box(c, bx0, by0, bx1, by1, sw=0.5)
    for i in range(1, 6):
        x = bx0 + 25 * i
        c.line(x, by0, x, by1, 0.45, color=N)
    B.break_line(c, 1170, by0 - 6, 1185, by1 + 6)
    B.arrow(c, [(bx0 + 10, 1178), (1150, 1178)])
    B.small(c, 1090, 1152, 'DN', size=4.0)
    B.door(c, (1062, 1124), (1062, 1201), side=1)          # basement door


def kitchen(c):
    N = B.NAVY
    c.line(320, 690, 383, 690, 0.6, color=N)               # end of the left-hand run
    x0, x1, y0, y1 = 480.0, 687.0, 760.0, 878.0             # island 7'-0" x 4'-0"
    B.box(c, x0, y0, x1, y1, sw=0.6)
    c.line(x0, y0 + 30, x1, y0 + 30, 0.35, color=N, dash=c.dash(2.5, 1.6))   # seating overhang
    B.kitchen_sink(c, 640, 830, horizontal=True, w_in=18, d_in=15)
    for i in range(3):
        c.circle(x0 + (x1 - x0) * (i + 0.5) / 3, y0 - 24, 18, sw=0.45, color=B.GREY)
    B.small(c, 560, 836, 'ISLAND', size=3.8)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    # names centred on each room's open floor; inside the tray outline where there is one
    L(c, 1109, 390, 'TWO-STORY\nFAMILY ROOM', '17\'-9" × 21\'-1"')
    L(c, 550, 430, 'SUNROOM', '18\'-11" × 12\'-3"')
    L(c, 1585, 562, 'STUDY', '13\'-2" × 13\'-6"')
    L(c, 2170, 640, 'BEDROOM 1', '14\'-2" × 17\'-10"')
    L(c, 583, 942, 'KITCHEN', '17\'-6" × 14\'-10"')
    L(c, 643, 1450, 'DINING ROOM', '13\'-6" × 15\'-4"', 'OPT. TRAY CEILING')
    L(c, 1332, 1540, 'LIVING ROOM', '13\'-5" × 13\'-5"', 'OPT. TRAY CEILING')
    L(c, 987, 1466, 'FOYER', name_pt=6.0)
    L(c, 1965, 1447, 'THREE-CAR GARAGE', '25\'-9" × 34\'-8"')
    L(c, 1036, 918, 'GALLERY', name_pt=5.6)
    L(c, 1446, 1175, 'LAUNDRY', name_pt=5.4)
    L(c, 1252, 1212, 'PDR.\nROOM', name_pt=4.8)
    L(c, 1890, 468, 'BATH', name_pt=5.0)
    L(c, 1890, 739, 'W.I.C.', name_pt=4.8)
    for x, y in ((1426, 843), (1671, 843), (567, 1146), (970, 1165), (1160, 1274)):
        L(c, x, y, 'HALL', name_pt=4.8)
    L(c, 978, 1782, 'CONC. PORCH', name_pt=4.8)
    S(c, 1108, 94, 'GAS FIREPLACE', size=3.6)
    S(c, 987, 1266, 'TRAY CEILING', size=3.4, color=o)
    S(c, 688, 1109, 'PANTRY', size=3.6)
    c.line(472.5, 1100, 472.5, 1205, 0.9, color=B.NAVY)      # butler's pantry shelf edge
    S(c, 460, 1156, "BUTLER'S", size=3.0, rotate=-90)
    S(c, 488, 1156, 'PANTRY', size=3.0, rotate=-90)
    S(c, 830, 1149, 'CLOSET', size=3.4, rotate=-90)
    S(c, 1365, 990, 'CLOSET', size=3.4, rotate=-90)
    S(c, 716, 223, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 392, 1445, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 1457, 1538, 'OPT. FIREPLACE', size=3.4, color=o, rotate=-90)
    S(c, 226, 1528, 'OPT. CONSERVATORY', size=3.4, color=o)
    S(c, 226, 1556, 'OR IN-LAW SUITE', size=3.4, color=o)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP, cut=CUT, add=ADD)
    drop = TEXT + STAIR + KITCHEN + PDR_SINK + TRAYS
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    B.dashed_rect(c, 503.5, 1283, 783.5, 1618, w=0.45)
    B.dashed_rect(c, 1192, 1400, 1471.5, 1679, w=0.45)
    B.vanity(c, 1345, 1288, 'left', 24, 19)
    kitchen(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
