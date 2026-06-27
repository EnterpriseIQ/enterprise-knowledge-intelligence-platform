# Maintenance

Routine maintenance tasks for EnterpriseIQ.

## Updating the Knowledge Base
When new PDFs, SQL dumps, or logs are added to the enterprise:
1. Place them in the appropriate `data/` subfolder.
2. Run the ingestion pipeline. Currently, this requires rebuilding the index, but future updates will support incremental additions.

## Updating Dependencies
Regularly update Python dependencies to ensure security patches are applied.
```bash
pip install --upgrade -r requirements.txt
```
If using Docker, rebuild the image periodically to pull in base OS security updates.
