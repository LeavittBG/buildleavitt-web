"""The Visionary - BASEMENT OPTIONS: OPTIONAL BATH WITH OPTIONAL SUNROOM ABOVE (brochure page 7, image xref 39, 478 dpi).
Walls, windows and linework traced, foundation band filled concrete as on the basement plan;
lettering re-set in Roboto Condensed.\nThe optional bath keeps its tub/shower (secondary bath); its sink is already in a vanity."""
import blib as B
import bhelp

PAGE, XREF = 7, 39
DROP = [(345, 183, 597, 327), (232, 310, 326, 402), (90, 500, 344, 538), (136, 93, 208, 165)]


def before(c):
    c.circle(172, 129, 30, sw=0.45, color=B.NAVY, fill='#ffffff')


def after(c):
    L, S, o = bhelp.vlabel, B.small, B.OPT
    L(c, 478, 255, 'OPTIONAL\nUNFINISHED\nSTORAGE/MECH.', name_pt=4.6)
    L(c, 279, 356, 'OPT.\nBATH', name_pt=4.4)
    S(c, 217, 520, '3 PIECE ROUGH-IN STD.', size=3.4)
    S(c, 172, 121, 'EJEC.', size=2.8)
    S(c, 172, 139, 'PIT', size=2.8)


def draw(c, img):
    B.K = c.K = 478.0
    bhelp.vignette(c, img, drop=DROP, band_drop=DROP + [(92, 172, 328, 498)], before=before, after=after)   # with the concrete foundation band
