"""
Brings the chi-square and histogram results together into one yes/no answer.

An image gets flagged if any one of these checks fires :
1.  Chi-square p >= 0.5 on the whole image           -> heavy embedding
2.  p >= 0.99 on the first 1/2/5% of the image, but  -> sequential embedding
    p < 0.5 on the later part of the image
3.  pair_diff <= 0.6                                 -> large random embedding
The thresholds were picked in notebooks/analysis.ipynb,  so that no clean
cover image gets flagged.
"""

import numpy as np
from PIL import Image

from analysis.chi_square import chi_square_test, p_value_from_counts
from analysis.histogram import lsb_ratio, pair_difference_score

CHI_P_THRESHOLD = 0.5
START_P_THRESHOLD = 0.99
PAIR_DIFF_THRESHOLD = 0.6


def start_of_image_p(flat: np.ndarray) -> float:
    """Best p-value from the start of image, but only if rest of it looks clean."""
    best = 0.0
    for w in (0.01, 0.02, 0.05):
        n = int(len(flat) * w)
        if n < 1000:
            continue
        start_p = p_value_from_counts(np.bincount(flat[:n], minlength=256))
        later = [p_value_from_counts(np.bincount(flat[int(s * len(flat)):int(s * len(flat)) + n], minlength=256))
                 for s in np.linspace(0.5, 1 - w, 9)]
        if np.median(later) < 0.5:
            best = max(best, start_p)
    return best


def detect(image_path: str) -> dict:
    image = np.array(Image.open(image_path).convert("RGB"), dtype=np.uint8)

    chi_p = chi_square_test(image)
    start_p = start_of_image_p(image.ravel())
    pair_diff = pair_difference_score(image)

    checks = [chi_p >= CHI_P_THRESHOLD,
                 start_p >= START_P_THRESHOLD,
                 pair_diff <= PAIR_DIFF_THRESHOLD]
    likely_hidden = any(checks)

    #confidence: 1 check agreeing -> 0.67, all 3 agreeing -> 1.0
    agree = sum(checks) if likely_hidden else 3 - sum(checks)
    return {
           "likely_hidden": bool(likely_hidden),
           "confidence": round(0.5 + agree / 6, 2),
           "chi_square_p": float(chi_p),
           "lsb_ratio": lsb_ratio(image),
           "pair_diff": float(pair_diff),
    }
