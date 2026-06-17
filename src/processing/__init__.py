"""Document processing layer: chunking and embedding."""

from src.processing.chunker import Chunk, chunk_documents
from src.processing.embedder import Embedder

__all__ = ["Chunk", "chunk_documents", "Embedder"]
