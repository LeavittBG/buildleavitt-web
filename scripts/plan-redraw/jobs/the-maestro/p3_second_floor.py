"""The Maestro - SECOND FLOOR (brochure page 3, image xref 21), redrawn clean.

Source raster 2356x2169 px placed at 446.4 dpi; 46.1 px/ft, as on the first floor.
Traced: walls, windows, linework (doors, stair, hall bath, laundry, closets, dashed options).
Modernised (Kyle, October 31, 2026):
  - owner's bath: the angled corner soaker tub on its deck becomes one walk-in shower in the
    same corner (about 5'-5" x 5'-0"): glass panel on the vanity side and along the front with an
    open entry, bench on the back wall, linear drain under the window. The old 3'-0" shower stall
    is across the room behind its own wall, so it can't join; it becomes a towel closet behind
    its existing door.
Left as drawn: the stair is a straight flight; the hall bath keeps its tub and its vanity sink.
"""
import blib as B

PAGE, XREF = 3, 21
K, PXFT = 446.4, 46.1

TEXT = [(108, 433, 392, 542), (1050, 266, 1467, 500), (850, 608, 933, 637), (1583, 608, 1662, 637),
        (1166, 663, 1347, 687), (941, 730, 1047, 775), (555, 646, 592, 700), (83, 820, 225, 867),
        (83, 1005, 225, 1053), (433, 853, 470, 1020), (825, 878, 928, 920), (1208, 863, 1325, 908),
        (1172, 1055, 1300, 1103), (617, 1122, 717, 1167), (587, 1218, 763, 1243), (108, 1308, 397, 1413),
        (587, 1333, 750, 1500), (925, 1308, 1217, 1413), (1650, 1130, 2000, 1303), (1908, 348, 2069, 444),
        (1730, 717, 1858, 763), (2053, 717, 2180, 763), (2155, 925, 2225, 1025), (2155, 1342, 2225, 1442),
        (547, 2083, 803, 2112)]
OB_TUB = [(1975, 118, 2234, 357), (2080, 350, 2156, 374)]
OB_STALL = [(1679, 384, 1809, 557)]
WIN_DROP = [(500, 620, 565, 662)]      # stair stringer end, not a window

# new shower, inside faces: top wall 122, window wall 2231; front edge where the deck ended
SX0, SY0, SX1, SY1 = 1985.0, 122.0, 2231.0, 352.0


def owners_shower(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    c.rect(SX0, SY0, SX1 - SX0, SY1 - SY0, sw=0, fill='#ffffff')
    c.line(SX0, SY0, SX0, SY1, 0.45, color=N)                    # shower floor edge
    c.line(SX0, SY1, SX1, SY1, 0.45, color=N)
    # bench 15" deep on the back (top) wall
    B.box(c, SX0 + 40, SY0, SX1, SY0 + 15 * k, sw=0.45)
    B.small(c, (SX0 + 40 + SX1) / 2, SY0 + 7.5 * k, 'BENCH', size=3.0, color=B.GREY)
    # linear drain along the window wall
    c.rect(SX1 - 6 * k, SY0 + 24 * k, 1.6 * k, (SY1 - SY0) - 32 * k, sw=0.35, color=N)
    # glass: fixed panel on the vanity side, front panel with a 30" open entry at the left
    c.line(SX0 + 1, SY0, SX0 + 1, SY1 - 2, 1.1, color=N)
    c.line(SX0 + 30 * k, SY1 - 1, SX1, SY1 - 1, 1.1, color=N)
    B.small(c, (SX0 + SX1) / 2 + 10, (SY0 + SY1) / 2 + 22, 'SHOWER', size=3.8)


def towel_closet(c):
    """Old shower stall: shelves along its back wall, behind the existing door."""
    N = B.NAVY
    x0, y0, x1, y1 = 1681.0, 386.0, 1808.0, 556.0
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill='#ffffff')
    k = B.PXFT / 12.0
    c.line(x0 + 16 * k, y0, x0 + 16 * k, y1, 0.45, color=N, dash=c.dash(2.5, 1.6))
    B.small(c, x0 + 16 * k + 22, (y0 + y1) / 2 - 10, 'TOWEL', size=3.4, rotate=-90)
    B.small(c, x0 + 16 * k + 44, (y0 + y1) / 2 - 10, 'CLOSET', size=3.4, rotate=-90)


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 262, 493, 'BEDROOM 2', '10\'-1" × 12\'-6"')
    L(c, 1255, 388, 'OPEN TO FAMILY\nROOM BELOW OR\nOPTIONAL BEDROOM 5', note='OPT. BEAMED CEILING')
    L(c, 995, 752, 'HALL', name_pt=5.4)
    L(c, 875, 899, 'BATH', name_pt=5.0)
    L(c, 1267, 886, 'MECH.', name_pt=5.0)
    L(c, 667, 1145, 'HALL', name_pt=5.4)
    L(c, 262, 1340, 'BEDROOM 3', '10\'-1" × 10\'-10"')
    L(c, 668, 1420, 'OPEN TO\nFOYER\nBELOW', name_pt=5.6)
    L(c, 1070, 1350, 'BEDROOM 4', '9\'-11" × 10\'-10"')
    L(c, 1824, 1182, "OWNER'S BEDROOM", '19\'-5" × 15\'-1"', 'OPT. TRAY CEILING')
    L(c, 1985, 425, "OWNER'S\nBATH", name_pt=5.0)
    S(c, 1236, 1079, 'W.I.C.', size=4.2)
    S(c, 1794, 740, 'W.I.C.', size=4.2)
    S(c, 2116, 740, 'W.I.C.', size=4.2)
    S(c, 891, 622, 'LINEN', size=3.4)
    S(c, 1622, 622, 'LINEN', size=3.4)
    S(c, 1256, 675, 'WOOD RAILING', size=3.4)
    S(c, 675, 1231, 'WOOD RAILING', size=3.4)
    S(c, 154, 843, 'CLOSET', size=4.0)
    S(c, 154, 1029, 'CLOSET', size=4.0)
    S(c, 451, 937, 'LAUNDRY', size=4.0, rotate=-90)
    S(c, 573, 673, 'DN', size=4.2, rotate=-90)
    for y in (975, 1392):
        S(c, 2172, y, 'OPT.', size=3.6, color=o, rotate=-90)
        S(c, 2208, y, 'WINDOW', size=3.6, color=o, rotate=-90)
    S(c, 675, 2097, 'WINDOW W/ ELEV. B', size=3.6, color=o)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + OB_TUB + OB_STALL
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_shower(c)
    towel_closet(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
