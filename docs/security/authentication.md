# Authentication

Authentication in EnterpriseIQ ensures that only verified clients can interact with the API endpoints.

## API Key Authentication

The primary mechanism is a static API Key.
- Configure this by setting the `API_KEY` environment variable.
- Clients must pass this key in the `X-API-Key` HTTP header.
- The comparison uses `secrets.compare_digest` to prevent timing attacks.

## Future Extensibility
For enterprise deployments, the API key middleware (`src/api/auth.py`) is designed to be easily swapped out for an OAuth2/OIDC bearer token validator.
