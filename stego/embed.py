"""
embed.py  --  OWNER: Khadija
Hide an encrypted message in a PNG using LSB.

mode="sequential": bits go into pixels 0, 1, 2, ... in order.
mode="random":     pixel positions come from a permutation seeded by the password
                   (use a seed derived from the password, e.g. via PBKDF2 or SHA-256,
                   and np.random.default_rng(seed).permutation(...)).

IMPORTANT: extract.py must regenerate the exact same order, so put the
position-order function in ONE place (here) and import it in extract.py.
"""

import numpy as np


def get_positions(total_values: int, count: int, password: str, mode: str) -> np.ndarray:
    """
    Indices (into the flattened image array) where the `count` bits will be stored.
    Same inputs MUST give the same output (used by both embed and extract).
    """
    raise NotImplementedError


def embed_message(cover_path: str, out_path: str, message: str,
                  password: str, mode: str = "random") -> dict:
    """
    1. load cover PNG as RGB numpy array
    2. encrypt message (crypto.encrypt)
    3. build bitstream (utils.build_bitstream) and check capacity
    4. overwrite LSBs at get_positions(...)
    5. save as PNG (lossless!) to out_path

    Returns {"capacity_bits": int, "used_bits": int, "mode": mode}.
    """
    raise NotImplementedError
