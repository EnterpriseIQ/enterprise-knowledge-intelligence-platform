"""Chunking layer.

Splits document text into overlapping, sentence-aware character windows. Overlap
preserves context across boundaries so answers are not truncated mid-thought.
Page markers (``[[page=N]]``) emitted by the PDF loader are consumed here and
turned into structured ``page`` metadata for citations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from src import config
from src.ingestion.document_loader import RawDocument

_PAGE_RE = re.compile(r"\[\[page=(\d+)\]\]")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict  # carries doc security metadata + page + chunk_index


def _split_with_pages(text: str) -> list[tuple[str, int | None]]:
    """Return (segment, page) pairs, tracking the current page marker."""
    segments: list[tuple[str, int | None]] = []
    current_page: int | None = None
    pos = 0
    for m in _PAGE_RE.finditer(text):
        if m.start() > pos:
            segments.append((text[pos:m.start()], current_page))
        current_page = int(m.group(1))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], current_page))
    return segments or [(text, None)]


def _window(text: str, size: int, overlap: int) -> list[str]:
    """Sentence-aware sliding window over a single-page text segment."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    sentences = _SENT_SPLIT.split(text)
    chunks: list[str] = []
    buf = ""
    for sent in sentences:
        if len(buf) + len(sent) + 1 <= size:
            buf = f"{buf} {sent}".strip()
        else:
            if buf:
                chunks.append(buf)
            # start new buffer with tail overlap from previous chunk
            tail = buf[-overlap:] if overlap and buf else ""
            buf = f"{tail} {sent}".strip()
            # very long single sentences are hard-split
            while len(buf) > size:
                chunks.append(buf[:size])
                buf = buf[size - overlap:]
    if buf:
        chunks.append(buf)
    return chunks


def chunk_documents(docs: list[RawDocument],
                    size: int | None = None,
                    overlap: int | None = None) -> list[Chunk]:
    size = size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    out: list[Chunk] = []
    for doc in docs:
        base_meta = doc.metadata()
        idx = 0
        for segment, page in _split_with_pages(doc.text):
            for piece in _window(segment, size, overlap):
                meta = dict(base_meta)
                meta["page"] = page if page is not None else 0
                meta["chunk_index"] = idx
                out.append(Chunk(chunk_id=f"{doc.doc_id}::{idx}", text=piece, metadata=meta))
                idx += 1
    return out
