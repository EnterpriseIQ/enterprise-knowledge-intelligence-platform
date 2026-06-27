# API Reference

EnterpriseIQ provides a RESTful API built with FastAPI. All endpoints (except `/health`) require authentication via the `X-API-Key` header if the `API_KEY` environment variable is set.

---

## Authentication

If the `API_KEY` environment variable is configured on the server, you must provide it in the headers for protected endpoints.

**Header Format:**
```http
X-API-Key: your_secure_api_key_here
```

If the key is invalid or missing, the API returns a `401 Unauthorized`.

---

## Endpoints

### 1. Health Check
Returns the liveness status of the API and the active backends (embedding model, vector store, and sparse index). It ensures the index and models are warm.

* **URL:** `/health`
* **Method:** `GET`
* **Auth Required:** No

#### Success Response
* **Code:** 200 OK
* **Content:**
  ```json
  {
    "status": "ok",
    "version": "1.0.0",
    "index": {
      "vectorstore": "ChromaDB",
      "embedding": "all-MiniLM-L6-v2",
      "documents": 1450,
      "chunks": 4200
    }
  }
  ```

---

### 2. Get Roles
Retrieves the available Role-Based Access Control (RBAC) roles, their allowed departments, clearance levels, and mapped users.

* **URL:** `/roles`
* **Method:** `GET`
* **Auth Required:** Yes

#### Success Response
* **Code:** 200 OK
* **Content:**
  ```json
  {
    "roles": {
      "Admin": {
        "departments": ["*"],
        "clearance": "restricted",
        "description": "Full access"
      },
      "HR": {
        "departments": ["HR"],
        "clearance": "confidential",
        "description": ""
      }
    },
    "users": {
      "fin_carol": "Finance",
      "eng_bob": "Engineering"
    }
  }
  ```

---

### 3. Execute Query
Submit a natural language query as a specific role or user. The pipeline routes the intent, retrieves hybrid results, enforces strict RBAC, and returns a grounded answer with citations.

* **URL:** `/query`
* **Method:** `POST`
* **Auth Required:** Yes

#### Request Body (JSON)
* `query` (string, required): The natural-language question.
* `role` (string, optional): Explicit role (e.g., "HR", "Engineering").
* `user_id` (string, optional): Known user id; its mapped role is used if `role` is omitted.
* `top_k` (integer, optional): Number of sources to retrieve (default: 5, max: 20).

**Example:**
```json
{
  "query": "What is the remote work policy?",
  "role": "HR",
  "top_k": 3
}
```

#### Success Response
* **Code:** 200 OK
* **Content:**
  ```json
  {
    "query": "What is the remote work policy?",
    "role": "HR",
    "answer": "According to the remote work policy, employees may work remotely up to 3 days a week [1]. Core hours are 10 AM to 3 PM [2].",
    "confidence": {
      "level": "high",
      "score": 0.85
    },
    "citations": [
      {
        "marker": 1,
        "reference": "[1]",
        "doc_id": "HR-2024-001",
        "title": "Employee Handbook",
        "department": "HR",
        "source_type": "PDF",
        "page": 12,
        "relevance": 0.92,
        "snippet": "employees may work remotely up to 3 days a week with manager approval."
      }
    ],
    "routing": {
      "intent": "lookup",
      "target_departments": ["HR"]
    },
    "source_coverage": {
      "HR-2024-001": 2
    },
    "access_summary": {
      "allowed": 3,
      "denied": 0,
      "reasons": []
    }
  }
  ```

#### Error Responses
* **Code:** 400 Bad Request
  * **Content:** `{"detail": "Invalid role specified."}`
* **Code:** 401 Unauthorized
  * **Content:** `{"detail": "Invalid or missing API Key"}`

---

### 4. Audit Log
Retrieves recent entries from the query audit trail, detailing who asked what and which documents were allowed or denied.

* **URL:** `/audit`
* **Method:** `GET`
* **Auth Required:** Yes
* **Query Params:** `limit` (integer, optional, default: 20)

#### Success Response
* **Code:** 200 OK
* **Content:**
  ```json
  {
    "entries": [
      {
        "timestamp": "2024-03-20T10:15:30Z",
        "user_id": "fin_carol",
        "role": "Finance",
        "query": "Show budget",
        "intent": "lookup",
        "docs_retrieved": 5,
        "docs_allowed": 3,
        "docs_denied": 2
      }
    ]
  }
  ```
