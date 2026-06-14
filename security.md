# Security & RBAC Design

Security is the defining requirement of this platform: a RAG system over enterprise
silos is only useful if it **cannot** become a data-exfiltration channel. This
document describes the access-control model, where it is enforced, the threat model
it addresses, and how every decision is made auditable.

## 1. Access-control model

The platform implements **role-based access control with attribute checks** at the
**document level**, inherited by every chunk at ingestion time.

A role may read a document only when **all three** predicates hold:

1. **Department scope** — `document.department ∈ role.departments`, or the role holds
   the `*` wildcard (Admin).
2. **Clearance** — `rank(document.sensitivity) ≤ rank(role.clearance)` on the ordered
   scale `public(0) < internal(1) < confidential(2) < restricted(3)`.
3. **Explicit ACL** — if `document.allowed_roles` is non-empty, `role` must be listed.
   Admin bypasses this.

The policy is data, not code: [`data/rbac/access_policies.json`](data/rbac/access_policies.json).

### Roles

| Role | Departments | Clearance | Notes |
|---|---|---|---|
| **Admin** | `*` | restricted | Full access. |
| **HR** | HR | confidential | Cannot read restricted HR docs (e.g. nothing above its clearance). |
| **Finance** | Finance | confidential | Isolated from HR/Eng/Compliance. |
| **Engineering** | Engineering, Operations | confidential | Owns platform docs + ops datasets. |
| **Compliance** | all (read) | restricted | Cross-department **read** for audit/GRC. |

The Compliance role models a real enterprise pattern: governance functions need
cross-cutting read access, but it is still bounded by clearance and is read-only at
the data level.

## 2. Where enforcement happens (defence in depth)

```
query → vector pre-filter (department)        ← layer 1: candidates restricted
      → per-candidate RBACEngine.check()       ← layer 2: clearance + ACL re-check
      → only allowed chunks fused & cited       ← unauthorised content never surfaces
      → every decision → audit trail            ← detection + accountability
```

- **Layer 1 — vector pre-filter.** `RBACEngine.vector_prefilter(role)` returns a
  ChromaDB `where` clause (`department ∈ allowed`). Unauthorised departments are never
  even scored. (Admin → no filter.)
- **Layer 2 — per-result authorization.** Every surviving candidate (dense *and*
  sparse, since BM25 is not pre-filtered) is re-checked for clearance and explicit
  ACL. This catches anything the coarse pre-filter could miss and is the
  authoritative gate.
- **Fail closed.** Unknown roles raise; missing/old sensitivity is treated as its
  declared value; if a check cannot pass, access is denied.

Because BM25 runs over the full corpus, **Layer 2 is essential** — it is the single
chokepoint that guarantees no unauthorised chunk is ever fused, regardless of channel.

## 3. Threat model & mitigations

| Threat | Mitigation |
|---|---|
| Cross-department data leak via relevance | RBAC filters candidates pre-fusion; tested for zero leakage. |
| Privilege bypass through the BM25 channel | Per-result `check()` re-applies to *all* candidates, not just dense. |
| Over-broad clearance | Sensitivity ladder enforced independently of department. |
| "Confused deputy" (model quotes restricted text) | Restricted text never enters the context window. |
| Silent denial / no accountability | Every allow **and** deny is written to the audit trail with a reason. |
| Prompt-injection exfiltration | Extractive generation can only emit text already authorised + retrieved. |

## 4. Demonstrated guarantees

`python run_demo.py` (and `pytest tests/test_rbac.py`) prove:

- **HR** reads HR, is **denied** Finance — Finance never appears in citations.
- **Finance** reads Finance, is **denied** HR.
- **Engineering** reads Engineering/Operations, is **denied** Finance.
- **Compliance** reads across departments (audit), bounded by clearance.
- **Admin** reads everything.

Each scenario asserts both *no forbidden department in the citations* and *the
forbidden department was blocked at source* (present in denied decisions).

## 5. Auditability & explainability

`src/security/audit.py` appends JSONL records to `data/logs/audit_trail.jsonl`:

- **query** events — who asked what, how many sources were authorised vs denied, and
  the answer confidence.
- **access_decision** events — per document: `allowed`, `department`, `sensitivity`
  and a human-readable `reason` (e.g. *"role 'Engineering' has no access to department
  'Finance'"*).

The API exposes recent entries at `GET /audit`. Each `/query` response also embeds an
`access_summary` (authorised/denied counts + a sample of decisions) and a `routing`
rationale, so callers can see *why* they got what they got.

## 6. Hardening roadmap (production)

- Authentication (OIDC/JWT) at the API edge; the role would come from a verified token
  rather than the request body (which is acceptable for this offline demo).
- Hash-chained / signed audit log for tamper evidence.
- Field- and row-level controls for structured sources (column masking).
- Per-tenant vector collections for isolation at scale.
- Rate limiting and query-content DLP scanning.
