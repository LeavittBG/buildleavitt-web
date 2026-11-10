"""The Novel - BASEMENT OPTIONS, "DOOR WITH OPTIONAL WALKOUT CONDITION" (page 6, image xref 32).

The picture is the same drawing as The Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_35.py; same size within
1 px, mean pixel difference under 3 of 255, the same one The Poet reuses), so that job's erase
rectangles and hand-drawn parts are reused; everything traced comes from this brochure's own
picture. Printed at this brochure's 412.4 dpi.
"""
import importlib.util
import os
import blib as B

PAGE, XREF = 6, 32
B.K, B.PXFT = 412.4, 37.95
_spec = importlib.util.spec_from_file_location(
    'pioneer_32', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_35.py'))
_P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_P)


def draw(c, img):
    B.K = c.K = 412.4
    _P.draw(c, img)
