"""Query Router.

Classifies user intent and routes the query toward the most relevant departments
and source types. Routing is a *soft* signal: it boosts the right sources rather
than hard-excluding others, so genuinely cross-source questions still work. The
router is intentionally rule/keyword based — transparent, dependency-free and easy
for a reviewer to audit — with a clear extension point for a learned classifier.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Department signal keywords. Curated for the synthetic corpus but representative
# of how an enterprise taxonomy would drive routing.
_DEPT_KEYWORDS = {
    "HR": ["leave", "vacation", "remote", "hybrid", "employee", "handbook", "hiring",
           "recruit", "parental", "sick", "benefit", "onboarding", "salary band"],
    "Finance": ["budget", "forecast", "expense", "cost", "spend", "allocation",
                "capex", "revenue", "financial", "invoice"],
    "Engineering": ["deployment", "deploy", "architecture", "incident", "platform",
                    "service", "api", "rollback", "latency", "release", "outage", "sev"],
    "Compliance": ["gdpr", "audit", "regulatory", "compliance", "security policy",
                   "breach", "retention", "finding", "data protection", "encryption"],
    "Operations": ["server", "ticket", "metric", "cpu", "uptime", "operational",
                   "database replica", "p99", "error rate"],
}

_SOURCE_KEYWORDS = {
    "sql": ["server", "ticket", "table", "database", "row", "record"],
    "csv": ["metric", "error rate", "latency", "cpu", "throughput"],
    "json": ["log", "audit trail", "event", "access log", "security event"],
}

_INTENTS = {
    "lookup": ["what is", "what's", "define", "explain", "policy", "how do", "where"],
    "summarize": ["summarize", "summary", "overview", "latest", "recent", "key findings"],
    "list": ["list", "show", "which", "all", "enumerate"],
    "aggregate": ["how many", "total", "average", "highest", "lowest", "count", "top"],
}


@dataclass
class RouteDecision:
    intent: str
    departments: list[str]            # ranked, most relevant first
    source_types: list[str]           # preferred source types (may be empty)
    rationale: str = ""
    scores: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "intent": self.intent,
            "departments": self.departments,
            "source_types": self.source_types,
            "rationale": self.rationale,
            "scores": self.scores,
        }


class QueryRouter:
    def classify(self, query: str) -> RouteDecision:
        q = query.lower()

        # Intent
        intent = "lookup"
        for name, cues in _INTENTS.items():
            if any(c in q for c in cues):
                intent = name
                break

        # Department scoring
        dept_scores: dict[str, int] = {}
        for dept, kws in _DEPT_KEYWORDS.items():
            score = sum(1 for kw in kws if kw in q)
            if score:
                dept_scores[dept] = score
        ranked = sorted(dept_scores, key=dept_scores.get, reverse=True)

        # Source-type preference
        src_pref = [st for st, kws in _SOURCE_KEYWORDS.items()
                    if any(kw in q for kw in kws)]

        rationale = self._explain(intent, ranked, dept_scores, src_pref)
        return RouteDecision(intent=intent, departments=ranked,
                             source_types=src_pref, rationale=rationale,
                             scores=dept_scores)

    @staticmethod
    def _explain(intent, ranked, scores, src_pref) -> str:
        if ranked:
            depts = ", ".join(f"{d}({scores[d]})" for d in ranked)
            base = f"Intent='{intent}'. Routed toward {depts} based on keyword signals."
        else:
            base = (f"Intent='{intent}'. No strong department signal; performing a broad "
                    f"cross-source search within the user's authorised scope.")
        if src_pref:
            base += f" Source-type preference: {', '.join(src_pref)}."
        return base
