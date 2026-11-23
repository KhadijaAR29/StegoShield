"""
crypto.py  --  OWNER: Khadija
Password -> key (PBKDF2) and AES-256-GCM encrypt / decrypt.

Payload format produced by encrypt():
    salt (16 bytes) | nonce (12 bytes) | ciphertext+tag (n + 16 bytes)
"""

SALT_SIZE = 16
NONCE_SIZE = 12
KDF_ITERATIONS = 200_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Return a 32-byte key (AES-256) from the password using PBKDF2-HMAC-SHA256."""
    raise NotImplementedError


def encrypt(message: bytes, password: str) -> bytes:
    """Encrypt with AES-GCM. Returns salt | nonce | ciphertext+tag."""
    raise NotImplementedError


def decrypt(payload: bytes, password: str) -> bytes:
    """
    Reverse of encrypt().
    Must raise ValueError("Wrong password or data was tampered with")
    when the GCM tag check fails (catch cryptography's InvalidTag).
    """
    raise NotImplementedError
