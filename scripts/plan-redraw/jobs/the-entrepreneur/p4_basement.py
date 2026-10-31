"""The Entrepreneur - BASEMENT (brochure page 4, image xref 22), redrawn clean.

Source raster 3420x3212 px placed at 532 dpi; 46.2 px/ft (same scale as the first floor; the
basement outline matches it). Same treatment as The Pioneer I's and The Craftsman's basements:
traced walls and linework, light concrete fill in the foundation band, mechanical circles redrawn
whole, lettering re-set. The optional bath keeps its tub/shower, toilet and vanity as drawn
(secondary baths keep a tub). The stair is straight with a landing: re-traced only.
"""
import blib as B
import bhelp

PAGE, XREF = 4, 22
K, PXFT = 532.0, 46.2
CONC = '#e4e7eb'

TEXT = [(1255, 838, 1575, 897), (2730, 795, 2960, 910), (1055, 1328, 1366, 1371), (1203, 1500, 1320, 1614),
        (1670, 1668, 1733, 1711), (408, 1738, 716, 1853), (2236, 1860, 2312, 1895), (2783, 1981, 2950, 2095),
        (1478, 2310, 1614, 2424), (2739, 3170, 3022, 3212)]
CIRCLES = [(1820, 2446, 66), (2282, 2060, 46), (2282, 2162, 46), (2290, 2468, 40), (1026, 1714, 39)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
WIN_DROP = [(2030, 1370, 2220, 1800)]
# rooms, so only the foundation band between the two foundation lines gets the concrete fill
INTERIOR = [(50, 245, 2390, 1380), (50, 1380, 1330, 2180), (1330, 1380, 2350, 2510), (2440, 600, 3380, 1340),
            (2410, 1400, 3380, 2680), (1390, 2160, 1700, 2580), (2370, 2700, 3420, 3212), (930, 230, 2230, 250)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 1205, 905, 'OPT. REC ROOM')
    L(c, 2902, 968, 'UNFINISHED\nSTORAGE', name_pt=5.6)
    L(c, 1255, 1557, 'OPT.\nBATH', name_pt=5.0)
    S(c, 1212, 1349, '3 PIECE ROUGH-IN STD.', size=3.8)
    L(c, 560, 1796, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 2900, 2036, 'GARAGE\nABOVE', name_pt=5.6, color=B.GREY)
    L(c, 1546, 2368, 'PORCH\nABOVE', name_pt=5.2, color=B.GREY)
    S(c, 2275, 1877, 'A.H.U.', size=3.2)
    S(c, 2282, 2060, 'WH', size=3.2)
    S(c, 2282, 2162, 'WT', size=3.2)
    S(c, 2290, 2468, 'SUMP', size=3.0)
    S(c, 1026, 1704, 'EJEC.', size=2.8)
    S(c, 1026, 1726, 'PIT', size=2.8)
    S(c, 1820, 2434, 'SPRINKLER', size=3.0)
    S(c, 1820, 2458, 'TANK', size=3.0)
    S(c, 1702, 1690, 'UP', size=4.2)
    S(c, 2880, 3192, 'OPT. 3-CAR GARAGE', size=3.8, color=B.OPT)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    conc = bhelp.bands_width(img, half=17, win=37, drop=INTERIOR)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, bhelp.thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
