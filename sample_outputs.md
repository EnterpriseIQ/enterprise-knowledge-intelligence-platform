# Sample Outputs

Real, unedited transcripts produced by the platform (offline, hashing-embedder
fallback active). Re-run with `python run_demo.py`.

---

## 1. Grounded answer with citations (Compliance)

```
$ python -m src.cli --role Compliance --query "Summarize latest audit findings."

Q: Summarize latest audit findings.
Role: Compliance   Confidence: high (0.6833)

Answer:
Latest Findings Summary The most recent audit findings highlight access-recertification
gaps and incomplete change records during incidents as the two highest-priority items. [1]
Internal Audit Report 2025 (Restricted) Scope This restricted audit reviewed access
management, change control and data retention across the engineering and finance functions
for the period January to May 2025. [1] Key Findings Finding A (Medium): 4 of 60 sampled
user accounts retained access to systems no longer required by their role, indicating gaps
in the quarterly access review. [1] No critical or high findings were identified. [1]

Citations:
  [1] Audit Report 2025 (Compliance, p.1)
  [2] Regulatory Findings (Compliance, p.1)
  [3] Audit Trail Logs (Compliance, json)
  [4] GDPR Policy (Compliance, p.1)
  [5] Security Policy (Compliance, p.1)

Routing: Intent='summarize'. Routed toward Compliance(2) based on keyword signals.
Access: 20 authorised / 0 denied chunks
```

Every clause carries a citation marker resolving to a specific document and page.

---

## 2. RBAC enforcement — no leakage (the core security guarantee)

```
$ python run_demo.py        # Part 2 (abridged)

PART 2 — RBAC ENFORCEMENT SCENARIOS
==============================================================================

[HR reads HR content]  ->  PASS
  served 'HR' content=True
  cited_departments=['HR'] | authorised=4 denied=11

[HR blocked from Finance]  ->  PASS
  forbidden 'Finance' leaked=False; blocked_at_source=True
  cited_departments=['HR'] | authorised=4 denied=5

[Finance reads Finance content]  ->  PASS
  served 'Finance' content=True
  cited_departments=['Finance'] | authorised=3 denied=5

[Finance blocked from HR]  ->  PASS
  forbidden 'HR' leaked=False; blocked_at_source=True
  cited_departments=['Finance'] | authorised=3 denied=12

[Engineering reads Engineering content]  ->  PASS
  served 'Engineering' content=True
  cited_departments=['Engineering', 'Operations'] | authorised=10 denied=0

[Engineering blocked from Finance]  ->  PASS
  forbidden 'Finance' leaked=False; blocked_at_source=True
  cited_departments=['Engineering', 'Operations'] | authorised=10 denied=6

RBAC enforcement: ALL SCENARIOS PASS
```

When HR asks a Finance question, **no Finance content is returned** — the Finance
documents are visibly *blocked at source* (counted in `denied`), and the answer is
grounded only in HR content.

---

## 3. Audit trail (explainability)

Every access decision is logged with a human-readable reason:

```
{'type': 'access_decision', 'role': 'Engineering', 'doc_id': 'fin-expense',
 'department': 'Finance', 'sensitivity': 'confidential', 'allowed': False,
 'reason': "role 'Engineering' has no access to department 'Finance'", 'ts': '...'}
{'type': 'query', 'role': 'Engineering', 'query': 'Show finance budget allocations.',
 'authorised_sources': 10, 'denied_sources': 6, 'confidence': 0.31, 'ts': '...'}
```

---

## 4. Grounding / refusal (no hallucination)

```
$ python -m src.cli --role Admin --query "What is the airspeed velocity of an unladen swallow?"

Role: Admin   Confidence: low (0.0333)

Answer:
I could not find sufficient authorised evidence to answer this question confidently.
Please refine the question or check that you have access to the relevant documents.
```

Out-of-corpus questions score low confidence and trigger an explicit refusal instead
of a fabricated answer.

---

## 5. `/health` (active backends)

```json
{
  "status": "ok",
  "version": "1.0.0",
  "index": {
    "documents": 20,
    "chunks": 23,
    "vectorstore_backend": "chromadb",
    "embedding_backend": "hashing-fallback",
    "bm25_backend": "rank-bm25"
  }
}
```

`embedding_backend` shows `sentence-transformers:all-MiniLM-L6-v2` when model weights
are available, and `hashing-fallback` otherwise — the platform runs either way.
