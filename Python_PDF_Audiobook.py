"""
Simple PDF -> audiobook script (minimal improvements and diagnostics).

Notes / fixes applied:
- Print a clear message and exit if required packages are missing.
- Use modern PyPDF2 PdfReader when available, fall back to PdfFileReader.
- Extract text from all pages (not only page 0).
- Use a valid volume value (0.0-1.0) instead of 200.
- Save to WAV (more portable with pyttsx3 backends) and name output after the PDF.
"""
import sys
import os

try:
    import pyttsx3
except ImportError:
    print("Missing dependency: pyttsx3. Install with: pip install pyttsx3")
    sys.exit(1)

try:
    import PyPDF2
except ImportError:
    print("Missing dependency: PyPDF2. Install with: pip install PyPDF2")
    sys.exit(1)


def main(pdf_path=None):
    if pdf_path is None:
        pdf_path = r"C:\Users\aalbo\OneDrive\Desktop\Python PDF to Audiobook\SOFTWARE PARA EDICIONES DE TEXTO.pdf"
    # allow overriding via command line
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return 1

    # Try modern PdfReader first (PyPDF2 >= 2.x), fallback to PdfFileReader
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(pdf_path)
        number_of_pages = len(reader.pages)

        def get_page_text(i):
            text = reader.pages[i].extract_text()
            return text or ""

    except Exception:
        # fallback for older PyPDF2
        pdf_file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfFileReader(pdf_file, strict=False)
        number_of_pages = reader.getNumPages()

        def get_page_text(i):
            return reader.getPage(i).extractText() or ""

    engine = pyttsx3.init()

    # set a sensible speaking rate and volume
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)  # valid range: 0.0 to 1.0

    voices = engine.getProperty('voices')
    # choose a female voice if available, else the first voice
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    elif voices:
        engine.setProperty('voice', voices[0].id)

    texts = []
    for i in range(number_of_pages):
        print(f"Extracting page {i+1}/{number_of_pages}...")
        t = get_page_text(i)
        if t.strip():
            texts.append(t)
        else:
            print(f"Warning: page {i+1} returned no text (may be scanned or image-based).")

    if not texts:
        print("No text extracted from PDF. The document may be scanned or encrypted. Try OCR or a different PDF.")
        return 1

    full_text = "\n\n".join(texts)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    out_file = base_name + "_audio.wav"

    print(f"Saving audio to {out_file} ...")
    engine.save_to_file(full_text, out_file)
    engine.runAndWait()
    engine.stop()

    print("Done.")
    return 0


if __name__ == '__main__':
    sys.exit(main())