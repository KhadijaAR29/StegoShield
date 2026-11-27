# Task Split

Two independent parts that meet at the shared interface in README.md.
Ayesha tests the detector with `tests/helpers.py` (fake stego images), so she does not
have to wait for Khadija's embed code.

## Khadija: Hiding side (core + interface)

- [x] `stego/crypto.py`: PBKDF2 key + AES-GCM encrypt/decrypt, reject wrong password
- [x] `stego/utils.py`: bytes<->bits, 32-bit length header, capacity check
- [x] `stego/embed.py`: LSB embed, `sequential` and `random` modes (password-seeded)
- [x] `stego/extract.py`: read header, read bits, decrypt
- [x] `stego/metrics.py`: PSNR and MSE
- [x] `main.py`: command-line interface
- [x] Tests: `test_crypto.py`, `test_embed_extract.py` all passing
- [x] `gui/app.py`: Embed / Extract / Detect tabs (after core works)
- [x] `experiments/psnr_experiment.py`: MSE, PSNR and speed at 10%, 25%, 50% of capacity

## Ayesha: Detection side (steganalysis + experiments)

- [x] Collect 10-20 cover PNGs of different sizes/types into `data/cover_images/`
- [x] `analysis/chi_square.py`: chi-square pairs test
- [x] `analysis/histogram.py`: LSB ratio, pair difference, histogram plots
- [x] `analysis/detector.py`: combine tests, choose thresholds, return the dict from README
- [x] Tests: `test_detector.py` passing
- [x] `notebooks/analysis.ipynb`: detection accuracy on clean vs stego, sequential vs random, different message lengths
- [x] Graphs and tables into `results/`

## Shared

- [x] Integration: once both parts are merged, generate real stego images with `embed_message` and rerun the notebook
- [x] `docs/architecture.png`: embed / extract / detect flow diagram
- [x] Documentation: architecture document and security analysis document

## Timeline suggestion

| Week | Khadija | Ayesha |
|---|---|---|
| 1 | crypto, utils, sequential embed/extract | cover images, chi-square, histogram |
| 2 | random mode, metrics, CLI, tests | detector + thresholds, tests |
| 3 | GUI | notebook experiments + graphs |
| 4 | integration, diagram, report | integration, report |

## Experiment note for the notebook

Run detection on clean images, sequential stego, and random stego at several message
sizes (for example 10%, 25%, 50% of capacity). The chi-square test should catch
sequential embedding easily and struggle more with random embedding on short
messages. That result is exactly what your evaluation section needs to show.
