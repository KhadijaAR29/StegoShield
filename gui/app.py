"""
app.py  --  OWNER: Khadija
Simple GUI with three tabs: Embed | Extract | Detect.
Streamlit (run: streamlit run gui/app.py) or Tkinter - decide once the core works.

It only calls these functions (the shared interface, see README):
    stego.embed.embed_message(cover_path, out_path, message, password, mode)
    stego.extract.extract_message(stego_path, password, mode)
    analysis.detector.detect(image_path)
    stego.metrics.psnr / mse
"""

if __name__ == "__main__":
    raise NotImplementedError
