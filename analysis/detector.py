"""
detector.py  --  OWNER: Ayesha
Combine chi-square + histogram results into one yes/no answer.
"""


def detect(image_path: str) -> dict:
    """
    Load the image, run the tests, combine them.

    MUST return a dict with exactly these keys (the GUI depends on it):
        {
            "likely_hidden": bool,      # final yes/no
            "confidence": float,        # 0.0 - 1.0
            "chi_square_p": float,
            "lsb_ratio": float,
            "pair_diff": float,
        }
    Pick the thresholds by experiment (notebooks/analysis.ipynb) and
    document how you chose them in the report.
    """
    raise NotImplementedError
