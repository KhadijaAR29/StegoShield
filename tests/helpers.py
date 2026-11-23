"""
helpers.py  --  shared by both members
Tiny stand-in tools so Ayesha can test the detector BEFORE Khadija's embed.py is finished.
Not part of the final system.
"""

import numpy as np
from PIL import Image


def make_cover(path: str, size=(256, 256), seed=0):
    """Make a smooth-ish synthetic PNG (gradient + noise) for quick tests."""
    rng = np.random.default_rng(seed)
    h, w = size
    x = np.linspace(0, 255, w)
    base = np.tile(x, (h, 1))
    img = np.stack([base, base[::-1], base.T[:h, :w] if h == w else base], axis=2)
    img = np.clip(img + rng.normal(0, 6, img.shape), 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path)
    return path


def simple_lsb_embed(in_path: str, out_path: str, fill: float = 0.5, seed=1):
    """
    Quick sequential LSB fill with random bits (no encryption).
    fill = fraction of values overwritten (0.0 - 1.0).
    """
    arr = np.array(Image.open(in_path).convert("RGB"))
    flat = arr.flatten()
    n = int(len(flat) * fill)
    bits = np.random.default_rng(seed).integers(0, 2, n, dtype=np.uint8)
    flat[:n] = (flat[:n] & 0xFE) | bits
    Image.fromarray(flat.reshape(arr.shape)).save(out_path)
    return out_path
