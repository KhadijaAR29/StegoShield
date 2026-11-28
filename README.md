# StegoShield

Secure image steganography with AES-256 encryption and hidden-data detection.
FAST-NUCES Lahore, Fall 2026. Authors: Khadija A-Rahim (23L-1008), Ayesha Arshad (23L-2596).

StegoShield hides a secret text message inside a PNG image. The message is first
encrypted with AES-256-GCM, then stored in the least significant bits (LSB) of the pixel
values, either in order (`sequential`) or in a password-seeded random order (`random`).
It can extract the message again, and it can check whether an image probably contains
hidden LSB data (chi-square and histogram analysis).

## Requirements

- Python 3 (we used Python 3.15; any recent Python 3 should work)
- The packages in `requirements.txt`
- PNG images only (JPEG compression destroys the hidden bits)

## Setup

```powershell
git clone https://github.com/KhadijaAR29/StegoShield.git
cd StegoShield
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
```

If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope Process Bypass`
first and activate again.

## Run

All commands are run from the project folder with the virtual environment active.

### Command line

```powershell
python main.py embed   data/cover_images/astronaut.png data/stego_images/stego_image.png "Happy Birthday" 87654321 --mode random
python main.py extract data/stego_images/stego_image.png 87654321 --mode random
python main.py detect  data/stego_images/stego_image.png
```

- `embed` takes: cover image, output image, message, password, and `--mode random` or
  `--mode sequential` (default is `random`).
- `extract` needs the same password and the same mode that were used to embed.
  A wrong password or wrong mode gives an error.
- `detect` prints `likely_hidden` (True or False), a confidence value and the test scores.

To see a detection result of True, hide a long message in sequential mode:

```powershell
$msg = "A" * 20000
python main.py embed data/cover_images/astronaut.png data/stego_images/big_stego.png $msg 87654321 --mode sequential
python main.py detect data/stego_images/big_stego.png
python main.py detect data/cover_images/astronaut.png
```

The second `detect` runs on the clean image and should print `likely_hidden: False`.
Short messages hidden in random mode are usually not detected. This is expected.

### Graphical interface

```powershell
streamlit run gui/app.py
```

A browser tab opens with three tabs: **Embed**, **Extract** and **Detect**.

If the app does not open on your computer, run it in Google Colab instead:

1. Open `notebooks/run_in_colab.ipynb` in Google Colab.
2. Run the cells in order: upload and unzip, install packages, tests, then the Cloudflare cell.
3. Keep the Cloudflare cell last, because it runs until you stop it.
4. Open the `trycloudflare.com` link it prints. The app opens with the Embed, Extract and Detect tabs.

### Tests

```powershell
pytest
```

All 10 tests should pass.

### Experiments

```powershell
python experiments/psnr_experiment.py
```

Measures MSE, PSNR and speed on every image in `data/cover_images/` in both modes at 10%,
25% and 50% of capacity. It writes `psnr_results.csv`, `psnr_summary.csv` and
`psnr_vs_size.png` to `results/`.

The detection experiments are in `notebooks/analysis.ipynb`. Open it with
`jupyter notebook notebooks/analysis.ipynb` and run all cells.

## Project structure

| Folder or file | What is inside | Owner |
|---|---|---|
| `stego/` | crypto, bit utils, embed, extract, PSNR/MSE | Khadija |
| `analysis/` | chi-square, histogram, detector | Ayesha |
| `gui/` | Streamlit interface | Khadija |
| `main.py` | command-line interface | Khadija |
| `experiments/` | PSNR/MSE and speed experiment | Khadija |
| `notebooks/` | detection experiments and graphs | Ayesha |
| `tests/` | unit tests | each owner tests their own part |
| `data/` | cover images and generated stego images | Ayesha collects covers |
| `results/` | graphs and tables from the experiments | shared |
| `docs/` | proposal and architecture diagram | shared |

## How it works

1. **Embed:** the password and a random salt give an AES key (PBKDF2-HMAC-SHA256, 200,000
   rounds). The message is encrypted with AES-256-GCM. A 32-bit length header is added.
   The bits are written into the last bit of chosen pixel values and saved as PNG.
2. **Extract:** the same positions are rebuilt from the password and mode, the header
   and payload are read, and AES-GCM decrypts them. A wrong password or damaged data is
   rejected.
3. **Detect:** chi-square tests on pairs of pixel values and a pair-difference score are
   combined into one yes/no answer.

## Results

Measured on 20 cover images (see `results/`):

| Message size (% of capacity) | PSNR (dB) | Sequential detected | Random detected |
|---|---|---|---|
| 10% | 61.14 | 75% | 5% |
| 25% | 57.16 | 80% | 10% |
| 50% | 54.15 | 95% | 70% |

PSNR is the same in both modes. No clean image was flagged, but the detector was tuned on
the same 20 images, so this is not an independent measurement.

## Limits

- Only lossless PNG works. JPEG, resizing or editing the stego image destroys the message.
- The mode is not stored in the image. The receiver must know it.
- Capacity is about 98,000 characters for a 512 x 512 image.
- Detection is statistical. It gives a likelihood, not proof.

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

See `TASKS.md` for the task split.
