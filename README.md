# StegoShield

Secure image steganography with AES-256 encryption and hidden-data detection.
FAST-NUCES Lahore, Fall 2026. Authors: Khadija A-Rahim (23L-1008), Ayesha Arshad (23L-2596).

The tool hides an AES-256-GCM encrypted message inside a PNG using LSB embedding
(sequential or password-seeded random order), extracts it again, and can detect
whether an image probably contains hidden LSB data (chi-square + histogram analysis).

## Setup

```bash
git clone <repo-url>
cd stegoshield
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
```

## Run

```bash
python main.py embed   data/cover_images/a.png data/stego_images/a_stego.png "secret" mypassword --mode random
python main.py extract data/stego_images/a_stego.png mypassword --mode random
python main.py detect  data/stego_images/a_stego.png
```

GUI (once finished): `streamlit run gui/app.py`

Tests: `pytest`

## Project structure

| Folder | What is inside | Owner |
|---|---|---|
| `stego/` | crypto, bit utils, embed, extract, PSNR/MSE | Khadija |
| `analysis/` | chi-square, histogram, detector | Ayesha |
| `gui/` | user interface | Khadija |
| `notebooks/` | bulk experiments and graphs | Ayesha |
| `tests/` | unit tests | each owner tests their own part |
| `data/` | cover images and generated stego images | Ayesha collects covers |
| `results/`, `docs/` | graphs, tables, report | shared (see TASKS.md) |

## Shared interface (do not change without telling the other person)

```python
# Khadija provides
stego.embed.embed_message(cover_path, out_path, message, password, mode="random") -> dict
stego.extract.extract_message(stego_path, password, mode="random") -> str   # raises ValueError if wrong password
stego.metrics.psnr(cover_array, stego_array) -> float
stego.metrics.mse(cover_array, stego_array) -> float

# Ayesha provides
analysis.detector.detect(image_path) -> {
    "likely_hidden": bool, "confidence": float,
    "chi_square_p": float, "lsb_ratio": float, "pair_diff": float
}
```

Images are always handled as RGB `uint8` NumPy arrays of shape (H, W, 3). Output is always PNG.

## Team workflow

1. Never commit directly to `main`. Work on your own branch: `khadija/core`, `ayesha/analysis`.
2. Commit small and often. Pull `main` before you start each day: `git pull origin main`.
3. Open a Pull Request on GitHub, the other person reviews and merges.
4. Only edit files you own. If you need a change in the other person's file, message them.

See `TASKS.md` for the full task split and timeline.
