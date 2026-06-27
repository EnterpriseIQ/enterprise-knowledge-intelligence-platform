# CI/CD Pipeline

Our Continuous Integration is driven by GitHub Actions.

## Workflows
1. **Lint and Test:** Triggered on every pull request to `main`.
   - Runs `ruff format --check` and `ruff check`.
   - Runs the full `pytest` suite across Python 3.10, 3.11, and 3.12.
2. **Docker Build:** Validates that the `Dockerfile` can build successfully.
3. **GitHub Pages (Docs):** Builds and deploys the React frontend from `website/` using `pnpm`.

## Local Verification
Before pushing, ensure you run the pre-commit checks locally:
```bash
ruff format .
ruff check .
python -m pytest
```
