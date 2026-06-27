# Release Process

This document outlines the steps for releasing a new version of EnterpriseIQ.

## Steps
1. Update the `CHANGELOG.md` with the new version and details.
2. Bump the version in `pyproject.toml` and `src/api/main.py`.
3. Create a git tag matching the version (e.g., `v1.0.0`).
4. Push the commit and the tag to the repository.
5. Create a GitHub Release referencing the tag and pasting the changelog notes.

For detailed instructions, refer to `RELEASE.md` in the repository root.
