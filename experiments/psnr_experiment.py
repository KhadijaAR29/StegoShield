"""
psnr_experiment.py  --  OWNER: Khadija
Measures image quality (MSE, PSNR) and speed for the embedding code.

For every cover image in data/cover_images/, in both modes (sequential, random),
at 10%, 25% and 50% of the image's capacity, it:
    1. hides a message of that size (embed_message),
    2. measures MSE and PSNR between the cover and the stego image,
    3. times embed and extract, and checks that extract returns the same message.

Run from the project root:
    python experiments/psnr_experiment.py

Writes to results/:
    psnr_results.csv    one row per (image, mode, size)
    psnr_summary.csv    averages per (mode, size)
    psnr_vs_size.png    graph of average PSNR against message size
"""

import csv
import glob
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from stego import crypto, utils
from stego.embed import embed_message
from stego.extract import extract_message
from stego.metrics import mse, psnr

SIZES = [0.10, 0.25, 0.50]
MODES = ["sequential", "random"]
PASSWORD = "87654321"
OVERHEAD_BYTES = crypto.SALT_SIZE + crypto.NONCE_SIZE + crypto.TAG_SIZE  # 44

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER_DIR = os.path.join(ROOT, "data", "cover_images")
RESULTS_DIR = os.path.join(ROOT, "results")


def message_for_fraction(capacity_bits: int, fraction: float) -> str:
    """A text message that fills about `fraction` of the image capacity."""
    target_bits = int(capacity_bits * fraction)
    payload_bytes = (target_bits - utils.HEADER_BITS) // 8
    return "A" * (payload_bytes - OVERHEAD_BYTES)


def run():
    covers = sorted(glob.glob(os.path.join(COVER_DIR, "*.png")))
    if not covers:
        sys.exit("No PNG files found in data/cover_images/")

    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for cover_path in covers:
            name = os.path.splitext(os.path.basename(cover_path))[0]
            cover = np.array(Image.open(cover_path).convert("RGB"), dtype=np.uint8)
            h, w, _ = cover.shape
            capacity = utils.capacity_bits(cover)

            for mode in MODES:
                for fraction in SIZES:
                    message = message_for_fraction(capacity, fraction)
                    out_path = os.path.join(tmp, "stego.png")

                    t0 = time.perf_counter()
                    info = embed_message(cover_path, out_path, message, PASSWORD, mode)
                    embed_s = time.perf_counter() - t0

                    t0 = time.perf_counter()
                    recovered = extract_message(out_path, PASSWORD, mode)
                    extract_s = time.perf_counter() - t0

                    stego = np.array(Image.open(out_path).convert("RGB"), dtype=np.uint8)
                    rows.append({
                        "image": name,
                        "width": w,
                        "height": h,
                        "mode": mode,
                        "target_size": f"{int(fraction * 100)}%",
                        "capacity_bits": info["capacity_bits"],
                        "used_bits": info["used_bits"],
                        "used_percent": round(100 * info["used_bits"] / info["capacity_bits"], 2),
                        "mse": round(mse(cover, stego), 6),
                        "psnr_db": round(psnr(cover, stego), 2),
                        "embed_seconds": round(embed_s, 3),
                        "extract_seconds": round(extract_s, 3),
                        "extract_ok": recovered == message,
                    })
            print(f"done: {name} ({w}x{h})")
    return rows


def summarise(rows):
    summary = []
    for mode in MODES:
        for fraction in SIZES:
            label = f"{int(fraction * 100)}%"
            sel = [r for r in rows if r["mode"] == mode and r["target_size"] == label]
            summary.append({
                "mode": mode,
                "target_size": label,
                "images": len(sel),
                "mean_mse": round(float(np.mean([r["mse"] for r in sel])), 4),
                "mean_psnr_db": round(float(np.mean([r["psnr_db"] for r in sel])), 2),
                "min_psnr_db": round(float(np.min([r["psnr_db"] for r in sel])), 2),
                "mean_embed_seconds": round(float(np.mean([r["embed_seconds"] for r in sel])), 3),
                "mean_extract_seconds": round(float(np.mean([r["extract_seconds"] for r in sel])), 3),
                "all_extracts_ok": all(r["extract_ok"] for r in sel),
            })
    return summary


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot(summary, path):
    labels = [f"{int(s * 100)}%" for s in SIZES]
    blue, orange = "#257de0", "#f47230"
    ink, quiet, grid = "#191919", "#666666", "#e6e6e6"

    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for mode, colour, marker, size in [("sequential", blue, "o", 9), ("random", orange, "s", 5)]:
        ys = [next(s["mean_psnr_db"] for s in summary if s["mode"] == mode and s["target_size"] == lab)
              for lab in labels]
        ax.plot(labels, ys, color=colour, linewidth=2, marker=marker, markersize=size,
                markeredgecolor="white", markeredgewidth=1.5, label=mode.capitalize())
        if mode == "sequential":
            for x, y in zip(labels, ys):
                ax.annotate(f"{y:.1f} dB", (x, y), textcoords="offset points", xytext=(0, 10),
                            ha="center", fontsize=9, color=ink)

    ax.set_ylim(40, 70)
    ax.set_xlabel("Message size (% of image capacity)", color=quiet)
    ax.set_ylabel("Average PSNR (dB), higher = less change", color=quiet)
    ax.set_title("Hiding up to half the image still keeps PSNR above 50 dB", loc="left",
                 fontsize=12, fontweight="bold", color=ink)
    ax.grid(axis="y", color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(grid)
    ax.tick_params(colors=quiet)
    ax.legend(frameon=False, loc="lower left", labelcolor=ink)
    ax.text(0.99, 0.04, "The two modes overlap: both change the same number of values.",
            transform=ax.transAxes, ha="right", fontsize=8.5, color=quiet)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = run()
    summary = summarise(rows)
    write_csv(os.path.join(RESULTS_DIR, "psnr_results.csv"), rows)
    write_csv(os.path.join(RESULTS_DIR, "psnr_summary.csv"), summary)
    plot(summary, os.path.join(RESULTS_DIR, "psnr_vs_size.png"))
    print()
    for s in summary:
        print(s)
    print("\nSaved psnr_results.csv, psnr_summary.csv and psnr_vs_size.png to results/")