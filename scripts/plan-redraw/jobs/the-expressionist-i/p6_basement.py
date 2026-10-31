"""The Expressionist I - BASEMENT (brochure page 6, image xref 34), redrawn clean.

Source raster 2405x1990 px placed at 370.3 dpi, about 32.1 px/ft. Same treatment as the earlier
basements: traced framed walls, foundation lines and linework; the foundation band gets the light
concrete fill; mechanical circles redrawn whole; lettering re-set. The stair is straight with a
45-degree winder turn at its foot (no flare or curved start), so it is traced as drawn. The
optional bath keeps its tub and vanity.
"""
import blib as B
import found

PAGE, XREF = 6, 34
K, PXFT = 370.3, 32.1
CONC = '#e4e7eb'

TEXT = [(1446, 344, 1526, 420), (1378, 436, 1582, 468), (1855, 518, 2097, 598), (1222, 774, 1255, 822),
        (708, 835, 916, 875), (1543, 805, 1597, 829), (1450, 1273, 1504, 1297), (1260, 1355, 1474, 1431),
        (1886, 1322, 2003, 1401), (118, 1505, 334, 1565), (935, 1732, 1030, 1811)]
CIRCLES = [(1660, 319, 25), (1482, 1507, 30), (1482, 1581, 30), (1481, 1693, 25), (1232, 1681, 42)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]
# steel columns, redrawn as plain squares (the trace breaks them up)
COLS = [(850, 725), (850, 1218), (1687, 750), (2029, 750)]
COL_DROP = [(x - 22, y - 22, x + 22, y + 22) for x, y in COLS]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def columns(c):
    for x, y in COLS:
        c.rect(x - 12, y - 12, 24, 24, sw=0.5, color=B.NAVY, fill='#ffffff')
        c.rect(x - 4, y - 4, 8, 8, sw=0, color=B.NAVY, fill=B.NAVY)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 812, 855, 'OPT. REC ROOM')
    L(c, 1976, 558, 'OPT. MEDIA ROOM', '24\'-6" × 20\'-6"')
    L(c, 1486, 383, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1480, 452, '3 PIECE ROUGH-IN STD.', size=3.6)
    S(c, 1238, 798, 'UP', size=4.0, rotate=-90)
    S(c, 1570, 817, 'A.H.U.', size=3.0)
    S(c, 1477, 1285, 'A.H.U.', size=3.0)
    L(c, 1367, 1393, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.2)
    L(c, 1944, 1362, 'GARAGE\nABOVE', name_pt=5.0, color=B.GREY)
    L(c, 982, 1772, 'PORCH\nABOVE', name_pt=4.6, color=B.GREY)
    S(c, 226, 1522, 'OPT. CONSERVATORY OR', size=3.4, color=o)
    S(c, 226, 1548, 'IN-LAW SUITE ABOVE', size=3.4, color=o)
    S(c, 1660, 311, 'EJEC.', size=2.6)
    S(c, 1660, 328, 'PIT', size=2.6)
    S(c, 1482, 1507, 'WH', size=3.0)
    S(c, 1482, 1581, 'WT', size=3.0)
    S(c, 1481, 1693, 'SUMP', size=2.8)
    S(c, 1232, 1672, 'SPRINKLER', size=2.6)
    S(c, 1232, 1690, 'TANK', size=2.6)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, cut=COL_DROP, win_drop=COL_DROP)
    conc, _ = found.bands(img, drop=COL_DROP)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP + COL_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    circles(c)
    columns(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
