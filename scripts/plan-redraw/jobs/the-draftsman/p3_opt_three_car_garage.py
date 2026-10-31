"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL 3 CAR GARAGE" (page 3, xref 20), 490 dpi."""
import blib as B
import bhelp

PAGE, XREF = 3, 20
B.K, B.PXFT = 490.0, 38.0


def after(c):
    bhelp.vlabel(c, 164, 784, 'THREE-CAR GARAGE', '21\'-6" × 38\'-9"')


def draw(c, img):
    bhelp.simple(c, img, 490.0, after=after, auto_text=False, drop=[(0, 736, 332, 832)])
