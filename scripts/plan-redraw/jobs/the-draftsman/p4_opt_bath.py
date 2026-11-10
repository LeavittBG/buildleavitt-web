"""The Draftsman - SECOND FLOOR OPTIONS, "OPTIONAL BATH" (page 4, xref 28), placed at 669.6 dpi.
Traced clean and re-lettered. The optional bath is a secondary bath: it keeps its tub/shower,
and its sink is already in a vanity."""
import blib as B
import bhelp

PAGE, XREF = 4, 28
B.K, B.PXFT = 669.6, 38.0
WIN_DROP = [(705, 40, 745, 95)]


def after(c):
    V = bhelp.vlabel
    V(c, 191, 245, 'OPT.\nBATH', name_pt=3.8)
    V(c, 545, 388, 'BEDROOM 2', '14\'-4" × 16\'-0"', name_pt=4.2, sub_pt=3.6)
    V(c, 172, 512, 'OPT.\nW.I.C.', name_pt=3.8)


def draw(c, img):
    bhelp.simple(c, img, 669.6, after=after, auto_text=False, win_drop=WIN_DROP,
                 drop=[(142, 198, 240, 293), (400, 338, 704, 436), (126, 464, 226, 560)])
