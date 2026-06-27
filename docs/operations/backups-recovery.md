# Backups and Recovery

## What to Backup
The application code is stateless, but the data is not. You must backup:
1. **Raw Documents:** The source files (PDFs, SQL, JSON).
2. **Configuration:** `.env` files and `data/rbac/access_policies.json`.
3. **Index Volume:** The ChromaDB storage directory (usually mapped to `/app/data` in Docker).

## Recovery Process
If the ChromaDB index is corrupted:
1. Delete the corrupted index folder.
2. Ensure your raw documents are in the correct `data/` subfolders.
3. Re-run `python -m data.generate_data` to rebuild the index from scratch.

*Because the chunking and embedding processes are deterministic, regenerating the index will result in the exact same state.*
