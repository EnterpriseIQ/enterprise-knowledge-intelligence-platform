# Contributing to EnterpriseIQ

First off, thank you for considering contributing to EnterpriseIQ! It's people like you that make open source such a fantastic community.

## 1. Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional, for testing container builds)
- Node.js & pnpm (if contributing to the frontend website)

### Development Setup
1. Fork the repo and clone your fork.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -e ".[dev,llm]"`
4. Run tests to ensure everything is working: `python -m pytest`

## 2. Development Workflow

1. **Create a branch** for your feature or bugfix: `git checkout -b feature/your-feature-name`
2. **Write code**, ensuring you follow our [Coding Conventions](docs/developer-experience/coding-conventions.md).
3. **Write tests** for your changes. We strive for high test coverage, especially around RBAC and retrieval logic.
4. **Format and Lint**: Run `ruff format .` and `ruff check .` to ensure your code meets our styling guidelines.
5. **Commit your changes**: Use descriptive commit messages.

## 3. Pull Request Process

1. Push your branch to your fork.
2. Open a Pull Request against the `main` branch of the upstream repository.
3. Fill out the PR template completely.
4. Ensure all CI checks pass.
5. Address any feedback from reviewers.

## 4. Reporting Bugs

Use the Bug Report issue template. Provide as much context as possible, including:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Logs or error traces
- Environment details (Python version, OS, etc.)

## 5. Feature Requests

Use the Feature Request issue template. Clearly describe the problem you are trying to solve and your proposed solution.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
