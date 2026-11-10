"""The Romantic - FIRST FLOOR OPTIONS: OPTIONAL SUNROOM (brochure page 3, image xref 19), redrawn clean.

Source raster 1907x1309 px placed at 370.3 dpi, 46.2 px/ft like the first floor. Traced and
re-lettered, labels where they were printed (option drawing). The powder room shown at the foot
gets the same 24" vanity as the first floor in place of its pedestal sink.
"""
import math
import blib as B
import bhelp

PAGE, XREF = 3, 19
K, PXFT = 370.3, 46.2
R2 = math.sqrt(2)

TEXT = [(465, 285, 675, 402), (388, 645, 742, 762), (1168, 748, 1482, 872), (1738, 735, 1778, 945),
        (288, 1045, 402, 1098), (527, 1025, 573, 1166), (338, 1192, 448, 1300), (712, 1138, 832, 1197)]
PDR_SINK = [(362, 1116, 466, 1194)]


def patio_band():
    """Small squares covering the lettering that runs at 45 degrees beside the patio door line,
    so the door and wall lines next to it are kept."""
    out = []
    ox, oy = 660.0, 95.0
    for s in range(20, 285, 5):
        for d in range(11, 49, 5):
            x = ox + s / R2 + d / R2
            y = oy + s / R2 - d / R2
            out.append((x - 4, y - 4, x + 4, y + 4))
    return out


# the three windows along the sunroom's angled wall (the tracer only finds their jambs)
JAMBS = [(226, 362), (330, 262), (434, 154), (534, 54)]


def windows(c):
    for (x0, y0), (x1, y1) in zip(JAMBS, JAMBS[1:]):
        L = math.hypot(x1 - x0, y1 - y0) - 12
        B.window_rot(c, ((x0 + x1) / 2, (y0 + y1) / 2), L, 22, -45)


def labels(c):
    windows(c)
    L, S, o = bhelp.vlabel, B.small, B.OPT
    L(c, 570, 345, 'OPTIONAL\nSUNROOM')
    L(c, 565, 705, 'BREAKFAST NOOK', '13\'-7" × 12\'-10"')
    L(c, 1325, 810, 'FAMILY ROOM', '18\'-0" × 14\'-9"')
    L(c, 395, 1247, 'PDR.\nROOM', name_pt=4.6)
    L(c, 772, 1167, 'HALL', name_pt=4.8)
    S(c, 345, 1072, 'PANTRY', size=3.8)
    S(c, 550, 1096, 'CLOSET', size=3.6, rotate=-90)
    S(c, 1758, 840, 'GAS FIREPLACE', size=3.6, rotate=-90)
    x, y = 660 + 150 / R2 + 28 / R2, 95 + 150 / R2 - 28 / R2
    S(c, x, y, 'OPT. PATIO DOOR', size=3.6, color=o, rotate=45)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    drop = TEXT + PDR_SINK + patio_band()
    bhelp.simple(c, img, K, drop=drop, auto_text=False, after=labels,
                 before=lambda c: B.vanity(c, 418, 1117, 'down', 24, 19))
