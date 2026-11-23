# Task Split

Two independent parts that meet at the shared interface in README.md.
Ayesha tests the detector with `tests/helpers.py` (fake stego images), so she does not
have to wait for Khadija's embed code.

## Khadija: Hiding side (core + interface)

- [ ] `stego/crypto.py`: PBKDF2 key + AES-GCM encrypt/decrypt, reject wrong password
- [ ] `stego/utils.py`: bytes<->bits, 32-bit length header, capacity check
- [ ] `stego/embed.py`: LSB embed, `sequential` and `random` modes (password-seeded)
- [ ] `stego/extract.py`: read header, read bits, decrypt
- [ ] `stego/metrics.py`: PSNR and MSE
- [ ] `main.py`: command-line interface
- [ ] Tests: `test_crypto.py`, `test_embed_extract.py` all passing
- [ ] `gui/app.py`: Embed / Extract / Detect tabs (after core works)

## Ayesha: Detection side (steganalysis + experiments)

- [ ] Collect 10-20 cover PNGs of different sizes/types into `data/cover_images/`
- [ ] `analysis/chi_square.py`: chi-square pairs test
- [ ] `analysis/histogram.py`: LSB ratio, pair difference, histogram plots
- [ ] `analysis/detector.py`: combine tests, choose thresholds, return the dict from README
- [ ] Tests: `test_detector.py` passing
- [ ] `notebooks/analysis.ipynb`: detection accuracy on clean vs stego, sequential vs random, different message lengths
- [ ] Graphs and tables into `results/`

## Shared

- [ ] Integration: once both parts are merged, generate real stego images with `embed_message` and rerun the notebook
- [ ] `docs/architecture.png`: embed / extract / detect flow diagram (Khadija draws, Ayesha reviews)
- [ ] `docs/report.pdf`: Khadija writes sections on crypto, embedding, GUI, PSNR/MSE. Ayesha writes steganalysis, experiments, results. Both write the security analysis (LSB weakness against JPEG/resize, limits of detection).

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
