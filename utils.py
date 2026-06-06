"""
Utility functions for the Enterprise Policy QA Agent.
Shared by ingest.py and app.py.
"""

import os


try:
    import pdfplumber
except ImportError:
    pdfplumber = None


# -------------------------------------------------------------------
# Text chunking
# -------------------------------------------------------------------

def chunk_text(text: str, size: int = 400, overlap: int = 50):
    """
    Split text into overlapping chunks (word-based).
    Args:
        text: full text string
        size: number of words per chunk
        overlap: number of overlapping words between chunks
    Yields:
        chunk strings
    """
    words = text.split()
    start = 0

    while start < len(words):
        end = start + size
        yield " ".join(words[start:end])
        start = end - overlap if end - overlap > start else end


# -------------------------------------------------------------------
# File reading
# -------------------------------------------------------------------

def read_txt(path: str):
    """
    Read a .txt file and return text.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(path: str):
    """
    Read a PDF file and return a list of (text, metadata) tuples.
    Metadata: {'page': page_number, 'section': 'page'}
    """
    if not pdfplumber:
        raise RuntimeError("pdfplumber not installed. Run: pip install pdfplumber")

    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages.append((text, {"page": i, "section": "page"}))
    return pages


# -------------------------------------------------------------------
# Confidence helper
# -------------------------------------------------------------------

def calculate_confidence(distance: float):
    """
    Convert similarity distance into a confidence score (0-1).
    """
    return round(1.0 - distance, 2)


# -------------------------------------------------------------------
# Safe filename helper
# -------------------------------------------------------------------

def safe_filename(path: str):
    """
    Extract the filename from a path safely.
    """
    return os.path.basename(path)
