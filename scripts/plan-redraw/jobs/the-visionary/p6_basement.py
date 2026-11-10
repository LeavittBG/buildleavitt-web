"""The Visionary - BASEMENT (brochure page 6, image xref 34), redrawn clean.

Source raster 2770x2922 px placed at 478 dpi, 37.85 px/ft. Same treatment as The Pioneer I
basement: framed walls solid, the foundation band filled light concrete, linework traced,
mechanical circles redrawn whole, lettering re-set. The optional bath keeps its tub/shower
(secondary bath); its sink is already in a vanity. The basement stair is straight already.
"""
import blib as B
import found
import bhelp

PAGE, XREF = 6, 34
K = 478.0
IMG = None
CONC = '#e4e7eb'

TEXT = [(1790, 144, 2082, 183), (1780, 663, 1862, 759), (1788, 586, 1848, 700), (2150, 610, 2187, 748), (1115, 774, 1378, 822),
        (1632, 774, 1888, 813), (2320, 930, 2615, 1025), (2098, 952, 2142, 1006), (1621, 1196, 1688, 1228),
        (1130, 1526, 1384, 1622), (150, 1630, 417, 1701), (1189, 1855, 1300, 1950), (2248, 1915, 2388, 2011),
        (2358, 2851, 2716, 2890)]
CIRCLES = [(1511, 1907, 54), (1630, 1921, 38), (1714, 1921, 38), (1842, 1917, 32), (2041, 632, 32)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]
WIN_DROP = [(2060, 1120, 2200, 1160), (1720, 1130, 1770, 1270)]


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 1183, 790, 'OPT. REC ROOM')
    L(c, 2463, 980, 'OPT. MEDIA ROOM', '13\'-7" × 21\'-1"')
    L(c, 1822, 738, 'OPT.\nBATH', name_pt=3.9)
    S(c, 1760, 795, '3 PIECE ROUGH-IN STD.', size=3.6)
    S(c, 2041, 624, 'EJEC.', size=2.8)
    S(c, 2041, 642, 'PIT', size=2.8)
    S(c, 2168, 680, 'OPT. CLOSET', size=3.6, rotate=-90)
    S(c, 2112, 980, 'UP', size=4.0, rotate=-90)
    B.arrow(c, [(2134, 960), (2134, 1036)], w=0.4)
    S(c, 1655, 1212, 'A.H.U.', size=3.2)
    L(c, 1236, 1545, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 1244, 1904, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    L(c, 2327, 1965, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    S(c, 1511, 1898, 'SPRINKLER', size=2.8)
    S(c, 1511, 1917, 'TANK', size=2.8)
    S(c, 1630, 1921, 'WH', size=3.0)
    S(c, 1714, 1921, 'WT', size=3.0)
    S(c, 1842, 1917, 'SUMP', size=3.0)
    S(c, 1936, 164, 'OPTIONAL SUNROOM ABOVE', size=3.6, color=o)
    S(c, 282, 1649, 'OPT. CONSERVATORY OR', size=3.6, color=o)
    S(c, 282, 1682, 'IN-LAW SUITE ABOVE', size=3.6, color=o)
    S(c, 2537, 2871, 'OPTIONAL 3-CAR GARAGE ABOVE', size=3.6, color=o)


def draw(c, img):
    global IMG
    IMG = img
    B.K = c.K = K
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    conc, _ = found.bands(img)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, bhelp.thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.toilet(c, 1818, 586, 'down')
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')
    B.draw_plan_walls(c, walls, wins)
    labels(c)
