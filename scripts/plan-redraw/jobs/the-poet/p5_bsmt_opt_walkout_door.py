"""The Poet - BASEMENT page, vignette "DOOR WITH OPTIONAL WALKOUT CONDITION" (image xref 28).

The picture is the same drawing as The Pioneer I's (jobs/the-pioneer-i/p6_bsmt_opt_35.py: same size, mean
pixel difference under 3 of 255), so that job's erase rectangles and hand-drawn parts are reused;
everything traced comes from this brochure's own picture. Printed at this brochure's 421.7 dpi.
"""
import importlib.util
import os
import blib as B

PAGE, XREF = 5, 28
B.K, B.PXFT = 421.7, 38.0
_spec = importlib.util.spec_from_file_location(
    'pioneer_28', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'the-pioneer-i', 'p6_bsmt_opt_35.py'))
_P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_P)


def draw(c, img):
    _P.draw(c, img)
