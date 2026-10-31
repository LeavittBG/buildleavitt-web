"""The Daydreamer - BASEMENT (brochure page 5, image xref 31), redrawn clean.

Source raster 2846x2380 px placed at 389.4 dpi, 37.8 px/ft (Opt. Media Room 18'-1" wide).
Same treatment as The Pioneer I's basement: traced framed walls, foundation lines, doors,
stairs, bath fixtures (the optional bath keeps its tub; its sink is already in a vanity) and
dashed options; light concrete fill in the foundation band; equipment circles and all lettering
redrawn. Nothing here needed modernising.
"""
import blib as B
import found
import bhelp

PAGE, XREF = 5, 31
B.K = 389.4
CONC = '#e4e7eb'

TEXT = [(1546, 28, 1834, 63), (2027, 180, 2579, 215), (1880, 540, 1975, 633), (2252, 586, 2552, 678),
        (898, 687, 1154, 731), (1714, 738, 1966, 773), (1735, 845, 1826, 912), (1428, 1020, 1491, 1050),
        (1392, 1227, 1642, 1320), (152, 1331, 415, 1398), (1087, 1354, 1132, 1406), (2243, 1447, 2380, 1539),
        (1163, 1593, 1273, 1685), (2129, 2311, 2484, 2346)]
CIRCLES = [(1760, 472, 32), (1796, 1358, 38), (1796, 1440, 38), (1798, 1544, 31), (1480, 1532, 52)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]
WIN_DROP = [(1050, 1080, 1200, 1125), (1365, 955, 1405, 1090)]
PORCH_IN = [(1078, 1548, 1372, 1742)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 1026, 709, 'OPT. REC ROOM')
    L(c, 2378, 655, 'OPT. MEDIA ROOM', '18\'-1" × 12\'-3"')
    L(c, 1927, 587, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1840, 756, '3 PIECE ROUGH-IN STD.', size=3.6)
    L(c, 1780, 878, 'OPT.\nCLOSET', name_pt=3.8)
    L(c, 1517, 1273, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.2)
    L(c, 2307, 1452, 'GARAGE\nABOVE', name_pt=5.0, color=B.GREY)
    L(c, 1218, 1639, 'PORCH\nABOVE', name_pt=4.6, color=B.GREY)
    S(c, 1460, 1035, 'A.H.U.', size=3.2)
    S(c, 1760, 464, 'EJEC.', size=2.7)
    S(c, 1760, 481, 'PIT', size=2.7)
    S(c, 1796, 1358, 'WH', size=3.0)
    S(c, 1796, 1440, 'WT', size=3.0)
    S(c, 1798, 1544, 'SUMP', size=3.0)
    S(c, 1480, 1523, 'SPRINKLER', size=2.8)
    S(c, 1480, 1542, 'TANK', size=2.8)
    S(c, 1110, 1380, 'UP', size=4.0, rotate=-90)
    S(c, 1690, 45, 'OPTIONAL SUNROOM ABOVE', size=3.6, color=o)
    S(c, 2303, 197, 'OPTIONAL KITCHEN/FAMILY ROOM EXTENSION ABOVE', size=3.6, color=o)
    S(c, 283, 1348, 'OPT. CONSERVATORY OR', size=3.4, color=o)
    S(c, 283, 1381, 'IN-LAW SUITE ABOVE', size=3.4, color=o)
    S(c, 2306, 2328, 'OPTIONAL 3-CAR GARAGE ABOVE', size=3.6, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    conc, _ = found.bands(img, drop=PORCH_IN)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, bhelp.thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
