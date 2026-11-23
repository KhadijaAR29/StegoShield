"""
metrics.py  --  OWNER: Khadija
Image quality metrics: compare a cover image with its stego version.
"""

import numpy as np


def mse(cover: np.ndarray, stego: np.ndarray) -> float:
    """Mean squared error between two images (same shape)."""
    if cover.shape != stego.shape:
        raise ValueError("Images must have the same shape")
    diff = cover.astype(np.float64) - stego.astype(np.float64)
    return float(np.mean(diff ** 2))


def psnr(cover: np.ndarray, stego: np.ndarray) -> float:
    """PSNR in dB: 10*log10(255^2 / MSE). Returns inf if the images are identical."""
    error = mse(cover, stego)
    if error == 0:
        return float("inf")
    return float(10 * np.log10((255.0 ** 2) / error))