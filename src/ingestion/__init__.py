"""Data ingestion layer.

Loaders turn heterogeneous raw sources (PDF, CSV, SQL, JSON) into a common
``RawDocument`` representation carrying the text plus security/provenance
metadata inherited from the dataset manifest.
"""
from src.ingestion.document_loader import RawDocument, load_corpus

__all__ = ["RawDocument", "load_corpus"]
