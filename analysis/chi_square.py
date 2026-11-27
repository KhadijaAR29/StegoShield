"""
Chi-square test for LSB embedding (pairs-of-values test).

When data is hidden in LSBs,  counts of values 2k and 2k+1 end up
almost equal. For each pair we use expected = (count[2k] + count[2k+1]) / 2
and observed = count[2k].
A HIGH p-value (close to 1) means pairs are nearly equal, so image
probably has hidden data in it.
"""

import numpy as np
from scipy.stats import chi2

def p_value_from_counts(counts: np.ndarray) -> float:
        """Get the chi-square p-value from a 256-bin histogram."""
        counts = counts.astype(np.float64)
        even, odd = counts[0::2], counts[1::2]
        total = even + odd
        keep = total >= 10                      # skip pairs that have too few pixels to  trust
        if keep.sum() < 2:
            return 0.0
        expected = total[keep] / 2
        statistic = np.sum((even[keep] - expected) ** 2 / expected)
        return float(chi2.sf(statistic, keep.sum() - 1))


def chi_square_test(image_array: np.ndarray, fraction: float = 1.0) -> float:
    """
    image_array: uint8 array (H, W, 3).
    fraction: how much of the data to test, taken from the start (1.0 = the whole image).
    Returns a p-value in [0, 1]. A HIGH p-value means the image is LIKELY STEGO.
    """
    flat = image_array.ravel()
    n = max(1, int(len(flat) * fraction))
    return p_value_from_counts(np.bincount(flat[:n], minlength=256))
