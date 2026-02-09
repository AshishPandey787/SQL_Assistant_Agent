# Optional OCR for scanned PDFs
# Requires: pytesseract, pdf2image, Pillow, and system deps for poppler+tesseract.

from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(path: str, dpi: int = 250) -> str:
    images = convert_from_path(path, dpi=dpi)
    text = []
    for img in images:
        text.append(pytesseract.image_to_string(img))
    return "\n".join(text).strip()