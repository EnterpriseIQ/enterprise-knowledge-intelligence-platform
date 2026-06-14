"""Synthetic enterprise dataset generator.

Produces a realistic, heterogeneous corpus across five departments and writes a
``manifest.json`` describing the department, sensitivity and source type of every
artefact. The manifest is the bridge between raw data and the RBAC engine: every
chunk inherits its document's security metadata at ingestion time.

Outputs
-------
data/documents/*.pdf      HR / Engineering / Finance / Compliance documents
data/structured/*.csv     Operations operational metrics
data/structured/operations.db   SQLite operational database (servers, tickets)
data/logs/*.json          Audit, access and security event logs
data/documents/manifest.json    Security + provenance metadata for everything

Run with:  python -m data.generate_data   (from the project root)
"""
from __future__ import annotations

import csv
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Allow running both as a module and as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config  # noqa: E402

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    _HAVE_REPORTLAB = True
except Exception:  # pragma: no cover - reportlab is in requirements
    _HAVE_REPORTLAB = False


MANIFEST: list[dict] = []


def _register(doc_id, title, path, source_type, department, sensitivity, allowed_roles=None):
    MANIFEST.append({
        "doc_id": doc_id,
        "title": title,
        "path": str(Path(path).relative_to(config.PROJECT_ROOT)),
        "source_type": source_type,
        "department": department,
        "sensitivity": sensitivity,
        # An empty list means "fall back to role/department/clearance rules".
        "allowed_roles": allowed_roles or [],
    })


def write_pdf(filename: str, title: str, paragraphs: list[str]) -> Path:
    """Render a simple, real-text PDF so retrieval has genuine content to index."""
    path = config.DOCUMENTS_DIR / filename
    if _HAVE_REPORTLAB:
        doc = SimpleDocTemplate(str(path), pagesize=LETTER,
                                topMargin=0.8 * inch, bottomMargin=0.8 * inch)
        styles = getSampleStyleSheet()
        story = [Paragraph(title, styles["Title"]), Spacer(1, 0.2 * inch)]
        for para in paragraphs:
            if para.startswith("## "):
                story.append(Spacer(1, 0.12 * inch))
                story.append(Paragraph(para[3:], styles["Heading2"]))
            else:
                story.append(Paragraph(para, styles["BodyText"]))
                story.append(Spacer(1, 0.08 * inch))
        doc.build(story)
    else:  # graceful degradation: emit a .txt with the same stem
        path = path.with_suffix(".txt")
        path.write_text(title + "\n\n" + "\n\n".join(paragraphs), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# HR documents
# --------------------------------------------------------------------------- #
def gen_hr():
    p = write_pdf("hr_employee_handbook.pdf", "Acme Corp Employee Handbook (2025)", [
        "## Purpose",
        "This handbook summarises the policies, benefits and expectations for all Acme Corp employees. It is an internal document and supersedes all previous versions.",
        "## Working Hours",
        "Standard working hours are 09:00 to 17:30, Monday to Friday, with a one hour lunch break. Core collaboration hours are 11:00 to 16:00 during which all employees are expected to be reachable.",
        "## Code of Conduct",
        "Employees must act with integrity, respect confidentiality and avoid conflicts of interest. Harassment of any kind is grounds for disciplinary action up to and including termination.",
        "## Benefits",
        "Full time employees receive private health insurance, a pension contribution of 6% of base salary, and an annual learning budget of 1,200 EUR.",
    ], )
    _register("hr-handbook", "Employee Handbook 2025", p, "pdf", "HR", "internal")

    p = write_pdf("hr_leave_policy.pdf", "Leave and Time-Off Policy", [
        "## Annual Leave",
        "Employees are entitled to 28 days of paid annual leave per calendar year, accrued monthly. Up to 5 unused days may be carried over into the following year and must be used by March 31.",
        "## Sick Leave",
        "Employees receive up to 10 paid sick days per year. A medical certificate is required for absences longer than three consecutive working days.",
        "## Parental Leave",
        "Primary caregivers are entitled to 16 weeks of paid parental leave; secondary caregivers to 4 weeks. Requests should be submitted at least 8 weeks in advance.",
        "## Requesting Leave",
        "All leave must be requested through the HR portal and approved by the line manager. Leave during the financial year-end freeze (December 15 to January 5) requires director approval.",
    ])
    _register("hr-leave", "Leave Policy", p, "pdf", "HR", "internal")

    p = write_pdf("hr_remote_work_policy.pdf", "Remote and Hybrid Work Policy", [
        "## Overview",
        "Acme Corp operates a hybrid working model. This policy defines eligibility, expectations and security requirements for remote work.",
        "## Eligibility and Schedule",
        "Employees may work remotely up to three days per week. At least two days per week must be worked from a company office to support collaboration. Fully remote arrangements require VP approval and are reviewed every six months.",
        "## Equipment and Security",
        "Remote workers must use company-issued laptops with full-disk encryption and the corporate VPN for all access to internal systems. Public Wi-Fi may only be used together with the VPN.",
        "## Expectations",
        "Remote employees are expected to be reachable during core hours (11:00 to 16:00), keep their calendars up to date, and attend on-site team meetings when requested.",
    ])
    _register("hr-remote", "Remote Work Policy", p, "pdf", "HR", "internal")

    p = write_pdf("hr_hiring_guidelines.pdf", "Hiring and Recruitment Guidelines (Confidential)", [
        "## Scope",
        "These confidential guidelines govern how hiring managers conduct recruitment to ensure fair, consistent and legally compliant hiring decisions.",
        "## Structured Interviews",
        "Every candidate must be assessed against a predefined scorecard. At least two independent interviewers are required, and interviewers must submit written feedback within 24 hours.",
        "## Compensation Bands",
        "Offers must fall within the approved compensation band for the level. Engineering L4 bands are 72,000 to 88,000 EUR base. Exceptions above the band require Finance and HR director sign-off.",
        "## Non-Discrimination",
        "Hiring decisions must never be based on protected characteristics. All recruitment data is retained for 12 months for compliance audit purposes.",
    ])
    _register("hr-hiring", "Hiring Guidelines", p, "pdf", "HR", "confidential")


# --------------------------------------------------------------------------- #
# Engineering documents
# --------------------------------------------------------------------------- #
def gen_engineering():
    p = write_pdf("eng_architecture_standards.pdf", "Engineering Architecture Standards", [
        "## Principles",
        "Services must be stateless where possible, expose health and readiness probes, and emit structured JSON logs. All inter-service communication uses authenticated HTTPS.",
        "## Data Layer",
        "Each service owns its database. Cross-service data access happens only through published APIs or an event stream, never by reaching into another service's database directly.",
        "## API Standards",
        "APIs follow REST conventions, are versioned under /v1, and must document every endpoint with OpenAPI. Breaking changes require a new major version and a deprecation window of 90 days.",
        "## Observability",
        "Every service exports metrics, logs and traces. Service level objectives (SLOs) target 99.9% availability and a p99 latency under 300 ms for synchronous endpoints.",
    ])
    _register("eng-arch", "Architecture Standards", p, "pdf", "Engineering", "internal")

    p = write_pdf("eng_deployment_guide.pdf", "Production Deployment Guide and Standards", [
        "## Deployment Pipeline",
        "All changes flow through CI: lint, unit tests, integration tests, and a security scan must pass before a build is promoted. Deployments to production require a green pipeline and one peer approval.",
        "## Release Strategy",
        "Production uses blue-green deployments with automated smoke tests. If error rates exceed 2% within ten minutes of a release, the deployment is automatically rolled back to the previous version.",
        "## Change Windows",
        "Standard deployments are permitted Monday to Thursday between 10:00 and 16:00. Friday and weekend deployments require an on-call lead approval to reduce incident risk.",
        "## Rollback",
        "Every deployment must be reversible within five minutes. Database migrations must be backward compatible and applied separately from code that depends on them.",
    ])
    _register("eng-deploy", "Deployment Guide", p, "pdf", "Engineering", "internal")

    p = write_pdf("eng_incident_reports.pdf", "Platform Incident Reports (Confidential)", [
        "## INC-2025-014: API Gateway Latency Spike",
        "On 2025-03-12 the API gateway experienced p99 latency above 1,200 ms for 42 minutes due to a connection pool exhaustion after a dependency upgrade. Mitigation: pool size increased and circuit breaker tuned. Severity: SEV-2.",
        "## INC-2025-021: Partial Search Outage",
        "On 2025-04-05 the search service returned errors for 18% of requests for 26 minutes following a bad index migration. Resolved by rolling back the migration. Root cause: missing backward-compatible index alias. Severity: SEV-2.",
        "## INC-2025-027: Authentication Service Degradation",
        "On 2025-05-19 token validation latency increased, causing intermittent 401 responses for 12 minutes. Cause: expired cache of signing keys. Action: automated key refresh added. Severity: SEV-3.",
        "## Action Items",
        "All SEV-2 incidents require a written postmortem within five business days and at least one preventive action tracked to completion.",
    ])
    _register("eng-incidents", "Incident Reports", p, "pdf", "Engineering", "confidential")

    p = write_pdf("eng_platform_documentation.pdf", "Internal Platform Documentation", [
        "## Platform Overview",
        "The Acme internal platform provides shared services for authentication, search, messaging and storage so that product teams can ship features without rebuilding infrastructure.",
        "## Authentication Service",
        "Issues short-lived JWT access tokens (15 minutes) and refresh tokens (8 hours). Supports OIDC federation with the corporate identity provider.",
        "## Search Service",
        "Provides hybrid keyword and vector search over indexed documents. Tenants are isolated by namespace and results are filtered by access policy before they are returned.",
        "## Storage Service",
        "Object storage with server-side encryption, lifecycle policies and per-bucket access controls integrated with the central RBAC system.",
    ])
    _register("eng-platform", "Platform Documentation", p, "pdf", "Engineering", "internal")


# --------------------------------------------------------------------------- #
# Finance documents
# --------------------------------------------------------------------------- #
def gen_finance():
    p = write_pdf("fin_budget_report_2025.pdf", "Annual Budget Report and Allocations 2025 (Confidential)", [
        "## Executive Summary",
        "The 2025 operating budget totals 24.6 million EUR, an increase of 8% over 2024, driven primarily by engineering headcount growth and cloud infrastructure investment.",
        "## Department Allocations",
        "Engineering is allocated 11.2 million EUR (46%), Sales and Marketing 5.4 million EUR (22%), Operations 3.1 million EUR (13%), HR 1.8 million EUR (7%), Compliance 1.3 million EUR (5%), and a contingency reserve of 1.8 million EUR (7%).",
        "## Capital Expenditure",
        "Capital expenditure of 2.4 million EUR is approved for data centre hardware refresh and security tooling. All capex above 100,000 EUR requires CFO approval.",
        "## Quarterly Phasing",
        "Spend is phased roughly evenly across quarters, with a planned uplift in Q3 for the annual hardware refresh and conference season.",
    ])
    _register("fin-budget", "Budget Report 2025", p, "pdf", "Finance", "confidential")

    p = write_pdf("fin_expense_report_q1.pdf", "Q1 2025 Expense Report (Confidential)", [
        "## Summary",
        "Total Q1 operating spend was 5.9 million EUR against a budget of 6.1 million EUR, a favourable variance of 3.3%.",
        "## Major Categories",
        "Cloud infrastructure accounted for 1.7 million EUR, salaries 3.4 million EUR, travel 0.21 million EUR, software licences 0.34 million EUR, and facilities 0.25 million EUR.",
        "## Notable Variances",
        "Travel was 35% under budget due to a continued shift to virtual conferences. Cloud spend was 6% over budget because of additional capacity provisioned during the April search outage remediation.",
        "## Controls",
        "All expenses above 5,000 EUR require manager approval; above 25,000 EUR require Finance director approval and a purchase order.",
    ])
    _register("fin-expense", "Expense Report Q1", p, "pdf", "Finance", "confidential")

    p = write_pdf("fin_department_forecast.pdf", "Department Forecast 2025-2026 (Confidential)", [
        "## Methodology",
        "Forecasts combine bottom-up departmental plans with a top-down revenue model. A conservative and an optimistic scenario are maintained for planning.",
        "## Engineering Forecast",
        "Engineering spend is forecast to grow 12% in 2026 to 12.5 million EUR, driven by 14 planned hires and increased GPU compute for machine learning workloads.",
        "## Operations Forecast",
        "Operations spend is expected to remain flat at 3.1 million EUR as efficiency gains offset volume growth.",
        "## Risk Factors",
        "Key risks include cloud price increases, currency fluctuation on USD-denominated contracts, and slower revenue growth in the conservative scenario.",
    ])
    _register("fin-forecast", "Department Forecast", p, "pdf", "Finance", "confidential")


# --------------------------------------------------------------------------- #
# Compliance documents
# --------------------------------------------------------------------------- #
def gen_compliance():
    p = write_pdf("comp_gdpr_policy.pdf", "GDPR and Data Protection Policy", [
        "## Lawful Basis",
        "Acme Corp processes personal data only where there is a lawful basis: consent, contract, legal obligation or legitimate interest. The basis for each processing activity is recorded in the data processing register.",
        "## Data Subject Rights",
        "Individuals may request access, rectification, erasure and portability of their personal data. Requests must be fulfilled within 30 days and are logged for audit.",
        "## Data Retention",
        "Personal data is retained only as long as necessary. Recruitment data is retained for 12 months, employee records for the duration of employment plus seven years, and access logs for 13 months.",
        "## Breach Notification",
        "Personal data breaches likely to result in risk to individuals must be reported to the supervisory authority within 72 hours of discovery.",
    ])
    _register("comp-gdpr", "GDPR Policy", p, "pdf", "Compliance", "internal")

    p = write_pdf("comp_security_policy.pdf", "Information Security Policy (Confidential)", [
        "## Access Control",
        "Access to systems and data follows least privilege and is granted based on role. All access is reviewed quarterly and revoked promptly on role change or departure.",
        "## Encryption",
        "Data is encrypted in transit using TLS 1.2 or higher and at rest using AES-256. Encryption keys are rotated at least annually and stored in a managed key vault.",
        "## Authentication",
        "Multi-factor authentication is mandatory for all administrative access and all remote access to internal systems.",
        "## Incident Response",
        "Security incidents must be reported to the security team within one hour. The incident response plan is tested at least twice per year.",
    ])
    _register("comp-security", "Security Policy", p, "pdf", "Compliance", "confidential")

    p = write_pdf("comp_audit_report_2025.pdf", "Internal Audit Report 2025 (Restricted)", [
        "## Scope",
        "This restricted audit reviewed access management, change control and data retention across the engineering and finance functions for the period January to May 2025.",
        "## Key Findings",
        "Finding A (Medium): 4 of 60 sampled user accounts retained access to systems no longer required by their role, indicating gaps in the quarterly access review. Finding B (Low): two production changes in March bypassed the standard peer-approval step during an incident.",
        "## Latest Findings Summary",
        "The most recent audit findings highlight access-recertification gaps and incomplete change records during incidents as the two highest-priority items. No critical or high findings were identified.",
        "## Remediation",
        "Management agreed to automate access recertification by Q3 2025 and to enforce break-glass change documentation within 24 hours of any emergency change.",
    ])
    _register("comp-audit", "Audit Report 2025", p, "pdf", "Compliance", "restricted")

    p = write_pdf("comp_regulatory_findings.pdf", "Regulatory Findings and Remediation Log (Restricted)", [
        "## Regulatory Context",
        "This restricted log tracks findings raised by external regulators and the resulting remediation commitments.",
        "## Finding R-2025-03",
        "A regulator noted that the data processing register was missing two recently introduced processing activities. Remediation: register updated and a quarterly review control introduced. Status: Closed.",
        "## Finding R-2025-07",
        "A review of breach handling found that one low-risk incident was logged after the internal one-hour target. Remediation: alerting tuned and staff retrained. Status: In progress.",
        "## Overall Status",
        "No fines were levied. All open items have committed remediation dates within the current year.",
    ])
    _register("comp-regulatory", "Regulatory Findings", p, "pdf", "Compliance", "restricted")


# --------------------------------------------------------------------------- #
# Operations structured data (CSV + SQL)
# --------------------------------------------------------------------------- #
def gen_operations():
    # CSV operational metrics ------------------------------------------------
    csv_path = config.STRUCTURED_DIR / "operations_metrics.csv"
    rows = [
        ["date", "service", "requests", "error_rate_pct", "p99_latency_ms", "cpu_util_pct"],
        ["2025-05-01", "api-gateway", 1_240_000, 0.31, 240, 58],
        ["2025-05-01", "search", 540_000, 0.42, 310, 64],
        ["2025-05-01", "auth", 880_000, 0.12, 95, 41],
        ["2025-05-02", "api-gateway", 1_310_000, 0.28, 235, 60],
        ["2025-05-02", "search", 560_000, 0.55, 330, 67],
        ["2025-05-02", "auth", 905_000, 0.10, 92, 43],
        ["2025-05-03", "api-gateway", 1_180_000, 0.35, 250, 55],
        ["2025-05-03", "search", 510_000, 0.48, 305, 62],
        ["2025-05-03", "auth", 860_000, 0.14, 98, 40],
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    _register("ops-metrics", "Operational Metrics (CSV)", csv_path, "csv", "Operations", "internal")

    # SQLite operational database -------------------------------------------
    db_path = config.SQL_DB_FILE
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE servers (
        hostname TEXT, region TEXT, role TEXT, status TEXT, cpu_cores INTEGER, memory_gb INTEGER)""")
    cur.executemany("INSERT INTO servers VALUES (?,?,?,?,?,?)", [
        ("web-eu-01", "eu-west", "frontend", "healthy", 16, 64),
        ("web-eu-02", "eu-west", "frontend", "healthy", 16, 64),
        ("db-eu-01", "eu-west", "database", "healthy", 32, 256),
        ("db-eu-02", "eu-west", "database", "degraded", 32, 256),
        ("cache-eu-01", "eu-west", "cache", "healthy", 8, 32),
        ("web-us-01", "us-east", "frontend", "healthy", 16, 64),
    ])
    cur.execute("""CREATE TABLE tickets (
        ticket_id TEXT, opened TEXT, priority TEXT, service TEXT, status TEXT, summary TEXT)""")
    cur.executemany("INSERT INTO tickets VALUES (?,?,?,?,?,?)", [
        ("OPS-5012", "2025-05-12", "P2", "search", "resolved", "Elevated search latency after index rebuild"),
        ("OPS-5031", "2025-05-18", "P3", "auth", "resolved", "Intermittent 401s due to signing key cache"),
        ("OPS-5044", "2025-05-22", "P1", "database", "open", "db-eu-02 replica lag exceeding threshold"),
        ("OPS-5050", "2025-05-25", "P3", "api-gateway", "open", "Connection pool warnings under peak load"),
    ])
    conn.commit()
    conn.close()
    _register("ops-sql", "Operations Database (SQL: servers, tickets)", db_path, "sql", "Operations", "confidential")


# --------------------------------------------------------------------------- #
# Logs (JSON)
# --------------------------------------------------------------------------- #
def gen_logs():
    base = datetime(2025, 5, 20, 8, 0, 0)

    access_log = [
        {"ts": (base + timedelta(minutes=i * 7)).isoformat(), "user": u, "action": a,
         "resource": r, "result": res, "ip": ip}
        for i, (u, a, r, res, ip) in enumerate([
            ("hr_bob", "read", "hr_leave_policy.pdf", "allow", "10.0.4.21"),
            ("fin_carol", "read", "fin_budget_report_2025.pdf", "allow", "10.0.5.34"),
            ("eng_dave", "read", "eng_deployment_guide.pdf", "allow", "10.0.6.12"),
            ("eng_dave", "read", "fin_budget_report_2025.pdf", "deny", "10.0.6.12"),
            ("hr_bob", "read", "fin_expense_report_q1.pdf", "deny", "10.0.4.21"),
            ("comp_erin", "read", "comp_audit_report_2025.pdf", "allow", "10.0.7.5"),
        ])
    ]
    p = config.LOGS_DIR / "access_logs.json"
    p.write_text(json.dumps(access_log, indent=2), encoding="utf-8")
    _register("log-access", "Access Logs", p, "json", "Operations", "confidential")

    security_events = [
        {"ts": (base + timedelta(hours=i)).isoformat(), "event_id": f"SEC-{1000+i}",
         "severity": sev, "category": cat, "description": desc}
        for i, (sev, cat, desc) in enumerate([
            ("low", "auth", "5 failed login attempts for user fin_carol from a new device, then success with MFA."),
            ("medium", "access", "User eng_dave attempted to access a Finance document and was denied by RBAC."),
            ("high", "exfiltration", "Anomalous bulk export attempt blocked: 4,200 records requested outside business hours."),
            ("low", "config", "TLS certificate for api-gateway renewed automatically 14 days before expiry."),
        ])
    ]
    p = config.LOGS_DIR / "security_events.json"
    p.write_text(json.dumps(security_events, indent=2), encoding="utf-8")
    _register("log-security", "Security Events", p, "json", "Compliance", "restricted")

    audit_log = [
        {"ts": (base + timedelta(hours=2 * i)).isoformat(), "actor": actor, "action": action,
         "target": target, "outcome": outcome}
        for i, (actor, action, target, outcome) in enumerate([
            ("admin_alice", "grant_role", "eng_dave:Engineering", "success"),
            ("comp_erin", "open_audit", "access-recertification-Q2", "success"),
            ("admin_alice", "rotate_key", "storage-service-kms", "success"),
            ("comp_erin", "review_finding", "R-2025-07", "in_progress"),
        ])
    ]
    p = config.LOGS_DIR / "audit_logs.json"
    p.write_text(json.dumps(audit_log, indent=2), encoding="utf-8")
    _register("log-audit", "Audit Trail Logs", p, "json", "Compliance", "restricted")


def main():
    config.ensure_dirs()
    print("Generating synthetic enterprise corpus...")
    gen_hr()
    gen_engineering()
    gen_finance()
    gen_compliance()
    gen_operations()
    gen_logs()

    manifest_path = config.DOCUMENTS_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(MANIFEST, indent=2), encoding="utf-8")

    by_dept: dict[str, int] = {}
    for m in MANIFEST:
        by_dept[m["department"]] = by_dept.get(m["department"], 0) + 1
    print(f"  Wrote {len(MANIFEST)} sources across departments: {by_dept}")
    print(f"  Manifest: {manifest_path.relative_to(config.PROJECT_ROOT)}")
    print("Done.")


if __name__ == "__main__":
    main()
