"""THE WHITE BACKGROUND RULE (4 Oct 2026, chat 9 - "mask the white background . do this always"): a photo of an object on a
white background has that background turned into the page colour (Oat #F5EEE3), so no white box shows on the page.
  python3 site/mask_white.py <in> <out> [--crop]     --crop: also cut the picture down to the object (prints the fractions kept)
The background = the light area (every channel > 200) joined to the picture's edge; its own white (60th percentile) becomes Oat,
shadows keep their depth; white inside the object is untouched. The original is never altered. Look at every result."""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
OAT = np.array([245, 238, 227], float)
def mask(src, out, crop=False):
    im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(float)
    lab, _ = ndimage.label(a.min(axis=2) > 200)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}; bg = np.isin(lab, list(edge))
    if not bg.any(): im.save(out, quality=94); return (1, 1), 0.0
    white = np.percentile(a[bg], 60, axis=0); mult = np.clip(a / white, 0, 1) * OAT
    m = np.asarray(Image.fromarray((bg * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.0))).astype(float) / 255; m = np.minimum(m, bg * 1.0)
    res = Image.fromarray((a * (1 - m[..., None]) + mult * m[..., None]).clip(0, 255).astype('uint8')); frac = (1, 1)
    if crop:
        ys, xs = np.where(ndimage.binary_opening(~bg, iterations=2)); pad = 3
        res = res.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad), min(im.height, ys.max() + pad))); frac = (res.width / im.width, res.height / im.height)
    res.save(out, quality=94); return frac, float(bg.mean())
if __name__ == '__main__':
    f, share = mask(sys.argv[1], sys.argv[2], '--crop' in sys.argv); print(f'{sys.argv[2]}: background {share:.0%} of the picture, kept {f[0]:.3f} x {f[1]:.3f}')
