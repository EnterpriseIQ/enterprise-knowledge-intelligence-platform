"""RBAC tests.

These are the most important tests in the suite: they prove unauthorised content is
never surfaced, regardless of how relevant it is to the query.
"""

from __future__ import annotations

from src.security import RBACEngine


def _meta(dept, sens="internal", roles=""):
    return {"doc_id": f"{dept}-x", "department": dept, "sensitivity": sens, "allowed_roles": roles}


def test_department_isolation():
    rbac = RBACEngine()
    assert rbac.check("HR", _meta("HR")).allowed
    assert not rbac.check("HR", _meta("Finance")).allowed
    assert rbac.check("Finance", _meta("Finance")).allowed
    assert not rbac.check("Finance", _meta("HR")).allowed
    assert rbac.check("Engineering", _meta("Engineering")).allowed
    assert not rbac.check("Engineering", _meta("Finance")).allowed


def test_admin_sees_everything():
    rbac = RBACEngine()
    for dept in ["HR", "Finance", "Engineering", "Compliance", "Operations"]:
        assert rbac.check("Admin", _meta(dept, "restricted")).allowed


def test_clearance_enforced():
    rbac = RBACEngine()
    # HR clearance is 'confidential'; a 'restricted' HR doc must be denied.
    d = rbac.check("HR", _meta("HR", "restricted"))
    assert not d.allowed and "clearance" in d.reason


def test_compliance_cross_department_read():
    rbac = RBACEngine()
    # Compliance has cross-department read for audit.
    for dept in ["HR", "Finance", "Engineering", "Operations", "Compliance"]:
        assert rbac.check("Compliance", _meta(dept, "confidential")).allowed


def test_explicit_acl():
    rbac = RBACEngine()
    # Document locked to Finance only; Engineering (even same clearance) is denied.
    meta = _meta("Operations", "confidential", roles="Finance")
    assert not rbac.check("Engineering", meta).allowed
    assert rbac.check("Admin", meta).allowed  # admin bypass


def test_vector_prefilter():
    rbac = RBACEngine()
    assert rbac.vector_prefilter("Admin") is None  # wildcard => no filter
    f = rbac.vector_prefilter("HR")
    assert f == {"department": {"$in": ["HR"]}}


def test_pipeline_no_leakage(pipeline):
    """HR asking a Finance question must not receive any Finance citation."""
    res = pipeline.query("Show finance budget allocations.", role="HR")
    cited_depts = {c["department"] for c in res.citations}
    assert "Finance" not in cited_depts
    denied_depts = {d.department for d in res.access_decisions if not d.allowed}
    assert "Finance" in denied_depts  # finance docs were considered and blocked
