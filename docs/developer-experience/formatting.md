# Formatting

We use `ruff` as our unified formatter. It replaces Black and is significantly faster.

## Configuration
The `ruff` configuration is defined in `pyproject.toml`.
- Line length is set to 100 characters.

## Applying Formatting
To auto-format your code:
```bash
ruff format .
```
To check if your code is formatted correctly (used in CI):
```bash
ruff format --check .
```
