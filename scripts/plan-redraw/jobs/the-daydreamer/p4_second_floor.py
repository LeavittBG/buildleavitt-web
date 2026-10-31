"""The Daydreamer - SECOND FLOOR (brochure page 4, image xref 29), redrawn clean.

Source raster 2299x1679 px placed at 389.5 dpi, 37.8 px/ft (owner's bedroom 23'-0" = 870 px).

Kept by tracing: walls, windows, doors, closets, the hall bath with its tub (a secondary bath keeps
its tub/shower), dashed options and the 'window with Elev. B' detail below the plan.
Changed (Kyle, October 31, 2026):
  - owner's bath: the oval soaker tub on its platform becomes one walk-in tiled shower (glass
    panel, linear drain, bench) in the same alcove; the old shower stall beside it cannot join
    (a partition and ledge sit between), so it becomes a towel closet behind its existing door,
    as on The Pioneer I
  - main stair, seen from above: the lower flight's rounded (bullnose) first step becomes a
    square-cut step with a square newel, matching the first floor
  - lettering re-set; room names centred in their rooms
"""
import blib as B

PAGE, XREF = 4, 29
B.K = 389.5

TEXT = [(2135, 58, 2197, 152), (2135, 420, 2197, 512), (172, 178, 428, 274), (1072, 192, 1217, 283),
        (843, 226, 884, 302), (1612, 258, 1910, 404), (850, 494, 941, 538), (618, 548, 772, 576),
        (345, 548, 381, 620), (1026, 621, 1120, 665), (148, 864, 402, 964), (952, 906, 1208, 1007),
        (580, 1009, 802, 1100), (208, 1181, 355, 1216), (580, 1571, 802, 1606),
        (68, 562, 182, 622), (188, 542, 302, 602), (855, 608, 909, 647), (1160, 628, 1275, 690),
        (1480, 628, 1595, 690), (1925, 628, 2040, 690)]
TUB = [(1070, 30, 1315, 178)]
STALL = [(874, 35, 1029, 133)]                 # shower stall interior: X lines and drain
STAIR = [(533, 712, 690, 1000)]
WIN_DROP = [(835, 640, 875, 715), (525, 705, 565, 735)]

# owner's bath: tub platform alcove (image px)
AX0, AX1, AY0, AY1 = 1073.0, 1312.0, 28.0, 175.0
# stair lower flight
SX0, SX1, SY0, SY1 = 537.0, 647.0, 716.0, 966.0
TREADS = 8


def owners_bath(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    bench = 15 * k
    B.shower(c, AX0, AY0, AX1, AY1, glass=((AX0, AY1), (AX0 + 128, AY1)), drain='linear')
    B.box(c, AX1 - bench, AY0, AX1, AY1, sw=0.45)
    B.small(c, AX1 - bench / 2, (AY0 + AY1) / 2, 'BENCH', size=3.0, rotate=-90)
    B.small(c, (AX0 + AX1 - bench) / 2, (AY0 + AY1) / 2 + 6, 'SHOWER', size=4.0, weight=700)
    # old stall: towel closet with shelves
    c.line(878, 60, 1026, 60, 0.45, color=N, dash=c.dash(3, 2))
    c.line(878, 104, 1026, 104, 0.45, color=N, dash=c.dash(3, 2))
    B.small(c, 952, 82, 'TOWEL CLOSET', size=3.6)


def stair(c):
    N = B.NAVY
    B.box(c, SX0, SY0, SX1, SY1, sw=0.55)
    for i in range(1, TREADS):
        y = SY0 + (SY1 - SY0) * i / TREADS
        c.line(SX0, y, SX1, y, 0.45, color=N)
    c.line(SX1 + 6, 700, SX1 + 6, SY1 - 4, 1.0, color=N)
    B.box(c, SX1, SY1 - 12, SX1 + 12, SY1, sw=0.4, fill=N)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 293, 250, 'BEDROOM 4', '14\'-6" × 12\'-0"')
    L(c, 1762, 304, 'OWNER\'S BEDROOM', '23\'-0" × 14\'-7"', 'OPT. TRAY CEILING')
    L(c, 1175, 262, 'OWNER\'S\nBATH', name_pt=5.6)
    L(c, 262, 915, 'BEDROOM 3', '13\'-0" × 12\'-0"')
    L(c, 1092, 985, 'BEDROOM 2', '12\'-0" × 13\'-4"')
    L(c, 691, 1055, 'OPEN TO\nFOYER BELOW', name_pt=5.4)
    L(c, 895, 516, 'HALL', name_pt=5.4)
    S(c, 1073, 643, 'MECH.', size=4.2)
    S(c, 125, 596, 'W.I.C.', size=4.2)
    S(c, 245, 576, 'W.I.C.', size=4.2)
    S(c, 1217, 665, 'W.I.C.', size=4.2)
    S(c, 1537, 665, 'W.I.C.', size=4.2)
    S(c, 1982, 665, 'W.I.C.', size=4.2)
    S(c, 362, 584, 'LINEN', size=3.4, rotate=-90)
    S(c, 862, 264, 'LINEN', size=3.4, rotate=-90)
    S(c, 695, 562, 'WOOD RAILING', size=3.4)
    S(c, 882, 627, 'DN', size=4.0)
    S(c, 2166, 105, 'OPT. WINDOW', size=3.2, color=o, rotate=-90)
    S(c, 2166, 466, 'OPT. WINDOW', size=3.2, color=o, rotate=-90)
    S(c, 282, 1199, 'ELEVATION D', size=3.4, color=o)
    S(c, 691, 1589, 'WINDOW W/ ELEV. B', size=3.4, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + TUB + STALL + STAIR
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_bath(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
