"""OWNER: Ayesha  (uses helpers.py so it works before embed.py is done)"""
from analysis.detector import detect
from tests.helpers import make_cover, simple_lsb_embed

REQUIRED_KEYS = {"likely_hidden", "confidence", "chi_square_p", "lsb_ratio", "pair_diff"}


def test_detect_output_format(tmp_path):
    cover = make_cover(str(tmp_path / "c.png"))
    result = detect(cover)
    assert REQUIRED_KEYS <= set(result)


def test_detects_heavy_embedding(tmp_path):
    cover = make_cover(str(tmp_path / "c.png"))
    stego = simple_lsb_embed(cover, str(tmp_path / "s.png"), fill=1.0)
    assert detect(stego)["likely_hidden"] is True


def test_clean_image_not_flagged(tmp_path):
    cover = make_cover(str(tmp_path / "c.png"))
    assert detect(cover)["likely_hidden"] is False
