"""Document processing layer: chunking and embedding."""
from src.processing.chunker import chunk_documents
from src.processing.embedder import Embedder

__all__ = ["chunk_documents", "Embedder"]
