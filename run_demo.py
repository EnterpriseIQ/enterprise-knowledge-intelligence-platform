"""End-to-end demonstration script.

Runs the five canonical demo queries plus the RBAC enforcement scenarios and prints
a readable transcript. This is the fastest way for a reviewer to see the whole
platform working: routing, hybrid retrieval, RBAC allow/deny, citations and
confidence — all without starting the web server.

    python run_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline import RAGPipeline  # noqa: E402

DEMO_QUERIES = [
    ("What is the remote work policy?", "HR"),
    ("Show engineering deployment standards.", "Engineering"),
    ("Summarize latest audit findings.", "Compliance"),
    ("Show finance budget allocations.", "Finance"),
    ("Show recent platform incidents.", "Engineering"),
]

# (description, query, role, expected_department, forbidden_department)
# expected_department is the department whose content the role SHOULD see;
# forbidden_department must NEVER appear in the returned citations.
RBAC_SCENARIOS = [
    ("HR reads HR content", "What is the leave policy?", "HR", "HR", None),
    ("HR blocked from Finance", "Show finance budget allocations.", "HR", None, "Finance"),
    (
        "Finance reads Finance content",
        "Show finance budget allocations.",
        "Finance",
        "Finance",
        None,
    ),
    ("Finance blocked from HR", "What is the remote work policy?", "Finance", None, "HR"),
    (
        "Engineering reads Engineering content",
        "Show deployment standards.",
        "Engineering",
        "Engineering",
        None,
    ),
    (
        "Engineering blocked from Finance",
        "Show finance budget allocations.",
        "Engineering",
        None,
        "Finance",
    ),
]

BAR = "=" * 78


def show(result) -> None:
    print(f"\n\033[1;34mQ ({result.role}):\033[0m {result.query}")
    print(
        f"\033[1;35mConfidence:\033[0m {result.confidence['label']} ({result.confidence['score']}) "
        f"| {result.confidence['explanation']}"
    )
    print(f"\033[1;36mRouting:\033[0m {result.route['rationale']}")
    print(f"\033[1;32mAnswer:\033[0m\n  {result.answer}")
    if result.citations:
        print("\033[1;33mCitations:\033[0m")
        for c in result.citations:
            print(f"  \033[33m{c['reference']}\033[0m")
    print(
        f"\033[1;31mAccess:\033[0m {result.authorised_count} authorised / {result.denied_count} denied; "
        f"coverage={result.coverage['source_types']}"
    )


def main() -> None:
    pipeline = RAGPipeline()
    stats = pipeline.build_index()
    print(BAR)
    print("SECURE ENTERPRISE RAG — DEMONSTRATION")
    print(BAR)
    print("Index:", stats)

    print("\n" + BAR + "\nPART 1 — CANONICAL DEMO QUERIES\n" + BAR)
    for q, role in DEMO_QUERIES:
        show(pipeline.query(q, role=role))

    print("\n" + BAR + "\nPART 2 — RBAC ENFORCEMENT SCENARIOS\n" + BAR)
    all_pass = True
    for desc, q, role, expected_dept, forbidden_dept in RBAC_SCENARIOS:
        result = pipeline.query(q, role=role)
        cited_depts = {c["department"] for c in result.citations}
        denied_depts = {d.department for d in result.access_decisions if not d.allowed}

        ok = True
        detail = ""
        if forbidden_dept:
            leaked = forbidden_dept in cited_depts
            ok = not leaked
            detail = (
                f"forbidden '{forbidden_dept}' leaked={leaked}; "
                f"blocked_at_source={forbidden_dept in denied_depts}"
            )
        elif expected_dept:
            ok = expected_dept in cited_depts
            detail = f"served '{expected_dept}' content={ok}"
        all_pass &= ok
        print(f"\n[{desc}]  ->  {'PASS' if ok else 'FAIL'}")
        print(f"  {detail}")
        print(
            f"  cited_departments={sorted(cited_depts)} | "
            f"authorised={result.authorised_count} denied={result.denied_count}"
        )
    print(f"\nRBAC enforcement: {'ALL SCENARIOS PASS' if all_pass else 'FAILURES DETECTED'}")

    print("\n" + BAR + "\nAudit trail (last 5 entries):\n" + BAR)
    for entry in pipeline.audit.tail(5):
        print(" ", entry)


if __name__ == "__main__":
    main()
