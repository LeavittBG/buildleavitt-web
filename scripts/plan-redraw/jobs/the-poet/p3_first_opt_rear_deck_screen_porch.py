"""The Poet - FIRST FLOOR OPTIONS: OPTIONAL REAR DECK AND SCREEN PORCH (image xref 20).
Traced walls, posts, doors and linework; lettering re-set. No modernising needed."""
import blib as B, bhelp

PAGE, XREF = 3, 20
B.K, B.PXFT = 421.7, 38.0
TEXT = [(267, 237, 519, 282), (861, 289, 1099, 382), (277, 567, 560, 664), (996, 725, 1088, 769)]


def after(c):
    B.label(c, 397, 250, 'OPTIONAL DECK', name_pt=5.6)
    B.label(c, 965, 390, 'OPTIONAL\nSCREEN PORCH', name_pt=5.6)
    B.label(c, 418, 612, 'BREAKFAST NOOK', '17\'-8" × 14\'-6"', name_pt=5.6)
    B.label(c, 1042, 747, 'HALL', name_pt=5.0)


def draw(c, img):
    bhelp.vignette(c, img, drop=TEXT, win_drop=[(1295, 350, 1320, 380)], bands=False, after=after)
