"""
crypto.py  --  OWNER: Khadija
Password -> key (PBKDF2) and AES-256-GCM encrypt / decrypt.

Payload format produced by encrypt():
    salt (16 bytes) | nonce (12 bytes) | ciphertext+tag (n + 16 bytes)
"""

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16
KDF_ITERATIONS = 200_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Return a 32-byte key (AES-256) from the password using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(message: bytes, password: str) -> bytes:
    """Encrypt with AES-GCM. Returns salt | nonce | ciphertext+tag."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, message, None)
    return salt + nonce + ciphertext


def decrypt(payload: bytes, password: str) -> bytes:
    """
    Reverse of encrypt().
    Raises ValueError("Wrong password or data was tampered with")
    when the GCM tag check fails.
    """
    if len(payload) < SALT_SIZE + NONCE_SIZE + TAG_SIZE:
        raise ValueError("Wrong password or data was tampered with")

    salt = payload[:SALT_SIZE]
    nonce = payload[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = payload[SALT_SIZE + NONCE_SIZE:]

    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError("Wrong password or data was tampered with")