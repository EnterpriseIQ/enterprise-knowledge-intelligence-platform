# Contributing to EnterpriseIQ

First off, thank you for considering contributing to EnterpriseIQ! It's people like you that make EnterpriseIQ such a great platform for secure, offline-first enterprise RAG.

## Code of Conduct

This project and everyone participating in it is governed by the [EnterpriseIQ Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs
This section guides you through submitting a bug report for EnterpriseIQ.
- Check the [FAQ](docs/FAQ.md) and [Troubleshooting Guide](docs/operations/troubleshooting.md) first.
- Use the Bug Report issue template to report the issue.
- Provide a clear, reproducible example if possible.

### Suggesting Enhancements
- Use the Feature Request issue template.
- Clearly describe the problem you are trying to solve and how the enhancement helps.

### Submitting Pull Requests
1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes (`python -m pytest`).
4. Format your code with `ruff format` and lint with `ruff check`.
5. Issue that pull request!

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform.git
   cd enterprise-knowledge-intelligence-platform
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies (including dev tools):**
   ```bash
   pip install -e ".[dev,llm]"
   ```

4. **Run tests:**
   ```bash
   python -m pytest
   ```

## Development Workflow
EnterpriseIQ uses strict PR reviews. All commits must be signed, and all tests/linters must pass before a review is assigned.

## Documentation
Documentation improvements are always welcome. Documentation is located in the `docs/` directory and written in Markdown. We use standard Mermaid.js for diagrams.
