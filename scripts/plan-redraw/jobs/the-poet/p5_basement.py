"""The Poet - BASEMENT (brochure page 5, image xref 27), redrawn clean.

Source raster 2516x2311 px at 421.7 dpi, about 38.0 px/ft. Same treatment as The Pioneer I's
basement: traced framed walls, foundation lines and linework; the foundation band gets the light
concrete fill; stair treads and the mechanical circles redrawn; lettering re-set. The optional
bath keeps its tub/shower and its vanity (no pedestal sink here).
"""
import blib as B
import found

PAGE, XREF = 5, 27
B.K, B.PXFT = 421.7, 38.0
CONC = '#e4e7eb'

TEXT = [(1730, 80, 1800, 110), (1740, 286, 1848, 346), (1832, 356, 2094, 458), (1466, 474, 1566, 574),
        (1414, 584, 1674, 626), (2116, 640, 2186, 676), (1430, 852, 1480, 910), (688, 912, 952, 964),
        (1968, 1115, 2112, 1215), (296, 1601, 604, 1701), (1062, 1642, 1408, 1696), (1026, 2058, 1144, 2158),
        (2125, 255, 2175, 295), (2125, 347, 2175, 387), (1735, 460, 1795, 505)]
STAIR = [(1416, 908, 1527, 1394)]
CIRCLES = [(1765, 93, 32), (1792, 317, 54), (2150, 274, 38), (2150, 366, 38), (1765, 482, 32)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]


def stair(c):
    N = B.NAVY
    x0, x1, y0, y1 = 1419.0, 1523.0, 916.0, 1391.0
    B.box(c, x0, y0, x1, y1, sw=0.55)
    n = 15
    for i in range(1, n):
        y = y0 + (y1 - y0) * i / n
        c.line(x0, y, x1, y, 0.45, color=N)
    B.arrow(c, [(1471, 866), (1471, 944)], w=0.45)
    B.small(c, 1446, 882, 'UP', size=4.0, rotate=-90)


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 766, 1000, 'OPT. REC ROOM')
    L(c, 450, 1660, 'OPT. MEDIA ROOM', '17\'-1" × 11\'-7"')
    L(c, 1235, 1690, 'UNFINISHED STORAGE', name_pt=5.6)
    L(c, 1975, 410, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.0)
    L(c, 1516, 522, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1544, 606, '3 PIECE ROUGH-IN STD.', size=3.6)
    L(c, 2035, 1192, 'GARAGE\nABOVE', name_pt=5.2, color=B.GREY)
    L(c, 1085, 2108, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 2152, 657, 'A.H.U.', size=3.2)
    S(c, 1765, 93, 'SUMP', size=3.0)
    S(c, 1792, 307, 'SPRINKLER', size=3.0)
    S(c, 1792, 328, 'TANK', size=3.0)
    S(c, 2150, 274, 'WT', size=3.2)
    S(c, 2150, 366, 'WH', size=3.2)
    S(c, 1765, 473, 'EJEC.', size=2.8)
    S(c, 1765, 492, 'PIT', size=2.8)


def draw(c, img):
    walls, wins = B.trace(img)
    conc, _ = found.bands(img)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + STAIR + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    stair(c)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
