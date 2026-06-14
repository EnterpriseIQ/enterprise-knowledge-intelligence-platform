"""PDF ingestion.

Extracts text from PDF documents using ``pypdf``. Page boundaries are preserved
as lightweight markers so that the chunker and citation engine can report the
page a passage came from.
"""
from __future__ import annotations

from pathlib import Path


def load_pdf(path: Path) -> str:
    """Return the full text of a PDF with per-page markers.

    Each page is prefixed with ``[[page=N]]`` which the chunker uses to attribute
    a chunk to a page number for citations.
    """
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    parts: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            parts.append(f"[[page={i}]]\n{text}")
    return "\n\n".join(parts)
