"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL KITCHEN/FAMILY ROOM EXTENSION (page 3, xref 21;
482 dpi, 37.8 px/ft). The kitchen has no peninsula, so nothing to modernise. Traced; re-lettered."""
import blib as B, bhelp

PAGE, XREF = 3, 21
B.K = 482.0
SKIP = [(600, 150, 650, 205), (705, 170, 745, 222)]   # patio-door marks


def after(c):
    bhelp.vlabel(c, 1385, 190, 'FAMILY ROOM', '23\'-0" × 19\'-7"')
    bhelp.vlabel(c, 355, 315, 'KITCHEN', '21\'-1" × 16\'-4"')
    bhelp.vlabel(c, 714, 360, 'BREAKFAST\nNOOK')


def draw(c, img):
    bhelp.simple(c, img, 482.0, after=after, auto_text=False,
                 drop=[(1244, 145, 1510, 242), (232, 272, 474, 374), (618, 330, 810, 425)])
