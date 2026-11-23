"""
chi_square.py  --  OWNER: Ayesha
Chi-square test for LSB embedding (pairs-of-values test).

Idea: LSB embedding makes the counts of pixel values 2k and 2k+1 become equal.
For each pair (2k, 2k+1): expected = (count[2k] + count[2k+1]) / 2,
observed = count[2k]. Chi-square statistic -> p-value with scipy.stats.chi2.
A p-value close to 1 means "pairs are suspiciously equal" = likely hidden data.
"""

import numpy as np


def chi_square_test(image_array: np.ndarray, fraction: float = 1.0) -> float:
    """
    image_array: uint8 array (H, W, 3).
    fraction: use only the first `fraction` of the pixels (useful for the
              sequential-embedding "sliding window" version, optional).
    Returns p-value in [0, 1]. HIGH p-value = LIKELY STEGO.
    """
    raise NotImplementedError
