# Coding Conventions

To keep the codebase maintainable and readable, we strictly adhere to the following conventions:

## Python Style
- **Type Hints:** Required for all function signatures and class properties. We use modern Python typing (`list[str]` instead of `List[str]`, `str | None` instead of `Optional[str]`).
- **Docstrings:** All public modules, classes, and methods must have a docstring. We loosely follow Google/Sphinx style.
- **Line Length:** Kept to 100 characters via `ruff`.

## Imports
- Standard library imports first.
- Third-party imports second.
- Local application imports (`src.*`) third.

## Security Practices
- Do not use `==` for comparing secrets or tokens; use `secrets.compare_digest`.
- If using `zip()`, explicitly declare `strict=True` or `strict=False` to comply with Ruff B905.
