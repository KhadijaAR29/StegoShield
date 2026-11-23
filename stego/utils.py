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
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))


def bits_to_bytes(bits: np.ndarray) -> bytes:
    """numpy array of 0/1 -> bytes (length must be a multiple of 8)."""
    if len(bits) % 8 != 0:
        raise ValueError("Number of bits must be a multiple of 8")
    return np.packbits(bits.astype(np.uint8)).tobytes()


def build_bitstream(payload: bytes) -> np.ndarray:
    """32-bit length header + payload bits."""
    header = len(payload).to_bytes(4, "big")
    return bytes_to_bits(header + payload)


def capacity_bits(image_array: np.ndarray) -> int:
    """How many bits fit in the image (1 bit per colour channel value)."""
    return int(image_array.size)


def check_capacity(image_array: np.ndarray, payload: bytes) -> None:
    """Raise ValueError with a clear message if the payload will not fit."""
    needed = HEADER_BITS + 8 * len(payload)
    available = capacity_bits(image_array)
    if needed > available:
        raise ValueError(
            f"Message too large for this image: needs {needed} bits, "
            f"image can hold {available} bits. Use a bigger image or a shorter message."
        )