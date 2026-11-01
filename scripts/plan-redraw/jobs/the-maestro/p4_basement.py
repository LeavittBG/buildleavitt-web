"""The Maestro - BASEMENT (brochure page 4, image xref 25), redrawn clean.

Source raster 2350x2717 px placed at 446.4 dpi; 46.1 px/ft, as on the floors above.
Same treatment as the other basements: traced walls and linework, light concrete fill in the
foundation band, mechanical circles redrawn whole, lettering re-set. The optional bath keeps its
tub/shower and its small vanity (secondary baths keep a tub). The stair is straight: re-traced.
"""
import blib as B
import bhelp

PAGE, XREF = 4, 25
K, PXFT = 446.4, 46.1
CONC = '#e4e7eb'

TEXT = [(1742, 54, 2152, 84), (1090, 1072, 1392, 1120), (1800, 1136, 2146, 1246), (714, 1227, 756, 1283),
        (609, 1435, 914, 1467), (1514, 1582, 1585, 1611), (930, 1614, 1238, 1720), (203, 1717, 495, 1828),
        (650, 1623, 752, 1732), (663, 1960, 793, 2068), (614, 2222, 739, 2328), (1680, 2123, 1837, 2228)]
CIRCLES = [(929, 1804, 40), (1247, 1802, 46), (1247, 1902, 46), (951, 2040, 65), (1240, 2058, 38)]
CIRC_DROP = [(x - r - 6, y - r - 6, x + r + 6, y + r + 6) for x, y, r in CIRCLES]
WIN_DROP = [(500, 930, 860, 1250)]      # stair top and foot bars, not windows
# rooms and the dashed morning-room outline, so only the foundation band gets the concrete fill
INTERIOR = [(52, 795, 860, 2098), (860, 700, 2205, 1670), (2200, 960, 2285, 1520), (860, 1670, 1305, 2098),
            (1345, 1725, 2210, 2690), (525, 2160, 825, 2390), (1158, 580, 1345, 690), (1640, 0, 2260, 662),
            (500, 900, 860, 1300)]


def circles(c):
    for x, y, r in CIRCLES:
        c.circle(x, y, r - 2, sw=0.45, color=B.NAVY, fill='#ffffff')


def labels(c):
    L, S = B.label, B.small
    L(c, 1241, 1096, 'OPT. REC ROOM')
    L(c, 1943, 1185, 'OPT. MEDIA ROOM', '11\'-5" × 20\'-9"')
    L(c, 336, 1790, 'OPT. DEN', '12\'-2" × 12\'-11"')
    L(c, 1084, 1667, 'UNFINISHED\nSTORAGE/MECH.', name_pt=5.4)
    L(c, 703, 1677, 'OPT.\nBATH', name_pt=5.0)
    L(c, 728, 2014, 'OPT.\nW.I.C.', name_pt=5.0)
    L(c, 676, 2275, 'PORCH\nABOVE', name_pt=5.0, color=B.GREY)
    L(c, 1777, 2210, 'GARAGE\nABOVE', name_pt=5.4, color=B.GREY)
    S(c, 762, 1451, '3 PIECE ROUGH-IN STD.', size=3.8)
    S(c, 1549, 1597, 'A.H.U.', size=3.2)
    S(c, 929, 1795, 'EJEC.', size=2.8)
    S(c, 929, 1815, 'PIT', size=2.8)
    S(c, 1247, 1802, 'WH', size=3.2)
    S(c, 1247, 1902, 'WT', size=3.2)
    S(c, 951, 2030, 'SPRINKLER', size=3.0)
    S(c, 951, 2052, 'TANK', size=3.0)
    S(c, 1240, 2058, 'SUMP', size=3.0)
    S(c, 735, 1255, 'UP', size=4.2, rotate=-90)
    S(c, 1947, 69, 'OPTIONAL MORNING ROOM ABOVE', size=3.8, color=B.OPT)


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
