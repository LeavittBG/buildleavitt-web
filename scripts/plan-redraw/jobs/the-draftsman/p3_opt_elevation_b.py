"""The Draftsman - FIRST FLOOR OPTIONS, "ELEVATION B" (page 3, xref 23), 490 dpi.
Traced clean and re-lettered; labels stay where they were printed."""
import blib as B
import bhelp

PAGE, XREF = 3, 23
B.K, B.PXFT = 490.0, 38.0
WIN_DROP = [(820, 370, 870, 420), (1575, 370, 1625, 420)]


def after(c):
    V = bhelp.vlabel
    V(c, 196, 58, 'W.I.C.', name_pt=4.6)
    V(c, 1101, 43, 'FOYER', name_pt=4.6)
    V(c, 1406, 89, 'DINING ROOM', '11\'-8" × 16\'-0"')
    V(c, 584, 204, 'STUDY', '11\'-5" × 15\'-0"')
    V(c, 1202, 311, 'CONC. PORCH', name_pt=4.6)
    V(c, 2062, 195, 'TWO-CAR GARAGE', '21\'-6" × 28\'-9"')


def draw(c, img):
    bhelp.simple(c, img, 490.0, after=after, auto_text=False, win_drop=WIN_DROP,
                 drop=[(136, 36, 256, 80), (1044, 20, 1158, 66), (1298, 40, 1514, 138), (466, 156, 704, 252),
                       (1092, 288, 1314, 336), (1910, 147, 2214, 243)])
