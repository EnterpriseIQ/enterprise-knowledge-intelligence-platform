# SDK Guide

While EnterpriseIQ currently does not ship with official PyPI or npm packages for client SDKs, the API is strictly defined via OpenAPI/Swagger, making it trivial to generate clients or use lightweight HTTP wrappers.

## Python Example

Using `httpx` to interact with the API:

```python
import httpx
import json

API_URL = "http://localhost:8000"
API_KEY = "your_secure_api_key_here"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# 1. Check Health
response = httpx.get(f"{API_URL}/health")
print("Health:", response.json())

# 2. Ask a Question
payload = {
    "query": "Show me the latest architecture diagrams.",
    "role": "Engineering",
    "top_k": 5
}

response = httpx.post(f"{API_URL}/query", headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"\nAnswer: {data['answer']}")
    print("\nCitations:")
    for cit in data['citations']:
        print(f"{cit['reference']} Document: {cit['title']} (Page {cit['page']})")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## TypeScript / Node.js Example

Using standard `fetch`:

```typescript
const API_URL = "http://localhost:8000";
const API_KEY = "your_secure_api_key_here";

async function queryEnterpriseIQ(question: string, role: string) {
    const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        body: JSON.stringify({
            query: question,
            role: role,
            top_k: 3
        })
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Answer:", data.answer);

    data.citations.forEach((cit: any) => {
        console.log(`${cit.reference} Source: ${cit.title} [${cit.department}]`);
    });
}

// Usage
queryEnterpriseIQ("What are the quarterly goals?", "Admin");
```

## Client Generation

Because EnterpriseIQ is built with FastAPI, it automatically serves an OpenAPI schema at `/openapi.json`. You can use tools like `openapi-typescript-codegen` or `openapi-python-client` to generate strongly typed SDKs automatically.
