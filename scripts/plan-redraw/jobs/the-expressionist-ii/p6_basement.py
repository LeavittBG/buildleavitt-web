"""The Expressionist II - BASEMENT (brochure page 6, image xref 33), redrawn clean.

Source raster 2405x1990 px at 370.4 dpi, 29.6 px/ft. Same treatment as the other basements:
traced framed walls, foundation lines and linework; the foundation band gets the light concrete
fill; the mechanical circles are redrawn; lettering re-set. The optional bath keeps its
tub/shower and vanity. The stair is straight with winders at its foot (no flare or curve), so
it is only traced.
"""
import blib as B
import found
import bhelp

PAGE, XREF = 6, 33
K, PXFT = 370.4, 29.6
CONC = '#e4e7eb'

TEXT = [(1780, 246, 1995, 279), (1445, 463, 1527, 540), (1377, 556, 1578, 587), (1855, 580, 2095, 659),
        (705, 833, 915, 877), (1222, 776, 1255, 818), (1537, 803, 1600, 832), (1449, 1272, 1508, 1300),
        (1265, 1355, 1470, 1429), (1890, 1320, 2004, 1400), (118, 1503, 334, 1565), (937, 1733, 1029, 1812)]
CIRCLES = [(1662, 438, 27), (1480, 1508, 31), (1480, 1580, 31), (1480, 1692, 28), (1233, 1680, 43)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]
WIN_DROP = [(1060, 1100, 1130, 1230)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 810, 900, 'OPT. REC ROOM')
    L(c, 1975, 620, 'OPT. MEDIA ROOM', '24\'-6" × 16\'-6"')
    L(c, 1367, 1392, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.2)
    L(c, 1486, 500, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1478, 572, '3 PIECE ROUGH-IN STD.', size=3.4)
    L(c, 1946, 1360, 'GARAGE\nABOVE', name_pt=5.2, color=B.GREY)
    L(c, 983, 1772, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 1238, 798, 'UP', size=3.8)
    S(c, 1568, 818, 'A.H.U.', size=3.0)
    S(c, 1478, 1287, 'A.H.U.', size=3.0)
    S(c, 1662, 430, 'EJEC.', size=2.6)
    S(c, 1662, 447, 'PIT', size=2.6)
    S(c, 1480, 1508, 'WH', size=3.0)
    S(c, 1480, 1580, 'WT', size=3.0)
    S(c, 1480, 1692, 'SUMP', size=2.8)
    S(c, 1233, 1671, 'SPRINKLER', size=2.8)
    S(c, 1233, 1690, 'TANK', size=2.8)
    o = B.OPT
    S(c, 1887, 262, 'OPTIONAL PORCH ABOVE', size=3.4, color=o)
    S(c, 226, 1520, 'OPT. CONSERVATORY OR', size=3.4, color=o)
    S(c, 226, 1546, 'IN-LAW SUITE ABOVE', size=3.4, color=o)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    # the furring walls inside the foundation and the columns are drawn thin; trace them too
    walls, wins = B.trace(img, win_drop=WIN_DROP, add=[bhelp.thin_walls(img, drop=TEXT + CIRC_DROP)])
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
