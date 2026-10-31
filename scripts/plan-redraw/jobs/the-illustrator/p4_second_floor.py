"""The Illustrator - SECOND FLOOR (brochure page 4, image xref 25), redrawn clean.

Source raster 2359x1952 px placed at 370.4 dpi, 32.3 px/ft (same scale as the first floor).

Kept by tracing: walls, windows, doors, closets, the stair, railings, the hall bath and its tub,
dashed options and ceilings.
Changed (Kyle, October 31, 2026):
  - owner's bath: the tub in its 3'-3" x 5'-7" alcove (the bath's only bathing fixture) becomes a
    walk-in tiled shower in the same alcove, glass along the open side, linear drain
  - lettering re-set in Roboto Condensed, room names centred in their rooms
Left as is: the stair is straight; the hall (buddy) bath keeps its tub/shower; the quarter-round
railing at the open-to-foyer edge is a floor edge, not a stair, and stays as drawn.
"""
import blib as B

PAGE, XREF = 4, 25
B.K, B.PXFT = 370.4, 32.3

TEXT = [(195, 403, 490, 442), (1628, 403, 1927, 442), (205, 625, 482, 730), (1363, 603, 1727, 747),
        (1943, 628, 2092, 722), (613, 753, 770, 788), (863, 688, 1019, 722), (1110, 753, 1267, 788),
        (943, 923, 1095, 957), (763, 1088, 857, 1154), (634, 1253, 727, 1320), (946, 836, 1038, 880),
        (648, 1163, 742, 1209), (697, 990, 748, 1025), (383, 1001, 480, 1045), (314, 1034, 534, 1074),
        (118, 933, 224, 974), (108, 1126, 214, 1167), (502, 1103, 538, 1178), (213, 1378, 472, 1477),
        (688, 1478, 914, 1574), (1128, 1321, 1382, 1420), (1514, 1298, 1550, 1384),
        (1788, 1038, 2039, 1075), (1780, 1078, 2080, 1172), (1788, 1208, 2070, 1243),
        (1838, 1705, 1939, 1745), (104, 1270, 172, 1367), (104, 1488, 172, 1587), (26, 900, 66, 1222),
        (2290, 838, 2332, 1150)]
# the family-room label block sits over the dashed beam lines: erased and knocked out white
FAM = (815, 283, 1065, 483)
TUB = [(1772, 484, 1869, 657)]
# the newel block at the head of the centre flight reads as a window
WIN_DROP = [(950, 1030, 1020, 1090)]


def owners_shower(c):
    # walk-in shower filling the old tub alcove (inside faces x 1767-1872, y 480-660)
    B.shower(c, 1767, 480, 1872, 660, glass=((1872, 482), (1872, 588)))
    B.small(c, 1820, 560, 'SHOWER', size=3.6, rotate=-90)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    c.rect(FAM[0], FAM[1], FAM[2] - FAM[0], FAM[3] - FAM[1], sw=0, fill='#ffffff')
    L(c, 940, 372, 'OPEN TO\nFAMILY ROOM\nBELOW', note='OPT. BEAMED CEILING')
    L(c, 345, 680, 'BEDROOM 4', '12\'-10" × 10\'-10"')
    L(c, 1530, 668, 'SITTING ROOM', '12\'-3" × 10\'-10"', '(OPT. LOFT OR OPT. BEDROOM 5)')
    L(c, 2012, 675, "OWNER'S\nBATH")
    L(c, 1930, 1122, "OWNER'S BEDROOM", '17\'-4" × 16\'-1"')
    S(c, 1913, 1057, 'OPT. TRAY CEILING', size=4.3, color=o)
    S(c, 1929, 1226, 'OPT. CATHEDRAL CEILING', size=4.3, color=o)
    L(c, 345, 1425, 'BEDROOM 3', '12\'-10" × 11\'-10"')
    L(c, 1255, 1368, 'BEDROOM 2', '12\'-10" × 14\'-10"')
    L(c, 800, 1525, 'OPEN TO\nFOYER BELOW')
    L(c, 990, 858, 'HALL', name_pt=5.6)
    L(c, 695, 1186, 'HALL', name_pt=5.2)
    L(c, 430, 1040, 'BATH', note='(OPT. BUDDY BATH)', name_pt=5.2)
    S(c, 171, 953, 'W.I.C.', size=4.2, weight=700)
    S(c, 161, 1146, 'W.I.C.', size=4.2, weight=700)
    L(c, 1889, 1725, 'W.I.C.', name_pt=5.2)
    S(c, 520, 1140, 'LINEN', size=3.6, rotate=-90)
    S(c, 1532, 1341, 'CLOSET', size=3.6, rotate=-90)
    S(c, 722, 1007, 'DN', size=4.2)
    for x, y in ((691, 770), (941, 705), (1188, 770), (1019, 940)):
        S(c, x, y, 'WOOD RAILING', size=3.4)
    for x, y in ((810, 1106), (680, 1268)):
        S(c, x, y, 'WOOD', size=3.4)
        S(c, x, y + 30, 'RAILING', size=3.4)
    S(c, 341, 422, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 1777, 422, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 46, 1080, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2311, 1007, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    for y in (1318, 1537):
        S(c, 122, y, 'OPT.', size=3.4, color=o, rotate=-90)
        S(c, 153, y, 'WINDOW', size=3.4, color=o, rotate=-90)


def draw(c, img):
    c.K = B.K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + [FAM] + TUB
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_shower(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
