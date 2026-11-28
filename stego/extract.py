"""
extract.py  --  OWNER: Khadija
Read hidden bits back out of a stego PNG and decrypt them.
"""

import numpy as np
from PIL import Image

from stego import crypto, utils
from stego.embed import get_positions

# smallest possible encrypted payload: salt + nonce + tag (empty message)
MIN_PAYLOAD_BYTES = crypto.SALT_SIZE + crypto.NONCE_SIZE + crypto.TAG_SIZE

def _extract(stego_path: str, password: str, mode: str) -> str:
    """
    1. load stego PNG
    2. read the 32-bit length header (positions via embed.get_positions)
    3. read the payload bits, rebuild bytes
    4. crypto.decrypt -> text

    Raises ValueError on wrong password / tampered data / no valid hidden data.
    """
    image = np.array(Image.open(stego_path).convert("RGB"), dtype=np.uint8)
    flat = image.flatten()

    if flat.size < utils.HEADER_BITS:
        raise ValueError("Image is too small to contain hidden data")

    # 1) length header
    header_pos = get_positions(flat.size, utils.HEADER_BITS, password, mode)
    header_bits = flat[header_pos] & 1
    length = int.from_bytes(utils.bits_to_bytes(header_bits), "big")

    # A wrong password in random mode reads garbage here, so check it is sane
    total_bits = utils.HEADER_BITS + 8 * length
    if length < MIN_PAYLOAD_BYTES or total_bits > flat.size:
        raise ValueError("No hidden data found, or wrong password")

    # 2) payload
    positions = get_positions(flat.size, total_bits, password, mode)
    payload_bits = flat[positions[utils.HEADER_BITS:]] & 1
    payload = utils.bits_to_bytes(payload_bits)

    # 3) decrypt (raises ValueError if the password is wrong or data changed)
    plaintext = crypto.decrypt(payload, password)
        try:
        plaintext = crypto.decrypt(payload, password)
        except ValueError:
            if mode == "random":
                raise ValueError("Hidden data was found, but it is damaged. "
                                 "The image was edited after embedding.")
            raise ValueError("Hidden data was found, but it could not be decrypted. "
                             "The password is wrong, or the image was edited.")
    try:
        return plaintext.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Decrypted data is not valid text")




def extract_message(stego_path: str, password: str, mode: str = "random") -> str:
    """Extract the message. If it fails, check whether the other mode works,
    only to tell the user they picked the wrong mode."""
    try:
        return _extract(stego_path, password, mode)
    except ValueError as first_error:
        other = "sequential" if mode == "random" else "random"
        try:
            _extract(stego_path, password, other)
        except ValueError:
            raise first_error from None
        raise ValueError(
            f"Wrong embedding mode: this message was hidden in '{other}' mode, "
            f"not '{mode}' mode. Select '{other}' and try again."
        ) from None
