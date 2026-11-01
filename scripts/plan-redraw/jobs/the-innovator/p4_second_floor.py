"""The Innovator - OPTIONAL SECOND FLOOR (brochure page 4, image xref 23), redrawn clean.

Source raster 2401x2869 px placed at 471.3 dpi; 46.1 px/ft (bedroom 4's 14'-6" = 667 px,
loft depth 16'-0" = 737 px). Traced walls, windows and linework; lettering re-set exactly as
printed, including the page's "optional second floor" wording, which Kyle is having corrected
in the brochure itself (CLAUDE.md). Nothing to modernise: the stair is straight and the bath
keeps its tub/shower (secondary bath).
"""
import blib as B

PAGE, XREF = 4, 23
K, PXFT = 471.3, 46.1

TEXT = [(930, 445, 1270, 565), (980, 733, 1218, 774), (1515, 893, 1640, 945), (1003, 991, 1194, 1028),
        (1123, 1136, 1312, 1173), (1127, 1061, 1240, 1113), (1905, 1228, 2195, 1345), (285, 1290, 585, 1405),
        (1515, 1212, 1575, 1258), (1000, 1478, 1350, 1600), (1520, 1458, 1636, 1511), (1953, 1634, 2106, 1688)]
WIN_DROP = [(1480, 1270, 1525, 1350)]      # stair stringer end, not a window


def labels(c):
    L, S = B.label, B.small
    L(c, 1097, 520, 'OPEN TO FAMILY\nROOM BELOW', name_pt=6.0)
    L(c, 458, 1365, 'LOFT', '18\'-6" × 16\'-0"')
    L(c, 2032, 1312, 'BEDROOM 4', '14\'-6" × 13\'-7"')
    L(c, 1137, 1538, 'MECH. ROOM', '10\'-0" × 8\'-7"', name_pt=5.6)
    L(c, 1183, 1087, 'HALL', name_pt=5.4)
    L(c, 1578, 1485, 'BATH', name_pt=5.0)
    S(c, 1577, 919, 'LINEN', size=4.0)
    S(c, 2030, 1661, 'CLOSET', size=4.0)
    S(c, 1545, 1232, 'DN', size=4.2)
    S(c, 1098, 1009, 'WOOD RAILING', size=3.4)
    S(c, 1216, 1154, 'WOOD RAILING', size=3.4)
    S(c, 1098, 754, 'VAULTED CEILING', size=3.6, color=B.OPT)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    nv, gr = B.lineart(img, walls, drop=TEXT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, TEXT), B.NAVY)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
