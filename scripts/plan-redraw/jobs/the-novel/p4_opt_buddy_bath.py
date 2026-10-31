"""The Novel - SECOND FLOOR OPTIONS, "OPTIONAL BUDDY BATH" (page 4, xref 24), redrawn clean.
Placed at 688.2 dpi; the drawing itself is at the main plan's 37.95 px/ft, so lettering prints at the
same paper size. The buddy bath keeps its tub (secondary bath); its sink is already in a vanity.
Lettering re-set as printed (the vignette prints Bedroom 4 as 15'-6" and Bedroom 3 as 15'-0")."""
import blib as B
import bhelp

PAGE, XREF = 4, 24
B.K, B.PXFT = 688.2, 37.95
TEXT = [(228, 28, 458, 122), (250, 380, 355, 528), (403, 332, 440, 408), (65, 165, 215, 215),
        (60, 605, 215, 655), (172, 700, 418, 798)]


def after(c):
    # this vignette prints the plan at 0.6x the main plan's size, so its lettering is set smaller
    # to keep the printed letter-to-room proportion
    bhelp.vlabel(c, 341, 72, 'BEDROOM 4', '13\'-9" × 15\'-6"', name_pt=3.8, sub_pt=3.2)
    bhelp.vlabel(c, 300, 452, 'OPT.\nBUDDY\nBATH', name_pt=3.2)
    bhelp.vlabel(c, 286, 748, 'BEDROOM 3', '13\'-9" × 15\'-0"', name_pt=3.8, sub_pt=3.2)
    B.small(c, 128, 190, 'W.I.C.', size=3.0)
    B.small(c, 125, 630, 'W.I.C.', size=3.0)
    B.small(c, 421, 370, 'LINEN', size=2.4, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 688.2, after=after, drop=TEXT, auto_text=False)
