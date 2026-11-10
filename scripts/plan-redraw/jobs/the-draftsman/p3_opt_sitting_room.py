"""The Draftsman - FIRST FLOOR OPTIONS, "OPTIONAL SITTING ROOM" (page 3, xref 22), 490 dpi."""
import blib as B
import bhelp

PAGE, XREF = 3, 22
B.K, B.PXFT = 490.0, 38.0


def after(c):
    bhelp.vlabel(c, 189, 190, 'OPT. SITTING ROOM', '8\'-6" × 6\'-2"')


def draw(c, img):
    bhelp.simple(c, img, 490.0, after=after, auto_text=False, drop=[(26, 140, 352, 242)])
