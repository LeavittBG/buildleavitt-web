"""The Daydreamer - FIRST FLOOR OPTIONS: OPTIONAL 3 CAR GARAGE (page 3, xref 22; 482 dpi,
37.8 px/ft). Traced; re-lettered."""
import blib as B, bhelp

PAGE, XREF = 3, 22
B.K = 482.0


def after(c):
    bhelp.vlabel(c, 165, 910, 'THREE-CAR GARAGE', '22\'-10" × 37\'-2"')


def draw(c, img):
    bhelp.simple(c, img, 482.0, after=after, drop=[(0, 862, 330, 958)], auto_text=False,
                 win_drop=[(340, 0, 380, 60)])
