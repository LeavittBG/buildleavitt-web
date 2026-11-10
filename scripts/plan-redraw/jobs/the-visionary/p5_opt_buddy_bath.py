"""The Visionary - SECOND FLOOR OPTIONS: OPTIONAL BUDDY BATH (brochure page 5, image xref 32, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed.
The buddy bath keeps its tub/shower (secondary bath); its sinks are already in a vanity."""
import blib as B
import bhelp

PAGE, XREF = 5, 32
DROP = [(175, 8, 465, 104), (82, 145, 124, 254), (82, 352, 124, 470), (238, 250, 334, 392), (170, 488, 438, 585)]


def after(c):
    L, S = bhelp.vlabel, B.small
    L(c, 318, 55, 'BEDROOM 4', '12\'-0" × 13\'-9"')
    L(c, 103, 200, 'W.I.C.', name_pt=4.4, rotate=-90)
    L(c, 103, 411, 'W.I.C.', name_pt=4.4, rotate=-90)
    L(c, 269, 322, 'OPT.\nBUDDY\nBATH', name_pt=4.4)
    L(c, 293, 537, 'BEDROOM 3', '12\'-5" × 14\'-0"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
