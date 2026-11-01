"""The Innovator - FIRST FLOOR (brochure page 2, image xref 14), redrawn clean.

Source raster 2525x2874 px placed at 471.2 dpi; 46.1 px/ft (garage 19'-7" inside = 903 px,
owner's bedroom 18'-7" = 857 px, garage depth 21'-1" = 975 px).
Traced: walls, windows, linework (doors, kitchen, island, stair, baths, laundry, dashed options).
Modernised (Kyle, October 31, 2026):
  - owner's bath: the angled corner soaker tub on its deck becomes a walk-in shower filling that
    corner (about 5'-6" x 5'-5"): glass on the room side and along the top with a 30" open entry,
    bench on the back wall, linear drain under the window. The old shower stall is across the
    room, so it can't join; it becomes a towel closet behind its existing door.
  - Kyle's follow-up the same day: the small closet above the right-hand vanity (beside it on the
    plan) is removed and the vanity runs on into its space as a 7'-2" double vanity, since the
    towel closet now gives the storage; the towel closet is made shallower, 2'-0" deep instead
    of the old stall's 2'-9", with a framed front and a 24" door, the rest going back to the bath.
Left as drawn: one kitchen island and no peninsula; the stair is straight; the hall bath keeps
its tub; the pantry is a reach-in. All lettering kept as printed (CLAUDE.md: the brochure's
second-floor wording is Kyle's to correct, not ours).
"""
import blib as B

PAGE, XREF = 2, 14
K, PXFT = 471.2, 46.1

TEXT = [(390, 52, 625, 92), (185, 160, 222, 272), (350, 375, 660, 484), (1085, 128, 1292, 165),
        (1045, 459, 1325, 570), (1035, 596, 1328, 636), (1850, 412, 2215, 524), (1900, 550, 2165, 590),
        (405, 605, 445, 698), (1205, 1051, 1317, 1103), (1648, 1051, 1760, 1103), (1760, 1203, 1812, 1330),
        (755, 1303, 868, 1355), (258, 1293, 517, 1345), (255, 1352, 518, 1402), (255, 1429, 518, 1470),
        (1012, 1386, 1165, 1440), (2103, 1449, 2280, 1560), (1252, 1530, 1365, 1583),
        (1558, 1530, 1740, 1583), (1033, 1580, 1145, 1632), (748, 1691, 902, 1771), (1289, 1795, 1442, 1849),
        (760, 1920, 893, 1972), (184, 2038, 581, 2207), (1115, 2090, 1425, 2210), (1820, 2276, 2180, 2387),
        (691, 2549, 954, 2603), (405, 2605, 542, 2685), (1109, 2605, 1246, 2685), (2486, 2600, 2528, 2780),
        (1925, 1099, 2060, 1153), (2270, 1099, 2405, 1153), (25, 1255, 66, 1445), (25, 2045, 66, 2183),
        (120, 1835, 200, 1948), (1548, 1215, 1600, 1255)]
OB_TUB = [(2206, 1586, 2454, 1832)]
OB_STALL = [(1870, 1256, 2092, 1488)]          # old stall, its door and swing, the niche below it
OB_CLOSET = [(2270, 1256, 2456, 1596)]         # closet beside the right-hand vanity + the vanity
# walls to take out: the closet's top jamb stub and its bottom wall (the vanity runs on through)
OB_CUT = [(2355, 1257, 2386, 1290), (2355, 1374, 2456, 1414)]

# new shower: inside faces of the corner, top = end of the right-hand vanity, left = end of the
# bottom vanity counter
SX0, SY0, SX1, SY1 = 2204.0, 1584.0, 2456.0, 1834.0


def owners_shower(c):
    N = B.NAVY
    k = B.PXFT / 12.0
    c.rect(SX0, SY0, SX1 - SX0, SY1 - SY0, sw=0, fill='#ffffff')
    c.line(SX0, SY0, SX1, SY0, 0.45, color=N)
    c.line(SX0, SY0, SX0, SY1, 0.45, color=N)
    B.box(c, SX0 + 2, SY1 - 15 * k, SX1, SY1, sw=0.45)                       # bench, back wall
    B.small(c, (SX0 + SX1) / 2, SY1 - 7.5 * k, 'BENCH', size=3.0, color=B.GREY)
    c.rect(SX1 - 6 * k, SY0 + 8 * k, 1.6 * k, (SY1 - SY0) - 26 * k, sw=0.35, color=N)   # drain
    c.line(SX0 + 1, SY0 + 1, SX0 + 1, SY1 - 15 * k, 1.1, color=N)           # glass, room side
    c.line(SX0 + 30 * k, SY0 + 1, SX1 - 2, SY0 + 1, 1.1, color=N)            # glass, top; entry left
    B.small(c, (SX0 + SX1) / 2 - 6, (SY0 + SY1) / 2 - 8, 'SHOWER', size=3.8)


def towel_closet(c):
    """Old shower stall made a towel closet, 2'-0" deep (back wall at x 1878): shelves behind a
    framed front with a 24" door that swings into the bath; the niche below keeps its place."""
    N = B.NAVY
    k = B.PXFT / 12.0
    x0, y0, y1 = 1878.0, 1261.0, 1440.0
    fx0 = x0 + 24 * k                       # inside face of the new front partition
    fx1 = fx0 + 4.5 * k
    c.rect(1870, 1256, 2092 - 1870, 1486 - 1256, sw=0, fill='#ffffff')
    c.line(x0 + 16 * k, y0 + 2, x0 + 16 * k, y1 - 2, 0.45, color=N, dash=c.dash(2.5, 1.6))   # shelves
    c.line(x0, y1, fx0, y1, 0.45, color=N)                                  # closet floor / niche top
    B.small(c, (x0 + x0 + 16 * k) / 2, (y0 + y1) / 2, 'TOWEL CLOSET', size=3.2, rotate=-90)
    d0, d1 = 1305.0, 1305.0 + 24 * k        # 24" door opening
    for ya, yb in ((1257.0, d0), (d1, 1488.0)):
        c.rect(fx0, ya, fx1 - fx0, yb - ya, sw=0.35, color=N, fill=B.FILL)
    B.door(c, (fx1, d0), (fx1, d1), side=-1)


def owners_vanity(c):
    """Double vanity along the right-hand wall, from the top wall to the shower: 7'-2" x 19"."""
    k = B.PXFT / 12.0
    xw, ya, yb = 2456.0, 1257.0, 1585.0
    L = (yb - ya) / k
    B.vanity(c, xw, (ya + yb) / 2, 'left', L, 19, sinks=(-L / 4, L / 4))


def labels(c):
    L, S, o = B.label, B.small, B.OPT
    L(c, 437, 430, 'KITCHEN', '14\'-2" × 18\'-10"')
    c.rect(1060, 500, 256, 112, sw=0, fill='#ffffff')                     # knock out the beam lines
    L(c, 1188, 555, 'FAMILY ROOM', '16\'-11" × 18\'-6"', 'OPT. BEAMED CEILING')
    L(c, 2026, 495, "OWNER'S BEDROOM", '18\'-7" × 18\'-6"', 'OPT. TRAY CEILING')
    L(c, 389, 1373, 'DINING ROOM', '11\'-5" × 15\'-6"', 'OPT. TRAY CEILING')
    L(c, 822, 1925, 'FOYER')
    S(c, 822, 1972, 'OPT. TRAY', size=3.8, color=B.OPT)
    S(c, 822, 2000, 'CEILING', size=3.8, color=B.OPT)
    L(c, 388, 2095, 'STUDY OR OPTIONAL\nBEDROOM 3', '11\'-5" × 15\'-8"')
    L(c, 1260, 2150, 'BEDROOM 2', '11\'-5" × 15\'-8"')
    L(c, 2003, 2350, 'TWO-CAR GARAGE', '19\'-7" × 21\'-1"')
    L(c, 2190, 1500, "OWNER'S\nBATH", name_pt=5.2)
    L(c, 1310, 1557, 'BATH', name_pt=5.0)
    L(c, 1648, 1557, 'LAUNDRY', name_pt=5.0)
    L(c, 1261, 1077, 'HALL', name_pt=5.4)
    L(c, 1704, 1077, 'HALL', name_pt=5.4)
    L(c, 811, 1329, 'HALL', name_pt=5.4)
    L(c, 1089, 1606, 'HALL', name_pt=5.0)
    L(c, 822, 2576, 'CONC. PORCH', name_pt=5.0)
    S(c, 1088, 1413, 'CLOSET', size=4.0)
    S(c, 1365, 1822, 'CLOSET', size=4.0)
    S(c, 1786, 1266, 'CLOSET', size=3.6, rotate=-90)
    S(c, 1992, 1126, 'W.I.C.', size=4.2)
    S(c, 2338, 1126, 'W.I.C.', size=4.2)
    S(c, 204, 216, 'PANTRY', size=3.4, rotate=-90)
    S(c, 425, 652, 'ISLAND', size=3.4, rotate=-90)
    S(c, 1574, 1235, 'DN', size=4.2)
    S(c, 1188, 147, 'GAS FIREPLACE', size=3.6)
    S(c, 507, 72, 'OPT. PATIO DOOR', size=3.6, color=o)
    S(c, 474, 2625, 'PORCH W/', size=3.4, color=o)
    S(c, 474, 2664, 'ELEV. C', size=3.4, color=o)
    S(c, 1178, 2625, 'PORCH W/', size=3.4, color=o)
    S(c, 1178, 2664, 'ELEV. C', size=3.4, color=o)
    S(c, 2505, 2713, 'OPT. DOOR', size=3.4, color=o, rotate=-90)
    S(c, 45, 1350, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 45, 2114, 'OPT. BAY', size=3.4, color=o, rotate=-90)
    S(c, 143, 1891, 'OPT.', size=3.4, color=o, rotate=-90)
    S(c, 180, 1891, 'WINDOW', size=3.4, color=o, rotate=-90)


def draw(c, img):
    B.K = c.K = K
    B.PXFT = PXFT
    walls, wins = B.trace(img, cut=OB_CUT)
    drop = TEXT + OB_TUB + OB_STALL + OB_CLOSET
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    B.draw_geom(c, B.hairlines(img, walls, drop), B.NAVY)
    owners_shower(c)
    towel_closet(c)
    owners_vanity(c)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
