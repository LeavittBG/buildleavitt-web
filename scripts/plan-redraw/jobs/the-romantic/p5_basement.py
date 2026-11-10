"""The Romantic - BASEMENT (brochure page 5, image xref 24), redrawn clean.

Source raster 2304x2103 px at 370.5 dpi, 46.2 px/ft like the floors above (Opt. Media Room
12'-11" wide = 597 px). Same treatment as the other basements: traced framed walls, foundation
lines and linework, the foundation band gets the light concrete fill, the equipment circles are
redrawn, lettering re-set. The stair is straight and kept as traced; the optional bath keeps its
tub/shower, and its sink is already in a vanity.
"""
import blib as B
import bhelp

PAGE, XREF = 5, 24
K, PXFT = 370.5, 46.2
CONC = '#e4e7eb'

TEXT = [(440, 498, 752, 552), (1243, 328, 1552, 367), (1748, 422, 2102, 538), (1533, 405, 1572, 584),
        (1258, 522, 1358, 569), (1258, 581, 1364, 627), (1108, 802, 1197, 832), (743, 982, 1057, 1092), (1638, 1292, 1802, 1398),
        (278, 1678, 412, 1788), (753, 1658, 1102, 1768)]
CIRCLES = [(918, 862, 46), (842, 938, 46), (1140, 918, 38), (992, 1160, 66), (1534, 700, 38)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
# everything inside the foundation (the band finder also reads gaps in lettering and fixtures)
INTERIOR = [(150, 150, 2140, 1850)]
WIN_DROP = [(1060, 960, 1240, 1010), (720, 1240, 1080, 1290)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 596, 525, 'OPT. REC ROOM')
    L(c, 1925, 480, 'OPT. DEN', '12\'-0" × 13\'-5"')
    L(c, 930, 1715, 'OPT. MEDIA ROOM', '12\'-11" × 12\'-9"')
    L(c, 880, 1037, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 1310, 575, "OPT.\nBATH", name_pt=4.8)
    L(c, 1720, 1345, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    L(c, 345, 1733, 'PORCH\nABOVE', name_pt=5.0, color=B.GREY)
    S(c, 1397, 347, '3 PIECE ROUGH-IN STD.', size=3.8)
    S(c, 1552, 494, 'OPT. CLOSET', size=3.6, rotate=-90)
    S(c, 1152, 818, 'A.H.U.', size=3.4)
    S(c, 1534, 690, 'EJEC.', size=3.0)
    S(c, 1534, 711, 'PIT', size=3.0)
    S(c, 918, 862, 'WT', size=3.4)
    S(c, 842, 938, 'WH', size=3.4)
    S(c, 1140, 918, 'SUMP', size=3.2)
    S(c, 992, 1149, 'SPRINKLER', size=3.2)
    S(c, 992, 1171, 'TANK', size=3.2)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    conc = bhelp.bands_width(img, half=14, win=33, drop=INTERIOR)
    B.draw_geom(c, conc, CONC)
    drop = TEXT + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
