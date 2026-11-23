"""
app.py  --  OWNER: Khadija
Streamlit GUI with three tabs: Embed | Extract | Detect.

Run from the project root:
    streamlit run gui/app.py
"""

import os
import sys
import tempfile

# make `stego` and `analysis` importable when running `streamlit run gui/app.py`
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import streamlit as st
from PIL import Image

from analysis.detector import detect
from stego.embed import embed_message
from stego.extract import extract_message
from stego.metrics import mse, psnr

st.set_page_config(page_title="StegoShield", page_icon="🛡️")
st.title("🛡️ StegoShield")
st.caption("AES-256 encrypted image steganography with hidden-data detection")


def save_upload(uploaded_file, folder: str) -> str:
    """Write an uploaded file to disk and return its path."""
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


tab_embed, tab_extract, tab_detect = st.tabs(["Embed", "Extract", "Detect"])

# ---------------------------------------------------------------- Embed
with tab_embed:
    st.subheader("Hide a message in an image")
    cover_file = st.file_uploader("Cover image (PNG)", type=["png"], key="embed_cover")
    message = st.text_area("Secret message", key="embed_msg")
    password = st.text_input("Password", type="password", key="embed_pw")
    mode = st.radio("Embedding mode", ["random", "sequential"], horizontal=True, key="embed_mode")

    if st.button("Embed message"):
        if not cover_file or not message or not password:
            st.warning("Please provide a cover image, a message and a password.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    cover_path = save_upload(cover_file, tmp)
                    out_path = os.path.join(tmp, "stego_" + os.path.splitext(cover_file.name)[0] + ".png")
                    info = embed_message(cover_path, out_path, message, password, mode)

                    cover_arr = np.array(Image.open(cover_path).convert("RGB"))
                    stego_arr = np.array(Image.open(out_path).convert("RGB"))
                    with open(out_path, "rb") as f:
                        stego_bytes = f.read()

                st.success("Message hidden successfully.")
                col1, col2 = st.columns(2)
                col1.image(cover_arr, caption="Original")
                col2.image(stego_arr, caption="Stego image")

                m1, m2, m3 = st.columns(3)
                m1.metric("PSNR (dB)", f"{psnr(cover_arr, stego_arr):.2f}")
                m2.metric("MSE", f"{mse(cover_arr, stego_arr):.5f}")
                m3.metric("Capacity used", f"{100 * info['used_bits'] / info['capacity_bits']:.2f}%")

                st.download_button("Download stego image", stego_bytes,
                                   file_name="stego_image.png", mime="image/png")
            except ValueError as e:
                st.error(str(e))

# -------------------------------------------------------------- Extract
with tab_extract:
    st.subheader("Extract a hidden message")
    stego_file = st.file_uploader("Stego image (PNG)", type=["png"], key="extract_file")
    password_x = st.text_input("Password", type="password", key="extract_pw")
    mode_x = st.radio("Embedding mode", ["random", "sequential"], horizontal=True, key="extract_mode")

    if st.button("Extract message"):
        if not stego_file or not password_x:
            st.warning("Please provide a stego image and a password.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    path = save_upload(stego_file, tmp)
                    secret = extract_message(path, password_x, mode_x)
                st.success("Message extracted.")
                st.text_area("Hidden message", secret, height=150)
            except ValueError as e:
                st.error(str(e))

# --------------------------------------------------------------- Detect
with tab_detect:
    st.subheader("Check if an image likely contains hidden data")
    image_file = st.file_uploader("Image (PNG)", type=["png"], key="detect_file")

    if st.button("Run detection"):
        if not image_file:
            st.warning("Please upload an image.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    path = save_upload(image_file, tmp)
                    result = detect(path)

                if result["likely_hidden"]:
                    st.error(f"Likely hidden data: YES (confidence {result['confidence']:.0%})")
                else:
                    st.success(f"Likely hidden data: NO (confidence {result['confidence']:.0%})")

                c1, c2, c3 = st.columns(3)
                c1.metric("Chi-square p-value", f"{result['chi_square_p']:.4f}")
                c2.metric("LSB ratio", f"{result['lsb_ratio']:.4f}")
                c3.metric("Pair difference", f"{result['pair_diff']:.4f}")
            except NotImplementedError:
                st.info("The detector is not implemented yet.")