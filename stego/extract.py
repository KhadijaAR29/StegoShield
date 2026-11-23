"""
extract.py  --  OWNER: Khadija
Read hidden bits back out of a stego PNG and decrypt them.
"""


def extract_message(stego_path: str, password: str, mode: str = "random") -> str:
    """
    1. load stego PNG
    2. read the 32-bit length header (positions via embed.get_positions)
    3. read the payload bits, rebuild bytes
    4. crypto.decrypt -> text

    Raises ValueError on wrong password / tampered data / no valid hidden data.
    """
    raise NotImplementedError
