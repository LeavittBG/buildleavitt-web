"""The Impressionist - BASEMENT (brochure page 4, image xref 20), redrawn clean.

Source raster 2754x3073 px placed at 505.2 dpi; 46.15 px/ft (the same scale as the floors above).
Same treatment as the other basements: traced walls and linework, light concrete fill in the
foundation band, mechanical circles redrawn whole, lettering re-set. The optional bath keeps its
tub/shower, and its sink is already in a vanity; the stair is straight. Nothing to modernise.
"""
import blib as B
import bhelp

PAGE, XREF = 4, 20
K, PXFT = 505.2, 46.15
CONC = '#e4e7eb'

TEXT = [(400, 445, 700, 555), (1487, 537, 1800, 588), (325, 1045, 465, 1150), (608, 922, 668, 1003),
        (750, 1155, 850, 1262), (575, 1445, 880, 1480), (362, 1620, 675, 1725), (1930, 1275, 2280, 1387),
        (1870, 1737, 2180, 1842), (2433, 1755, 2515, 1788), (1110, 1922, 1168, 1968),
        (430, 2220, 563, 2325), (1110, 2237, 1333, 2345), (1983, 2487, 2143, 2595), (0, 937, 43, 1225),
        (2655, 1400, 2695, 1695)]
CIRCLES = [(590, 1370, 40), (1912, 1945, 65), (2155, 1962, 45), (2265, 1962, 45), (2472, 1962, 38)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
WIN_DROP = [(1340, 1470, 1520, 2050)]          # the stair's own posts and stringers
# rooms, so only the foundation band between the foundation lines gets the concrete fill
INTERIOR = [(185, 145, 2525, 2015), (1592, 2050, 2532, 3015), (168, 2055, 852, 2490),
            (886, 2035, 1563, 2582)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 552, 488, 'OPT. OFFICE', '16\'-0" × 16\'-0"')
    L(c, 1645, 560, 'OPT. REC ROOM')
    L(c, 395, 1098, 'OPT.\nW.I.C.', name_pt=5.2)
    L(c, 800, 1208, 'OPT.\nBATH', name_pt=5.0)
    S(c, 727, 1462, '3 PIECE ROUGH-IN STD.', size=3.6)
    L(c, 518, 1672, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.4)
    L(c, 2105, 1331, 'OPT. MEDIA ROOM', '17\'-8" × 15\'-0"')
    L(c, 2025, 1790, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.4)
    L(c, 497, 2272, 'PORCH\nABOVE', name_pt=5.0, color=B.GREY)
    L(c, 1222, 2291, 'UNFINISHED\nSTORAGE', name_pt=5.2)
    L(c, 2063, 2541, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    S(c, 638, 963, 'OPT. LINEN', size=3.0, rotate=-90)
    S(c, 2474, 1772, 'A.H.U.', size=3.0)
    S(c, 590, 1361, 'EJEC.', size=2.8)
    S(c, 590, 1381, 'PIT', size=2.8)
    S(c, 1912, 1934, 'SPRINKLER', size=3.0)
    S(c, 1912, 1956, 'TANK', size=3.0)
    S(c, 2155, 1962, 'WH', size=3.2)
    S(c, 2265, 1962, 'WT', size=3.2)
    S(c, 2472, 1962, 'SUMP', size=2.8)
    S(c, 1138, 1946, 'UP', size=4.0)
    S(c, 21, 1081, 'OPT. 2\'-0" EXTENSION', size=3.4, color=B.OPT, rotate=-90)
    S(c, 2675, 1548, 'OPT. 2\'-0" EXTENSION', size=3.4, color=B.OPT, rotate=-90)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    c.K = K
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
