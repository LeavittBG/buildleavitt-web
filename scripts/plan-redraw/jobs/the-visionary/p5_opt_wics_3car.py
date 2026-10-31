"""The Visionary - SECOND FLOOR OPTIONS: W.I.C.'S WITH OPTIONAL 3 CAR GARAGE (brochure page 5, image xref 31, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed.
The strip of owner's bath along the top showed the corner tub; it now shows the foot of the new
walk-in shower (its bench along the outside wall), as on the second floor."""
import blib as B
import bhelp

PAGE, XREF = 5, 31
DROP = [(455, 368, 570, 420), (455, 975, 570, 1026), (712, 0, 912, 74)]


def after(c):
    L, S = bhelp.vlabel, B.small
    L(c, 512, 394, 'W.I.C.', name_pt=5.0)
    L(c, 512, 1000, 'W.I.C.', name_pt=5.0)


def shower(c):
    c.line(719, 0, 719, 84, 0.45, color=B.NAVY)          # shower floor edge (glass opening above)
    B.box(c, 879, 0, 922, 67, sw=0.45)                   # bench along the outside wall


def draw(c, img):
    bhelp.simple(c, img, 478.0, before=shower, after=after, drop=DROP, auto_text=False)
