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

# Error messages (one per situation)
NO_DATA_MSG = (
    "No hidden message found. Either this image has nothing hidden in it "
    "(for example, it is the original cover image), or the password is wrong."
)
WRONG_PASSWORD_OR_EDITED_MSG = (
    "Hidden data was found, but it could not be decrypted. "
    "The password is wrong, or the image was edited after embedding."
)
EDITED_MSG = (
    "Hidden data was found, but it is damaged. The image was edited, "
    "resized or saved in a lossy format (like JPEG) after embedding."
)
WRONG_MODE_MSG = (
    "Wrong embedding mode: this message was hidden in '{right}' mode, "
    "not '{wrong}' mode. Select '{right}' and try again."
)


def _extract(flat: np.ndarray, password: str, mode: str) -> str:
    """Try to extract with one mode. Raises ValueError with a clear message."""
    # 1) length header
    header_pos = get_positions(flat.size, utils.HEADER_BITS, password, mode)
    header_bits = flat[header_pos] & 1
    length = int.from_bytes(utils.bits_to_bytes(header_bits), "big")

    # A garbage header means nothing was hidden here with this password/mode
    total_bits = utils.HEADER_BITS + 8 * length
    if length < MIN_PAYLOAD_BYTES or total_bits > flat.size:
        raise ValueError(NO_DATA_MSG)

    # 2) payload
    positions = get_positions(flat.size, total_bits, password, mode)
    payload_bits = flat[positions[utils.HEADER_BITS:]] & 1
    payload = utils.bits_to_bytes(payload_bits)

    # 3) decrypt. The header was valid, so data is there but GCM rejected it.
    try:
        plaintext = crypto.decrypt(payload, password)
    except ValueError:
        # Random mode: a valid header already proves the password is right
        # (wrong password = wrong positions = garbage header), so it was edited.
        # Sequential mode: the header does not depend on the password,
        # so it can be either.
        raise ValueError(EDITED_MSG if mode == "random" else WRONG_PASSWORD_OR_EDITED_MSG)

    try:
        return plaintext.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Decrypted data is not valid text")


def extract_message(stego_path: str, password: str, mode: str = "random") -> str:
    """
    1. load stego PNG
    2. read the 32-bit length header (positions via embed.get_positions)
    3. read the payload bits, rebuild bytes
    4. crypto.decrypt -> text

    If it fails, the other mode is tried with the same password, only to
    give a clearer error ("wrong mode"). The message is never returned
    unless the mode the user chose is correct.

    Raises ValueError on wrong password / wrong mode / tampered data /
    no hidden data.
    """
    if mode not in ("random", "sequential"):
        raise ValueError("mode must be 'sequential' or 'random'")

    image = np.array(Image.open(stego_path).convert("RGB"), dtype=np.uint8)
    flat = image.flatten()

    if flat.size < utils.HEADER_BITS:
        raise ValueError("Image is too small to contain hidden data")

    try:
        return _extract(flat, password, mode)
    except ValueError as first_error:
        other = "sequential" if mode == "random" else "random"
        try:
            _extract(flat, password, other)
        except ValueError:
            raise first_error from None
        raise ValueError(WRONG_MODE_MSG.format(right=other, wrong=mode)) from None
