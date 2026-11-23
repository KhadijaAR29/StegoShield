"""OWNER: Khadija"""
import pytest
from stego.embed import embed_message
from stego.extract import extract_message
from tests.helpers import make_cover


@pytest.mark.parametrize("mode", ["sequential", "random"])
def test_embed_then_extract(tmp_path, mode):
    cover = make_cover(str(tmp_path / "cover.png"))
    out = str(tmp_path / "stego.png")
    embed_message(cover, out, "secret message", "pw123", mode)
    assert extract_message(out, "pw123", mode) == "secret message"


def test_wrong_password_rejected(tmp_path):
    cover = make_cover(str(tmp_path / "cover.png"))
    out = str(tmp_path / "stego.png")
    embed_message(cover, out, "secret", "pw123", "random")
    with pytest.raises(ValueError):
        extract_message(out, "wrong", "random")


def test_message_too_large(tmp_path):
    cover = make_cover(str(tmp_path / "cover.png"), size=(8, 8))
    with pytest.raises(ValueError):
        embed_message(cover, str(tmp_path / "o.png"), "x" * 5000, "pw", "random")
