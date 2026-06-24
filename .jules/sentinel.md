## 2025-02-18 - [SQL Injection in SQLite Ingestion]
**Vulnerability:** `load_sql` in `src/ingestion/sql_loader.py` interpolates table and column names directly into SQL strings without proper escaping. This allowed malicious SQLite databases with crafted table or column names to execute arbitrary SQL or break parsing.
**Learning:** Even though `sqlite3` driver was connected in read-only mode (`?mode=ro`), executing a `UNION ALL` statement through string interpolation allowed an attacker to inject queries that can extract secrets from other tables or execute statements leading to denial of service. Dynamic SQL query construction must always escape literals and identifiers.
**Prevention:** I escaped single quotes (`'`) as double single quotes (`''`) for string literals and double quotes (`"`) as double double quotes (`""`) for table and column identifiers when building the `SELECT` queries string.

## 2025-02-18 - [Authorization Bypass in Role Resolution]
**Vulnerability:** `resolve_role` in `src/security/rbac.py` allowed a user to supply a `role` explicitly without verifying if the given `user_id` is actually assigned that role.
**Learning:** Any user could elevate their privileges and act as an `Admin` or any other role by passing that role in their request and bypassing the actual role assignment tied to their `user_id`.
**Prevention:** I modified the `resolve_role` logic to first look up the `user_role` from the `users` dict if `user_id` is present, and then if a `role` is requested, verify that it matches the assigned `user_role`. If it differs, a `ValueError` is raised, denying the privilege escalation.
