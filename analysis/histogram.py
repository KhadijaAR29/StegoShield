"""
LSB and pixel-value histogram analysis.
"""

import matplotlib.pyplot as plt
import numpy as np

def lsb_ratio(image_array: np.ndarray) -> float:
    """Share of LSBs that are  1. Stego images tend to sit close to  0.5."""
    return float(np.mean(image_array & 1))

def pair_difference_score(image_array: np.ndarray) -> float:
    """
    Compares how different the values are inside each pair (2k, 2k+1) with how
    different they are between neighbouring pairs (2k+1, 2k+2), capped at 1.
    A clean image scores about 1. A SMALL value means the pairs have been
    evened out, which points to stego.
    """
    counts = np.bincount(image_array.ravel(), minlength=256).astype(np.float64)
    within = np.abs(counts[0::2] - counts[1::2]).sum()
    across = np.abs(counts[1:-1:2] - counts[2::2]).sum()
    if across == 0:
        return 1.0
    return float(min(within / across, 1.0))

def plot_histograms(cover_array: np.ndarray, stego_array: np.ndarray, save_path: str = None):
    """Plots  cover vs stego histograms, zoom in on values 120-159 (blue = even, orange = odd)."""
    values = np.arange(120, 160)
    colours = ["tab:blue" if v % 2 == 0 else "tab:orange" for v in values]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, arr, title in [(axes[0], cover_array, "Cover"), (axes[1], stego_array, "Stego")]:
        counts = np.bincount(arr.ravel(), minlength=256)
        ax.bar(values, counts[120:160], color=colours)
        ax.set_title(title)
        ax.set_xlabel("pixel value")
    axes[0].set_ylabel("count")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
