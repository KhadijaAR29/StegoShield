"""OWNER: Khadija"""
import pytest
from stego import crypto


def test_roundtrip():
    payload = crypto.encrypt(b"hello", "pw123")
    assert crypto.decrypt(payload, "pw123") == b"hello"


def test_wrong_password_rejected():
    payload = crypto.encrypt(b"hello", "pw123")
    with pytest.raises(ValueError):
        crypto.decrypt(payload, "wrong")


def test_tampered_data_rejected():
    payload = bytearray(crypto.encrypt(b"hello", "pw123"))
    payload[-1] ^= 1
    with pytest.raises(ValueError):
        crypto.decrypt(bytes(payload), "pw123")
