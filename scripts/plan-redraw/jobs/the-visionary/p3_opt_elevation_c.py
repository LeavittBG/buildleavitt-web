"""The Visionary - FIRST FLOOR OPTIONS: ELEVATION C (brochure page 3, image xref 22, 478 dpi).
Walls, windows and linework traced; lettering re-set in Roboto Condensed."""
import blib as B
import bhelp

PAGE, XREF = 3, 22
DROP = [(135, 20, 395, 132), (488, 12, 738, 112), (1000, 0, 1268, 96), (1405, 195, 1760, 305)]


def after(c):
    B.label(c, 265, 75, 'LIVING ROOM', '12\'-5" × 14\'-6"')
    B.label(c, 613, 62, 'TWO-STORY\nFOYER', name_pt=5.4)
    B.label(c, 1134, 48, 'DINING ROOM', '12\'-3" × 14\'-6"')
    B.label(c, 1582, 250, 'TWO-CAR GARAGE', '21\'-8" × 28\'-8"')


def draw(c, img):
    bhelp.simple(c, img, 478.0, after=after, drop=DROP, auto_text=False)
