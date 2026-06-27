# Testing Strategy

EnterpriseIQ relies heavily on automated testing to ensure the RBAC engine never leaks data.

## Running Tests
To run the full suite:
```bash
python -m pytest
```

## Test Structure
- `tests/rbac/`: Critical security tests validating that access policies are enforced correctly.
- `tests/retrieval/`: Validates hybrid fusion scoring and router logic.
- `tests/api/`: Integration tests using `FastAPI.testclient` to mock HTTP requests to the endpoints.

## Adding Tests
When writing a bug fix, always include a regression test that fails without the fix. For security patches, explicitly document the threat model scenario the test covers.
