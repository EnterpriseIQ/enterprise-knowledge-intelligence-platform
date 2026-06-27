# Release Process

This document outlines the steps for releasing a new version of EnterpriseIQ.

## Versioning Scheme

We follow [Semantic Versioning](https://semver.org/).
- **MAJOR** version for incompatible API changes or architectural shifts.
- **MINOR** version for adding functionality in a backwards compatible manner.
- **PATCH** version for backwards compatible bug fixes.

## Release Steps

1. **Update Changelog**: Ensure `CHANGELOG.md` is updated with all notable changes for the upcoming release under the new version header.
2. **Update Version**: Update the version number in `pyproject.toml` and `src/api/main.py`. If releasing frontend updates, also update `website/package.json`.
3. **Commit Version Bump**: Commit these changes with the message `chore: bump version to X.Y.Z`.
4. **Create a Tag**: Create a git tag for the version: `git tag vX.Y.Z`.
5. **Push**: Push the commit and the tag to GitHub: `git push origin main && git push origin vX.Y.Z`.
6. **GitHub Release**: Go to the GitHub Releases page, create a new release from the pushed tag. Copy the contents from `CHANGELOG.md` for this version into the release description.
7. **Verify Deployments**: Ensure CI pipelines (e.g., Docker build, GitHub Pages) trigger and complete successfully based on the tag.
