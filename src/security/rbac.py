"""RBAC Authorization Engine.

Implements document-level, attribute-based access control on top of roles. A
retrieval candidate is authorised only when ALL of the following hold:

1. **Department scope** — the document's department is in the role's allowed
   departments (or the role holds the ``*`` wildcard).
2. **Clearance** — the document's sensitivity is at or below the role's clearance
   on the ordered scale ``public < internal < confidential < restricted``.
3. **Explicit ACL** — if the document declares ``allowed_roles``, the user's role
   must be listed (Admin bypasses this).

The engine produces a structured :class:`AccessDecision` for every check, which
feeds both the audit trail and the explainability surface in API responses.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src import config


@dataclass
class AccessDecision:
    user_id: str
    role: str
    doc_id: str
    department: str
    sensitivity: str
    allowed: bool
    reason: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class RBACEngine:
    def __init__(self, policy_path: Path | None = None):
        policy_path = policy_path or config.ACCESS_POLICY_FILE
        policy = json.loads(Path(policy_path).read_text(encoding="utf-8"))
        self.roles: dict = policy["roles"]
        self.users: dict = policy.get("users", {})
        self.levels: list[str] = policy["sensitivity_levels"]
        self._rank = {lvl: i for i, lvl in enumerate(self.levels)}

    # ------------------------------------------------------------------ #
    def resolve_role(self, user_id: str | None, role: str | None) -> str:
        """Resolve an effective role from an explicit role or a known user id."""
        if user_id and user_id in self.users:
            user_role = self.users[user_id]["role"]
            if role and role != user_role:
                raise ValueError(f"User '{user_id}' cannot assume role '{role}'.")
            return user_role
        if role:
            if role not in self.roles:
                raise ValueError(f"Unknown role '{role}'. Valid roles: {list(self.roles)}")
            return role
        raise ValueError("Could not resolve a role: provide a valid role or known user_id.")

    def allowed_departments(self, role: str) -> list[str]:
        return self.roles[role]["departments"]

    # ------------------------------------------------------------------ #
    def check(self, role: str, doc_meta: dict, user_id: str = "") -> AccessDecision:
        department = doc_meta.get("department", "")
        sensitivity = doc_meta.get("sensitivity", "internal")
        doc_id = doc_meta.get("doc_id", "")
        allowed_roles_raw = doc_meta.get("allowed_roles", "")
        explicit_roles = [r for r in str(allowed_roles_raw).split(",") if r]

        role_cfg = self.roles[role]
        depts = role_cfg["departments"]
        is_admin = "*" in depts

        # 1. Department scope
        if not is_admin and department not in depts:
            return self._deny(user_id, role, doc_meta, f"role '{role}' has no access to department '{department}'")
        # 2. Clearance
        if self._rank.get(sensitivity, 99) > self._rank.get(role_cfg["clearance"], -1):
            return self._deny(user_id, role, doc_meta,
                              f"document sensitivity '{sensitivity}' exceeds role clearance "
                              f"'{role_cfg['clearance']}'")
        # 3. Explicit ACL
        if explicit_roles and not is_admin and role not in explicit_roles:
            return self._deny(user_id, role, doc_meta, f"document restricted to roles {explicit_roles}")

        return AccessDecision(user_id, role, doc_id, department, sensitivity, True,
                              "authorised: department scope, clearance and ACL satisfied")

    def _deny(self, user_id: str, role: str, doc_meta: dict, reason: str) -> AccessDecision:
        department = doc_meta.get("department", "")
        sensitivity = doc_meta.get("sensitivity", "internal")
        doc_id = doc_meta.get("doc_id", "")
        return AccessDecision(user_id, role, doc_id, department, sensitivity, False, reason)

    # ------------------------------------------------------------------ #
    def vector_prefilter(self, role: str) -> dict | None:
        """Return a vector-store ``where`` filter that pushes department scope into
        the query. Clearance and explicit ACLs are still enforced per-result by
        :meth:`check` (defence in depth)."""
        depts = self.roles[role]["departments"]
        if "*" in depts:
            return None
        return {"department": {"$in": depts}}
