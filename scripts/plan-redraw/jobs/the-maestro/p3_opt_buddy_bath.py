"""The Maestro - SECOND FLOOR OPTIONS: OPTIONAL BUDDY BATH (brochure page 3, image xref 20,
619x1707 px placed at 945.8 dpi, 46.1 px/ft). Walls, windows and linework traced; lettering
re-set, bedroom names centred. The buddy bath keeps its tub/shower (secondary bath); its two
sinks are already in a vanity."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
K, PXFT = 945.8, 46.1
DROP = [(126, 212, 415, 333), (60, 523, 208, 572), (283, 665, 408, 837), (56, 974, 204, 1022),
        (126, 1152, 415, 1273)]


def after(c):
    L, S = bhelp.vlabel, B.small
    L(c, 248, 262, 'BEDROOM 2', '10\'-1" × 12\'-8"', name_pt=3.6, sub_pt=3.1)
    L(c, 248, 1212, 'BEDROOM 3', '10\'-1" × 11\'-0"', name_pt=3.6, sub_pt=3.1)
    L(c, 345, 751, 'OPT.\nBUDDY\nBATH', name_pt=3.0)
    S(c, 134, 548, 'CLOSET', size=2.6)
    S(c, 130, 998, 'CLOSET', size=2.6)


def draw(c, img):
    B.PXFT = PXFT
    bhelp.simple(c, img, K, after=after, drop=DROP, auto_text=False)
