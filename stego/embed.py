"""
embed.py  --  OWNER: Khadija
Hide an encrypted message in a PNG using LSB.

mode="sequential": bits go into values 0, 1, 2, ... in order.
mode="random":     positions come from a permutation seeded by the password.

IMPORTANT: extract.py imports get_positions from here, so embed and extract
always use exactly the same order.
"""

import hashlib

import numpy as np
from PIL import Image

from stego import crypto, utils

SEED_LABEL = b"stegoshield-position-seed"


def _seed_from_password(password: str) -> int:
    """Derive a big integer seed from the password (separate from the AES key)."""
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), SEED_LABEL, 100_000, dklen=32
    )
    return int.from_bytes(digest, "big")


def get_positions(total_values: int, count: int, password: str, mode: str) -> np.ndarray:
    """
    Indices (into the flattened image array) where the `count` bits will be stored.
    Same inputs MUST give the same output (used by both embed and extract).

    Random mode: one permutation of ALL positions is generated, and the first
    `count` are used. So the first 32 positions are the same no matter how long
    the message is, which lets extract read the length header first.
    """
    if count > total_values:
        raise ValueError("Not enough room in the image")
    if mode == "sequential":
        return np.arange(count)
    if mode == "random":
        rng = np.random.default_rng(_seed_from_password(password))
        return rng.permutation(total_values)[:count]
    raise ValueError("mode must be 'sequential' or 'random'")


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
    image = np.array(Image.open(cover_path).convert("RGB"), dtype=np.uint8)

    payload = crypto.encrypt(message.encode("utf-8"), password)
    utils.check_capacity(image, payload)
    bits = utils.build_bitstream(payload)

    flat = image.flatten()
    positions = get_positions(flat.size, len(bits), password, mode)
    flat[positions] = (flat[positions] & 0xFE) | bits

    Image.fromarray(flat.reshape(image.shape)).save(out_path, format="PNG")

    return {
        "capacity_bits": utils.capacity_bits(image),
        "used_bits": int(len(bits)),
        "mode": mode,
    }