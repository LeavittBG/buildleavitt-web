"""The Storyteller - SECOND FLOOR (brochure page 3, image xref 12), redrawn clean.

Listing-sheet source like the first floor (see p2_first_floor.py); 346.7 dpi, 37.6 px/ft.

Restyle only. The primary bath already has a large walk-in shower and a double vanity and no tub;
the hall baths keep their tubs; the stair turns on winders and is kept as drawn. Labels are the
listing sheet's (BEDROOM rather than the room table's Bedroom 2-4), sizes in the brochure format.
"""
import blib as B
import bhelp as H

PAGE, XREF = 3, 12
K, PXFT = 346.7, 37.6

TEXT = [(40, 395, 185, 475), (282, 325, 372, 490), (630, 290, 710, 440), (905, 38, 1040, 126),
        (890, 350, 1045, 435), (1333, 235, 1497, 323), (1990, 200, 2170, 285), (2345, 108, 2508, 195),
        (2350, 385, 2510, 465), (1355, 609, 1526, 697), (2250, 605, 2410, 685), (2295, 830, 2450, 910),
        (325, 1145, 615, 1230), (1113, 1177, 1328, 1265), (1622, 1256, 1877, 1299),
        (2195, 1265, 2365, 1345)]
HARD = []
PAD = 10
TEXT = [(x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD) for x0, y0, x1, y1 in TEXT]


def vlabel(c, x, y, name, size_txt, name_pt=5.6, sub_pt=4.4):
    d = c.pt(name_pt) * 0.75
    B.text(c, x - d, y, name, size=name_pt, weight=700, spacing=0.25, rotate=90)
    B.text(c, x + d, y, size_txt, size=sub_pt, weight=500, color=B.GREY, spacing=0.1, rotate=90)


def labels(c):
    L = B.label
    s = dict(name_pt=5.4, sub_pt=4.2)
    L(c, 116, 450, 'BATH', '3\'-2" × 5\'-9"', **s)
    vlabel(c, 335, 410, 'BATH', '9\'-8" × 12\'-8"')
    vlabel(c, 656, 343, 'W.I.C.', '5\'-8" × 12\'-8"')
    L(c, 975, 82, 'BATH', '7\'-9" × 4\'-6"', **s)
    L(c, 969, 400, 'LAUNDRY', '6\'-9" × 7\'-9"')
    L(c, 1412, 290, 'BEDROOM', '10\'-11" × 10\'-9"')
    L(c, 2070, 274, 'BEDROOM', '10\'-11" × 9\'-9"')
    L(c, 2450, 142, 'W.I.C.', '4\'-5" × 4\'-3"', **s)
    L(c, 2430, 425, 'BATH', '4\'-5" × 5\'-2"', **s)
    L(c, 1440, 650, 'HALL', '25\'-8" × 9\'-9"')
    L(c, 2340, 645, 'BATH', '8\'-0" × 5\'-1"', **s)
    L(c, 2372, 870, 'HALL', '3\'-1" × 4\'-5"', **s)
    L(c, 472, 1190, 'PRIMARY BEDROOM', '18\'-0" × 27\'-2"')
    L(c, 1221, 1240, 'FAMILY ROOM', '12\'-6" × 12\'-0"')
    L(c, 1761, 1270, 'OPEN TO BELOW')
    L(c, 2280, 1327, 'BEDROOM', '11\'-7" × 13\'-1"')


def draw(c, img):
    B.K, B.PXFT, c.K = K, PXFT, K
    clean = H.listing_erase_text(img, TEXT, hard=HARD)
    walls, wins = H.listing_trace(clean)
    B.draw_geom(c, H.listing_lines(clean, walls), B.NAVY)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
