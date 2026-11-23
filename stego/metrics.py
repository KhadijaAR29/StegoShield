"""
metrics.py  --  OWNER: Khadija
Image quality metrics: compare a cover image with its stego version.
"""

import numpy as np


def mse(cover: np.ndarray, stego: np.ndarray) -> float:
    """Mean squared error between two images (same shape)."""
    raise NotImplementedError


def psnr(cover: np.ndarray, stego: np.ndarray) -> float:
    """PSNR in dB: 10*log10(255^2 / MSE). Return float('inf') if MSE == 0."""
    raise NotImplementedError
