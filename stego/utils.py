"""
utils.py  --  OWNER: Khadija
Bytes <-> bits, length header, capacity check.

Bit stream layout hidden in the image:
    [ 32-bit payload length (in bytes) ][ payload bits ... ]
"""

import numpy as np

HEADER_BITS = 32


def bytes_to_bits(data: bytes) -> np.ndarray:
    """bytes -> numpy array of 0/1 (uint8)."""
    raise NotImplementedError


def bits_to_bytes(bits: np.ndarray) -> bytes:
    """numpy array of 0/1 -> bytes (length must be a multiple of 8)."""
    raise NotImplementedError


def build_bitstream(payload: bytes) -> np.ndarray:
    """32-bit length header + payload bits."""
    raise NotImplementedError


def capacity_bits(image_array: np.ndarray) -> int:
    """How many bits fit in the image (1 bit per colour channel value)."""
    raise NotImplementedError


def check_capacity(image_array: np.ndarray, payload: bytes) -> None:
    """Raise ValueError with a clear message if the payload will not fit."""
    raise NotImplementedError
