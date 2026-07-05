# Internals

This section covers the internal operations of the EnterpriseIQ platform.

## The RBAC Engine

The `RBACEngine` is the core security component. It reads policies from `data/rbac/access_policies.json`.

```mermaid
flowchart TD
    UserReq[User Request] --> Auth[Resolve Role]
    Auth --> FetchPolicy[Load Policy from JSON]
    FetchPolicy --> EvalDept{Match Department?}
    EvalDept -- No --> Deny[Reject Chunk]
    EvalDept -- Yes --> EvalClearance{Clearance Level >= Chunk?}
    EvalClearance -- No --> Deny
    EvalClearance -- Yes --> EvalACL{Explicit ACL Allow?}
    EvalACL -- No --> Deny
    EvalACL -- Yes --> Allow[Approve Chunk]
```

## Hybrid Fusion Algorithm

We use a Min-Max normalized Reciprocal Rank Fusion algorithm to combine Dense and Sparse scores.

$Score_{final} = (\alpha \times Score_{dense}) + ((1 - \alpha) \times Score_{sparse})$

Where $\alpha$ is defined by `HYBRID_ALPHA` in the configuration.
