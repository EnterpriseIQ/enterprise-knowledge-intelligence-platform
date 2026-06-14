# Sample Queries

Copy-paste examples for the CLI and the API. Roles: `Admin | HR | Finance |
Engineering | Compliance`. Known users: `admin_alice, hr_bob, fin_carol, eng_dave,
comp_erin`.

## Canonical demo queries

| # | Query | Role | Expected source(s) |
|---|---|---|---|
| 1 | What is the remote work policy? | HR | Remote Work Policy (HR) |
| 2 | Show engineering deployment standards. | Engineering | Deployment Guide / Architecture Standards |
| 3 | Summarize latest audit findings. | Compliance | Audit Report 2025 / Regulatory Findings |
| 4 | Show finance budget allocations. | Finance | Budget Report 2025 |
| 5 | Show recent platform incidents. | Engineering | Incident Reports (+ ops tickets) |

```bash
python -m src.cli --role HR          --query "What is the remote work policy?"
python -m src.cli --role Engineering --query "Show engineering deployment standards."
python -m src.cli --role Compliance  --query "Summarize latest audit findings."
python -m src.cli --role Finance      --query "Show finance budget allocations."
python -m src.cli --role Engineering --query "Show recent platform incidents." --json
```

## RBAC enforcement examples (expected: blocked)

```bash
# HR asks a Finance question -> no Finance content is returned
python -m src.cli --role HR --query "Show finance budget allocations."

# Engineering asks a Finance question -> denied at source
python -m src.cli --user eng_dave --query "Show finance budget allocations."

# Finance asks an HR question -> no HR content is returned
python -m src.cli --role Finance --query "What is the remote work policy?"
```

## Cross-source examples

```bash
# Spans Engineering PDFs + Operations SQL tickets + CSV metrics
python -m src.cli --role Admin --query "Show recent operational tickets and platform incidents."

# Operational health from CSV + SQL
python -m src.cli --role Engineering --query "Which services had the highest error rate and which servers are degraded?"
```

## Grounding / refusal example (out-of-corpus)

```bash
# Confidence is low -> the system refuses instead of hallucinating
python -m src.cli --role Admin --query "What is the airspeed velocity of an unladen swallow?"
```

## API

```bash
uvicorn src.api.main:app --reload

curl -s localhost:8000/health | jq .
curl -s localhost:8000/roles  | jq .

curl -s localhost:8000/query -H 'Content-Type: application/json' \
  -d '{"query":"Summarize latest audit findings.","role":"Compliance"}' | jq .

# by known user id (role inferred)
curl -s localhost:8000/query -H 'Content-Type: application/json' \
  -d '{"query":"Show finance budget allocations.","user_id":"fin_carol"}' | jq .

curl -s "localhost:8000/audit?limit=10" | jq .
```
