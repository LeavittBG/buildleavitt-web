"""The Innovator - BASEMENT (brochure page 5, image xref 28), redrawn clean.

Source raster 2406x2880 px placed at 471.3 dpi; 46.1 px/ft, as on the floors above.
Same treatment as the other basements: traced walls and linework, light concrete fill in the
foundation band, mechanical circles redrawn whole, lettering re-set. The optional bath keeps its
tub/shower (secondary baths keep a tub); the stair is straight, re-traced.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 28
K, PXFT = 471.3, 46.1
CONC = '#e4e7eb'

TEXT = [(1000, 586, 1320, 645), (1478, 936, 1792, 982), (1560, 1054, 1675, 1170), (1925, 1330, 2288, 1448),
        (790, 1215, 852, 1262), (1762, 1484, 1815, 1636), (1062, 1550, 1375, 1670), (285, 1828, 586, 1946),
        (1822, 2296, 1996, 2415), (660, 2477, 802, 2597), (1348, 1404, 1426, 1440)]
CIRCLES = [(1572, 1441, 39), (1572, 1645, 65), (1381, 1778, 48), (1381, 1879, 48), (1372, 2405, 39)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
WIN_DROP = [(1420, 1180, 1470, 1340)]      # stair stringer ends, not windows
# rooms, garage and porch interiors, so only the foundation band gets the concrete fill
INTERIOR = [(60, 150, 2320, 975), (60, 975, 1440, 1325), (60, 1345, 900, 2205), (60, 2205, 525, 2425),
            (945, 1340, 1440, 2445), (1455, 995, 1805, 1705), (1825, 995, 2330, 1805),
            (1490, 1875, 2345, 2830), (1475, 1735, 1765, 1875), (535, 2290, 885, 2655)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 1195, 600, 'OPT. REC ROOM')
    L(c, 2080, 1405, 'OPT. MEDIA ROOM', '11\'-3" × 17\'-3"')
    L(c, 470, 1890, 'OPT. DEN', '18\'-8" × 23\'-8"')
    L(c, 1218, 1610, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 1617, 1113, 'OPT.\nBATH', name_pt=5.0)
    L(c, 731, 2537, 'PORCH\nABOVE', name_pt=5.2, color=B.GREY)
    L(c, 1910, 2355, 'GARAGE\nABOVE', name_pt=5.6, color=B.GREY)
    S(c, 1635, 959, '3 PIECE ROUGH-IN STD.', size=3.8)
    S(c, 1788, 1568, 'CLOSET', size=3.8, rotate=-90)
    S(c, 1387, 1422, 'A.H.U.', size=3.2)
    S(c, 1572, 1431, 'EJEC.', size=2.8)
    S(c, 1572, 1452, 'PIT', size=2.8)
    S(c, 1572, 1634, 'SPRINKLER', size=3.0)
    S(c, 1572, 1657, 'TANK', size=3.0)
    S(c, 1381, 1778, 'WH', size=3.2)
    S(c, 1381, 1879, 'WT', size=3.2)
    S(c, 1372, 2405, 'SUMP', size=3.0)
    S(c, 818, 1236, 'UP', size=4.2)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    B.draw_geom(c, bhelp.bands_width(img, drop=INTERIOR), CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, bhelp.thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
