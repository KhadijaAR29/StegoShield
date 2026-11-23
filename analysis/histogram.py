"""
histogram.py  --  OWNER: Ayesha
LSB / pixel-value histogram analysis.
"""

import numpy as np


def lsb_ratio(image_array: np.ndarray) -> float:
    """Fraction of LSBs that are 1. Natural images are rarely exactly 0.5; stego tends toward 0.5."""
    raise NotImplementedError


def pair_difference_score(image_array: np.ndarray) -> float:
    """
    Average |count[2k] - count[2k+1]| over all pairs, normalised (0..1).
    SMALL value = pairs are equalised = likely stego.
    """
    raise NotImplementedError


def plot_histograms(cover_array: np.ndarray, stego_array: np.ndarray, save_path: str = None):
    """Matplotlib figure comparing cover vs stego pixel histograms (for the report)."""
    raise NotImplementedError
