# GitHub Actions

This repository utilizes GitHub Actions to automate testing and deployment.

## Active Workflows
1. **CI Pipeline (`.github/workflows/ci.yml`)**: Runs on pull requests and pushes to `main`. It sets up Python, installs dependencies, lints with `ruff`, runs `pytest`, and builds the Docker image.
2. **Deploy Pages (`.github/workflows/deploy-pages.yml`)**: Triggers on pushes to `main` (or specific tags) to build the Vite/React frontend using `pnpm` and deploys it to GitHub Pages.

## Secrets
Certain actions may require repository secrets (like `DOCKERHUB_TOKEN` or `ANTHROPIC_API_KEY` for advanced tests). Ensure these are configured in the GitHub repository settings.
