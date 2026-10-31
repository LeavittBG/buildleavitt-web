"""The Visionary - FIRST FLOOR OPTIONS: OPTIONAL IN-LAW SUITE (brochure page 3, image xref 25, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed.
The optional bath keeps its tub/shower (secondary bath); its sink is a vanity already."""
import blib as B
import bhelp

PAGE, XREF = 3, 25
DROP = [(105, 190, 255, 290), (355, 100, 480, 190), (60, 540, 500, 655)]


def after(c):
    B.label(c, 160, 240, 'OPT.\nBATH', name_pt=5.0)
    B.label(c, 418, 148, 'OPT.\nW.I.C.', name_pt=5.0)
    B.label(c, 318, 597, 'OPTIONAL\nIN-LAW SUITE', '13\'-6" × 15\'-5"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
