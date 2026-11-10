"""The Draftsman - FIRST FLOOR (brochure page 2, image xref 15), redrawn clean.

Source raster 2832x2572 px placed at 420.9 dpi, 38.0 px/ft (garage 21'-6" inside = 817 px).

Kept by tracing: walls, windows, doors, cabinets, appliances, stairs, dashed options.
Changed (Kyle, October 31, 2026):
  - owner's bath: the oval soaker tub and the angled corner shower beside it become one large
    walk-in shower across both alcoves (glass front, open entry, bench, linear drain)
  - main stair: the rounded (bullnose) first step becomes a square-cut step with square newels
  - powder room: pedestal sink -> 24" vanity
  - lettering re-set in Roboto Condensed, room names centred in their rooms
  - kitchen: the small island becomes a 6'-4" x 3'-2" island with three stools (40" to the
    cooktop and angled sink runs, 36" to the bar and behind the stools)
Left as is: the bar counter between the family
room and kitchen is a divider, not a peninsula; no desk or garage-entry bench; no room for a
walk-in pantry (the pantry is a reach-in under the counter run).
"""
import blib as B
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union

PAGE, XREF = 2, 15
B.K, B.PXFT = 420.9, 38.0

TEXT = [(1596, 0, 1822, 36), (1026, 230, 1224, 266), (2172, 218, 2614, 258), (1454, 310, 1714, 408),
        (1706, 326, 1814, 468), (122, 240, 234, 294), (416, 312, 594, 410), (452, 426, 504, 702),
        (884, 578, 1342, 672), (1598, 624, 1852, 726), (1768, 764, 1872, 796), (2254, 882, 2446, 926),
        (628, 896, 796, 942), (2044, 1018, 2172, 1052), (148, 1082, 492, 1232), (642, 1108, 778, 1156),
        (986, 1098, 1036, 1142), (1458, 1102, 1512, 1142), (678, 1328, 806, 1422), (908, 1464, 1066, 1508),
        (1278, 1460, 1532, 1606), (1872, 1554, 2216, 1654), (54, 1608, 306, 1686), (468, 1690, 698, 1788),
        (860, 1772, 1122, 1816), (1078, 2006, 1368, 2042), (328, 2052, 836, 2096), (1708, 2512, 2016, 2546)]
LINEN_TEXT = Polygon([(282, 652), (342, 712), (360, 694), (300, 634)])
# owner's bath: tub alcove + corner shower (with its door swing) become one shower
SHOWER = Polygon([(378, 160), (780, 160), (780, 390), (721, 390), (618, 293), (378, 293)])
BATH_DROP = unary_union([SHOWER.buffer(5, join_style=2),
                         Polygon([(624, 298), (726, 394), (705, 412), (624, 412)])])
STAIR_START = [(1026, 1030, 1072, 1250)]
PDR_SINK = [(632, 1318, 692, 1410)]
WIN_DROP = [(790, 990, 825, 1030), (790, 1225, 825, 1265), (1130, 1040, 1310, 1225),
            (1440, 1070, 1470, 1215), (2185, 1065, 2340, 1095)]


def shower(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    c.polyline(list(SHOWER.exterior.coords), w=0.5, color=N, close=True, fill='#ffffff')
    c.rect(392, 166, 345, 1.6 * k, sw=0.3, color=N)                       # linear drain, back wall
    B.box(c, 733, 200, 780, 386, sw=0.45)                                # 15" bench, right end
    c.line(470, 293, 618, 293, 1.0, color=N)                             # glass front
    c.line(618, 293, 721, 390, 1.0, color=N)                             # glass on the angle
    B.small(c, 600, 228, 'SHOWER', size=4.2)
    B.small(c, 757, 293, 'BENCH', size=3.0, rotate=-90)
    # the cathedral ridge line runs on over the shower, as printed
    c.line(495, 166, 495, 290, 0.35, color=N, dash=c.dash(6, 3))


def stair_start(c):
    N = B.NAVY
    B.box(c, 1040, 1046, 1072, 1234, sw=0.55)                            # square-cut first step
    for y in (1062, 1218):
        c.rect(1047, y - 6, 12, 12, sw=0.4, color=N, fill=N)              # square newels
        c.line(1059, y, 1074, y, 0.9, color=N)
    B.arrow(c, [(994, 1140), (1036, 1140)], w=0.45)


OLD_ISLAND = [(1732, 731, 1904, 848)]

def island(c, x0, y0, x1, y1, stools):
    """Larger island (Kyle, October 31, 2026): seating overhang on the same side as the old
    island's, 12 in deep (dashed), stools drawn like The Pioneer I's."""
    k = B.PXFT / 12.0
    B.box(c, x0, y0, x1, y1, sw=0.6)
    c.line(x0, y1 - 12 * k, x1, y1 - 12 * k, 0.35, color=B.NAVY, dash=c.dash(2.5, 1.6))
    for i in range(stools):
        cx = x0 + (x1 - x0) * (i + 0.5) / stools
        c.circle(cx, y1 + 9.5 * k, 7 * k, sw=0.45, color=B.GREY)


def labels(c):
    L, S = B.label, B.small
    o = B.OPT
    L(c, 1123, 645, 'TWO-STORY\nFAMILY ROOM', '16\'-3" × 21\'-8"')
    L(c, 1705, 335, 'MORNING ROOM', '13\'-6" × 11\'-10"', 'OPTIONAL CATHEDRAL CEILING')
    L(c, 1764, 663, 'KITCHEN', '19\'-4" × 14\'-0"')
    L(c, 317, 1128, "OWNER'S BEDROOM", '15\'-5" × 19\'-11"', 'OPT. TRAY CEILING')
    L(c, 505, 420, "OWNER'S\nBATH", note='OPT. CATHEDRAL CEILING')
    L(c, 1408, 1530, 'DINING ROOM', '11\'-8" × 16\'-0"', 'OPT. TRAY CEILING')
    L(c, 2055, 1610, 'TWO-CAR GARAGE', '21\'-6" × 28\'-9"')
    L(c, 581, 1746, 'STUDY', '11\'-5" × 12\'-0"')
    L(c, 990, 1490, 'FOYER')
    L(c, 2328, 905, 'LAUNDRY', name_pt=5.6)
    L(c, 712, 1127, 'HALL', name_pt=5.4)
    L(c, 745, 1376, 'PDR.\nROOM', name_pt=5.0)
    L(c, 178, 267, 'W.I.C.', name_pt=5.4)
    L(c, 180, 1647, 'W.I.C.', note='OPT. SITTING ROOM', name_pt=5.4)
    L(c, 991, 1794, 'CONC. PORCH', name_pt=5.0)
    S(c, 712, 919, 'CLOSET', size=4.0)
    S(c, 2108, 1035, 'PANTRY', size=3.6)
    S(c, 1764, 771, 'ISLAND', size=3.6)
    S(c, 321, 673, 'LINEN', size=3.4, rotate=45)
    S(c, 1010, 1118, 'UP', size=4.0)
    S(c, 1485, 1122, 'DN', size=4.0)
    S(c, 1125, 248, 'GAS FIREPLACE', size=3.6)
    S(c, 1708, 17, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 2393, 238, 'OPTIONAL SUNROOM OR IN-LAW SUITE', size=3.6, color=o)
    S(c, 1223, 2024, 'PORCH W/ ELEVATION B', size=3.6, color=o)
    S(c, 582, 2074, 'EXTENDED STUDY W/ ELEVATION B', size=3.6, color=o)
    S(c, 1862, 2529, 'OPTIONAL 3-CAR GARAGE', size=3.6, color=o)


def draw(c, img):
    walls, wins = B.trace(img, win_drop=WIN_DROP)
    drop = TEXT + STAIR_START + PDR_SINK + OLD_ISLAND
    cutout = unary_union([BATH_DROP, LINEN_TEXT])
    nv, gr = B.lineart(img, walls, drop=drop)
    hl = B.hairlines(img, walls, drop)
    B.draw_geom(c, gr.difference(cutout), B.OPT)
    B.draw_geom(c, nv.difference(cutout), B.NAVY)
    B.draw_geom(c, hl.difference(cutout), B.NAVY)
    shower(c)
    stair_start(c)
    B.vanity(c, 630, 1365, 'right', 24, 19)                     # powder room vanity
    island(c, 1644, 727, 1884, 847, 3)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
