"""The Illustrator - BASEMENT (brochure page 6, image xref 36), redrawn clean.

Source raster 2374x1968 px at 370.4 dpi, 32.3 px/ft (same scale as the floors above). Same
treatment as The Pioneer I's basement: traced framed walls, foundation lines and linework; the
foundation band gets the light concrete fill; the mechanical circles are redrawn; lettering re-set.
The stair is a straight L with a square landing, kept as traced. The optional bath keeps its
tub/shower and its vanity (no pedestal sink here).
"""
import blib as B
import found

PAGE, XREF = 6, 36
B.K, B.PXFT = 370.4, 32.3
CONC = '#e4e7eb'

TEXT = [(1365, 113, 1652, 147), (195, 406, 492, 449), (1840, 406, 2139, 449), (718, 718, 982, 772),
        (1848, 723, 2127, 822), (1490, 600, 1590, 693), (1343, 710, 1602, 744), (358, 1328, 622, 1422),
        (1823, 1443, 1967, 1532), (748, 1733, 862, 1827), (918, 1413, 962, 1467), (28, 928, 67, 1202),
        (2298, 848, 2337, 1147), (131, 1138, 195, 1167)]
CIRCLES = [(1298, 544, 33), (754, 1151, 40), (836, 1151, 39), (157, 1341, 31), (821, 1343, 53)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 850, 745, 'OPT. REC ROOM')
    L(c, 1987, 772, 'OPT. MEDIA ROOM', '14\'-5" × 13\'-11"')
    L(c, 490, 1375, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 1540, 646, 'OPT.\nBATH', name_pt=4.8)
    S(c, 1472, 727, '3 PIECE ROUGH-IN STD.', size=3.6)
    L(c, 1895, 1487, 'GARAGE\nABOVE', name_pt=5.2, color=B.GREY)
    L(c, 805, 1780, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 940, 1440, 'UP', size=4.0, rotate=-90)
    S(c, 163, 1152, 'A.H.U.', size=3.2)
    S(c, 1298, 535, 'EJEC.', size=2.8)
    S(c, 1298, 554, 'PIT', size=2.8)
    S(c, 754, 1151, 'WH', size=3.2)
    S(c, 836, 1151, 'WT', size=3.2)
    S(c, 157, 1341, 'SUMP', size=3.0)
    S(c, 821, 1333, 'SPRINKLER', size=3.0)
    S(c, 821, 1354, 'TANK', size=3.0)
    S(c, 1508, 130, 'OPTIONAL SUNROOM ABOVE', size=3.6, color=o)
    S(c, 343, 427, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 1988, 427, 'OPTIONAL 2\'-0" EXTENSION', size=3.6, color=o)
    S(c, 47, 1065, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)
    S(c, 2317, 997, 'OPTIONAL 2\'-0" EXTENSION', size=3.4, color=o, rotate=-90)


def draw(c, img):
    c.K = B.K
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
