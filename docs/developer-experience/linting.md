# Linting

We use `ruff` for fast and comprehensive code linting. It replaces Flake8, isort, and pylint.

## Running the Linter
To identify issues:
```bash
ruff check .
```

To attempt automatic fixes for certain rules (like import sorting):
```bash
ruff check --fix .
```

## Rules
Our base configuration (in `pyproject.toml`) selects standard error (`E`), fatal (`F`), import (`I`), and bug-bear (`B`) rules.
