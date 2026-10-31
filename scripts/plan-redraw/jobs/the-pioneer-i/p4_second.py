"""The Pioneer I - SECOND FLOOR (brochure page 4, image xref 25), redrawn clean.

Source: assets-src/plans/the-pioneer-i.pdf page 4, raster 2289x2063 px at 438 dpi, same scale as
the first floor (about 37.8 px/ft). Coordinates are this raster's pixels. Against the first-floor
raster this one is offset by about (-532, -83) px (front and family-room windows line up).

Kept from the source by tracing: walls, windows, doors, closets, vanities, toilets, the hall-bath
shower stall, dashed option outlines. Redrawn by hand (Kyle, October 31, 2026):
  - main stair seen from above: the flared lower flight is straightened to match the first floor
    (straight 45-degree flight, 4'-0" wide, parallel treads), shown inside the floor opening;
    upper flight and wood railings redrawn clean
  - owner's bath: angled corner soaker tub and the old 3'-0" shower removed; one large walk-in
    tiled shower (glass panel, bench, linear drain) where the tub was; the old shower alcove is
    now a towel closet behind its existing door
  - hall bath tub redrawn as a plain rectangular tub/shower (kept as a tub, per Kyle)
  - all lettering in Roboto Condensed
"""
import math, sys
import blib as B

PAGE, XREF = 4, 25
IMG = None   # set by draw()
R2 = math.sqrt(2)

TEXT = [(565, 25, 1012, 60), (52, 405, 408, 438), (1525, 405, 1880, 438), (660, 432, 898, 625),
        (1188, 566, 1426, 662), (1474, 624, 1584, 718), (1758, 695, 2062, 848), (105, 640, 366, 736),
        (752, 832, 905, 860), (788, 888, 884, 933), (380, 978, 485, 1022), (145, 1038, 241, 1084),
        (40, 1166, 76, 1248), (345, 1192, 448, 1236), (1206, 1106, 1258, 1146), (1228, 1245, 1355, 1290),
        (702, 1355, 794, 1398), (652, 1420, 805, 1450), (135, 1459, 384, 1555), (612, 1559, 836, 1659),
        (1064, 1502, 1291, 1598), (1459, 1416, 1555, 1464), (1709, 1428, 1826, 1475),
        (1952, 1342, 2105, 1436), (1916, 1216, 1984, 1284), (1095, 1776, 1241, 1808),
        (1731, 1938, 1976, 1974)]
# main stair: whole floor opening (treads, railings, their notes, DN) redrawn
STAIR = [(528, 950, 1040, 1322)]
OB_TUB = [(2062, 1393, 2257, 1588)]
OB_SHOWER = [(2155, 1045, 2257, 1235)]
HALL_TUB = [(20, 940, 130, 1122)]
WIN_DROP = [(1240, 1080, 1290, 1190)]
# the old shower's partition (solid 8 px, no grey fill, so the tracer misses it): now the towel
# closet's wall, either side of its door
ADD_WALLS = [(2145, 1007, 2153, 1097), (2145, 1181, 2153, 1247)]

# stair frame: first-floor stair() origin (1068, 1262) shifted by (-532, -83)
O = (536.0, 1179.0)
DU = (1 / R2, 1 / R2)
DV = (1 / R2, -1 / R2)
W, U0, T, N_LOW = 151.0, 92.0, 34.0, 4
# upper flight as printed on this floor: 10 treads, 666..987 x 991..1124
UX0, UX1, UY0, UY1, N_UP = 666.0, 987.0, 991.0, 1124.0, 10
# edges of the floor opening (wood railings), as printed
TOP_RAIL_Y = 983.0
OPENING = [(562, 1218), (634, 1290), (853, 1290), (995, 1150), (995, UY1 + 3)]


def P(u, v):
    return (O[0] + DU[0] * u + DV[0] * v, O[1] + DU[1] * u + DV[1] * v)


def rail(c, pts, posts=()):
    """Wood railing: a double line (navy edge, white core) with small square posts."""
    c.polyline(pts, w=1.5, color=B.NAVY, join='miter')
    c.polyline(pts, w=0.45, color='#ffffff', join='miter')
    k = 9.0
    for x, y in posts:
        c.rect(x - k / 2, y - k / 2, k, k, sw=0.5, color=B.NAVY, fill='#ffffff')


def stair(c):
    from shapely.geometry import Polygon, LineString
    N = B.NAVY
    # lower flight, clipped to the floor opening (the rest runs under the hall floor)
    hole = Polygon([(520, UY1 + 3), (520, 1218)] + OPENING)
    u1 = U0 + T * N_LOW
    flight = Polygon([P(U0, 0), P(U0, W), P(u1, W), P(u1, 0)]).intersection(hole)
    c.polyline(list(flight.exterior.coords), w=0.55, color=N, close=True, fill='#ffffff')
    for i in range(1, N_LOW):
        seg = LineString([P(U0 + T * i, 0), P(U0 + T * i, W)]).intersection(hole)
        if not seg.is_empty:
            (ax, ay), (bx, by) = seg.coords[0], seg.coords[-1]
            c.line(ax, ay, bx, by, 0.45, color=N)
    for v in (0, W):                                  # flight rails
        seg = LineString([P(U0 - 4, v), P(u1, v)]).intersection(hole)
        if not seg.is_empty:
            (ax, ay), (bx, by) = seg.coords[0], seg.coords[-1]
            c.line(ax, ay, bx, by, 1.0, color=N)
    # upper flight
    B.box(c, UX0, UY0, UX1, UY1, sw=0.55)
    tw = (UX1 - UX0) / N_UP
    for i in range(1, N_UP):
        x = UX0 + tw * i
        c.line(x, UY0, x, UY1, 0.45, color=N)
    B.arrow(c, [(UX1 + 20, 1058), (UX1 - 26, 1058)], w=0.45)
    B.small(c, UX1 + 26, 1036, 'DN', size=4.2)
    # wood railings around the opening
    rail(c, [(528, TOP_RAIL_Y), (1000, TOP_RAIL_Y)], posts=[(756, TOP_RAIL_Y), (995, TOP_RAIL_Y)])
    rail(c, [(UX0, UY1 + 3), (995, UY1 + 3)] + OPENING[::-1][1:], posts=[(UX0 + 6, UY1 + 3), (995, UY1 + 3)])
    rail(c, OPENING[:4], posts=[(658, 1290), (829, 1290)])
    S = B.small
    S(c, 755, 965, 'WOOD RAILING', size=3.4)
    S(c, 735, 1308, 'WOOD RAILING', size=3.4)
    x, y = (912 + 945) / 2, 1222
    S(c, x + 14, y + 4, 'WOOD RAILING', size=3.4, rotate=-45)


def owners_shower(c):
    """Walk-in shower in the old tub corner: 5'-3" x 5'-0" inside, glass panel on the vanity
    side, open entry from the bath, bench on the back wall, linear drain under the window."""
    N = B.NAVY
    x0, y0, x1, y1 = 2062.0, 1400.0, 2259.0, 1590.0
    c.rect(x0, y0, x1 - x0, y1 - y0, sw=0, fill='#ffffff')
    c.line(x0, y0, x0, y1, 0.45, color=N)                        # shower floor edge
    c.line(x0, y0, x1, y0, 0.45, color=N)
    k = B.PXFT / 12.0
    # bench 15" deep along the bottom wall
    B.box(c, x0 + 40, y1 - 15 * k, x1, y1, sw=0.45)
    B.small(c, (x0 + 40 + x1) / 2, y1 - 7.5 * k, 'BENCH', size=3.0, color=B.GREY)
    # linear drain along the window wall
    c.rect(x1 - 6 * k, y0 + 12 * k, 1.6 * k, (y1 - y0) - 30 * k, sw=0.35, color=N)
    # glass: fixed panel along the vanity side, short return at the top
    c.line(x0, y1 - 2, x0, y0 + 70, 1.1, color=N)
    c.line(x1 - 2, y0, x1 - 60, y0, 1.1, color=N)
    B.small(c, 2150, 1475, 'SHOWER', size=3.8)


def hall_tub(c):
    B.tub(c, 19, 939, 133, 1123)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    S(c, 789, 43, 'OPTIONAL 4\'-0" FAMILY ROOM EXTENSION', size=3.6, color=o)
    S(c, 230, 421, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    S(c, 1703, 421, 'OPTIONAL 2\'-0" REAR EXTENSION', size=3.6, color=o)
    L(c, 779, 515, 'OPEN TO\nFAMILY ROOM\nBELOW', None, 'OPT. BEAMED CEILING', name_pt=5.4)
    L(c, 1307, 612, 'SITTING ROOM', '8\'-4" × 15\'-6"')
    S(c, 1529, 640, 'OPT. 3', size=3.4, color=o)
    S(c, 1529, 669, 'SIDED', size=3.4, color=o)
    S(c, 1529, 698, 'FIREPLACE', size=3.4, color=o)
    L(c, 1910, 770, "OWNER'S BEDROOM", '21\'-2" × 15\'-6"', 'OPT. TRAY CEILING')
    L(c, 235, 688, 'BEDROOM 4', '10\'-10" × 11\'-10"')
    L(c, 836, 911, 'HALL', name_pt=5.0)
    S(c, 432, 1000, 'W.I.C.', size=4.2)
    S(c, 193, 1061, 'BATH', size=4.4, weight=700)
    S(c, 58, 1207, 'LINEN', size=3.6, rotate=-90)
    S(c, 396, 1214, 'W.I.C.', size=4.2)
    S(c, 1291, 1268, 'CLOSET', size=4.0)
    S(c, 1232, 1126, 'DN', size=4.0)
    L(c, 748, 1376, 'HALL', name_pt=5.0)
    L(c, 260, 1506, 'BEDROOM 3', '13\'-11" × 11\'-10"')
    L(c, 724, 1609, 'OPEN TO\nFOYER BELOW', name_pt=5.4)
    L(c, 1177, 1550, 'BEDROOM 2', '14\'-1" × 11\'-6"')
    S(c, 1507, 1440, 'BATH', size=4.4, weight=700)
    S(c, 1767, 1451, 'W.I.C.', size=4.2)
    L(c, 1987, 1395, "OWNER'S\nBATH", name_pt=5.0)
    S(c, 1950, 1250, 'LINEN', size=3.4, rotate=-45)
    S(c, 2206, 1140, 'TOWEL', size=3.4)
    S(c, 2206, 1162, 'CLOSET', size=3.4)
    S(c, 1168, 1792, 'ELEVATION D', size=3.4, color=o)
    S(c, 1853, 1956, 'OPT. EXTENDED W.I.C.', size=3.6, color=o)


def thin_lines(walls, drop):
    """1-px dark lines (dashed option outlines, ceiling lines, thin door swings) that
    B.lineart loses when it vectorises them; drawn in the option grey."""
    import numpy as np, cv2
    from scipy import ndimage as ndi
    a, grey, navy = B.load(IMG)
    lum = a.sum(-1) / 3.0
    core = lum < 120
    thick = ndi.binary_opening(core, np.ones((2, 2), bool))
    thin = core & ~ndi.binary_dilation(thick, np.ones((3, 3), bool))
    wm = np.zeros(core.shape, np.uint8)
    for p in getattr(walls, 'geoms', [walls]):
        cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
    thin &= ~ndi.binary_dilation(wm.astype(bool), np.ones((7, 7), bool))
    thin &= ~B._rects_mask(core.shape, drop)
    thin = ndi.binary_dilation(thin, np.ones((2, 2), bool))
    return B._contours_to_geom(thin, eps=0.6, min_area=2)


def _draw(c):
    walls, wins = B.trace(IMG, win_drop=WIN_DROP, add=ADD_WALLS)
    drop = TEXT + STAIR + OB_TUB + OB_SHOWER + HALL_TUB
    nv, gr = B.lineart(IMG, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, thin_lines(walls, drop), B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    hall_tub(c)
    owners_shower(c)
    stair(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)


def draw(c, img):
    global IMG
    IMG = img
    _draw(c)
