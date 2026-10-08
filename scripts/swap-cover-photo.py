"""Replace the elevation drawing on a Leavitt brochure's cover with a photo rendering.

Usage: python3 scripts/swap-cover-photo.py <in.pdf> <photo> <out.pdf>
       (needs `pip install pikepdf pillow`; then run `npm run plans`)

Every October 2026 cover sizes its drawing to the drawing's own shape, but all
of them sit on the same baseline (y=326pt) inside the same frame: at most 528pt
wide from x=42, and at most 300pt tall. The photo is placed whole - nothing is
cropped - as large as that frame allows, centred across it and standing on the
baseline, so every cover's photo lines up with the others. The drawing's image
object is overwritten, so the old drawing does not linger in the file, and the
caption and figures below are untouched.
"""
import io, re, sys
import pikepdf
from pikepdf import Name
from PIL import Image

FRAME_X, FRAME_Y, FRAME_W, FRAME_H = 42.0, 326.0, 528.0, 300.0
MAX_PX = 2400

src, photo, out = sys.argv[1:4]

pdf = pikepdf.open(src)
page = pdf.pages[0]
xobjs = page.Resources.XObject
name, target = max(xobjs.items(), key=lambda kv: int(kv[1].Width) * int(kv[1].Height))

im = Image.open(photo).convert("RGB")
if im.width > MAX_PX:
    im = im.resize((MAX_PX, round(MAX_PX * im.height / im.width)), Image.LANCZOS)
aspect = im.width / im.height
w, h = FRAME_W, FRAME_W / aspect
if h > FRAME_H:
    h, w = FRAME_H, FRAME_H * aspect
x = FRAME_X + (FRAME_W - w) / 2

buf = io.BytesIO()
im.save(buf, "JPEG", quality=90, optimize=True, progressive=True)
target.write(buf.getvalue(), filter=Name.DCTDecode)
target.Width, target.Height = im.width, im.height
target.ColorSpace = Name.DeviceRGB
target.BitsPerComponent = 8
for key in ("/SMask", "/DecodeParms", "/Decode", "/Mask"):
    if key in target:
        del target[key]

streams = list(page.Contents) if isinstance(page.Contents, pikepdf.Array) else [page.Contents]
pattern = re.compile(rb"[\d.\-]+ 0 0 [\d.\-]+ [\d.\-]+ [\d.\-]+ cm(\s*)" + re.escape(name.encode()) + rb" Do")
done = 0
for s in streams:
    data = s.read_bytes()
    new, n = pattern.subn(lambda m: f"{w:.3f} 0 0 {h:.3f} {x:.3f} {FRAME_Y:.3f} cm".encode()
                          + m.group(1) + name.encode() + b" Do", data)
    if n:
        s.write(new)
        done += n
if done != 1:
    sys.exit(f"{src}: expected one placement of {name}, found {done}")

pdf.save(out)
print(f"{src}: {im.width}x{im.height} photo at {w:.0f}x{h:.0f}pt, x={x:.0f}")
