from pathlib import Path

from src.ingestion.sql_loader import load_sql

# Try to find a way to inject
print(load_sql(Path("data/structured/operations.db")))
