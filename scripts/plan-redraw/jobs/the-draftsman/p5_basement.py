"""The Draftsman - BASEMENT (brochure page 5, image xref 31), redrawn clean.

Source raster 2833x2527 px at 420.9 dpi, 38.0 px/ft. Same treatment as the other basements:
traced framed walls, foundation lines and linework; the foundation band gets the light concrete
fill; stair treads and the equipment circles redrawn; lettering re-set. The optional bath keeps
its tub/shower and its vanity (no pedestal sink here).
"""
import blib as B
import bhelp
from shapely.geometry import box as sbox
from shapely.ops import unary_union

PAGE, XREF = 5, 31
B.K, B.PXFT = 420.9, 38.0
CONC = '#e4e7eb'

TEXT = [(924, 604, 1182, 656), (1090, 912, 1200, 962), (988, 950, 1064, 980), (96, 1124, 350, 1162),
        (164, 1182, 256, 1276), (810, 1398, 1074, 1496), (1984, 1486, 2120, 1584), (944, 1699, 1056, 1773), (946, 1694, 968, 1699),
        (2150, 180, 2626, 218), (1686, 2456, 2042, 2496)]
STAIR = [(912, 1030, 1458, 1166)]
CIRCLES = [(100, 1426, 32), (436, 1748, 56), (732, 1748, 40), (732, 1832, 40), (416, 1880, 32)]
# rooms inside the foundation that the band finder can mistake for wall (bath, porch box)
NOT_CONCRETE = [(40, 1168, 372, 1372), (806, 1688, 1172, 1784)]
CIRC_DROP = [(x - r - 5, y - r - 5, x + r + 5, y + r + 5) for x, y, r in CIRCLES]


def stair(c):
    N = B.NAVY
    x0, x1, y0, y1 = 970.0, 1458.0, 1032.0, 1162.0
    B.box(c, x0, y0, x1, y1, sw=0.55)
    n = 15
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        c.line(x, y0, x, y1, 0.45, color=N)
    B.arrow(c, [(924, 1101), (1004, 1101)], w=0.45)
    B.small(c, 944, 1078, 'UP', size=4.0)


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 1050, 630, 'OPT. REC ROOM')
    L(c, 1145, 937, 'MECH.', name_pt=5.0)
    L(c, 942, 1446, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.6)
    L(c, 210, 1228, 'OPT.\nBATH', name_pt=4.6)
    S(c, 222, 1143, '3 PIECE ROUGH-IN STD.', size=3.6)
    L(c, 2052, 1535, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    L(c, 1000, 1737, 'PORCH\nABOVE', name_pt=4.8, color=B.GREY)
    S(c, 1026, 965, 'A.H.U.', size=3.0)
    S(c, 100, 1418, 'EJEC.', size=2.8)
    S(c, 100, 1436, 'PIT', size=2.8)
    S(c, 436, 1738, 'SPRINKLER', size=3.0)
    S(c, 436, 1759, 'TANK', size=3.0)
    S(c, 732, 1748, 'WH', size=3.2)
    S(c, 732, 1832, 'WT', size=3.2)
    S(c, 416, 1880, 'SUMP', size=3.0)
    S(c, 2388, 199, 'OPTIONAL SUNROOM OR IN-LAW SUITE ABOVE', size=3.6, color=o)
    S(c, 1864, 2476, 'OPTIONAL 3-CAR GARAGE ABOVE', size=3.6, color=o)


def draw(c, img):
    walls, wins = B.trace(img)
    conc = bhelp.bands_width(img, half=17, win=37, drop=STAIR + CIRC_DROP + TEXT)
    conc = conc.difference(unary_union([sbox(*r) for r in NOT_CONCRETE]))
    B.draw_geom(c, conc, CONC)
    drop = TEXT + STAIR + CIRC_DROP
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    stair(c)
    circles(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
