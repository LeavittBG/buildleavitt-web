"""Helpers for the basement jobs (kept out of blib.py)."""
import sys
import numpy as np, cv2
from scipy import ndimage as ndi
import blib as B


def thin_lines(img_path, walls_geom, drop=(), keep_only=None):
    """1-2 px dark lines (dashed option outlines, hairlines). blib.lineart loses these because a
    1 px contour collapses to a zero-area polygon; here they are widened to 3 px first."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    core = lum < 140
    thick = ndi.binary_opening(core, np.ones((3, 3), bool))
    thick = ndi.binary_dilation(thick, np.ones((3, 3), bool))
    thin = core & ~thick
    wm = np.zeros(grey.shape, np.uint8)
    for p in getattr(walls_geom, 'geoms', [walls_geom]):
        if p.is_empty:
            continue
        cv2.fillPoly(wm, [np.array(p.exterior.coords, np.int32)], 1)
    thin &= ~ndi.binary_dilation(wm.astype(bool), np.ones((5, 5), bool))
    dm = B._rects_mask(grey.shape, drop)
    if keep_only is not None:
        dm |= ~B._rects_mask(grey.shape, keep_only)
    thin &= ~dm
    thin = ndi.binary_dilation(thin, np.ones((2, 2), bool))
    return B._contours_to_geom(thin, eps=0.7, min_area=4)


def bands_any(img_path, max_half=15, min_area=250, drop=(), keep=None):
    """Foundation bands for cropped option drawings: narrow white gaps between two foundation
    lines, found without needing an enclosed outline (the crop cuts them open). The image edge
    is treated as ink so a band running off the edge still closes."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = (lum < 200) | grey
    ink[0, :] = ink[-1, :] = True
    ink[:, 0] = ink[:, -1] = True
    free = ~ink
    lab, n = ndi.label(free)
    dist = ndi.distance_transform_edt(free)
    out = np.zeros_like(free)
    for i in range(1, n + 1):
        comp = lab == i
        if comp.sum() < min_area or dist[comp].max() > max_half:
            continue
        out |= comp
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    out[0, :] = out[-1, :] = False
    out[:, 0] = out[:, -1] = False
    return B._contours_to_geom(out, eps=1.0, min_area=50)


def bands_dir(img_path, L=34, min_area=300, drop=(), keep=None):
    """Foundation bands for cropped drawings: white gaps narrower than L px between two solid
    (>= 3 px) lines, closed along each of four directions. Dashed lines are too thin to count.
    Stairs and other striped areas must be excluded with `drop`."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = ndi.binary_opening((lum < 170) | grey, np.ones((3, 3), bool))
    free = ~((lum < 230) | grey)
    k = L
    kernels = [np.ones((1, k), bool), np.ones((k, 1), bool), np.eye(k, dtype=bool), np.fliplr(np.eye(k, dtype=bool))]
    out = np.zeros_like(free)
    for ker in kernels:
        out |= ndi.binary_closing(ink, structure=ker) & free
    lab, n = ndi.label(out)
    sizes = ndi.sum(out, lab, range(1, n + 1))
    keep_ids = [i + 1 for i, s in enumerate(sizes) if s >= min_area]
    out = np.isin(lab, keep_ids)
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    return B._contours_to_geom(out, eps=1.0, min_area=50)


def bands_width(img_path, half=13, win=31, min_area=300, drop=(), keep=None):
    """Foundation bands: white areas whose local half-width (distance to the nearest solid line,
    maximised over a win x win window) stays <= half px, i.e. gaps under about 2*half px between
    two solid lines. Room corners and open space fail the test; stairs must be dropped."""
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = ndi.binary_opening((lum < 170) | grey, np.ones((3, 3), bool))
    free = ~ink & ~((lum < 230) | grey)
    dist = ndi.distance_transform_edt(~ink)
    lm = ndi.maximum_filter(dist, size=win)
    out = free & (lm <= half)
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    if keep is not None:
        out &= B._rects_mask(out.shape, keep)
    lab, n = ndi.label(out)
    sizes = ndi.sum(out, lab, range(1, n + 1))
    out = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= min_area])
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    out[0, :] = out[-1, :] = False
    out[:, 0] = out[:, -1] = False
    return B._contours_to_geom(out, eps=1.0, min_area=50)


CONC = '#e4e7eb'


def vignette(c, img, drop=(), band_drop=(), win_drop=(), add=(), cut=(), before=None, after=None,
             bands=True, trace_kw=None):
    """Standard option-drawing build: concrete bands, traced linework minus `drop`, hand-drawn
    items (`before`, under the walls), walls and windows, then `after` (labels)."""
    walls, wins = B.trace(img, win_drop=win_drop, add=add, cut=cut, **(trace_kw or {}))
    if bands:
        B.draw_geom(c, bands_width(img, drop=band_drop), CONC)
    nv, gr = B.lineart(img, walls, drop=drop)
    B.draw_geom(c, thin_lines(img, walls, drop=drop), B.OPT)
    B.draw_geom(c, gr, B.OPT)
    B.draw_geom(c, nv, B.NAVY)
    if before:
        before(c)
    B.draw_plan_walls(c, walls, wins)
    if after:
        after(c)
