"""The Pioneer I - BASEMENT (brochure page 5, image xref 28), redrawn clean.

Source: assets-src/plans/the-pioneer-i.pdf page 5, raster 3287x2155 px at 438 dpi, about 37.8 px/ft
(Opt. Media Room 18'-1" wide = 2777-2093 = 684 px). Coordinates are that raster's pixels.

Kept from the source by tracing: framed walls, foundation lines, doors and swings, mechanical
equipment, dashed option outlines. The foundation (white band between the two foundation lines in
the source) gets a light concrete fill so it reads as concrete next to the solid framed walls.
Redrawn by hand: the stair treads, the optional bath fixtures (tub kept: secondary baths keep a
tub/shower), and all lettering in Roboto Condensed.
"""
import sys
import blib as B
import found
import bhelp

PAGE, XREF = 5, 28
IMG = None   # set by draw()
CONC = '#e4e7eb'

TEXT = [(1095, 105, 1555, 138), (2195, 105, 2565, 138), (575, 488, 945, 522), (2060, 488, 2430, 522),
        (1020, 800, 1290, 855), (1812, 612, 1868, 668), (1980, 715, 2085, 820), (2305, 775, 2615, 880),
        (1825, 897, 2088, 933), (970, 1092, 1022, 1132), (2105, 1090, 2375, 1190), (2382, 1128, 2450, 1158),
        (2186, 1245, 2295, 1305), (2506, 1278, 2546, 1308), (2591, 1278, 2631, 1308), (2711, 1278, 2775, 1308),
        (1520, 1515, 1790, 1615), (2335, 1690, 2475, 1780), (145, 1620, 420, 1685), (1625, 1850, 1785, 1882),
        (1205, 1885, 1320, 1980), (2900, 2080, 3195, 2112)]
STAIR = [(1018, 1074, 1517, 1199), (965, 1128, 1062, 1142)]
BATH = [(1890, 578, 2086, 692), (1890, 700, 1995, 780), (1890, 783, 1962, 885)]
WIN_DROP = [(1490, 1060, 1530, 1215)]
PORCH_IN = [(560, 1840, 705, 2020)]
# mechanical circles redrawn whole (the text inside them would otherwise cut their outlines)
CIRCLES = [(1842, 638, 32), (2238, 1276, 54), (2528, 1294, 40), (2610, 1294, 40), (2744, 1290, 32)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]


def stair(c):
    N = B.NAVY
    x0, x1, y0, y1 = 1023.0, 1513.0, 1073.0, 1200.0
    B.box(c, x0, y0, x1, y1, sw=0.55)
    xs = [1027 + 31.73 * i for i in range(16)]
    for x in xs[1:]:
        c.line(x, y0, x, y1, 0.45, color=N)
    B.arrow(c, [(975, 1135), (1060, 1135)], w=0.45)
    B.small(c, 996, 1112, 'UP', size=4.2)


def bath(c):
    B.tub(c, 1895, 580, 2083, 686)
    B.toilet(c, 1895, 737, 'right')
    B.vanity(c, 1895, 835, 'right', 30, 19)


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 1155, 828, 'OPT. REC ROOM')
    L(c, 2460, 826, 'OPT. MEDIA ROOM', '18\'-1" × 12\'-7"')
    L(c, 2032, 768, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1956, 916, '3 PIECE ROUGH-IN STD.', size=3.6)
    S(c, 1842, 630, 'EJEC.', size=2.7)
    S(c, 1842, 647, 'PIT', size=2.7)
    L(c, 2240, 1141, 'UNFINISHED\nSTORAGE/MECH.', name_pt=4.8)
    L(c, 1655, 1564, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.2)
    S(c, 2416, 1143, 'A.H.U.', size=3.2)
    S(c, 2238, 1267, 'SPRINKLER', size=2.8)
    S(c, 2238, 1286, 'TANK', size=2.8)
    S(c, 2528, 1294, 'WH', size=3.0)
    S(c, 2610, 1294, 'WT', size=3.0)
    S(c, 2744, 1290, 'SUMP', size=3.0)
    L(c, 2405, 1736, 'GARAGE\nABOVE', name_pt=5.0, color=B.GREY)
    L(c, 1262, 1932, 'PORCH\nABOVE', name_pt=4.6, color=B.GREY)
    S(c, 1325, 122, 'OPTIONAL 4\'-0" FAMILY ROOM EXTENSION', size=3.6, color=o)
    S(c, 2380, 122, 'OPTIONAL MORNING ROOM ABOVE', size=3.6, color=o)
    S(c, 760, 505, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 2245, 505, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 283, 1640, 'OPT. CONSERVATORY OR', size=3.6, color=o)
    S(c, 283, 1668, 'IN-LAW SUITE ABOVE', size=3.6, color=o)
    S(c, 1705, 1866, 'ELEVATION D', size=3.4, color=o)
    S(c, 3048, 2097, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)


def _draw(c):
    walls, wins = B.trace(IMG, win_drop=WIN_DROP)
    conc, _ = found.bands(IMG, drop=PORCH_IN)
    B.draw_geom(c, conc, CONC)
    nv, gr = B.lineart(IMG, walls, drop=TEXT + STAIR + BATH + CIRC_DROP)
    B.draw_geom(c, bhelp.thin_lines(IMG, walls, drop=TEXT + STAIR + BATH + CIRC_DROP), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    bath(c)
    stair(c)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
