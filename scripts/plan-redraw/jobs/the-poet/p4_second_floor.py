"""The Poet - SECOND FLOOR (brochure page 4, image xref 23), redrawn clean.

Source raster 2498x2254 px at 421.7 dpi, about 38.0 px/ft (owner's bedroom 15'-8" = 595 px).
Changed (Kyle, October 31, 2026): the owner's bath oval soaking tub and its separate corner
shower become one large walk-in shower (about 9'-3" x 5'-7") with glass, a bench and a linear
drain along the back wall; the tub's corner by the door is open floor. Hall bath keeps its
tub/shower. Lettering re-set. The tray ceiling over the owner's bath is redrawn as printed.
"""
import blib as B

PAGE, XREF = 4, 23
B.K, B.PXFT = 421.7, 38.0


def pad(r, p=6):
    return (r[0] - p, r[1] - p, r[2] + p, r[3] + p)


TEXT = [pad(r) for r in [
    (488, 215, 555, 555), (1090, 120, 1152, 295), (1503, 273, 1590, 332), (23, 1295, 82, 1385),
    (98, 1505, 165, 1605), (1402, 1565, 1472, 1652), (1402, 1690, 1472, 1772), (1160, 1448, 1187, 1593),
    (1298, 1340, 1327, 1393), (1235, 1828, 1355, 1893), (1048, 1935, 1168, 2000), (1665, 1641, 1855, 1670),
    (338, 1957, 477, 1985), (778, 403, 935, 427), (728, 473, 998, 502), (715, 307, 1007, 393),
    (237, 912, 488, 998), (282, 1615, 510, 1705), (1927, 1060, 2185, 1148), (743, 1003, 848, 1047),
    (1298, 952, 1407, 995), (712, 1645, 813, 1685), (290, 660, 368, 685), (743, 1485, 810, 1510),
    (373, 1295, 460, 1332), (980, 1315, 1063, 1352), (857, 1860, 998, 1897), (1584, 1098, 1641, 1120)]]
# owner's bath: tub, corner shower, its door and the tray-ceiling lines over them (redrawn)
OWNERS_BATH = [(1176, 364, 1657, 712)]
WIN_DROP = [(1360, 1385, 1400, 1415), (290, 1425, 345, 1460)]

SHOWER = (1290.0, 361.0, 1652.0, 573.0)


def bath_tray(c):
    # tray ceiling over the owner's bath as printed: outer and inner outline joined at the corners
    o = (1247, 435, 1595, 705)
    i = (1283, 473, 1558, 667)
    B.dashed_rect(c, *o, w=0.4)
    B.dashed_rect(c, *i, w=0.4)
    for (ax, ay), (bx, by) in (((o[0], o[1]), (i[0], i[1])), ((o[2], o[1]), (i[2], i[1])),
                               ((o[0], o[3]), (i[0], i[3])), ((o[2], o[3]), (i[2], i[3]))):
        c.line(ax, ay, bx, by, 0.3, color=B.OPT)


def owners_bath(c):
    N = B.NAVY
    x0, y0, x1, y1 = SHOWER
    k = B.PXFT / 12.0
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill='#ffffff')
    c.line(x0, y0, x0, y1, 0.9, color=N)                    # glass side panel
    c.line(x0 + 130, y1, x1, y1, 0.9, color=N)              # glass front, open entry at the left
    c.line(x0, y1, x0 + 130, y1, 0.3, color=N, dash=c.dash(2, 1.5))
    c.rect(x0 + 30, y0 + 4 * k, x1 - x0 - 60 - 15 * k, 1.6 * k, sw=0.3, color=N)   # linear drain
    c.rect(x1 - 15 * k, y0 + 18, 15 * k, y1 - y0 - 36, sw=0.45, color=N, fill='#ffffff')   # bench
    B.small(c, x1 - 7.5 * k, (y0 + y1) / 2, 'BENCH', size=3.0, rotate=-90, color=B.GREY)
    B.small(c, (x0 + x1 - 15 * k) / 2, (y0 + y1) / 2 + 6, 'SHOWER', size=4.2)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 865, 452, "OWNER'S BEDROOM", '15\'-8" × 20\'-0"', 'OPT. TRAY CEILING')
    S(c, 865, 540, 'OPT. CATHEDRAL CEILING', size=4.5, color=o)
    L(c, 1412, 620, "OWNER'S\nBATH", name_pt=5.6)
    S(c, 1421, 687, 'OPT. TRAY CEILING', size=3.8, color=o)
    L(c, 387, 955, 'BEDROOM 2', '14\'-10" × 13\'-0"')
    L(c, 401, 1665, 'BEDROOM 3', '15\'-7" × 11\'-8"')
    L(c, 2079, 1075, 'BONUS ROOM', '20\'-10" × 17\'-11"')
    L(c, 417, 1314, 'BATH', name_pt=5.4)
    L(c, 1022, 1334, 'HALL', name_pt=5.6)
    L(c, 921, 1890, 'LAUNDRY', name_pt=5.6)
    S(c, 795, 1025, 'W.I.C.', size=4.4)
    S(c, 1353, 974, 'W.I.C.', size=4.4)
    S(c, 762, 1665, 'W.I.C.', size=4.0)
    S(c, 329, 672, 'CLOSET', size=3.6)
    S(c, 776, 1497, 'LINEN', size=3.6)
    S(c, 1612, 1110, 'A.H.U.', size=3.0)
    S(c, 1312, 1366, 'DN', size=3.8, rotate=-90)
    S(c, 1173, 1520, 'WOOD RAILING', size=3.2, rotate=-90)
    S(c, 1295, 1850, 'OPTIONAL', size=3.4, color=o)
    S(c, 1295, 1872, 'CABINETRY', size=3.4, color=o)
    S(c, 1108, 1956, 'OPTIONAL', size=3.4, color=o)
    S(c, 1108, 1978, 'CABINETRY', size=3.4, color=o)
    S(c, 1760, 1656, 'OPTIONAL DORMER', size=3.4, color=o)
    S(c, 408, 1971, 'ELEVATION C', size=3.4, color=o)
    S(c, 1546, 289, 'OPT.', size=3.4, color=o)
    S(c, 1546, 314, 'WINDOW', size=3.4, color=o)
    for x, y in ((502, 288), (502, 385), (502, 482)):          # three optional windows, left wall
        S(c, x, y, 'OPT.', size=3.2, color=o, rotate=-90)
        S(c, x + 33, y, 'WINDOW', size=3.2, color=o, rotate=-90)
    for x, y in ((1105, 165), (1105, 250)):
        S(c, x, y, 'OPT.', size=3.2, color=o, rotate=-90)
        S(c, x + 33, y, 'WINDOW', size=3.2, color=o, rotate=-90)
    for x, y in ((38, 1340), (115, 1555)):
        S(c, x, y, 'OPT.', size=3.2, color=o, rotate=-90)
        S(c, x + 30, y, 'WINDOW', size=3.2, color=o, rotate=-90)
    for x, y in ((1420, 1608), (1420, 1731)):
        S(c, x, y, 'OPT.', size=3.2, color=o, rotate=-90)
        S(c, x + 33, y, 'WINDOW', size=3.2, color=o, rotate=-90)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + OWNERS_BATH
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    bath_tray(c)
    owners_bath(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
