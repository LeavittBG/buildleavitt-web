"""The Storyteller - FIRST FLOOR (brochure page 2, image xref 7), redrawn clean.

Source: assets-src/plans/originals/the-storyteller.pdf page 2. This brochure was made here from a
listing-sheet plan (scripts/make-storyteller-brochure.py), not Leavitt's CAD drawings: black wall
bands, beige floors, framed white windows. bhelp.listing_* read that style. The image is placed at
346.7 dpi; 37.6 px/ft (garage 17'-10" x 24'-10" = 671 x 934 px between wall faces).

Restyle only: no soaker tub, pedestal sink, flared or curved stair, desk or bench on this floor. The
kitchen already has one large island; the stair turns on winders and is kept as drawn. Lettering is
re-set with the sizes in the brochure's own format (as in its room table), names centred.
"""
import blib as B
import bhelp as H

PAGE, XREF = 2, 7
K, PXFT = 346.7, 37.6

TEXT = [(1110, 150, 1340, 226), (380, 686, 548, 762), (1280, 775, 1435, 851), (1845, 865, 1975, 945),
        (2110, 905, 2240, 980), (2325, 915, 2450, 990), (1930, 580, 2004, 700), (860, 1010, 932, 1115),
        (1030, 1135, 1112, 1206), (940, 1392, 1068, 1464), (1336, 1390, 1467, 1462),
        (1754, 1324, 1917, 1396), (2242, 1280, 2377, 1351), (350, 1450, 509, 1522)]


HARD = [(790, 1046, 893, 1160), (860, 1010, 934, 1138), (990, 1135, 1112, 1205), (2325, 915, 2450, 990), (2110, 905, 2241, 1028)]


def vlabel(c, x, y, name, size_txt, name_pt=5.4, sub_pt=4.2):
    """Label turned to read bottom-to-top, its two lines side by side."""
    d = c.pt(name_pt) * 0.75
    B.text(c, x - d, y, name, size=name_pt, weight=700, spacing=0.25, rotate=-90)
    B.text(c, x + d, y, size_txt, size=sub_pt, weight=500, color=B.GREY, spacing=0.1, rotate=-90)


def labels(c):
    L = B.label
    L(c, 1218, 200, 'BREAKFAST NOOK', '21\'-2" × 9\'-1"')
    L(c, 455, 742, 'LIVING ROOM', '19\'-7" × 14\'-8"')
    L(c, 1440, 822, 'KITCHEN', '27\'-2" × 17\'-10"')
    vlabel(c, 1950, 645, 'PANTRY', '5\'-5" × 9\'-5"', name_pt=5.6, sub_pt=4.4)
    L(c, 1908, 930, 'HALL', '5\'-5" × 5\'-5"', name_pt=5.6, sub_pt=4.4)
    L(c, 2180, 903, 'W.I.C.', '5\'-2" × 5\'-5"', name_pt=5.4, sub_pt=4.2)
    L(c, 2419, 960, 'BATH', '8\'-0" × 5\'-5"', name_pt=4.6, sub_pt=3.3)
    vlabel(c, 945, 1068, 'HALL', '6\'-1" × 8\'-10"')
    L(c, 1072, 1170, 'BATH', '4\'-11" × 5\'-6"', name_pt=5.0, sub_pt=4.0)
    L(c, 1018, 1436, 'OFFICE', '12\'-6" × 9\'-9"')
    L(c, 1436, 1462, 'FOYER', '9\'-4" × 12\'-0"')
    L(c, 1830, 1372, 'DINING ROOM', '11\'-7" × 17\'-10"')
    L(c, 2313, 1330, 'BEDROOM', '13\'-7" × 15\'-5"')
    L(c, 438, 1495, 'GARAGE', '17\'-10" × 24\'-10"')


def draw(c, img):
    B.K, B.PXFT, c.K = K, PXFT, K
    clean = H.listing_erase_text(img, TEXT, hard=HARD)
    walls, wins = H.listing_trace(clean)
    B.draw_geom(c, H.listing_lines(clean, walls), B.NAVY)
    c.line(1004.5, 1132, 1004.5, 1256, 0.5, color=B.NAVY)   # powder-room vanity edge under the old label
    B.door(c, (2290, 1030), (2385, 1030), side=-1)
    B.door(c, (787, 1053), (787, 1153), side=-1)
    B.door(c, (2236, 1030), (2145, 1030), side=1)        # W.I.C. door        # garage-entry door (its swing crossed the label)     # in-law bath door (its swing crossed the label)
    B.draw_plan_walls(c, walls, wins)
    labels(c)
