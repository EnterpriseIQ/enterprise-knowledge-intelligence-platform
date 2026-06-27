# Branch Strategy

We follow a standard GitHub Flow model.

- **`main` branch:** The single source of truth. It must always be deployable.
- **Feature Branches:** Create a branch for every new feature or bug fix. Use descriptive names like `feature/add-azure-ad-auth` or `bugfix/fix-rbac-leak`.
- **Pull Requests:** All changes must be merged into `main` via a Pull Request. PRs require a review from a core maintainer and passing CI checks.
