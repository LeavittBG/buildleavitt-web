"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL SUNROOM (page 3, xref 25; 482 dpi, 37.8 px/ft).
Traced; re-lettered."""
import blib as B, bhelp

PAGE, XREF = 3, 25
B.K = 482.0
TEXT = [(40, 100, 80, 300), (145, 145, 195, 258), (280, 100, 315, 320), (314, 95, 522, 240)]
SKIP = [(90, 185, 150, 215), (75, 288, 125, 322)]


def after(c):
    o = B.OPT
    bhelp.vlabel(c, 422, 168, 'OPTIONAL\nSUNROOM', '11\'-1" × 9\'-6"')
    B.small(c, 298, 210, 'CATHEDRAL CEILING', size=3.4, color=o, rotate=-90)
    B.small(c, 60, 200, 'OPT. PATIO DOOR', size=3.4, color=o, rotate=-90)


def draw(c, img):
    bhelp.simple(c, img, 482.0, after=after, drop=TEXT, text_skip=SKIP, auto_text=False)
