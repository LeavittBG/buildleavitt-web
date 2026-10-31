"""The Visionary - SECOND FLOOR OPTIONS: OPTIONAL BEDROOM 5 (brochure page 5, image xref 29, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed.
The optional bath keeps its tub/shower (secondary bath); its sink is already in a vanity."""
import blib as B
import bhelp

PAGE, XREF = 5, 29
DROP = [(240, 295, 600, 395), (155, 676, 275, 768), (594, 706, 694, 806), (115, 876, 190, 911), (388, 950, 481, 1000)]


def after(c):
    L, S = bhelp.vlabel, B.small
    L(c, 424, 344, 'OPTIONAL BEDROOM 5', '17\'-1" × 13\'-8"')
    L(c, 215, 722, 'OPT.\nW.I.C.', name_pt=4.6)
    L(c, 644, 756, 'OPT.\nBATH', name_pt=4.6)
    S(c, 152, 894, 'LINEN', size=3.4)
    L(c, 434, 975, 'HALL', name_pt=4.8)


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
