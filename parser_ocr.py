import os
import tempfile
from pdfminer.high_level import extract_text
import pytesseract
from pdf2image import convert_from_path
from logger import logger


def extract_text_smart(pdf_path, max_pages=3):
    """
    Try parsing first; if fails or empty, fallback to OCR.
    Returns (text, source)
    """
    try:
        # Attempt parsing
        text = extract_text(pdf_path, maxpages=max_pages)
        if text and text.strip():
            logger.info(f"Parsed text from {pdf_path}")
            full_text = extract_text(pdf_path)  # full doc
            return full_text, 'parsed'
    except Exception as e:
        logger.warning(f"Parsing failed for {pdf_path}: {e}")
    
    # Fallback to OCR
    logger.info(f"Falling back to OCR for {pdf_path}")
    pages = convert_from_path(pdf_path)
    ocr_text = []
    for page in pages:
        txt = pytesseract.image_to_string(page)
        ocr_text.append(txt)
    return "\n".join(ocr_text), 'ocr'