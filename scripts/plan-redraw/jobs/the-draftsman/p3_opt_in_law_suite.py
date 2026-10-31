"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL IN-LAW SUITE" (page 3, xref 21), 490 dpi.
Traced clean and re-lettered. The optional bath keeps its tub/shower and its vanity
(secondary bath; no pedestal sink)."""
import blib as B
import bhelp

PAGE, XREF = 3, 21
B.K, B.PXFT = 490.0, 38.0


def after(c):
    bhelp.vlabel(c, 452, 347, 'OPTIONAL IN-LAW SUITE', '19\'-4" × 13\'-1"')
    bhelp.vlabel(c, 796, 273, 'OPT.\nBATH', name_pt=4.4)
    B.small(c, 870, 508, 'OPT. CLOSET', size=3.4, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 490.0, after=after, auto_text=False, win_drop=[(35, 0, 85, 45)], 
                 drop=[(256, 300, 650, 395), (748, 226, 844, 322), (851, 438, 889, 580)])
