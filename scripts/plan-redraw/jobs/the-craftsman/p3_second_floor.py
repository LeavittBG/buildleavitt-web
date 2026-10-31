"""The Craftsman - SECOND FLOOR (brochure page 3, image xref 20), redrawn clean.

Source raster 2403x1832 px at 387 dpi, 46.2 px/ft (same print scale as the first floor).
Modernised (Kyle, October 31, 2026): the owner's bath loses its oval soaker tub and its old 3'
shower; the tub alcove (about 4'-3" x 7'-2") becomes one walk-in shower with a glass panel,
linear drain and bench, and the old shower becomes a towel closet behind its existing door.
The hall bath keeps its tub. The U-stair turns on winders and is only re-traced.
"""
import blib as B

PAGE, XREF = 3, 20
K, PXFT = 387.1, 46.2

TEXT = [(190, 256, 502, 372), (761, 165, 810, 305), (956, 236, 1249, 352), (1665, 265, 2024, 377),
        (1672, 424, 2003, 450), (1712, 606, 1963, 640), (140, 656, 269, 702), (140, 898, 269, 945),
        (1145, 856, 1269, 902), (1401, 931, 1527, 980), (495, 756, 602, 802), (751, 826, 855, 872),
        (973, 873, 1019, 994), (1865, 898, 2035, 1005), (915, 1065, 974, 1110), (720, 1141, 897, 1171),
        (173, 1203, 465, 1307), (673, 1286, 940, 1394), (2131, 1115, 2252, 1164)]
OLD_TUB = [(2087, 756, 2277, 1081)]
OLD_SHOWER = [(1655, 761, 1779, 932)]
WIN_DROP = [(950, 1010, 1010, 1080), (1270, 1010, 1310, 1060), (1270, 1440, 1310, 1490)]


def owners_shower(c):
    """Walk-in shower in the old tub alcove: x 2084-2280, y 753-1084."""
    N, k = B.NAVY, PXFT / 12.0
    x0, y0, x1, y1 = 2084.0, 753.0, 2280.0, 1084.0
    B.box(c, x0, y0, x1, y1, sw=0.45)
    c.rect(x1 - 6 * k, y0 + 8 * k, 1.8 * k, (y1 - y0) - 16 * k, sw=0.3, color=N)     # linear drain
    bench = y1 - 15 * k
    c.line(x0, bench, x1, bench, 0.45, color=N)                                       # 15" bench
    c.line(x0, y0 + 38 * k, x0, y1, 1.0, color=N)                                      # glass panel
    B.small(c, (x0 + x1) / 2, (y0 + bench) / 2, 'SHOWER', size=4.2)
    B.small(c, (x0 + x1) / 2, (bench + y1) / 2, 'BENCH', size=3.4, color=B.GREY)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 365, 343, 'BEDROOM 2', '16\'-9" × 10\'-10"')
    L(c, 1100, 323, 'BEDROOM 4', '12\'-0" × 10\'-0"')
    L(c, 1838, 303, "OWNER'S BEDROOM", '19\'-0" × 13\'-10"')
    S(c, 1838, 437, 'OPT. CATHEDRAL CEILING', size=4.0, color=o)
    S(c, 1838, 624, 'OPT. TRAY CEILING', size=4.0, color=o)
    L(c, 332, 1255, 'BEDROOM 3', '13\'-1" × 10\'-10"')
    L(c, 810, 1340, 'OPEN TO\nFOYER BELOW', name_pt=5.6)
    L(c, 803, 850, 'HALL', name_pt=5.4)
    L(c, 548, 780, 'BATH', name_pt=5.2)
    L(c, 1940, 930, "OWNER'S\nBATH", name_pt=5.4)
    S(c, 200, 680, 'W.I.C.', size=4.4)
    S(c, 200, 920, 'W.I.C.', size=4.4)
    S(c, 1203, 865, 'W.I.C.', size=4.4)
    S(c, 1460, 940, 'W.I.C.', size=4.4)
    S(c, 1717, 846, 'TOWEL', size=3.8)
    S(c, 1717, 872, 'CLOSET', size=3.8)
    S(c, 783, 235, 'CLOSET', size=3.8, rotate=-90)
    S(c, 996, 933, 'LINEN', size=3.6, rotate=-90)
    S(c, 945, 1087, 'DN', size=4.2)
    S(c, 808, 1158, 'WOOD RAILING', size=3.4)
    S(c, 2182, 1131, 'SHELF', size=4.0)


def draw(c, img):
    B.K, B.PXFT = K, PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + OLD_TUB + OLD_SHOWER
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_shower(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
