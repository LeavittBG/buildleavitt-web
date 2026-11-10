"""Foundation bands for basement plans: the white band between the outer foundation line and the
next line in. Returned as a shapely geometry to draw as a light concrete fill under the linework."""
import numpy as np, cv2, sys
import blib as B
from scipy import ndimage as ndi

def bands(img_path, max_half=16, near_out=10, seeds_out=None, extra_ink=(), drop=()):
    a, grey, navy = B.load(img_path)
    lum = a.sum(-1) / 3.0
    ink = (lum < 200) | grey
    for x0, y0, x1, y1 in extra_ink:
        ink[int(y0):int(y1), int(x0):int(x1)] = True
    free = ~ink
    lab, n = ndi.label(free)
    H, W = free.shape
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(border))
    near = ndi.binary_dilation(outside, np.ones((2 * near_out + 1,) * 2, bool))
    dist = ndi.distance_transform_edt(free)
    out = np.zeros_like(free)
    for i in range(1, n + 1):
        if i in border:
            continue
        comp = lab == i
        if comp.sum() < 400:
            continue
        if not (comp & near).any():
            continue
        if dist[comp].max() > max_half:
            continue
        out |= comp
    for x0, y0, x1, y1 in drop:
        out[int(y0):int(y1), int(x0):int(x1)] = False
    out = ndi.binary_dilation(out, np.ones((5, 5), bool))
    return B._contours_to_geom(out, eps=1.0, min_area=50), outside

if __name__ == '__main__':
    from PIL import Image
    g, outside = bands(sys.argv[1])
    a, _, _ = B.load(sys.argv[1])
    im = a.astype(np.uint8).copy()
    m = np.zeros(im.shape[:2], np.uint8)
    for p in getattr(g, 'geoms', [g]):
        cv2.fillPoly(m, [np.array(p.exterior.coords, np.int32)], 1)
    im[m.astype(bool)] = (230, 120, 40)
    Image.fromarray(im).resize((im.shape[1] // 2, im.shape[0] // 2)).save(sys.argv[2])
