"""The Novel - BASEMENT (brochure page 5, image xref 28), redrawn clean.

Source raster 2769x2520 px at 412.4 dpi, about 37.95 px/ft. Same treatment as the other basements:
traced foundation and framed walls, light concrete fill in the foundation band, mechanical circles
redrawn whole, lettering re-set. The stair is straight (traced as drawn). The optional bath keeps its
tub and its vanity (no pedestal sink here).
"""
import blib as B
import found

PAGE, XREF = 5, 28
B.K, B.PXFT = 412.4, 37.95
CONC = '#e4e7eb'

TEXT = [(1140, 738, 1400, 782), (2160, 690, 2460, 785), (1815, 1072, 1880, 1102), (1740, 1148, 1840, 1192),
        (1190, 1255, 1232, 1297), (685, 1432, 942, 1530), (1305, 1465, 1560, 1500), (1190, 1518, 1290, 1612),
        (1540, 1565, 1795, 1660), (150, 1575, 415, 1642), (2245, 1525, 2385, 1615), (1188, 1835, 1298, 1925),
        (2150, 2450, 2508, 2488)]
CIRCLES = [(1454, 1621, 32), (1488, 1884, 54), (1852, 1713, 40), (1852, 1796, 40), (1844, 1905, 32)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 1270, 760, 'OPT. REC ROOM')
    L(c, 2310, 738, 'OPT. MEDIA ROOM', '21\'-8" × 13\'-5"')
    L(c, 805, 1482, 'OPT. DEN', '12\'-5" × 15\'-9"')
    L(c, 1790, 1170, 'MECH.', name_pt=5.4)
    L(c, 1668, 1612, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.0)
    L(c, 1240, 1565, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1432, 1483, '3 PIECE ROUGH-IN STD.', size=3.6)
    S(c, 1211, 1276, 'UP', size=4.0)
    S(c, 1848, 1087, 'A.H.U.', size=3.2)
    L(c, 2315, 1570, 'GARAGE\nABOVE', name_pt=5.2, color=B.GREY)
    L(c, 1243, 1880, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 1454, 1612, 'EJEC.', size=2.8)
    S(c, 1454, 1631, 'PIT', size=2.8)
    S(c, 1488, 1873, 'SPRINKLER', size=3.0)
    S(c, 1488, 1894, 'TANK', size=3.0)
    S(c, 1852, 1713, 'WH', size=3.2)
    S(c, 1852, 1796, 'WT', size=3.2)
    S(c, 1844, 1905, 'SUMP', size=3.0)
    S(c, 282, 1592, 'OPT. CONSERVATORY OR', size=3.4, color=o)
    S(c, 282, 1624, 'IN-LAW SUITE ABOVE', size=3.4, color=o)
    S(c, 2329, 2469, 'OPTIONAL 3-CAR GARAGE ABOVE', size=3.4, color=o)


def draw(c, img):
    walls, wins = B.trace(img)
    conc, _ = found.bands(img)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
