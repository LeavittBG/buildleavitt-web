"""The Craftsman - BASEMENT (brochure page 4, image xref 27), redrawn clean.

Source raster 2412x2269 px at 387 dpi, 46.2 px/ft (Opt. Den 12'-1" x 12'-6" = 558 x 577 px).
Same treatment as The Pioneer I's basement: traced walls and linework, light concrete fill in the
foundation band, mechanical circles redrawn whole, lettering re-set. The optional bath keeps its
tub/shower and vanity (secondary baths keep a tub). The U-stair turns on winders: re-traced only.
"""
import blib as B
import bhelp

PAGE, XREF = 4, 27
K, PXFT = 387.1, 46.2
CONC = '#e4e7eb'

TEXT = [(988, 43, 1237, 80), (638, 876, 945, 925), (1450, 905, 1574, 954), (1325, 1003, 1402, 1033),
        (1851, 765, 2132, 872), (303, 1090, 605, 1124), (435, 1170, 544, 1272), (131, 1535, 444, 1639),
        (918, 1768, 972, 1810), (1698, 1635, 1855, 1739), (745, 1995, 869, 2099)]
CIRCLES = [(1500, 1043, 47), (1600, 1043, 47), (105, 1213, 39), (200, 1213, 39), (562, 1480, 65)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
WIN_DROP = [(950, 1400, 1320, 1900)]
PORCH_IN = [(680, 1935, 938, 2172)]
# rooms, so only the foundation band between the two foundation lines gets the concrete fill
INTERIOR = [(45, 520, 1310, 1890), (1310, 520, 2265, 1110), (1360, 1165, 2272, 2190)] + PORCH_IN


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 672, 831, 'OPT. REC ROOM')
    L(c, 1497, 925, 'MECH.', name_pt=5.4)
    L(c, 1979, 808, 'OPT. DEN', '12\'-1" × 12\'-6"')
    L(c, 490, 1220, 'OPT.\nBATH', name_pt=5.0)
    S(c, 454, 1107, '3 PIECE ROUGH-IN STD.', size=3.8)
    L(c, 330, 1650, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.4)
    L(c, 1813, 1678, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    L(c, 808, 2054, 'PORCH\nABOVE', name_pt=5.0, color=B.GREY)
    S(c, 1364, 1018, 'A.H.U.', size=3.2)
    S(c, 1500, 1043, 'WH', size=3.2)
    S(c, 1600, 1043, 'WT', size=3.2)
    S(c, 105, 1213, 'SUMP', size=3.0)
    S(c, 200, 1204, 'EJEC.', size=2.8)
    S(c, 200, 1224, 'PIT', size=2.8)
    S(c, 562, 1470, 'SPRINKLER', size=3.0)
    S(c, 562, 1492, 'TANK', size=3.0)
    S(c, 945, 1789, 'UP', size=4.2)
    S(c, 1112, 62, 'PORCH W/ ELEV. D', size=3.8, color=B.OPT)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
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
